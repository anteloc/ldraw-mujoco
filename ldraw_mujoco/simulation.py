"""Hold checks, simulation reports, static views and snapshots using MuJoCo's own APIs."""

from __future__ import annotations

import itertools
import math
import sys
import time
from pathlib import Path

import mujoco
import numpy as np
from PIL import Image


def _warnings(data):
    """MuJoCo's warning counters that fired, by warning name."""
    return {
        mujoco.mjtWarning(i).name: int(w.number) for i, w in enumerate(data.warning) if w.number
    }


def _body_states(model, data):
    return [
        {
            "name": model.body(i).name,
            "position_m": data.xpos[i].tolist(),
            "quaternion_wxyz": data.xquat[i].tolist(),
        }
        for i in range(1, model.nbody)
    ]


def contacts(model, data):
    result = []
    for contact_index, contact in enumerate(data.contact):
        force = np.zeros(6)
        mujoco.mj_contactForce(model, data, contact_index, force)
        result.append(
            {
                "geom1": model.geom(int(contact.geom[0])).name,
                "geom2": model.geom(int(contact.geom[1])).name,
                "position_m": contact.pos.tolist(),
                "distance_m": float(contact.dist),
                "normal_force_n": float(force[0]),
            }
        )
    return result


def simulate(model, *, seconds=5.0, data=None, viewer=False):
    """Simulate with an optional independent browser, closed when this call returns."""
    from .viewer import browser_session

    with browser_session(model, enabled=viewer) as handle:
        return _simulate(model, seconds=seconds, data=data, handle=handle)


def _display(handle, data, status):
    if handle is not None:
        try:
            handle.publish(data.qpos, status=status)
        except Exception as exc:
            print(f"Browser viewer unavailable: {exc}", file=sys.stderr)
            handle.close()
            return None
    return handle


def _simulate(model, *, seconds=5.0, data=None, handle=None):
    """Step a model, returning (MjData, report); failures are reported, not hidden.

    Duration is rounded up to whole timesteps. Samples are retained every 0.1 s;
    maxima, numerical state and warnings are checked on every step.
    """
    if not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("seconds must be finite and positive")
    data = mujoco.MjData(model) if data is None else data
    model.opt.enableflags |= int(mujoco.mjtEnableBit.mjENBL_ENERGY)
    handle = _display(handle, data, "Loading physics")
    mujoco.mj_forward(model, data)
    initial = _body_states(model, data)
    start = float(data.time)
    steps = math.ceil(seconds / model.opt.timestep)
    stride = max(1, round(0.1 / model.opt.timestep))
    samples = []
    max_contacts, max_penetration, completed = 0, 0.0, 0
    max_speed = np.zeros(model.nbody - 1)
    max_tilt = np.zeros(model.nbody - 1)
    previous_positions = data.xpos[1:].copy()
    valid, failures = True, []
    wall_start = time.monotonic()
    frame_stride = max(1, round(0.05 / model.opt.timestep))
    try:
        for step in range(steps):
            before = float(data.time)
            mujoco.mj_step(model, data)
            completed += 1
            if (
                not np.isfinite(data.qpos).all()
                or not np.isfinite(data.qvel).all()
                or not np.isfinite(data.qacc).all()
                or data.time <= before
            ):
                valid = False
                failures.append("Non-finite state or simulation time reset")
                break
            # Positions and contacts come from the start of the step: one step behind
            # qpos, which avoids a second, equally expensive mj_forward per step.
            max_contacts = max(max_contacts, data.ncon)
            if data.ncon:
                max_penetration = max(max_penetration, float(max(0, -data.contact.dist.min())))
            max_speed = np.maximum(
                max_speed,
                np.linalg.norm(data.xpos[1:] - previous_positions, axis=1) / model.opt.timestep,
            )
            previous_positions = data.xpos[1:].copy()
            # Imported bodies start with identity orientation; local +Z is their up axis.
            tilt = np.degrees(np.arccos(np.clip(data.xmat[1:, 8], -1, 1)))
            max_tilt = np.maximum(max_tilt, tilt)
            if step % stride == 0 or step == steps - 1:
                samples.append(
                    {
                        "time_s": float(data.time),
                        "contact_count": data.ncon,
                        "potential_energy_j": float(data.energy[0]),
                        "kinetic_energy_j": float(data.energy[1]),
                        "bodies": _body_states(model, data),
                    }
                )
            if handle is not None and ((step + 1) % frame_stride == 0 or step + 1 == steps):
                handle = _display(handle, data, "Running")
                if handle is not None and handle.connected:
                    target = (step + 1) * model.opt.timestep
                    time.sleep(max(0, target - (time.monotonic() - wall_start)))
    finally:
        _display(handle, data, "Finished" if valid else "Stopped: invalid physics")
    if valid:
        mujoco.mj_forward(model, data)  # mj_step leaves positions one step behind qpos.
    warnings = _warnings(data)
    final = _body_states(model, data)
    for i, body in enumerate(final):
        body["displacement_m"] = (np.array(body["position_m"]) - initial[i]["position_m"]).tolist()
        body["max_speed_m_s"] = float(max_speed[i])
        body["max_tilt_deg"] = float(max_tilt[i])
    return data, {
        "requested_duration_s": seconds,
        "start_time_s": start,
        "final_time_s": float(data.time),
        "steps": completed,
        "numerically_valid": valid and not warnings,
        "failures": failures,
        "warnings": warnings,
        "max_contact_count": max_contacts,
        "max_penetration_m": max_penetration,
        "potential_energy_j": float(data.energy[0]),
        "kinetic_energy_j": float(data.energy[1]),
        "initial_bodies": initial,
        "final_bodies": final,
        "final_contacts": contacts(model, data),
        "samples": samples,
        "interpretation": "Numerical execution and approximate rigid-body behavior; not proof of physical stability or attachment strength.",
    }


# Signs of a box's eight corners, used to follow each geom's bounding box.
_CORNERS = np.array(list(itertools.product((-1, 1), repeat=3)))


def _corners(model, data, geoms):
    """World positions of the local bounding-box corners of ``geoms``: (n, 8, 3)."""
    local = model.geom_aabb[geoms, None, :3] + _CORNERS * model.geom_aabb[geoms, None, 3:]
    rotation = data.geom_xmat[geoms].reshape(-1, 3, 3)
    return data.geom_xpos[geoms, None] + local @ rotation.transpose(0, 2, 1)


def _displacement(model, geoms, before, after):
    """Largest corner displacement per body, indexed by body ID."""
    result = np.zeros(model.nbody)
    np.maximum.at(
        result, model.geom_bodyid[geoms], np.linalg.norm(after - before, axis=2).max(axis=1)
    )
    return result


def hold(model, *, seconds=5.0, tolerance=0.002, settle=0.2, data=None):
    """Check that no body moves more than ``tolerance`` meters for ``seconds``.

    Contacts are soft: a scene first drops its import clearance and sinks into
    its contacts. The first ``settle`` seconds are reported, not judged. Then,
    every 10 ms of simulated time, each body's movement is the largest
    displacement of any corner of its colliding geoms' bounding boxes. The run
    stops at the first body that moved too far. Returns (MjData, report).
    """
    if not (math.isfinite(seconds) and seconds > 0 and math.isfinite(tolerance) and tolerance > 0):
        raise ValueError("seconds and tolerance must be finite and positive")
    if not (math.isfinite(settle) and settle >= 0):
        raise ValueError("settle must be finite and non-negative")
    data = mujoco.MjData(model) if data is None else data
    # Physical shapes: geoms that collide, on bodies that can move.
    geoms = np.flatnonzero(
        (model.geom_bodyid > 0) & ((model.geom_contype | model.geom_conaffinity) > 0)
    )
    timestep = model.opt.timestep
    check = max(1, round(0.01 / timestep))
    wall = time.perf_counter()
    mujoco.mj_forward(model, data)
    initial = _corners(model, data, geoms)
    if settle_steps := math.ceil(settle / timestep):
        mujoco.mj_step(model, data, nstep=settle_steps)
    mujoco.mj_forward(model, data)
    start, held_from = _corners(model, data, geoms), float(data.time)
    settled = _displacement(model, geoms, initial, start)
    moved = np.zeros(model.nbody)
    steps = math.ceil(seconds / timestep)
    for done in range(0, steps, check):
        mujoco.mj_step(model, data, nstep=min(check, steps - done))
        # MuJoCo warns, then resets the state, when a simulation becomes unstable.
        if _warnings(data) or not np.isfinite(data.qpos).all():
            break
        moved = np.maximum(moved, _displacement(model, geoms, start, _corners(model, data, geoms)))
        if moved.max() > tolerance:
            break
    warnings = _warnings(data)
    valid = not warnings and bool(np.isfinite(data.qpos).all())
    if valid:
        mujoco.mj_forward(model, data)  # mj_step leaves positions one step behind qpos.
    movers = np.flatnonzero(moved > tolerance)
    movers = movers[np.argsort(-moved[movers])]
    worst = int(settled.argmax())
    return data, {
        "holds": valid and not len(movers),
        "seconds": seconds,
        "settle_s": settle,
        "tolerance_m": tolerance,
        "held_s": float(data.time) - held_from,
        "wall_s": time.perf_counter() - wall,
        "solver": mujoco.mjtSolver(model.opt.solver).name.removeprefix("mjSOL_").lower(),
        "settle_displacement_m": float(settled[worst]),
        "settle_body": model.body(worst).name if settled[worst] > 0 else None,
        "max_displacement_m": float(moved.max()),
        "moved_bodies": [
            {"name": model.body(i).name, "displacement_m": float(moved[i])} for i in movers
        ],
        "numerically_valid": valid,
        "warnings": warnings,
        "interpretation": "Holds means no body moved more than the tolerance after settling, "
        "under approximate physics: parts stay together only through the imported "
        "attachments (rigid links without clutch limits, joints with uncalibrated friction); "
        "studs alone give no interlock, and contacts are soft. "
        "Falls that end within the settle window are only reported. "
        "Not proof of physical stability.",
    }


def _frame(model, data, selected, azimuth=135, elevation=-25):
    """A free camera framing the bounding spheres of the selected geoms."""
    centers = data.geom_xpos[selected]
    radii = model.geom_rbound[selected, None]
    low, high = (centers - radii).min(axis=0), (centers + radii).max(axis=0)
    camera = mujoco.MjvCamera()
    camera.lookat = (low + high) / 2
    camera.distance = max(float(np.linalg.norm(high - low)) * 1.4, 0.05)
    camera.azimuth, camera.elevation = azimuth, elevation
    return camera


def show(model, data, *, highlight=()):
    """View ``data`` in MuJoCo's viewer without stepping; tint ``highlight`` bodies red.

    Returns when the window closes. On macOS, run under ``mjpython``.
    """
    from mujoco import viewer

    original = model.geom_rgba.copy()
    bodies = [model.body(name).id for name in highlight]
    visuals = model.geom_group == 0
    model.geom_rgba[np.isin(model.geom_bodyid, bodies) & visuals] = (0.9, 0.1, 0.1, 1)
    try:
        with viewer.launch_passive(model, data) as handle:
            # Start with the whole model in view, like snapshot().
            frame = _frame(model, data, (model.geom_bodyid != 0) & visuals)
            with handle.lock():
                handle.cam.lookat[:] = frame.lookat
                handle.cam.distance = frame.distance
                handle.cam.azimuth, handle.cam.elevation = frame.azimuth, frame.elevation
            while handle.is_running():
                time.sleep(0.1)
    finally:
        model.geom_rgba[:] = original


def snapshot(model, data, path, *, body=None, azimuth=135, elevation=-25, width=1000, height=750):
    """Render all bodies or one named assembly; collision geometry stays hidden."""
    path = Path(path)
    mujoco.mj_forward(model, data)
    selected = model.geom_bodyid != 0
    if body is not None:
        selected = model.geom_bodyid == model.body(body).id
    selected &= model.geom_group == 0
    if not selected.any():
        raise ValueError(f"No visual geometry to render for {body or 'scene'}")
    camera = _frame(model, data, selected, azimuth, elevation)
    options = mujoco.MjvOption()
    options.geomgroup[3:] = 0
    original_groups = model.geom_group.copy()
    old_size = (model.vis.global_.offwidth, model.vis.global_.offheight)
    try:
        model.vis.global_.offwidth = max(width, old_size[0])
        model.vis.global_.offheight = max(height, old_size[1])
        if body is not None:
            model.geom_group[(model.geom_bodyid != 0) & ~selected] = 5
        with mujoco.Renderer(model, height=height, width=width) as renderer:
            renderer.update_scene(data, camera=camera, scene_option=options)
            pixels = renderer.render()
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(pixels).save(path)
    finally:
        model.geom_group[:] = original_groups
        model.vis.global_.offwidth, model.vis.global_.offheight = old_size
