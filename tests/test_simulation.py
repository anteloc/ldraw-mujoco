import json

import mujoco
import numpy as np
import pytest

from ldraw_mujoco.cli import main
from ldraw_mujoco.simulation import hold, simulate

PLACEMENT = "1 4 0 0 0 1 0 0 0 1 0 0 0 1 cube.dat\n"


def tilted_tall_box():
    """An 8 cm tall box standing on one edge, tilted 30 degrees, so it must tip over."""
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
    return spec.compile()


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
    data, report = simulate(tilted_tall_box(), seconds=1)
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


def test_resting_part_holds(build):
    data, report = hold(build(PLACEMENT).model, seconds=0.5)
    assert report["holds"] and report["numerically_valid"]
    assert report["held_s"] == pytest.approx(0.5)
    assert report["moved_bodies"] == [] and report["max_displacement_m"] < 0.0005
    # Settling covers the 1 mm clearance drop and the contact sink.
    assert report["settle_displacement_m"] < 0.002


def test_falling_part_crumbles_fast(build):
    model = build(PLACEMENT, clearance=0.1).model
    data, report = hold(model, seconds=5, settle=0)
    assert not report["holds"] and report["numerically_valid"]
    assert report["held_s"] < 0.05  # Stops at the first check beyond 2 mm, not after 5 s.
    assert [body["name"] for body in report["moved_bodies"]] == [model.body(1).name]
    # With the default settle window, the cube lands before judging starts; the
    # fall stays visible in the report.
    _, landed = hold(build(PLACEMENT, clearance=0.1).model, seconds=0.1)
    assert landed["settle_displacement_m"] > 0.09  # Corners also turn on impact.


def test_tipping_body_crumbles():
    data, report = hold(tilted_tall_box(), seconds=1)
    assert not report["holds"]
    assert report["moved_bodies"][0]["name"] == "tall"


@pytest.mark.parametrize(
    "options",
    [
        {"seconds": 0},
        {"tolerance": -0.001},
        {"tolerance": float("nan")},
        {"settle": -1},
        {"settle": float("inf")},
    ],
)
def test_hold_rejects_invalid_arguments(build, options):
    with pytest.raises(ValueError, match="finite"):
        hold(build(PLACEMENT).model, **options)


def test_cli_hold_writes_report_and_exit_code(tmp_path, small_library):
    source = tmp_path / "input.ldr"
    source.write_text(PLACEMENT)
    library = ["--library", str(small_library), "--no-shadow"]
    resting, falling = tmp_path / "resting.xml", tmp_path / "falling.xml"
    assert main(["convert", str(source), *library, "--output", str(resting)]) == 0
    assert (
        main(["convert", str(source), *library, "--clearance", "0.1", "--output", str(falling)])
        == 0
    )
    assert main(["hold", str(resting), "--seconds", "0.3"]) == 0
    assert json.loads(resting.with_suffix(".hold.json").read_text())["holds"]
    assert main(["hold", str(falling), "--settle", "0"]) == 1


@pytest.mark.integration
def test_sample_hold_reports_a_verdict(sample):
    data, report = hold(sample.spec.compile(), seconds=1)
    # Preserve the observed outcome, without asserting that the sample holds.
    assert isinstance(report["holds"], bool)
    assert report["numerically_valid"]
    assert np.isfinite(report["max_displacement_m"]) and report["held_s"] > 0
