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


# Synthetic parts (box extents, offset) and LDCad snap metas written like
# data/offLibShadow: a stud and its socket both extend along local -Y.
CONNECTED_PARTS = {
    # A 1 x 1 plate: a stud on top, a round socket below.
    "plate.dat": (
        [20, 8, 20],
        [0, 4, 0],
        "0 !LDCAD SNAP_CYL [gender=M] [caps=one] [secs=R 6 4]\n"
        "0 !LDCAD SNAP_CYL [gender=F] [caps=one] [secs=R 6 4] [pos=0 8 0]\n",
    ),
    # Real 1 x 1 and 1 x N plates have square sockets.
    "square.dat": (
        [20, 8, 20],
        [0, 4, 0],
        "0 !LDCAD SNAP_CYL [gender=M] [caps=one] [secs=R 6 4]\n"
        "0 !LDCAD SNAP_CYL [gender=F] [caps=one] [secs=S 6 4] [pos=0 8 0]\n",
    ),
    # A 1 x 3 plate.
    "long.dat": (
        [60, 8, 20],
        [0, 4, 0],
        "0 !LDCAD SNAP_CYL [gender=M] [caps=one] [secs=R 6 4] [grid=C 3 1 20 0]\n"
        "0 !LDCAD SNAP_CYL [gender=F] [caps=one] [secs=R 6 4] [pos=0 8 0] [grid=C 3 1 20 0]\n",
    ),
    # A beam with two vertical pin holes, and a pin long enough for two beams.
    "beam.dat": (
        [60, 8, 20],
        [0, 4, 0],
        "0 !LDCAD SNAP_CYL [gender=F] [caps=none] [secs=R 4 8] [center=true] [pos=0 4 0] "
        "[grid=C 2 1 40 0]\n",
    ),
    "pin.dat": (
        [6, 16, 6],
        [0, 0, 0],
        "0 !LDCAD SNAP_CYL [gender=M] [caps=none] [secs=R 4 16] [center=true]\n",
    ),
}


@pytest.fixture
def attached(tmp_path, small_library):
    """Like ``build``, for the connected parts above and their shadow metas."""
    shadow = tmp_path / "shadow"
    (shadow / "parts").mkdir(parents=True)
    for name, (extents, offset, metas) in CONNECTED_PARTS.items():
        (small_library / "parts" / name).write_text(box_dat(f"0 Synthetic {name}", extents, offset))
        (shadow / "parts" / name).write_text(metas)

    def run(text, suffix=".ldr", **kwargs):
        path = tmp_path / ("input" + suffix)
        path.write_text(text)
        return import_ldraw(
            path, library=small_library, shadows=[shadow], cache=tmp_path / "cache", **kwargs
        )

    run.library, run.shadow = small_library, shadow
    return run


@pytest.fixture(scope="session")
def sample():
    root = Path(__file__).resolve().parents[1]
    source = root / "data/models-annotated/106-1.mpd"
    if not (root / "data/ldraw/parts").is_dir() or not source.exists():
        pytest.skip("Local LDraw library and 106-1 sample are required")
    return import_ldraw(source)
