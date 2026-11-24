---
name: api-globals
description: 'MuJoCo C API globals: error, memory and physics callbacks (mjcb_*), the collision function table, string and numeric constants (mjMINVAL, mjNEQDATA, ...), macros and X macros. Use when installing callbacks or needing a MuJoCo constant or macro.'
---

# MuJoCo API Globals

Look up MuJoCo's global C definitions: the error, memory and physics callbacks,
the narrow-phase collision table, the string constants used to label options in
GUIs, the numeric constants (limits and array sizes), the macros, and the X
macros. Use this skill to install a callback correctly or to find the value and
meaning of a constant.

The callback function types (`mjfGeneric`, `mjfConFilt`, `mjfSensor`,
`mjfTime`, `mjfAct`, `mjfCollision`) and the enums the strings name are defined
in [api-types](../api-types/SKILL.md). The functions mentioned here are in
[api-functions](../api-functions/SKILL.md).

## Callbacks: the rules

- Every user callback (a global function pointer whose name starts with `mjcb`)
  starts as NULL. NULL disables it, and the default processing runs.
- To install one, set the global pointer to a user function of the correct type.
- Callbacks are global, not model-specific. Models simulated in parallel share
  one set of callbacks.
- There is no automated error checking of callbacks.
- Physics callbacks often need non-standard parameters. Put them in the MJCF
  custom fields and user data arrays, and make the callback check that they
  exist before using them, so it disables itself on a regular model instead of
  crashing.

## Error callbacks (deprecated)

Both are deprecated: use `mju_setLogHandler` instead (see
[api-functions](../api-functions/SKILL.md) and "Installing a handler" in
[simulation-loop](../../c-programming/simulation-loop/SKILL.md)). If a custom
log handler is installed with `mju_setLogHandler`, neither callback is
consulted.

| Name | Declaration | Meaning |
|---|---|---|
| `mju_user_error` | `extern void (*mju_user_error)(const char*);` | Called by the default log handler on a fatal error; overrides default error processing. It may `longjmp` out or return, but MuJoCo assumes error handlers do not return: if one returns, behavior is undefined. |
| `mju_user_warning` | `extern void (*mju_user_warning)(const char*);` | Called by the default log handler when a warning occurs. |

## Memory callbacks

Install custom allocation and deallocation (for example, a MATLAB wrapper whose
mex files must use MATLAB's memory mechanism).

| Name | Declaration | Meaning |
|---|---|---|
| `mju_user_malloc` | `extern void* (*mju_user_malloc)(size_t);` | Used for all heap memory the MuJoCo runtime needs, instead of aligned malloc. Must return memory aligned on 8-byte boundaries. The C++ parser and compiler sometimes use `new`, which bypasses it. |
| `mju_user_free` | `extern void (*mju_user_free)(void*);` | Frees heap memory MuJoCo allocated, instead of aligned free. |

## Physics callbacks

Options control the default pipeline; physics callbacks extend it at
well-defined places.

| Name | Declaration | Meaning |
|---|---|---|
| `mjcb_passive` | `extern mjfGeneric mjcb_passive;` | Custom passive force in joint space (depends on position and velocity, not control). Standard passive forces (springs, dampers, viscosity, density) are already in `mjData.qfrc_passive` when it runs: **add** to that vector, do not overwrite it. For Cartesian forces, map with the end-effector Jacobian. |
| `mjcb_control` | `extern mjfGeneric mjcb_control;` | Control law. Writes `mjData.ctrl`, and may write `mjData.qfrc_applied` and `mjData.xfrc_applied`. Called from `mj_forward` and `mj_step` just before controls are needed; 4 times per step with the RK integrator. |
| `mjcb_contactfilter` | `extern mjfConFilt mjcb_contactfilter;` | Replaces default collision filtering. Called for each geom pair that passed the broad phase (or is a predefined MJCF pair). Replaces the whole mechanism: re-implement contype/conaffinity yourself if you need them. |
| `mjcb_sensor` | `extern mjfSensor mjcb_sensor;` | Fills `mjData.sensordata` for user-defined sensors. Called once per stage (`mjSTAGE_POS`, `mjSTAGE_VEL`, `mjSTAGE_ACC`) when the model has user sensors; must fill all user sensor values for that stage, respecting the MJCF dimensions and data types. |
| `mjcb_time` | `extern mjfTime mjcb_time;` | Enables the built-in profiler; timing statistics go to `mjData.timer`. Returns `mjtNum`; units are up to you, but simulate.cc and the `mjTOPIC_TIME_STP` topic assume 1 millisecond. Use a high-resolution timer (at least microsecond precision). |
| `mjcb_act_dyn` | `extern mjfAct mjcb_act_dyn;` | Returns `mjData.act_dot` (time-derivative of `mjData.act`) for actuators with user dynamics (`mjDYN_USER`). Not installed: the derivative is 0. |
| `mjcb_act_gain` | `extern mjfAct mjcb_act_gain;` | Returns the gain for actuators with `mjModel.actuator_gaintype` = `mjGAIN_USER`. Not installed: gain is 1. |
| `mjcb_act_bias` | `extern mjfAct mjcb_act_bias;` | Returns the bias for actuators with `mjModel.actuator_biastype` = `mjBIAS_USER`. Not installed: bias is 0. |

### Control callback pitfalls

- Values written by `mjcb_control` may depend on position, velocity and
  quantities derived from them. They cannot depend on contact forces or other
  quantities computed after the control is set: read there, those fields do
  not match the current time step.
- Alternatives: set controls before `mj_step`, or call `mj_step1`, set
  controls (using its position and velocity results), then `mj_step2`.
- Only the control callback can change controls between the RK integrator's
  sub-steps.

## Collision table

```C
extern mjfCollision mjCOLLISIONFUNC[mjNGEOMTYPES][mjNGEOMTYPES];
```

- Pairwise narrow-phase collision functions, indexed by geom type. Only the
  upper-right triangle is used.
- Replace an entry with a custom routine to replace MuJoCo's collider for that
  pair. A NULL entry means that pair of geom types cannot collide.
- The broad phase is built in and cannot be modified.
- Custom colliders get a return buffer of size `mjMAXCONPAIR` (50); writing
  more contacts can cause unpredictable behavior.
- The built-in function for each pair is listed in the "Pair-wise colliders"
  table in [physics-computation](../../physics-computation/SKILL.md).

## String constants

English names of option lists, for menus and dialogs in a GUI (simulate.cc,
see [c-programming](../../c-programming/SKILL.md), shows how). Each array is
indexed by the matching enum in [api-types](../api-types/SKILL.md).

| Declaration | Enum | Entries, in index order |
|---|---|---|
| `const char* mjDISABLESTRING[mjNDISABLE]` | `mjtDisableBit` | Constraint, Equality, Frictionloss, Limit, Contact, Spring, Damper, Gravity, Clampctrl, Warmstart, Filterparent, Actuation, Refsafe, Sensor, Midphase, Eulerdamp, AutoReset, NativeCCD, Island, MultiCCD |
| `const char* mjENABLESTRING[mjNENABLE]` | `mjtEnableBit` | Override, Energy, Fwdinv, InvDiscrete, Sleep, DiagExact, IPC, Speculative |
| `const char* mjTIMERSTRING[mjNTIMER]` | `mjtTimer` (mjData timers) | step, forward, inverse, position, velocity, actuation, constraint, advance, pos_kinematics, pos_inertia, pos_collision, pos_make, pos_project, col_broadphase, col_narrowphase |
| `const char* mjTOPICSTRING[mjNTOPIC]` | `mjtLogTopic` | Step timing, Compile timing, Sleep/wake |
| `const char* mjLABELSTRING[mjNLABEL]` | `mjtLabel` | None, Body, Joint, Geom, Site, Camera, Light, Tendon, Actuator, Constraint, Flex, Skin, Selection, SelPoint, Contact, ContactForce, Island |
| `const char* mjFRAMESTRING[mjNFRAME]` | `mjtFrame` | None, Body, Geom, Site, Camera, Light, Contact, World |

### mjVISSTRING and mjRNDSTRING

Three strings per flag: `[0]` flag name; `[1]` `"0"` or `"1"`, whether the
flag is on by default; `[2]` a one-character suggested keyboard shortcut for
interactive viewers (empty if none).

```C
const char* mjVISSTRING[mjNVISFLAG][3] = {
  {"Convex Hull",     "0", "H"},
  {"Texture",         "1", "X"},
  {"Joint",           "0", "J"},
  {"Camera",          "0", "Q"},
  {"Actuator",        "0", "U"},
  {"Activation",      "0", ","},
  {"Light",           "0", "Z"},
  {"Tendon",          "1", "V"},
  {"Range Finder",    "1", "Y"},
  {"Equality",        "0", "E"},
  {"Inertia",         "0", "I"},
  {"Scale Inertia",   "0", "'"},
  {"Perturb Force",   "0", "B"},
  {"Perturb Object",  "1", "O"},
  {"Contact Point",   "0", "C"},
  {"Island",          "0", "N"},
  {"Contact Force",   "0", "F"},
  {"Contact Split",   "0", "P"},
  {"Transparent",     "0", "T"},
  {"Auto Connect",    "0", "A"},
  {"Center of Mass",  "0", "M"},
  {"Select Point",    "0", ""},
  {"Static Body",     "1", "D"},
  {"Skin",            "1", ";"},
  {"Flex Vert",       "0", ""},
  {"Flex Edge",       "1", ""},
  {"Flex Face",       "0", ""},
  {"Flex Skin",       "1", ""},
  {"Body Tree",       "0", "`"},
  {"Mesh Tree",       "0", "\\"},
  {"SDF iters",       "0", ""}
};
```

`mjVISSTRING` describes `mjtVisFlag`; its defaults are those set by
`mjv_defaultOption`.

```C
const char* mjRNDSTRING[mjNRNDFLAG][3] = {
  {"Shadow",          "1", "S"},
  {"Wireframe",       "0", "W"},
  {"Reflection",      "1", "R"},
  {"Additive",        "0", "L"},
  {"Skybox",          "1", "K"},
  {"Fog",             "0", "G"},
  {"Haze",            "1", "/"},
  {"Depth",           "0", ""},
  {"Segment",         "0", ","},
  {"Id Color",        "0", ""},
  {"Cull Face",       "1", ""},
  {"Post Processing", "1", ""}
};
```

`mjRNDSTRING` describes the OpenGL rendering flags `mjtRndFlag`; its defaults
are those set by `mjv_makeScene`.

## Numeric constants

Many integer constants are documented with the types in
[api-types](../api-types/SKILL.md). Extended key codes `mjKEY_XXX` (GLFW key
codes) are defined in
[mjui.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjui.h)
and not listed here.

### Version ([mujoco.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mujoco.h))

| Symbol | Value | Meaning |
|---|---|---|
| `mjVERSION_HEADER` | 4000002 | Header version, `(S * 1e6) + (M * 1e3) + P` for "S.M.P" (4.2.1 is 4002001). `mj_version` returns the same for the compiled library. See [VERSIONING.md](https://github.com/google-deepmind/mujoco/blob/main/VERSIONING.md). |

### Engine constants ([mjmodel.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjmodel.h); first three in [mjtype.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjtype.h))

| Symbol | Value | Meaning |
|---|---|---|
| `mjMINVAL` | 1E-15 | Minimal value in any denominator or operation where 0 is not allowed. Smaller values are almost always silently clamped to it. |
| `mjPI` | π | Used in trigonometric functions and the compiler's degrees-to-radians conversion. |
| `mjMAXVAL` | 1E+10 | Maximal absolute value in `mjData.qpos`, `qvel`, `qacc`. `mj_checkPos`, `mj_checkVel`, `mj_checkAcc` use it to detect instability. |
| `mjMINMU` | 1E-5 | Minimal friction coefficient for any included friction dimension (see condim); smaller values are clamped. |
| `mjMINIMP` | 0.0001 | Minimal constraint impedance; smaller values are clamped. |
| `mjMAXIMP` | 0.9999 | Maximal constraint impedance; larger values are clamped. |
| `mjMAXCONPAIR` | 50 | Maximal contact points per geom pair. User collision functions get a buffer of this size and must respect it. |
| `mjMAXTREEDEPTH` | 50 | Maximal depth of each body and mesh bounding volume hierarchy. Exceeding it raises a warning and ray casting may not be possible. |
| `mjMAXFLEXNODES` | 27 | Maximal nodes in a trilinear flex element. |
| `mjMINAWAKE` | 10 | Minimal timesteps after a tree is awoken before it may sleep again. |

### Array sizes ([mjmodel.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjmodel.h))

Kept symbolic because they may grow in future versions.

| Symbol | Value | Meaning |
|---|---|---|
| `mjNEQDATA` | 12 | Parameters per equality constraint; size of `mjModel.eq_data`. |
| `mjNDYN` | 10 | Activation dynamics parameters per actuator; size of `mjModel.actuator_dynprm`. |
| `mjNGAIN` | 10 | Gain parameters per actuator; size of `mjModel.actuator_gainprm`. |
| `mjNBIAS` | 10 | Bias parameters per actuator; size of `mjModel.actuator_biasprm`. |
| `mjNPOLY` | 2 | Nonlinear polynomial coefficients for joint and tendon stiffness and damping; size of `mjModel.{jnt,tendon}_{stiffness,damping}poly`. See polynomial forces in [physics-computation](../../physics-computation/SKILL.md). |
| `mjNFLUID` | 12 | Per-geom fluid interaction parameters of the ellipsoidal model. |
| `mjNREF` | 2 | Reference acceleration parameters per scalar constraint; size of all `mjModel.XXX_solref`. |
| `mjNIMP` | 5 | Impedance parameters per scalar constraint; size of all `mjModel.XXX_solimp`. |
| `mjNSENS` | 3 | Sensor parameters; size of `mjModel.sensor_intprm`. |
| `mjNSOLVER` | 200 | Solver iterations whose statistics fit in `mjData.solver`. Actual count: `mjData.solver_niter`. |
| `mjNISLAND` | 20 | Islands whose solver statistics fit in `mjData.solver`. Actual count: `mjData.nsolver_island`. |

### Visualization ([mjvisualize.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjvisualize.h))

| Symbol | Value | Meaning |
|---|---|---|
| `mjNGROUP` | 6 | Geom, site, joint, tendon and actuator groups toggled via `mjvOption`. |
| `mjMAXLIGHT` | 100 | Maximal lights in a scene. |
| `mjMAXOVERLAY` | 500 | Maximal characters in overlay text. |
| `mjMAXLINE` | 100 | Maximal lines per 2D figure (`mjvFigure`). |
| `mjMAXLINEPNT` | 1001 | Maximal points per figure line; `mjvFigure.linepnt` has length `2*mjMAXLINEPNT` (X and Y). |
| `mjMAXPLANEGRID` | 200 | Maximal grid lines per dimension when rendering planes. |

### Rendering ([mjrender.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjrender.h))

| Symbol | Value | Meaning |
|---|---|---|
| `mjNAUX` | 10 | Auxiliary buffers that can be allocated in `mjrContext`. |
| `mjMAXTEXTURE` | 1000 | Maximal textures. |
| `mjMAXMATERIAL` | 1000 | Maximal materials with textures. |

### UI ([mjui.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjui.h))

| Symbol | Value | Meaning |
|---|---|---|
| `mjMAXUISECT` | 10 | UI sections. |
| `mjMAXUIITEM` | 200 | Items per UI section. |
| `mjMAXUITEXT` | 300 | Characters in UI fields 'edittext' and 'other'. |
| `mjMAXUINAME` | 40 | Characters in any UI name. |
| `mjMAXUIMULTI` | 35 | Radio and select items in a UI group. |
| `mjMAXUIEDIT` | 7 | Elements in a UI edit list. |
| `mjMAXUIRECT` | 25 | UI rectangles. |

## Macros

| Macro | Definition | Use |
|---|---|---|
| `mjUSESINGLE` | (compile-time flag) | Selects the `mjtNum` precision; see `mjtNum` in [api-types](../api-types/SKILL.md). |
| `mjDISABLED(x)` | `#define mjDISABLED(x) (m->opt.disableflags & (x))` | Is standard feature `x` (`mjtDisableBit`) disabled? Needs `mjModel* m` in scope. |
| `mjENABLED(x)` | `#define mjENABLED(x) (m->opt.enableflags & (x))` | Is optional feature `x` (`mjtEnableBit`) enabled? Needs `mjModel* m` in scope. |
| `mjMAX(a,b)` | `#define mjMAX(a,b) (((a) > (b)) ? (a) : (b))` | Maximum. Arguments are evaluated twice; for `mjtNum` use `mju_max`. |
| `mjMIN(a,b)` | `#define mjMIN(a,b) (((a) < (b)) ? (a) : (b))` | Minimum. Arguments are evaluated twice; for `mjtNum` use `mju_min`. |

### mjPLUGIN_LIB_INIT

```C
#define mjPLUGIN_LIB_INIT(n)                                      \
     static void _mj_init_##n(void) __attribute__((constructor)); \
     static void _mj_init_##n(void)
```

Registers a plugin before `main()` runs. `n` is a unique identifier that
avoids name collisions between plugin initialization functions. See plugin
registration in [engine-plugins](../../c-programming/engine-plugins/SKILL.md).

## X Macros

Most projects do not need them. MuJoCo uses them internally to allocate the
model; they help when writing wrappers for scripting languages that must build
structures matching MuJoCo's data structures programmatically. The definitions
are in
[mjxmacro.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjxmacro.h)
and
[mjspecmacro.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjspecmacro.h);
the docs do not list them.

## Source docs

Verbatim copies, for details not covered above:

- [APIreference/APIglobals.md](references/APIreference-APIglobals.md)
