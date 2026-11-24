---
name: python-bindings
description: 'The `mujoco` Python package: installation, MjModel.from_xml_string/from_xml_path, MjData, mj_step / mj_forward, named access (model.body(''x''), data.joint(''y'')), the interactive viewer (mujoco.viewer.launch, launch_passive), Renderer, MjSpec model editing from Python, rollout, minimize and other utilities, building from source and migrating from mujoco-py. Use when writing Python that loads, steps, inspects, edits or views MuJoCo models.'
---

# MuJoCo Python bindings

Use the `mujoco` package to load, step, inspect, edit, render and view MuJoCo models from Python. The bindings are low-level pybind11 wrappers that follow the C API (so the [API reference](../reference/SKILL.md) applies to both languages), with Pythonic deviations documented below. Core concepts (mjModel, mjData, mjSpec, MJCF) are in the [root skill](../SKILL.md).

Related: [MuJoCo Playground](https://playground.mujoco.org) and [reaf-sim](https://reaf-sim.readthedocs.io) for RL/sim-to-real in PyTorch; [dm_control](https://github.com/google-deepmind/dm_control) depends on `mujoco` (pre-1.0.0 users: [migration guide](https://github.com/google-deepmind/dm_control/blob/main/migration_guide_1.0.md)). Tutorial: [colab notebook](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/tutorial.ipynb).

## Install

``` shell
pip install mujoco
```

The MuJoCo library is bundled; no separate download. Since MuJoCo 4.0.0, `mujoco` is a metapackage:

| Package | Contents |
|---|---|
| `mujoco` | `mujoco-core` + `mujoco-studio` + classic OpenGL deps (`glfw`, `pyopengl`) |
| `mujoco-core` | Core simulation bindings, depends only on `numpy` (headless servers, RL). `mujoco-core[rendering]` adds `glfw` and `pyopengl` for classic rendering and `mujoco.viewer` without Studio. |
| `mujoco-studio` | MuJoCo Studio viewer and Filament renderer bindings (pulls in `mujoco-core`, `mujoco-studio-wasm`) |
| `mujoco[usd]` / `mujoco-usd` | OpenUSD importer, exporter, physics schemas |
| `mujoco[sysid]` | System identification toolbox |

## Minimal example

``` python
import mujoco

XML=r"""
<mujoco>
  <asset>
    <mesh file="gizmo.stl"/>
  </asset>
  <worldbody>
    <body>
      <freejoint/>
      <geom type="mesh" name="gizmo" mesh="gizmo"/>
    </body>
  </worldbody>
</mujoco>
"""

ASSETS=dict()
with open('/path/to/gizmo.stl', 'rb') as f:
  ASSETS['gizmo.stl'] = f.read()

model = mujoco.MjModel.from_xml_string(XML, ASSETS)
data = mujoco.MjData(model)
while data.time < 1:
  mujoco.mj_step(model, data)
  print(data.geom_xpos)
```

Passing an assets dict is **deprecated**; prefer `MjVfs` (see Assets and the VFS below).

## Structs

- Everything (structs, functions, constants, enums) is at top level: `import mujoco`.
- Struct names are capitalized (PEP 8): `mjData` → `mujoco.MjData`.
- `MjModel` has **no constructor**. Use the static factories `mujoco.MjModel.from_xml_string`, `mujoco.MjModel.from_xml_path` or `mujoco.MjModel.from_binary_path` (XML or MJB). They accept an optional VFS/assets argument.
- Other structs have constructors. With an `mj_defaultFoo` initializer it is called automatically (`mujoco.MjOption()` uses *mj_defaultOption*); otherwise the C struct is zero-initialized.
- `mj_makeFoo` initializers map to constructor overloads, e.g. `mujoco.MjvScene(model, maxgeom=10)`. The matching free/delete function runs automatically when the object is deleted.
- Fields are **views into C memory, not copies**. `mj_step` changes them in place. Copy what you keep: `positions.append(data.body('my_body').xpos.copy())`. A slice like `qpos_slice = data.qpos[3:8]` also changes after stepping.
- Assignment writes into C memory: `model.opt.gravity = value` equals `model.opt.gravity[:] = value`. Sub-structs `opt`, `vis`, `stat` of `MjModel` and `global_`, `quality`, `headlight`, `map`, `scale`, `rgba` of `MjVisual` can be assigned (`model.opt = new_opt` copies fields in place; existing views stay valid; later changes to `new_opt` do not propagate).

## Functions, enums, constants

- Functions keep their C names (`mujoco.mj_step`, `mujoco.mj_forward`, ...). Arguments follow C order; keyword names match `mujoco.h`.
- Array inputs take NumPy arrays or convertible iterables. **Output arrays must be writeable NumPy arrays.**
- Array size arguments are omitted: `mujoco.mj_jac(m, d, jacp, jacr, point, body)`.
- The GIL is released during each C call (only for the C function itself).
- `mj_step` takes an extra `nstep` (default 1). This runs 20 steps without reacquiring the GIL in between:

  ``` python
  mj_step(model, data, nstep=20)
  ```

- Enums: `mujoco.mjtEnumType.ENUM_VALUE`, e.g. `mujoco.mjtObj.mjOBJ_SITE`. Constants: `mujoco.mjVISSTRING`.
- *mj_recompile* returns **new** `MjModel` and `MjData` objects instead of modifying in place (avoids dangling references).

## Named access

Each `name_fooadr` field of mjModel defines a category `foo`. `MjModel` and `MjData` have a method `foo(name_or_id)` returning an accessor whose attributes are the fields with the prefix before the underscore removed, plus `id` and `name`:

- `m.geom('gizmo').rgba` is a view of `m.geom_rgba[4*i:4*i+4]`, where `i = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_GEOM, 'gizmo')`.
- `m.geom('gizmo').id` equals that `i`; `m.geom(i).name` is `'gizmo'`.
- Joint accessors also expose DoF-sized fields: `d.joint('foo').qpos`, `d.joint('foo').qvel` (length depends on joint type).
- Lookup is O(1) in the number of entities.

Categories (aliases after "or"): `body`, `jnt` or `joint`, `geom`, `site`, `cam` or `camera`, `light`, `mesh`, `skin`, `hfield`, `tex` or `texture`, `mat` or `material`, `pair`, `exclude`, `eq` or `equality`, `tendon` or `ten`, `actuator`, `sensor`, `numeric`, `text`, `tuple`, `key` or `keyframe`.

## Interactive viewer (`mujoco.viewer`)

Based on the same code as the [simulate](../c-programming/SKILL.md) app. For MuJoCo Studio viewers (native window or web), see [studio-viewers](../studio-viewers/SKILL.md).

| Mode | Call | Behavior |
|---|---|---|
| Managed | `viewer.launch()` / `viewer.launch(model)` / `viewer.launch(model, data)` | **Blocks** user code; the viewer runs physics. Use when user code is [engine plugins](../c-programming/engine-plugins/SKILL.md) or physics callbacks. With `data`, the viewer modifies it in place. With no args, load a model by drag-and-drop. |
| Standalone | `python -m mujoco.viewer` / `python -m mujoco.viewer --mjcf=/path/to/some/mjcf.xml` | Managed viewer from the command line. |
| Passive | `viewer.launch_passive(m, d)` | **Does not block**. Your script times and steps physics; mouse perturbations work only if you sync. |

**macOS:** `launch_passive` requires running under `mjpython` (installed with the package; drop-in for `python`, e.g. `mjpython my_script.py`, `mjpython -m IPython`).

Passive handle API:

| Member | Purpose |
|---|---|
| `cam`, `opt`, `pert` | `mjvCamera`, `mjvOption`, `mjvPerturb` |
| `lock()` | Context-manager mutex; hold it before modifying model/data or `cam`/`opt`/`pert`. |
| `sync(state_only=False)` | Exchange state with the GUI; required for the viewer to show changes. Also pushes GUI inputs (flags, controls, perturbations) into `mjOption` and `mjData`. `state_only=True` syncs only `mjSTATE_INTEGRATION` fields then calls *mj_forward*: faster, but misses arbitrary edits such as `mjModel.geom_rgba`. |
| `update_hfield(hfieldid)`, `update_mesh(meshid)`, `update_texture(texid)` | Re-upload asset data for rendering. |
| `close()`, `is_running()` | Safe without the lock. The handle is also a context manager that closes on exit. |
| `user_scn` | User-owned `mjvScene`: add geoms (e.g. *mjv_initGeom*, *mjv_connector*) or set `user_scn.flags`; applied on next `sync()`. |

Keyword arguments: `key_callback` (called with a keycode on key events), `show_left_ui`, `show_right_ui` (Tab / Shift+Tab still toggle).

``` python
import time

import mujoco
import mujoco.viewer

m = mujoco.MjModel.from_xml_path('/path/to/mjcf.xml')
d = mujoco.MjData(m)

with mujoco.viewer.launch_passive(m, d) as viewer:
  # Close the viewer automatically after 30 wall-seconds.
  start = time.time()
  while viewer.is_running() and time.time() - start < 30:
    step_start = time.time()

    # mj_step can be replaced with code that also evaluates
    # a policy and applies a control signal before stepping the physics.
    mujoco.mj_step(m, d)

    # Example modification of a viewer option: toggle contact points every two seconds.
    with viewer.lock():
      viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = int(d.time % 2)

    # Pick up changes to the physics state, apply perturbations, update options from GUI.
    viewer.sync()

    # Rudimentary time keeping, will drift relative to wall clock.
    time_until_next_step = m.opt.timestep - (time.time() - step_start)
    if time_until_next_step > 0:
      time.sleep(time_until_next_step)
```

`key_callback` example: toggle a `paused` flag when `chr(keycode) == ' '`, and only call `mj_step` and `viewer.sync()` when not paused.

Custom geoms via `user_scn` (inside the loop): set `viewer.user_scn.ngeom = 0`, call `mujoco.mjv_initGeom(viewer.user_scn.geoms[i], type=mujoco.mjtGeom.mjGEOM_SPHERE, size=[0.02, 0, 0], pos=..., mat=np.eye(3).flatten(), rgba=...)` for each geom, set `viewer.user_scn.ngeom = i`, then `viewer.sync()`. Wireframe: `viewer.user_scn.flags[mujoco.mjtRndFlag.mjRND_WIREFRAME] = 1`.

## Offscreen rendering

Two APIs: classic (OpenGL 1.5) and [Filament](../c-programming/visualization-rendering/SKILL.md) (physically based).

**Classic:** create a context with `ctx = mujoco.GLContext(max_width, max_height)`, call `ctx.make_current()` (one thread at a time; render from that thread), then follow the standard `mjr_` flow in [visualization-rendering](../c-programming/visualization-rendering/SKILL.md). Freed on deletion, or explicitly with `ctx.free()`. The Bazel notes mention a `mujoco.Renderer` class for offscreen rendering, but these docs do not describe its API.

**Filament** (`from mujoco import mjrf`): enums drop the `mjr` prefix (`mjrf.GraphicsApi.GRAPHICS_API_DEFAULT`); POD structs are plain Python types; create/destroy types are Python-owned objects (`del` destroys; returned references are not owned); functions taking an object first become methods (`Light.set_active(bool)`); buffers you pass (e.g. `mjrf.ReadRequest.set_buffer`) must outlive the request. Helpers: `mujoco.rendering.filament.model_scene.ModelScene` and `mujoco.rendering.filament.renderer.Renderer`.

``` python
import mujoco
from mujoco import mjrf
from mujoco.rendering.filament import model_scene
from mujoco.rendering.filament import renderer
import numpy as np

def render(model: mujoco.MjModel, data: MjData, width: int, height: int) -> np.ndarray:
  ctx = mjrf.Context(mjrf.ContextConfig())
  r = renderer.Renderer(ctx)
  ms = model_scene.ModelScene(ctx, model, r.scene("scn"))
  pixels = np.empty((height, width, 3), dtype=np.uint8)
  r.target("out", pixels)
  ms.update(data)
  vcam = mujoco.MjvCamera()
  mujoco.mjv_defaultFreeCamera(model, vcam)
  vcam.type = int(mujoco.mjtCamera.mjCAMERA_FIXED)
  vcam.fixedcamid = 0
  view = renderer.View(
      scene="scn",
      target="out",
      camera=mujoco.mjv_camera2GLCamera(model, data, vcam),
  )
  r.render([view])  # blocks until the target is written
  return pixels
```

## Errors and callbacks

- Irrecoverable MuJoCo errors (*mju_error*) become `mujoco.FatalError` exceptions (via longjmp, thread-local handler), so you can catch them.
- Set a callback `mjcb_foo` with `mujoco.set_mjcb_foo(some_callable)`, reset with `mujoco.set_mjcb_foo(None)`, read with `mujoco.get_mjcb_foo()` (only for callbacks set through the bindings). Examples: `mjcb_sensor`, `mjcb_control`. Python callbacks take the GIL on every call: slow, meant for prototyping. A native function passed via `ctypes` is installed directly without the GIL.

## Model editing with MjSpec

Mirrors the C [model editing API](../model-editing/SKILL.md) plus conveniences. More examples: [MjSpec colab](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/mjspec.ipynb).

``` python
import mujoco
spec = mujoco.MjSpec()
spec.modelname = "my model"
body = spec.worldbody.add_body(
    pos=[1, 2, 3],
    quat=[0, 1, 0, 0],
)
geom = body.add_geom(
    name='my_geom',
    type=mujoco.mjtGeom.mjGEOM_SPHERE,
    size=[1, 0, 0],
    rgba=[1, 0, 0, 1],
)
...
model = spec.compile()
```

Construct with `mujoco.MjSpec()`, `mujoco.MjSpec.from_string(xml_string)` or `mujoco.MjSpec.from_file(file_path)` (the loaders only at construction time).

### Assets and the VFS

``` python
with mujoco.MjVfs() as vfs:
    vfs["model.xml"] = b"<mujoco/>"
    spec = mujoco.MjSpec.from_file("model.xml", vfs=vfs)
    spec.compile(vfs=vfs)
```

Or create `vfs = mujoco.MjVfs()` and call `vfs.close()`. Operations: `vfs["name"] = data` (`bytes`), `del vfs["name"]`, `"name" in vfs`. `MjModel.from_xml_string`, `MjModel.from_xml_path`, `MjSpec.from_string`, `MjSpec.from_file` and `spec.compile()` accept `vfs`. The `assets` dict (and `spec.assets = {...}`) is deprecated, will be removed in the next release, and cannot be combined with `vfs`.

### Save, encode, copy back

- `spec.to_xml()` returns XML. It **compiles first** (the spec must compile with its assets, and compilation changes it, e.g. applying `fusestatic`). By default compiled values are saved; set `spec.compiler.savecompiled = False` to save the spec as written.
- `spec.encode(...)` takes the target filename, an optional compiled `model`, an optional `vfs` and an optional `content_type`. The format comes from the extension (`.xml`, `.mjb`, `.txt`, `.mjz`) or the content type.

  ``` python
  spec.encode('model.xml')               # spec to MJCF
  spec.encode('model.xml', model=model)  # copies modified model values back first
  spec.encode('model.mjb', model=model)  # binary mjModel only
  spec.encode('robot.mjz', model=model)  # zip with referenced assets
  ```

- `spec.copy_back(model)` writes changed compiled values into the spec (see *mj_copyBack*):

  ``` python
  model = spec.compile()
  model.geom('my_geom').size[0] = 2
  spec.copy_back(model)
  print(spec.geom('my_geom').size[0])  # 2.0
  ```

- `spec.to_zip(file)` / `MjSpec.from_zip(file)`: spec with all assets (path or file object).

### Attachment

| Call | Result |
|---|---|
| `frame.attach_body(body, prefix, suffix)` | Child body attached to a parent frame; returns the body. |
| `body.attach_frame(frame, prefix, suffix)` | Child frame attached to a parent body; returns the frame. |
| `parent_spec.attach(child_spec, site=site_name_or_obj)` | Child worldbody as a frame at a site; `prefix`/`suffix` kwargs. |
| `parent_spec.attach(child_spec, frame=frame_name_or_obj)` | Same, at a frame. |

By default attaching does **not copy**: child references stay valid and edits to the child modify the parent (unlike MJCF `attach`/`replicate`, which deep-copy). Set `spec.copy_during_attach = True` to copy. Without copying, a whole child spec can be attached only once; elements of the parent can be re-attached to it only as copies.

Example: `frame.attach_body(child_body, 'child-', '')`, `body.attach_frame(child_frame, 'child-', '')`, `parent.attach(child2, site=site, prefix='child2-')`, `parent.attach(child3, frame=frame, prefix='child3-')`.

### Conveniences

- Named access: `spec.geom('my_geom')` returns the `mjsGeom` or `None`; likewise `.body()`, `.joint()`, `.site()`, ...
- Lists: `sites`, `geoms`, `joints`, `lights`, `cameras`, `bodies`, `frames`, `materials`, `meshes`, `pairs`, `equalities`, `tendons`, `actuators`, `skins`, `textures`, `texts`, `tuples`, `flexes`, `hfields`, `keys`, `numerics`, `excludes`, `sensors`, `plugins`.
- Removal: `spec.delete(spec.geom('my_geom'))` removes the element, everything referencing it, and children of bodies/frames/defaults.
- Tree: `body.geoms` etc. (direct children: `bodies`, `joints`, `geoms`, `sites`, `cameras`, `lights`, `frames`); `body.find_all(mujoco.mjtObj.mjOBJ_SITE)` or `body.find_all('site')` (subtree); `site.parent`.
- Meshes: `mesh = spec.add_mesh(name='prism')`, then `mesh.make_cone(nedge=5, radius=1)` (mesh/builtin semantics).
- Textures: `texture = spec.add_texture(name='texture', height=1, width=3, nchannel=3)`; `texture.data` holds `bytes` (edit a `bytearray` copy and reassign).
- Binding: `data.bind(geom)` gives mjModel/mjData values for an `mjs` element, e.g. `[data.bind(geom) for geom in spec.geoms if 'torso' in geom.name]` then `.xpos`. Model and data must be compiled from that spec; adding or removing elements since compilation raises an error.

`MjSpec` is conceptually like dm_control PyMJCF's `mjcf_model`, but roughly two orders of magnitude faster.

## Modules

### rollout

Steps trajectories in C, optionally in parallel (one `MjData` per thread). [Colab](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/rollout.ipynb).

``` python
state, sensordata = rollout.rollout(model, data, initial_state, control)
```

- `model`: one `MjModel` or `nbatch` homogeneous models (same integer sizes). `data`: one `MjData` or `nthread` of them.
- `initial_state`: `nbatch x nstate`, `nstate = mj_stateSize(model, mjtState.mjSTATE_FULLPHYSICS)`.
- `control`: `nbatch x nstep x ncontrol` (default: the `nu` actuators; other inputs via `control_spec` bitflag).
- Stateless: existing `MjData` contents do not matter. A diverged rollout repeats its last state (detect via non-increasing time). An `MjData` with *mju_threadpool* is rejected.
- `persistent_pool=True` reuses a pool across calls (not thread safe; shut down with `rollout.shutdown_persistent_pool`). For several pools, use `with rollout.Rollout(nthread=nthread) as rollout_: rollout_.rollout(model, data, initial_state)` or call `rollout_.close()` before exit.

### batch

`mujoco.batch.Batch` runs many simulations of one model on a thread pool; fields are `nsim x ...` NumPy rows. Results are bit-identical to a per-simulation loop.

``` python
from mujoco import batch

b = batch.Batch(model, nsim=1024, nthread=8)
qpos, ctrl, xpos = b.bind('qpos'), b.bind('ctrl'), b.bind('xpos')
for _ in range(1000):
  ctrl[:] = policy(qpos, xpos)
  b.step()
```

- `bind(name)` / attributes (`b.xpos`, `b.ctrl = u`): state fields are writable views; other fields are read-only copies that lag one substep after `step`. Valid names: `mujoco.batch.DATA_FIELDS`, `mujoco.batch.MODEL_FIELDS`.
- Named views: `joint`, `body`, `site`, `sensor`, `actuator`, `geom`, `tendon`, `camera`, `light` (data and model attributes, e.g. `b.body('pole').mass = masses`); `equality`, `pair`, `material`, `numeric`, `keyframe` (model only).
- `expand(name)` (or `opt.<name>`) makes a model field per-simulation; `expanded(name)`; `set_const(ids)` after changing inputs of *mj_setConst*; `set_models(models)`.
- `step(ids, nstep)`, `forward(ids)`, `reset(ids, keyframe)`, `rollout(nstep, control, control_spec, record, ids)`, `jac(body, point, ids)`, `ray(pnt, vec, ..., normal=False)`, `get_model(sim)`, `get_data(sim)`, `b.warning`. `step(..., stage=mujoco.mjtStage.mjSTAGE_VEL)` makes fields describe the new state.
- Errors: `mujoco.batch.SimulationError` (a `RuntimeError` with `ids`); `b.status`, `b.error(i)`. Do not use one `Batch` from several Python threads.
- `Batch(model, nsim, persistent=True)` keeps one `MjData` per simulation; required with sleep or IPC enabled, and for plugins with state outside `plugin_state`. Physics callbacks must be C functions via `ctypes`.

### minimize, sysid, USD, utilities

- `minimize.least_squares()`: nonlinear least squares via SQP with *mju_boxQP*; see the [notebook](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/least_squares.ipynb).
- `mujoco.sysid` (`pip install mujoco[sysid]`): fits `MjSpec` parameters to recorded trajectories with batched rollouts; see the [README](https://github.com/google-deepmind/mujoco/blob/main/python/mujoco/sysid/README.md).
- `mujoco.studio`: see [studio-viewers](../studio-viewers/SKILL.md).
- `mujoco.usd.exporter.USDExporter(model=m)` (args `max_geom`, `output_directory`, `output_directory_root`, `light_intensity`, `camera_names`, `verbose`): call `exp.update_scene(data=d)` per frame (check `exp.frame_count`), then `exp.save_scene(filetype="usd")` (`.usd`, `.usda`, `.usdc`); also `add_light(...)`, `add_camera(...)`. Native OpenUSD workflows: [interop](../interop/SKILL.md).
- `msh2obj.py` converts the deprecated legacy `.msh` surface mesh format to OBJ.

## Building from source

Only needed to modify the bindings (or for very old Linux). Needs CMake and a C++17 compiler.

``` shell
git clone https://github.com/google-deepmind/mujoco.git
cd mujoco/python
python3 -m venv /tmp/mujoco
source /tmp/mujoco/bin/activate
bash make_sdist.sh
cd dist
MUJOCO_PATH=/PATH/TO/MUJOCO \
MUJOCO_PLUGIN_PATH=/PATH/TO/MUJOCO/PLUGIN \
pip install mujoco_core-x.y.z.tar.gz
```

First install MuJoCo itself (a [binary release](https://github.com/google-deepmind/mujoco/releases) or a [source build](../c-programming/SKILL.md)). `MUJOCO_PLUGIN_PATH` can point to the repo's `plugin` folder. On macOS use `MUJOCO_PATH=/Volumes/MuJoCo MUJOCO_PLUGIN_PATH=/Volumes/MuJoCo/MuJoCo.app/Contents/MacOS/mujoco_plugin` from the mounted DMG. Sub-package sdists: run `bash make_sdist.sh` in `studio`, `studio_wasm`, `usd` or `mujoco_full`. Verify outside the repo with `python -c "import mujoco"`. Reference config: [CI workflow](https://github.com/google-deepmind/mujoco/blob/main/.github/workflows/build.yml).

**Bazel:** depend on `@mujoco//python/mujoco` (with `rules_python`):

``` python
load("@rules_python//python:py_binary.bzl", "py_binary")

py_binary(
    name = "simulate_model",
    srcs = ["simulate_model.py"],
    deps = ["@mujoco//python/mujoco"],
)
```

Covers core bindings and offscreen rendering; the interactive viewer, MJX and the USD exporter are not yet supported. Tests: `bazel test //python/...`.

## Migrating from mujoco-py

`mujoco` is stateless; there is no `MjSim`. Hold the model and data yourself.

| mujoco-py | mujoco |
|---|---|
| `mujoco_py.load_model_from_xml(bstring)` | `mujoco.MjModel.from_xml_*`, then `mujoco.MjData(model)` |
| `sim.reset()`, `sim.forward()`, `sim.step()` | `mujoco.mj_resetData(model, data)`, `mujoco.mj_forward(model, data)`, `mujoco.mj_step(model, data)` |
| `sim.get_state()` / `set_state` / flattened variants | State functions in [simulation-loop](../c-programming/simulation-loop/SKILL.md) |
| `sim.model.get_joint_qvel_addr(name)` | Build from `model.jnt_qposadr[joint_index]` and the joint type |
| `sim.model.*_name2id(name)` | Named access or `mujoco.mj_name2id(model, type_enum, name)` |
| `sim.save(fstream, format_name)` | `mujoco.mj_saveLastXML(fname)` (no automatic keyframe from current pose) |

## Source docs

Verbatim copies, for details not covered above:

- [python.md](references/python.md)
