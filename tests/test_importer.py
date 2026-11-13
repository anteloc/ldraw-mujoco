import json

import mujoco
import numpy as np
import pytest

from ldraw_mujoco import import_ldraw
from ldraw_mujoco.cli import main
from ldraw_mujoco.geometry import BASIS, LDU_TO_METERS, Document, Surfaces, triangle_mesh
from ldraw_mujoco.library import load_library

IDENTITY = "1 0 0 0 1 0 0 0 1"


def collision_points(model):
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    points = []
    for gid in np.flatnonzero(model.geom_group == 3):
        mesh = model.geom_dataid[gid]
        start = model.mesh_vertadr[mesh]
        vertices = model.mesh_vert[start : start + model.mesh_vertnum[mesh]]
        points.extend(vertices @ data.geom_xmat[gid].reshape(3, 3).T + data.geom_xpos[gid])
    return np.array(points)


def test_scale_and_handedness():
    np.testing.assert_allclose(BASIS @ [0, -20, 0] * LDU_TO_METERS, [0, 0, 0.008])
    assert np.linalg.det(BASIS) == 1
    np.testing.assert_allclose(np.cross(BASIS[:, 0], BASIS[:, 1]), BASIS[:, 2])


def test_nested_repeated_placements_and_inherited_colours(build):
    result = build(
        f"""0 FILE root.ldr
1 4 0 0 0 {IDENTITY} nested.ldr
1 1 60 0 0 0 0 -1 0 1 0 1 0 0 nested.ldr
0 FILE nested.ldr
1 16 20 0 0 {IDENTITY} cube.dat
1 16 0 -8 0 {IDENTITY} cube.dat
""",
        suffix=".mpd",
        grouping="top-level",
    )
    assert result.report["occurrence_count"] == 4
    assert [b["occurrence_count"] for b in result.report["bodies"]] == [2, 2]
    assert [o["colour"] for o in result.report["occurrences"]] == [4, 4, 1, 1]
    assert result.report["occurrences"][2]["position_ldu"] == [60, 0, 20]
    model = result.spec.compile()
    assert (model.nq, model.nv) == (14, 12)
    points = collision_points(model)
    np.testing.assert_allclose(points.min(axis=0), [-0.004, -0.004, 0.001], atol=1e-8)
    np.testing.assert_allclose(points.max(axis=0), [0.028, 0.012, 0.0074], atol=1e-8)


def test_standalone_dat_embedded_dat_and_drawing_lines(build, small_library):
    cube = (small_library / "parts/cube.dat").read_text()
    cube += "2 24 10000 0 0 0 10000 0\n5 24 0 0 0 1 1 1 90000 90000 90000 -90000 0 0\n"
    standalone = build(cube, suffix=".dat")
    assert standalone.report["occurrence_count"] == 1
    assert standalone.report["source_bounds_m"][1][0] == pytest.approx(0.004)
    embedded = build(
        f"0 FILE main.ldr\n1 4 0 0 0 {IDENTITY} custom.dat\n0 FILE custom.dat\n{cube}",
        suffix=".mpd",
    )
    assert embedded.report["occurrence_count"] == 1
    np.testing.assert_allclose(
        embedded.report["source_bounds_m"], standalone.report["source_bounds_m"]
    )


def test_affine_and_mirrored_instances(build):
    result = build("1 4 0 0 0 -2 0.1 0 0 1 0 0 0 1 cube.dat\n")
    assert result.report["warnings"][0]["code"] == "affine_placement"
    expected_width = (40 + 0.8) * LDU_TO_METERS
    bounds = np.array(result.report["source_bounds_m"])
    assert bounds[1, 0] - bounds[0, 0] == pytest.approx(expected_width)
    assert result.spec.compile().body_mass[1] > 0


def test_planar_colour_patch_and_transparency(build, small_library):
    cube = (small_library / "parts/cube.dat").read_text().replace("3 16", "3 47")
    cube += "3 15 -5 0 -5 5 0 -5 0 0 5\n"
    result = build(cube, suffix=".dat")
    model = result.spec.compile()
    visuals = (model.geom_group == 0) & (model.geom_bodyid != 0)
    rgba = model.geom_rgba[visuals]
    assert len(rgba) == 2
    assert np.min(rgba[:, 3]) == pytest.approx(128 / 255)
    assert np.max(rgba[:, 3]) == 1
    assert np.all(model.geom_contype[visuals] == 0)
    # Patches do not add mass to the solid hull.
    assert model.body_mass[1] == pytest.approx(20 * 8 * 20 * LDU_TO_METERS**3 * 1050)


def test_bfc_winding_and_mirror(tmp_path, small_library):
    path = tmp_path / "part.dat"
    path.write_text("0 BFC INVERTNEXT\n1 16 0 0 0 -1 0 0 0 1 0 0 0 1 cube.dat\n")
    parts, _, _ = load_library(small_library, [], tmp_path / "cache")
    surfaces = Surfaces(Document(path, parts))
    cube = triangle_mesh(surfaces.get("cube.dat").triangles)
    inverted = triangle_mesh(surfaces.get("part.dat").triangles)
    assert cube.volume > 0
    assert inverted.volume == pytest.approx(-cube.volume)


def test_external_ldr_reference(tmp_path, small_library):
    (tmp_path / "child.ldr").write_text(f"1 16 10 0 0 {IDENTITY} cube.dat\n")
    path = tmp_path / "main.ldr"
    path.write_text(f"1 1 20 0 0 {IDENTITY} child.ldr\n")
    result = import_ldraw(path, library=small_library, shadows=[], cache=tmp_path / "cache")
    assert result.report["occurrences"][0]["position_ldu"] == [30, 0, 0]
    assert result.report["occurrences"][0]["colour"] == 1


@pytest.mark.parametrize(
    "text,match",
    [
        (f"1 4 0 0 0 {IDENTITY} missing.dat\n", "missing.dat"),
        (f"1 4 0 0 0 {IDENTITY} missing.ldr\n", "Missing model"),
        ("1 4 nan 0 0 1 0 0 0 1 0 0 0 1 cube.dat\n", "Non-finite"),
        ("1 4 0 0 0 0 0 0 0 1 0 0 0 1 cube.dat\n", "Singular"),
        ("0 FILE root.ldr\n1 4 0 0 0 1 0 0 0 1 0 0 0 1 root.ldr\n", "[Cc]ycl"),
        ("0 !TEXMAP START PLANAR 0 0 0\n", "Unsupported"),
    ],
)
def test_bad_input_is_actionable(build, text, match):
    with pytest.raises(Exception, match=match):
        build(text)


def test_geometry_cycle(build):
    with pytest.raises(ValueError, match="Geometry reference cycle"):
        build(
            f"0 FILE root.ldr\n1 4 0 0 0 {IDENTITY} self.dat\n"
            f"0 FILE self.dat\n1 16 0 0 0 {IDENTITY} self.dat\n",
            suffix=".mpd",
        )


def test_cli_export_reloads_without_library(tmp_path, small_library):
    source = tmp_path / "input.ldr"
    source.write_text(f"1 4 0 0 0 {IDENTITY} cube.dat\n")
    output = tmp_path / "portable.xml"
    assert (
        main(
            [
                "convert",
                str(source),
                "--library",
                str(small_library),
                "--no-shadow",
                "--output",
                str(output),
            ]
        )
        == 0
    )
    small_library.rename(tmp_path / "hidden-library")
    assert mujoco.MjModel.from_xml_path(str(output)).nq == 7
    assert json.loads(output.with_suffix(".import.json").read_text())["occurrence_count"] == 1


@pytest.mark.integration
def test_sample_counts_and_xml_round_trip(sample):
    report = sample.report
    assert (report["occurrence_count"], report["unique_parts"]) == (65, 36)
    assert [b["occurrence_count"] for b in report["bodies"]] == [55, 10]
    first = sample.spec.compile()
    second = mujoco.MjModel.from_xml_string(sample.spec.to_xml())
    assert (first.nbody, first.nq, first.nv) == (3, 14, 12)
    assert np.all(first.body_mass[1:] > 0)
    assert np.all(first.body_inertia[1:] > 0)
    for name in ("body_pos", "geom_pos", "geom_size"):
        np.testing.assert_allclose(
            getattr(first, name), getattr(second, name), atol=1e-7, rtol=1e-6
        )
    np.testing.assert_allclose(first.body_mass, second.body_mass, atol=1e-10, rtol=1e-5)
    np.testing.assert_allclose(first.body_inertia, second.body_inertia, atol=1e-13, rtol=1e-5)
    # MuJoCo serializes inline mesh vertices with limited decimal precision.
    # Compare physical geometry, not the compiler's principal-axis mesh frames.
    np.testing.assert_allclose(collision_points(first), collision_points(second), atol=1e-7)
    a, b = mujoco.MjData(first), mujoco.MjData(second)
    for _ in range(100):
        mujoco.mj_step(first, a)
        mujoco.mj_step(second, b)
    for body in range(2):
        np.testing.assert_allclose(
            a.qpos[7 * body : 7 * body + 3], b.qpos[7 * body : 7 * body + 3], atol=1e-6
        )
        np.testing.assert_allclose(
            a.qpos[7 * body + 3 : 7 * body + 7], b.qpos[7 * body + 3 : 7 * body + 7], atol=1e-5
        )
        np.testing.assert_allclose(
            a.qvel[6 * body : 6 * body + 3], b.qvel[6 * body : 6 * body + 3], atol=1e-4
        )
        np.testing.assert_allclose(
            a.qvel[6 * body + 3 : 6 * body + 6], b.qvel[6 * body + 3 : 6 * body + 6], atol=5e-3
        )
