---
name: upgrading
description: 'Version-by-version migration notes for pyldraw3 1.1 through 1.7: breaking changes, new APIs, behaviour changes (Y-rotation fix, strict colour parsing, strict stud_contacts, HTTPX downloads, stud receptacle grid) and upgrade checklists. Use when moving between pyldraw3 versions, when behaviour differs from what code expects, or to find which version introduced an API.'
---

# Upgrading pyldraw3 (1.1 to 1.7)

Find what changed between pyldraw3 versions, which version introduced an API,
and what code must change when upgrading. Each section lists breaking or
result-changing behaviour first, then new APIs and a checklist. How to use
the newer APIs in depth is in [library-setup](../library-setup/SKILL.md),
[occurrences-and-geometry](../occurrences-and-geometry/SKILL.md) and
[connections](../connections/SKILL.md).

## Quick lookup: which version changed what

| Symptom / API | Version |
|---|---|
| `Piece.place("3001").reference` is `"3001.dat"` not `"3001.DAT"` | 1.1 |
| `Parts.part()` raises `PartNotFoundError` instead of returning `None` | 1.1 |
| `Colour.rgb` always `#RRGGBB` | 1.1 |
| `ensure_library`, `LDrawSession`, `iter_occurrences`, `ModelSummary` | 1.2 |
| Y rotations turn the other way; `scale` composes in local frame | 1.3 |
| BOM colour 16 resolves through submodels | 1.3 |
| `InvalidColourValueError` at parse time | 1.3 |
| `Vector.norm()` gone (use `normalized()`) | 1.3 |
| `InstructionBuilder`, `instruction_document`, `ldraw instructions` | 1.4 |
| `prepare_catalog`, `load_model`, `CancellationToken`, `inspect_model`, `render_preview` | 1.5 |
| `ModelOccurrence.path` | 1.5 |
| Typed connections, `stud_contacts()` strict, `Matrix.inverse()` | 1.6 |
| HTTPX2 downloads; stud receptacles on the mating grid | 1.7 |

## 1.0 → 1.1

**Behaviour changes**

| Change | Impact |
|---|---|
| Piece part/suffix case preserved | `DEFAULT_SUFFIX` is `".dat"`; `split_reference` no longer uppercases |
| `Parts.part()` always raises on a miss | Use `find_part()` for `None` |
| `Colour.rgb` canonicalized to `#RRGGBB` | Malformed values raise `ValueError` at construction |
| Minifig descriptions kept as written | Catalog/BOM/`ldraw parts` show `Minifig Torso`; symbol names unchanged |
| `PartCategory` gained 27 members | Parts leave `OTHER`; new modules such as `ldraw.library.parts.panels` |
| Colour finishes `GLITTER`, `SPECKLE`, `LUMINANCE` | New tokens in `colour_attributes` |
| Config no longer sniffs `sys.argv` | Pass `Config.load(config_file="/path/to/config.yml")` |

**Removed:** `ldraw.config.is_valid_config_file`, the module-level `parser`,
`ldraw.errors.InvalidConfigFileError`.

Migrate case comparisons by casefolding:

```python
# 1.1.0
if piece.part.casefold() == "3001":
    ...
if piece.reference.casefold() == "3001.dat":
    ...
```

Migrate `part()` miss handling:

```python
try:
    part = parts.part(code="3001")
except PartNotFoundError:
    handle_missing()

# ...or keep the None-flavored flow with find_part()
if (part := parts.find_part(code="3001")) is None:
    handle_missing()
```

`part()` with neither argument raises `ValueError`. `PartNotFoundError`
has `.code` and `.path`.

**New APIs:** `Parts.bounding_box(code)`, `Parts.studs(code)`,
`Parts.stud_positions(code)`, `BoundingBox`, `StudReference`,
`Model.add_step()` / `Model.steps`, `Model.set_header(ldraw_org=...,
license=...)`, `Model.submodel_view(name)`, `Parts.find_part(...)`,
`Parts.description_for(code)`, `Colour.is_solid`,
`symbol_description(description)`; functional forms
`part_bounding_box(parts, code)` / `part_studs(parts, code)` in
`ldraw.part_geometry`.

- `submodel_view` fixes BOMs taken from `root.submodels["wing.ldr"]`, which
  count sibling submodel references as parts. Unknown names raise
  `UnknownSubmodelError`.
- `bounding_box` raises `NoGeometryError` for a part with no geometry.
- Colliding generated symbols now get part-code suffixes.

**Checklist:** upgrade; caches self-heal (or `ldraw generate --force` then
`ldraw stubs`); search for uppercase `.part`/`.reference` comparisons,
`".DAT"`, `part(...) is None`, non-`#RRGGBB` rgb comparisons, stripped
`"Minifig "` prefixes, removed config names; regenerate golden `.ldr` files.

## 1.1 → 1.2 (purely additive)

No behaviour changes, no removals. New:

| API | Purpose |
|---|---|
| `ensure_library(...)`, `LDrawSession`, `LDrawState`/`LDrawStateReason`, `LDrawPaths` | Embeddable setup |
| `ProgressEvent`/`ProgressStage`; `on_progress=` on `download()`/`generate()` | Progress |
| `Model.iter_occurrences()`, `ModelOccurrence`, `Model.source_line_for(piece)` | World-space placements |
| `ModelSummary`, `model_bounds()`, `SkippedGeometry` | Whole-model bounds |
| `Parts.references_for(code)`, `PartReference`/`PartReferenceKind`, `Parts.resolve_colour` | Part introspection |
| `CatalogEntry.symbol_name`/`.module_path`/`.import_statement()`, `ldraw.snippets` | Generated-import helpers |
| `Colour.display_label`/`swatch_rgb`/`swatch_alpha`/`is_transparent` | UI colour accessors |

Python 3.14 added (3.12+ floor). Checklist: upgrade; nothing else.

## 1.2 → 1.3 (correctness release; results change)

| Change | Old | New |
|---|---|---|
| `Matrix.rotate(angle, YAxis)` | Opposite to X/Z | Cyclic: 90° about Y maps +Z→+X |
| `Matrix.scale(...)` | World frame (pre-multiply) | Local frame, like `rotate` |
| `bill_of_materials()` / `ldraw bom` | Colour 16 in submodels stayed 16 | Placed colour wins |
| `Model.add_submodel(same_object)` | `DuplicateSubmodelError` | Another placement |
| `is_top_stud` / `stud_positions` | Counted sideways/inverted studs | Uses `StudReference.up` |
| Validator colours | Warned on real 256–511 colours | Catalog checked first; all direct-colour spellings |
| `Person` defaults | `3815b`/`3816b`/`3817b`, hair as hat | `3815`/`3816`/`3817`, head `3626b`, hat `3624` |

```python
Identity().rotate(90, YAxis) * Vector(0, 0, 1)  # → (1, 0, 0): ẑ→x̂  (was (-1, 0, 0))
```

Remove any negated-Y-angle compensation.

**Now raise:** `InvalidColourValueError` (bad colour token at parse),
`StructuralCommentError` (serializing `Comment("NOFILE")`/`Comment("FILE
x")`), `MisplacedNofileError` (`0 NOFILE` before `0 FILE`),
`EmptyPartFileError`, `ConfigLoadError` (bad `config.yml`). Also new:
`GeneratedModuleSyntaxError`.

**Now warn and continue:** malformed `parts.lst` lines; missing/unparseable
part files during categorization; descriptions containing `.dat` parse.

**Removed:** `LibraryImporter.load_module`/`find_module`/`get_code` (use
`import` or `ldraw.imports.load_lib(generated_path, fullname)`),
`Vector.norm()` (use `Vector.normalized()`, raises `ValueError` on zero),
`Vector`/`Vector2D` `__rsub__`/`__cmp__`, `ldraw.utils.flatten`,
`ldraw.schemas`, `NoLibrarySelectedError`.

Other notes:

- `Matrix`/`Vector`/`Vector2D` are unhashable; `vector * scalar` works;
  `matrix * unsupported` raises `TypeError`.
- `Model` and `ModelOccurrence` compare/hash by identity; compare content
  with `to_ldraw()`.
- Direct colours accept `0X2FF0000` and decimal `50266112`; re-serialize as
  `0x2RRGGBB`. `0x2RGB` shorthand rejected in files.
- Import hook uses `find_spec`; no generated library → `ModuleNotFoundError`;
  `set_config`/`clean` thread-safe; `StaleModuleSpecError` can be retried.
- Cache fingerprints hash every file under `parts/` and `p/`; generation
  schema v3, catalog v4.
- CLI errors go to stderr; 30-second network timeout; importing `ldraw` no
  longer creates directories.
- Parse errors keep their concrete class; `PartError` has `source` and
  `line_number`.

**Checklist:** upgrade; caches rebuild automatically; re-check Y rotations
and `.rotate(...).scale(...)` chains; expect BOM rows split by placed colour;
`except PartError` still catches all parse errors.

## 1.3 → 1.4 (backward compatible)

Adds renderer-neutral building instructions. Raw `Model.objects`, comments,
serialization and legacy `Model.steps` are unchanged.

```python
from ldraw import (
    CameraState,
    InstructionBuilder,
    InstructionDocument,
    InstructionIssue,
    InstructionSection,
    InstructionStep,
    RotationMode,
    RotationStep,
    iter_instruction_issues,
)
```

- `model.instruction_document(parts=...)` → root-first sections, each with
  its own steps; `model.iter_instruction_steps()` for the root.
- Recognizes `STEP`, MLCad `ROTSTEP`, `0 !LPUB`/`0 LPUB` callouts, multi-step,
  suppression, ignore ranges, pages, camera, and `!PYLDRAW` notes,
  highlights, arrows. Unsupported LPub stays raw.
- New CLI: `ldraw instructions inspect|validate|export|snapshots` (see
  [cli](../cli/SKILL.md)); all require a configured parts catalog.
- Not provided: PDF/image/HTML rendering, page layout, `.io`, `.lxf`, full
  LPub grammar, `BUFEXCHG`, automatic camera selection.

## 1.4 → 1.5 (report-oriented APIs)

```python
from ldraw import CancellationToken, LDrawCapability, prepare_catalog

token = CancellationToken()
result = prepare_catalog(
    capabilities=(LDrawCapability.CATALOG,),
    on_progress=lambda event: print(
        event.stage, event.current, event.total, event.unit
    ),
    cancellation=token,
)
parts = result.parts
```

```python
from ldraw import load_model

loaded = load_model("model.mpd", parts=parts)
if loaded.model is not None:
    analysis = loaded.analyze(parts)
    print(analysis.summary, analysis.bom, analysis.instruction_steps)
```

| New | Notes |
|---|---|
| `prepare_catalog()` | One pass; returns state, `CatalogBuildReport`, diagnostics. Generated modules checked only with `LDrawCapability.GENERATED_MODULES` |
| `ProgressUnit`, `CancellationToken`, `OperationCancelled` | Progress units and cancellation |
| `load_model()` → `ModelLoadResult(model, diagnostics, complete)` | Tolerant; `read_model`/`parse_model` stay strict |
| `ModelAnalysis`, `ModelSummary.from_occurrences()`, `bill_of_materials(occurrences=...)` | Reuse occurrences |
| `PartsCatalog.search()`, `PartMetadata` (catalog schema v6) | Search and header metadata |
| `Parts.library_root`, `parts.inspect_part()`, `parts.geometry(code)`, `inspect_model()` | Exact geometry and diagnostics |
| `ModelOccurrence.path` | Root-to-leaf placements with source model, reference, line, steps |
| `discover_libraries()`, `inspect_library()`, `plan_download()`, `download(..., resume=True, cancellation=token)` | First-run setup |
| `render_capabilities()`, `render_preview()` | Optional LDView/LeoCAD previews; `refresh=True` bypasses cache |

Behaviour notes:

- `iter_ldr_issues()` reports unreadable files as `IO_READ_FAILED` instead of
  raising, in source-line order; `iter_ldr_issues(loaded)` never rereads.
- `Parts.bounding_box()` / `parts.geometry()` report unreadable files via
  `NoGeometryError` and diagnostics instead of `OSError`/`UnicodeError`.
- `OperationCancelled` derives from `Exception`, not `RuntimeError`.
- All validation codes are `DiagnosticCode` members.

## 1.5 → 1.6 (typed connections)

Adds `ConnectionFeature`, `ConnectionKind`/`Role`/`Source`, profiles,
`connections_compatible()`, `connection_residual()`, `snap_transform()`,
`Parts.connections(code)`, `Parts.connection_metadata(code)`, LDCad shadow
and Studio sources, `ModelInspection.connection_contacts()` /
`connection_graphs()` / `snap_candidates()`. Details:
[connections](../connections/SKILL.md).

**`stud_contacts(*, tolerance=0.1, probe_distance=0.1)` is now strict**
(same signature, different results):

- Candidates need stud-receptacle evidence; studs on plain tiles or merely
  overlapping AABBs no longer count. Counts can drop.
- Sideways/averted studs rejected; axes anti-parallel within 2 degrees.
- At most one contact per stud feature and candidate occurrence.
- `tolerance` is now a residual cap; `probe_distance` a minimum penetration.
  Values are not comparable across versions.
- `StudContact` gains `stud_feature`, `receptacle_feature`, `residual`;
  results sorted by occurrence indices and feature IDs.

Other behaviour notes:

- `PartGeometry` gained `connections` (between `studs` and `diagnostics`) and
  a trailing `connection_metadata`. Construct it with keywords.
- Unsupported/invalid inline `SNAP_*` records make
  `PartGeometry.complete == False`; CLI exit codes unaffected.
- First geometry query per part reads the file twice.
- `Matrix.inverse()` is new; raises `numpy.linalg.LinAlgError` if singular.
- `from ldraw import *` adds ~40 connection names; check for shadowing.
- `Parts.get` memoization key includes `connection_shadows=` /
  `studio_metadata=` sources.

## 1.6 → 1.7 (connection fixes, HTTPX2)

No public API removed; no new required arguments. No cache rebuild needed;
call `clear_part_geometry_cache()` only if you hold one in process.

**Downloads use `httpx2>=2.13.1`.** Catch `httpx2.HTTPError` from
`ldraw.download()` (`httpx2.HTTPStatusError` for status failures).
`ensure_library()` still wraps failures in `RuntimeError`.

**Stud receptacles move onto the mating grid.** Plain stacks now confirm:

```python
from ldraw import inspect_model, load_model, prepare_catalog

parts = prepare_catalog().parts
model = load_model("stack.ldr").model  # two Brick 2 x 4 stacked squarely
report = inspect_model(model, parts=parts)

len(report.stud_contacts())  # 1.6.0: 0    1.7.0: 8
len(report.connection_graphs().confirmed.edges)  # 1.6.0: 0    1.7.0: 8
```

- Open tubes (`stud4`) add four diagonal corner sockets at ±10 LDU plus a
  centre socket; solid tubes (`stud3`) add four axial neighbours at ±20 LDU
  and lose the centre.
- Sockets sit at the far end of the tube (the underside face), so
  `snap_transform()` mates flush.
- Derived sockets: `name == "Stud Socket"`, `feature_id` suffix
  `:socket:<±x><±z>`, `provenance` ends with `"derived:stud-socket"`.
- Replace matching by `feature_id == "stud4"`, `"Stud Tube Solid"` or one
  receptacle per tube with `"derived:stud-socket" in feature.provenance`.
- Overrides under mirrored/sheared placements are rejected with
  `connection.invalid_transform`; degenerate placements yield no sockets.
- New: `ldraw.connection_types.METADATA_SOURCES` (not re-exported from
  `ldraw`).
- `bom`, `validate`, `parts`, parsing and serialization are untouched.

## Source docs

Verbatim copies, for details not covered above:

- [upgrading-1.1/index.md](references/upgrading-1.1-index.md)
- [upgrading-1.2/index.md](references/upgrading-1.2-index.md)
- [upgrading-1.3/index.md](references/upgrading-1.3-index.md)
- [upgrading-1.4/index.md](references/upgrading-1.4-index.md)
- [upgrading-1.5/index.md](references/upgrading-1.5-index.md)
- [upgrading-1.6/index.md](references/upgrading-1.6-index.md)
- [upgrading-1.7/index.md](references/upgrading-1.7-index.md)
