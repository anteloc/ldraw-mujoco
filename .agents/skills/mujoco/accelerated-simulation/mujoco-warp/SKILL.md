---
name: mujoco-warp
description: 'MuJoCo Warp (mujoco_warp): when to use it, installation, basic usage (put_model, put_data, step), feature parity, performance tuning, batched Model fields, batch rendering, FAQ and differences from MuJoCo. Use when simulating many MuJoCo worlds on NVIDIA GPUs with Warp.'
---

# MuJoCo Warp (MJWarp)

MuJoCo Warp (`mujoco_warp`) is MuJoCo written in [Warp](https://nvidia.github.io/warp/) and optimized for NVIDIA GPUs and parallel simulation. NVIDIA and Google DeepMind build it together in [google-deepmind/mujoco_warp](https://github.com/google-deepmind/mujoco_warp). Use this skill to put models on the GPU, step thousands of worlds, size the contact and constraint buffers, randomize model fields per world, batch-render cameras, and work around differences from MuJoCo. Tutorial: [notebook](https://github.com/google-deepmind/mujoco_warp/blob/main/notebooks/tutorial.ipynb) ([open in colab](https://colab.research.google.com/github/google-deepmind/mujoco_warp/blob/main/notebooks/tutorial.ipynb)).

## When to use it

- **Throughput, not latency.** MJWarp maximizes total steps per unit time. One MJWarp step is expected to be slower than one MuJoCo step. Use MJWarp when you need many samples, as in RL. Use MuJoCo for real-time work such as MPC or teleoperation.
- **Versus the alternatives.** [`mujoco.rollout`](../../python-bindings/SKILL.md) runs multi-threaded `mj_step` on CPU, but host-device transfers can become the bottleneck. [`mjx.step`](../mjx/SKILL.md) batches with `jax.vmap`/`jax.pmap` on CPU, GPU or TPU. MJWarp scales better than MJX on nearly every workload, especially complex scenes, and works well with PyTorch.
- **Complex scenes.** MJWarp scales better than MJX with many geoms or DoFs, but not as well as MuJoCo for one large kinematic tree. It reaches hundreds of DoFs if [sleeping](../../physics-computation/SKILL.md) is on and the scene splits into independent islands. Single connected mechanisms above about 60 DoFs are still being worked on.
- **No autodiff.** MJWarp is not differentiable (tracked in [issue 500](https://github.com/google-deepmind/mujoco_warp/issues/500)). For gradients, use MJX-JAX.

## Install

```shell
pip install mujoco-warp
pip install "mujoco-warp[viewer]"   # needed for mjwarp-viewer and mjwarp-record
pip install "mujoco-warp[optix]"    # optional OptiX ray-casting backend (RTX GPUs)
```

MJWarp depends only on the core MuJoCo bindings ([mujoco-core](../../python-bindings/SKILL.md)). To install from source:

```shell
git clone https://github.com/google-deepmind/mujoco_warp.git
cd mujoco_warp
uv sync --all-extras
uv run pytest -n 8
```

## Basic usage

`import mujoco_warp as mjw`. Structs, functions and enums are in the top-level module. Function names are MuJoCo's, in PEP 8 style. Most of the main simulation functions are there.

Copy structs to the device: an [mjModel](../../reference/api-types/SKILL.md) becomes `mjw.Model` via `mjw.put_model`, and an [mjData](../../reference/api-types/SKILL.md) becomes `mjw.Data` via `mjw.put_data` or `mjw.make_data`. Both hold Warp arrays. Some fields are missing, for unsupported features or for GPU performance.

```python
mjm = mujoco.MjModel.from_xml_string("...")
mjd = mujoco.MjData(mjm)
m = mjw.put_model(mjm)
d = mjw.put_data(mjm, mjd)
```

Minimal example:

```python
# Throw a ball at 100 different velocities.

import mujoco
import mujoco_warp as mjw
import warp as wp

_MJCF=r"""
<mujoco>
  <worldbody>
    <body>
      <freejoint/>
      <geom size=".15" mass="1" type="sphere"/>
    </body>
  </worldbody>
</mujoco>
"""

mjm = mujoco.MjModel.from_xml_string(_MJCF)
m = mjw.put_model(mjm)
d = mjw.make_data(mjm, nworld=100)

# initialize velocities
wp.copy(d.qvel, wp.array([[float(i) / 100, 0, 0, 0, 0, 0] for i in range(100)], dtype=float))

# simulate physics
mjw.step(m, d)

print(f'qpos:\n{d.qpos.numpy()}')
```

### Batch size arguments (to `make_data` / `put_data`)

| Argument | Meaning |
|---|---|
| `nworld` | Number of worlds. |
| `nconmax` | Expected contacts **per world**. The total cap is `nconmax * nworld`, so one world may exceed `nconmax` as long as the total fits. |
| `naconmax` | Maximum contacts over **all worlds**. If both are set, `nconmax` is ignored. |
| `njmax` | Maximum constraints **per world**, enforced strictly. |
| `nccdmax` / `naccdmax` | Maximum contacts from CCD colliders, per world / all worlds. Set them below `nconmax` / `naconmax` to save CCD memory. |
| `nvmax` | Maximum active DoFs per world for the compact solver. Defaults to `nv`. |

Values are **not** parsed from the deprecated [size/nconmax and size/njmax](../../reference/xml-reference/SKILL.md). Pass them in code.

### Command line

```shell
mjwarp-testspeed benchmark/humanoid/humanoid.xml
mjwarp-viewer benchmark/humanoid/humanoid.xml   # requires mujoco-warp[viewer]
```

Useful `mjwarp-testspeed` flags: `--measure_alloc` prints the contacts and constraints at each step, `--overflow_behavior=error` (default) or `continue`, `--memory` reports memory use, `--nvmax=64`, `--function=render`, and `--render_backend=optix`.

## Performance tuning

### Capture a CUDA graph

Called directly, `mjw.step` launches its kernels one at a time. Capture them once and relaunch the graph, which is typically much faster. See the [Warp graph docs](https://nvidia.github.io/warp/stable/user_guide/execution_and_performance/concurrency.html#graph-launches).

```python
with wp.ScopedCapture() as capture:
  mjw.step(m, d)
```

```python
wp.capture_launch(capture.graph)
```

After changing an `mjw.Option` field, you may need a new graph capture before the setting takes effect.

### Size the buffers, then the solver

1. Memory and compute scale with `nconmax`/`naconmax` and `njmax`. Make them as small as possible without overflowing, using `mjwarp-testspeed --measure_alloc` and overflow checks. Good values are environment specific and usually found by trial and error.
2. Lowering `Option.iterations` / `Option.ls_iterations` is secondary. The solver exits early once all worlds converge, so these matter less than in MJX. Set them too low and the solver may not converge.
3. Contact sensors: make `Option.contact_sensor_maxmatch` as small as possible. Matches beyond the limit are ignored. Set it as `model.opt.contact_sensor_maxmatch = 16` or in XML:

```xml
<custom>
  <numeric name="contact_sensor_maxmatch" data="16"/>
</custom>
```

Note: the docs spell this field both `contact_sensor_max_match` and `contact_sensor_maxmatch`. The code examples and option list use `contact_sensor_maxmatch`.

### Memory

- CCD colliders need more memory than primitive colliders. [multiccd](../../reference/xml-reference/SKILL.md) needs more than CCD. CCD memory grows linearly with [Option.ccd_iterations](../../reference/xml-reference/SKILL.md).
- With a mesh and multiccd, memory grows linearly with the maximum vertices per face and the maximum edges per vertex over all meshes.
- Sparse Jacobians (`efc.J`, `ten_J`, `flexedge_J`, `actuator_moment`) store only potentially non-zero entries. Above `nv > 60` they allow scenes that dense mode cannot run. Example: Aloha clutter (nv=136, 2048 worlds, njmax=384) needs about 84 MB sparse versus 408 MB dense.
- `nccdmax` example: 10 worlds with 80 contacts (mesh-mesh 30 CCD, ellipsoid-ellipsoid 10 CCD, sphere-sphere 40 primitive) need `nconmax`/`naconmax` ≥ 8/80 (more may be needed for broadphase) and `nccdmax`/`naccdmax` = 3/30.

### Large scenes: sleeping and the compact solver

MJWarp puts stationary islands to [sleep](../../physics-computation/SKILL.md). Collision and the constraint solver skip sleeping bodies. When few DoFs are active (typically under 64), the **compact solver** packs the active DoFs into a dense workspace of size `nvmax` and runs Newton with fixed-size tile operations. To enable it:

1. Use the Newton solver: `<option solver="Newton"/>`.
2. Enable sleep:

```xml
<option>
  <flag sleep="enable"/>
</option>
```

Or with mjSpec:

```python
spec = mujoco.MjSpec()
spec.option.solver = mujoco.mjtSolver.mjSOL_NEWTON
spec.option.enableflags |= mujoco.mjtEnableBit.mjENBL_SLEEP
```

3. Size the workspace with `nvmax`, the maximum expected active DoFs in any world. A tight bound saves GPU memory and raises throughput.

```python
# Allocate data with a maximum of 64 active DOFs per world
d = mjw.make_data(mjm, nworld=2048, nvmax=64)
```

With `nvmax < nv`, start with all trees asleep to avoid an initial DoF overflow:

```python
d.tree_asleep.assign(np.array(np.arange(mjm.ntree, dtype=np.int32)), dtype=np.int32)
```

To put objects to sleep sooner, raise `sleep_tolerance` from its default 0.001 (for example `spec.option.sleep_tolerance = 0.01`).

### Overflow detection

When the fixed buffers (`nconmax`/`naconmax`, `njmax`, `nccdmax`/`naccdmax`, `nvmax`, `contact_sensor_maxmatch`) overflow, behaviour is **undefined**. `Data.overflow` is an `(nworld,)` array of `mjw.OverflowType` bitmasks. It starts at zero and is cleared by `mjw.reset_data`.

```python
mjw.step(m, d)

# device-to-host transfer
overflow = d.overflow.numpy()

# check worlds for any overflow
any_overflow = np.any(overflow != 0)

# check for each world for (narrowphase) contact overflow
has_contact_overflow = (overflow & mjw.OverflowType.NARROWPHASE) != 0
```

- `m.opt.warn_overflow` defaults to `True` and prints from the GPU, which serializes threads and can badly slow throughput. Set it to `False` for high-throughput runs. Bitmasks are still recorded.
- `d.overflow.numpy()` syncs host and device. Check it at resets or rollout boundaries, not every step.

Runtime warnings and fixes:

| Warning | Fix |
|---|---|
| `nconmax` / `njmax` exceeded | Raise the argument to `make_data` / `put_data`. |
| `mjw.Option.ccd_iterations` | Raise it in the XML / mjSpec / mjModel that you pass to `put_model` **and** `make_data`/`put_data`. |
| `mjw.Option.contact_sensor_maxmatch` | Raise `m.opt.contact_sensor_maxmatch`, or narrow the sensor's matching, for example with `geom1` and `geom2`. |
| `height field collision overflow` | Contacts above `mjMAXCONPAIR` are dropped. Lower the hfield resolution or shrink the colliding geom. |

## Batched Model fields (domain randomization)

Many `mjw.Model` fields have a leading batch dimension, 1 by default, shared by all worlds. Enlarge it per field and assign values. World `w` reads `field[worldid % field.shape[0]]`.

```python
m = mjw.put_model(mjm, batch_sizes={"dof_damping": 2})
m.dof_damping.assign(np.array([[0.1], [0.2]], dtype=float))
```

To change a field properly, edit the mjSpec and recompile. That takes one host call per variant. Some fields are safe to change directly on device: see [mjModel changes](../../c-programming/simulation-loop/SKILL.md) and [issue 893](https://github.com/google-deepmind/mujoco_warp/issues/893).

### Per-world assets (meshes, hfields, materials, textures)

1. Create an mjSpec that contains **all** assets.
2. Compile each variant by mutating the spec and calling `spec.compile()`.
3. Compile a **base** model and build `mjw.Model` from it.
4. Override the dependent fields with per-world arrays taken from the variants.

Geom-level example (worlds 0-1 use `mesh_a`, worlds 2-3 use `mesh_b`). The spec setup is trimmed:

```python
# compile each variant
geom.meshname = "mesh_a"
mjm_a = spec.compile()
geom.meshname = "mesh_b"
mjm_b = spec.compile()

# restore and compile base
geom.meshname = "mesh_a"
mjm = spec.compile()

m = mjw.put_model(mjm)
d = mjw.make_data(mjm, nworld=nworld)

geom_id = mujoco.mj_name2id(mjm, mujoco.mjtObj.mjOBJ_GEOM, "obj")
variants = [mjm_a, mjm_b]
assignment = [0, 0, 1, 1]  # variant index per world

dataid = np.tile(mjm.geom_dataid, (nworld, 1))
geom_size = np.zeros((nworld, mjm.ngeom, 3))
# ... same pattern for geom_aabb (nworld, ngeom, 2, 3), geom_rbound, geom_pos,
# body_mass, body_subtreemass, body_inertia, body_invweight0, body_ipos, body_iquat

for w in range(nworld):
  ref = variants[assignment[w]]
  dataid[w, geom_id] = ref.geom_dataid[geom_id]
  geom_size[w] = ref.geom_size
  geom_aabb[w] = ref.geom_aabb.reshape(mjm.ngeom, 2, 3)
  # ... copy the remaining fields from ref

m.geom_dataid = wp.array(dataid, dtype=int)
m.geom_size = wp.array(geom_size, dtype=wp.vec3)
m.geom_aabb = wp.array(geom_aabb, dtype=wp.vec3)
# ... assign the remaining fields with the dtypes below
```

Fields to override for per-world meshes:

| Field | dtype | Shape |
|---|---|---|
| `geom_dataid` | `int` | `(nworld, ngeom)` |
| `geom_size` | `wp.vec3` | `(nworld, ngeom)` |
| `geom_aabb` | `wp.vec3` | `(nworld, ngeom, 2)` |
| `geom_rbound` | `float` | `(nworld, ngeom)` |
| `geom_pos` | `wp.vec3` | `(nworld, ngeom)` |
| `body_mass` | `float` | `(nworld, nbody)` |
| `body_subtreemass` | `float` | `(nworld, nbody)` |
| `body_inertia` | `wp.vec3` | `(nworld, nbody)` |
| `body_invweight0` | `wp.vec2` | `(nworld, nbody)` |
| `body_ipos` | `wp.vec3` | `(nworld, nbody)` |
| `body_iquat` | `wp.quat` | `(nworld, nbody)` |

Body-level randomization, where variants have different geom counts: give the base body the **maximum** number of geoms over all variants. In variants that do not use a slot, disable it (`contype=0`, `conaffinity=0`, `dataid=-1`), but keep it in the base model. MJWarp provides no utilities that build these dependent arrays. You build them yourself, or an environment framework does.

## Batch rendering

The batch renderer is a single-hit raycaster on [Warp BVHs](https://nvidia.github.io/warp/stable/api_reference/_generated/warp.Bvh.html), built for throughput, not fidelity. It supports textured meshes, heightfields, flex, 3D Gaussian splats, point and directional lights with shadows, and several cameras per world, each with its own resolution, FOV and output. It also accelerates `mjw.ray`, `mjw.rays` and rangefinder sensors. It has no global illumination, no PBR materials, and no view-dependent SH for 3DGS.

```python
rc = mjw.create_render_context(
    mjm,
    nworld=1,
    cam_res=(256, 256),           # Override camera resolution (or per-camera list)
    render_rgb=True,              # Enable RGB output (or per-camera list)
    render_depth=True,            # Enable depth output (or per-camera list)
    use_textures=True,            # Apply material textures
    use_shadows=False,            # Enable shadow casting (slower)
    enabled_geom_groups=[0, 1],   # Only render geoms in groups 0 and 1
    cam_active=[True, False],     # Selectively enable/disable cameras
    flex_render_smooth=True,      # Smooth shading for soft bodies
    backend="warp",               # Ray-casting backend ("warp" or "optix")
)
```

Each parameter applies globally or per camera. Parameters can also come from XML (`<camera ... resolution="64 64" output="rgb depth"/>`) or from mjSpec. To render:

```python
mjw.refit_bvh(m, d, rc)
mjw.render(m, d, rc)
```

```python
nworld = 1
cam_index = 0
resolution = rc.cam_res.numpy()[cam_index]
rgb_data = wp.zeros((nworld, resolution[1], resolution[0]), dtype=wp.vec3)
mjw.get_rgb(rc, rgb_data=rgb_data, cam_id=cam_index)
```

Raw buffers have shape `(nworld, npixel)`, with RGB packed into one `uint32`. Index cameras with `RenderContext.rgb_adr` / `depth_adr`, or use `mjw.get_rgb` / `mjw.get_depth`.

- Domain-randomizable render fields: `geom_matid`, `geom_size`, `geom_rgba`, `mat_texid`, `mat_texrepeat`, `mat_rgba`, and `light_active`, `light_type`, `light_castshadow`, `light_xpos`, `light_xdir`.
- OptiX (`backend="optix"`): falls back to `"warp"` with a warning if OptiX is unavailable or the scene has flex or splats. It **cannot** be captured in CUDA graphs. `mjw.ray`/`mjw.rays` need `backend="warp"`.
- Cost grows linearly with pixel count and camera count, and with mesh vertex and face counts. Primitives render faster than similar meshes or heightfields.
- 3DGS: pass `splat_position` (nsplat,3), `splat_rotation` (nsplat,4, `w,x,y,z`), `splat_scale` (nsplat,3, standard deviations) and `splat_rgba` (nsplat,4) as float32. For per-world groups, add `splat_adr` (ngroup+1,) and `splat_group_id` (nworld,). If splats move, call `mjw.refit_splat_bvh(rc)` before `mjw.render`. CLI: `mjwarp-render scene.xml --splat=my_scene.ply --width=512 --height=512` (add `--orbit` for an orbit video).

## Differences from MuJoCo

- **Precision:** float32, versus MuJoCo's float64 `mjtNum`. Results differ. Solver iterations, collisions and small friction values can be sensitive to this.
- **Orientations:** `mjw.Data` stores only quaternions (`xquat`, `xiquat`, `geom_xquat`, `site_xquat`), in MuJoCo's `w, x, y, z` order, not Warp's `x, y, z, w`. It omits `xmat`, `ximat`, `geom_xmat` and `site_xmat`. `mjw.get_data_into` fills them when copying back to mjData.
- **Shapes:** most `Data` fields have a leading `nworld` dimension. `Model.M`, `Data.efc.J` and `Data.efc.D` are padded.
- **Warmstart:** always starts from `qacc_warmstart`. MuJoCo compares it with `qacc_smooth` first.
- **Options:** `impratio` is stored as `impratio_invsqrt`. `tolerance` is clamped to at least `1e-6`. `o_margin`, `o_solref`, `o_solimp` and `o_friction` are not available. `mjDSBL_MIDPHASE`, `mjDSBL_AUTORESET`, `mjENBL_OVERRIDE`, `mjENBL_FWDINV` and `mjENBL_SPECULATIVE` are not available. If you change `density`, `viscosity` or `wind`, you may need to update `Model.has_fluid`.
- **MJWarp-only options:** `broadphase` (`mjw.BroadphaseType`), `broadphase_filter` (`mjw.BroadphaseFilter`), `graph_conditional`, `run_collision_detection`, `contact_sensor_maxmatch`, `warn_overflow`, `deterministic` (`mjw.DeterminismType` bitmask).
- **Collision sensors:** each geom pair that feeds a collision sensor reports one contact, even when the pair is not colliding. Contact sensors still report the contacts that affect the physics correctly.
- **Box-box:** uses GJK/EPA by default (up to 4 contacts). `m.opt.disableflags |= mjw.DisableBit.NATIVECCD` switches to the primitive box collider (up to 8 contacts), which may help stacking.
- **Not available:** named access / `bind` ([issue 884](https://github.com/google-deepmind/mujoco_warp/issues/884)). GPU results are not deterministic. Use `wp.set_device("cpu")` for deterministic results.

### Physics callbacks

Callbacks are set per model on `Model.callback`, not as global pointers: `control` (writes `Data.ctrl`), `passive` (`Data.qfrc_passive`), `act_dyn` (`Data.act_dot`), `act_gain` and `act_bias` (`Data.actuator_force`), `sensor` (`Data.sensordata`, gets an extra `stage` argument) and `contactfilter` (`Data.contact`).

```python
@wp.kernel
def _ctrl_callback(ctrl_out: wp.array2d(dtype=float)):
  worldid = wp.tid()
  ctrl_out[worldid, 0] = 2.0

def ctrl_callback(m, d):
  wp.launch(_ctrl_callback, dim=(d.nworld,), outputs=[d.ctrl])

m.callback.control = ctrl_callback
mjw.step(m, d)
```

### SDF plugins

Write the distance and gradient as `@wp.func`, then override the module hooks (example after [bowl.cc](https://github.com/google-deepmind/mujoco/blob/main/plugin/sdf/bowl.cc)):

```python
@wp.func
def user_sdf(p: wp.vec3, attr: wp.vec3, sdf_type: int) -> float:
  return bowl(p, attr)


@wp.func
def user_sdf_grad(p: wp.vec3, attr: wp.vec3, sdf_type: int) -> wp.vec3:
  return bowl_sdf_grad(p, attr)


# override the module-level hooks
mjw._src.collision_sdf.user_sdf = user_sdf
mjw._src.collision_sdf.user_sdf_grad = user_sdf_grad
```

### Pair-wise colliders (max contacts, nativeccd and multiccd on)

| | Sphere | Capsule | Ellipsoid | Cylinder | Box | Mesh | SDF |
|---|---|---|---|---|---|---|---|
| Plane | prim 1 | prim 2 | prim 1 | prim 4 | prim 4 | prim 4 | prim 1 |
| HField | HFieldCCD 4 | HFieldCCD 4 | HFieldCCD 4 | HFieldCCD 4 | HFieldCCD 4 | HFieldCCD 4 | HFieldSDF |
| Sphere | prim 1 | prim 1 | CCD 1 | prim 1 | prim 1 | CCD 1 | SDF |
| Capsule | | prim 2 | CCD 1 | CCD 2* | prim 2 | CCD 2* | SDF |
| Ellipsoid | | | CCD 1 | CCD 1 | CCD 1 | CCD 1 | SDF |
| Cylinder | | | | CCD 4* | CCD 4* | CCD 4* | SDF |
| Box | | | | | CCD 4* (prim 8 without nativeccd) | CCD 4* | SDF |
| Mesh | | | | | | CCD 4* | MeshSDF |
| SDF | | | | | | | SDF |

\* 1 without multiccd. SDF colliders' counts are set by [sdf_initpoints](../../reference/xml-reference/SKILL.md). Versus MuJoCo, `PLANE<>MESH` gives 4 contacts, not 3, and `HFieldCCD` gives 4, not `mjMAXCONPAIR`.

## FAQ

- **JAX:** interoperates via [Warp JAX interop](https://nvidia.github.io/warp/stable/user_guide/interoperability/jax.html). [MJX](../mjx/SKILL.md) with `impl='warp'` exposes part of the MJWarp API.
- **PyTorch:** interoperates via [Warp PyTorch interop](https://nvidia.github.io/warp/stable/user_guide/interoperability/pytorch.html). To train policies, see [MuJoCo Playground](https://playground.mujoco.org) with [reaf-sim](https://reaf-sim.readthedocs.io), [Isaac Lab](https://github.com/isaac-sim/IsaacLab) via [Newton](https://github.com/newton-physics/newton), and [mjlab](https://github.com/mujocolab/mjlab).
- **Multi-GPU:** use `wp.ScopedDevice`, one graph per device:

```python
graph = {}
for device in wp.get_cuda_devices():
  with wp.ScopedDevice(device):
    m = mjw.put_model(mjm)
    d = mjw.make_data(mjm)
    with wp.ScopedCapture(device) as capture:
      mjw.step(m, d)
    graph[device] = capture.graph

for device in wp.get_cuda_devices():
  wp.capture_launch(graph[device])
```

- **Faster compilation:** use fewer distinct colliders that need the general convex (`CCD`) pipeline. Ahead-of-time compilation is possible: see the [Warp AOT docs](https://nvidia.github.io/warp/stable/user_guide/programming_model/code_generation.html#ahead-of-time-compilation-workflows).
- **Physics wrong after an upgrade:** clear the Warp kernel cache with `rm -rf ~/.cache/warp`, or with `import warp as wp; wp.clear_kernel_cache()`.
- **Unexpected results or NaNs:** open a GitHub issue.
- **Feature support:** copying an mjModel with unsupported features raises an exception. For current status, see [MuJoCo API Compatibility](https://github.com/google-deepmind/mujoco_warp#mujoco-api-compatibility).

## Source docs

Verbatim copies, for details not covered above:

- [mjwarp/index.md](references/mjwarp-index.md)
