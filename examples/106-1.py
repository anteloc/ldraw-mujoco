"""Export full and selected instances, in both modes, with initial views and hold checks.

Run with: uv run python examples/106-1.py
"""

from pathlib import Path

import mujoco

from ldraw_mujoco import import_ldraw, inspect_ldraw
from ldraw_mujoco.cli import write_json
from ldraw_mujoco.simulation import hold, snapshot

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/106-1"


def main():
    source = ROOT / "data/models-annotated/106-1.mpd"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT / "inventory.json", inspect_ldraw(source))
    selection = ["106 - wheel assembly.ldr:0/46", "106 - Minifig.ldr"]
    examples = {
        "scene": {},
        "car": {"sections": "106 - car.ldr"},
        "minifigure": {"sections": "106 - Minifig.ldr"},
        "selection": {"sections": selection},
        "parts": {"individual_parts": True},
        "selection-parts": {"sections": selection, "individual_parts": True},
    }
    for name, options in examples.items():
        result = import_ldraw(source, **options)
        scene = OUTPUT / f"{name}.xml"
        scene.write_text(result.spec.to_xml())
        write_json(OUTPUT / f"{name}.import.json", result.report)
        # Render the portable artifact, also usable by the MCP server.
        model = mujoco.MjModel.from_xml_path(str(scene))
        data = mujoco.MjData(model)
        image = "initial.png" if name == "scene" else f"{name}.png"
        snapshot(model, data, OUTPUT / image)
        # Check once, on fresh state, that the exported scene holds still.
        _, check = hold(model)
        write_json(OUTPUT / f"{name}.hold.json", check)
        verdict = "holds" if check["holds"] else f"{len(check['moved_bodies'])} bodies moved"
        print(f"{name}: {result.report['occurrence_count']} parts, {model.nbody - 1} bodies, {verdict}")
    print(f"Artifacts: {OUTPUT}")


if __name__ == "__main__":
    main()
