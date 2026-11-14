import asyncio
import hashlib
import importlib.util
import json
from contextlib import asynccontextmanager
from types import SimpleNamespace

import mujoco
import numpy as np
import pytest

from ldraw_mujoco import ExecutionError, Interpreter, inspect_ldraw
from ldraw_mujoco.debugger import terminal
from ldraw_mujoco.mcp import MCPError, MujocoClient, decode_result, server_command
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
        elif tool == "sim_set_state":
            d.qpos[:] = args["qpos"]
            d.qvel[:] = args["qvel"]
        elif tool == "analyze_contacts":
            return {"n_contacts": d.ncon, "contacts": contacts(m, d)[: args["max_contacts"]]}
        elif tool == "viewer_open":
            raise MCPError("No display")
        else:
            assert tool == "sim_forward"
        mujoco.mj_forward(m, d)
        return {"n_contacts": d.ncon, "time": d.time}


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


def test_undo_restores_calls_parts_empty_returns_and_completed_program(program):
    async def check():
        client = NativeClient()
        await program._load(client)
        count = len(client.calls)
        assert (await program.undo())["undone_command"] is None
        assert len(client.calls) == count
        checkpoints = []
        for operation in (
            program.step_into,
            program.step_into,
            program.step_over,
            program.step_into,
            program.step_out,
            program.step_into,
        ):
            checkpoints.append(
                (
                    program.status,
                    await client.call("sim_get_state"),
                    client.model.body_gravcomp.copy(),
                    client.model.body_contype.copy(),
                    client.model.body_conaffinity.copy(),
                    client.model.geom_contype.copy(),
                    client.model.geom_conaffinity.copy(),
                    client.model.geom_rgba.copy(),
                )
            )
            await operation()
        assert program.status["done"]
        await program.run()  # Completed no-ops must not hide the last real command.
        await program.step_out()
        for status, state, *fields in reversed(checkpoints):
            result = await program.undo()
            assert result["events"] == []
            assert program.status == status
            assert await client.call("sim_get_state") == state
            for name, expected in zip(
                (
                    "body_gravcomp",
                    "body_contype",
                    "body_conaffinity",
                    "geom_contype",
                    "geom_conaffinity",
                    "geom_rgba",
                ),
                fields,
                strict=True,
            ):
                np.testing.assert_array_equal(getattr(client.model, name), expected)
            allowed = {program.parts[i]["body"] for i in program.enabled} | {"world"}
            for contact in client.data.contact:
                assert all(
                    client.model.body(client.model.geom_bodyid[g]).name in allowed
                    for g in contact.geom
                )
        assert len(client.starts) == 4  # Undo never advances physics.
        assert client.data.ncon == 0
        count = len(client.calls)
        assert (await program.undo())["undone_command"] is None
        assert len(client.calls) == count
        records = [
            json.loads(line)
            for line in (program.output_dir / "events.jsonl").read_text().splitlines()
        ]
        assert len([r for r in records if r["kind"] == "undo"]) == len(checkpoints)
        await program.run()
        await program.reset()
        assert (await program.undo())["undone_command"] is None
        assert not program.enabled

    asyncio.run(check())


@pytest.mark.parametrize(
    "method, command", [("step_over", "next"), ("step_out", "finish"), ("run", "continue")]
)
def test_undo_undoes_whole_command_and_allows_reexecution(program, method, command):
    async def check():
        client = NativeClient()
        await program._load(client)
        await program.step_into()
        await program.step_into()
        before = program.status
        state = await client.call("sim_get_state")
        operation = getattr(program, method)
        first = await operation()
        result = await program.undo()
        assert result["undone_command"] == command
        assert program.status == before
        assert await client.call("sim_get_state") == state
        assert await operation() == first
        await program.undo()
        await program.undo()
        assert not program.enabled
        assert program.status["next_instruction"]["id"] == "0/0"

    asyncio.run(check())


@pytest.mark.parametrize("failure", ["partial", "state", "cancelled"])
def test_undo_failure_halts_until_reset(program, failure):
    async def check():
        client = NativeClient()
        await program._load(client)
        await program.step_into()
        await program.step_into()
        await program.run()
        original = client.call

        async def fail(tool, **args):
            if failure == "partial" and tool == "modify_model":
                await original(tool, **{**args, "modifications": args["modifications"][:1]})
                raise MCPError("partial undo failure")
            if tool == "sim_set_state":
                if failure == "cancelled":
                    raise asyncio.CancelledError()
                raise MCPError("state undo failure")
            return await original(tool, **args)

        client.call = fail
        error = asyncio.CancelledError if failure == "cancelled" else ExecutionError
        with pytest.raises(error):
            await program.undo()
        assert program.failed
        assert program.last_result["operation"] == "undo"
        with pytest.raises(ExecutionError, match="halted"):
            await program.undo()
        with pytest.raises(ExecutionError, match="halted"):
            await program.run()
        client.call = original
        await program.reset()
        assert (await program.undo())["undone_command"] is None
        assert (await program.run())["done"]

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
        with pytest.raises(ExecutionError, match="halted"):
            await program.undo()
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
        with pytest.raises(RuntimeError, match="sequential"):
            await program.undo()
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
        commands = iter(
            [
                "help",
                "where",
                "u",
                "s",
                "n",
                "undo",
                "n",
                "f",
                "r",
                "c",
                "u",
                "c",
                "unknown",
                "q",
            ]
        )
        output = []

        async def read():
            return next(commands)

        assert await terminal(program, read=read, write=output.append) == 0
        assert any("Placed 0/0" in line for line in output)
        assert any("Finished: 4 parts" in line for line in output)
        assert "undo (u)" in output[0]
        help_lines = output[2].splitlines()
        assert len(help_lines) == 9
        assert all(" - " in line for line in help_lines)
        assert "undo (u) - Undo the last step, next, finish, or continue." in help_lines
        assert "Nothing to undo." in output
        assert "Undid next." in output
        assert "Undid continue." in output
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


@pytest.mark.parametrize(
    "platform, graphical, executable, arguments",
    [
        ("darwin", True, "mjpython", ["-m", "mujoco_mcp"]),
        ("darwin", False, "mujoco-mcp", []),
        ("linux", True, "mujoco-mcp", []),
    ],
)
def test_viewer_launcher_uses_installed_environment(
    monkeypatch, tmp_path, platform, graphical, executable, arguments
):
    import ldraw_mujoco.mcp as adapter

    monkeypatch.setattr(adapter.sys, "platform", platform)
    monkeypatch.setattr(adapter.sysconfig, "get_path", lambda _: str(tmp_path))
    (tmp_path / executable).touch()
    assert server_command(viewer=graphical) == (str(tmp_path / executable), arguments)


@pytest.mark.parametrize("available", [True, False])
def test_viewer_option_paces_success_and_preserves_headless_fallback(
    monkeypatch, tmp_path, small_library, available
):
    client = NativeClient()
    original = client.call

    async def call(tool, **args):
        if available and tool == "viewer_open":
            return {"ok": True}
        return await original(tool, **args)

    client.call = call

    @asynccontextmanager
    async def connect(**kwargs):
        assert kwargs["viewer"] is True
        yield client

    monkeypatch.setattr(MujocoClient, "connect", connect)
    source = tmp_path / "viewer.mpd"
    source.write_text(PROGRAM)

    async def check():
        async with Interpreter.open(
            source, library=small_library, shadows=[], cache=tmp_path / "cache", viewer=True
        ) as program:
            assert bool(program.viewer_error) is not available
            assert (await program.run())["done"]
            steps = [args for tool, args in client.calls if tool == "sim_step"]
            assert len(steps) == 4
            assert all(args["realtime"] is available for args in steps)

    asyncio.run(check())


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
            first = await program.step_into()
            before = program.status
            state = await program._call("sim_get_state")
            result = await program.run()
            assert result["done"]
            assert result["enabled_ids"] == ["0/0", "0/1/0", "1/0", "1/1/0"]
            physics = [
                e["physics"] for e in first["events"] + result["events"] if e["kind"] == "place"
            ]
            assert all(p["state_finite"] and p["duration_matches"] for p in physics)
            assert all(p["actual_duration_s"] == pytest.approx(0.1) for p in physics)
            assert physics[0]["contacts"]
            assert (await program.undo())["undone_command"] == "continue"
            assert program.status == before
            assert await program._call("sim_get_state") == state
            assert await program.run() == result
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
