---
name: simulation-loop
description: 'Running simulations with the MuJoCo API: initialization, the simulation loop, state and control (mjtState, qpos, qvel, ctrl), forward and inverse dynamics, multi-threading, changing mjModel at runtime, data layout and the internal stack, errors/warnings/logging, diagnostics, Jacobians (mj_jac), reading contacts (data.contact, mj_contactForce), sleeping islands and coordinate frames. Use when stepping, resetting, saving/restoring state, reading contact forces, computing Jacobians or diagnosing simulation warnings.'
---

# Simulation Loop (C API)

Use this skill to load, step, control, save/restore and parallelize MuJoCo
simulations from C, change mjModel at runtime, handle errors and logs, and
read diagnostics, Jacobians, contacts, sleep state and frames. Build setup and
naming conventions are in [c-programming](../SKILL.md).

## Initialize and clean up

Never allocate mjModel or mjData yourself. All heap memory is allocated up
front, so no malloc/free happens during simulation. The variable-size arena
is set by the `memory` attribute of the MJCF `size` element; if it is
exceeded, an error is generated (it does not grow).

``` C
// option 1: parse and compile XML from file
mjModel* m = mj_loadXML("mymodel.xml", NULL, errstr, errstr_sz);
// option 2: parse and compile XML from virtual file system
mjModel* m = mj_loadXML("mymodel.xml", vfs, errstr, errstr_sz);
// option 3: load precompiled model from MJB file
mjModel* m = mj_loadModel("mymodel.mjb", NULL);
// option 4: load precompiled model from virtual file system
mjModel* m = mj_loadModel("mymodel.mjb", vfs);
// option 5: deep copy from existing mjModel
mjModel* m = mj_copyModel(NULL, mexisting);
// option 6: compile model from mjSpec
mjModel* m = mj_compile(spec, vfs);
```

All return NULL on error or warning; `mj_loadXML` writes the message into
`errstr`, the others call `mju_error` / `mju_warning`. The VFS is searched
before the disk.

``` C
// option 1: create mjData corresponding to given mjModel
mjData* d = mj_makeData(m);
// option 2: deep copy from existing mjData
mjData* d = mj_copyData(NULL, m, dexisting);
// ... simulate ...
mj_deleteModel(m);
mj_deleteData(d);
```

mjData belongs to one mjModel; passing an incompatible or NULL pair is
undefined behaviour (arguments are barely checked).

## Step the simulation

``` C
// simulate until t = 10 seconds
while (d->time < 10)
  mj_step(m, d);
```

That alone gives passive dynamics. Three ways to control:

1. **Control callback** (default way; required for RK4):

``` C
// simple controller applying damping to each DOF
void mycontroller(const mjModel* m, mjData* d) {
  if (m->nu == m->nv)
    mju_scl(d->ctrl, d->qvel, -0.1, m->nv);
}
// install control callback
mjcb_control = mycontroller;
```

   Check model dimensions in the callback; it may be used with several
   models. `mj_step` calls it as late as possible, after everything that
   depends on state but not on control.

2. **Set inputs before `mj_step`**: write `d->ctrl`, `d->qfrc_applied` or
   `d->xfrc_applied`, then call `mj_step`. Intermediate results available to
   your controller are then one step outdated.

3. **Split the step** (fresh intermediate results, no callback):

``` C
while (d->time < 10) {
  mj_step1(m, d);
  // set d->ctrl or d->qfrc_applied or d->xfrc_applied
  mj_step2(m, d);
}
```

   Works only with the single-step integrators (Euler, implicit,
   implicitfast). `mj_step2` always uses a single-step integrator; if RK4 is
   selected it falls back to Euler.

`mj_step` = `mj_checkPos`, `mj_checkVel`, `mj_forward`, `mj_checkAcc`, then
the integrator (`mj_Euler`, `mj_RungeKutta`, `mj_implicit`). The checks
reset the simulation automatically if values become invalid or too large.
`mj_step1` is the position/velocity stages plus `mjcb_control`; `mj_step2`
is actuation, acceleration, constraints, acceleration sensors and the
integration.

## State and control

The continuous-time dynamics `dx/dt = f(t, x, u)` correspond to
`mj_forward`. State components are bits of the `mjtState` enum:

| Group | Fields | Notes |
|----|----|----|
| Physics (`mjSTATE_PHYSICS`) | `qpos`, `qvel`, `act`, `history`, `plastic` | Time-integrated. `qpos` has size `nq`, `qvel` size `nv` (differ with quaternion joints). `history` holds samples when actuators/sensors have `nsample` > 0. `plastic` holds plastic reference state (`springyield`, flex `yield`, elastic rods). |
| Full physics (`mjSTATE_FULLPHYSICS`) | physics + `time`, `plugin_state` | Everything that advances in time. |
| User inputs (`mjSTATE_USER`) | `ctrl`, `qfrc_applied`, `xfrc_applied`, `mocap_pos`, `mocap_quat`, `eq_active`, `userdata` | Never touched by the simulator, so persistent. All default to 0 except mocap poses. |
| Warmstart | `qacc_warmstart` | Previous accelerations used to warmstart the solver. |
| Integration (`mjSTATE_INTEGRATION`) | union of all of the above | Entire input to forward dynamics. Same integration state gives identical outputs. |

- `ctrl` drives actuators (directly or via `act`); `qfrc_applied` are
  generalized forces; `xfrc_applied` are Cartesian wrenches at body CoMs (used
  by the viewer for perturbations). `eq_active` toggles equality constraints
  (initially `eq_active0`); `userdata` size is set by `nuserdata`.
- Warmstarts matter with slow solvers (PGS), capped iterations/tolerance, and
  for exact reproducibility when loading a non-initial state.
- `mjSTATE_INTEGRATION` is maximalist; omit unused fields (`xfrc_applied` is
  `nbody x 6`). Recomputing from it is often much faster than `mj_copyData`.

### Save, copy and restore state

Combine `mjtState` bits with OR. Copy the integration state between two
mjData:

``` C
mj_copyState(model, src, dst, mjSTATE_INTEGRATION);
```

Stepping `src` or `dst` then gives identical results. With a flat array:

``` C
int sig = mjSTATE_TIME | mjSTATE_QPOS | mjSTATE_CTRL;
int size = mj_stateSize(model, sig);
mjtNum* state = mju_malloc(size * sizeof(mjtNum));
mj_getState(model, src, state, sig);  // copy time, qpos and ctrl from src into state
mj_setState(model, dst, state, sig);  // copy time, qpos and ctrl from state into dst
```

`mj_extractState` also takes these bitfields. `mj_resetData` sets `qpos` to
`mjModel.qpos0`, mocap poses to the fixed body poses, and all other state and
control to 0 (more work if trees are initialized asleep).

## Forward dynamics and skipping stages

`mj_forward` computes `qacc` and `act_dot`, plus all intermediates (contacts,
inertia and its LTDL factorization, constraint forces, sensors). It calls
`mj_forwardSkip(m, d, mjSTAGE_NONE, 0)`; the signature is
`void mj_forwardSkip(const mjModel* m, mjData* d, int skipstage, int skipsensor)`.
It runs the position stage if `skipstage < mjSTAGE_POS`, the velocity stage
if `skipstage < mjSTAGE_VEL`, then control, actuation, acceleration and
constraints (sensors unless `skipsensor`).

| `skipstage` | Skips |
|----|----|
| `mjSTAGE_NONE` | Nothing. |
| `mjSTAGE_POS` | Position-only work: forward kinematics, collision, inertia and factorization (the most expensive part). |
| `mjSTAGE_VEL` | Position and velocity work: Coriolis/centrifugal, passive damping, constraint reference accelerations. |

Skipping assumes those sections are already computed. Use it when sampling
where only position, velocity or control differs (e.g. finite differences):
about a 2x speedup. Not usable in a regular simulation.

## Inverse dynamics

Inputs: `qpos`, `qvel`, `qacc`, `mocap_pos`, `mocap_quat` (no `act`, no
`time`, assuming no callbacks using user state). Main output:
`mjData.qfrc_inverse`, the force needed to produce `qacc`. With full solver
convergence:

    mjData.qfrc_inverse = mjData.qfrc_applied + Jacobian'*mjData.xfrc_applied + mjData.qfrc_actuator

- `mj_inverse` calls `mj_inverseSkip` with `(mjSTAGE_NONE, 0)`; skipping
  works as in forward dynamics.
- With the `fwdinv` flag in `mjModel.opt.enableflags`, `mjData.solver_fwdinv`
  gets the L2 norms of the forward/inverse mismatch (joint forces and
  constraint forces).

## Multi-threading

- Within a step: initialize a thread pool with `mju_threadpool`; collision
  detection and constraint solving across islands are distributed.
- Sampling (more common): one mjData per thread, shared read-only mjModel.
  No further synchronization is needed because top-level functions treat
  mjModel as `const`.

``` C
// prepare OpenMP
int nthread = omp_get_num_procs();      // get number of logical cores
omp_set_dynamic(0);                     // disable dynamic scheduling
omp_set_num_threads(nthread);           // number of threads = number of logical cores
// allocate per-thread mjData
mjData* d[64];
for (int n=0; n < nthread; n++)
  d[n] = mj_makeData(m);
// parallel section
#pragma omp parallel
{
  int n = omp_get_thread_num();       // thread-private variable with thread id (0 to nthread-1)
  // ... initialize d[n] from results in serial code
  // thread function
  worker(m, d[n]);                    // shared mjModel (read-only), per-thread mjData (read-write)
}
// delete per-thread mjData
for (int n=0; n < nthread; n++)
  mj_deleteData(d[n]);
```

Tips: one thread per core, distribute work inside `worker`; adjust shared
`mjOption` before the parallel section; copy state and recompute rather than
`mj_copyData`; use skip stages; warm-start from the central sample.

### Batched simulation (`mujoco/mjbatch.h`)

An `mjBatch` holds `nsim` simulations of one model on its own thread pool.
Results are bit-identical to a serial loop at any thread count.

- **State rows:** `mjb_state` is an `nsim x nstate` table (`mjb_nstate`),
  the only input storage; write inputs at `mjb_stateComponent` addresses.
  Warning counters (`mjb_warning`) travel with the row.
- **Calls** (`mjb_step`, ...) run on `ids` or all; a simulation that errors
  keeps its previous state (`mjb_status`, `mjb_error`).
- **Outputs:** `mjb_output` registers a derived field, copied out to an
  `nsim x size` array after every call.
- **Persistent batches** keep one mjData per simulation (default: one per
  thread, so non-state fields are shared); `mjb_getData` copies it; required
  for sleep or IPC models. They can *continue* a step with `mj_step2` when
  only `ctrl`, `qfrc_applied`, `xfrc_applied` changed.
- **Stages:** step/reset take an `mjtStage` run at the new state afterwards:
  `mjSTAGE_VEL` (like `mj_step1`, typical observation) or `mjSTAGE_ACC`.
- **Per-simulation models:** `mjb_expand` a field (options as
  `"opt.<name>"`, no assets), then `mjb_setConst` if derived constants
  change; or `mjb_setModels` with same-layout models. `mjb_getModel`
  extracts one. `mjb_rollout` records open-loop trajectories; `mjb_apply`
  runs any function per simulation.

``` C
const int nsim = 1024;  // number of simulations
const int nstep = 500;  // number of control steps
char error[1000];
mjBatchConfig config;
mjb_defaultConfig(&config);
config.nthread = 8;  // default 0: all logical CPUs, at most nsim
mjBatch* b = mjb_makeBatch(m, nsim, &config, error, sizeof(error));
if (!b) {
  mju_error("could not make batch: %s", error);
}
int nstate = mjb_nstate(b);                                // length of a state row
mjtNum* ctrl = mjb_stateComponent(b, mjSTATE_CTRL, NULL);  // ctrl in row 0; row i is nstate*i further
mjtNum* xpos = mjb_output(b, "xpos", NULL, NULL);          // nsim x 3*nbody, copied after every call
mjb_reset(b, /*ids=*/NULL, 0, /*key=*/NULL, mjSTAGE_ACC);
for (int k=0; k < nstep; k++) {
  for (int i=0; i < nsim; i++) {
    policy(xpos + 3*m->nbody*i, ctrl + nstate*i);
  }
  if (mjb_step(b, /*ids=*/NULL, 0, 1, mjSTAGE_VEL)) {
    // simulations that raised an error kept their previous state; see mjb_status and mjb_error
  }
}
mjb_deleteBatch(b);
```

Batch threads run across simulations; `mju_threadpool` threads run within
one. They are not combined. Global callbacks such as `mjcb_control` run
concurrently on batch threads without knowing which simulation they serve;
put per-simulation work in `mjb_apply`. Python: `mujoco.batch` (see
[python-bindings](../../python-bindings/SKILL.md)).

## Changing mjModel at runtime

Prefer editing the mjSpec and recompiling
([model-editing](../../model-editing/SKILL.md)); modify mjModel directly only
for speed. Rule: real-valued parameters are safe, structural integers are
not. Exceptions:

- Safe integers: `XXX_limited`, `XXX_group`, `XXX_matid`, `XXX_texid`,
  `geom_condim`, `geom_priority`, `geom_castshadow`, `cam_resolution`,
  `light_castshadow`, `light_active`, `flex_contype`, `flex_conaffinity`,
  `flex_condim`, `flex_priority`, `tex_data` (then `mjr_uploadTexture`).
- Unsafe: `XXX_sameframe` (nonzero to zero is safe); `geom_contype`,
  `geom_conaffinity` unless the parent `body_contype`/`body_conaffinity`
  become the bitwise OR over its geoms.

`mj_setConst` (last compile step) propagates changes to derived fields. It
does not redo `dampratio` actuator damping, joint `springdamper`, default
tendon spring lengths, or model statistics. It uses the mjData as workspace
and wakes sleeping trees: call `mj_resetData` or restore the state afterward.
With sleeping enabled, static body poses are computed only by `mj_makeData`
and `mj_resetData`.

| Real field | Status |
|----|----|
| `qpos0`, `qpos_spring`, `body_mass`, `body_inertia`, `body_ipos`, `body_iquat`, `dof_armature`, `geom_margin`, `geom_gap`, `site_pos`, `site_quat`, `eq_data`, `hfield_size` | Safe with `mj_setConst` (diagonal inertias must obey the triangle inequality) |
| `body_pos`, `body_quat` | Safe with `mj_setConst`; unsafe for static bodies (invalidates BVH) |
| `geom_pos`, `geom_quat`, `geom_size` | Safe with `mj_setConst`; geom-inferred masses/inertias do not follow |
| `geom_contype`, `geom_conaffinity` | Safe with `mj_setConst`, but a geom that did not collide at compile time, in a body whose other geoms did, cannot be made to collide |
| `body_gravcomp`, `geom_surfacevel` | Safe; update `flg_gravcomp` / `flg_surfacevel` (directly or via `mj_setConst`) when switching from/to all zero |
| `cam_pos`, `cam_quat`, `light_pos`, `light_dir` | Mostly safe; `mj_setConst` needed with tracking |
| `tendon_stiffness`, `tendon_damping` | Mostly safe; `mj_setConst` when changing from/to zero (affects sleep) |
| `actuator_gainprm`, `actuator_biasprm` | Safe (`dampratio` damping keeps its value) |
| `hfield_data` | Safe; range [0, 1]; call `mjr_uploadHField` |
| `mesh_scale`, `mesh_pos`, `mesh_quat` | No effect (`mesh_pos`/`mesh_quat` affect SDF sensors) |
| `mesh_vert`, `mesh_normal`, `mesh_face`, `mesh_polynormal` | Unsafe for colliding meshes; visual ones need `mjr_uploadMesh` |
| `bvh_aabb`, `oct_aabb`, `oct_coeff` | Unsafe |

To save changes: `mj_saveLastXML` and `mj_copyBack` copy changed real-valued
parameters back to the spec (not all changes). Only `mj_saveModel` (MJB)
guarantees everything is kept.

## Data layout

- Matrices are **row-major**; all `mju_` matrix functions assume it.
- `qM` (custom tree format) and `qLD` (CSR) are always sparse: use
  `mj_factorM`, `mj_solveM`, `mj_solveM2`, `mj_mulM`; `mj_fullM` makes dense.
- `efc_J` is CSR when sparse Jacobians are on (`mj_isSparse`; then `efc_JT`
  exists and `efc_AR` is sparse). Element `A[A_rowadr[r]+k]` is at column
  `A_colind[A_rowadr[r]+k]`, `k < A_rownnz[r]`; storage may be
  "uncompressed" (`A_rowadr[r] = r*n`).
- Quaternions are `(w, x, y, z)`; null rotation is `(1, 0, 0, 0)`.
- Fields prefixed `c` (`cvel`, `cacc`, `cdof`) are 6D spatial vectors,
  rotation first then translation.
- Arrays are byte-aligned inside one buffer; never assume adjacent fields are
  contiguous:

``` C
// do this
mju_copy(myqpos, d->qpos, m->nq);
mju_copy(myqvel, d->qvel, m->nv);
// DO NOT do this, there may be padding at the end of d->qpos
mju_copy(myqposqvel, d->qpos, m->nq + m->nv);
```

## Internal stack

`mjData.arena` holds constraint memory and a stack for temporaries. MuJoCo
functions leave `mjData.pstack` unchanged on return, except `mj_resetData`
and variants, which set it to 0. `mj_step`, `mj_step1` and `mj_step2` call
it on instability, so use the stack only between calls that may reset.

``` C
// mark an mjData stack frame
mj_markStack(d);
// allocate space
mjtNum* myqpos = mj_stackAllocNum(d, m->nq);
mjtNum* myqvel = mj_stackAllocNum(d, m->nv);
// restore the mjData stack frame
mj_freeStack(d);
```

`mj_stackAllocNum` errors when out of space. Also `mj_stackAllocInt` and
`mj_stackAllocByte` (arbitrary size and alignment).

## Errors, warnings, logging

All output goes through one `mjfLogHandler` receiving an `mjLogMessage`
(level, `subject` text, optional `func`, `file`, `line`).

``` C
void my_handler(const mjLogMessage* msg) {
  printf("%s\n", msg->subject);
}
mjfLogHandler prev = mju_setLogHandler(my_handler);
// ... do work ...
mju_setLogHandler(prev);
```

- `mju_setLogHandler` returns the previous handler (never NULL); passing
  NULL restores the default. Chain to it to observe; do not chain when
  recovering.
- `mjLOG_ERROR` is always fatal. A handler must not return from it: `longjmp`
  or otherwise transfer control (as the compiler and Python bindings do).
  Returning is undefined behaviour.
- Never call `mju_error` inside a handler (infinite recursion).
- Default handler: calls legacy `mju_user_error`/`mju_user_warning` if
  installed (deprecated; a custom handler takes precedence); else writes to
  `MUJOCO_LOG.TXT` and the console (stderr for errors/warnings, stdout for
  info); errors `exit(EXIT_FAILURE)`. Configure it with `mju_setLogConfig` / `mju_getLogConfig` (console, log file path or
  empty string to disable, info topics).
- Model load failure is recoverable: `mj_loadXML` and `mj_loadModel` return
  NULL (internally via a thread-local handler that throws a C++ exception).
- Heap allocation goes through `mju_malloc`/`mju_free`, which call
  `mju_user_malloc`/`mju_user_free` if installed.

Info (`mjLOG_INFO`, filtered in the default handler; custom handlers get all)
and debug (`mjLOG_DEBUG`, filtered at the producer; only enabled topics are
sent) use `mjtLogTopic`. Topics are 1-indexed; topic 0 (`mjTOPIC_NONE`)
always passes.

``` C
mjLogConfig config = mju_getLogConfig();
config.topics |= (1 << (mjTOPIC_SLEEP - 1));
mju_setLogConfig(config);
```

Or set `MUJOCO_LOG_TOPICS=sleep,time_stp` (names without `mjTOPIC_`,
lowercase), read once at startup.

## Diagnostics

- **Warnings:** `mjData.warning` has one `mjWarningStat` per `mjtWarning`
  (count since reset, usually the element index). The first occurrence is
  printed via `mju_warning`. `mj_warning` raises one.
- **Timers:** `mjData.timer` has one `mjTimerStat` per `mjtTimer`. All zero
  unless you install `mjcb_time`.

``` C
mjtNum avtm = d->timer[mjTIMER_STEP].duration / mjMAX(1, d->timer[mjTIMER_STEP].number);
```

- **Solver:** `mjData.solver_niter` iterations of the last call (can be 0 if
  the warmstart is already converged, then no stats are written);
  `mjData.solver` has one `mjSolverStat` per iteration.
- **fwdinv:** with the `fwdinv` enable flag, the forward/inverse mismatch is
  populated; discrepancies mean poor forward-solver convergence.
- **Memory:** `mjData.maxuse_arena` is the peak arena use since reset. Set a
  large `memory`, monitor it, then reduce. Out-of-memory triggers an error.
- **Energy:** with the energy flag, `mjData.energy` holds kinetic and
  potential energy; growing energy suggests instability. For
  energy-conserving systems, RK4 tracks energy much better than Euler.

## Jacobians

Jacobians are `N x nv` (not `nq`). Automatic ones: `ten_moment`,
`actuator_moment`, `efc_J`. `mj_jac` takes a 3D point and a body and
computes translational and rotational Jacobians (map joint velocities to
point velocities; the transpose maps forces to joint forces). `mj_jacXXX`
variants use other points (body CoM, geom center, ...). It is essentially
free; use it freely. Exact signatures are in
[api-functions](../../reference/api-functions/SKILL.md).

## Contacts

`mjData.contact` holds `mjContact` entries from the position stage, sorted
so contacts of one body pair are contiguous (first body major index).
Included contacts have `exclude == 0` and `efc_address` into the constraint
list (exclusion comes e.g. from geom `gap`).

``` C
mjtNum* contactforce = d->efc_force + d->contact[i].efc_address;
```

- Pyramidal cones (`mj_isPyramidal`) give forces along redundant pyramid
  edges. Use `mj_contactForce` to get a 3D force followed by a 3D torque
  (torque zero for `condim` 1 or 3) in the contact frame.
- `mjContact.frame` is **transposed**: axes along rows. Normal (X) is
  `frame[0-2]`, Y `frame[3-5]`, Z `frame[6-8]`.
- Custom near-phase collisions: set entries of `mjCOLLISIONFUNC` (upper-left
  triangle, type `mjfCollision`), build an `mjContact` per contact and call
  `mj_addContact`.

## Sleeping islands

- `mjData.tree_asleep`: negative = awake, non-negative = asleep. Trees count
  from `-(1 + mjMINAWAKE)` up to -1 ("ready") while below
  `sleep_tolerance`; an island sleeps when all its trees are ready.
- Velocities are scaled by `mjModel.dof_length` before the infinity norm, so
  `sleep_tolerance` is in length/time. Sleeping zeroes velocities.
- Policy is "allowed" or "never" from the compiler, overridable with
  `body/sleep`; "init" puts trees to sleep at mjData initialization (default
  configuration only, not keyframes; all trees of an island must be marked).
  Trees with actuators do not sleep by default.
- Waking happens in the position stage when: `qpos` is changed; `qvel`,
  `qfrc_applied` or `xfrc_applied` are set nonzero (bytewise check, `-0.0`
  wakes); contact with an awake tree or mocap body; connection by active
  equality or limited tendon to an awake tree; equality to a sleeping tree
  in another island.
- Enable sleep (`m->opt.enableflags |= mjENABLE_SLEEP`) either before
  `mj_makeData` or after at least one `mj_step`. Enabling it between
  `mj_makeData` and the first step is undefined behaviour (static elements
  are not computed).

- Fully saving state with sleeping islands requires copying all of mjData;
  standard state tools still work but wake the islands.
- Not supported with sleep: RK4, `mjd_transitionFD`, `mjd_inverseFD`.

## Coordinate frames

- Joint space: `qpos` (`nq`) vs `qvel`/`qacc` (`nv`). Use
  `mj_differentiatePos` (positions to velocity) and `mj_integratePos`.
- Local coordinates: all spatial quantities in mjModel (`body_pos`,
  `body_quat`, ...). Global: mjData fields starting with `x` (`xpos`,
  `geom_xpos`, `xmat`; bodies also `xquat`). `mj_local2Global` converts.
- Poses (position + quaternion): `mju_mulPose`, `mju_negPose`,
  `mju_trnVecPose`; quaternions: `mju_mulQuat`, `mju_negQuat`,
  `mju_rotVecQuat`.
- Com-based `c` quantities: do not use directly. Use `mj_objectVelocity`,
  `mj_objectAcceleration` and `mju_transformSpatial`; `mj_objectVelocity`
  returns a body-centered, world-aligned 6D vector.

## Source docs

Verbatim copies, for details not covered above:

- [programming/simulation.md](references/programming-simulation.md)
