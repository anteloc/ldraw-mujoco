"""A deliberately small terminal front end to the asynchronous interpreter."""

import json
import sys

from .editing import edit_placement
from .interpreter import ExecutionError, Interpreter
from .mcp import MCPError

COMMANDS = (
    "step (s), next (n), undo (u), finish (f), continue (c), "
    "inspect (i), edit (e) <part id>, where (w), reset (r), help (h), quit (q)"
)
HELP = """step (s) - Execute one instruction, entering submodels.
next (n) - Execute the next instruction, completing submodel calls.
undo (u) - Undo the last execution command or edit.
finish (f) - Finish the current submodel; at root, finish the program.
continue (c) - Execute the rest of the program.
inspect (i) - Show current physics as JSON, with part IDs.
edit (e) <part id> - Edit one occurrence's type-1 placement line for this session.
where (w) - Show the call stack and next instruction.
reset (r) - Disable all parts, rewind, and clear undo history.
help (h) - Show this command list.
quit (q) - Exit the debugger and close its viewer and server."""


def describe(status):
    instruction = status["next_instruction"]
    if instruction is None:
        return f"Finished: {len(status['enabled_ids'])} parts enabled."
    return (
        f"{instruction['source_file']}:{instruction['line']} "
        f"[{instruction['section']}, {instruction['id']}] {instruction['reference']}"
    )


async def terminal(program, *, read=None, write=print, edit_prompt=None):
    """Return an exit status; injected text I/O also allows scripted sessions."""
    if read is None:
        if sys.stdin.isatty():
            from prompt_toolkit import PromptSession

            session = PromptSession("ldraw> ")
            read = session.prompt_async
        else:
            # Piped commands run while physics is paused. Read on the main thread
            # so Ctrl+C can interrupt input without leaving a worker behind.
            async def read():
                return input("ldraw> ")

    methods = {
        "step": program.step_into,
        "s": program.step_into,
        "next": program.step_over,
        "n": program.step_over,
        "undo": program.undo,
        "u": program.undo,
        "finish": program.step_out,
        "f": program.step_out,
        "continue": program.run,
        "c": program.run,
        "reset": program.reset,
        "r": program.reset,
    }
    write(COMMANDS)
    write(describe(program.status))
    while True:
        try:
            entered = (await read()).strip().split(maxsplit=1)
            command = entered[0].lower() if entered else ""
            argument = entered[1] if len(entered) > 1 else ""
        except EOFError:
            return int(program.failed)
        if command in {"quit", "q"}:
            return int(program.failed)
        if command in {"help", "h", "?"}:
            write(HELP)
        elif command in {"where", "w"}:
            write(json.dumps(program.status, indent=2))
        elif command in {"inspect", "i"}:
            try:
                write(json.dumps(await program.inspect(), indent=2, allow_nan=False))
            except (ExecutionError, MCPError) as exc:
                write(json.dumps({"kind": "inspect", "error": str(exc), "failed": program.failed}))
        elif command in {"edit", "e"}:
            if not argument:
                write("Usage: edit (e) <part id>")
                continue
            try:
                result = await edit_placement(program, argument, prompt=edit_prompt, write=write)
                if result is not None:
                    write(f"Edited {argument}." if result["changed"] else "Line unchanged.")
                    if program.viewer_error:
                        write(f"Viewer unavailable: {program.viewer_error}")
                    write(describe(result))
            except (ValueError, ExecutionError, MCPError) as exc:
                write(f"Edit not applied: {exc}")
        elif command in methods:
            try:
                result = await methods[command]()
                if "undone_command" in result:
                    undone = result["undone_command"]
                    write(f"Undid {undone}." if undone else "Nothing to undo.")
                for event in result["events"]:
                    instruction = event["instruction"]
                    if event["kind"] == "call":
                        write(f"Call {instruction['reference']} [{instruction['id']}]")
                    else:
                        physics = event["physics"]
                        write(
                            f"Placed {instruction['id']}: {physics['actual_duration_s']:.3f}s, "
                            f"{physics['contact_count']} contacts"
                        )
                write(describe(result))
            except (ExecutionError, MCPError) as exc:
                write(f"Execution halted: {exc}. Use reset or quit.")
        elif command:
            write(f"Unknown command: {command}. {COMMANDS}")


async def execute(args):
    async with Interpreter.open(
        args.input,
        seconds_per_part=args.seconds_per_part,
        output_dir=args.output_dir or f"output/{args.input.stem}/execution",
        library=args.library,
        shadows=[] if args.no_shadow else args.shadow,
        density=args.density,
        friction=args.friction,
        timestep=args.timestep,
        clearance=args.clearance,
        viewer=args.viewer,
    ) as program:
        if program.viewer_error:
            print(
                f"Viewer unavailable; terminal execution is ready: {program.viewer_error}",
                file=sys.stderr,
            )
        return await terminal(program)
