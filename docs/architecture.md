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
Welded groups have no internal constraints or self-contacts. Every body's initial
orientation is identity; source orientations are already in its local vertices.
One shared ground offset preserves the input's relative positions.

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
in individual-parts mode). Source matrices remain baked into vertices. One
shared offset brings the lowest selected point to the requested ground
clearance, preserving all relative source positions and orientations.

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

The example writes portable scenes, import reports, an inventory and initial
views. The report records input/dependency hashes, versions, attribution, IDs,
body/geom mappings, assumptions and shadow diagnostics. Inspect whole and
selected scenes when geometry/body boundaries change.

Tests cover placement-path IDs, repeated ancestors, ambiguity and name/ID mismatch errors, unique
names, multiple/overlapping selections, inherited transforms/colors, independent
child bodies, primitive/embedded DAT boundaries, standalone inputs, winding,
planar color patches, and missing/cyclic references. Integration tests verify
sample counts, positive mass/inertia and XML round trips. Existing generic
simulation checks remain; there is no requirement to keep assemblies upright
or attached, and no stability decision is produced.

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
for ordinary package use. No stability analysis is required for this increment.

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

Source execution is now a separate layer on the importer, described below.
Mixed per-instance modes, support contexts, stability verdicts, attachments and
articulated mechanisms remain deferred until explicitly requested.

## Interpreter and MCP execution

`Interpreter.open()` imports the full input with `individual_parts=True` and
owns a stdio MCP process for its lifetime. The optional `interpreter` extra pins
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

`undo()` / `undo (u)` undoes one successful step/next/finish/continue
command, including the entire work of a compound command. Before execution,
save a copy of the stack and enabled IDs plus the most recent MCP state response.
Successful commands with events enter the session's undo history; empty completed
operations do not. Undo restores original visibility, gravity compensation and
body/geom contact masks for that enabled set, then uses `sim_set_state` to restore
saved poses and velocities. Every completed trial has the same duration, so its
time is preserved and checked. Undoing all placements uses `sim_reset` to return
to time zero. Undoing a call alone requires no MCP updates. No physics steps run.
The server recomputes contacts and refreshes the viewer. Solver caches and contact
forces are not checkpointed; the next placement still resets to CAD before its
trial. Reset clears history, and undo failures/cancellation halt execution until
reset. The append-only event log includes `undo` records rather than erasing
the commands they undo. Persistent sessions and redo are not implemented.

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
so collision structures are retained. After MCP loads the XML, a batch update
hides every geom, zeros geom and body contact masks, and keeps gravity
compensated. These inactive bodies retain mass and inertia but cannot contact
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

The CLI provides the debugger commands, one-line explanations through `help`,
and an optional server viewer. Headless
operation is fully supported. `Interpreter.open(viewer=True)` selects MuJoCo's
`mjpython -m mujoco_mcp` launcher on macOS. Its environment includes the base
Python `LIBDIR` in `DYLD_FALLBACK_LIBRARY_PATH`, avoiding uv virtual-environment
symlink resolution failures. Other platforms and ordinary headless sessions
use the installed `mujoco-mcp` entrypoint. The pinned server detects native
CGL/GLFW instead of requiring Linux display variables on macOS/Windows.

Opening the viewer enables `sim_step(realtime=True)`. The server synchronizes
the actual slot's model/data approximately every 1/60 simulated second and
sleeps only as needed to pace playback while the window is open. It preserves
the requested number of physics steps and their timestep. Closing the viewer
lets the same simulation finish without pacing. Reopening restores paced
playback. The CAD reset between placements is visible; no alternate simulation
or trajectory playback is involved. Window-launch errors are recorded in
`viewer_error` and the event log. Startup errors include the server log tail.

Interactive input uses prompt_toolkit's async
prompt so Ctrl+C can exit without a blocked input thread. Server stderr is
captured separately in `server.log`. Artifacts include the exact loaded XML and hash,
import evidence, preparation/activation settings, and a flushed JSONL log.
The XML represents the complete collision-capable scene: replay its recorded
initialization to reproduce the empty interpreter state. Reset events separate
runs within one log; a fresh session replaces artifacts in its output directory.

`examples/execute-106-1.py` exercises a car call, a nested wheel, undo, step out and
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
