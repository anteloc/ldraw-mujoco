---
name: building-models
description: 'Building LDraw models programmatically with pyldraw3: coordinate system and units (LDU, STUD_PITCH, PLATE_HEIGHT, BRICK_HEIGHT), Piece placement with Vector and Matrix rotations, Colour lookup, Group transforms, minifigures (Person, MinifigSection), part categories, scene composition, reading/writing model files, and troubleshooting part-not-found, colour and positioning issues. Use when creating or editing .ldr/.mpd content in Python, placing or rotating pieces, choosing colours, or following the example scripts.'
---

# Building LDraw Models

Build LEGO models in Python with pyldraw3: place pieces with `Vector`
positions and `Matrix` rotations, pick colours, move groups of pieces as a
unit, pose minifigures, compose scenes and read/write `.ldr`/`.mpd` files.
Installation and the core object overview are in the [root skill](../SKILL.md).

## Setup

```
uv sync
source .venv/bin/activate
uv run ldraw download --version 2018-02 --yes
uv run ldraw generate --yes
```

`ldraw.library.*` imports (colours, part modules) need a generated library.
`Piece.place("3001", ...)` with plain LDraw codes works without generated
part modules. See [library-setup](../library-setup/SKILL.md) for details.

## First model (no generated part modules)

```python
from pathlib import Path
from ldraw import Matrix, Model, Piece, Vector, LDrawSession
from ldraw.units import STUD_PITCH, PLATE_HEIGHT, BRICK_HEIGHT, LDU_TO_MM

model = Model(name="first.ldr")
model.add(Piece.place("3001", colour=4))
model.add(
    Piece.place(
        "3005",
        colour=14,
        position=Vector(STUD_PITCH, -BRICK_HEIGHT, 0),
        matrix=Matrix.rotation(x=0, y=90, z=0),
    )
)
model.save(Path("first.ldr"))
parts = LDrawSession().load()
print(parts.description_for("3001"))
```

## Coordinates and units

| Axis | Direction |
|---|---|
| X | left negative, right positive |
| Y | top negative, bottom positive (Y is inverted: positive goes **down**) |
| Z | front positive, back negative |

Positions are in LDraw units (LDU); 1 LDU is about 0.4 mm.

| Constant (`ldraw.units`) | Value |
|---|---|
| `STUD_PITCH` | 20 LDU |
| `PLATE_HEIGHT` | 8 LDU |
| `BRICK_HEIGHT` | 24 LDU |
| `LDU_TO_MM` | 0.4 (multiply LDU by it for millimetres) |

The historical `ldraw.model_summary.LDU_TO_MM` import remains available.
To stack a brick on top of another, use a negative Y offset
(`-BRICK_HEIGHT`).

## Rotations

`Matrix.rotation(*, x=0, y=0, z=0, units=Degrees)` returns a fresh matrix,
equivalent to the local X/Y/Z `Identity().rotate(...)` chain. Use `Radians`
from `ldraw.geometry` for radian angles. Each matrix is independent.

Chain rotations explicitly with `rotate(angle, axis)`:

```python
from ldraw.geometry import Identity, Vector, XAxis, YAxis
from ldraw.library.colours import Red
from ldraw.library.parts import Brick2X2
from ldraw.pieces import Piece

rotation = Identity()
rotation = rotation.rotate(90, YAxis)
rotation = rotation.rotate(45, XAxis)

piece = Piece(Red, Vector(0, 0, 0), rotation, Brick2X2)
```

## Two ways to construct a Piece

| Style | Form |
|---|---|
| Positional (classic) | `Piece(colour, position, matrix, part, group=...)` |
| Keyword-first (new code) | `Piece.place("3005", colour=4, position=..., matrix=...)` |

`Piece.place("custom.v1")` uses the default reference `custom.v1.dat`,
matching the constructor. Pass `suffix=""` to keep a reference suffix-free
(earlier factory behaviour kept `custom.v1` suffix-free).

## Colours

Import colour constants from `ldraw.library.colours` (names such as
`Dark_Blue`, `Chrome_Gold`, `Trans_Red` follow the same pattern):

```python
from ldraw.library.colours import (
    Black,
    Chrome_Silver,
    Light_Grey,
    Red,
    Trans_Clear,
    Yellow,
)
```

`Piece.place` and `Person` methods also accept integer LDraw colour codes
(`colour=4`, `colour=14`), as in the `Model` examples.

## Groups and group transforms

Groups organize pieces and transform them together. Change `position` and
`matrix` on the group, then re-emit its pieces:

```python
from ldraw.geometry import Identity, Vector, YAxis
from ldraw.library.colours import Blue, Red, Yellow
from ldraw.library.parts import Brick1X1, Brick2X2
from ldraw.pieces import Group, Piece

building = Group(Vector(0, 0, 0), Identity())

Piece(Red, Vector(0, 0, 0), Identity(), Brick2X2, group=building)
Piece(Blue, Vector(0, -24, 0), Identity(), Brick2X2, group=building)
Piece(Yellow, Vector(20, -48, 0), Identity(), Brick1X1, group=building)

building.position = Vector(100, 0, 0)
building.matrix = Identity().rotate(45, YAxis)

for piece in building.pieces:
    print(piece)
```

To duplicate geometry, keep one group and loop: set `position`/`matrix`,
then print `group.pieces` each time (see `stairs.py` below).

## Minifigures (`Person`)

Call one method per body part; the classic examples `print` each result to
emit LDraw text. The numeric arguments set the pose (the docs show values
such as `35`, `70`, `-90` without naming the parameter).

```python
from ldraw.figure import Person
from ldraw.library.colours import Black, Blue, Red, Yellow
from ldraw.library.parts.minifig.accessories import HairMale
from ldraw.library.parts.minifig.torsos import Torso

figure = Person()

print(figure.head(Yellow, 35))
print(figure.hat(Black, HairMale))
print(figure.torso(Red, Torso))
print(figure.hips(Blue))
print(figure.left_leg(Blue, 5))
print(figure.right_leg(Blue, 20))
print(figure.left_arm(Red, 0))
print(figure.left_hand(Yellow, 0))
print(figure.right_arm(Red, -90))
print(figure.right_hand(Yellow, 0))
```

Pose limbs and hold accessories with `right_hand_item` (trimmed from the
docs' detective example):

```python
from ldraw.figure import Person
from ldraw.geometry import Vector
from ldraw.library.colours import Black, Chrome_Silver, White, Yellow
from ldraw.library.parts.minifig.accessories import ToolMagnifyingGlass
from ldraw.library.parts.minifig.hats import TopHat
from ldraw.library.parts.minifig.heads import HeadWithMonocle_Scar_AndMoustachePattern

detective = Person()
detective.head(Yellow, part=HeadWithMonocle_Scar_AndMoustachePattern)
detective.hat(Black, TopHat)
detective.left_arm(Black, 70)
detective.right_hand(White, 0)

detective.right_hand_item(
    Chrome_Silver,
    Vector(0, -58, -20),
    0,
    ToolMagnifyingGlass,
)
```

`Person(position=Vector(...), group=group)` places the figure inside a group.
`hips_and_legs` is a convenience method (shown in `figures.py`).
`MinifigSection` is not documented in these docs; check
[api-reference](../api-reference/SKILL.md) for it.

## Part categories

Generated part modules follow library categories, e.g.
`ldraw.library.parts`, `ldraw.library.parts.minifig.accessories`, `.hats`,
`.heads`, `.torsos`. Star-imports such as
`from ldraw.library.parts.minifig.hats import *` work.

## Scene lighting

`LIGHT` pseudo-pieces have no effect in pyldraw3, but some downstream
raytracers honour them:

```python
from ldraw.geometry import Identity, Vector
from ldraw.library.colours import White
from ldraw.pieces import Piece

print(Piece(White, Vector(150, -100, -150), Identity(), "LIGHT"))
print(Piece(White, Vector(-150, -100, -150), Identity(), "LIGHT"))
print(Piece(White, Vector(0, -100, 150), Identity(), "LIGHT"))
```

## Compose a `Model`

The `Model.from_pieces` / `add_group` / `add_submodel` / `save` pattern is in
the [root skill](../SKILL.md). `model.add(piece)` appends one piece, and
`add_submodel` registers an MPD section and returns the type-1 piece that
references it:

```python
reference = model.add_submodel(wheels, position=Vector(0, -24, 0))
```

Query helpers work on built and parsed models alike:

```python
model.find_pieces(part="3001")
model.find_pieces(colour=4)
model.find_pieces(colour=4, recursive=True)
list(model.iter_pieces())
model.bill_of_materials()
```

`bill_of_materials` counts leaf pieces by part and colour; a submodel placed
twice contributes its pieces twice. Pass `parts=Parts.get(...)` to resolve
descriptions and colour names. Export with `ldraw.bom.rows_to_csv` or
`rows_to_json`.

## Read and edit model files

`read_model` reads `.ldr` and `.mpd` files into a `Model`. MPD documents split
on `0 FILE` / `0 NOFILE`: the first section is the root model, later ones are
submodels.

```python
from ldraw import parse_model, read_model

model = read_model("my_model.mpd")

print(model.description, model.header_name, model.author)
print(model.ldraw_org, model.license, model.bfc)

for piece in model.pieces:
    submodel = model.submodel_for(piece)
    print(piece.reference, submodel)

model.objects.append(
    parse_model("1 4 0 0 0 1 0 0 0 1 0 0 0 1 3005.dat").objects[0],
)
model.save("my_model_out.mpd")
```

- Every parsed object has `to_ldraw()`; `str(model)` serializes the document.
- `str(model)` can raise the same errors as `to_ldraw()` or `save()`; use
  `repr()` for inspection.
- Distinct submodels with conflicting normalized names raise
  `DuplicateSubmodelError` on serialization.
- NaN/Infinity values parse, but serialization raises `ValueError` until
  repaired.
- Parse errors name the file and 1-based line number.

Instructions (`InstructionBuilder`) are introduced in the
[root skill](../SKILL.md).

## Compare a model with an inventory CSV

```python
from ldraw import compare_inventory, read_inventory, read_model

inventory = read_inventory("inventory.csv")
comparison = compare_inventory(
    read_model("scene.mpd"), inventory, part_aliases={"old-part": "new-part"}
)
for difference in comparison.differences:
    print(
        difference.part,
        difference.colour,
        difference.expected,
        difference.actual,
        difference.missing,
        difference.extra,
    )
assert comparison.matched
```

- Native BOM CSV columns: `part`, `colour_code`, `quantity` (RGB rows use
  `colour_name` when `colour_code` is empty). Quantities must be nonnegative
  integers.
- Third-party CSV: `read_inventory(columns={"part": "Part ID", "colour":
  "Colour ID", "quantity": "Qty"}, colour_map={"red": 4})`. A supplied colour
  map must cover every inventory colour.
- Pass `parts=parts` to `compare_inventory` so leaf references without `.dat`
  are checked against `parts.lst`.
- Missing columns, invalid quantities/colours, cycles, unresolved references
  and non-finite geometry fail instead of giving partial matches.

The CLI form (`ldraw bom --compare`) is in [cli](../cli/SKILL.md).

## Example scripts

The [`examples/`](https://github.com/hbmartin/pyldraw3/tree/main/examples)
scripts print LDraw text to stdout. Redirect into a file and open it in
LDView, LeoCAD or Stud.io:

```
python examples/figures.py > figures.ldr
```

| Script | Demonstrates |
|---|---|
| `figure.py` | Simplest minifigure, plus `"LIGHT"` sources. Best starting point. |
| `diver.py` | Accessories (`DiverMask`, `Airtanks`, `Flipper`...), whole `Person` tilted by a rotated matrix. |
| `brothers.py` | Build inside a `Group`, change its `position`/`matrix`, re-emit. |
| `figures.py` | Multiple posed figures, `hips_and_legs`, `Baseplate16X16`. |
| `spaceman.py` | Procedural grid of figures with seeded `random` rotations. |
| `stairs.py` | Reusing one group to emit a spiral of staircases. |
| `buggy.py` | Full vehicle with chrome, rubber and metallic colours. |
| `moon_landing.py` | Diorama; one rover `Group` emitted twice at new placements. |
| `mandelbrot.py` | Computed artwork from `Brick1X1`, colour per escape count. |
| `instructions.py` | Steps, callout, ROTSTEP, camera, note, highlight, arrow; self-contained MPD. |

The examples use the classic style (`print(...)` each object as built).
New code can assemble a `Model` and save once. Both produce the same LDraw
output.

## Troubleshooting

| Problem | Fix |
|---|---|
| Part not found / generated imports fail | `uv run ldraw generate --yes` |
| Imports fail after switching library versions | `uv run ldraw download --version 2018-02 --yes` then `uv run ldraw generate --yes` |
| Wrong colours | Import constants from `ldraw.library.colours` |
| Pieces in wrong place | Y is inverted (positive is down); adjust in small increments |

Validate files with `ldraw validate my_model.ldr` (see [cli](../cli/SKILL.md)).

## Source docs

Verbatim copies, for details not covered above:

- [guide/index.md](references/guide-index.md)
- [examples/index.md](references/examples-index.md)
