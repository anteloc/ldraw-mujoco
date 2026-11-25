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
external section names fail explicitly. If an exact DAT reference is absent
from both the document and library, a unique document-local section ending in
` - reference.dat` supplies its geometry. This narrowly handles partially
namespaced MPDs without editing their source. Ambiguous suffix matches fail;
malformed library parts do not trigger fallback. Reports retain the original
reference and IDs, and record `reference_aliases` plus `embedded_dat_alias`
warnings, including aliases encountered inside DAT geometry. Assembly traversal uses
`Model.iter_occurrences()` with embedded DATs excluded from assembly expansion;
a DAT is one physical occurrence even when it contains many primitives.

`geometry.Surfaces` consumes parsed triangles, quads and references. It expands
part geometry in local coordinates, splits each quad into two triangles, and
caches those surfaces by reference. It propagates colors, BFC winding and
INVERTNEXT, and reverses faces for reflected transforms. Lines and conditional
line control points are excluded. Degenerate faces are counted and omitted.
TEXMAP/DATA fail explicitly. Assembly-level inline faces are collected into one
in-memory DAT leaf per section, retaining parsed records and BFC state. Source
files remain unchanged. Existing references stay in their assembly, so they are
not duplicated or absorbed into the generated hull. Each generated occurrence
has an `inline` path suffix (`inline` at root), a null source line and
`generated: inline_faces` in the inventory. Source type-1 IDs stay unchanged.
The generated leaf follows normal grouping/selection and inherits ancestor
transforms, colours and INVERTNEXT. It cannot be edited as a source type-1 line;
edit its parent placement instead. Individual-parts mode treats the face
collection as one rigid part; the default welds it with the assembly’s direct
parts. Like other parts, its points must span a 3D hull (no invented thickness
for planar-only collections).

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

NetworkX is an explicit dependency for trimesh’s hull winding/normal repair
path. MuJoCo handles the hulls' local mesh offsets, inertial frames and
combination into each body's mass distribution. We avoid custom inertia
formulas and signed-volume assumptions about open LDraw meshes.

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

Part geoms use two MJCF default classes, so the exported XML states each
assumption once. `collision` holds the hull settings: group 3, density,
sliding friction, condim and the contact margin. `visual` holds group 0 and
disabled contacts. Each visual geom still carries `mass="0"` itself. MuJoCo
3.5's XML writer drops a zero mass or density from a default class and never
saves `compiler/inertiagrouprange`. Without the per-geom zero mass, a
reloaded scene would weigh visuals at density 1000. The XML round-trip test
catches this.

Each physical group is a body at its original anchor with identity initial
orientation. Bodies without mated connectors are world-parented free bodies;
attached bodies nest under them (see
[Connections and attachment](#connections-and-attachment)). The native compiled
model is returned alongside the editable spec. Changes to the spec take effect
on the next compilation.

`ImportedModel.connections` holds pyldraw3's part-local feature tuples for the
selected library DATs, keyed by normalized reference. Reports carry coverage
and diagnostics once per reference. Document-local DATs take precedence over
library names for geometry and retain explicit unqueried connector coverage.

`import_ldraw` works in three phases:

1. `_place` places every occurrence and registers its meshes.
2. `connections.py` links bodies by their mated connectors.
3. `_build_bodies` builds the bodies, parents first, adding each
   occurrence's geoms.

The rest of `import_ldraw` assembles the report. Body
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

`connections.forest` picks the body trees with Kruskal's algorithm, using
networkx's `UnionFind` and `bfs_edges` in an explicit link order, and taking
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
| Default impedance 0.9 | 72.6 mm | 87–95 mrad |
| Default impedance 0.9, `noslip_iterations=10` | 0.0 mm | 86–99 mrad |
| Impedance 0.999 | 0.73 mm | 0.13–0.16 mrad |
| Impedance 0.9999 (`HARD_FRICTION`) | 0.07 mm | 0.008–0.010 mrad |

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

Matching uses a 0.5 LDU (0.2 mm) tolerance instead of pyldraw3's 0.25 LDU.
Rounded source positions miss the default: a 1 × 4 plate in 6399-1 sits
0.33 LDU off its studs. Studs are 20 LDU apart, so the wider tolerance cannot
pair the wrong stud. It linked 26 more parts in 6399-1, 8 in 10030-1 and none
in 106-1.

| Model | pyldraw3 as is | With the workarounds and 0.5 LDU |
|---|---|---|
| 106-1, 65 parts | 53 contacts, 37 parts connected | 143 contacts, 59 parts connected |
| 6399-1, 788 parts | not measured | 1,903 contacts, 711 parts connected |
| 10030-1, 3,037 parts | 97 contacts, 73 parts connected, 42 s | 12,697 contacts, 2,840 parts connected, 8 s placing + 19–40 s matching |

The 10030-1 matching time varied between runs of the same code.

One gap remains on purpose, because closing it would need matching rules of
our own. pyldraw3's strict stud check wants the stud's base on the receptacle
part's bounding-box face. Recessed sockets fail it even when stud and socket
align exactly, for example 1 × 4 plates mounted sideways (SNOT) onto 6399-1's
part 2672.

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
parts form the root's own group. The LDraw tree is source organization, not a
MuJoCo body tree: bodies nest only by their mated connectors (see
[Connections and attachment](#connections-and-attachment)). With
`attach=False` / `--no-attach`, every body is a world-parented free body and no
constraints are introduced.

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
   `settle_displacement_m` and `settle_body` (`null` when nothing moved), but
   is not judged.
2. It takes the settled pose as the reference. Every 10 ms of simulated time,
   which is one `mj_step(model, data, nstep=…)` call, it measures each body's
   largest displacement of any corner of its colliding geoms' bounding boxes
   (`geom_aabb`), so rotations count.
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
  publishes to its browser viewer about 20 times per simulated second.
- **Attached scenes overflowed MuJoCo's arena.** MuJoCo guesses `mjData`'s
  arena from the DoFs, but its broadphase needs 8 bytes per pair of bodies on
  the arena stack, and a stack overflow is fatal. Free bodies get gigabytes, but
  attachment leaves many bodies with few DoFs. A 2,760-part attached scene
  (nv 78) needed 31 MB of a 19 MB guess, and failed in its first
  `mj_forward`. The importer's `_compile` now raises `<size memory>` to twice
  that need, MuJoCo's 50 % worst-case target. With that, the same scene
  peaked at 30.7 of 60.9 MB and held for 5 s.

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
produces seven bodies: 45 direct car parts, five two-part wheels, and ten
minifigure parts. The wheels hinge on the car's wheel pins and the minifigure
stands free, so `nq=19`, `nv=17`, `nbody=8` including the world (`nq=49`,
`nv=42` with `--no-attach`). The car selection includes six bodies; one
selected wheel instance includes one. Individual-parts mode produces 65 bodies
for the complete input: 8 free roots, 47 rigid children and 10 hinges.

Hold verdicts for 106-1, before and after attachment:

| Scene | Before | Attached |
|---|---|---|
| Full model (default) | crumbles: spare wheel `0/19` fell | holds 5 s, at most 0.02 mm |
| Car only | crumbles: spare wheel fell | holds 5 s |
| Individual parts | crumbles: 18 bodies within 10 ms | 1 body: the scaled left arm `1/5`, which has no connectors |

After 2 s of `simulate`, the attached individual parts keep the car and the
minifigure together; only the scaled arms and hands lie on the ground. The
unattached parts collapse (44 versus 251 final contacts).

The 10,000 spaced bricks of `examples/repeated_bricks.py` have no mates, so
they stay free bodies. Placing and matching their connectors adds 8 s to the
import (105 s versus 97 s) and 50 MiB peak memory (445 versus 395 MiB).

6399-1, 788 individual parts, `--solver cg`, `hold` for 5 s:

| | Attached | `--no-attach` |
|---|---|---|
| Import | 19.0 s | 14.7 s |
| Bodies | 136 free roots, 74 hinges, 9 loops | 788 free bodies |
| DoFs (nv) | 890 | 4,728 |
| Contacts at import | 1,662 | 8,092 |
| Verdict | crumbles: 39 bodies moved | crumbles: 440 bodies moved |
| Check wall time | 3.3 s | 11.9 s |

Of the 39 attached movers, 11 are among the 77 parts without a confirmed mate,
for example grille tiles (2412b). The other 28 are attached: 9 roots of small
groups, 13 parts rigidly attached to them, and 6 hinged parts. With welded
submodels, attachment nests one body; the one submodel that falls does so in
both modes during the settle window (18 mm).

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
tipping body, invalid arguments and the CLI exit code. Connection tests use
synthetic parts with LDCad shadow metas:

- stacked plates attach rigidly, including with rounded rotations and square
  sockets
- a pin in a hole gives a hinge with hard friction and the expected axis
- one pin between two submodels is a hinge, two pins are rigid
- two pins through two beams close a loop that holds in the imported pose and
  survives the XML round trip
- an overhanging plate holds only when attached
- the CLI options, and `forest()`'s ordering, loops and roots

Integration tests verify sample counts, the car's five wheel hinges, positive
mass/inertia, XML round trips (world poses under identical forces), the
individual-parts attachments of tyres, rims and minifigure legs, and that the
sample gets a valid verdict.

MuJoCo rounds inline XML numbers. Round-trip tests compare geometry to 0.1
micrometer, mass/inertia within serialization tolerances, and free-flight
trajectories under identical forces. Contacts are disabled only in that
trajectory comparison to avoid comparing divergent responses of initially
overlapping convex hulls. Exported scenes retain ordinary contacts. Nearly
symmetric mesh principal-axis frames may differ after compilation, so compare
world geometry rather than those internal frames.

For MCP verification, validate and load the XML, inspect `scene_map` and the
joints, and step briefly to confirm the artifact runs. The local renderer
supplies inspection images when MCP rendering is unavailable. MCP is optional
for ordinary package use. Use `hold` for the verdict, not the MCP stability
tools: its tolerance, settle window and report are the project's convention.

## Lessons retained and next steps

The reference work established several useful boundaries: use pyldraw3 instead
of another parser; preserve library/source attribution; distinguish physical
leaves from geometric primitives; and keep connector evidence, geometry,
collision approximations and physical strength as separate claims. Attachment
now follows pyldraw3's confirmed matches only. The LDCad socket conventions
that needed care are handled by the documented workarounds; no matching
heuristics of our own have been added.

The Technic reference demonstrated rigid grouping and representing articulated
mechanisms with body trees and equality constraints. Attachment uses the same
structure. Its reflection mapping and hand-written approximate inertia formulas
were not carried into this importer.

Use `examples/repeated_bricks.py` to reproduce the 10,000-body asset-sharing
check in a fresh process. Its timing covers source loading through native model
compilation. Peak resident memory includes constructing the data and taking one
step with spaced bricks. Dense contact workloads need separate measurements.

Keep the single parts/welded flag and the single `attach` flag for future
changes. Source execution is a separate layer on the importer, described
[below](#interpreter-and-mcp-execution). Mixed per-instance modes and support contexts are deferred until
explicitly requested.

A cleanup pass on 2026-11-25 left behaviour unchanged: reports, hold
verdicts and compiled models were identical for every 106-1 scene. It
changed four things:

- the code reuses networkx and the `nstep` stepping of MuJoCo's Python
  bindings;
- geoms use default classes;
- `import_ldraw` is split into phases;
- pyldraw3 pieces and models are keyed by identity instead of `id()`.

The interpreter was out of scope. Its `_replace_scene` still swaps state
with `self.__dict__.update(candidate.__dict__)`. Moving the per-scene state
(XML, model, masks, slot, preparation) into a small `Scene` object would make
edit and undo swap one attribute. That change needs the interpreter tests to
stop reaching into private members.

Attachment was the chosen answer to clutch. Studs that pyldraw3 confirms as
mated, in any orientation including SNOT, now hold their parts rigidly.
Convex decomposition with hollow receptacles was the alternative; it remains
unneeded. Next steps, in order of expected value:

- **Breakable clutch.** Rigid links never break. To limit them, turn a link
  into a `weld` equality constraint and deactivate it (`eq_active`) when its
  force exceeds a clutch limit. Set the weld's `data` explicitly: MjSpec's
  default puts the anchor at (0, 1, 0), 1 m away.
- **Per-part friction.** One friction torque serves all joints, so the car's
  wheels need a push to roll while some heavy arms may still swing. Free
  wheels versus friction pins would need part-level data, which the connector
  metadata does not carry.
- **Slides.** LDCad's `slide` is ignored. Slide joints need axial limits from
  the overlap of the mated features, or a part slides out of its hole.
- **Faster matching.** pyldraw3's matcher is pure Python: 19–40 s for 3,000
  parts. `--no-attach` skips it.
- **Upstream fixes** for the three pyldraw3 gaps (drafts above). Each fix lets
  one workaround in `connections.py` go.

Calibrating contacts (stiffer `solref`, zero clearance) still lets settling
stay well below the tolerance, so that the settle window can shrink.

## Interpreter and MCP execution

`Interpreter.open()` imports the full input with `individual_parts=True` and
`attach=False`, so every placement is one free body, and owns a stdio MCP
process for its lifetime. The optional `interpreter` extra pins
the server to `3e249d3834322c49bf611e48903dd54871823de8`, the MCP SDK to 1.26.0,
and retains MuJoCo 3.5.0. The executable comes from the project environment;
editable server installations are rejected. No neighboring checkout is imported
or launched. Existing conversion and local simulation APIs remain independent.

The ordered inventory supplies instructions and their parent/child links;
there is no new record parser or transform composer. Source-file provenance is
included alongside section and line in inventory nodes. The interpreter keeps
a stack of occurrence IDs and next-instruction indices. A submodel instruction
pushes a frame, while exhausting its children implicitly returns. Repeated
definitions have separate occurrence frames. DATs stop execution traversal.
Empty calls produce a call event and return immediately.

Step into executes one instruction. Step over finishes the next call at its
original stack depth. Step out finishes the current frame; at root it finishes
the program. Run executes until the stack empties. All operations use the same
instruction executor and produce ordered call/placement events. Call events
have no physics observation or source-language return value. Completed programs
allow harmless further stepping.

`undo()` / `undo (u)` undoes one successful step/next/finish/continue or edit
command, including the entire work of a compound command. Before execution,
save a copy of the stack and enabled IDs plus the most recent MCP state response.
Successful commands with events enter the session's undo history; empty completed
operations do not. Undo restores original visibility, gravity compensation and
body/geom contact masks for that enabled set, then uses `sim_set_state` to restore
saved poses and velocities. Every completed trial has the same duration, so its
time is preserved and checked. Undoing all placements uses `sim_reset` to return
to time zero. Undoing a call alone requires no MCP updates. Undoing execution
commands runs no physics steps; undoing edits rebuilds the old scene as below.
The server recomputes contacts and refreshes the viewer. Solver caches and contact
forces are not checkpointed; the next placement still resets to CAD before its
trial. Reset clears history, and undo failures/cancellation halt execution until
reset. The append-only event log includes `undo` records rather than erasing
the commands they undo. Persistent sessions and redo are not implemented.

`edit <part id>` stages a full placement line using prompt_toolkit. Its type marker and colour
are a non-editable prompt; the reference is a read-only suffix. Only the twelve
position/matrix values are in the input buffer. Tab/Shift+Tab navigate those
fields. An immediately preceding `0 // …` source comment is read-only context. Field-level UI validation supplies caret offsets and
repair suggestions, while pyldraw3's `parse_ldraw_line` parses the actual record.
Syntax errors retain the draft and return focus to the first failing field after
the user chooses to correct it. Cancelling discards only the current draft.

The importer accepts `placement_overrides`, mapping type-1 occurrence IDs to
replacement type-1 lines. It expands a private chain of the occurrence's ancestor
placements through pyldraw3, preserving inherited colours, affine transforms,
source provenance and BFC ownership. It never mutates a shared source submodel or
writes the source files. Colour and references cannot change, so part IDs and call frames
stay valid. Editing a submodel placement affects only that instance and its descendants. Inventories include `source_text`, showing the effective line for
each occurrence. Source/dependency hashes remain hashes of the original files;
reports retain the overrides and the execution XML hash scopes the edited scene.

An accepted edit prepares the full scene in a spare MCP slot, reapplies the
enabled set, and evaluates one CAD trial. The current scene is replaced only
after preparation succeeds. Two slot names alternate, bounding server model
storage even after repeated edits. The browser assets are replaced while keeping the camera;
rendering failures do not prevent terminal execution. Edits checkpoint the exact
previous XML, report, line overrides, call stack, enabled IDs and live state.
Undo rebuilds from that saved XML and restores the saved poses/velocities after
initializing the trial's time. It removes the checkpoint without creating a new
edit, stopping at the original source revision when all edits have been undone.
Reset clears all undo history but keeps current overrides. Old scene/report
artifacts are retained in `revisions/<xml hash>/`; the existing event log appends
edit/undo records instead of being reset when a scene changes.

`inspect()` / `inspect (i)` uses the same observation helper as placements:
`sim_forward` refreshes derived quantities without stepping, `sim_get_state`
reads current poses/velocities/time, and `analyze_contacts` requests the full
reported contact count. Dimension and contact-count checks reject incomplete
responses. Every reported body has an occurrence `id`, and every contact maps
both geoms to occurrence IDs (`null` for ground); unknown geoms are rejected.
Inspection reports live state rather than the last placement's cached trial.
It returns JSON-ready data with the XML hash, SI units, contact-force frame and
debugger status, and logs a separate `inspect` record. It does not update the
undo history, instruction pointer, cached trial state or `last_result`. Query
errors/cancellation release the busy guard without halting execution. Inspection
of an already halted program requires reset, since partially applied changes
may disagree with the interpreter's enabled-part list.

The execution XML retains every mesh and free body. Before exporting it, set
gravity compensation on every part so MuJoCo initializes its compensation
bookkeeping at compilation. Keep collision masks enabled during compilation
so collision structures are retained. The interpreter retains a canonical
`scene.xml` and derives `bootstrap.xml` with only the runtime contact flag
disabled. The headless MCP server loads that file by path; its automatic
`mj_forward` cannot solve contacts for the assembled model. A first batch
hides every geom, zeros geom and body contact masks, and keeps gravity
compensated. Only after that batch succeeds does a separate option update
restore the exact original disableflags. A failed update cannot re-enable
contacts prematurely. This same sequence handles edit/undo candidate scenes.
Without an output directory, bootstrap files live in an owned temporary
directory for the duration of loading. These inactive bodies retain mass and inertia but cannot contact
the enabled assembly. Do not zero masses or edit free-joint topology.

For each part, `sim_reset` restores all poses, velocities, warmstarts and time.
Model-field changes survive that reset, so earlier parts stay enabled. A batch
`modify_model` restores the new part's original RGBA and contact masks, updates
its body's aggregate masks, and disables its compensation. Body masks must
match the bitwise OR of their attached geom masks. Changes are followed by MCP
`sim_step`, `sim_forward`, state queries, and an untruncated contact query.
Time advancement occurs only in the server. This follows the runtime rules in
[MuJoCo's model-change reference](https://mujoco.readthedocs.io/en/3.5.0/programming/simulation.html#mjmodel-changes).

Each trial starts at CAD, with the accumulated enabled set, rather than carrying
the previous trial's motion forward. The default observation window is 100 ms;
requested duration rounds up to whole timesteps. No attachment constraints or
success verdicts are introduced. Results expose final poses, native free-joint
velocities, displacement, contact measurements, duration and state finiteness.
Native angular free-joint velocities are in the body frame. Server warning
counters and intermediate numerical checks are not exposed by the tools used
here; final-state observations must not be described as a full numerical audit.
Global energy would include dormant masses, so it is intentionally omitted.

The MCP adapter checks required tools and MuJoCo version and decodes structured
or textual JSON responses. Tool-level errors and individual failed modification
entries halt execution. A partially applied update is not rolled back or
automatically retried. The failing instruction and completed events remain in
the exception/result/log; reset reapplies all inactive settings before rewinding.
Cancellation also marks execution halted. Concurrent debugger operations are
rejected. Exiting the context closes the owned process and its viewer.

The CLI provides debugger commands and a separate browser inspection service.
`viewer.BrowserViewer` uses pinned Viser 1.1.1: its wheel supplies the client,
WebSocket transport, camera controls and batching. The service binds loopback
only and disables sharing. Both commands use the ordinary Python launcher;
MCP runs with `MUJOCO_MCP_NO_RENDER=1` and never owns a viewer or GL renderer.

Browser geometry comes from compiled visual mesh vertices/faces and geom-local
transforms; native primitives use trimesh tessellation. Collision hulls stay
hidden. Identical geometry shares a batched mesh; per-instance colour, opacity,
and transforms remain distinct. There is no mesh simplification or additional
LDraw parser. Unsupported visual types fail viewer preparation explicitly while
leaving physics available. The view uses Z-up metres. Separate render MjData
receives only qpos and `mj_kinematics`, never forward dynamics or stepping.
Unplaced bodies use their initial CAD transforms and 15% of their original
opacity; ghosting does not modify the simulation model. Accepted edits rebuild
assets on the existing service; rejected edits preserve the previous view.

Connected execution uses roughly 50 ms chunks of the same native simulation
steps and publishes each returned qpos. Wall-clock pacing happens in the client,
not the MCP viewer. Chunks never change timestep or total steps; disconnected
runs use the ordinary larger batches. Reset, undo and replacement publish exact
current state without stepping. Browser camera input and reconnection are
handled by Viser's separate server thread, independent of simulation calls.

`simulate --viewer` uses the same presentation adapter with every body active.
It publishes the initial picture before forward dynamics; genuine expensive
contact solves remain possible, but do not freeze camera interaction. The
simulation loop publishes about 20 times per simulated second and continues
if the browser closes or fails. The CLI owns the service through report/snapshot
saving and final interactive inspection (Enter/Ctrl+C to close). Noninteractive
runs and Python `simulate(viewer=True)` close the service upon completion.
The viewer offers only inspection controls; terminal commands own physics.

Interactive input uses prompt_toolkit's async
prompt so Ctrl+C can exit without a blocked input thread. Server stderr is
captured separately in `server.log`. Artifacts include canonical and bootstrap XML with hashes, restored option
flags, phase timings, import evidence, activation settings, and a flushed JSONL log.
The XML represents the complete collision-capable scene: replay its recorded
initialization to reproduce the empty interpreter state. Reset events separate
runs within one log; a fresh session replaces artifacts in its output directory.

`examples/execute-106-1.py` exercises a car call, a nested wheel, editing, undo, step out and
completion. It saves current physics inspections and exact remote states,
rendering them locally without stepping when server graphics are unavailable. Continuation checks should
include debugger/cancellation/error tests, real stdio integration, mass and mask
invariants, reset-before-each-placement behavior, and whole/affected-assembly
images. To run the complete test suite with the transport installed, use
`uv run --extra interpreter pytest -q`; without the extra the real stdio test skips.

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
