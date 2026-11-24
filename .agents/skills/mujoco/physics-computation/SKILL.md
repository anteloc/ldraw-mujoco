---
name: physics-computation
description: 'How MuJoCo computes physics: soft contact model, generalized coordinates, the constraint model (equality, friction loss, limits, contacts), constraint solvers (Newton, CG, PGS) and their parameters, collision detection (broadphase, convex/multiccd, margins), sleeping islands, the simulation pipeline and derivatives. Use when reasoning about solver choice, constraint softness (solref, solimp), contact penetration or creep, friction, or why a simulation behaves as it does.'
---

# MuJoCo Physics Computation

Use this skill to reason about how MuJoCo turns a model and state into
motion: dynamics, soft constraints, solvers, collision, sleeping, pipeline and
derivatives. Use it to choose a solver or integrator, tune `solref`/`solimp`,
or explain penetration, creep, slip or instability. Core concepts are in the
[root skill](../SKILL.md).

Background paper: [Analytically-invertible dynamics with contacts and constraints: Theory and implementation in MuJoCo](https://scholar.google.com/scholar?cluster=9217655838195954277), E. Todorov (2014).

## Mental model

- Dynamics are defined in **continuous time**, in terms of forces and
  accelerations. Forward dynamics are then integrated over
  `mjModel.opt.timestep` (the opt-in `discrete` integrator is the exception).
- Contacts are **soft** and the model is **convex** (no strict LCP
  complementarity): normal force and velocity can both be positive and slip
  needs some normal motion. The effects are small and realistic for soft
  materials.
- Constraint forces are the unique solution of a convex problem; inverse
  dynamics are analytic. The hard limit `R -> 0` is not allowed.

## Notation and mjData fields

| Symbol | Size | Meaning | Field |
|----|----|----|----|
| nq | | position coordinates | `mjModel.nq` |
| nv | | degrees of freedom | `mjModel.nv` |
| nc | | active constraints | `mjData.nefc` |
| q | nq | joint position | `mjData.qpos` |
| v | nv | joint velocity | `mjData.qvel` |
| τ | nv | applied force | `qfrc_passive + qfrc_actuator + qfrc_applied` |
| c(q,v) | nv | bias: Coriolis, centrifugal, gravity | `mjData.qfrc_bias` |
| M(q) | nv×nv | joint-space inertia | `mjData.qM` |
| J(q) | nc×nv | constraint Jacobian | `mjData.efc_J` |
| r(q) | nc | constraint residual | `mjData.efc_pos` |
| f | nc | constraint force | `mjData.efc_force` |

Equations of motion: `M v̇ + c = τ + Jᵀ f`. Once `f` is known, forward
`v̇ = M⁻¹ (τ + Jᵀ f − c)` and inverse `τ = M v̇ + c − Jᵀ f`.

- `nq > nv` whenever quaternions are used (ball/free joints). Use
  *mj_differentiatePos* to "subtract" two `nq` positions into an `nv` velocity.
- `c` is computed by RNE with zero acceleration; `M` by CRB, stored sparse,
  with a sparsity-preserving `LᵀDL` factorization for `M⁻¹x` solves.
- `nc`-sized vectors change at runtime: fixed enumeration order, inactive
  constraints omitted. Prefix `efc` marks constraint data in `mjData`.

## Forces entering τ

**Actuators** (`mjData.ctrl` in, `mjData.actuator_force` out, activations
`mjData.act`, total in `mjData.qfrc_actuator`; counts `nactuator`, `nu`,
`nout`). Transmissions: `joint`, `tendon`, `jointinparent`, `slider-crank`,
`site` (optional `refsite`), `body`. Activation types: `integrator`,
`filter`, `filterexact`, `muscle`, `user` (`mjcb_act_dyn`), `none`. SISO
force `p = (a w or a u) + b0 + b1 l + b2 l̇` (`actuator_gainprm`,
`actuator_biasprm`). Euler filters diverge for `t < h`; `filterexact` is
stable for any positive `t`. Shortcuts and muscles:
[MJCF modeling](../mjcf-modeling/SKILL.md).

**Passive forces** (`mjData.qfrc_passive`, position/velocity only):
joint/tendon spring-dampers, body `gravcomp`, [fluid forces](fluid-forces/SKILL.md),
custom `mjcb_passive`. User forces: `qfrc_applied`, `xfrc_applied`.
Polynomial stiffness `f(x) = a x + b x² + c x³ + …` and damping
`f(v) = a v + b v|v| + c v³ + …` apply force `−f`; the compiler does not check
sign-preservation `z·f(z) ≥ 0` (order ≤ 3: `a ≥ 0, c ≥ 0`, `b² ≤ 4ac`, for
damping only when `b < 0`). `stiffness="a b c"` maps to `jnt_stiffness[i] = a`,
`jnt_stiffnesspoly[i*mjNPOLY] = b`, `jnt_stiffnesspoly[i*mjNPOLY + 1] = c`.

## Integrators and timestep

| Integrator | D matrix / behaviour | Use when |
|----|----|----|
| `Euler` | semi-implicit; implicit joint damping only (`qH`); falls back to plain semi-implicit if no damping or `eulerdamp` disabled | compatibility with older models |
| `implicitfast` | all force derivatives except RNE Coriolis/centripetal, symmetrized, Cholesky; gyroscopic terms reinstated for standalone free bodies | **recommended default** for most models |
| `implicit` | all derivatives except constraint forces, same sparsity as `M`, LU (`qLU`) | coupled rotating systems (multi-link pendula) |
| `discrete` | constraint solve and implicit update in one step, metric `M̂ = M + hD + h²K`; implicit in position | stiff springs, position servos or strong damping interacting with contacts |
| `RK4` | fixed-step 4th-order Runge-Kutta | energy-conserving systems |

- The timestep is "perhaps the single most important parameter". Too large is
  unstable; too small wastes CPU. The good range is model-dependent.
- `discrete`: `mjData.qacc` holds `(v⁺ − v)/h`, not continuous acceleration,
  so it depends on the timestep. Constraint rows are stable for any `solref`;
  the `refsafe` flag replaces rows with `timeconst × dampratio < h` by the
  stiffest zero-restitution spring for the timestep. Status: new (September
  2026), under development. Unsupported (runtime error): flex elasticity or
  passive flex contact with `PGS` or noslip; flex edge stiffness/damping;
  sleep without islands. Under `PGS`, tendon and actuator terms integrate
  explicitly.
- `mj_step1`/`mj_step2` do not support `RK4`.

## Constraint model

Active constraints are ordered by type: **equality, friction loss, limit,
contact**. Limits are treated as frictionless contacts by the solver.

**Equality** (`r(q) = 0`, contributes `dim(r)` rows):

| Type | Dim | Notes |
|----|----|----|
| `connect` | 3 | ball joint outside the tree; two give a hinge |
| `weld` | 6 | relative pose from `qpos0` by default; orientation residual `sin(θ/2)(x,y,z)` weakens near 180° |
| `joint` | 1 | hinge/slide only; lock or couple via quartic polynomial |
| `tendon` | 1 | same as joint, on tendon length |

Prefer the kinematic tree over loop joints made of equalities (slower, less
accurate); use equalities for soft joints. For a child body, drop its joints instead of welding.

**Friction loss** (dry friction, `frictionloss` on joints and tendons): an
upper bound on the friction force, not a velocity-dependent force; no position
residual. Joint rows: 1, 3 (ball) or 6 (free; one parameter for linear and
angular).

**Limits** (joints and tendons with `limited` and `range`): unilateral; active
when the distance falls below `margin`. Ball limits apply to the rotation
angle using the second `range` value (first must be 0). Avoid narrow ranges as
a substitute for equality constraints; use a soft equality instead.

**Contacts**: point contact with frame whose **x axis is the normal**. Distance
is positive when separated, negative when penetrating.

| Parameter | Meaning |
|----|----|
| `condim` | 1 frictionless, 3 tangential friction, 4 + torsional, 6 + rolling (2 and 5 not allowed) |
| `friction` | `condim−1` coefficients; torsional and rolling have units of length |
| `margin` | forces generated when distance < `margin` |
| `gap` | extra detection band: contacts in `(margin, margin+gap]` are inactive (`efc_address = -1`) |
| `solref`, `solimp` | solver parameters (below) |

Geom `margin` and `gap` are summed for a pair. Negative margin is allowed if
`margin + gap >= 0`. Rows per contact: elliptic `condim`, pyramidal
`2(condim−1)`. Contact force acts from the first geom toward the second.

## Constraint solver

- Primal: generalized Gauss principle over accelerations with a diagonal
  regularizer `R > 0` (softness) and reference acceleration `aref`
  (spring-damper stabilization, similar in spirit to Baumgarte). Friction loss
  uses a Huber norm, giving box constraints in the dual.
- Reduced primal: `v̇ = argmin_x ‖x − M⁻¹(τ − c)‖²_M + s(J x − aref)`, `s`
  convex and C¹; `f = −∇s`. Newton and CG solve this.
- Dual: `f = argmin_λ ½ λᵀ(A + R)λ + λᵀ(au − aref)`, `λ ∈ Ω`, `A = J M⁻¹ Jᵀ`.
  PGS solves this.
- Inverse dynamics drop `A` (only `R` remains): diagonal and analytic. With
  the `fwdinv` enable flag the forward/inverse mismatch goes to
  `mjData.solver_fwdinv`; discrepancies mean poor solver convergence.

| Solver | Formulation | Notes |
|----|----|----|
| `Newton` | reduced primal | **default**; exact Newton, Cholesky of `H = M̂ + JᵀDJ`, incremental rank-1 updates; stops when cost improvement, gradient norm or Newton decrement < `tolerance` |
| `CG` | reduced primal | nonlinear CG (Hager-Zhang), exact line search, no setup cost, matrix-free |
| `PGS` | dual | one scalar (or one contact for elliptic) at a time; first-order but fast early progress |
| NoSlip | post-pass | enabled by `noslip_iterations > 0`; re-solves friction rows with `R = 0` to suppress slip; ad hoc, can cause instabilities with complex multi-contact |

All solvers support pyramidal and elliptic cones, dense or sparse. The two
cone types give different (usually very close) soft-contact dynamics;
elliptic is more principled.

**Warmstart.** Forces from the previous step are compared with zero forces
(`qacc_smooth`); the cheaper is used. CG and Newton check a convergence
certificate first and may return with zero iterations in quiescent scenes.

**Constraint islands.** Trees linked by constraints form islands that are
solved independently (and can be multi-threaded); unconstrained DOFs are
untouched. `mjData.nidof` can be smaller than `mjModel.nv`.

### Solver parameters (softness)

Per constraint: impedance `0 < d < 1`, damping `b > 0`, stiffness `k ≥ 0`,
computed from `solimp` and `solref` (details and automation such as critical
damping in [MJCF modeling](../mjcf-modeling/SKILL.md)).

- `R_ii = (1 − d_i)/d_i · Â_ii`, with `Â` a diagonal approximation of `A`
  from end-effector inertias at `qpos0`.
- `aref_i = −b_i (J v)_i − k_i r_i`. Friction loss and elliptic friction rows
  have `r ≡ 0`, so pure damping.
- Approximately: `ac_i = d_i aref_i + (1 − d_i) au_i`; `d → 1` is hard,
  `d → 0` is no constraint.
- Each scalar constraint behaves roughly like a damped second-order system:
  `solref` sets time constant and damping ratio, `solimp` sets strength. When
  critically damped, steady-state penetration under constant load is
  independent of the effective mass.
- `diagexact` flag: use the exact diagonal `A_ii` at the current configuration.
  Use it when inertias are very anisotropic or chains run far from `qpos0`:
  there the approximation can drive `R` near zero, making constraints
  infinitely hard and causing divergence. Cheap with PGS/NoSlip.
- Surface velocity (`mjContact.surfacevel`) biases tangential/torsional rows,
  e.g. conveyor belts; reported in `mjData.efc_vel`.
- Adhesion `δ` shifts the friction cone down the normal: a constant
  attraction is accumulated in `mjData.qfrc_adhesion` and `aref → aref + R δ`.
  Resting penetration is unaffected.

## Collision detection

Output: active contacts in `mjData.contact` (distance < margin, or predicted
within the step when speculative contacts are on).

**Selection.** Candidates come from body pairs (sweep-and-prune along the
principal axis of geom centres, then per-body AABB BVH) plus explicit `pair`
elements; `exclude` removes body pairs. Filters:

1. A collision function must exist for the geom types (plane-plane is not
   supported).
2. Bounding-sphere test including margin (and motion when `speculative`).
3. Body-pair only: not the same body (cannot be disabled), not parent-child
   unless the parent is the world (can be disabled). Bodies welded without
   joints count as one body. Pairs where neither body can move are skipped.
4. Body-pair only: `(contype1 & conaffinity2) || (contype2 & conaffinity1)`.
   Default `contype = conaffinity = 1`.

Filters 3 and 4 are bypassed by explicit `pair` elements.

**Convexity.** Collision is limited to convex geoms (except SDF plugins and
height fields, which are triangular prisms). Meshes collide as their **convex
hulls** (qhull; press 'H' in simulate to see them). Decompose non-convex
objects into convex geoms on one body (tools:
[CoACD](https://github.com/SarahWeiii/CoACD), [mjfit](https://github.com/younghyopark/mjfit)).

**CCD pipelines** (pairs without analytic colliders, e.g. meshes): native
GJK/EPA (default, faster and more robust) or legacy libccd MPR (disable the
`nativeccd` flag). Both use `mjOption.ccd_tolerance` and
`mjOption.ccd_iterations`. Legacy gives wrong *mj_geomDistance* values except
at small distances.

**Multiple contacts (`multiccd` flag).** General CCD returns one point, which
is problematic for surface contact such as box stacking. With nativeccd,
multiccd is single-shot with little overhead and supports capsules, cylinders,
boxes and meshes. With legacy CCD it re-runs with ±1e-3 rad rotations (up to 4
extra points, about 5× cost). Max contacts for a pair: *mj_maxContact*.
Examples: box-plane 4, box-box 8, mesh-mesh 1 (4 with native multiccd, 5
legacy), mesh-plane 4.

**Speculative contacts** (`speculative` flag): see [speculative contacts](speculative-contacts/SKILL.md).

## Sleeping islands

Off by default; enable with the `sleep` flag. A kinematic tree is the smallest
unit; connected trees sleep together. Sleeping islands act like static bodies
for collision, so contacts inside them and with static bodies are skipped
(the main speedup). Contacts with awake trees wake them, in the position
stage. Automatic sleep: a tree below the velocity `tolerance` for
`mjMINAWAKE` steps is ready; an island sleeps when all its trees are ready.
`body/sleep="init"` on a tree root starts it asleep in any configuration.
Details in [simulation loop](../c-programming/simulation-loop/SKILL.md).

## Simulation pipeline

*mj_step* runs stages 1-26; *mj_forward* 2-23 (ends with `mjData.qacc`);
*mj_step1* 1-19 and *mj_step2* 20-26; *mj_fwdPosition* 2-11.

| Stages | Functions |
|----|----|
| 1 check | *mj_checkPos*, *mj_checkVel* (reset on divergence) |
| 2-12 position | *mj_kinematics*, *mj_camLight*, *mj_comPos*, *mj_flex*, *mj_tendon*, *mj_makeM*, *mj_factorM*, *mj_collision* (8), *mj_makeConstraint* + islands, *mj_transmission*, *mj_projectConstraint*, *mj_sensorPos*, *mj_energyPos* |
| 13-18 velocity | *mj_fwdVelocity*, *mj_comVel*, *mj_passive*, *mj_sensorVel*, *mj_referenceConstraint*, *mj_rne* |
| 19 control | `mjcb_control` |
| 20-25 force/accel | *mj_fwdActuation*, *mj_fwdAcceleration*, *mj_fwdConstraint* (22, gives `qacc`), *mj_sensorAcc*, *mj_checkAcc*, *mj_compareFwdInv* (optional) |
| 26 advance | *mj_Euler*, *mj_RungeKutta* or *mj_implicit* |

Use `mjModel.opt.disableflags` / `enableflags` to skip or add stages. With
sleeping enabled, velocities are read during island construction, so do not
modify `qvel` between position and velocity stages; modify it before
*mj_fwdPosition* or use *mj_forwardSkip*.

**Consistency.** Nothing updates automatically: after setting `qpos`, call
*mj_kinematics* (or the needed stages); after *mj_step*, `mjData` quantities
refer to the *previous* state. **Reproducibility:** deterministic within one
version on one architecture; save the full integration state (including
warmstart) with *mj_getState* / *mj_setState* (`mjtState` flags).

**Inverse dynamics** (*mj_inverse*): computes the constraint force
analytically and outputs `mjData.qfrc_inverse`. With `invdiscrete` (and not
`RK4`) input accelerations are converted from discrete to continuous time.

## Derivatives

- Analytic velocity derivatives of smooth dynamics power the implicit integrators.
- The docs state that the default solver impedance makes contacts *not*
  differentiable and that it "needs to be set to 0" for smooth contact-force
  onset; see solver parameters in [MJCF modeling](../mjcf-modeling/SKILL.md).
- Finite-difference Jacobians: *mjd_transitionFD* (state and control
  transition of *mj_step*) and *mjd_inverseFD* (inverse dynamics). Forward and
  centred differences; warmstarts, quaternions and control clamping handled.
  Signatures are in [API functions](../reference/api-functions/SKILL.md).

## Troubleshooting map

| Symptom | Look at |
|----|----|
| Diverges / unstable | smaller `timestep`; `implicitfast` or `implicit`; `diagexact` for anisotropic or far-from-`qpos0` chains |
| Penetration or sinking | `solref` / `solimp` softness (impedance `d`, time constant) |
| Slow slip or creep under friction | slip is inherent to soft constraints; NoSlip (`noslip_iterations`); elliptic cones for fine grasping; `condim` 4 for grasp stability |
| Box/mesh resting on one point, rocking | `multiccd` |
| Objects pass through each other | [speculative contacts](speculative-contacts/SKILL.md), smaller timestep |
| Mesh collides as if filled | convex hull rule; decompose into convex parts |
| Unwanted self-collision | parent-child filter, `contype`/`conaffinity`, `exclude` |
| Solver not converging | `fwdinv` + `mjData.solver_fwdinv`; `tolerance`; solver choice |
| Large passive scenes slow | `sleep` flag, islands |
| Bodies in air or water | [fluid forces](fluid-forces/SKILL.md) |

## Subskills

Read the one that matches your task:

- [fluid-forces](fluid-forces/SKILL.md): MuJoCo fluid dynamics: the inertia-box model and the ellipsoid model for drag, lift and added mass, with the fluidshape/fluidcoef parameters, density and viscosity options. Use when simulating bodies moving through air or water.
- [speculative-contacts](speculative-contacts/SKILL.md): Speculative contacts in MuJoCo: broadphase and sphere filtering, conservative advancement, line-of-sight raycasting and effective contact distance for detecting contacts before penetration. Use when fast-moving or thin objects tunnel through each other, or when tuning contact margins for early detection.

## Source docs

Verbatim copies, for details not covered above:

- [computation/index.md](references/computation-index.md)
