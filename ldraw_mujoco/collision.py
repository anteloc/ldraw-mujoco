"""Cached convex decomposition of parsed surfaces; no source-library edits."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
from pathlib import Path

import coacd
import numpy as np
import trimesh

from .geometry import LDU_TO_METERS, triangle_mesh
from .library import data_root


def decompose(triangles, *, cache=None, tolerance=0.00005):
    """Return part-local convex meshes in meters and reproducibility evidence.

    The tolerance controls CoACD's concavity metric, not the preprocessing error
    or a certified surface-distance bound. Mating clearances need separate checks.
    """
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("collision_tolerance must be finite and positive")
    mesh = triangle_mesh(triangles * LDU_TO_METERS)
    settings = dict(
        threshold=tolerance, real_metric=True, preprocess_mode="auto",
        preprocess_resolution=100, seed=0,
    )
    evidence = {
        "coacd_version": importlib.metadata.version("coacd"),
        "settings": settings,
        "input_watertight": bool(mesh.is_watertight),
        "input_winding_consistent": bool(mesh.is_winding_consistent),
    }
    digest = hashlib.sha256(json.dumps(evidence, sort_keys=True).encode())
    digest.update(mesh.vertices.tobytes())
    digest.update(mesh.faces.tobytes())
    key = digest.hexdigest()
    folder = Path(cache or data_root().parent / ".cache") / "collision"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{key}.npz"
    if path.exists():
        with np.load(path, allow_pickle=False) as stored:
            pieces = [
                trimesh.Trimesh(stored[f"v{i}"], stored[f"f{i}"], process=False)
                for i in range(len(stored.files) // 2)
            ]
    else:
        coacd.set_log_level("warn")
        result = coacd.run_coacd(coacd.Mesh(mesh.vertices, mesh.faces), **settings)
        pieces = [trimesh.Trimesh(v, f, process=False) for v, f in result]
        if not pieces or any(not p.is_volume or p.volume <= 0 for p in pieces):
            raise ValueError("CoACD did not produce closed positive-volume collision solids")
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(dir=folder, suffix=".npz", delete=False) as tmp:
            np.savez_compressed(
                tmp, **{k: a for i, p in enumerate(pieces)
                        for k, a in ((f"v{i}", p.vertices), (f"f{i}", p.faces))}
            )
        os.replace(tmp.name, path)
    return pieces, {**evidence, "cache_key": key, "hull_count": len(pieces)}
