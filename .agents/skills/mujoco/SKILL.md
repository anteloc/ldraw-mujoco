---
name: mujoco
description: 'MuJoCo (Multi-Joint dynamics with Contact) physics engine: core concepts (mjModel, mjData, mjSpec, MJCF/XML models, bodies, joints, geoms, sites, actuators, sensors, equality constraints, contacts, options) and the map to task subskills for Python bindings, MJCF modeling, model editing, simulation, physics, rendering, viewers, GPU backends and the API/XML references. Use when code imports `mujoco`, loads or writes MJCF XML, steps a simulation with mj_step, or tunes contacts, joints, solvers or rendering.'
---

# MuJoCo

MuJoCo (**Mu**lti-**Jo**int dynamics with **Co**ntact) is a general purpose physics engine for robotics, biomechanics, graphics, animation and machine learning. This skill gives the mental model shared by every subskill: how models are described, compiled and simulated, what the model elements are, and the conventions (units, names, ids, coordinates) that most often confuse new users. Use the subskills for task details.

- Code: [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) (open source since May 2022, [license](https://github.com/google-deepmind/mujoco/blob/main/LICENSE)).
- Try in the browser with nothing installed: [mujoco.org](https://mujoco.org), and [live.mujoco.org](https://live.mujoco.org) to drag and drop your own models (WebAssembly build of [MuJoCo Studio](studio-viewers/SKILL.md), slower than native C).
- Also: [MuJoCo Playground](https://playground.mujoco.org).

## What MuJoCo is

- A C/C++ library with a C API. First-class [Python bindings](python-bindings/SKILL.md) give access to the full C API.
- Models are written in **MJCF**, an XML format designed to be human readable and editable. URDF files can also be loaded.
- The built-in parser and compiler turn the model into low-level, preallocated runtime structures. The runtime does **zero memory allocations** after initialization.
- Simulation runs in **generalized (joint) coordinates** with **optimization-based, soft, convex contact dynamics**. The default Newton solver converges quadratically; CG and a generalized PGS are alternatives. See [physics-computation](physics-computation/SKILL.md).
- GPU backends [MJX](accelerated-simulation/mjx/SKILL.md) (JAX) and [MuJoCo Warp](accelerated-simulation/mujoco-warp/SKILL.md) (NVIDIA Warp) consume the same `mjModel` and `mjData`.
- Engine plugins (dynamically loaded shared libraries) add custom sensors, actuators and passive forces: [engine plugins](c-programming/engine-plugins/SKILL.md).

## Model, spec and data

MuJoCo separates constant model description from time-varying state:

| Struct | Role |
|---|---|
| `mjSpec` | High-level, in-memory model; one-to-one with MJCF. Create or edit it in code, save to MJCF/MJZ, or compile it. |
| `mjModel` | Compiled, cross-indexed low-level model. Expected to stay constant; embedded options (`mjOption`, `mjVisual`, `mjStatistic`) may be changed by the user between steps. |
| `mjData` | All dynamic variables and intermediate results. A scratch pad every function reads from and writes to, with a preallocated internal stack. |

`mjModel` is built by the compiler. `mjData` is built at runtime from an `mjModel`. Top-level functions take both:

``` C
void mj_step(const mjModel* m, mjData* d);
```

Because of this split, many `mjData` instances can share one `mjModel`; run each on its own thread for parallel sampling or finite differences ([multi-threading](c-programming/simulation-loop/SKILL.md)). A single step is single-threaded by default, but constraint islands allow per-island parallelism.

### Paths to an mjModel

- (text editor) → MJCF/URDF file → (MuJoCo parser → mjSpec → compiler) → mjModel
- MJZ archive → (MJZ decoder → mjSpec → compiler) → mjModel
- (user code) → mjSpec → (MuJoCo compiler) → mjModel
- MJB file → (model loader) → mjModel

| Medium | High level | Low level |
|---|---|---|
| File | MJCF/URDF (XML), MJZ (Zip archive) | MJB (binary) |
| Memory | `mjSpec` | `mjModel` |

MJB files are version-specific and cannot be decompiled. Maintain models as XML or MJZ archives. Models and specs can be serialized back to disk with *mj_encode*. Programmatic construction and editing: [model-editing](model-editing/SKILL.md).

## Canonical usage

A plane, a light and a free-floating box (`hello.xml`):

``` xml
<mujoco>
  <worldbody>
    <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
    <geom type="plane" size="1 1 0.1" rgba=".9 0 0 1"/>
    <body pos="0 0 1">
      <joint type="free"/>
      <geom type="box" size=".1 .2 .3" rgba="0 .9 0 1"/>
    </body>
  </worldbody>
</mujoco>
```

Simulate the passive dynamics without rendering (valid C and C++):

``` c
#include "mujoco.h"
#include "stdio.h"

char error[1000];
mjModel* m;
mjData* d;

int main(void) {
  // load model from file and check for errors
  m = mj_loadXML("hello.xml", NULL, error, 1000);
  if (!m) {
    printf("%s\n", error);
    return 1;
  }

  // make data corresponding to model
  d = mj_makeData(m);

  // run simulation for 10 seconds
  while (d->time < 10)
    mj_step(m, d);

  // free model and data
  mj_deleteData(d);
  mj_deleteModel(m);

  return 0;
}
```

The pattern is always: load/compile → make data → call `mj_step` in a loop (setting controls or forces as needed) → free. For the Python equivalent (`mujoco` package), see [python-bindings](python-bindings/SKILL.md).

A richer MJCF example showing defaults, a skybox texture, ball and hinge joints, sites and a spatial tendon:

``` xml
<mujoco model="example">
  <default>
    <geom rgba=".8 .6 .4 1"/>
  </default>

  <asset>
    <texture type="skybox" builtin="gradient" rgb1="1 1 1" rgb2=".6 .8 1" width="256" height="256"/>
  </asset>

  <worldbody>
    <light pos="0 1 1" dir="0 -1 -1" diffuse="1 1 1"/>
    <body pos="0 0 1">
      <joint type="ball"/>
      <geom type="capsule" size="0.06" fromto="0 0 0  0 0 -.4"/>
      <body pos="0 0 -0.4">
        <joint axis="0 1 0"/>
        <joint axis="1 0 0"/>
        <geom type="capsule" size="0.04" fromto="0 0 0  .3 0 0"/>
        <body pos=".3 0 0">
          <joint axis="0 1 0"/>
          <joint axis="0 0 1"/>
          <geom pos=".1 0 0" size="0.1 0.08 0.02" type="ellipsoid"/>
          <site name="end1" pos="0.2 0 0" size="0.01"/>
        </body>
      </body>
    </body>

    <body pos="0.3 0 0.1">
      <joint type="free"/>
      <geom size="0.07 0.1" type="cylinder"/>
      <site name="end2" pos="0 0 0.1" size="0.01"/>
    </body>
  </worldbody>

  <tendon>
    <spatial limited="true" range="0 0.6" width="0.005">
      <site site="end1"/>
      <site site="end2"/>
    </spatial>
  </tendon>
</mujoco>
```

Note how little is specified: body frames and inertias are inferred from geoms (uniform density), collision rules are automatic, and friction, gravity and timestep take defaults. Multiple joints in one body need no dummy bodies. Only elements referenced elsewhere (the sites) are named. Writing MJCF: [mjcf-modeling](mjcf-modeling/SKILL.md); every attribute: [XML reference](reference/xml-reference/SKILL.md).

## Model elements

### Options (always present)

| Struct | Contents |
|---|---|
| `mjOption` | Physics options: algorithms and parameters, enable/disable pipeline parts, gravity and other system properties. |
| `mjVisual` | Visualization options (session OpenGL options are not part of the model). |
| `mjStatistic` | Compiler-computed statistics (average body mass, spatial extent); used by the visualizer for scaling. |

Options may be changed before each time step, never within one.

### Assets (referenced by name; every asset has a name)

| Asset | Key facts |
|---|---|
| Mesh | OBJ or binary STL (or embedded in XML). Collision uses the **convex hull**. Can infer inertia. No color of its own: colored by the geom's material. |
| Skin | Deforming meshes attached to bodies ("bones"). Visual only. |
| Height field | PNG (gray-scale) or custom binary; normalized to [0-1], extent from geom size. Only on geoms attached to the world body. At most the first 64 contacts per geom pair are kept. |
| Texture | PNG, KTX or procedural; 2D or cube mapping; skyboxes. Referenced only through a material. |
| Material | Appearance of geoms, sites and tendons (RGBA, specularity, shininess, emission, reflectance). Local `rgba` takes precedence over the material. |

### Kinematic tree (elements inside bodies)

- **World body** has id `0` and is its own parent: `body_parentid[0] == 0`, and `body_parentid[i] < i` otherwise. The world and joint-less children form a static tree with no DOFs.
- **Kinematic loops are not allowed**; model loop joints with equality constraints.
- **Body**: mass and inertia, no geometry. Has a definition frame and an inertial frame (at the COM, principal axes). Count: `nbody`.
- **Joint**: **adds** DOFs between a body and its parent; no joint means welded to the parent. Types: ball, slide, hinge, free. Ball/free orientations are unit quaternions. Count: `njnt`.
  - Reference pose `mjModel.qpos0`: reset sets `mjData.qpos = qpos0`; joints transform by `qpos - qpos0`. The `ref` attribute applies only to slide and hinge.
  - Spring reference `mjModel.qpos_spring` (attribute `springref` for slide/hinge).
- **DOF**: velocity/force coordinates (friction loss, damping, armature). Joints carry position properties (limits, stiffness). Created by the compiler. Count: `nv`.
- **Tree**: a movable body and all its descendants. Bodies, joints and DOFs of a tree are sequential (depth-first). Count: `ntree`. Island discovery and sleeping work per tree. `body_subtreemass` is per-body subtree mass (a different notion).
- **Geom**: 3D shape rigidly attached to a body; collision, rendering and inertia inference. Primitives: plane, sphere, capsule, ellipsoid, cylinder, box; also mesh and height field. Only **convex** collisions: build non-convex shapes from several geoms in one body. Count: `ngeom`.
- **Site**: light geom marking a frame of interest. No collisions, no inertia. Used for sensors, tendon routing, slider-crank endpoints. Count: `nsite`.
- **Camera**: fixed to the world or a body; fov, IPD, oblique projections, separate focal lengths and principal point. Count: `ncam`.
- **Light**: world- or body-attached; shadows cost one render pass each. A built-in headlight (default "auto") moves with the camera. Count: `nlight`.

### Stand-alone elements

| Element | Purpose |
|---|---|
| Tendon | Scalar length element. **Fixed**: linear combination of joint positions. **Spatial**: shortest path through sites, wrapping spheres/cylinders (separate wrapping geoms with sites), pulleys. Used for actuation, limits, equality, spring-dampers, friction loss. |
| Actuator | Transmission (joint, tendon, slider-crank, site, body) + activation dynamics + force generation. Models motors, cylinders, PD controllers, muscles. |
| Sensor | Writes `mjData.sensordata`; not used internally. Touch, IMU, force-torque, joint/tendon, actuator, frame, rangefinder, user sensors and more. Camera sensors are done by off-screen rendering. |
| Equality | Connect (ball joint outside the tree), weld, fix joint/tendon position, couple two joints/tendons via a cubic polynomial, keep flex edge lengths. |
| Flex | Deformable 1D/2D/3D meshes (capsules, triangles, tetrahedra) built from multiple bodies; collide and create shape-preserving forces. `flexcomp` expands meshes, grids and shapes automatically. |
| Contact pair | Explicit geom pair with its own contact parameters; complements the automatic ("dynamic") pair generation. |
| Contact exclude | Body pairs removed from candidate contacts. |
| Custom numeric / text / tuple | User data: named numeric arrays, `nuser_XXX` per-element arrays, `mjData.userdata`; text fields; lists of elements. Not used by the simulator. |
| Keyframe | Snapshot of qpos, qvel, activations, controls, mocap poses and time, for resets. Not for trajectory storage. |

## Conventions and clarifications

### Units

MuJoCo does not fix units; any consistent system works. Prefer MKS, since two defaults assume it: gravity `(0, 0, -9.81)` and geom density `1000` (water). Angles may be given in degrees in MJCF (degrees are the default), but **everything in `mjModel` and `mjData` is in radians**.

### Names and ids

- Each element type has arrays in `mjModel` sized by a count (`njnt`, ...). Matrices are row-major:

  ``` C
  mjtNum* jnt_range;             // joint limits       (njnt x 2)
  ```

- Element types are the enum `mjtObj` ([mjtype.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjtype.h)). *mj_name2id* / *mj_id2name* map names to 0-based ids and back.
- Names are optional, required only to reference an element in XML; two elements of the same type cannot share a name. Unnamed elements render as "joint N".
- `mj_name2id` returns -1 if not found. Always check:

  ``` C
  int jntid = mj_name2id(m, mjOBJ_JOINT, "elbow");
  if (jntid >= 0)
     printf("(%f, %f)\n", m->jnt_range[2*jntid], m->jnt_range[2*jntid+1]);
  ```

### Data-oriented design

There are no objects with private state: a few data structures and many functions taking `mjModel` and `mjData`. No globals, so each thread can use its own `mjData`.

### Bodies, geoms, sites

All three have frames computed each step from `mjData.qpos` by forward kinematics: `xpos`, `xquat`, `xmat` (bodies), `geom_xpos`, `geom_xmat` (geoms), `site_xpos`, `site_xmat` (sites). Bodies hold inertia and build the tree. Geoms hold appearance and collision shape; their mass or density only feeds the parent body's inertia at compile time (`shellinertia` puts mass on the surface). Compiled geoms have no inertial properties. Sites hold neither.

### Joint coordinates and floating bodies

- Joints **add** DOFs; constraints of the tree are implicit and cannot be violated. Body poses follow from `qpos` by forward kinematics and cannot be set directly (use IK), except for root bodies.
- A free joint stores 7 numbers in `qpos` (3D position, then unit quaternion) and 6 in `qvel` (linear, then angular velocity). Position, linear velocity and the quaternion are in the **global frame**; angular velocity is in the **local body frame**. Accelerations use the velocity space.
- See `freejoint/align` in the [XML reference](reference/xml-reference/SKILL.md) for aligning the free-joint frame with the inertia; structured state access is in [simulation-loop](c-programming/simulation-loop/SKILL.md).

### Surprising collisions

Geoms of a direct parent-child body pair do not collide, **unless the parent is static** (the world or a body with no DOFs relative to it). Removing the root joint of a floating base therefore makes new collisions appear. Fixes:

1. Make the body a mocap body (its children keep the parent-child exclusion; it can be moved interactively).
2. Keep the root joint; disable gravity and maybe add fluid viscosity.
3. Filter collisions with `contype`/`conaffinity` or a contact `exclude`.

### Divergence

Usually shows as an `mjWARN_BADQACC` warning. It means the timestep is too large for the integrator; reduce the timestep and/or switch to a more stable integrator. If that fails, look elsewhere, e.g. bodies initialized in penetration.

### Softness and slip

The constraint model is inherently soft: pushing harder always gives more acceleration, which keeps the problem convex and the inverse dynamics unique. Consequently gradual contact slip and gradual yielding of frictional joints under gravity are expected, and usually not a sign of too little friction. To reduce them:

- Tune `solref` and `solimp`; raising constraint impedance (first two `solimp` elements) and `mjModel.opt.impratio` is particularly effective. This may need smaller timesteps.
- The recommended approach is the Newton solver with elliptic friction cones and a large `impratio`.
- The NoSlip post-processing solver suppresses slip more strongly but leaves the convex formulation and can be less robust.

Details: [physics-computation](physics-computation/SKILL.md) and the "preventing slip" tips in [mjcf-modeling](mjcf-modeling/SKILL.md).

## Other features worth knowing

- **Reconfigurable pipeline**: `mj_step` runs everything, but option flags can disable pipeline parts and many lower-level functions can be called directly. Callbacks implement custom forces, actuators, collisions and controllers.
- **Constraint islands and sleeping**: independent groups of bodies are solved separately; stationary islands can sleep to save computation.
- **Visualization**: [MuJoCo Studio](studio-viewers/SKILL.md) (Filament rendering, Dear ImGui panels, plugins; native and browser, plus Python native or web viewers). A classic OpenGL renderer is used by the `simulate` sample: [visualization-rendering](c-programming/visualization-rendering/SKILL.md). Both support perturbing bodies with the mouse.

## Which subskill for which task

| Task | Subskill |
|---|---|
| Python: load, step, inspect, view, render | [python-bindings](python-bindings/SKILL.md) |
| Write or debug MJCF, tune contacts and stability, Menagerie models | [mjcf-modeling](mjcf-modeling/SKILL.md) |
| Build or edit models in code, attach subtrees, save XML/MJZ | [model-editing](model-editing/SKILL.md) |
| C/C++ builds, headers, samples (`simulate`, `testspeed`) | [c-programming](c-programming/SKILL.md) |
| Solvers, constraints, collision, pipeline, derivatives | [physics-computation](physics-computation/SKILL.md) |
| Interactive viewers, Studio plugins | [studio-viewers](studio-viewers/SKILL.md) |
| Batched GPU/TPU simulation (MJX, MJWarp) | [accelerated-simulation](accelerated-simulation/SKILL.md) |
| Unity, OpenUSD | [interop](interop/SKILL.md) |
| Exact attribute, struct field, function, enum, version change | [reference](reference/SKILL.md) |

## Subskills

Read the one that matches your task:

- [python-bindings](python-bindings/SKILL.md): The `mujoco` Python package: installation, MjModel.from_xml_string/from_xml_path, MjData, mj_step / mj_forward, named access (model.body('x'), data.joint('y')), the interactive viewer (mujoco.viewer.launch, launch_passive), Renderer, MjSpec model editing from Python, rollout, minimize and other utilities, building from source and migrating from mujoco-py. Use when writing Python that loads, steps, inspects, edits or views MuJoCo models.
- [mjcf-modeling](mjcf-modeling/SKILL.md): Writing MuJoCo models in MJCF: kinematic trees, defaults and classes, joints and degrees of freedom, geoms and meshes, contact pairs and excludes, equality constraints (connect, weld), tendons, actuators, sensors, solref/solimp, margin and friction tuning, inertia from geoms, tips and tricks, model tuning for stability, and the MuJoCo Menagerie model gallery. Use when designing or debugging an MJCF model, choosing contact or solver parameters, or fixing unstable, jittering or penetrating simulations.
- [model-editing](model-editing/SKILL.md): Programmatic model construction with mjSpec: parsing and loading (mj_parseXML, mj_loadXML), compiling (mj_compile, recompile), encoding and saving (mj_saveXML), attaching subtrees, MJZ archives, custom formats and the virtual file system. Use when building or modifying models in code instead of hand-written XML, attaching one model into another, or saving a compiled model back to XML.
- [c-programming](c-programming/SKILL.md): Using MuJoCo from C/C++: getting started, building from source and with Bazel, header files, versions and compatibility, naming conventions and the sample programs (testspeed, simulate, compile, basic, render). Use when writing or building native code against libmujoco, or when C-API conventions explain behaviour also seen from Python.
- [physics-computation](physics-computation/SKILL.md): How MuJoCo computes physics: soft contact model, generalized coordinates, the constraint model (equality, friction loss, limits, contacts), constraint solvers (Newton, CG, PGS) and their parameters, collision detection (broadphase, convex/multiccd, margins), sleeping islands, the simulation pipeline and derivatives. Use when reasoning about solver choice, constraint softness (solref, solimp), contact penetration or creep, friction, or why a simulation behaves as it does.
- [studio-viewers](studio-viewers/SKILL.md): MuJoCo Studio: web viewers (MuJoCo Live, WebViewer, browser sandboxing), native viewers (standalone app, Python NativeViewer, rendering backends), architecture (thread model, message passing), Python viewer and simulation plugins with lifecycle events and hot reload, and C++/WebAssembly builds. Use when viewing models interactively, embedding a viewer, or writing Studio plugins.
- [accelerated-simulation](accelerated-simulation/SKILL.md): Running MuJoCo on accelerators with batched, parallel simulation: MuJoCo XLA (MJX, JAX) and MuJoCo Warp (MJWarp, NVIDIA Warp). Use when many environments must step in parallel on GPU/TPU, for reinforcement learning, or when choosing between MJX, MJWarp and CPU MuJoCo.
- [interop](interop/SKILL.md): MuJoCo integrations with other tools: the Unity plug-in (installation, importing MJCF, design and implementation notes) and OpenUSD support (building with USD, mjcPhysics schemas, the MJCF file format plugin, importing USD into MJCF and exporting to USD). Use when moving MuJoCo models to or from Unity or USD pipelines.
- [reference](reference/SKILL.md): MuJoCo reference material: the MJCF XML element and attribute reference, the C API types, functions and globals, and the changelog. Use when an exact XML attribute, default value, struct field, function signature, enum or version change is needed.

## Source docs

Verbatim copies, for details not covered above:

- [index.md](references/index.md)
- [overview.md](references/overview.md)
