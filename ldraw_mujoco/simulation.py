"""Small simulation reports and local snapshots using MuJoCo's own APIs."""

from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import mujoco
import numpy as np
from PIL import Image


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
            mujoco.mj_forward(model, data)
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
    warnings = {
        mujoco.mjtWarning(i).name: int(w.number) for i, w in enumerate(data.warning) if w.number
    }
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
    centers = data.geom_xpos[selected]
    radii = model.geom_rbound[selected, None]
    low, high = (centers - radii).min(axis=0), (centers + radii).max(axis=0)
    camera = mujoco.MjvCamera()
    camera.lookat = (low + high) / 2
    camera.distance = max(float(np.linalg.norm(high - low)) * 1.4, 0.05)
    camera.azimuth, camera.elevation = azimuth, elevation
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
