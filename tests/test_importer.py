import json
from itertools import product

import mujoco
import numpy as np
import pytest
from ldraw import ConnectionFeature

from ldraw_mujoco import import_ldraw
from ldraw_mujoco.cli import main
from ldraw_mujoco.geometry import BASIS, LDU_TO_METERS, Document, Surfaces
from ldraw_mujoco.importer import _compile
from ldraw_mujoco.library import load_library
from ldraw_mujoco.meshes import triangle_mesh

IDENTITY = "1 0 0 0 1 0 0 0 1"


def collision_points(model, group=3):
    """World vertices of the meshes in a geom group: 3 for hulls, 0 for visuals."""
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    points = []
    for gid in np.flatnonzero((model.geom_group == group) & (model.geom_bodyid != 0)):
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


def test_studs_are_visual_only(build):
    result = build(f"1 4 0 0 0 {IDENTITY} brick.dat\n", clearance=0)
    model = result.model
    # The hull stops at the cube top; the 4 LDU stud stays in visuals and bounds.
    assert collision_points(model)[:, 2].max() == pytest.approx(8 * LDU_TO_METERS)
    assert collision_points(model, group=0)[:, 2].max() == pytest.approx(12 * LDU_TO_METERS)
    bounds = np.array(result.report["source_bounds_m"])
    assert bounds[1, 2] - bounds[0, 2] == pytest.approx(12 * LDU_TO_METERS)
    assert model.body_mass[1] == pytest.approx(20 * 8 * 20 * LDU_TO_METERS**3 * 1050)
    # A part made only of a stud keeps it as its hull.
    knob = build(f"1 4 0 0 0 {IDENTITY} knob.dat\n").model
    assert knob.body_mass[1] == pytest.approx(12 * 4 * 12 * LDU_TO_METERS**3 * 1050)


def test_solver_and_contact_options_round_trip(build):
    placement = f"1 4 0 0 0 {IDENTITY} cube.dat\n"
    assert build(placement).model.opt.solver == mujoco.mjtSolver.mjSOL_NEWTON
    result = build(placement, solver="cg")
    assert result.report["options"]["solver"] == "cg"
    assert result.report["options"]["contact_margin_m"] == 0.0002
    for model in (result.model, mujoco.MjModel.from_xml_string(result.spec.to_xml())):
        assert model.opt.solver == mujoco.mjtSolver.mjSOL_CG
        assert model.opt.enableflags & int(mujoco.mjtEnableBit.mjENBL_MULTICCD)
        np.testing.assert_allclose(model.geom_margin[model.geom_group == 3], 0.0002)
    with pytest.raises(ValueError, match="solver"):
        build(placement, solver="fast")


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
    assert [b["occurrence_count"] for b in report["bodies"]] == [45, 2, 2, 2, 2, 2, 10]
    # The car carries its five wheel assemblies on pins; the minifigure stands free.
    car, *wheels, minifigure = report["bodies"]
    assert car["joint"] == minifigure["joint"] == "free"
    assert all((w["parent"], w["joint"]) == (car["name"], "hinge") for w in wheels)
    first = sample.spec.compile()
    second = mujoco.MjModel.from_xml_string(sample.spec.to_xml())
    assert (first.nbody, first.nq, first.nv) == (8, 19, 17)
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
    # Compare free-flight dynamics: rounded XML vertices can perturb the contact
    # solution for the sample's initially overlapping, now independent hulls.
    # This affects only this test, never the exported scene's collision settings.
    for model in (first, second):
        model.opt.disableflags |= int(mujoco.mjtDisableBit.mjDSBL_CONTACT)
    a, b = mujoco.MjData(first), mujoco.MjData(second)
    a.xfrc_applied[1:, :3] = b.xfrc_applied[1:, :3] = [0.001, -0.001, 0]
    a.xfrc_applied[1:, 3:] = b.xfrc_applied[1:, 3:] = [1e-8, -1e-8, 1e-8]
    for _ in range(100):
        mujoco.mj_step(first, a)
        mujoco.mj_step(second, b)
    # Compare world poses, which do not depend on how joints split qpos.
    np.testing.assert_allclose(a.xpos, b.xpos, atol=1e-6)
    np.testing.assert_allclose(a.xquat, b.xquat, atol=1e-5)


def test_shared_meshes_keep_placement_colour_and_independent_motion(build, small_library):
    part = small_library / "parts/cube.dat"
    part.write_text(part.read_text() + "3 15 -5 0 -5 5 0 -5 0 0 5\n")
    result = build(
        f"1 4 0 0 0 {IDENTITY} cube.dat\n1 1 60 0 0 0 -1 0 1 0 0 0 0 1 cube.dat\n",
        individual_parts=True,
        clearance=0.1,
    )
    model = result.model
    a, b = result.report["occurrences"]
    assert (model.nbody, model.njnt, model.nmesh) == (3, 2, 3)
    assert model.geom(a["collision_geom"]).dataid == model.geom(b["collision_geom"]).dataid
    for left, right in zip(a["visual_geoms"], b["visual_geoms"], strict=True):
        assert model.geom(left).dataid == model.geom(right).dataid
    colours = [[model.geom(g).rgba for g in o["visual_geoms"]] for o in (a, b)]
    np.testing.assert_allclose(colours[0], np.array([[201, 26, 9, 255], [255] * 4]) / 255)
    np.testing.assert_allclose(colours[1], np.array([[0, 85, 191, 255], [255] * 4]) / 255)

    corners = np.array(list(product([-10, 10], [0, 8], [-10, 10])))
    expected = []
    for occurrence in (a, b):
        vertices = corners @ np.array(occurrence["matrix_ldraw"]).T + occurrence["position_ldu"]
        expected.extend(vertices @ BASIS.T * LDU_TO_METERS + result.report["scene_offset_m"])
    assert set(map(tuple, collision_points(model).round(8))) == set(
        map(tuple, np.round(expected, 8))
    )

    data = mujoco.MjData(model)
    data.xfrc_applied[model.body(a["body"]).id, 0] = 0.001
    mujoco.mj_step(model, data)
    assert data.qvel[0] > 0 and data.qvel[6] == pytest.approx(0)
    result.spec.option.timestep = 0.01
    assert result.spec.compile().opt.timestep == 0.01
    assert model.opt.timestep == 0.001


def test_affine_asset_reuse_and_bfc_winding(build):
    # A reflected shear followed by two translated copies, one inverted.
    matrix = "-1 0.25 0 0 1 0 0 0 1"
    result = build(
        f"1 4 0 0 0 {matrix} cube.dat\n1 4 60 0 0 {matrix} cube.dat\n"
        f"0 BFC INVERTNEXT\n1 4 120 0 0 {matrix} cube.dat\n"
        f"1 4 180 0 0 {IDENTITY} cube.dat\n"
    )
    model = result.model
    a, b, inverted, rigid = result.report["occurrences"]

    def mesh_id(occ, visual):
        name = occ["visual_geoms"][0] if visual else occ["collision_geom"]
        return int(model.geom(name).dataid[0])

    assert model.nmesh == 5
    assert mesh_id(a, False) == mesh_id(b, False) == mesh_id(inverted, False)
    assert mesh_id(rigid, False) != mesh_id(a, False)
    assert mesh_id(a, True) == mesh_id(b, True) != mesh_id(inverted, True)
    for occurrence, sign in [(a, 1), (inverted, -1)]:
        mesh = mesh_id(occurrence, True)
        start = model.mesh_faceadr[mesh]
        faces = model.mesh_face[start : start + model.mesh_facenum[mesh]]
        triangles = model.mesh_vert[model.mesh_vertadr[mesh] + faces]
        assert np.sign(triangle_mesh(triangles).volume) == sign
    assert result.report["bodies"][0]["occurrence_count"] == 4


def test_resolved_connectors_follow_library_namespace(tmp_path, small_library):
    shadow = tmp_path / "shadow"
    (shadow / "parts").mkdir(parents=True)
    (shadow / "parts/cube.dat").write_text(
        "0 !LDCAD SNAP_CYL [gender=M] [caps=one] [secs=R 4 8] [pos=1 2 3]\n"
    )
    cube = (small_library / "parts/cube.dat").read_text()
    (small_library / "parts/plain.dat").write_text(cube)
    path = tmp_path / "main.ldr"
    path.write_text(
        f"1 4 0 0 0 {IDENTITY} CUBE.DAT\n1 4 40 0 0 {IDENTITY} cube.dat\n"
        f"1 4 80 0 0 {IDENTITY} plain.dat\n"
    )
    options = dict(library=small_library, cache=tmp_path / "cache", shadows=[shadow])
    result = import_ldraw(path, **options)
    assert set(result.connections) == {"cube.dat", "plain.dat"}
    (feature,) = result.connections["cube.dat"]
    assert isinstance(feature, ConnectionFeature)
    assert [feature.position.x, feature.position.y, feature.position.z] == [1, 2, 3]
    assert feature.connection_provenance is not None
    assert result.report["connection_metadata"]["cube.dat"]["feature_count"] == 1
    assert result.connections["plain.dat"] == ()
    local = tmp_path / "main.mpd"
    local.write_text("0 FILE main.ldr\n" + path.read_text() + "0 FILE cube.dat\n" + cube)
    embedded = import_ldraw(local, **options)
    assert "cube.dat" not in embedded.connections
    assert embedded.report["connection_metadata"]["cube.dat"]["coverage"] == "not_queried"


@pytest.mark.parametrize("individual", [False, True])
def test_inline_faces_match_explicit_dat(build, small_library, individual):
    faces = (small_library / "parts/cube.dat").read_text()
    # Exercise quad splitting and BFC changes between faces as well as colours.
    faces += "0 BFC CW\n4 15 -10 0 -10 10 0 -10 10 0 10 -10 0 10\n"
    header = (
        "0 FILE root.ldr\n0 BFC INVERTNEXT\n"
        "1 4 30 10 20 -2 0.1 0 0 1 0 0 0 1 child.ldr\n"
        f"1 1 100 0 0 {IDENTITY} child.ldr\n0 FILE child.ldr\n"
        f"1 16 40 0 0 {IDENTITY} cube.dat\n"
    )
    implicit = build(header + faces, suffix=".mpd", individual_parts=individual)
    explicit = build(
        header + f"1 16 0 0 0 {IDENTITY} faces.dat\n0 FILE faces.dat\n" + faces,
        suffix=".mpd", individual_parts=individual,
    )
    assert [o["id"] for o in implicit.report["occurrences"]] == [
        "0/0", "0/inline", "1/0", "1/inline"
    ]
    assert [b["occurrence_count"] for b in implicit.report["bodies"]] == (
        [1, 1, 1, 1] if individual else [2, 2]
    )
    a, b = implicit.spec.compile(), explicit.spec.compile()
    for field in ("mesh_vert", "mesh_face", "geom_rgba", "body_mass", "body_inertia"):
        np.testing.assert_allclose(getattr(a, field), getattr(b, field))
    reloaded = mujoco.MjModel.from_xml_string(implicit.spec.to_xml())
    np.testing.assert_allclose(collision_points(a), collision_points(reloaded), atol=1e-7)


def test_inline_inventory_selection_and_edits(tmp_path, small_library):
    faces = (small_library / "parts/cube.dat").read_text()
    source = (
        f"0 FILE root.ldr\n1 4 20 0 0 {IDENTITY} child.ldr\n"
        f"1 1 80 0 0 {IDENTITY} child.ldr\n"
        f"0 FILE child.ldr\n{faces}"
    )
    path = tmp_path / "input.mpd"
    path.write_text(source)
    inventory = Document(path).inventory()
    generated = [n for n in inventory["instances"] if n.get("generated")]
    assert [n["id"] for n in generated] == ["0/inline", "1/inline"]
    assert all(n["line"] is None for n in generated)
    result = import_ldraw(
        path, library=small_library, shadows=[], cache=tmp_path / "cache",
        sections="child.ldr:1",
        placement_overrides={"1": f"1 1 120 0 0 {IDENTITY} child.ldr"},
    )
    assert [o["id"] for o in result.report["occurrences"]] == ["1/inline"]
    assert result.report["occurrences"][0]["position_ldu"] == [120, 0, 0]
    assert result.report["occurrences"][0]["colour"] == 1
    with pytest.raises(ValueError, match="type-1"):
        Document(path, placement_overrides={"1/inline": generated[1]["source_text"]})
    assert path.read_text() == source
    assert list(tmp_path.glob("*.dat")) == []


def test_root_inline_faces(build, small_library):
    faces = (small_library / "parts/cube.dat").read_text()
    result = build(faces)
    assert [o["id"] for o in result.report["occurrences"]] == ["inline"]
    assert result.report["bodies"][0]["instance_id"] == "root"
    assert result.spec.compile().nq == 7


def test_missing_dat_resolves_unique_prefixed_section(build, small_library, tmp_path):
    faces = (small_library / "parts/cube.dat").read_text()
    source = (
        f"0 FILE main.ldr\n1 4 20 0 0 {IDENTITY} custom.dat\n"
        f"0 FILE model - custom.dat\n{faces}"
    )
    result = build(source, suffix=".mpd")
    assert result.report["reference_aliases"] == {"custom.dat": "model - custom.dat"}
    assert result.report["warnings"][0]["code"] == "embedded_dat_alias"
    assert result.report["occurrences"][0]["id"] == "0"
    assert result.report["occurrences"][0]["reference"] == "custom.dat"
    assert (tmp_path / "input.mpd").read_text() == source
    explicit = build(source.replace(f"{IDENTITY} custom.dat", f"{IDENTITY} model - custom.dat"),
                     suffix=".mpd")
    np.testing.assert_allclose(collision_points(result.spec.compile()),
                               collision_points(explicit.spec.compile()))
    assert mujoco.MjModel.from_xml_string(result.spec.to_xml()).nq == 7


def test_prefixed_dat_fallback_rejects_ambiguity(build, small_library):
    faces = (small_library / "parts/cube.dat").read_text()
    with pytest.raises(ValueError, match="Ambiguous embedded DAT.*a - custom.dat, b - custom.dat"):
        build(
            f"0 FILE main.ldr\n1 4 0 0 0 {IDENTITY} custom.dat\n"
            f"0 FILE a - custom.dat\n{faces}\n0 FILE b - custom.dat\n{faces}",
            suffix=".mpd",
        )


def test_prefixed_dat_does_not_replace_exact_library_part(build):
    result = build(
        f"0 FILE main.ldr\n1 4 0 0 0 {IDENTITY} cube.dat\n"
        "0 FILE model - cube.dat\n0 Empty decoy\n",
        suffix=".mpd",
    )
    assert result.report["reference_aliases"] == {}
    assert result.spec.compile().body_mass[1] > 0


def test_prefixed_dat_does_not_replace_exact_document_part(build, small_library):
    faces = (small_library / "parts/cube.dat").read_text()
    result = build(
        f"0 FILE main.ldr\n1 4 0 0 0 {IDENTITY} custom.dat\n"
        f"0 FILE custom.dat\n{faces}\n0 FILE model - custom.dat\n0 Empty decoy\n",
        suffix=".mpd",
    )
    assert result.report["reference_aliases"] == {}
    assert result.spec.compile().body_mass[1] > 0


def welded_bodies(count):
    """One free root with ``count - 1`` jointless children: many bodies, nv 6."""
    spec = mujoco.MjSpec()
    root = spec.worldbody.add_body(name="root", pos=[0, 0, 0.1])
    root.add_freejoint()
    for index in range(count):
        body = root if index == 0 else root.add_body(pos=[0.03 * (index % 50), 0.03 * (index // 50), 0])
        body.add_geom(type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.01] * 3)
    return spec


def test_arena_makes_room_for_the_broadphase_of_attached_bodies():
    # MuJoCo sizes the arena from nv; its broadphase needs 8 bytes per body pair.
    spec = welded_bodies(2000)
    with pytest.raises(mujoco.FatalError, match="stack overflow at mj_broadphase"):
        mujoco.mj_forward(model := spec.compile(), mujoco.MjData(model))
    model = _compile(spec)
    for model in (model, mujoco.MjModel.from_xml_string(spec.to_xml())):
        data = mujoco.MjData(model)
        mujoco.mj_forward(model, data)
        assert data.maxuse_arena < 0.55 * model.narena  # About MuJoCo's 50 % target.

    small = welded_bodies(10)
    assert _compile(small).narena == small.compile().narena  # MuJoCo's own guess stays.
