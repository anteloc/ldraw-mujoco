---
name: api-reference
description: 'Full generated reference of the public `ldraw` API (ldraw.__all__): signatures, fields and docstrings of classes such as Model, ModelOccurrence, Parts, PartsCatalog, Piece, Matrix, Vector, Colour, LDrawSession, ConnectionFeature, ConnectionContact, StudContact, Diagnostic, InstructionBuilder, and functions such as load_model, parse_model, model_bounds, part_bounding_box, part_studs, connections_compatible, snap_transform, ensure_library, validate helpers and bill_of_materials. Use when an exact signature, field, enum value or return type is needed.'
---

# pyldraw3 API Reference

A compact map of the public `ldraw` API (`ldraw.__all__`). Use it to find a
signature, field, enum value or return type quickly. The reference is
generated from `ldraw.__all__` using type annotations and docstrings. The
generated `ldraw.library.*` modules are not part of it, because they depend
on the LDraw release you downloaded. In a consuming project, run
`ldraw generate` and `ldraw stubs` to get imports and type stubs for that
release.

Signatures below are copied from the generated reference, with their line
breaks collapsed. For every field and docstring, read the verbatim API
reference doc listed with this skill's sources. For concepts and workflows,
see the [root skill](../SKILL.md) and the task skills. For connections, see
[connections](../connections/SKILL.md).

## Models and occurrences

| Name | Signature / fields |
|----|----|
| `read_model` | `read_model(path: Path \| str) -> Model` |
| `load_model` | `load_model(path: Path \| str, parts: Parts \| None = None, *, tolerant: bool = True) -> ModelLoadResult`. Reads, parses and validates without raising for data failures. |
| `parse_model` | `parse_model(text: str, *, name: str = "", source: Path \| str \| None = None) -> Model`. In an MPD, the first section is the root and later sections are submodels. |
| `parse_model_result` | `parse_model_result(text: str, *, name: str = "", source: Path \| str \| None = None, parts: Parts \| None = None, tolerant: bool = True) -> ModelLoadResult` |
| `ModelLoadResult` | `model: Model \| None`, `diagnostics`, `complete: bool`, `valid: bool` (no error diagnostics). `analyze(parts: Parts \| None = None) -> ModelAnalysis \| None` |
| `analyze_model` | `analyze_model(model: Model, *, parts: Parts \| None = None, diagnostics: Iterable[Diagnostic] = ()) -> ModelAnalysis` |
| `ModelAnalysis` | `occurrences`, `summary: ModelSummary`, `bom: tuple[BomRow, ...]`, `instruction_steps`, `diagnostics`, `inspection: ModelInspection \| None = None` |
| `ModelSummary` | `bounds`, `origin_bounds`, `part_counts: dict[str, int]`, `colour_usage`, `skipped_geometry: tuple[SkippedGeometry, ...]`, `occurrence_count`, `size_ldu`, `size_mm`. Constructors: `from_model(model, parts)`, `from_inspection(inspection)`, `from_occurrences(occurrences, parts)` |

`Model` fields are `name: str = ''`, `objects: list[ParsedObject]` and
`submodels: dict[str, Model]`. Its header properties are `description`,
`header_name`, `author`, `ldraw_org`, `license` and `bfc`. `pieces` holds the
type-1 references. `steps: list[list[Piece]]` holds the pieces grouped by
`0 STEP`. Models compare and hash by identity, so compare content with
`m1.to_ldraw() == m2.to_ldraw()`.

| `Model` method | Signature |
|----|----|
| `from_pieces` | `from_pieces(pieces: Iterable[Piece], *, name: str = "", description: str \| None = None, author: str \| None = None) -> Self` |
| `add` / `add_group` | `add(*objects: ParsedObject) -> None` / `add_group(group: Group) -> None` |
| `set_header` | `set_header(*, description=None, name=None, author=None, ldraw_org=None, license=None) -> None` (each `str \| None`) |
| `add_submodel` | `add_submodel(submodel: Model, *, colour: Colour \| int = MAIN_COLOUR_CODE, position: Vector \| None = None, matrix: Matrix \| None = None) -> Piece`. Raises `DuplicateSubmodelError` if a different model is already registered under the name. |
| `submodel_for` | `submodel_for(piece: Piece) -> Model \| None` |
| `submodel_view` | `submodel_view(name: str) -> Model`. References resolve against the root. Raises `UnknownSubmodelError`. |
| `add_step` / `add_rotation_step` / `end_rotation_steps` | `add_rotation_step(x: float, y: float, z: float, *, mode: RotationMode \| str = "REL") -> None` |
| `iter_pieces` | `iter_pieces() -> Iterator[Piece]`. Recursive, expanding submodels. |
| `iter_occurrences` | `iter_occurrences(*, expand_submodels: bool = True, include_steps: bool = True) -> Iterator[ModelOccurrence]` |
| `find_pieces` | `find_pieces(*, part: str \| None = None, colour: Colour \| int \| None = None, recursive: bool = False) -> list[Piece]` |
| `bill_of_materials` | `bill_of_materials(*, parts: Parts \| None = None) -> list[BomRow]` |
| `instruction_document` / `iter_instruction_steps` | `instruction_document(*, parts: Parts \| None = None) -> InstructionDocument` |
| `source_line_for` | `source_line_for(obj: ParsedObject) -> int \| None` |
| `to_ldraw` / `save` | `to_ldraw() -> str` / `save(path: Path \| str) -> None` |

| Class | Fields |
|----|----|
| `ModelOccurrence` | `piece`, `part_code`, `reference`, `colour`, `position`, `matrix`, `source_model`, `source_line`, `step` (effective, inherited), `source_step` (local), `path: tuple[OccurrencePathItem, ...] = ()`. Compares by identity. |
| `OccurrencePathItem` | `model`, `piece`, `source_line`, `local_step`, `effective_step`, `step` (alias of `local_step`) |
| `OccurrenceAttribution` | `index`, `occurrence`, `model_path`, `reference_path`, `source_line_path`, `local_step_path`, `effective_step_path`, `page_path`, `step_path` (alias), `installation_page`, `source_page` |

## Building blocks

| Name | Signature / fields |
|----|----|
| `Piece` | Fields: `part: str`, `suffix`, `colour: Colour`, `position: Vector`, `matrix: Matrix`, `group: Group \| None = None`. Property `reference` (e.g. `3001.dat`). `to_ldraw() -> str` |
| `Piece.place` | `place(part: str, *, colour: Colour \| int = MAIN_COLOUR_CODE, position: Vector \| None = None, matrix: Matrix \| None = None, group: Group \| None = None, suffix: str = DEFAULT_SUFFIX) -> Self` |
| `Group` | `position: Vector`, `matrix: Matrix`, `pieces: list[Piece]`. Methods: `to_ldraw()`, `add_piece(piece)`, `remove_piece(piece)`, `copy() -> Self` |
| `Vector` | `x`, `y`, `z: Number`. Methods: `copy()`, `cross(other) -> Vector`, `dot(other) -> float`, `normalized() -> Vector`. Property `repr` |
| `Identity` | `Identity() -> Matrix` |
| `XAxis`, `YAxis`, `ZAxis` | Axis types (bases: `Axis`) |
| `Person` | Minifigure builder: `head`, `hat`, `torso`, `backpack`, `hips_and_legs`, `hips`, `left_arm`/`right_arm`, `left_hand`/`right_hand`, `left_hand_item`/`right_hand_item`, `left_leg`/`right_leg`, `left_shoe`/`right_shoe`. Each returns a `Piece` (`Piece \| None` for items and shoes). |

`Matrix` is a 3x3 transformation matrix. Its methods:

| Method | Signature |
|----|----|
| `rotation` | `rotation(*, x: Number = 0, y: Number = 0, z: Number = 0, units: type[AngleUnits] = Degrees) -> Self` |
| `rotate` | `rotate(angle: Number, axis: type[Axis], units: type[AngleUnits] = Degrees) -> Matrix` |
| `scale` | `scale(sx: Number, sy: Number, sz: Number) -> Matrix` |
| `transpose`, `inverse`, `copy` | `inverse()` raises for a singular matrix |
| `det` | `det() -> float` |
| `is_singular` / `is_orthonormal` | `(*, tolerance: float = 1e-06) -> bool` |
| `flatten` | `flatten() -> tuple[float, ...]`, row-major |
| `rows`, `fix_diagonal() -> bool` | |

Constants: `STUD_PITCH = 20`, `PLATE_HEIGHT = 8`, `BRICK_HEIGHT = 24` and
`LDU_TO_MM = 0.4`.

## Colours

`Colour` is a dataclass with `code: int | None`, `name`, `rgb` (canonicalized
to `#RRGGBB`; a malformed value raises `ValueError`), `alpha` and
`colour_attributes: list[str] | None`. Its properties are `is_solid`,
`is_transparent`, `display_label`, `swatch_rgb` and `swatch_alpha`. A bare
`Colour(code=...)` reads as solid. To judge the real palette entry, look the
code up in `Parts.colours_by_code`. To get catalog metadata, use
`Parts.resolve_colour(colour: Colour | int) -> Colour`.

`Parts.ColourAttributes` is `("CHROME", "PEARLESCENT", "RUBBER",
"MATTE_METALLIC", "METAL", "GLITTER", "SPECKLE", "LUMINANCE")`.

## Parts and catalog

`Parts` is the part catalog loader. Its lookup dicts are `by_name`, `by_code`,
`by_code_name`, `by_category`, `primitives_by_name`, `primitives_by_code`,
`colours`, `alpha_values`, `colour_attributes`, `colours_by_name` and
`colours_by_code`. Its properties are `library_root`, `catalog: PartsCatalog`
and `tyre_rim_compatibility`.

| `Parts` method | Signature |
|----|----|
| `get` / `fresh` | `get(parts_lst: str \| Path, *, tree_fingerprint: str \| None = None, parts_lst_md5: str \| None = None, connection_shadows: Iterable[str \| Path] = (), studio_metadata: Iterable[str \| Path] = ()) -> Parts`. `fresh` has the same signature. |
| `clear_cache` | `clear_cache() -> None` |
| `from_catalog` / `adopt_catalog` | `from_catalog(parts_lst: str \| Path, catalog: PartsCatalog) -> Parts` / `adopt_catalog(catalog) -> None` |
| `build_catalog` | `build_catalog(*, on_progress: ProgressCallback \| None = None, cancellation: CancellationToken \| None = None) -> PartsCatalog` |
| `load` | `load() -> None`. Cheap passes only. Categorization runs lazily. |
| `part` / `find_part` | `part(description: str \| None = None, code: str \| None = None) -> Part`. Raises `PartNotFoundError`. `find_part` returns `None` instead. |
| `description_for` | `description_for(code: str) -> str \| None` |
| `get_entry_by_code` / `get_entry_by_description` | `-> CatalogEntry \| None` |
| `entries_by_category` | `entries_by_category(category: PartCategory) -> tuple[CatalogEntry, ...]` |
| `minifig_entries` | `minifig_entries(section: MinifigSection \| None = None) -> tuple[CatalogEntry, ...]` |
| `get_category` | `get_category(part_description: str) -> PartCategory \| None` |
| `section_find` | `section_find(pieces: list[str]) -> tuple[str, str]` |
| `inspect_part` | `inspect_part(code: str, *, include_geometry: bool = True, recursive_references: bool = False) -> PartInspection` |
| `references_for` | `references_for(code: str, *, recursive: bool = False) -> tuple[PartReference, ...]` |

| Class | Key members |
|----|----|
| `PartsCatalog` | `by_code`, `by_description`, `by_category`, `by_minifig_section`, `add(entry)`, `get_entry_by_code`, `get_entry_by_description`, `entries_by_category`, `minifig_entries`, `module_sections()` |
| `PartsCatalog.search` | `search(query: str, *, within: Iterable[CatalogEntry] \| None = None, fields: Iterable[CatalogSearchField] = ALL_CATALOG_SEARCH_FIELDS, limit: int \| None = None) -> tuple[CatalogEntry, ...]`. Every token must match. |
| `CatalogEntry` | `code`, `description`, `category: PartCategory`, `part`, `minifig_section`, `keywords`, `metadata: PartMetadata \| None`. Also `symbol_name`, `module_path`, `import_statement()` |
| `PartMetadata` | `description`, `name`, `author`, `author_username`, `file_kind: PartFileKind`, `origin: LibraryOrigin`, `qualifiers`, `release`, `license`, `bfc: BfcCertification`, `history: tuple[PartHistoryEntry, ...]`, `category`, `keywords`, `status: PartStatus`, `replacement`, `preview: PreviewTransform \| None`. Also `to_dict()` and `from_dict(value)` |
| `PartInspection` | `code`, `entry`, `path`, `metadata`, `references`, `geometry`, `diagnostics`, `complete` |
| `PartReference` | `parent_code`, `code`, `reference`, `kind: PartReferenceKind`, `description`, `colour`, `position`, `matrix`, `depth` |
| `PartHistoryEntry` / `PreviewTransform` | `date`, `contributor`, `text`, `raw` / `colour_code`, `position`, `matrix` |

Generated-library helpers:

- `symbol_name(entry) -> str`
- `symbol_name_for_description(description) -> str`
- `symbol_description(description) -> str` (drops the `Minifig` prefix)
- `module_path(entry) -> str | None`
- `suggested_import(entry) -> str | None`

| Enum | Values |
|----|----|
| `CatalogSearchField` | `CODE`, `DESCRIPTION`, `CATEGORY`, `KEYWORD`. `ALL_CATALOG_SEARCH_FIELDS = tuple(CatalogSearchField)` |
| `PartCategory` | The official LDraw.org list, from `ANIMAL='animal'` to `ZNAP='znap'`, plus `OTHER`. Multi-word values use spaces (`'minifig accessory'`). Has `module_name` and `from_label(label)`. |
| `MinifigSection` | `HATS`, `HEADS`, `TORSOS`, `HIPS`, `LEGS`, `ARMS`, `HANDS`, `ACCESSORIES`. Has `marker` |
| `PartFileKind` | `PART`, `SUBPART`, `PRIMITIVE`, `PRIMITIVE_8='8_primitive'`, `PRIMITIVE_48='48_primitive'`, `SHORTCUT`, `UNKNOWN` |
| `PartReferenceKind` | `PART`, `SUBPART`, `PRIMITIVE`, `UNKNOWN` |
| `PartStatus` | `CURRENT`, `ALIAS`, `MOVED`, `OBSOLETE` |
| `LibraryOrigin` | `OFFICIAL`, `UNOFFICIAL`, `UNKNOWN` |
| `BfcCertification` | `CCW`, `CW`, `NOCERTIFY`, `UNKNOWN` |

## Geometry and bounds

| Name | Signature / fields |
|----|----|
| `Parts.geometry` | `geometry(code: str) -> PartGeometry` |
| `Parts.bounding_box` / `part_bounding_box` | `bounding_box(code: str) -> BoundingBox` / `part_bounding_box(parts: _PartGeometryLibrary, code: str) -> BoundingBox`. Both raise `PartNotFoundError` and `NoGeometryError`. |
| `Parts.studs` / `part_studs` | `studs(code: str) -> tuple[StudReference, ...]` / `part_studs(parts, code)`. These include underside tubes. |
| `Parts.stud_positions` | `stud_positions(code: str) -> tuple[Vector, ...]`, top studs only |
| `model_bounds` | `model_bounds(model: Model, parts: Parts) -> BoundingBox \| None` |
| `bounds_gap` | `bounds_gap(left: BoundingBox, right: BoundingBox) -> BoundsGap` |
| `inspect_model` | `inspect_model(model: Model, parts: Parts, *, occurrences: Iterable[ModelOccurrence] \| None = None, page_marker_prefix: str = DEFAULT_PAGE_MARKER_PREFIX) -> ModelInspection` |
| `BoundingBox` | `min`, `max: Vector` (Y points down, so `min.y` is the top), `size`, `corners()` |
| `BoundsGap` | `axes: Vector`, `distance: float`, `intersects: bool` |
| `PartGeometry` | `code`, `description`, `bounds`, `points`, `studs`, `connections = ()`, `diagnostics = ()`, `connection_metadata = None`, `complete`, `top_studs`, `receptacles`. Construct it with keywords. |
| `StudReference` | `name` (casefolded stem), `description`, `position`, `up = Vector(0, -1, 0)`, `is_receptacle`, `is_placeholder`, `is_top_stud` |
| `ModelInspection` | `bounds`, `occurrences: tuple[OccurrenceGeometry, ...]`, `skipped_geometry`, `diagnostics`, `occurrence_count`, `complete` |
| `ModelInspection.contact_gaps` | `contact_gaps(*, minimum_gap: float = 5.0, chronological: bool = False) -> tuple[OccurrenceContact, ...]` |
| `OccurrenceGeometry` | `attribution`, `local: PartGeometry`, `bounds`, `studs`, `connections = ()`, `occurrence`, `index` |
| `OccurrenceContact` | `subject`, `nearest`, `gap: BoundsGap` |
| `SkippedOccurrenceGeometry` / `SkippedGeometry` | `attribution`, `diagnostic`, `reason` / `part`, `source_model`, `source_line`, `reason` |

## Connections

| Name | Signature |
|----|----|
| `Parts.connections` | `connections(code: str) -> tuple[ConnectionFeature, ...]` |
| `Parts.connection_metadata` | `connection_metadata(code: str) -> ConnectionMetadataReport` |
| `Parts.add_connection_shadow` / `clear_connection_shadows` | `add_connection_shadow(source: str \| Path) -> None` |
| `Parts.add_studio_metadata` / `clear_studio_metadata` | `add_studio_metadata(source: str \| Path) -> None` |
| `Parts.set_connection_overrides` | `set_connection_overrides(code: str, features: Iterable[ConnectionFeature], *, replace_existing: bool = False) -> None` |
| `Parts.clear_connection_overrides` | `clear_connection_overrides(code: str \| None = None) -> None` |
| `Parts.compatible_tyres` / `compatible_rims` | `compatible_tyres(rim_code: str) -> tuple[str, ...]` / `compatible_rims(tyre_code: str)` |
| `ModelInspection.stud_contacts` | `stud_contacts(*, tolerance: float = 0.1, probe_distance: float = 0.1) -> tuple[StudContact, ...]` |
| `ModelInspection.connection_contacts` | `connection_contacts(*, tolerance: float = 0.25, angular_tolerance: float = 2.0) -> tuple[ConnectionContact, ...]` |
| `ModelInspection.connection_graphs` | `connection_graphs(*, tolerance: float = 0.25, angular_tolerance: float = 2.0) -> ConnectionGraphs` |
| `ModelInspection.snap_candidates` | `snap_candidates(moving: OccurrenceGeometry \| int, *, fixed: OccurrenceGeometry \| int \| None = None, limit: int \| None = None) -> tuple[SnapCandidate, ...]` |
| `connections_compatible` | `connections_compatible(left: ConnectionFeature, right: ConnectionFeature, *, radius_tolerance: float = 0.35) -> bool` |
| `connection_residual` | `connection_residual(left: ConnectionFeature, right: ConnectionFeature) -> ConnectionResidual` |
| `angular_alignment_within` | `angular_alignment_within(alignment: float, tolerance_degrees: float) -> bool` |
| `snap_transform` | `snap_transform(moving: ConnectionFeature, target: ConnectionFeature) -> SnapTransform` |
| `LDCadShadowLibrary.connections_for` | `connections_for(code: str, *, siblings: tuple[ShadowLibrarySources, ...] = ()) -> ShadowConnectionResult` |
| `StudioConnectionLibrary.connections_for` | `connections_for(code: str) -> ShadowConnectionResult` |

`ConnectionFeature` fields: `kind`, `role`, `position: Vector`,
`frame: Matrix` (local +Y is the axis), `profile: ConnectionProfile`,
`name = ''`, `feature_id = None`, `group = None`, `freedoms = frozenset()`,
`source = ConnectionSource.PRIMITIVE`, `confidence = 1.0`, `owner_code`,
`compatible_parts = ()`, `occupied = False`, `occupied_by`,
`provenance = ()`, `metadata_id`, `connection_provenance`,
`scale_inheritance = 'yandr'` and `mirror_inheritance = 'none'`. Its
properties are `axis`, `radial`, `length`, `centered` and `axial_midpoint`.
It has the method `transformed(*, position: Vector, matrix: Matrix,
inherit: bool = True) -> ConnectionFeature`.

| Class | Fields |
|----|----|
| `ConnectionContact` | `first_occurrence`, `second_occurrence`, `first`, `second`, `residual`, `status = ConnectionStatus.CONFIRMED` |
| `ConnectionResidual` | `distance`, `axial_gap`, `alignment`, `roll_alignment = 1.0`, `entry_face_gap = None`, `penetration = None` |
| `ConnectionGraphs` / `ConnectionMultigraph` | `confirmed`, `optimistic` / `nodes: tuple[int, ...]`, `edges` |
| `ConnectionGraphEdge` | `first: int`, `second: int`, `first_feature_id`, `second_feature_id`, `status`, `residual` |
| `StudContact` | `stud_occurrence`, `supported_occurrence`, `stud: StudReference`, `position`, `stud_feature`, `receptacle_feature`, `residual` (the last three default to `None`) |
| `SnapCandidate` / `SnapTransform` | `moving_occurrence`, `fixed_occurrence`, `moving`, `fixed`, `transform`, `residual` / `position`, `matrix` |
| `ConnectionMetadataReport` | `part_code`, `coverage`, `features`, `source_count`, `recognized_record_count`, `unsupported_record_count`, `invalid_record_count`, `diagnostics` |
| `ConnectionProvenance` | `source`, `path`, `archive_member`, `line_number`, `command`, `include_chain = ()` |
| `PartCompatibility` | `first`, `second`, `relation`, `source`, `evidence = None` |
| `CylindricalProfile` | `sections`, `centered = True`, `friction = False`, `caps = CylindricalCaps.NONE`, `length`, `primary_shape`, `mating_radius`, `scaled(*, radial, axial)` |
| `CylindricalSection` | `shape: SectionShape`, `radius`, `length`, `flexible = False` |
| `FingerProfile` | `sequence`, `radius`, `first_role = ConnectionRole.MALE`, `detents = ()`, `centered = True`, `length` |
| `AnnularProfile` | `radius`, `width`, `offset = 0.0`, `length` |
| `GenericProfile` | `name`, `length = 0.0`, `bounds: GenericBounds \| None`, `match = GenericMatch.SHAPE`, `placement = GenericPlacement.ALIGNED` |
| `GenericBounds` | `kind: GenericBoundsKind`, `dimensions = ()` |

Every profile and section has `scaled(*, radial: float, axial: float)`.

| Enum (`StrEnum`) | Values |
|----|----|
| `ConnectionKind` | `STUD`, `STUD_RECEPTACLE`, `BAR`, `CLIP`, `PIN`, `PIN_HOLE`, `AXLE`, `AXLE_HOLE`, `HINGE`, `RIM_SEAT`, `TYRE_BEAD`, `GENERIC` |
| `ConnectionRole` | `MALE`, `FEMALE`, `NEUTRAL` |
| `ConnectionFreedom` | `ROTATE`, `SLIDE`, `DISCRETE_ROTATE`, `FREE_ROTATE` |
| `ConnectionSource` | `HEURISTIC`, `PRIMITIVE`, `SHORTCUT`, `LDCAD_INLINE`, `LDCAD_SHADOW`, `STUDIO`, `OVERRIDE` |
| `ConnectionStatus` | `CONFIRMED`, `POTENTIAL` |
| `ConnectionMetadataCoverage` | `COMPLETE`, `PARTIAL`, `NONE` |
| `CylindricalCaps` | `NONE`, `ONE`, `TWO`, `A`, `B` |
| `SectionShape` | `ROUND`, `AXLE`, `SQUARE` |
| `GenericBoundsKind` | `POINT`, `BOX`, `CYLINDER`, `SPHERE` |
| `GenericMatch` / `GenericPlacement` | `SHAPE`, `SIZE`, `GROUP` / `ALIGNED`, `FREE` |

Each value is the lowercase member name, for example `STUD_RECEPTACLE = 'stud_receptacle'`.

## Instructions

| Name | Signature / fields |
|----|----|
| `InstructionBuilder` | `step()`, `rotation_step(x, y, z, *, mode: RotationMode = RotationMode.RELATIVE)`, `end_rotation()`, `note(text)`, `arrow(start: Vector, end: Vector, *, label: str \| None = None)`, `highlight(piece)`, `page_break(*, offset: tuple[float, float] \| None = None)`, `suppress_step()` |
| `InstructionBuilder.set_camera` | `set_camera(camera: CameraState, *, scope: InstructionScope = InstructionScope.LOCAL, context: CameraContext = CameraContext.ASSEMBLY) -> None` |
| Context managers | `callout(*, mode: CalloutMode = CalloutMode.ASSEMBLED)`, `multi_step()`, `ignore(target: InventoryTarget)` |
| `InstructionDocument` | `root`, `sections`, `orphan_sections`, `model`, `parts`. `from_model(model: Model, *, parts: Parts \| None = None) -> InstructionDocument`, `section(name: str) -> InstructionSection` |
| `InstructionSection` | `name`, `is_root`, `reachable`, `references`, `steps`, `model` |
| `InstructionStep` | `number`, `section_name`, `objects`, `added_pieces`, `directives`, `rotation: RotationStep \| None`, `camera: CameraState`, `callouts`, `multi_step_group`, `page_break_before`, `suppressed`, `source_start_line`, `source_end_line`, `cumulative_pieces`, `cumulative_objects`, `source_line_for(obj)` |
| `InstructionStep` occurrences | `added_occurrences(*, expand_submodels: bool = True)` and `cumulative_occurrences(...)`, both `-> tuple[ModelOccurrence, ...]` |
| `InstructionStep` BOM | `added_bill_of_materials(*, parts: Parts \| None = None, expand_submodels: bool = True, respect_lpub: bool = True) -> list[BomRow]`. `cumulative_bill_of_materials` takes the same arguments. |
| `iter_instruction_issues` | `iter_instruction_issues(document: InstructionDocument, *, max_parts: int \| None = None) -> Iterator[InstructionIssue]` |
| `InstructionIssue` | `section`, `line_number`, `code: str`, `message`, `severity = Severity.ERROR` |
| `CameraState` | `angles`, `angle_preset`, `position`, `target`, `up_vector`, `distance`, `fov`, `name`, `orthographic`, `z_near`, `z_far` (all default to `None`). `merged(override: CameraState) -> CameraState` |
| `RotationStep` | `mode`, `angles`, `command_matrix`, `effective_matrix`, `source_line = None` |
| `RotationMode` | `RELATIVE='REL'`, `ADDITIVE='ADD'`, `ABSOLUTE='ABS'`, `END='END'` |

## BOM and inventory

| Name | Signature |
|----|----|
| `bill_of_materials` | `bill_of_materials(model: _ModelLike \| None = None, *, parts: Parts \| None = None, occurrences: Iterable[ModelOccurrence] \| None = None) -> list[BomRow]` |
| `BomRow` | `part`, `description`, `colour_code`, `colour_name`, `quantity`. `to_dict()` |
| `rows_to_csv` / `rows_to_json` | `(rows: Iterable[BomRow]) -> str` |
| `read_inventory` | `read_inventory(path: str \| Path, *, columns: Mapping[str, str] \| None = None, colour_map: Mapping[str, str \| int] \| None = None) -> list[BomRow]` |
| `compare_inventory` | `compare_inventory(model: _ModelLike, expected: Iterable[BomRow], *, part_aliases: Mapping[str, str] \| None = None, parts: Parts \| None = None) -> InventoryComparison` |
| `InventoryComparison` | `differences`, `matched`, `to_dict()` |
| `InventoryDifference` | `part`, `colour`, `expected`, `actual`, `missing`, `extra`, `to_dict()` |
| `comparison_to_csv` | `comparison_to_csv(comparison: InventoryComparison) -> str` |

## Validation and diagnostics

| Name | Signature / fields |
|----|----|
| `iter_ldr_issues` | `iter_ldr_issues(path: Path \| ModelLoadResult, parts: Parts \| None = None) -> Iterator[ValidationIssue]`. Issues come in line order, with file-level issues first. |
| `Diagnostic` | `line_number = None`, `message = ''`, `severity = Severity.ERROR`, `code: DiagnosticCode \| str = DiagnosticCode.GENERIC`, `path`, `section`, `offending_value`, `suggestions = ()`, `cause`. `to_dict() -> dict[str, Any]` |
| `ValidationIssue` | `ValidationIssue = Diagnostic` |
| `Severity` | `ERROR`, `WARNING` |

Diagnostic equality and hashing compare only `line_number`, `message` and
`severity`. To deduplicate across files, key on
`(diagnostic.path, diagnostic.code, diagnostic.line_number, diagnostic.message)`.

The `DiagnosticCode` values use dotted names:

| Family | Values |
|----|----|
| General and catalog | `generic`, `catalog.library_missing`, `catalog.index_missing`, `catalog.index_stale`, `catalog.index_unreadable`, `catalog.persist_failed`, `generation.failed` |
| IO and parse | `io.read_failed`, `io.decode_failed`, `parse.invalid_line`, `parse.invalid_numeric`, `parse.invalid_colour` |
| MPD | `mpd.misplaced_nofile`, `mpd.content_after_nofile`, `mpd.duplicate_section`, `mpd.unresolved_submodel`, `mpd.cycle` |
| Model | `model.unknown_part`, `model.unknown_colour`, `model.legacy_colour`, `model.singular_matrix`, `model.non_orthonormal_matrix`, `model.unknown_meta`, `model.non_finite_numeric`, `model.duplicate_placement` |
| Part and geometry | `part.not_found`, `part.header_invalid`, `part.reference_unresolved`, `part.reference_cycle`, `geometry.incomplete` |
| Connection | `connection.unsupported_record`, `connection.unsupported_option`, `connection.invalid_option_value` (`CONNECTION_METADATA_INVALID` is an alias), `connection.missing_required_option`, `connection.include_not_found`, `connection.include_cycle`, `connection.feature_conflict`, `connection.invalid_transform`, `connection.invalid_grid` |
| Setup and render | `discovery.invalid_library`, `download.plan_failed`, `download.integrity_failed`, `render.unavailable`, `render.failed` |

The member names are the upper-case form of the value: `MODEL_UNKNOWN_PART`
for `model.unknown_part`, `CATALOG_INDEX_STALE` for `catalog.index_stale`, and
so on.

Errors:

- `PartNotFoundError` has `code`, `path`, `message`, `source` and
  `line_number`.
- `NoGeometryError` has `code`, `message`, `source` and `line_number`.
- `UnknownSubmodelError` has `message`, `source` and `line_number`.

All three have the bases `PartError` and the method
`add_context(*, source: str, line_number: int) -> Self`. `OperationCancelled`
derives from `Exception`, not `RuntimeError`.

## Session, setup and library

| Name | Signature |
|----|----|
| `ensure_library` | `ensure_library(config: Config \| None = None, *, version: str = COMPLETE_VERSION, write_config: bool = False, config_file: str \| Path \| None = None, force_generate: bool = False, on_progress: ProgressCallback \| None = None, cancellation: CancellationToken \| None = None) -> LDrawSession` |
| `prepare_catalog` | `prepare_catalog(config: Config \| None = None, *, capabilities: Iterable[LDrawCapability] = (LDrawCapability.CATALOG,), connection_shadows: Iterable[str \| Path] = (), studio_metadata: Iterable[str \| Path] = (), force: bool = False, on_progress: ProgressCallback \| None = None, cancellation: CancellationToken \| None = None) -> CatalogPreparationResult` |
| `download` | `download(*, show_progress: bool = True, version: str = COMPLETE_VERSION, on_progress: ProgressCallback \| None = None, resume: bool = False, cancellation: CancellationToken \| None = None) -> str` |
| `plan_download` | `plan_download(version: str = COMPLETE_VERSION, *, cache_path: str \| Path \| None = None, cancellation: CancellationToken \| None = None) -> DownloadPlan` |
| `generate` | `generate(config: Config, *, force: bool = False, on_progress: ProgressCallback \| None = None, fingerprint: str \| None = None, cancellation: CancellationToken \| None = None) -> None` |
| `discover_libraries` | `discover_libraries(paths: Iterable[str \| Path] \| None = None, *, on_progress=None, cancellation=None) -> tuple[LibraryInspection, ...]` |
| `inspect_library` | `inspect_library(path: str \| Path) -> LibraryInspection` |

`LDrawSession` has `config`, defaulting to `Config.load()`, and `paths:
LDrawPaths`. Its methods:

- `state(*, capabilities=None, fingerprint=None) -> LDrawState`
- `load() -> Parts`
- `prepare_catalog(...)`, the same as the function minus `config`, plus
  `fingerprint: CatalogFingerprint | None = None`
- `rebuild_index(*, force: bool = True, on_progress=None, cancellation=None,
  fingerprint=None) -> Parts`
- `open_model(path) -> Model`
- `load_model(path, parts=None, *, tolerant=True) -> ModelLoadResult`

| Class | Fields |
|----|----|
| `Config` | `ldraw_library_path`, `generated_path`. `load(config_file=None) -> Config` raises `ConfigLoadError`. `to_dict()`, `write(config_file=None)` |
| `LDrawPaths` | `library_path`, `ldraw_path`, `parts_lst`, `generated_path`, `generated_library`, `generation_hash`, `catalog_db`. `from_config(config)` |
| `LDrawState` | `paths`, `reasons`, `capabilities`, `ready`, `library_available`, `needs_index_rebuild`, `needs_generation` |
| `CatalogPreparationResult` | `parts: Parts \| None`, `initial_state`, `final_state`, `report: CatalogBuildReport`, `diagnostics`, `complete` |
| `CatalogBuildReport` | `library_root`, `index_path`, `fingerprint`, `entry_count`, `outcome: CatalogBuildOutcome`, `persisted` |
| `DownloadPlan` | `version`, `release`, `url`, `archive_path`, `destination`, `download_size`, `cached_bytes`, `resumable`, `cached_archive_valid`, `diagnostics`, `remaining_bytes` |
| `LibraryInspection` | `path`, `ldraw_path`, `release`, `components: tuple[LibraryComponent, ...]`, `diagnostics`, `valid`, `missing_components`, `corrupt_components` |
| `LibraryComponent` | `name`, `path`, `present`, `valid`, `detail = None` |
| `CancellationToken` | `cancelled`, `cancel()`, `raise_if_cancelled()` (raises `OperationCancelled`) |
| `ProgressEvent` | `stage: ProgressStage`, `message`, `current`, `total`, `path`, `unit: ProgressUnit \| None`, `determinate` |

| Enum | Values |
|----|----|
| `LDrawCapability` | `CATALOG='catalog'`, `GENERATED_MODULES='generated-modules'` |
| `LDrawStateReason` | `LIBRARY_MISSING`, `INDEX_MISSING`, `INDEX_STALE`, `INDEX_UNREADABLE`, `GENERATED_LIBRARY_MISSING`, `GENERATED_LIBRARY_STALE`, `GENERATED_LIBRARY_UNREADABLE` (values are hyphenated, e.g. `'index-stale'`) |
| `CatalogBuildOutcome` | `UNAVAILABLE`, `LOADED`, `REBUILT`, `REBUILT_NOT_PERSISTED='rebuilt-not-persisted'` |
| `ProgressStage` | `DOWNLOAD`, `UNPACK`, `PARTS_LIST`, `LIBRARY_GENERATION`, `FINGERPRINT`, `INDEX_LOAD`, `INDEX_REBUILD`, `LIBRARY_DISCOVERY`, `VALIDATION`, `RENDER`, `DONE` (multi-word values are hyphenated, e.g. `'parts-list'`) |
| `ProgressUnit` | `BYTES`, `FILES`, `PARTS`, `STEPS`, `VIEWS` |

## Rendering

| Name | Signature / fields |
|----|----|
| `render_preview` | `render_preview(source: str \| Path, *, view: RenderView = RenderView.ISOMETRIC, size: tuple[int, int] = (800, 600), backend: RenderBackend \| None = None, output: str \| Path \| None = None, cache_path: str \| Path \| None = None, refresh: bool = False, on_progress=None, cancellation=None) -> RenderResult` |
| `render_capabilities` | `render_capabilities() -> tuple[RenderCapability, ...]` |
| `RenderResult` | `source`, `view`, `size`, `backend`, `output: Path \| None`, `cached`, `diagnostics`, `complete` |
| `RenderCapability` | `backend`, `available`, `executable` |
| `RenderBackend` / `RenderView` | `LDVIEW`, `LEOCAD` / `FRONT`, `ISOMETRIC`, `TOP` |

The preview cache key covers the bytes of the top-level source, the renderer
path and the render command. It does not cover referenced files or the
library state. Pass `refresh=True` to re-render.

## Gaps in the generated reference

The reference does not list constructor signatures for `Piece`, `Colour`,
`Vector` or `Matrix`; it gives only their fields and methods. It also does not
define `ProgressCallback`, `ParsedObject`, `Part`, `ConnectionProfile`,
`ShadowConnectionResult`, `CatalogFingerprint`, `InstructionScope`,
`CameraContext`, `CalloutMode` or `InventoryTarget`. Look these up in the
package source rather than guessing.

## Source docs

Verbatim copies, for details not covered above:

- [api/index.md](references/api-index.md)
