"""Compile and step 10,000 copies of a library brick. Run in a fresh Python process."""

import platform
import resource
import sys
from pathlib import Path
from time import perf_counter

import mujoco
import numpy as np

from ldraw_mujoco import import_ldraw
from ldraw_mujoco.cli import write_json

OUTPUT = Path(__file__).resolve().parents[1] / "output" / "repeated-bricks"


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = OUTPUT / "bricks.ldr"
    # Space a 100 x 100 grid of 2 x 4 bricks above the floor for one free-flight step.
    source.write_text(
        "".join(
            f"1 4 {x * 100} 0 {z * 60} 1 0 0 0 1 0 0 0 1 3001.dat\n"
            for z in range(100)
            for x in range(100)
        )
    )
    start = perf_counter()
    result = import_ldraw(source, individual_parts=True)
    import_seconds = perf_counter() - start
    model = result.model
    assert (model.nbody, model.njnt, model.nmesh) == (10_001, 10_000, 2)
    assert np.all(model.jnt_type == mujoco.mjtJoint.mjJNT_FREE)
    collision = model.geom_group == 3
    assert collision.sum() == 10_000
    assert len(np.unique(model.geom_dataid[collision])) == 1
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    mujoco.mj_step(model, data)
    assert data.time == model.opt.timestep and data.ncon == 0
    assert np.isfinite(data.qpos).all() and not any(w.number for w in data.warning)
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    report = {
        "platform": platform.platform(),
        "versions": result.report["versions"],
        "source_sha256": result.report["source_sha256"],
        "part": "3001.dat",
        "occurrences": result.report["occurrence_count"],
        "bodies_including_world": model.nbody,
        "collision_geoms": int(collision.sum()),
        "mesh_assets": model.nmesh,
        "import_wall_seconds": import_seconds,
        "process_peak_rss_mib_through_step": peak_rss
        / (2**20 if sys.platform == "darwin" else 1024),
        "simulation_time_s": data.time,
        "contacts": data.ncon,
    }
    write_json(OUTPUT / "acceptance.json", report)
    print((OUTPUT / "acceptance.json").read_text())


if __name__ == "__main__":
    main()
