---
name: mjcf-modeling
description: 'Writing MuJoCo models in MJCF: kinematic trees, defaults and classes, joints and degrees of freedom, geoms and meshes, contact pairs and excludes, equality constraints (connect, weld), tendons, actuators, sensors, solref/solimp, margin and friction tuning, inertia from geoms, tips and tricks, model tuning for stability, and the MuJoCo Menagerie model gallery. Use when designing or debugging an MJCF model, choosing contact or solver parameters, or fixing unstable, jittering or penetrating simulations.'
---

# MJCF Modeling

Write and tune MuJoCo models in MJCF, the native XML format. Use this skill to
structure the kinematic tree and defaults, set solver and contact parameters,
configure actuators and sensors, and fix unstable, jittering, slipping or
penetrating simulations. The full element and attribute list is in the
[XML reference](../reference/xml-reference/SKILL.md). To build or edit models
in code with mjSpec, see [model editing](../model-editing/SKILL.md).

MJCF works like a modeling format with a built-in compiler: many quantities
(inertias, length ranges, quaternions) are computed at compile time from what
you write.

## Start here: recommended overrides

Several internal defaults date from early versions and are kept only for
backwards compatibility. Override them once, in `option` and the top-level
`default` class, at the start of a project:

| Setting | Internal default | Recommended initial value | Why? |
|----|----|----|----|
| `integrator` | `"Euler"` | `"implicitfast"` (`"discrete"` for flex elasticity or stiff springs/servos) | Cheap implicit integration of velocity-dependent forces. |
| `cone`, `impratio` | `"pyramidal"`, `"1"` | `"elliptic"`, `"10"` | Isotropic friction cones and stronger tangential resistance to slip. |
| `solref[0]` | `"0.02"` | `"0.004"` --- `"0.01"` | Crisper rigid contacts and tighter equality constraints. |
| `solimp[0]` | `"0.9"` | Keep, or `"0.95"` if needed | Halves rest penetration and creep, at the cost of more solver iterations. |
| `contype`, `conaffinity` | `"1"`, `"1"` | Separate visual / collision classes | Keeps detailed visual meshes out of collision detection. |
| `condim` | `"3"` | `"4"` or `"6"` on grasp pads and rolling props | Adds torsional (and rolling) friction. |
| joint `armature`, `damping` | `"0"`, `"0"` | Nonzero rotor inertia & light damping | Better mass-matrix conditioning and free implicit damping of chatter. |
| `actuator/position` | `kv="0"`, unlimited force | `dampratio="1"` (or `kv`) + `forcerange` | Critically damped servo response and bounded contact impulses. |

Before tuning, load the model paused in [MuJoCo Studio](../studio-viewers/SKILL.md)
(or [simulate](../c-programming/SKILL.md)) and rule out modeling bugs that
look like bad contacts:

- geoms intersecting at `t = 0` (toggle contact points/forces);
- visual/collision geom mismatches (toggle geom groups);
- concave collision meshes replaced by their convex hulls (toggle convex hulls);
- implausible CAD/URDF inertias (toggle equivalent inertia boxes);
- millimeter/meter mismatches (check `mesh/scale` and total mass);
- degree/radian or joint-axis mismatches (`compiler/angle` defaults to `"degree"`);
- position targets driving past joint limits or into surfaces.

Stiffening contacts to mask these issues can cause chatter or divergence.
Measure headless throughput with `testspeed`.

## Kinematic tree

Nest `body` elements under `worldbody`. A child body is literally an XML child
of its parent (unlike URDF links connected by joints).

- A `joint` inside a body creates degrees of freedom between the body and its
  parent. A body with no joints is welded to its parent.
- Put several primitive joints in one body for a composite joint (e.g. two
  slides and one hinge for planar motion). No dummy bodies are needed.
- `joint`, `geom`, `site`, `camera`, `light` defined in a body move with it.
  Elements that refer to several bodies (or none) live in separate sections
  outside the tree.
- Positions and orientations are local: relative to the parent body for
  bodies, relative to the containing body for other elements.
- `compiler/angle` sets degrees or radians in the file; after compilation
  angles are always radians.

### Frame orientation

Use at most one of these attributes. If none is given, the frame is not
rotated.

| Attribute | Type | Meaning |
|----|----|----|
| `quat` | real(4), "1 0 0 0" | Preferred; normalized and copied directly. |
| `axisangle` | real(4) | `(x, y, z, a)`; axis normalized, angle in `compiler/angle` units, right-handed. |
| `euler` | real(3) | Axis sequence from `compiler/eulerseq`, same for the whole model. |
| `xyaxes` | real(6) | X axis, then Y axis (made orthogonal to X); Z = X × Y. |
| `zaxis` | real(3) | Minimal rotation mapping (0,0,1) to this vector. Good for symmetric geoms and lights. |

## Default classes

Defaults work like CSS: set attributes once and let them propagate.

```xml
<mujoco>
  <default class="main">
    <geom rgba="1 0 0 1"/>
    <default class="sub">
      <geom rgba="0 1 0 1"/>
    </default>
  </default>

  <worldbody>
    <geom type="box"/>
    <body childclass="sub">
      <geom type="ellipsoid"/>
      <geom type="sphere" rgba="0 0 1 1"/>
      <geom type="cylinder" class="main"/>
    </body>
  </worldbody>
</mujoco>
```

Results: box red (top-level class), ellipsoid green (`childclass`), sphere
blue (explicit attribute wins), cylinder red (explicit `class` beats
`childclass`). (This example does not compile; it only shows rgba.)

Rules:

- Classes nest; a child class inherits all parent values and may override.
  Each class needs a unique name, except the top-level one ("main" if unnamed).
- Active class: the element's `class` if set; otherwise the nearest ancestor
  body's `childclass`; otherwise the top-level class.
- Some attributes (e.g. body inertia) have an "undefined" state that tells the
  compiler to infer them. You cannot write "undefined" in XML, so once a class
  defines such an attribute, it stays defined in that class and its children.
- Each class has a single actuator default. Shortcut parameters (`kp`, `kv`,
  `area`, ...) are inherited only from a default written with the same
  shortcut, or a `general` default with that shortcut's gain type. A `motor`
  in a class whose default is `position` is a plain motor with the class's
  `ctrlrange`, not a servo. `general` inherits raw gain, bias and dynamics
  parameters of any default.

## Naming and including

- Names are optional, case-sensitive and unique per element type. Name only
  what you reference (e.g. tendon sites), want labeled, or look up with
  `mj_name2id` / `mj_id2name`. Assets must have names, but a name can be taken
  from the file name.
- `<include>` replaces itself with the children of the included file's
  top-level element. Repeated sections (several `worldbody`) are merged.
- Global settings like `compiler/angle` may appear several times; the last one
  wins for the whole composite model. Make included models compatible.
- Duplicate names across included files are compile errors. Including the same
  file twice is a parse error.

## Solver parameters: solref and solimp

Every constraint element accepts `solref` and `solimp`, per element or per
default class. The constraint dynamics are approximately
`a1 + d·(b·v + k·r) = (1 − d)·a0`, with impedance `d`, stiffness `k`, damping
`b`, residual `r`.

**solimp: real(5), "0.9 0.95 0.001 0.5 2"** = (`d0`, `dw`, `width`,
`midpoint`, `power`). Impedance `d` is how strongly the constraint can
generate force. It goes from `d0` at `r = 0` to `dw` at `r = width` along a
sigmoid. `power` >= 1 (1 means linear), `midpoint` in (0, 1). `d` is clamped
to [0.0001, 0.9999]. For smooth, differentiable dynamics use `solimp[0]=0` on
limits and contacts.

**solref: real(2), "0.02 1"**, two formats chosen by sign:

- Positive `(timeconst, dampratio)`: `timeconst` controls softness (larger is
  softer). Keep it at least 2× the timestep; this is enforced unless
  `flag/refsafe` is false. `dampratio` 1 is critical damping. Raising
  `dampratio` at fixed `timeconst` lowers stiffness rather than adding damping.
- Negative `(-stiffness, -damping)`: direct control, e.g. `damping = 0` for
  perfectly elastic bounces. Recommended for system identification.
  `dampratio` 1 equals `damping = 2·sqrt(stiffness)`.

Rest penetration with constant `d` (positive format):
`r = a0·(1 − d)·timeconst²·dampratio²`.

**Friction dimensions** (joint/tendon frictionloss, elliptic cone friction)
have `r ≡ 0`: impedance is always `solimp[0]`, there is no spring, only the
time constant (or direct damping) matters, and `solimp[1]` still scales `b`.
So exact sticking is not guaranteed (see slow slippage below).

Tuning: rigid contacts prefer `solref[0]` of `0.004–0.01`, loop-closure
equalities `0.004–0.005`. Rest penetration and static creep scale with
`1 − d0`. Lower `solref` and switch to elliptic cones before raising `d0`.
Scale `width` to the compliant layer; do not confuse the two attributes
(`solimp="0.01 1 ..."` sets `d0 = 0.01`, nearly disabling the constraint).

## Contact parameters

Explicit `pair` elements set all contact parameters directly; geom values are
then ignored. For dynamically generated contacts, parameters of the two geoms
are combined:

| Parameter | Rule |
|----|----|
| `condim` | Higher `priority` wins; equal priority takes the maximum. |
| `friction` | Higher priority wins; else element-wise maximum. Geoms have 3 coefficients (sliding, torsional, rolling), expanded to 5. Anisotropic friction only via `pair`. |
| `margin`, `gap` | Sum of both geoms; priority ignored. |
| `solref`, `solimp` | Higher priority wins; else weighted average by `solmix`. If either `solref` is non-positive (direct format), element-wise minimum. |

Guidance:

- `condim` "3" is sliding only, "4" adds torsional, "6" adds rolling. Use 4/6
  on fingertips, pads, and curved objects that should settle. `friction[1]`
  and `friction[2]` have units of length. Rolling default is `0.0001`.
- For frictionless contact use `condim="1"`, not near-zero friction (badly
  conditioned under pyramidal cones).
- Equal-priority mixing takes the max friction, so a low-friction object on a
  `friction="1"` floor gets 1. Set `priority="1"` on the geom that should
  govern.
- Leave `margin="0"` unless paired with a matching `gap`; otherwise objects
  hover by `margin - gap`.
- Keep visual meshes out of collision: put them in a default class with
  `contype="0" conaffinity="0"`. Prune other pairs with `contype`/`conaffinity`
  or `exclude`.
- Prefer primitive collision geoms (sphere, capsule, box, cylinder): faster and
  better normals than mesh CCD or `sdf`. Otherwise decimate or convex-decompose
  meshes and cap `maxhullvert`.

**Contact override**: enable `flag/override` and set `option` `o_margin`,
`o_solref`, `o_solimp`, `o_friction` to replace contact parameters globally at
runtime without editing the model. Applies to contacts only. Useful for
sweeping softness in Studio or for continuation methods in optimization.

These docs do not detail `pair`, `exclude`, `equality` (connect, weld) or
`tendon` attributes; look them up in the
[XML reference](../reference/xml-reference/SKILL.md).

## Global options and solver

| Option (default) | Guidance |
|----|----|
| `timestep` ("0.002") | Main speed/fidelity knob. 0.5–2 ms for contact-rich manipulation, 5–15 ms can work for locomotion. With `refsafe`, `solref[0]` is clamped to >= 2·timestep, so larger steps soften contacts. |
| `integrator` ("Euler") | `implicitfast` for most models; `RK4` for near energy-conserving systems; `implicit` for fast-spinning coupled chains; `discrete` required for flex elasticity. |
| `solver` ("Newton"), `iterations` ("100"), `tolerance` ("1e-8") | Newton for most models; tighten tolerance (e.g. 1e-10) cheaply. CG when Hessian factorization dominates (very large or high fill-in scenes). PGS rarely, mainly when `ncon < nv`. |
| `cone` ("pyramidal"), `impratio` ("1") | `elliptic` plus `impratio` 10 for manipulation, 10–100 for legged locomotion. Avoid large `impratio` with pyramidal cones. |
| `noslip_iterations` ("0") | 1–3 strongly suppress drift; ~2× step time, ill-defined inverse dynamics, occasional chatter. |
| `jacobian` ("auto") | Dense up to 60 DOFs, sparse above. Same physics either way. |
| `sleep` ("disable") | Freezes settled trees below `sleep_tolerance`; big speedups for resting clutter. |
| `diagexact` ("disable") | Exact constraint-space inertia diagonal at runtime instead of the `qpos0` approximation. Try when you see `badqacc`, excessive penetration or poor convergence; check with the `fwdinv` flag. |
| `speculative` ("disable") | Adds contacts before impact to prevent tunneling of thin or fast geoms. Not for height fields, SDFs, flexes. New (October 2026); behavior may change. |

**Body ordering**: with sparse Newton, declare moving bodies that contact many
objects (trays, containers, platforms) *before* those objects in `worldbody`.
Declared last, such a hub couples all N bodies into a dense O(N³) block.
Models with `flex` reorder DOFs automatically.

## Joints, masses and inertias

- Add realistic `armature` (reflected rotor inertia `I_rotor·N²`) to geared
  joints: better realism, conditioning and timestep stability.
- Joint `damping` is implicit even under Euler and damps chatter at no solver
  cost. `frictionloss` adds a constraint row; reserve it for real stiction.
- Without `inertial` or geom `mass`, mass and inertia are inferred from geom
  volume at `density` 1000 kg/m³. This misestimates hollow or metal parts.
- When inferring inertia from geoms, use `inertiagrouprange` or `density="0"`
  so visual and collision geoms are not both counted.
- For thin or non-watertight meshes set mesh `inertia="shell"`.
- Avoid mass or inertia ratios > 1000:1. Fix CAD/URDF inertias at the source
  or clamp with `boundmass` and `boundinertia`.

## Actuators

All actuators are internally `general`. Shortcuts (`motor`, `position`,
`velocity`, `intvelocity`, `orientation`, `pid`, `damper`, `cylinder`,
`muscle`, `adhesion`, `dcmotor`) set gain, bias and dynamics parameters for
you. E.g. `position` exposes `kp`, which the parser maps to gain/bias.

**Force limits** (combinable):

| Mechanism | Effect |
|----|----|
| `ctrlrange` | Clamps control input. For motors equals clamping force. |
| `forcerange` | Clamps actuator output force. Use on position actuators. |
| `joint/actuatorfrcrange` | Clamps the sum of all actuator forces on a joint after transmission. Read with the `jointactuatorfrc` sensor. |
| `tendon/actuatorfrcrange` | Same for tendons. |

Prefer one multi-input `pid` or `dcmotor` (with `pos`, `vel`, `ff` inputs,
bounded by `forcerange`) over stacking actuators and clamping their sum.
Joint clamping stays useful when a transmission combines forces across joints.
A saturated `forcerange` adds no implicit damping; give such joints armature
and passive damping. Keep `ctrlrange` within joint `range` (grippers may
extend slightly past pad contact to generate grip force).

**Group disable**: assign actuators to `group`s; `actuatorgroupdisable` picks
groups disabled by default, and `mjOption.disableactuator` switches at
runtime. `nu` and indices do not change; disabled `ctrl` values are ignored.

**Activation limits**: clamp the integrated setpoint of `intvelocity` with
`actrange` (always in radians):

```xml
<actuator>
   <intvelocity name="unclamped" joint="joint1"/>
   <intvelocity name="clamped" joint="joint2" actrange="-1.57 1.57"/>
</actuator>
```

**Muscles**: one line on a tendon gives a reasonable model:

```xml
<actuator>
    <muscle name="mymuscle" tendon="mytendon">
</actuator>
```

Adjust `scale` (overall strength, best in `default`), `force` (peak force
F0; default -1 means `scale / actuator_acc0`), `range` (scaled operating
length, default 0.75–1.05), `timeconst` (default 0.01 0.04), `tausmooth`, and
`lmin, lmax, vmax, fpmax, fvmax` (FLV curve shape). Muscles need
`actuator_lengthrange`: set `lengthrange` explicitly, copy from joint/tendon
limits, or compute automatically (tune with the `lengthrange` element). A
convergence error usually means missing joint limits.

## Sensors and delays

Sensors do not affect simulation; output goes to `mjData.sensordata`. Common
attributes:

| Attribute | Default | Meaning |
|----|----|----|
| `name` | | Optional. |
| `noise` | "0" | Stored standard deviation only; not applied. |
| `cutoff` | "0" | If positive, limits absolute output. |
| `nsample` | "0" | Ring buffer size; required (> 0) for `delay` and `interval`. |
| `interp` | "zoh" | `zoh`, `linear` or `cubic` reading from history. |
| `delay` | "0" | Read values at `time - delay`. |
| `interval` | "0 0" | `period phase` for slower sampling; period 0 = every step. |

Actuators also support `nsample`, `delay`, `interp`. The usual setting is
`delay = timestep * nsample`. `delay > timestep * nsample` silently
extrapolates non-causally. History buffers need a positive timestep.

## Tips and tricks

**Slip**: check the normal force times sliding friction exceeds the load,
raise `friction`, use `condim` 4 or 6, add contact points, keep `multiccd`
and `nativeccd` enabled. Slow residual slip is expected in the soft model:
use elliptic cones with higher `impratio`, then `noslip_iterations` 1–3.

**High-frequency vibration**: reduce `timestep`, add `armature`, use
`implicit` or `implicitfast`.

**Backlash**: two coincident hinges; actuate only J1, limit J2:

```xml
<body>
  <joint name="J1" type="hinge" pos="0 0 0" axis="0 0 1" armature="0.01"/>
  <joint name="J2" type="hinge" pos="0 0 0" axis="0 0 1" limited="true" range="-1 1"/>
</body>
```

The armature on J1 avoids a singular mass matrix.

**Restitution**: direct-format `solref` with zero damping:

```xml
<worldbody>
  <geom type="plane" size="1 1 .1"/>

  <body pos="0 0 1">
    <freejoint/>
    <geom type="sphere" size="0.1" solref="-1000 0"/>
  </body>
</worldbody>
```

**Mocap bodies**: static world children with `mocap="true"`; set
`mjData.mocap_pos` / `mocap_quat` each step. For better-behaved contact, weld a
regular body to the mocap body with an equality constraint and tune its
`solref`/`solimp`.

**URDF**: add a `<mujoco>` child of `<robot>` with `compiler`, `option`,
`size` (e.g. `meshdir`, `balanceinertia`, `discardvisual`). URDF is not
schema-checked, so typos are silently ignored. Joint `effort` limits become
`actuatorfrcrange`. Convert once to MJCF and edit the MJCF.

**Memory**: the `size/memory` attribute sets the arena. Watch
`mjData.maxuse_arena`; aim for ~50% worst-case use. Out of memory drops
contacts or disables the solver for a step (warning), but stack exhaustion is
a hard error.

**Deformables** (`flex`, `flexcomp`): use `integrator="discrete"` with Newton,
`1–4 ms` steps; continuum `young`/`poisson` elasticity for accuracy; prefer
`dof="trilinear"` for volumes; `selfcollide="none"` unless the flex folds.

**System identification**: fit armature, damping, frictionloss, gains,
inertias and delays to hardware logs with
[mujoco.sysid](../python-bindings/SKILL.md) instead of hand-tuning.

## Model gallery

[MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie) is a
curated collection of well-designed models that work out of the box. Start
from or compare against these:

| Category | Models |
|----|----|
| Bipeds | Agility Cassie |
| Humanoids | Unitree G1, Unitree H1, Robotis OP3 |
| Mobile manipulators | Google Robot, Hello Robot Stretch 2 |
| Quadrupeds | Unitree A1, Go1, Go2; ANYmal B, C; Google Barkour v0, vB; Boston Dynamics Spot |
| Grippers & hands | Shadow E3M5, Robotiq 2F-85, Wonik Allegro |
| Arms | Franka Panda, Franka FR3, UR5e, UR10e, LBR iiwa14, xArm7, Sawyer, Lite 6, ViperX 300, WidowX 250, ALOHA 2, Unitree Z1 |
| Drones | Skydio X2, Bitcraze Crazyflie 2 |
| Biomechanical | Fruitfly, MS-Human-700 |

## Source docs

Verbatim copies, for details not covered above:

- [modeling.md](references/modeling.md)
- [models.md](references/models.md)
