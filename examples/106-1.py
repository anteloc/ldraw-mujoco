"""Reproduce the sample's portable scene, five-second report and inspection views.

Run from any directory with the project environment:
    uv run python examples/106-1.py
"""

from pathlib import Path

import mujoco

from ldraw_mujoco import import_ldraw
from ldraw_mujoco.cli import write_json
from ldraw_mujoco.simulation import simulate, snapshot

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/106-1"


def main():
    result = import_ldraw(ROOT / "data/models-annotated/106-1.mpd", grouping="top-level")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    scene = OUTPUT / "scene.xml"
    scene.write_text(result.spec.to_xml())
    write_json(OUTPUT / "scene.import.json", result.report)

    # Inspect the exported artifact, which is also used by the MCP server.
    model = mujoco.MjModel.from_xml_path(str(scene))
    data = mujoco.MjData(model)
    snapshot(model, data, OUTPUT / "initial.png")
    car, minifigure = [body["name"] for body in result.report["bodies"]]
    snapshot(model, data, OUTPUT / "car.png", body=car)
    snapshot(model, data, OUTPUT / "car-rear.png", body=car, azimuth=-45)
    snapshot(model, data, OUTPUT / "minifigure.png", body=minifigure)

    data, report = simulate(model, seconds=5, data=data)
    write_json(OUTPUT / "scene.simulation.json", report)
    snapshot(model, data, OUTPUT / "final.png")
    print(f"Artifacts: {OUTPUT}")
    print(f"Numerically valid: {report['numerically_valid']}; contacts: {data.ncon}")
    if not report["numerically_valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
