"""Project-local parts and shadow loading; original libraries stay read-only."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

from ldraw import Parts
from ldraw.generate import generate_parts_lst

PROJECT = Path(__file__).resolve().parents[1]


def data_root() -> Path:
    return PROJECT / "data" if (PROJECT / "data").is_dir() else Path.cwd() / "data"


def load_library(library=None, shadows=None, cache=None):
    root = Path(library or os.environ.get("LDRAW_DIR") or data_root() / "ldraw").resolve()
    for name in ("parts", "p", "LDConfig.ldr"):
        if not (root / name).exists():
            raise ValueError(f"LDraw library is missing {name}: {root}; pass --library")

    # pyldraw3 expects parts.lst alongside parts/, p/ and LDConfig.ldr. Build a
    # read-through view, and let its existing index generator own the format.
    cache = Path(cache or data_root().parent / ".cache")
    key = hashlib.sha256(str(root).encode()).hexdigest()[:16]
    version = cache / "libraries" / key
    view = version / "ldraw"
    view.mkdir(parents=True, exist_ok=True)
    for name in ("parts", "p", "LDConfig.ldr"):
        link = view / name
        if not link.is_symlink():
            link.symlink_to(root / name, target_is_directory=(root / name).is_dir())
    signature = hashlib.sha256(
        "\n".join(
            f"{p.name}:{p.stat().st_size}:{p.stat().st_mtime_ns}"
            for p in sorted((root / "parts").glob("*.dat"))
        ).encode()
    ).hexdigest()
    stamp = version / "signature"
    if not (view / "parts.lst").exists() or not stamp.exists() or stamp.read_text() != signature:
        generate_parts_lst("number", version)
        stamp.write_text(signature)

    parts = Parts(view / "parts.lst")
    if shadows is None:
        configured = os.environ.get("LDRAW_SHADOW")
        shadows = configured.split(os.pathsep) if configured else [data_root() / "offLibShadow"]
    elif isinstance(shadows, (str, Path)):
        shadows = [shadows]
    selected = []
    for source in shadows:
        source = Path(source).resolve()
        if not source.exists():
            raise ValueError(f"Shadow library does not exist: {source}; use --no-shadow to disable")
        parts.add_connection_shadow(source)
        selected.append(str(source))
    return parts, root, selected
