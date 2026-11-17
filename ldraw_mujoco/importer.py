"""Construct native MjSpec models from explicitly grouped LDraw occurrences."""

from __future__ import annotations

import hashlib
import importlib.metadata
import re
from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np
import trimesh

from .collision import decompose
from .connections import add_bodies, add_constraints, resolve_connections
from .geometry import (
    BASIS,
    LDU_TO_METERS,
    Document,
    Surfaces,
    check_transform,
    normalized,
    triangle_mesh,
    vector,
)
from .library import load_library


@dataclass
class ImportedModel:
    """The editable native spec and JSON-serializable import evidence."""

    spec: mujoco.MjSpec
    report: dict


def inspect_ldraw(path: str | Path) -> dict:
    """List model, submodel and part IDs without building meshes or compiling physics."""
    return Document(path).inventory()


def _name(text):
    return re.sub(r"[^a-zA-Z0-9_]+", "_", text).strip("_")[:60] or "model"


def _add_mesh(spec, name, mesh, *, visual=False):
    spec.add_mesh(
        name=name,
        uservert=mesh.vertices.flatten().tolist(),
        userface=mesh.faces.flatten().tolist(),
        inertia=(
            mujoco.mjtMeshInertia.mjMESH_INERTIA_SHELL
            if visual
            else mujoco.mjtMeshInertia.mjMESH_INERTIA_CONVEX
        ),
    )


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
    placement_overrides: dict[str, str] | None = None,
    connections: str | Path | None = None,
    collision: str = "hull",
    collision_tolerance: float = 0.00005,
    contact_solref: tuple[float, float] | None = None,
    contact_solimp: tuple[float, float, float] | None = None,
) -> ImportedModel:
    """Import MPD/LDR/DAT geometry; all dimensions exposed here are SI units.

    Each model/submodel instance's direct parts share one free body. Child
    submodels are independent of their parents. ``individual_parts=True``
    instead gives every physical part its own free body, never its primitives.
    ``sections`` accepts unambiguous section names or ``section:id`` selectors.
    Repeated sections require the latter (see ``inspect_ldraw``), and the name
    must match the instance. Bare IDs are not accepted. Selection preserves full-input
    IDs, ancestor transforms and colors; overlapping selections form a union.
    ``shadows=[]`` disables external connector metadata. The returned spec is
    compiled once for validation and is still editable by the caller.
    ``placement_overrides`` maps type-1 occurrence IDs to replacement type-1
    lines. It changes only those occurrences, leaving source files unchanged.
    ``connections`` is a source-bound JSON specification and requires individual
    parts. ``collision='decomposed'`` preserves concavities using cached CoACD
    solids. Connection imports default to stiff contacts and an elliptic cone;
    their constraints are uncalibrated, permanent attachments, not clutch forces.
    """
    path = Path(path).resolve()
    if not isinstance(individual_parts, bool):
        raise ValueError("individual_parts must be a boolean")
    if connections is not None and not individual_parts:
        raise ValueError("connections requires individual_parts=True")
    if collision not in {"hull", "decomposed"}:
        raise ValueError("collision must be 'hull' or 'decomposed'")
    if not np.isfinite(collision_tolerance) or collision_tolerance <= 0:
        raise ValueError("collision_tolerance must be finite and positive")
    if contact_solref is None:
        contact_solref = (0.001, 1) if connections else (0.02, 1)
    if contact_solimp is None:
        contact_solimp = (0.95, 0.99, 0.0005) if connections else (0.9, 0.95, 0.001)
    if (len(contact_solref) != 2 or not np.isfinite(contact_solref).all()
            or min(contact_solref) <= 0):
        raise ValueError("contact_solref requires a positive time constant and damping ratio")
    if (len(contact_solimp) != 3 or not np.isfinite(contact_solimp).all()
            or not 0 < contact_solimp[0] <= contact_solimp[1] < 1 or contact_solimp[2] <= 0):
        raise ValueError("contact_solimp requires 0 < dmin <= dmax < 1 and positive width")
    solimp = [*contact_solimp, 0.5, 2]
    for key, value in {
        "density": density,
        "friction": friction,
        "timestep": timestep,
        "clearance": clearance,
    }.items():
        if not np.isfinite(value) or value < 0 or (key in {"density", "timestep"} and value == 0):
            raise ValueError(f"Invalid {key}: {value}")
    parts, library_root, shadow_paths = load_library(library, shadows, cache)
    document = Document(path, parts, sections=sections, placement_overrides=placement_overrides)
    occurrences = document.occurrences()
    if not occurrences:
        raise ValueError(f"No physical part occurrences in {path}")
    connection_report = (resolve_connections(document, occurrences, connections)
                         if connections is not None else None)
    surfaces = Surfaces(document)
    warnings, groups, placements, metadata = [], {}, [], {}
    if individual_parts and connections is None:
        warnings.append(
            {
                "code": "independent_parts",
                "message": "Parts have independent free joints and no attachment constraints. "
                "Convex hulls of assembled parts can overlap and push each other apart.",
            }
        )

    for index, occ in enumerate(occurrences):
        instance_id = document.occurrence_id(occ)
        matrix, position = np.array(occ.matrix.rows), vector(occ.position)
        check_transform(matrix, position, occ.reference)
        error = float(np.max(np.abs(matrix.T @ matrix - np.eye(3))))
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
        surface = surfaces.get(occ.reference)
        if not len(surface.triangles):
            raise ValueError(f"No surface geometry for occurrence {index}: {occ.reference}")
        triangles = (surface.triangles @ matrix.T + position) @ BASIS.T * LDU_TO_METERS
        inversion = sum(id(p.piece) in document.inverted for p in occ.path) % 2
        if (np.linalg.det(matrix) < 0) != bool(inversion):
            triangles = triangles[:, ::-1]
        if individual_parts:
            key = instance_id
            origin = position @ BASIS.T * LDU_TO_METERS
        else:
            # Only direct parts belong to this assembly; nested assemblies get
            # their own world-parented free bodies, with no inter-body welds.
            key = document.instances[instance_id]["parent_id"]
            anchor, rotation = np.zeros(3), np.eye(3)
            for item in occ.path[:-1]:
                anchor += rotation @ vector(item.piece.position)
                rotation = rotation @ np.array(item.piece.matrix.rows)
            origin = anchor @ BASIS.T * LDU_TO_METERS
        if key not in groups:
            label = document.instances[key]["reference"]
            groups[key] = {
                "name": f"body_{key.replace('/', '_')}_{_name(label)}",
                "instance_id": key,
                "source": label,
                "origin": origin,
                "occurrences": [],
            }
        groups[key]["occurrences"].append(index)
        placements.append((occ, surface, triangles, key))

        reference = normalized(occ.reference)
        if reference not in metadata:
            if reference in document.models:
                metadata[reference] = {"coverage": "not_queried", "reason": "document-local part"}
            else:
                evidence = parts.geometry(occ.part_code)
                diagnostics = [d.to_dict() for d in evidence.diagnostics]
                errors = [
                    d
                    for d in diagnostics
                    if not (d["severity"] == "warning" and d["code"].startswith("connection."))
                ]
                if errors:
                    raise ValueError(f"Incomplete geometry for {occ.reference}: {errors}")
                metadata_report = evidence.connection_metadata
                metadata[reference] = {
                    "feature_count": len(evidence.connections),
                    "coverage": str(metadata_report.coverage) if metadata_report else "none",
                    "source_count": metadata_report.source_count if metadata_report else 0,
                    "recognized_record_count": metadata_report.recognized_record_count
                    if metadata_report
                    else 0,
                    "diagnostics": diagnostics,
                }

    bounds = np.array(
        [
            np.min([p[2].min(axis=(0, 1)) for p in placements], axis=0),
            np.max([p[2].max(axis=(0, 1)) for p in placements], axis=0),
        ]
    )
    offset = np.array([0.0, 0.0, clearance - bounds[0, 2]])
    spec = mujoco.MjSpec()
    spec.modelname = _name(path.stem)
    spec.compiler.degree = False
    spec.compiler.inertiagrouprange = [3, 3]  # Only collision hulls contribute inertia.
    spec.option.timestep = timestep
    spec.option.gravity = [0, 0, -9.81]
    spec.option.enableflags |= int(mujoco.mjtEnableBit.mjENBL_ENERGY)
    spec.default.geom.solref = contact_solref
    spec.default.geom.solimp = solimp
    if connections:
        spec.option.cone = mujoco.mjtCone.mjCONE_ELLIPTIC
        # Native hinge parents must still collide with their mounted wheels.
        spec.option.disableflags |= int(mujoco.mjtDisableBit.mjDSBL_FILTERPARENT)
    spec.worldbody.add_geom(
        name="ground",
        type=mujoco.mjtGeom.mjGEOM_PLANE,
        size=[0.5, 0.5, 0.01],
        rgba=[0.24, 0.27, 0.31, 1],
        friction=[friction, 0.005, 0.0001],
        condim=3,
    )
    spec.worldbody.add_light(name="key_light", pos=[0.2, -0.3, 0.6], dir=[-0.2, 0.3, -0.6])
    add_bodies(spec, groups, offset, connection_report)
    if connection_report is not None:
        add_constraints(spec, groups, connection_report, contact_solref, solimp)

    occurrence_report = []
    decompositions = {}
    for index, (occ, surface, triangles, key) in enumerate(placements):
        group = groups[key]
        local = triangles - group["origin"]
        instance_id = document.occurrence_id(occ)
        prefix = f"part_{instance_id.replace('/', '_')}_{_name(occ.part_code)}"
        try:
            if collision == "hull":
                hulls = [trimesh.convex.convex_hull(local.reshape(-1, 3))]
            else:
                reference = normalized(occ.reference)
                if reference not in decompositions:
                    decompositions[reference] = decompose(
                        surface.triangles, cache=cache, tolerance=collision_tolerance,
                    )
                source_hulls, _ = decompositions[reference]
                transform = np.eye(4)
                transform[:3, :3] = BASIS @ np.array(occ.matrix.rows)
                transform[:3, 3] = (BASIS @ vector(occ.position) * LDU_TO_METERS
                                        - group["origin"])
                hulls = [h.copy().apply_transform(transform) for h in source_hulls]
        except Exception as exc:
            raise ValueError(f"Cannot build {collision} collision geometry for {occ.reference}: {exc}") from exc
        collision_names = []
        for number, hull in enumerate(hulls):
            name = prefix + "_collision" + (f"_{number}" if collision == "decomposed" else "")
            collision_names.append(name)
            _add_mesh(spec, name + "_mesh", hull)
            group["body"].add_geom(
                name=name, type=mujoco.mjtGeom.mjGEOM_MESH, meshname=name + "_mesh",
                group=3, density=density, friction=[friction, 0.005, 0.0001], condim=3,
            )
        colour_groups = {}
        for face_index, colour in enumerate(surface.colours):
            if colour.code == 16:
                colour = occ.colour
            if colour.code == 16:
                colour = parts.resolve_colour(7)
                if not any(w["code"] == "root_colour" for w in warnings):
                    warnings.append(
                        {"code": "root_colour", "message": "Unresolved root color 16 uses color 7"}
                    )
            colour = parts.resolve_colour(colour)
            if colour.rgb is None:
                raise ValueError(f"No RGB value for color {colour.code} in {occ.reference}")
            rgba = tuple(int(colour.rgb[i : i + 2], 16) / 255 for i in (1, 3, 5)) + (
                colour.swatch_alpha / 255,
            )
            colour_groups.setdefault(rgba, []).append(face_index)
        visuals = []
        for number, (rgba, face_indices) in enumerate(colour_groups.items()):
            name = f"{prefix}_visual_{number}"
            mesh = triangle_mesh(local[face_indices])
            _add_mesh(spec, name + "_mesh", mesh, visual=True)
            group["body"].add_geom(
                name=name,
                type=mujoco.mjtGeom.mjGEOM_MESH,
                meshname=name + "_mesh",
                rgba=rgba,
                mass=0,
                density=0,
                contype=0,
                conaffinity=0,
                group=0,
            )
            visuals.append(name)
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
                "position_ldu": vector(occ.position).tolist(),
                "bounds_m": [
                    triangles.min(axis=(0, 1)).tolist(),
                    triangles.max(axis=(0, 1)).tolist(),
                ],
                **({"collision_geom": collision_names[0]} if collision == "hull" else {}),
                "collision_geoms": collision_names,
                "visual_geoms": visuals,
                "estimated_mass_kg": float(sum(h.volume for h in hulls) * density),
            }
        )

    # Compile here to fail before a CLI writes a successful-looking artifact.
    model = spec.compile()
    initial_data = mujoco.MjData(model)
    mujoco.mj_forward(model, initial_data)
    body_report = []
    for group in groups.values():
        body = model.body(group["name"])
        body_report.append(
            {
                "name": group["name"],
                "instance_id": group["instance_id"],
                "source": group["source"],
                "occurrence_count": len(group["occurrences"]),
                "initial_position_m": initial_data.xpos[body.id].tolist(),
                "estimated_mass_kg": float(body.mass[0]),
                "inertia_kg_m2": body.inertia.tolist(),
            }
        )
    body_names = {g["instance_id"]: g["name"] for g in groups.values()}
    body_names.update({o["id"]: o["body"] for o in occurrence_report})
    warnings.extend(
        {
            "code": "embedded_dat_alias",
            "reference": reference,
            "resolved_reference": target,
            "message": "Missing exact reference resolved to a unique prefixed document-local DAT",
        }
        for reference, target in document.reference_aliases.items()
    )
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
        "options": {
            "density_kg_m3": density,
            "sliding_friction": friction,
            "timestep_s": timestep,
            "ground_clearance_m": clearance,
            "collision": collision,
            "collision_tolerance_m": collision_tolerance if collision == "decomposed" else None,
            "contact_solref": list(contact_solref),
            "contact_solimp": solimp,
            "cone": "elliptic" if connections else "pyramidal",
        },
        "coordinate_mapping": "0.0004 * (x, z, -y)",
        "source_bounds_m": bounds.tolist(),
        "scene_offset_m": offset.tolist(),
        "bodies": body_report,
        "occurrences": occurrence_report,
        "connection_metadata": metadata,
        "attachments": connection_report,
        "collision_decompositions": {k: v[1] for k, v in decompositions.items()},
        "warnings": warnings,
        "dropped_degenerate_faces": surfaces.dropped_degenerate,
        "assumptions": [
            ("Confirmed connector evidence and explicit exceptions define permanent attachments."
             if connections else "Rigid grouping is user-selected, not inferred from connectors."),
            ("CoACD compound solids approximate cavities; preprocessing error and overlapping volumes are uncalibrated."
             if collision == "decomposed" else
             "One convex hull per occurrence fills cavities; overlapping hull volumes are counted separately."),
            "Mass, inertia and friction are uncalibrated estimates; all parts use the selected density.",
            (
                "Fixed welds and passive hinges approximate attachments; no calibrated clutch release or bearing friction."
                if connections else
                "Each physical part is free; there are no welds, clutch forces or articulated connections."
                if individual_parts
                else "Each assembly's direct parts are welded; child assemblies remain independent."
            ),
        ],
    }
    return ImportedModel(spec, report)
