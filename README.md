# LDraw in MuJoCo

Import `.mpd`, `.ldr` and `.dat` files as independent submodel bodies or
individual physical parts. One pyldraw3 → `MjSpec` builder supports Python
and self-contained MJCF export.

## Quick start

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/), a local LDraw parts
library in `data/ldraw`, and the supplied `data/offLibShadow`. The library must
contain `parts/`, `p/` and `LDConfig.ldr`; its index is generated in `.cache/`
without modifying source files. No downloads occur during import.

```sh
uv sync --locked
uv run ldraw-mujoco inspect data/models-annotated/106-1.mpd
uv run ldraw-mujoco convert data/models-annotated/106-1.mpd \
  --output output/106-1/scene.xml
```

`inspect` prints a JSON inventory of all placed parts and submodels, including
IDs, parent IDs and source lines. It needs the source model and its external
submodel files, but no parts library or mesh compilation. `convert` writes
portable XML with inline meshes and a neighboring `.import.json` report.

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

There is one switch for the entire import operation:

| Mode | Result |
|---|---|
| Default | Each model/submodel instance's **direct parts** share one rigid body. Every child submodel is independent of its parent and siblings. |
| `--individual-parts` | Every included physical part occurrence gets its own free body. No parts are welded together. |

An assembly containing only child submodels remains an identified container;
it gets no empty physics body. Loose parts directly under the root share its
body. A flat model without submodels therefore imports as one body by default.
All physics bodies have free joints under the world. “Welded” means attaching
geoms to the same body, not introducing constraints between submodels.

For 106-1, default import gives **seven bodies**: car direct parts (45), five
wheel assemblies (2 each), and minifigure (10). Importing only the car gives
six bodies. Individual-parts mode gives 65 bodies for the full model, 55 for
the car, or two for a selected wheel instance.

```sh
# Independent parts throughout the full model.
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
`individual_parts=True` / `--individual-parts` for loose parts; omit it for
independently welded submodels, including nested ones.

## Python

```python
from ldraw_mujoco import import_ldraw, inspect_ldraw
import mujoco

path = "data/models-annotated/106-1.mpd"
inventory = inspect_ldraw(path)  # inventory["instances"] lists names and IDs.
result = import_ldraw(
    path,
    sections=["106 - wheel assembly.ldr:0/46", "106 - Minifig.ldr"],
    individual_parts=True,  # Omit for welded submodels; omit sections for the full input.
)
model = result.spec.compile()
data = mujoco.MjData(model)
xml = result.spec.to_xml()
```

The report's `instances` list identifies included model/submodel/part nodes
and their bodies (`null` for containers without direct geometry). `occurrences`
adds part IDs, transforms and geom names; `bodies` maps each body to its owning
`instance_id`. `selected_instances` records the resolved IDs (such as `0/46`). Names of
bodies/geoms derive from full-input IDs, so selection does not renumber them.

## Execute LDraw instructions through MCP

The optional interpreter treats model/submodel references as subroutine calls
and physical DAT references as part placements. It uses the existing parser
and full-input IDs; a DAT's internal primitives are never instructions.

```sh
uv sync --locked --extra interpreter
uv run --extra interpreter ldraw-mujoco execute data/models-annotated/106-1.mpd

# Open the native MuJoCo window and watch each placement's physics.
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
| `undo` / `u` | `undo()` | Undo the last step, next, finish, or continue. |
| `finish` / `f` | `step_out()` | Finish the current submodel; at root, finish the program. |
| `continue` / `c` | `run()` | Finish the program. |
| `where` / `w` | `status` property | Show the stack and next instruction. |
| `reset` / `r` | `reset()` | Disable all parts, rewind, and clear undo history. |
| `help` / `h` | — | Show each command with a brief explanation. |
| `quit` / `q` | — | Close the owned viewer and server. |

Every DAT placement enables one free body. Before each evaluation, **all enabled
parts return to their original CAD poses with zero velocity**. Physics then
runs for 100 ms, rounded up to whole timesteps. Change this with
`--seconds-per-part` or `seconds_per_part=`. Each trial starts at time zero;
motion from the previous evaluation is not carried into the next placement.
The full input's common ground offset remains fixed throughout execution.

Entering a submodel changes only the call stack. Returning is implicit, with
no subroutine return value. Step over/out still evaluate every contained DAT
placement and retain every observation. Empty submodels return immediately.

`undo` restores the stack, enabled parts, poses and velocities from before
the last execution command. For example, `next` on a submodel followed by `u`
undoes that whole call. Repeating `u` walks further back, including after program
completion. It does not run physics backward or advance time. `help` and `where`
do not affect history; `reset` clears it. With no history, `u` does nothing.
You can execute forward again after undoing. History lasts only for this session;
execution failures still require `reset` or reopening.

```python
import asyncio
from ldraw_mujoco import Interpreter

async def main():
    async with Interpreter.open(
        "data/models-annotated/106-1.mpd",
        output_dir="output/106-1/python-execution",
        viewer=True,  # Optional native window with paced physics playback.
    ) as program:
        await program.step_into()  # Enter the car submodel.
        result = await program.step_over()  # Place its first DAT part.
        print(result["events"][0]["physics"])
        print(result["next_instruction"])

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
XML contains all collision-capable bodies; the interpreter applies the recorded
initial disabling settings after loading it. Each new session replaces those
artifacts in its output directory; use distinct directories to retain runs.

`--library`, `--shadow` / `--no-shadow`, `--density`, `--friction`, `--timestep`
and `--clearance` configure import. Execution always covers the full input in
individual-parts mode. With `--viewer`, each trial plays at approximately real
time, with viewer updates around 60 times per simulated second. The window
shows the MCP process's actual model and state: CAD reset, new part placement,
physics motion, then a pause awaiting the next debugger command. Continue and
step over/out also show the contained placements. Physics timesteps and trial
durations are unchanged. The terminal remains the execution controller; use
the native viewer to rotate, pan and zoom the scene.

The interpreter selects `mjpython` automatically on macOS and handles uv's
Python library path. Linux and Windows use the ordinary server launcher.
Closing the window leaves the interpreter usable and removes playback pacing.
`await program.viewer()` reopens it; on macOS, open the interpreter with
`viewer=True` so its server has the native launcher. A window-launch failure is
available as `program.viewer_error`, and the CLI reports it while keeping
terminal execution available. A local desktop is required for the live window.

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

`simulate` writes motion, contacts, energy and numerical warnings to
`.simulation.json`. Falling or detachment is allowed: this iteration concerns
import structure, not stability assessment or attachment forces. There are no
constraints between the imported free bodies. Convex collision hulls fill
cavities and may overlap, so initially assembled bodies can push apart.

On macOS, use `.venv/bin/mjpython -m ldraw_mujoco simulate SCENE.xml --viewer`.
Elsewhere add `--viewer` to the ordinary command. Offscreen snapshots do not
require the viewer. Native MuJoCo APIs can edit the returned spec or run physics.

- Library: `--library`, then `LDRAW_DIR`, then project-local `data/ldraw`.
- Shadows: repeat `--shadow`, or set `LDRAW_SHADOW` to paths separated by the
  platform path separator. Defaults to `data/offLibShadow`. `--no-shadow` or
  Python `shadows=[]` disables external connector metadata.
- Defaults: timestep 1 ms, gravity −9.81 m/s², clearance 1 mm, density
  1050 kg/m³ and sliding friction 0.6. `--timestep`, `--clearance`, `--density`
  and `--friction` change these uncalibrated assumptions.
- Each part has detailed colored visual meshes and one convex collision hull.
  Only hulls contribute mass/inertia. Texture images and inline faces in LDR
  assemblies are unsupported; use geometry-based patterns or embedded DATs.
- Full source assembly references must resolve for indexing. Geometry is built
  only for selected part occurrences. Shadow metadata is diagnostic, not a
  source of joints or attachment strength.

## Development and reproduction

```sh
uv run python examples/106-1.py
uv run pytest -q
uv run ruff check .
```

The example exports the full model, car, minifigure, selected wheel/minifigure,
and individual-parts variants, with inventories, reports and initial images
under `output/106-1/`. See [architecture notes](docs/architecture.md) for the
conventions, tests and continuation guidance.

Code follows the existing GPL-3.0-or-later license; documentation follows the
existing CC-BY-SA-4.0 notice. LDraw models, parts and shadows retain their own
licenses; 106-1 credits Michael Heidemann. The occurrence-path convention was
adapted from Carlos Antelo's [ldraw-mecha](https://github.com/anteloc/ldraw-mecha)
documentation (2026, CC BY-SA 4.0); here, selecting an instance preserves its
full-input ID and coordinate frame. There is no runtime dependency on that
project.
