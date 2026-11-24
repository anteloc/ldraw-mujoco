---
name: occurrences-and-geometry
description: 'Walking and measuring loaded models with pyldraw3: load_model / parse_model, Model.iter_occurrences() with ModelOccurrence paths and inherited colours, ModelSummary, model_bounds(), part geometry and local-frame scaling, Parts.references_for(), stud geometry, BOM colour resolution through submodels and repeated submodels. Use when traversing MPD submodel hierarchies, computing world transforms or bounds, extracting part geometry, or building a bill of materials.'
---

# Occurrences and Geometry

Walk a loaded model's MPD submodel hierarchy as flattened, world-space part
placements, measure the model's bounds and size, look inside part files,
find top studs and build bills of materials whose colours resolve through
submodels. Reading files with `read_model` is in the [root skill](../SKILL.md);
getting a `parts` catalog (`LDrawSession().load()` / `ensure_library()`) is in
[library-setup](../library-setup/SKILL.md).

`load_model`, `parse_model` options and `ModelOccurrence` path fields are
not described in these docs; see [api-reference](../api-reference/SKILL.md)
for their exact signatures.

## Walk placed parts: `Model.iter_occurrences()`

Yields one `ModelOccurrence` per placed **leaf** part, with world transform
and inherited colour already computed:

```python
from ldraw import read_model

model = read_model("castle.mpd")

for occ in model.iter_occurrences():
    print(occ.part_code, occ.colour.code, occ.position, occ.step)
```

`ModelOccurrence` (frozen dataclass) fields:

| Field | Meaning |
|---|---|
| `piece`, `part_code`, `reference` | The source piece and its code |
| `colour` | **Effective** colour: main colour 16 resolved to the colour of the enclosing submodel reference |
| `position` / `matrix` | **World** transform, composed through every submodel reference (not piece-local) |
| `source_model` / `source_line` | Submodel the piece lives in and the line it was parsed from (`None` for pieces built in code) |
| `step` / `source_step` | Building step of this occurrence |

| Keyword | Effect |
|---|---|
| `expand_submodels=False` | Treat submodel references as leaves (yield the reference) instead of recursing |
| `include_steps=False` | Skip `0 STEP` accounting; `step`/`source_step` become `None` |

- Submodel cycles raise `SubmodelCycleError`.
- `Model.source_line_for(piece)` returns the parsed source line for that exact
  parsed piece object (preserved by `submodel_view`).
- `Model` and `ModelOccurrence` compare and hash **by identity**. Compare
  content with `m1.to_ldraw() == m2.to_ldraw()`.
- Leaf `ModelOccurrence.part_code` preserves dotted part identities
  (e.g. `custom.v1`).

Use occurrences to export world-space placements to renderers, make per-step
snapshots, map pieces back to file/line for diagnostics, or run any analysis
that needs flattened placements.

## Measure a model: `ModelSummary` and `model_bounds()`

```python
from ldraw import ModelSummary, model_bounds, read_model

model = read_model("castle.mpd")
summary = ModelSummary.from_model(model, parts)

summary.bounds  # transformed axis-aligned bounds (BoundingBox | None)
summary.size_ldu  # overall size as a Vector, in LDU
summary.size_mm  # same, in millimetres (× 0.4)
summary.part_counts  # {part_code: count}
summary.colour_usage  # {colour_code_or_rgb: count}
summary.occurrence_count
summary.skipped_geometry  # parts whose geometry couldn't be resolved
```

- `bounds` is the true transformed extent: each part's bounding-box corners
  are transformed by the world matrix before folding, so rotation counts.
- `origin_bounds` is the cheaper bounds of placement origins only.
- Unresolvable parts (missing, or no geometry) do not abort the summary.
  They become `SkippedGeometry` records (`part`, `source_model`,
  `source_line`, `reason`). Report them.
- Summaries count raw `part_code` spellings separately (BOMs aggregate case
  and separator variants).

Shorthand when only the box is needed:

```python
model_bounds(model, parts)  # -> BoundingBox
```

This supersedes hand-folding per-piece `bounding_box()` calls. Use it for
camera framing, dimension readouts and size sanity checks.

## Look inside a part: `Parts.references_for()`

Lists the type-1 subfile references inside a part file:

```python
for ref in parts.references_for("3001"):
    print(ref.kind, ref.code, ref.description)

# Recurse through subparts and primitives:
tree = parts.references_for("3001", recursive=True)
```

- `PartReference` fields: `parent_code`, `code`, `reference`, `kind`,
  `description`, resolved `colour`, `position`/`matrix`, `depth`.
- `PartReferenceKind`: `PART`, `SUBPART`, `PRIMITIVE`, `UNKNOWN` (from the
  catalog, the primitive index and the `8/48/p` primitive path conventions).
- Recursion follows everything except `UNKNOWN` and guards against cycles.

`Parts.resolve_colour(colour)` takes a `Colour` or a bare integer code and
returns the catalog's full metadata when known, else the input unchanged.

## Stud geometry

`StudReference.up` is the stud's local up direction under the placing
transforms. `is_top_stud`, and therefore `Parts.stud_positions`, use it to
exclude sideways and inverted studs:

```python
parts.stud_positions("4070")  # Headlight Brick
# 1.2.0: included the sideways front stud — a brick cannot sit on it
# 1.3.0: only the genuine top stud
```

For stud-to-stud attachment, see [connections](../connections/SKILL.md).

## Matrix and vector geometry

All three axes rotate cyclically (fixed in 1.3.0):

```python
from ldraw.geometry import Identity, Vector, XAxis, YAxis, ZAxis

Identity().rotate(90, XAxis) * Vector(0, 1, 0)  # → (0, 0, 1): ŷ→ẑ
Identity().rotate(90, YAxis) * Vector(0, 0, 1)  # → (1, 0, 0): ẑ→x̂  (was (-1, 0, 0))
Identity().rotate(90, ZAxis) * Vector(1, 0, 0)  # → (0, 1, 0): x̂→ŷ
```

`rotate` and `scale` both compose in the **local frame**:

```python
m = Identity().rotate(90, ZAxis).scale(2, 1, 1)
m * Vector(1, 0, 0)  # → (0, 2, 0): the *local* X axis was scaled
# Equivalent identity that now holds:
m == Identity().rotate(90, ZAxis) * Identity().scale(2, 1, 1)
```

- `vector * scalar` and `scalar * vector` both work.
- `matrix * unsupported` raises `TypeError`.
- `Matrix`, `Vector`, `Vector2D` are mutable and **unhashable**. Use
  `.copy()` plus a tuple key if you need one.
- `Vector.normalized()` returns a unit-length copy; raises `ValueError` for
  zero length. (`Vector.norm()` was removed.)

## Bill of materials through submodels

`bill_of_materials()` (and `ldraw bom`) traverse resolved occurrences, so the
placed colour wins over colour 16 inside a submodel:

```python
root = Model(name="main.ldr")
arm = Model(name="arm.ldr", objects=[Piece.place("3001", colour=16)])
root.add_submodel(arm, colour=4)

root.bill_of_materials()
# 1.2.0: [BomRow(part="3001", colour_code=16, quantity=1)]
# 1.3.0: [BomRow(part="3001", colour_code=4,  quantity=1)]
```

- Root-level colour-16 pieces still report code 16.
- Placing one submodel in two colours gives two rows, one per placed colour.
- A submodel placed twice contributes its pieces twice.
- `bill_of_materials(model)` and `model.bill_of_materials()` honour custom
  `iter_occurrences` overrides (relabelling, filtering).

## Repeated and shared submodels

Placing the same `Model` object again is accepted and appends another
placement piece:

```python
root.add_submodel(wheel)
root.add_submodel(wheel, position=Vector(0, -24, 0))  # now: second placement
```

Diamond-sharing a nested submodel between two parents works the same way. A
**different** `Model` object under an already-registered name still raises
`DuplicateSubmodelError`.

## Errors to catch

| Exception | When |
|---|---|
| `SubmodelCycleError` | Submodel references form a cycle during traversal |
| `DuplicateSubmodelError` | Different model object registered under an existing name |
| `InvalidColourValueError` | Unparseable colour token at parse time (file/line context) |
| `MisplacedNofileError` | `0 NOFILE` before any `0 FILE` |
| `StructuralCommentError` | Serializing `Comment("NOFILE")` / `Comment("FILE x")` |
| `EmptyPartFileError` | `.description` of an empty part file |

Concrete parse error classes are preserved; `except PartError` catches all of
them, and `PartError` carries `source` and `line_number`:

```python
try:
    read_model("broken.ldr")
except InvalidNumericValueError as exc:  # now catchable by concrete class
    print(exc.source, exc.line_number)
```

## Source docs

Verbatim copies, for details not covered above:

- [upgrading-1.2/index.md](references/upgrading-1.2-index.md)
- [upgrading-1.3/index.md](references/upgrading-1.3-index.md)
