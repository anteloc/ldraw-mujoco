"""Parts attach where their connectors mate: rigidly, by friction-held hinges, or in loops."""

import mujoco
import numpy as np
import pytest

from ldraw_mujoco import import_ldraw
from ldraw_mujoco.cli import main
from ldraw_mujoco.connections import Link, forest
from ldraw_mujoco.simulation import hold

IDENTITY = "1 0 0 0 1 0 0 0 1"
# 30 degrees about Y with three decimals, like the rounded matrices of real models.
ROUNDED = "0.866 0 0.5 0 1 0 -0.5 0 0.866"
# 90 degrees about X: a vertical pin then lies along LDraw Z.
LYING = "1 0 0 0 0 -1 0 1 0"


def test_studs_attach_rigidly(attached):
    stack = f"1 4 0 0 0 {IDENTITY} plate.dat\n1 1 0 -8 0 {IDENTITY} plate.dat\n"
    result = attached(stack, individual_parts=True)
    lower, upper = result.report["bodies"]
    assert (lower["joint"], upper["parent"], upper["joint"]) == ("free", lower["name"], "rigid")
    assert (result.model.njnt, result.model.nq) == (1, 7)
    assert result.report["links"][0]["parts"] == [["0", "1"]]
    assert result.report["connections"]["unlinked_parts"] == []
    free = attached(stack, individual_parts=True, attach=False)
    assert (free.model.njnt, free.model.nq) == (2, 14)
    assert free.report["links"] == [] and free.report["connections"] is None


@pytest.mark.parametrize("matrix,part", [(ROUNDED, "plate.dat"), (IDENTITY, "square.dat")])
def test_rounded_rotations_and_square_sockets_attach(attached, matrix, part):
    result = attached(
        f"1 4 0 0 0 {IDENTITY} plate.dat\n1 1 0 -8 0 {matrix} {part}\n", individual_parts=True
    )
    assert result.report["bodies"][1]["joint"] == "rigid"


@pytest.mark.parametrize("matrix,axis", [(IDENTITY, [0, 0, 1]), (LYING, [0, 1, 0])])
def test_pin_turns_in_its_hole_against_friction(attached, matrix, axis):
    text = f"1 4 0 0 0 {matrix} beam.dat\n1 1 -20 0 0 {matrix} pin.dat\n"
    model = attached(text, individual_parts=True).model
    assert model.jnt_type[1] == mujoco.mjtJoint.mjJNT_HINGE
    np.testing.assert_allclose(np.abs(model.jnt_axis[1]), axis, atol=1e-9)
    dof = model.jnt_dofadr[1]
    assert model.dof_frictionloss[dof] == pytest.approx(0.01)
    assert model.dof_solimp[dof, 0] == pytest.approx(0.9999)  # Hard friction: no creep.
    free = attached(text, individual_parts=True, joint_friction=0).model
    assert free.dof_frictionloss[free.jnt_dofadr[1]] == 0


@pytest.mark.parametrize("pins,joint", [(1, "hinge"), (2, "rigid")])
def test_pins_on_two_axes_lock_submodels_together(attached, pins, joint):
    placed = "".join(f"1 4 {x} 0 0 {IDENTITY} pin.dat\n" for x in (-20, 20)[:pins])
    text = (
        f"0 FILE main.ldr\n1 16 0 0 0 {IDENTITY} lower.ldr\n1 16 0 -8 0 {IDENTITY} upper.ldr\n"
        f"0 FILE lower.ldr\n1 4 0 0 0 {IDENTITY} beam.dat\n{placed}"
        f"0 FILE upper.ldr\n1 1 0 0 0 {IDENTITY} beam.dat\n"
    )
    lower, upper = attached(text, suffix=".mpd").report["bodies"]
    assert (upper["parent"], upper["joint"]) == (lower["name"], joint)


def test_two_pins_through_two_beams_close_a_loop(attached):
    text = (
        f"1 4 0 0 0 {IDENTITY} beam.dat\n1 1 0 -8 0 {IDENTITY} beam.dat\n"
        f"1 1 -20 0 0 {IDENTITY} pin.dat\n1 1 20 0 0 {IDENTITY} pin.dat\n"
    )
    result = attached(text, individual_parts=True)
    joints = sorted(b["joint"] for b in result.report["bodies"])
    assert joints == ["free", "hinge", "hinge", "hinge"]
    (loop,) = [link for link in result.report["links"] if link["constraint"] == "loop"]
    assert loop["kind"] == "hinge"
    for model in (result.model, mujoco.MjModel.from_xml_string(result.spec.to_xml())):
        assert (model.njnt, model.neq, model.nexclude) == (4, 1, 1)
        assert model.eq_type[0] == mujoco.mjtEq.mjEQ_CONNECT
        data = mujoco.MjData(model)
        mujoco.mj_forward(model, data)
        # The loop constraint holds in the imported pose.
        equality = data.efc_type == mujoco.mjtConstraint.mjCNSTR_EQUALITY
        np.testing.assert_allclose(data.efc_pos[equality], 0, atol=1e-9)
    # Welded into one body by default, the pins join nothing.
    welded = attached(text)
    assert welded.model.njnt == 1 and welded.report["links"] == []


def test_overhang_holds_only_when_attached(attached):
    # One stud holds the upper plate, whose center of mass is beyond the lower
    # plate's edge.
    text = f"1 4 0 0 0 {IDENTITY} long.dat\n1 1 40 -8 0 {IDENTITY} long.dat\n"
    for attach, holds in ((True, True), (False, False)):
        model = attached(text, individual_parts=True, attach=attach, clearance=0).model
        _, report = hold(model, seconds=0.5, settle=0)
        assert report["holds"] is holds and report["numerically_valid"]


def test_cli_attach_options(tmp_path, attached):
    source = tmp_path / "pin.ldr"
    source.write_text(f"1 4 0 0 0 {IDENTITY} beam.dat\n1 1 -20 0 0 {IDENTITY} pin.dat\n")
    output = tmp_path / "pin.xml"
    options = ["--library", str(attached.library), "--shadow", str(attached.shadow)]
    options += ["--individual-parts", "--output", str(output)]
    assert main(["convert", str(source), *options, "--joint-friction", "0.02"]) == 0
    model = mujoco.MjModel.from_xml_path(str(output))
    assert model.dof_frictionloss[model.jnt_dofadr[1]] == pytest.approx(0.02)
    assert main(["convert", str(source), *options, "--no-attach"]) == 0
    model = mujoco.MjModel.from_xml_path(str(output))
    assert (model.njnt, model.nq) == (2, 14)


def link(kind):
    return Link(kind, np.zeros(3), np.array([0.0, -1.0, 0.0]), ())


def kinds(tree):
    return [(body, parent, link and link.kind) for body, parent, link in tree]


def test_forest_takes_rigid_links_first():
    # The hinge between 0 and 1 is locked: both are rigidly joined through 2.
    tree, loops = forest(3, {(0, 1): link("hinge"), (0, 2): link("rigid"), (1, 2): link("rigid")})
    assert kinds(tree) == [(0, None, None), (2, 0, "rigid"), (1, 2, "rigid")]
    assert loops == []


def test_forest_closes_joint_loops_and_roots_trees_at_their_first_body():
    hinges = {(0, 1): link("hinge"), (0, 2): link("hinge"), (1, 2): link("hinge")}
    tree, loops = forest(5, {**hinges, (3, 4): link("ball")})
    assert kinds(tree) == [
        (0, None, None),
        (1, 0, "hinge"),
        (2, 0, "hinge"),
        (3, None, None),
        (4, 3, "ball"),
    ]
    assert [(a, b) for a, b, _ in loops] == [(1, 2)]


@pytest.mark.integration
def test_sample_parts_attach_by_their_connections(sample):
    result = import_ldraw(sample.report["source"], individual_parts=True)
    bodies = {b["instance_id"]: b for b in result.report["bodies"]}

    def joined(child, parent, joint):
        return (bodies[child]["parent"], bodies[child]["joint"]) == (bodies[parent]["name"], joint)

    # Tyres press onto rims, and rims turn on the wheel holders' pins.
    holders = {"0/19": "0/18", "0/46": "0/45", "0/47": "0/44", "0/48": "0/44", "0/49": "0/45"}
    for wheel, holder in holders.items():
        assert joined(f"{wheel}/1", f"{wheel}/0", "rigid")
        assert joined(f"{wheel}/0", holder, "hinge")
    # Minifigure legs swing on the hips.
    assert joined("1/8", "1/3", "hinge") and joined("1/9", "1/3", "hinge")
    _, report = hold(result.model, seconds=1)
    assert report["numerically_valid"]
