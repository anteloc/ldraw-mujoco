[](https://github.com/hbmartin/pyldraw3/edit/main/docs/api/index.md "Edit this page") [](https://github.com/hbmartin/pyldraw3/raw/main/docs/api/index.md "View source of this page")

# API Reference

This reference is generated from `ldraw.__all__` at build time, then rendered from the exported objects' type annotations and docstrings with mkdocstrings.

Generated `ldraw.library.*` modules are intentionally not included because they depend on the locally downloaded LDraw release. Run `ldraw generate` and `ldraw stubs` in consuming projects for release-specific import and type-stub coverage.

## ALL_CATALOG_SEARCH_FIELDS <span class="small">`module-attribute`</span>

    ALL_CATALOG_SEARCH_FIELDS = tuple(CatalogSearchField)

## AnnularProfile <span class="small">`dataclass`</span>

Axisymmetric tyre bead or wheel-rim seat.

### radius <span class="small">`instance-attribute`</span>

    radius: float

### width <span class="small">`instance-attribute`</span>

    width: float

### offset <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    offset: float = 0.0

### length <span class="small">`property`</span>

    length: float

Axial width of the fitted interface.

### scaled

    scaled(*, radial: float, axial: float) -> AnnularProfile

Return this profile under radial and axial scaling.

## BfcCertification

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Back-face-culling certification declared in the header.

### CCW <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CCW = 'ccw'

### CW <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CW = 'cw'

### NOCERTIFY <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    NOCERTIFY = 'nocertify'

### UNKNOWN <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    UNKNOWN = 'unknown'

## BomRow <span class="small">`dataclass`</span>

One line of a bill of materials.

### part <span class="small">`instance-attribute`</span>

    part: str

### description <span class="small">`instance-attribute`</span>

    description: str | None

### colour_code <span class="small">`instance-attribute`</span>

    colour_code: int | None

### colour_name <span class="small">`instance-attribute`</span>

    colour_name: str | None

### quantity <span class="small">`instance-attribute`</span>

    quantity: int

### to_dict

    to_dict() -> dict[str, str | int | None]

Return the row as a plain dict keyed by `BOM_FIELDS`.

## BoundingBox <span class="small">`dataclass`</span>

An axis-aligned box in LDraw units (LDU).

LDraw's Y axis points down, so `min.y` is the highest point of the part (typically the stud tops) and `max.y` the lowest.

### min <span class="small">`instance-attribute`</span>

    min: Vector

### max <span class="small">`instance-attribute`</span>

    max: Vector

### size <span class="small">`property`</span>

    size: Vector

Extent along each axis.

### corners

    corners() -> tuple[Vector, ...]

Return the eight corner points of the box.

## BoundsGap <span class="small">`dataclass`</span>

Non-negative axis and Euclidean separation between two AABBs.

### axes <span class="small">`instance-attribute`</span>

    axes: Vector

### distance <span class="small">`instance-attribute`</span>

    distance: float

### intersects <span class="small">`property`</span>

    intersects: bool

Return whether the two bounds overlap or touch.

## CameraState <span class="small">`dataclass`</span>

Renderer-neutral LPub3D assembly camera state.

### angles <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    angles: tuple[float, float] | None = None

### angle_preset <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    angle_preset: str | None = None

### position <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    position: tuple[float, float, float] | None = None

### target <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    target: tuple[float, float, float] | None = None

### up_vector <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    up_vector: tuple[float, float, float] | None = None

### distance <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    distance: float | None = None

### fov <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    fov: float | None = None

### name <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    name: str | None = None

### orthographic <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    orthographic: bool | None = None

### z_near <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    z_near: float | None = None

### z_far <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    z_far: float | None = None

### merged

    merged(override: CameraState) -> CameraState

Return this state with non-None fields from `override` applied.

## CancellationToken

Thread-safe cancellation token shared by library operations.

### cancelled <span class="small">`property`</span>

    cancelled: bool

Whether cancellation has been requested.

### cancel

    cancel() -> None

Request cancellation; safe to call repeatedly from any thread.

### raise_if_cancelled

    raise_if_cancelled() -> None

Raise `OperationCancelled` when cancellation was requested.

## CatalogBuildOutcome

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

How a catalog preparation obtained its in-memory catalog.

### UNAVAILABLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    UNAVAILABLE = 'unavailable'

### LOADED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LOADED = 'loaded'

### REBUILT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    REBUILT = 'rebuilt'

### REBUILT_NOT_PERSISTED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    REBUILT_NOT_PERSISTED = 'rebuilt-not-persisted'

## CatalogBuildReport <span class="small">`dataclass`</span>

Index work and persistence performed by `prepare_catalog`.

### library_root <span class="small">`instance-attribute`</span>

    library_root: Path

### index_path <span class="small">`instance-attribute`</span>

    index_path: Path

### fingerprint <span class="small">`instance-attribute`</span>

    fingerprint: CatalogFingerprint | None

### entry_count <span class="small">`instance-attribute`</span>

    entry_count: int

### outcome <span class="small">`instance-attribute`</span>

    outcome: CatalogBuildOutcome

### persisted <span class="small">`instance-attribute`</span>

    persisted: bool

## CatalogEntry <span class="small">`dataclass`</span>

Typed catalog entry for one part or primitive.

### code <span class="small">`instance-attribute`</span>

    code: str

### description <span class="small">`instance-attribute`</span>

    description: str

### category <span class="small">`instance-attribute`</span>

    category: PartCategory

### part <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    part: Part | None = None

### minifig_section <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    minifig_section: MinifigSection | None = None

### keywords <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    keywords: tuple[str, ...] = ()

### metadata <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    metadata: PartMetadata | None = None

### symbol_name <span class="small">`property`</span>

    symbol_name: str

Generated Python symbol name for this entry.

### module_path <span class="small">`property`</span>

    module_path: str | None

Generated module path for this entry, if it is importable.

### import_statement

    import_statement() -> str | None

Generated-library import statement for this entry, if available.

## CatalogPreparationResult <span class="small">`dataclass`</span>

Parts plus before/after state and diagnostics from one preparation.

### parts <span class="small">`instance-attribute`</span>

    parts: Parts | None

### initial_state <span class="small">`instance-attribute`</span>

    initial_state: LDrawState

### final_state <span class="small">`instance-attribute`</span>

    final_state: LDrawState

### report <span class="small">`instance-attribute`</span>

    report: CatalogBuildReport

### diagnostics <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...] = ()

### complete <span class="small">`property`</span>

    complete: bool

Whether usable parts were produced without an error diagnostic.

## CatalogSearchField

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Catalog entry fields considered by `PartsCatalog.search`.

### CODE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CODE = 'code'

### DESCRIPTION <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DESCRIPTION = 'description'

### CATEGORY <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CATEGORY = 'category'

### KEYWORD <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    KEYWORD = 'keyword'

## Colour <span class="small">`dataclass`</span>

A colour, identified by a code, or by rgb/alpha for direct colours.

`rgb` is canonicalized on construction to `#RRGGBB` — a leading `#`, six uppercase hex digits — whatever form it was given in; malformed values raise `ValueError`.

### code <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    code: int | None = None

### name <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    name: str | None = None

### rgb <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    rgb: str | None = None

### alpha <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    alpha: int | None = None

### colour_attributes <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    colour_attributes: list[str] | None = None

### is_solid <span class="small">`property`</span>

    is_solid: bool

Whether this colour is plain opaque paint — no alpha, no finish.

Judged from the data on this instance: full alpha (or none given) and no colour attributes (`CHROME`, `GLITTER`, `LUMINANCE`, …). Colours from a parts catalog carry both fields; a bare `Colour(code=...)` placeholder carries neither and so reads as solid — look the code up in `Parts.colours_by_code` to judge the real palette entry.

### display_label <span class="small">`property`</span>

    display_label: str

Human-readable label for UI lists and inspectors.

### swatch_rgb <span class="small">`property`</span>

    swatch_rgb: str | None

RGB hex value suitable for colour swatches, when known.

### swatch_alpha <span class="small">`property`</span>

    swatch_alpha: int

Alpha channel suitable for colour swatches.

### is_transparent <span class="small">`property`</span>

    is_transparent: bool

Whether this colour has a non-opaque alpha value.

## ConnectionContact <span class="small">`dataclass`</span>

Two placed connection features that are aligned and overlapping.

### first_occurrence <span class="small">`instance-attribute`</span>

    first_occurrence: OccurrenceGeometry

### second_occurrence <span class="small">`instance-attribute`</span>

    second_occurrence: OccurrenceGeometry

### first <span class="small">`instance-attribute`</span>

    first: ConnectionFeature

### second <span class="small">`instance-attribute`</span>

    second: ConnectionFeature

### residual <span class="small">`instance-attribute`</span>

    residual: ConnectionResidual

### status <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    status: ConnectionStatus = ConnectionStatus.CONFIRMED

## ConnectionFeature <span class="small">`dataclass`</span>

One physical connection interface in a part's local coordinates.

The feature frame uses local +Y as its axis. The X and Z axes retain cross-section roll, which is significant for Technic axles and clips.

### kind <span class="small">`instance-attribute`</span>

    kind: ConnectionKind

### role <span class="small">`instance-attribute`</span>

    role: ConnectionRole

### position <span class="small">`instance-attribute`</span>

    position: Vector

### frame <span class="small">`instance-attribute`</span>

    frame: Matrix

### profile <span class="small">`instance-attribute`</span>

    profile: ConnectionProfile

### name <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    name: str = ''

### feature_id <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    feature_id: str | None = None

### group <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    group: str | None = None

### freedoms <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    freedoms: frozenset[ConnectionFreedom] = field(
        default_factory=frozenset
    )

### source <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    source: ConnectionSource = ConnectionSource.PRIMITIVE

### confidence <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    confidence: float = 1.0

### owner_code <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    owner_code: str | None = None

### compatible_parts <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    compatible_parts: tuple[str, ...] = ()

### occupied <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    occupied: bool = False

### occupied_by <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    occupied_by: str | None = None

### provenance <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    provenance: tuple[str, ...] = ()

### metadata_id <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    metadata_id: str | None = None

### connection_provenance <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    connection_provenance: ConnectionProvenance | None = None

### scale_inheritance <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    scale_inheritance: str = 'yandr'

### mirror_inheritance <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    mirror_inheritance: str = 'none'

### axis <span class="small">`property`</span>

    axis: Vector

Unit axis, or the zero vector after a degenerate transform.

### radial <span class="small">`property`</span>

    radial: Vector

Unit roll reference, or zero after a degenerate transform.

### length <span class="small">`property`</span>

    length: float

Axial span represented by the profile.

### centered <span class="small">`property`</span>

    centered: bool

Whether the profile spans symmetrically around `position`.

### axial_midpoint <span class="small">`property`</span>

    axial_midpoint: Vector

Center of the feature's axial extent in its coordinate frame.

### transformed

    transformed(
        *,
        position: Vector,
        matrix: Matrix,
        inherit: bool = True,
    ) -> ConnectionFeature

Return this feature transformed by an LDraw placement.

## ConnectionFreedom

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Motion retained after a connection is made.

### ROTATE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ROTATE = 'rotate'

### SLIDE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SLIDE = 'slide'

### DISCRETE_ROTATE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DISCRETE_ROTATE = 'discrete_rotate'

### FREE_ROTATE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FREE_ROTATE = 'free_rotate'

## ConnectionGraphEdge <span class="small">`dataclass`</span>

One typed feature contact between two occurrence nodes.

### first <span class="small">`instance-attribute`</span>

    first: int

### second <span class="small">`instance-attribute`</span>

    second: int

### first_feature_id <span class="small">`instance-attribute`</span>

    first_feature_id: str

### second_feature_id <span class="small">`instance-attribute`</span>

    second_feature_id: str

### status <span class="small">`instance-attribute`</span>

    status: ConnectionStatus

### residual <span class="small">`instance-attribute`</span>

    residual: ConnectionResidual

## ConnectionGraphs <span class="small">`dataclass`</span>

Confirmed and optimistic views of one inspection's connectivity.

### confirmed <span class="small">`instance-attribute`</span>

    confirmed: ConnectionMultigraph

### optimistic <span class="small">`instance-attribute`</span>

    optimistic: ConnectionMultigraph

## ConnectionKind

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Physical interface represented by a connection feature.

### STUD <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    STUD = 'stud'

### STUD_RECEPTACLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    STUD_RECEPTACLE = 'stud_receptacle'

### BAR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    BAR = 'bar'

### CLIP <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CLIP = 'clip'

### PIN <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PIN = 'pin'

### PIN_HOLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PIN_HOLE = 'pin_hole'

### AXLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    AXLE = 'axle'

### AXLE_HOLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    AXLE_HOLE = 'axle_hole'

### HINGE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    HINGE = 'hinge'

### RIM_SEAT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    RIM_SEAT = 'rim_seat'

### TYRE_BEAD <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TYRE_BEAD = 'tyre_bead'

### GENERIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GENERIC = 'generic'

## ConnectionMetadataCoverage

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Completeness of normalized connection metadata for one part.

### COMPLETE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    COMPLETE = 'complete'

### PARTIAL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PARTIAL = 'partial'

### NONE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    NONE = 'none'

## ConnectionMetadataReport <span class="small">`dataclass`</span>

Immutable report for all connection metadata applied to one part.

### part_code <span class="small">`instance-attribute`</span>

    part_code: str

### coverage <span class="small">`instance-attribute`</span>

    coverage: ConnectionMetadataCoverage

### features <span class="small">`instance-attribute`</span>

    features: tuple[ConnectionFeature, ...]

### source_count <span class="small">`instance-attribute`</span>

    source_count: int

### recognized_record_count <span class="small">`instance-attribute`</span>

    recognized_record_count: int

### unsupported_record_count <span class="small">`instance-attribute`</span>

    unsupported_record_count: int

### invalid_record_count <span class="small">`instance-attribute`</span>

    invalid_record_count: int

### diagnostics <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...]

## ConnectionMultigraph <span class="small">`dataclass`</span>

Immutable occurrence multigraph retaining parallel feature edges.

### nodes <span class="small">`instance-attribute`</span>

    nodes: tuple[int, ...]

### edges <span class="small">`instance-attribute`</span>

    edges: tuple[ConnectionGraphEdge, ...]

## ConnectionProvenance <span class="small">`dataclass`</span>

Structured origin of a normalized connection feature.

### source <span class="small">`instance-attribute`</span>

    source: ConnectionSource

### path <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    path: Path | None = None

### archive_member <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    archive_member: str | None = None

### line_number <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    line_number: int | None = None

### command <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    command: str | None = None

### include_chain <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    include_chain: tuple[str, ...] = ()

## ConnectionResidual <span class="small">`dataclass`</span>

Geometric residuals between two compatible features.

### distance <span class="small">`instance-attribute`</span>

    distance: float

### axial_gap <span class="small">`instance-attribute`</span>

    axial_gap: float

### alignment <span class="small">`instance-attribute`</span>

    alignment: float

### roll_alignment <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    roll_alignment: float = 1.0

### entry_face_gap <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    entry_face_gap: float | None = None

### penetration <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    penetration: float | None = None

## ConnectionRole

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Mating role of a feature.

### MALE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MALE = 'male'

### FEMALE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FEMALE = 'female'

### NEUTRAL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    NEUTRAL = 'neutral'

## ConnectionSource

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Evidence from which a connection feature was derived.

### HEURISTIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    HEURISTIC = 'heuristic'

### PRIMITIVE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PRIMITIVE = 'primitive'

### SHORTCUT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SHORTCUT = 'shortcut'

### LDCAD_INLINE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LDCAD_INLINE = 'ldcad_inline'

### LDCAD_SHADOW <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LDCAD_SHADOW = 'ldcad_shadow'

### STUDIO <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    STUDIO = 'studio'

### OVERRIDE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    OVERRIDE = 'override'

## ConnectionStatus

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Confidence tier assigned to a placed feature contact.

### CONFIRMED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONFIRMED = 'confirmed'

### POTENTIAL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    POTENTIAL = 'potential'

## CylindricalCaps

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Blocked ends of an LDCad cylindrical connection profile.

### NONE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    NONE = 'none'

### ONE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ONE = 'one'

### TWO <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TWO = 'two'

### A <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    A = 'a'

### B <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    B = 'b'

## CylindricalProfile <span class="small">`dataclass`</span>

Axial profile composed of round, axle, or square sections.

### sections <span class="small">`instance-attribute`</span>

    sections: tuple[CylindricalSection, ...]

### centered <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    centered: bool = True

### friction <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    friction: bool = False

### caps <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    caps: CylindricalCaps = CylindricalCaps.NONE

### length <span class="small">`property`</span>

    length: float

Total length along the feature axis.

### primary_shape <span class="small">`property`</span>

    primary_shape: SectionShape

Most constraining cross-section in the profile.

### mating_radius <span class="small">`property`</span>

    mating_radius: float

Smallest rigid radius, used for broad compatibility checks.

### scaled

    scaled(
        *, radial: float, axial: float
    ) -> CylindricalProfile

Return this profile under radial and axial scaling.

## CylindricalSection <span class="small">`dataclass`</span>

One axial section of a pin, hole, axle, bar, or clip profile.

### shape <span class="small">`instance-attribute`</span>

    shape: SectionShape

### radius <span class="small">`instance-attribute`</span>

    radius: float

### length <span class="small">`instance-attribute`</span>

    length: float

### flexible <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    flexible: bool = False

### scaled

    scaled(
        *, radial: float, axial: float
    ) -> CylindricalSection

Return this section under radial and axial scaling.

## Diagnostic <span class="small">`dataclass`</span>

One structured problem, warning, or recovery made by an operation.

`line_number` remains the first field so the historical `ValidationIssue(line_number, message, severity)` constructor stays source compatible. New callers should prefer keyword arguments.

Warning: equality and hashing deliberately compare only `line_number`, `message`, and `severity` (historical `ValidationIssue` behavior), so `set`/`dict` deduplication collapses diagnostics that differ only by `code`, `path`, or `section`. To deduplicate diagnostics across files, key on a tuple such as `(diagnostic.path, diagnostic.code, diagnostic.line_number, diagnostic.message)` instead.

### line_number <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    line_number: int | None = None

### message <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    message: str = ''

### severity <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    severity: Severity = Severity.ERROR

### code <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    code: DiagnosticCode | str = field(
        default=DiagnosticCode.GENERIC, compare=False
    )

### path <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    path: Path | None = field(default=None, compare=False)

### section <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    section: str | None = field(default=None, compare=False)

### offending_value <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    offending_value: object | None = field(
        default=None, compare=False
    )

### suggestions <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    suggestions: tuple[str, ...] = field(
        default=(), compare=False
    )

### cause <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    cause: BaseException | None = field(
        default=None, compare=False, repr=False
    )

### to_dict

    to_dict() -> dict[str, Any]

Return a JSON-ready representation, including safe cause details.

`offending_value` passes JSON-native scalars through unchanged; any other value (bytes, matrices, exceptions, ...) is coerced with `repr()` so the result always survives `json.dumps`.

## DiagnosticCode

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Stable codes emitted by PyLDraw report-oriented operations.

### GENERIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GENERIC = 'generic'

### CATALOG_LIBRARY_MISSING <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CATALOG_LIBRARY_MISSING = 'catalog.library_missing'

### CATALOG_INDEX_MISSING <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CATALOG_INDEX_MISSING = 'catalog.index_missing'

### CATALOG_INDEX_STALE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CATALOG_INDEX_STALE = 'catalog.index_stale'

### CATALOG_INDEX_UNREADABLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CATALOG_INDEX_UNREADABLE = 'catalog.index_unreadable'

### CATALOG_PERSIST_FAILED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CATALOG_PERSIST_FAILED = 'catalog.persist_failed'

### GENERATION_FAILED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GENERATION_FAILED = 'generation.failed'

### IO_READ_FAILED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    IO_READ_FAILED = 'io.read_failed'

### IO_DECODE_FAILED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    IO_DECODE_FAILED = 'io.decode_failed'

### PARSE_INVALID_LINE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PARSE_INVALID_LINE = 'parse.invalid_line'

### PARSE_INVALID_NUMERIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PARSE_INVALID_NUMERIC = 'parse.invalid_numeric'

### PARSE_INVALID_COLOUR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PARSE_INVALID_COLOUR = 'parse.invalid_colour'

### MPD_MISPLACED_NOFILE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MPD_MISPLACED_NOFILE = 'mpd.misplaced_nofile'

### MPD_CONTENT_AFTER_NOFILE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MPD_CONTENT_AFTER_NOFILE = 'mpd.content_after_nofile'

### MPD_DUPLICATE_SECTION <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MPD_DUPLICATE_SECTION = 'mpd.duplicate_section'

### MPD_UNRESOLVED_SUBMODEL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MPD_UNRESOLVED_SUBMODEL = 'mpd.unresolved_submodel'

### MPD_CYCLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MPD_CYCLE = 'mpd.cycle'

### MODEL_UNKNOWN_PART <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MODEL_UNKNOWN_PART = 'model.unknown_part'

### MODEL_UNKNOWN_COLOUR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MODEL_UNKNOWN_COLOUR = 'model.unknown_colour'

### MODEL_LEGACY_COLOUR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MODEL_LEGACY_COLOUR = 'model.legacy_colour'

### MODEL_SINGULAR_MATRIX <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MODEL_SINGULAR_MATRIX = 'model.singular_matrix'

### MODEL_NON_ORTHONORMAL_MATRIX <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MODEL_NON_ORTHONORMAL_MATRIX = (
        "model.non_orthonormal_matrix"
    )

### MODEL_UNKNOWN_META <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MODEL_UNKNOWN_META = 'model.unknown_meta'

### MODEL_NON_FINITE_NUMERIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MODEL_NON_FINITE_NUMERIC = 'model.non_finite_numeric'

### MODEL_DUPLICATE_PLACEMENT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MODEL_DUPLICATE_PLACEMENT = 'model.duplicate_placement'

### PART_NOT_FOUND <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PART_NOT_FOUND = 'part.not_found'

### PART_HEADER_INVALID <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PART_HEADER_INVALID = 'part.header_invalid'

### PART_REFERENCE_UNRESOLVED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PART_REFERENCE_UNRESOLVED = 'part.reference_unresolved'

### PART_REFERENCE_CYCLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PART_REFERENCE_CYCLE = 'part.reference_cycle'

### GEOMETRY_INCOMPLETE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GEOMETRY_INCOMPLETE = 'geometry.incomplete'

### CONNECTION_UNSUPPORTED_RECORD <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_UNSUPPORTED_RECORD = (
        "connection.unsupported_record"
    )

### CONNECTION_UNSUPPORTED_OPTION <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_UNSUPPORTED_OPTION = (
        "connection.unsupported_option"
    )

### CONNECTION_INVALID_OPTION_VALUE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_INVALID_OPTION_VALUE = (
        "connection.invalid_option_value"
    )

### CONNECTION_METADATA_INVALID <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_METADATA_INVALID = (
        "connection.invalid_option_value"
    )

### CONNECTION_MISSING_REQUIRED_OPTION <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_MISSING_REQUIRED_OPTION = (
        "connection.missing_required_option"
    )

### CONNECTION_INCLUDE_NOT_FOUND <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_INCLUDE_NOT_FOUND = (
        "connection.include_not_found"
    )

### CONNECTION_INCLUDE_CYCLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_INCLUDE_CYCLE = 'connection.include_cycle'

### CONNECTION_FEATURE_CONFLICT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_FEATURE_CONFLICT = 'connection.feature_conflict'

### CONNECTION_INVALID_TRANSFORM <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_INVALID_TRANSFORM = (
        "connection.invalid_transform"
    )

### CONNECTION_INVALID_GRID <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONNECTION_INVALID_GRID = 'connection.invalid_grid'

### DISCOVERY_INVALID_LIBRARY <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DISCOVERY_INVALID_LIBRARY = 'discovery.invalid_library'

### DOWNLOAD_PLAN_FAILED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DOWNLOAD_PLAN_FAILED = 'download.plan_failed'

### DOWNLOAD_INTEGRITY_FAILED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DOWNLOAD_INTEGRITY_FAILED = 'download.integrity_failed'

### RENDER_UNAVAILABLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    RENDER_UNAVAILABLE = 'render.unavailable'

### RENDER_FAILED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    RENDER_FAILED = 'render.failed'

## DownloadPlan <span class="small">`dataclass`</span>

Network and local-cache facts for a prospective library download.

### version <span class="small">`instance-attribute`</span>

    version: str

### release <span class="small">`instance-attribute`</span>

    release: str | None

### url <span class="small">`instance-attribute`</span>

    url: str

### archive_path <span class="small">`instance-attribute`</span>

    archive_path: Path

### destination <span class="small">`instance-attribute`</span>

    destination: Path

### download_size <span class="small">`instance-attribute`</span>

    download_size: int | None

### cached_bytes <span class="small">`instance-attribute`</span>

    cached_bytes: int

### resumable <span class="small">`instance-attribute`</span>

    resumable: bool

### cached_archive_valid <span class="small">`instance-attribute`</span>

    cached_archive_valid: bool | None

### diagnostics <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...] = ()

### remaining_bytes <span class="small">`property`</span>

    remaining_bytes: int | None

Return the expected remaining transfer size when known.

## FingerProfile <span class="small">`dataclass`</span>

Interlocking hinge fingers arranged along the hinge axis.

### sequence <span class="small">`instance-attribute`</span>

    sequence: tuple[float, ...]

### radius <span class="small">`instance-attribute`</span>

    radius: float

### first_role <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    first_role: ConnectionRole = ConnectionRole.MALE

### detents <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    detents: tuple[float, ...] = ()

### centered <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    centered: bool = True

### length <span class="small">`property`</span>

    length: float

Total finger span along the hinge axis.

### scaled

    scaled(*, radial: float, axial: float) -> FingerProfile

Return this profile under radial and axial scaling.

## GenericBounds <span class="small">`dataclass`</span>

One validated LDCad generic bounding shape.

### kind <span class="small">`instance-attribute`</span>

    kind: GenericBoundsKind

### dimensions <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    dimensions: tuple[float, ...] = ()

### scaled

    scaled(*, radial: float, axial: float) -> GenericBounds

Return the bounds under radial and axial scaling.

## GenericBoundsKind

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Bounding shape used to rank and validate a generic interface.

### POINT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    POINT = 'point'

### BOX <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    BOX = 'box'

### CYLINDER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CYLINDER = 'cylinder'

### SPHERE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SPHERE = 'sphere'

## GenericMatch

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

LDCad matching rule for generic interfaces.

### SHAPE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SHAPE = 'shape'

### SIZE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SIZE = 'size'

### GROUP <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GROUP = 'group'

## GenericPlacement

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Orientation behavior retained by a generic interface.

### ALIGNED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ALIGNED = 'aligned'

### FREE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FREE = 'free'

## GenericProfile <span class="small">`dataclass`</span>

Named interface for shapes which need curated compatibility.

### name <span class="small">`instance-attribute`</span>

    name: str

### length <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    length: float = 0.0

### bounds <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    bounds: GenericBounds | None = None

### match <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    match: GenericMatch = GenericMatch.SHAPE

### placement <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    placement: GenericPlacement = GenericPlacement.ALIGNED

### scaled

    scaled(*, radial: float, axial: float) -> GenericProfile

Return this profile under axial scaling.

## Group <span class="small">`dataclass`</span>

A group of pieces.

### position <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    position: Vector = field(
        default_factory=lambda: Vector(0, 0, 0)
    )

### matrix <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    matrix: Matrix = field(default_factory=Identity)

### pieces <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    pieces: list[Piece] = field(default_factory=list)

### to_ldraw

    to_ldraw() -> str

Serialize all pieces in this group to LDraw lines.

### add_piece

    add_piece(piece: Piece) -> None

Add a piece to the group.

### remove_piece

    remove_piece(piece: Piece) -> None

Remove a piece from the group.

### copy

    copy() -> Self

Return an independent copy of this group with copies of its pieces.

## Identity

    Identity() -> Matrix

Return a transformation matrix representing Identity.

## InstructionBuilder

Write balanced instruction directives into a `Model`.

### model <span class="small">`instance-attribute`</span>

    model = model

### step

    step() -> None

Append a plain LDraw step boundary.

### rotation_step

    rotation_step(
        x: float,
        y: float,
        z: float,
        *,
        mode: RotationMode = RotationMode.RELATIVE,
    ) -> None

Append a rotation-step boundary.

### end_rotation

    end_rotation() -> None

Restore the default instruction view.

### note

    note(text: str) -> None

Append a renderer-neutral textual note.

### arrow

    arrow(
        start: Vector, end: Vector, *, label: str | None = None
    ) -> None

Append a section-local 3D arrow annotation.

### highlight

    highlight(piece: Piece) -> None

Highlight an existing placement using proximity-safe metadata.

### page_break

    page_break(
        *, offset: tuple[float, float] | None = None
    ) -> None

Append an LPub3D page break.

### suppress_step

    suppress_step() -> None

Mark the current step as suppressed in LPub3D.

### set_camera

    set_camera(
        camera: CameraState,
        *,
        scope: InstructionScope = InstructionScope.LOCAL,
        context: CameraContext = CameraContext.ASSEMBLY,
    ) -> None

Append canonical LPub3D camera directives for non-None fields.

### callout

    callout(
        *, mode: CalloutMode = CalloutMode.ASSEMBLED
    ) -> Generator[None, None, None]

Write a balanced LPub3D callout range.

### multi_step

    multi_step() -> Generator[None, None, None]

Write a balanced LPub3D multi-step range.

### ignore

    ignore(
        target: InventoryTarget,
    ) -> Generator[None, None, None]

Write a balanced LPub3D inventory-ignore range.

## InstructionDocument <span class="small">`dataclass`</span>

A sectioned semantic view of an LDraw model's instructions.

### root <span class="small">`instance-attribute`</span>

    root: InstructionSection

### sections <span class="small">`instance-attribute`</span>

    sections: tuple[InstructionSection, ...]

### orphan_sections <span class="small">`instance-attribute`</span>

    orphan_sections: tuple[InstructionSection, ...]

### model <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    model: Model = field(repr=False, compare=False)

### parts <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    parts: Parts | None = field(
        default=None, repr=False, compare=False
    )

### from_model <span class="small">`classmethod`</span>

    from_model(
        model: Model, *, parts: Parts | None = None
    ) -> InstructionDocument

Build a semantic instruction document from `model`.

### section

    section(name: str) -> InstructionSection

Return a reachable section by case-insensitive reference name.

## InstructionIssue <span class="small">`dataclass`</span>

A structural or semantic instruction problem.

### section <span class="small">`instance-attribute`</span>

    section: str

### line_number <span class="small">`instance-attribute`</span>

    line_number: int | None

### code <span class="small">`instance-attribute`</span>

    code: str

### message <span class="small">`instance-attribute`</span>

    message: str

### severity <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    severity: Severity = Severity.ERROR

## InstructionSection <span class="small">`dataclass`</span>

The independent instruction sequence for one model section.

### name <span class="small">`instance-attribute`</span>

    name: str

### is_root <span class="small">`instance-attribute`</span>

    is_root: bool

### reachable <span class="small">`instance-attribute`</span>

    reachable: bool

### references <span class="small">`instance-attribute`</span>

    references: tuple[str, ...]

### steps <span class="small">`instance-attribute`</span>

    steps: tuple[InstructionStep, ...]

### model <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    model: Model = field(repr=False, compare=False)

## InstructionStep <span class="small">`dataclass`</span>

One section-local building step and its effective instruction state.

### number <span class="small">`instance-attribute`</span>

    number: int

### section_name <span class="small">`instance-attribute`</span>

    section_name: str

### objects <span class="small">`instance-attribute`</span>

    objects: tuple[ParsedObject, ...]

### added_pieces <span class="small">`instance-attribute`</span>

    added_pieces: tuple[Piece, ...]

### directives <span class="small">`instance-attribute`</span>

    directives: tuple[InstructionDirective, ...]

### rotation <span class="small">`instance-attribute`</span>

    rotation: RotationStep | None

### camera <span class="small">`instance-attribute`</span>

    camera: CameraState

### callouts <span class="small">`instance-attribute`</span>

    callouts: tuple[InstructionCallout, ...]

### multi_step_group <span class="small">`instance-attribute`</span>

    multi_step_group: int | None

### page_break_before <span class="small">`instance-attribute`</span>

    page_break_before: bool

### suppressed <span class="small">`instance-attribute`</span>

    suppressed: bool

### source_start_line <span class="small">`instance-attribute`</span>

    source_start_line: int | None

### source_end_line <span class="small">`instance-attribute`</span>

    source_end_line: int | None

### cumulative_pieces <span class="small">`property`</span>

    cumulative_pieces: tuple[Piece, ...]

Direct placements accumulated in this section through this step.

### cumulative_objects <span class="small">`property`</span>

    cumulative_objects: tuple[ParsedObject, ...]

Parsed objects accumulated in this section through this step.

### source_line_for

    source_line_for(obj: ParsedObject) -> int | None

Return the source line for one object in this step's section.

### added_occurrences

    added_occurrences(
        *, expand_submodels: bool = True
    ) -> tuple[ModelOccurrence, ...]

Return leaf occurrences added in this step.

### cumulative_occurrences

    cumulative_occurrences(
        *, expand_submodels: bool = True
    ) -> tuple[ModelOccurrence, ...]

Return leaf occurrences accumulated through this step.

### added_bill_of_materials

    added_bill_of_materials(
        *,
        parts: Parts | None = None,
        expand_submodels: bool = True,
        respect_lpub: bool = True,
    ) -> list[BomRow]

Return the parts tray for placements added in this step.

### cumulative_bill_of_materials

    cumulative_bill_of_materials(
        *,
        parts: Parts | None = None,
        expand_submodels: bool = True,
        respect_lpub: bool = True,
    ) -> list[BomRow]

Return the accumulated BOM through this step.

## InventoryComparison <span class="small">`dataclass`</span>

Deterministically ordered inventory differences.

### differences <span class="small">`instance-attribute`</span>

    differences: tuple[InventoryDifference, ...]

### matched <span class="small">`property`</span>

    matched: bool

Whether the model and inventory have identical counts.

### to_dict

    to_dict() -> dict[str, object]

Return the comparison as a JSON-ready object.

## InventoryDifference <span class="small">`dataclass`</span>

A mismatched part/colour count; expected is the inventory quantity.

### part <span class="small">`instance-attribute`</span>

    part: str

### colour <span class="small">`instance-attribute`</span>

    colour: str

### expected <span class="small">`instance-attribute`</span>

    expected: int

### actual <span class="small">`instance-attribute`</span>

    actual: int

### missing <span class="small">`property`</span>

    missing: int

Number of inventory pieces missing from the model.

### extra <span class="small">`property`</span>

    extra: int

Number of model pieces absent from the inventory.

### to_dict

    to_dict() -> dict[str, str | int]

Return counts suitable for JSON and CSV output.

## LDCadShadowLibrary

Bases: `ShadowLibrarySources`

Read unpacked, ZIP, or CSL LDCad shadow metadata.

### source <span class="small">`instance-attribute`</span>

    source = Path(source).expanduser()

### connections_for

    connections_for(
        code: str,
        *,
        siblings: tuple[ShadowLibrarySources, ...] = (),
    ) -> ShadowConnectionResult

Return resolved shadow features for a part or primitive code.

`siblings` is the full ordered registry of shadow libraries used to resolve `SNAP_INCL` references across the merged shadow namespace.

## LDrawCapability

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Configured data capabilities a caller may require.

### CATALOG <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CATALOG = 'catalog'

### GENERATED_MODULES <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GENERATED_MODULES = 'generated-modules'

## LDrawPaths <span class="small">`dataclass`</span>

Resolved filesystem paths for one pyldraw configuration.

### library_path <span class="small">`instance-attribute`</span>

    library_path: Path

### ldraw_path <span class="small">`instance-attribute`</span>

    ldraw_path: Path

### parts_lst <span class="small">`instance-attribute`</span>

    parts_lst: Path

### generated_path <span class="small">`instance-attribute`</span>

    generated_path: Path

### generated_library <span class="small">`instance-attribute`</span>

    generated_library: Path

### generation_hash <span class="small">`instance-attribute`</span>

    generation_hash: Path

### catalog_db <span class="small">`instance-attribute`</span>

    catalog_db: Path

### from_config <span class="small">`classmethod`</span>

    from_config(config: Config) -> Self

Resolve paths from `config`.

## LDrawSession

Manage one configured LDraw catalog and generated library.

### config <span class="small">`instance-attribute`</span>

    config: Config = (
        config if config is not None else Config.load()
    )

### paths <span class="small">`property`</span>

    paths: LDrawPaths

Resolved paths for this session.

### state

    state(
        *,
        capabilities: Iterable[LDrawCapability] | None = None,
        fingerprint: CatalogFingerprint | None = None,
    ) -> LDrawState

Classify only the configured capabilities requested by the caller.

`capabilities=None` (the default) means every capability; an empty iterable raises `ValueError`, matching `prepare_catalog`.

### load

    load() -> Parts

Load parts, building and persisting the catalog index when needed.

### prepare_catalog

    prepare_catalog(
        *,
        capabilities: Iterable[LDrawCapability] = (
            LDrawCapability.CATALOG,
        ),
        connection_shadows: Iterable[str | Path] = (),
        studio_metadata: Iterable[str | Path] = (),
        force: bool = False,
        on_progress: ProgressCallback | None = None,
        cancellation: CancellationToken | None = None,
        fingerprint: CatalogFingerprint | None = None,
    ) -> CatalogPreparationResult

Load or rebuild requested data using one filesystem fingerprint.

`fingerprint` lets a caller reuse an already-computed snapshot to avoid a second parts-tree walk; the caller is then responsible for its freshness — a stale value persists the index under stale keys.

### rebuild_index

    rebuild_index(
        *,
        force: bool = True,
        on_progress: ProgressCallback | None = None,
        cancellation: CancellationToken | None = None,
        fingerprint: CatalogFingerprint | None = None,
    ) -> Parts

Rebuild the persistent catalog index and return the loaded parts.

`fingerprint` lets a caller reuse an already-computed snapshot; the caller is then responsible for its freshness — the rebuilt index is persisted under exactly the keys it carries, so a stale value poisons the index until the next filesystem change.

### open_model

    open_model(path: Path | str) -> Model

Read a `.ldr` or `.mpd` model file.

### load_model

    load_model(
        path: Path | str,
        parts: Parts | None = None,
        *,
        tolerant: bool = True,
    ) -> ModelLoadResult

Read and validate a model into a structured load result.

## LDrawState <span class="small">`dataclass`</span>

Freshness state for a configured LDraw library and generated data.

### paths <span class="small">`instance-attribute`</span>

    paths: LDrawPaths

### reasons <span class="small">`instance-attribute`</span>

    reasons: tuple[LDrawStateReason, ...]

### capabilities <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    capabilities: frozenset[LDrawCapability] = frozenset(
        {
            LDrawCapability.CATALOG,
            LDrawCapability.GENERATED_MODULES,
        }
    )

### ready <span class="small">`property`</span>

    ready: bool

Whether every capability this state was scoped to is fresh.

Only the capabilities in :attr:`capabilities` were classified; unrequested capabilities may still be missing or stale.

### library_available <span class="small">`property`</span>

    library_available: bool

Whether `parts.lst` exists and catalog loading can start.

### needs_index_rebuild <span class="small">`property`</span>

    needs_index_rebuild: bool

Whether loading will need the slow catalog categorization pass.

### needs_generation <span class="small">`property`</span>

    needs_generation: bool

Whether `ldraw.library` should be generated or refreshed.

## LDrawStateReason

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Reasons the configured LDraw data is not fully ready.

### LIBRARY_MISSING <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LIBRARY_MISSING = 'library-missing'

### INDEX_MISSING <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    INDEX_MISSING = 'index-missing'

### INDEX_STALE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    INDEX_STALE = 'index-stale'

### INDEX_UNREADABLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    INDEX_UNREADABLE = 'index-unreadable'

### GENERATED_LIBRARY_MISSING <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GENERATED_LIBRARY_MISSING = 'generated-library-missing'

### GENERATED_LIBRARY_STALE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GENERATED_LIBRARY_STALE = 'generated-library-stale'

### GENERATED_LIBRARY_UNREADABLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GENERATED_LIBRARY_UNREADABLE = (
        "generated-library-unreadable"
    )

## LibraryComponent <span class="small">`dataclass`</span>

Presence and basic readability of one expected library component.

### name <span class="small">`instance-attribute`</span>

    name: str

### path <span class="small">`instance-attribute`</span>

    path: Path

### present <span class="small">`instance-attribute`</span>

    present: bool

### valid <span class="small">`instance-attribute`</span>

    valid: bool

### detail <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    detail: str | None = None

## LibraryInspection <span class="small">`dataclass`</span>

Non-mutating inspection of a possible LDraw installation.

### path <span class="small">`instance-attribute`</span>

    path: Path

### ldraw_path <span class="small">`instance-attribute`</span>

    ldraw_path: Path

### release <span class="small">`instance-attribute`</span>

    release: str | None

### components <span class="small">`instance-attribute`</span>

    components: tuple[LibraryComponent, ...]

### diagnostics <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...] = ()

### valid <span class="small">`property`</span>

    valid: bool

Return whether every required component is present and usable.

### missing_components <span class="small">`property`</span>

    missing_components: tuple[str, ...]

Return names of components that were not found.

### corrupt_components <span class="small">`property`</span>

    corrupt_components: tuple[str, ...]

Return names of present components that failed validation.

## LibraryOrigin

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Whether a header declares official or unofficial library origin.

### OFFICIAL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    OFFICIAL = 'official'

### UNOFFICIAL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    UNOFFICIAL = 'unofficial'

### UNKNOWN <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    UNKNOWN = 'unknown'

## Matrix <span class="small">`dataclass`</span>

A 3x3 transformation matrix.

### rows <span class="small">`property`</span> <span class="small">`writable`</span>

    rows: MatrixRows

Return matrix rows as plain Python lists.

### rotation <span class="small">`classmethod`</span>

    rotation(
        *,
        x: Number = 0,
        y: Number = 0,
        z: Number = 0,
        units: type[AngleUnits] = Degrees,
    ) -> Self

Create an X/Y/Z local-axis rotation, using degrees by default.

Equivalent to `Identity().rotate(x, XAxis).rotate(y, YAxis) .rotate(z, ZAxis)`; matrix composition applies the rightmost rotation to a vector first. Each call owns a new matrix.

### copy

    copy() -> Self

Make a copy of this matrix.

### rotate

    rotate(
        angle: Number,
        axis: type[Axis],
        units: type[AngleUnits] = Degrees,
    ) -> Matrix

Rotate the matrix by an angle around an axis.

### scale

    scale(sx: Number, sy: Number, sz: Number) -> Matrix

Scale the matrix on each axis, applied in the local frame like rotate.

### transpose

    transpose() -> Matrix

Return the transposed matrix.

### inverse

    inverse() -> Matrix

Return the inverse transform, raising for a singular matrix.

### det

    det() -> float

Return the determinant of the matrix.

### is_singular

    is_singular(*, tolerance: float = 1e-06) -> bool

Return whether the matrix flattens geometry (determinant near zero).

### is_orthonormal

    is_orthonormal(*, tolerance: float = 1e-06) -> bool

Return whether the matrix is a pure rotation or reflection.

### flatten

    flatten() -> tuple[float, ...]

Flatten the matrix in row-major order.

### fix_diagonal

    fix_diagonal() -> bool

POV-Ray does not like matrices with zero diagonal elements.

## MinifigSection

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Known minifigure catalog sections.

### HATS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    HATS = 'hats'

### HEADS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    HEADS = 'heads'

### TORSOS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TORSOS = 'torsos'

### HIPS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    HIPS = 'hips'

### LEGS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LEGS = 'legs'

### ARMS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ARMS = 'arms'

### HANDS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    HANDS = 'hands'

### ACCESSORIES <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ACCESSORIES = 'accessories'

### marker <span class="small">`property`</span>

    marker: str

Return the description marker used to infer this section.

## Model <span class="small">`dataclass`</span>

A whole LDraw model, optionally with MPD submodels.

Models compare and hash by identity: their objects contain identity-compared pieces, so field-wise equality would be meaningless. Compare model content with `m1.to_ldraw() == m2.to_ldraw()`.

### name <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    name: str = ''

### objects <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    objects: list[ParsedObject] = field(default_factory=list)

### submodels <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    submodels: dict[str, Model] = field(default_factory=dict)

### description <span class="small">`property`</span>

    description: str | None

The description from the first line, when it is an unmanaged comment.

### header_name <span class="small">`property`</span>

    header_name: str | None

The `0 Name:` header value.

### author <span class="small">`property`</span>

    author: str | None

The `0 Author:` header value.

### ldraw_org <span class="small">`property`</span>

    ldraw_org: str | None

The `0 !LDRAW_ORG` header value.

### license <span class="small">`property`</span>

    license: str | None

The `0 !LICENSE` header value.

### bfc <span class="small">`property`</span>

    bfc: str | None

The `0 BFC` header value.

### pieces <span class="small">`property`</span>

    pieces: list[Piece]

The type-1 subfile references in this model.

### steps <span class="small">`property`</span>

    steps: list[list[Piece]]

Pieces grouped by `0 STEP` markers.

Pieces after the last marker form a final step, so a model without any `0 STEP` lines is a single step. A trailing marker does not produce an empty step. Submodel references are not expanded.

### submodel_for

    submodel_for(piece: Piece) -> Model | None

Resolve a piece's subfile reference to a submodel, if any.

### source_line_for

    source_line_for(obj: ParsedObject) -> int | None

Return the parsed source line for this exact object.

### add

    add(*objects: ParsedObject) -> None

Append parsed objects (pieces, comments, geometry) to the model.

### add_group

    add_group(group: Group) -> None

Append a group's pieces; group transforms apply at serialization.

### from_pieces <span class="small">`classmethod`</span>

    from_pieces(
        pieces: Iterable[Piece],
        *,
        name: str = "",
        description: str | None = None,
        author: str | None = None,
    ) -> Self

Build a model from pieces, optionally with header comments.

### set_header

    set_header(
        *,
        description: str | None = None,
        name: str | None = None,
        author: str | None = None,
        ldraw_org: str | None = None,
        license: str | None = None,
    ) -> None

Set or replace standard header lines at the top of the model.

`ldraw_org` and `license` write the `0 !LDRAW_ORG` and `0 !LICENSE` meta commands, placed after any `Name:`/`Author:` comments in canonical header order.

### add_submodel

    add_submodel(
        submodel: Model,
        *,
        colour: Colour | int = MAIN_COLOUR_CODE,
        position: Vector | None = None,
        matrix: Matrix | None = None,
    ) -> Piece

Register a submodel and append a type-1 piece referencing it.

The submodel's own nested submodels are hoisted into this model's flat mapping, since serialization only walks one level. The same submodel object may be added repeatedly; each call appends another placement piece. A *different* model under an already-registered name still raises `DuplicateSubmodelError`.

### submodel_view

    submodel_view(name: str) -> Model

Return a submodel that resolves references against this root.

Models taken straight from `Model.submodels` have an empty submodel table, so iterating them treats references to sibling submodels as leaf pieces. The returned model shares this root's submodel table instead, making `iter_pieces`, `bill_of_materials`, and `find_pieces(recursive=True)` expand nested references correctly. State reads and writes are forwarded to the selected model; references resolve through the original root. The private adapter inherits the selected class, preserving `isinstance` and custom traversal without copying subclass state. Descriptors bind to the view, with isolated cached properties. Shallow copies keep these bindings; deep copies and pickle preserve them in their copied graphs. View creation skips user subclass hooks.

Raises `UnknownSubmodelError` for a name that is neither this model's nor one of its submodels'.

### add_step

    add_step() -> None

Append a `0 STEP` marker ending the current building step.

### add_rotation_step

    add_rotation_step(
        x: float,
        y: float,
        z: float,
        *,
        mode: RotationMode | str = "REL",
    ) -> None

Append a canonical MLCad `ROTSTEP` instruction boundary.

### end_rotation_steps

    end_rotation_steps() -> None

Append `0 ROTSTEP END` and restore the default instruction view.

### instruction_document

    instruction_document(
        *, parts: Parts | None = None
    ) -> InstructionDocument

Interpret this model and its reachable submodels as instructions.

### iter_instruction_steps

    iter_instruction_steps() -> Iterator[InstructionStep]

Yield this model section's semantic instruction steps.

This convenience method constructs the complete instruction document, including reachable and orphan sections. Callers that need to inspect steps repeatedly should build :meth:`instruction_document` once and reuse its `root.steps` tuple.

### iter_pieces

    iter_pieces() -> Iterator[Piece]

Recursively yield leaf pieces, expanding submodel references.

References are resolved against *this* model's submodel table. A model taken straight from `Model.submodels` has an empty table, so references to sibling submodels are silently yielded as if they were leaf pieces — inspect a submodel through `root.submodel_view(name)` instead.

### iter_occurrences

    iter_occurrences(
        *,
        expand_submodels: bool = True,
        include_steps: bool = True,
    ) -> Iterator[ModelOccurrence]

Yield placed part occurrences with transform and source context.

### bill_of_materials

    bill_of_materials(
        *, parts: Parts | None = None
    ) -> list[BomRow]

Count leaf pieces by part and colour, expanding submodel references.

Colour 16 (the main colour) inside a submodel is resolved to the colour the submodel was placed with. As with `iter_pieces`, submodel references only resolve against this model's own submodel table; to count a single submodel of a larger model, call this on `root.submodel_view(name)`. Built-in expansion skips cyclic references; custom overrides delegating to `super()` inherit that tolerance. Other custom exceptions propagate.

### find_pieces

    find_pieces(
        *,
        part: str | None = None,
        colour: Colour | int | None = None,
        recursive: bool = False,
    ) -> list[Piece]

Return pieces matching the given part code and/or colour.

Part codes are compared case-insensitively.

### to_ldraw

    to_ldraw() -> str

Serialize the model (and any submodels) to LDraw text.

### save

    save(path: Path | str) -> None

Write the model to a file, with a trailing newline.

## ModelAnalysis <span class="small">`dataclass`</span>

Occurrences, statistics, BOM, steps, and diagnostics for one model.

### occurrences <span class="small">`instance-attribute`</span>

    occurrences: tuple[ModelOccurrence, ...]

### summary <span class="small">`instance-attribute`</span>

    summary: ModelSummary

### bom <span class="small">`instance-attribute`</span>

    bom: tuple[BomRow, ...]

### instruction_steps <span class="small">`instance-attribute`</span>

    instruction_steps: tuple[InstructionStep, ...]

### diagnostics <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...]

### inspection <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    inspection: ModelInspection | None = None

## ModelInspection <span class="small">`dataclass`</span>

Exact bounds, resolved occurrences, failures, and source attribution.

### bounds <span class="small">`instance-attribute`</span>

    bounds: BoundingBox | None

### occurrences <span class="small">`instance-attribute`</span>

    occurrences: tuple[OccurrenceGeometry, ...]

### skipped_geometry <span class="small">`instance-attribute`</span>

    skipped_geometry: tuple[SkippedOccurrenceGeometry, ...]

### diagnostics <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...]

### occurrence_count <span class="small">`instance-attribute`</span>

    occurrence_count: int

### complete <span class="small">`property`</span>

    complete: bool

Whether every occurrence and nested part reference resolved.

### stud_contacts

    stud_contacts(
        *, tolerance: float = 0.1, probe_distance: float = 0.1
    ) -> tuple[StudContact, ...]

Return strict stud matches as the historical stud-contact view.

### connection_contacts

    connection_contacts(
        *,
        tolerance: float = 0.25,
        angular_tolerance: float = 2.0,
    ) -> tuple[ConnectionContact, ...]

Return compatible connection features already mated in the model.

### connection_graphs

    connection_graphs(
        *,
        tolerance: float = 0.25,
        angular_tolerance: float = 2.0,
    ) -> ConnectionGraphs

Return confirmed and heuristic-inclusive occurrence multigraphs.

### snap_candidates

    snap_candidates(
        moving: OccurrenceGeometry | int,
        *,
        fixed: OccurrenceGeometry | int | None = None,
        limit: int | None = None,
    ) -> tuple[SnapCandidate, ...]

Return ranked placements for mating a moving occurrence's features.

`moving` and `fixed` accept either an occurrence geometry or its stable inspection index. When `fixed` is omitted, every other occurrence is considered.

### contact_gaps

    contact_gaps(
        *, minimum_gap: float = 5.0, chronological: bool = False
    ) -> tuple[OccurrenceContact, ...]

Return occurrences farther than `minimum_gap` from every peer.

## ModelLoadResult <span class="small">`dataclass`</span>

Model, diagnostics, and source completeness from one read/parse pass.

### model <span class="small">`instance-attribute`</span>

    model: Model | None

### diagnostics <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...]

### complete <span class="small">`instance-attribute`</span>

    complete: bool

### valid <span class="small">`property`</span>

    valid: bool

Whether the load emitted no error diagnostics.

### analyze

    analyze(parts: Parts | None = None) -> ModelAnalysis | None

Analyze the loaded model without discarding its diagnostics.

## ModelOccurrence <span class="small">`dataclass`</span>

One placed leaf part occurrence in a model.

Occurrences are traversal events: two placements of the same submodel produce distinct occurrences, so they compare and hash by identity.

`step` is the *effective* (inherited) step: pieces inside a submodel report the step their outermost placement belongs to. This differs from `path[-1].step`, which is the placement's *local* step within its own section (`OccurrencePathItem.local_step`); `source_step` carries the same local semantics.

### piece <span class="small">`instance-attribute`</span>

    piece: Piece

### part_code <span class="small">`instance-attribute`</span>

    part_code: str

### reference <span class="small">`instance-attribute`</span>

    reference: str

### colour <span class="small">`instance-attribute`</span>

    colour: Colour

### position <span class="small">`instance-attribute`</span>

    position: Vector

### matrix <span class="small">`instance-attribute`</span>

    matrix: Matrix

### source_model <span class="small">`instance-attribute`</span>

    source_model: Model

### source_line <span class="small">`instance-attribute`</span>

    source_line: int | None

### step <span class="small">`instance-attribute`</span>

    step: int | None

### source_step <span class="small">`instance-attribute`</span>

    source_step: int | None

### path <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    path: tuple[OccurrencePathItem, ...] = ()

## ModelSummary <span class="small">`dataclass`</span>

Reusable summary of a model's placed parts and geometry extents.

### bounds <span class="small">`instance-attribute`</span>

    bounds: BoundingBox | None

### origin_bounds <span class="small">`instance-attribute`</span>

    origin_bounds: BoundingBox | None

### part_counts <span class="small">`instance-attribute`</span>

    part_counts: dict[str, int]

### colour_usage <span class="small">`instance-attribute`</span>

    colour_usage: dict[int | str | None, int]

### skipped_geometry <span class="small">`instance-attribute`</span>

    skipped_geometry: tuple[SkippedGeometry, ...]

### occurrence_count <span class="small">`instance-attribute`</span>

    occurrence_count: int

### size_ldu <span class="small">`property`</span>

    size_ldu: Vector | None

Overall model size in LDraw units.

### size_mm <span class="small">`property`</span>

    size_mm: Vector | None

Overall model size in millimetres.

### from_model <span class="small">`classmethod`</span>

    from_model(
        model: Model, parts: Parts | None
    ) -> ModelSummary

Build a summary for `model` using geometry from `parts`.

Built-in expansion and custom overrides delegating to it skip cyclic references. Other custom exceptions propagate.

### from_inspection <span class="small">`classmethod`</span>

    from_inspection(
        inspection: ModelInspection,
    ) -> ModelSummary

Build a summary reusing bounds already computed by an inspection.

`inspect_model` already transforms every occurrence's expanded points into exact world bounds; this constructor folds those results instead of recomputing them, so callers building both an inspection and a summary pay for the geometry only once.

### from_occurrences <span class="small">`classmethod`</span>

    from_occurrences(
        occurrences: Iterable[ModelOccurrence],
        parts: Parts | None,
    ) -> ModelSummary

Build a summary from occurrences already traversed by a caller.

## OccurrenceAttribution <span class="small">`dataclass`</span>

Stable traversal identity and full source path for one occurrence.

### index <span class="small">`instance-attribute`</span>

    index: int

### occurrence <span class="small">`instance-attribute`</span>

    occurrence: ModelOccurrence

### model_path <span class="small">`instance-attribute`</span>

    model_path: tuple[str, ...]

### reference_path <span class="small">`instance-attribute`</span>

    reference_path: tuple[str, ...]

### source_line_path <span class="small">`instance-attribute`</span>

    source_line_path: tuple[int | None, ...]

### local_step_path <span class="small">`instance-attribute`</span>

    local_step_path: tuple[int | None, ...]

### effective_step_path <span class="small">`instance-attribute`</span>

    effective_step_path: tuple[int | None, ...]

### page_path <span class="small">`instance-attribute`</span>

    page_path: tuple[int | None, ...]

### step_path <span class="small">`property`</span>

    step_path: tuple[int | None, ...]

Compatibility alias for local source steps.

### installation_page <span class="small">`property`</span>

    installation_page: int | None

Page that places the outermost occurrence or submodel instance.

### source_page <span class="small">`property`</span>

    source_page: int | None

Page local to the section which directly places the leaf part.

## OccurrenceContact <span class="small">`dataclass`</span>

One occurrence and its nearest AABB neighbour.

### subject <span class="small">`instance-attribute`</span>

    subject: OccurrenceGeometry

### nearest <span class="small">`instance-attribute`</span>

    nearest: OccurrenceGeometry

### gap <span class="small">`instance-attribute`</span>

    gap: BoundsGap

## OccurrenceGeometry <span class="small">`dataclass`</span>

Expanded local geometry transformed into one occurrence's world frame.

### attribution <span class="small">`instance-attribute`</span>

    attribution: OccurrenceAttribution

### local <span class="small">`instance-attribute`</span>

    local: PartGeometry

### bounds <span class="small">`instance-attribute`</span>

    bounds: BoundingBox

### studs <span class="small">`instance-attribute`</span>

    studs: tuple[StudReference, ...]

### connections <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    connections: tuple[ConnectionFeature, ...] = ()

### occurrence <span class="small">`property`</span>

    occurrence: ModelOccurrence

Return the source occurrence represented by this geometry.

### index <span class="small">`property`</span>

    index: int

Return the occurrence's stable analysis-order index.

## OccurrencePathItem <span class="small">`dataclass`</span>

One local placement in a root-to-leaf occurrence path.

### model <span class="small">`instance-attribute`</span>

    model: Model

### piece <span class="small">`instance-attribute`</span>

    piece: Piece

### source_line <span class="small">`instance-attribute`</span>

    source_line: int | None

### local_step <span class="small">`instance-attribute`</span>

    local_step: int | None

### effective_step <span class="small">`instance-attribute`</span>

    effective_step: int | None

### step <span class="small">`property`</span>

    step: int | None

Compatibility spelling for `local_step` — the *local* step.

This is the step counted within the placement's own section, not the inherited one, so for submodel contents it differs from `ModelOccurrence.step` (which is the *effective* step). Use `effective_step` for the inherited semantics.

## OperationCancelled

Bases: [`Exception`](https://docs.python.org/3/builtins/exceptions.html#Exception)

A caller requested cancellation of an in-progress operation.

Deliberately derives from `Exception` rather than `RuntimeError`: setup helpers such as `ensure_library` wrap genuine failures in `RuntimeError`, so a caller's `except RuntimeError` must not misreport a user-requested cancel as a failure.

## PartCategory

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Known LDraw part categories, mirroring the official LDraw.org list.

### ANIMAL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ANIMAL = 'animal'

### ANTENNA <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ANTENNA = 'antenna'

### ARCH <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ARCH = 'arch'

### ARM <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ARM = 'arm'

### BAR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    BAR = 'bar'

### BASEPLATE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    BASEPLATE = 'baseplate'

### BELVILLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    BELVILLE = 'belville'

### BOAT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    BOAT = 'boat'

### BRACKET <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    BRACKET = 'bracket'

### BRICK <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    BRICK = 'brick'

### CANVAS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CANVAS = 'canvas'

### CAR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CAR = 'car'

### CLIKITS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CLIKITS = 'clikits'

### COCKPIT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    COCKPIT = 'cockpit'

### CONE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONE = 'cone'

### CONSTRACTION <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONSTRACTION = 'constraction'

### CONSTRACTION_ACCESSORY <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONSTRACTION_ACCESSORY = 'constraction accessory'

### CONTAINER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONTAINER = 'container'

### CONVEYOR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CONVEYOR = 'conveyor'

### CRANE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CRANE = 'crane'

### CYLINDER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CYLINDER = 'cylinder'

### DISH <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DISH = 'dish'

### DOOR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DOOR = 'door'

### DUPLO <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DUPLO = 'duplo'

### ELECTRIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ELECTRIC = 'electric'

### EXHAUST <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    EXHAUST = 'exhaust'

### FENCE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FENCE = 'fence'

### FIGURE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FIGURE = 'figure'

### FIGURE_ACCESSORY <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FIGURE_ACCESSORY = 'figure accessory'

### FLAG <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FLAG = 'flag'

### FORKLIFT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FORKLIFT = 'forklift'

### FREESTYLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FREESTYLE = 'freestyle'

### GARAGE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GARAGE = 'garage'

### GLASS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GLASS = 'glass'

### GRAB <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    GRAB = 'grab'

### HINGE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    HINGE = 'hinge'

### HOMEMAKER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    HOMEMAKER = 'homemaker'

### HOSE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    HOSE = 'hose'

### LADDER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LADDER = 'ladder'

### LEVER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LEVER = 'lever'

### MAGNET <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MAGNET = 'magnet'

### MINIFIG <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MINIFIG = 'minifig'

### MINIFIG_ACCESSORY <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MINIFIG_ACCESSORY = 'minifig accessory'

### MINIFIG_FOOTWEAR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MINIFIG_FOOTWEAR = 'minifig footwear'

### MINIFIG_HEADWEAR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MINIFIG_HEADWEAR = 'minifig headwear'

### MINIFIG_HIPWEAR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MINIFIG_HIPWEAR = 'minifig hipwear'

### MINIFIG_NECKWEAR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MINIFIG_NECKWEAR = 'minifig neckwear'

### MONORAIL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MONORAIL = 'monorail'

### PANEL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PANEL = 'panel'

### PLANE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PLANE = 'plane'

### PLANT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PLANT = 'plant'

### PLATE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PLATE = 'plate'

### PLATFORM <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PLATFORM = 'platform'

### PROPELLOR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PROPELLOR = 'propellor'

### RACK <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    RACK = 'rack'

### ROADSIGN <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ROADSIGN = 'roadsign'

### ROCK <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ROCK = 'rock'

### SCALA <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SCALA = 'scala'

### SCREW <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SCREW = 'screw'

### SHEET_CARDBOARD <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SHEET_CARDBOARD = 'sheet cardboard'

### SHEET_FABRIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SHEET_FABRIC = 'sheet fabric'

### SHEET_PLASTIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SHEET_PLASTIC = 'sheet plastic'

### SLOPE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SLOPE = 'slope'

### SPHERE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SPHERE = 'sphere'

### STAIRCASE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    STAIRCASE = 'staircase'

### STICKER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    STICKER = 'sticker'

### STRING <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    STRING = 'string'

### SUPPORT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SUPPORT = 'support'

### TAIL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TAIL = 'tail'

### TAP <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TAP = 'tap'

### TECHNIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TECHNIC = 'technic'

### TILE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TILE = 'tile'

### TIPPER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TIPPER = 'tipper'

### TRACTOR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TRACTOR = 'tractor'

### TRAILER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TRAILER = 'trailer'

### TRAIN <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TRAIN = 'train'

### TURNTABLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TURNTABLE = 'turntable'

### TYRE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TYRE = 'tyre'

### VEHICLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    VEHICLE = 'vehicle'

### WEDGE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    WEDGE = 'wedge'

### WHEEL <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    WHEEL = 'wheel'

### WINCH <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    WINCH = 'winch'

### WINDOW <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    WINDOW = 'window'

### WINDSCREEN <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    WINDSCREEN = 'windscreen'

### WING <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    WING = 'wing'

### ZNAP <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ZNAP = 'znap'

### OTHER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    OTHER = 'other'

### module_name <span class="small">`property`</span>

    module_name: str

Return the generated module name for this category.

These names are a frozen public contract: renaming one would break existing `ldraw.library.parts.*` imports.

### from_label <span class="small">`classmethod`</span>

    from_label(label: str | None) -> PartCategory | None

Return the category matching an LDraw label.

## PartCompatibility <span class="small">`dataclass`</span>

Evidence that two complete parts fit one another.

### first <span class="small">`instance-attribute`</span>

    first: str

### second <span class="small">`instance-attribute`</span>

    second: str

### relation <span class="small">`instance-attribute`</span>

    relation: str

### source <span class="small">`instance-attribute`</span>

    source: ConnectionSource

### evidence <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    evidence: str | None = None

## PartFileKind

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Kind declared by the `!LDRAW_ORG` header.

### PART <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PART = 'part'

### SUBPART <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SUBPART = 'subpart'

### PRIMITIVE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PRIMITIVE = 'primitive'

### PRIMITIVE_8 <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PRIMITIVE_8 = '8_primitive'

### PRIMITIVE_48 <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PRIMITIVE_48 = '48_primitive'

### SHORTCUT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SHORTCUT = 'shortcut'

### UNKNOWN <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    UNKNOWN = 'unknown'

## PartGeometry <span class="small">`dataclass`</span>

Expanded drawable geometry plus explicit completeness diagnostics.

### code <span class="small">`instance-attribute`</span>

    code: str

### description <span class="small">`instance-attribute`</span>

    description: str

### bounds <span class="small">`instance-attribute`</span>

    bounds: BoundingBox | None

### points <span class="small">`instance-attribute`</span>

    points: tuple[Vector, ...]

### studs <span class="small">`instance-attribute`</span>

    studs: tuple[StudReference, ...]

### connections <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    connections: tuple[ConnectionFeature, ...] = ()

### diagnostics <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...] = ()

### connection_metadata <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    connection_metadata: ConnectionMetadataReport | None = None

### complete <span class="small">`property`</span>

    complete: bool

Whether every referenced child was resolved and expanded.

### top_studs <span class="small">`property`</span>

    top_studs: tuple[StudReference, ...]

Upward-facing stud connectors in local coordinates.

### receptacles <span class="small">`property`</span>

    receptacles: tuple[StudReference, ...]

Detected underside/tube receivers in local coordinates.

## PartHistoryEntry <span class="small">`dataclass`</span>

One parsed `!HISTORY` line.

### date <span class="small">`instance-attribute`</span>

    date: str

### contributor <span class="small">`instance-attribute`</span>

    contributor: str | None

### text <span class="small">`instance-attribute`</span>

    text: str

### raw <span class="small">`instance-attribute`</span>

    raw: str

## PartInspection <span class="small">`dataclass`</span>

Part lookup, metadata, references, geometry, and explicit failures.

### code <span class="small">`instance-attribute`</span>

    code: str

### entry <span class="small">`instance-attribute`</span>

    entry: CatalogEntry | None

### path <span class="small">`instance-attribute`</span>

    path: Path | None

### metadata <span class="small">`instance-attribute`</span>

    metadata: PartMetadata | None

### references <span class="small">`instance-attribute`</span>

    references: tuple[PartReference, ...]

### geometry <span class="small">`instance-attribute`</span>

    geometry: PartGeometry | None

### diagnostics <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...]

### complete <span class="small">`property`</span>

    complete: bool

Return whether every requested inspection component succeeded.

## PartMetadata <span class="small">`dataclass`</span>

Metadata and relationships represented by an LDraw part header.

### description <span class="small">`instance-attribute`</span>

    description: str

### name <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    name: str | None = None

### author <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    author: str | None = None

### author_username <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    author_username: str | None = None

### file_kind <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    file_kind: PartFileKind = PartFileKind.UNKNOWN

### origin <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    origin: LibraryOrigin = LibraryOrigin.UNKNOWN

### qualifiers <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    qualifiers: tuple[str, ...] = ()

### release <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    release: str | None = None

### license <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    license: str | None = None

### bfc <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    bfc: BfcCertification = BfcCertification.UNKNOWN

### history <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    history: tuple[PartHistoryEntry, ...] = ()

### category <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    category: str | None = None

### keywords <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    keywords: tuple[str, ...] = ()

### status <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    status: PartStatus = PartStatus.CURRENT

### replacement <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    replacement: str | None = None

### preview <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    preview: PreviewTransform | None = None

### to_dict

    to_dict() -> dict[str, Any]

Return a JSON-ready representation for the persistent catalog.

### from_dict <span class="small">`classmethod`</span>

    from_dict(value: dict[str, Any]) -> PartMetadata

Restore metadata previously returned by `to_dict`.

## PartReference <span class="small">`dataclass`</span>

A type-1 subfile reference found inside a part file.

### parent_code <span class="small">`instance-attribute`</span>

    parent_code: str

### code <span class="small">`instance-attribute`</span>

    code: str

### reference <span class="small">`instance-attribute`</span>

    reference: str

### kind <span class="small">`instance-attribute`</span>

    kind: PartReferenceKind

### description <span class="small">`instance-attribute`</span>

    description: str | None

### colour <span class="small">`instance-attribute`</span>

    colour: Colour

### position <span class="small">`instance-attribute`</span>

    position: Vector

### matrix <span class="small">`instance-attribute`</span>

    matrix: Matrix

### depth <span class="small">`instance-attribute`</span>

    depth: int

## PartReferenceKind

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Kind of type-1 reference found inside a part file.

### PART <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PART = 'part'

### SUBPART <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SUBPART = 'subpart'

### PRIMITIVE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PRIMITIVE = 'primitive'

### UNKNOWN <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    UNKNOWN = 'unknown'

## PartStatus

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Relationship/lifecycle status derived from header evidence.

### CURRENT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    CURRENT = 'current'

### ALIAS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ALIAS = 'alias'

### MOVED <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    MOVED = 'moved'

### OBSOLETE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    OBSOLETE = 'obsolete'

## Parts

Part catalog loader.

### ColourAttributes <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ColourAttributes = (
        "CHROME",
        "PEARLESCENT",
        "RUBBER",
        "MATTE_METALLIC",
        "METAL",
        "GLITTER",
        "SPECKLE",
        "LUMINANCE",
    )

### path <span class="small">`instance-attribute`</span>

    path = Path(parts_lst)

### parts_dirs <span class="small">`instance-attribute`</span>

    parts_dirs: list[Path] = []

### parts_subdirs <span class="small">`instance-attribute`</span>

    parts_subdirs: dict[str, Path] = {}

### by_name <span class="small">`instance-attribute`</span>

    by_name: dict[str, str] = {}

### by_code <span class="small">`instance-attribute`</span>

    by_code: dict[str, str] = {}

### by_code_name <span class="small">`instance-attribute`</span>

    by_code_name: dict[tuple[str, str], Part | None] = {}

### by_category <span class="small">`instance-attribute`</span>

    by_category: defaultdict[str, dict[str, str]] = defaultdict(
        dict
    )

### primitives_by_name <span class="small">`instance-attribute`</span>

    primitives_by_name: dict[str, str] = {}

### primitives_by_code <span class="small">`instance-attribute`</span>

    primitives_by_code: dict[str, str] = {}

### colours <span class="small">`instance-attribute`</span>

    colours: dict[str | int, str] = {}

### alpha_values <span class="small">`instance-attribute`</span>

    alpha_values: dict[str | int, int] = {}

### colour_attributes <span class="small">`instance-attribute`</span>

    colour_attributes: dict[str | int, list[str]] = {}

### colours_by_name <span class="small">`instance-attribute`</span>

    colours_by_name: dict[str, Colour] = {}

### colours_by_code <span class="small">`instance-attribute`</span>

    colours_by_code: dict[int, Colour] = {}

### library_root <span class="small">`property`</span>

    library_root: Path

Directory containing `parts.lst`, parts, primitives, and colours.

### catalog <span class="small">`property`</span>

    catalog: PartsCatalog

The typed parts catalog, categorized on first access.

### tyre_rim_compatibility <span class="small">`property`</span>

    tyre_rim_compatibility: tuple[PartCompatibility, ...]

Tyre/rim pairs evidenced by official complete-part shortcuts.

### get <span class="small">`classmethod`</span>

    get(
        parts_lst: str | Path,
        *,
        tree_fingerprint: str | None = None,
        parts_lst_md5: str | None = None,
        connection_shadows: Iterable[str | Path] = (),
        studio_metadata: Iterable[str | Path] = (),
    ) -> Parts

Get a memoized Parts keyed by list and optional content fingerprints.

Omitting `parts_lst_md5` memoizes under a different key than passing it, so mixing both styles for one file parses it twice. Directory connection sources are deliberately not walked on cache lookup; call `fresh` after editing their nested contents.

### clear_cache <span class="small">`classmethod`</span>

    clear_cache() -> None

Clear memoized instances, including stale directory sources.

### fresh <span class="small">`classmethod`</span>

    fresh(
        parts_lst: str | Path,
        *,
        tree_fingerprint: str | None = None,
        parts_lst_md5: str | None = None,
        connection_shadows: Iterable[str | Path] = (),
        studio_metadata: Iterable[str | Path] = (),
    ) -> Parts

Return a freshly constructed Parts, replacing the memoized one.

Explicit rebuild paths call this to guarantee a genuinely fresh categorization and reload nested connection-source edits; the memo is repopulated with the fresh instance.

### from_catalog <span class="small">`classmethod`</span>

    from_catalog(
        parts_lst: str | Path, catalog: PartsCatalog
    ) -> Parts

Construct a Parts that adopts a prebuilt catalog.

Skips the expensive per-part categorization pass.

### adopt_catalog

    adopt_catalog(catalog: PartsCatalog) -> None

Adopt a prebuilt catalog, skipping categorization.

A no-op when this instance is already categorized, so a memoized instance can safely adopt the same persisted index repeatedly.

### build_catalog

    build_catalog(
        *,
        on_progress: ProgressCallback | None = None,
        cancellation: CancellationToken | None = None,
    ) -> PartsCatalog

Materialize the catalog with determinate progress and cancellation.

### get_entry_by_code

    get_entry_by_code(code: str) -> CatalogEntry | None

Return a typed catalog entry by part code.

### get_entry_by_description

    get_entry_by_description(
        description: str,
    ) -> CatalogEntry | None

Return a typed catalog entry by part description.

### entries_by_category

    entries_by_category(
        category: PartCategory,
    ) -> tuple[CatalogEntry, ...]

Return entries in a part category.

### minifig_entries

    minifig_entries(
        section: MinifigSection | None = None,
    ) -> tuple[CatalogEntry, ...]

Return entries in minifigure sections.

### get_category

    get_category(part_description: str) -> PartCategory | None

Get the category of a part based on its description.

### load

    load() -> None

Load the parts list, colours, and primitives (all cheap passes).

The expensive categorization pass — opening every part file for its `!CATEGORY` header — runs lazily on first catalog access.

### section_find

    section_find(pieces: list[str]) -> tuple[str, str]

Return code and description from a parts.lst split line.

The description is kept exactly as written in `parts.lst`; detected minifig sections are recorded for the catalog. Generated symbol names strip the `Minifig` prefix at generation time (see `symbol_description`).

### description_for

    description_for(code: str) -> str | None

Return the `parts.lst` description for a part code, or None.

Prefer exact casing, then normalize casing and reference separators without parsing or categorizing parts.

### part

    part(
        description: str | None = None, code: str | None = None
    ) -> Part

Get a Part from its description or code.

Raises `PartNotFoundError` when the description or code is not in the library or the part file is missing; use `find_part` for a lookup that returns None instead.

### find_part

    find_part(
        description: str | None = None, code: str | None = None
    ) -> Part | None

Get a Part from its description or code, or None when not found.

### bounding_box

    bounding_box(code: str) -> BoundingBox

Axis-aligned bounding box of a part's geometry, in LDU.

Subfiles are resolved recursively; unresolvable ones are skipped with a warning. Raises `PartNotFoundError` for an unknown code and `NoGeometryError` when the part draws nothing.

### geometry

    geometry(code: str) -> PartGeometry

Return exact expanded geometry and completeness diagnostics.

### connections

    connections(code: str) -> tuple[ConnectionFeature, ...]

Return physical connection features detected for a part.

### connection_metadata

    connection_metadata(code: str) -> ConnectionMetadataReport

Return features and normalized metadata coverage for a part.

### add_connection_shadow

    add_connection_shadow(source: str | Path) -> None

Add an LDCad shadow library as an optional connection source.

Sources are applied in registration order; later sources can clear or supersede features from earlier sources.

### clear_connection_shadows

    clear_connection_shadows() -> None

Remove all configured LDCad shadow-library sources.

### add_studio_metadata

    add_studio_metadata(source: str | Path) -> None

Add a Studio connectivity JSON source at Studio precedence.

### clear_studio_metadata

    clear_studio_metadata() -> None

Remove every configured Studio connectivity source.

### set_connection_overrides

    set_connection_overrides(
        code: str,
        features: Iterable[ConnectionFeature],
        *,
        replace_existing: bool = False,
    ) -> None

Register authoritative connection features for one part.

By default overrides augment inferred and shadow-derived features. Set `replace_existing` to discard every lower-priority feature.

### clear_connection_overrides

    clear_connection_overrides(code: str | None = None) -> None

Remove connection overrides for one part or the whole library.

### compatible_tyres

    compatible_tyres(rim_code: str) -> tuple[str, ...]

Return tyre codes evidenced as compatible with `rim_code`.

### compatible_rims

    compatible_rims(tyre_code: str) -> tuple[str, ...]

Return rim codes evidenced as compatible with `tyre_code`.

### inspect_part

    inspect_part(
        code: str,
        *,
        include_geometry: bool = True,
        recursive_references: bool = False,
    ) -> PartInspection

Inspect one part without translating failures into empty data.

### studs

    studs(code: str) -> tuple[StudReference, ...]

All stud primitives a part places, in the part's own coordinates.

Includes underside tubes and other downward studs; filter with `StudReference.is_top_stud` or use `stud_positions`.

### stud_positions

    stud_positions(code: str) -> tuple[Vector, ...]

Positions of a part's top studs (upward connectors), in LDU.

### resolve_colour

    resolve_colour(colour: Colour | int) -> Colour

Return catalog metadata for `colour` when it is known.

### references_for

    references_for(
        code: str, *, recursive: bool = False
    ) -> tuple[PartReference, ...]

Return type-1 references placed by a part file.

## PartsCatalog <span class="small">`dataclass`</span>

Typed collection of part catalog entries.

### by_code <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    by_code: dict[str, CatalogEntry] = field(
        default_factory=dict
    )

### by_description <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    by_description: dict[str, CatalogEntry] = field(
        default_factory=dict
    )

### by_category <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    by_category: defaultdict[
        PartCategory, list[CatalogEntry]
    ] = field(default_factory=lambda: defaultdict(list))

### by_minifig_section <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    by_minifig_section: defaultdict[
        MinifigSection, list[CatalogEntry]
    ] = field(default_factory=lambda: defaultdict(list))

### add

    add(entry: CatalogEntry) -> None

Add or replace an entry in every lookup index.

### get_entry_by_code

    get_entry_by_code(code: str) -> CatalogEntry | None

Return a catalog entry by part code.

### get_entry_by_description

    get_entry_by_description(
        description: str,
    ) -> CatalogEntry | None

Return a catalog entry by part description.

### entries_by_category

    entries_by_category(
        category: PartCategory,
    ) -> tuple[CatalogEntry, ...]

Return catalog entries in a category.

### minifig_entries

    minifig_entries(
        section: MinifigSection | None = None,
    ) -> tuple[CatalogEntry, ...]

Return minifigure catalog entries, optionally for one section.

### search

    search(
        query: str,
        *,
        within: Iterable[CatalogEntry] | None = None,
        fields: Iterable[
            CatalogSearchField
        ] = ALL_CATALOG_SEARCH_FIELDS,
        limit: int | None = None,
    ) -> tuple[CatalogEntry, ...]

Return normalized token matches in deterministic relevance order.

Every token must occur somewhere in the selected fields. `within` scopes the search to a caller-provided category or other subset.

### module_sections

    module_sections() -> dict[tuple[str, ...], dict[str, str]]

Return generated module sections keyed by package path.

Section dicts are keyed by the catalog description exactly as written in `parts.lst`; symbol names (including minifig-prefix stripping) are derived at generation time, where collisions are deduplicated with part-code suffixes.

## Person

Representation of a LEGO minifigure.

### position <span class="small">`instance-attribute`</span>

    position = (
        position if position is not None else Vector(0, 0, 0)
    )

### matrix <span class="small">`instance-attribute`</span>

    matrix = matrix if matrix is not None else Identity()

### pieces_info <span class="small">`instance-attribute`</span>

    pieces_info: dict[str, Piece] = {}

### group <span class="small">`instance-attribute`</span>

    group = group

### head

    head(
        colour: ColourInput, angle: Number = 0, part: str = Head
    ) -> Piece

Add a head.

### hat

    hat(
        head: Piece, colour: ColourInput, part: str = Hat
    ) -> Piece

Add a hat piece to the figure's head.

### torso

    torso(colour: ColourInput, part: str = Torso) -> Piece

Add a torso piece.

### backpack

    backpack(
        colour: ColourInput,
        displacement: Vector | None = None,
        part: str = Airtanks,
    ) -> Piece

Add a backpack.

### hips_and_legs

    hips_and_legs(
        colour: ColourInput, part: str = HipsAndLegs
    ) -> Piece

Add combined hips and legs.

### hips

    hips(colour: ColourInput, part: str = Hips) -> Piece

Add hips.

### left_arm

    left_arm(
        colour: ColourInput,
        angle: Number = 0,
        part: str = ArmLeft,
    ) -> Piece

Add a left arm.

### left_hand

    left_hand(
        left_arm: Piece,
        colour: ColourInput,
        angle: Number = 0,
        part: str = Hand,
    ) -> Piece

Add a left hand piece to the figure's left arm.

### left_hand_item

    left_hand_item(
        left_hand: Piece,
        colour: ColourInput,
        displacement: Vector,
        angle: Number = 0,
        part: str | None = None,
    ) -> Piece | None

Add an item to the left hand.

### right_arm

    right_arm(
        colour: ColourInput,
        angle: Number = 0,
        part: str = ArmRight,
    ) -> Piece

Add a right arm.

### right_hand

    right_hand(
        right_arm: Piece,
        colour: ColourInput,
        angle: Number = 0,
        part: str = Hand,
    ) -> Piece

Add a right hand piece to the figure's right arm.

### right_hand_item

    right_hand_item(
        right_hand: Piece,
        colour: ColourInput,
        displacement: Vector,
        angle: Number = 0,
        part: str | None = None,
    ) -> Piece | None

Add a right hand item.

### left_leg

    left_leg(
        colour: ColourInput,
        angle: Number = 0,
        part: str = LegLeft,
    ) -> Piece

Add a left leg.

### left_shoe

    left_shoe(
        left_leg: Piece,
        colour: ColourInput,
        angle: Number = 0,
        part: str | None = None,
    ) -> Piece | None

Add a shoe on the left.

### right_leg

    right_leg(
        colour: ColourInput,
        angle: Number = 0,
        part: str = LegRight,
    ) -> Piece

Add a right leg.

### right_shoe

    right_shoe(
        right_leg: Piece,
        colour: ColourInput,
        angle: Number = 0,
        part: str | None = None,
    ) -> Piece | None

Add a shoe on the right.

## Piece <span class="small">`dataclass`</span>

A part with a defined colour, position, and rotation.

### part <span class="small">`instance-attribute`</span>

    part: str

### suffix <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    suffix: str = DEFAULT_SUFFIX

### colour <span class="small">`instance-attribute`</span>

    colour: Colour = _as_colour(colour)

### position <span class="small">`instance-attribute`</span>

    position: Vector = position

### matrix <span class="small">`instance-attribute`</span>

    matrix: Matrix = matrix

### group <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    group: Group | None = None

### reference <span class="small">`property`</span>

    reference: str

The subfile reference this piece serializes to, e.g. `3001.dat`.

### place <span class="small">`classmethod`</span>

    place(
        part: str,
        *,
        colour: Colour | int = MAIN_COLOUR_CODE,
        position: Vector | None = None,
        matrix: Matrix | None = None,
        group: Group | None = None,
        suffix: str = DEFAULT_SUFFIX,
    ) -> Self

Create a piece keyword-first, defaulting to the origin and identity.

### to_ldraw

    to_ldraw() -> str

Serialize this piece to an LDraw type 1 line.

## PreviewTransform <span class="small">`dataclass`</span>

Official `!PREVIEW` colour and placement transform.

### colour_code <span class="small">`instance-attribute`</span>

    colour_code: int

### position <span class="small">`instance-attribute`</span>

    position: Vector

### matrix <span class="small">`instance-attribute`</span>

    matrix: Matrix

## ProgressEvent <span class="small">`dataclass`</span>

One progress update from a long-running library operation.

### stage <span class="small">`instance-attribute`</span>

    stage: ProgressStage

### message <span class="small">`instance-attribute`</span>

    message: str

### current <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    current: int | None = None

### total <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    total: int | None = None

### path <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    path: Path | None = None

### unit <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    unit: ProgressUnit | None = None

### determinate <span class="small">`property`</span>

    determinate: bool

Whether this event has a current value, total, and explicit unit.

## ProgressStage

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

High-level setup stages reported to embedding applications.

### DOWNLOAD <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DOWNLOAD = 'download'

### UNPACK <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    UNPACK = 'unpack'

### PARTS_LIST <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PARTS_LIST = 'parts-list'

### LIBRARY_GENERATION <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LIBRARY_GENERATION = 'library-generation'

### FINGERPRINT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FINGERPRINT = 'fingerprint'

### INDEX_LOAD <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    INDEX_LOAD = 'index-load'

### INDEX_REBUILD <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    INDEX_REBUILD = 'index-rebuild'

### LIBRARY_DISCOVERY <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LIBRARY_DISCOVERY = 'library-discovery'

### VALIDATION <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    VALIDATION = 'validation'

### RENDER <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    RENDER = 'render'

### DONE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    DONE = 'done'

## ProgressUnit

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Unit carried by determinate progress events.

### BYTES <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    BYTES = 'bytes'

### FILES <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FILES = 'files'

### PARTS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    PARTS = 'parts'

### STEPS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    STEPS = 'steps'

### VIEWS <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    VIEWS = 'views'

## RenderBackend

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Supported optional command-line renderers, in preference order.

### LDVIEW <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LDVIEW = 'ldview'

### LEOCAD <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    LEOCAD = 'leocad'

## RenderCapability <span class="small">`dataclass`</span>

Availability and executable path for one optional backend.

### backend <span class="small">`instance-attribute`</span>

    backend: RenderBackend

### available <span class="small">`instance-attribute`</span>

    available: bool

### executable <span class="small">`instance-attribute`</span>

    executable: Path | None

## RenderResult <span class="small">`dataclass`</span>

Output or diagnostics from one preview request.

### source <span class="small">`instance-attribute`</span>

    source: Path

### view <span class="small">`instance-attribute`</span>

    view: RenderView

### size <span class="small">`instance-attribute`</span>

    size: tuple[int, int]

### backend <span class="small">`instance-attribute`</span>

    backend: RenderBackend | None

### output <span class="small">`instance-attribute`</span>

    output: Path | None

### cached <span class="small">`instance-attribute`</span>

    cached: bool

### diagnostics <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    diagnostics: tuple[Diagnostic, ...] = ()

### complete <span class="small">`property`</span>

    complete: bool

Return whether a usable image was produced.

## RenderView

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Stable named preview viewpoints.

### FRONT <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    FRONT = 'front'

### ISOMETRIC <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ISOMETRIC = 'isometric'

### TOP <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    TOP = 'top'

## RotationMode

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

MLCad rotation-step modes.

### RELATIVE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    RELATIVE = 'REL'

### ADDITIVE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ADDITIVE = 'ADD'

### ABSOLUTE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ABSOLUTE = 'ABS'

### END <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    END = 'END'

## RotationStep <span class="small">`dataclass`</span>

A parsed MLCad `ROTSTEP` boundary.

### mode <span class="small">`instance-attribute`</span>

    mode: RotationMode

### angles <span class="small">`instance-attribute`</span>

    angles: tuple[float, float, float] | None

### command_matrix <span class="small">`instance-attribute`</span>

    command_matrix: Matrix

### effective_matrix <span class="small">`instance-attribute`</span>

    effective_matrix: Matrix

### source_line <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    source_line: int | None = None

## SectionShape

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

Cross-section used by one cylindrical profile section.

### ROUND <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ROUND = 'round'

### AXLE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    AXLE = 'axle'

### SQUARE <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    SQUARE = 'square'

## Severity

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum "enum.StrEnum")

How serious a diagnostic is.

### ERROR <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    ERROR = 'error'

### WARNING <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    WARNING = 'warning'

## SkippedGeometry <span class="small">`dataclass`</span>

A part occurrence whose geometry could not be folded into bounds.

### part <span class="small">`instance-attribute`</span>

    part: str

### source_model <span class="small">`instance-attribute`</span>

    source_model: str

### source_line <span class="small">`instance-attribute`</span>

    source_line: int | None

### reason <span class="small">`instance-attribute`</span>

    reason: str

## SkippedOccurrenceGeometry <span class="small">`dataclass`</span>

Occurrence whose geometry could not produce world bounds.

### attribution <span class="small">`instance-attribute`</span>

    attribution: OccurrenceAttribution

### diagnostic <span class="small">`instance-attribute`</span>

    diagnostic: Diagnostic

### reason <span class="small">`property`</span>

    reason: str

Return the structured diagnostic's human-readable message.

## SnapCandidate <span class="small">`dataclass`</span>

Compatible feature pair and the resulting moving-part placement.

### moving_occurrence <span class="small">`instance-attribute`</span>

    moving_occurrence: OccurrenceGeometry

### fixed_occurrence <span class="small">`instance-attribute`</span>

    fixed_occurrence: OccurrenceGeometry

### moving <span class="small">`instance-attribute`</span>

    moving: ConnectionFeature

### fixed <span class="small">`instance-attribute`</span>

    fixed: ConnectionFeature

### transform <span class="small">`instance-attribute`</span>

    transform: SnapTransform

### residual <span class="small">`instance-attribute`</span>

    residual: ConnectionResidual

## SnapTransform <span class="small">`dataclass`</span>

Rigid placement aligning one local feature to another feature.

### position <span class="small">`instance-attribute`</span>

    position: Vector

### matrix <span class="small">`instance-attribute`</span>

    matrix: Matrix

## StudContact <span class="small">`dataclass`</span>

Compatibility projection of one strict stud/receptacle feature match.

### stud_occurrence <span class="small">`instance-attribute`</span>

    stud_occurrence: OccurrenceGeometry

### supported_occurrence <span class="small">`instance-attribute`</span>

    supported_occurrence: OccurrenceGeometry

### stud <span class="small">`instance-attribute`</span>

    stud: StudReference

### position <span class="small">`instance-attribute`</span>

    position: Vector

### stud_feature <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    stud_feature: ConnectionFeature | None = None

### receptacle_feature <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    receptacle_feature: ConnectionFeature | None = None

### residual <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    residual: ConnectionResidual | None = None

## StudReference <span class="small">`dataclass`</span>

A stud primitive placed by a part, in the part's own coordinates.

### name <span class="small">`instance-attribute`</span>

    name: str

Casefolded primitive stem, e.g. `stud` or `stud4`.

### description <span class="small">`instance-attribute`</span>

    description: str

The primitive's header description, e.g. `Stud Tube Open`.

### position <span class="small">`instance-attribute`</span>

    position: Vector

The primitive's origin -- for top studs, the centre of the stud base.

### up <span class="small">`class-attribute`</span> <span class="small">`instance-attribute`</span>

    up: Vector = field(default_factory=lambda: Vector(0, -1, 0))

Image of the stud's local up direction (0, -1, 0) under the placing transforms; unit length under rigid placements.

### is_receptacle <span class="small">`property`</span>

    is_receptacle: bool

Whether this primitive describes an underside/tube receiver.

### is_placeholder <span class="small">`property`</span>

    is_placeholder: bool

Whether this is a drawing placeholder rather than a connector.

### is_top_stud <span class="small">`property`</span>

    is_top_stud: bool

Whether this stud is an upward connector a brick can sit on.

Excludes underside tubes and placeholder primitives by description, and any stud whose placing transforms point it away from up (LDraw up is -Y), such as the sideways front stud of a headlight brick.

## StudioConnectionLibrary

Read the supported connectivity subset of a Studio JSON export.

A part row with an empty or absent `connections` list contributes no authoritative evidence: heuristic and primitive features are kept and coverage is unchanged. Explicit clear-to-empty is an LDCad `SNAP_CLEAR` or override concern.

### source <span class="small">`instance-attribute`</span>

    source = Path(source).expanduser()

### connections_for

    connections_for(code: str) -> ShadowConnectionResult

Return one part's row, or the document fallback when absent.

This single-part view carries per-part statistics, so summing it over an assembly double-counts document evidence. Assembly aggregation must use `_part_feature_contribution` per child and `_document_result_for` once per root query instead.

## ValidationIssue <span class="small">`module-attribute`</span>

    ValidationIssue = Diagnostic

## Vector <span class="small">`dataclass`</span>

A vector in 3D.

### x <span class="small">`instance-attribute`</span>

    x: Number

### y <span class="small">`instance-attribute`</span>

    y: Number

### z <span class="small">`instance-attribute`</span>

    z: Number

### repr <span class="small">`property`</span>

    repr: str

Return string representation of vector coordinates.

### copy

    copy() -> Self

Copy the vector to a new vector containing the same values.

### cross

    cross(other: Vector) -> Vector

Cross product.

### dot

    dot(other: Vector) -> float

Dot product.

### normalized

    normalized() -> Vector

Return a unit-length copy of this vector.

## XAxis

Bases: `Axis`

X-axis representation.

## YAxis

Bases: `Axis`

Y-axis representation.

## ZAxis

Bases: `Axis`

Z-axis representation.

## analyze_model

    analyze_model(
        model: Model,
        *,
        parts: Parts | None = None,
        diagnostics: Iterable[Diagnostic] = (),
    ) -> ModelAnalysis

Traverse leaf occurrences once and reuse them for all derived views.

Built-in expansion and custom overrides delegating to it skip cyclic submodel references; other custom exceptions propagate. Each skip surfaces as an `MPD_CYCLE` diagnostic unless an equal one was already passed in via `diagnostics`.

## angular_alignment_within

    angular_alignment_within(
        alignment: float, tolerance_degrees: float
    ) -> bool

Return whether an absolute axis alignment is within a tolerance.

## bill_of_materials

    bill_of_materials(
        model: _ModelLike | None = None,
        *,
        parts: Parts | None = None,
        occurrences: Iterable[ModelOccurrence] | None = None,
    ) -> list[BomRow]

Count leaf pieces by part and colour, expanding submodel references.

A submodel placed twice contributes its pieces twice. Submodel reference pieces themselves are expanded, never counted. Colour 16 (the main colour) inside a submodel is resolved to the colour the submodel was placed with. Descriptions and colour names are resolved when a parts catalog is given.

References only resolve against the given model's own submodel table. To count one submodel of a larger model, pass `root.submodel_view(name)` rather than a model taken straight from `Model.submodels` — the latter treats nested submodel references as leaf parts.

Part codes are counted case- and separator-insensitively; each row shows the first occurrence's spelling. `ModelOccurrence.part_code` is authoritative, including caller-provided overrides. Parsed part identities retain dotted names and omit their terminal .dat suffix.

Custom occurrence traversals are authoritative. Concrete Model overrides delegating to super() retain the BOM's cycle-skipping behavior. Iterable returns and narrower overrides accepting only include_steps are supported; other custom exceptions propagate.

## bounds_gap

    bounds_gap(
        left: BoundingBox, right: BoundingBox
    ) -> BoundsGap

Return axis and Euclidean distance between two AABBs.

## compare_inventory

    compare_inventory(
        model: _ModelLike,
        expected: Iterable[BomRow],
        *,
        part_aliases: Mapping[str, str] | None = None,
        parts: Parts | None = None,
    ) -> InventoryComparison

Compare expanded model counts with inventory rows, aggregating duplicates.

Part aliases apply to both sides; colour mapping belongs to CSV input. Cyclic or unresolved submodel references fail instead of returning a potentially matching partial inventory. Leaf references without an explicit `.dat` suffix require listing evidence in `parts` before aliases are applied; explicit `.dat` part references do not require a catalog.

Non-finite geometry in a concrete Model, or non-finite expanded transforms from any occurrence provider, raises ValueError before comparing counts. Submodel views check their selected section and reachable sections rather than unrelated siblings in their shared resolution table. Custom traversals audit reachable submodel placement transforms separately; part placement transforms are checked when their occurrences are emitted.

## connection_residual

    connection_residual(
        left: ConnectionFeature, right: ConnectionFeature
    ) -> ConnectionResidual

Return centerline, axial, and orientation residuals for two features.

## connections_compatible

    connections_compatible(
        left: ConnectionFeature,
        right: ConnectionFeature,
        *,
        radius_tolerance: float = 0.35,
    ) -> bool

Return whether two features are physically eligible to mate.

## discover_libraries

    discover_libraries(
        paths: Iterable[str | Path] | None = None,
        *,
        on_progress: ProgressCallback | None = None,
        cancellation: CancellationToken | None = None,
    ) -> tuple[LibraryInspection, ...]

Discover valid and partial installations in configured/common locations.

## download

    download(
        *,
        show_progress: bool = True,
        version: str = COMPLETE_VERSION,
        on_progress: ProgressCallback | None = None,
        resume: bool = False,
        cancellation: CancellationToken | None = None,
    ) -> str

Download and unpack an LDraw library version, generating parts.lst file.

The complete library comes from ldraw.org; versioned releases come from snapshot tags of the rienafairefr/ldraw-parts GitHub repository.

## ensure_library

    ensure_library(
        config: Config | None = None,
        *,
        version: str = COMPLETE_VERSION,
        write_config: bool = False,
        config_file: str | Path | None = None,
        force_generate: bool = False,
        on_progress: ProgressCallback | None = None,
        cancellation: CancellationToken | None = None,
    ) -> LDrawSession

Ensure a configured library, generated package, and catalog index exist.

When the library is downloaded, `config.ldraw_library_path` is updated in place on the caller's Config (persisted only when `write_config` is true), and the process-global default import configuration is replaced via `LibraryImporter.set_config`.

## generate

    generate(
        config: Config,
        *,
        force: bool = False,
        on_progress: ProgressCallback | None = None,
        fingerprint: str | None = None,
        cancellation: CancellationToken | None = None,
    ) -> None

Generate the library from configuration.

## inspect_library

    inspect_library(path: str | Path) -> LibraryInspection

Inspect a candidate installation without building its catalog.

## inspect_model

    inspect_model(
        model: Model,
        parts: Parts,
        *,
        occurrences: Iterable[ModelOccurrence] | None = None,
        page_marker_prefix: str = DEFAULT_PAGE_MARKER_PREFIX,
    ) -> ModelInspection

Inspect leaf occurrences using recursively expanded exact geometry.

## iter_instruction_issues

    iter_instruction_issues(
        document: InstructionDocument,
        *,
        max_parts: int | None = None,
    ) -> Iterator[InstructionIssue]

Yield structural and semantic issues in `document`.

## iter_ldr_issues

    iter_ldr_issues(
        path: Path | ModelLoadResult, parts: Parts | None = None
    ) -> Iterator[ValidationIssue]

Yield the issues found in an LDraw model or part file, in line order.

Malformed lines, unparseable colour values, and (when a parts catalog with colour definitions is given) unknown part references and colour codes are errors. Suspicious-but-legal constructs — legacy dithered colours, non-orthonormal or singular transformation matrices, and unknown bang meta-commands — are warnings.

Unreadable or non-UTF-8 files do not raise; they yield an `IO_READ_FAILED` or `IO_DECODE_FAILED` error diagnostic with `line_number=None`. Issues are yielded sorted by line number, with file-level diagnostics (`line_number=None`) first.

## load_model

    load_model(
        path: Path | str,
        parts: Parts | None = None,
        *,
        tolerant: bool = True,
    ) -> ModelLoadResult

Read, parse, and validate a model without throwing for data failures.

## model_bounds

    model_bounds(
        model: Model, parts: Parts
    ) -> BoundingBox | None

Return the true transformed bounds for `model` in LDraw units.

## parse_model

    parse_model(
        text: str,
        *,
        name: str = "",
        source: Path | str | None = None,
    ) -> Model

Parse LDraw document text into a Model.

A document without `0 FILE` sections becomes a single model. In an MPD document the first section becomes the returned root model and later sections become its submodels, resolvable via `Model.submodel_for`.

## parse_model_result

    parse_model_result(
        text: str,
        *,
        name: str = "",
        source: Path | str | None = None,
        parts: Parts | None = None,
        tolerant: bool = True,
    ) -> ModelLoadResult

Parse and validate text once, optionally retaining a partial model.

## plan_download

    plan_download(
        version: str = COMPLETE_VERSION,
        *,
        cache_path: str | Path | None = None,
        cancellation: CancellationToken | None = None,
    ) -> DownloadPlan

Inspect remote size/resume support and local archive integrity.

## prepare_catalog

    prepare_catalog(
        config: Config | None = None,
        *,
        capabilities: Iterable[LDrawCapability] = (
            LDrawCapability.CATALOG,
        ),
        connection_shadows: Iterable[str | Path] = (),
        studio_metadata: Iterable[str | Path] = (),
        force: bool = False,
        on_progress: ProgressCallback | None = None,
        cancellation: CancellationToken | None = None,
    ) -> CatalogPreparationResult

Prepare requested configured data and return a structured report.

## read_inventory

    read_inventory(
        path: str | Path,
        *,
        columns: Mapping[str, str] | None = None,
        colour_map: Mapping[str, str | int] | None = None,
    ) -> list[BomRow]

Read native BOM CSV or explicitly mapped inventory columns/colours.

`columns` maps `part`, `colour`, and `quantity` to CSV headers. Without a colour map, colour values are LDraw codes or direct RGB. When a map is supplied, every inventory colour must have an entry. Empty native `colour_code` cells fall back to `colour_name` for RGB. Malformed rows raise `ValueError` with their CSV line number.

## read_model

    read_model(path: Path | str) -> Model

Read a `.ldr` or `.mpd` file into a Model.

## render_capabilities

    render_capabilities() -> tuple[RenderCapability, ...]

Detect optional renderers without invoking them.

## render_preview

    render_preview(
        source: str | Path,
        *,
        view: RenderView = RenderView.ISOMETRIC,
        size: tuple[int, int] = (800, 600),
        backend: RenderBackend | None = None,
        output: str | Path | None = None,
        cache_path: str | Path | None = None,
        refresh: bool = False,
        on_progress: ProgressCallback | None = None,
        cancellation: CancellationToken | None = None,
    ) -> RenderResult

Render one view, using a content-addressed PNG cache when possible.

The cache key covers the top-level source bytes, the resolved renderer executable path, and the full render command (backend, view angles, size, and renderer options). Files referenced by the source (submodels and sidecar part files) and the parts-library state are NOT part of the key, so edits to them do not invalidate cached previews; pass `refresh=True` to skip the cache read and force a re-render (the fresh image is still written back to the cache). The managed default cache evicts PNGs older than 90 days and caps retained data at 512 MiB, checking at most once per hour; caller-provided cache directories are never pruned automatically.

## snap_transform

    snap_transform(
        moving: ConnectionFeature, target: ConnectionFeature
    ) -> SnapTransform

Return a rigid transform placing `moving` onto `target`.

Centered cylindrical interfaces are direction-symmetric, so their target frame is flipped when that gives the smaller axis rotation; non-centered profiles extend one-sided and always mate axis-to-axis. Cross-section roll is preserved for axle profiles. Candidate frames are matched to the moving frame's handedness, so the delta is always a proper rotation and a part placed with a mirroring matrix is never reflected.

## comparison_to_csv

    comparison_to_csv(comparison: InventoryComparison) -> str

Serialize comparison differences as CSV, including an empty header on match.

## STUD_PITCH <span class="small">`module-attribute`</span>

    STUD_PITCH: Final[int] = 20

## PLATE_HEIGHT <span class="small">`module-attribute`</span>

    PLATE_HEIGHT: Final[int] = 8

## BRICK_HEIGHT <span class="small">`module-attribute`</span>

    BRICK_HEIGHT: Final[int] = 24

## LDU_TO_MM <span class="small">`module-attribute`</span>

    LDU_TO_MM: Final[float] = 0.4

## rows_to_csv

    rows_to_csv(rows: Iterable[BomRow]) -> str

Serialize rows to CSV text with a header line.

## rows_to_json

    rows_to_json(rows: Iterable[BomRow]) -> str

Serialize rows to a JSON array of objects.

## Config

Configuration settings for pyldraw.

### ldraw_library_path <span class="small">`instance-attribute`</span>

    ldraw_library_path: str = (
        ldraw_library_path
        if ldraw_library_path is not None
        else str(Path(get_cache_dir()) / "complete")
    )

### generated_path <span class="small">`instance-attribute`</span>

    generated_path: str = (
        generated_path
        if generated_path is not None
        else str(Path(get_data_dir()) / "generated")
    )

### load <span class="small">`classmethod`</span>

    load(config_file: str | Path | None = None) -> Config

Load configuration from YAML file or create default configuration.

A missing file yields the defaults; an unreadable or malformed file raises `ConfigLoadError` naming the path and the problem.

### to_dict

    to_dict() -> dict[str, str]

Return public configuration values for serialization.

### write

    write(config_file: str | Path | None = None) -> None

Write the config atomically with a unique sibling temporary file.

## NoGeometryError

Bases: `PartError`

The part (including its subfiles) draws no geometry at all.

### code <span class="small">`instance-attribute`</span>

    code = code

### message <span class="small">`instance-attribute`</span>

    message = message

### source <span class="small">`instance-attribute`</span>

    source: str | None = None

### line_number <span class="small">`instance-attribute`</span>

    line_number: int | None = None

### add_context

    add_context(*, source: str, line_number: int) -> Self

Extend the message with file/line context, at most once.

## PartNotFoundError

Bases: `PartError`

Part was not found as expected.

### code <span class="small">`instance-attribute`</span>

    code = code

### path <span class="small">`instance-attribute`</span>

    path = path

### message <span class="small">`instance-attribute`</span>

    message = message

### source <span class="small">`instance-attribute`</span>

    source: str | None = None

### line_number <span class="small">`instance-attribute`</span>

    line_number: int | None = None

### add_context

    add_context(*, source: str, line_number: int) -> Self

Extend the message with file/line context, at most once.

## UnknownSubmodelError

Bases: `PartError`

The requested submodel name is not in this model's submodel table.

### message <span class="small">`instance-attribute`</span>

    message = message

### source <span class="small">`instance-attribute`</span>

    source: str | None = None

### line_number <span class="small">`instance-attribute`</span>

    line_number: int | None = None

### add_context

    add_context(*, source: str, line_number: int) -> Self

Extend the message with file/line context, at most once.

## part_bounding_box

    part_bounding_box(
        parts: _PartGeometryLibrary, code: str
    ) -> BoundingBox

Axis-aligned bounding box of a part's geometry, in LDU.

Subfiles are resolved recursively and the expanded drawable points are transformed before the box is folded, including under oblique transforms. Unresolvable subfiles are skipped with a warning.

Raises `PartNotFoundError` for an unknown code and `NoGeometryError` when the part draws nothing. Read failures (`OSError`/`UnicodeError`) on the part's own file are tolerated the same way as unresolvable subfiles: the file contributes no geometry, so the query raises `NoGeometryError` rather than the underlying IO error.

## part_studs

    part_studs(
        parts: _PartGeometryLibrary, code: str
    ) -> tuple[StudReference, ...]

All stud primitives a part places, in the part's own coordinates.

Stud groups and subparts are expanded down to individual `stud*` primitives; recursion stops at each stud so nothing is counted twice. Filter with `StudReference.is_top_stud` (or use `Parts.stud_positions`) to keep only upward connectors.

## symbol_description

    symbol_description(description: str) -> str

Return the description that generated symbol names derive from.

Minifig part descriptions drop their `Minifig` prefix so symbols in the `minifig`/`minifig_*` modules read `Torso`, not `MinifigTorso`; every other description passes through unchanged.

## module_path

    module_path(entry: CatalogEntry) -> str | None

Return the generated module path containing `entry`, if any.

## suggested_import

    suggested_import(entry: CatalogEntry) -> str | None

Return an import statement for `entry` in the generated library.

## symbol_name

    symbol_name(entry: CatalogEntry) -> str

Return the generated Python symbol name for a catalog entry.

## symbol_name_for_description

    symbol_name_for_description(description: str) -> str

Return the generated Python symbol for an LDraw description.
