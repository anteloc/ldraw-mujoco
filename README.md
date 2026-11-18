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

In Python, open the complete model with one independent rigid body per placed DAT.
The importer resolves geometry and library connectors, builds an editable
`MjSpec`, and compiles it once in memory.

```python
import mujoco
import mujoco.viewer

from ldraw_mujoco import import_ldraw

result = import_ldraw("data/models-annotated/106-1.mpd", individual_parts=True)
model = result.model
data = mujoco.MjData(model)
mujoco.viewer.launch(model, data)
```

For a headless simulation, call `mujoco.mj_step(model, data)` directly. After
editing `result.spec`, call `result.spec.compile()` to obtain a new model and
create matching `MjData`. Use `result.spec.to_xml()` for a portable scene.

To list instance IDs or export from the command line, run

```sh
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
