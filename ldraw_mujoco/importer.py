"""Construct native MjSpec models from explicitly grouped LDraw occurrences."""

from __future__ import annotations

import hashlib
import importlib.metadata
import re
from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np
from ldraw import ConnectionFeature

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
    density: float = 1050.0,
    friction: float = 0.6,
    timestep: float = 0.001,
    clearance: float = 0.001,
    solver: str = "newton",
) -> ImportedModel:
    """Import MPD/LDR/DAT geometry; all dimensions exposed here are SI units.

    Each model/submodel instance's direct parts share one free body. Child
    submodels are independent of their parents. ``individual_parts=True``
    instead gives every physical part its own free body, never its primitives.
    ``sections`` accepts unambiguous section names or ``section:id`` selectors.
    Repeated sections require the latter (see ``inspect_ldraw``), and the name
    must match the instance. Bare IDs are not accepted. Selection preserves full-input
    IDs, ancestor transforms and colors; overlapping selections form a union.
    ``shadows=[]`` disables external connector metadata. ``solver`` is one of
    ``SOLVERS``; use ``"cg"`` for thousands of touching individual parts. The
    returned spec is compiled once into ``result.model``. Recompile after editing
    the spec.
    """
    path = Path(path).resolve()
    if not isinstance(individual_parts, bool):
        raise ValueError("individual_parts must be a boolean")
    if solver not in SOLVERS:
        raise ValueError(f"Invalid solver: {solver!r}; use one of {', '.join(SOLVERS)}")
    for key, value in {
        "density": density,
        "friction": friction,
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
    assets = MeshAssets(spec, document)
    groups, metadata, connections = {}, {}, {}
    occurrence_report, warnings = [], []
    if individual_parts:
        warnings.append(
            {
                "code": "independent_parts",
                "message": "Parts have independent free joints and no attachment constraints, "
                "so parts held only by studs fall. Hulls without studs can still overlap "
                "where parts interpenetrate in CAD and push each other apart.",
            }
        )
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
            origin = position_m if individual_parts else _assembly_origin(occ)
            name = f"body_{key.replace('/', '_')}_{_name(label)}"
            body = spec.worldbody.add_body(name=name, pos=origin)
            body.add_freejoint(name=name + "_free")
            groups[key] = {
                "name": name,
                "instance_id": key,
                "source": label,
                "origin": origin,
                "occurrence_count": 0,
                "body": body,
            }
        group = groups[key]
        group["occurrence_count"] += 1
        local_position = position_m - group["origin"]
        prefix = f"part_{instance_id.replace('/', '_')}_{_name(occ.part_code)}"
        collision = prefix + "_collision"
        group["body"].add_geom(
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
            group["body"].add_geom(
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
            visuals.append(name)
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

    offset = np.array([0.0, 0.0, clearance - low[2]])
    for group in groups.values():
        group["body"].pos = group["origin"] + offset

    # Compile here to fail before a CLI writes a successful-looking artifact.
    model = spec.compile()
    body_report = []
    for group in groups.values():
        body = model.body(group["name"])
        body_report.append(
            {
                "name": group["name"],
                "instance_id": group["instance_id"],
                "source": group["source"],
                "occurrence_count": group["occurrence_count"],
                "initial_position_m": body.pos.tolist(),
                "estimated_mass_kg": float(body.mass[0]),
                "inertia_kg_m2": body.inertia.tolist(),
            }
        )
    body_names = {g["instance_id"]: g["name"] for g in groups.values()}
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
            "density_kg_m3": density,
            "sliding_friction": friction,
            "timestep_s": timestep,
            "ground_clearance_m": clearance,
            "solver": solver,
            "contact_margin_m": CONTACT_MARGIN,
        },
        "coordinate_mapping": "0.0004 * (x, z, -y)",
        "source_bounds_m": [low.tolist(), high.tolist()],
        "scene_offset_m": offset.tolist(),
        "bodies": body_report,
        "occurrences": occurrence_report,
        "connection_metadata": metadata,
        "warnings": warnings,
        "dropped_degenerate_faces": assets.surfaces.dropped_degenerate,
        "assumptions": [
            "Rigid grouping is user-selected, not inferred from connectors.",
            "One convex hull per occurrence, without studs, fills cavities; overlapping hull volumes are counted separately.",
            "Studs are visual only: no lateral interlock or clutch, in any orientation (including SNOT).",
            "Hull contacts use multi-point collision (multiccd) and start within the contact margin.",
            "Mass, inertia and friction are uncalibrated estimates; all parts use the selected density.",
            (
                "Each physical part is free; there are no welds, clutch forces or articulated connections."
                if individual_parts
                else "Each assembly's direct parts are welded; child assemblies remain independent."
            ),
        ],
    }
    return ImportedModel(spec, report, model, connections)
