---
name: api-functions
description: 'MuJoCo C API functions by group: parse and compile, main simulation (mj_step, mj_forward), support (mj_jac, mj_contactForce, mj_name2id), components, ray casting, printing, virtual file system, initialization, visualization, OpenGL/Filament rendering, UI, derivatives, plugins, threads, batched simulation, math and quaternion utilities, and the mjSpec editing functions (mjs_addBody, mjs_attach, attribute setters/getters, find utilities). Use when looking up the signature or semantics of a mj_*, mjv_*, mjr_*, mju_*, mjd_* or mjs_* function.'
---

# MuJoCo C API Functions

Use this skill to look up the exact C prototype and semantics of a MuJoCo API function (`mj_*`, `mjv_*`, `mjr_*`, `mjrf_*`, `mjui_*`, `mju_*`, `mjd_*`, `mjc_*`, `mjp_*`, `mjb_*`, `mjs_*`). The most-used functions are listed with their verbatim prototypes. The long tail is listed by name, grouped as in `mujoco.h` and the docs. For any prototype not shown here, open the verbatim `APIfunctions.md` copy in the source docs instead of guessing. Struct fields and enums are in [api-types](../api-types/SKILL.md); callbacks and constants are in [api-globals](../api-globals/SKILL.md).

## Conventions

| Prefix | Group |
|----|----|
| `mj_` | parse/compile, simulation, support, components, VFS, initialization |
| `mju_` | utilities: math, errors/logging, memory, resources, threads |
| `mjv_` / `mjr_` / `mjrf_` / `mjui_` | abstract visualization / OpenGL / Filament rendering / UI |
| `mjd_` | derivatives (analytic, or finite-differenced with suffix `FD`) |
| `mjc_` / `mjp_` / `mjb_` | signed distance functions / plugins and providers / batched simulation (`mujoco/mjbatch.h`) |
| `mjs_` | model editing on `mjSpec` |

- Outputs usually come first. Derivative functions are the exception: their outputs are the trailing arguments.
- Error reporting: `char* error, int error_sz`. If `error` is not NULL, it must have size `error_sz`. The docs mark optional pointers as *Nullable*.
- `mjSpec` compile errors are read with `mjs_getError`, not from a buffer.
- Most users need only a small fraction of the API: parse/compile, `mj_step`, and a few support functions.

## Parse and compile

```C
mjModel* mj_loadXML(const char* filename, const mjVFS* vfs, char* error, int error_sz);
mjSpec* mj_parseXML(const char* filename, const mjVFS* vfs, char* error, int error_sz);
mjSpec* mj_parseXMLString(const char* xml, const mjVFS* vfs, char* error, int error_sz);
mjSpec* mj_parse(const char* filename, const char* content_type,
                 const mjVFS* vfs, char* error, int error_sz);
mjModel* mj_compile(mjSpec* s, const mjVFS* vfs);
int mj_recompile(mjSpec* s, const mjVFS* vfs, mjModel* m, mjData* d);
int mj_copyBack(mjSpec* s, const mjModel* m);
int mj_saveXML(const mjSpec* s, const char* filename, char* error, int error_sz);
int mj_saveXMLString(const mjSpec* s, char* xml, int xml_sz, char* error, int error_sz);
mjtSize mj_encode(const mjSpec* s, const mjModel* m, const char* filename,
                  const char* content_type, const mjVFS* vfs, char* error,
                  int error_sz);
```

- `mj_loadXML` parses MJCF or URDF and compiles it. It returns NULL on failure, so check `error`. A non-NULL `vfs` is searched before the disk.
- `mj_compile` returns NULL on failure; read the error with `mjs_getError`. A spec can be edited and compiled many times, and each compile gives a new model. Compiling completes keyframes (sized to the model, added up to `nkey`). The `discardvisual` and `fusestatic` compiler attributes apply `mjs_discardVisual` and `mjs_fuseStatic` to the spec, so pointers to removed elements become invalid.
- `mj_recompile` reallocates the given `mjModel`/`mjData` in place and keeps the integration state when DOFs are added or removed. It returns 0 on success. **On failure it deletes `m` and `d`.**
- `mj_copyBack` writes values that were changed in the compiled model back into the spec. It covers `opt`, `vis`, `stat`, the real-valued element parameters, custom data, keyframes and hfield data. It returns 1 on success and 0 when the structure differs or a change cannot be expressed (error via `mjs_getError`). Then nothing is copied.
- `mj_saveXML` returns 0 on success and -1 otherwise. The `savecompiled` and `savecanonical` compiler attributes select what is saved. `mj_saveXMLString` returns the required size if the buffer is too small.
- `mj_encode` picks the format from the extension (`.xml`, `.mjb`, `.txt`, `.mjz`) or from `content_type`. It returns the bytes written, or -1. See [model-editing](../../model-editing/SKILL.md).
- Long tail: `mj_loadTexture`, `mj_embedAssets` (copy with by-reference assets loaded), `mj_saveLastXML` (only for models from `mj_loadXML`), `mj_freeLastXML`, `mju_getXMLDependencies`.

## Main simulation

```C
void mj_step(const mjModel* m, mjData* d);
void mj_step1(const mjModel* m, mjData* d);
void mj_step2(const mjModel* m, mjData* d);
void mj_forward(const mjModel* m, mjData* d);
void mj_inverse(const mjModel* m, mjData* d);
void mj_forwardSkip(const mjModel* m, mjData* d, int skipstage, int skipsensor);
void mj_inverseSkip(const mjModel* m, mjData* d, int skipstage, int skipsensor);
```

- Set controls and applied forces (`mjData.{ctrl, qfrc_applied, xfrc_applied}`) before `mj_step`, or install `mjcb_control`. Alternatively, set them between `mj_step1` and `mj_step2`. **RK4 does not work with `mj_step1/2`.**
- `mj_forward` is `mj_step` without integration. Call it after loading or resetting, so that all of `mjData` is valid.
- `mj_inverse` writes `mjData.qfrc_inverse`. `qacc` must be set first. Use `mj_compareFwdInv` to check forward against inverse.
- `skipstage` is an `mjtStage`. For example, `mjSTAGE_POS` skips the position-dependent work when only `qvel` changed (finite differencing).
- See [simulation-loop](../../c-programming/simulation-loop/SKILL.md) and [physics-computation](../../physics-computation/SKILL.md).

## Initialization

```C
mjData* mj_makeData(const mjModel* m);
void mj_deleteData(mjData* d);
void mj_deleteModel(mjModel* m);
void mj_resetData(const mjModel* m, mjData* d);
void mj_resetDataKeyframe(const mjModel* m, mjData* d, int key);
mjModel* mj_copyModel(mjModel* dest, const mjModel* src);
mjData* mj_copyData(mjData* dest, const mjModel* m, const mjData* src);
mjModel* mj_loadModel(const char* filename, const mjVFS* vfs);
mjModel* mj_loadModelBuffer(const void* buffer, mjtSize buffer_sz);
void mj_saveModel(const mjModel* m, const char* filename, void* buffer, mjtSize buffer_sz);
mjSpec* mj_makeSpec(void);
mjSpec* mj_copySpec(const mjSpec* s);
void mj_deleteSpec(mjSpec* s);
void mj_setConst(mjModel* m, mjData* d);
```

- `mj_copyModel` allocates a new model if `dest` is NULL. `mj_loadModel` and `mj_saveModel` handle binary MJB; for `mj_saveModel` the buffer takes precedence. To make a hermetic MJB file, call `mj_embedAssets`, then `mj_saveModel`, then `mj_deleteModel`.
- `mj_resetDataKeyframe` loads keyframe `key` if `0 <= key < nkey`.
- `mj_setConst` sets the constant fields of `mjModel` for the `qpos0` configuration.
- Long tail: `mj_defaultLROpt`, `mj_defaultSolRefImp`, `mj_defaultOption`, `mj_defaultVisual`, `mj_sizeModel`, `mjv_copyData` (visualization-only copy, not valid for simulation), `mj_resetCtrl`, `mj_resetDataDebug`, `mj_markStack`, `mj_freeStack`, `mj_stackAllocByte`, `mj_stackAllocNum`, `mj_stackAllocInt`, `mj_resetCallbacks`, `mj_setLengthRange`, `mjs_activatePlugin`, `mjs_setDeepCopy`.

## Support

### State

```C
int mj_stateSize(const mjModel* m, int sig);
void mj_getState(const mjModel* m, const mjData* d, mjtNum* state, int sig);
void mj_setState(const mjModel* m, mjData* d, const mjtNum* state, int sig);
void mj_copyState(const mjModel* m, const mjData* src, mjData* dst, int sig);
void mj_extractState(const mjModel* m, const mjtNum* src, int srcsig,
                     mjtNum* dst, int dstsig);
```

The bits of `sig` are `mjtState` fields. An invalid `sig` fails with `mju_error`.

### Jacobians and inertia

```C
void mj_jac(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr,
            const mjtNum point[3], int body);
void mj_jacBody(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr, int body);
void mj_jacBodyCom(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr, int body);
void mj_jacSubtreeCom(const mjModel* m, mjData* d, mjtNum* jacp, int body);
void mj_jacGeom(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr, int geom);
void mj_jacSite(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr, int site);
void mj_jacPointAxis(const mjModel* m, mjData* d, mjtNum* jacPoint, mjtNum* jacAxis,
                     const mjtNum point[3], const mjtNum axis[3], int body);
void mj_jacDot(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr,
               const mjtNum point[3], int body);
void mj_fullM(const mjModel* m, const mjData* d, mjtNum* dst);
void mj_mulM(const mjModel* m, const mjData* d, mjtNum* res, const mjtNum* vec);
```

- `jacp` and `jacr` are each `3 x nv`. Pass NULL to skip either one. `point` is in world coordinates and treated as attached to `body`. The frame is centered at the body CoM and aligned with the world frame.
- Call `mj_kinematics` and then `mj_comPos` first, so the Jacobian matches the current `qpos`. `mj_jacDot` also needs `mj_comVel`.
- `mj_fullM` converts the sparse inertia matrix to dense.

### Names, forces, kinematics

```C
int mj_name2id(const mjModel* m, int type, const char* name);
const char* mj_id2name(const mjModel* m, int type, int id);
void mj_contactForce(const mjModel* m, const mjData* d, int id, mjtNum result[6]);
void mj_applyFT(const mjModel* m, mjData* d, const mjtNum force[3], const mjtNum torque[3],
                const mjtNum point[3], int body, mjtNum* qfrc_target);
void mj_objectVelocity(const mjModel* m, const mjData* d,
                       int objtype, int objid, mjtNum res[6], int flg_local);
void mj_objectAcceleration(const mjModel* m, const mjData* d,
                           int objtype, int objid, mjtNum res[6], int flg_local);
mjtNum mj_geomDistance(const mjModel* m, mjData* d, int geom1, int geom2, mjtNum distmax,
                       mjtNum fromto[6]);
void mj_differentiatePos(const mjModel* m, mjtNum* qvel, mjtNum dt,
                         const mjtNum* qpos1, const mjtNum* qpos2);
void mj_integratePos(const mjModel* m, mjtNum* qpos, const mjtNum* qvel, mjtNum dt);
```

- `type` is an `mjtObj`. `mj_name2id` returns -1 and `mj_id2name` returns NULL when nothing is found.
- `mj_contactForce` gives the 6D force:torque of contact `id` in the contact frame.
- `mj_applyFT` adds a Cartesian force and torque at a point on a body to `qfrc_target`, which is usually `d->qfrc_applied`.
- `mj_objectVelocity` and `mj_objectAcceleration` return 6D (rot:lin) values in an object-centered frame, with world or local orientation. Without acceleration or force sensors, call `mj_rnePostConstraint` first to compute `cacc`.
- `mj_geomDistance` returns the smallest signed distance, capped at `distmax`. If nothing is closer, `fromto` is zeroed. Distances are inaccurate with the legacy CCD pipeline.
- `mj_differentiatePos` maps `nq`-sized inputs to an `nv`-sized output while respecting quaternions. `mj_integratePos` is the inverse.
- Long tail: `mj_readCtrl` / `mj_readSensor` (read at a time through delay buffers; `interp` 0 hold, 1 linear, 2 Catmull-Rom, -1 use the element's value), `mj_initCtrlHistory`, `mj_initSensorHistory`, `mj_setKeyframe`, `mj_addContact`, `mj_isPyramidal`, `mj_isSparse`, `mj_isDual`, `mj_mulJacVec`, `mj_mulJacTVec`, `mj_angmomMat`, `mj_actuatorInputName`, `mj_mulM2`, `mj_addM`, `mj_insideSite`, `mj_normalizeQuat`, `mj_local2Global`, `mj_getTotalmass`, `mj_setTotalmass`, `mj_getPluginConfig`, `mj_loadPluginLibrary`, `mj_loadAllPluginLibraries`, `mj_version` (returns the same encoding as `mjVERSION_HEADER`, `(S * 1e6) + (M * 1e3) + P`, per [api-globals](../api-globals/SKILL.md); its own docstring still says the outdated "1.0.2 is encoded as 102"), `mj_versionString`.

## Pipeline components and sub components

The engine calls these from `mj_step`, `mj_forward` and `mj_inverse`. Users rarely need them. They all take `(const mjModel* m, mjData* d)` unless noted.

- **Components:** `mj_fwdKinematics`, `mj_fwdPosition`, `mj_fwdVelocity`, `mj_fwdActuation`, `mj_fwdAcceleration`, `mj_fwdConstraint`, `mj_Euler`, `mj_RungeKutta` (`int N`), `mj_implicit`, `mj_invPosition`, `mj_invVelocity`, `mj_invConstraint`, `mj_compareFwdInv`.
- **Sub components:** `mj_sensorPos`, `mj_sensorVel`, `mj_sensorAcc`, `mj_energyPos`, `mj_energyVel`, `mj_checkPos`, `mj_checkVel`, `mj_checkAcc`, `mj_kinematics`, `mj_comPos`, `mj_camlight`, `mj_flex`, `mj_tendon`, `mj_transmission`, `mj_crb`, `mj_makeM`, `mj_factorM`, `mj_solveM`, `mj_solveM2`, `mj_comVel`, `mj_passive`, `mj_subtreeVel`, `mj_rne`, `mj_rnePostConstraint`, `mj_maxContact`, `mj_collision`, `mj_makeConstraint`, `mj_island`, `mj_projectConstraint`, `mj_referenceConstraint`, `mj_constraintUpdate`.

```C
void mj_rne(const mjModel* m, mjData* d, int flg_acc, mjtNum* result);
void mj_solveM(const mjModel* m, mjData* d, mjtNum* x, const mjtNum* y, int n);
```

- `mj_rne` computes M(q)·qacc + C(q,qvel). `flg_acc=0` drops the inertial term.
- `mj_rnePostConstraint` fills `cacc`, `cfrc_int` and `cfrc_ext`.

## Ray casting

```C
mjtNum mj_ray(const mjModel* m, const mjData* d, const mjtNum pnt[3], const mjtNum vec[3],
              const mjtByte* geomgroup, mjtBool flg_static, int bodyexclude,
              int geomid[1], mjtNum normal[3]);
void mj_multiRay(const mjModel* m, mjData* d, const mjtNum pnt[3], const mjtNum* vec,
                 const mjtByte* geomgroup, mjtBool flg_static, int bodyexclude,
                 int* geomid, mjtNum* dist, mjtNum* normal, int nray, mjtNum cutoff);
```

- These return the distance `x` along `pnt + x*vec`, or -1 if there is no hit. Call them after `mj_kinematics` (or a function that calls it, such as `mj_fwdPosition`).
- `geomgroup` has length `mjNGROUP`, where 1 means include; NULL means no group filter. `flg_static=0` excludes static geoms. `bodyexclude=-1` includes all bodies. `geomid` gets -1 if there is no hit. `normal` always points out of the geometry.
- `mj_multiRay` ignores geoms beyond `cutoff`.
- Long tail: `mj_rayHfield`, `mj_rayMesh`, `mju_rayGeom`, `mj_rayFlex`, `mju_raySkin`.

## Printing, VFS, asset cache, resources

- **Printing:** `mj_printModel`, `mj_printFormattedModel`, `mj_printData`, `mj_printFormattedData`, `mju_printMat`, `mju_printMatSparse`, `mj_printSchema`, `mj_printScene`, `mj_printFormattedScene`.
- **VFS:** allocate with `mj_defaultVFS` and free with `mj_deleteVFS`. Pass the VFS to `mj_loadXML` / `mj_loadModel`, which check it before the disk.

```C
void mj_defaultVFS(mjVFS* vfs);
int mj_addFileVFS(mjVFS* vfs, const char* directory, const char* filename);
int mj_addBufferVFS(mjVFS* vfs, const char* name, const void* buffer, int nbuffer);
int mj_deleteFileVFS(mjVFS* vfs, const char* filename);
void mj_deleteVFS(mjVFS* vfs);
```

- VFS return codes: the add functions return 0 on success, 2 on a repeated name and -1 on failure. `mj_deleteFileVFS` returns 0 on success and -1 if the file is not found. Also: `mj_mountVFS`, `mj_unmountVFS`, `mj_containsBufferVFS`, `mj_containsFileVFS`.
- **Asset cache:** `mj_getCache`, `mj_getCacheSize`, `mj_getCacheCapacity`, `mj_setCacheCapacity` (0 disables), `mj_clearCache`.
- **Resources:** `mju_openResource`, `mju_closeResource`, `mju_readResource`, `mju_writeResource`, `mju_getResourceDir`, `mju_isModifiedResource`, `mju_decodeResource`. See [engine-plugins](../../c-programming/engine-plugins/SKILL.md).

## Errors, logging, memory

```C
void mju_error(const char* msg, ...) mjPRINTFLIKE(1, 2);
void mju_warning(const char* msg, ...) mjPRINTFLIKE(1, 2);
mjfLogHandler mju_setLogHandler(mjfLogHandler handler);
void* mju_malloc(size_t size);
void mju_free(void* ptr);
const char* mjs_getError(mjSpec* s);
int mjs_numWarnings(const mjSpec* spec);
const char* mjs_getWarning(const mjSpec* spec, int index);
```

- `mju_error` is always fatal. If the handler returns, the process exits with `exit(EXIT_FAILURE)`. To recover, a handler must `longjmp` or otherwise transfer control.
- `mju_setLogHandler` returns the previous handler, which is never NULL. Passing NULL restores the default handler.
- Long tail: `mju_clearHandlers`, `mju_getLogConfig`, `mju_setLogConfig`, `mju_info`, `mju_message`, `mj_warning`, `mju_writeLog`, `mjs_getTimer`, `mjs_isWarning` (deprecated: use `mjs_numWarnings(s) > 0`).
- **Miscellaneous:** `mju_muscleGain`, `mju_muscleBias`, `mju_muscleDynamics`, `mju_encodePyramid`, `mju_decodePyramid`, `mju_springDamper`, `mju_min`, `mju_max`, `mju_clip`, `mju_sign`, `mju_round`, `mju_type2Str`, `mju_str2Type`, `mju_writeNumBytes`, `mju_warningText`, `mju_isBad`, `mju_isZero`, `mju_standardNormal`, `mju_f2n`, `mju_n2f`, `mju_d2n`, `mju_n2d`, `mju_insertionSort`, `mju_insertionSortInt`, `mju_Halton`, `mju_strncpy`, `mju_sigmoid`.

## Visualization, rendering, UI

```C
void mjv_defaultCamera(mjvCamera* cam);
void mjv_defaultOption(mjvOption* opt);
void mjv_defaultScene(mjvScene* scn);
void mjv_makeScene(const mjModel* m, mjvScene* scn, int maxgeom);
void mjv_freeScene(mjvScene* scn);
void mjv_updateScene(const mjModel* m, mjData* d, const mjvOption* opt,
                     const mjvPerturb* pert, mjvCamera* cam, int catmask, mjvScene* scn);
void mjv_moveCamera(const mjModel* m, int action, mjtNum reldx, mjtNum reldy, mjvCamera* cam);
void mjr_defaultContext(mjrContext* con);
void mjr_makeContext(const mjModel* m, mjrContext* con, int fontscale);
void mjr_freeContext(mjrContext* con);
void mjr_setBuffer(int framebuffer, mjrContext* con);
void mjr_render(mjrRect viewport, mjvScene* scn, const mjrContext* con);
void mjr_readPixels(unsigned char* rgb, float* depth,
                    mjrRect viewport, const mjrContext* con);
```

- `mjr_setBuffer` takes `mjFB_WINDOW` or `mjFB_OFFSCREEN`. `fontscale` is an `mjtFontScale` and `action` is an `mjtMouse`.
- **Interaction (long tail):** `mjv_defaultFreeCamera`, `mjv_defaultPerturb`, `mjv_room2model`, `mjv_model2room`, `mjv_cameraInModel`, `mjv_cameraInRoom`, `mjv_frustumHeight`, `mjv_alignToCamera`, `mjv_movePerturb`, `mjv_moveModel`, `mjv_initPerturb`, `mjv_applyPerturbPose`, `mjv_applyPerturbForce`, `mjv_averageCamera`, `mjv_camera2GLCamera`, `mjv_select` (returns the geom id under a 2D point, or -1).
- **Visualization:** `mjv_defaultFigure`, `mjv_initGeom`, `mjv_connector`, `mjv_copyModel`, `mjv_addGeoms`, `mjv_makeLights`, `mjv_updateCamera`, `mjv_updateSkin`, `mjv_cameraFrame`, `mjv_cameraFrustum`.
- **OpenGL:** `mjr_defaultRendererInfo`, `mjr_getRendererInfo`, `mjr_changeFont`, `mjr_addAux`, `mjr_resizeOffscreen`, `mjr_uploadTexture`, `mjr_uploadMesh`, `mjr_uploadHField`, `mjr_restoreBuffer`, `mjr_drawPixels`, `mjr_blitBuffer`, `mjr_setAux`, `mjr_blitAux`, `mjr_text`, `mjr_overlay`, `mjr_maxViewport`, `mjr_rectangle`, `mjr_label`, `mjr_figure`, `mjr_finish`, `mjr_getError`, `mjr_findRect`.
- **Filament (`mjrf_`):** `mjrf_defaultContextConfig`, `mjrf_createContext` / `mjrf_destroyContext`, `mjrf_getRendererInfo`, `mjrf_default*Opts` (Shadow, Material, Headlight, Skybox, Haze, Fog, Bloom, Vignette, Reflection, DepthOfField, Dithering, ColorGrading, Antialiasing, AmbientOcclusion, Render), `mjrf_modelRenderOpts`, `mjrf_defaultRenderRequest`, `mjrf_defaultReadRequest`, `mjrf_render` (asynchronous: submit render and read requests in the same call, grouped by target), `mjrf_waitForFrame`, `mjrf_flush`, `mjrf_setClearColor`, `mjrf_defaultFrameStats` / `mjrf_getFrameStats`. Texture, mesh, scene, light, renderable and render target objects each have `mjrf_default*`, `mjrf_create*` and `mjrf_destroy*` functions plus setters (`mjrf_uploadTexture`, `mjrf_uploadMesh`, `mjrf_addSceneLight`, `mjrf_addSceneRenderable`, `mjrf_configureSceneFromModel`, `mjrf_setLight*`, `mjrf_setRenderable*`, `mjrf_resizeRenderTarget`, ...).
- **UI:** `mjui_themeSpacing`, `mjui_themeColor`, `mjui_add` (the `mjuiDef` array ends with an item of type -1), `mjui_addToSection`, `mjui_resize`, `mjui_update` (-1 updates all sections or items), `mjui_event`, `mjui_render`.
- See [visualization-rendering](../../c-programming/visualization-rendering/SKILL.md).

## Derivatives

```C
void mjd_transitionFD(const mjModel* m, mjData* d, mjtNum eps, mjtBool flg_centered,
                      mjtNum* A, mjtNum* B, mjtNum* C, mjtNum* D);
void mjd_inverseFD(const mjModel* m, mjData* d, mjtNum eps, mjtBool flg_actuation,
                   mjtNum *DfDq, mjtNum *DfDv, mjtNum *DfDa,
                   mjtNum *DsDq, mjtNum *DsDv, mjtNum *DsDa,
                   mjtNum *DmDq);
void mjd_subQuat(const mjtNum qa[4], const mjtNum qb[4], mjtNum Da[9], mjtNum Db[9]);
void mjd_quatIntegrate(const mjtNum vel[3], mjtNum scale,
                       mjtNum Dquat[9], mjtNum Dvel[9], mjtNum Dscale[3]);
```

| `mjd_transitionFD` output | Jacobian | Dimension |
|----|----|----|
| `A` | ∂(next state)/∂state | `2*nv+na x 2*nv+na` |
| `B` | ∂(next state)/∂control | `2*nv+na x nu` |
| `C` | ∂sensor/∂state | `nsensordata x 2*nv+na` |
| `D` | ∂sensor/∂control | `nsensordata x nu` |

- All outputs are optional (NULL). `flg_centered` selects forward (0) or centered (1) differences.
- Neither function supports RK4 or sleeping (disable the `sleep` flag). `mjd_transitionFD` does not support delays. `mjd_inverseFD` does not support noslip.
- `mjd_inverseFD` outputs `DfDq`, `DfDv`, `DfDa` (`nv x nv`), `DsDq`, `DsDv`, `DsDa` (`nv x nsensordata`) and `DmDq` (`nv x nC`). They are transposed relative to the control-theory convention.
- Speed-up from the docs: call `mj_forward`, lower solver `iterations`, call `mjd_transitionFD`, then restore. For accuracy, set `tolerance` to 0.

## Signed distance functions, plugins, threads

- **SDF:** `mjc_getSDF`, `mjc_distance`, `mjc_gradient`.
- **Plugins:** `mjp_defaultPlugin`, `mjp_registerPlugin` (thread-safe; a non-identical plugin with the same name raises `mju_error`), `mjp_pluginCount`, `mjp_getPlugin`, `mjp_getPluginAtSlot`. Providers, decoders, encoders and archive providers: `mjp_defaultProvider`, `mjp_registerProvider`, `mjp_providerCount`, `mjp_findProvider`, `mjp_getProviderAtSlot`, `mjp_registerDecoder`, `mjp_defaultDecoder`, `mjp_findDecoder`, `mjp_registerEncoder`, `mjp_defaultEncoder`, `mjp_findEncoder`, `mjp_registerArchiveProvider`, `mjp_findArchiveProvider`, `mjp_archiveProviderCount`.
- **Threads:** `void mju_threadpool(mjData* d, int nthread);` creates a thread pool with `nthread` workers.

## Batched simulation (`mujoco/mjbatch.h`)

```C
void mjb_defaultConfig(mjBatchConfig* config);
mjBatch* mjb_makeBatch(const mjModel* m, int nsim, const mjBatchConfig* config,
                       char* error, int error_sz);
void mjb_deleteBatch(mjBatch* b);
mjtNum* mjb_state(mjBatch* b);
int mjb_step(mjBatch* b, const int* ids, int nid, int nstep, int stage);
int mjb_forward(mjBatch* b, const int* ids, int nid, int stage);
int mjb_reset(mjBatch* b, const int* ids, int nid, const int* key, int stage);
int mjb_rollout(mjBatch* b, const int* ids, int nid, int nstep, const mjtNum* control,
                int control_spec, const mjBatchRecord* record, int nrecord);
int mjb_apply(mjBatch* b, const int* ids, int nid, mjfBatchFunc func, void* arg,
              int save);
```

- `ids` holds `nid` sorted, unique indices. NULL selects all simulations.
- The run functions return the number of simulations that raised an error. Those keep their prior state. Invalid arguments raise `mju_error` on the caller's thread.
- `mjb_state` returns `nsim x nstate` rows of integration state in `mj_getState` order. `stage` is an `mjtStage` (`mjSTAGE_NONE`, `_VEL`, `_ACC`).
- `config->persistent` keeps one `mjData` per simulation. Models with sleep or IPC enabled need it.
- Physics callbacks, plugins and `mjb_apply` functions must not call `mju_error` or throw.
- Long tail: `mjb_nstate`, `mjb_stateComponent`, `mjb_warning`, `mjb_status`, `mjb_error`, `mjb_output`, `mjb_expand`, `mjb_expanded`, `mjb_setConst`, `mjb_setModels`, `mjb_getModel`, `mjb_getData`, `mjb_nsim`, `mjb_nthread`, `mjb_persistent`, `mjb_model`. See [simulation-loop](../../c-programming/simulation-loop/SKILL.md).

## Math

- **Standard math macros:** `mju_sqrt`, `mju_exp`, `mju_sin`, `mju_cos`, `mju_tan`, `mju_asin`, `mju_acos`, `mju_atan2`, `mju_tanh`, `mju_pow`, `mju_abs` (= `fabs`), `mju_log`, `mju_log10`, `mju_floor`, `mju_ceil`.
- **Vector (3D/4D):** `mju_zero3`, `mju_copy3`, `mju_scl3`, `mju_add3`, `mju_sub3`, `mju_addTo3`, `mju_subFrom3`, `mju_addToScl3`, `mju_addScl3`, `mju_normalize3`, `mju_norm3`, `mju_dot3`, `mju_dist3`, `mju_mulMatVec3`, `mju_mulMatTVec3`, `mju_cross`, `mju_zero4`, `mju_unit4`, `mju_copy4`, `mju_normalize4`.
- **Vector/matrix (size `n`):** `mju_zero`, `mju_fill`, `mju_copy`, `mju_sum`, `mju_L1`, `mju_scl`, `mju_add`, `mju_sub`, `mju_addTo`, `mju_subFrom`, `mju_addToScl`, `mju_addScl`, `mju_normalize`, `mju_norm`, `mju_dot`, `mju_mulMatVec`, `mju_mulMatTVec`, `mju_mulVecMatVec`, `mju_transpose`, `mju_symmetrize`, `mju_eye`, `mju_mulMatMat`, `mju_mulMatMatT`, `mju_mulMatTMat`, `mju_sqrMatTD`, `mju_transformSpatial`.
- **Sparse:** `mju_dense2sparse`, `mju_sparse2dense`, `mju_sym2dense`.
- **Decompositions/solvers:** `mju_cholFactor`, `mju_cholSolve`, `mju_cholUpdate`, `mju_cholFactorBand`, `mju_cholSolveBand`, `mju_band2Dense`, `mju_dense2Band`, `mju_bandMulMatVec`, `mju_bandDiag`, `mju_eig3`, `mju_boxQP`, `mju_boxQPmalloc`, `mju_QP` (dual active-set QP).

```C
void mju_rotVecQuat(mjtNum res[3], const mjtNum vec[3], const mjtNum quat[4]);
void mju_negQuat(mjtNum res[4], const mjtNum quat[4]);
void mju_mulQuat(mjtNum res[4], const mjtNum quat1[4], const mjtNum quat2[4]);
void mju_mulQuatAxis(mjtNum res[4], const mjtNum quat[4], const mjtNum axis[3]);
void mju_axisAngle2Quat(mjtNum res[4], const mjtNum axis[3], mjtNum angle);
void mju_quat2Vel(mjtNum res[3], const mjtNum quat[4], mjtNum dt);
void mju_subQuat(mjtNum res[3], const mjtNum qa[4], const mjtNum qb[4]);
void mju_quat2Mat(mjtNum res[9], const mjtNum quat[4]);
void mju_mat2Quat(mjtNum quat[4], const mjtNum mat[9]);
void mju_derivQuat(mjtNum res[4], const mjtNum quat[4], const mjtNum vel[3]);
void mju_quatIntegrate(mjtNum quat[4], const mjtNum vel[3], mjtNum scale);
void mju_quatZ2Vec(mjtNum quat[4], const mjtNum vec[3]);
int mju_mat2Rot(mjtNum quat[4], const mjtNum mat[9]);
void mju_euler2Quat(mjtNum quat[4], const mjtNum euler[3], const char* seq);
void mju_mulPose(mjtNum posres[3], mjtNum quatres[4],
                 const mjtNum pos1[3], const mjtNum quat1[4],
                 const mjtNum pos2[3], const mjtNum quat2[4]);
void mju_negPose(mjtNum posres[3], mjtNum quatres[4],
                 const mjtNum pos[3], const mjtNum quat[4]);
void mju_trnVecPose(mjtNum res[3], const mjtNum pos[3], const mjtNum quat[4],
                    const mjtNum vec[3]);
```

- `mju_subQuat` gives the 3D velocity `res` with `qb*quat(res) = qa`. `mju_negQuat` is the conjugate (the opposite rotation).
- `mju_euler2Quat` takes radians. Each `seq[0,1,2]` is in `xyzXYZ`: lowercase means intrinsic and uppercase extrinsic.
- `mju_mat2Rot` extracts a rotation from an arbitrary 3x3 matrix by refining the input quaternion. It returns the iteration count.

## Model editing (`mjs_*`)

Task guide: [model-editing](../../model-editing/SKILL.md).

```C
mjsElement* mjs_attach(mjsElement* parent, const mjsElement* child,
                       const char* prefix, const char* suffix);
mjsBody* mjs_addBody(mjsBody* body, const mjsDefault* def);
mjsSite* mjs_addSite(mjsBody* body, const mjsDefault* def);
mjsJoint* mjs_addJoint(mjsBody* body, const mjsDefault* def);
mjsJoint* mjs_addFreeJoint(mjsBody* body);
mjsGeom* mjs_addGeom(mjsBody* body, const mjsDefault* def);
mjsCamera* mjs_addCamera(mjsBody* body, const mjsDefault* def);
mjsLight* mjs_addLight(mjsBody* body, const mjsDefault* def);
mjsFrame* mjs_addFrame(mjsBody* body, mjsFrame* parentframe);
int mjs_delete(mjSpec* spec, mjsElement* element);
mjsActuator* mjs_addActuator(mjSpec* s, const mjsDefault* def);
mjsSensor* mjs_addSensor(mjSpec* s);
mjsEquality* mjs_addEquality(mjSpec* s, const mjsDefault* def);
mjsExclude* mjs_addExclude(mjSpec* s);
mjsPair* mjs_addPair(mjSpec* s, const mjsDefault* def);
mjsTendon* mjs_addTendon(mjSpec* s, const mjsDefault* def);
mjsMesh* mjs_addMesh(mjSpec* s, const mjsDefault* def);
mjsDefault* mjs_addDefault(mjSpec* s, const char* classname, const mjsDefault* parent);
```

- `mjs_attach` returns the attached element, or NULL on failure.
- `def` may be NULL. `mjs_delete` returns 0 on success. Deleting a body or frame deletes its contents and every element that references a deleted element.
- **Other non-tree elements:** `mjs_addFlex`, `mjs_makeFlex` (creates a flexcomp; arguments mirror its attributes), `mjs_wrapSite`, `mjs_wrapGeom`, `mjs_wrapJoint`, `mjs_wrapPulley`, `mjs_addNumeric`, `mjs_addText`, `mjs_addTuple`, `mjs_addKey`, `mjs_addPlugin`.
- **Assets:** `mjs_addHField`, `mjs_addSkin`, `mjs_addTexture`, `mjs_addMaterial`, `mjs_makeMesh` (built-in procedural mesh of type `mjtMeshBuiltin`; returns 0 on success).
- **Actuator shortcuts** (return an error string, if any): `mjs_setToMotor`, `mjs_setToPosition`, `mjs_setToIntVelocity`, `mjs_setToVelocity`, `mjs_setToOrientation`, `mjs_setToPID`, `mjs_setToDamper`, `mjs_setToCylinder`, `mjs_setToMuscle`, `mjs_setToAdhesion`, `mjs_setToDCMotor`.

```C
const char* mjs_setToPosition(mjsActuator* actuator, double kp, double kv[1],
                              double dampratio[1], double timeconst[1], double inheritrange);
```

### Find and get

```C
mjSpec* mjs_getSpec(const mjsElement* element);
mjsBody* mjs_findBody(const mjSpec* s, const char* name);
mjsElement* mjs_findElement(const mjSpec* s, mjtObj type, const char* name);
mjsBody* mjs_findChild(const mjsBody* body, const char* name);
mjsBody* mjs_getParent(const mjsElement* element);
mjsFrame* mjs_findFrame(const mjSpec* s, const char* name);
mjsDefault* mjs_findDefault(const mjSpec* s, const char* classname);
int mjs_getId(const mjsElement* element);
mjsElement* mjs_firstChild(const mjsBody* body, mjtObj type, int recurse);
mjsElement* mjs_nextChild(const mjsBody* body, const mjsElement* child, int recurse);
mjsElement* mjs_firstElement(const mjSpec* s, mjtObj type);
mjsElement* mjs_nextElement(const mjSpec* s, const mjsElement* element);
```

- The `next*` functions return NULL after the last element. A nonzero `recurse` also searches the body's subtree.
- Long tail: `mjs_getOriginSpec` (does not change after attachment), `mjs_getCompiler`, `mjs_findSpec`, `mjs_getFrame`, `mjs_getDefault`, `mjs_getSpecDefault`, `mjs_getWrapTarget`, `mjs_getWrapSideSite`, `mjs_getWrapDivisor`, `mjs_getWrapCoef`.

### Attribute setters and getters

```C
int mjs_setName(mjsElement* element, const char* name);
void mjs_setString(mjString* dest, const char* text);
void mjs_setDouble(mjDoubleVec* dest, const double* array, int size);
mjString* mjs_getName(mjsElement* element);
const char* mjs_getString(const mjString* source);
const double* mjs_getDouble(const mjDoubleVec* source, int* size);
```

- Setters: `mjs_setBuffer`, `mjs_setStringVec`, `mjs_setInStringVec`, `mjs_appendString`, `mjs_setInt`, `mjs_appendIntVec`, `mjs_setFloat`, `mjs_appendFloatVec`, `mjs_setPluginAttributes`.
- Getters: `mjs_getInStringVec`, `mjs_getWrapNum`, `mjs_getWrap`, `mjs_getPluginAttributes`.

### Spec utilities, initialization, casting

- **Spec utilities:** `mjs_setDefault`, `mjs_setFrame`, `mjs_resolveOrientation`, `mjs_fuseStatic`, `mjs_discardVisual`, `mjs_dedupAssets`, `mjs_adoptInertial`, `mjs_bodyToFrame`, `mjs_setUserValue`, `mjs_setUserValueWithCleanup`, `mjs_getUserValue`, `mjs_deleteUserValue`, `mjs_sensorDim`. `mjs_fuseStatic`, `mjs_discardVisual` and `mjs_dedupAssets` return the number of changes, 0 if the spec is unchanged, or -1 on error (in which case nothing changes). Afterwards, pointers to removed elements are invalid.
- **Element initialization:** `void mjs_default<Type>(mjs<Type>* ...)` exists for Spec (`mjs_defaultSpec(mjSpec*)`), Orientation, Body, Frame, Joint, Geom, Site, Camera, Light, Flex, Mesh, HField, Skin, Texture, Material, Pair, Equality, Tendon, Actuator, Sensor, Numeric, Text, Tuple, Key and Plugin.
- **Element casting:** `mjs<Type>* mjs_as<Type>(mjsElement* element)` safely casts, or returns NULL on a type mismatch. It exists for Body, Geom, Joint, Site, Camera, Light, Frame, Actuator, Sensor, Flex, Pair, Equality, Exclude, Tendon, Numeric, Text, Tuple, Key, Mesh, HField, Skin, Texture, Material and Plugin.

## Pitfalls

- Do not use `mj_step1`/`mj_step2` with RK4.
- Before Jacobians or ray casts, run at least `mj_kinematics` (+ `mj_comPos` for Jacobians). After a reset, call `mj_forward`.
- A failed `mj_recompile` frees the model and data you passed in.
- `mjv_copyData` output cannot be simulated: its large arrays are NULL.
- `mj_freeStack` invalidates every `mj_stackAlloc*` pointer since the matching `mj_markStack`.
- Free `mju_boxQPmalloc` buffers with `mju_free`. `mj_loadTexture` allocates its buffer with `mju_malloc`, and the caller must free it.

## Source docs

Verbatim copies, for details not covered above:

- [APIreference/APIfunctions.md](references/APIreference-APIfunctions.md)
