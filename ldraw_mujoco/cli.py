"""Inspect source instances, convert an LDraw input, or simulate its MJCF."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

import mujoco

from .importer import import_ldraw, inspect_ldraw
from .simulation import _simulate, snapshot


def write_json(path, report):
    text = json.dumps(report, indent=2, allow_nan=False) + "\n"
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text)


def import_arguments(parser):
    parser.add_argument("--library", type=Path)
    shadow = parser.add_mutually_exclusive_group()
    shadow.add_argument(
        "--shadow", action="append", type=Path, help="Repeat for multiple shadow sources"
    )
    shadow.add_argument("--no-shadow", action="store_true")
    parser.add_argument("--density", type=float, default=1050, help="Estimated density in kg/m³")
    parser.add_argument("--friction", type=float, default=0.6, help="Sliding friction coefficient")
    parser.add_argument("--timestep", type=float, default=0.001, help="Seconds")
    parser.add_argument(
        "--clearance", type=float, default=0.001, help="Initial ground clearance in meters"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Import LDraw rigid assemblies into MuJoCo")
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="List part/submodel instance IDs as JSON")
    inspect.add_argument("input", type=Path)
    convert = commands.add_parser("convert", help="Convert MPD/LDR/DAT to self-contained MJCF")
    convert.add_argument("input", type=Path)
    convert.add_argument("--output", type=Path, required=True)
    convert.add_argument("--connections", type=Path, help="Source-bound connection JSON; requires --individual-parts")
    convert.add_argument("--collision", choices=["hull", "decomposed"], default="hull")
    convert.add_argument("--collision-tolerance", type=float, default=0.00005, help="CoACD concavity threshold in meters")
    convert.add_argument("--contact-solref", type=float, nargs=2, metavar=("TIMECONST", "DAMPRATIO"))
    convert.add_argument("--contact-solimp", type=float, nargs=3, metavar=("DMIN", "DMAX", "WIDTH"))
    import_arguments(convert)
    convert.add_argument(
        "--section",
        action="append",
        metavar="SECTION[:ID]",
        help="Unique section name or SECTION:ID; repeat to select several. "
        "Use inspect to discover IDs. Preserves original placements.",
    )
    convert.add_argument(
        "--individual-parts",
        action="store_true",
        help="One independent free body per placed DAT part, never per geometric subpart",
    )
    execute = commands.add_parser("execute", help="Debug type-1 placements through MuJoCo MCP")
    execute.add_argument("input", type=Path)
    import_arguments(execute)
    execute.add_argument("--seconds-per-part", type=float, default=0.1)
    execute.add_argument("--output-dir", type=Path, help="Default: output/INPUT_STEM/execution")
    execute.add_argument(
        "--viewer", action="store_true", help="Open an independent browser inspection viewer"
    )
    run = commands.add_parser("simulate", help="Simulate MJCF and report approximate behavior")
    run.add_argument("input", type=Path)
    run.add_argument("--seconds", type=float, default=5)
    run.add_argument("--report", type=Path, help="Default: INPUT.simulation.json")
    run.add_argument("--snapshot", type=Path, help="Save the final scene as PNG")
    run.add_argument(
        "--viewer", action="store_true", help="Open an independent browser inspection viewer"
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            print(json.dumps(inspect_ldraw(args.input), indent=2, allow_nan=False))
        elif args.command == "execute":
            from .debugger import execute

            return asyncio.run(execute(args))
        elif args.command == "convert":
            if args.output.resolve() == args.input.resolve():
                raise ValueError("Output must not overwrite the LDraw input")
            result = import_ldraw(
                args.input,
                library=args.library,
                shadows=[] if args.no_shadow else args.shadow,
                individual_parts=args.individual_parts,
                sections=args.section,
                density=args.density,
                friction=args.friction,
                timestep=args.timestep,
                clearance=args.clearance,
                connections=args.connections,
                collision=args.collision,
                collision_tolerance=args.collision_tolerance,
                contact_solref=args.contact_solref,
                contact_solimp=args.contact_solimp,
            )
            xml = result.spec.to_xml()
            # Check the artifact the user will actually load, before writing it.
            mujoco.MjModel.from_xml_string(xml)
            report_path = args.output.with_suffix(".import.json")
            report_text = json.dumps(result.report, indent=2, allow_nan=False) + "\n"
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(xml)
            report_path.write_text(report_text)
            print(
                f"Wrote {args.output} and {report_path}: "
                f"{result.report['occurrence_count']} occurrences, {len(result.report['bodies'])} rigid bodies"
            )
        else:
            from .viewer import browser_session

            print("Loading and compiling XML…", file=sys.stderr)
            model = mujoco.MjModel.from_xml_path(str(args.input.resolve()))
            with browser_session(model, enabled=args.viewer) as handle:
                data, report = _simulate(model, seconds=args.seconds, handle=handle)
                report_path = args.report or args.input.with_suffix(".simulation.json")
                write_json(report_path, report)
                if args.snapshot:
                    snapshot(model, data, args.snapshot)
                print(
                    f"Wrote {report_path}: time={data.time:.3f}s, "
                    f"contacts={data.ncon}, numerical warnings={report['warnings']}"
                )
                if handle is not None and sys.stdin.isatty():
                    try:
                        input("Final scene available in the browser. Press Enter to exit. ")
                    except (EOFError, KeyboardInterrupt):
                        pass
            return 0 if report["numerically_valid"] else 1
    except (OSError, ValueError, RuntimeError, ExceptionGroup) as exc:
        print(f"ldraw-mujoco: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Execution interrupted; reopen the interpreter to restart.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
