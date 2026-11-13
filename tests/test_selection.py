import json

import mujoco
import numpy as np
import pytest

from ldraw_mujoco import import_ldraw, inspect_ldraw
from ldraw_mujoco.cli import main
from ldraw_mujoco.geometry import Document
from ldraw_mujoco.library import load_library

IDENTITY = "1 0 0 0 1 0 0 0 1"
NESTED = f"""0 FILE main.ldr
1 4 0 0 0 {IDENTITY} car.ldr
1 1 100 0 0 0 0 -1 0 1 0 1 0 0 car.ldr
0 FILE car.ldr
1 16 20 0 0 {IDENTITY} wheel.ldr
1 16 -20 0 0 {IDENTITY} wheel.ldr
1 16 0 -16 0 {IDENTITY} cube.dat
0 FILE wheel.ldr
1 16 0 0 0 {IDENTITY} cube.dat
1 16 0 -8 0 {IDENTITY} cube.dat
"""


def body_counts(result):
    return {b["instance_id"]: b["occurrence_count"] for b in result.report["bodies"]}


def test_default_welds_direct_parts_only_and_children_are_free(build):
    result = build(NESTED, suffix=".mpd")
    assert body_counts(result) == {"0": 1, "0/0": 2, "0/1": 2, "1": 1, "1/0": 2, "1/1": 2}
    model = result.spec.compile()
    assert np.all(model.body_parentid == 0)
    assert np.all(model.jnt_type == mujoco.mjtJoint.mjJNT_FREE)
    assert model.neq == 0
    names = {b["instance_id"]: b["name"] for b in result.report["bodies"]}
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    child = data.body(names["0/0"]).xpos.copy()
    parent = model.body(names["0"])
    qpos_adr = model.jnt_qposadr[parent.jntadr[0]]
    data.qpos[qpos_adr] += 0.1
    mujoco.mj_forward(model, data)
    np.testing.assert_allclose(data.body(names["0/0"]).xpos, child)


def test_flat_and_root_loose_parts_share_a_body(build):
    flat = build(f"1 4 0 0 0 {IDENTITY} cube.dat\n1 4 20 0 0 {IDENTITY} cube.dat\n")
    assert body_counts(flat) == {"root": 2}
    text = NESTED.replace("0 FILE main.ldr", f"0 FILE main.ldr\n1 4 200 0 0 {IDENTITY} cube.dat")
    mixed = build(text, suffix=".mpd")
    assert body_counts(mixed)["root"] == 1
    assert len(mixed.report["bodies"]) == 7


def test_containers_have_ids_without_empty_physics_bodies(build):
    text = NESTED.replace(f"1 16 0 -16 0 {IDENTITY} cube.dat\n", "")
    text = text.replace("0 FILE car.ldr", f"1 4 0 0 0 {IDENTITY} empty.ldr\n0 FILE car.ldr")
    text += "0 FILE empty.ldr\n"
    result = build(text, suffix=".mpd")
    assert body_counts(result) == {"0/0": 2, "0/1": 2, "1/0": 2, "1/1": 2}
    nodes = {n["id"]: n for n in result.report["instances"]}
    assert all(nodes[i]["body"] is None for i in ("root", "0", "1", "2"))
    assert nodes["2"]["reference"] == "empty.ldr"
    with pytest.raises(ValueError, match="No physical part occurrences"):
        build(text, suffix=".mpd", sections="empty.ldr")


def test_inventory_has_unique_ids_for_parts_submodels_and_empty_containers(tmp_path):
    source = tmp_path / "source.mpd"
    source.write_text(NESTED + "0 FILE unused.ldr\n")
    inventory = inspect_ldraw(source)
    nodes = {n["id"]: n for n in inventory["instances"]}
    assert len(nodes) == len(inventory["instances"]) == 17
    assert nodes["0/0/1"]["reference"] == "cube.dat"
    assert nodes["0/0/1"]["parent_id"] == "0/0"
    assert nodes["1/0"]["kind"] == "submodel"
    assert nodes["1/0"]["section"] == "car.ldr"
    assert nodes["1/0"]["line"] is not None
    assert "unused.ldr" in inventory["available_sections"]
    # A section with no direct parts remains an identifiable container.
    source.write_text(NESTED.replace(f"1 16 0 -16 0 {IDENTITY} cube.dat\n", ""))
    empty = inspect_ldraw(source)
    assert next(n for n in empty["instances"] if n["id"] == "0")["kind"] == "submodel"
    assert empty["source_sha256"] != inventory["source_sha256"]


def test_selected_instances_keep_full_input_ids_transforms_colours_and_geom_names(build):
    full = build(NESTED, suffix=".mpd")
    selected = build(NESTED, suffix=".mpd", sections=["wheel.ldr:0/1", "WHEEL.LDR:1/0"])
    assert body_counts(selected) == {"0/1": 2, "1/0": 2}
    originals = {o["id"]: o for o in full.report["occurrences"]}
    assert [o["id"] for o in selected.report["occurrences"]] == ["0/1/0", "0/1/1", "1/0/0", "1/0/1"]
    for occurrence in selected.report["occurrences"]:
        original = originals[occurrence["id"]]
        for field in (
            "position_ldu",
            "matrix_ldraw",
            "colour",
            "body",
            "collision_geom",
            "visual_geoms",
        ):
            assert occurrence[field] == original[field]
    assert [b["initial_position_m"][:2] for b in selected.report["bodies"]] == [
        [-0.008, 0],
        [0.04, 0.008],
    ]


def test_unique_names_and_ids_can_select_different_sections_together(build):
    text = NESTED.replace("0 FILE car.ldr", f"1 4 200 0 0 {IDENTITY} figure.ldr\n0 FILE car.ldr")
    text += f"0 FILE figure.ldr\n1 16 0 0 0 {IDENTITY} cube.dat\n"
    result = build(text, suffix=".mpd", sections=["FIGURE.LDR", "wheel.ldr:0/0"])
    assert body_counts(result) == {"0/0": 2, "2": 1}
    assert result.report["selected_instances"] == ["2", "0/0"]


def test_repeated_names_require_ids_and_list_choices(build):
    with pytest.raises(
        ValueError,
        match=r"Ambiguous section.*wheel.ldr:0/0, wheel.ldr:0/1, wheel.ldr:1/0, wheel.ldr:1/1",
    ):
        build(NESTED, suffix=".mpd", sections="wheel.ldr")
    with pytest.raises(ValueError, match=r"Ambiguous section.*car.ldr:0, car.ldr:1"):
        build(NESTED, suffix=".mpd", sections="CAR.LDR")


def test_overlapping_selections_are_a_union_without_changing_body_boundaries(build):
    result = build(NESTED, suffix=".mpd", sections=["car.ldr:0", "wheel.ldr:0/0", "CAR.LDR:0"])
    assert result.report["occurrence_count"] == 5
    assert body_counts(result) == {"0": 1, "0/0": 2, "0/1": 2}
    assert result.report["selected_instances"] == ["0", "0/0"]
    root = build(NESTED, suffix=".mpd", sections="MAIN.LDR:root")
    assert root.report["occurrence_count"] == 10


def test_selection_skips_unselected_part_geometry(build):
    text = NESTED.replace("0 FILE main.ldr", f"0 FILE main.ldr\n1 4 0 0 0 {IDENTITY} missing.dat")
    result = build(text, suffix=".mpd", sections="wheel.ldr:1/0")
    assert result.report["occurrence_count"] == 2


@pytest.mark.parametrize(
    "selector,match",
    [
        ("typo.ldr", r"Unknown section.*Available sections:.*car.ldr"),
        ("unused.ldr", "no placements"),
        ("cube.dat:0/0/0", "identifies a part"),
        ("99", "Unknown section or instance"),
        ("0/0", r"Bare instance IDs.*wheel.ldr:0/0"),
        ("wheel.ldr:0", r"belongs to section 'car.ldr'.*car.ldr:0"),
        ("wheel.ldr:99", "Unknown instance ID"),
        (":0/0", "expected SECTION:ID"),
        ("wheel.ldr:", "expected SECTION:ID"),
    ],
)
def test_invalid_selections_are_actionable(build, selector, match):
    text = NESTED + f"0 FILE unused.ldr\n1 4 0 0 0 {IDENTITY} cube.dat\n"
    with pytest.raises(ValueError, match=match):
        build(text, suffix=".mpd", sections=selector)


def test_selection_preserves_bfc_reference_ownership(tmp_path, small_library):
    source = tmp_path / "source.mpd"
    source.write_text(
        "0 FILE main.ldr\n0 BFC INVERTNEXT\n"
        f"1 4 0 0 0 {IDENTITY} ignored.ldr\n"
        "1 4 0 0 0 -1 0 0 0 1 0 0 0 1 selected.ldr\n"
        f"0 FILE ignored.ldr\n1 16 0 0 0 {IDENTITY} cube.dat\n"
        f"0 FILE selected.ldr\n1 16 0 0 0 {IDENTITY} cube.dat\n"
    )
    parts, _, _ = load_library(small_library, [], tmp_path / "cache")
    document = Document(source, parts, sections="selected.ldr")
    occurrence = document.occurrences()[0]
    assert document.occurrence_id(occurrence) == "1/0"
    assert id(occurrence.path[0].piece) not in document.inverted


def test_flat_ldr_and_standalone_dat_individual_parts(build, small_library):
    result = build(
        f"1 4 0 0 0 {IDENTITY} cube.dat\n1 1 40 0 0 {IDENTITY} cube.dat\n",
        individual_parts=True,
    )
    assert body_counts(result) == {"0": 1, "1": 1}
    assert result.spec.compile().nq == 14
    dat = build(
        (small_library / "parts/cube.dat").read_text(), suffix=".dat", individual_parts=True
    )
    assert body_counts(dat) == {"0": 1}


def test_embedded_dat_and_library_primitives_are_not_split(build, small_library):
    original = (small_library / "parts/cube.dat").read_text()
    (small_library / "p/solid.dat").write_text(original)
    (small_library / "parts/cube.dat").write_text(
        f"0 Cube with nested primitive geometry\n1 16 0 0 0 {IDENTITY} solid.dat\n"
    )
    result = build(
        NESTED, suffix=".mpd", sections=["wheel.ldr:0/0", "wheel.ldr:1/1"], individual_parts=True
    )
    model = result.spec.compile()
    assert (model.nbody, model.njnt, model.nq, model.nv) == (5, 4, 28, 24)
    assert all(b["occurrence_count"] == 1 for b in result.report["bodies"])
    assert {o["reference"] for o in result.report["occurrences"]} == {"cube.dat"}
    assert np.all(model.jnt_type == mujoco.mjtJoint.mjJNT_FREE)
    assert model.neq == 0
    assert sum(model.geom_group == 3) == 4
    embedded = build(
        f"0 FILE main.ldr\n1 4 0 0 0 {IDENTITY} custom.dat\n0 FILE custom.dat\n"
        f"1 16 0 0 0 {IDENTITY} cube.dat\n1 16 20 0 0 {IDENTITY} cube.dat\n",
        suffix=".mpd",
        individual_parts=True,
    )
    assert body_counts(embedded) == {"0": 1}


def test_inspect_and_select_cli(tmp_path, small_library, capsys):
    source = tmp_path / "source.mpd"
    source.write_text(NESTED)
    assert main(["inspect", str(source)]) == 0
    nodes = json.loads(capsys.readouterr().out)["instances"]
    assert any(n["id"] == "1/1/0" for n in nodes)
    output = tmp_path / "selected.xml"
    args = [
        "convert",
        str(source),
        "--library",
        str(small_library),
        "--no-shadow",
        "--section",
        "wheel.ldr:0/0",
        "--section",
        "wheel.ldr:1/1",
        "--output",
        str(output),
    ]
    assert main(args) == 0
    assert mujoco.MjModel.from_xml_path(str(output)).njnt == 2
    assert main([*args, "--individual-parts"]) == 0
    assert mujoco.MjModel.from_xml_path(str(output)).njnt == 4
    report = json.loads(output.with_suffix(".import.json").read_text())
    assert report["individual_parts"] is True
    assert report["selected_instances"] == ["0/0", "1/1"]
    assert main([*args, "--section", "wheel.ldr"]) == 1
    assert "Ambiguous section" in capsys.readouterr().err


@pytest.mark.integration
@pytest.mark.parametrize(
    "sections,individual_parts,count,bodies",
    [
        (None, False, 65, 7),
        (["106 - car.ldr"], False, 55, 6),
        (["106 - Minifig.ldr"], False, 10, 1),
        (["106 - wheel assembly.ldr:0/46"], False, 2, 1),
        (
            ["106 - wheel assembly.ldr:0/46", "106 - wheel assembly.ldr:0/49", "106 - Minifig.ldr"],
            False,
            14,
            3,
        ),
        (None, True, 65, 65),
        (["106 - Minifig.ldr"], True, 10, 10),
        (
            ["106 - wheel assembly.ldr:0/46", "106 - wheel assembly.ldr:0/49", "106 - Minifig.ldr"],
            True,
            14,
            14,
        ),
    ],
)
def test_sample_selection(sample, sections, individual_parts, count, bodies):
    result = import_ldraw(
        sample.report["source"], sections=sections, individual_parts=individual_parts
    )
    model = result.spec.compile()
    assert result.report["occurrence_count"] == count
    assert model.nbody == bodies + 1
    assert (model.nq, model.nv) == (7 * bodies, 6 * bodies)
    assert len({n["id"] for n in result.report["instances"]}) == len(result.report["instances"])
    assert all(o["parent_id"] == o["id"].rsplit("/", 1)[0] for o in result.report["occurrences"])
    if sections and "106 - wheel assembly.ldr:0/46" in sections:
        assert (
            next(o for o in result.report["occurrences"] if o["id"] == "0/46/1")["reference"]
            == "4084.dat"
        )
