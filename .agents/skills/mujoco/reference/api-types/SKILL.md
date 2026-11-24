---
name: api-types
description: 'MuJoCo C API types: primitive types, enums (mjtObj, mjtGeom, mjtJoint, mjtSolver, mjtCone, mjtDisableBit, mjtState, ...), structs (mjModel, mjData, mjOption, mjContact, mjSpec elements such as mjsBody, mjsGeom, mjsJoint, visualization and rendering structs) and function types. Use when the exact field name, array shape or enum value of a MuJoCo struct is needed, in C or through the Python bindings.'
---

# MuJoCo API Types

Look up the exact name, array shape or enum value of a MuJoCo C type:
primitive types, `mjt*` enums, the main structs (`mjModel`, `mjOption`,
`mjData`, `mjContact`), visualization structs, the `mjs*` model-editing
structs and callback function types. Field lines are copied verbatim from the
headers. For anything not shown, read the verbatim `APIreference/APItypes.md`
copy in the source docs. For using these structs from Python, see
[python-bindings](../../python-bindings/SKILL.md).

## Conventions

- Enums use the `mjt` prefix. The API takes and stores them as `int` (enum
  size is compiler-dependent); comments say which enum an int holds.
- Array comments end with the shape: `(nbody x 3)` is 3 values per body,
  `(njnt x mjNREF)` is `mjNREF` values per joint. `-1: none` marks absence.
- Constants such as `mjNREF`, `mjNIMP`, `mjNPOLY`, `mjNEQDATA`, `mjNGAIN`,
  `mjNBIAS`, `mjNDYN`, `mjNSENS`, `mjNGROUP` size arrays; their values are in
  [api-globals](../api-globals/SKILL.md).
- Struct prefixes: `mj` engine, `mjv` abstract visualization, `mjr` classic
  renderer, `mjrf` filament renderer, `mjui` UI, `mjs` model editing, `mjp` plugins.

## Primitive types (`mjtype.h`)

| Type | Definition |
|---|---|
| `mjtNum` | `double` by default; `float` if `mjUSESINGLE` is defined. Only the double build is distributed; never edit the shipped headers. `mjMINVAL` is `1E-15`. |
| `mjtByte` | `typedef unsigned char mjtByte;` |
| `mjtBool` | `_Bool` in C, `bool` in C++ |
| `mjtSize` | `typedef int64_t mjtSize;` (buffer sizes; all `mjModel` sizes) |

## Model enums (`mjtype.h`)

Sequential enums start at 0 unless a value is shown.

| Enum (used in) | Values |
|---|---|
| `mjtDisableBit` (`opt.disableflags`) | bits `1<<0` to `1<<19` in this order: `mjDSBL_CONSTRAINT` (entire constraint solver), `mjDSBL_EQUALITY`, `mjDSBL_FRICTIONLOSS`, `mjDSBL_LIMIT`, `mjDSBL_CONTACT`, `mjDSBL_SPRING`, `mjDSBL_DAMPER`, `mjDSBL_GRAVITY`, `mjDSBL_CLAMPCTRL`, `mjDSBL_WARMSTART`, `mjDSBL_FILTERPARENT` (remove collisions with parent body), `mjDSBL_ACTUATION`, `mjDSBL_REFSAFE` (make ref[0]>=2*timestep), `mjDSBL_SENSOR`, `mjDSBL_MIDPHASE`, `mjDSBL_EULERDAMP` (implicit joint damping in Euler), `mjDSBL_AUTORESET`, `mjDSBL_NATIVECCD`, `mjDSBL_ISLAND`, `mjDSBL_MULTICCD` (multiple CCD contact points); `mjNDISABLE` = 20 |
| `mjtEnableBit` (`opt.enableflags`) | bits `1<<0` to `1<<7`: `mjENBL_OVERRIDE` (override contact parameters), `mjENBL_ENERGY`, `mjENBL_FWDINV` (record solver statistics), `mjENBL_INVDISCRETE` (discrete-time inverse dynamics), `mjENBL_SLEEP`, `mjENBL_DIAGEXACT` (exact diagonal of constraint inertia), `mjENBL_IPC` (IPC flex contact mode of the discrete integrator), `mjENBL_SPECULATIVE`; `mjNENABLE` = 8 |
| `mjtObj` (`mj_name2id`, `mj_id2name`) | `mjOBJ_UNKNOWN`, `mjOBJ_BODY`, `mjOBJ_XBODY` (body, regular frame instead of i-frame), `mjOBJ_JOINT`, `mjOBJ_DOF`, `mjOBJ_GEOM`, `mjOBJ_SITE`, `mjOBJ_CAMERA`, `mjOBJ_LIGHT`, `mjOBJ_FLEX`, `mjOBJ_MESH`, `mjOBJ_SKIN`, `mjOBJ_HFIELD`, `mjOBJ_TEXTURE`, `mjOBJ_MATERIAL`, `mjOBJ_PAIR`, `mjOBJ_EXCLUDE`, `mjOBJ_EQUALITY`, `mjOBJ_TENDON`, `mjOBJ_ACTUATOR`, `mjOBJ_SENSOR`, `mjOBJ_NUMERIC`, `mjOBJ_TEXT`, `mjOBJ_TUPLE`, `mjOBJ_KEY`, `mjOBJ_PLUGIN`, `mjNOBJECT`; meta elements (not in mjModel) from 100: `mjOBJ_FRAME`, `mjOBJ_DEFAULT`, `mjOBJ_MODEL` |
| `mjtJoint` (`jnt_type`) | `mjJNT_FREE` (7 qpos), `mjJNT_BALL` (4), `mjJNT_SLIDE` (1), `mjJNT_HINGE` (1). Ball and free rotations are unit quaternions: 4 coordinates, 3 dofs. |
| `mjtGeom` (`geom_type`, `site_type`) | `mjGEOM_PLANE`, `mjGEOM_HFIELD`, `mjGEOM_SPHERE`, `mjGEOM_CAPSULE`, `mjGEOM_ELLIPSOID`, `mjGEOM_CYLINDER`, `mjGEOM_BOX`, `mjGEOM_MESH`, `mjGEOM_SDF`, `mjNGEOMTYPES`; rendering-only from 100: `mjGEOM_ARROW`, `mjGEOM_ARROW1`, `mjGEOM_ARROW2`, `mjGEOM_LINE`, `mjGEOM_LINEBOX`, `mjGEOM_FLEX`, `mjGEOM_SKIN`, `mjGEOM_LABEL`, `mjGEOM_TRIANGLE`, `mjGEOM_DISC`; `mjGEOM_NONE` = 1001 |
| `mjtProjection` (`cam_projection`) | `mjPROJ_PERSPECTIVE`, `mjPROJ_ORTHOGRAPHIC` |
| `mjtCamLight` (`cam_mode`, `light_mode`) | `mjCAMLIGHT_FIXED`, `mjCAMLIGHT_TRACK`, `mjCAMLIGHT_TRACKCOM`, `mjCAMLIGHT_TARGETBODY`, `mjCAMLIGHT_TARGETBODYCOM` |
| `mjtLightType` (`light_type`) | `mjLIGHT_SPOT`, `mjLIGHT_DIRECTIONAL`, `mjLIGHT_POINT`, `mjLIGHT_IMAGE` |
| `mjtTexture` (`tex_type`) | `mjTEXTURE_2D`, `mjTEXTURE_CUBE`, `mjTEXTURE_SKYBOX` |
| `mjtTextureRole` (index into `mat_texid`) | `mjTEXROLE_USER`, `_RGB`, `_OCCLUSION`, `_ROUGHNESS`, `_METALLIC`, `_NORMAL`, `_OPACITY`, `_EMISSIVE`, `_RGBA`, `_ORM`, `mjNTEXROLE` |
| `mjtColorSpace` | `mjCOLORSPACE_AUTO`, `mjCOLORSPACE_LINEAR`, `mjCOLORSPACE_SRGB` |
| `mjtIntegrator` (`opt.integrator`) | `mjINT_EULER`, `mjINT_RK4`, `mjINT_IMPLICIT`, `mjINT_IMPLICITFAST`, `mjINT_DISCRETE` |
| `mjtCone` / `mjtJacobian` (`opt.cone` / `opt.jacobian`) | `mjCONE_PYRAMIDAL`, `mjCONE_ELLIPTIC` / `mjJAC_DENSE`, `mjJAC_SPARSE`, `mjJAC_AUTO` (dense if nv<60) |
| `mjtSolver` (`opt.solver`) | `mjSOL_PGS` (dual), `mjSOL_CG` (primal), `mjSOL_NEWTON` (primal) |
| `mjtEq` (`eq_type`) | `mjEQ_CONNECT`, `mjEQ_WELD`, `mjEQ_JOINT`, `mjEQ_TENDON`, `mjEQ_FLEX`, `mjEQ_FLEXVERT` (unsupported), `mjEQ_FLEXSTRAIN`, `mjEQ_DISTANCE` (unsupported) |
| `mjtTendon` / `mjtWrap` (`tendon_type` / `wrap_type`) | `mjTENDON_FIXED`, `mjTENDON_SPATIAL` / `mjWRAP_NONE`, `mjWRAP_JOINT`, `mjWRAP_PULLEY`, `mjWRAP_SITE`, `mjWRAP_SPHERE`, `mjWRAP_CYLINDER` |
| `mjtTrn` (`actuator_trntype`) | `mjTRN_JOINT`, `mjTRN_JOINTINPARENT`, `mjTRN_SLIDERCRANK`, `mjTRN_TENDON`, `mjTRN_SITE`, `mjTRN_BODY`, `mjTRN_SO3`; `mjTRN_UNDEFINED` = 1000 |
| `mjtDyn` (`actuator_dyntype`) | `mjDYN_NONE`, `mjDYN_INTEGRATOR`, `mjDYN_FILTER`, `mjDYN_FILTEREXACT`, `mjDYN_MUSCLE`, `mjDYN_DCMOTOR`, `mjDYN_PID`, `mjDYN_USER` |
| `mjtGain` (`actuator_gaintype`) | `mjGAIN_FIXED`, `mjGAIN_AFFINE`, `mjGAIN_MUSCLE`, `mjGAIN_DCMOTOR`, `mjGAIN_SO3`, `mjGAIN_PID`, `mjGAIN_USER` |
| `mjtBias` (`actuator_biastype`) | `mjBIAS_NONE`, `mjBIAS_AFFINE`, `mjBIAS_MUSCLE`, `mjBIAS_DCMOTOR`, `mjBIAS_SO3`, `mjBIAS_USER` |
| `mjtCtrlChart` / `mjtCtrlInput` (`actuator_ctrlspec`) | `mjCHART_EXPMAP` = 1 (3 controls), `mjCHART_QUAT` = 2 (4 controls) / bits `mjINPUT_POS` = 1, `_VEL` = 2, `_FF` = 4, `_VOLTAGE` = 8, `_NONE` = 16, `_PRESSURE` = 32 |
| `mjtStage` (`mj_forwardSkip`, `mj_inverseSkip`) | `mjSTAGE_NONE`, `mjSTAGE_POS`, `mjSTAGE_VEL`, `mjSTAGE_ACC` |
| `mjtDataType` (`sensor_datatype`) | `mjDATATYPE_REAL`, `mjDATATYPE_POSITIVE`, `mjDATATYPE_AXIS`, `mjDATATYPE_QUATERNION` |
| `mjtConDataField` / `mjtRayDataField` (contact / rangefinder sensor) | `mjCONDATA_FOUND`, `_FORCE`, `_TORQUE`, `_DIST`, `_POS`, `_NORMAL`, `_TANGENT`, `_LINVEL`, `_ANGVEL`, `mjNCONDATA` / `mjRAYDATA_DIST`, `_DIR`, `_ORIGIN`, `_POINT`, `_NORMAL`, `_DEPTH`, `mjNRAYDATA` |
| `mjtCamOutBit` (`cam_output`) | `mjCAMOUT_RGB` = 1<<0, `_DEPTH` = 1<<1, `_DIST` = 1<<2, `_NORMAL` = 1<<3, `_SEG` = 1<<4; `mjNCAMOUT` = 5 |
| `mjtSameFrame` | `mjSAMEFRAME_NONE`, `_BODY`, `_INERTIA`, `_BODYROT`, `_INERTIAROT` |
| `mjtSleepPolicy` (`tree_sleep_policy`) | `mjSLEEP_AUTO`, `mjSLEEP_AUTO_NEVER`, `mjSLEEP_AUTO_ALLOWED`, `mjSLEEP_NEVER`, `mjSLEEP_ALLOWED`, `mjSLEEP_INIT` (user only) |
| `mjtLRMode` (`mjLROpt.mode`) | `mjLRMODE_NONE`, `mjLRMODE_MUSCLE`, `mjLRMODE_MUSCLEUSER`, `mjLRMODE_ALL` |
| `mjtFlexSelf` / `mjtSDFType` | `mjFLEXSELF_NONE`, `_NARROW`, `_BVH`, `_SAP`, `_AUTO` / `mjSDFTYPE_SINGLE`, `_INTERSECTION`, `_MIDSURFACE`, `_COLLISION` |

`mjtSensor` (`sensor_type`), in order: site-attached `mjSENS_TOUCH`,
`_ACCELEROMETER`, `_VELOCIMETER`, `_GYRO`, `_FORCE`, `_TORQUE`, `_MAGNETOMETER`,
`_RANGEFINDER`, `_CAMPROJECTION`; scalar `_JOINTPOS`, `_JOINTVEL`, `_TENDONPOS`,
`_TENDONVEL`, `_ACTUATORPOS`, `_ACTUATORVEL`, `_ACTUATORFRC`, `_JOINTACTFRC`,
`_TENDONACTFRC`; ball `_BALLQUAT`, `_BALLANGVEL`; limits `_JOINTLIMITPOS`,
`_JOINTLIMITVEL`, `_JOINTLIMITFRC`, `_TENDONLIMITPOS`, `_TENDONLIMITVEL`,
`_TENDONLIMITFRC`; frame ((x)body, geom, site, camera) `_FRAMEPOS`, `_FRAMEQUAT`,
`_FRAMEXAXIS`, `_FRAMEYAXIS`, `_FRAMEZAXIS`, `_FRAMELINVEL`, `_FRAMEANGVEL`,
`_FRAMELINACC`, `_FRAMEANGACC`; subtree `_SUBTREECOM`, `_SUBTREELINVEL`,
`_SUBTREEANGMOM`; geometric `_INSIDESITE`, `_GEOMDIST`, `_GEOMNORMAL`,
`_GEOMFROMTO`; `_CONTACT`; global `_E_POTENTIAL`, `_E_KINETIC`, `_CLOCK`;
`_TACTILE` (SDF); `_PLUGIN`; `mjSENS_USER` (filled by `mjcb_sensor`).

## Data enums (`mjtype.h`)

`mjtState` (for `mj_getState`, `mj_setState`, `mj_stateSize`), bits 0..14 in
order, `mjNSTATE` = 15: `mjSTATE_TIME`, `mjSTATE_QPOS`, `mjSTATE_QVEL`,
`mjSTATE_ACT`, `mjSTATE_HISTORY`, `mjSTATE_WARMSTART`, `mjSTATE_CTRL`,
`mjSTATE_QFRC_APPLIED`, `mjSTATE_XFRC_APPLIED`, `mjSTATE_EQ_ACTIVE`,
`mjSTATE_MOCAP_POS`, `mjSTATE_MOCAP_QUAT`, `mjSTATE_USERDATA`,
`mjSTATE_PLUGIN`, `mjSTATE_PLASTIC`. Combinations:

```c
  mjSTATE_PHYSICS        = mjSTATE_QPOS | mjSTATE_QVEL | mjSTATE_ACT | mjSTATE_HISTORY |
                           mjSTATE_PLASTIC,
  mjSTATE_FULLPHYSICS    = mjSTATE_TIME | mjSTATE_PHYSICS | mjSTATE_PLUGIN,
  mjSTATE_USER           = mjSTATE_CTRL | mjSTATE_QFRC_APPLIED | mjSTATE_XFRC_APPLIED |
                           mjSTATE_EQ_ACTIVE | mjSTATE_MOCAP_POS | mjSTATE_MOCAP_QUAT |
                           mjSTATE_USERDATA,
  mjSTATE_INTEGRATION    = mjSTATE_FULLPHYSICS | mjSTATE_USER | mjSTATE_WARMSTART
```

| Enum | Values |
|---|---|
| `mjtConstraint` (`d->efc_type`) | `mjCNSTR_EQUALITY`, `mjCNSTR_FRICTION_DOF`, `mjCNSTR_FRICTION_TENDON`, `mjCNSTR_LIMIT_JOINT`, `mjCNSTR_LIMIT_TENDON`, `mjCNSTR_CONTACT_FRICTIONLESS`, `mjCNSTR_CONTACT_PYRAMIDAL`, `mjCNSTR_CONTACT_ELLIPTIC` |
| `mjtConstraintState` (`efc_state`) | `mjCNSTRSTATE_SATISFIED`, `_QUADRATIC`, `_LINEARNEG`, `_LINEARPOS`, `_CONE` |
| `mjtWarning` (index of `d->warning`) | `mjWARN_INERTIA`, `mjWARN_CONTACTFULL`, `mjWARN_CNSTRFULL`, `mjWARN_BADQPOS`, `mjWARN_BADQVEL`, `mjWARN_BADQACC`, `mjWARN_BADCTRL`, `mjNWARNING` |
| `mjtTimer` (index of `d->timer`) | `mjTIMER_STEP`, `_FORWARD`, `_INVERSE`, `_POSITION`, `_VELOCITY`, `_ACTUATION`, `_CONSTRAINT`, `_ADVANCE`, `_POS_KINEMATICS`, `_POS_INERTIA`, `_POS_COLLISION`, `_POS_MAKE`, `_POS_PROJECT`, `_COL_BROAD`, `_COL_NARROW`, `mjNTIMER` |
| `mjtSleepState` (`body_awake`) | `mjS_STATIC` = -1, `mjS_ASLEEP` = 0, `mjS_AWAKE` = 1 |
| `mjtLogLevel` / `mjtLogTopic` | `mjLOG_DEBUG`, `mjLOG_INFO`, `mjLOG_WARNING`, `mjLOG_ERROR` / `mjTOPIC_NONE` = 0 (always passes), `mjTOPIC_TIME_STP` = 1, `mjTOPIC_TIME_CMP` = 2, `mjTOPIC_SLEEP` = 3; `mjNTOPIC` = 3. Bitmask for topic `t` is `(1 << (t - 1))`. |

## Visualization, rendering and UI enums

| Enum (used in) | Values |
|---|---|
| `mjtCatBit` (`mjr_render` mask) | `mjCAT_STATIC` = 1, `mjCAT_DYNAMIC` = 2, `mjCAT_DECOR` = 4, `mjCAT_ALL` = 7 |
| `mjtMouse` | `mjMOUSE_NONE`, `_ROTATE_V`, `_ROTATE_H`, `_MOVE_V`, `_MOVE_H`, `_ZOOM`, `_MOVE_V_REL`, `_MOVE_H_REL`, `_TURN_V`, `_TURN_H` |
| `mjtCamera` (`mjvCamera.type`) | `mjCAMERA_FREE`, `mjCAMERA_TRACKING` (uses `trackbodyid`), `mjCAMERA_FIXED` (uses `fixedcamid`), `mjCAMERA_USER` |
| `mjtLabel` (`mjvOption.label`) | `mjLABEL_NONE`, `_BODY`, `_JOINT`, `_GEOM`, `_SITE`, `_CAMERA`, `_LIGHT`, `_TENDON`, `_ACTUATOR`, `_CONSTRAINT`, `_FLEX`, `_SKIN`, `_SELECTION`, `_SELPNT`, `_CONTACTPOINT`, `_CONTACTFORCE`, `_ISLAND`, `mjNLABEL` |
| `mjtFrame` (`mjvOption.frame`) | `mjFRAME_NONE`, `_BODY`, `_GEOM`, `_SITE`, `_CAMERA`, `_LIGHT`, `_CONTACT`, `_WORLD`, `mjNFRAME` |
| `mjtVisFlag` (index of `mjvOption.flags`) | `mjVIS_CONVEXHULL`, `_TEXTURE`, `_JOINT`, `_CAMERA`, `_ACTUATOR`, `_ACTIVATION`, `_LIGHT`, `_TENDON`, `_RANGEFINDER`, `_CONSTRAINT`, `_INERTIA`, `_SCLINERTIA`, `_PERTFORCE`, `_PERTOBJ`, `_CONTACTPOINT`, `_ISLAND`, `_CONTACTFORCE`, `_CONTACTSPLIT`, `_TRANSPARENT`, `_AUTOCONNECT`, `_COM`, `_SELECT`, `_STATIC`, `_SKIN`, `_FLEXVERT`, `_FLEXEDGE`, `_FLEXFACE`, `_FLEXSKIN`, `_BODYBVH`, `_MESHBVH`, `_SDFITER`, `mjNVISFLAG` |
| `mjtRndFlag` (index of `mjvScene.flags`) | `mjRND_SHADOW`, `_WIREFRAME`, `_REFLECTION`, `_ADDITIVE`, `_SKYBOX`, `_FOG`, `_HAZE`, `_DEPTH`, `_SEGMENT`, `_IDCOLOR`, `_CULL_FACE`, `_POST_PROCESSING`, `mjNRNDFLAG` |
| `mjtStereo` / `mjtPertBit` (`mjvScene.stereo` / `mjvPerturb.active`) | `mjSTEREO_NONE`, `mjSTEREO_QUADBUFFERED`, `mjSTEREO_SIDEBYSIDE` / `mjPERT_TRANSLATE` = 1, `mjPERT_ROTATE` = 2 |
| `mjtGridPos` (`mjr_overlay`) | `mjGRID_TOPLEFT`, `_TOPRIGHT`, `_BOTTOMLEFT`, `_BOTTOMRIGHT`, `_TOP`, `_BOTTOM`, `_LEFT`, `_RIGHT` |
| `mjtFramebuffer` (`mjr_setBuffer`) | `mjFB_WINDOW`, `mjFB_OFFSCREEN` |
| `mjtDepthMap` (`mjr_readPixels` depth) | `mjDEPTH_ZERONEAR` = 0 (0: znear, 1: zfar), `mjDEPTH_ZEROFAR` = 1 (reversed) |
| `mjtFontScale` / `mjtFont` | `mjFONTSCALE_50`, `_100`, `_150`, `_200`, `_250`, `_300` (value = percent) / `mjFONT_NORMAL`, `mjFONT_SHADOW`, `mjFONT_BIG` |
| `mjrPixelFormat` | `mjPIXEL_FORMAT_UNKNOWN`, `_R8`, `_RGB8`, `_RGBA8`, `_R32F`, `_DEPTH32F`, `_KTX` |
| `mjtButton` / `mjtSection` | `mjBUTTON_NONE`, `_LEFT`, `_RIGHT`, `_MIDDLE` / `mjSECT_CLOSED`, `mjSECT_OPEN`, `mjSECT_FIXED` |
| `mjtEvent` | `mjEVENT_NONE`, `_MOVE`, `_PRESS`, `_RELEASE`, `_SCROLL`, `_KEY`, `_RESIZE`, `_REDRAW`, `_FILESDROP` |
| `mjtItem` | `mjITEM_END` = -2, `mjITEM_SECTION` = -1, `mjITEM_SEPARATOR` = 0, `_STATIC`, `_BUTTON`, `_CHECKINT`, `_CHECKBYTE`, `_RADIO`, `_RADIOLINE`, `_SELECT`, `_SLIDERINT`, `_SLIDERNUM`, `_EDITINT`, `_EDITNUM`, `_EDITFLOAT`, `_EDITTXT`, `mjNITEM` |

Mesh-buffer enums (`mjrVertexAttributeUsage`, `mjrVertexAttributeType`,
`mjrIndexType`, `mjrMeshPrimitiveType`) and filament enums (`mjrGraphicsApi`,
`mjrDrawMode`, `mjrQuality`, `mjrToneMapper`, `mjrShadowType`,
`mjrAmbientOcclusionType`, `mjrDitheringType`) are in the verbatim copy.

## Spec enums (`mjspec.h`) and plugin enum

| Enum | Values |
|---|---|
| `mjtBuiltin` / `mjtMark` | `mjBUILTIN_NONE`, `_GRADIENT`, `_CHECKER`, `_FLAT` / `mjMARK_NONE`, `_EDGE`, `_CROSS`, `_RANDOM` |
| `mjtLimited` / `mjtAlignFree` | `mjLIMITED_FALSE`, `mjLIMITED_TRUE`, `mjLIMITED_AUTO` (inferred from range) / `mjALIGNFREE_FALSE`, `mjALIGNFREE_TRUE`, `mjALIGNFREE_AUTO` (global compiler flag) |
| `mjtPassthrough` (bits) / `mjtEmbed` | `mjPASSTHROUGH_NONE` = 0, `mjPASSTHROUGH_TEXTURES` = 1<<0 / `mjEMBED_FALSE` (by reference), `mjEMBED_TRUE`, `mjEMBED_AUTO` |
| `mjtInertiaFromGeom` | `mjINERTIAFROMGEOM_FALSE`, `_TRUE`, `_AUTO` (only if inertial missing) |
| `mjtOrientation` | `mjORIENTATION_QUAT`, `_AXISANGLE`, `_XYAXES`, `_ZAXIS`, `_EULER` |
| `mjtMeshInertia` | `mjMESH_INERTIA_CONVEX`, `_EXACT`, `_LEGACY`, `_SHELL` |
| `mjtMeshBuiltin` | `mjMESH_BUILTIN_NONE`, `_SPHERE`, `_HEMISPHERE`, `_CONE`, `_SUPERSPHERE`, `_SUPERTORUS`, `_WEDGE`, `_PLATE`, `_GRID`, `_BOX`, `_CYLINDER`, `_ELLIPSOID`, `_SQUARE`, `_DISC` |
| `mjtGeomInertia` / `mjtFlexSection` | `mjINERTIA_VOLUME`, `mjINERTIA_SHELL` / `mjFLEXSECTION_CIRCLE`, `mjFLEXSECTION_BOX` |
| `mjtConflict` (attach) / `mjtScaling` (frame scale) | `mjCONFLICT_WARNING`, `mjCONFLICT_MERGE`, `mjCONFLICT_ERROR` / `mjSCALING_SIMILAR`, `mjSCALING_GEOMETRY` |
| `mjtActuator` | `mjACTUATOR_GENERAL`, `_MOTOR`, `_POSITION`, `_VELOCITY`, `_INTVELOCITY`, `_DAMPER`, `_CYLINDER`, `_MUSCLE`, `_ADHESION`, `_PID`, `_ORIENTATION`, `_DCMOTOR` |
| `mjtCTimer` (`mjs_getTimer`) | `mjCTIMER_TOTAL`, `_ASSETS`, `_TEXTURE`, `_MESH_LOAD`, `_MESH_HULL`, `_MESH_POLYGON`, `_MESH_INERTIA`, `_MESH_BVH`, `_MESH_OCTREE`, `mjNCTIMER` |
| `mjtPluginCapabilityBit` | `mjPLUGIN_ACTUATOR` = 1<<0, `mjPLUGIN_SENSOR` = 1<<1, `mjPLUGIN_PASSIVE` = 1<<2, `mjPLUGIN_SDF` = 1<<3 |

## mjModel

Constant to the simulator. All sizes are `mjtSize`; most used: `nq`
(dim(qpos)), `nv` (dim(qvel)), `nu` (dim(ctrl)), `na` (dim(act)), `nactuator`,
`nout` (force outputs), `nbody`, `njnt`, `ngeom`, `nsite`, `ncam`, `nlight`,
`nmesh`, `ntendon`, `neq`, `npair`, `nexclude`, `nsensor`, `nsensordata`,
`nkey`, `nmocap`, `ntree`, `nuserdata`. Embedded: `mjOption opt`,
`mjVisual vis`, `mjStatistic stat`. Excerpt:

```c
  mjtNum*   qpos0;                // qpos values at default pose              (nq x 1)
  int*      body_parentid;        // id of body's parent                      (nbody x 1)
  int*      body_jntadr;          // start addr of joints; -1: no joints      (nbody x 1)
  int*      body_dofadr;          // start addr of dofs; -1: no dofs          (nbody x 1)
  int*      body_geomnum;         // number of geoms                          (nbody x 1)
  int*      body_geomadr;         // start addr of geoms; -1: no geoms        (nbody x 1)
  mjtNum*   body_pos;             // position offset rel. to parent body      (nbody x 3)
  mjtNum*   body_quat;            // orientation offset rel. to parent body   (nbody x 4)
  mjtNum*   body_mass;            // mass                                     (nbody x 1)
  mjtNum*   body_inertia;         // diagonal inertia in ipos/iquat frame     (nbody x 3)
  int*      jnt_type;             // type of joint (mjtJoint)                 (njnt x 1)
  int*      jnt_qposadr;          // start addr in 'qpos' for joint's data    (njnt x 1)
  int*      jnt_dofadr;           // start addr in 'qvel' for joint's data    (njnt x 1)
  int*      jnt_bodyid;           // id of joint's body                       (njnt x 1)
  mjtNum*   jnt_range;            // joint limits                             (njnt x 2)
  int*      dof_jntid;            // id of dof's joint                        (nv x 1)
  int*      geom_type;            // geometric type (mjtGeom)                 (ngeom x 1)
  int*      geom_contype;         // geom contact type                        (ngeom x 1)
  int*      geom_conaffinity;     // geom contact affinity                    (ngeom x 1)
  int*      geom_condim;          // contact dimensionality (1, 3, 4, 6)      (ngeom x 1)
  int*      geom_bodyid;          // id of geom's body                        (ngeom x 1)
  int*      geom_dataid;          // id of geom's mesh/hfield; -1: none       (ngeom x 1)
  mjtNum*   geom_size;            // geom-specific size parameters            (ngeom x 3)
  mjtNum*   geom_friction;        // friction for (slide, spin, roll)         (ngeom x 3)
  float*    geom_rgba;            // rgba when material is omitted            (ngeom x 4)
  int*      actuator_trnid;       // transmission id: joint, tendon, site     (nactuator x 2)
  mjtNum*   actuator_gainprm;     // gain parameters                          (nactuator x mjNGAIN)
  mjtNum*   actuator_ctrlrange;   // range of controls                        (nu x 2)
  mjtNum*   actuator_gear;        // scale length and transmitted force       (nout x 6)
  int*      sensor_adr;           // address in sensor array                  (nsensor x 1)
  mjtNum*   key_qpos;             // key position                             (nkey x nq)
```

Also common: `body_weldid`, `body_mocapid` (-1: none), `body_ipos` (x3),
`body_subtreemass`, `jnt_limited`, `jnt_axis` (x3), `dof_armature`,
`dof_damping`, `geom_group`, `geom_solref` (x mjNREF), `geom_solimp`
(x mjNIMP), `geom_pos` (x3), `geom_quat` (x4), `geom_margin`, `geom_gap`,
`eq_type` (mjtEq), `eq_data` (x mjNEQDATA), `actuator_biasprm` (x mjNBIAS),
`sensor_dim`. Same pattern for `site_*`, `cam_*`, `light_*`, `mesh_*`,
`tendon_*`, `key_*`, `name_*adr` + `char* names`, `pair_*`, `flex_*`, `tex_*`,
`mat_*`. `uint64_t signature` is shared with the compiling mjSpec.

## mjOption (`m->opt`, MJCF `option`)

```c
  mjtNum timestep;                // timestep
  mjtNum impratio;                // ratio of friction-to-normal contact impedance
  mjtNum tolerance;               // main solver tolerance
  mjtNum ls_tolerance;            // CG/Newton linesearch tolerance
  mjtNum noslip_tolerance;        // noslip solver tolerance
  mjtNum ccd_tolerance;           // convex collision solver tolerance
  mjtNum sleep_tolerance;         // sleep velocity tolerance
  mjtNum gravity[3];              // gravitational acceleration
  mjtNum wind[3];                 // wind (for lift, drag and viscosity)
  mjtNum magnetic[3];             // global magnetic flux
  mjtNum density;                 // density of medium
  mjtNum viscosity;               // viscosity of medium
  mjtNum o_margin;                // margin
  mjtNum o_solref[mjNREF];        // solref
  mjtNum o_solimp[mjNIMP];        // solimp
  mjtNum o_friction[5];           // friction
  int integrator;                 // integration mode (mjtIntegrator)
  int cone;                       // type of friction cone (mjtCone)
  int jacobian;                   // type of Jacobian (mjtJacobian)
  int solver;                     // solver algorithm (mjtSolver)
  int iterations;                 // maximum number of main solver iterations
  int ls_iterations;              // maximum number of CG/Newton linesearch iterations
  int noslip_iterations;          // maximum number of noslip solver iterations
  int ccd_iterations;             // maximum number of convex collision solver iterations
  int disableflags;               // bit flags for disabling standard features
  int enableflags;                // bit flags for enabling optional features
  int disableactuator;            // bit flags for disabling actuators by group id
  int sdf_initpoints;             // number of starting points for gradient descent
  int sdf_iterations;             // max number of iterations for gradient descent
```

The `o_*` fields override contact parameters only when `mjENBL_OVERRIDE` is set.

## mjData

The workspace all functions read inputs from and write outputs to. Header:
`time`, `energy[2]` (potential, kinetic), `ncon`, `ne`, `nf`, `nl`, `nefc`,
`nisland`, `warning[mjNWARNING]` (`mjWarningStat`: `lastinfo`, `number`),
`timer[mjNTIMER]` (`mjTimerStat`: `duration`, `number`),
`solver[mjNISLAND*mjNSOLVER]` (`mjSolverStat`), `solver_niter[mjNISLAND]`,
`maxuse_stack`, `maxuse_arena`, `maxuse_con`, `maxuse_efc`. Excerpt:

```c
  mjtNum* qpos;              // position                                         (nq x 1)
  mjtNum* qvel;              // velocity                                         (nv x 1)
  mjtNum* act;               // actuator activation                              (na x 1)
  mjtNum* ctrl;              // control                                          (nu x 1)
  mjtNum* qfrc_applied;      // applied generalized force                        (nv x 1)
  mjtNum* xfrc_applied;      // applied Cartesian force/torque                   (nbody x 6)
  mjtNum* mocap_pos;         // positions of mocap bodies                        (nmocap x 3)
  mjtNum* qacc;              // acceleration                                     (nv x 1)
  mjtNum* sensordata;        // sensor data array                                (nsensordata x 1)
  //-------------------- POSITION dependent
  mjtNum* xpos;              // Cartesian position of body frame                 (nbody x 3)
  mjtNum* xquat;             // Cartesian orientation of body frame              (nbody x 4)
  mjtNum* xmat;              // Cartesian orientation of body frame              (nbody x 9)
  mjtNum* geom_xpos;         // Cartesian geom position                          (ngeom x 3)
  mjtNum* geom_xmat;         // Cartesian geom orientation                       (ngeom x 9)
  mjtNum* site_xpos;         // Cartesian site position                          (nsite x 3)
  //-------------------- POSITION, VELOCITY dependent
  mjtNum* cvel;              // com-based velocity (rot:lin)                     (nbody x 6)
  mjtNum* qfrc_bias;         // C(qpos,qvel)                                     (nv x 1)
  mjtNum* qfrc_passive;      // total passive force                              (nv x 1)
  //-------------------- POSITION, VELOCITY, CONTROL/ACCELERATION dependent
  mjtNum* actuator_force;    // actuator force in actuation space                (nout x 1)
  mjtNum* qfrc_actuator;     // actuator force in joint space                    (nv x 1)
  mjtNum* qfrc_constraint;   // constraint force (flag ipc: incl. flex contact)  (nv x 1)
  //-------------------- arena-allocated: POSITION dependent
  mjContact* contact;        // array of all detected contacts                   (ncon x 1)
  int*    efc_type;          // constraint type (mjtConstraint)                  (nefc x 1)
  //-------------------- arena-allocated: POSITION, VELOCITY, CONTROL/ACCELERATION dependent
  mjtNum* efc_force;         // constraint force in constraint space             (nefc x 1)
```

Also: `eq_active` (neq), `mocap_quat` (nmocap x 4), `xipos` (nbody x 3),
`xanchor`, `xaxis` (njnt x 3), `site_xmat` (nsite x 9), `subtree_com`
(nbody x 3), `cdof` (nv x 6), `cinert` (nbody x 10), `ten_length` (ntendon),
`actuator_length` (nout), `qacc_smooth` (nv), `efc_id` (nefc), `qfrc_inverse`
(nv; should equal qfrc_applied + J'*xfrc_applied + qfrc_actuator). Joint-space
inertia is `M` (sparse, `nC x 1`, `mj_makeM`) with factor `qLD`.
`subtree_linvel`/`subtree_angmom` (`mj_subtreeVel`) and `cacc`/`cfrc_int`/
`cfrc_ext` (`mj_rnePostConstraint`) are computed only if needed; `flg_subtreevel`,
`flg_rnepost`, `flg_energypos`, `flg_energyvel` record whether those ran.
Passive parts (`qfrc_spring`, `qfrc_damper`, `qfrc_gravcomp`, `qfrc_fluid`,
`qfrc_adhesion`), island, sleep and flex fields are in the verbatim copy.

## mjContact (`d->contact[i]`, `i < d->ncon`)

```c
  mjtNum  dist;                    // distance between nearest points; neg: penetration
  mjtNum  pos[3];                  // position of contact point: midpoint between geoms
  mjtNum  frame[9];                // normal is in [0-2], points from geom[0] to geom[1]
  mjtNum  includemargin;           // margin for force generation
  mjtNum  friction[5];             // tangent1, 2, spin, roll1, 2
  mjtNum  solref[mjNREF];          // constraint solver reference, normal direction
  mjtNum  solreffriction[mjNREF];  // constraint solver reference, friction directions
  mjtNum  solimp[mjNIMP];          // constraint solver impedance
  mjtNum  adhesion;                // adhesive force along the contact normal
  mjtNum  surfacevel[3];           // surface velocity (geom[1] - geom[0]): tangent1, 2, spin
  int     dim;                     // contact space dimensionality: 1, 3, 4 or 6
  int     geom[2];                 // geom ids; -1 for flex
  int     exclude;                 // 0: include, 1: in gap, 2: fused, 3: no dofs, 4: passive
  int     efc_address;             // address in efc; -1: not included
```

Also `mu` (regularized-cone friction), `flex[2]`, `elem[2]`, `vert[2]` (flex
contacts; -1 for geom). `geom1`/`geom2` are deprecated: use `geom[0]`/`geom[1]`.

## Other engine and visualization structs

| Struct | Fields |
|---|---|
| `mjVisual` (`m->vis`) | sub-structs `global` (`cameraid`, `orthographic`, `fovy`, `azimuth`, `elevation`, `realtime`, `offwidth`, `offheight`, ...), `quality` (`shadowsize`, `offsamples`, ...), `headlight` (`ambient[3]`, `diffuse[3]`, `specular[3]`, `active`), `map` (`znear`, `zfar`, `force`, `torque`, ...), `scale`, `rgba` |
| `mjStatistic` (`m->stat`) | `meaninertia`, `meanmass`, `meansize`, `extent`, `center[3]` |
| `mjLROpt` | `mode` (mjtLRMode), `useexisting`, `uselimit`, `accel`, `maxforce`, `timeconst`, `timestep`, `inttotal`, `interval`, `tolrange` |
| `mjPreContact` | `dist`, `pos[3]`, `normal[3]`, `tangent[3]` (narrowphase output) |
| `mjResource` / `mjVFS`, `mjCache` | `name`, `data`, `vfs`, `timestamp[512]`, `provider`, `args` / opaque `void* impl_` |
| `mjLogMessage` / `mjLogConfig` | `level`, `topic`, `subject[1024]`, `body`, `func`, `file`, `line`, `timestamp` / `logto_console` (true), `logto_file` (true), `logfile[1024]` ("MUJOCO_LOG.TXT"), `topics` (0) |
| `mjSolverStat` | `improvement`, `gradient`, `lineslope`, `nactive`, `nchange`, `neval`, `nupdate` |
| `mjBatchConfig` / `mjBatchRecord` | `nthread` (<= 0: one per logical CPU), `persistent` / `field` (NULL: record a state), `spec` (mjtState bits), `buf` (n x nstep x size) |
| `mjvCamera` | `type` (mjtCamera), `fixedcamid`, `trackbodyid`, `lookat[3]`, `distance`, `azimuth` (deg), `elevation` (deg), `orthographic` |
| `mjvOption` | `label` (mjtLabel), `frame` (mjtFrame), `geomgroup[mjNGROUP]`, `sitegroup`, `jointgroup`, `tendongroup`, `actuatorgroup`, `flexgroup`, `skingroup`, `flags[mjNVISFLAG]`, `bvh_depth`, `flex_layer` |
| `mjvScene` | `maxgeom`, `ngeom`, `geoms` (mjvGeom*), `nlight`, `lights[mjMAXLIGHT]`, `camera[2]` (mjvGLCamera), `enabletransform`, `translate[3]`, `rotate[4]`, `scale`, `stereo`, `flags[mjNRNDFLAG]`, `framewidth`, `framergb[3]`, `status` (1: geoms exhausted) |
| `mjvGeom` | `type`, `dataid`, `objtype`, `objid` (-1 for decor), `category`, `matid`, `texid`, `segid`, `size[3]`, `pos[3]`, `mat[9]`, `rgba[4]`, `emission`, `specular`, `shininess`, `reflectance`, `castshadow`, `label[100]` |
| `mjvPerturb` | `select` (body id; non-positive: none), `flexselect`, `skinselect`, `active`, `active2` (mjtPertBit), `refpos[3]`, `refquat[4]`, `refselpos[3]`, `localpos[3]`, `localmass`, `scale` |
| `mjvGLCamera` / `mjvLight` | `pos[3]`, `forward[3]`, `up[3]`, `frustum_*`, `orthographic` / `id` (-1 headlight), `pos[3]`, `dir[3]`, `type`, `castshadow`, `intensity`, ... |
| `mjrRect` / `mjrContext` | `left`, `bottom`, `width`, `height` / OpenGL resource ids, `readPixelFormat`, `readDepthMap` (mjtDepthMap), `offWidth`, `offHeight`, `currentBuffer` |

`mjvFigure`, filament structs (`mjrfContextConfig`, `mjrfMaterial`,
`mjrfRenderRequest`, `mjrfRenderOpts`, ...) and UI structs (`mjuiState`,
`mjuiItem`, `mjuiSection`, `mjuiDef`, `mjUI`) are in the verbatim copy.

## Model editing structs (`mjspec.h`)

Every `mjs*` element starts with `mjsElement* element` (`elemtype` as mjtObj,
`signature`); never modify it. Strings and vectors are `mjString*`,
`mjStringVec*`, `mjIntVec*`, `mjFloatVec*`, `mjDoubleVec*`, `mjByteVec*`:
`std::` types in C++, opaque `void` in C (use the getters/setters in
[api-functions](../api-functions/SKILL.md)). Most elements end with
`mjString* info` (message appended to compiler errors). Workflows:
[model-editing](../../model-editing/SKILL.md).

`mjSpec`: `element`, `modelname`, `compiler` (mjsCompiler), `strippath`,
`option` (mjOption), `visual` (mjVisual), `stat`, `memory`, `nemax`,
`nuserdata`, `nuser_*`, `nkey`, `comment`, `modelfiledir`, `authored`.
`mjsCompiler`: `autolimits`, `boundmass`, `boundinertia`, `balanceinertia`,
`fitaabb`, `degree`, `eulerseq[3]`, `discardvisual`, `usethread`,
`fusestatic`, `inertiafromgeom`, `inertiagrouprange[2]`, `saveinertial`,
`alignfree`, `conflict`, `passthrough`, `LRopt`, `meshdir`, `texturedir`.

```c
typedef struct mjsBody_ {          // body specification
  double pos[3];                   // frame position
  double quat[4];                  // frame orientation
  double mass;                     // mass
  double ipos[3];                  // inertial frame position
  double inertia[3];               // diagonal inertia (in i-frame)
  double gravcomp;                 // gravity compensation
  ...
} mjsBody;
typedef struct mjsJoint_ {         // joint specification
  mjtJoint type;                   // joint type
  double pos[3];                   // anchor position
  double axis[3];                  // joint axis
  double stiffness[mjNPOLY+1];     // stiffness coefficients
  mjtLimited limited;              // does joint have limits
  double range[2];                 // joint limits
  double armature;                 // armature inertia (mass for slider)
  double damping[mjNPOLY+1];       // damping coefficients
  double frictionloss;             // friction loss
  ...
} mjsJoint;
typedef struct mjsGeom_ {          // geom specification
  mjtGeom type;                    // geom type
  double pos[3];                   // position
  double quat[4];                  // orientation
  double size[3];                  // type-specific size
  int contype;                     // contact type
  int conaffinity;                 // contact affinity
  int condim;                      // contact dimensionality
  double friction[3];              // one-sided friction coefficients: slide, roll, spin
  mjtNum solref[mjNREF];           // solver reference
  mjtNum solimp[mjNIMP];           // solver impedance
  double density;                  // used to compute mass and inertia from volume or surface
  float rgba[4];                   // rgba when material is omitted
  mjString* meshname;              // mesh attached to geom
  ...
} mjsGeom;
```

| Element | Other / key fields |
|---|---|
| `mjsBody` (rest) | `alt`, `fullinertia[6]`, `mocap`, `childclass`, `iquat[4]`, `ialt`, `sleep` (mjtSleepPolicy), `simple`, `fuse`, `userdata`, `explicitinertial`, `plugin` |
| `mjsJoint` (rest) | `ref` (qpos0), `springref` (qpos_spring), `align` (mjtAlignFree), `springyield`, `springdamper[2]` (timeconst, dampratio), `margin`, `solref_limit`, `solimp_limit`, `actfrclimited`, `actfrcrange[2]`, `solref_friction`, `solimp_friction`, `group`, `actgravcomp`, `userdata` |
| `mjsGeom` (rest) | `alt`, `fromto[6]`, `margin`, `gap`, `mass`, `material`, `group`, `priority`, `solmix`, `surfacevel[6]`, `adhesion`, `typeinertia` (mjtGeomInertia), `fluid_ellipsoid`, `fluid_coefs[5]`, `castshadow`, `hfieldname`, `fitscale`, `userdata`, `plugin` |
| `mjsFrame` | `childclass`, `pos[3]`, `quat[4]`, `alt`, `scale[3]`, `scaling` (mjtScaling), `massscale` |
| `mjsSite` | `pos[3]`, `quat[4]`, `alt`, `fromto[6]`, `size[3]`, `type` (mjtGeom), `material`, `group`, `rgba[4]`, `meshname`, `userdata` |
| `mjsCamera` | `pos[3]`, `quat[4]`, `alt`, `mode` (mjtCamLight), `targetbody`, `proj`, `resolution[2]`, `output`, `fovy`, `ipd`, `intrinsic[4]`, `sensor_size[2]`, `focal_length[2]`, `focal_pixel[2]`, `principal_length[2]`, `principal_pixel[2]` |
| `mjsLight` | `pos[3]`, `dir[3]`, `mode`, `targetbody`, `active`, `type`, `texture`, `castshadow`, `bulbradius`, `intensity`, `range`, `attenuation[3]`, `cutoff`, `softness`, `exponent`, `ambient[3]`, `diffuse[3]`, `specular[3]` |
| `mjsMesh` | `content_type`, `file`, `refpos[3]`, `refquat[4]`, `scale[3]`, `inertia` (mjtMeshInertia), `smoothnormal`, `needsdf`, `maxhullvert`, `uservert`, `usernormal`, `usertexcoord`, `userface`, `material`, `octree_maxdepth` |
| `mjsHField` | `content_type`, `file`, `size[4]`, `nrow`, `ncol`, `userdata` (elevation) |
| `mjsTexture` | `type`, `colorspace`, `builtin`, `mark`, `rgb1[3]`, `rgb2[3]`, `markrgb[3]`, `random`, `height`, `width`, `nchannel`, `file`, `gridsize[2]`, `gridlayout[12]`, `cubefiles`, `data`, `hflip`, `vflip`, `embed` |
| `mjsMaterial` | `textures` (mjStringVec), `texuniform`, `texrepeat[2]`, `emission`, `specular`, `shininess`, `reflectance`, `metallic`, `roughness`, `rgba[4]` |
| `mjsPair` / `mjsExclude` / `mjsWrap` | `geomname1`, `geomname2`, `condim`, `solref`, `solreffriction`, `solimp`, `margin`, `gap`, `adhesion`, `friction[5]` / `bodyname1`, `bodyname2` / `type` (mjtWrap) |
| `mjsEquality` | `type` (mjtEq), `data[mjNEQDATA]`, `active`, `name1`, `name2`, `objtype` (mjtObj), `solref`, `solimp` |
| `mjsTendon` | `stiffness[mjNPOLY+1]`, `springlength[2]`, `damping[mjNPOLY+1]`, `frictionloss`, `armature`, `limited`, `actfrclimited`, `range[2]`, `actfrcrange[2]`, `margin`, `solref_limit`, `solimp_limit`, `material`, `width`, `rgba[4]`, `group` |
| `mjsActuator` | `type` (mjtActuator), `gaintype`, `gainprm[mjNGAIN]`, `biastype`, `biasprm[mjNBIAS]`, `dyntype`, `dynprm[mjNDYN]`, `actdim`, `ctrlspec`, `actearly`, `trntype`, `gear[6]`, `target`, `refsite`, `slidersite`, `cranklength`, `lengthrange[2]`, `inheritrange`, `damping[mjNPOLY+1]`, `armature`, `ctrllimited`, `ctrlrange[2]`, `forcelimited`, `forcerange[2]`, `actlimited`, `actrange[2]`, `group`, `nsample`, `interp`, `delay`, `plugin` |
| `mjsSensor` | `type` (mjtSensor), `objtype`, `objname`, `reftype`, `refname`, `intprm[mjNSENS]`, `datatype`, `needstage`, `dim`, `cutoff`, `noise`, `nsample`, `interp`, `delay`, `interval[2]`, `plugin` |
| `mjsKey` | `time`, `qpos`, `qvel`, `act`, `mpos`, `mquat`, `ctrl`, `plastic` (all mjDoubleVec*) |
| `mjsNumeric` / `mjsText` / `mjsTuple` | `data`, `size` / `data` / `objtype`, `objname`, `objprm` |
| `mjsDefault` | pointers `joint`, `geom`, `site`, `camera`, `light`, `flex`, `mesh`, `texture`, `material`, `pair`, `equality`, `tendon`, `actuator` |
| `mjsPlugin` / `mjsOrientation` | `name`, `plugin_name`, `active` / `type` (mjtOrientation), `axisangle[4]`, `xyaxes[6]`, `zaxis[3]`, `euler[3]` |

`mjsFlex` and `mjsSkin` are in the verbatim copy. `mjsFlex.elastic3d` is
experimental and mjSpec-only: 0 Saint Venant-Kirchhoff (default), 1 Stable
Neo-Hookean, which requires the discrete integrator.

## Function types

| Type | Declaration | Used by |
|---|---|---|
| `mjfGeneric` | `typedef void (*mjfGeneric)(const mjModel* m, mjData* d);` | `mjcb_passive`, `mjcb_control` |
| `mjfConFilt` | `typedef int (*mjfConFilt)(const mjModel* m, mjData* d, int geom1, int geom2);` | `mjcb_contactfilter`; return 1: discard, 0: proceed |
| `mjfSensor` | `typedef void (*mjfSensor)(const mjModel* m, mjData* d, int stage);` | `mjcb_sensor` |
| `mjfTime` | `typedef mjtNum (*mjfTime)(void);` | `mjcb_time` |
| `mjfAct` | `typedef mjtNum (*mjfAct)(const mjModel* m, const mjData* d, int id);` | `mjcb_act_dyn`, `mjcb_act_gain`, `mjcb_act_bias` |
| `mjfCollision` | `typedef int (*mjfCollision)(const mjModel* m, const mjData* d, mjPreContact* con, int g1, int g2, mjtNum margin);` | `mjCOLLISIONFUNC` table |
| `mjfLogHandler` | `typedef void (*mjfLogHandler)(const mjLogMessage*);` | `mju_setLogHandler`; must be thread-safe, must not call `mju_error` |
| `mjfItemEnable` | `typedef int (*mjfItemEnable)(int category, void* data);` | UI item predicate |
| `mjfBatchFunc` | `typedef void (*mjfBatchFunc)(const mjModel* m, mjData* d, int sim, void* arg);` | `mjb_apply` |

Resource-provider callbacks: `mjfOpenResource` (returns 0 on failure, and then
`close` is not called), `mjfReadResource` (returns bytes, -1 on error),
`mjfCloseResource`, `mjfGetResourceDir`, `mjfResourceModified` (>0 modified,
0 not, <0 inconclusive), `mjfDecode`, `mjfCanDecode`, `mjfEncode`. Plugin
structs `mjpPlugin`, `mjpResourceProvider`, `mjpDecoder`, `mjpEncoder` and
`mjSDF` are in the verbatim copy; see
[engine-plugins](../../c-programming/engine-plugins/SKILL.md).

## Notes on data layout

- `cdof` and `cinert` use the c-frame: origin at `subtree_com`, oriented like
  the world frame. `cdof` rows are 6D motion vectors (3 rotation, 3
  translation). `cinert` packs (6, 3, 1): `cinert[0-5]` upper triangle of the
  inertia matrix, `cinert[6-8]` mass times CoM offset from the c-frame origin,
  `cinert[9]` mass. Analytic Jacobians need `mj_kinematics` then `mj_comPos`.
- `cvel`, `cacc`, `cfrc_int`, `cfrc_ext` are also rotation:translation.
- Convex hull: if `m->mesh_graphadr[N]` is not -1, `m->mesh_graph` at that
  offset holds `numvert`, `numface`, `vert_edgeadr[numvert]`,
  `vert_globalid[numvert]`, `edge_localid[numvert+3*numface]` (-1-terminated
  edge records), `face_globalid[3*numface]`.

## Pitfalls

- `geom_friction` is commented (slide, spin, roll) in mjModel, while
  `mjsGeom.friction` says slide, roll, spin; both are verbatim. Contacts and
  pairs use 5 values: tangent1, 2, spin, roll1, 2.
- Actuator arrays have three lengths: per actuator (`nactuator`), per control
  (`actuator_ctrlrange`, `nu`) and per force output (`actuator_gear`,
  `actuator_length`, `actuator_force`, `nout`).
- `stiffness` and `damping` in `mjsJoint` and `mjsTendon`, and
  `mjsActuator.damping`, are arrays `[mjNPOLY+1]`, not scalars.

## Source docs

Verbatim copies, for details not covered above:

- [APIreference/APItypes.md](references/APIreference-APItypes.md)
