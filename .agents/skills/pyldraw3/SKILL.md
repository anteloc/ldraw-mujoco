---
name: pyldraw3
description: Python package (import name `ldraw`) for reading, writing, building and analysing LDraw LEGO CAD files (.ldr, .mpd, .dat). Covers installation, library setup, the core objects (Piece, Group, Matrix, Vector, Colour, Model), reading models and the map to task subskills. Use when code imports `ldraw` or `ldraw.library.*`, depends on pyldraw3, parses or writes LDraw files, or needs LDraw parts, colours, geometry, connections or the `ldraw` CLI.
---

# pyldraw3

`pyldraw3` (import name `ldraw`) is a modern Python package for creating and
manipulating LDraw files (`.ldr`, `.mpd`), the standard used by LEGO CAD
applications. It is a drop-in replacement for the unmaintained `pyldraw`
library. Use this skill for installation, the library setup, the core objects
and the canonical build/read/write pattern. It also shows which subskill
covers each task.

## Features

- Complete LDraw format support for creating `.ldr` and `.mpd` files.
- Pythonic model construction with `Piece`, `Group`, `Model` and `Person`.
- Dynamic `ldraw.library.*` modules generated from a downloaded LDraw library.
- Catalog search, validation, bill-of-materials export and type-stub helpers.
- Tolerant one-read loading with machine-readable diagnostics and partial models.
- Sectioned STEP/ROTSTEP and LPub3D instruction semantics, manifests and snapshots.
- Exact geometry, connector, occurrence-provenance and inspection APIs.

## Install

```
uv add pyldraw3
```

## Set up the LDraw library

Activate the virtual environment, then download the library and generate
`ldraw.library.*`:

```
source .venv/bin/activate
ldraw download --yes
ldraw generate --yes
```

`ldraw download` fetches the `complete` LDraw release by default. Pin a dated
release for reproducible builds with `--version`:

```
ldraw download --version 2018-02 --yes
ldraw generate --yes
```

Each downloaded release is cached separately. `ldraw generate` builds
`ldraw.library.*` from whichever release is currently configured. For
configuration, programmatic setup and the import hook, see
[library-setup](library-setup/SKILL.md).

## Core API

The top-level `ldraw` package re-exports the main construction and file I/O
types:

```python
from ldraw import Group, Identity, Model, Parts, Person, Piece, Vector, read_model
```

| Object | Role |
|---|---|
| `Piece` | One placed part. Positional form: colour, position (`Vector`), rotation (e.g. `Identity()`), part, group. `Piece.place` is the keyword-first constructor. |
| `Group` | A container of pieces; `print(group)` emits its LDraw text. |
| `Model` | Bridges construction and file I/O: pieces, groups, submodels, BOM, save. |
| `Person` | Minifigure builder (`head`, `torso`, ...). |
| `Parts` | Runtime part lookup by catalog description or LDraw code. |
| `read_model` | Parses `.ldr` and `.mpd` files into a `Model`. |

## Canonical pattern: build and write

```python
from ldraw import Group, Identity, Piece, Vector
from ldraw.library.colours import Light_Grey
from ldraw.library.parts.bricks import Brick1X2WithClassicSpaceLogoPattern

model = Group()
Piece(
    Light_Grey,
    Vector(-10, -32, -90),
    Identity(),
    Brick1X2WithClassicSpaceLogoPattern,
    model,
)

with open("my_model.ldr", "w") as ldr_file:
    print(model, file=ldr_file)
```

For new code, `Piece.place` offers a keyword-first constructor with sensible
defaults:

```python
from ldraw import Piece

piece = Piece.place("3005", colour=4)
```

## Compose a `Model`

```python
from ldraw import Group, Model, Person, Piece, Vector

model = Model.from_pieces(
    [Piece.place("3001", colour=4)],
    name="scene.ldr",
    description="A scene",
    author="you",
)

group = Group()
figure = Person(position=Vector(0, -48, 0), group=group)
figure.head(colour=14)
figure.torso(colour=4)
model.add_group(group)

wheels = Model.from_pieces([Piece.place("3005", colour=0)], name="wheels.ldr")
model.add_submodel(wheels, position=Vector(0, -24, 0))

model.find_pieces(colour=4)
list(model.iter_pieces())
model.bill_of_materials()
model.save("scene.ldr")
```

## Look up parts at runtime

Use `Parts` to resolve a catalog description to an LDraw code:

```python
from pathlib import Path

from ldraw.config import Config
from ldraw.parts import Parts

config = Config.load()
parts = Parts(Path(config.ldraw_library_path) / "ldraw" / "parts.lst")
cowboy_hat = parts.get_entry_by_description("Minifig Hat Cowboy").code
brick1x1 = parts.get_entry_by_description("Brick  1 x  1").code
```

## Read model files

`read_model` parses `.ldr` and `.mpd` files, including MPD `0 FILE` /
`0 NOFILE` sections:

```python
from ldraw import read_model

model = read_model("my_model.ldr")
print(model.description, model.author)

for piece in model.pieces:
    print(piece.part, piece.position)

model.save("my_model_out.ldr")
```

- Every parsed object has a `to_ldraw()` method, so parsed content
  round-trips back to LDraw text.
- Parse errors report the file and 1-based line number.
- To walk submodel hierarchies with world transforms and inherited colours,
  use [occurrences-and-geometry](occurrences-and-geometry/SKILL.md).

## Building instructions

`Model.instruction_document()` interprets root and reachable submodels as
independent instruction sections. `InstructionBuilder` authors portable
STEP/ROTSTEP and supported LPub3D structures plus namespaced notes, arrows and
highlights:

```python
from ldraw import InstructionBuilder, Model, Piece

model = Model(name="model.ldr", objects=[Piece.place("3001", colour=4)])
builder = InstructionBuilder(model)
builder.note("Attach the red brick")
builder.step()

for step in model.iter_instruction_steps():
    print(step.number, step.added_bill_of_materials())
```

Use `ldraw instructions export` for JSON consumers or
`ldraw instructions snapshots` for cumulative MPD and flattened LDR artifacts
(see [cli](cli/SKILL.md)). Rendering and PDF page layout are outside
pyldraw3's scope.

Open generated `.ldr` files in an LDraw viewer such as LDView, LeoCAD or
Stud.io.

## Which subskill for which task

| Task | Subskill |
|---|---|
| Place/rotate pieces, colours, units, minifigs, example scripts | [building-models](building-models/SKILL.md) |
| Parts not found, `ldraw.library` import errors, config, cache, slow loading | [library-setup](library-setup/SKILL.md) |
| Traverse MPD hierarchies, world transforms, bounds, part geometry, BOM through submodels | [occurrences-and-geometry](occurrences-and-geometry/SKILL.md) |
| Which parts are attached (studs, pins, axles, clips, hinges), LDCad shadow metadata | [connections](connections/SKILL.md) |
| Running `ldraw` commands, validating files, inventory comparison | [cli](cli/SKILL.md) |
| Comparing renders against reference images | [visual-comparison](visual-comparison/SKILL.md) |
| Moving between versions 1.1 to 1.7, behaviour changes | [upgrading](upgrading/SKILL.md) |
| Exact signatures, fields, enum values | [api-reference](api-reference/SKILL.md) |

## Subskills

Read the one that matches your task:

- [building-models](building-models/SKILL.md): Building LDraw models programmatically with pyldraw3: coordinate system and units (LDU, STUD_PITCH, PLATE_HEIGHT, BRICK_HEIGHT), Piece placement with Vector and Matrix rotations, Colour lookup, Group transforms, minifigures (Person, MinifigSection), part categories, scene composition, reading/writing model files, and troubleshooting part-not-found, colour and positioning issues. Use when creating or editing .ldr/.mpd content in Python, placing or rotating pieces, choosing colours, or following the example scripts.
- [library-setup](library-setup/SKILL.md): Setting up the LDraw parts library for pyldraw3: download, ensure_library(), LDrawSession, Config, LDrawPaths, `ldraw generate` / `ldraw stubs`, the generated `ldraw.library.*` import hook, set_config and clean, IDE stubs, progress events and cancellation, caching and performance numbers. Use when parts cannot be found, `ldraw.library` imports fail, the library location or cache must be configured, setup must be embedded in an app, or loading is slow.
- [occurrences-and-geometry](occurrences-and-geometry/SKILL.md): Walking and measuring loaded models with pyldraw3: load_model / parse_model, Model.iter_occurrences() with ModelOccurrence paths and inherited colours, ModelSummary, model_bounds(), part geometry and local-frame scaling, Parts.references_for(), stud geometry, BOM colour resolution through submodels and repeated submodels. Use when traversing MPD submodel hierarchies, computing world transforms or bounds, extracting part geometry, or building a bill of materials.
- [connections](connections/SKILL.md): Typed part connectivity in pyldraw3: ConnectionKind/Role/Freedom vocabulary, ConnectionFeature queries from the catalog, LDCad shadow (LDCadShadowLibrary) and Studio connectivity sources, authoritative metadata configuration, stud_contacts(), ConnectionContact, typed contacts and connection multigraphs, stud receptacles on the mating grid and derived sockets, diagnostics and caching. Use when detecting which parts are attached (studs, pins, axles, clips, hinges), loading LDCad shadow metadata, or interpreting connection results and diagnostics.
- [cli](cli/SKILL.md): The `ldraw` command-line tool: geometry and model inspection, rendering previews, validating LDraw files (severity levels, checks, exit codes, iter_ldr_issues programmatic API), instruction commands, inventory comparison against CSV, development commands and testing CLI handlers. Use when running or scripting `ldraw` commands, validating .ldr/.mpd files, or comparing a model against an inventory.
- [visual-comparison](visual-comparison/SKILL.md): Comparing renders of LDraw models against reference images with pyldraw3: comparing one view, ranking existing renders, generating and ranking a LeoCAD camera grid, cropping important regions, multi-view reports and interpreting scores. Use when checking that a reconstructed or converted model looks like a reference photo or render.
- [upgrading](upgrading/SKILL.md): Version-by-version migration notes for pyldraw3 1.1 through 1.7: breaking changes, new APIs, behaviour changes (Y-rotation fix, strict colour parsing, strict stud_contacts, HTTPX downloads, stud receptacle grid) and upgrade checklists. Use when moving between pyldraw3 versions, when behaviour differs from what code expects, or to find which version introduced an API.
- [api-reference](api-reference/SKILL.md): Full generated reference of the public `ldraw` API (ldraw.__all__): signatures, fields and docstrings of classes such as Model, ModelOccurrence, Parts, PartsCatalog, Piece, Matrix, Vector, Colour, LDrawSession, ConnectionFeature, ConnectionContact, StudContact, Diagnostic, InstructionBuilder, and functions such as load_model, parse_model, model_bounds, part_bounding_box, part_studs, connections_compatible, snap_transform, ensure_library, validate helpers and bill_of_materials. Use when an exact signature, field, enum value or return type is needed.

## Source docs

Verbatim copies, for details not covered above:

- [index.md](references/index.md)
