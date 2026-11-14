import asyncio
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from ldraw_mujoco import Interpreter
from ldraw_mujoco.debugger import terminal
from ldraw_mujoco.editing import EditError, edit_placement, editor_bindings, validate_placement
from ldraw_mujoco.mcp import MCPError

IDENTITY = "1 0 0 0 1 0 0 0 1"
LINE = f"1 16 0 0 0 {IDENTITY} cube.dat"
PROGRAM = f"""0 FILE main.ldr
1 4 0 0 0 {IDENTITY} sub.ldr
1 1 100 0 0 {IDENTITY} sub.ldr
0 FILE sub.ldr
{LINE}
"""


@pytest.mark.parametrize(
    "field,value",
    [
        (1, "red"),
        (1, "4.2"),
        (2, "00.234.57"),
        (3, "nan"),
        (4, "1e999"),
        (5, "x"),
    ],
)
def test_editor_rejects_invalid_fields_at_their_locations(field, value):
    fields = LINE.split()
    fields[field] = value
    line = " ".join(fields)
    with pytest.raises(EditError) as caught:
        validate_placement(line)
    error = caught.value
    assert error.field_start == line.index(value)
    assert error.column >= error.field_start
    if value == "00.234.57":
        assert line[error.column] == "."
        assert error.column == error.field_start + 6
    assert error.suggestion
    assert error.display(line).splitlines()[1][error.column] == "^"


def test_editor_accepts_direct_colours_exponents_and_filenames_with_spaces():
    piece = validate_placement(f"1 0x2FF0000 -1.5 2e-3 .4 {IDENTITY} a part.dat")
    assert piece.reference == "a part.dat"
    assert piece.position.y == 0.002
    assert piece.colour.rgb == "#FF0000"
    with pytest.raises(EditError, match="singular"):
        validate_placement("1 4 0 0 0 0 0 0 0 0 0 0 0 0 cube.dat")
    with pytest.raises(EditError, match="must stay 1"):
        validate_placement(LINE.replace("1 ", "2 ", 1))


@pytest.mark.parametrize("old,new", [("1 16", "2 16"), ("16", "4"), ("cube.dat", "other.dat")])
def test_static_fields_cannot_change(old, new):
    with pytest.raises(EditError):
        validate_placement(LINE.replace(old, new, 1), original=LINE)


def test_submodel_transform_edit_is_instance_specific_and_comment_is_context(build):
    source = PROGRAM.replace(LINE, "0 // Test brick Red\n" + LINE)
    original = build(source, suffix=".mpd", individual_parts=True)
    line = next(n["source_text"] for n in original.report["instances"] if n["id"] == "0")
    edited = build(
        source,
        suffix=".mpd",
        individual_parts=True,
        placement_overrides={"0": line.replace("4 0", "4 25", 1)},
    )
    occurrences = {o["id"]: o for o in edited.report["occurrences"]}
    assert occurrences["0/0"]["position_ldu"] == [25, 0, 0]
    assert occurrences["1/0"]["position_ldu"] == [100, 0, 0]
    nodes = {n["id"]: n for n in edited.report["instances"]}
    assert nodes["0/0"]["context_comment"] == "0 // Test brick Red"
    assert nodes["0"]["context_comment"] is None


@pytest.mark.skipif(
    importlib.util.find_spec("prompt_toolkit") is None, reason="Install the interpreter extra"
)
def test_editor_tab_and_shift_tab_navigate_only_position_and_rotation():
    from prompt_toolkit.buffer import Buffer
    from prompt_toolkit.document import Document
    from prompt_toolkit.keys import Keys

    text = " ".join(LINE.split()[2:14])
    buffer = Buffer(document=Document(text, 0))
    event = SimpleNamespace(current_buffer=buffer)
    bindings = editor_bindings()
    tab = bindings.get_bindings_for_keys((Keys.ControlI,))[-1].handler
    previous = bindings.get_bindings_for_keys((Keys.BackTab,))[-1].handler
    tab(event)
    assert buffer.cursor_position == 2  # y, after x.
    previous(event)
    assert buffer.cursor_position == 0
    previous(event)
    assert buffer.cursor_position == len(text) - 1
    tab(event)
    assert buffer.cursor_position == 0


@pytest.mark.skipif(
    importlib.util.find_spec("prompt_toolkit") is None, reason="Install the interpreter extra"
)
def test_editor_correction_and_cancellation_preserve_original_and_focus_error():
    async def check():
        calls, output = [], []

        async def edit(ident, line):
            calls.append((ident, line))
            return {"changed": True}

        program = SimpleNamespace(
            placement_line=lambda _: LINE,
            edit=edit,
            nodes={"0/0": {"context_comment": "0 // Test brick Red"}},
        )
        bad = " ".join(LINE.replace("16 0", "16 00.234.57").split()[2:14])
        values = iter([bad, "e", " ".join(LINE.split()[2:14])])
        defaults = []

        async def prompt(message, **kwargs):
            if "default" in kwargs:
                defaults.append(kwargs["default"])
            return next(values)

        await edit_placement(program, "0/0", prompt=prompt, write=output.append)
        assert defaults[1].text == bad
        assert defaults[1].cursor_position == bad.index("00.234.57")
        assert calls == [("0/0", LINE)]
        assert "0 // Test brick Red" in output
        assert any("^\nx is not a float" in message for message in output)
        calls.clear()
        values = iter([bad, "c"])
        assert await edit_placement(program, "0/0", prompt=prompt, write=output.append) is None
        assert not calls
        assert output[-1] == LINE
        assert "reverted" in output[-2]

    asyncio.run(check())


@pytest.mark.skipif(
    importlib.util.find_spec("prompt_toolkit") is None, reason="Install the interpreter extra"
)
def test_interactive_editor_typing_error_correction_with_real_key_input():
    from prompt_toolkit import PromptSession
    from prompt_toolkit.input import create_pipe_input
    from prompt_toolkit.output import DummyOutput

    async def check():
        calls, output = [], []
        prompts = asyncio.Queue()

        async def edit(ident, line):
            calls.append(line)
            return {"changed": True}

        program = SimpleNamespace(
            placement_line=lambda _: LINE,
            edit=edit,
            nodes={"0/0": {"context_comment": "0 // Test brick Red"}},
        )
        with create_pipe_input() as keys:
            session = PromptSession(input=keys, output=DummyOutput())

            async def prompt(message, **kwargs):
                await prompts.put(message)
                return await session.prompt_async(message, **kwargs)

            task = asyncio.create_task(
                edit_placement(program, "0/0", prompt=prompt, write=output.append)
            )
            assert await prompts.get() == "1 16 "
            keys.send_text("\x1b[3~00.234.57\r")
            assert "Edit the error" in await asyncio.wait_for(prompts.get(), 3)
            keys.send_text("e\r")
            assert await asyncio.wait_for(prompts.get(), 3) == "1 16 "
            keys.send_text("\x1b[3~" * 9 + "2.5\r")
            assert (await asyncio.wait_for(task, 3))["changed"]
        assert calls == [LINE.replace("16 0", "16 2.5")]

    asyncio.run(check())


def test_occurrence_edit_preserves_siblings_colours_affine_transforms_and_sources(build):
    original = build(PROGRAM, suffix=".mpd", individual_parts=True)
    source = Path(original.report["source"])
    unchanged = source.read_bytes()
    edited_line = "1 16 10 -20 30 -1 .2 0 0 1 0 0 0 1 cube.dat"
    edited = build(
        PROGRAM, suffix=".mpd", individual_parts=True, placement_overrides={"0/0": edited_line}
    )
    before = {p["id"]: p for p in original.report["occurrences"]}
    after = {p["id"]: p for p in edited.report["occurrences"]}
    assert before["1/0"] == after["1/0"]
    assert after["0/0"]["colour"] == 4
    assert after["0/0"]["position_ldu"] == [10, -20, 30]
    assert after["0/0"]["matrix_ldraw"][0] == [-1, 0.2, 0]
    nodes = {n["id"]: n for n in edited.report["instances"]}
    assert nodes["0/0"]["source_text"] == edited_line
    assert nodes["1/0"]["source_text"] == LINE
    assert nodes["0/0"]["source_file"] == nodes["1/0"]["source_file"] == str(source)
    assert nodes["0/0"]["line"] == nodes["1/0"]["line"] == 5
    assert source.read_bytes() == unchanged
    assert edited.report["source_sha256"] == original.report["source_sha256"]


@pytest.mark.integration
@pytest.mark.skipif(
    importlib.util.find_spec("mujoco_mcp") is None, reason="Install the interpreter extra"
)
def test_real_edit_undo_history_and_failed_staging(tmp_path, small_library):
    source = tmp_path / "edit.mpd"
    source.write_text(PROGRAM)
    original_source = source.read_bytes()

    async def check():
        async with Interpreter.open(
            source, library=small_library, shadows=[], output_dir=tmp_path / "execution"
        ) as program:
            await program.step_over()
            original_xml = program.xml
            before = program.status
            state = await program._call("sim_get_state")
            first_line = LINE.replace("16 0", "16 10")
            second_line = LINE.replace("16 0", "16 20")
            result = await program.edit("0/0", first_line)
            assert result["changed"]
            assert program.status == before
            assert program.placement_line("1/0") == LINE
            assert program.placement_line("0/0") == first_line
            first_state = await program._call("sim_get_state")
            await program.edit("0/0", second_line)
            assert (await program.undo())["undone_command"] == "edit"
            assert program.placement_line("0/0") == first_line
            assert await program._call("sim_get_state") == first_state
            assert (await program.undo())["undone_command"] == "edit"
            assert program.placement_line("0/0") == LINE
            assert program.xml == original_xml
            assert await program._call("sim_get_state") == state
            assert not program.report["placement_overrides"]
            assert (await program.undo())["undone_command"] == "next"
            assert (await program.undo())["undone_command"] is None
            assert program.placement_line("0/0") == LINE
            assert not (await program.edit("0/0", LINE))["changed"]
            with pytest.raises(EditError):
                await program.edit("0/0", LINE.replace("cube.dat", "missing.dat"))
            assert not program.failed
            await program.run()
            old_slot, old_xml = program.slot, program.xml
            old_state = await program._call("sim_get_state")
            call = program.client.call

            async def fail(tool, **args):
                if tool == "sim_step" and args.get("sim_name") != old_slot:
                    raise MCPError("injected staging failure")
                return await call(tool, **args)

            program.client.call = fail
            with pytest.raises(MCPError, match="staging"):
                await program.edit("0/0", first_line)
            program.client.call = call
            assert not program.failed
            assert program.slot == old_slot and program.xml == old_xml
            assert await program._call("sim_get_state") == old_state
            assert len((await program.client.call("sim_list"))["slots"]) == 2
            records = [
                json.loads(line)
                for line in (program.output_dir / "events.jsonl").read_text().splitlines()
            ]
            assert len([r for r in records if r["kind"] == "edit"]) == 2
            assert source.read_bytes() == original_source
            assert list((program.output_dir / "revisions").glob("*/scene.xml"))
            parent = program.placement_line("0")
            await program.edit("0", parent.replace("4 0", "4 25", 1))
            assert program.placement_line("1") == f"1 1 100 0 0 {IDENTITY} sub.ldr"
            assert (await program.undo())["undone_command"] == "edit"
            assert program.placement_line("0") == parent
            assert await program._call("sim_get_state") == old_state

    asyncio.run(check())


@pytest.mark.integration
@pytest.mark.skipif(
    importlib.util.find_spec("mujoco_mcp") is None, reason="Install the interpreter extra"
)
def test_terminal_edit_then_undo_to_original(tmp_path, small_library):
    source = tmp_path / "terminal.mpd"
    source.write_text(PROGRAM)

    async def check():
        async with Interpreter.open(source, library=small_library, shadows=[]) as program:
            commands = iter(["e", "edit 0/0", "u", "u", "q"])
            output = []

            async def read():
                return next(commands)

            async def prompt(*args, **kwargs):
                return " ".join(LINE.replace("16 0", "16 10").split()[2:14])

            assert await terminal(program, read=read, write=output.append, edit_prompt=prompt) == 0
            assert "Undid edit." in output
            assert "Nothing to undo." in output
            assert program.placement_line("0/0") == LINE
            assert not program.enabled

    asyncio.run(check())
