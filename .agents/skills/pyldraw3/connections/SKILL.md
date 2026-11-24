---
name: connections
description: 'Typed part connectivity in pyldraw3: ConnectionKind/Role/Freedom vocabulary, ConnectionFeature queries from the catalog, LDCad shadow (LDCadShadowLibrary) and Studio connectivity sources, authoritative metadata configuration, stud_contacts(), ConnectionContact, typed contacts and connection multigraphs, stud receptacles on the mating grid and derived sockets, diagnostics and caching. Use when detecting which parts are attached (studs, pins, axles, clips, hinges), loading LDCad shadow metadata, or interpreting connection results and diagnostics.'
---

# Connections

Find out which parts in a model are attached and how. pyldraw3 gives parts
typed connection features: studs, stud receptacles, bars, clips, pins, pin holes,
axles, axle holes, hinges, rim seats, tyre beads and generic interfaces. It
matches them into typed contacts, connection multigraphs and ranked snap
suggestions. The features come from heuristics, connector primitives, inline
`!LDCAD` records, LDCad shadow libraries, Studio connectivity exports and
explicit overrides. This skill covers the subsystem as of 1.6 and the fixes
made in 1.7.

The root skill covers library setup, `prepare_catalog()` and loading models.
For full signatures, see [api-reference](../api-reference/SKILL.md).

## Quick start: which parts are attached

```python
from ldraw import inspect_model, load_model, prepare_catalog

parts = prepare_catalog().parts
model = load_model("stack.ldr").model  # two Brick 2 x 4 stacked squarely
report = inspect_model(model, parts=parts)

len(report.stud_contacts())  # 1.6.0: 0    1.7.0: 8
len(report.connection_graphs().confirmed.edges)  # 1.6.0: 0    1.7.0: 8
```

In 1.7, each of those eight contacts has a residual `distance` of `0.0`.

Walk the confirmed graph:

```python
from ldraw import inspect_model

inspection = inspect_model(model, parts)
graphs = inspection.connection_graphs()

for edge in graphs.confirmed.edges:
    print(edge.first, edge.second, edge.first_feature_id, edge.second_feature_id)
```

## Vocabulary

`ConnectionFeature` is the central type. Its fields:

| Field | Meaning |
|----|----|
| `kind` | `ConnectionKind` (stud, stud_receptacle, axle, clip, ...) |
| `role` | `ConnectionRole.MALE` / `FEMALE` / `NEUTRAL` |
| `position`, `frame` | Local position and orthonormal frame. The **+Y column is the feature axis**. X/Z keep cross-section roll, which matters for axles and clips. |
| `profile` | Shape profile (a tagged union, see below) |
| `feature_id` | Stable ID |
| `freedoms` | Allowed motions: rotate, slide, discrete rotate, free rotate |
| `source` | Evidence source, a `ConnectionSource` |
| `confidence` | In `[0, 1]` |
| `occupied` / `occupied_by` | Occupancy |
| `connection_provenance` | Source, path, archive member, line number, command, include chain |

Profiles:

- `CylindricalProfile`: one or more `CylindricalSection`s (round, axle or
  square, optionally flexible), plus `centered`, `friction` and `caps`.
- `FingerProfile`: hinge finger sequence, radius, first finger role, detents.
- `AnnularProfile`: radius, width and offset, for rim seats and tyre beads.
- `GenericProfile`: a named interface with optional `GenericBounds` (point,
  box, cylinder, sphere), a `match` mode and an `aligned`/`free` placement.

All connection enums are `StrEnum`s. Serialized values are the lowercase member
strings (`"stud"`, `"ldcad_shadow"`, `"confirmed"`, ...).

The top-level helpers:

| Helper | Purpose |
|----|----|
| `connections_compatible()` | Can two features mate? It allows the fixed pairs stud/stud-receptacle, bar/clip, pin/pin-hole, axle/axle-hole and rim-seat/tyre-bead, plus hinge/hinge and generic/generic. It checks role, group, occupancy and radius tolerance. |
| `connection_residual()` | Centerline distance, axial gap, and angular/roll alignment |
| `angular_alignment_within()` | Converts a dot-product alignment to a degree tolerance |
| `snap_transform()` | The placement that mates one feature to another |

`ldraw.connection_types.METADATA_SOURCES` (new in 1.7) is a
`frozenset[ConnectionSource]` of the four authored sources: `LDCAD_INLINE`,
`LDCAD_SHADOW`, `STUDIO` and `OVERRIDE`. It is not re-exported from `ldraw`:

```python
from ldraw.connection_types import METADATA_SOURCES

authored = [f for f in features if f.source in METADATA_SOURCES]
```

## Query features from the catalog

```python
from ldraw import prepare_catalog

prepared = prepare_catalog()
parts = prepared.parts

for feature in parts.connections("3001"):
    print(feature.kind, feature.role, feature.position, feature.source)

report = parts.connection_metadata("3001")
print(report.coverage, report.source_count, report.diagnostics)
```

`connections()` returns the `features` part of the full report.
`ConnectionMetadataReport` holds the part code, a coverage grade, the
features, and per-source counts: `source_count`, `recognized_record_count`,
`unsupported_record_count`, `invalid_record_count` and `diagnostics`.

| `ConnectionMetadataCoverage` | Meaning |
|----|----|
| `COMPLETE` | Clean authoritative metadata was processed, including an explicit clear-to-empty document |
| `PARTIAL` | Relies on primitive/heuristic evidence, or recovered around unsupported or invalid records |
| `NONE` | Neither metadata nor connector primitives were found |

Wheels and tyres: `parts.tyre_rim_compatibility` returns `PartCompatibility`
rows, built from official shortcut descriptions. For lookups, use
`parts.compatible_tyres(rim_code)` and `parts.compatible_rims(tyre_code)`. If
a shortcut assembles a rim with its tyre, the matching rim-seat and tyre-bead
features are marked `occupied`.

Other entry points: `PartGeometry.connections`, and `part_connections()` and
`clear_part_geometry_cache()` in `ldraw.part_geometry`.

## Configure authoritative metadata

Register sources when you prepare the catalog:

```python
from ldraw import prepare_catalog

prepared = prepare_catalog(
    connection_shadows=("LDCadShadowLibrary.csl",),
    studio_metadata=("studio-connectivity.json",),
)
parts = prepared.parts
report = parts.connection_metadata("32000")
print(report.coverage, report.source_count, report.diagnostics)
```

`LDrawSession.prepare_catalog()`, `catalog.load_parts()`, `Parts.get()` and
`Parts.fresh()` take the same keywords. Both default to empty.

To change an existing `Parts` instance:

| Method | Effect |
|----|----|
| `add_connection_shadow(source)` / `clear_connection_shadows()` | LDCad shadow sources |
| `add_studio_metadata(source)` / `clear_studio_metadata()` | Studio sources |
| `set_connection_overrides(code, features, replace_existing=False)` | Per-part overrides. By default they add to the existing features. `replace_existing=True` discards every lower-priority feature for that part. |
| `clear_connection_overrides(code=None)` | Remove overrides |

### Fold order and precedence

Sources are folded in this fixed order:

1. connector primitives collected during geometry traversal;
2. conservative description/bounds heuristics and official wheel/tyre shortcuts;
3. inline `!LDCAD SNAP_*` records in the part file itself;
4. registered LDCad shadow sources, in registration order;
5. registered Studio sources, in registration order;
6. `Parts.set_connection_overrides()`.

Two rules apply during the fold:

- **Between metadata sources, feature IDs decide replacement, not shared
  position.** A later feature with the same (case-insensitive) ID replaces the
  earlier one and emits a `connection.feature_conflict` warning. Features with
  different IDs may coexist at the same location.
- **Authoritative metadata supersedes inference.** If inline LDCad, shadow,
  Studio or override data survives the fold, any heuristic-, primitive- or
  shortcut-sourced feature for the *same interface* is dropped. Same interface
  means the same kind, a colocated position and a parallel axis. The IDs do
  not need to match. In 1.7, metadata that matches **any** interface of a tube
  resolves that tube's whole socket set. Metadata that clears all features, or
  an override that replaces them, discards the deferred candidates.

`SNAP_CLEAR [id=...]` targets the raw `metadata_id`. A `SNAP_CLEAR` without an
ID applies at its exact position in the stream: it wipes the features
accumulated so far, including pending targeted clears.

## LDCad shadow sources

`LDCadShadowLibrary` accepts a shadow directory, a ZIP file, or an LDCad `.csl`
archive (a CSL is a ZIP).

- All three use the same case-insensitive resolver over `parts/`, `parts/s/`,
  `p/`, `p/8/` and `p/48/`. A bare code tries `parts/<code>.dat`, then
  `p/<code>.dat`.
- A missing source raises `FileNotFoundError` when you register it. A file
  that is not a ZIP raises `zipfile.BadZipFile`.
- If an archive has duplicate logical names, the first member wins.

| Record | Options |
|----|----|
| `SNAP_CLEAR` | `id` |
| `SNAP_INCL` | `id`, `ref` (required), `pos`, `ori`, `scale`, `grid`, `slide` |
| `SNAP_CYL` | `id`, `group`, `pos`, `ori`, `scale`, `mirror`, `gender`, `secs` (required), `caps`, `grid`, `center`, `slide` |
| `SNAP_CLP` | `id`, `group`, `pos`, `ori`, `radius`, `length`, `center`, `slide`, `scale`, `mirror`, `gender` |
| `SNAP_FGR` | `id`, `group`, `pos`, `ori`, `genderofs`, `gender`, `seq` (required), `radius`, `center`, `scale`, `mirror` |
| `SNAP_GEN` | `id`, `group`, `pos`, `ori`, `gender`, `bounding`, `scale`, `mirror`, `match`, `placement` |

- `SNAP_CYL` maps to an axle, stud, bar or pin kind, based on its sections,
  label and gender.
- `SNAP_CLP` is always a female clip. `SNAP_FGR` gives a hinge with a finger
  profile. `SNAP_GEN` gives a generic feature.
- `ori` must be orthonormal with a positive determinant. Express mirroring with
  the `mirror` option, not the orientation.
- A `grid` copies the feature once per cell.
- `SNAP_INCL` resolves `ref` across the whole registered shadow registry, so
  an include in one archive can reach a document in another. It transforms the
  included features without placement inheritance, assigns them to the
  including part, and records the nesting path in the provenance
  `include_chain`. Unresolvable references and include cycles are diagnosed.
- Parsing is tolerant. An unknown `SNAP_*` record or option key gives a warning
  diagnostic and is skipped. Geometry is never aborted.

For direct use, `ldraw.connection_metadata` exports `parse_ldcad_text()`,
`parse_ldcad_commands()`, `metadata_report()` and the `ShadowConnectionResult`
accumulator. `LDCadShadowLibrary.connections_for()` returns the same shape.
The source docs do not give the signatures of these functions.

## Studio connectivity sources

`StudioConnectionLibrary` reads Studio connectivity JSON with this shape:
`{"parts": [{"part_id": ..., "connections": [...]}]}`.

- Each connection row accepts `id`, `type`, `position`, `axis`, `gender`,
  `group`, `radius`, `length` and `width`.
- The recognized types are `stud`, `pin`/`technic_pin`, `axle`, `bar`, `clip`,
  `hinge`, `tyre_rim`, `ball`/`ball_joint` and `turntable`.
- Unknown fields are excluded with a warning. An unknown type makes the row
  invalid.
- Studio features have `source="studio"` and confidence 0.95.

Limitations:

- Studio data has no cross-section roll, so the frame comes from the axis
  alone.
- Profiles have a single section.
- There is no support for grids, includes, clears, or scale or mirror
  inheritance.
- An empty `connections` list adds no authoritative evidence. Primitive and
  heuristic features survive, and coverage does not change. To clear a part's
  features, use LDCad `SNAP_CLEAR` or
  `set_connection_overrides(..., replace_existing=True)`.

## Typed contacts, graphs and snaps

`inspect_model()` attaches world-space features to every resolved occurrence
(`OccurrenceGeometry.connections`). `ModelInspection` has three methods for
them.

### `connection_contacts(*, tolerance=0.25, angular_tolerance=2.0)`

This method matches compatible feature pairs through a deterministic spatial
index. It returns `ConnectionContact` values. Each one holds:

- the two occurrences and the two features;
- a `ConnectionResidual`: centerline `distance`, `axial_gap`, angular
  `alignment` and `roll_alignment`, plus `entry_face_gap` and `penetration`
  for stud matches;
- a `ConnectionStatus`. A contact that involves a heuristic-sourced feature is
  `POTENTIAL`. Every other source gives `CONFIRMED`.

Stud matching is strict. A male stud is confirmed only when all of these hold:

- the candidate part has stud-receptacle evidence;
- the axes are anti-parallel within the angular tolerance;
- the stud's base lies on the candidate's oriented entry face;
- the stud penetrates inward.

Two overlapping surfaces are not a stud connection. Half-offset studs and
studs touching a wall are rejected.

### `connection_graphs()`

This method returns `ConnectionGraphs`, a pair of `ConnectionMultigraph`s:

- Both graphs share one zero-based tuple of occurrence nodes. It covers
  *every* occurrence. Unresolved occurrences are isolated nodes.
- Parallel feature contacts stay as parallel edges. Edges carry feature-ID
  strings (an empty string when a feature has no ID), the status and the
  residual.
- `confirmed` is the subset of `optimistic` whose edges are `CONFIRMED`.
- `optimistic` adds only contacts that involve heuristic features. It does not
  add generic AABB surface edges or component analysis.

### `snap_candidates(moving, *, fixed=None, limit=None)`

`moving` is an occurrence object or index. The method ranks compatible feature
pairings by residual and returns `SnapCandidate` values. Each `transform` is
the world-space `SnapTransform` (position and matrix) that would mate the
moving part:

```python
best = inspection.snap_candidates(moving=2, limit=3)
for candidate in best:
    print(candidate.fixed_occurrence.index, candidate.transform.position)
```

## `stud_contacts()`

`stud_contacts(*, tolerance=0.1, probe_distance=0.1)` is the convenient
stud-only view. Since 1.6, it projects the strict typed stud matches above.
Use `connection_contacts()` for all connection types.

- A candidate occurrence must have stud-receptacle evidence. A stud pressed
  against a plain tile does not count, and neither do two overlapping AABBs.
- The axes must be anti-parallel within 2 degrees. The checks for the
  oriented entry face and inward penetration reject sideways or averted studs.
- It reports at most one contact per stud feature and candidate occurrence.
  The best receptacle wins.
- `tolerance` is the residual cap: centerline distance, axial gap,
  entry-face gap and lateral slack. `probe_distance` is the minimum
  penetration depth. These values are not comparable with 1.5.
- `StudContact.position` is the position of the matched feature.
  `StudContact.stud` is the nearest qualifying `StudReference`. The optional
  fields are `stud_feature`, `receptacle_feature` and `residual`.
- Results are sorted by occurrence indices and feature IDs.

## Stud receptacles and derived sockets (1.7)

When a part is resolved, each tube receptacle expands into the sockets a stud
can actually enter. The sockets replace the feature on the tube's centreline:

- An **open tube** (the `stud4` family, whose description contains `open`)
  gets its four diagonal grid corners at ±10 LDU, **plus** a socket on its own
  centreline for half-offset "jumper" mounts.
- A **solid tube** (the `stud3` family) gets its four axial neighbours at
  ±20 LDU and **loses** its centreline feature.
- Sockets sit at the **far end of the transformed tube primitive**, which is
  the tube's opening. They are not at the tube's centre or on the face of the
  part's bounding box. As a result, `snap_transform()` mates a stud flush with
  the part.

| Part | 1.7.0 receptacles |
|----|----|
| `3001` Brick 2 x 4 | 3 × `Stud Tube Open` + 8 × `Stud Socket` at `y = 24` |
| `3020` Plate 2 x 4 | 3 × `Stud Tube Open` + 8 × `Stud Socket` |
| `3022` Plate 2 x 2 | 1 × `Stud Tube Open` + 4 × `Stud Socket` |
| `3710` Plate 1 x 4 | 4 × `Stud Socket` (no solid centres) |
| `3623` Plate 1 x 3 | 3 × `Stud Socket` |
| `3068b` Tile 2 x 2 | 1 × `Stud Tube Open` + 4 × `Stud Socket` |

**Recognize a derived socket.** A derived socket is `replace()`d from its
tube. It keeps the tube's `kind`, `role`, `axis`, `profile`, `source`,
`confidence` and `owner_code`, and changes three fields:

- `name` becomes the literal `"Stud Socket"`;
- `feature_id` gets a `:socket:<±x><±z>` suffix, for example
  `s/3001s01@R0/stud4@R0/stud4:socket:+1-1`;
- `provenance` gets a trailing `"derived:stud-socket"` entry.

An open tube's centre socket keeps the primitive's header description
(`Stud Tube Open`) and its original `feature_id`. It also gets the
`"derived:stud-socket"` entry. When a solid tube's centre feature is emitted at
all, its `feature_id` gets the suffix `:opening`. To find derived sockets, test
`"derived:stud-socket" in feature.provenance`. Do not match on
`feature_id == "stud4"` or `"Stud Tube Solid"`, and do not assume one
receptacle per tube.

**Grid validation.** A candidate socket is accepted only when its position
lands on a phase of the part's own top-stud grid. Positions are reduced modulo
the 20 LDU pitch, using studs whose axis opposes the socket's. This keeps
sockets off the outside of walls.

- If an incomplete grid rejects a candidate (stud-group primitives and
  subparts see only a slice of the part), the candidate is **deferred**. It is
  absent from `connections()`. It is carried up through the enclosing geometry,
  transformed by the child's complete placement, including scale. The parent's
  grid then reconsiders it.
- Only a **catalog part** may fall back to filtering by lateral bounds (4 LDU
  margin). This handles studless undersides such as tiles. If bounds filtering
  rejects every offset candidate, a solid tube contributes nothing. An open
  tube still keeps its centre socket.
- If two sockets contest a cell (within 0.5 LDU and aligned to 0.999), the one
  with higher confidence wins. Ties go to the tube's own opening over a derived
  neighbour, then to emission order. An existing non-derived receptacle with
  positive confidence holds its cell. A zero-confidence one (a placeholder
  primitive) competes as a candidate.

**Placements that invalidate features.**

- Features from `OVERRIDE`, `LDCAD_INLINE`, `LDCAD_SHADOW` and `STUDIO` are
  rejected, not just downgraded, under a mirrored, sheared or otherwise
  disallowed placement. Each rejection is reported as a
  `connection.invalid_transform` warning.
- If a placement leaves a tube's frame non-orthonormal (singular, collapsed,
  or scaled off the grid unit), that tube contributes nothing, not even its
  centre socket. These candidates are dropped, not deferred.
- If a placement degrades socket evidence from positive to zero confidence,
  the evidence is dropped with its own `connection.invalid_transform` warning.

## Diagnostics

All connection metadata problems are `Severity.WARNING` diagnostics with
stable codes. Parsing recovers and geometry is never aborted.

| `DiagnosticCode` member | Value | Meaning |
|----|----|----|
| `CONNECTION_UNSUPPORTED_RECORD` | `connection.unsupported_record` | `SNAP_*` record type not implemented |
| `CONNECTION_UNSUPPORTED_OPTION` | `connection.unsupported_option` | Option key not allowed for the record; excluded Studio field |
| `CONNECTION_INVALID_OPTION_VALUE` | `connection.invalid_option_value` | Malformed option syntax or value; unreadable/invalid document |
| `CONNECTION_MISSING_REQUIRED_OPTION` | `connection.missing_required_option` | `SNAP_INCL` without `ref`, `SNAP_CYL` without `secs`, `SNAP_FGR` without `seq` |
| `CONNECTION_INCLUDE_NOT_FOUND` | `connection.include_not_found` | `SNAP_INCL` reference unresolvable |
| `CONNECTION_INCLUDE_CYCLE` | `connection.include_cycle` | `SNAP_INCL` recursion |
| `CONNECTION_FEATURE_CONFLICT` | `connection.feature_conflict` | Later source replaced a same-ID feature with different content |
| `CONNECTION_INVALID_TRANSFORM` | `connection.invalid_transform` | Non-orthonormal/singular/mirroring orientation or bad scale |
| `CONNECTION_INVALID_GRID` | `connection.invalid_grid` | Malformed `[grid=...]` specification |

`DiagnosticCode.CONNECTION_METADATA_INVALID` is only an attribute alias of
`CONNECTION_INVALID_OPTION_VALUE`. It does not appear when you iterate
`DiagnosticCode`, and `DiagnosticCode("connection.metadata_invalid")` raises
`ValueError`. Match on `connection.invalid_option_value`.

If a part has an unsupported or invalid inline `SNAP_*` record, it carries
warnings and reports `PartGeometry.complete == False`. `ModelInspection.complete`
and the `inspect` JSON `complete` field inherit this. CLI exit codes depend
only on error severity.

## Caching and invalidation

- `Parts.get` memoizes instances. The key includes every registered connection
  source: file sources by size and modification time, and directory sources by
  the root's modification time, size, device and inode. It does not walk
  descendants.
- A wholesale replacement of a shadow directory, or a touched file source, is
  picked up automatically. A nested edit that leaves the root directory's
  metadata unchanged is not. After a nested edit, call `Parts.fresh(...)` or
  `Parts.clear_cache()`.
- `add_connection_shadow()`, `add_studio_metadata()`,
  `set_connection_overrides()` and every `clear_*` method invalidate that
  instance's derived geometry caches. They also drop all memoized `Parts`
  instances process-wide.
- No cached artifact stores connection features. Upgrading from 1.6 to 1.7
  needs no rebuild. If you hold the in-process geometry cache across the
  upgrade, call `clear_part_geometry_cache()`.
- The first geometry query for each part reads the part file a second time to
  collect inline metadata. If the file becomes unreadable between the two
  reads, the query raises instead of degrading to a diagnostic.

## Pitfalls

- Construct `PartGeometry` with keyword arguments. `connections` sits between
  `studs` and `diagnostics`, and `connection_metadata` is the last field.
- `from ldraw import *` brings in about forty connection names. Check for
  name shadowing.
- `StudContact` equality, `repr` and tuple forms include the three optional
  fields.

## CLI

Repeat `--ldcad-shadow PATH` and `--studio-metadata PATH` on `parts geometry`
or `inspect`. The command reports a bad path on stderr and exits 1 before the
catalog loads.

- `parts geometry --format json` adds `connection_count`, `connections` and
  `connection_metadata`. The table format prints a `connections:` line.
- `inspect --format json` adds top-level `connection_contacts` and
  `connection_graphs`, and per-occurrence `connection_count`, `connections`
  and `connection_metadata`. Each `stud_contacts` entry gets `stud_feature`,
  `receptacle_feature` and `residual`. The table format prints a
  `connection contacts:` line.
- Only error-severity diagnostics make `inspect` fail.

See [cli](../cli/SKILL.md) for the rest of the CLI.

To check the pinned LDCad shadow corpus (commit
`15aa1e718b6a8da37d24fc7af5e52e262c041bfb`; pass `--source PATH` to use an
existing checkout), run the following. It exits nonzero on command or option
forms that pyldraw3 does not recognize:

```
uv run python scripts/check_ldcad_shadow_corpus.py
```

## Source docs

Verbatim copies, for details not covered above:

- [upgrading-1.6/index.md](references/upgrading-1.6-index.md)
- [upgrading-1.7/index.md](references/upgrading-1.7-index.md)
