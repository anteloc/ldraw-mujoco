"""Construct native MjSpec models from grouped LDraw occurrences, attached by their connections."""

from __future__ import annotations

import hashlib
import importlib.metadata
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np
from ldraw import ConnectionFeature, ConnectionStatus

from .connections import body_links, forest, mated_contacts
from .geometry import (
    BASIS,
    LDU_TO_METERS,
    Document,
    check_transform,
    normalized,
    vector,
)
from .library import load_library
from .meshes import MeshAssets

# MuJoCo's constraint solvers by their MJCF names. Newton suits most scenes; CG
# scales far better when thousands of touching parts form one contact island.
SOLVERS = {
    "newton": mujoco.mjtSolver.mjSOL_NEWTON,
    "cg": mujoco.mjtSolver.mjSOL_CG,
    "pgs": mujoco.mjtSolver.mjSOL_PGS,
}
# Hull contacts start 0.2 mm before touching. With multiccd, flat mesh faces then
# keep several contact points, so stacked parts rest instead of sinking into each other.
CONTACT_MARGIN = 0.0002
# Joints of articulated links. A rigid link nests a body without any joint.
JOINTS = {"hinge": mujoco.mjtJoint.mjJNT_HINGE, "ball": mujoco.mjtJoint.mjJNT_BALL}
# Joint friction holds a pose only as a hard constraint. At MuJoCo's default
# impedance (0.9) a loaded hinge creeps (a 12 cm beam's tip: 72 mm in 5 s, and
# 106-1's wheels turned 0.09 rad); at its maximum, 0.9999, 0.07 mm and 7 µrad.
HARD_FRICTION = [0.9999, 0.9999, 0.001, 0.5, 2]


@dataclass
class ImportedModel:
    """Editable spec, compiled scene, import report and part-local connector features."""

    spec: mujoco.MjSpec
    report: dict
    model: mujoco.MjModel
    connections: dict[str, tuple[ConnectionFeature, ...]]


def inspect_ldraw(path: str | Path) -> dict:
    """List model, submodel and part IDs without building meshes or compiling physics."""
    return Document(path).inventory()


def _name(text):
    return re.sub(r"[^a-zA-Z0-9_]+", "_", text).strip("_")[:60] or "model"


def _assembly_origin(occ):
    anchor, rotation = np.zeros(3), np.eye(3)
    for item in occ.path[:-1]:
        anchor += rotation @ vector(item.piece.position)
        rotation = rotation @ np.array(item.piece.matrix.rows)
    return BASIS @ anchor * LDU_TO_METERS


def _meters(point):
    """An LDraw point (LDU) in import coordinates, before the ground offset."""
    return BASIS @ point * LDU_TO_METERS


def _library_connections(parts, occ):
    evidence = parts.geometry(occ.part_code)
    diagnostics = [d.to_dict() for d in evidence.diagnostics]
    errors = [
        d
        for d in diagnostics
        if not (d["severity"] == "warning" and d["code"].startswith("connection."))
    ]
    if errors:
        raise ValueError(f"Incomplete geometry for {occ.reference}: {errors}")
    report = evidence.connection_metadata
    return evidence.connections, {
        "feature_count": len(evidence.connections),
        "coverage": str(report.coverage) if report else "none",
        "source_count": report.source_count if report else 0,
        "recognized_record_count": report.recognized_record_count if report else 0,
        "diagnostics": diagnostics,
    }


def import_ldraw(
    path: str | Path,
    *,
    library: str | Path | None = None,
    shadows=None,
    cache: str | Path | None = None,
    sections: str | list[str] | None = None,
    individual_parts: bool = False,
    attach: bool = True,
    density: float = 1050.0,
    friction: float = 0.6,
    joint_friction: float = 0.01,
    timestep: float = 0.001,
    clearance: float = 0.001,
    solver: str = "newton",
) -> ImportedModel:
    """Import MPD/LDR/DAT geometry; all dimensions exposed here are SI units.

    Each model/submodel instance's direct parts share one body.
    ``individual_parts=True`` instead gives every physical part its own body,
    never its primitives. With ``attach`` (the default), bodies joined by
    connectors that pyldraw3 confirms as mated are nested: studs, tyres and
    axles in axle holes attach rigidly; pins, clips and finger hinges become
    hinge joints and ball sockets ball joints, held by ``joint_friction``
    (N·m; 0 lets them swing). Other bodies, and all with ``attach=False``, are
    free. ``sections`` accepts unambiguous section names or ``section:id``
    selectors. Repeated sections require the latter (see ``inspect_ldraw``),
    and the name must match the instance. Bare IDs are not accepted. Selection
    preserves full-input IDs, ancestor transforms and colors; overlapping
    selections form a union. ``shadows=[]`` disables external connector
    metadata. ``solver`` is one of ``SOLVERS``; use ``"cg"`` for thousands of
    touching individual parts. The returned spec is compiled once into
    ``result.model``. Recompile after editing the spec.
    """
    path = Path(path).resolve()
    for key, value in {"individual_parts": individual_parts, "attach": attach}.items():
        if not isinstance(value, bool):
            raise ValueError(f"{key} must be a boolean")
    if solver not in SOLVERS:
        raise ValueError(f"Invalid solver: {solver!r}; use one of {', '.join(SOLVERS)}")
    for key, value in {
        "density": density,
        "friction": friction,
        "joint_friction": joint_friction,
        "timestep": timestep,
        "clearance": clearance,
    }.items():
        if not np.isfinite(value) or value < 0 or (key in {"density", "timestep"} and value == 0):
            raise ValueError(f"Invalid {key}: {value}")
    parts, library_root, shadow_paths = load_library(library, shadows, cache)
    document = Document(path, parts, sections=sections)
    occurrences = document.occurrences()
    if not occurrences:
        raise ValueError(f"No physical part occurrences in {path}")
    spec = mujoco.MjSpec()
    spec.modelname = _name(path.stem)
    spec.compiler.degree = False
    spec.compiler.inertiagrouprange = [3, 3]  # Only collision hulls contribute inertia.
    spec.option.timestep = timestep
    spec.option.gravity = [0, 0, -9.81]
    spec.option.solver = SOLVERS[solver]
    spec.option.enableflags |= int(mujoco.mjtEnableBit.mjENBL_ENERGY)
    # Multi-point convex contacts: one point per mesh pair cannot hold a stack.
    spec.option.enableflags |= int(mujoco.mjtEnableBit.mjENBL_MULTICCD)
    spec.worldbody.add_geom(
        name="ground",
        type=mujoco.mjtGeom.mjGEOM_PLANE,
        size=[0.5, 0.5, 0.01],
        rgba=[0.24, 0.27, 0.31, 1],
        friction=[friction, 0.005, 0.0001],
        condim=3,
    )
    spec.worldbody.add_light(name="key_light", pos=[0.2, -0.3, 0.6], dir=[-0.2, 0.3, -0.6])

    # 1. Place every occurrence and register its meshes. Bodies come later: a
    # body's parent depends on the connections of all parts.
    assets = MeshAssets(spec, document)
    groups, metadata, connections = {}, {}, {}
    occurrence_report, warnings, geoms, body_of = [], [], [], []
    low, high = np.full(3, np.inf), np.full(3, -np.inf)
    palette = {}
    identity = np.eye(3)
    reflection = np.diag([-1.0, 1.0, 1.0])
    for index, occ in enumerate(occurrences):
        instance_id = document.occurrence_id(occ)
        reference = normalized(occ.reference)
        matrix, position = np.array(occ.matrix.rows), vector(occ.position)
        check_transform(matrix, position, occ.reference)
        mirrored = np.linalg.det(matrix) < 0
        error = float(np.max(np.abs(matrix.T @ matrix - identity)))
        # A quaternion can carry only a proper rotation. Preserve even small
        # source distortions in the asset, apart from floating-point roundoff.
        if error <= 1e-14:
            bake = reflection if mirrored else identity
            rotation = BASIS @ (matrix @ bake) @ BASIS.T
        else:
            bake, rotation = matrix, identity
        if error > 1e-5:
            warnings.append(
                {
                    "code": "affine_placement",
                    "occurrence": index,
                    "instance_id": instance_id,
                    "orthogonality_error": error,
                    "message": "Source scale/shear baked into visual and collision vertices",
                }
            )
        inverted = sum(id(p.piece) in document.inverted for p in occ.path) % 2
        reverse = mirrored != bool(inverted)
        meshes = assets.get(reference, bake, reverse)
        quat = np.empty(4)
        mujoco.mju_mat2Quat(quat, rotation.ravel())
        position_m = BASIS @ position * LDU_TO_METERS
        vertices = meshes.bounds_points @ rotation.T + position_m
        bounds = np.array([vertices.min(axis=0), vertices.max(axis=0)])
        low, high = np.minimum(low, bounds[0]), np.maximum(high, bounds[1])

        key = instance_id if individual_parts else document.instances[instance_id]["parent_id"]
        if key not in groups:
            label = document.instances[key]["reference"]
            groups[key] = {
                "index": len(groups),
                "name": f"body_{key.replace('/', '_')}_{_name(label)}",
                "instance_id": key,
                "source": label,
                "origin": position_m if individual_parts else _assembly_origin(occ),
                "occurrences": [],
            }
        group = groups[key]
        group["occurrences"].append(index)
        body_of.append(group["index"])
        local_position = position_m - group["origin"]
        prefix = f"part_{instance_id.replace('/', '_')}_{_name(occ.part_code)}"
        collision = prefix + "_collision"
        part_geoms = [
            dict(
                name=collision,
                type=mujoco.mjtGeom.mjGEOM_MESH,
                meshname=meshes.collision,
                pos=local_position,
                quat=quat,
                group=3,
                density=density,
                friction=[friction, 0.005, 0.0001],
                condim=3,
                margin=CONTACT_MARGIN,
            )
        ]
        visuals = []
        for number, (meshname, face_colour) in enumerate(meshes.visuals[reverse]):
            colour = occ.colour if face_colour.code == 16 else face_colour
            if colour not in palette:
                if colour.code == 16:
                    warnings.append(
                        {"code": "root_colour", "message": "Unresolved root color 16 uses color 7"}
                    )
                resolved = parts.resolve_colour(7 if colour.code == 16 else colour)
                if resolved.rgb is None:
                    raise ValueError(f"No RGB value for color {colour.code} in {occ.reference}")
                palette[colour] = tuple(
                    int(resolved.rgb[i : i + 2], 16) / 255 for i in (1, 3, 5)
                ) + (resolved.swatch_alpha / 255,)
            name = f"{prefix}_visual_{number}"
            part_geoms.append(
                dict(
                    name=name,
                    type=mujoco.mjtGeom.mjGEOM_MESH,
                    meshname=meshname,
                    pos=local_position,
                    quat=quat,
                    rgba=palette[colour],
                    mass=0,
                    density=0,
                    contype=0,
                    conaffinity=0,
                    group=0,
                )
            )
            visuals.append(name)
        geoms.append(part_geoms)
        if reference not in metadata:
            if reference in document.models:
                metadata[reference] = {"coverage": "not_queried", "reason": "document-local part"}
            else:
                connections[reference], metadata[reference] = _library_connections(parts, occ)

        occurrence_report.append(
            {
                "index": index,
                "id": instance_id,
                "parent_id": document.instances[instance_id]["parent_id"],
                "reference": occ.reference,
                "body": group["name"],
                "colour": occ.colour.code if occ.colour.code is not None else occ.colour.rgb,
                "source_path": [
                    {"section": p.model.name, "line": p.source_line, "reference": p.piece.reference}
                    for p in occ.path
                ],
                "matrix_ldraw": occ.matrix.rows,
                "position_ldu": position.tolist(),
                "bounds_m": bounds.tolist(),
                "collision_geom": collision,
                "visual_geoms": visuals,
                "estimated_mass_kg": meshes.volume * density,
            }
        )

    # 2. Link bodies where pyldraw3 confirms mated connectors (see connections.py).
    # Document-local DATs have no library connectors.
    contacts = mated_contacts(parts, occurrences, skip=document.models.keys()) if attach else []
    bodies = list(groups.values())
    tree, loops = forest(len(bodies), body_links(contacts, body_of))

    # 3. Build bodies, parents first. Every body keeps the world orientation,
    # so a child's frame is its parent's frame shifted to the child's origin.
    offset = np.array([0.0, 0.0, clearance - low[2]])
    for index, parent, link in tree:
        group = bodies[index]
        if parent is None:
            body = spec.worldbody.add_body(name=group["name"], pos=group["origin"] + offset)
            body.add_freejoint(name=group["name"] + "_free")
        else:
            above = bodies[parent]
            body = above["body"].add_body(name=group["name"], pos=group["origin"] - above["origin"])
            if link.kind in JOINTS:
                body.add_joint(
                    name=f"{group['name']}_{link.kind}",
                    type=JOINTS[link.kind],
                    pos=_meters(link.point) - group["origin"],
                    axis=BASIS @ link.axis,
                    frictionloss=joint_friction,
                    solimp_friction=HARD_FRICTION,
                )
        group.update(body=body, parent=parent, link=link)
        for occurrence in group["occurrences"]:
            for geom in geoms[occurrence]:
                body.add_geom(**geom)
    for number, (a, b, link) in enumerate(loops):
        # A joint that closes a loop pins both bodies together at its anchor.
        first, second = bodies[a], bodies[b]
        spec.add_equality(
            name=f"loop_{number}",
            type=mujoco.mjtEq.mjEQ_CONNECT,
            objtype=mujoco.mjtObj.mjOBJ_BODY,
            name1=first["name"],
            name2=second["name"],
            data=[*(_meters(link.point) - first["origin"]), *[0.0] * 8],
        )
        spec.add_exclude(bodyname1=first["name"], bodyname2=second["name"])

    ids = [o["id"] for o in occurrence_report]
    confirmed = [c for c in contacts if c.status is ConnectionStatus.CONFIRMED]
    linked = {i for c in confirmed for i in (c.first_occurrence.index, c.second_occurrence.index)}
    unlinked = [ids[i] for i in range(len(ids)) if i not in linked]
    if individual_parts:
        warnings.append(
            {
                "code": "unlinked_parts" if attach else "independent_parts",
                "message": (
                    f"{len(unlinked)} of {len(ids)} parts have no confirmed connection and are "
                    "free bodies; parts held only by undetected connections fall."
                    if attach
                    else "Parts have independent free joints and no attachment constraints, so "
                    "parts held only by studs fall. Hulls without studs can still overlap where "
                    "parts interpenetrate in CAD and push each other apart."
                ),
            }
        )

    def link_report(link, constraint, first, second):
        pairs = {
            tuple(sorted((ids[c.first_occurrence.index], ids[c.second_occurrence.index])))
            for c in link.contacts
        }
        return {
            "bodies": [first["name"], second["name"]],
            "constraint": constraint,
            "kind": link.kind,
            "anchor_m": (_meters(link.point) + offset).tolist(),
            "axis": (BASIS @ link.axis).tolist() if link.kind == "hinge" else None,
            "contact_count": len(link.contacts),
            "parts": [list(pair) for pair in sorted(pairs)],
        }

    # Compile here to fail before a CLI writes a successful-looking artifact.
    model = spec.compile()
    body_report = []
    for group in bodies:
        body = model.body(group["name"])
        body_report.append(
            {
                "name": group["name"],
                "instance_id": group["instance_id"],
                "source": group["source"],
                "parent": None if group["parent"] is None else bodies[group["parent"]]["name"],
                "joint": "free" if group["link"] is None else group["link"].kind,
                "occurrence_count": len(group["occurrences"]),
                "initial_position_m": (group["origin"] + offset).tolist(),
                "estimated_mass_kg": float(body.mass[0]),
                "inertia_kg_m2": body.inertia.tolist(),
            }
        )
    body_names = {g["instance_id"]: g["name"] for g in bodies}
    body_names.update({o["id"]: o["body"] for o in occurrence_report})
    report = {
        "source": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "geometry_dependencies": {
            str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(document.files)
        },
        "source_attribution": [
            {"section": m.name, "author": m.author, "license": m.license}
            for m in {id(m): m for m in document.models.values()}.values()
        ],
        "versions": {
            p: importlib.metadata.version(p) for p in ("pyldraw3", "mujoco", "trimesh", "numpy")
        },
        "library": str(library_root),
        "shadows": shadow_paths,
        "individual_parts": individual_parts,
        "selected_instances": document.selected_ids,
        "available_sections": document.available_sections,
        "instances": [
            {**node, "body": body_names.get(node["id"])}
            for node in document.instances.values()
            if document.included(node["id"])
        ],
        "occurrence_count": len(occurrences),
        "unique_parts": len({normalized(o.reference) for o in occurrences}),
        "nq": model.nq,
        "nv": model.nv,
        "nbody": model.nbody,
        "nmesh": model.nmesh,
        "options": {
            "attach": attach,
            "density_kg_m3": density,
            "sliding_friction": friction,
            "joint_friction_n_m": joint_friction,
            "timestep_s": timestep,
            "ground_clearance_m": clearance,
            "solver": solver,
            "contact_margin_m": CONTACT_MARGIN,
        },
        "coordinate_mapping": "0.0004 * (x, z, -y)",
        "source_bounds_m": [low.tolist(), high.tolist()],
        "scene_offset_m": offset.tolist(),
        "bodies": body_report,
        "links": [
            link_report(link, "tree", bodies[parent], bodies[index])
            for index, parent, link in tree
            if parent is not None
        ]
        + [link_report(link, "loop", bodies[a], bodies[b]) for a, b, link in loops],
        "connections": (
            {
                "contacts": dict(Counter(c.status.value for c in contacts)),
                "kinds": dict(
                    Counter("/".join(sorted((c.first.kind, c.second.kind))) for c in confirmed)
                ),
                "unlinked_parts": unlinked,
            }
            if attach
            else None
        ),
        "occurrences": occurrence_report,
        "connection_metadata": metadata,
        "warnings": warnings,
        "dropped_degenerate_faces": assets.surfaces.dropped_degenerate,
        "assumptions": [
            "Sections never imply attachment"
            + (
                "; bodies attach only where pyldraw3 confirms mated connectors."
                if attach
                else "; attachment is off, so every body is free."
            ),
            "One convex hull per occurrence, without studs, fills cavities; overlapping hull volumes are counted separately.",
            (
                "Mated studs, tyres on rims and axles in axle holes attach rigidly and never "
                "break (no clutch limit); a stud without a confirmed mate gives no interlock."
                if attach
                else "Studs are visual only: no lateral interlock or clutch, in any orientation (including SNOT)."
            ),
            *(
                [
                    "Pins, clips and finger hinges turn about their axis, ball sockets about "
                    "their center, against one uncalibrated friction torque; LDCad slide hints "
                    "are ignored.",
                    "A jointed body does not collide with its parent body or the bodies "
                    "rigidly attached to it (MuJoCo's parent filter).",
                ]
                if attach
                else []
            ),
            "Hull contacts use multi-point collision (multiccd) and start within the contact margin.",
            "Mass, inertia and friction are uncalibrated estimates; all parts use the selected density.",
            (
                "Each physical part is its own body."
                if individual_parts
                else "Each assembly's direct parts are welded into one body."
            ),
        ],
    }
    return ImportedModel(spec, report, model, connections)
