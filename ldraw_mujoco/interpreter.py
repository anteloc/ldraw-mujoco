"""Execute parsed type-1 placements with debugger-style submodel calls."""

from __future__ import annotations

import asyncio
import hashlib
import json
import math
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

import mujoco
import numpy as np

from .importer import import_ldraw
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
        model = mujoco.MjModel.from_xml_string(self.xml)
        self.timestep = float(model.opt.timestep)
        self.steps = math.ceil(seconds_per_part / self.timestep)
        self.parts, self.activate, self.inactive = {}, {}, []
        self.geom_ids = {"ground": None}
        for occurrence in self.report["occurrences"]:
            ident, body = occurrence["id"], model.body(occurrence["body"])
            joint = int(body.jntadr[0])
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
        self.client = None
        self.enabled = []
        self._stack = []
        self.failed = False
        self.last_result = None
        self._busy = False
        self.output_dir = Path(output_dir) if output_dir is not None else None
        self.preparation = {
            "xml_sha256": hashlib.sha256(self.xml.encode()).hexdigest(),
            "seconds_per_part": seconds_per_part,
            "steps_per_part": self.steps,
            "timestep_s": self.timestep,
            "reset_policy": "CAD poses and zero velocity per placement",
            "parts": self.parts,
            "initial_modifications": self.inactive,
            "activation_modifications": self.activate,
            "interpretation": "Approximate rigid-body observations; caller decides placement success. "
            "Final-state checks do not establish numerical validity throughout a trial or attachment strength.",
        }

    @classmethod
    @asynccontextmanager
    async def open(cls, path, *, seconds_per_part=0.1, output_dir=None, **import_options):
        """Convert once and own a stdio server until the context exits.

        Import options are those of ``import_ldraw``, except selection/grouping.
        ``output_dir`` saves the exact XML, reports and a flushed JSONL event log.
        """
        if {"sections", "individual_parts"} & import_options.keys():
            raise ValueError("The interpreter always executes the full input as individual parts")
        program = cls(
            import_ldraw(path, individual_parts=True, **import_options),
            seconds_per_part=seconds_per_part,
            output_dir=output_dir,
        )
        log_path = program.output_dir / "server.log" if program.output_dir else None
        async with MujocoClient.connect(log_path=log_path) as client:
            await program._load(client)
            try:
                yield program
            finally:
                program.client = None

    async def _call(self, tool, **arguments):
        if self.client is None:
            raise RuntimeError("Interpreter is closed; use Interpreter.open()")
        return await self.client.call(tool, sim_name=self.slot, **arguments)

    async def _load(self, client):
        self.client = client
        summary = await client.call("sim_load", name=self.slot, xml_string=self.xml)
        if any(summary[k] != v for k, v in self.model_dimensions.items()):
            raise MCPError("Loaded model dimensions differ from the prepared XML")
        if not set(p["body"] for p in self.parts.values()) <= set(summary["bodies"]):
            raise MCPError("Loaded model is missing expected part bodies")
        if self.output_dir is not None:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            (self.output_dir / "scene.xml").write_text(self.xml)
            for name, payload in (
                ("scene.import.json", self.report),
                ("execution.json", self.preparation),
            ):
                (self.output_dir / name).write_text(
                    json.dumps(payload, indent=2, allow_nan=False) + "\n"
                )
            (self.output_dir / "events.jsonl").write_text("")
        self._record(
            {"kind": "load", "xml_sha256": self.preparation["xml_sha256"], "server": summary}
        )
        await self.reset()

    def _record(self, event):
        if self.output_dir is not None:
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
            self._unwind()
            self.failed = False
            result = {"events": [], **self.status}
            self.last_result = result
            self._record({"kind": "reset", **result})
            return result
        finally:
            self._busy = False

    async def viewer(self):
        """Ask the server to open its optional live viewer."""
        return await self._call("viewer_open")

    async def _place(self, ident):
        await self._call("sim_reset")
        await self._call("modify_model", modifications=self.activate[ident])
        remaining = self.steps
        while remaining:
            count = min(remaining, 100_000)
            await self._call("sim_step", n_steps=count)
            remaining -= count
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
        for active in [*self.enabled, ident]:
            part = self.parts[active]
            qa, va = part["qpos_address"], part["qvel_address"]
            bodies.append(
                {
                    "id": active,
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
            contact["part1_id"] = self.geom_ids[contact["geom1"]]
            contact["part2_id"] = self.geom_ids[contact["geom2"]]
        physics = {
            "requested_duration_s": self.seconds_per_part,
            "steps": self.steps,
            "actual_duration_s": state["time"],
            "state_finite": bool(np.isfinite(qpos).all() and np.isfinite(qvel).all()),
            "duration_matches": math.isclose(
                state["time"], self.steps * self.timestep, rel_tol=1e-9, abs_tol=1e-12
            ),
            "bodies": bodies,
            "contacts": contacts["contacts"],
            "contact_count": contacts["n_contacts"],
        }
        return _json_safe(physics)

    async def _advance(self, mode):
        if self._busy:
            raise RuntimeError("Debugger operations must be sequential")
        if self.failed:
            raise ExecutionError(
                "Execution halted; call reset() or reopen", {"events": [], **self.status}
            )
        self._busy = True
        events = []
        depth = len(self._stack)
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
