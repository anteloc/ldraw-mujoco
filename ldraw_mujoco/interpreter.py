"""Execute parsed type-1 placements with debugger-style submodel calls."""

from __future__ import annotations

import asyncio
import hashlib
import json
import math
import shutil
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

import mujoco
import numpy as np

from .editing import EditError, field_spans, validate_placement
from .importer import ImportedModel, import_ldraw
from .mcp import MCPError, MujocoClient


def _json_safe(value):
    """Keep diagnostic records valid JSON even when a server reports NaN/Inf."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    return value


class ExecutionError(RuntimeError):
    """Execution stopped; result retains completed events and the failing instruction."""

    def __init__(self, message, result):
        super().__init__(message)
        self.result = result


class Interpreter:
    """One full source program and one owned MCP scene; operations are sequential.

    Use ``async with Interpreter.open(path) as program``. Each DAT placement
    starts a fresh trial from CAD with the accumulated set of enabled parts.
    Call events are observations of execution, not subroutine return values.
    """

    def __init__(self, imported, *, seconds_per_part=0.1, output_dir=None):
        if not math.isfinite(seconds_per_part) or seconds_per_part <= 0:
            raise ValueError("seconds_per_part must be finite and positive")
        self.report = imported.report
        if not self.report["individual_parts"] or self.report["selected_instances"] != ["root"]:
            raise ValueError("Execution requires the full input in individual-parts mode")
        self.seconds_per_part = seconds_per_part
        self.nodes = {n["id"]: n for n in self.report["instances"]}
        self.children = {n: [] for n in self.nodes}
        for node in self.nodes.values():
            if node["parent_id"] is not None:
                self.children[node["parent_id"]].append(node["id"])
        names = {p["body"] for p in self.report["occurrences"]}
        for body in imported.spec.bodies:
            if body.name in names:
                body.gravcomp = 1
        # Compile with collisions present so MuJoCo retains collision structures.
        # Nonzero gravcomp at compile time also initializes its cached body count.
        self.xml = imported.spec.to_xml()
        model = imported.spec.compile()
        self._model = model
        self._viewer = None
        self._disableflags = int(model.opt.disableflags)
        self._prepare_bootstrap()
        self.timestep = float(model.opt.timestep)
        self.steps = math.ceil(seconds_per_part / self.timestep)
        self.parts, self.activate, self.inactive = {}, {}, []
        self.geom_ids = {"ground": None}
        for occurrence in self.report["occurrences"]:
            ident, body = occurrence["id"], model.body(occurrence["body"])
            joint = int(body.jntadr[0])
            if body.jntnum[0] != 1 or model.jnt_type[joint] != mujoco.mjtJoint.mjJNT_FREE:
                raise ValueError(
                    "Execution requires one free body per part; import with attach=False"
                )
            qa, va = int(model.jnt_qposadr[joint]), int(model.jnt_dofadr[joint])
            self.parts[ident] = {
                "body": body.name,
                "qpos_address": qa,
                "qvel_address": va,
                "initial_qpos": model.qpos0[qa : qa + 7].tolist(),
            }
            active, inactive = [], []
            for field, enabled, disabled in (
                ("gravcomp", 0, 1),
                ("contype", int(model.body_contype[body.id]), 0),
                ("conaffinity", int(model.body_conaffinity[body.id]), 0),
            ):
                mod = {"element": "body", "name": body.name, "field": field}
                active.append({**mod, "value": enabled})
                inactive.append({**mod, "value": disabled})
            for name in [occurrence["collision_geom"], *occurrence["visual_geoms"]]:
                self.geom_ids[name] = ident
                geom = model.geom(name)
                rgba = geom.rgba.tolist()
                for field, enabled, disabled in (
                    ("contype", int(geom.contype[0]), 0),
                    ("conaffinity", int(geom.conaffinity[0]), 0),
                    ("rgba", rgba, [*rgba[:3], 0]),
                ):
                    mod = {"element": "geom", "name": name, "field": field}
                    active.append({**mod, "value": enabled})
                    inactive.append({**mod, "value": disabled})
            self.activate[ident] = active
            self.inactive.extend(inactive)
        self.model_dimensions = {k: int(getattr(model, k)) for k in ("nq", "nv", "nbody")}
        self.slot = "ldraw-" + uuid4().hex
        self._spare_slot = self.slot + "-edit"
        options = self.report["options"]
        self._import_options = {
            "library": self.report["library"],
            "shadows": self.report["shadows"],
            "density": options["density_kg_m3"],
            "friction": options["sliding_friction"],
            "timestep": options["timestep_s"],
            "clearance": options["ground_clearance_m"],
            "solver": options["solver"],
        }
        self.client = None
        self.enabled = []
        self._stack = []
        self._history = []
        self._state = None
        self.failed = False
        self.last_result = None
        self._busy = False
        self.viewer_error = None
        self.output_dir = Path(output_dir) if output_dir is not None else None
        self.preparation = {
            "xml_sha256": hashlib.sha256(self.xml.encode()).hexdigest(),
            "bootstrap_xml_sha256": hashlib.sha256(self._bootstrap_xml.encode()).hexdigest(),
            "restored_disableflags": self._disableflags,
            "seconds_per_part": seconds_per_part,
            "steps_per_part": self.steps,
            "timestep_s": self.timestep,
            "reset_policy": "CAD poses and zero velocity per placement",
            "parts": self.parts,
            "placement_overrides": self.report.get("placement_overrides", {}),
            "initial_modifications": self.inactive,
            "activation_modifications": self.activate,
            "interpretation": "Approximate rigid-body observations; caller decides placement success. "
            "Final-state checks do not establish numerical validity throughout a trial or attachment strength.",
        }

    @classmethod
    @asynccontextmanager
    async def open(
        cls, path, *, seconds_per_part=0.1, output_dir=None, viewer=False, **import_options
    ):
        """Convert the source and own a stdio server until the context exits.

        Import options are those of ``import_ldraw``, except selection/grouping and
        attachment: every part is its own free body (``attach=False``).
        ``output_dir`` saves the exact XML, reports and a flushed JSONL event log.
        ``viewer=True`` opens an independent browser viewer and paces connected playback.
        A failed window launch is recorded in ``viewer_error``; execution remains available.
        """
        if {"sections", "individual_parts", "attach"} & import_options.keys():
            raise ValueError(
                "The interpreter always executes the full input as individual free parts"
            )
        started = time.monotonic()
        print("Importing and compiling LDraw geometry…", file=sys.stderr)
        imported = import_ldraw(path, individual_parts=True, attach=False, **import_options)
        imported_at = time.monotonic()
        print("Preparing execution model…", file=sys.stderr)
        program = cls(
            imported,
            seconds_per_part=seconds_per_part,
            output_dir=output_dir,
        )
        del imported  # The editable spec is large; execution retains the compiled model and XML.
        program._import_options.update(
            {
                k: v
                for k, v in import_options.items()
                if v is not None and k != "placement_overrides"
            }
        )
        program.preparation["timings_s"] = {
            "import": imported_at - started,
            "prepare": time.monotonic() - imported_at,
        }
        if program.output_dir is not None:
            program.output_dir.mkdir(parents=True, exist_ok=True)
            (program.output_dir / "events.jsonl").write_text("")
        log_path = program.output_dir / "server.log" if program.output_dir else None
        try:
            if viewer:
                print("Preparing browser scene…", file=sys.stderr)
                before = time.monotonic()
                try:
                    await program.viewer()
                except MCPError as exc:
                    program.viewer_error = str(exc)
                program.preparation["timings_s"]["browser"] = time.monotonic() - before
            print("Loading physics with inactive parts…", file=sys.stderr)
            async with MujocoClient.connect(log_path=log_path) as client:
                await program._load(client)
                print(f"Execution ready ({time.monotonic() - started:.1f}s).", file=sys.stderr)
                yield program
        finally:
            if program._viewer is not None:
                program._viewer.close()
            program.client = None

    def _prepare_bootstrap(self):
        # This is MJCF, not LDraw. Preserve the canonical artifact separately.
        root = ET.fromstring(self.xml)
        option = root.find("option")
        if option is None:
            option = ET.SubElement(root, "option")
        flag = option.find("flag")
        if flag is None:
            flag = ET.SubElement(option, "flag")
        flag.set("contact", "disable")
        self._bootstrap_xml = ET.tostring(root, encoding="unicode")

    async def _call(self, tool, **arguments):
        if self.client is None:
            raise RuntimeError("Interpreter is closed; use Interpreter.open()")
        return await self.client.call(tool, sim_name=self.slot, **arguments)

    async def _load(self, client):
        self.client = client
        before = time.monotonic()
        # The owned stdio server shares this filesystem. Retain the bootstrap
        # through loading; do not put a large mesh payload into a JSON request.
        with tempfile.TemporaryDirectory(prefix="ldraw-bootstrap-") as directory:
            path = Path(directory) / "bootstrap.xml"
            path.write_text(self._bootstrap_xml)
            summary = await client.call("sim_load", name=self.slot, xml_path=str(path))
        # modify_model runs forward automatically: leave contacts disabled until
        # every inactive mask has been applied successfully, then restore options.
        await self._call("modify_model", modifications=self.inactive)
        await self._call(
            "modify_model",
            modifications=[
                {
                    "element": "option",
                    "field": "disableflags",
                    "value": self._disableflags,
                }
            ],
        )
        self.preparation.setdefault("timings_s", {})["physics_load"] = time.monotonic() - before
        if any(summary[k] != v for k, v in self.model_dimensions.items()):
            raise MCPError("Loaded model dimensions differ from the prepared XML")
        if not set(p["body"] for p in self.parts.values()) <= set(summary["bodies"]):
            raise MCPError("Loaded model is missing expected part bodies")
        if self.output_dir is not None:
            self._save_scene()
            (self.output_dir / "events.jsonl").touch(exist_ok=True)
        self._record(
            {"kind": "load", "xml_sha256": self.preparation["xml_sha256"], "server": summary}
        )
        await self.reset()

    def _save_scene(self):
        if self.output_dir is None:
            return
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "scene.xml").write_text(self.xml)
        (self.output_dir / "bootstrap.xml").write_text(self._bootstrap_xml)
        for name, payload in (
            ("scene.import.json", self.report),
            ("execution.json", self.preparation),
        ):
            (self.output_dir / name).write_text(
                json.dumps(payload, indent=2, allow_nan=False) + "\n"
            )

    def placement_line(self, ident):
        """Return this occurrence's current type-1 line, including session edits."""
        if ident not in self.nodes or self.nodes[ident]["kind"] == "model":
            raise ValueError(
                f"Unknown type-1 occurrence ID: {ident!r}; use where or inspect to find IDs"
            )
        if self.nodes[ident].get("generated"):
            raise ValueError("Inline geometry has no source placement; edit its parent assembly")
        return self.nodes[ident]["source_text"]

    async def edit(self, ident, line):
        """Edit one type-1 occurrence transform for this session, preserving execution position."""
        self._check_ready()
        original = self.placement_line(ident)
        validate_placement(line, original=original)
        if line == original:
            return {"events": [], **self.status, "edited_id": ident, "changed": False}
        self._busy = True
        try:
            overrides = {**self.report.get("placement_overrides", {}), ident: line}
            try:
                imported = import_ldraw(
                    self.report["source"],
                    individual_parts=True,
                    attach=False,
                    placement_overrides=overrides,
                    **self._import_options,
                )
            except (ValueError, OSError) as exc:
                field = 1 if "color" in str(exc).lower() else 14
                start = field_spans(line)[field][0]
                raise EditError(
                    str(exc),
                    column=start,
                    field_start=start,
                    suggestion="Check the DAT reference and placement values, then edit or cancel",
                ) from exc
            checkpoint = {
                "command": "edit",
                "edited_id": ident,
                "stack": [frame.copy() for frame in self._stack],
                "enabled": list(self.enabled),
                "state": await self._call("sim_get_state") if self.enabled else None,
                # Exact old geometry makes undo independent of subsequent source/library changes.
                "xml": self.xml,
                "report": self.report,
            }
            physics = await self._replace_scene(
                imported, checkpoint, [*self._history, checkpoint], restore_state=False
            )
            self.last_result = {
                "events": [],
                **self.status,
                "edited_id": ident,
                "changed": True,
                "source_text": line,
                "physics": physics,
            }
            self._record(
                {
                    "kind": "edit",
                    "before": original,
                    "after": line,
                    "xml_sha256": self.preparation["xml_sha256"],
                    **self.last_result,
                }
            )
            return self.last_result
        finally:
            self._busy = False

    async def _replace_scene(self, imported, checkpoint, history, *, restore_state):
        """Prepare in a spare MCP slot; a rejected edit leaves the current scene intact."""
        candidate = Interpreter(imported, seconds_per_part=self.seconds_per_part)
        if restore_state:
            candidate.xml = checkpoint["xml"]
            candidate._prepare_bootstrap()
            candidate.preparation["bootstrap_xml_sha256"] = hashlib.sha256(
                candidate._bootstrap_xml.encode()
            ).hexdigest()
            candidate.preparation["xml_sha256"] = hashlib.sha256(candidate.xml.encode()).hexdigest()
        candidate.slot, candidate._spare_slot = self._spare_slot, self.slot
        candidate._import_options = dict(self._import_options)
        await candidate._load(self.client)
        enabled = checkpoint["enabled"]
        physics = None
        if enabled:
            modifications = [m for ident in enabled[:-1] for m in candidate.activate[ident]]
            if modifications:
                await candidate._call("modify_model", modifications=modifications)
            candidate.enabled = list(enabled[:-1])
            physics = await candidate._place(enabled[-1])
            if not physics["state_finite"] or not physics["duration_matches"]:
                raise MCPError("Edited scene produced invalid physics; the edit was not applied")
            candidate.enabled.append(enabled[-1])
            if restore_state:
                state = checkpoint["state"]
                await candidate._call("sim_set_state", qpos=state["qpos"], qvel=state["qvel"])
                candidate._state = state
        candidate._stack = [frame.copy() for frame in checkpoint["stack"]]
        candidate._history = list(history)
        candidate.output_dir = self.output_dir
        if self.output_dir is not None:
            archive = self.output_dir / "revisions" / self.preparation["xml_sha256"]
            archive.mkdir(parents=True, exist_ok=True)
            for name in ("scene.xml", "bootstrap.xml", "scene.import.json", "execution.json"):
                shutil.copy2(self.output_dir / name, archive / name)
        candidate._save_scene()
        browser = self._viewer
        self.__dict__.update(candidate.__dict__)
        self._busy = True
        self._viewer = browser
        if browser is not None:
            try:
                browser.set_scene(self._model, enabled_bodies=self._enabled_bodies(self.enabled))
                self._publish(self._state, self.enabled)
            except Exception as exc:
                self._viewer_failed(exc)
        return physics

    def _record(self, event):
        if self.output_dir is not None:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            with (self.output_dir / "events.jsonl").open("a") as stream:
                stream.write(json.dumps(_json_safe(event), allow_nan=False) + "\n")

    def _unwind(self):
        while self._stack and self._stack[-1][1] == len(self.children[self._stack[-1][0]]):
            self._stack.pop()

    @property
    def status(self):
        """A local debugger snapshot; no physics calls or state changes."""
        next_node = None
        if self._stack:
            parent, index = self._stack[-1]
            next_node = dict(self.nodes[self.children[parent][index]])
        return {
            "stack": [
                {
                    "instance_id": ident,
                    "section": self.nodes[ident]["reference"],
                    "next_index": index,
                }
                for ident, index in self._stack
            ],
            "next_instruction": next_node,
            "done": not self._stack,
            "enabled_ids": list(self.enabled),
            "failed": self.failed,
        }

    async def reset(self):
        """Recover from failures, disable every part and rewind the program."""
        if self._busy:
            raise RuntimeError("Wait for the current debugger operation before resetting")
        self._busy, self.failed = True, True
        try:
            await self._call("modify_model", modifications=self.inactive)
            await self._call("sim_reset")
            self.enabled = []
            self._stack = [["root", 0]]
            self._history.clear()
            self._state = None
            self._unwind()
            self.failed = False
            result = {"events": [], **self.status}
            self.last_result = result
            self._record({"kind": "reset", **result})
            self._publish(None, [])
            return result
        finally:
            self._busy = False

    async def viewer(self):
        """Open/reopen the local browser; simulation remains in the MCP process."""
        from .viewer import BrowserViewer

        try:
            if self._viewer is None:
                self._viewer = BrowserViewer(
                    self._model, enabled_bodies=self._enabled_bodies(self.enabled)
                )
            self._publish(
                self._state,
                self.enabled,
                status="Loading physics" if self.client is None else "Paused",
            )
            result = self._viewer.open()
            self.viewer_error = (
                None if result["opened"] else "Open the printed browser URL manually"
            )
            self._record({"kind": "viewer_open", **result})
            return result
        except Exception as exc:
            self._viewer_failed(exc)
            raise MCPError(f"Browser viewer unavailable: {exc}") from exc

    def _enabled_bodies(self, enabled):
        return [self._model.body(self.parts[ident]["body"]).id for ident in enabled]

    def _viewer_failed(self, exc):
        self.viewer_error = str(exc)
        if self._viewer is not None:
            self._viewer.close()
            self._viewer = None
        self._record({"kind": "viewer_unavailable", "error": str(exc)})
        print(f"Browser viewer unavailable: {exc}", file=sys.stderr)

    def _publish(self, state, enabled, *, status="Paused"):
        if self._viewer is not None:
            try:
                self._viewer.publish(
                    self._model.qpos0 if state is None else state["qpos"],
                    self._enabled_bodies(enabled),
                    status=status,
                )
            except Exception as exc:
                self._viewer_failed(exc)

    def _check_ready(self):
        if self._busy:
            raise RuntimeError("Debugger operations must be sequential")
        if self.failed:
            raise ExecutionError(
                "Execution halted; call reset() or reopen", {"events": [], **self.status}
            )

    async def undo(self):
        """Undo one execution command or edit; reset clears this session's history."""
        self._check_ready()
        if not self._history:
            self.last_result = {"events": [], **self.status, "undone_command": None}
            return self.last_result
        checkpoint = self._history[-1]
        self._busy = True
        try:
            if checkpoint["command"] == "edit":
                spec = mujoco.MjSpec.from_string(checkpoint["xml"])
                # Execution never attaches parts, so it needs no connector features.
                imported = ImportedModel(spec, checkpoint["report"], spec.compile(), {})
                await self._replace_scene(
                    imported, checkpoint, self._history[:-1], restore_state=True
                )
            elif checkpoint["enabled"] != self.enabled:
                modifications = list(self.inactive)
                for ident in checkpoint["enabled"]:
                    modifications.extend(self.activate[ident])
                await self._call("modify_model", modifications=modifications)
                state = checkpoint["state"]
                if state is None:
                    await self._call("sim_reset")
                else:
                    # Every completed trial has the same duration. Keep that
                    # time; sim_set_state restores motion and refreshes contacts
                    # and the viewer without advancing physics. Solver caches
                    # need no checkpoint: the next placement resets them to CAD.
                    restored = await self._call(
                        "sim_set_state", qpos=state["qpos"], qvel=state["qvel"]
                    )
                    if not math.isclose(restored["time"], state["time"], abs_tol=1e-12):
                        raise MCPError("Restored simulation time differs from the checkpoint")
            self.enabled = checkpoint["enabled"]
            self._stack = checkpoint["stack"]
            self._state = checkpoint["state"]
            if checkpoint["command"] != "edit":
                self._history.pop()
            self.last_result = {
                "events": [],
                **self.status,
                "undone_command": checkpoint["command"],
                "xml_sha256": self.preparation["xml_sha256"],
            }
            self._record({"kind": "undo", **self.last_result})
            self._publish(self._state, self.enabled)
            return self.last_result
        except (Exception, asyncio.CancelledError) as exc:
            self.failed = True
            result = {
                "events": [],
                **self.status,
                "error": str(exc),
                "operation": "undo",
                "failing_instruction": self.status["next_instruction"],
            }
            self.last_result = result
            self._record({"kind": "error", **result})
            if isinstance(exc, asyncio.CancelledError):
                raise
            raise ExecutionError(str(exc), result) from exc
        finally:
            self._busy = False

    async def _place(self, ident):
        await self._call("sim_reset")
        await self._call("modify_model", modifications=self.activate[ident])
        remaining = self.steps
        started = time.monotonic()
        self._publish(None, [*self.enabled, ident], status="Running")
        while remaining:
            connected = self._viewer is not None and self._viewer.connected
            count = min(remaining, max(1, round(0.05 / self.timestep)) if connected else 100_000)
            state = await self._call("sim_step", n_steps=count)
            remaining -= count
            self._publish(state, [*self.enabled, ident], status="Running")
            if connected:
                target = (self.steps - remaining) * self.timestep
                await asyncio.sleep(max(0, target - (time.monotonic() - started)))
        state, physics = await self._observe([*self.enabled, ident])
        self._state = state
        self._publish(state, [*self.enabled, ident])
        return _json_safe(
            {
                **physics,
                "requested_duration_s": self.seconds_per_part,
                "steps": self.steps,
                "actual_duration_s": state["time"],
                "duration_matches": math.isclose(
                    state["time"], self.steps * self.timestep, rel_tol=1e-9, abs_tol=1e-12
                ),
            }
        )

    async def inspect(self):
        """Read current physics as JSON-ready data without stepping or changing history."""
        self._check_ready()
        self._busy = True
        try:
            state, physics = await self._observe(self.enabled)
            result = _json_safe(
                {
                    "kind": "inspect",
                    "xml_sha256": self.preparation["xml_sha256"],
                    "time_s": state["time"],
                    "timestep_s": self.timestep,
                    **self.status,
                    **physics,
                    "units": {"length": "m", "time": "s", "angle": "rad", "force": "N"},
                    "contact_force_frame": "contact",
                    "interpretation": self.preparation["interpretation"],
                }
            )
            self._record(result)
            return result
        finally:
            self._busy = False

    async def _observe(self, enabled):
        """Refresh derived quantities, then query live poses and every contact through MCP."""
        forward = await self._call("sim_forward")
        state = await self._call("sim_get_state")
        contacts = await self._call("analyze_contacts", max_contacts=forward["n_contacts"])
        if (
            len(contacts["contacts"]) != forward["n_contacts"]
            or contacts["n_contacts"] != forward["n_contacts"]
        ):
            raise MCPError("Server returned an incomplete contact list")
        qpos, qvel = np.asarray(state["qpos"]), np.asarray(state["qvel"])
        if qpos.shape != (self.model_dimensions["nq"],) or qvel.shape != (
            self.model_dimensions["nv"],
        ):
            raise MCPError("Server returned unexpected state dimensions")
        bodies = []
        for active in enabled:
            part = self.parts[active]
            qa, va = part["qpos_address"], part["qvel_address"]
            bodies.append(
                {
                    "id": active,
                    "reference": self.nodes[active]["reference"],
                    "body": part["body"],
                    "position_m": qpos[qa : qa + 3].tolist(),
                    "quaternion_wxyz": qpos[qa + 3 : qa + 7].tolist(),
                    "linear_velocity_m_s": qvel[va : va + 3].tolist(),
                    "angular_velocity_rad_s": qvel[va + 3 : va + 6].tolist(),
                    "angular_velocity_frame": "body",
                    "displacement_m": (qpos[qa : qa + 3] - part["initial_qpos"][:3]).tolist(),
                }
            )
        for contact in contacts["contacts"]:
            try:
                contact["part1_id"] = self.geom_ids[contact["geom1"]]
                contact["part2_id"] = self.geom_ids[contact["geom2"]]
            except KeyError as exc:
                raise MCPError(f"Server returned an unknown contact geom: {exc}") from exc
        physics = {
            "state_finite": bool(
                math.isfinite(state["time"]) and np.isfinite(qpos).all() and np.isfinite(qvel).all()
            ),
            "bodies": bodies,
            "contacts": contacts["contacts"],
            "contact_count": contacts["n_contacts"],
        }
        return state, physics

    async def _advance(self, mode):
        self._check_ready()
        self._busy = True
        events = []
        depth = len(self._stack)
        checkpoint = {
            "command": {"into": "step", "over": "next", "out": "finish", "run": "continue"}[mode],
            "stack": [frame.copy() for frame in self._stack],
            "enabled": list(self.enabled),
            "state": self._state,
        }
        try:
            while self._stack:
                instruction = self.status["next_instruction"]
                ident = instruction["id"]
                event = {
                    "kind": "call" if instruction["kind"] == "submodel" else "place",
                    "instruction": instruction,
                    "call_path": [frame[0] for frame in self._stack],
                    "physics": None,
                }
                if event["kind"] == "place":
                    event["physics"] = await self._place(ident)
                    if (
                        not event["physics"]["state_finite"]
                        or not event["physics"]["duration_matches"]
                    ):
                        raise MCPError(
                            "Non-finite final state or unexpected simulation time; reset required"
                        )
                    self.enabled.append(ident)
                self._stack[-1][1] += 1
                if event["kind"] == "call":
                    self._stack.append([ident, 0])
                self._unwind()
                events.append(event)
                self._record(event)
                if (
                    mode == "into"
                    or (mode == "over" and len(self._stack) <= depth)
                    or (mode == "out" and len(self._stack) < depth)
                ):
                    break
            self._publish(
                self._state, self.enabled, status="Finished" if not self._stack else "Paused"
            )
            if events:
                self._history.append(checkpoint)
            self.last_result = {"events": events, **self.status}
            return self.last_result
        except (Exception, asyncio.CancelledError) as exc:
            self.failed = True
            result = {
                "events": events,
                **self.status,
                "error": str(exc),
                "failing_instruction": instruction,
                "failing_event": event,
            }
            self.last_result = result
            self._record({"kind": "error", **result})
            if isinstance(exc, asyncio.CancelledError):
                raise
            raise ExecutionError(str(exc), result) from exc
        finally:
            self._busy = False

    async def step_into(self):
        return await self._advance("into")

    async def step_over(self):
        return await self._advance("over")

    async def step_out(self):
        return await self._advance("out")

    async def run(self):
        return await self._advance("run")
