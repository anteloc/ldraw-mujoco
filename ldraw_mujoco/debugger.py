"""A deliberately small terminal front end to the asynchronous interpreter."""

import json
import sys

from .interpreter import ExecutionError, Interpreter
from .mcp import MCPError

HELP = "step (s), next (n), finish (f), continue (c), where (w), reset (r), help (h), quit (q)"


def describe(status):
    instruction = status["next_instruction"]
    if instruction is None:
        return f"Finished: {len(status['enabled_ids'])} parts enabled."
    return (
        f"{instruction['source_file']}:{instruction['line']} "
        f"[{instruction['section']}, {instruction['id']}] {instruction['reference']}"
    )


async def terminal(program, *, read=None, write=print):
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
        "finish": program.step_out,
        "f": program.step_out,
        "continue": program.run,
        "c": program.run,
        "reset": program.reset,
        "r": program.reset,
    }
    write(HELP)
    write(describe(program.status))
    while True:
        try:
            command = (await read()).strip().lower()
        except EOFError:
            return int(program.failed)
        if command in {"quit", "q"}:
            return int(program.failed)
        if command in {"help", "h", "?"}:
            write(HELP)
        elif command in {"where", "w"}:
            write(json.dumps(program.status, indent=2))
        elif command in methods:
            try:
                result = await methods[command]()
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
            write(f"Unknown command: {command}. {HELP}")


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
    ) as program:
        if args.viewer:
            try:
                await program.viewer()
            except MCPError as exc:
                print(f"Viewer unavailable; terminal execution is ready: {exc}", file=sys.stderr)
        return await terminal(program)
