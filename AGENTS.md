# Working in ldraw-mujoco

Build small, idiomatic Python tools for importing LDraw geometry into MuJoCo.
Keep the code intuitive and lean. Prefer existing packages over new parsers,
mesh algorithms or physics engines. Explain assumptions and leave useful
continuation notes when behavior or scope changes. Ask for guidance when a
physical modeling decision cannot be resolved from the task and evidence.

## Current workflow

1. `uv sync --locked` installs the pinned environment.
2. `uv run python examples/106-1.py` reproduces the sample and inspection views.
3. `uv run pytest -q` checks parsing, transforms, physics and XML round-tripping.
4. `uv run ruff check .` checks maintained code. Source data is excluded.

Use `ldraw_mujoco.import_ldraw()` or the `ldraw-mujoco convert` command to build
models. Use native MuJoCo APIs after compilation. Keep parsing/geometry,
physics construction and simulation/reporting separate; no second backend.

## Conventions that must stay explicit

- LDraw is Y-down; 1 LDU is 0.0004 m. Convert with `(x, z, -y)`, a proper
  rotation, not `(x, -z, -y)`, which reflects the model.
- pyldraw3 owns record parsing, MPD expansion, inherited placement colors and
  shadow loading. Consume its parsed objects and geometry/metadata APIs;
  do not write an independent parser or manually parse original library DATs.
- Model sections organize CAD sources. They do not prove physical connections.
  DAT subparts/primitives are geometry, not independently moving bricks.
- Keep affine source transforms in mesh vertices. Never turn scale/shear into
  a quaternion silently. Preserve BFC winding and mirrored transforms.
- Visual surfaces have zero mass and no contacts. Group 3 geoms are collision
  hulls and the sole source of inferred mass/inertia; group 0 is visual.
- Hulls fill cavities and can overlap. Density and friction are assumptions.
  Numerical success does not prove attachment strength or real-world stability.
- Shadow coverage/warnings are separate from solid geometry completeness.
  Do not treat inferred connectors as calibrated joints or clutch forces.

## Files and evidence

Keep original `data/` and source libraries unchanged. The importer writes its
read-through index to `.cache/`; generated scenes and evidence go in `output/`.
There must be no imports or runtime paths into neighboring projects.

When changing geometry or physics, regenerate and open the relevant images;
check the whole model and affected assemblies. Retain reports for the exact
exported artifact. MCP can validate, load and step the self-contained XML;
local rendering can provide images when the MCP renderer is unavailable.

Keep README CLI examples and `docs/architecture.md` aligned with behavior.
Preserve source authors/licenses and the existing repository license files.
