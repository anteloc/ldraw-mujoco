# LDraw in MuJoCo

Import `.mpd`, `.ldr` and `.dat` files as submodel bodies or individual
physical parts, attached where their LDraw connectors mate: studs hold
rigidly, pins, clips and hinges turn. One pyldraw3 → `MjSpec` builder
supports Python and self-contained MJCF export.

## Quick start

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/), a local LDraw parts
library in `data/ldraw`, and the supplied `data/offLibShadow`. The library must
contain `parts/`, `p/` and `LDConfig.ldr`; its index is generated in `.cache/`
without modifying source files. No downloads occur during import.

```sh
uv sync --locked
```

In Python, import the complete model, check once that it holds still, then look
at the result. The importer resolves geometry and library connectors, attaches
the parts whose connectors mate, builds an editable `MjSpec`, and compiles it
once in memory.

```python
from ldraw_mujoco import import_ldraw
from ldraw_mujoco.simulation import hold, show

result = import_ldraw("data/models-annotated/106-1.mpd")
data, report = hold(result.model, seconds=5)
moved = [body["name"] for body in report["moved_bodies"]]
print("holds" if report["holds"] else f"crumbles: {moved}")
show(result.model, data, highlight=moved)  # Static view; moved bodies in red.
```

`hold` steps the physics once, headless and as fast as possible, and stops as
soon as the verdict is known. `show` opens MuJoCo's viewer on that result
without stepping, so it stays responsive with thousands of parts. On macOS,
run such scripts with `mjpython` (see [the viewer notes](#optional-simulation-and-configuration)).
`mujoco.viewer.launch(model)` instead runs physics continuously, even while
paused: fine for 106-1, unusable for thousands of touching parts.

For your own headless loop, call `mujoco.mj_step(model, data)` directly. After
editing `result.spec`, call `result.spec.compile()` to obtain a new model and
create matching `MjData`. Use `result.spec.to_xml()` for a portable scene.

To list instance IDs, export, and check the exported scene from the command line, run

```sh
uv run ldraw-mujoco inspect data/models-annotated/106-1.mpd
uv run ldraw-mujoco convert data/models-annotated/106-1.mpd \
  --output output/106-1/scene.xml
uv run ldraw-mujoco hold output/106-1/scene.xml --snapshot output/106-1/held.png
```

`inspect` prints a JSON inventory of all placed parts and submodels, including
IDs, parent IDs and source lines. It needs the source model and its external
submodel files, but no parts library or mesh compilation. `convert` writes
portable XML with inline meshes and a neighboring `.import.json` report.
`hold` writes `scene.hold.json` and exits with 0 when the scene holds, 1 when
it does not (see [Hold check](#hold-check)).

## IDs and selecting instances

IDs use **zero-based type-1 placement indices through the full input tree**.
For 106-1, `0` is the car, `0/46` is one wheel assembly, and `0/46/1` is its
tyre. Identical parts at different placements have different IDs. Comments,
STEP lines and geometric primitives do not count as placements. `root` names
the input model itself; a standalone DAT has one physical occurrence, `0`.

IDs remain unchanged when selecting subsets or toggling individual-parts mode.
They identify occurrences in a particular source tree, not permanent part
identities across source edits. Keep the source/dependency hashes from the
inventory or import report alongside IDs.

Use `--section SECTION[:ID]` to select an instance and its descendants:

- A subsection name is accepted only when it has **one placed instance**.
- Repeated subsections require **`section:id`**, even when the repetitions
  come from repeated ancestors. An ambiguous name lists complete selectors.
- Repeat `--section` to include several instances, including different submodels.
- Selecting a parent and its child includes each occurrence only once.
- An unplaced definition cannot be selected; no standalone copy is invented.

```sh
# One uniquely named car instance, including its child submodels.
uv run ldraw-mujoco convert data/models-annotated/106-1.mpd \
  --section "106 - car.ldr" --output output/106-1/car.xml

# One specific wheel and the uniquely named minifigure.
uv run ldraw-mujoco convert data/models-annotated/106-1.mpd \
  --section "106 - wheel assembly.ldr:0/46" --section "106 - Minifig.ldr" \
  --output output/106-1/selection.xml
```

Selecting `106 - wheel assembly.ldr` by name is ambiguous: its IDs are
`0/19`, `0/46`, `0/47`, `0/48` and `0/49`. Use, for example,
`"106 - wheel assembly.ldr:0/46"` to select one. Bare IDs are not accepted.
Names are case-insensitive, and a qualified name must match its instance: the
minifigure is `"106 - Minifig.ldr:1"`, not `"106 - Minifig.ldr:0/46"`.
All selected geometry keeps its composed source placement and inherited colors.
One shared vertical offset puts the lowest
selected point 1 mm above ground; relative placement is preserved.

## Welded or individual parts

There is one grouping switch for the entire import operation:

| Mode | Result |
|---|---|
| Default | Each model/submodel instance's **direct parts** share one rigid body. A child submodel is a body of its own. |
| `--individual-parts` | Every included physical part occurrence gets its own body. No parts are welded together. |

An assembly containing only child submodels remains an identified container;
it gets no empty physics body. Loose parts directly under the root share its
body. A flat model without submodels therefore imports as one body by default.
“Welded” means attaching geoms to the same body. Sections never decide how
bodies attach to each other: their mated connectors do (see
[Connections](#connections-studs-pins-and-hinges)). Bodies without mated
connectors have free joints under the world.

For 106-1, default import gives **seven bodies**: car direct parts (45), five
wheel assemblies (2 each), and minifigure (10). The wheels turn on the car's
wheel pins; the minifigure stands free. Importing only the car gives six
bodies. Individual-parts mode gives 65 bodies for the full model, 55 for the
car, or two for a selected wheel instance.

```sh
# Individual parts throughout the full model, attached by their connectors.
uv run ldraw-mujoco convert data/models-annotated/106-1.mpd \
  --individual-parts --output output/106-1/parts.xml

# The same switch applies to every selected instance and all descendants.
uv run ldraw-mujoco convert data/models-annotated/106-1.mpd \
  --section "106 - wheel assembly.ldr:0/46" --section "106 - Minifig.ldr" --individual-parts \
  --output output/106-1/selection-parts.xml
```

Physical parts are the placed library DATs, including shortcuts and embedded
DATs. A brick's studs, faces, primitives and geometric subparts stay within
that brick. Selection and welding never split them into separate bodies.

The earlier `grouping` API and `--grouping` modes have been removed. Use
`individual_parts=True` / `--individual-parts` for one body per part; omit it
for one body per submodel instance, including nested ones.

## Connections: studs, pins and hinges

By default, bodies attach where pyldraw3 confirms that their connectors mate.
Connector features come from library primitives and the LDCad shadow library
(`data/offLibShadow`). Each mated pair becomes the MuJoCo equivalent:

| Mated connectors | MuJoCo |
|---|---|
| Stud in a stud receptacle, tyre on a rim, axle in an axle hole | Rigid: a child body without a joint |
| Pin or axle in a round hole, bar in a clip, hinge fingers | Hinge joint about the connector axis |
| LDCad generic connector with free placement (ball sockets) | Ball joint at the connector |

Connected bodies form one tree under a free root. Two connectors on different
axes, such as two pins, hold two bodies rigidly. A hinge or ball joint that
would close a loop becomes a `connect` equality constraint with a contact
exclusion. MuJoCo does not compute contacts between bodies that are rigidly
attached, nor between a jointed body and its parent.

```sh
# Independent free bodies, as before attachment existed.
uv run ldraw-mujoco convert data/models-annotated/106-1.mpd \
  --individual-parts --no-attach --output output/106-1/parts-free.xml

# Joints that swing freely; the default 0.01 N·m holds poses.
uv run ldraw-mujoco convert data/models-annotated/106-1.mpd \
  --joint-friction 0 --output output/106-1/free-joints.xml
```

In Python, use `attach=False` and `joint_friction=...` (N·m). The report adds:

- `bodies[].parent` and `bodies[].joint` (`free`, `rigid`, `hinge`, `ball`).
- `links`: each attachment's bodies, kind, anchor and axis in meters, contact
  count, and the part IDs that carry it. `constraint` is `tree` for the body
  tree and `loop` for equality constraints.
- `connections`: contact counts by status and connector kind, and
  `unlinked_parts`, the parts without a confirmed mate.

The modeling is deliberately simple:

- Rigid links never break: there is no clutch limit.
- Every hinge and ball joint has the same uncalibrated friction torque, held
  without creep, so posed hinges and limbs stay put while wheels need a push.
- LDCad's `slide` option is an editing aid, not a physical freedom, so links
  never slide.
- Only connectors that pyldraw3 confirms count; heuristic matches are reported
  but not used.
- Parts placed with real scale or shear have no connectors, as pyldraw3 rules.

For 106-1, 59 of 65 parts attach. The minifigure's hair, arms and hands, and
one ladder plate, have no confirmed mate. The source scales the arms and hands.

## Shared meshes and connectors

Repeated placements share part-local visual meshes and a convex hull within
one import. Each geom has its own pose and color. A red brick and a blue copy
can therefore use the same visual mesh. Scale, shear, and reflections are baked
into mesh variants. The report's `nmesh` counts the compiled mesh assets.

Look up the connector features for a placed library part in the Python result:

```python
tyre = next(o for o in result.report["occurrences"] if o["id"] == "0/46/1")
ref = tyre["reference"].replace("\\", "/").casefold()
features = result.connections[ref]  # Tuple of pyldraw3 ConnectionFeature objects
coverage = result.report["connection_metadata"][ref]["coverage"]
```

Positions and profile dimensions are in part-local LDU. Each feature carries
its frame, kind, role, and available provenance. The occurrence's
`matrix_ldraw` and `position_ldu` place it in the source assembly. Apply the
coordinate mapping and `scene_offset_m` to locate the point in the initial
MuJoCo scene. A queried library part can have an empty tuple. Embedded and
other document-local DATs have `not_queried` coverage and no dictionary entry,
so they never attach. MuJoCo computes contacts from the placed collision geoms.

The report's `instances` list identifies included model/submodel/part nodes
and their bodies (`null` for containers without direct geometry). `occurrences`
adds part IDs, transforms and geom names; `bodies` maps each body to its owning
`instance_id`. `selected_instances` records the resolved IDs (such as `0/46`). Names of
bodies/geoms derive from full-input IDs, so selection does not renumber them.

## Hold check

A model **holds** when, after a short settling window, no body moves more than
the tolerance for the whole duration. Run it once, right after importing:

```sh
uv run ldraw-mujoco hold SCENE.xml --seconds 5 --tolerance 0.002 --settle 0.2
```

- Movement is the largest displacement of any corner of a body's collision
  bounding boxes, checked every 10 ms of simulated time. Rotations count.
- The check stops at the first body beyond the tolerance (it crumbles), so a
  failing model answers quickly. A holding model runs the full duration.
- The first `--settle` seconds are reported but not judged. Contacts are soft:
  the scene drops its 1 mm import clearance and sinks into its contacts, which
  alone can move large bodies about 2 mm. A part that falls and comes to rest
  inside this window is not judged; `settle_displacement_m` and `settle_body`
  show it. `--settle 0` checks strictly from the import pose.
- The report lists `moved_bodies` by name and displacement. `--viewer` then
  shows the result with those bodies in red, and `--snapshot` saves it as PNG.

A verdict reflects the approximations below and the attachment rules above.
Parts stay together only through their mated connectors, which never break.
A part without a confirmed mate is held by nothing but contacts: studs alone
give no interlock, so such parts fall when only studs held them. "Holds" is
therefore not proof of real-world stability.

For 106-1, the full scene and the car hold for 5 s; before attachment, the
spare wheel fell off. With individual parts, one part moves instead of 18: the
scaled left arm, which has no connectors.

Measured on a 2,175-part garden: the welded import (41 bodies) answers in 4 s,
and individual parts with `--solver cg` in 39 s. With the default Newton
solver, one step of the individual-parts scene takes 13–39 s. See
[architecture notes](docs/architecture.md#hold-check-and-performance).

## Execute LDraw instructions through MCP

The optional interpreter treats model/submodel references as subroutine calls
and physical DAT references as part placements. It uses the existing parser
and full-input IDs; a DAT's internal primitives are never instructions.

```sh
uv sync --locked --extra interpreter
uv run --extra interpreter ldraw-mujoco execute data/models-annotated/106-1.mpd

# Open the browser viewer and watch each placement's physics.
uv run --extra interpreter ldraw-mujoco execute data/models-annotated/106-1.mpd --viewer
```

The interpreter starts its own stdio MuJoCo MCP process from the installed
project environment. The extra pins the server source revision, MCP SDK and
MuJoCo version. It has no runtime dependency on another checkout or the MCP
process connected to an assistant. Ordinary import/conversion needs no extra.

| Terminal command | Python method | Effect |
|---|---|---|
| `step` / `s` | `step_into()` | Execute a DAT placement or enter a submodel. |
| `next` / `n` | `step_over()` | Execute a DAT placement or an entire submodel call. |
| `undo` / `u` | `undo()` | Undo the last execution command or edit. |
| `finish` / `f` | `step_out()` | Finish the current submodel; at root, finish the program. |
| `continue` / `c` | `run()` | Finish the program. |
| `inspect` / `i` | `inspect()` | Return current physics as JSON, with part IDs. |
| `edit` / `e` `<part id>` | `edit(id, line)` | Edit one occurrence's type-1 line for this session. |
| `where` / `w` | `status` property | Show the stack and next instruction. |
| `reset` / `r` | `reset()` | Disable all parts, rewind, and clear undo history. |
| `help` / `h` | — | Show each command with a brief explanation. |
| `quit` / `q` | — | Close the owned viewer and server. |

Every DAT placement enables one free body. Before each evaluation, **all enabled
parts return to their original CAD poses with zero velocity**. Physics then
runs for 100 ms, rounded up to whole timesteps. Change this with
`--seconds-per-part` or `seconds_per_part=`. Each trial starts at time zero;
motion from the previous evaluation is not carried into the next placement.
The full input's common ground offset remains fixed until an edit rebuilds the scene.

Entering a submodel changes only the call stack. Returning is implicit, with
no subroutine return value. Step over/out still evaluate every contained DAT
placement and retain every observation. Empty submodels return immediately.

`undo` restores the stack, enabled parts, poses and velocities from before
the last execution command. For example, `next` on a submodel followed by `u`
undoes that whole call. Repeating `u` walks further back, including after program
completion. It does not run physics backward or advance time. `help`, `where`
and `inspect` do not affect history; `reset` clears it. With no history, `u` does nothing.
You can execute forward again after undoing. History lasts only for this session;
execution failures still require `reset` or reopening.

Use `edit 0/19/0` (or `e 0/19/0`) to edit a type-1 placement, including a
submodel instance. Only x/y/z and the nine rotation-matrix values are editable.
The leading `1`, colour and part/submodel reference are fixed. An immediately
preceding `0 // …` comment is shown read-only when present, giving part/colour
context. Tab and Shift+Tab move between numeric fields. Enter applies the line;
Esc or Ctrl+C cancels the draft. All twelve entries must be finite floats and
the transform must remain invertible. A rejected value gets a caret under the
offending character, a brief explanation and a suggested fix. Choose `e` to
return to its field or `c` to cancel and restore the pre-edit line.

Edits affect **only that occurrence**, even inside a repeated submodel. Original
files and libraries stay unchanged. The importer rebuilds the scene and evaluates
the currently enabled parts from their new CAD poses, keeping the instruction
pointer and enabled IDs. The browser updates to the rebuilt scene while preserving its camera. Rejected edits
leave the current scene intact. `undo` restores the previous line, geometry and
poses/velocities. Consecutive edits undo back to the original unedited line;
undoing does not add another edit. Execution commands and edits share one history,
so intervening execution commands undo first. Reset keeps session edits but
clears undo history. Reopening starts from the source files again.

For callers, `program.placement_line(id)` returns the current full line and
`await program.edit(id, line)` applies a validated replacement. Session overrides
are retained in the import/preparation reports. Earlier scene artifacts are
archived under `output/…/revisions/<xml hash>/`; the event log records accepted
edits and undos. Source hashes still describe the unchanged original files;
the XML hash identifies the edited geometry.

```python
import asyncio
import json
from ldraw_mujoco import Interpreter

async def main():
    async with Interpreter.open(
        "data/models-annotated/106-1.mpd",
        output_dir="output/106-1/python-execution",
        viewer=True,  # Local browser inspection with paced physics playback.
    ) as program:
        await program.step_into()  # Enter the car submodel.
        result = await program.step_over()  # Place its first DAT part.
        print(result["events"][0]["physics"])
        print(result["next_instruction"])
        print(json.dumps(await program.inspect(), indent=2, allow_nan=False))

asyncio.run(main())
```

Results are JSON-serializable dictionaries with `events`, `stack`,
`next_instruction`, `done`, `enabled_ids`, and `failed`. Events contain the source
file, section, line, occurrence ID and call path. Placement observations include
all enabled parts' positions, quaternions, velocities and CAD displacement, plus
complete final contacts/forces and requested/actual evaluation duration.
Linear velocities use world coordinates; angular velocities use the body frame.
Call events have `physics: null`. Source lines are one-based; occurrence IDs
remain zero-based placement paths.

`inspect (i)` reads the live MCP state at the current picture, including after
undo or reset. It refreshes contacts without advancing time, placing parts, or
changing the instruction pointer, undo history, or `last_result`. Its JSON
contains `time_s`, `timestep_s`, `xml_sha256`, debugger status, `state_finite`,
`bodies`, `contacts`, and `contact_count`. Each enabled body has its occurrence
`id`, DAT `reference`, pose, velocity and displacement from CAD. Each contact has
`part1_id` and `part2_id`; `null` identifies the ground (`geom1` or `geom2` is
`ground`). Contact `pos` and `dist` are meters, with negative distance indicating
penetration. `normal_force` and the two `friction_force` components are newtons
in the contact frame. All contacts are returned. Empty scenes have empty arrays.
Inspections are also saved as `kind: "inspect"` records in `events.jsonl`.
A failed inspection query can be retried; an already halted execution still
requires reset or reopening.

The caller decides whether a placement succeeded. `state_finite` and
`duration_matches` describe the final observation, not a guarantee of numerical
validity throughout the trial or physical stability. Collision hulls may overlap,
and independent parts have no clutch forces. Global energy is not reported,
because hidden parts retain their compiled masses. Their contacts are disabled
and gravity is compensated while they wait to be placed.

An execution error halts further stepping until reset or reopening.
`ExecutionError.result` and `program.last_result` retain completed events and
the failing instruction, including its physics observation when available.
Non-finite diagnostic numbers become JSON `null`. Cancelled operations also halt
the program. Operations on the same interpreter must be awaited sequentially.
Stepping after completion returns an empty completed result. Ctrl+C in the
terminal closes the owned server; reopen the interpreter to restart.

The CLI writes `scene.xml`, `scene.import.json`, `execution.json`, server
diagnostics in `server.log`, and a flushed `events.jsonl` under
`output/INPUT_STEM/execution/`; change the directory with `--output-dir`.
The Python API writes these when `output_dir` is supplied.
The preparation report includes the XML hash and the exact activation settings.
Canonical `scene.xml` contains all collision-capable bodies. The exact
`bootstrap.xml` loaded by MCP temporarily disables contacts, avoiding an
all-parts contact solve before the inactive masks are applied. Only after those
masks succeed does the interpreter restore the original option flags. Both XML
hashes and the restored flags are recorded in `execution.json`. Each new session replaces those
artifacts in its output directory; use distinct directories to retain runs.

`--library`, `--shadow` / `--no-shadow`, `--density`, `--friction`, `--timestep`
and `--clearance` configure import. Execution always covers the full input in
individual-parts mode, without attachments (`attach=False`): each placement is
one free body. With `--viewer`, an independent browser tab shows live poses,
with orbit, pan, zoom, and a **Frame model** button. Unplaced parts appear
at their CAD positions at 15% opacity; **Show unplaced parts** toggles this visual
context. Placed parts retain their original colours/transparency. Physics and
editing controls remain in the terminal.

The local Viser service is bound to `127.0.0.1` on an available port. The printed
URL can be opened manually or revisited after closing the tab. No installed
viewer app, Node build, CDN, or `mjpython` launcher is needed. The interpreter's
MCP process runs headlessly and remains the sole physics engine. Browser assets
come with the pinned Python dependency; no public sharing is enabled.

Connected playback publishes poses about 20 times per simulated second and
paces against wall time when possible. Timestep, step count, contact settings,
and trial duration are unchanged. A disconnected browser removes pacing;
reconnecting receives the current scene. Browser failures leave terminal
execution available and are recorded in `program.viewer_error` and the event
log. `await program.viewer()` opens the URL again. Import/compilation, browser
preparation, and physics loading are reported separately; large models still
require time to compile, but startup never solves contacts for inactive parts.

```sh
# Script a debugger session, or type these commands interactively.
printf 'step\nnext\ncontinue\nquit\n' | uv run --extra interpreter \
  ldraw-mujoco execute data/models-annotated/106-1.mpd --seconds-per-part 0.1

# Real MCP execution plus saved states and locally rendered inspection images.
uv run --extra interpreter python examples/execute-106-1.py
uv run --extra interpreter pytest -q
```

The example covers empty, first-part, nested-wheel and completed states, including
a wheel detail. Local rendering uses the exact XML and returned MCP state;
all time advancement remains in the MCP process.

## Optional simulation and configuration

```sh
uv run ldraw-mujoco simulate output/106-1/scene.xml --seconds 1 \
  --snapshot output/106-1/simulated.png
```

`simulate` runs the full duration and writes motion, contacts, energy and
numerical warnings to `.simulation.json`, without a verdict.

On macOS, the native viewer (`hold --viewer`, Python `show()`) needs `mjpython`,
for example `.venv/bin/mjpython -m ldraw_mujoco hold SCENE.xml --viewer`. With a
uv-managed Python, `mjpython` cannot find `libpython` unless you point it at the
interpreter's library folder:

```sh
export DYLD_FALLBACK_LIBRARY_PATH="$(.venv/bin/python -c 'import sys; print(sys.base_prefix)')/lib:/usr/local/lib:/usr/lib"
```

Elsewhere add `--viewer` to `hold`. For very large scenes, turning off shadows
in the native viewer's Rendering panel makes each frame about 40 % cheaper.
Native MuJoCo APIs can edit the returned spec or run physics.

`simulate --viewer` instead opens the interpreter's independent browser viewer,
on any platform and without `mjpython`.
All simulated bodies are active, so this command does not ghost parts or disable
contacts. The initial picture is published before the first physics solve;
camera navigation remains independent of that solve. Closing the tab does not
stop simulation or mark its report invalid.

After the requested duration, the CLI saves its report and optional snapshot,
then keeps the final scene available until Enter or Ctrl+C. Piped/noninteractive
runs exit normally. Python `simulate(..., viewer=True)` closes its service when
it returns. Offscreen snapshots do not require the browser.

- Library: `--library`, then `LDRAW_DIR`, then project-local `data/ldraw`.
- Shadows: repeat `--shadow`, or set `LDRAW_SHADOW` to paths separated by the
  platform path separator. Defaults to `data/offLibShadow`. `--no-shadow` or
  Python `shadows=[]` disables external connector metadata, so far fewer
  parts attach.
- Defaults: timestep 1 ms, gravity −9.81 m/s², clearance 1 mm, density
  1050 kg/m³, sliding friction 0.6 and joint friction 0.01 N·m. `--timestep`,
  `--clearance`, `--density`, `--friction` and `--joint-friction` change these
  uncalibrated assumptions.
- Solver: Newton (MuJoCo's default) by default. Use `--solver cg` (Python:
  `solver="cg"`) for thousands of touching individual parts. They form a huge
  contact island, where Newton needs 13–39 s per step and CG under 0.5 s.
  Newton stays faster for welded or loosely connected scenes.
- Each part has detailed colored visual meshes and one convex collision hull.
  Hulls leave out stud primitives (pyldraw3's `stud*` rule), so stacked parts
  start face to face instead of overlapping by a stud height. Hull contacts use
  MuJoCo multi-point collision (`multiccd`) with a 0.2 mm margin. With a single
  contact point per pair, stacked meshes sink into each other.
  Only hulls contribute mass/inertia. Inline faces in LDR assemblies are collected
  into in-memory DAT parts without changing source files. Their IDs end in
  `inline` (e.g. `0/inline`), leaving source placement IDs unchanged. Each face
  collection uses one hull and follows the normal grouping mode. It must span
  a 3D volume. Like other document-local DATs, face collections have no
  connectors and never attach. Texture images remain unsupported; use
  geometry-based patterns.
- Missing DAT references can resolve to a unique document-local section named
  `PREFIX - reference.dat`, after exact document and library lookup fail. The
  import report records these aliases and warnings; ambiguous matches fail.
- Full source assembly references must resolve for indexing. Geometry is built
  only for selected part occurrences, and only selected parts attach to each
  other. Connector metadata decides attachment and joints, never attachment
  strength.

## Development and reproduction

```sh
uv run python examples/106-1.py
uv run pytest -q
uv run ruff check .
# Optional browser integration checks (skip when Chromium is not installed):
uv run playwright install chromium
uv run pytest -q tests/test_viewer.py
```

The example exports the full model, car, minifigure, selected wheel/minifigure,
and individual-parts variants, plus `parts-free` (individual parts without
attachment) for comparison. It writes inventories, reports, initial images and
hold checks under `output/106-1/`. See [architecture notes](docs/architecture.md) for the
conventions, tests and continuation guidance.

To reproduce the 10,000-body acceptance run on macOS or Linux, run
`uv run python examples/repeated_bricks.py`. It builds a spaced grid of
2 × 4 bricks, checks that they share two meshes, and takes one physics step.
The input and measured import time and peak process memory are in
`output/repeated-bricks/`.

Code follows the existing GPL-3.0-or-later license; documentation follows the
existing CC-BY-SA-4.0 notice. LDraw models, parts and shadows retain their own
licenses; 106-1 credits Michael Heidemann. The occurrence-path convention was
adapted from Carlos Antelo's [ldraw-mecha](https://github.com/anteloc/ldraw-mecha)
documentation (2026, CC BY-SA 4.0); here, selecting an instance preserves its
full-input ID and coordinate frame. There is no runtime dependency on that
project.
