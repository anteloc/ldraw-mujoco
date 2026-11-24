"""Construct native MjSpec models from grouped LDraw occurrences, attached by their connections.

``import_ldraw`` works in three phases: place every occurrence and register its
meshes (``_place``), link bodies by their mated connectors (``connections.py``),
then build the bodies, parents first (``_build_bodies``). Bodies come last
because a body's parent depends on the connections of all parts.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import mujoco
import numpy as np
from ldraw import ConnectionFeature, ConnectionStatus

from .connections import body_links, forest, mated_contacts
from .geometry import BASIS, Document, check_transform, normalized, to_mujoco, vector
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
# 106-1's wheels turned 0.09 rad); at its maximum, 0.9999, 0.07 mm and 10 µrad.
HARD_FRICTION = [0.9999, 0.9999, 0.001, 0.5, 2]
# A source reflection becomes a shared X-mirrored mesh variant plus a proper rotation.
MIRROR_X = np.diag([-1.0, 1.0, 1.0])
# Visual surfaces are massless. Exported XML keeps this only on each geom: MuJoCo
# 3.5 writes neither inertiagrouprange nor a zero mass in a default class.
VISUAL_MASS = {"mass": 0, "density": 0}


@dataclass
class ImportedModel:
    """Editable spec, compiled scene, import report and part-local connector features."""

    spec: mujoco.MjSpec
    report: dict
    model: mujoco.MjModel
    connections: dict[str, tuple[ConnectionFeature, ...]]


@dataclass
class _Placement:
    """Phase 1: every occurrence placed and grouped into a future body with its geoms."""

    # Future bodies by owning instance ID: name, origin, occurrences, add_geom arguments.
    groups: dict = field(default_factory=dict)
    body_of: list = field(default_factory=list)  # Group index of each occurrence.
    occurrences: list = field(default_factory=list)  # Report rows, one per occurrence.
    metadata: dict = field(default_factory=dict)  # Connector coverage per reference.
    connections: dict = field(default_factory=dict)  # Part-local features per library DAT.
    warnings: list = field(default_factory=list)
    low: np.ndarray = field(default_factory=lambda: np.full(3, np.inf))  # Scene bounds (m).
    high: np.ndarray = field(default_factory=lambda: np.full(3, -np.inf))
    dropped_degenerate: int = 0


def inspect_ldraw(path: str | Path) -> dict:
    """List model, submodel and part IDs without building meshes or compiling physics."""
    return Document(path).inventory()


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
    placement_overrides: dict[str, str] | None = None,
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
    touching individual parts. ``placement_overrides`` maps type-1 occurrence
    IDs to replacement type-1 lines. It changes only those occurrences, leaving
    source files unchanged. The returned spec is compiled once into
    ``result.model``. Recompile after editing the spec.
    """
    path = Path(path).resolve()
    _check_options(
        solver,
        flags={"individual_parts": individual_parts, "attach": attach},
        values={
            "density": density,
            "friction": friction,
            "joint_friction": joint_friction,
            "timestep": timestep,
            "clearance": clearance,
        },
    )
    parts, library_root, shadow_paths = load_library(library, shadows, cache)
    document = Document(path, parts, sections=sections, placement_overrides=placement_overrides)
    occurrences = document.occurrences()
    if not occurrences:
        raise ValueError(f"No physical part occurrences in {path}")
    spec = _new_spec(path.stem, timestep=timestep, solver=solver, density=density, friction=friction)

    # 1. Place every occurrence and register its meshes.
    placed = _place(spec, parts, document, occurrences, individual_parts, density)
    # 2. Link bodies where pyldraw3 confirms mated connectors (see connections.py).
    # Document-local DATs have no library connectors.
    contacts = mated_contacts(parts, occurrences, skip=document.models.keys()) if attach else []
    bodies = list(placed.groups.values())
    tree, loops = forest(len(bodies), body_links(contacts, placed.body_of))
    # 3. Build bodies, parents first. One shared offset lifts the scene to the clearance.
    offset = np.array([0.0, 0.0, clearance - placed.low[2]])
    _build_bodies(spec, bodies, tree, loops, offset, joint_friction)
    # Compile here to fail before a CLI writes a successful-looking artifact.
    model = spec.compile()

    ids = [o["id"] for o in placed.occurrences]
    unlinked = _unlinked(contacts, ids)
    warnings = placed.warnings
    if individual_parts:
        warnings.append(_independence_warning(attach, len(unlinked), len(ids)))
    warnings.extend(
        {
            "code": "embedded_dat_alias",
            "reference": reference,
            "resolved_reference": target,
            "message": "Missing exact reference resolved to a unique prefixed document-local DAT",
        }
        for reference, target in document.reference_aliases.items()
    )
    body_names = {g["instance_id"]: g["name"] for g in bodies}
    body_names.update({o["id"]: o["body"] for o in placed.occurrences})
    report = {
        "source": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "placement_overrides": document.placement_overrides,
        "reference_aliases": document.reference_aliases,
        "geometry_dependencies": {
            str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(document.files)
        },
        "source_attribution": [
            {"section": m.name, "author": m.author, "license": m.license}
            for m in dict.fromkeys(document.models.values())
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
        "source_bounds_m": [placed.low.tolist(), placed.high.tolist()],
        "scene_offset_m": offset.tolist(),
        "bodies": _body_report(model, bodies, offset),
        "links": [
            _link_report(link, "tree", bodies[parent], bodies[index], ids, offset)
            for index, parent, link in tree
            if parent is not None
        ]
        + [_link_report(link, "loop", bodies[a], bodies[b], ids, offset) for a, b, link in loops],
        "connections": _connection_summary(contacts, unlinked) if attach else None,
        "occurrences": placed.occurrences,
        "connection_metadata": placed.metadata,
        "warnings": warnings,
        "dropped_degenerate_faces": placed.dropped_degenerate,
        "assumptions": _assumptions(attach, individual_parts),
    }
    return ImportedModel(spec, report, model, placed.connections)


def _check_options(solver, *, flags, values):
    for key, value in flags.items():
        if not isinstance(value, bool):
            raise ValueError(f"{key} must be a boolean")
    if solver not in SOLVERS:
        raise ValueError(f"Invalid solver: {solver!r}; use one of {', '.join(SOLVERS)}")
    for key, value in values.items():
        if not np.isfinite(value) or value < 0 or (key in {"density", "timestep"} and value == 0):
            raise ValueError(f"Invalid {key}: {value}")


def _new_spec(name, *, timestep, solver, density, friction):
    """An empty scene: options, ground, light, and default classes for part geoms.

    The ``collision`` class holds every physical assumption of a part's hull
    (group 3, the only source of mass and inertia); the ``visual`` class makes
    detailed surfaces contact-free (group 0).
    """
    spec = mujoco.MjSpec()
    spec.modelname = _name(name)
    spec.compiler.degree = False
    spec.compiler.inertiagrouprange = [3, 3]  # Only collision hulls contribute inertia.
    spec.option.timestep = timestep
    spec.option.gravity = [0, 0, -9.81]
    spec.option.solver = SOLVERS[solver]
    spec.option.enableflags |= int(mujoco.mjtEnableBit.mjENBL_ENERGY)
    # Multi-point convex contacts: one point per mesh pair cannot hold a stack.
    spec.option.enableflags |= int(mujoco.mjtEnableBit.mjENBL_MULTICCD)
    sliding = [friction, 0.005, 0.0001]

    collision = spec.add_default("collision", spec.default).geom
    collision.type = mujoco.mjtGeom.mjGEOM_MESH
    collision.group = 3
    collision.density = density
    collision.friction = sliding
    collision.condim = 3
    collision.margin = CONTACT_MARGIN
    visual = spec.add_default("visual", spec.default).geom
    visual.type = mujoco.mjtGeom.mjGEOM_MESH
    visual.group = 0
    visual.contype = 0
    visual.conaffinity = 0  # Zero mass stays on each visual geom: see VISUAL_MASS.

    spec.worldbody.add_geom(
        name="ground",
        type=mujoco.mjtGeom.mjGEOM_PLANE,
        size=[0.5, 0.5, 0.01],
        rgba=[0.24, 0.27, 0.31, 1],
        friction=sliding,
        condim=3,
    )
    spec.worldbody.add_light(name="key_light", pos=[0.2, -0.3, 0.6], dir=[-0.2, 0.3, -0.6])
    return spec


def _place(spec, parts, document, occurrences, individual_parts, density):
    """Phase 1: register each occurrence's meshes and describe its geoms in its future body."""
    placed = _Placement()
    assets = MeshAssets(spec, document)
    collision, visual = spec.find_default("collision"), spec.find_default("visual")
    palette = {}
    for index, occ in enumerate(occurrences):
        instance_id = document.occurrence_id(occ)
        reference = normalized(occ.reference)
        matrix, position = np.array(occ.matrix.rows), vector(occ.position)
        check_transform(matrix, position, occ.reference)
        rotation, bake, error = _split_transform(matrix)
        if error > 1e-5:
            placed.warnings.append(
                {
                    "code": "affine_placement",
                    "occurrence": index,
                    "instance_id": instance_id,
                    "orthogonality_error": error,
                    "message": "Source scale/shear baked into visual and collision vertices",
                }
            )
        inverted = sum(p.piece in document.inverted for p in occ.path) % 2
        reverse = (np.linalg.det(matrix) < 0) != bool(inverted)
        meshes = assets.get(reference, bake, reverse)
        quat = np.empty(4)
        mujoco.mju_mat2Quat(quat, rotation.ravel())
        position_m = to_mujoco(position)
        vertices = meshes.bounds_points @ rotation.T + position_m
        bounds = np.array([vertices.min(axis=0), vertices.max(axis=0)])
        placed.low = np.minimum(placed.low, bounds[0])
        placed.high = np.maximum(placed.high, bounds[1])

        key = instance_id if individual_parts else document.instances[instance_id]["parent_id"]
        if key not in placed.groups:
            label = document.instances[key]["reference"]
            placed.groups[key] = {
                "index": len(placed.groups),
                "name": f"body_{key.replace('/', '_')}_{_name(label)}",
                "instance_id": key,
                "source": label,
                "origin": position_m if individual_parts else _assembly_origin(occ),
                "occurrences": [],
                "geoms": [],
            }
        group = placed.groups[key]
        group["occurrences"].append(index)
        placed.body_of.append(group["index"])

        pose = {"pos": position_m - group["origin"], "quat": quat}
        prefix = f"part_{instance_id.replace('/', '_')}_{_name(occ.part_code)}"
        geoms = [
            {"name": prefix + "_collision", "meshname": meshes.collision, "default": collision}
        ]
        for number, (meshname, face_colour) in enumerate(meshes.visuals[reverse]):
            colour = occ.colour if face_colour.code == 16 else face_colour
            geoms.append(
                {
                    "name": f"{prefix}_visual_{number}",
                    "meshname": meshname,
                    "rgba": _rgba(parts, colour, palette, placed.warnings, occ.reference),
                    "default": visual,
                    **VISUAL_MASS,
                }
            )
        group["geoms"].extend({**geom, **pose} for geom in geoms)

        if reference not in placed.metadata:
            if reference in document.models:
                placed.metadata[reference] = {
                    "coverage": "not_queried",
                    "reason": "document-local part",
                }
            else:
                features, placed.metadata[reference] = _library_connections(parts, occ)
                placed.connections[reference] = features
        placed.occurrences.append(
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
                "collision_geom": geoms[0]["name"],
                "visual_geoms": [geom["name"] for geom in geoms[1:]],
                "estimated_mass_kg": meshes.volume * density,
            }
        )
    placed.dropped_degenerate = assets.surfaces.dropped_degenerate
    return placed


def _build_bodies(spec, bodies, tree, loops, offset, joint_friction):
    """Phase 3: add bodies parents first, with their joints and geoms, then loop constraints.

    Every body keeps the world orientation, so a child's frame is its parent's
    frame shifted to the child's origin.
    """
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
                    pos=to_mujoco(link.point) - group["origin"],
                    axis=BASIS @ link.axis,
                    frictionloss=joint_friction,
                    solimp_friction=HARD_FRICTION,
                )
        group.update(body=body, parent=parent, link=link)
        for geom in group["geoms"]:
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
            data=[*(to_mujoco(link.point) - first["origin"]), *[0.0] * 8],
        )
        spec.add_exclude(bodyname1=first["name"], bodyname2=second["name"])


def _name(text):
    return re.sub(r"[^a-zA-Z0-9_]+", "_", text).strip("_")[:60] or "model"


def _assembly_origin(occ):
    """The composed origin of an occurrence's containing model instance, in meters."""
    anchor, rotation = np.zeros(3), np.eye(3)
    for item in occ.path[:-1]:
        anchor += rotation @ vector(item.piece.position)
        rotation = rotation @ np.array(item.piece.matrix.rows)
    return to_mujoco(anchor)


def _split_transform(matrix):
    """Split an LDraw matrix into a MuJoCo geom rotation and the part-local mesh bake.

    A quaternion carries only a proper rotation. A reflection is baked as the
    shared X-mirror; any other non-orthogonal matrix, even a slightly distorted
    one, is baked in full. Only floating-point roundoff counts as orthogonal.
    Returns ``(rotation, bake, orthogonality_error)``.
    """
    error = float(np.max(np.abs(matrix.T @ matrix - np.eye(3))))
    if error > 1e-14:
        return np.eye(3), matrix, error
    bake = MIRROR_X if np.linalg.det(matrix) < 0 else np.eye(3)
    return BASIS @ (matrix @ bake) @ BASIS.T, bake, error


def _rgba(parts, colour, palette, warnings, reference):
    """RGBA in [0, 1] from the library's colour table, resolved once per colour."""
    if colour not in palette:
        if colour.code == 16:
            warnings.append(
                {"code": "root_colour", "message": "Unresolved root color 16 uses color 7"}
            )
        resolved = parts.resolve_colour(7 if colour.code == 16 else colour)
        if resolved.rgb is None:
            raise ValueError(f"No RGB value for color {colour.code} in {reference}")
        rgb = (channel / 255 for channel in bytes.fromhex(resolved.rgb[1:]))
        palette[colour] = (*rgb, resolved.swatch_alpha / 255)
    return palette[colour]


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


def _unlinked(contacts, ids):
    """Occurrence IDs without any confirmed connection."""
    linked = {
        i
        for c in contacts
        if c.status is ConnectionStatus.CONFIRMED
        for i in (c.first_occurrence.index, c.second_occurrence.index)
    }
    return [ident for index, ident in enumerate(ids) if index not in linked]


def _independence_warning(attach, unlinked, total):
    if attach:
        return {
            "code": "unlinked_parts",
            "message": f"{unlinked} of {total} parts have no confirmed connection and are "
            "free bodies; parts held only by undetected connections fall.",
        }
    return {
        "code": "independent_parts",
        "message": "Parts have independent free joints and no attachment constraints, so "
        "parts held only by studs fall. Hulls without studs can still overlap where "
        "parts interpenetrate in CAD and push each other apart.",
    }


def _body_report(model, bodies, offset):
    report = []
    for group in bodies:
        body = model.body(group["name"])
        report.append(
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
    return report


def _link_report(link, constraint, first, second, ids, offset):
    pairs = {
        tuple(sorted((ids[c.first_occurrence.index], ids[c.second_occurrence.index])))
        for c in link.contacts
    }
    return {
        "bodies": [first["name"], second["name"]],
        "constraint": constraint,
        "kind": link.kind,
        "anchor_m": (to_mujoco(link.point) + offset).tolist(),
        "axis": (BASIS @ link.axis).tolist() if link.kind == "hinge" else None,
        "contact_count": len(link.contacts),
        "parts": [list(pair) for pair in sorted(pairs)],
    }


def _connection_summary(contacts, unlinked):
    confirmed = [c for c in contacts if c.status is ConnectionStatus.CONFIRMED]
    return {
        "contacts": dict(Counter(c.status.value for c in contacts)),
        "kinds": dict(Counter("/".join(sorted((c.first.kind, c.second.kind))) for c in confirmed)),
        "unlinked_parts": unlinked,
    }


def _assumptions(attach, individual_parts):
    return [
        "Sections never imply attachment"
        + (
            "; bodies attach only where pyldraw3 confirms mated connectors."
            if attach
            else "; attachment is off, so every body is free."
        ),
        "One convex hull per occurrence, without studs, fills cavities; overlapping hull volumes "
        "are counted separately.",
        (
            "Mated studs, tyres on rims and axles in axle holes attach rigidly and never "
            "break (no clutch limit); a stud without a confirmed mate gives no interlock."
            if attach
            else "Studs are visual only: no lateral interlock or clutch, in any orientation "
            "(including SNOT)."
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
    ]
