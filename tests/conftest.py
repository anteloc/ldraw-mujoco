from pathlib import Path

import pytest
import trimesh

from ldraw_mujoco import import_ldraw


def box_dat(description, extents, offset):
    box = trimesh.creation.box(extents=extents)
    box.apply_translation(offset)
    records = [description, "0 BFC CERTIFY CCW"]
    for face in box.faces:
        coords = " ".join(str(x) for x in box.vertices[face].flatten())
        records.append("3 16 " + coords)
    return "\n".join(records) + "\n"


@pytest.fixture
def small_library(tmp_path):
    root = tmp_path / "library"
    (root / "parts").mkdir(parents=True)
    (root / "p").mkdir()
    (root / "LDConfig.ldr").write_text(
        "0 !COLOUR Red CODE 4 VALUE #C91A09 EDGE #333333\n"
        "0 !COLOUR Blue CODE 1 VALUE #0055BF EDGE #333333\n"
        "0 !COLOUR Light_Grey CODE 7 VALUE #9BA19D EDGE #333333\n"
        "0 !COLOUR White CODE 15 VALUE #FFFFFF EDGE #333333\n"
        "0 !COLOUR Trans_Clear CODE 47 VALUE #FCFCFC EDGE #C3C3C3 ALPHA 128\n"
    )
    (root / "parts/cube.dat").write_text(box_dat("0 Synthetic test brick", [20, 8, 20], [0, 4, 0]))
    # A 4 LDU stud primitive on the cube top; hulls skip it, visuals keep it.
    (root / "p/stud.dat").write_text(box_dat("0 Stud", [12, 4, 12], [0, -2, 0]))
    identity = "0 0 0 1 0 0 0 1 0 0 0 1"
    (root / "parts/brick.dat").write_text(
        f"0 Synthetic studded brick\n1 16 {identity} cube.dat\n1 16 {identity} stud.dat\n"
    )
    (root / "parts/knob.dat").write_text(f"0 Synthetic stud-only part\n1 16 {identity} stud.dat\n")
    return root


@pytest.fixture
def build(tmp_path, small_library):
    def run(text, suffix=".ldr", **kwargs):
        path = tmp_path / ("input" + suffix)
        path.write_text(text)
        return import_ldraw(
            path, library=small_library, shadows=[], cache=tmp_path / "cache", **kwargs
        )

    return run


@pytest.fixture(scope="session")
def sample():
    root = Path(__file__).resolve().parents[1]
    source = root / "data/models-annotated/106-1.mpd"
    if not (root / "data/ldraw/parts").is_dir() or not source.exists():
        pytest.skip("Local LDraw library and 106-1 sample are required")
    return import_ldraw(source)
