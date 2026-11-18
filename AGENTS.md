# Working in ldraw-mujoco

Build small, idiomatic Python tools for importing LDraw geometry into MuJoCo.
Keep the code intuitive and lean. Prefer existing packages over new parsers,
mesh algorithms or physics engines. Explain assumptions and leave useful
continuation notes when behavior or scope changes. Ask for guidance when a
physical modeling decision cannot be resolved from the task and evidence.

## Current workflow

1. `uv sync --locked` installs the pinned environment.
2. `uv run python examples/106-1.py` reproduces the sample and inspection views.
3. `uv run pytest -q` checks IDs, selection, body boundaries, geometry and XML round-tripping.
4. `uv run ruff check .` checks maintained code. Source data is excluded.

Use `ldraw_mujoco.import_ldraw()` or the `ldraw-mujoco convert` command to build
models, and `hold()` or `ldraw-mujoco hold` to check them once, headless. View
results with `show()` or `--viewer`, which never step physics. Use native
MuJoCo APIs after compilation. Keep parsing/geometry, physics construction and
simulation/reporting separate; no second backend.

## Conventions that must stay explicit

- LDraw is Y-down; 1 LDU is 0.0004 m. Convert with `(x, z, -y)`, a proper
  rotation, not `(x, -z, -y)`, which reflects the model.
- pyldraw3 owns record parsing, MPD expansion, inherited placement colors and
  shadow loading. Consume its parsed objects and geometry/metadata APIs;
  do not write an independent parser or manually parse original library DATs.
- Model sections organize CAD sources. They do not prove physical connections.
  DAT subparts/primitives are geometry, not independently moving bricks.
- IDs are zero-based type-1 placement paths from the full input: `0/46/1`.
  `root` is the input container. Preserve IDs across selection and parts mode;
  source/dependency hashes scope IDs to a source revision. Use `inspect` to list
  IDs before conversion. Every placed part and submodel is identified.
- Repeat `--section SECTION[:ID]` for a union of specific submodel instances.
  A name alone must match exactly one placed instance; repeats require `section:id`.
  Check that the name matches the instance. Reject bare IDs and list qualified
  selectors in ambiguity errors. Keep raw path IDs in inventories and reports.
  Preserve full-input transforms, inherited colors and BFC ownership.
- Default welding groups only the direct DAT parts of each model/submodel
  instance. Child submodels are independent world-parented free bodies; never
  weld them to ancestors or siblings. Containers without direct parts have IDs
  but no empty physics body. Root loose parts share the root's own body.
- `individual_parts=True` / `--individual-parts` is the only grouping switch,
  applied to the entire import. Each physical DAT occurrence gets a free body;
  geometric subparts/primitives stay inside it. Do not restore grouping modes
  or per-instance overrides. Do not add attachment inference until approved.
- The hold check is the one stability workflow: settle (0.2 s), then stop at
  the first body that moves beyond the tolerance (2 mm) within the duration
  (5 s). Run it once, headless. Never step large scenes in
  `mujoco.viewer.launch`: it runs physics continuously, even when paused.
  `--solver cg` suits thousands of touching individual parts; Newton the rest.
- Keep affine source transforms in mesh vertices. Never turn scale/shear into
  a quaternion silently. Preserve BFC winding and mirrored transforms.
- Visual surfaces have zero mass and no contacts. Group 3 geoms are collision
  hulls and the sole source of inferred mass/inertia; group 0 is visual.
- Hulls omit stud primitives (pyldraw3's `stud` file-stem rule) and fill
  cavities; CAD interpenetrations (pins, clips, minifig joints) can still
  overlap. Hull contacts use multiccd and a 0.2 mm margin so flat faces rest on
  each other. Density, friction and the margin are assumptions. Studs give no
  interlock or clutch in any orientation, SNOT included. Numerical success
  does not prove attachment strength or real-world stability.
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
