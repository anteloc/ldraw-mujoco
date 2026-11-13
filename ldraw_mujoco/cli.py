"""Two ordinary commands: convert an LDraw input, simulate the resulting MJCF."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import mujoco

from .importer import import_ldraw
from .simulation import simulate, snapshot


def write_json(path, report):
    text = json.dumps(report, indent=2, allow_nan=False) + "\n"
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Import LDraw rigid assemblies into MuJoCo")
    commands = parser.add_subparsers(dest="command", required=True)
    convert = commands.add_parser("convert", help="Convert MPD/LDR/DAT to self-contained MJCF")
    convert.add_argument("input", type=Path)
    convert.add_argument("--output", type=Path, required=True)
    convert.add_argument("--library", type=Path)
    shadow = convert.add_mutually_exclusive_group()
    shadow.add_argument(
        "--shadow", action="append", type=Path, help="Repeat for multiple shadow sources"
    )
    shadow.add_argument("--no-shadow", action="store_true")
    convert.add_argument("--grouping", choices=["model", "top-level"], default="model")
    convert.add_argument("--density", type=float, default=1050, help="Estimated density in kg/m³")
    convert.add_argument("--friction", type=float, default=0.6, help="Sliding friction coefficient")
    convert.add_argument("--timestep", type=float, default=0.001, help="Seconds")
    convert.add_argument(
        "--clearance", type=float, default=0.001, help="Initial ground clearance in meters"
    )
    run = commands.add_parser("simulate", help="Simulate MJCF and report approximate behavior")
    run.add_argument("input", type=Path)
    run.add_argument("--seconds", type=float, default=5)
    run.add_argument("--report", type=Path, help="Default: INPUT.simulation.json")
    run.add_argument("--snapshot", type=Path, help="Save the final scene as PNG")
    run.add_argument(
        "--viewer", action="store_true", help="Interactive viewer; use mjpython on macOS"
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "convert":
            if args.output.resolve() == args.input.resolve():
                raise ValueError("Output must not overwrite the LDraw input")
            result = import_ldraw(
                args.input,
                library=args.library,
                shadows=[] if args.no_shadow else args.shadow,
                grouping=args.grouping,
                density=args.density,
                friction=args.friction,
                timestep=args.timestep,
                clearance=args.clearance,
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
            model = mujoco.MjModel.from_xml_path(str(args.input.resolve()))
            data, report = simulate(model, seconds=args.seconds, viewer=args.viewer)
            report_path = args.report or args.input.with_suffix(".simulation.json")
            write_json(report_path, report)
            if args.snapshot:
                snapshot(model, data, args.snapshot)
            print(
                f"Wrote {report_path}: time={data.time:.3f}s, "
                f"contacts={data.ncon}, numerical warnings={report['warnings']}"
            )
            return 0 if report["numerically_valid"] else 1
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ldraw-mujoco: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
