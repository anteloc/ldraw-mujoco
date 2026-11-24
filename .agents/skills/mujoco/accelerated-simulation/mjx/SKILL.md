---
name: mjx
description: 'MuJoCo XLA (mujoco.mjx): installation, mjx.put_model / put_data, jitted mjx.step, vmap batching, implementations (JAX, Warp), reinforcement learning, feature parity, performance tuning and the sharp bits. Use when writing JAX code that simulates MuJoCo models.'
---

# MuJoCo XLA (MJX)

MJX (`mujoco.mjx`) is a [JAX](https://github.com/jax-ml/jax#readme) API for MuJoCo. It runs batched simulations with `jax.vmap`/`jax.jit` and has two implementations: MJX-JAX, a pure-JAX re-implementation that runs on every XLA backend, and MJX-Warp, which wraps [MuJoCo Warp](../mujoco-warp/SKILL.md) for NVIDIA GPUs. Use this skill to install MJX, put models and data on device, step batches of worlds, pick an implementation and tune performance.

## Install

```shell
pip install mujoco-mjx
```

To use [MuJoCo Warp](../mujoco-warp/SKILL.md) with MJX:

```shell
pip install mujoco-mjx[warp]
```

The package brings in a copy of the MuJoCo library, so you do not install it separately. It depends on `mujoco` for model compilation and visualization, and on MuJoCo Warp for the Warp implementation.

## Minimal example

Import `mujoco.mjx`. Put the model on device with `mjx.put_model`, create device data with `mjx.make_data`, and step with `mjx.step`.

```python
# Throw a ball at 100 different velocities.

import jax
import mujoco
from mujoco import mjx

XML=r"""
<mujoco>
  <worldbody>
    <body>
      <freejoint/>
      <geom size=".15" mass="1" type="sphere"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(XML)
mjx_model = mjx.put_model(model)

@jax.vmap
def batched_step(vel):
  mjx_data = mjx.make_data(mjx_model)
  qvel = mjx_data.qvel.at[0].set(vel)
  mjx_data = mjx_data.replace(qvel=qvel)
  pos = mjx.step(mjx_model, mjx_data).qpos[0]
  return pos

vel = jax.numpy.arange(0.0, 1.0, 0.01)
pos = jax.jit(batched_step)(vel)
print(pos)
```

## Structs: `mjx.Model` and `mjx.Data`

Copy structs to the device before calling MJX functions. Placing an [mjModel](../../reference/api-types/SKILL.md) on device gives an `mjx.Model`; placing an [mjData](../../reference/api-types/SKILL.md) gives an `mjx.Data`.

```python
model = mujoco.MjModel.from_xml_string("...")
data = mujoco.MjData(model)
mjx_model = mjx.put_model(model)
mjx_data = mjx.put_data(model, data)
```

Or create fresh data with `mjx.make_data`, which mirrors `mj_makeData`. Prefer it when you build batched `mjx.Data` inside a `vmap`:

```python
model = mujoco.MjModel.from_xml_string("...")
mjx_model = mjx.put_model(model)
mjx_data = mjx.make_data(model)
```

How they differ from the MuJoCo structs:

1. They hold JAX arrays that are copied onto the device.
2. Some fields are missing: those private to one implementation, and those for unsupported features.
3. JAX arrays accept batch dimensions. Batch `mjx.Model` for domain randomization and `mjx.Data` for high-throughput RL.
4. Numpy arrays are structural fields that control JIT output. Changing them forces a recompile. For example, `jnt_limited` is a numpy array (changing it recompiles), while `jnt_range` is a JAX array you can change at runtime. It applies only to joints that `jnt_limited` marks as limited.

Do not construct `mjx.Model` or `mjx.Data` by hand.

## Functions, enums, constants

- MuJoCo functions appear under the same names in [PEP 8](https://peps.python.org/pep-0008/) style. Most *main simulation* functions and some forward sub-components are in the top-level `mjx` module.
- MJX functions are **not** JIT compiled by default. Wrap them, or your own functions that call them, in `jax.jit`.
- Enums are `mjx.EnumType.ENUM_VALUE`, for example `mjx.JointType.FREE`. Enums for unsupported features are left out.
- MJX declares no constants. It uses MuJoCo's constants directly.

## Choose an implementation

| | MJX-Warp (`impl='warp'`) | MJX-JAX (default) |
|---|---|---|
| Hardware | NVIDIA GPUs | Nvidia and AMD GPUs, Apple Silicon, Google Cloud TPUs |
| Autodiff | No, and no immediate plans | Mostly supported |
| Contacts/constraints at scale | Fixes the main MJX-JAX bottlenecks | Slows as contacts grow |
| Mesh collisions | Fully supported | Convex only, needs small meshes |
| Best for | Most workloads | Small scenes, or when you need rough gradients |

The docs recommend MJX-Warp unless you want a simulator that is fast for small scenes and roughly supports gradients.

## MJX-Warp

### Basic usage

Pass `impl='warp'` to `mjx.put_model` and `mjx.make_data`:

```python
mj_model = mujoco.MjModel.from_xml_path(...)
model = mjx.put_model(mj_model, impl='warp')
data = mjx.make_data(mj_model, impl='warp', naconmax=naconmax, njmax=njmax)
```

- `naconmax`: maximum number of contacts for **all worlds combined**. Scale it by the number of environments you will `jax.vmap` over.
- `njmax`: maximum number of constraints **per world**.

To tune them for a new scene, load the scene in the [MJWarp viewer](../mujoco-warp/SKILL.md) and raise the values as overflows occur.

### Contacts

JAX and Warp lay out contact buffers differently, so with Warp the contacts live in the private `mjx.Data._impl`, not `mjx.Data.contact`. Read contacts only through [contact sensors](../../reference/xml-reference/SKILL.md). More examples: the [MuJoCo Playground announcement](https://github.com/google-deepmind/mujoco_playground/discussions/197).

### Batched `Data` updates (resets)

`jax.tree.map(jax.numpy.where, done, reset_data, data)` resets a subset of environments in MJX-JAX, but it does not work out of the box with MJX-Warp. Use the unified `where` method, which works for both implementations:

```python
data = data.where(done, reset_data)
```

### Graph modes

`mjx.put_model` takes `graph_mode`, a value of the `mjx.warp.GraphMode` enum that controls CUDA graph capture. See the [Warp JAX interoperability docs](https://nvidia.github.io/warp/stable/user_guide/interoperability/jax.html).

```python
import mujoco.mjx.warp as mjxw

model = mjx.put_model(mj_model, impl='warp', graph_mode=mjxw.GraphMode.WARP_STAGED)
```

| Mode | Behaviour |
|---|---|
| `JAX` | Does not work with MuJoCo Warp: Warp creates child graph nodes that cannot be rolled into the XLA graph. |
| `WARP` (default) | Warp captures and caches the CUDA graph using XLA buffer pointers. If JAX changes those pointers between calls, the graph is recaptured, which is expensive. |
| `WARP_STAGED` | Copies XLA buffers in and out of staging buffers so pointers stay stable. Captures once. Uses more memory. |
| `WARP_STAGED_EX` | Like `WARP_STAGED`, but the copies are moved outside the initial graph capture. |

Measured steps per second:

| Configuration | Humanoid | Aloha Pot |
|---|---|---|
| Pure Warp (No JAX FFI) | 3.35M | 2.45M |
| JAX FFI (`WARP`) | 2.96M | 2.33M |
| JAX FFI (`WARP_STAGED`) | 2.67M | 1.96M |
| JAX FFI (`WARP` with forced recaptures on every step) | 0.80M | 0.65M |

If your program is slowed by repeated graph captures, switch to `WARP_STAGED` or `WARP_STAGED_EX`.

### Batch rendering

MJX-Warp has a hardware-accelerated batch renderer for RGB and depth across parallel environments. Create a render context first. `nworld` is fixed at creation.

```python
from mujoco.mjx import create_render_context

rc = create_render_context(
    mjm=m,
    nworld=nworld,
    cam_res=(width, height),
    use_textures=True,
    use_shadows=True,
    render_rgb=[True] * ncam,
    render_depth=[False] * ncam,
    enabled_geom_groups=[0, 1, 2],
)
```

Keep a reference to `rc` for the life of the program. Pass `rc.pytree()`, a lightweight handle, into `jit`/`vmap` functions. Refit the BVH, then render:

```python
from mujoco.mjx import get_rgb

@jax.jit
def render_fn(mx, d, rc_pytree):
    # 1. Update the BVH for the current scene state
    d = mjx.refit_bvh(mx, d, rc_pytree)

    # 2. Render all configured cameras
    pixels, _, d = mjx.render(mx, d, rc_pytree)

    # 3. Extract the RGB tensor for the first camera (index 0)
    rgb = get_rgb(rc_pytree, 0, pixels)

    return rgb, d

rgb, d = render_fn(mx, d, rc.pytree())
```

- `refit_bvh` and `render` update an internal token (`d._impl._jax_token`). Thread `d` through both so XLA cannot reorder BVH updates and raycasts.
- `render` always returns a leading batch dimension of size `nworld`. Known issue: it does not work well with `jax.vmap(jax.lax.scan)`.

Multi-GPU: pass `devices` to create one context per device, then use `jax.pmap`. Full example: [visualize_render.py](https://github.com/google-deepmind/mujoco/blob/main/mjx/mujoco/mjx/warp/visualize_render.py).

```python
ndevices = jax.local_device_count()
nworld_per_device = nworld // ndevices

# Create one render context for all devices
rc = create_render_context(
    mjm=m,
    nworld=nworld_per_device,
    devices=[f'cuda:{i}' for i in range(ndevices)],
    cam_res=(width, height),
)
```

### Tuning

MJX-Warp handles many contacts and constraints and full mesh collisions. For tuning, follow the [MuJoCo Warp performance tuning](../mujoco-warp/SKILL.md) section.

## MJX-JAX

A re-implementation using the same algorithms as MuJoCo. It diverges from the MuJoCo API in a few places to suit JAX, and it lacks some features (see Feature parity). It succeeds Brax's generalized pipeline. Brax depends on `mujoco-mjx`, and that pipeline is no longer maintained.

### Performance tuning

Change these from the MuJoCo defaults:

| Setting | Advice |
|---|---|
| [option/iterations, option/ls_iterations](../../reference/xml-reference/SKILL.md) | Lower them until just before the simulation goes unstable. `NEWTON` converges in very few iterations (often one) and does well on GPU. `CG` is currently better on TPU. |
| [contact/pair](../../reference/xml-reference/SKILL.md) | List the valid contacts explicitly. This can have a dramatic effect on performance. |
| [maxhullvert](../../reference/xml-reference/SKILL.md) | Set it to `64` or less for faster convex mesh collisions. |
| [option/flag/eulerdamp](../../reference/xml-reference/SKILL.md) | Disabling it can help and is often not needed for stability (see [Numerical Integration](../../physics-computation/SKILL.md)). |
| [option/jacobian](../../reference/xml-reference/SKILL.md) | `"auto"` means sparse when `nv >= 60` or on TPU, dense otherwise. On TPU, `"sparse"` with Newton can be 2x to 3x faster. On GPU, `"dense"` can be 10% to 20% faster if it fits in memory. |
| Broadphase | Use the experimental custom numeric parameters `max_contact_points` (caps contact points sent to the solver per condim type) and `max_geom_pairs` (caps geom pairs per geom-type pair). See the [shadow hand](https://github.com/google-deepmind/mujoco/tree/main/mjx/mujoco/mjx/test_data/shadow_hand) config. |

On GPU, set `XLA_FLAGS=--xla_gpu_triton_gemm_any=true` (up to 30% faster on NVIDIA). With several GPUs, see the [JAX GPU performance tips](https://jax.readthedocs.io/en/latest/gpu_performance_tips.html).

### Sharp bits

MJX-JAX is built for big batches of identical scenes on SIMD hardware. MJX-Warp avoids all of the following:

- **Single scene:** one `mjData` can be **10x** slower than CPU MuJoCo. Run thousands to tens of thousands of scenes in parallel.
- **Large meshes:** convex collisions use a branchless Separating Axis Test, not MPR or GJK/EPA. Keep meshes to about **200 vertices or fewer** for mesh-primitive collisions and **fewer than 32** for convex-convex. Use [maxhullvert](../../reference/xml-reference/SKILL.md) to get there.
- **Many contacts:** the branchless broadphase is weaker than MuJoCo's. Throughput falls faster than CPU MuJoCo as contacts grow. One humanoid ran at 650K (M3 Max CPU), 1.8M (64-core AMD 3995WX CPU), 950K (A100, batch 8192) and 2.7M (8-chip v5 TPU, batch 16384) steps per second.

## Feature parity

Copying an [mjModel](../../reference/api-types/SKILL.md) that uses unsupported features raises an exception.

| Category | MJX-Warp | MJX-JAX |
|---|---|---|
| Dynamics | Forward, Inverse | Forward, Inverse |
| Differentiability | ✗ | ✓ (mostly, see [issue 2259](https://github.com/google-deepmind/mujoco/issues/2259)) |
| Joint | All | `FREE`, `BALL`, `SLIDE`, `HINGE` |
| Transmission | All | `JOINT`, `JOINTINPARENT`, `SITE`, `TENDON` |
| Actuator dynamics | All | `NONE`, `INTEGRATOR`, `FILTER`, `FILTEREXACT`, `MUSCLE` |
| Actuator gain | All | `FIXED`, `AFFINE`, `MUSCLE` |
| Actuator bias | All | `NONE`, `AFFINE`, `MUSCLE` |
| Geom | All | `PLANE`, `HFIELD`, `SPHERE`, `CAPSULE`, `BOX`, `MESH` fully. `ELLIPSOID` and `CYLINDER` only collide with other primitives. `BOX` is implemented as a mesh. |
| Constraint | All | `EQUALITY`, `LIMIT_JOINT`, `CONTACT_FRICTIONLESS`, `CONTACT_PYRAMIDAL`, `CONTACT_ELLIPTIC`, `FRICTION_DOF`, `FRICTION_TENDON` |
| Equality | All | `CONNECT`, `WELD`, `JOINT`, `TENDON` |
| Integrator | All except the `IMPLICITFAST` midpoint integrator feature | `EULER`, `RK4`, `IMPLICITFAST` (not with [fluid drag](../../physics-computation/fluid-forces/SKILL.md)) |
| Cone | All | `PYRAMIDAL`, `ELLIPTIC` |
| Condim | All | 1, 3, 4, 6 (1 not with `ELLIPTIC`) |
| Solver | All except `PGS`, `noslip` | `CG`, `NEWTON` |
| Fluid model | All | Inertia model only |
| Tendon wrapping | All | `JOINT`, `SITE`, `PULLEY`, `SPHERE`, `CYLINDER` |
| Tendons | All | Fixed, Spatial |
| Sensors | All except `PLUGIN` | See below |
| Flex | `VERTCOLLIDE`, `ELASTICITY` | Not supported |
| Mass matrix | Sparse and Dense | Sparse and Dense |
| Jacobian | `DENSE` and `SPARSE` | `DENSE` only |
| Lights | ✓ | Positions and directions |
| Ray | All, BVH for meshes, hfield and flex | Slow for meshes. hfield and flex unimplemented. |

MJX-JAX does not support `SDF` geoms, collisions between (`SPHERE`, `BOX`, `MESH`, `HFIELD`) and `CYLINDER`, or collisions between (`BOX`, `MESH`, `HFIELD`) and `ELLIPSOID`.

MJX-JAX sensors: `MAGNETOMETER`, `CAMPROJECTION`, `RANGEFINDER`, `JOINTPOS`, `TENDONPOS`, `ACTUATORPOS`, `BALLQUAT`, `FRAMEPOS`, `FRAMEXAXIS`, `FRAMEYAXIS`, `FRAMEZAXIS`, `FRAMEQUAT`, `SUBTREECOM`, `CLOCK`, `VELOCIMETER`, `GYRO`, `JOINTVEL`, `TENDONVEL`, `ACTUATORVEL`, `BALLANGVEL`, `FRAMELINVEL`, `FRAMEANGVEL`, `SUBTREELINVEL`, `SUBTREEANGMOM`, `TOUCH`, `CONTACT`, `ACCELEROMETER`, `FORCE`, `TORQUE`, `ACTUATORFRC`, `JOINTACTFRC`, `TENDONACTFRC`, `FRAMELINACC`, `FRAMEANGACC`. For `CONTACT`: matching `none-none`, `geom-geom`; reduction `mindist`, `maxforce`; data `all`.

## Command line tools

```shell
mjx-testspeed --mjcf=/PATH/TO/MJCF/ --base_path=.
```

Reports total simulation time, steps per second and realtime factor across all devices. Run it with `--help` to see the options.

```shell
mjx-viewer --help
```

Opens the model in the simulate viewer, stepped by MJX physics rather than C MuJoCo. Use it to debug solver parameters.

## Reinforcement learning

- JAX RL environments on MJX: the [rss2025](https://github.com/google-deepmind/mujoco_playground/tree/main/rss2025) directory of [MuJoCo Playground](https://playground.mujoco.org).
- New PyTorch RL and sim-to-real workflows on MuJoCo and MuJoCo Warp: [MuJoCo Playground](https://playground.mujoco.org) and [reaf-sim](https://reaf-sim.readthedocs.io).

## Source docs

Verbatim copies, for details not covered above:

- [mjx.md](references/mjx.md)
