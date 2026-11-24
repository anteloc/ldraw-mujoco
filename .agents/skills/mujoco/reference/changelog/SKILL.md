---
name: changelog
description: 'MuJoCo release notes from early versions up to 4.0.1 and upcoming changes: new features, breaking API and MJCF changes, bug fixes and deprecations per version. Use when code targets a specific MuJoCo version (e.g. a pinned 3.x), when behaviour differs between versions, or to check whether an attribute or function exists in a given release.'
---

# MuJoCo Changelog

Use this skill to check whether a function, field, attribute or behaviour exists in a
given MuJoCo release, and what changed between two releases (for example a project
pinned at 3.5.0 against docs written for 4.0.1). Versions are listed newest first.
3.5.0 → 4.0.1 is covered in detail; older releases list only breaking changes and
headline features. For anything not listed here (most bug fixes, MJX/Warp details,
models, docs), read the verbatim changelog in the source docs.

Since 3.5.0, version numbers follow Semantic Versioning (see
[VERSIONING.md](https://github.com/google-deepmind/mujoco/blob/main/VERSIONING.md)).
Releases before 2.1.0 are documented only at [roboti.us](https://www.roboti.us/download.html).

## Quick lookup: renamed, removed or changed, and since when

| Old / previous | New / current | Version |
|---|---|---|
| `camera/orthographic="true/false"`, `mjModel.cam_orthographic` | `camera/projection="orthographic/perspective"`, `cam_projection` (`mjtProjection`) | 3.5.0 |
| `mj_ray`, `mj_multiRay`, `mju_rayGeom`, `mj_rayHfield`, `mj_rayMesh` | extra `mjtNum normal[3]` argument (pass `NULL` in C) | 3.5.0 |
| `mju_rayFlex` | `mj_rayFlex` | 3.5.0 |
| contact `margin`/`gap` combined with max | summed | 3.5.0 |
| `ten_J_rownnz/rowadr/colind` in `mjData` | moved to `mjModel`, `ten_J` always sparse | 3.6.0 |
| `mjsJoint/mjsTendon.stiffness`, `.damping` scalars | `mjtNum[mjNPOLY+1]` arrays (`joint.stiffness[0] = val`) | 3.7.0 |
| `mjPLUGIN_LIB_INIT` | needs a name argument | 3.7.0 |
| URDF forced `strippath="true"` | respects setting, default "false" | 3.7.0 |
| `multiccd` off by default | on by default | 3.8.0 |
| detection `dist < margin`, force `dist < margin - gap` | detection `dist < margin + gap`, force `dist < margin` | 3.9.0 |
| `mjtnum.h` | `mjtype.h` | 3.9.0 |
| `mjx.make_data/put_data(nconmax=...)` | `naconmax` | 3.9.0 |
| `mjthread.h` threading API | *mju_threadpool* | 3.10.0 |
| `mjData.efc_diagApprox` | `efc_diagA` | 3.10.0 |
| `mj_fullM(m, dst, M)` | `mj_fullM(m, d, dst)` | 3.10.0 |
| `mju_{error,warning}_{i,s}` | removed (variadic `mju_error`/`mju_warning`) | 3.10.0 |
| `mjData.qM` | removed; use CSR `mjData.M` | 3.11.0 |
| `sleep_tolerance` default 1e-4 | 1e-3 | 3.11.0 |
| `mjv_moveCamera(..., scn, ...)` | `mjvScene` argument removed | 3.11.0 |
| `image/vnd.mujoco.texture` custom textures | PNG and KTX only | 3.12.0 |
| `dcmotor input="position/velocity"` | `input="pos"`/`"vel"`, gains in torque space | 3.12.0 |
| `bvactive` default "true" | "false" | 3.12.0 |
| `pixels, depth = mjx.render(...)` | `pixels, depth, d = mjx.render(...)` | 3.12.0 |
| implicit flex metric under `implicit`/`implicitfast` + CG | `integrator="discrete"` | 3.13.0 |
| `mj_readCtrl` | same signature as `mj_readSensor` (output buffer, returns `const mjtNum*`) | 3.14.0 |
| `mjp_getResourceProvider` etc. | `mjp_findProvider`, `mjp_registerProvider`, ... | 3.16.0 |
| `mjrf_addRenderableToScene`, `mjrf_setMeshData`, ... | `mjrf_addSceneRenderable`, `mjrf_uploadMesh`, ... | 3.16.0 |
| `filament.clearColor`, camelCase fog flags | `filament.clear_color`, snake_case | 3.16.0 |
| keyframes copied per `replicate` | one keyframe for the complete model | 3.16.0 |
| `mjs_addTexture(spec)` | `mjs_addTexture(spec, NULL)` | 3.17.0 |
| `mjs_fuseStatic`/`mjs_discardVisual` return 0 | return count, -1 on error | 3.17.0 |
| `mjNEQDATA` 11 | 12 | 3.17.0 |
| `cable` plugin, `composite` element | 1D `flexcomp` with `elasticity` | 4.0.0 |
| `flexvert` equality, `<edge equality="vert"/>` | removed | 4.0.0 |
| `mjModel.flex_matid` per flex, `mjsFlex.material` `mjString` | per element, `mjStringVec` | 4.0.0 |
| single `mujoco` Python package | `mujoco-core` + `mujoco-studio` + `mujoco` | 4.0.0 |
| `sample/record.cc` | `render model.xml out.rgb --duration=T --fps=F` | 4.0.0 |

## Upcoming (not yet released)

- *mju_QP*: dual active-set solver for dense convex QPs with bounds, two-sided linear and soft constraints, warmstartable.
- `mjModel.flex_cellempty`, `flex_celladr`; interpolated-flex points are evaluated in their active (non-empty) cell.
- Appending to an mjSpec body tree is O(1) (procedural construction up to ~250x faster).
- [strippath](../xml-reference/SKILL.md) no longer strips names matching a registered resource provider (e.g. `package://`).
- Breaking (rendering): Filament planar reflections are energy conserving. Orthographic free/tracking cameras derive view height from camera distance and `global/fovy`. Migration: set `global/fovy` back to an angle in degrees.
- Added `mjGEOM_DISC` rendering-only geom type (`size = [r_out, r_in, 0]`).
- Python: fixed a 4.0.0 memory leak in `mujoco-core` when `glfw` is missing.
- New `plugin/package_uri` resource provider for ROS `package://` URIs (build from source, load with *mj_loadPluginLibrary*).
- OpenUSD exporter writes `xformOp:translate` + `xformOp:orient` instead of `xformOp:transform`.

## 4.0.1 (November 11, 2026)

- Added *mjs_getInStringVec*.
- Studio Web Viewer (`mujoco-studio --gfx=web`, `mujoco.studio.launch_web`) works on Windows via the `mujoco-studio-wasm` wheel.
- Fixed a 4.0.0 sparse Cholesky bug that gave Newton a wrong Hessian factor (slow convergence, divergence).
- *mj_loadAllPluginLibraries* skips unloadable libraries with a warning instead of *mju_error*.
- Fixed single-shot multicontact for cylinder edges.

## 4.0.0 (November 6, 2026)

New features:
- `speculative` enable flag: [speculative contacts](../../physics-computation/speculative-contacts/SKILL.md) stop fast convex geoms tunneling through thin obstacles.
- Elasto-plasticity with state in `mjData.plastic` (`mjSTATE_PLASTIC`): `springyield` for joint and tendon springs, `yield` for 2D/3D flexes.
- Python split into `mujoco-core` (numpy only), `mujoco-studio` (Studio, Filament) and `mujoco` (both). When upgrading with pip, run `pip uninstall -y mujoco && pip install mujoco`, or `pip install --force-reinstall --no-deps mujoco mujoco-core mujoco-studio`.

Breaking (engine):
- `sidesite` semantics changed: the tendon follows the homotopy of the path through the side site. Existing models can change. Migration: place side sites so endpoints do not cross the opposite ray, typically mid-arc.
- `RK4` is now 4th-order for ball/free joint orientations (simulation changes).
- Added `mjContact.surfacevel[3]`, `mjData.xiquat`, `geom_xquat`, `site_xquat`, `mjModel.tendon_type` (`mjtTendon`).

Breaking (deformables):
- Removed the `cable` plugin and the `composite` element. Migration: use `flexcomp dim="1"` (`type="grid"`/`"circle"`/`"direct"`), `radius`, `<elasticity young= shear=>`, and `<pin id="0 1"/>` (was `initial="none"`), `<pin id="0"/>` (`"ball"`) or no pin (`"free"`).
- Open elastic 1D flexcomps create per-edge twist bodies and hinge joints `<name>_twist_*`, which changes `nq`, `nv`, `nbody` and `qpos` layout. Address bodies and joints by name.
- Elastic constants of non-interpolated flexes are fixed, so models get stiffer. The changelog gives conversion formulas to keep the old behaviour.
- 1D rod bending is not supported under `implicit`/`implicitfast`: use `discrete` or `Euler`. Flex edge stiffness/damping is not supported under `discrete`.
- Unpinned flexcomps fail to compile if an ancestor body has joints.
- Removed `flexvert` equality and its `mjModel`/`mjData` fields. `mjEQ_FLEXVERT` stays as an erroring placeholder.
- `flex_matid` is `(nflexelem x 1)`. `mjsFlex.material` is `mjStringVec` (Python: `flex.material = ['mat']`).
- 1D `flex_bending` records grow from 4 to 10 values.
- Other changes: Newton is 1.4-3x faster on flexes, and Newton + `discrete` supports flexes attached to articulated bodies. Rods can have curved rest shapes and torsion. Volumetric interpolated flexes use FCM quadrature. Flex contacts are distributed with barycentric weights. Interpolated flexes support `passive` contact.

Breaking (compiler):
- Including the same file via different paths is rejected (`already included`).
- These models are now rejected: hfields with `nrow`/`ncol` < 2, fixed tendons on ball/free/duplicate joints or with negative armature, pulley `divisor` <= 0, bad camera references in `camprojection`/rangefinder, out-of-range skin face indices.
- Non-positive-definite inertias are bounded by `boundinertia` when it is positive, instead of failing to compile. *mj_encode* writes MJB for mjSpec (`model/vnd.mujoco.mjb`).

Rendering and other:
- Added geom `castshadow` (`mjModel.geom_castshadow`), *mjrf_setRenderableCastShadow*, Filament haze/skybox (`mjRND_HAZE`, `mjRND_SKYBOX`), *mjrf_flush*, `mjRND_POST_PROCESSING`, `filament.material.base_color_type`.
- `headlight.active` accepts "false"/"true"/"auto". The default is now "auto".
- Dropped Python 3.10. The manual and agent skills are bundled under `mujoco/doc/`.
- Removed `sample/record.cc`: use `render ... --duration --fps`.
- Bug fixes that change behaviour: accelerometer on static/mocap bodies reports gravity again (regression from 3.3.7). Actuators saturated by `actuatorfrcrange` give no implicit derivatives. *mj_setConst* wakes sleeping trees. Pairs without `solref` mix their geoms' `solref` with `solmix`. Windows paths are UTF-8. Stricter `dcmotor` validation.

## 3.17.0 (October 22, 2026)

- New batch API `mujoco/mjbatch.h` / Python `mujoco.batch` (`Batch(model, nsim)`, `bind()`, `expand()`, `step`, `rollout`, ...): results are bit-identical to a loop.
- 1D flex bending `elasticity` (`section`, `sectionsize`). Self-collision for interpolated flexes. Smaller default flex arena memory.
- *mj_setConst* no longer resolves `dampratio`, tendon spring length `(-1,-1)` or statistics. Set the model fields directly.
- Solver tolerances scale by the trace of the inertia. `meaninertia` is deprecated (compile warning).
- Breaking ABI: `mjNEQDATA` is 12. *mj_setConst* recomputes body-weld relpose (`eq_data[11]` flag).
- Single-shot multicontact with positive margins. *mju_boxQP* is faster. `sleep="init"` failures warn.
- Breaking API: *mjs_fuseStatic*/*mjs_discardVisual* return a count (test `< 0`). `mjs_addTexture(spec, NULL)`.
- Textures by reference (`compiler/passthrough="textures"`, `texture/embed="false"`). Added *mj_loadTexture*, *mj_embedAssets*, texture default classes, *mjs_dedupAssets*.
- Asset paths in `mjModel` store resolved paths/URIs (pass them to *mju_openResource* as is).
- Python: named-access fixes for multi-control actuators. `data.actuator('a').moment` is a dense read-only copy. Unallocated arena arrays read as zeros or -1.

## 3.16.0 (October 14, 2026)

- `frame` `scale`, `scaling` (`similar`/`geometry`) and `massscale` attributes.
- Compiler `savecompiled`, `savecanonical` (preserve authoring on save). *mj_copyBack* updates only modified fields.
- Bazel builds.
- Breaking: the decoder callback and *mju_decodeResource* take `char* error, int error_sz`. Resource-provider functions renamed (`mjp_registerProvider`, `mjp_findProvider`, `mjp_providerCount`, `mjp_registerArchiveProvider`, ...).
- `contact` sensor `linvel`/`angvel` data. *mj_setConst* recomputes bounding volumes, margins and fluid added mass.
- Breaking compiler: *mj_copyBack*/*mj_saveLastXML* fail on inexpressible changes. API-added assets need names. `replicate` no longer copies keyframes. `discardvisual` with massive visual geoms errors under `inertiafromgeom="true"`.
- `flexcomp mesh=` attribute. New builtin mesh types `grid`, `box`, `cylinder`, `ellipsoid`, `square`, `disc`. Added *mjs_fuseStatic*, body `fuse` attribute, *mjs_discardVisual*, *mjs_adoptInertial*.
- `settotalmass` is deprecated: use *mj_setTotalmass* + *mj_setConst*.
- Actuation: shortcuts inherit gains only from same-shortcut or `general` defaults. `pid` without `kp` has gain 1. Added `mjsActuator.type`, `input` for fixed/affine gaintype (`actuator_ctrlspec`), and `general inheritrange`.
- Breaking Filament: `mjrf` renames (see the table), custom flags take strings, VSM blur removed (use `filament.shadows.type="pcss"`), `filament.msaa.enabled` removed (use `visual/quality/offsamples`, *mjrf_setSceneMsaa*).
- Python: `model.opt`, `model.vis` and `model.stat` are assignable.

## 3.15.0 (October 5, 2026)

- Breaking: `dampratio` uses operational-space reflected inertia. Removed the `internal` flex collision option.
- Experimental Stable Neo-Hookean (`mjsFlex.elastic3d = 1`, not in MJCF). Capsule multicontact. `insidesite` `enclosed` attribute.
- *mj_saveModel*/*mj_loadModelBuffer* take `mjtSize` (models > 2 GiB). Fixes for `.mjz` paths.

## 3.14.0 (September 22, 2026)

- Experimental `ipc` flag (penetration-free dim-2 flex contact under `discrete`).
- Archive resource providers. `<frame>` elements are preserved when saving MJCF.
- Breaking: new *mj_readCtrl* signature. Actuator history stores `ctrlnum` values per sample. `mjsElement.signature` is 0 until compiled.
- `mjWARN_INERTIA` from more integrators. Sparse Newton no longer aborts on a lost pivot.
- Fixes: weld torque in *mj_rnePostConstraint*, spatial tendon forces in force/torque sensors. Tendon `actuatorfrclimited` defaults to "auto". `mjd_*FD` error when sleeping.

## 3.13.0 (September 8, 2026)

- New `discrete` integrator (implicit in the effective metric, with the `refsafe` flag). Breaking: the implicit flex metric needs `integrator="discrete"`.
- Mesh sites (`type="mesh"`), *mj_insideSite*. Python 3.15. Cylinder multicontact. Faster elliptic Newton.
- `custom/text` CDATA, `tactile` `cutoff`, `render.cc` sample.
- Breaking rendering: the PBR metallic fallback is white.

## 3.12.0 (August 20, 2026)

- MJCF grammar generated from `src/xml/mjcf.schema`. Breaking: PNG/KTX textures only.
- New `pid` actuator (`ki`, `imax`, `slewmax`, `input`). Redesigned `dcmotor` `input` signature (breaking, see the table).
- Breaking engine: passive flex contacts are implicit (implicit/implicitfast + CG). Removed `efc_L_rownnz/rowadr/colind`. `bvactive` default "false". Mocap bodies root their own weld group.
- Breaking rendering: primitive UVs changed (finite plane textures anchored bottom-left). `light/softness` (default 0.2; set 1 for the old look).
- Breaking MJX: `mjx.render` returns `d`. Breaking ABI: `mjsActuator.velrange/ffrange`, `pid` enum members, `mjResource.args`.
- Flex `nodecoord` attribute. OpenUSD Newton schema 0.4.0.

## 3.11.0 (July 27, 2026)

- `geom/surfacevel` (conveyors), `geom/adhesion`, `pair/adhesion`, `body/simple`.
- Gyroscopic derivatives in `implicitfast` (replace midpoint). `invdiscrete` no longer affects forward dynamics.
- `flg_gravcomp`, `flg_surfacevel` (`ngravcomp` deprecated).
- Breaking: `sleep_tolerance` 1e-3, `mjData.qM` removed, `mjd_inverseFD` `DmDq` is `(nv x nC)`, `mju_round` ties go away from zero, `mjv_moveCamera` lost `scn`, `mjrfMeshData` split (`mjrfMeshConfig`), `mjrVertexAttribute.bytes` removed, `mj_encode` returns `mjtSize`.
- Breaking ABI: `actuator_ctrlspec`, `so3` gain/bias, `mjvGeom.texid/texuniform/texrepeat`, `mjContact.adhesion`.
- MIMO actuator infrastructure (`ctrlnum`, `outnum`, `nout`). New `orientation` actuator. Added *mj_actuatorInputName*, *mj_resetCtrl*.
- Solvers: implicit flex metric in CG, PGS Nesterov momentum, Newton decrement, zero-iteration warmstart exits.
- `attach` self-attachment and `frame=` attribute, *mju_writeResource*. Python free threading on 3.14.

## 3.10.0 (June 22, 2026)

- *mju_threadpool* (breaking: `mjthread.h` removed). Unified logging API (*mju_setLogHandler*, *mju_setLogConfig*, *mju_info*, `mjLogMessage`). `mju_user_error`/`mju_user_warning` are deprecated.
- *mjs_numWarnings*, *mjs_getWarning* (`mjs_isWarning` deprecated). `compiler/conflict` attribute ("warning" default; future default "merge").
- Hager-Zhang CG. *mjs_makeFlex* / `body.make_flex()`. 1D flex from OBJ lines.
- Breaking: island matrices `iM, iLD, iefc_J` off the arena, `efc_diagA`, `mju_error_i/s` removed, `mj_fullM(m, d, dst)`.
- Security fix in the sysid toolbox (`allow_pickle=False`).

## 3.9.0 (May 27, 2026)

- `mjData.efc_Y`, `diagexact` flag. Flexes can sleep. *mjs_getTimer* / `mjtCTimer`. `mjtBool` replaces `mjtByte` for booleans.
- Breaking: margin/gap redesign. Migration for `gap > 0`: `margin_new = margin_old - gap_old`, `gap_new = gap_old`. Negative margins allowed.
- Breaking: `mjfCollision` fills `mjPreContact`, `mjtnum.h` → `mjtype.h`, `tactile` reports raw depth, MJX `nconmax` removed, new `mjassert.h`.

## 3.8.1 (May 11, 2026)

- PGS islands and random order. `elastic2d` for trilinear/quadratic. Midpoint integration only in `implicitfast`, without fluid.
- *mjs_getOriginSpec*, *mju_sym2dense*. Python `MjSpec.encode` and `mujoco.MjVfs` (the `assets` dict is deprecated).

## 3.8.0 (April 24, 2026)

- Python 3.14. Multi-cell trilinear/quadratic flexes. Per-cell `strain` equality (`cell`). *mj_maxContact*. `mj_containsBufferVFS`/`mj_containsFileVFS`.
- Breaking: `multiccd` on by default (disable it to restore). Child-spec asset paths resolve relative to the child.

## 3.7.0 (April 14, 2026)

- `dcmotor` actuator. Actuator `damping`/`armature` reflected to the transmission. Polynomial stiffness/damping (`mjNPOLY`, `jnt_stiffnesspoly`, ...).
- `connect`/`weld` Jdot·v bias. `mjpEncoder`, *mj_encode*, *mjp_registerEncoder*.
- Breaking: `mjsJoint/mjsTendon` stiffness/damping arrays, OBJ/STL decoders built in, `mjsFlex.vertcollide` removed, `mjPLUGIN_LIB_INIT(name)`, `mjWARN_VGEOMFULL` removed, URDF `strippath` respected.

## 3.6.0 (March 10, 2026)

- Breaking: `ten_J` always sparse, with index fields in `mjModel`.
- *mjs_getCompiler* / element `compiler` property. `strain` equality. Flex-SDF collisions. MJX-Warp batch rendering.

## 3.5.0 (February 12, 2026)

- MuJoCo Warp officially released. Python System Identification toolbox (`mujoco.sysid`).
- Actuator/sensor delays and sensor intervals via `mjData.history`. `flexvert` equality (removed in 4.0.0). Implicit flex integration (dense block).
- `rangefinder/camera` (one ray per pixel) and richer rangefinder outputs.
- Breaking: ray functions take `normal`, `mju_rayFlex` → `mj_rayFlex`, `cam_orthographic` → `cam_projection`, `getdir` removed from `mjpResourceProvider`, margins/gaps are summed.
- Camera frustum shown when `resolution` > 1. Camera `output` (`cam_output`). *mj_mountVFS*/*mj_unmountVFS*. Collision sensors no longer share computation.
- OpenUSD is an `mjpDecoder` plugin (`pxr_DIR` replaces `USD_DIR`). `mjModel` sizes are 64-bit. MJX: `graph_mode` in `put_model`.
- Fix: the `usethread` flag had disabled multithreaded mesh processing.

## 3.4.0 and 3.3.x (2025)

- **3.4.0**: sleeping islands (preliminary), `flexcomp dof="quadratic"`, *mj_fwdKinematics*, *mj_extractState*, *mj_copyState*, `MjsTendon.path`. `mjtSize` is `int64_t`. MJX: `tex_data` is numpy.
- **3.3.7**: Breaking: mjSpec `meshdir`/`texturedir` → `compiler.meshdir`/`compiler.texturedir`, `mjOption.apirate` removed, MJX `_full_compat` removed, `nconmax`/`njmax` default `None`, C++20 required. Added *mju_getXMLDependencies*.
- **3.3.6**: islands on by default (`mjDSBL_ISLAND`). Breaking: `qacc_warmstart` is updated in *mj_step* (so *mj_forward* is idempotent), `mjDSBL_PASSIVE` → `mjDSBL_SPRING` + `mjDSBL_DAMPER`, `mjMOUSE_SELECT` removed, MJX `ten_length` is public. Curved shells, `mesh/material`.
- **3.3.5**: `insidesite`, `contact` and `tactile` sensors, native SDFs (SdfLib removed), `mesh/builtin`, *mj_makeM*. Breaking: `mjVIS_FLEXBVH` → `mjVIS_MESHBVH`. MJX Warp backend (`impl='warp'`). Wheels are `manylinux_2_28`.
- **3.3.4**: Breaking: `mjs_detachBody`/`mjs_detachDefault` → *mjs_delete*, Python `spec.delete(element)`, *mjs_setName* (the `name` field is removed). `visual/global/cameraid`.
- **3.3.3**: Breaking: light `directional` → `type` (`mjtLightType`), texture `colorspace` (set "linear" for the old look). Added *mj_copyBack*, `mjData.M` (CSR). `mjv_sceneState` → *mjv_copyModel*/*mjv_copyData*. Shell plugin removed.
- **3.3.1**: Breaking: internal flex contacts default off, attach functions → *mjs_attach*. Tendon armature, `compiler/saveinertial`, tendon actuator force limits.
- **3.3.0**: `nativeccd` default (set "disable" to restore). `flexcomp dof="trilinear"`. Energy sensors. Breaking: *mjs_setDeepCopy* (attach is shallow by default), mesh inertia via `asset/mesh/inertia`, composite `grid` and `particle` removed.

## 3.2.x – 3.0.x (2023–2025)

- **3.2.7**: `rollout` multithreading (`Rollout` class). `mjData.qLDiagSqrtInv` removed.
- **3.2.6**: composite rope/loop removed. Python `bind`, mjSpec ids removed. Python 3.13 wheels.
- **3.2.5**: mjSpec stable. `exactmeshinertia` → mesh `inertia`. `convexhull` option, `mju_rotVecMat(T)` and `mjv_makeConnector` removed. Material `layer`. Composite box/cylinder/sphere removed.
- **3.2.4**: Newton needs no `nv*nv` memory. solid/membrane plugins moved into the engine. `mjs_setActivePlugins` → *mjs_activatePlugin*. Python 3.8 dropped.
- **3.2.3**: Breaking: `mpr_tolerance`/`mpr_iterations` → `ccd_tolerance`/`ccd_iterations`, `mjs_findMesh`/`mjs_findKeyframe` → `mjs_findElement`. `nativeccd` flag, site-based connect/weld, free joint `align`/`alignfree`, *mj_jacDot*, `mjtSameFrame`.
- **3.2.2**: texture/material limit back to 1000. **3.2.1**: `tex_rgb` → `tex_data`, `autoreset` flag, material texture sub-elements.
- **3.2.0**: [mjSpec](../../model-editing/SKILL.md) model editing introduced. MJCF `attach`. Orthographic cameras. `maxhullvert`, *mj_setKeyframe*, `mjUSESINGLE`. Quaternions are no longer normalized in place. Breaking: `mj_makeEmptyFileVFS`/`mj_findFileVFS` removed (use *mj_addBufferVFS*), *mj_deleteVFS* is required, `actuator_actdim` callback → `actdim`.
- **3.1.6**: *mj_geomDistance* with `distance`/`normal`/`fromto` sensors. Position `timeconst` and `dampratio`.
- **3.1.5**: MJCF `replicate`, compiler cache, `mesh_scale`, `bulbradius`/`metallic`/`roughness`. MJX: `device_get_into`/`device_put` removed.
- **3.1.4**: Breaking: native sensor noise removed. `actuatorgravcomp`, *mju_euler2Quat*, Python `mujoco.minimize`.
- **3.1.3**: `inheritrange`, *mj_addBufferVFS*, *mj_angmomMat*. **3.1.2**: `discardvisual` improved, `bvactive`, hfield `elevation`, `rollout` outputs changed (breaking).
- **3.1.0**: MJCF `frame`, position/intvelocity `kv`, `pid` actuator plugin, MJX `put_data`/`get_data`. **3.0.1**: `qfrc_spring/damper/gravcomp/fluid`, `actuatorgroupdisable`, MJX Newton.
- **3.0.0**: MJX, SDF collisions, `flex`/`deformable`/`flexcomp`, islands (*mj_island*). Breaking: `mjMARKSTACK`/`mjFREESTACK` → *mj_markStack*/*mj_freeStack*, `mj_stackAlloc` → *mj_stackAllocNum*, `nstack` → `narena` (bytes), `solver_iter` → `solver_niter`, `option/collision` removed, `mjModel.eq_active` → `eq_active0` + `mjData.eq_active`, `autolimits` default "true", `actuatorforcerange` → `actuatorfrcrange`. Added `filterexact`, `actearly`, `eulerdamp`, `invdiscrete`, `ls_iterations`, camera intrinsics, reversed-Z depth.

## 2.x (2021–2023)

- **2.3.7**: joint `actuatorfrcrange`, `jointactuatorfrc` sensor, asset `content_type`, *mjv_connector*. macOS 11 minimum.
- **2.3.6** (last with Python 3.7): *mj_getState*/*mj_setState*, `solreffriction`, *mjd_inverseFD*, *mj_multiRay*, muscle `tausmooth`, `mjmacro.h`. `mj_activate`/`mj_deactivate` removed.
- **2.3.5**: VFS asset fix (skip 2.3.4). **2.3.4**: `compiler/coordinate="global"` removed, resource providers, `launch_passive` handle with `sync`, `launch_repl` removed.
- **2.3.3**: `implicitfast` integrator, collision midphase, variadic `mju_error`. **2.3.2**: hashed *mj_name2id*. Plugin `capabilities` → `capabilityflags`.
- **2.3.1**: `mujoco.viewer`, Python `Renderer`, body `gravcomp`, `actdim`, *mj_loadPluginLibrary*. Breaking: `tendon_lengthspring` is `ntendon x 2`.
- **2.3.0**: `contact`/`efc_` arrays in the arena, plugin API, *mju_boxQP*, `assetdir`, cable composite. `MjData.contact` length is `ncon`.
- **2.2.2**: adhesion actuators, weld `torquescale`/`anchor` (`mjNEQDATA` 7 → 11), `refsite`, `autolimits`, `exactmeshinertia`, `shellinertia`. `distance` constraints removed.
- **2.2.1**: *mjd_transitionFD*, keyframe `ctrl`, `clock` sensor, `intvelocity`/`damper` shortcuts. `ctrl` is no longer clamped in place.
- **2.2.0**: open source, `implicit` integrator, `actlimited`/`actrange`, `qfrc_unc`/`qacc_unc` → `qfrc_smooth`/`qacc_smooth`, headers in `include/mujoco/`.
- **2.1.5**: experimental multiCCD. **2.1.4**: GLAD replaces GLEW, no `_nogl` library. **2.1.3**: simulate camera cycling.
- **2.1.2**: Python bindings (`pip install mujoco`), Unity plug-in, OBJ meshes, `reftype`/`refname` frame sensors, `fluidshape="ellipsoid"`.
- **2.1.1**: `mj_versionString`, `_mjModel` → `mjModel_`, exact capsule inertia. **2.1.0**: license manager removed, keyframe `mpos`/`quat`.

## Source docs

Verbatim copies, for details not covered above:

- [changelog.md](references/changelog.md)
