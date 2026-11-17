import hashlib
import json

import mujoco
import numpy as np
import pytest

from ldraw_mujoco import import_ldraw

IDENTITY = "1 0 0 0 1 0 0 0 1"


@pytest.fixture
def connected(tmp_path, small_library):
    source = tmp_path / "input.ldr"
    source.write_text("\n".join(f"1 4 {i * 30} 0 0 {IDENTITY} cube.dat" for i in range(3)))
    config = tmp_path / "connections.json"

    def build(overrides, **kwargs):
        config.write_text(json.dumps({
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "infer": False, "overrides": overrides,
        }))
        return import_ldraw(source, library=small_library, shadows=[], cache=tmp_path / "cache",
                            individual_parts=True, connections=config, **kwargs)

    return build


def fixed(a="0", b="1", **kwargs):
    return dict(first=a, second=b, kind="fixed", reason="Synthetic fixed fit", **kwargs)


def hinge(a="0", b="1"):
    return dict(first=a, second=b, kind="hinge", reason="Synthetic revolute fit",
                anchor_m=[0.006, 0, 0], axis=[0, 2, 0])


def test_weld_forest_and_contacts_roundtrip(connected):
    result = connected([fixed(exclude_contact=True), fixed("1", "2"), fixed("0", "2")])
    model = mujoco.MjModel.from_xml_string(result.spec.to_xml())
    assert model.neq == 2
    assert model.nexclude == 1
    assert model.nv == 18
    assert len(result.report["attachments"]["components"]) == 1
    np.testing.assert_allclose(model.eq_data[:, 10], 0.008)
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    assert np.max(np.abs(data.efc_pos[:12])) < 1e-10
    assert model.opt.cone == mujoco.mjtCone.mjCONE_ELLIPTIC


def test_hinge_preserves_world_poses_and_can_turn(connected):
    result = connected([hinge(), fixed("1", "2")])
    model = mujoco.MjModel.from_xml_string(result.spec.to_xml())
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    occurrences = result.report["occurrences"]
    parent, child = (model.body(o["body"]).id for o in occurrences[:2])
    assert model.body_parentid[child] == parent
    np.testing.assert_allclose(data.xpos[child] - data.xpos[parent], [0.012, 0, 0])
    j = model.joint("hinge_1")
    data.qpos[j.qposadr[0]] = np.pi / 2
    mujoco.mj_forward(model, data)
    np.testing.assert_allclose(data.xpos[child] - data.xpos[parent], [0.006, 0, -0.006], atol=1e-9)
    assert model.opt.disableflags & mujoco.mjtDisableBit.mjDSBL_FILTERPARENT


@pytest.mark.parametrize("overrides,match", [
    ([fixed(), fixed()], "Duplicate"),
    ([fixed("0", "root")], "physical part"),
    ([fixed("0", "0")], "self"),
    ([{**hinge(), "exclude_contact": True}], "Only a fixed"),
    ([{**hinge(), "axis": [0, 0, 0]}], "zero axis"),
    ([hinge(), hinge("2", "1")], "Conflicting"),
    ([hinge(), fixed("0", "2"), fixed("1", "2")], "closed articulation"),
    ([{**fixed(), "reason": ""}], "requires"),
])
def test_invalid_connections(connected, overrides, match):
    with pytest.raises(ValueError, match=match):
        connected(overrides)


def test_source_hash_and_required_parts_mode(tmp_path, small_library):
    source = tmp_path / "input.ldr"
    source.write_text(f"1 4 0 0 0 {IDENTITY} cube.dat")
    config = tmp_path / "connections.json"
    config.write_text('{"source_sha256": "stale"}')
    with pytest.raises(ValueError, match="individual_parts"):
        import_ldraw(source, connections=config)
    with pytest.raises(ValueError, match="source_sha256"):
        import_ldraw(source, library=small_library, shadows=[], cache=tmp_path / "cache",
                     individual_parts=True, connections=config)


def test_decomposed_convex_part_and_cache(build, tmp_path):
    result = build(f"1 4 0 0 0 {IDENTITY} cube.dat", collision="decomposed")
    occurrence = result.report["occurrences"][0]
    assert occurrence["collision_geoms"]
    assert "collision_geom" not in occurrence
    assert len(list((tmp_path / "cache/collision").glob("*.npz"))) == 1
    model = mujoco.MjModel.from_xml_string(result.spec.to_xml())
    assert model.body_mass[1] == pytest.approx(20 * 8 * 20 * 0.0004**3 * 1050, rel=1e-4)
    second = build(f"1 4 0 0 0 {IDENTITY} cube.dat", collision="decomposed")
    assert result.report["collision_decompositions"] == second.report["collision_decompositions"]
