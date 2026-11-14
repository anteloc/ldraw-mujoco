import asyncio
import hashlib
import importlib.util
import json
from types import SimpleNamespace

import mujoco
import numpy as np
import pytest

from ldraw_mujoco import ExecutionError, Interpreter, inspect_ldraw
from ldraw_mujoco.debugger import terminal
from ldraw_mujoco.mcp import MCPError, decode_result
from ldraw_mujoco.simulation import contacts

IDENTITY = "1 0 0 0 1 0 0 0 1"
PROGRAM = f"""0 FILE main.ldr
1 4 0 0 0 {IDENTITY} sub.ldr
1 1 100 0 0 {IDENTITY} sub.ldr
1 16 0 0 0 {IDENTITY} empty.ldr
0 FILE sub.ldr
1 47 0 0 0 {IDENTITY} cube.dat
1 16 0 -30 0 {IDENTITY} leaf.ldr
0 FILE leaf.ldr
1 16 0 0 0 {IDENTITY} cube.dat
0 FILE empty.ldr
"""


class NativeClient:
    """Test double using native MuJoCo to check the requested tool operations.

    Production execution uses only the real MCP adapter. The real stdio test
    below independently checks the actual server contract.
    """

    def __init__(self):
        self.calls, self.starts = [], []
        self.failure = None

    async def call(self, tool, **args):
        self.calls.append((tool, args))
        if tool == self.failure:
            raise MCPError("injected tool failure")
        if tool == "sim_load":
            self.model = mujoco.MjModel.from_xml_string(args["xml_string"])
            self.data = mujoco.MjData(self.model)
            return {
                **{k: getattr(self.model, k) for k in ("nq", "nv", "nbody")},
                "bodies": [self.model.body(i).name for i in range(self.model.nbody)],
            }
        m, d = self.model, self.data
        if tool == "modify_model":
            for change in args["modifications"]:
                index = getattr(m, change["element"])(change["name"]).id
                getattr(m, change["element"] + "_" + change["field"])[index] = change["value"]
        elif tool == "sim_reset":
            mujoco.mj_resetData(m, d)
        elif tool == "sim_step":
            self.starts.append((d.qpos.copy(), d.qvel.copy(), d.time))
            mujoco.mj_step(m, d, nstep=args["n_steps"])
        elif tool == "sim_get_state":
            return {"time": d.time, "qpos": d.qpos.tolist(), "qvel": d.qvel.tolist()}
        elif tool == "analyze_contacts":
            return {"n_contacts": d.ncon, "contacts": contacts(m, d)[: args["max_contacts"]]}
        elif tool == "viewer_open":
            raise MCPError("No display")
        else:
            assert tool == "sim_forward"
        mujoco.mj_forward(m, d)
        return {"n_contacts": d.ncon}


@pytest.fixture
def program(build, tmp_path):
    imported = build(PROGRAM, suffix=".mpd", individual_parts=True)
    return Interpreter(imported, output_dir=tmp_path / "execution")


def test_debugger_calls_returns_repeated_instances_and_empty_submodel(program):
    async def check():
        client = NativeClient()
        await program._load(client)
        entered = await program.step_into()
        assert entered["events"][0]["kind"] == "call"
        assert entered["events"][0]["physics"] is None
        assert not client.starts
        assert entered["next_instruction"]["id"] == "0/0"
        part = await program.step_into()
        assert part["enabled_ids"] == ["0/0"]
        leaf = await program.step_over()
        assert [e["instruction"]["id"] for e in leaf["events"]] == ["0/1", "0/1/0"]
        assert leaf["next_instruction"]["id"] == "1"
        await program.step_into()
        finished = await program.step_out()
        assert [e["instruction"]["id"] for e in finished["events"]] == ["1/0", "1/1", "1/1/0"]
        assert finished["next_instruction"]["id"] == "2"
        empty = await program.step_into()
        assert empty["done"] and len(empty["enabled_ids"]) == 4
        count = len(client.calls)
        assert (await program.run())["events"] == []
        assert (await program.step_out())["done"]
        assert len(client.calls) == count
        assert len(client.starts) == 4
        await program.reset()
        assert program.status["next_instruction"]["id"] == "0"
        assert not program.enabled
        all_events = (await program.step_out())["events"]
        assert len(all_events) == 9
        assert len({e["instruction"]["id"] for e in all_events}) == 9
        assert json.loads(json.dumps(all_events, allow_nan=False)) == all_events

    asyncio.run(check())


def test_activation_preserves_mass_transparency_and_resets_every_trial(program):
    async def check():
        client = NativeClient()
        await program._load(client)
        m, d = client.model, client.data
        mass, inertia = m.body_mass.copy(), m.body_inertia.copy()
        assert d.ncon == 0
        assert np.all(m.body_gravcomp[1:] == 1)
        assert np.all(m.geom_rgba[m.geom_bodyid != 0, 3] == 0)
        assert np.all(m.body_contype[1:] == 0)
        mujoco.mj_step(m, d, nstep=100)
        np.testing.assert_allclose(d.qpos, m.qpos0, atol=1e-15)
        await program.step_into()
        event = (await program.step_into())["events"][0]
        active = m.body(program.parts["0/0"]["body"]).id
        visuals = (m.geom_bodyid == active) & (m.geom_group == 0)
        np.testing.assert_allclose(m.geom_rgba[visuals, 3], 128 / 255, atol=1e-6)
        assert m.body_gravcomp[active] == 0
        assert m.body_contype[active] == 1
        for body in range(1, m.nbody):
            mask = m.geom_bodyid == body
            assert m.body_contype[body] == np.bitwise_or.reduce(m.geom_contype[mask])
            assert m.body_conaffinity[body] == np.bitwise_or.reduce(m.geom_conaffinity[mask])
        for ident, part in program.parts.items():
            if ident != "0/0":
                qa, va = part["qpos_address"], part["qvel_address"]
                np.testing.assert_allclose(d.qpos[qa : qa + 7], part["initial_qpos"], atol=1e-15)
                np.testing.assert_allclose(d.qvel[va : va + 6], 0, atol=1e-15)
        assert event["physics"]["actual_duration_s"] == pytest.approx(0.1)
        assert event["physics"]["contacts"]
        assert all(
            c["part1_id"] in {None, "0/0"} and c["part2_id"] in {None, "0/0"}
            for c in event["physics"]["contacts"]
        )
        await program.run()
        for qpos, qvel, time in client.starts:
            np.testing.assert_array_equal(qpos, m.qpos0)
            np.testing.assert_array_equal(qvel, 0)
            assert time == 0
        np.testing.assert_array_equal(m.body_mass, mass)
        np.testing.assert_array_equal(m.body_inertia, inertia)
        assert len([c for c in client.calls if c[0] == "sim_load"]) == 1
        await program.reset()
        assert not d.ncon

    asyncio.run(check())


def test_failure_retains_completed_events_and_requires_reset(program):
    async def check():
        client = NativeClient()
        await program._load(client)
        client.failure = "sim_step"
        with pytest.raises(ExecutionError) as caught:
            await program.step_over()
        assert caught.value.result["failing_instruction"]["id"] == "0/0"
        assert [e["kind"] for e in caught.value.result["events"]] == ["call"]
        assert program.status["failed"]
        count = len(client.calls)
        with pytest.raises(ExecutionError, match="halted"):
            await program.step_into()
        assert len(client.calls) == count
        client.failure = None
        await program.reset()
        assert (await program.run())["done"]
        records = [
            json.loads(line)
            for line in (program.output_dir / "events.jsonl").read_text().splitlines()
        ]
        assert any(r["kind"] == "error" for r in records)

    asyncio.run(check())


def test_cancellation_halts_program_and_reset_recovers(program):
    async def check():
        client = NativeClient()
        await program._load(client)
        original = client.call
        started = asyncio.Event()

        async def blocked(tool, **args):
            if tool == "sim_step":
                started.set()
                await asyncio.Event().wait()
            return await original(tool, **args)

        client.call = blocked
        task = asyncio.create_task(program.run())
        await started.wait()
        with pytest.raises(RuntimeError, match="sequential"):
            await program.step_into()
        with pytest.raises(RuntimeError, match="current debugger operation"):
            await program.reset()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert program.failed
        assert program.last_result["failing_instruction"]["id"] == "0/0"
        client.call = original
        await program.reset()
        assert not program.failed
        assert (await program.step_over())["enabled_ids"] == ["0/0", "0/1/0"]

    asyncio.run(check())


def test_reset_recovers_after_a_partially_applied_activation(program):
    async def check():
        client = NativeClient()
        await program._load(client)
        original = client.call

        async def partial(tool, **args):
            if tool == "modify_model":
                await original(tool, **{**args, "modifications": args["modifications"][:1]})
                raise MCPError("partial modification failure")
            return await original(tool, **args)

        client.call = partial
        with pytest.raises(ExecutionError, match="partial"):
            await program.run()
        assert not program.enabled
        assert client.model.body_gravcomp[1] == 0
        client.call = original
        await program.reset()
        assert np.all(client.model.body_gravcomp[1:] == 1)
        assert np.all(client.model.body_contype[1:] == 0)
        assert (await program.run())["done"]

    asyncio.run(check())


@pytest.mark.parametrize("bad_state", ["time", "nan", "contacts"])
def test_incomplete_physics_is_not_reported_as_success(program, bad_state):
    async def check():
        client = NativeClient()
        await program._load(client)
        original = client.call

        async def corrupt(tool, **args):
            result = await original(tool, **args)
            if tool == "sim_get_state":
                if bad_state == "time":
                    result["time"] = 0
                elif bad_state == "nan":
                    result["qpos"][0] = float("nan")
            if tool == "analyze_contacts" and bad_state == "contacts":
                result["contacts"] = []
            return result

        client.call = corrupt
        with pytest.raises(ExecutionError) as caught:
            await program.run()
        assert program.failed
        if bad_state != "contacts":
            observation = caught.value.result["failing_event"]["physics"]
            assert not observation["state_finite"] or not observation["duration_matches"]
        json.dumps(caught.value.result, allow_nan=False)
        for line in (program.output_dir / "events.jsonl").read_text().splitlines():
            assert "NaN" not in line
            json.loads(line)

    asyncio.run(check())


def test_terminal_controls_and_artifact_hash(program):
    async def check():
        await program._load(NativeClient())
        commands = iter(["help", "where", "s", "n", "f", "r", "c", "unknown", "q"])
        output = []

        async def read():
            return next(commands)

        assert await terminal(program, read=read, write=output.append) == 0
        assert any("Placed 0/0" in line for line in output)
        assert any("Finished: 4 parts" in line for line in output)
        metadata = json.loads((program.output_dir / "execution.json").read_text())
        assert (
            metadata["xml_sha256"]
            == hashlib.sha256((program.output_dir / "scene.xml").read_bytes()).hexdigest()
        )
        with pytest.raises(MCPError, match="No display"):
            await program.viewer()
        assert not program.failed

    asyncio.run(check())


def test_source_provenance_for_external_submodels(tmp_path):
    source = tmp_path / "main.mpd"
    child = tmp_path / "external.ldr"
    source.write_text(f"1 16 0 0 0 {IDENTITY} external.ldr\n")
    child.write_text(f"0 comment\n1 4 0 0 0 {IDENTITY} cube.dat\n")
    nodes = inspect_ldraw(source)["instances"]
    assert nodes[1]["source_file"] == str(source)
    assert nodes[1]["line"] == 1
    assert nodes[2]["source_file"] == str(child)
    assert nodes[2]["line"] == 2


@pytest.mark.parametrize("structured", [True, False])
def test_mcp_response_formats_and_errors(structured):
    def response(payload, is_error=False):
        encoded = json.dumps(payload)
        return SimpleNamespace(
            isError=is_error,
            structuredContent={"result": encoded} if structured else None,
            content=[SimpleNamespace(type="text", text=encoded)],
        )

    assert decode_result(response({"time": 0.1})) == {"time": 0.1}
    for payload in (
        {"error": "invalid_input"},
        {"ok": False},
        {"ok": True, "modifications": [{"ok": False}]},
    ):
        with pytest.raises(MCPError):
            decode_result(response(payload))
    with pytest.raises(MCPError):
        decode_result(response({}, is_error=True))


def test_duration_validation_and_rounding(build):
    imported = build(PROGRAM, suffix=".mpd", individual_parts=True)
    for duration in (0, -1, float("nan"), float("inf")):
        with pytest.raises(ValueError, match="positive"):
            Interpreter(imported, seconds_per_part=duration)
    assert Interpreter(imported, seconds_per_part=0.0011).steps == 2


@pytest.mark.integration
@pytest.mark.skipif(
    importlib.util.find_spec("mujoco_mcp") is None, reason="Install the interpreter extra"
)
def test_real_stdio_execution(tmp_path, small_library):
    source = tmp_path / "real.mpd"
    source.write_text(PROGRAM)

    async def check():
        async with Interpreter.open(
            source, library=small_library, shadows=[], cache=tmp_path / "cache"
        ) as program:
            assert not (await program.step_into())["enabled_ids"]
            result = await program.run()
            assert result["done"]
            assert result["enabled_ids"] == ["0/0", "0/1/0", "1/0", "1/1/0"]
            physics = [e["physics"] for e in result["events"] if e["kind"] == "place"]
            assert all(p["state_finite"] and p["duration_matches"] for p in physics)
            assert all(p["actual_duration_s"] == pytest.approx(0.1) for p in physics)
            assert physics[0]["contacts"]
            await program.reset()
            assert not program.enabled

    asyncio.run(check())


@pytest.mark.integration
@pytest.mark.skipif(
    importlib.util.find_spec("mujoco_mcp") is None, reason="Install the interpreter extra"
)
def test_owned_context_preserves_execution_exceptions(tmp_path, small_library):
    source = tmp_path / "failure.mpd"
    source.write_text(PROGRAM)

    async def check():
        with pytest.raises(ExecutionError, match="injected") as caught:
            async with Interpreter.open(
                source, library=small_library, shadows=[], cache=tmp_path / "cache"
            ) as program:
                original = program.client.call

                async def fail(tool, **args):
                    if tool == "sim_step":
                        raise MCPError("injected failure through real context")
                    return await original(tool, **args)

                program.client.call = fail
                await program.step_over()
        assert caught.value.result["failing_instruction"]["id"] == "0/0"
        assert program.client is None

    asyncio.run(check())
