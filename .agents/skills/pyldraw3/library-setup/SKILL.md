---
name: library-setup
description: 'Setting up the LDraw parts library for pyldraw3: download, ensure_library(), LDrawSession, Config, LDrawPaths, `ldraw generate` / `ldraw stubs`, the generated `ldraw.library.*` import hook, set_config and clean, IDE stubs, progress events and cancellation, caching and performance numbers. Use when parts cannot be found, `ldraw.library` imports fail, the library location or cache must be configured, setup must be embedded in an app, or loading is slow.'
---

# LDraw Library Setup

Get the LDraw parts library downloaded, generated and indexed so that
`ldraw.library.*` imports and `Parts` lookups work: from the CLI, from inside
an application with `ensure_library()` / `LDrawSession`, or by switching
libraries at runtime. Also covers IDE stubs, progress callbacks and
performance numbers. The basic `ldraw download` / `ldraw generate` commands
are in the [root skill](../SKILL.md).

## Quick decision

| Situation | Do this |
|---|---|
| Developer machine, scripts | `ldraw download --yes` then `ldraw generate --yes` |
| Reproducible builds | `ldraw download --version 2018-02 --yes` then `ldraw generate --yes` |
| Application bootstrap | `ensure_library()` |
| Check status before expensive work | `LDrawSession().state()` |
| Switch library inside a running process | `LibraryImporter.set_config(config)` |
| IDE shows unresolved `ldraw.library.*` imports | `ldraw stubs` |

## One-call setup: `ensure_library()`

Inspects the current state and does only the missing work: downloads the
library if absent, (re)generates `ldraw.library` if stale, rebuilds the
catalog index if stale, then wires up the importer.

```python
from ldraw import ensure_library

session = ensure_library()  # download + generate + index as needed
parts = session.load()  # ready to use
model = session.open_model("castle.mpd")
```

| Keyword | Effect |
|---|---|
| `config` / `config_file` | Explicit `Config` or config path instead of the default |
| `version=` | LDraw release to download if missing (defaults to the complete release) |
| `force_generate=True` | Regenerate `ldraw.library` even if it looks fresh |
| `write_config=True` | Persist the resolved configuration to disk |
| `on_progress=` | Callback receiving `ProgressEvent`s |

Setup failures are normalized to `RuntimeError` with a readable message
(wrapping the underlying `httpx2`/zip/`UnwritableOutputError` cause).

## Step-by-step control: `LDrawSession`

```python
from ldraw import LDrawSession

session = LDrawSession()  # uses Config.load() by default
state = session.state()

if state.ready:
    parts = session.load()
else:
    if state.needs_generation:
        ...  # call ensure_library() to fix, or regenerate
    if state.needs_index_rebuild:
        parts = session.rebuild_index()
```

| Member | Returns / does |
|---|---|
| `session.state()` | `LDrawState` with booleans `ready`, `library_available`, `needs_index_rebuild`, `needs_generation`; causes in `state.reasons` as `LDrawStateReason` (`LIBRARY_MISSING`, `INDEX_STALE`, `GENERATED_LIBRARY_MISSING`, ...) |
| `session.paths` | `LDrawPaths`: resolved `parts.lst`, generated-library, catalog-db and other paths |
| `session.load()` | Loads `Parts`, building and persisting the catalog index when needed |
| `session.rebuild_index(force=..., on_progress=...)` | Rebuilds the persistent index (unlinks a stale DB first), returns loaded parts |
| `session.open_model(path)` | Thin wrapper over `read_model` |

Use `session.paths` instead of reconstructing paths from `Config` by hand.
Without a session, `Parts` can be built from the config directly:

```python
from pathlib import Path

from ldraw.config import Config
from ldraw.parts import Parts

config = Config.load()
parts = Parts(Path(config.ldraw_library_path) / "ldraw" / "parts.lst")
```

## Progress events

Pass `on_progress` to `ensure_library`, `download` or `generate`:

```python
from ldraw import ProgressEvent, ProgressStage, ensure_library


def report(event: ProgressEvent) -> None:
    if event.total:
        print(f"[{event.stage}] {event.message}: {event.current}/{event.total}")
    else:
        print(f"[{event.stage}] {event.message}")


ensure_library(on_progress=report)
```

- `ProgressStage` is a `StrEnum`: `DOWNLOAD`, `UNPACK`, `PARTS_LIST`,
  `LIBRARY_GENERATION`, `INDEX_REBUILD`, `DONE`.
- `ProgressEvent` carries `stage`, `message`, optional `current`/`total` byte
  counts (download stage) and an optional `path`.
- Download progress is throttled to at most one event per megabyte; the first
  (`current=0`) and final counts are always sent. An ~80 MB download gives
  ~80 events.
- With no callback, no events are built.

Cancellation (`CancellationToken`, `prepare_catalog()`, resumable
`download(..., resume=True, cancellation=token)`) arrived in 1.5 and is not
covered by this skill's source docs; see [upgrading](../upgrading/SKILL.md)
and [api-reference](../api-reference/SKILL.md).

## Caches

- The generated `ldraw.library` package and the `catalog.sqlite` index
  self-heal. `LDrawSession`/`ensure_library` use the same fingerprints as
  `ldraw generate`, so they agree on when a rebuild is needed.
- Each downloaded release is cached separately.
- The generated tree lives in an OS-appropriate cache directory
  (`generated_path`); see the `ldraw config` command in [cli](../cli/SKILL.md).

## How `ldraw.library.*` imports work

pyldraw3 ships **no** parts modules. `ldraw generate` turns each catalog
description into a Python identifier (`"Brick 2 x 4"` becomes `Brick2X4`) and
writes modules into `<generated_path>/library/`:

```
<generated_path>/
└── library/
    ├── __init__.py          # ldraw.library
    ├── py.typed
    ├── colours.py           # ldraw.library.colours   (Light_Grey, Red, …)
    └── parts/
        ├── __init__.py      # ldraw.library.parts
        ├── bricks.py        # ldraw.library.parts.bricks   (Brick2X4, …)
        ├── …
        └── minifig/
            ├── __init__.py  # ldraw.library.parts.minifig
            ├── accessories.py
            ├── torsos.py
            └── …
```

Each leaf module is a flat list of `Name = "code"` assignments (for example
`Brick2X4 = "3001"`), grouped by catalog category, with subpackages for
subcategories. Imported names are plain strings holding LDraw part codes.
Users on different LDraw releases get different, matching contents.

`LibraryImporter` (in `ldraw/imports.py`) is a meta path finder inserted at
`sys.meta_path[0]` when you `import ldraw`. Registration is idempotent. It
claims only `ldraw.library` and its submodules (`ldraw.librarything` is not
claimed) and returns a file-backed spec: `<name>/__init__.py` (package) or
`<name>.py` (module).

### Import failures

| Symptom | Meaning |
|---|---|
| `ModuleNotFoundError` for `ldraw.library` | Nothing generated yet; run `ldraw generate --yes` |
| `CouldNotFindModuleError` (names both candidate paths) | Library generated, but that submodule does not exist in this release |
| `StaleModuleSpecError` | `set_config()`/`clean()` invalidated the spec before it executed; retry the import |

Probe availability without importing:

```python
importlib.util.find_spec("ldraw.library")  # None when nothing is generated
```

A failed import never leaves a half-initialised module in `sys.modules`.
Imports work under `python -W error::ImportWarning`. `load_lib` remains for
embedders that load a generated module from an explicit path.

### Where the importer gets its config

Priority order:

1. `self.config`: a `Config` passed to a specific `LibraryImporter` instance
   (rarely needed).
2. `self._default_config`: process-wide default from
   `LibraryImporter.set_config(config)`. `LDrawSession`/`ensure_library` use
   this.
3. `Config.load()`: the persisted YAML config written by `ldraw download` /
   `ldraw generate`.

In the common case you never touch the importer.

### Switching libraries at runtime: `set_config` and `clean`

```python
@classmethod
def set_config(cls, config):
    cls.clean(config=config)
```

Under one state lock, `clean` installs the optional config, advances a
configuration generation, evicts every cached `ldraw.library*` module from
`sys.modules` and drops the `library` attribute from the `ldraw` module. The
next import re-resolves against the new `generated_path`, with no restart.
If another thread is importing a generated module, `clean` waits for it to
finish. A resolved-but-not-executed spec raises `StaleModuleSpecError` and
can be retried.

## IDE stubs

Type checkers (Pylance, pyright, mypy) cannot see the generated modules.
Write a PEP 561 `ldraw-stubs/` package of `.pyi` files into the project root:

```
ldraw stubs
```

Regenerate the stubs whenever you change LDraw releases.

## Catalog symbol and import helpers

Map a catalog entry to its generated symbol:

```python
entry.symbol_name  # e.g. "Brick2X4"
entry.module_path  # "ldraw.library.parts.bricks" (or None if uncategorized)
entry.import_statement()  # "from ldraw.library.parts.bricks import Brick2X4"
```

`ldraw.snippets` offers the same as free functions: `symbol_name(entry)`,
`module_path(entry)`, `suggested_import(entry)`,
`symbol_name_for_description(description)`. They apply the exact
transformation code generation uses.

## Performance

Measured on macOS ARM64, CPython 3.12, pinned 2018-02 library, synthetic
360-piece model, seven rounds (medians):

| Operation | Before | After | Improvement |
|---|---|---|---|
| Geometry, cold (12 common parts) | 46.33 ms | 28.94 ms | 37.5% |
| Geometry, warm | 12.67 µs | 12.63 µs | 0.3% |
| Inspection, cold (360 pieces) | 860.83 ms | 209.85 ms | 75.6% |
| Inspection, warm | 802.33 ms | 177.49 ms | 77.9% |
| Analysis, cold | 859.92 ms | 216.64 ms | 74.8% |
| Analysis, warm | 810.76 ms | 179.20 ms | 77.9% |

| Fresh-process startup | Before | After |
|---|---|---|
| `import ldraw` | 93.67 ms | 13.43 ms |
| CLI `--help` | 100.52 ms | 22.92 ms |

- Cold runs clear recursive part geometry caches; warm runs reuse them.
- Geometry transforms all expanded vertices in NumPy batches and reduces
  actual vertex bounds; public `Vector` results are retained.
- `import ldraw` uses cached PEP 562 lazy exports; bare imports and `--help`
  do not load NumPy or HTTPX2. The import hook still registers immediately.

Reproduce:

```
uv run ldraw download --version 2018-02 --yes
uv run pytest benchmarks/test_model.py --benchmark-only --benchmark-json=results.json
```

Results depend on host and environment.

## Source docs

Verbatim copies, for details not covered above:

- [dynamic-imports/index.md](references/dynamic-imports-index.md)
- [upgrading-1.2/index.md](references/upgrading-1.2-index.md)
- [performance/index.md](references/performance-index.md)
