# LDraw in MuJoCo

Import `.mpd`, `.ldr` and `.dat` assemblies as rigid objects for approximate
gravity, contact, sliding and tipping experiments. One pyldraw3 → `MjSpec`
builder supports both Python simulation and self-contained MJCF export.

## Quick start

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/), a local LDraw parts
library in `data/ldraw`, and the supplied `data/offLibShadow`. The official
library must contain `parts/`, `p/` and `LDConfig.ldr`; `parts.lst` is generated
in `.cache/` without modifying the library. No downloads occur during import.

```sh
uv sync --locked
uv run ldraw-mujoco convert data/models-annotated/106-1.mpd \
  --grouping top-level --output output/106-1/scene.xml
uv run ldraw-mujoco simulate output/106-1/scene.xml --seconds 5 \
  --snapshot output/106-1/final.png
```

The sample contains 65 part occurrences: 55 in the car (including five wheel
assemblies) and 10 in the separate minifigure. `--grouping top-level` creates
two free bodies. Wheels, doors, roof and minifigure joints are fixed.

The default `--grouping model` treats an entire input as one rigid body.
Grouping expresses an assumption; an LDraw submodel is not evidence of a
physical attachment. Select grouping deliberately for each model.

`convert` writes XML and a neighboring `.import.json` report. `simulate`
writes `.simulation.json` with motion, contacts, penetration, energy and
numerical warnings. It exits unsuccessfully on numerical failure. Reports do
not claim that a successful run proves a model is buildable or stable in reality.

## Python and viewer

```python
from ldraw_mujoco import import_ldraw
import mujoco

result = import_ldraw("data/models-annotated/106-1.mpd", grouping="top-level")
model = result.spec.compile()
data = mujoco.MjData(model)
mujoco.mj_step(model, data)
xml = result.spec.to_xml()
```

Use native MuJoCo APIs to set initial velocities, apply forces or change the
returned spec before recompiling. On macOS, use MuJoCo's `mjpython` launcher
for the passive viewer:

```sh
.venv/bin/mjpython -m ldraw_mujoco simulate output/106-1/scene.xml --viewer
```

On other platforms, add `--viewer` to the ordinary `simulate` command.
Offscreen `--snapshot` rendering does not require the passive viewer.

## Configuration and limits

- Library: `--library`, then `LDRAW_DIR`, then project-local `data/ldraw`.
- Shadows: repeat `--shadow`; alternatively set `LDRAW_SHADOW` to paths
  separated by the platform path separator. Defaults to local `offLibShadow`.
  `--no-shadow` or Python `shadows=[]` disables external shadow metadata.
- Defaults: 1 ms timestep, gravity −9.81 m/s², 1 mm ground clearance,
  density 1050 kg/m³ and sliding friction 0.6. Flags `--timestep`, `--clearance`,
  `--density` and `--friction` change these uncalibrated assumptions.
- Detailed surfaces carry colors, geometry-based patterns and transparency.
  Drawn edges are omitted. TEXMAP textures and inline faces in LDR assemblies
  are rejected explicitly; place custom solid geometry in DAT files/sections.
- Each occurrence has one convex collision hull. Cavities and holes are filled.
  Overlapping hull volumes are counted separately, so mass, inertia and center
  of mass can differ materially from real hollow LEGO parts.
- All parts share the selected density and friction, including tires. There
  is no clutch force, separation, internal articulation, deformation or damage.
- Shadow metadata coverage and warnings are reported separately from geometry.
  Connector records do not establish joint forces or attachment strength.

See [architecture and continuation notes](docs/architecture.md) for conventions,
the approach comparison, validation, and the next useful extensions.

## Development

```sh
uv run pytest -q
uv run ruff check .
```

Small synthetic library fixtures exercise the importer independently of the
full library. Integration tests use the local library and the 106-1 sample;
they report a skip if those inputs are unavailable.

Code follows the existing GPL-3.0-or-later license; documentation follows the
existing CC-BY-SA-4.0 notice. LDraw models, parts and shadow data retain their
own attribution and licenses. The 106-1 source credits Michael Heidemann.
