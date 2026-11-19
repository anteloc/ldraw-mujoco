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

`meshes.MeshAssets` registers meshes once per import, keyed by normalized DAT
reference and the linear transform baked into its vertices. Rigid placements
use a body-relative geom pose and the canonical part mesh. An orthogonal
reflection uses a shared X-reflected variant plus a proper rotation. Other
affine matrices are baked in full, including the scale and shear in the
sample's arms and hands. The rigid check allows only floating-point roundoff.
Both vertices and poses use the proper coordinate rotation into MuJoCo and a
length scale of 0.0004 m/LDU.

Each shape has one trimesh convex hull. Every occurrence references it from
a group 3 geom, contributing its own contacts, mass, and inertia. Winding
variants share the same hull.

The hull leaves out faces reached through stud primitives, following
pyldraw3's own rule (a referenced file stem starting with `stud`). A filled
hull cannot receive a stud, so a stud would start 1.6 mm inside the part above
and push it away. Without studs, stacked parts start face to face. Visual
meshes keep their studs. The extreme points of the full surface, studs
included, give the placed bounds and the common ground offset.

Hull geoms have a 0.2 mm contact margin, and the scene enables MuJoCo's
multi-point convex collision (`multiccd`). With one contact point per mesh
pair (MuJoCo's default), a five-high stack of mesh boxes telescoped 39 mm in
1 s, while the same boxes as primitives sank 3 mm. With `multiccd` and the
margin, the mesh stack sank 1.45 mm. The importer's `solver` option (default
`newton`) sets MuJoCo's constraint solver.

Visual meshes group faces by their source color, keeping inherited color 16
as a separate group for per-geom RGBA. Placement-path BFC inversion selects
the visual winding. Visual geoms have zero mass and disabled contacts.
Shell-mode visual meshes support planar patches. A lone triangle is subdivided
in its plane to satisfy MuJoCo's four-vertex minimum.

Each physical group is a world-parented free body at its original anchor with
identity initial orientation. The native compiled model is returned alongside
the editable spec. Changes to the spec take effect on the next compilation.

`ImportedModel.connections` holds pyldraw3's part-local feature tuples for the
selected library DATs, keyed by normalized reference. Reports carry coverage
and diagnostics once per reference. Document-local DATs take precedence over
library names for geometry and retain explicit unqueried connector coverage.

`import_ldraw` works in three phases. It places every occurrence and registers
its meshes, links bodies by their mated connectors (`connections.py`), and only
then builds bodies, parents first, adding each occurrence's geoms. Body
creation waits because a body's parent depends on the connections of all
parts.

## Connections and attachment

`connections.mated_contacts` hands pyldraw3 its own placed occurrences
(`OccurrenceGeometry` in a `ModelInspection`) and calls
`connection_contacts()`, pyldraw3's matcher. Only `confirmed` contacts attach
bodies; heuristic-only matches are counted in the report. Each contact then
becomes a link:

| Mated connectors | Link | MuJoCo |
|---|---|---|
| stud ↔ stud receptacle, rim seat ↔ tyre bead | rigid (clutch, press fit) | child body without a joint |
| axle ↔ axle hole (both cross-sections axle or square) | rigid | child body without a joint |
| pin ↔ pin hole (also an axle in a round hole), bar ↔ clip, hinge fingers | hinge about the first feature's axis | `hinge` joint |
| generic with free placement | ball at the first feature | `ball` joint |
| generic, aligned | rigid | child body without a joint |

LDCad's `slide` option lets an editor slide parts together. It is not a
physical freedom: friction holds the axial position, so links never slide.

All contacts between two bodies combine into one link:

- Any rigid contact makes the pair rigid.
- Hinges stay a hinge only when they are collinear: axes within 2° (pyldraw3's
  angular tolerance) and anchors within 1 LDU of the axis line.
- Balls must share one center. A ball on a hinge axis leaves the hinge.
- Anything else is rigid. Two pins on different axes lock two beams together.

`connections.forest` picks the body trees with Kruskal's algorithm, taking
rigid links first. Rigidly connected bodies therefore form exactly rigid
clusters. A rigid link never closes a loop, and a joint inside one cluster is
locked and dropped. A joint between clusters that other links already join
closes a loop. It becomes a `connect` equality constraint at its anchor, plus a
contact exclusion for the two bodies. Each tree is rooted at its lowest body
index, which in source order is the car rather than one of its wheels. Edges
point away from the root.

The importer builds the trees under the world:

- Roots get a free joint. Children are placed relative to their parent.
- Every body keeps the world orientation at import, so a child's frame is its
  parent's frame shifted to the child's origin.
- Hinge and ball joints sit at the link's anchor and carry
  `frictionloss=joint_friction` (default 0.01 N·m).

MuJoCo already filters the contacts that attachment would otherwise create.
Bodies without joints between them share a weld group and never collide. A
jointed body does not collide with its parent's weld group, which this
experiment confirmed: a hinged child did not collide with a body rigidly
attached to its parent. Wheels therefore turn inside their mudguards' filled
hulls. The price is that a hinged lid can swing through its parent's rigid
cluster, which its joint friction normally prevents.

**Joint friction must be a hard constraint.** At MuJoCo's default friction
impedance (`solimpfriction` 0.9), a constant load makes a joint creep instead
of sticking:

| Hinge friction setup | 12 cm beam, 4.75 N·mm load, tip travel in 5 s | 106-1 car wheels, rotation in 5 s |
|---|---|---|
| Default impedance 0.9 | 72.6 mm | 88–99 mrad |
| Default impedance 0.9, `noslip_iterations=10` | 0.0 mm | 86–99 mrad |
| Impedance 0.999 | 0.73 mm | 0.11 mrad |
| Impedance 0.9999 (`HARD_FRICTION`) | 0.07 mm | 0.007 mrad |

The value of the friction above the load made no difference, so the creep
comes from the soft constraint, not from the friction value. Noslip fixed a
single hinge but not the car's coupled wheels, ground contacts and free root.
The maximum impedance fixes both, so joints use it. A friction limit below the
load still lets the joint swing (a 3 N·mm limit gave 190 mm of tip travel).

### pyldraw3 1.7.0 workarounds

pyldraw3 1.7.0 (the latest release) has three gaps that hide most stud
connections in real models. `connections.py` corrects each one on the placed
features, before pyldraw3's own matcher runs. Each is marked for removal once
pyldraw3 handles it.

1. **Rounded rotations void authored features.** A placement more than 1e-6
   from orthonormal gives LDCad features zero confidence. In 10030-1, 2,959 of
   3,037 placements are rounded by 1e-6 to 1e-2. `_rotation` uses the nearest
   rotation, the SVD polar factor, which keeps reflections, when the source
   matrix is within 1e-2 of it. Real scale or shear stays and still voids the
   features: 106-1's minifigure arms and hands, at 2.9 %, never attach.
2. **LDCad sockets point the other way.** LDCad authors a stud and its socket
   along the same local -Y axis, so a mated pair is co-located and
   co-directional. pyldraw3's strict stud check wants the socket axis opposing
   the stud, like its primitive tube receptacles. As a result only tubes ever
   matched.
3. **Square sockets never seat round studs.** LDCad's 1 × N and 1 × 1 sockets
   are square (`secs=S 6 4`). pyldraw3 mates only identical section shapes.

`_socket` fixes the second and third gap. It reverses an LDCad
`STUD_RECEPTACLE`'s axis with a proper rotation and moves its position to the
other end unless it is centered, so the physical extent is unchanged. It also
turns square sections round.

`_placed` also replaces `inspect_model`'s exact bounds. Those transform every
expanded point in pure Python and took 72 % of its time. `_placed` transforms
the 8 local box corners instead, because the bounds only guide pyldraw3's
search for candidate pairs.

| Model | pyldraw3 as is | With the workarounds |
|---|---|---|
| 106-1, 65 parts | 53 contacts, 37 parts connected | 143 contacts, 59 parts connected |
| 6399-1, 788 parts | not measured | 1,853 contacts, 685 parts connected |
| 10030-1, 3,037 parts | 97 contacts, 73 parts connected, 42 s | 12,646 contacts, 2,832 parts connected, 27 s |

Draft upstream reports (not filed):

- *Strict stud matching ignores LDCad socket direction*: LDCad `SNAP_CYL`
  female stud sockets extend along the same -Y as studs (for example plate
  3022 `[gender=F] [secs=R 6 4] [pos=0 8 0]`). `_strict_stud_candidate`
  requires `-stud.axis·receptacle.axis ≈ 1`, so shadow-only stud pairs never
  match.
- *Round studs never mate square LDCad sockets*:
  `_cylindrical_profiles_compatible` requires the same section shape, but
  LDCad's 1 × N plates and bricks (3710, 3024, 3004 via `s/3004s01.dat`)
  define square `S 6` sockets that accept round `R 6` studs.
- *Authored features are voided by rounded rotations*:
  `_transform_invalidates_metadata` rejects any mismatch or shear above 1e-6,
  which most real models exceed. A tolerance near 1e-2, or snapping to the
  nearest rotation, keeps them. `inspect_model` would also be faster with
  vectorized bounds.

## Instance selection and body boundaries

The inventory is built from pyldraw3's parsed type-1 placements. Enumerate each
section's placements from zero and join their indices with `/` through the
assembly tree. `root` is the model container; `0/46/1` is a particular tyre
inside wheel `0/46` inside car `0`. Repeated uses of a subsection get distinct
paths, even when their ancestor sections are also repeated. DAT references
stop inventory expansion: their internal references supply geometry only.
Empty assembly containers retain IDs but receive no massless free body.

`inspect_ldraw(path)` / `ldraw-mujoco inspect INPUT` returns a JSON inventory
without compiling meshes. It includes all placed nodes with parent IDs,
references, source sections/lines, and source-file hashes. The hierarchy must
resolve and be acyclic. Unplaced definitions appear in `available_sections`
but have no occurrence ID. A standalone DAT gets a synthetic root and part `0`.

`sections=["name.ldr", "106 - wheel assembly.ldr:0/46", ...]` (repeat `--section`) resolves each selector
to an instance ID. A name alone must identify exactly one placed model/submodel;
repeated sections require `section:id`. The section name must match that instance,
and bare IDs are rejected. Ambiguous names list complete `section:id` choices;
unknown/unplaced selections and mismatched names/IDs fail with actionable errors.
Part IDs cannot be used as submodel selectors. Filter physical occurrences by
selected path prefixes, including descendants only once when selections
intersect. Only selected part geometry is resolved and meshed. The full assembly
namespace is still indexed, so missing external assembly files block indexing.

pyldraw3's `Model.iter_occurrences()` composes placements and inherited colors.
Filtering its results preserves the original paths, BFC reference ownership
and source transforms. Selection never creates a standalone definition copy or
renumbers IDs. IDs are scoped to the full source tree/revision, with hashes
recording that revision; editing/regrouping placements can change identities.
This adapts the ldraw-mecha path convention, while deliberately retaining full
input IDs and coordinates when selecting subsets.

By default, group each physical occurrence by its **immediate containing
model/submodel instance ID**. A parent owns only its direct DAT parts. Its
child submodels own their direct parts separately, recursively. Loose root
parts form the root's own group. All resulting bodies have world parents and
free joints: the LDraw tree is source organization, not a MuJoCo body tree.
No equality constraints or inter-body welds are introduced.

`individual_parts=True` / `--individual-parts` instead groups by each physical
part occurrence ID. This single boolean applies to the whole selection; there
are no per-instance overrides or additional grouping modes. Embedded DATs and
library shortcuts remain single physical parts. Geom names contain part IDs;
body names contain their owning instance IDs. Reports map the canonical IDs
to those names and retain the source hierarchy for external callers.

Group origins use the containing section's composed origin (or the part origin
in individual-parts mode). One shared offset brings the lowest selected point
to the requested ground clearance, preserving relative source placements.

## Hold check and performance

The goal is one evaluation right after import: if a model holds still for a
set time (default 5 s), treat it as not crumbling. Viewing is separate and
never runs physics.

`hold(model, seconds=5, tolerance=0.002, settle=0.2)` (CLI: `hold`) works in
three steps:

1. It steps through the settle window. The displacement there is reported as
   `settle_displacement_m` and `settle_body`, but not judged.
2. It takes the settled pose as the reference. Every 10 ms of simulated time,
   it measures each body's largest displacement of any corner of its colliding
   geoms' bounding boxes (`geom_aabb`), so rotations count.
3. It stops at the first body beyond the tolerance, or after `seconds`.

`show(model, data, highlight=...)` opens `mujoco.viewer.launch_passive` on the
result, frames the whole model and tints moved bodies red. It never steps.

Measurements on a 2,175-part garden (MuJoCo 3.5.0, Apple silicon) explain the
design. They were taken with the importer as it was before this change.

| Individual parts, before | Measured |
|---|---|
| Bodies, DoFs | 2,175 free bodies, nv 13,050 |
| Contacts at t=0 | 8,119 contacts, 32,476 constraint rows, one island |
| Hull overlap at t=0 | max 11.2 mm; 2,606 contacts deeper than 0.1 mm |
| `mj_step` with Newton | 6–17 s; 99.9 % in the constraint solver, 16 ms collision |
| `mj_step` with CG | 62–130 ms, always at the 100-iteration cap |
| Rendering, 1280×720 | 1.79 M triangles: 38 ms per frame with shadows, 22 ms without |

- **The viewer ran physics.** `mujoco.viewer.launch` steps in real time and,
  even when paused, calls `mj_forward` about every 1 ms under the lock its
  render thread needs. No frame can be faster than one physics call.
- **Newton on one giant island.** Overlapping hulls linked every part into one
  13,050-DoF island, and Newton refactorizes its Hessian each iteration. CG is
  about 150× faster there. Newton is faster for small or loosely connected
  scenes (41 welded bodies: 2.8 vs 5.1 ms per step; 2,500 separate bricks: 7 vs
  12 ms). The island size depends on contacts, not on nv, so the solver is an
  explicit option, not an automatic rule.
- **Nothing came to rest.** Single-point mesh contacts, stud overlaps and the
  lack of clutch made every part move more than 1 mm within 50 ms. A scene
  that never settles never becomes cheaper to step.
- **`simulate()` doubled the cost** with a second `mj_forward` after each step.
  It now reads positions one step late, refreshes them once at the end, and
  syncs a viewer at most 60 times per second.

Results after this change, for the same garden (wall time of the check after
XML loading):

| Scene | Verdict | Wall time |
|---|---|---|
| Welded, 41 bodies, Newton | crumbles: unattached bamboo stalk moved 3.2 mm right after settling | 3.8 s |
| Individual parts, CG | crumbles: 476 parts beyond 2 mm 10 ms after settling (no clutch) | 38.9 s |

Multi-point contacts raise the individual-parts scene to about 35,000
contacts in 91 islands. CG then needs 0.35–0.41 s per step at the start, and
Newton still needs 13–39 s, so `--solver cg` remains necessary there.

Why settle first: from the import pose, the 1 mm clearance drop plus
soft-contact tilt of large bodies moved 29 of 41 welded bodies more than 2 mm
by t=0.03 s. After 0.2 s of settling, the median body moved 0.6 mm in the next
3 s, and only bodies that really toppled exceeded 2 mm. The cost is that a
part which falls and comes to rest inside the window is not judged. `settle=0`
gives the strict check.

Deferred:

- **Sleep** (`mjENBL_SLEEP`). A resting body that falls asleep makes steps 27×
  cheaper. But a resting brick keeps jittering at about 5e-4 rad/s, above
  MuJoCo's 1e-4 default sleep tolerance, so it never sleeps. A tolerance of
  1e-3 lets it sleep after 0.15 s, but could freeze parts that are about to tip.
- **Lighter rendering.** Turning off shadows or showing only hulls cuts the
  frame time to 22 or 7 ms; the viewer's Rendering panel already offers both.

## Verification and reproduction

106-1 has 65 physical occurrences across 36 part references. Default import
produces seven free bodies: 45 direct car parts, five two-part wheels, and ten
minifigure parts. Thus `nq=49`, `nv=42`, `nbody=8` including the world. The car
selection includes six bodies; one selected wheel instance includes one.
Individual-parts mode produces 65 bodies for the complete input.

```sh
uv sync --locked
uv run python examples/106-1.py
uv run pytest -q --junitxml=output/106-1/tests.xml
uv run ruff check .
```

The example writes portable scenes, import reports, an inventory, initial
views and a `.hold.json` check for each scene. The import report records
input/dependency hashes, versions, attribution, IDs, body/geom mappings,
options, assumptions and shadow diagnostics. Inspect whole and selected scenes
when geometry/body boundaries change.

Tests cover placement-path IDs, repeated ancestors, ambiguity and name/ID mismatch errors, unique
names, multiple/overlapping selections, inherited transforms/colors, independent
child bodies, primitive/embedded DAT boundaries, standalone inputs, winding,
planar color patches, missing/cyclic references, stud-free hulls with studded
visuals, and the solver, multiccd and margin options in the XML round trip.
Hold tests cover a resting part, a falling part with and without settling, a
tipping body, invalid arguments and the CLI exit code. Integration tests verify
sample counts, positive mass/inertia, XML round trips and that the sample gets
a valid verdict. They do not require the sample to hold.

MuJoCo rounds inline XML numbers. Round-trip tests compare geometry to 0.1
micrometer, mass/inertia within serialization tolerances, and free-flight
trajectories under identical forces. Contacts are disabled only in that
trajectory comparison to avoid comparing divergent responses of initially
overlapping convex hulls. Exported scenes retain ordinary contacts. Nearly
symmetric mesh principal-axis frames may differ after compilation, so compare
world geometry rather than those internal frames.

For MCP verification, validate and load the XML, inspect `scene_map` and the
free joints, and step briefly to confirm the artifact runs. The local renderer
supplies inspection images when MCP rendering is unavailable. MCP is optional
for ordinary package use. Use `hold` for the verdict, not the MCP stability
tools: its tolerance, settle window and report are the project's convention.

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

Use `examples/repeated_bricks.py` to reproduce the 10,000-body asset-sharing
check in a fresh process. Its timing covers source loading through native model
compilation. Peak resident memory includes constructing the data and taking one
step with spaced bricks. Dense contact workloads need separate measurements.

Keep the single parts/welded flag for future changes. Mixed per-instance
modes, support contexts, attachments and articulated mechanisms are deferred
until explicitly requested.

The next step for meaningful verdicts is clutch. In real LEGO, a stud holds
only inside a hollow receptacle (shear interlock) plus clutch, in any
orientation, including SNOT side studs. A filled convex hull has no hollow, so
studs cannot be represented there. Two options, to be decided before work
starts:

- Constraints between parts that pyldraw3's connection graph says are
  connected. The graph already detects top and side studs with their frames.
  This reverses the "no attachment inference" rule.
- Convex decomposition with hollow receptacles. This gives geometric interlock
  without inference, but adds a dependency and many more contacts.

Calibrating contacts (stiffer `solref`, zero clearance) belongs with either
option, so that settling stays well below the tolerance and the settle window
can shrink.

The ID convention comes from Carlos Antelo's
[ldraw-mecha](https://github.com/anteloc/ldraw-mecha) documentation (2026,
CC BY-SA 4.0). This implementation adds selection-stable full-input IDs rather
than rebasing to a chosen definition. No neighboring checkout is needed at
runtime.

These notes incorporate lessons from the ldraw-nova project and
[LegoTechnicSimulation](https://github.com/yoff/LegoTechnicSimulation), without
requiring either project at runtime. Operational instructions are included here.
The sample is attributed to Michael Heidemann; source model, parts and shadow
library licenses remain authoritative for those data.
