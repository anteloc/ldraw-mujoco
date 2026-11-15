import mujoco
import numpy as np
import pytest

from ldraw_mujoco.simulation import simulate

PLACEMENT = "1 4 0 0 0 1 0 0 0 1 0 0 0 1 cube.dat\n"


def test_gravity_matches_free_fall(build):
    model = build(PLACEMENT, clearance=0.1).spec.compile()
    data = mujoco.MjData(model)
    start_z = data.qpos[2]
    data, report = simulate(model, seconds=0.05, data=data)
    assert start_z - data.qpos[2] == pytest.approx(0.5 * 9.81 * 0.05**2, abs=0.0003)
    assert report["max_contact_count"] == 0
    assert report["numerically_valid"]


def test_higher_friction_reduces_sliding(build):
    distances = []
    for friction in (0.05, 0.9):
        model = build(PLACEMENT, friction=friction, clearance=0).spec.compile()
        data = mujoco.MjData(model)
        data.qvel[0] = 0.2
        data, report = simulate(model, seconds=0.5, data=data)
        assert report["max_contact_count"] > 0
        assert report["numerically_valid"]
        distances.append(abs(data.qpos[0]))
    assert distances[0] > 3 * distances[1]


def test_unstable_tall_body_tips_instead_of_being_frozen():
    angle = np.radians(30)
    spec = mujoco.MjSpec()
    spec.option.timestep = 0.001
    spec.worldbody.add_geom(type=mujoco.mjtGeom.mjGEOM_PLANE, size=[1, 1, 0.01])
    body = spec.worldbody.add_body(
        name="tall",
        pos=[0, 0, 0.04 * np.cos(angle) + 0.005 * np.sin(angle) + 0.001],
        quat=[np.cos(angle / 2), 0, np.sin(angle / 2), 0],
    )
    body.add_freejoint()
    body.add_geom(type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.005, 0.005, 0.04], mass=0.01)
    model = spec.compile()
    data, report = simulate(model, seconds=1)
    assert report["numerically_valid"]
    assert report["final_bodies"][0]["max_tilt_deg"] > 80
    assert data.xpos[1, 2] < 0.01


@pytest.mark.integration
def test_sample_five_seconds(sample):
    model = sample.spec.compile()
    data, report = simulate(model, seconds=5)
    assert data.time == pytest.approx(5)
    assert report["numerically_valid"]
    assert report["warnings"] == {}
    assert report["max_contact_count"] > 0
    assert report["final_contacts"]
    assert np.isfinite(data.qpos).all()
    # Preserve the observed outcome, without asserting that every model stays upright.
    assert all("max_tilt_deg" in body for body in report["final_bodies"])


@pytest.mark.parametrize("seconds", [0, -1, float("nan"), float("inf")])
def test_invalid_duration(build, seconds):
    with pytest.raises(ValueError, match="positive"):
        simulate(build(PLACEMENT).spec.compile(), seconds=seconds)


def test_browser_playback_preserves_simulation_and_survives_disconnect(build):
    from ldraw_mujoco.simulation import _simulate

    class Viewer:
        connected = True
        frames = []

        def publish(self, qpos, **kwargs):
            self.frames.append((np.array(qpos).copy(), kwargs["status"]))
            if len(self.frames) > 2:
                self.connected = False

    m = build(PLACEMENT, timestep=0.007).spec.compile()
    a, expected = simulate(m, seconds=0.113)
    viewer = Viewer()
    b, report = _simulate(m, seconds=0.113, handle=viewer)
    np.testing.assert_array_equal(a.qpos, b.qpos)
    np.testing.assert_array_equal(a.qvel, b.qvel)
    assert report == expected
    assert viewer.frames[0][1] == "Loading physics"
    assert viewer.frames[-1][1] == "Finished"


def test_cli_saves_report_before_final_inspection_and_closes_service(build, tmp_path, monkeypatch):
    import builtins
    from contextlib import contextmanager
    from types import SimpleNamespace

    import ldraw_mujoco.cli as cli
    import ldraw_mujoco.viewer as browser

    path = tmp_path / "scene.xml"
    path.write_text(build(PLACEMENT).spec.to_xml())
    report = path.with_suffix(".simulation.json")
    closed = []

    class Viewer:
        connected = False

        def publish(self, *_args, **_kwargs):
            pass

    @contextmanager
    def session(model, *, enabled):
        assert enabled
        try:
            yield Viewer()
        finally:
            closed.append(True)

    def finish(_):
        assert report.exists()
        raise KeyboardInterrupt

    monkeypatch.setattr(browser, "browser_session", session)
    monkeypatch.setattr(cli.sys, "stdin", SimpleNamespace(isatty=lambda: True))
    monkeypatch.setattr(builtins, "input", finish)
    assert cli.main(["simulate", str(path), "--seconds", "0.01", "--viewer"]) == 0
    assert closed == [True]
