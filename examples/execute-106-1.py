"""Exercise debugger controls and retain exact MCP states plus inspection images.

Run: uv run --extra interpreter python examples/execute-106-1.py
Physics runs in the owned MCP process. Local MuJoCo only renders returned states.
"""

import asyncio
from pathlib import Path

import mujoco

from ldraw_mujoco import Interpreter
from ldraw_mujoco.cli import write_json
from ldraw_mujoco.simulation import snapshot

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/106-1/execution"


async def capture(program, name, *, selection=None):
    state = await program.client.call("sim_get_state", sim_name=program.slot)
    write_json(
        OUTPUT / f"{name}.state.json",
        {
            "xml_sha256": program.preparation["xml_sha256"],
            "enabled_ids": list(program.enabled),
            "state": state,
        },
    )
    model = mujoco.MjModel.from_xml_string(program.xml)
    data = mujoco.MjData(model)
    modifications = list(program.inactive)
    for ident in program.enabled:
        modifications.extend(program.activate[ident])
    for change in modifications:
        index = getattr(model, change["element"])(change["name"]).id
        getattr(model, change["element"] + "_" + change["field"])[index] = change["value"]
    data.qpos[:] = state["qpos"]
    data.qvel[:] = state["qvel"]
    data.time = state["time"]
    if selection:
        bodies = {model.body(program.parts[i]["body"]).id for i in selection}
        for geom in model.geom_bodyid.nonzero()[0]:
            if model.geom_bodyid[geom] not in bodies:
                model.geom_group[geom] = 5
    # snapshot calls mj_forward for rendering, never mj_step.
    snapshot(model, data, OUTPUT / f"{name}.png")


async def main():
    async with Interpreter.open(
        ROOT / "data/models-annotated/106-1.mpd",
        output_dir=OUTPUT,
    ) as program:
        await capture(program, "empty")
        await program.step_into()  # Enter car 0; no placement yet.
        await program.step_into()  # Execute its first DAT placement.
        await capture(program, "first-part")
        while program.status["next_instruction"]["id"] != "0/19":
            await program.step_over()
        await capture(program, "before-wheel")
        await program.step_over()  # Wheel call, including both contained DATs.
        await capture(program, "nested-wheel")
        await capture(program, "wheel-detail", selection=["0/19/0", "0/19/1"])
        await program.undo()  # Undo that whole call, including both parts.
        assert program.status["next_instruction"]["id"] == "0/19"
        assert not {"0/19/0", "0/19/1"} & set(program.enabled)
        await capture(program, "undo-wheel")
        await program.step_over()  # Execute it again from the restored position.
        await program.step_out()  # Finish the car and return to the root.
        await program.run()  # Place the minifigure and finish the program.
        await capture(program, "completed")
        assert len(program.enabled) == 65
        write_json(OUTPUT / "final.json", program.last_result)
        print(f"Executed {len(program.enabled)} parts. Artifacts: {OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())
