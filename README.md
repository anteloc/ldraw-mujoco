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
```

In Python, import the complete model, check once that it holds still, then look
at the result. The importer resolves geometry and library connectors, builds an
editable `MjSpec`, and compiles it once in memory.

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
other document-local DATs have `not_queried` coverage and no dictionary entry.
MuJoCo computes contacts from the placed collision geoms.

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

A verdict reflects the approximations below. There is no clutch and studs are
visual only, so parts held by studs, including SNOT parts, fall in
individual-parts mode. In the default mode, submodels resting on other
submodels can topple. "Holds" is therefore not proof of real-world stability.

Measured on a 2,175-part garden: the welded import (41 bodies) answers in 4 s,
and individual parts with `--solver cg` in 39 s. With the default Newton
solver, one step of the individual-parts scene takes 13–39 s. See
[architecture notes](docs/architecture.md#hold-check-and-performance).

## Optional simulation and configuration

```sh
uv run ldraw-mujoco simulate output/106-1/scene.xml --seconds 1 \
  --snapshot output/106-1/simulated.png
```

`simulate` runs the full duration and writes motion, contacts, energy and
numerical warnings to `.simulation.json`, without a verdict. There are no
constraints between the imported free bodies.

On macOS, viewers need `mjpython`, for example
`.venv/bin/mjpython -m ldraw_mujoco hold SCENE.xml --viewer`. With a
uv-managed Python, `mjpython` cannot find `libpython` unless you point it at the
interpreter's library folder:

```sh
export DYLD_FALLBACK_LIBRARY_PATH="$(.venv/bin/python -c 'import sys; print(sys.base_prefix)')/lib:/usr/local/lib:/usr/lib"
```

Elsewhere add `--viewer` to the ordinary command. Offscreen snapshots do not
require the viewer. For very large scenes, turning off shadows in the viewer's
Rendering panel makes each frame about 40 % cheaper. Native MuJoCo APIs can
edit the returned spec or run physics.

- Library: `--library`, then `LDRAW_DIR`, then project-local `data/ldraw`.
- Shadows: repeat `--shadow`, or set `LDRAW_SHADOW` to paths separated by the
  platform path separator. Defaults to `data/offLibShadow`. `--no-shadow` or
  Python `shadows=[]` disables external connector metadata.
- Defaults: timestep 1 ms, gravity −9.81 m/s², clearance 1 mm, density
  1050 kg/m³ and sliding friction 0.6. `--timestep`, `--clearance`, `--density`
  and `--friction` change these uncalibrated assumptions.
- Solver: Newton (MuJoCo's default) by default. Use `--solver cg` (Python:
  `solver="cg"`) for thousands of touching individual parts. They form a huge
  contact island, where Newton needs 13–39 s per step and CG under 0.5 s.
  Newton stays faster for welded or loosely connected scenes.
- Each part has detailed colored visual meshes and one convex collision hull.
  Hulls leave out stud primitives (pyldraw3's `stud*` rule), so stacked parts
  start face to face instead of overlapping by a stud height. Hull contacts use
  MuJoCo multi-point collision (`multiccd`) with a 0.2 mm margin. With a single
  contact point per pair, stacked meshes sink into each other.
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
and individual-parts variants, with inventories, reports, initial images and
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
