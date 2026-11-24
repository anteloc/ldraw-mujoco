---
name: xml-reference
description: 'Complete MJCF XML reference: every element (mujoco, compiler, option, size, visual, statistic, default, asset, mesh, worldbody, body, joint, geom, site, camera, light, contact pair/exclude, equality connect/weld/joint, tendon, actuator, sensor, keyframe, extension, plugin) with all attributes, types and defaults. Use when writing or checking any MJCF attribute such as solref, solimp, solimpfriction, margin, condim, friction, frictionloss, damping, armature, density, mass, inertia, meshdir or option flags.'
---

# MJCF XML Reference

A map of every MJCF element and its most-used attributes, with types and
internal defaults. Use it to write or check an attribute such as `solref`,
`condim`, `margin`, `frictionloss`, `armature`, `density` or an `option/flag`.
For anything not listed here, such as flex internals, dcmotor parameters or
camera intrinsics, read the verbatim `XMLreference.md` copy in the source docs.
For modeling concepts (defaults, solver parameters, shortcuts), see
[mjcf-modeling](../../mjcf-modeling/SKILL.md).

## Reading the reference

| Notation | Meaning |
|---|---|
| `string` | file name or user-defined name |
| `int(N)` / `real(N)` | array of N integers / reals (N omitted = 1); length enforced unless stated |
| `[a, b]` | keyword attribute; valid keywords in brackets |
| `required` | parser error if missing |
| `optional` | no internal default; stays "undefined" so the compiler knows it was not touched |
| `"..."` | optional, internal default in quotes |

Element icons: `star` required, appears once (`mujoco`). `sync` optional, repeatable recursively (`body`, `default`, `frame`, `replicate`). `dot` optional, at most once (`option/flag`, `body/inertial`, `visual/*`). No icon: optional, repeatable.

- Element and attribute order is free, with four exceptions: joints in a body (applied in sequence), elements of a spatial tendon (path order), repeated sections setting the same attribute (the last one wins), and several actuator shortcuts in one defaults class (each resets gain, bias and dynamics).
- Text content is ignored, except CDATA in `custom/text`.
- Units are not fixed. Hinge/ball `range`, `ref`, `springref` and orientations use `compiler/angle` (default **degree**). `camera/fovy`, `light/cutoff` and `visual/global/fovy` are always degrees.
- Shared orientation attributes `quat, axisangle, xyaxes, zaxis, euler` are explained under Frame orientations in [mjcf-modeling](../../mjcf-modeling/SKILL.md).
- `solref` / `solimp` (and the `*limit`, `*friction` variants) have no defaults in this chapter. Their semantics and defaults are in Solver parameters in [mjcf-modeling](../../mjcf-modeling/SKILL.md).
- Editors can validate against the generated XSD (`src/xml/generated/mjcf.xsd`). The XSD accepts some models that the compiler rejects.

```xml
<mujoco xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/google-deepmind/mujoco/refs/heads/main/src/xml/generated/mjcf.xsd">
```

## Element tree

```
mujoco(model="MuJoCo Model")
├─ compiler ─ lengthrange
├─ option ─ flag
├─ size · statistic · visual(global, quality, headlight, map, scale, rgba)
├─ default(class) ─ mesh texture material joint geom site camera light pair
│                   equality tendon general motor position velocity intvelocity
│                   pid orientation damper cylinder muscle adhesion dcmotor
├─ asset ─ mesh(plugin) hfield texture material(layer) model [skin: deprecated here]
├─ worldbody / body ─ inertial joint freejoint geom(plugin) site camera light
│                     flexcomp(contact edge elasticity pin plugin) plugin attach frame body
├─ contact ─ pair exclude
├─ deformable ─ flex(edge elasticity contact) skin(bone)
├─ equality ─ connect weld joint tendon flex flexstrain
├─ tendon ─ spatial(site geom pulley) fixed(joint)
├─ actuator ─ general motor position pid orientation velocity intvelocity damper
│             cylinder muscle adhesion dcmotor plugin
├─ sensor ─ (see Sensors)
├─ keyframe ─ key
├─ custom ─ numeric text tuple(element)
└─ extension ─ plugin ─ instance ─ config
Meta: include(file), frame, replicate(count, sep, offset, euler), attach, flexcomp
```

## option (maps to `mjModel.opt`, can be changed at runtime)

| Attribute | Type, default | Notes |
|---|---|---|
| `timestep` | real, "0.002" | seconds; main speed/accuracy trade-off |
| `integrator` | [Euler, RK4, implicit, implicitfast, discrete], "Euler" | Euler handles joint damping implicitly |
| `solver` | [PGS, CG, Newton], "Newton" | |
| `iterations` | int, "100" | solver max iterations |
| `tolerance` | real, "1e-8" | 0 disables early termination |
| `ls_iterations` / `ls_tolerance` | int "50" / real "0.01" | CG/Newton linesearch |
| `noslip_iterations` / `noslip_tolerance` | int "0" / real "1e-6" | 0 disables NoSlip |
| `ccd_iterations` / `ccd_tolerance` | int "35" / real "1e-6" | convex collisions |
| `sdf_iterations` / `sdf_initpoints` | int "10" / int "40" | SDF collisions |
| `sleep_tolerance` | real, "1e-3" | velocity below which sleeping is allowed |
| `cone` | [pyramidal, elliptic], "pyramidal" | |
| `impratio` | real, "1" | >1 makes friction "harder" (elliptic cones) |
| `jacobian` | [dense, sparse, auto], "auto" | auto: dense up to 60 dofs |
| `gravity` | real(3), "0 0 -9.81" | |
| `wind` / `magnetic` | real(3), "0 0 0" / "0 -0.5 0" | |
| `density` / `viscosity` | real, "0" / "0" | of the medium; 0 disables lift/drag / viscous forces |
| `o_margin` | real, "0" | used only when the `override` flag is enabled |
| `o_solref`, `o_solimp`, `o_friction` | (no default given) | override contact params when `override` is enabled |
| `actuatorgroupdisable` | int(31), optional | actuator groups 0..30 producing no force |

### option/flag

Every flag is `[disable, enable]`. These default to **"enable"**:
`constraint, equality, frictionloss, limit, contact, spring, damper, gravity,
clampctrl, warmstart, filterparent, actuation, refsafe, sensor, midphase,
nativeccd, island, eulerdamp, autoreset, multiccd`.

These default to **"disable"**:
`override, energy, fwdinv, invdiscrete, sleep, diagexact, ipc, speculative`.

- `constraint` and the type flag (`equality`, `frictionloss`, `limit`, `contact`) must both be enabled for a constraint type to run.
- Disabling `spring` and `damper` together disables all passive forces, including gravity compensation and fluid forces.
- `refsafe` uses `max(solref[0], 2*timestep)`.
- `multiccd` gives several contacts for convex-convex pairs (for example mesh-mesh), which helps flat faces rest stably.
- `sleep` also acts at `mj_makeData` / `mj_resetData`.
- `ipc` is experimental and works only with the `discrete` integrator.

## compiler (parse/compile time only)

| Attribute | Type, default | Notes |
|---|---|---|
| `angle` | [radian, degree], "degree" (URDF: always radian) | |
| `eulerseq` | string, "xyz" | lower case intrinsic, upper case extrinsic; URDF rpy = "XYZ" |
| `meshdir` / `texturedir` / `assetdir` | string, optional | `assetdir` sets both; the specific ones win |
| `strippath` | [false, true], "false" | |
| `autolimits` | [false, true], "true" | infer `limited`/`ctrllimited`/... from `*range` |
| `inertiafromgeom` | [false, true, auto], "auto" | auto: only bodies without `<inertial>` |
| `inertiagrouprange` | int(2), "0 5" | geom groups used for mass/inertia |
| `boundmass` / `boundinertia` | real, "0" / "0" | lower bounds (not world body) |
| `balanceinertia` | [false, true], "false" | fix A+B>=C violations |
| `settotalmass` | real, "-1" | deprecated |
| `fitaabb` | [false, true], "false" | primitive fit: AABB vs inertia box |
| `discardvisual` | [false, true], "false" (URDF "true") | drops geoms with contype=conaffinity=0, unused materials/meshes |
| `fusestatic` | [false, true], "false" (URDF "true") | |
| `alignfree` | [false, true], "false" | default for `freejoint/align` |
| `usethread` | [false, true], "true" | |
| `saveinertial` / `savecompiled` / `savecanonical` | "false" / "true" / "true" | save behavior |
| `coordinate` | [local, global], "local" | "global" is an error |
| `conflict` | [warning, merge, error], "warning" | `mjs_attach` global-attribute conflicts |
| `passthrough` | [none, textures], "none" | keep textures by reference |

`compiler/lengthrange` sets `mode` [none, muscle, muscleuser, all] "muscle", `useexisting` "true", `uselimit` "false", `accel` "20", `maxforce` "0", `timeconst` "1", `timestep` "0.01", `inttotal` "10", `interval` "2", `tolrange` "0.05".

## size and statistic

- **size:** `memory` string "-1" (for example "16M"). `nuserdata` "0". `nkey` "0". `nuser_body|jnt|geom|site|cam|tendon|actuator|sensor` "-1". Legacy: `njmax`, `nconmax`, `nstack` "-1". Setting both `njmax` (or `nstack`) and `memory` is an error.
- **statistic:** all optional overrides. `meanmass` scales perturbation forces. `meansize` is the length unit of `visual/scale`. `extent` (>0; the free camera starts at 1.5x extent). `center` real(3). `meaninertia` is deprecated.

## asset

| Element | Key attributes (type, default) |
|---|---|
| `mesh` | `name`, `class`, `file` (stl/msh/obj), `content_type`, `scale` real(3) "1 1 1" (negative flips), `inertia` [convex, exact, legacy, shell] "legacy" (convex recommended), `smoothnormal` "false", `maxhullvert` int "-1", `vertex`, `normal`, `texcoord`, `face`, `refpos` "0 0 0", `refquat` "1 0 0 0", `builtin` (sphere, hemisphere, cone, supersphere, supertorus, wedge, plate, grid, box, cylinder, ellipsoid, square, disc) + `params`, `material` |
| `hfield` | `name`, `file` (PNG or custom binary), `content_type`, `nrow` "0", `ncol` "0", `elevation`, `size` real(4) **required** (radius_x, radius_y, elevation_z, base_z) |
| `texture` | `name`, `type` [2d, cube, skybox] "cube", `file`, `fileright/left/up/down/front/back`, `gridsize` "1 1", `gridlayout`, `builtin` [none, gradient, checker, flat] "none", `rgb1` "0.8 0.8 0.8", `rgb2` "0.5 0.5 0.5", `mark` [none, edge, cross, random] "none", `markrgb` "0 0 0", `random` "0.01", `width`/`height` "0", `hflip`/`vflip` "false", `nchannel` "3", `colorspace` [auto, linear, sRGB] "auto", `embed` [false, true, auto] "auto" |
| `material` | `name` **required**, `texture`, `texrepeat` "1 1", `texuniform` "false", `emission` "0", `specular` "0.5", `shininess` "0.5", `reflectance` "0", `metallic` "-1", `roughness` "-1", `rgba` "1 1 1 1"; child `layer(texture, role)` with roles rgb, normal, occlusion, roughness, metallic, opacity, emissive, orm, rgba |
| `model` | `name`, `file` **required**, `content_type` (text/xml): a sub-model for `attach` |

The compiler centers each mesh and aligns it with its principal axes, storing the offsets in `mesh_pos` / `mesh_quat`. Collision uses the convex hull.

## Kinematic tree

### body / worldbody

`worldbody` has no attributes, no `inertial` and no `joint`, and its name is "world".
`body` attributes: `name`, `childclass`, `mocap` "false" (only world children
without joints), `pos` (default 0,0,0), orientation, `gravcomp` real "0" (1 =
exact compensation), `sleep` [auto, never, allowed, init] "auto", `simple`
[false, auto] "auto", `fuse` [false, auto] "auto", `user`. Without joints, a body is welded to its parent.

### inertial (presence disables inference for this body)

`pos` real(3) **required**, orientation, `mass` real **required** (>=0), and
`diaginertia` real(3) or `fullinertia` real(6) (M11 M22 M33 M12 M13 M23). One of the two inertia attributes is needed.

### joint

| Attribute | Type, default | Notes |
|---|---|---|
| `type` | [free, ball, slide, hinge], "hinge" | free only in world children |
| `pos` / `axis` | real(3), "0 0 0" / "0 0 1" | axis auto-normalized |
| `range` | real(2), "0 0" | ball: only 2nd value used, first 0 |
| `limited` | [false, true, auto], "auto" | |
| `margin` | real, "0" | limit activation distance |
| `ref` / `springref` | real, "0" / "0" | `qpos0` / `qpos_spring` |
| `stiffness` | real, "0 0 0" | a, b, c polynomial spring |
| `damping` | real, "0 0 0" | a, b, c polynomial damping |
| `springdamper` | real(2), "0 0" | timeconst, dampratio; overrides stiffness/damping |
| `armature` | real, "0" | added inertia; improves stability |
| `frictionloss` | real, "0" | dry friction (positive enables) |
| `solreflimit`, `solimplimit` | | limit constraint params |
| `solreffriction`, `solimpfriction` | | dry-friction constraint params |
| `actuatorfrcrange` / `actuatorfrclimited` | real(2) "0 0" / auto | clamps total actuator force (hinge/slide) |
| `actuatorgravcomp` | [false, true], "false" | gravcomp goes to `qfrc_actuator` |
| `springyield` | real, "0" | plasticity threshold |
| `group` | int, "0" | |

`<freejoint/>` takes only `name`, `group` and `align` [false, true, auto] "auto". It expands to `<joint type="free" stiffness="0" damping="0" frictionloss="0" armature="0"/>` and does **not** inherit joint defaults.

### geom

| Attribute | Type, default | Notes |
|---|---|---|
| `type` | [plane, hfield, sphere, capsule, ellipsoid, cylinder, box, mesh, sdf], "sphere" | |
| `size` | real(3), "0 0 0" | see the size table below; defaults are invalid |
| `fromto` | real(6), optional | capsule, box, cylinder, ellipsoid; overrides pos/orientation |
| `pos` | real(3), "0 0 0" | plus orientation attributes |
| `contype` / `conaffinity` | int, "1" / "1" | collide if `contype` of one AND `conaffinity` of the other share a bit |
| `condim` | int, "3" | 1 frictionless, 3 sliding, 4 +torsional, 6 +rolling; pair uses max |
| `friction` | real(3), "1 0.005 0.0001" | sliding, torsional, rolling |
| `priority` / `solmix` | int "0" / real "1" | contact param combination |
| `solref`, `solimp` | | contact constraint params |
| `margin` | real, "0" | forces active below this distance |
| `gap` | real, "0" | detect at margin+gap; inactive contacts in the gap |
| `mass` | real, optional | overrides density |
| `density` | real, "1000" | mass/volume (mass/area if `shellinertia`) |
| `shellinertia` | [false, true], "false" | primitives only; meshes use `mesh/inertia="shell"` |
| `group` | int, "0" | groups 0, 1, 2 visible by default; inertia uses `inertiagrouprange` |
| `material` / `rgba` | string / real(4) "0.5 0.5 0.5 1" | rgba wins if not default |
| `mesh` / `hfield` | string | mesh with a primitive type fits that primitive |
| `fitscale` | real, "1" | |
| `castshadow` | [false, true], "true" | |
| `surfacevel` | real(6), "0 0 0 0 0 0" | conveyor/turntable surface velocity |
| `adhesion` | real, "0" | per-contact pull-off force |
| `fluidshape` / `fluidcoef` | [none, ellipsoid] "none" / real(5) "0.5 0.25 1.5 1.0 1.0" | |

| Type | Sizes |
|---|---|
| plane | 3: X half, Y half, grid spacing (0 = infinite); world/static only |
| sphere | 1: radius |
| capsule, cylinder | 1 or 2: radius; half-length (omitted with `fromto`) |
| ellipsoid | 3: radii |
| box | 3: half-sizes |
| hfield, mesh | 0: taken from the asset |

### site, camera, light

- **site:** `type` [sphere, capsule, ellipsoid, cylinder, box, mesh] "sphere", `size` "0.005 0.005 0.005", `rgba` "0.5 0.5 0.5 1", `group` "0", `material`, `mesh`, `fromto`, `pos`, orientation, `user`. Sites take no part in collisions or inertia.
- **camera:** looks along -Z, +X right, +Y up. `mode` [fixed, track, trackcom, targetbody, targetbodycom] "fixed", `target`, `projection` [perspective, orthographic] "perspective", `fovy` "45" (degrees), `resolution` int(2) "1 1", `output` [rgb, depth, distance, normal, segmentation] "rgb", `sensorsize`/`focal`/`focalpixel`/`principal`/`principalpixel` "0 0", `ipd` "0.068".
- **light:** `mode`/`target` as camera, `type` [spot, directional, point, image] "spot", `castshadow` "true", `active` "true", `pos` "0 0 0", `dir` "0 0 -1", `diffuse` "0.7 0.7 0.7", `ambient` "0 0 0", `specular` "0.3 0.3 0.3", `attenuation` "1 0 0", `cutoff` "45" (degrees), `exponent` "10", `range` "10.0", `intensity` "0.0", `bulbradius` "0.02", `softness` "0.2". `directional` is a deprecated legacy attribute.

### frame, attach, replicate, include

- **frame:** `name`, `childclass`, `pos` "0 0 0", orientation, `scale` real(1 or 3) "1", `scaling` [similar, geometry] "similar", `massscale` "0" (0 = volume ratio). Frames are preserved on save.
- **attach:** `model` (an asset `model`; omit for self-attachment), `body` or `frame`, `prefix` **required**.
- **replicate:** `count` **required**, `sep`, `offset` real(3), `euler` real(3). Joints cannot be direct children; keyframes are not replicated.
- **include:** `file` **required**, relative to the main file. Each file can be included at most once. Prefer `attach`.

## contact

- **pair:** `geom1`, `geom2` **required**, `name`, `class`, `condim` "3", `friction` real(5) "1 1 0.005 0.0001 0.0001" (anisotropic; length not enforced), `solref`, `solimp`, `solreffriction` "0 0" (= use solref; elliptic cones only), `margin` "0", `gap` "0", `adhesion` "0". Geom properties are not used for a pair.
- **exclude:** `body1`, `body2` **required**, `name`. Excludes all geom collisions between the two bodies.

## equality

All types share `name`, `class`, `active` [false, true] "true", `solref` and `solimp`.

| Element | Specific attributes |
|---|---|
| `connect` | `body1` + `anchor` real(3) (in body1 frame), optional `body2` (default world); or `site1` + `site2` |
| `weld` | `body1`, `body2`, `relpose` real(7) "0 1 0 0 0 0 0" (zero quat = use qpos0), `anchor` "0 0 0", `torquescale` "1" (0 behaves like connect); or `site1` + `site2` |
| `joint` | `joint1` **required**, `joint2`, `polycoef` real(5) "0 1 0 0 0" (quartic y-y0 = f(x-x0)) |
| `tendon` | `tendon1` **required**, `tendon2`, `polycoef` "0 1 0 0 0" |
| `flex` | `flex` **required**: edge lengths |
| `flexstrain` | `flex` **required**, `cell` int(3): trilinear/quadratic 3D flex |

## tendon

**spatial:** `name`, `class`, `group` "0", `limited` "auto", `range` "0 0",
`actuatorfrclimited`/`actuatorfrcrange`, `solreflimit`, `solimplimit`,
`solreffriction`, `solimpfriction`, `margin` "0", `frictionloss` "0", `width`
"0.003", `material`, `rgba`, `springlength` real(2) "-1 -1" (-1 = from
`qpos_spring`; two values = deadband), `stiffness` "0 0 0", `damping` "0 0 0",
`springyield` "0", `armature` "0", `user`. Path children: `site(site)`,
`geom(geom, sidesite)` (sphere/cylinder only), `pulley(divisor)`.

**fixed:** a subset of the spatial attributes. Child `joint(joint, coef)` takes scalar joints only, and `coef` is required.

## actuator

### Common attributes (`general` and shortcuts)

| Attribute | Type, default | Notes |
|---|---|---|
| transmission | exactly one of `joint`, `jointinparent`, `site` (+`refsite`), `body`, `tendon`, `cranksite` (+`slidersite`, `cranklength`) | |
| `gear` | real(6), "1 0 0 0 0 0" | scales length, moment, velocity, force |
| `ctrlrange` / `forcerange` / `actrange` | real(2), "0 0" | needs `*limited` if `autolimits="false"` |
| `ctrllimited` / `forcelimited` / `actlimited` | [false, true, auto], "auto" | |
| `lengthrange` | real(2), "0 0" | |
| `damping` | real(3), "0 0 0" | applied at target, scaled by gear² |
| `armature` | real, "0" | reflected inertia, scaled by gear² |
| `group` | int, "0" | see `option/actuatorgroupdisable` |
| `nsample` / `interp` / `delay` | int "0" / [zoh, linear, cubic] "zoh" / real "0" | delay needs nsample>0 |
| `user` | real(nuser_actuator) | |

`general` only: `dyntype` [none, integrator, filter, filterexact, pid, dcmotor,
muscle, user] "none", `gaintype` [fixed, affine, muscle, dcmotor, pid, so3,
user] "fixed", `biastype` [none, affine, muscle, dcmotor, so3, user] "none",
`dynprm` real(10) "1 0 ... 0", `gainprm` real(10) "1 0 ... 0", `biasprm`
real(10) "0 ... 0", `actdim` "-1", `actearly` "false", `input`,
`inheritrange` "0", `velrange`/`ffrange` "0 0". The force is
`gain_term * (act or ctrl) + bias_term`.

### Shortcuts (each expands to `general`)

| Shortcut | Custom attributes (default) | Expansion |
|---|---|---|
| `motor` | none | fixed gain 1, no bias |
| `position` | `kp` "1", `kv` "0", `dampratio` "0", `timeconst` "0", `inheritrange` "0" | gainprm kp; biasprm 0 -kp -kv; filterexact if timeconst>0 |
| `velocity` | `kv` "1" | gainprm kv; biasprm 0 0 -kv |
| `intvelocity` | `kp` "1", `kv` "0", `dampratio` "0", `inheritrange` "0" | integrator dynamics; sets actrange |
| `pid` | `kp` "1", `kv` "0", `dampratio`, `ki` "0", `imax` "0", `slewmax` "0", `input` "pos vel", `posrange`/`velrange`/`ffrange` | gaintype pid |
| `orientation` | `kp` "1", `kv` "0", `dampratio`, `input` [expmap, quat] "expmap" | so3 gain/bias; ball joint or site+refsite |
| `damper` | `kv` "1" | F = -kv·vel·ctrl; ctrlrange required, nonnegative |
| `cylinder` | `timeconst` "1", `area` "1", `diameter`, `bias` "0 0 0" | filter dynamics |
| `muscle` | `timeconst` "0.01 0.04", `tausmooth` "0", `range` "0.75 1.05", `force` "-1", `scale` "200", `lmin` "0.5", `lmax` "1.6", `vmax` "1.5", `fpmax` "1.3", `fvmax` "1.2" | muscle dyn/gain/bias |
| `adhesion` | `body` **required**, `gain` "1" | body transmission, ctrllimited |
| `dcmotor` | `resistance`, `motorconst`, `nominal`, `inductance`, `thermal`, `saturation`, `cogging`, `lugre`, `input` "voltage", `controller` | see the verbatim copy |

`kv` and `dampratio` are exclusive. Use the implicitfast or implicit integrator with `kv`, `dampratio` and velocity servos.

## Sensors

All sensors share `name`, `noise`, `cutoff`, `nsample`, `interval`, `delay` and `user`. Outputs are concatenated into `mjData.sensordata`.

| Attach by | Sensors |
|---|---|
| `site` (required) | touch, accelerometer, velocimeter, gyro, force, torque, magnetometer |
| `site` or `camera` | rangefinder (`data` [dist, dir, origin, point, normal, depth] "dist") |
| `site` + `camera` | camprojection |
| `joint` | jointpos, jointvel, jointactuatorfrc, ballquat, ballangvel, jointlimitpos, jointlimitvel, jointlimitfrc |
| `tendon` | tendonpos, tendonvel, tendonactuatorfrc, tendonlimitpos, tendonlimitvel, tendonlimitfrc |
| `actuator` | actuatorpos, actuatorvel, actuatorfrc |
| `objtype` [body, xbody, geom, site, camera] + `objname` (+ `reftype`, `refname`) | framepos, framequat, framexaxis, frameyaxis, framezaxis, framelinvel, frameangvel; framelinacc and frameangacc have no ref frame |
| `body` | subtreecom, subtreelinvel, subtreeangmom |
| `objtype` + `objname` + `site` (+ `enclosed` "false") | insidesite |
| `geom1`/`body1` + `geom2`/`body2` | distance, normal, fromto; `cutoff` is the max detection distance (default 0 reports only penetration) |
| matching `geom*`/`body*`/`subtree*`/`site` | contact: `num` "1", `data` [found, force, torque, dist, pos, normal, tangent, linvel, angvel] "found", `reduce` [none, mindist, maxforce, netforce] "none" |
| `geom` + `mesh` | tactile |
| none | e_potential, e_kinetic, clock |
| callback | user: `objtype`, `objname`, `datatype` [real, positive, axis, quaternion] "real", `needstage` [pos, vel, acc] "acc", `dim` **required** |

Multi-value `data` keywords must keep the listed order.

## keyframe/key

`name`, `time` "0", `qpos` (default `qpos0`), `qvel`, `act`, `ctrl` (default
zeros), `mpos`, `mquat` (default `body_pos` / `body_quat`), `plastic`. Missing entries take
default values. The number of keys is max(`size/nkey`, number of `key` elements).

## visual (maps to `mjModel.vis`)

- **global:** `cameraid` "-1", `orthographic` "false", `fovy` "45", `ipd` "0.068", `azimuth` "90", `elevation` "-45", `linewidth` "1", `glow` "0.3", `realtime` "1", `offwidth` "640", `offheight` "480", `ellipsoidinertia` "false", `bvactive` "false".
- **quality:** `shadowsize` "4096", `offsamples` "4", `numslices` "28", `numstacks` "16", `numquads` "4".
- **headlight:** `ambient` "0.1 0.1 0.1", `diffuse` "0.4 0.4 0.4", `specular` "0.5 0.5 0.5", `active` [false, true, auto] "auto".
- **map:** `stiffness` "100", `stiffnessrot` "500", `force` "0.005", `torque` "0.1", `alpha` "0.3", `fogstart` "3", `fogend` "10", `znear` "0.01", `zfar` "50", `haze` "0.3", `shadowclip` "1", `shadowscale` "0.6", `actuatortendon` "2".
- **scale** (multiples of `meansize`) and **rgba** (decor colors): see the verbatim copy.

## default

`default(class)` nests, and the top level is "main". Each child sets the dummy
element of its type: all attributes except `name` and `class`. Further exceptions:

- texture: no file attributes or content_type
- camera: no mode or target
- pair: no geom1 or geom2
- equality: `active`, `solref`, `solimp` only
- mesh: `scale` and `maxhullvert` only
- actuators: no transmission targets; adhesion: no `body`

A class holds a single actuator default.

## custom and extension

- `custom/numeric(name, size, data)`
- `custom/text(name, data)`
- `custom/tuple(name)` > `element(objtype, objname, prm "0")`
- `extension/plugin(plugin)` > `instance(name)` > `config(key, value)`
- `plugin(plugin | instance)` under body, geom, mesh, flexcomp, actuator, sensor

## Deformables (long tail)

`flexcomp` is a macro that creates a `flex`, child bodies and an optional flex
equality. It takes `name` **required**, `type` [grid, box, cylinder, ellipsoid, disc,
circle, mesh, gmsh, direct] "grid", `dim` "2", `dof` [full, radial, trilinear,
quadratic, 2d] "full", `count` "10 10 10", `spacing` "0.02 0.02 0.02", `mass` "1",
`inertiabox` "0.005", `rigid` "false", and the children `pin`, `edge`, `elasticity` and `contact`.
`deformable/flex` takes `dim` "2", `radius` "0.005", `body` and `element` **required**. Skins are visual only.
See the verbatim copy for elasticity, plasticity and contact details.

## Pitfalls

- Hinge `range` is in **degrees** unless `compiler angle="radian"`.
- With `autolimits="false"`, setting `range`, `ctrlrange` and so on without the matching `*limited` is an error.
- `solreffriction` on `pair` takes effect only with `cone="elliptic"`.
- Mesh `inertia` defaults to "legacy", which overcounts volume for non-convex meshes. Use "convex" or "exact".
- Only geoms whose `group` is within `inertiagrouprange` "0 5" contribute inferred mass and inertia. Put redundant visual geoms in a group outside that range to exclude them. World-body geoms never count.
- `margin` makes contacts active (forces) at a distance. `gap` detects contacts without force.
- Joint defaults such as damping or armature leak into `<joint type="free">`. Use `<freejoint/>`.
- `discardvisual` with `inertiafromgeom="true"` is a compile error if a discarded geom contributed inertia.

## Source docs

Verbatim copies, for details not covered above:

- [XMLreference.md](references/XMLreference.md)
