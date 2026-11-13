# Import architecture and continuation notes

## Why one MjSpec builder

| Approach | Advantages | Costs |
|---|---|---|
| Generate MJCF first | Readable artifact; easy viewer/MCP loading; reproducible input | XML generation and asset handling; changes require regeneration |
| Build MjSpec in Python | Directly consumes parsed geometry; editable before compilation; convenient experiments | Depends on the construction API; still needs explicit physics modeling |
| Selected: MjSpec with MJCF export | One implementation serves Python and portable-file workflows | Round-trip validation is needed |

Both routes compile through MuJoCo's model specification, so neither supplies
more accurate physics by itself. We pin MuJoCo 3.5.0 and pyldraw3 1.7.0 and
test both routes. Inline mesh arrays allow one XML file to contain the complete
scene; the exported XML has no runtime dependency on LDraw libraries.

## Data flow

`library` builds a cached read-through library view and calls pyldraw3's index
generator. `Parts.add_connection_shadow()` loads the local shadow library or
explicitly selected alternatives. Original data is read-only.

`geometry.Document` uses pyldraw3 to parse source documents and resolve their
namespace. External local LDRs and embedded DATs are supported. Ambiguous
external section names fail explicitly. Assembly traversal uses
`Model.iter_occurrences()` with embedded DATs excluded from assembly expansion;
a DAT is one physical occurrence even when it contains many primitives.

`geometry.Surfaces` consumes parsed triangles, quads and references. It expands
part geometry in local coordinates, splits each quad into two triangles, and
caches those surfaces by reference. It propagates colors, BFC winding and
INVERTNEXT, and reverses faces for reflected transforms. Lines and conditional
line control points are excluded. Degenerate faces are counted and omitted.
TEXMAP/DATA and assembly-level inline faces fail explicitly in this version.

`importer` bakes placement matrices into vertices. This preserves scale/shear
in the sample's arm and hand placements without claiming they are rigid
rotations. The orthogonality warning records this approximation. The coordinate
rotation has determinant +1 and maps `(x,y,z)` to `(x,z,-y)`; all lengths then
scale by 0.0004. Using `(x,-z,-y)` would mirror the source.

Visual faces are grouped by effective RGBA, preserving geometry-based patterns
and transparency. These meshes use shell inertia mode to permit planar patches
but contribute no mass. An isolated triangle is subdivided without changing its
surface, because MuJoCo requires at least four mesh vertices.

trimesh constructs one convex hull per physical occurrence. Only these hulls
contribute contacts, mass and inertia. MuJoCo handles their local mesh offsets,
inertial frames and combination into each body's mass distribution. We avoid
custom inertia formulas and signed-volume assumptions about open LDraw meshes.

Each chosen group becomes a free body with all its geoms attached directly.
No internal constraints or self-contacts are required. Every body's initial
orientation is identity; source orientations are already in its local vertices.
One shared ground offset preserves the input's relative positions.

## What the PoC measures

The 106-1 sample has 65 occurrences of 36 distinct part references, including
five rim/tire pairs. Top-level grouping produces the car (55 occurrences) and
the minifigure (10), with two free joints: `nq=14`, `nv=12`, `nbody=3` including
the world. Library shortcuts remain single occurrences.

The model estimates mass with a uniform density of 1050 kg/m³ over convex hull
volumes. Hollow bricks become solid hulls, rim and tire volumes overlap, and
internal studs may overlap neighboring hulls. Mass and center of mass therefore
need calibration before quantitative predictions. There is one uniform sliding
friction coefficient; no rubber-specific calibration is implied.

The simulation reports contact pairs and normal forces, maximum penetration,
energy, displacement, maximum translational speed and maximum tilt from the
world +Z axis. Tilt is an observation, not a stability verdict. The runner checks
finite state, time resets and MuJoCo warnings on every step. It samples motion
every 0.1 seconds. Interactive runs stop and report incompleteness if the viewer
is closed early.

With default soft contacts, the sample's five-second run settled upright with
14 final contacts and no numerical warnings. Maximum transient penetration was
approximately 1.24 mm. This is a material limitation at LEGO scale: use the
contact reports when tuning solver parameters or calibrating geometry, rather
than interpreting the rendered contact surface as exact.

## Verification and reproduction

```sh
uv sync --locked
uv run python examples/106-1.py
uv run pytest -q --junitxml=output/106-1/tests.xml
uv run ruff check .
```

The example writes a self-contained scene, import report, five-second simulation
report, initial/final views and isolated car/minifigure views. The import report
records source authors/licenses, input geometry SHA-256 hashes, dependency
versions, occurrence paths, named geoms, assumptions and connector diagnostics.

Tests cover nested/repeated models, inherited colors, DAT boundaries, mirrored
and affine transforms, drawing controls, planar colored patches, missing/cyclic
references, standalone inputs, gravity, friction and tipping. Integration tests
compare direct compilation with reloaded XML and run the full sample.

MuJoCo's XML writer rounds inline numeric data. Round-trip tests compare world
geometry to 0.1 micrometer and use small tolerances for contact-sensitive
trajectories. Internal principal-axis mesh quaternions are not an appropriate
identity check: nearly symmetric geometry can change those axes slightly.

For MCP verification, load `output/106-1/scene.xml` with `validate_mjcf` and
`sim_load`, inspect `scene_map`, advance `sim_step(n_steps=5000)`, then query
`analyze_contacts` and `analyze_energy`. The MCP server used for this PoC runs
MuJoCo 3.5.0 without rendering; the local renderer supplies inspection images.
The package does not depend on MCP for ordinary operation.

## Lessons retained and next steps

The reference work established several useful boundaries: use pyldraw3 instead
of another parser; preserve library/source attribution; distinguish physical
leaves from geometric primitives; and keep connector evidence, geometry,
collision approximations and physical strength as separate claims. LDCad female
socket frame conventions and pyldraw3 1.7's inferred connector classifications
need care before connection matching is used to create joints. No matching
heuristics or uncalibrated attachment forces have been added here.

The Technic reference demonstrated rigid grouping and representing articulated
mechanisms with body trees and equality constraints. Those mechanisms are a
later extension. Its reflection mapping and hand-written approximate inertia
formulas were not carried into this importer.

The next useful increment is four explicit wheel hinges while retaining a
fixed spare wheel. After that, add measured masses/friction, selected collision
decompositions, and reviewed connections with explicit force semantics. Keep
those as separate steps with tests and evidence; do not infer the complete
mechanical structure from MPD hierarchy or bounding-box overlap.

These notes incorporate lessons from the ldraw-nova project and
[LegoTechnicSimulation](https://github.com/yoff/LegoTechnicSimulation), without
requiring either project at runtime. Operational instructions are included here.
The sample is attributed to Michael Heidemann; source model, parts and shadow
library licenses remain authoritative for those data.
