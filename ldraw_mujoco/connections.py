"""Map pyldraw3 evidence and reviewed exceptions to native MuJoCo constraints."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

import mujoco
import networkx as nx
import numpy as np
from ldraw.inspection import inspect_model

from .geometry import BASIS, LDU_TO_METERS, vector


def _pair(first, second):
    return tuple(sorted((first, second)))


def _vector(value, label):
    result = np.asarray(value, dtype=float)
    if result.shape != (3,) or not np.isfinite(result).all():
        raise ValueError(f"{label} must contain three finite numbers")
    return result


def resolve_connections(document, occurrences, path):
    """Resolve before constructing bodies; unknown interfaces remain unresolved.

    Anchor coordinates are meters in the converted full-input frame, before the
    importer's ground offset. An override's first body is a hinge's parent.
    """
    config_path = Path(path)
    config = json.loads(config_path.read_text())
    if config.get("source_sha256") != hashlib.sha256(document.path.read_bytes()).hexdigest():
        raise ValueError("Connection specification source_sha256 does not match the input")
    if document.placement_overrides:
        raise ValueError("Connection specifications cannot be combined with placement_overrides")
    if not isinstance(config.get("infer", True), bool):
        raise ValueError("Connection specification infer must be a boolean")
    ids = [document.occurrence_id(o) for o in occurrences]
    selected = set(ids)
    evidence, resolved = {}, {}
    inspection = inspect_model(document.view, document.parts, occurrences=occurrences)
    for contact in inspection.connection_contacts():
        a, b = ids[contact.first_occurrence.index], ids[contact.second_occurrence.index]
        key = _pair(a, b)
        features = (contact.first, contact.second)
        item = {
            "first": a, "second": b, "status": str(contact.status),
            "features": [
                {"id": f.feature_id, "kind": str(f.kind), "source": str(f.source),
                 "freedoms": sorted(f.freedoms), "provenance": list(f.provenance)}
                for f in features
            ],
            "residual_ldu": asdict(contact.residual),
            "anchor_m": (BASIS @ vector(contact.first.position) * LDU_TO_METERS).tolist(),
            "axis": (BASIS @ vector(contact.first.axis)).tolist(),
        }
        evidence.setdefault(key, []).append(item)
        kinds = {str(f.kind) for f in features}
        if config.get("infer", True) and str(contact.status) == "confirmed" and kinds in (
            {"stud", "stud_receptacle"}, {"rim_seat", "tyre_bead"},
        ):
            resolved[key] = {
                "first": key[0], "second": key[1], "kind": "fixed",
                "reason": "Confirmed stud fit" if "stud" in kinds else
                "Confirmed tyre/rim fit; tyre slip is locked for this approximation",
                "source": "inferred", "exclude_contact": False,
            }
    omitted, overridden = [], set()
    for override in config.get("overrides", []):
        a, b = override.get("first"), override.get("second")
        for ident in (a, b):
            if ident not in document.instances or document.instances[ident]["kind"] != "part":
                raise ValueError(f"Connection endpoint must identify a physical part: {ident!r}")
        key = _pair(a, b)
        if a == b or key in overridden:
            raise ValueError(f"Duplicate or self connection override: {key}")
        overridden.add(key)
        kind, reason = override.get("kind"), override.get("reason")
        if kind not in {"fixed", "hinge", "ignore"} or not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"Connection {key} requires fixed/hinge/ignore and a reason")
        excluded = override.get("exclude_contact", False)
        if not isinstance(excluded, bool) or (excluded and kind != "fixed"):
            raise ValueError(f"Only a fixed mating pair can exclude contacts: {key}")
        item = {**override, "source": "explicit", "exclude_contact": excluded}
        if kind == "hinge":
            matches = [e for e in evidence.get(key, []) if e["status"] == "confirmed"]
            if "anchor_m" not in item or "axis" not in item:
                if a not in selected or b not in selected:
                    pass  # Boundary connections are reported, never reconstructed or grounded.
                elif not matches:
                    raise ValueError(f"Hinge {key} requires an anchor_m and axis or confirmed evidence")
                else:
                    item.setdefault("anchor_m", matches[0]["anchor_m"])
                    item.setdefault("axis", matches[0]["axis"])
            if "anchor_m" in item:
                item["anchor_m"] = _vector(item["anchor_m"], "anchor_m").tolist()
            if "axis" in item:
                axis = _vector(item["axis"], "axis")
                if np.linalg.norm(axis) < 1e-12:
                    raise ValueError(f"Hinge {key} has a zero axis")
                item["axis"] = (axis / np.linalg.norm(axis)).tolist()
        if a not in selected or b not in selected:
            omitted.append(item)
            continue
        resolved[key] = item
    graph = nx.Graph()
    graph.add_nodes_from(ids)
    graph.add_edges_from(k for k, c in resolved.items() if c["kind"] != "ignore")
    components = [sorted(c) for c in nx.connected_components(graph)]
    if document.selected_ids == ["root"] and "expected_components" in config:
        expected = sorted(sorted(c) for c in config["expected_components"])
        if sorted(components) != expected:
            raise ValueError(f"Connection components do not match specification: {components}")
    forest = nx.utils.UnionFind(ids)
    records = []
    for key, item in sorted(resolved.items()):
        record = {**item, "evidence": evidence.get(key, []), "constraint": None}
        if item["kind"] == "fixed" and forest[key[0]] != forest[key[1]]:
            forest.union(*key)
            record["constraint"] = "weld_" + "__".join(i.replace("/", "_") for i in key)
        records.append(record)
    # A native hinge tree cannot represent multiple parents or closed kinematic loops.
    children = set()
    for c in records:
        if c["kind"] != "hinge":
            continue
        a, b = c["first"], c["second"]
        if b in children or forest[a] == forest[b]:
            raise ValueError(f"Conflicting hinge or closed articulation loop: {a}, {b}")
        children.add(b)
        forest.union(a, b)
        c["constraint"] = "hinge_" + b.replace("/", "_")
    unresolved = [
        {"first": a, "second": b, "evidence": e}
        for (a, b), e in sorted(evidence.items()) if (a, b) not in resolved
    ]
    return {
        "specification": str(config_path.resolve()),
        "specification_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "connections": records, "components": components,
        "omitted_boundary_connections": omitted, "unresolved_contacts": unresolved,
        "skipped_geometry_count": len(inspection.skipped_geometry),
    }


def add_bodies(spec, groups, offset, report=None):
    """Keep part meshes in their original frames when introducing hinge parents."""
    hinges = {c["second"]: c for c in (report or {}).get("connections", [])
              if c["kind"] == "hinge"}

    def add(key):
        group = groups[key]
        if "body" in group:
            return group["body"]
        hinge = hinges.get(key)
        parent = add(hinge["first"]) if hinge else spec.worldbody
        pos = (group["origin"] - groups[hinge["first"]]["origin"]
               if hinge else group["origin"] + offset)
        body = parent.add_body(name=group["name"], pos=pos)
        if hinge:
            body.add_joint(
                name=hinge["constraint"], type=mujoco.mjtJoint.mjJNT_HINGE,
                pos=np.asarray(hinge["anchor_m"]) - group["origin"], axis=hinge["axis"],
                limited=False, damping=0, frictionloss=0,
            )
        else:
            body.add_freejoint(name=group["name"] + "_free")
        group["body"] = body
        return body

    for key in groups:
        add(key)


def add_constraints(spec, groups, report, solref, solimp):
    for c in report["connections"]:
        a, b = (groups[c[k]]["name"] for k in ("first", "second"))
        if c["kind"] == "fixed" and c["constraint"]:
            # Zero relpose quaternion asks MuJoCo to use the initial relative pose.
            # Torquescale is one stud pitch, not a calibrated glue-patch diameter.
            spec.add_equality(
                name=c["constraint"], type=mujoco.mjtEq.mjEQ_WELD,
                objtype=mujoco.mjtObj.mjOBJ_BODY, name1=a, name2=b,
                data=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.008],
                solref=solref, solimp=solimp,
            )
        if c["exclude_contact"]:
            spec.add_exclude(bodyname1=a, bodyname2=b)
