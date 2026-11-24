# Functions

Tip

Clicking on a function name below will take you to the source implementation in the GitHub repository.

The main header [mujoco.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mujoco.h) exposes a large number of functions. However the functions that most users are likely to need are a small fraction.

API function can be classified as:

- **Main entry points**  
  - [Parse and compile](#parseandcompile) an [mjModel](APItypes.md#mjmodel) from XML files and assets.

  - [Main simulation](#mainsimulation) entry points, including [mj_step](#mj-step).

- **Support functions**  
  - [Support](#support) functions requiring [mjModel](APItypes.md#mjmodel) and [mjData](APItypes.md#mjdata).

  - Pipeline [components](#components), called from [mj_step](#mj-step), [mj_forward](#mj-forward) and [mj_inverse](#mj-inverse).

  - [Sub components](#subcomponents) of the simulation pipeline.

  - [Ray casting](#raycollisions).

  - [Printing](#printing) of various quantities.

  - [Virtual file system](#virtualfilesystem), used to load assets from memory.

  - [Asset cache](#assetcache), used to speed up model compilation.

  - [Resources](#resources), interfacing with resource providers to load assets.

  - [Initialization](#initialization) of data structures.

  - [Error and memory](#errorandmemory).

  - [Miscellaneous](#miscellaneous) functions.

- **Visualization, Rendering, UI**  
  - [Abstract interaction](#interaction): mouse control of cameras and perturbations.

  - [Abstract Visualization](#visualization-api).

  - [OpenGL rendering](#openglrendering).

  - [Filament rendering](#filamentrenderingapi).

  - [UI framework](#uiframework).

- **Threads, Plugins, Derivatives**  
  - [Derivatives](#derivatives-api).

  - [Signed Distance Functions](#signeddistancefunction).

  - [Thread](#thread)⁠-related functions.

  - [Batched simulation](#batchedsimulation).

  - [Plugin](#plugins-api)⁠-related functions.

- **Math**  
  - Aliases for C [standard math](#standardmath) functions.

  - [Vector math](#vectormath).

  - [Sparse math](#sparsemath).

  - [Quaternions](#quaternions).

  - [Pose transformations](#poses).

  - [Matrix decompositions and solvers](#decompositions).

- **Model editing**  
  - [Attachment](#attachment).

  - [Tree elements](#addtreeelements).

  - [Non-tree elements](#addnontreeelements).

  - [Set actuator parameters](#setactuatorparameters).

  - [Assets](#addassets).

  - [Find and get utilities](#findandgetutilities).

  - [Attribute setters](#attributesetters).

  - [Attribute getters](#attributegetters).

  - [Spec utilities](#specutilities).

  - [Element initialization](#elementinitialization).

  - [Element casting](#elementcasting).

## Parse and compile

The key function here is [mj_loadXML](#mj-loadxml). It invokes the built-in parser and compiler, and either returns a pointer to a valid mjModel, or NULL - in which case the user should check the error information in the user-provided string. The model and all files referenced in it can be loaded from disk or from a VFS when provided.

### [mj_loadXML](#mj_loadXML)

``` C
mjModel* mj_loadXML(const char* filename, const mjVFS* vfs, char* error, int error_sz);
```

Parse XML file in MJCF or URDF format, compile it; return low-level model.

If vfs is not NULL, look up files in vfs before reading from disk.

If error is not NULL, it must have size error_sz.

*Nullable:* `vfs`, `error`

### [mj_parseXML](#mj_parseXML)

``` C
mjSpec* mj_parseXML(const char* filename, const mjVFS* vfs, char* error, int error_sz);
```

Parse spec from XML file.

*Nullable:* `vfs`, `error`

### [mj_parseXMLString](#mj_parseXMLString)

``` C
mjSpec* mj_parseXMLString(const char* xml, const mjVFS* vfs, char* error, int error_sz);
```

Parse spec from XML string.

*Nullable:* `vfs`, `error`

### [mj_parse](#mj_parse)

``` C
mjSpec* mj_parse(const char* filename, const char* content_type,
                 const mjVFS* vfs, char* error, int error_sz);
```

Parse spec from a file.

*Nullable:* `vfs`, `error`

### [mj_encode](#mj_encode)

``` C
mjtSize mj_encode(const mjSpec* s, const mjModel* m, const char* filename,
                  const char* content_type, const mjVFS* vfs, char* error,
                  int error_sz);
```

Encode [mjSpec](APItypes.md#mjspec) or [mjModel](APItypes.md#mjmodel) to a file. The output format is determined by the file extension (case insensitive) or `content_type`. Returns the number of bytes written on success, -1 on failure.

For detailed documentation, supported output formats (`.xml`, `.mjb`, `.txt`, `.mjz`), and custom encoder plugins, see [Model Encoding & Saving](../programming/modeledit.md#mesaving).

*Nullable:* `s`, `m`, `vfs`, `error`

### [mj_compile](#mj_compile)

``` C
mjModel* mj_compile(mjSpec* s, const mjVFS* vfs);
```

Compile [mjSpec](APItypes.md#mjspec) to [mjModel](APItypes.md#mjmodel). A spec can be edited and compiled multiple times, returning a new [mjModel](APItypes.md#mjmodel) instance that takes the edits into account. If compilation fails, [mj_compile](#mj-compile) returns `NULL`; the error can be read with [mjs_getError](#mjs-geterror).

Compilation leaves the spec as it is written, with two exceptions. It completes [keyframes](../XMLreference.md#keyframe): their vectors are sized for the model, and keyframes are added up to [nkey](../XMLreference.md#size-nkey). And the compiler attributes [discardvisual](../XMLreference.md#compiler-discardvisual) and [fusestatic](../XMLreference.md#compiler-fusestatic) apply [mjs_discardVisual](#mjs-discardvisual) and [mjs_fuseStatic](#mjs-fusestatic) to the spec before it is compiled, which changes it: pointers to the elements which they remove are no longer valid. An operation which fails changes nothing, but one which succeeded stays applied if a later one, or the compilation, fails; the error then says so.

### [mj_copyBack](#mj_copyBack)

``` C
int mj_copyBack(mjSpec* s, const mjModel* m);
```

Copy to an [mjSpec](APItypes.md#mjspec) the values which were changed in the [mjModel](APItypes.md#mjmodel) that was compiled from it. The changes can then be read in the spec, are saved with it, and are in the models which are compiled from it afterwards. An attribute is copied if the model no longer has what compilation gave it, all of its numbers; everything else in the spec is left as it is, including what was written there since it was compiled. The position and the orientation of a pose, and the bounds of a range, are separate attributes. Returns 1 on success. Returns 0 if the model was not compiled from the spec as it is structured now, or if a value was changed which the spec cannot express; nothing is copied then, and the error can be read with [mjs_getError](#mjs-geterror). A model can also be copied back to a copy of the spec made by [mj_copySpec](#mj-copyspec).

The values which are copied are `mjModel.opt`, `mjModel.vis` and `mjModel.stat`, the real-valued parameters of bodies, joints, geoms, sites, cameras, lights, materials, contact pairs, equalities, tendons, actuators and sensors, custom numeric and tuple data, keyframes and the elevation data of height fields. Each is written as what compiles to it:

- A pose is written in the [frame](../XMLreference.md#frame) which the element is in. An orientation which was not changed stays as it was written, for example as Euler angles, and one which was changed is written as a quaternion. Where compilation offsets the position by the orientation, for a mesh geom whose mesh is not centered at its origin and a body which is [aligned](../XMLreference.md#body-freejoint-align) with its free joint, a new orientation also writes the position. The reference pose of a body with a free joint is taken from `mjModel.qpos0` if that was changed.

- Angles are written in the [unit](../XMLreference.md#compiler-angle) of the spec.

- The size and pose of a geom or site which were written as `fromto`, or computed by fitting a geom to a mesh, are written in its place. A new radius of a capsule or cylinder leaves `fromto` as it is.

- A mass or inertia which was changed gives the body an explicit [inertial](../XMLreference.md#body-inertial), which is then no longer inferred from its geoms; a body which has one keeps it as it was written if only the mass was changed. The inertia of the other bodies still follows their geoms, including a size or pose which was copied.

- A range whose `limited` attribute is “auto” keeps the limited state which it has in the model: the attribute is set if the new range would be inferred otherwise.

- A stiffness or damping of a joint with [springdamper](../XMLreference.md#body-joint-springdamper), and a control or activation range which was inherited with [inheritrange](../XMLreference.md#actuator-position-inheritrange), are written in its place.

- Elevation data of a height field which was read from a file is written in place of the file.

- The relative pose of a [weld](../XMLreference.md#equality-weld) between bodies which is marked by a nonzero `mjModel.eq_data[11]` is written as computed, with a zero quaternion.

The following changes cannot be expressed in the spec and are errors: the mass or inertia of a body when [inertiafromgeom](../XMLreference.md#compiler-inertiafromgeom) is “true” or [settotalmass](../XMLreference.md#compiler-settotalmass) is set; the inertial frame of a body which is [aligned](../XMLreference.md#body-freejoint-align) with its free joint; the pose of the world body; the anchor or axis of a free joint and the axis of a ball joint; the size of a mesh or height field geom or of a mesh site, and the frame of a mesh; the field of view of a camera which has a sensor size, and the intrinsics of one which has none; and different control ranges for the inputs of an actuator which has one. So are changes which the next compilation would not keep: damping, armature, friction loss or their solver parameters which differ between the degrees of freedom of a ball or free joint; elevation data of a height field whose lowest and highest values are not 0 and 1; and the anchor of a [connect](../XMLreference.md#equality-connect) between bodies in its second body, or the relative pose of a marked weld, other than the one which [mj_setConst](#mj-setconst) computes.

### [mj_recompile](#mj_recompile)

``` C
int mj_recompile(mjSpec* s, const mjVFS* vfs, mjModel* m, mjData* d);
```

Recompile spec to model, preserving the state. Like [mj_compile](#mj-compile), this function compiles an [mjSpec](APItypes.md#mjspec) to an [mjModel](APItypes.md#mjmodel), with two differences. First, rather than returning an entirely new model, it will reallocate existing [mjModel](APItypes.md#mjmodel) and [mjData](APItypes.md#mjdata) instances in-place. Second, it will preserve the [integration state](../programming/simulation.md#siintegrationstate), as given in the provided [mjData](APItypes.md#mjdata) instance, while accounting for newly added or removed degrees of freedom. This allows the user to continue simulation with the same model and data struct pointers while editing the model programmatically.

[mj_recompile](#mj-recompile) returns 0 if compilation succeed. In the case of failure, the given [mjModel](APItypes.md#mjmodel) and [mjData](APItypes.md#mjdata) instances will be deleted; as in [mj_compile](#mj-compile), the compilation error can be read with [mjs_getError](#mjs-geterror).

### [mj_loadTexture](#mj_loadTexture)

``` C
int mj_loadTexture(const mjModel* m, int id, mjtByte** data, int* width, int* height,
                   int* colorspace, char* error, int error_sz);
```

Decode texture id to raw bytes, exactly what compilation would store in tex_data, with tex_nchannel channels; embedded textures are copied from the model. The buffer is allocated with mju_malloc and freed by the caller; colorspace receives the resolved colorspace (mjtColorSpace).

Return 0 on success.

*Nullable:* `width`, `height`, `colorspace`, `error`

### [mj_embedAssets](#mj_embedAssets)

``` C
mjModel* mj_embedAssets(const mjModel* m, char* error, int error_sz);
```

Copy of m with every by-reference asset loaded into it, as compilation would have stored it.

Return NULL with error on a file that does not resolve. A hermetic MJB file of a model with by-reference assets is mj_embedAssets, then mj_saveModel, then mj_deleteModel.

*Nullable:* `error`

### [mj_saveLastXML](#mj_saveLastXML)

``` C
int mj_saveLastXML(const char* filename, const mjModel* m, char* error, int error_sz);
```

Update XML data structures with info from low-level model created with [mj_loadXML](#mj-loadxml), save as MJCF. If error is not NULL, it must have size error_sz.

Note that this function only saves models that have been loaded with [mj_loadXML](#mj-loadxml), the legacy loading mechanism. See the [model editing](../programming/modeledit.md#meoverview) chapter to understand the difference between the old and new model loading and saving mechanisms.

### [mj_freeLastXML](#mj_freeLastXML)

``` C
void mj_freeLastXML(void);
```

Free last XML model if loaded. Called internally at each load.

### [mj_saveXMLString](#mj_saveXMLString)

``` C
int mj_saveXMLString(const mjSpec* s, char* xml, int xml_sz, char* error, int error_sz);
```

Save spec to XML string, return 0 on success, -1 on failure. If the length of the output buffer is too small, returns the required size. See [mj_saveXML](#mj-savexml) for what is saved.

### [mj_saveXML](#mj_saveXML)

``` C
int mj_saveXML(const mjSpec* s, const char* filename, char* error, int error_sz);
```

Save spec to XML file, return 0 on success, -1 otherwise. The compiler attributes [savecompiled](../XMLreference.md#compiler-savecompiled) and [savecanonical](../XMLreference.md#compiler-savecanonical) of the spec say whether the model is saved as it was compiled or as it is written in the spec, and in which notation; see [Model Encoding & Saving](../programming/modeledit.md#mesaving). Saving the compiled values requires that the spec first be compiled, and compiled again after it is structurally edited (elements added, deleted or attached).

### [mju_getXMLDependencies](#mju_getXMLDependencies)

``` C
void mju_getXMLDependencies(const char* filename, mjStringVec* dependencies);
```

Given MJCF filename, fills dependencies with a list of all other asset files it depends on.

The search is recursive, and the list includes the filename itself.

## Main simulation

These are the main entry points to the simulator. Most users will only need to call [mj_step](#mj-step), which computes everything and advanced the simulation state by one time step. Controls and applied forces must either be set in advance (in `mjData.{ctrl, qfrc_applied, xfrc_applied}`), or a control callback [mjcb_control](APIglobals.md#mjcb-control) must be installed which will be called just before the controls and applied forces are needed. Alternatively, one can use [mj_step1](#mj-step1) and [mj_step2](#mj-step2) which break down the simulation pipeline into computations that are executed before and after the controls are needed; in this way one can set controls that depend on the results from [mj_step1](#mj-step1). Keep in mind though that the RK4 solver does not work with mj_step1/2. See [Simulation pipeline](../computation/index.md#pipeline) for a more detailed description.

mj_forward performs the same computations as [mj_step](#mj-step) but without the integration. It is useful after loading or resetting a model (to put the entire mjData in a valid state), and also for out-of-order computations that involve sampling or finite-difference approximations.

[mj_inverse](#mj-inverse) runs the inverse dynamics, and writes its output in `mjData.qfrc_inverse`. Note that `mjData.qacc` must be set before calling this function. Given the state (qpos, qvel, act), mj_forward maps from force to acceleration, while mj_inverse maps from acceleration to force. Mathematically these functions are inverse of each other, but numerically this may not always be the case because the forward dynamics rely on a constraint optimization algorithm which is usually terminated early. The difference between the results of forward and inverse dynamics can be computed with the function [mj_compareFwdInv](#mj-comparefwdinv), which can be thought of as another solver accuracy check (as well as a general sanity check).

The skip version of [mj_forward](#mj-forward) and [mj_inverse](#mj-inverse) are useful for example when qpos was unchanged but qvel was changed (usually in the context of finite differencing). Then there is no point repeating the computations that only depend on qpos. Calling the dynamics with skipstage = [mjSTAGE_POS](APItypes.md#mjtstage) will achieve these savings.

### [mj_step](#mj_step)

``` C
void mj_step(const mjModel* m, mjData* d);
```

Advance simulation, use control callback to obtain external force and control.

### [mj_step1](#mj_step1)

``` C
void mj_step1(const mjModel* m, mjData* d);
```

Advance simulation in two steps: before external force and control is set by user.

### [mj_step2](#mj_step2)

``` C
void mj_step2(const mjModel* m, mjData* d);
```

Advance simulation in two steps: after external force and control is set by user.

### [mj_forward](#mj_forward)

``` C
void mj_forward(const mjModel* m, mjData* d);
```

Forward dynamics: same as mj_step but do not integrate in time.

### [mj_inverse](#mj_inverse)

``` C
void mj_inverse(const mjModel* m, mjData* d);
```

Inverse dynamics: qacc must be set before calling.

### [mj_forwardSkip](#mj_forwardSkip)

``` C
void mj_forwardSkip(const mjModel* m, mjData* d, int skipstage, int skipsensor);
```

Forward dynamics with skip; skipstage is mjtStage.

### [mj_inverseSkip](#mj_inverseSkip)

``` C
void mj_inverseSkip(const mjModel* m, mjData* d, int skipstage, int skipsensor);
```

Inverse dynamics with skip; skipstage is mjtStage.

## Support

These are support functions that need access to [mjModel](APItypes.md#mjmodel) and [mjData](APItypes.md#mjdata), unlike the utility functions which do not need such access. Support functions are called within the simulator but some of them can also be useful for custom computations, and are documented in more detail below.

### [mj_stateSize](#mj_stateSize)

``` C
int mj_stateSize(const mjModel* m, int sig);
```

Returns the number of [mjtNum](APItypes.md#mjtnum)⁠s required for a given state signature. The bits of the integer `sig` correspond to element fields of [mjtState](APItypes.md#mjtstate).

### [mj_getState](#mj_getState)

``` C
void mj_getState(const mjModel* m, const mjData* d, mjtNum* state, int sig);
```

Copy concatenated state components specified by `sig` from `d` into `state`. The bits of the integer `sig` correspond to element fields of [mjtState](APItypes.md#mjtstate). Fails with [mju_error](#mju-error) if `sig` is invalid.

### [mj_extractState](#mj_extractState)

``` C
void mj_extractState(const mjModel* m, const mjtNum* src, int srcsig,
                     mjtNum* dst, int dstsig);
```

Extract into `dst` the subset of components specified by `dstsig` from a state `src` previously obtained via [mj_getState](#mj-getstate) with components specified by `srcsig`. Fails with [mju_error](#mju-error) if the bits set in `dstsig` is not a subset of the bits set in `srcsig`.

### [mj_setState](#mj_setState)

``` C
void mj_setState(const mjModel* m, mjData* d, const mjtNum* state, int sig);
```

Copy concatenated state components specified by `sig` from `state` into `d`. The bits of the integer `sig` correspond to element fields of [mjtState](APItypes.md#mjtstate). Fails with [mju_error](#mju-error) if `sig` is invalid.

### [mj_copyState](#mj_copyState)

``` C
void mj_copyState(const mjModel* m, const mjData* src, mjData* dst, int sig);
```

Copy state from src to dst.

### [mj_readCtrl](#mj_readCtrl)

``` C
const mjtNum* mj_readCtrl(const mjModel* m, const mjData* d, int id, mjtNum time,
                          mjtNum* result, int interp);
```

Read the control value for an actuator at a given time, taking delays into account. If no history buffer exists, return a pointer to the actuator’s slice of `mjData.ctrl`. If a history buffer exists ([nsample](../XMLreference.md#actuator-general-nsample) \> 0), read from the delay buffer at `time - actuator_delay[id]`. Note that the subtraction of the delay changes the semantic of the `time` argument from “time at which values were pushed into the delay buffer” to “time at which values come out of the delay buffer”. See [Delays](../modeling.md#cdelay) for details.

**Return value semantics:**

- If no history buffer exists ([nsample](../XMLreference.md#actuator-general-nsample) = 0), returns a pointer to the actuator’s slice of `mjData.ctrl`.

- If a history buffer exists ([nsample](../XMLreference.md#actuator-general-nsample) \> 0) and the requested time matches a stored sample (always true for `interp = 0`), returns a pointer to the data in the history buffer.

- If interpolation is required (`interp = 1 or 2`), returns `NULL` and writes the interpolated result to `result` (must be of size `actuator_ctrlnum[id]`).

**Interpolation:**

- `interp = 0`: Zero-order hold (piecewise constant)

- `interp = 1`: Piecewise Linear

- `interp = 2`: Cubic Spline (Catmull-Rom)

- `interp = -1`: Use the actuator’s [interp](../XMLreference.md#actuator-general-interp) value.

Constant extrapolation is used outside of buffer bounds.

### [mj_readSensor](#mj_readSensor)

``` C
const mjtNum* mj_readSensor(const mjModel* m, const mjData* d, int id, mjtNum time,
                            mjtNum* result, int interp);
```

Read a sensor value at a given time, taking delays into account. If no history buffer exists, return a pointer to the sensor’s slice of `mjData.sensordata`. If a history buffer exists ([nsample](../modeling.md#sensor-nsample) \> 0), read from the history buffer at `time - sensor_delay[id]`. Note that the subtraction of the delay changes the semantic of the `time` argument from “time at which values were pushed into the delay buffer” to “time at which values come out of the delay buffer”. See [Delays](../modeling.md#cdelay) for details.

**Return value semantics:**

- If no history buffer exists ([nsample](../modeling.md#sensor-nsample) = 0), returns a pointer to the sensor’s slice of `mjData.sensordata`.

- If a history buffer exists ([nsample](../modeling.md#sensor-nsample) \> 0) and the requested time matches a stored sample (always true for `interp = 0`), returns a pointer to the data in the history buffer.

- If interpolation is required (`interp = 1 or 2`), returns `NULL` and writes the interpolated result to `result` (must be of size `dim`).

**Interpolation:**

- `interp = 0`: Zero-order hold (piecewise constant)

- `interp = 1`: Piecewise Linear

- `interp = 2`: Cubic Spline (Catmull-Rom)

- `interp = -1`: Use the value in [interp](../modeling.md#sensor-interp)

Constant extrapolation is used outside of buffer bounds.

**Usage:**

``` C
// read sensor 0 of data size `dim` at time t
mjtNum result[dim];
const mjtNum* ptr = mj_readSensor(m, d, 0, t, result, /* interp = */ 1);
const mjtNum* data = ptr ? ptr : result;
```

### [mj_initCtrlHistory](#mj_initCtrlHistory)

``` C
void mj_initCtrlHistory(const mjModel* m, mjData* d, int id,
                        const mjtNum* times, const mjtNum* values);
```

Initialize the history buffer for an actuator with custom values. The `times` array specifies the timestamps for each sample (must be length [nsample](../XMLreference.md#actuator-general-nsample)), and `values` specifies the control values (must be of size `nsample * actuator_ctrlnum[id]`). If `times` is `NULL`, the existing timestamps in the buffer are used, and only the values are updated. See [Delays](../modeling.md#cdelay) for details.

### [mj_initSensorHistory](#mj_initSensorHistory)

``` C
void mj_initSensorHistory(const mjModel* m, mjData* d, int id,
                          const mjtNum* times, const mjtNum* values, mjtNum phase);
```

Initialize the history buffer for a sensor with custom values. The `times` array specifies the timestamps for each sample (must be length [nsample](../modeling.md#sensor-nsample)), and `values` specifies the sensor values (must be of size `nsample * dim`). If `times` is `NULL`, the existing timestamps in the buffer are used. The `phase` argument sets the user slot, which stores the last computation time for interval sensors. See [Delays](../modeling.md#cdelay) for details.

### [mj_setKeyframe](#mj_setKeyframe)

``` C
void mj_setKeyframe(mjModel* m, const mjData* d, int k);
```

Copy current state to the k-th model keyframe.

### [mj_addContact](#mj_addContact)

``` C
int mj_addContact(const mjModel* m, mjData* d, const mjContact* con);
```

Add contact to d-\>contact list; return 0 if success; 1 if buffer full.

### [mj_isPyramidal](#mj_isPyramidal)

``` C
int mj_isPyramidal(const mjModel* m);
```

Determine type of friction cone.

### [mj_isSparse](#mj_isSparse)

``` C
int mj_isSparse(const mjModel* m);
```

Determine type of constraint Jacobian.

### [mj_isDual](#mj_isDual)

``` C
int mj_isDual(const mjModel* m);
```

Determine type of solver (PGS is dual, CG and Newton are primal).

### [mj_mulJacVec](#mj_mulJacVec)

``` C
void mj_mulJacVec(const mjModel* m, const mjData* d, mjtNum* res, const mjtNum* vec);
```

This function multiplies the constraint Jacobian mjData.efc_J by a vector. Note that the Jacobian can be either dense or sparse; the function is aware of this setting. Multiplication by J maps velocities from joint space to constraint space.

### [mj_mulJacTVec](#mj_mulJacTVec)

``` C
void mj_mulJacTVec(const mjModel* m, const mjData* d, mjtNum* res, const mjtNum* vec);
```

Same as mj_mulJacVec but multiplies by the transpose of the Jacobian. This maps forces from constraint space to joint space.

### [mj_jac](#mj_jac)

``` C
void mj_jac(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr,
            const mjtNum point[3], int body);
```

This function computes an end-effector kinematic Jacobian, describing the local linear relationship between the degrees-of-freedom and a given point. Given a body specified by its integer id (`body`) and a 3D point in the world frame (`point`) treated as attached to the body, the Jacobian has both translational (`jacp`) and rotational (`jacr`) components. Passing `NULL` for either pointer will skip that part of the computation. Each component is a 3-by-nv matrix. Each row of this matrix is the gradient of the corresponding coordinate of the specified point with respect to the degrees-of-freedom. The frame with respect to which the Jacobian is computed is centered at the body center-of-mass but aligned with the world frame. The minimal [pipeline stages](../computation/index.md#piforward) required for Jacobian computations to be consistent with the current generalized positions `mjData.qpos` are [mj_kinematics](#mj-kinematics) followed by [mj_comPos](#mj-compos).

*Nullable:* `jacp`, `jacr`

### [mj_jacBody](#mj_jacBody)

``` C
void mj_jacBody(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr, int body);
```

This and the remaining variants of the Jacobian function call mj_jac internally, with the center of the body, geom or site. They are just shortcuts; the same can be achieved by calling mj_jac directly.

*Nullable:* `jacp`, `jacr`

### [mj_jacBodyCom](#mj_jacBodyCom)

``` C
void mj_jacBodyCom(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr, int body);
```

Compute body center-of-mass end-effector Jacobian.

*Nullable:* `jacp`, `jacr`

### [mj_jacSubtreeCom](#mj_jacSubtreeCom)

``` C
void mj_jacSubtreeCom(const mjModel* m, mjData* d, mjtNum* jacp, int body);
```

Compute subtree center-of-mass end-effector Jacobian.

### [mj_jacGeom](#mj_jacGeom)

``` C
void mj_jacGeom(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr, int geom);
```

Compute geom end-effector Jacobian.

*Nullable:* `jacp`, `jacr`

### [mj_jacSite](#mj_jacSite)

``` C
void mj_jacSite(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr, int site);
```

Compute site end-effector Jacobian.

*Nullable:* `jacp`, `jacr`

### [mj_jacPointAxis](#mj_jacPointAxis)

``` C
void mj_jacPointAxis(const mjModel* m, mjData* d, mjtNum* jacPoint, mjtNum* jacAxis,
                     const mjtNum point[3], const mjtNum axis[3], int body);
```

Compute translation end-effector Jacobian of point, and rotation Jacobian of axis.

*Nullable:* `jacPoint`, `jacAxis`

### [mj_jacDot](#mj_jacDot)

``` C
void mj_jacDot(const mjModel* m, const mjData* d, mjtNum* jacp, mjtNum* jacr,
               const mjtNum point[3], int body);
```

This function computes the time-derivative of an end-effector kinematic Jacobian computed by [mj_jac](#mj-jac). The minimal [pipeline stages](../computation/index.md#pistages) required for computation to be consistent with the current generalized positions and velocities `mjData.{qpos, qvel}` are [mj_kinematics](#mj-kinematics), [mj_comPos](#mj-compos), [mj_comVel](#mj-comvel) (in that order).

*Nullable:* `jacp`, `jacr`

### [mj_angmomMat](#mj_angmomMat)

``` C
void mj_angmomMat(const mjModel* m, mjData* d, mjtNum* mat, int body);
```

This function computes the `3 x nv` angular momentum matrix \\H(q)\\, providing the linear mapping from generalized velocities to subtree angular momentum. More precisely if \\h\\ is the subtree angular momentum of body index `body` in `mjData.subtree_angmom` (reported by the [subtreeangmom](../XMLreference.md#sensor-subtreeangmom) sensor) and \\\dot q\\ is the generalized velocity `mjData.qvel`, then \\h = H \dot q\\.

### [mj_name2id](#mj_name2id)

``` C
int mj_name2id(const mjModel* m, int type, const char* name);
```

Get id of object with the specified [mjtObj](APItypes.md#mjtobj) type and name, returns -1 if id not found.

### [mj_id2name](#mj_id2name)

``` C
const char* mj_id2name(const mjModel* m, int type, int id);
```

Get name of object with the specified [mjtObj](APItypes.md#mjtobj) type and id, returns `NULL` if name not found.

### [mj_actuatorInputName](#mj_actuatorInputName)

``` C
const char* mj_actuatorInputName(const mjModel* m, int id, int input);
```

Get name of actuator input, determined by the actuator type and input signature; return NULL if the actuator type defines no input names.

### [mj_fullM](#mj_fullM)

``` C
void mj_fullM(const mjModel* m, const mjData* d, mjtNum* dst);
```

Convert sparse inertia matrix into full (i.e. dense) matrix.

### [mj_mulM](#mj_mulM)

``` C
void mj_mulM(const mjModel* m, const mjData* d, mjtNum* res, const mjtNum* vec);
```

This function multiplies the joint-space inertia matrix stored in `mjData.M` by a vector.

### [mj_mulM2](#mj_mulM2)

``` C
void mj_mulM2(const mjModel* m, const mjData* d, mjtNum* res, const mjtNum* vec);
```

Multiply vector by (inertia matrix)^(1/2).

### [mj_addM](#mj_addM)

``` C
void mj_addM(const mjModel* m, mjData* d, mjtNum* dst, int* rownnz, int* rowadr, int* colind);
```

Add inertia matrix to destination matrix (lower triangle only).

Destination can be sparse or dense when all int\* are NULL.

*Nullable:* `rownnz`, `rowadr`, `colind`

### [mj_applyFT](#mj_applyFT)

``` C
void mj_applyFT(const mjModel* m, mjData* d, const mjtNum force[3], const mjtNum torque[3],
                const mjtNum point[3], int body, mjtNum* qfrc_target);
```

This function can be used to apply a Cartesian force and torque to a point on a body, and add the result to the vector mjData.qfrc_applied of all applied forces. Note that the function requires a pointer to this vector, because sometimes we want to add the result to a different vector.

### [mj_objectVelocity](#mj_objectVelocity)

``` C
void mj_objectVelocity(const mjModel* m, const mjData* d,
                       int objtype, int objid, mjtNum res[6], int flg_local);
```

Compute object 6D velocity (rot:lin) in object-centered frame, world/local orientation.

### [mj_objectAcceleration](#mj_objectAcceleration)

``` C
void mj_objectAcceleration(const mjModel* m, const mjData* d,
                           int objtype, int objid, mjtNum res[6], int flg_local);
```

Compute object 6D acceleration (rot:lin) in object-centered frame, world/local orientation. If acceleration or force sensors are not present in the model, [mj_rnePostConstraint](#mj-rnepostconstraint) must be manually called in order to calculate mjData.cacc – the total body acceleration, including contributions from the constraint solver.

### [mj_geomDistance](#mj_geomDistance)

``` C
mjtNum mj_geomDistance(const mjModel* m, mjData* d, int geom1, int geom2, mjtNum distmax,
                       mjtNum fromto[6]);
```

Returns the smallest signed distance between two geoms and optionally the segment from `geom1` to `geom2`. Returned distances are bounded from above by `distmax`.\
If no collision of distance smaller than `distmax` is found, the function will return `distmax` and `fromto`, if given, will be set to (0, 0, 0, 0, 0, 0).

*Nullable:* `fromto`

different (correct) behavior under `nativeccd`

As explained in [Collision Detection](../computation/index.md#codistance), distances are inaccurate when using the [legacy CCD pipeline](../computation/index.md#coccd), and its use is discouraged.

### [mj_insideSite](#mj_insideSite)

``` C
int mj_insideSite(const mjModel* m, const mjData* d, int siteid, const mjtNum point[3]);
```

Return 1 if point is inside a site (convex hull for meshes), 0 otherwise.

### [mj_contactForce](#mj_contactForce)

``` C
void mj_contactForce(const mjModel* m, const mjData* d, int id, mjtNum result[6]);
```

Extract 6D force:torque given contact id, in the contact frame.

### [mj_differentiatePos](#mj_differentiatePos)

``` C
void mj_differentiatePos(const mjModel* m, mjtNum* qvel, mjtNum dt,
                         const mjtNum* qpos1, const mjtNum* qpos2);
```

This function subtracts two vectors in the format of qpos (and divides the result by dt), while respecting the properties of quaternions. Recall that unit quaternions represent spatial orientations. They are points on the unit sphere in 4D. The tangent to that sphere is a 3D plane of rotational velocities. Thus when we subtract two quaternions in the right way, the result is a 3D vector and not a 4D vector. Thus the output qvel has dimensionality nv while the inputs have dimensionality nq.

### [mj_integratePos](#mj_integratePos)

``` C
void mj_integratePos(const mjModel* m, mjtNum* qpos, const mjtNum* qvel, mjtNum dt);
```

This is the opposite of mj_differentiatePos. It adds a vector in the format of qvel (scaled by dt) to a vector in the format of qpos.

### [mj_normalizeQuat](#mj_normalizeQuat)

``` C
void mj_normalizeQuat(const mjModel* m, mjtNum* qpos);
```

Normalize all quaternions in qpos-type vector.

### [mj_local2Global](#mj_local2Global)

``` C
void mj_local2Global(mjData* d, mjtNum xpos[3], mjtNum xmat[9], const mjtNum pos[3],
                     const mjtNum quat[4], int body, mjtByte sameframe);
```

Map from body local to global Cartesian coordinates, sameframe takes values from mjtSameFrame.

### [mj_getTotalmass](#mj_getTotalmass)

``` C
mjtNum mj_getTotalmass(const mjModel* m);
```

Sum all body masses.

### [mj_setTotalmass](#mj_setTotalmass)

``` C
void mj_setTotalmass(mjModel* m, mjtNum newmass);
```

Scale body masses and inertias to achieve specified total mass.

### [mj_getPluginConfig](#mj_getPluginConfig)

``` C
const char* mj_getPluginConfig(const mjModel* m, int plugin_id, const char* attrib);
```

Return a config attribute value of a plugin instance;

NULL: invalid plugin instance ID or attribute name

### [mj_loadPluginLibrary](#mj_loadPluginLibrary)

``` C
void mj_loadPluginLibrary(const char* path);
```

Load a dynamic library. The dynamic library is assumed to register one or more plugins.

### [mj_loadAllPluginLibraries](#mj_loadAllPluginLibraries)

``` C
void mj_loadAllPluginLibraries(const char* directory, mjfPluginLibraryLoadCallback callback);
```

Scan a directory and load all dynamic libraries. Dynamic libraries in the specified directory are assumed to register one or more plugins. Optionally, if a callback is specified, it is called for each dynamic library encountered that registers plugins. A library that fails to load is skipped with a warning.

### [mj_version](#mj_version)

``` C
int mj_version(void);
```

Return version number: 1.0.2 is encoded as 102.

### [mj_versionString](#mj_versionString)

``` C
const char* mj_versionString(void);
```

Return the current version of MuJoCo as a null-terminated string.

## Components

These are components of the simulation pipeline, called internally from [mj_step](#mj-step), [mj_forward](#mj-forward) and [mj_inverse](#mj-inverse). It is unlikely that the user will need to call them.

### [mj_fwdKinematics](#mj_fwdKinematics)

``` C
void mj_fwdKinematics(const mjModel* m, mjData* d);
```

Run all kinematics-like computations (kinematics, comPos, camlight, flex, tendon).

### [mj_fwdPosition](#mj_fwdPosition)

``` C
void mj_fwdPosition(const mjModel* m, mjData* d);
```

Run position-dependent computations.

### [mj_fwdVelocity](#mj_fwdVelocity)

``` C
void mj_fwdVelocity(const mjModel* m, mjData* d);
```

Run velocity-dependent computations.

### [mj_fwdActuation](#mj_fwdActuation)

``` C
void mj_fwdActuation(const mjModel* m, mjData* d);
```

Compute actuator force qfrc_actuator.

### [mj_fwdAcceleration](#mj_fwdAcceleration)

``` C
void mj_fwdAcceleration(const mjModel* m, mjData* d);
```

Add up all non-constraint forces, compute qacc_smooth.

### [mj_fwdConstraint](#mj_fwdConstraint)

``` C
void mj_fwdConstraint(const mjModel* m, mjData* d);
```

Run selected constraint solver.

### [mj_Euler](#mj_Euler)

``` C
void mj_Euler(const mjModel* m, mjData* d);
```

Euler integrator, semi-implicit in velocity.

### [mj_RungeKutta](#mj_RungeKutta)

``` C
void mj_RungeKutta(const mjModel* m, mjData* d, int N);
```

Runge-Kutta explicit order-N integrator.

### [mj_implicit](#mj_implicit)

``` C
void mj_implicit(const mjModel* m, mjData* d);
```

Integrates the simulation state using an implicit-in-velocity integrator (either “implicit” or “implicitfast”, see [Numerical Integration](../computation/index.md#geintegration)), and advances simulation time. See [mjdata.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjdata.h) for fields computed by this function.

### [mj_invPosition](#mj_invPosition)

``` C
void mj_invPosition(const mjModel* m, mjData* d);
```

Run position-dependent computations in inverse dynamics.

### [mj_invVelocity](#mj_invVelocity)

``` C
void mj_invVelocity(const mjModel* m, mjData* d);
```

Run velocity-dependent computations in inverse dynamics.

### [mj_invConstraint](#mj_invConstraint)

``` C
void mj_invConstraint(const mjModel* m, mjData* d);
```

Apply the analytical formula for inverse constraint dynamics.

### [mj_compareFwdInv](#mj_compareFwdInv)

``` C
void mj_compareFwdInv(const mjModel* m, mjData* d);
```

Compare forward and inverse dynamics, save results in fwdinv.

## Sub components

These are sub-components of the simulation pipeline, called internally from the components above.

### [mj_sensorPos](#mj_sensorPos)

``` C
void mj_sensorPos(const mjModel* m, mjData* d);
```

Evaluate position-dependent sensors.

### [mj_sensorVel](#mj_sensorVel)

``` C
void mj_sensorVel(const mjModel* m, mjData* d);
```

Evaluate velocity-dependent sensors.

### [mj_sensorAcc](#mj_sensorAcc)

``` C
void mj_sensorAcc(const mjModel* m, mjData* d);
```

Evaluate acceleration and force-dependent sensors.

### [mj_energyPos](#mj_energyPos)

``` C
void mj_energyPos(const mjModel* m, mjData* d);
```

Evaluate position-dependent energy (potential).

### [mj_energyVel](#mj_energyVel)

``` C
void mj_energyVel(const mjModel* m, mjData* d);
```

Evaluate velocity-dependent energy (kinetic).

### [mj_checkPos](#mj_checkPos)

``` C
void mj_checkPos(const mjModel* m, mjData* d);
```

Check qpos, reset if any element is too big or nan.

### [mj_checkVel](#mj_checkVel)

``` C
void mj_checkVel(const mjModel* m, mjData* d);
```

Check qvel, reset if any element is too big or nan.

### [mj_checkAcc](#mj_checkAcc)

``` C
void mj_checkAcc(const mjModel* m, mjData* d);
```

Check qacc, reset if any element is too big or nan.

### [mj_kinematics](#mj_kinematics)

``` C
void mj_kinematics(const mjModel* m, mjData* d);
```

Run forward kinematics.

### [mj_comPos](#mj_comPos)

``` C
void mj_comPos(const mjModel* m, mjData* d);
```

Map inertias and motion dofs to global frame centered at CoM.

### [mj_camlight](#mj_camlight)

``` C
void mj_camlight(const mjModel* m, mjData* d);
```

Compute camera and light positions and orientations.

### [mj_flex](#mj_flex)

``` C
void mj_flex(const mjModel* m, mjData* d);
```

Compute flex-related quantities.

### [mj_tendon](#mj_tendon)

``` C
void mj_tendon(const mjModel* m, mjData* d);
```

Compute tendon lengths, velocities and moment arms.

### [mj_transmission](#mj_transmission)

``` C
void mj_transmission(const mjModel* m, mjData* d);
```

Compute actuator transmission lengths and moments.

### [mj_crb](#mj_crb)

``` C
void mj_crb(const mjModel* m, mjData* d);
```

Run composite rigid body inertia algorithm (CRB).

### [mj_makeM](#mj_makeM)

``` C
void mj_makeM(const mjModel* m, mjData* d);
```

Compute the composite rigid body inertia with [mj_crb](#mj-crb), add terms due to [tendon armature](../XMLreference.md#tendon-spatial-armature). The joint-space inertia matrix is stored in both `mjData.qM` and `mjData.M`. These arrays represent the same quantity using different layouts (parent-based and compressed sparse row, respectively).

### [mj_factorM](#mj_factorM)

``` C
void mj_factorM(const mjModel* m, mjData* d);
```

Compute sparse \\L^T D L\\ factorizaton of inertia matrix.

### [mj_solveM](#mj_solveM)

``` C
void mj_solveM(const mjModel* m, mjData* d, mjtNum* x, const mjtNum* y, int n);
```

Solve linear system \\M x = y\\ using factorization: \\x = (L^T D L)^{-1} y\\

### [mj_solveM2](#mj_solveM2)

``` C
void mj_solveM2(const mjModel* m, mjData* d, mjtNum* x, const mjtNum* y,
                const mjtNum* sqrtInvD, int n);
```

Half of linear solve: \\x = \sqrt{D^{-1}} (L^T)^{-1} y\\

### [mj_comVel](#mj_comVel)

``` C
void mj_comVel(const mjModel* m, mjData* d);
```

Compute cvel, cdof_dot.

### [mj_passive](#mj_passive)

``` C
void mj_passive(const mjModel* m, mjData* d);
```

Compute qfrc_passive from spring-dampers, gravity compensation and fluid forces.

### [mj_subtreeVel](#mj_subtreeVel)

``` C
void mj_subtreeVel(const mjModel* m, mjData* d);
```

Sub-tree linear velocity and angular momentum: compute `subtree_linvel`, `subtree_angmom`. This function is triggered automatically if the subtree [velocity](../XMLreference.md#sensor-subtreelinvel) or [momentum](../XMLreference.md#sensor-subtreeangmom) sensors are present in the model. It is also triggered for [user sensors](../XMLreference.md#sensor-user) of [stage](../XMLreference.md#sensor-user-needstage) “vel”.

### [mj_rne](#mj_rne)

``` C
void mj_rne(const mjModel* m, mjData* d, int flg_acc, mjtNum* result);
```

Recursive Newton Euler: compute \\M(q) \ddot q + C(q,\dot q)\\. `flg_acc=0` removes the inertial term (i.e. assumes \\\ddot q = 0\\).

### [mj_rnePostConstraint](#mj_rnePostConstraint)

``` C
void mj_rnePostConstraint(const mjModel* m, mjData* d);
```

Recursive Newton Euler with final computed forces and accelerations. Computes three body-level `nv x 6` arrays, all defined in the subtreecom-based [c-frame](APItypes.md#tynotescom) and arranged in `[rotation(3), translation(3)]` order.

- `cacc`: Body acceleration, required for [mj_objectAcceleration](#mj-objectacceleration).

- `cfrc_int`: Interaction force with the parent body.

- `cfrc_ext`: External force acting on the body.

This function is triggered automatically if the following sensors are present in the model: [accelerometer](../XMLreference.md#sensor-accelerometer), [force](../XMLreference.md#sensor-force), [torque](../XMLreference.md#sensor-torque), [framelinacc](../XMLreference.md#sensor-framelinacc), [frameangacc](../XMLreference.md#sensor-frameangacc). It is also triggered for [user sensors](../XMLreference.md#sensor-user) of [stage](../XMLreference.md#sensor-user-needstage) “acc”.

`cfrc_ext` collects the forces that are not transmitted through the joints: applied Cartesian forces (`xfrc_applied`), contacts, connect and weld constraints, and spatial tendons (spring, damper, actuator, constraint and armature forces along the tendon path). `cfrc_int` is then the wrench transmitted through the joint, and its projection on the joint axes is the total joint-space force. Forces of actuators with site, slider-crank and body transmissions, gravity compensation, fluid forces, flex forces and custom passive forces are not yet collected and are attributed to the joints.

### [mj_maxContact](#mj_maxContact)

``` C
int mj_maxContact(const mjModel* m, int g1, int g2, int has_margin);
```

Return the maximum number of contacts that can be generated between two geoms.

If has_margin is -1, then the margin is pulled from the model, otherwise if has_margin \> 0 indicates that the geoms have a positive margin.

### [mj_collision](#mj_collision)

``` C
void mj_collision(const mjModel* m, mjData* d);
```

Run collision detection.

### [mj_makeConstraint](#mj_makeConstraint)

``` C
void mj_makeConstraint(const mjModel* m, mjData* d);
```

Construct constraints.

### [mj_island](#mj_island)

``` C
void mj_island(const mjModel* m, mjData* d);
```

Find constraint islands.

### [mj_projectConstraint](#mj_projectConstraint)

``` C
void mj_projectConstraint(const mjModel* m, mjData* d);
```

Compute inverse constraint inertia efc_AR.

### [mj_referenceConstraint](#mj_referenceConstraint)

``` C
void mj_referenceConstraint(const mjModel* m, mjData* d);
```

Compute efc_vel, efc_aref.

### [mj_constraintUpdate](#mj_constraintUpdate)

``` C
void mj_constraintUpdate(const mjModel* m, mjData* d, const mjtNum* jar, mjtNum cost[1]);
```

Compute `efc_state`, `efc_force`, and `qfrc_constraint`. If `cost` is not `NULL`, set `*cost = s(jar)` where `jar = Jac*qacc - aref`.

*Nullable:* `cost`

## Ray casting

Ray collisions, also known as ray casting, find the distance `x` of a ray’s intersection with a geom, where a ray is a line emanating from the 3D point `p` in the direction `v` i.e., `(p + x*v, x >= 0)`. All functions in this family return the distance to the nearest geom surface, or -1 if there is no intersection. Note that if `p` is inside a geom, the ray will intersect the surface from the inside which still counts as an intersection.

All ray collision functions rely on quantities computed by [mj_kinematics](#mj-kinematics) (see [mjData](APItypes.md#mjdata)), so must be called after [mj_kinematics](#mj-kinematics), or functions that call it (e.g. [mj_fwdPosition](#mj-fwdposition)). The top level functions, which intersect with all geoms types, are [mj_ray](#mj-ray) which casts a single ray, and [mj_multiRay](#mj-multiray) which casts multiple rays from a single point.

### [mj_ray](#mj_ray)

``` C
mjtNum mj_ray(const mjModel* m, const mjData* d, const mjtNum pnt[3], const mjtNum vec[3],
              const mjtByte* geomgroup, mjtBool flg_static, int bodyexclude,
              int geomid[1], mjtNum normal[3]);
```

Intersect ray `pnt+x*vec, x >= 0` with geoms.

- Return distance `x` to nearest surface, or -1 if no intersection.

- If `geomid` is not NULL, write the id of the intersected geom or -1 if not intersection.

- If `normal` is not NULL, write the surface normal at the intersection point. The normal always points **out of the geometry**, regardless of the ray’s direction (i.e., including rays hitting the surface from the inside).

- Exclude geoms in body with id `bodyexclude`, use -1 to include all bodies.

- `geomgroup` is an array of length [mjNGROUP](APIglobals.md#glnumericvisualization), where 1 means the group should be included. Pass NULL to skip geom group exclusion.

- If `flg_static` is 0, static geoms will be excluded.

*Nullable:* `geomgroup`, `geomid`, `normal`

### [mj_multiRay](#mj_multiRay)

``` C
void mj_multiRay(const mjModel* m, mjData* d, const mjtNum pnt[3], const mjtNum* vec,
                 const mjtByte* geomgroup, mjtBool flg_static, int bodyexclude,
                 int* geomid, mjtNum* dist, mjtNum* normal, int nray, mjtNum cutoff);
```

Intersect multiple rays emanating from a single point, compute normals if given.

Similar semantics to mj_ray, but vec, normal and dist are arrays.

Geoms further than cutoff are ignored.

*Nullable:* `geomgroup`, `geomid`, `normal`

### [mj_rayHfield](#mj_rayHfield)

``` C
mjtNum mj_rayHfield(const mjModel* m, const mjData* d, int geomid,
                    const mjtNum pnt[3], const mjtNum vec[3], mjtNum normal[3]);
```

Intersect ray with hfield; return nearest distance or -1 if no intersection.

*Nullable:* `normal`

### [mj_rayMesh](#mj_rayMesh)

``` C
mjtNum mj_rayMesh(const mjModel* m, const mjData* d, int geomid,
                  const mjtNum pnt[3], const mjtNum vec[3], mjtNum normal[3]);
```

Intersect ray with mesh; return nearest distance or -1 if no intersection.

*Nullable:* `normal`

### [mju_rayGeom](#mju_rayGeom)

``` C
mjtNum mju_rayGeom(const mjtNum pos[3], const mjtNum mat[9], const mjtNum size[3],
                   const mjtNum pnt[3], const mjtNum vec[3], int geomtype,
                   mjtNum normal[3]);
```

Intersect ray with pure geom; return nearest distance or -1 if no intersection.

*Nullable:* `normal`

### [mj_rayFlex](#mj_rayFlex)

``` C
mjtNum mj_rayFlex(const mjModel* m, const mjData* d, int flex_layer,
                  mjtBool flg_vert, mjtBool flg_edge, mjtBool flg_face,
                  mjtBool flg_skin, int flexid, const mjtNum pnt[3],
                  const mjtNum vec[3], int vertid[1], mjtNum normal[3]);
```

Intersect ray with flex; return nearest distance or -1 if no intersection, and also output nearest vertex id and surface normal.

*Nullable:* `vertid`, `normal`

### [mju_raySkin](#mju_raySkin)

``` C
mjtNum mju_raySkin(int nface, int nvert, const int* face, const float* vert,
                   const mjtNum pnt[3], const mjtNum vec[3], int vertid[1]);
```

Intersect ray with skin; return nearest distance or -1 if no intersection, and also output nearest vertex id.

*Nullable:* `vertid`

## Printing

These functions can be used to print various quantities to the screen for debugging purposes.

### [mj_printFormattedModel](#mj_printFormattedModel)

``` C
void mj_printFormattedModel(const mjModel* m, const char* filename, const char* float_format);
```

Print mjModel to text file, specifying format. float_format must be a valid printf-style format string for a single float value.

### [mj_printModel](#mj_printModel)

``` C
void mj_printModel(const mjModel* m, const char* filename);
```

Print model to text file.

### [mj_printFormattedData](#mj_printFormattedData)

``` C
void mj_printFormattedData(const mjModel* m, const mjData* d, const char* filename,
                           const char* float_format);
```

Print mjData to text file, specifying format. float_format must be a valid printf-style format string for a single float value.

### [mj_printData](#mj_printData)

``` C
void mj_printData(const mjModel* m, const mjData* d, const char* filename);
```

Print data to text file.

### [mju_printMat](#mju_printMat)

``` C
void mju_printMat(const mjtNum* mat, int nr, int nc);
```

Print matrix to screen.

### [mju_printMatSparse](#mju_printMatSparse)

``` C
void mju_printMatSparse(const mjtNum* mat, int nr,
                        const int* rownnz, const int* rowadr, const int* colind);
```

Print sparse matrix to screen.

### [mj_printSchema](#mj_printSchema)

``` C
int mj_printSchema(const char* filename, char* buffer, int buffer_sz,
                   int flg_html, int flg_pad);
```

Print internal XML schema as plain text or HTML, with style-padding or `&nbsp;`.

### [mj_printScene](#mj_printScene)

``` C
void mj_printScene(const mjvScene* s, const char* filename);
```

Print scene to text file.

### [mj_printFormattedScene](#mj_printFormattedScene)

``` C
void mj_printFormattedScene(const mjvScene* s, const char* filename,
                            const char* float_format);
```

Print scene to text file, specifying format. float_format must be a valid printf-style format string for a single float value.

## Virtual file system

Virtual file system (VFS) enables the user to load all necessary files in memory, including MJB binary model files, XML files (MJCF, URDF and included files), STL meshes, PNGs for textures and height fields, and HF files in our custom height field format. Model and resource files in the VFS can also be constructed programmatically (say using a Python library that writes to memory). Once all desired files are in the VFS, the user can call [mj_loadModel](#mj-loadmodel) or [mj_loadXML](#mj-loadxml) with a pointer to the VFS. When this pointer is not NULL, the loaders will first check the VFS for any files they are about to load, and only access the disk if the file is not found in the VFS.

The VFS must first be allocated using [mj_defaultVFS](#mj-defaultvfs) and must be freed with [mj_deleteVFS](#mj-deletevfs).

### [mj_defaultVFS](#mj_defaultVFS)

``` C
void mj_defaultVFS(mjVFS* vfs);
```

Initialize an empty VFS, [mj_deleteVFS](#mj-deletevfs) must be called to deallocate the VFS.

### [mj_mountVFS](#mj_mountVFS)

``` C
int mj_mountVFS(mjVFS* vfs, const char* filepath, const mjpResourceProvider* provider);
```

Mount a provider to handle file operations under the given path; return 0: success, 2: repeated name, -1: invalid provider.

### [mj_unmountVFS](#mj_unmountVFS)

``` C
int mj_unmountVFS(mjVFS* vfs, const char* filename);
```

Unmount a previously mounted provider; return 0: success, -1: not found in VFS.

### [mj_addFileVFS](#mj_addFileVFS)

``` C
int mj_addFileVFS(mjVFS* vfs, const char* directory, const char* filename);
```

Add file to VFS. The directory argument is optional and can be NULL or empty. Returns 0 on success, 2 on name collision, or -1 when an internal error occurs.

*Nullable:* `directory`

### [mj_addBufferVFS](#mj_addBufferVFS)

``` C
int mj_addBufferVFS(mjVFS* vfs, const char* name, const void* buffer, int nbuffer);
```

Add file to VFS from buffer; return 0: success, 2: repeated name, -1: failed to load.

### [mj_deleteFileVFS](#mj_deleteFileVFS)

``` C
int mj_deleteFileVFS(mjVFS* vfs, const char* filename);
```

Delete file from VFS; return 0: success, -1: not found in VFS.

### [mj_containsBufferVFS](#mj_containsBufferVFS)

``` C
int mj_containsBufferVFS(mjVFS* vfs, const char* name);
```

Check if buffer exists in VFS; return 1: exists, 0: not found.

### [mj_containsFileVFS](#mj_containsFileVFS)

``` C
int mj_containsFileVFS(mjVFS* vfs, const char* directory, const char* filename);
```

Check if file exists in VFS; return 1: exists, 0: not found.

### [mj_deleteVFS](#mj_deleteVFS)

``` C
void mj_deleteVFS(mjVFS* vfs);
```

Delete all files from VFS and deallocates VFS internal memory.

## Asset cache

The asset cache is a mechanism for caching assets (e.g. textures, meshes, etc.) to avoid repeated slow recompilation. The following methods provide way to control the capacity of the cache or to disable it altogether.

### [mj_getCacheSize](#mj_getCacheSize)

``` C
size_t mj_getCacheSize(const mjCache* cache);
```

Get the current size of the asset cache in bytes.

### [mj_getCacheCapacity](#mj_getCacheCapacity)

``` C
size_t mj_getCacheCapacity(const mjCache* cache);
```

Get the capacity of the asset cache in bytes.

### [mj_setCacheCapacity](#mj_setCacheCapacity)

``` C
size_t mj_setCacheCapacity(mjCache* cache, size_t size);
```

Set the capacity of the asset cache in bytes (0 to disable); return the new capacity.

### [mj_getCache](#mj_getCache)

``` C
mjCache* mj_getCache(void);
```

Get the internal asset cache used by the compiler.

### [mj_clearCache](#mj_clearCache)

``` C
void mj_clearCache(mjCache* cache);
```

Clear the asset cache.

## Resources

Resources are the interface between [resource providers](../programming/extension.md#exprovider) and MuJoCo model compilation code. These functions provide the means to query the resource provider and obtain resources.

### [mju_openResource](#mju_openResource)

``` C
mjResource* mju_openResource(const char* dir, const char* name,
                             const mjVFS* vfs, char* error, size_t nerror);
```

Open a resource; if the name doesn’t have a prefix matching a registered provider, then the OS filesystem is used.

*Nullable:* `dir`, `vfs`, `error`

### [mju_closeResource](#mju_closeResource)

``` C
void mju_closeResource(mjResource* resource);
```

Close a resource; no-op if resource is NULL.

### [mju_readResource](#mju_readResource)

``` C
int mju_readResource(mjResource* resource, const void** buffer);
```

Set buffer to bytes read from the resource and return number of bytes in buffer; return negative value if error.

### [mju_writeResource](#mju_writeResource)

``` C
mjtSize mju_writeResource(const char* name, const void* buffer, mjtSize nbytes,
                          const mjVFS* vfs, char* error, size_t nerror);
```

Write resource data via its provider, return bytes written or -1 on error.

*Nullable:* `vfs`, `error`

### [mju_getResourceDir](#mju_getResourceDir)

``` C
void mju_getResourceDir(mjResource* resource, const char** dir, int* ndir);
```

For a resource with a name partitioned as {dir}{filename}, get the dir and ndir pointers.

### [mju_isModifiedResource](#mju_isModifiedResource)

``` C
int mju_isModifiedResource(const mjResource* resource, const char* timestamp);
```

Compare resource timestamp to provided timestamp.

Return 0 if timestamps match, \>0 if resource is newer, \<0 if resource is older.

### [mju_decodeResource](#mju_decodeResource)

``` C
mjSpec* mju_decodeResource(mjResource* resource, const char* content_type,
                           const mjVFS* vfs, char* error, int error_sz);
```

Find the decoder for a resource and return the decoded spec.

The caller takes ownership of the spec and is responsible for cleaning it up.

On failure, return NULL and write the reason to error.

*Nullable:* `vfs`, `error`

## Initialization

This section contains functions that load/initialize the model or other data structures. Their use is well illustrated in the code samples.

### [mj_defaultLROpt](#mj_defaultLROpt)

``` C
void mj_defaultLROpt(mjLROpt* opt);
```

Set default options for length range computation.

### [mj_defaultSolRefImp](#mj_defaultSolRefImp)

``` C
void mj_defaultSolRefImp(mjtNum* solref, mjtNum* solimp);
```

Set solver parameters to default values.

*Nullable:* `solref`, `solimp`

### [mj_defaultOption](#mj_defaultOption)

``` C
void mj_defaultOption(mjOption* opt);
```

Set physics options to default values.

### [mj_defaultVisual](#mj_defaultVisual)

``` C
void mj_defaultVisual(mjVisual* vis);
```

Set visual options to default values.

### [mj_copyModel](#mj_copyModel)

``` C
mjModel* mj_copyModel(mjModel* dest, const mjModel* src);
```

Copy mjModel, allocate new if dest is NULL.

*Nullable:* `dest`

### [mj_saveModel](#mj_saveModel)

``` C
void mj_saveModel(const mjModel* m, const char* filename, void* buffer, mjtSize buffer_sz);
```

Save model to binary MJB file or memory buffer; buffer has precedence when given. The model is written as it is: a model with [by-reference](../modeling.md#cassetreference) textures keeps them as references, and the file loads wherever the paths resolve. A hermetic file is [mj_embedAssets](#mj-embedassets), then [mj_saveModel](#mj-savemodel) on the result, then [mj_deleteModel](#mj-deletemodel).

*Nullable:* `filename`, `buffer`

### [mj_loadModel](#mj_loadModel)

``` C
mjModel* mj_loadModel(const char* filename, const mjVFS* vfs);
```

Load model from binary MJB file.

If vfs is not NULL, look up file in vfs before reading from disk.

*Nullable:* `vfs`

### [mj_loadModelBuffer](#mj_loadModelBuffer)

``` C
mjModel* mj_loadModelBuffer(const void* buffer, mjtSize buffer_sz);
```

Load model from memory buffer.

### [mj_deleteModel](#mj_deleteModel)

``` C
void mj_deleteModel(mjModel* m);
```

Free memory allocation in model.

### [mj_sizeModel](#mj_sizeModel)

``` C
mjtSize mj_sizeModel(const mjModel* m);
```

Return size of buffer needed to hold model.

### [mj_makeData](#mj_makeData)

``` C
mjData* mj_makeData(const mjModel* m);
```

Allocate mjData corresponding to given model.

If the model buffer is unallocated the initial configuration will not be set.

### [mj_copyData](#mj_copyData)

``` C
mjData* mj_copyData(mjData* dest, const mjModel* m, const mjData* src);
```

Copy mjData. m is only required to contain the size fields from MJMODEL_INTS.

### [mjv_copyData](#mjv_copyData)

``` C
mjData* mjv_copyData(mjData* dest, const mjModel* m, const mjData* src);
```

Copy [mjData](APItypes.md#mjdata), skipping large arrays not required for visualization, like the constraint Jacobian. The copy is meant for visualization, e.g. with [mjv_updateScene](#mjv-updatescene); the skipped arrays are `NULL`, so it is not a valid input to simulation functions.

### [mj_resetCtrl](#mj_resetCtrl)

``` C
void mj_resetCtrl(const mjModel* m, mjData* d);
```

Reset ctrl to neutral values: zero, except quaternion inputs which reset to the identity.

### [mj_resetData](#mj_resetData)

``` C
void mj_resetData(const mjModel* m, mjData* d);
```

Reset data to defaults.

### [mj_resetDataDebug](#mj_resetDataDebug)

``` C
void mj_resetDataDebug(const mjModel* m, mjData* d, unsigned char debug_value);
```

Reset data to defaults, fill everything else with debug_value.

### [mj_resetDataKeyframe](#mj_resetDataKeyframe)

``` C
void mj_resetDataKeyframe(const mjModel* m, mjData* d, int key);
```

Reset data. If 0 \<= key \< nkey, set fields from specified keyframe.

### [mj_markStack](#mj_markStack)

``` C
void mj_markStack(mjData* d);
```

Mark a new frame on the mjData stack.

### [mj_freeStack](#mj_freeStack)

``` C
void mj_freeStack(mjData* d);
```

Free the current mjData stack frame. All pointers returned by mj_stackAlloc since the last call to mj_markStack must no longer be used afterwards.

### [mj_stackAllocByte](#mj_stackAllocByte)

``` C
void* mj_stackAllocByte(mjData* d, size_t bytes, size_t alignment);
```

Allocate a number of bytes on mjData stack at a specific alignment.

Call mju_error on stack overflow.

### [mj_stackAllocNum](#mj_stackAllocNum)

``` C
mjtNum* mj_stackAllocNum(mjData* d, size_t size);
```

Allocate array of mjtNums on mjData stack. Call mju_error on stack overflow.

### [mj_stackAllocInt](#mj_stackAllocInt)

``` C
int* mj_stackAllocInt(mjData* d, size_t size);
```

Allocate array of ints on mjData stack. Call mju_error on stack overflow.

### [mj_deleteData](#mj_deleteData)

``` C
void mj_deleteData(mjData* d);
```

Free memory allocation in mjData.

### [mj_resetCallbacks](#mj_resetCallbacks)

``` C
void mj_resetCallbacks(void);
```

Reset all callbacks to NULL pointers (NULL is the default).

### [mj_setConst](#mj_setConst)

``` C
void mj_setConst(mjModel* m, mjData* d);
```

Set constant fields of mjModel, corresponding to qpos0 configuration.

### [mj_setLengthRange](#mj_setLengthRange)

``` C
int mj_setLengthRange(mjModel* m, mjData* d, int index,
                      const mjLROpt* opt, char* error, int error_sz);
```

Set actuator_lengthrange for specified actuator; return 1 if ok, 0 if error.

*Nullable:* `error`

### [mj_makeSpec](#mj_makeSpec)

``` C
mjSpec* mj_makeSpec(void);
```

Create empty spec.

### [mj_copySpec](#mj_copySpec)

``` C
mjSpec* mj_copySpec(const mjSpec* s);
```

Copy spec.

### [mj_deleteSpec](#mj_deleteSpec)

``` C
void mj_deleteSpec(mjSpec* s);
```

Free memory allocation in mjSpec.

### [mjs_activatePlugin](#mjs_activatePlugin)

``` C
int mjs_activatePlugin(mjSpec* s, const char* name);
```

Activate plugin; return 0 on success.

### [mjs_setDeepCopy](#mjs_setDeepCopy)

``` C
int mjs_setDeepCopy(mjSpec* s, int deepcopy);
```

Turn deep copy on or off attach; return 0 on success.

## Error and memory

### [mju_error](#mju_error)

``` C
void mju_error(const char* msg, ...) mjPRINTFLIKE(1, 2);
```

Main error function. The error message is dispatched to the active log handler (see [mju_setLogHandler](#mju-setloghandler)). Errors are always fatal: if the handler returns, the process is terminated with `exit(EXIT_FAILURE)`. Handlers wishing to recover must `longjmp` or otherwise transfer control before returning.

### [mju_warning](#mju_warning)

``` C
void mju_warning(const char* msg, ...) mjPRINTFLIKE(1, 2);
```

Main warning function; returns to caller. The warning message is dispatched to the active log handler.

### [mju_clearHandlers](#mju_clearHandlers)

``` C
void mju_clearHandlers(void);
```

Clear all user handlers and restore defaults. Resets the legacy error/warning/memory callbacks to `NULL`, restores the default log handler, and resets the log configuration to its defaults (console and file output enabled, all info topics disabled).

### [mju_setLogHandler](#mju_setLogHandler)

``` C
mjfLogHandler mju_setLogHandler(mjfLogHandler handler);
```

Set the active global log handler. Returns the previous handler (which is never `NULL`), intended for save/restore or callback chaining. If `handler` is `NULL`, the default handler is restored. The handler receives all errors, warnings and informational messages as a structured [mjLogMessage](APItypes.md#mjlogmessage). See [Installing a handler](../programming/simulation.md#siloghandler) for usage examples.

### [mju_getLogConfig](#mju_getLogConfig)

``` C
mjLogConfig mju_getLogConfig(void);
```

Get the current default handler configuration. See [mjLogConfig](APItypes.md#mjlogconfig).

### [mju_setLogConfig](#mju_setLogConfig)

``` C
void mju_setLogConfig(mjLogConfig config);
```

Set the default handler configuration. Controls console output, file output, and info topic filtering. See [mjLogConfig](APItypes.md#mjlogconfig).

Example usage (disabling file output):

``` C
mjLogConfig config = mju_getLogConfig();
config.logto_file = false;
mju_setLogConfig(config);
```

### [mju_info](#mju_info)

``` C
void mju_info(int topic, const char* msg, ...) mjPRINTFLIKE(2, 3);
```

Log an informational message with optional topic filtering. The `topic` argument is a [mjtLogTopic](APItypes.md#mjtlogtopic) value. Topic 0 (`mjTOPIC_NONE`) always passes through. Other topics must be enabled in the default handler configuration via [mju_setLogConfig](#mju-setlogconfig). Note that topic filtering is implemented in the default handler; custom handlers receive all info messages regardless.

### [mju_message](#mju_message)

``` C
void mju_message(const mjLogMessage* msg);
```

Dispatch a structured [mjLogMessage](APItypes.md#mjlogmessage) to the active log handler. This is the primary entry point for emitting log messages with full control over all fields. The convenience functions [mju_error](#mju-error), [mju_warning](#mju-warning), and [mju_info](#mju-info) are thin wrappers that populate an `mjLogMessage` and call this function.

The `subject` field is a one-line summary (up to 1024 bytes, inline in the struct). The `body` field is an optional `const char*` pointer to multi-line detail text, owned by the caller. When `body` is `NULL`, only the subject line is printed.

The default handler formats the output as follows:

    LEVEL FUNC (FILE:LINE) TIME: SUBJECT
    BODY

where:

- `LEVEL` is `ERROR`, `WARNING`, `INFO`, or `DEBUG`.

- `FUNC` is present when the `func` field is set.

- `(FILE:LINE)` is present when the `file` and `line` fields are set.

- `TIME` is present when the `timestamp` field is set or file logging is active.

- `SUBJECT` is the contents of the `subject` field.

- `BODY` follows on the next line(s), printed raw without indentation or separators, only if non-NULL.

The default handler appends a trailing blank line after `ERROR`, `WARNING`, and `INFO` messages for visual separation. `DEBUG` messages are printed compactly without a trailing blank line.

Example usage:

``` C
mjLogMessage msg = {
  .level = mjLOG_INFO,
  .timestamp = true,
  .body = "  height:     0.001 m\n  velocity:   0.000 m/s\n  bounces:    47",
};
snprintf(msg.subject, sizeof(msg.subject), "The ball has come to rest");
mju_message(&msg);
```

This produces:

    INFO Mon Jun  9 15:04:05 2026: The ball has come to rest
      height:     0.001 m
      velocity:   0.000 m/s
      bounces:    47

### [mju_malloc](#mju_malloc)

``` C
void* mju_malloc(size_t size);
```

Allocate memory; byte-align on 64; pad size to multiple of 64.

### [mju_free](#mju_free)

``` C
void mju_free(void* ptr);
```

Free memory, using free() by default.

### [mj_warning](#mj_warning)

``` C
void mj_warning(mjData* d, int warning, int info);
```

High-level warning function: count warnings in mjData, print only the first.

### [mju_writeLog](#mju_writeLog)

``` C
void mju_writeLog(const char* type, const char* msg);
```

Write \[datetime, type: message\] to MUJOCO_LOG.TXT.

### [mjs_getError](#mjs_getError)

``` C
const char* mjs_getError(mjSpec* s);
```

Get compiler error message from spec.

### [mjs_getTimer](#mjs_getTimer)

``` C
const double* mjs_getTimer(mjSpec* s);
```

Get compiler timing diagnostics from spec, returns pointer to array of size mjNCTIMER.

### [mjs_isWarning](#mjs_isWarning)

``` C
int mjs_isWarning(mjSpec* s);
```

Return 1 if compiler error is a warning. Deprecated: use mjs_numWarnings(s) \> 0.

### [mjs_numWarnings](#mjs_numWarnings)

``` C
int mjs_numWarnings(const mjSpec* spec);
```

Get number of warnings accumulated in the spec.

### [mjs_getWarning](#mjs_getWarning)

``` C
const char* mjs_getWarning(const mjSpec* spec, int index);
```

Get the i-th warning message (returns nullptr if index out of bounds).

## Miscellaneous

### [mju_muscleGain](#mju_muscleGain)

``` C
mjtNum mju_muscleGain(mjtNum len, mjtNum vel, const mjtNum lengthrange[2],
                      mjtNum acc0, const mjtNum prm[9]);
```

Muscle active force, prm = (range\[2\], force, scale, lmin, lmax, vmax, fpmax, fvmax).

### [mju_muscleBias](#mju_muscleBias)

``` C
mjtNum mju_muscleBias(mjtNum len, const mjtNum lengthrange[2],
                      mjtNum acc0, const mjtNum prm[9]);
```

Muscle passive force, prm = (range\[2\], force, scale, lmin, lmax, vmax, fpmax, fvmax).

### [mju_muscleDynamics](#mju_muscleDynamics)

``` C
mjtNum mju_muscleDynamics(mjtNum ctrl, mjtNum act, const mjtNum prm[3]);
```

Muscle activation dynamics, prm = (tau_act, tau_deact, smoothing_width).

### [mju_encodePyramid](#mju_encodePyramid)

``` C
void mju_encodePyramid(mjtNum* pyramid, const mjtNum* force, const mjtNum* mu, int dim);
```

Convert contact force to pyramid representation.

### [mju_decodePyramid](#mju_decodePyramid)

``` C
void mju_decodePyramid(mjtNum* force, const mjtNum* pyramid, const mjtNum* mu, int dim);
```

Convert pyramid representation to contact force.

### [mju_springDamper](#mju_springDamper)

``` C
mjtNum mju_springDamper(mjtNum pos0, mjtNum vel0, mjtNum Kp, mjtNum Kv, mjtNum dt);
```

Integrate spring-damper analytically; return pos(dt).

### [mju_min](#mju_min)

``` C
mjtNum mju_min(mjtNum a, mjtNum b);
```

Return min(a,b) with single evaluation of a and b.

### [mju_max](#mju_max)

``` C
mjtNum mju_max(mjtNum a, mjtNum b);
```

Return max(a,b) with single evaluation of a and b.

### [mju_clip](#mju_clip)

``` C
mjtNum mju_clip(mjtNum x, mjtNum min, mjtNum max);
```

Clip x to the range \[min, max\].

### [mju_sign](#mju_sign)

``` C
mjtNum mju_sign(mjtNum x);
```

Return sign of x: +1, -1 or 0.

### [mju_round](#mju_round)

``` C
int mju_round(mjtNum x);
```

Round x to nearest integer.

### [mju_type2Str](#mju_type2Str)

``` C
const char* mju_type2Str(int type);
```

Convert type id (mjtObj) to type name.

### [mju_str2Type](#mju_str2Type)

``` C
int mju_str2Type(const char* str);
```

Convert type name to type id (mjtObj).

### [mju_writeNumBytes](#mju_writeNumBytes)

``` C
const char* mju_writeNumBytes(size_t nbytes);
```

Return human readable number of bytes using standard letter suffix.

### [mju_warningText](#mju_warningText)

``` C
const char* mju_warningText(int warning, size_t info);
```

Construct a warning message given the warning type and info.

### [mju_isBad](#mju_isBad)

``` C
int mju_isBad(mjtNum x);
```

Return 1 if nan or abs(x)\>mjMAXVAL, 0 otherwise. Used by check functions.

### [mju_isZero](#mju_isZero)

``` C
int mju_isZero(const mjtNum* vec, int n);
```

Return 1 if all elements are 0.

### [mju_standardNormal](#mju_standardNormal)

``` C
mjtNum mju_standardNormal(mjtNum* num2);
```

Standard normal random number generator (optional second number).

### [mju_f2n](#mju_f2n)

``` C
void mju_f2n(mjtNum* res, const float* vec, int n);
```

Convert from float to mjtNum.

### [mju_n2f](#mju_n2f)

``` C
void mju_n2f(float* res, const mjtNum* vec, int n);
```

Convert from mjtNum to float.

### [mju_d2n](#mju_d2n)

``` C
void mju_d2n(mjtNum* res, const double* vec, int n);
```

Convert from double to mjtNum.

### [mju_n2d](#mju_n2d)

``` C
void mju_n2d(double* res, const mjtNum* vec, int n);
```

Convert from mjtNum to double.

### [mju_insertionSort](#mju_insertionSort)

``` C
void mju_insertionSort(mjtNum* list, int n);
```

Insertion sort, resulting list is in increasing order.

### [mju_insertionSortInt](#mju_insertionSortInt)

``` C
void mju_insertionSortInt(int* list, int n);
```

Integer insertion sort, resulting list is in increasing order.

### [mju_Halton](#mju_Halton)

``` C
mjtNum mju_Halton(int index, int base);
```

Generate Halton sequence.

### [mju_strncpy](#mju_strncpy)

``` C
char* mju_strncpy(char *dst, const char *src, int n);
```

Call strncpy, then set dst\[n-1\] = 0.

### [mju_sigmoid](#mju_sigmoid)

``` C
mjtNum mju_sigmoid(mjtNum x);
```

Twice continuously differentiable sigmoid function using a quintic polynomial:

\\s(x) = \begin{cases} 0, & & x \le 0 \\ 6x^5 - 15x^4 + 10x^3, & 0 \lt & x \lt 1 \\ 1, & 1 \le & x \qquad \end{cases} \\

## Interaction

These functions implement abstract mouse interactions, allowing control over cameras and perturbations. Their use is well illustrated in [simulate](../programming/samples.md#sasimulate).

### [mjv_defaultCamera](#mjv_defaultCamera)

``` C
void mjv_defaultCamera(mjvCamera* cam);
```

Set default camera.

### [mjv_defaultFreeCamera](#mjv_defaultFreeCamera)

``` C
void mjv_defaultFreeCamera(const mjModel* m, mjvCamera* cam);
```

Set default free camera.

### [mjv_defaultPerturb](#mjv_defaultPerturb)

``` C
void mjv_defaultPerturb(mjvPerturb* pert);
```

Set default perturbation.

### [mjv_room2model](#mjv_room2model)

``` C
void mjv_room2model(mjtNum modelpos[3], mjtNum modelquat[4], const mjtNum roompos[3],
                    const mjtNum roomquat[4], const mjvScene* scn);
```

Transform pose from room to model space.

### [mjv_model2room](#mjv_model2room)

``` C
void mjv_model2room(mjtNum roompos[3], mjtNum roomquat[4], const mjtNum modelpos[3],
                    const mjtNum modelquat[4], const mjvScene* scn);
```

Transform pose from model to room space.

### [mjv_cameraInModel](#mjv_cameraInModel)

``` C
void mjv_cameraInModel(mjtNum headpos[3], mjtNum forward[3], mjtNum up[3],
                       const mjvScene* scn);
```

Get camera info in model space; average left and right OpenGL cameras.

### [mjv_cameraInRoom](#mjv_cameraInRoom)

``` C
void mjv_cameraInRoom(mjtNum headpos[3], mjtNum forward[3], mjtNum up[3],
                      const mjvScene* scn);
```

Get camera info in room space; average left and right OpenGL cameras.

### [mjv_frustumHeight](#mjv_frustumHeight)

``` C
mjtNum mjv_frustumHeight(const mjvScene* scn);
```

Get frustum height at unit distance from camera; average left and right OpenGL cameras.

### [mjv_alignToCamera](#mjv_alignToCamera)

``` C
void mjv_alignToCamera(mjtNum res[3], const mjtNum vec[3], const mjtNum forward[3]);
```

Rotate 3D vec in horizontal plane by angle between (0,1) and (forward_x,forward_y).

### [mjv_moveCamera](#mjv_moveCamera)

``` C
void mjv_moveCamera(const mjModel* m, int action, mjtNum reldx, mjtNum reldy, mjvCamera* cam);
```

Move camera with mouse; action is mjtMouse.

### [mjv_movePerturb](#mjv_movePerturb)

``` C
void mjv_movePerturb(const mjModel* m, const mjData* d, int action, mjtNum reldx,
                     mjtNum reldy, const mjvScene* scn, mjvPerturb* pert);
```

Move perturb object with mouse; action is mjtMouse.

### [mjv_moveModel](#mjv_moveModel)

``` C
void mjv_moveModel(const mjModel* m, int action, mjtNum reldx, mjtNum reldy,
                   const mjtNum roomup[3], mjvScene* scn);
```

Move model with mouse; action is mjtMouse.

### [mjv_initPerturb](#mjv_initPerturb)

``` C
void mjv_initPerturb(const mjModel* m, mjData* d, const mjvScene* scn, mjvPerturb* pert);
```

Copy perturb pos,quat from selected body; set scale for perturbation.

### [mjv_applyPerturbPose](#mjv_applyPerturbPose)

``` C
void mjv_applyPerturbPose(const mjModel* m, mjData* d, const mjvPerturb* pert,
                          int flg_paused);
```

Set perturb pos,quat in d-\>mocap when selected body is mocap, and in d-\>qpos otherwise.

Write d-\>qpos only if flg_paused and subtree root for selected body has free joint.

### [mjv_applyPerturbForce](#mjv_applyPerturbForce)

``` C
void mjv_applyPerturbForce(const mjModel* m, mjData* d, const mjvPerturb* pert);
```

Set perturb force,torque in d-\>xfrc_applied, if selected body is dynamic.

### [mjv_averageCamera](#mjv_averageCamera)

``` C
mjvGLCamera mjv_averageCamera(const mjvGLCamera* cam1, const mjvGLCamera* cam2);
```

Return the average of two OpenGL cameras.

### [mjv_camera2GLCamera](#mjv_camera2GLCamera)

``` C
mjvGLCamera mjv_camera2GLCamera(const mjModel* model, const mjData* data,
                                const mjvCamera* mjv_camera);
```

Converts a mjvCamera to a mjvGLCamera.

### [mjv_select](#mjv_select)

``` C
int mjv_select(const mjModel* m, const mjData* d, const mjvOption* vopt,
               mjtNum aspectratio, mjtNum relx, mjtNum rely,
               const mjvScene* scn, mjtNum selpnt[3],
               int geomid[1], int flexid[1], int skinid[1]);
```

This function is used for mouse selection, relying on ray intersections. aspectratio is the viewport width/height. relx and rely are the relative coordinates of the 2D point of interest in the viewport (usually mouse cursor). The function returns the id of the geom under the specified 2D point, or -1 if there is no geom (note that they skybox if present is not a model geom). The 3D coordinates of the clicked point are returned in selpnt. See [simulate](../programming/samples.md#sasimulate) for an illustration.

## Visualization

The functions in this section implement abstract visualization. The results are used by the OpenGL renderer, and can also be used by users wishing to implement their own renderer, or hook up MuJoCo to advanced rendering tools such as Unity or Unreal Engine. See [simulate](../programming/samples.md#sasimulate) for illustration of how to use these functions.

### [mjv_defaultOption](#mjv_defaultOption)

``` C
void mjv_defaultOption(mjvOption* opt);
```

Set default visualization options.

### [mjv_defaultFigure](#mjv_defaultFigure)

``` C
void mjv_defaultFigure(mjvFigure* fig);
```

Set default figure.

### [mjv_initGeom](#mjv_initGeom)

``` C
void mjv_initGeom(mjvGeom* geom, int type, const mjtNum size[3],
                  const mjtNum pos[3], const mjtNum mat[9], const float rgba[4]);
```

Initialize given geom fields when not NULL, set the rest to their default values.

*Nullable:* `size`, `pos`, `mat`, `rgba`

### [mjv_connector](#mjv_connector)

``` C
void mjv_connector(mjvGeom* geom, int type, mjtNum width,
                   const mjtNum from[3], const mjtNum to[3]);
```

Set (type, size, pos, mat) for connector-type geom between given points.

Assume that mjv_initGeom was already called to set all other properties.

Width of mjGEOM_LINE is denominated in pixels.

### [mjv_defaultScene](#mjv_defaultScene)

``` C
void mjv_defaultScene(mjvScene* scn);
```

Set default abstract scene.

### [mjv_makeScene](#mjv_makeScene)

``` C
void mjv_makeScene(const mjModel* m, mjvScene* scn, int maxgeom);
```

Allocate resources in abstract scene.

### [mjv_freeScene](#mjv_freeScene)

``` C
void mjv_freeScene(mjvScene* scn);
```

Free abstract scene.

### [mjv_updateScene](#mjv_updateScene)

``` C
void mjv_updateScene(const mjModel* m, mjData* d, const mjvOption* opt,
                     const mjvPerturb* pert, mjvCamera* cam, int catmask, mjvScene* scn);
```

Update entire scene given model state.

### [mjv_copyModel](#mjv_copyModel)

``` C
void mjv_copyModel(mjModel* dest, const mjModel* src);
```

Copy mjModel, skip large arrays not required for abstract visualization.

*Nullable:* `dest`

### [mjv_addGeoms](#mjv_addGeoms)

``` C
void mjv_addGeoms(const mjModel* m, mjData* d, const mjvOption* opt,
                  const mjvPerturb* pert, int catmask, mjvScene* scn);
```

Add geoms from selected categories.

### [mjv_makeLights](#mjv_makeLights)

``` C
void mjv_makeLights(const mjModel* m, const mjData* d, mjvScene* scn);
```

Make list of lights.

### [mjv_updateCamera](#mjv_updateCamera)

``` C
void mjv_updateCamera(const mjModel* m, const mjData* d, mjvCamera* cam, mjvScene* scn);
```

Update camera.

### [mjv_updateSkin](#mjv_updateSkin)

``` C
void mjv_updateSkin(const mjModel* m, const mjData* d, mjvScene* scn);
```

Update skins.

### [mjv_cameraFrame](#mjv_cameraFrame)

``` C
void mjv_cameraFrame(mjtNum headpos[3], mjtNum forward[3], mjtNum up[3], mjtNum right[3],
                     const mjData* d, const mjvCamera* cam);
```

Compute camera position and forward, up, and right vectors.

*Nullable:* `headpos`, `forward`, `up`, `right`

### [mjv_cameraFrustum](#mjv_cameraFrustum)

``` C
void mjv_cameraFrustum(float zver[2], float zhor[2], float zclip[2],  const mjModel* m,
                       const mjvCamera* cam);
```

Compute camera frustum: vertical, horizontal, and clip planes.

*Nullable:* `zver`, `zhor`, `zclip`

## OpenGL rendering

These functions expose the OpenGL renderer. See [simulate](../programming/samples.md#sasimulate) for an illustration of how to use these functions.

### [mjr_defaultContext](#mjr_defaultContext)

``` C
void mjr_defaultContext(mjrContext* con);
```

Set default mjrContext.

### [mjr_defaultRendererInfo](#mjr_defaultRendererInfo)

``` C
void mjr_defaultRendererInfo(mjrRendererInfo* info);
```

Set default mjrRendererInfo.

### [mjr_getRendererInfo](#mjr_getRendererInfo)

``` C
void mjr_getRendererInfo(mjrRendererInfo* info);
```

Get active renderer information.

### [mjr_makeContext](#mjr_makeContext)

``` C
void mjr_makeContext(const mjModel* m, mjrContext* con, int fontscale);
```

Allocate resources in custom OpenGL context; fontscale is mjtFontScale.

### [mjr_changeFont](#mjr_changeFont)

``` C
void mjr_changeFont(int fontscale, mjrContext* con);
```

Change font of existing context.

### [mjr_addAux](#mjr_addAux)

``` C
void mjr_addAux(int index, int width, int height, int samples, mjrContext* con);
```

Add Aux buffer with given index to context; free previous Aux buffer.

### [mjr_freeContext](#mjr_freeContext)

``` C
void mjr_freeContext(mjrContext* con);
```

Free resources in custom OpenGL context, set to default.

### [mjr_resizeOffscreen](#mjr_resizeOffscreen)

``` C
void mjr_resizeOffscreen(int width, int height, mjrContext* con);
```

Resize offscreen buffers.

### [mjr_uploadTexture](#mjr_uploadTexture)

``` C
void mjr_uploadTexture(const mjModel* m, const mjrContext* con, int texid);
```

Upload texture to GPU, overwriting previous upload if any. A by-reference texture (tex_adr == -1) is decoded with mj_loadTexture.

### [mjr_uploadMesh](#mjr_uploadMesh)

``` C
void mjr_uploadMesh(const mjModel* m, const mjrContext* con, int meshid);
```

Upload mesh to GPU, overwriting previous upload if any.

### [mjr_uploadHField](#mjr_uploadHField)

``` C
void mjr_uploadHField(const mjModel* m, const mjrContext* con, int hfieldid);
```

Upload height field to GPU, overwriting previous upload if any.

### [mjr_restoreBuffer](#mjr_restoreBuffer)

``` C
void mjr_restoreBuffer(const mjrContext* con);
```

Make con-\>currentBuffer current again.

### [mjr_setBuffer](#mjr_setBuffer)

``` C
void mjr_setBuffer(int framebuffer, mjrContext* con);
```

Set OpenGL framebuffer for rendering: mjFB_WINDOW or mjFB_OFFSCREEN.

If only one buffer is available, set that buffer and ignore framebuffer argument.

### [mjr_readPixels](#mjr_readPixels)

``` C
void mjr_readPixels(unsigned char* rgb, float* depth,
                    mjrRect viewport, const mjrContext* con);
```

Read pixels from current OpenGL framebuffer to client buffer.

Viewport is in OpenGL framebuffer; client buffer starts at (0,0).

### [mjr_drawPixels](#mjr_drawPixels)

``` C
void mjr_drawPixels(const unsigned char* rgb, const float* depth,
                    mjrRect viewport, const mjrContext* con);
```

Draw pixels from client buffer to current OpenGL framebuffer.

Viewport is in OpenGL framebuffer; client buffer starts at (0,0).

### [mjr_blitBuffer](#mjr_blitBuffer)

``` C
void mjr_blitBuffer(mjrRect src, mjrRect dst,
                    int flg_color, int flg_depth, const mjrContext* con);
```

Blit from src viewpoint in current framebuffer to dst viewport in other framebuffer.

If src, dst have different size and flg_depth==0, color is interpolated with GL_LINEAR.

### [mjr_setAux](#mjr_setAux)

``` C
void mjr_setAux(int index, const mjrContext* con);
```

Set Aux buffer for custom OpenGL rendering (call restoreBuffer when done).

### [mjr_blitAux](#mjr_blitAux)

``` C
void mjr_blitAux(int index, mjrRect src, int left, int bottom, const mjrContext* con);
```

Blit from Aux buffer to con-\>currentBuffer.

### [mjr_text](#mjr_text)

``` C
void mjr_text(int font, const char* txt, const mjrContext* con,
              float x, float y, float r, float g, float b);
```

Draw text at (x,y) in relative coordinates; font is mjtFont.

### [mjr_overlay](#mjr_overlay)

``` C
void mjr_overlay(int font, int gridpos, mjrRect viewport,
                 const char* overlay, const char* overlay2, const mjrContext* con);
```

Draw text overlay; font is mjtFont; gridpos is mjtGridPos.

### [mjr_maxViewport](#mjr_maxViewport)

``` C
mjrRect mjr_maxViewport(const mjrContext* con);
```

Get maximum viewport for active buffer.

### [mjr_rectangle](#mjr_rectangle)

``` C
void mjr_rectangle(mjrRect viewport, float r, float g, float b, float a);
```

Draw rectangle.

### [mjr_label](#mjr_label)

``` C
void mjr_label(mjrRect viewport, int font, const char* txt,
               float r, float g, float b, float a, float rt, float gt, float bt,
               const mjrContext* con);
```

Draw rectangle with centered text.

### [mjr_figure](#mjr_figure)

``` C
void mjr_figure(mjrRect viewport, mjvFigure* fig, const mjrContext* con);
```

Draw 2D figure.

### [mjr_render](#mjr_render)

``` C
void mjr_render(mjrRect viewport, mjvScene* scn, const mjrContext* con);
```

Render 3D scene.

### [mjr_finish](#mjr_finish)

``` C
void mjr_finish(void);
```

Call glFinish.

### [mjr_getError](#mjr_getError)

``` C
int mjr_getError(void);
```

Call glGetError and return result.

### [mjr_findRect](#mjr_findRect)

``` C
int mjr_findRect(int x, int y, int nrect, const mjrRect* rect);
```

Find first rectangle containing mouse, -1: not found.

## Filament rendering

Rendering functions using the Filament rendering engine. These functions are prefixed with `mjrf`. See [Filament Rendering](APItypes.md#tyfilamentrenderstructure) for an overview of the core types and their uses.

### [mjrf_defaultContextConfig](#mjrf_defaultContextConfig)

``` C
void mjrf_defaultContextConfig(mjrfContextConfig* config);
```

Initializes the mjrfContextConfig to default values.

### [mjrf_createContext](#mjrf_createContext)

``` C
mjrfContext* mjrf_createContext(const mjrfContextConfig* config);
```

Creates a filament rendering context.

### [mjrf_destroyContext](#mjrf_destroyContext)

``` C
void mjrf_destroyContext(mjrfContext* ctx);
```

Destroys the filament rendering context.

### [mjrf_getRendererInfo](#mjrf_getRendererInfo)

``` C
void mjrf_getRendererInfo(mjrfContext* ctx, mjrRendererInfo* info);
```

Gets active renderer information for the given filament context.

### [mjrf_defaultShadowOpts](#mjrf_defaultShadowOpts)

``` C
void mjrf_defaultShadowOpts(mjrfShadowOpts* opts);
```

Initializes the mjrfShadowOpts to default values.

### [mjrf_defaultMaterialOpts](#mjrf_defaultMaterialOpts)

``` C
void mjrf_defaultMaterialOpts(mjrfMaterialOpts* opts);
```

Initializes the mjrfMaterialOpts to default values.

### [mjrf_defaultHeadlightOpts](#mjrf_defaultHeadlightOpts)

``` C
void mjrf_defaultHeadlightOpts(mjrfHeadlightOpts* opts);
```

Initializes the mjrfHeadlightOpts to default values.

### [mjrf_defaultSkyboxOpts](#mjrf_defaultSkyboxOpts)

``` C
void mjrf_defaultSkyboxOpts(mjrfSkyboxOpts* opts);
```

Initializes the mjrfSkyboxOpts to default values.

### [mjrf_defaultHazeOpts](#mjrf_defaultHazeOpts)

``` C
void mjrf_defaultHazeOpts(mjrfHazeOpts* opts);
```

Initializes the mjrfHazeOpts to default values.

### [mjrf_defaultFogOpts](#mjrf_defaultFogOpts)

``` C
void mjrf_defaultFogOpts(mjrfFogOpts* opts);
```

Initializes the mjrfFogOpts to default values.

### [mjrf_defaultBloomOpts](#mjrf_defaultBloomOpts)

``` C
void mjrf_defaultBloomOpts(mjrfBloomOpts* opts);
```

Initializes the mjrfBloomOpts to default values.

### [mjrf_defaultVignetteOpts](#mjrf_defaultVignetteOpts)

``` C
void mjrf_defaultVignetteOpts(mjrfVignetteOpts* opts);
```

Initializes the mjrfVignetteOpts to default values.

### [mjrf_defaultReflectionOpts](#mjrf_defaultReflectionOpts)

``` C
void mjrf_defaultReflectionOpts(mjrfReflectionOpts* opts);
```

Initializes the mjrfReflectionOpts to default values.

### [mjrf_defaultDepthOfFieldOpts](#mjrf_defaultDepthOfFieldOpts)

``` C
void mjrf_defaultDepthOfFieldOpts(mjrfDepthOfFieldOpts* opts);
```

Initializes the mjrfDepthOfFieldOpts to default values.

### [mjrf_defaultDitheringOpts](#mjrf_defaultDitheringOpts)

``` C
void mjrf_defaultDitheringOpts(mjrfDitheringOpts* opts);
```

Initializes the mjrfDitheringOpts to default values.

### [mjrf_defaultColorGradingOpts](#mjrf_defaultColorGradingOpts)

``` C
void mjrf_defaultColorGradingOpts(mjrfColorGradingOpts* opts);
```

Initializes the mjrfColorGradingOpts to default values.

### [mjrf_defaultAntialiasingOpts](#mjrf_defaultAntialiasingOpts)

``` C
void mjrf_defaultAntialiasingOpts(mjrfAntialiasingOpts* opts);
```

Initializes the mjrfAntialiasingOpts to default values.

### [mjrf_defaultAmbientOcclusionOpts](#mjrf_defaultAmbientOcclusionOpts)

``` C
void mjrf_defaultAmbientOcclusionOpts(mjrfAmbientOcclusionOpts* opts);
```

Initializes the mjrfAmbientOcclusionOpts to default values.

### [mjrf_defaultRenderOpts](#mjrf_defaultRenderOpts)

``` C
void mjrf_defaultRenderOpts(mjrfRenderOpts* opts);
```

Initializes the mjrfRenderOpts to default values.

### [mjrf_modelRenderOpts](#mjrf_modelRenderOpts)

``` C
void mjrf_modelRenderOpts(mjrfRenderOpts* opts, const mjModel* model);
```

Configures the rendering options based on the parameters in an mjModel.

### [mjrf_defaultRenderRequest](#mjrf_defaultRenderRequest)

``` C
void mjrf_defaultRenderRequest(mjrfRenderRequest* request);
```

Initializes the mjrfRenderRequest to default values.

### [mjrf_defaultReadRequest](#mjrf_defaultReadRequest)

``` C
void mjrf_defaultReadRequest(mjrfReadRequest* request);
```

Initializes the mjrfReadRequest to default values.

### [mjrf_render](#mjrf_render)

``` C
mjrfFrameHandle mjrf_render(mjrfContext* ctx, const mjrfRenderRequest* req, int nreq,
                      const mjrfReadRequest* read_req, int nread_req);
```

Submits the given requests for rendering. Because rendering happens asynchronously, callers have to submit both the render and read requests in the same call. Multiple requests and reads can be submitted in a single call. These requests will be processed in order, so some care must be taken. Firstly, requests should be grouped by target. Next, the combined area of the viewports for all requests for a given target must be contained within the dimensions of the target itself.

Callbacks will be invoked from within this function, though there is no guarantee on which invocation of this function it will be done.

### [mjrf_waitForFrame](#mjrf_waitForFrame)

``` C
void mjrf_waitForFrame(mjrfContext* ctx, mjrfFrameHandle frame);
```

Waits for all rendering operations to complete for the given frame handle, triggering any callbacks as needed.

### [mjrf_flush](#mjrf_flush)

``` C
void mjrf_flush(mjrfContext* ctx);
```

Flushes pending operations to the rendering backend and invokes any completed callbacks.

### [mjrf_setClearColor](#mjrf_setClearColor)

``` C
void mjrf_setClearColor(mjrfContext* ctx, const float color[3]);
```

Sets the clear color for the renderer.

### [mjrf_defaultFrameStats](#mjrf_defaultFrameStats)

``` C
void mjrf_defaultFrameStats(mjrfFrameStats* stats);
```

Initializes the mjrFrameStats to default values.

### [mjrf_getFrameStats](#mjrf_getFrameStats)

``` C
void mjrf_getFrameStats(mjrfContext* ctx, mjrfFrameHandle frame, mjrfFrameStats* stats_out);
```

Returns the stats for the given frame but updating the given `stats_out`.

### [mjrf_defaultTextureConfig](#mjrf_defaultTextureConfig)

``` C
void mjrf_defaultTextureConfig(mjrfTextureConfig* config);
```

Initializes the mjrfTextureConfig to default values.

### [mjrf_createTexture](#mjrf_createTexture)

``` C
mjrfTexture* mjrf_createTexture(mjrfContext* ctx, const mjrfTextureConfig* config);
```

Creates a filament texture. Note that the texture will not be created on the GPU until `mjrf_uploadTexture()` is called.

### [mjrf_destroyTexture](#mjrf_destroyTexture)

``` C
void mjrf_destroyTexture(mjrfTexture* texture);
```

Destroys the texture.

### [mjrf_defaultTextureData](#mjrf_defaultTextureData)

``` C
void mjrf_defaultTextureData(mjrfTextureData* data);
```

Initializes the mjrfTextureData to default values.

### [mjrf_uploadTexture](#mjrf_uploadTexture)

``` C
void mjrf_uploadTexture(mjrfTexture* texture, const mjrfTextureData* data);
```

Uploads the given texture data to the texture.

### [mjrf_getTextureWidth](#mjrf_getTextureWidth)

``` C
int mjrf_getTextureWidth(const mjrfTexture* texture);
```

Returns the width of the texture.

### [mjrf_getTextureHeight](#mjrf_getTextureHeight)

``` C
int mjrf_getTextureHeight(const mjrfTexture* texture);
```

Returns the height of the texture.

### [mjrf_getTextureSamplerType](#mjrf_getTextureSamplerType)

``` C
int mjrf_getTextureSamplerType(const mjrfTexture* texture);
```

Returns the sampler type (mjrSamplerType) used by the texture. \[returns: mjrSamplerType\]

### [mjrf_defaultMeshConfig](#mjrf_defaultMeshConfig)

``` C
void mjrf_defaultMeshConfig(mjrfMeshConfig* config);
```

Initializes the mjrfMeshConfig to default values.

### [mjrf_createMesh](#mjrf_createMesh)

``` C
mjrfMesh* mjrf_createMesh(mjrfContext* ctx, const mjrfMeshConfig* config);
```

Creates an empty mesh with the given config.

### [mjrf_destroyMesh](#mjrf_destroyMesh)

``` C
void mjrf_destroyMesh(mjrfMesh* mesh);
```

Destroys the mesh.

### [mjrf_defaultMeshData](#mjrf_defaultMeshData)

``` C
void mjrf_defaultMeshData(mjrfMeshData* data);
```

Initializes the mjrfMeshData to default values.

### [mjrf_uploadMesh](#mjrf_uploadMesh)

``` C
void mjrf_uploadMesh(mjrfMesh* mesh, const mjrfMeshData* data);
```

Uploads the given mesh data to the mesh.

### [mjrf_defaultSceneParams](#mjrf_defaultSceneParams)

``` C
void mjrf_defaultSceneParams(mjrfSceneParams* params);
```

Initializes the mjrfSceneParams to default values.

### [mjrf_createScene](#mjrf_createScene)

``` C
mjrfScene* mjrf_createScene(mjrfContext* ctx, const mjrfSceneParams* params);
```

Creates a scene with the given parameters.

### [mjrf_destroyScene](#mjrf_destroyScene)

``` C
void mjrf_destroyScene(mjrfScene* scene);
```

Destroys the scene.

### [mjrf_addSceneLight](#mjrf_addSceneLight)

``` C
void mjrf_addSceneLight(mjrfScene* scene, mjrfLight* light);
```

Adds a light to the scene.

### [mjrf_removeSceneLight](#mjrf_removeSceneLight)

``` C
void mjrf_removeSceneLight(mjrfScene* scene, mjrfLight* light);
```

Removes the light from the scene.

### [mjrf_addSceneRenderable](#mjrf_addSceneRenderable)

``` C
void mjrf_addSceneRenderable(mjrfScene* scene, mjrfRenderable* renderable);
```

Adds a renderable to the scene.

### [mjrf_removeSceneRenderable](#mjrf_removeSceneRenderable)

``` C
void mjrf_removeSceneRenderable(mjrfScene* scene, mjrfRenderable* renderable);
```

Removes the renderable from the scene.

### [mjrf_setSceneSkybox](#mjrf_setSceneSkybox)

``` C
void mjrf_setSceneSkybox(mjrfScene* scene, const mjrfTexture* texture);
```

Sets the skybox (cube texture) for the scene.

### [mjrf_configureSceneFromModel](#mjrf_configureSceneFromModel)

``` C
void mjrf_configureSceneFromModel(mjrfScene* scene, const mjModel* model);
```

Configures the scene based on the parameters in an mjModel.

### [mjrf_setSceneMsaa](#mjrf_setSceneMsaa)

``` C
void mjrf_setSceneMsaa(mjrfScene* scene, int samples);
```

Sets the number of multi-sample anti-aliasing samples; values \<= 1 disable MSAA.

### [mjrf_defaultLightParams](#mjrf_defaultLightParams)

``` C
void mjrf_defaultLightParams(mjrfLightParams* params);
```

Initializes the mjrfLightParams to default values.

### [mjrf_createLight](#mjrf_createLight)

``` C
mjrfLight* mjrf_createLight(mjrfContext* ctx, const mjrfLightParams* params);
```

Creates a light for the filament renderer.

### [mjrf_destroyLight](#mjrf_destroyLight)

``` C
void mjrf_destroyLight(mjrfLight* light);
```

Destroys the light.

### [mjrf_setLightActive](#mjrf_setLightActive)

``` C
void mjrf_setLightActive(mjrfLight* light, mjtBool active);
```

Activates or deactivates the light.

### [mjrf_setLightCastShadow](#mjrf_setLightCastShadow)

``` C
void mjrf_setLightCastShadow(mjrfLight* light, mjtBool enabled);
```

Enables or disables whether or not the light casts shadows.

### [mjrf_setLightColor](#mjrf_setLightColor)

``` C
void mjrf_setLightColor(mjrfLight* light, const float color[3]);
```

Sets the RGB color of the light.

### [mjrf_setLightIntensity](#mjrf_setLightIntensity)

``` C
void mjrf_setLightIntensity(mjrfLight* light, float intensity);
```

Sets the intensity of the light, in candela.

### [mjrf_setLightRange](#mjrf_setLightRange)

``` C
void mjrf_setLightRange(mjrfLight* light, float range);
```

Sets the effective range of the light, in meters.

### [mjrf_setLightCutoff](#mjrf_setLightCutoff)

``` C
void mjrf_setLightCutoff(mjrfLight* light, float cutoff);
```

Sets the cutoff angle of the light, in degrees. Only used for spot lights.

### [mjrf_setLightSoftness](#mjrf_setLightSoftness)

``` C
void mjrf_setLightSoftness(mjrfLight* light, float softness);
```

Sets the softness of the light, in the range \[0, 1\]. Only used for spot lights.

### [mjrf_setLightBulbRadius](#mjrf_setLightBulbRadius)

``` C
void mjrf_setLightBulbRadius(mjrfLight* light, float radius);
```

Sets the radius of the light bulb.

### [mjrf_setLightShadowMapSize](#mjrf_setLightShadowMapSize)

``` C
void mjrf_setLightShadowMapSize(mjrfLight* light, int map_size);
```

Sets the resolution of the light’s shadow map, in texels.

### [mjrf_setLightPose](#mjrf_setLightPose)

``` C
void mjrf_setLightPose(mjrfLight* light, const float position[3], const float direction[3]);
```

Sets the position and direction of the light.

### [mjrf_getLightType](#mjrf_getLightType)

``` C
int mjrf_getLightType(const mjrfLight* light);
```

Returns the type of the light (mjrLightType).

### [mjrf_defaultMaterial](#mjrf_defaultMaterial)

``` C
void mjrf_defaultMaterial(mjrfMaterial* material);
```

Initializes the mjrfMaterial to default values.

### [mjrf_defaultRenderableParams](#mjrf_defaultRenderableParams)

``` C
void mjrf_defaultRenderableParams(mjrfRenderableParams* params);
```

Initializes the mjrfRenderableParams to default values.

### [mjrf_createRenderable](#mjrf_createRenderable)

``` C
mjrfRenderable* mjrf_createRenderable(mjrfContext* ctx, const mjrfRenderableParams* params);
```

Creates a renderable with the given parameters.

### [mjrf_destroyRenderable](#mjrf_destroyRenderable)

``` C
void mjrf_destroyRenderable(mjrfRenderable* renderable);
```

Destroys the renderable.

### [mjrf_setRenderableMesh](#mjrf_setRenderableMesh)

``` C
void mjrf_setRenderableMesh(mjrfRenderable* renderable, const mjrfMesh* mesh, int elem_offset,
                      int elem_count);
```

Sets the mesh of the renderable.

### [mjrf_setRenderableGeomMesh](#mjrf_setRenderableGeomMesh)

``` C
void mjrf_setRenderableGeomMesh(mjrfRenderable* renderable, int type, int nstack, int nslice,
                          int nquad);
```

Sets the mesh of the renderable to a built-in mesh based on the geom type. Note: using the same parameters (nstack, nslice, nquad) will have better performance as the internal mesh data can be shared across renderables. \[type: mjtGeom\]

### [mjrf_setRenderableMaterial](#mjrf_setRenderableMaterial)

``` C
void mjrf_setRenderableMaterial(mjrfRenderable* renderable, const mjrfMaterial* material);
```

Sets the material properties and textures of the renderable.

### [mjrf_getRenderableMaterial](#mjrf_getRenderableMaterial)

``` C
void mjrf_getRenderableMaterial(mjrfRenderable* renderable, mjrfMaterial* material);
```

Copies the material properties of the renderable into the given mjrfMaterial.

### [mjrf_setRenderablePose](#mjrf_setRenderablePose)

``` C
void mjrf_setRenderablePose(mjrfRenderable* renderable, const float position[3],
                      const float rotation[9]);
```

Sets the position and rotation of the renderable.

### [mjrf_setRenderableSize](#mjrf_setRenderableSize)

``` C
void mjrf_setRenderableSize(mjrfRenderable* renderable, const float size[3]);
```

Sets the size of the renderable. Note that, for most renderables, this is equivalent to setting the scale. However, for some geom-based renderables, the size scale is not applied uniformly (e.g. the spherical ends of a capsule are scaled such that they always remain spherical).

### [mjrf_setRenderableCastShadow](#mjrf_setRenderableCastShadow)

``` C
void mjrf_setRenderableCastShadow(mjrfRenderable* renderable, mjtBool enabled);
```

Enables or disables whether or not the renderable casts shadows.

### [mjrf_defaultRenderTargetConfig](#mjrf_defaultRenderTargetConfig)

``` C
void mjrf_defaultRenderTargetConfig(mjrfRenderTargetConfig* config);
```

Initializes the mjrfRenderTargetConfig to default values.

### [mjrf_createRenderTarget](#mjrf_createRenderTarget)

``` C
mjrfRenderTarget* mjrf_createRenderTarget(mjrfContext* ctx, const mjrfRenderTargetConfig* config);
```

Creates a render target for the filament renderer.

### [mjrf_destroyRenderTarget](#mjrf_destroyRenderTarget)

``` C
void mjrf_destroyRenderTarget(mjrfRenderTarget* render_target);
```

Destroys the render target.

### [mjrf_resizeRenderTarget](#mjrf_resizeRenderTarget)

``` C
void mjrf_resizeRenderTarget(mjrfRenderTarget* render_target, int width, int height);
```

Resizes the render target to the given width and height.

## UI framework

For a high-level description of the UI framework, see [User Interface](../programming/ui.md#ui).

### [mjui_themeSpacing](#mjui_themeSpacing)

``` C
mjuiThemeSpacing mjui_themeSpacing(int ind);
```

Get builtin UI theme spacing (ind: 0-1).

### [mjui_themeColor](#mjui_themeColor)

``` C
mjuiThemeColor mjui_themeColor(int ind);
```

Get builtin UI theme color (ind: 0-3).

### [mjui_add](#mjui_add)

``` C
void mjui_add(mjUI* ui, const mjuiDef* def);
```

This is the helper function used to construct a UI. The second argument points to an array of [mjuiDef](APItypes.md#mjuidef) structs, each corresponding to one item. The last (unused) item has its type set to -1, to mark termination. The items are added after the end of the last used section. There is also another version of this function ([mjui_addToSection](#mjui-addtosection)) which adds items to a specified section instead of adding them at the end of the UI. Keep in mind that there is a maximum preallocated number of sections and items per section, given by [mjMAXUISECT](APIglobals.md#glnumericui) and [mjMAXUIITEM](APIglobals.md#glnumericui). Exceeding these maxima results in low-level errors.

### [mjui_addToSection](#mjui_addToSection)

``` C
void mjui_addToSection(mjUI* ui, int sect, const mjuiDef* def);
```

Add definitions to UI section.

### [mjui_resize](#mjui_resize)

``` C
void mjui_resize(mjUI* ui, const mjrContext* con);
```

Compute UI sizes.

### [mjui_update](#mjui_update)

``` C
void mjui_update(int section, int item, const mjUI* ui,
                 const mjuiState* state, const mjrContext* con);
```

This is the main UI update function. It needs to be called whenever the user data (pointed to by the item data pointers) changes, or when the UI state itself changes. It is normally called by a higher-level function implemented by the user (`UiModify` in [simulate.cc](../programming/samples.md#sasimulate)) which also recomputes the layout of all rectangles and associated auxiliary buffers. The function updates the pixels in the offscreen OpenGL buffer. To perform minimal updates, the user specifies the section and the item that was modified. A value of -1 means all items and/or sections need to be updated (which is needed following major changes.)

### [mjui_event](#mjui_event)

``` C
mjuiItem* mjui_event(mjUI* ui, mjuiState* state, const mjrContext* con);
```

This function is the low-level event handler. It makes the necessary changes in the UI and returns a pointer to the item that received the event (or `NULL` if no valid event was recorded). This is normally called within the event handler implemented by the user (`UiEvent` in [simulate.cc](../programming/samples.md#sasimulate)), and then some action is taken by user code depending on which UI item was modified and what the state of that item is after the event is handled.

### [mjui_render](#mjui_render)

``` C
void mjui_render(mjUI* ui, const mjuiState* state, const mjrContext* con);
```

This function is called in the screen refresh loop. It copies the offscreen OpenGL buffer to the window framebuffer. If there are multiple UIs in the application, it should be called once for each UI. Thus `mjui_render` is called all the time, while [mjui_update](#mjui-update) is called only when changes in the UI take place. dsffsdg

## Derivatives

The functions below provide useful derivatives of various functions, both analytic and finite-differenced. The latter have names with the suffix `FD`. Note that unlike much of the API, outputs of derivative functions are the trailing rather than leading arguments.

### [mjd_transitionFD](#mjd_transitionFD)

``` C
void mjd_transitionFD(const mjModel* m, mjData* d, mjtNum eps, mjtBool flg_centered,
                      mjtNum* A, mjtNum* B, mjtNum* C, mjtNum* D);
```

Compute finite-differenced discrete-time transition matrices.

Letting \\x, u\\ denote the current [state](../programming/simulation.md#siphysicsstate) and [control](../programming/simulation.md#siinput) vector in an mjData instance, and letting \\y, s\\ denote the next state and sensor values, the top-level [mj_step](#mj-step) function computes \\(x,u) \rightarrow (y,s)\\ [mjd_transitionFD](#mjd-transitionfd) computes the four associated Jacobians using finite-differencing. These matrices and their dimensions are:

| matrix | Jacobian                    | dimension               |
|--------|-----------------------------|-------------------------|
| `A`    | \\\partial y / \partial x\\ | `2*nv+na x 2*nv+na`     |
| `B`    | \\\partial y / \partial u\\ | `2*nv+na x nu`          |
| `C`    | \\\partial s / \partial x\\ | `nsensordata x 2*nv+na` |
| `D`    | \\\partial s / \partial u\\ | `nsensordata x nu`      |

- All outputs are optional (can be NULL).

- `eps` is the finite-differencing epsilon.

- `flg_centered` denotes whether to use forward (0) or centered (1) differences.

- The Runge-Kutta integrator ([mjINT_RK4](APItypes.md#mjtintegrator)) is not supported.

- [Sleeping](../computation/index.md#sleeping) is not supported. Disable the [sleep](../XMLreference.md#option-flag-sleep) flag before calling.

- [Delays](../modeling.md#cdelay) are not supported.

Improving speed and accuracy

warmstart  
If warm-starts are not [disabled](../XMLreference.md#option-flag-warmstart), the warm-start accelerations `mjData.qacc_warmstart` which are present at call-time are loaded at the start of every relevant pipeline call, to preserve determinism. If solver computations are an expensive part of the simulation, the following trick can lead to significant speed-ups: First call [mj_forward](#mj-forward) to let the solver converge, then reduce [solver iterations](../XMLreference.md#option-iterations) significantly, then call [mjd_transitionFD](#mjd-transitionfd), finally, restore the original value of [iterations](../XMLreference.md#option-iterations). Because we are already near the solution, few iteration are required to find the new minimum. This is especially true for the [Newton](../XMLreference.md#option-solver) solver, where the required number of iteration for convergence near the minimum can be as low as 1.

tolerance  
Accuracy can be improved if solver [tolerance](../XMLreference.md#option-tolerance) is set to 0. This means that all calls to the solver will perform exactly the same number of iterations, preventing numerical errors due to early termination. Of course, this means that [solver iterations](../XMLreference.md#option-iterations) should be small, to not tread water at the minimum. This method and the one described above can and should be combined.

*Nullable:* `A`, `B`, `D`, `C`

### [mjd_inverseFD](#mjd_inverseFD)

``` C
void mjd_inverseFD(const mjModel* m, mjData* d, mjtNum eps, mjtBool flg_actuation,
                   mjtNum *DfDq, mjtNum *DfDv, mjtNum *DfDa,
                   mjtNum *DsDq, mjtNum *DsDv, mjtNum *DsDa,
                   mjtNum *DmDq);
```

Finite differenced continuous-time inverse-dynamics Jacobians.

Letting \\x, a\\ denote the current [state](../programming/simulation.md#siphysicsstate) and acceleration vectors in an mjData instance, and letting \\f, s\\ denote the forces computed by the inverse dynamics (`qfrc_inverse`), the function [mj_inverse](#mj-inverse) computes \\(x,a) \rightarrow (f,s)\\. [mjd_inverseFD](#mjd-inversefd) computes seven associated Jacobians using finite-differencing. These matrices and their dimensions are:

| matrix | Jacobian                    | dimension          |
|--------|-----------------------------|--------------------|
| `DfDq` | \\\partial f / \partial q\\ | `nv x nv`          |
| `DfDv` | \\\partial f / \partial v\\ | `nv x nv`          |
| `DfDa` | \\\partial f / \partial a\\ | `nv x nv`          |
| `DsDq` | \\\partial s / \partial q\\ | `nv x nsensordata` |
| `DsDv` | \\\partial s / \partial v\\ | `nv x nsensordata` |
| `DsDa` | \\\partial s / \partial a\\ | `nv x nsensordata` |
| `DmDq` | \\\partial M / \partial q\\ | `nv x nC`          |

- All outputs are optional (can be NULL).

- All outputs are transposed relative to Control Theory convention (i.e., column major).

- `DmDq`, which contains a sparse representation of the `nv x nv x nv` tensor \\\partial M / \partial q\\, is not strictly an inverse dynamics Jacobian but is useful in related applications. It is provided as a convenience to the user, since the required values are already computed if either of the other two \\\partial / \partial q\\ Jacobians are requested.

- `eps` is the (forward) finite-differencing epsilon.

- `flg_actuation` denotes whether to subtract actuation forces (`qfrc_actuator`) from the output of the inverse dynamics. If this flag is positive, actuator forces are not considered as external.

- The model option flag `invdiscrete` should correspond to the representation of `mjData.qacc` in order to compute the correct derivative information.

Attention

- The Runge-Kutta 4th-order integrator (`mjINT_RK4`) is not supported.

- The noslip solver is not supported.

- [Sleeping](../computation/index.md#sleeping) is not supported. Disable the [sleep](../XMLreference.md#option-flag-sleep) flag before calling.

*Nullable:* `DfDq`, `DfDv`, `DfDa`, `DsDq`, `DsDv`, `DsDa`, `DmDq`

### [mjd_subQuat](#mjd_subQuat)

``` C
void mjd_subQuat(const mjtNum qa[4], const mjtNum qb[4], mjtNum Da[9], mjtNum Db[9]);
```

Derivatives of [mju_subQuat](#mju-subquat) (quaternion difference).

*Nullable:* `Da`, `Db`

### [mjd_quatIntegrate](#mjd_quatIntegrate)

``` C
void mjd_quatIntegrate(const mjtNum vel[3], mjtNum scale,
                       mjtNum Dquat[9], mjtNum Dvel[9], mjtNum Dscale[3]);
```

Derivatives of [mju_quatIntegrate](#mju-quatintegrate).

\\{\tt \small mju\\quatIntegrate}(q, v, h)\\ performs the in-place rotation \\q \leftarrow q + v h\\, where \\q \in \mathbf{S}^3\\ is a unit quaternion, \\v \in \mathbf{R}^3\\ is a 3D angular velocity and \\h \in \mathbf{R^+}\\ is a timestep. This is equivalent to \\{\tt \small mju\\quatIntegrate}(q, s, 1.0)\\, where \\s\\ is the scaled velocity \\s = h v\\.

\\{\tt \small mjd\\quatIntegrate}(v, h, D_q, D_v, D_h)\\ computes the Jacobians of the output \\q\\ with respect to the inputs. Below, \\\bar q\\ denotes the pre-modified quaternion:

\\\begin{aligned} D_q &= \partial q / \partial \bar q \\ D_v &= \partial q / \partial v \\ D_h &= \partial q / \partial h \end{aligned} \\

Note that derivatives depend only on \\h\\ and \\v\\ (in fact, on \\s = h v\\). All outputs are optional.

*Nullable:* `Dquat`, `Dvel`, `Dscale`

## Signed Distance Functions

### [mjc_getSDF](#mjc_getSDF)

``` C
const mjpPlugin* mjc_getSDF(const mjModel* m, int id);
```

get sdf from geom id

### [mjc_distance](#mjc_distance)

``` C
mjtNum mjc_distance(const mjModel* m, const mjData* d, const mjSDF* s, const mjtNum x[3]);
```

signed distance function

### [mjc_gradient](#mjc_gradient)

``` C
void mjc_gradient(const mjModel* m, const mjData* d, const mjSDF* s, mjtNum gradient[3],
                  const mjtNum x[3]);
```

gradient of sdf

## Plugins

### [mjp_defaultPlugin](#mjp_defaultPlugin)

``` C
void mjp_defaultPlugin(mjpPlugin* plugin);
```

Set default plugin definition.

### [mjp_registerPlugin](#mjp_registerPlugin)

``` C
int mjp_registerPlugin(const mjpPlugin* plugin);
```

Globally register a plugin. This function is thread-safe.

If an identical mjpPlugin is already registered, this function does nothing.

If a non-identical mjpPlugin with the same name is already registered, an mju_error is raised.

Two mjpPlugins are considered identical if all member function pointers and numbers are equal, and the name and attribute strings are all identical, however the char pointers to the strings need not be the same.

### [mjp_pluginCount](#mjp_pluginCount)

``` C
int mjp_pluginCount(void);
```

Return the number of globally registered plugins.

### [mjp_getPlugin](#mjp_getPlugin)

``` C
const mjpPlugin* mjp_getPlugin(const char* name, int* slot);
```

Look up a plugin by name. If slot is not NULL, also write its registered slot number into it.

### [mjp_getPluginAtSlot](#mjp_getPluginAtSlot)

``` C
const mjpPlugin* mjp_getPluginAtSlot(int slot);
```

Look up a plugin by the registered slot number that was returned by mjp_registerPlugin.

### [mjp_defaultProvider](#mjp_defaultProvider)

``` C
void mjp_defaultProvider(mjpResourceProvider* provider);
```

Set default provider definition.

### [mjp_registerProvider](#mjp_registerProvider)

``` C
int mjp_registerProvider(const mjpResourceProvider* provider);
```

Globally register a provider in a thread-safe manner. The provider must have a prefix that is not a sub-prefix or super-prefix of any current registered providers.

Return a slot number \>= 0 on success, -1 on failure.

### [mjp_providerCount](#mjp_providerCount)

``` C
int mjp_providerCount(void);
```

Return the number of globally registered providers.

### [mjp_findProvider](#mjp_findProvider)

``` C
const mjpResourceProvider* mjp_findProvider(const char* resource_name);
```

Return the provider with the prefix that matches against the resource name.

If no match, return NULL.

### [mjp_getProviderAtSlot](#mjp_getProviderAtSlot)

``` C
const mjpResourceProvider* mjp_getProviderAtSlot(int slot);
```

Look up a provider by slot number returned by mjp_registerProvider.

If invalid slot number, return NULL.

### [mjp_registerDecoder](#mjp_registerDecoder)

``` C
void mjp_registerDecoder(const mjpDecoder* decoder);
```

Globally register a decoder. This function is thread-safe.

If an identical mjpDecoder is already registered, this function does nothing.

If a non-identical mjpDecoder with the same name is already registered, an mju_error is raised.

### [mjp_defaultDecoder](#mjp_defaultDecoder)

``` C
void mjp_defaultDecoder(mjpDecoder* decoder);
```

Set default resource decoder definition.

### [mjp_findDecoder](#mjp_findDecoder)

``` C
const mjpDecoder* mjp_findDecoder(const mjResource* resource, const char* content_type);
```

Return the decoder that matches against the resource or content type.

If no match, return NULL.

### [mjp_registerEncoder](#mjp_registerEncoder)

``` C
void mjp_registerEncoder(const mjpEncoder* encoder);
```

Globally register an encoder. This function is thread-safe.

If an identical mjpEncoder is already registered, this function does nothing.

If a non-identical mjpEncoder with the same name is already registered, an mju_error is raised.

### [mjp_defaultEncoder](#mjp_defaultEncoder)

``` C
void mjp_defaultEncoder(mjpEncoder* encoder);
```

Set default resource encoder definition.

### [mjp_findEncoder](#mjp_findEncoder)

``` C
const mjpEncoder* mjp_findEncoder(const char* filename, const char* content_type);
```

Return the encoder that matches against the content type or filename extension.

If no match, return NULL.

### [mjp_registerArchiveProvider](#mjp_registerArchiveProvider)

``` C
void mjp_registerArchiveProvider(const mjpResourceProvider* provider);
```

Globally register an archive provider. This function is thread-safe. provider-\>prefix specifies the filename extension(s) (e.g. .mjz\|.zip).

### [mjp_findArchiveProvider](#mjp_findArchiveProvider)

``` C
const mjpResourceProvider* mjp_findArchiveProvider(const char* resource_name);
```

Return the archive provider that matches against the resource name.

If no match, return NULL.

### [mjp_archiveProviderCount](#mjp_archiveProviderCount)

``` C
int mjp_archiveProviderCount(void);
```

Return the number of globally registered archive providers.

## Threads

### [mju_threadpool](#mju_threadpool)

``` C
void mju_threadpool(mjData* d, int nthread);
```

Create a thread pool with nthread worker threads.

## Batched simulation

Functions for running many simulations of one model on a thread pool, declared in `mujoco/mjbatch.h`. See [Batched simulation](../programming/simulation.md#sibatch) for an overview and an example.

The functions that run simulations take a selection: `ids` holds `nid` sorted, unique simulation indices, or is `NULL` to select every simulation, in which case `nid` is ignored. They return the number of simulations in which MuJoCo raised an error. Those simulations keep the state they had before the call, and the others run to completion. [mjb_status](#mjb-status) and [mjb_error](#mjb-error) report the outcome of each simulation’s last call.

Invalid arguments, such as unsorted `ids` or an unknown `stage`, are a different kind of error: the function raises it with [mju_error](#mju-error) on the caller’s thread, before any simulation runs, and it is not counted in the return value.

Errors in simulations are trapped by a thread-local log handler. Therefore, [physics callbacks](APIglobals.md#glphysics), engine plugins and functions run by [mjb_apply](#mjb-apply) must not raise errors with [mju_error](#mju-error) or throw exceptions. Other messages, such as warnings, go to the log handler the thread would use anyway. On the batch’s threads this is the [global handler](#mju-setloghandler). On the caller’s thread it can also be a thread-local handler, such as the one the Python bindings install. Either way, the counters of [mjb_warning](#mjb-warning) count every simulation’s warnings.

The arrays that the batch returns, such as the state rows, outputs and expanded fields, are owned by the batch. They stay at the same address until [mjb_deleteBatch](#mjb-deletebatch) frees them.

Timers (`mjData.timer`, see [mjTimerStat](APItypes.md#mjtimerstat)) are not part of the state. In a persistent batch, each simulation’s mjData times that simulation, and [mjb_getData](#mjb-getdata) copies its timers. Otherwise, each thread’s mjData accumulates the timing of every simulation the thread runs, until a reset of one of them clears it. These timers profile the batch as a whole rather than any one simulation.

### [mjb_defaultConfig](#mjb_defaultConfig)

``` C
void mjb_defaultConfig(mjBatchConfig* config);
```

Set the default [mjBatchConfig](APItypes.md#mjbatchconfig) parameters: one thread per logical CPU, and one mjData per thread. Call it first, then change the parameters you need.

### [mjb_makeBatch](#mjb_makeBatch)

``` C
mjBatch* mjb_makeBatch(const mjModel* m, int nsim, const mjBatchConfig* config,
                       char* error, int error_sz);
```

Allocate a batch of `nsim` simulations of a copy of `m`, and return it. `config` holds the [mjBatchConfig](APItypes.md#mjbatchconfig) parameters; if it is `NULL`, the defaults of [mjb_defaultConfig](#mjb-defaultconfig) apply. If the model cannot be batched, or making an mjData raises an error, return `NULL` and write the reason into `error`, a buffer of `error_sz` bytes.

The batch runs on `config->nthread` threads, including the caller’s. If `nthread <= 0`, it uses one thread per logical CPU. Either way, it uses at most `nsim` threads. The number of logical CPUs is the machine’s, which can exceed what the process may use, for example in a container; set `nthread` explicitly there.

If `config->persistent` is nonzero, the batch keeps one mjData per simulation instead of one per thread. Models with [sleep](../XMLreference.md#option-flag-sleep) or [IPC](../XMLreference.md#option-flag-ipc) enabled require this. In a batch that is not persistent, [engine plugins](../programming/extension.md#explugin) that keep state outside `plugin_state` share that state among the simulations a thread runs.

### [mjb_deleteBatch](#mjb_deleteBatch)

``` C
void mjb_deleteBatch(mjBatch* b);
```

Free the batch, its threads, and every array it returned. `b` may be `NULL`. A function run by [mjb_apply](#mjb-apply) must not delete its own batch.

### [mjb_nstate](#mjb_nstate)

``` C
int mjb_nstate(const mjBatch* b);
```

Return size of a state row: mj_stateSize(m, mjSTATE_INTEGRATION).

### [mjb_state](#mjb_state)

``` C
mjtNum* mjb_state(mjBatch* b);
```

Return the state rows, `nsim x nstate`. Row `i` is simulation `i`’s [integration state](../programming/simulation.md#siintegrationstate), in [mj_getState](#mj-getstate) order. Writing to a row sets the simulation’s state for its next call, which then overwrites the row with the new state.

### [mjb_stateComponent](#mjb_stateComponent)

``` C
mjtNum* mjb_stateComponent(mjBatch* b, int component, int* size);
```

Return the address of state component `component` (one bit of [mjtState](APItypes.md#mjtstate)) in the first state row, and write its number of elements into `size`. Simulation `i`’s component is `mjb_nstate(b) * i` elements further on. Raise an error if `component` is not one bit of `mjSTATE_INTEGRATION`.

### [mjb_warning](#mjb_warning)

``` C
mjWarningStat* mjb_warning(mjBatch* b);
```

Return the warning counters, `nsim x mjNWARNING` [mjWarningStat](APItypes.md#mjwarningstat)⁠s. They are saved and restored with the state.

### [mjb_step](#mjb_step)

``` C
int mjb_step(mjBatch* b, const int* ids, int nid, int nstep, int stage);
```

Advance each selected simulation by `nstep` calls to [mj_step](#mj-step), then compute the stages of [mj_forward](#mj-forward) up to `stage` (an [mjtStage](APItypes.md#mjtstage)) at the new state. Return the number of simulations in which MuJoCo raised an error.

As with [mj_step](#mj-step), derived fields after the steps describe the state before the last substep. `stage` brings them up to date:

- `mjSTAGE_NONE` leaves them as [mj_step](#mj-step) does.

- `mjSTAGE_VEL` makes position- and velocity-dependent fields and sensors current, as [mj_step1](#mj-step1) does. Acceleration-dependent fields remain those of the last substep, under the controls it applied.

- `mjSTAGE_ACC` runs [mj_forward](#mj-forward), at nearly the cost of another step. Its acceleration-dependent values use controls that the next step will replace.

In a persistent batch, a simulation’s next step continues from these stages with [mj_step2](#mj-step2), so `mjSTAGE_VEL` costs nothing extra. The step does not continue if anything the stages depend on changed in between, other than `ctrl`, `qfrc_applied` and `xfrc_applied`; the results are the same either way. As with [mj_step1](#mj-step1) and [mj_step2](#mj-step2), this assumes that plugins do not make the position and velocity stages depend on those inputs. A loop of [mj_forward](#mj-forward) and [mj_step](#mj-step) computes these stages twice at the same state, while a continued step computes them once; this matters only to plugins whose computations have side effects. Installed [physics callbacks](APIglobals.md#glphysics) turn the continuation off, but removing one between a call and the next step is not detected. A continued step counts as one step in `mjData.timer`, but its `mjTIMER_STEP` duration excludes the position and velocity stages, which are timed in the call that computed them.

### [mjb_forward](#mjb_forward)

``` C
int mjb_forward(mjBatch* b, const int* ids, int nid, int stage);
```

Compute the stages of [mj_forward](#mj-forward) up to `stage` (an [mjtStage](APItypes.md#mjtstage)) on each selected simulation. `mjSTAGE_ACC` runs [mj_forward](#mj-forward). Return the number of simulations in which MuJoCo raised an error.

### [mjb_reset](#mjb_reset)

``` C
int mjb_reset(mjBatch* b, const int* ids, int nid, const int* key, int stage);
```

Reset each selected simulation, then compute the stages of [mj_forward](#mj-forward) up to `stage` (an [mjtStage](APItypes.md#mjtstage)). Return the number of simulations in which MuJoCo raised an error.

`key` holds one keyframe per selected simulation, in call order; a keyframe of -1, or a `NULL` `key`, resets to the model’s defaults. `mjSTAGE_ACC` runs [mj_forward](#mj-forward). `mjSTAGE_NONE` suits a reset that is followed by writes to the state and [mjb_forward](#mjb-forward). Writes to the state rows made before the call are discarded.

### [mjb_status](#mjb_status)

``` C
const int* mjb_status(const mjBatch* b);
```

Return the status of each simulation’s last call: `nsim` values, nonzero where MuJoCo raised an error. Each call updates the values of the simulations it runs.

### [mjb_error](#mjb_error)

``` C
const char* mjb_error(const mjBatch* b, int sim);
```

Return the error message of simulation `sim`’s last call, or `""` if there was none. The string remains valid until the next call on the simulation.

### [mjb_output](#mjb_output)

``` C
void* mjb_output(mjBatch* b, const char* name, int* size, int* elemsize);
```

Register [mjData](APItypes.md#mjdata) field `name` as an output, and return its storage: `nsim x size` elements of the field’s type. Write the number of elements per simulation into `size` and the element size in bytes into `elemsize`. After every call on a simulation except [mjb_apply](#mjb-apply), the batch copies the field from the simulation’s mjData into its row of the storage. Registering a field again returns the same storage.

`name` can be an array field, or one of the counts `ncon`, `ne`, `nf`, `nl`, `nefc`, `nJ`, `nA`, `nisland` and `nidof`. Return `NULL` for unknown fields, and for fields of the state row, which [mjb_state](#mjb-state) already holds.

In a persistent batch, the storage starts with each simulation’s current values. Otherwise, it is zero until the next call on a simulation, and a field that the call does not compute holds another simulation’s value. Examples are `qfrc_inverse` after [mj_step](#mj-step), quantities computed only for the sensors that need them, and fields of stages above the call’s `stage`.

### [mjb_expand](#mjb_expand)

``` C
void* mjb_expand(mjBatch* b, const char* name, int* size, int* elemsize);
```

Give [mjModel](APItypes.md#mjmodel) field `name` per-simulation values, and return their storage: `nsim x size` elements of the field’s type, initialized from the model. Before each call on a simulation, the batch copies the simulation’s row into its model. `size` and `elemsize` are written as by [mjb_output](#mjb-output). Expanding a field again returns the same storage.

Array fields are named as in [mjModel](APItypes.md#mjmodel), and [mjOption](APItypes.md#mjoption) fields as `"opt.<name>"`. The storage of `bvh_aabb` holds only the bodies’ bounding volumes, which come before the meshes’. Return `NULL` for unknown fields and for asset fields (meshes, heightfields, textures, skins), which all simulations share.

Writing a field that [mj_setConst](#mj-setconst) reads, an input in `MJSETCONST_ARRAYS` of `mjxmacro.h` or an [mjOption](APItypes.md#mjoption) field, does not update the constants derived from it until [mjb_setConst](#mjb-setconst) runs.

Expanding a field that [mjb_setConst](#mjb-setconst) expanded makes it an input of later calls to [mjb_setConst](#mjb-setconst), if [mj_setConst](#mj-setconst) reads it before writing it. To read such a field without that effect, use [mjb_expanded](#mjb-expanded).

### [mjb_expanded](#mjb_expanded)

``` C
const void* mjb_expanded(mjBatch* b, const char* name, int* size, int* elemsize);
```

Return the per-simulation storage of [mjModel](APItypes.md#mjmodel) field `name` if it is expanded, by [mjb_expand](#mjb-expand) or by [mjb_setConst](#mjb-setconst). Otherwise, return `NULL`: every simulation has the model’s value. Unlike [mjb_expand](#mjb-expand), this expands nothing, and fields that [mjb_setConst](#mjb-setconst) derives stay derived. Treat the storage as read-only, since [mjb_setConst](#mjb-setconst) overwrites derived fields. `size` and `elemsize` are written as by [mjb_expand](#mjb-expand), also when the field is not expanded.

### [mjb_setConst](#mjb_setConst)

``` C
int mjb_setConst(mjBatch* b, const int* ids, int nid);
```

Run [mj_setConst](#mj-setconst) on each selected simulation’s model. Return the number of simulations in which MuJoCo raised an error; those simulations keep their constants.

Every model field that [mj_setConst](#mj-setconst) changes becomes per-simulation, as with [mjb_expand](#mjb-expand), so each simulation gets its own derived constants; only the arrays marked `mjSC_OUT` in `MJSETCONST_ARRAYS` and the scalars in `MJSETCONST_SCALARS` can change. If a call makes a new field per-simulation, [mj_setConst](#mj-setconst) runs again on the call’s simulations. Simulations outside the call need no update, since the new field starts from the model’s value, which is theirs.

Only the groups of [mj_setConst](#mj-setconst) computations (the columns of `MJSETCONST_ARRAYS`) that read a per-simulation field, or what an earlier such group writes, run; the others would give every simulation the model’s values. With no per-simulation field that [mj_setConst](#mj-setconst) reads, for example only friction or actuator gains, the call does nothing. Per-simulation [mjOption](APItypes.md#mjoption) fields count as read by every group. Skipping groups assumes that the constants of the model given to [mjb_makeBatch](#mjb-makebatch) are current, as after compilation or [mj_setConst](#mj-setconst).

On each call, the fields that [mj_setConst](#mj-setconst) derives are recomputed from the model’s values. Expanding such a field with [mjb_expand](#mjb-expand) makes its values inputs instead if [mj_setConst](#mj-setconst) reads it before writing it, as the anchors of connect constraints are in `eq_data`; otherwise they are recomputed all the same. [mjb_expanded](#mjb-expanded) reads them without that effect.

### [mjb_setModels](#mjb_setModels)

``` C
void mjb_setModels(mjBatch* b, const mjModel* const* models);
```

Run each simulation `i` on `models[i]`, a model of the caller’s, instead of the batch’s model. If `models` is `NULL`, return to the batch’s model.

Each model must give mjData the same layout as the batch’s model, that is, the same sizes for everything mjData holds. Models compiled from one spec with different parameters qualify, and so do models whose meshes have other shapes but the same numbers of vertices and faces. The batch only reads the models, so one model can serve several simulations. After editing a model, call [mjb_setModels](#mjb-setmodels) again; otherwise a persistent batch may continue a step from stages computed before the edit.

Caller models replace per-simulation fields, and the two cannot be combined: raise an error if the batch has fields from [mjb_expand](#mjb-expand). While caller models are set:

- [mjb_expand](#mjb-expand) and [mjb_setConst](#mjb-setconst) raise an error.

- Keyframes are those of each simulation’s model.

- [mjb_getModel](#mjb-getmodel) copies the simulation’s model.

### [mjb_rollout](#mjb_rollout)

``` C
int mjb_rollout(mjBatch* b, const int* ids, int nid, int nstep, const mjtNum* control,
                int control_spec, const mjBatchRecord* record, int nrecord);
```

Advance each selected simulation by `nstep` calls to [mj_step](#mj-step), as [rollout](../python.md#pyrollout) does, recording after each substep. Return the number of simulations in which MuJoCo raised an error.

Before each substep, set the state components in `control_spec` (a subset of the [mjtState](APItypes.md#mjtstate) bits in `mjSTATE_USER`) from `control`. `control` is `n x nstep x mj_stateSize(m, control_spec)`, for the `n` selected simulations in call order; if it is `NULL`, the inputs are left as they are. After each substep, copy each of the `nrecord` [mjBatchRecord](APItypes.md#mjbatchrecord)⁠s in `record` into its buffer. A simulation whose warning counters rise stops stepping, and its remaining records repeat its last ones.

### [mjb_apply](#mjb_apply)

``` C
int mjb_apply(mjBatch* b, const int* ids, int nid, mjfBatchFunc func, void* arg,
              int save);
```

Run `func` (an [mjfBatchFunc](APItypes.md#mjfbatchfunc)) on each selected simulation’s model and data, on the batch’s threads, passing it the simulation’s index and `arg`. If `save` is nonzero, save the state back afterwards. Return the number of simulations in which MuJoCo raised an error.

Fields registered with [mjb_output](#mjb-output) are not refreshed; `func` returns its results through `arg`. `func` may call other batches, as long as they do not call back into this one; a call on its own batch raises an error in the simulation. An error raised by a MuJoCo function that `func` calls unwinds to the batch with `longjmp`, so `func` must not hold C++ objects with destructors across MuJoCo calls.

In a persistent batch:

- With `save` zero, `func` should not change the simulation’s state. The mjData keeps what lies outside the state, such as the sleep bookkeeping, which would then no longer match the row.

- The mjData that `func` receives may hold the stages that [mjb_step](#mjb-step) computed at the new state. Its contacts are then those of the new state, but its constraint forces are not yet computed, so do not read contact forces before the acceleration stage runs.

For example, this computes the finite-differenced transition matrices of every simulation at its current state, into arrays indexed by simulation. [mjd_transitionFD](#mjd-transitionfd) restores the state it perturbs, so `save` is zero:

``` C
// arrays of TransitionFD, nx = 2*nv + na
struct TransitionArgs {
  mjtNum* A;  // nsim x nx x nx
  mjtNum* B;  // nsim x nx x nu
};

// mjb_apply function: transition matrices of simulation sim
void TransitionFD(const mjModel* m, mjData* d, int sim, void* arg) {
  struct TransitionArgs* a = arg;
  int nx = 2*m->nv + m->na;
  mjd_transitionFD(m, d, 1e-6, /*flg_centered=*/0, a->A + sim*nx*nx, a->B + sim*nx*m->nu, NULL, NULL);
}

struct TransitionArgs args = {A, B};
mjb_apply(b, /*ids=*/NULL, 0, TransitionFD, &args, /*save=*/0);
```

A function can also read one field of one simulation. The mjData it receives holds the simulation’s state, but in a batch that is not persistent its derived fields belong to another simulation, so the function computes what it reads. In a persistent batch, it can instead read the fields that the simulation’s last call left in its mjData:

``` C
// mjb_apply function: subtree centers of mass, into arg (3*nbody)
void SubtreeCom(const mjModel* m, mjData* d, int sim, void* arg) {
  mj_kinematics(m, d);
  mj_comPos(m, d);
  mju_copy(arg, d->subtree_com, 3*m->nbody);
}

int sim = 7;
mjb_apply(b, &sim, 1, SubtreeCom, com, /*save=*/0);
```

### [mjb_getModel](#mjb_getModel)

``` C
void mjb_getModel(mjBatch* b, int sim, mjModel* m);
```

Write simulation `sim`’s model into `m`, ready to render or to pass to any function. Normally, this is the batch’s model with the simulation’s per-simulation fields and the constants [mjb_setConst](#mjb-setconst) computed for it; `m` must then have the batch’s sizes, such as a copy of [mjb_model](#mjb-model). With caller models from [mjb_setModels](#mjb-setmodels), it is a copy of the simulation’s model, and `m` must have that model’s sizes. Raise an error if `sim` is out of range or the sizes differ.

### [mjb_getData](#mjb_getData)

``` C
void mjb_getData(mjBatch* b, int sim, mjData* d);
```

Write simulation `sim`’s state and warning counters into `d`, including writes to its row since its last call; `d` must have the batch’s sizes. In a persistent batch, first copy the simulation’s mjData, so that `d` also holds its derived fields and sleep state. Otherwise, run [mj_forward](#mj-forward) with the model from [mjb_getModel](#mjb-getmodel) to compute them. Raise an error if `sim` is out of range or the sizes differ.

### [mjb_nsim](#mjb_nsim)

``` C
int mjb_nsim(const mjBatch* b);
```

Return number of simulations.

### [mjb_nthread](#mjb_nthread)

``` C
int mjb_nthread(const mjBatch* b);
```

Return number of threads, including the caller’s.

### [mjb_persistent](#mjb_persistent)

``` C
int mjb_persistent(const mjBatch* b);
```

Return 1 if the batch keeps one mjData per simulation, 0 otherwise.

### [mjb_model](#mjb_model)

``` C
const mjModel* mjb_model(const mjBatch* b);
```

Return the batch’s copy of the model, made by [mjb_makeBatch](#mjb-makebatch). Per-simulation fields and caller models never change it; [mjb_getModel](#mjb-getmodel) gives a simulation’s own model.

## Standard math

The “functions” in this section are preprocessor macros replaced with the corresponding C standard library math functions. When MuJoCo is compiled with single precision (which is not currently available to the public, but we sometimes use it internally) these macros are replaced with the corresponding single-precision functions (not shown here). So one can think of them as having inputs and outputs of type mjtNum, where mjtNum is defined as double or float depending on how MuJoCo is compiled. We will not document these functions here; see the C standard library specification.

### mju_sqrt

``` C
#define mju_sqrt    sqrt
```

### mju_exp

``` C
#define mju_exp     exp
```

### mju_sin

``` C
#define mju_sin     sin
```

### mju_cos

``` C
#define mju_cos     cos
```

### mju_tan

``` C
#define mju_tan     tan
```

### mju_asin

``` C
#define mju_asin    asin
```

### mju_acos

``` C
#define mju_acos    acos
```

### mju_atan2

``` C
#define mju_atan2   atan2
```

### mju_tanh

``` C
#define mju_tanh    tanh
```

### mju_pow

``` C
#define mju_pow     pow
```

### mju_abs

``` C
#define mju_abs     fabs
```

### mju_log

``` C
#define mju_log     log
```

### mju_log10

``` C
#define mju_log10   log10
```

### mju_floor

``` C
#define mju_floor   floor
```

### mju_ceil

``` C
#define mju_ceil    ceil
```

## Vector math

### [mju_zero3](#mju_zero3)

``` C
void mju_zero3(mjtNum res[3]);
```

Set res = 0.

### [mju_copy3](#mju_copy3)

``` C
void mju_copy3(mjtNum res[3], const mjtNum data[3]);
```

Set res = vec.

### [mju_scl3](#mju_scl3)

``` C
void mju_scl3(mjtNum res[3], const mjtNum vec[3], mjtNum scl);
```

Set res = vec\*scl.

### [mju_add3](#mju_add3)

``` C
void mju_add3(mjtNum res[3], const mjtNum vec1[3], const mjtNum vec2[3]);
```

Set res = vec1 + vec2.

### [mju_sub3](#mju_sub3)

``` C
void mju_sub3(mjtNum res[3], const mjtNum vec1[3], const mjtNum vec2[3]);
```

Set res = vec1 - vec2.

### [mju_addTo3](#mju_addTo3)

``` C
void mju_addTo3(mjtNum res[3], const mjtNum vec[3]);
```

Set res = res + vec.

### [mju_subFrom3](#mju_subFrom3)

``` C
void mju_subFrom3(mjtNum res[3], const mjtNum vec[3]);
```

Set res = res - vec.

### [mju_addToScl3](#mju_addToScl3)

``` C
void mju_addToScl3(mjtNum res[3], const mjtNum vec[3], mjtNum scl);
```

Set res = res + vec\*scl.

### [mju_addScl3](#mju_addScl3)

``` C
void mju_addScl3(mjtNum res[3], const mjtNum vec1[3], const mjtNum vec2[3], mjtNum scl);
```

Set res = vec1 + vec2\*scl.

### [mju_normalize3](#mju_normalize3)

``` C
mjtNum mju_normalize3(mjtNum vec[3]);
```

Normalize vector; return length before normalization.

### [mju_norm3](#mju_norm3)

``` C
mjtNum mju_norm3(const mjtNum vec[3]);
```

Return vector length (without normalizing the vector).

### [mju_dot3](#mju_dot3)

``` C
mjtNum mju_dot3(const mjtNum vec1[3], const mjtNum vec2[3]);
```

Return dot-product of vec1 and vec2.

### [mju_dist3](#mju_dist3)

``` C
mjtNum mju_dist3(const mjtNum pos1[3], const mjtNum pos2[3]);
```

Return Cartesian distance between 3D vectors pos1 and pos2.

### [mju_mulMatVec3](#mju_mulMatVec3)

``` C
void mju_mulMatVec3(mjtNum res[3], const mjtNum mat[9], const mjtNum vec[3]);
```

Multiply 3-by-3 matrix by vector: res = mat \* vec.

### [mju_mulMatTVec3](#mju_mulMatTVec3)

``` C
void mju_mulMatTVec3(mjtNum res[3], const mjtNum mat[9], const mjtNum vec[3]);
```

Multiply transposed 3-by-3 matrix by vector: res = mat’ \* vec.

### [mju_cross](#mju_cross)

``` C
void mju_cross(mjtNum res[3], const mjtNum a[3], const mjtNum b[3]);
```

Compute cross-product: res = cross(a, b).

### [mju_zero4](#mju_zero4)

``` C
void mju_zero4(mjtNum res[4]);
```

Set res = 0.

### [mju_unit4](#mju_unit4)

``` C
void mju_unit4(mjtNum res[4]);
```

Set res = (1,0,0,0).

### [mju_copy4](#mju_copy4)

``` C
void mju_copy4(mjtNum res[4], const mjtNum data[4]);
```

Set res = vec.

### [mju_normalize4](#mju_normalize4)

``` C
mjtNum mju_normalize4(mjtNum vec[4]);
```

Normalize vector; return length before normalization.

### [mju_zero](#mju_zero)

``` C
void mju_zero(mjtNum* res, int n);
```

Set res = 0.

### [mju_fill](#mju_fill)

``` C
void mju_fill(mjtNum* res, mjtNum val, int n);
```

Set res = val.

### [mju_copy](#mju_copy)

``` C
void mju_copy(mjtNum* res, const mjtNum* vec, int n);
```

Set res = vec.

### [mju_sum](#mju_sum)

``` C
mjtNum mju_sum(const mjtNum* vec, int n);
```

Return sum(vec).

### [mju_L1](#mju_L1)

``` C
mjtNum mju_L1(const mjtNum* vec, int n);
```

Return L1 norm: sum(abs(vec)).

### [mju_scl](#mju_scl)

``` C
void mju_scl(mjtNum* res, const mjtNum* vec, mjtNum scl, int n);
```

Set res = vec\*scl.

### [mju_add](#mju_add)

``` C
void mju_add(mjtNum* res, const mjtNum* vec1, const mjtNum* vec2, int n);
```

Set res = vec1 + vec2.

### [mju_sub](#mju_sub)

``` C
void mju_sub(mjtNum* res, const mjtNum* vec1, const mjtNum* vec2, int n);
```

Set res = vec1 - vec2.

### [mju_addTo](#mju_addTo)

``` C
void mju_addTo(mjtNum* res, const mjtNum* vec, int n);
```

Set res = res + vec.

### [mju_subFrom](#mju_subFrom)

``` C
void mju_subFrom(mjtNum* res, const mjtNum* vec, int n);
```

Set res = res - vec.

### [mju_addToScl](#mju_addToScl)

``` C
void mju_addToScl(mjtNum* res, const mjtNum* vec, mjtNum scl, int n);
```

Set res = res + vec\*scl.

### [mju_addScl](#mju_addScl)

``` C
void mju_addScl(mjtNum* res, const mjtNum* vec1, const mjtNum* vec2, mjtNum scl, int n);
```

Set res = vec1 + vec2\*scl.

### [mju_normalize](#mju_normalize)

``` C
mjtNum mju_normalize(mjtNum* res, int n);
```

Normalize vector; return length before normalization.

### [mju_norm](#mju_norm)

``` C
mjtNum mju_norm(const mjtNum* res, int n);
```

Return vector length (without normalizing vector).

### [mju_dot](#mju_dot)

``` C
mjtNum mju_dot(const mjtNum* vec1, const mjtNum* vec2, int n);
```

Return dot-product of vec1 and vec2.

### [mju_mulMatVec](#mju_mulMatVec)

``` C
void mju_mulMatVec(mjtNum* res, const mjtNum* mat, const mjtNum* vec, int nr, int nc);
```

Multiply matrix and vector: res = mat \* vec.

### [mju_mulMatTVec](#mju_mulMatTVec)

``` C
void mju_mulMatTVec(mjtNum* res, const mjtNum* mat, const mjtNum* vec, int nr, int nc);
```

Multiply transposed matrix and vector: res = mat’ \* vec.

### [mju_mulVecMatVec](#mju_mulVecMatVec)

``` C
mjtNum mju_mulVecMatVec(const mjtNum* vec1, const mjtNum* mat, const mjtNum* vec2, int n);
```

Multiply square matrix with vectors on both sides: return vec1’ \* mat \* vec2.

### [mju_transpose](#mju_transpose)

``` C
void mju_transpose(mjtNum* res, const mjtNum* mat, int nr, int nc);
```

Transpose matrix: res = mat’.

### [mju_symmetrize](#mju_symmetrize)

``` C
void mju_symmetrize(mjtNum* res, const mjtNum* mat, int n);
```

Symmetrize square matrix \\R = \frac{1}{2}(M + M^T)\\.

### [mju_eye](#mju_eye)

``` C
void mju_eye(mjtNum* mat, int n);
```

Set mat to the identity matrix.

### [mju_mulMatMat](#mju_mulMatMat)

``` C
void mju_mulMatMat(mjtNum* res, const mjtNum* mat1, const mjtNum* mat2,
                   int r1, int c1, int c2);
```

Multiply matrices: res = mat1 \* mat2.

### [mju_mulMatMatT](#mju_mulMatMatT)

``` C
void mju_mulMatMatT(mjtNum* res, const mjtNum* mat1, const mjtNum* mat2,
                    int r1, int c1, int r2);
```

Multiply matrices, second argument transposed: res = mat1 \* mat2’.

### [mju_mulMatTMat](#mju_mulMatTMat)

``` C
void mju_mulMatTMat(mjtNum* res, const mjtNum* mat1, const mjtNum* mat2,
                    int r1, int c1, int c2);
```

Multiply matrices, first argument transposed: res = mat1’ \* mat2.

### [mju_sqrMatTD](#mju_sqrMatTD)

``` C
void mju_sqrMatTD(mjtNum* res, const mjtNum* mat, const mjtNum* diag, int nr, int nc);
```

Set res = mat’ \* diag \* mat if diag is not NULL, and res = mat’ \* mat otherwise.

### [mju_transformSpatial](#mju_transformSpatial)

``` C
void mju_transformSpatial(mjtNum res[6], const mjtNum vec[6], int flg_force,
                          const mjtNum newpos[3], const mjtNum oldpos[3],
                          const mjtNum rotnew2old[9]);
```

Coordinate transform of 6D motion or force vector in rotation:translation format. rotnew2old is 3-by-3, NULL means no rotation; flg_force specifies force or motion type.

*Nullable:* `rotnew2old`

## Sparse math

### [mju_dense2sparse](#mju_dense2sparse)

``` C
int mju_dense2sparse(mjtNum* res, const mjtNum* mat, int nr, int nc,
                     int* rownnz, int* rowadr, int* colind, int nnz);
```

Convert matrix from dense to sparse.  
nnz is size of res and colind; return 1 if too small, 0 otherwise.

### [mju_sparse2dense](#mju_sparse2dense)

``` C
void mju_sparse2dense(mjtNum* res, const mjtNum* mat, int nr, int nc,
                      const int* rownnz, const int* rowadr, const int* colind);
```

Convert matrix from sparse to dense.

### [mju_sym2dense](#mju_sym2dense)

``` C
void mju_sym2dense(mjtNum* res, const mjtNum* mat, int n,
                   const int* rownnz, const int* rowadr, const int* colind);
```

Convert lower-triangular symmetric CSR matrix to full dense matrix.

## Quaternions

### [mju_rotVecQuat](#mju_rotVecQuat)

``` C
void mju_rotVecQuat(mjtNum res[3], const mjtNum vec[3], const mjtNum quat[4]);
```

Rotate vector by quaternion.

### [mju_negQuat](#mju_negQuat)

``` C
void mju_negQuat(mjtNum res[4], const mjtNum quat[4]);
```

Conjugate quaternion, corresponding to opposite rotation.

### [mju_mulQuat](#mju_mulQuat)

``` C
void mju_mulQuat(mjtNum res[4], const mjtNum quat1[4], const mjtNum quat2[4]);
```

Multiply quaternions.

### [mju_mulQuatAxis](#mju_mulQuatAxis)

``` C
void mju_mulQuatAxis(mjtNum res[4], const mjtNum quat[4], const mjtNum axis[3]);
```

Multiply quaternion and axis.

### [mju_axisAngle2Quat](#mju_axisAngle2Quat)

``` C
void mju_axisAngle2Quat(mjtNum res[4], const mjtNum axis[3], mjtNum angle);
```

Convert axisAngle to quaternion.

### [mju_quat2Vel](#mju_quat2Vel)

``` C
void mju_quat2Vel(mjtNum res[3], const mjtNum quat[4], mjtNum dt);
```

Convert quaternion (corresponding to orientation difference) to 3D velocity.

### [mju_subQuat](#mju_subQuat)

``` C
void mju_subQuat(mjtNum res[3], const mjtNum qa[4], const mjtNum qb[4]);
```

Subtract quaternions, express as 3D velocity: qb\*quat(res) = qa.

### [mju_quat2Mat](#mju_quat2Mat)

``` C
void mju_quat2Mat(mjtNum res[9], const mjtNum quat[4]);
```

Convert quaternion to 3D rotation matrix.

### [mju_mat2Quat](#mju_mat2Quat)

``` C
void mju_mat2Quat(mjtNum quat[4], const mjtNum mat[9]);
```

Convert 3D rotation matrix to quaternion.

### [mju_derivQuat](#mju_derivQuat)

``` C
void mju_derivQuat(mjtNum res[4], const mjtNum quat[4], const mjtNum vel[3]);
```

Compute time-derivative of quaternion, given 3D rotational velocity.

### [mju_quatIntegrate](#mju_quatIntegrate)

``` C
void mju_quatIntegrate(mjtNum quat[4], const mjtNum vel[3], mjtNum scale);
```

Integrate quaternion given 3D angular velocity.

### [mju_quatZ2Vec](#mju_quatZ2Vec)

``` C
void mju_quatZ2Vec(mjtNum quat[4], const mjtNum vec[3]);
```

Construct quaternion performing rotation from z-axis to given vector.

### [mju_mat2Rot](#mju_mat2Rot)

``` C
int mju_mat2Rot(mjtNum quat[4], const mjtNum mat[9]);
```

Extract 3D rotation from an arbitrary 3x3 matrix by refining the input quaternion.

Return the number of iterations required to converge.

### [mju_euler2Quat](#mju_euler2Quat)

``` C
void mju_euler2Quat(mjtNum quat[4], const mjtNum euler[3], const char* seq);
```

Convert sequence of Euler angles (radians) to quaternion. seq\[0,1,2\] must be in ‘xyzXYZ’, lower/upper-case mean intrinsic/extrinsic rotations.

## Poses

### [mju_mulPose](#mju_mulPose)

``` C
void mju_mulPose(mjtNum posres[3], mjtNum quatres[4],
                 const mjtNum pos1[3], const mjtNum quat1[4],
                 const mjtNum pos2[3], const mjtNum quat2[4]);
```

Multiply two poses.

### [mju_negPose](#mju_negPose)

``` C
void mju_negPose(mjtNum posres[3], mjtNum quatres[4],
                 const mjtNum pos[3], const mjtNum quat[4]);
```

Conjugate pose, corresponding to the opposite spatial transformation.

### [mju_trnVecPose](#mju_trnVecPose)

``` C
void mju_trnVecPose(mjtNum res[3], const mjtNum pos[3], const mjtNum quat[4],
                    const mjtNum vec[3]);
```

Transform vector by pose.

## Decompositions / Solvers

### [mju_cholFactor](#mju_cholFactor)

``` C
int mju_cholFactor(mjtNum* mat, int n, mjtNum mindiag);
```

Cholesky decomposition: mat = L\*L’; return rank, decomposition performed in-place into mat.

### [mju_cholSolve](#mju_cholSolve)

``` C
void mju_cholSolve(mjtNum* res, const mjtNum* mat, const mjtNum* vec, int n);
```

Solve (mat\*mat’) \* res = vec, where mat is a Cholesky factor.

### [mju_cholUpdate](#mju_cholUpdate)

``` C
int mju_cholUpdate(mjtNum* mat, mjtNum* x, int n, int flg_plus);
```

Cholesky rank-one update: L\*L’ +/- x\*x’; return rank.

### [mju_cholFactorBand](#mju_cholFactorBand)

``` C
mjtNum mju_cholFactorBand(mjtNum* mat, int ntotal, int nband, int ndense,
                          mjtNum diagadd, mjtNum diagmul);
```

Band-dense Cholesky decomposition.\
Add `diagadd + diagmul*mat_ii` to diagonal before decomposition.\
Returns the minimum value of the factorized diagonal or 0 if rank-deficient.

> **Symmetric band-dense matrices**
>
> [mju_cholFactorBand](#mju-cholfactorband) and subsequent functions containing the substring “band” operate on matrices which are a generalization of symmetric [band matrices](https://en.wikipedia.org/wiki/Band_matrix). *Symmetric band-dense* or “arrowhead” matrices have non-zeros along proximal diagonal bands and dense blocks on the bottom rows and right columns. These matrices have the property that Cholesky factorization creates no fill-in and can therefore be performed efficiently in-place. Matrix structure is defined by three integers:
>
> - `ntotal`: the number of rows (columns) of the symmetric matrix.
>
> - `nband`: the number of bands under (over) the diagonal, inclusive of the diagonal.
>
> - `ndense`: the number of dense rows (columns) at the bottom (right).
>
> The non-zeros are stored in memory as two contiguous row-major blocks, colored green and blue in the illustration below. The first block has size `nband x (ntotal-ndense)` and contains the diagonal and the bands below it. The second block has size `ndense x ntotal` and contains the dense part. Total required memory is the sum of the block sizes.
>
> <figure>
> <a href="https://mujoco.readthedocs.io/en/latest/_images/arrowhead.svg"><img src="https://mujoco.readthedocs.io/en/latest/_images/arrowhead.svg" alt="../_images/arrowhead.svg" /></a>
> </figure>
>
> For example, consider an arrowhead matrix with `nband = 3`, `ndense = 2` and `ntotal = 8`. In this example, the total memory required is `3*(8-2) + 2*8 = 34` mjtNum’s, laid out as follows:
>
>     0   1   2
>         3   4   5
>             6   7   8
>                 9   10  11
>                     12  13  14
>                         15  16  17
>             18  19  20  21  22  23  24  25
>             26  27  28  29  30  31  32  33
>
> The diagonal elements are `2, 5, 8, 11, 14, 17, 24, 33`.\
> Elements `0, 1, 3, 25` are present in memory but never touched.

### [mju_cholSolveBand](#mju_cholSolveBand)

``` C
void mju_cholSolveBand(mjtNum* res, const mjtNum* mat, const mjtNum* vec,
                       int ntotal, int nband, int ndense);
```

Solve (mat\*mat’)\*res = vec where mat is a band-dense Cholesky factor.

### [mju_band2Dense](#mju_band2Dense)

``` C
void mju_band2Dense(mjtNum* res, const mjtNum* mat, int ntotal, int nband, int ndense,
                    mjtBool flg_sym);
```

Convert banded matrix to dense matrix, fill upper triangle if flg_sym\>0.

### [mju_dense2Band](#mju_dense2Band)

``` C
void mju_dense2Band(mjtNum* res, const mjtNum* mat, int ntotal, int nband, int ndense);
```

Convert dense matrix to banded matrix.

### [mju_bandMulMatVec](#mju_bandMulMatVec)

``` C
void mju_bandMulMatVec(mjtNum* res, const mjtNum* mat, const mjtNum* vec,
                       int ntotal, int nband, int ndense, int nvec, mjtBool flg_sym);
```

Multiply band-diagonal matrix with nvec vectors, include upper triangle if flg_sym\>0.

### [mju_bandDiag](#mju_bandDiag)

``` C
int mju_bandDiag(int i, int ntotal, int nband, int ndense);
```

Address of diagonal element i in band-dense matrix representation.

### [mju_eig3](#mju_eig3)

``` C
int mju_eig3(mjtNum eigval[3], mjtNum eigvec[9], mjtNum quat[4], const mjtNum mat[9]);
```

Eigenvalue decomposition of symmetric 3x3 matrix, mat = eigvec \* diag(eigval) \* eigvec’.

### [mju_boxQP](#mju_boxQP)

``` C
int mju_boxQP(mjtNum* res, mjtNum* R, int* index, const mjtNum* H, const mjtNum* g, int n,
              const mjtNum* lower, const mjtNum* upper);
```

Solve the box-constrained quadratic program

\\\min_x \\ \tfrac{1}{2} x^T H x + x^T g \quad \text{s.t.} \quad l \le x \le u \\

Return the rank of the unconstrained subspace, or -1 on failure.

inputs:  
| Argument | Size | Description |
|----|----|----|
| `n` |  | Problem dimension. |
| `H` | \\n \times n\\ | Symmetric positive definite matrix \\H\\. |
| `g` | \\n\\ | Bias vector \\g\\. |
| `lower` | \\n\\ | Lower bounds \\l\\ on \\x\\. Optional. |
| `upper` | \\n\\ | Upper bounds \\u\\ on \\x\\. Optional. |
| `res` | \\n\\ | Initial value of \\x\\, used to warmstart the solver. |

outputs:  
| Argument | Size | Description |
|----|----|----|
| `res` | \\n\\ | Solution \\x\\. |
| `R` | \\n\_{free} \times n\_{free}\\ | Cholesky factor of the unconstrained subspace. Allocated size \\n (n + 7)\\. |
| `index` | \\n\_{free}\\ | Integer array, the set of free dimensions. Allocated size \\n\\. Optional. |
| return value |  | Rank \\n\_{free} \le n\\ of the unconstrained subspace, or -1 on failure. |

notes:  
`R` must have allocated size \\n (n + 7)\\, but only \\n\_{free} \times n\_{free}\\ values are used as output. `index` (if given) must have allocated size \\n\\, but only \\n\_{free}\\ values are used as output.

The convenience function [mju_boxQPmalloc](#mju-boxqpmalloc) allocates the required data structures.

Only the lower triangles of \\H\\ and `R` are read from and written to, respectively.

### [mju_boxQPmalloc](#mju_boxQPmalloc)

``` C
void mju_boxQPmalloc(mjtNum** res, mjtNum** R, int** index, mjtNum** H, mjtNum** g, int n,
                     mjtNum** lower, mjtNum** upper);
```

Allocate heap memory for box-constrained Quadratic Program. As in [mju_boxQP](#mju-boxqp), `index`, `lower`, and `upper` are optional. Free all pointers with `mju_free()`.

### [mju_QP](#mju_QP)

``` C
int mju_QP(mjtNum* res, mjtNum* dual, int* active, mjtNum* work, const mjtNum* H,
           const mjtNum* g, int n, const mjtNum* lower, const mjtNum* upper,
           const mjtNum* A, const mjtNum* alower, const mjtNum* aupper, int m,
           const mjtNum* threshold, const mjtNum* compliance);
```

Solve the quadratic program

\\\min_x \\ \tfrac{1}{2} x^T H x + x^T g \quad \text{s.t.} \quad l \le x \le u, \quad l_A \le A x \le u_A \\

with a dual active-set method. Return the number of active constraints, or a negative value on failure.

inputs:  
| Argument | Size | Description |
|----|----|----|
| `n` |  | Number of variables. |
| `m` |  | Number of rows of \\A\\. |
| `H` | \\n \times n\\ | Positive semidefinite matrix \\H\\. |
| `g` | \\n\\ | Bias vector \\g\\. |
| `lower` | \\n\\ | Lower bounds \\l\\ on \\x\\. Optional. |
| `upper` | \\n\\ | Upper bounds \\u\\ on \\x\\. Optional. |
| `A` | \\m \times n\\ | Constraint matrix \\A\\. Optional. |
| `alower` | \\m\\ | Lower bounds \\l_A\\ on \\A x\\. Optional. |
| `aupper` | \\m\\ | Upper bounds \\u_A\\ on \\A x\\. Optional. |
| `threshold` | \\n + m\\ | Multiplier thresholds of soft constraints. Optional. |
| `compliance` | \\n + m\\ | Constraint compliances, positive for soft constraints. Optional. |
| `active` | \\n + m\\ | Integer array, the active set used to warmstart the solver. Optional. |
| `work` | see below | Workspace. Optional. |

outputs:  
<table>
<thead>
<tr>
<th><p>Argument</p></th>
<th><p>Size</p></th>
<th><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p><code class="docutils literal notranslate">res</code></p></td>
<td><p>\(n\)</p></td>
<td><p>Solution \(x\).</p></td>
</tr>
<tr>
<td><p><code class="docutils literal notranslate">dual</code></p></td>
<td><p>\(n + m\)</p></td>
<td><p>Constraint multipliers \(\lambda\). Optional.</p></td>
</tr>
<tr>
<td><p><code class="docutils literal notranslate">active</code></p></td>
<td><p>\(n + m\)</p></td>
<td><p>Integer array, the constraint states. Optional.</p></td>
</tr>
<tr>
<td><p>return value</p></td>
<td></td>
<td>Number of active constraints, or
-1: \(H\) is not positive semidefinite
-2: constraints are infeasible
-3: objective is unbounded on the feasible set
-4: iteration limit reached</td>
</tr>
</tbody>
</table>

notes:  
Constraints are the \\n\\ bounds on \\x\\ followed by the \\m\\ rows of \\A\\. This is the order of `dual`, `active`, `threshold` and `compliance`, so that \\\lambda = (\lambda_x, \lambda_A)\\.

A bound with absolute value [mjMAXVAL](APIglobals.md#glnumeric) or larger is ignored. Equal lower and upper bounds define an equality constraint.

A positive multiplier corresponds to an upper bound and a negative one to a lower bound, so that at the solution \\H x + g + \lambda_x + A^T \lambda_A = 0\\.

Constraint states are 0: inactive, ±1: holds at its upper/lower bound, ±2: yields.

A constraint with positive `compliance` is soft. It holds exactly while the absolute value of its multiplier is below its threshold \\w\\. Beyond that it yields, and is violated by \\c \\ (\|\lambda\| - w)\\, where \\c\\ is its compliance. This is the minimizer of the penalty \\w s + s^2 / (2 c)\\ on the violation \\s\\. A zero threshold gives a quadratic penalty. A large compliance approaches the exact \\\ell_1\\ penalty: the constraint yields with constant force. Problems where all constraints are soft are always feasible.

Nonzero values of `active` are used to warmstart the solver. Passing the states returned by a previous call speeds up the solution of a sequence of similar problems.

On failure, `res` is the unconstrained minimum corrected by the multipliers found so far.

Only the lower triangle of \\H\\ is read.

\\H\\ can be singular, in which case a proximal term is added and iterated to convergence. This includes linear programs, where \\H = 0\\. If the objective is unbounded on the feasible set, this is detected when a step of the proximal iteration has no curvature, decreases the objective and approaches no bound.

The method follows the dual active-set approach of [Arnström, Bemporad and Axehill (2022)](https://arxiv.org/abs/2103.16236).

`work` (if given) must have allocated size \\n^2 + (n+m)(2n+m+13)\\. If not given, a smaller workspace is allocated internally.

## Attachment

### [mjs_attach](#mjs_attach)

``` C
mjsElement* mjs_attach(mjsElement* parent, const mjsElement* child,
                       const char* prefix, const char* suffix);
```

Attach child to a parent; return the attached element if success or NULL otherwise.

## Tree elements

### [mjs_addBody](#mjs_addBody)

``` C
mjsBody* mjs_addBody(mjsBody* body, const mjsDefault* def);
```

Add child body to body; return child.

*Nullable:* `def`

### [mjs_addSite](#mjs_addSite)

``` C
mjsSite* mjs_addSite(mjsBody* body, const mjsDefault* def);
```

Add site to body; return site spec.

*Nullable:* `def`

### [mjs_addJoint](#mjs_addJoint)

``` C
mjsJoint* mjs_addJoint(mjsBody* body, const mjsDefault* def);
```

Add joint to body.

*Nullable:* `def`

### [mjs_addFreeJoint](#mjs_addFreeJoint)

``` C
mjsJoint* mjs_addFreeJoint(mjsBody* body);
```

Add freejoint to body.

### [mjs_addGeom](#mjs_addGeom)

``` C
mjsGeom* mjs_addGeom(mjsBody* body, const mjsDefault* def);
```

Add geom to body.

*Nullable:* `def`

### [mjs_addCamera](#mjs_addCamera)

``` C
mjsCamera* mjs_addCamera(mjsBody* body, const mjsDefault* def);
```

Add camera to body.

*Nullable:* `def`

### [mjs_addLight](#mjs_addLight)

``` C
mjsLight* mjs_addLight(mjsBody* body, const mjsDefault* def);
```

Add light to body.

*Nullable:* `def`

### [mjs_addFrame](#mjs_addFrame)

``` C
mjsFrame* mjs_addFrame(mjsBody* body, mjsFrame* parentframe);
```

Add frame to body.

### [mjs_delete](#mjs_delete)

``` C
int mjs_delete(mjSpec* spec, mjsElement* element);
```

Remove object corresponding to the given element; return 0 on success. Deleting a body or a frame also deletes everything inside it, along with all the elements that reference a deleted element. A [plugin instance](../XMLreference.md#plugin-instance) is deleted along with the last element that references it.

## Non-tree elements

### [mjs_addActuator](#mjs_addActuator)

``` C
mjsActuator* mjs_addActuator(mjSpec* s, const mjsDefault* def);
```

Add actuator.

*Nullable:* `def`

### [mjs_addSensor](#mjs_addSensor)

``` C
mjsSensor* mjs_addSensor(mjSpec* s);
```

Add sensor.

### [mjs_addFlex](#mjs_addFlex)

``` C
mjsFlex* mjs_addFlex(mjSpec* s);
```

Add flex.

### [mjs_makeFlex](#mjs_makeFlex)

``` C
mjsFlex* mjs_makeFlex(mjsBody* body, const char* name, const char* type, int dim,
                      const char* dof, const int count[3], const int cellcount[3],
                      const double spacing[3], const double scale[3], double radius,
                      double mass, double inertiabox, int equality, int rigid, int flatskin,
                      int elastic2d, const double pos[3], const double quat[4],
                      const double origin[3], const char* file, const mjVFS* vfs);
```

Create a [flexcomp](../XMLreference.md#body-flexcomp) in `body` and return the resulting flex; the arguments correspond to the flexcomp attributes. If `file` is the name of an existing [mesh asset](../XMLreference.md#asset-mesh), the flexcomp uses that mesh as with the [mesh](../XMLreference.md#body-flexcomp-mesh) attribute, otherwise `file` is the name of a mesh file. The flexcomp is expanded immediately, so later changes to the mesh asset do not affect the created flex.

### [mjs_addPair](#mjs_addPair)

``` C
mjsPair* mjs_addPair(mjSpec* s, const mjsDefault* def);
```

Add contact pair.

*Nullable:* `def`

### [mjs_addExclude](#mjs_addExclude)

``` C
mjsExclude* mjs_addExclude(mjSpec* s);
```

Add excluded body pair.

### [mjs_addEquality](#mjs_addEquality)

``` C
mjsEquality* mjs_addEquality(mjSpec* s, const mjsDefault* def);
```

Add equality.

*Nullable:* `def`

### [mjs_addTendon](#mjs_addTendon)

``` C
mjsTendon* mjs_addTendon(mjSpec* s, const mjsDefault* def);
```

Add tendon.

*Nullable:* `def`

### [mjs_wrapSite](#mjs_wrapSite)

``` C
mjsWrap* mjs_wrapSite(mjsTendon* tendon, const char* name);
```

Wrap site using tendon.

### [mjs_wrapGeom](#mjs_wrapGeom)

``` C
mjsWrap* mjs_wrapGeom(mjsTendon* tendon, const char* name, const char* sidesite);
```

Wrap geom using tendon.

### [mjs_wrapJoint](#mjs_wrapJoint)

``` C
mjsWrap* mjs_wrapJoint(mjsTendon* tendon, const char* name, double coef);
```

Wrap joint using tendon.

### [mjs_wrapPulley](#mjs_wrapPulley)

``` C
mjsWrap* mjs_wrapPulley(mjsTendon* tendon, double divisor);
```

Wrap pulley using tendon.

### [mjs_addNumeric](#mjs_addNumeric)

``` C
mjsNumeric* mjs_addNumeric(mjSpec* s);
```

Add numeric.

### [mjs_addText](#mjs_addText)

``` C
mjsText* mjs_addText(mjSpec* s);
```

Add text.

### [mjs_addTuple](#mjs_addTuple)

``` C
mjsTuple* mjs_addTuple(mjSpec* s);
```

Add tuple.

### [mjs_addKey](#mjs_addKey)

``` C
mjsKey* mjs_addKey(mjSpec* s);
```

Add keyframe.

### [mjs_addPlugin](#mjs_addPlugin)

``` C
mjsPlugin* mjs_addPlugin(mjSpec* s);
```

Add plugin.

### [mjs_addDefault](#mjs_addDefault)

``` C
mjsDefault* mjs_addDefault(mjSpec* s, const char* classname, const mjsDefault* parent);
```

Add default.

*Nullable:* `parent`

## Set actuator parameters

### [mjs_setToMotor](#mjs_setToMotor)

``` C
const char* mjs_setToMotor(mjsActuator* actuator);
```

Set actuator to motor; return error if any.

### [mjs_setToPosition](#mjs_setToPosition)

``` C
const char* mjs_setToPosition(mjsActuator* actuator, double kp, double kv[1],
                              double dampratio[1], double timeconst[1], double inheritrange);
```

Set actuator to position; return error if any.

### [mjs_setToIntVelocity](#mjs_setToIntVelocity)

``` C
const char* mjs_setToIntVelocity(mjsActuator* actuator, double kp, double kv[1],
                                 double dampratio[1], double timeconst[1], double inheritrange);
```

Set actuator to integrated velocity; return error if any.

### [mjs_setToVelocity](#mjs_setToVelocity)

``` C
const char* mjs_setToVelocity(mjsActuator* actuator, double kv);
```

Set actuator to velocity servo; return error if any.

### [mjs_setToOrientation](#mjs_setToOrientation)

``` C
const char* mjs_setToOrientation(mjsActuator* actuator, double kp, double kv[1],
                                 double dampratio[1], int ctrlspec);
```

Set actuator to orientation servo.

### [mjs_setToPID](#mjs_setToPID)

``` C
const char* mjs_setToPID(mjsActuator* actuator, double kp, double kv[1], double dampratio[1],
                         double ki[1], double imax[1], double slewmax[1], double inheritrange,
                         int ctrlspec);
```

Set actuator to PID controller.

### [mjs_setToDamper](#mjs_setToDamper)

``` C
const char* mjs_setToDamper(mjsActuator* actuator, double kv);
```

Set actuator to activate damper; return error if any.

### [mjs_setToCylinder](#mjs_setToCylinder)

``` C
const char* mjs_setToCylinder(mjsActuator* actuator, double timeconst,
                              double bias, double area, double diameter);
```

Set actuator to hydraulic or pneumatic cylinder; return error if any.

### [mjs_setToMuscle](#mjs_setToMuscle)

``` C
const char* mjs_setToMuscle(mjsActuator* actuator, double timeconst[2], double tausmooth,
                            double range[2], double force, double scale, double lmin,
                            double lmax, double vmax, double fpmax, double fvmax);
```

Set actuator to muscle; return error if any.a

### [mjs_setToAdhesion](#mjs_setToAdhesion)

``` C
const char* mjs_setToAdhesion(mjsActuator* actuator, double gain);
```

Set actuator to active adhesion; return error if any.

### [mjs_setToDCMotor](#mjs_setToDCMotor)

``` C
const char* mjs_setToDCMotor(mjsActuator* actuator, double motorconst[2], double resistance,
                             double nominal[3], double saturation[3], double inductance[2],
                             double cogging[3], double controller[6], double thermal[6],
                             double lugre[5], int ctrlspec);
```

Set actuator to DC motor; return error if any.

*Nullable:* `motorconst`, `nominal`, `saturation`, `inductance`, `cogging`, `controller`, `thermal`, `lugre`

## Assets

### [mjs_addMesh](#mjs_addMesh)

``` C
mjsMesh* mjs_addMesh(mjSpec* s, const mjsDefault* def);
```

Add mesh.

*Nullable:* `def`

### [mjs_addHField](#mjs_addHField)

``` C
mjsHField* mjs_addHField(mjSpec* s);
```

Add height field.

### [mjs_addSkin](#mjs_addSkin)

``` C
mjsSkin* mjs_addSkin(mjSpec* s);
```

Add skin.

### [mjs_addTexture](#mjs_addTexture)

``` C
mjsTexture* mjs_addTexture(mjSpec* s, const mjsDefault* def);
```

Add texture.

*Nullable:* `def`

### [mjs_addMaterial](#mjs_addMaterial)

``` C
mjsMaterial* mjs_addMaterial(mjSpec* s, const mjsDefault* def);
```

Add material.

*Nullable:* `def`

### [mjs_makeMesh](#mjs_makeMesh)

``` C
int mjs_makeMesh(mjsMesh* mesh, mjtMeshBuiltin builtin, double* params, int nparams);
```

Generate a built-in procedural mesh of type [mjtMeshBuiltin](APItypes.md#mjtmeshbuiltin) with the given parameters. Returns 0 on success; on failure, returns a nonzero value and sets the error of the spec. The parameters of the sphere, hemisphere, cone, supersphere, supertorus, wedge and plate types are those of the corresponding [mesh/builtin](../XMLreference.md#asset-mesh-builtin) attribute. The procedural types below generate the same shapes as the corresponding [flexcomp](../XMLreference.md#body-flexcomp) types; their nodes are stored in double precision in `usernode`.

- `mjMESH_BUILTIN_GRID` (count\[3\], spacing\[3\], \[dim\]): A regular grid with `count[i] > 0` points along each axis, separated by `spacing[i]`. `dim` (default 3) creates tetrahedra (3) or triangles (2); `count` must be 1 along the axes beyond `dim`.

- `mjMESH_BUILTIN_BOX`, `mjMESH_BUILTIN_CYLINDER`, `mjMESH_BUILTIN_ELLIPSOID` (count\[3\], spacing\[3\], \[dim\]): The surface of a box grid with `count[i] >= 2` points along each axis, projected onto the shape. `dim` (default 3) creates tetrahedra connecting the surface to the center (3) or surface triangles (2).

- `mjMESH_BUILTIN_SQUARE`, `mjMESH_BUILTIN_DISC` (count\[3\], spacing\[3\]): A triangulated square, or a disc obtained by radial projection of the square; `count[2]` must be 1.

Types without volume (square, disc, and grid, box, cylinder and ellipsoid with `dim` \< 3) change a `legacy` [inertia](../XMLreference.md#asset-mesh-inertia) to `shell`.

## Find and get utilities

### [mjs_getSpec](#mjs_getSpec)

``` C
mjSpec* mjs_getSpec(const mjsElement* element);
```

Get spec from body.

### [mjs_getOriginSpec](#mjs_getOriginSpec)

``` C
mjSpec* mjs_getOriginSpec(const mjsElement* element);
```

get spec that originally defined an element contrary to mjs_getSpec, this does not change after attachment

### [mjs_getCompiler](#mjs_getCompiler)

``` C
mjsCompiler* mjs_getCompiler(const mjsElement* element);
```

Get compiler associated with element’s origin spec.

### [mjs_findSpec](#mjs_findSpec)

``` C
mjSpec* mjs_findSpec(const mjSpec* spec, const char* name);
```

Find spec (model asset) by name.

### [mjs_findBody](#mjs_findBody)

``` C
mjsBody* mjs_findBody(const mjSpec* s, const char* name);
```

Find body in spec by name.

### [mjs_findElement](#mjs_findElement)

``` C
mjsElement* mjs_findElement(const mjSpec* s, mjtObj type, const char* name);
```

Find element in spec by name.

### [mjs_findChild](#mjs_findChild)

``` C
mjsBody* mjs_findChild(const mjsBody* body, const char* name);
```

Find child body by name.

### [mjs_getParent](#mjs_getParent)

``` C
mjsBody* mjs_getParent(const mjsElement* element);
```

Get parent body.

### [mjs_getFrame](#mjs_getFrame)

``` C
mjsFrame* mjs_getFrame(const mjsElement* element);
```

Get parent frame.

### [mjs_findFrame](#mjs_findFrame)

``` C
mjsFrame* mjs_findFrame(const mjSpec* s, const char* name);
```

Find frame by name.

### [mjs_getDefault](#mjs_getDefault)

``` C
mjsDefault* mjs_getDefault(const mjsElement* element);
```

Get default corresponding to an element.

### [mjs_findDefault](#mjs_findDefault)

``` C
mjsDefault* mjs_findDefault(const mjSpec* s, const char* classname);
```

Find default in model by class name.

### [mjs_getSpecDefault](#mjs_getSpecDefault)

``` C
mjsDefault* mjs_getSpecDefault(const mjSpec* s);
```

Get global default from model.

### [mjs_getId](#mjs_getId)

``` C
int mjs_getId(const mjsElement* element);
```

Get element id.

### [mjs_firstChild](#mjs_firstChild)

``` C
mjsElement* mjs_firstChild(const mjsBody* body, mjtObj type, int recurse);
```

Return body’s first child of given type. If recurse is nonzero, also search the body’s subtree.

### [mjs_nextChild](#mjs_nextChild)

``` C
mjsElement* mjs_nextChild(const mjsBody* body, const mjsElement* child, int recurse);
```

Return body’s next child of the same type; return NULL if child is last.

If recurse is nonzero, also search the body’s subtree.

### [mjs_firstElement](#mjs_firstElement)

``` C
mjsElement* mjs_firstElement(const mjSpec* s, mjtObj type);
```

Return spec’s first element of selected type.

### [mjs_nextElement](#mjs_nextElement)

``` C
mjsElement* mjs_nextElement(const mjSpec* s, const mjsElement* element);
```

Return spec’s next element; return NULL if element is last.

### [mjs_getWrapTarget](#mjs_getWrapTarget)

``` C
mjsElement* mjs_getWrapTarget(const mjsWrap* wrap);
```

Get wrapped element in tendon path.

### [mjs_getWrapSideSite](#mjs_getWrapSideSite)

``` C
mjsSite* mjs_getWrapSideSite(const mjsWrap* wrap);
```

Get wrapped element side site in tendon path if it has one, nullptr otherwise.

### [mjs_getWrapDivisor](#mjs_getWrapDivisor)

``` C
double mjs_getWrapDivisor(const mjsWrap* wrap);
```

Get divisor of mjsWrap wrapping a puller.

### [mjs_getWrapCoef](#mjs_getWrapCoef)

``` C
double mjs_getWrapCoef(const mjsWrap* wrap);
```

Get coefficient of mjsWrap wrapping a joint.

## Attribute setters

### [mjs_setName](#mjs_setName)

``` C
int mjs_setName(mjsElement* element, const char* name);
```

Set element’s name; return 0 on success.

### [mjs_setBuffer](#mjs_setBuffer)

``` C
void mjs_setBuffer(mjByteVec* dest, const void* array, int size);
```

Copy buffer.

### [mjs_setString](#mjs_setString)

``` C
void mjs_setString(mjString* dest, const char* text);
```

Copy text to string.

### [mjs_setStringVec](#mjs_setStringVec)

``` C
void mjs_setStringVec(mjStringVec* dest, const char* text);
```

Split text to entries and copy to string vector.

### [mjs_setInStringVec](#mjs_setInStringVec)

``` C
mjtBool mjs_setInStringVec(mjStringVec* dest, int i, const char* text);
```

Set entry in string vector.

### [mjs_appendString](#mjs_appendString)

``` C
void mjs_appendString(mjStringVec* dest, const char* text);
```

Append text entry to string vector.

### [mjs_setInt](#mjs_setInt)

``` C
void mjs_setInt(mjIntVec* dest, const int* array, int size);
```

Copy int array to vector.

### [mjs_appendIntVec](#mjs_appendIntVec)

``` C
void mjs_appendIntVec(mjIntVecVec* dest, const int* array, int size);
```

Append int array to vector of arrays.

### [mjs_setFloat](#mjs_setFloat)

``` C
void mjs_setFloat(mjFloatVec* dest, const float* array, int size);
```

Copy float array to vector.

### [mjs_appendFloatVec](#mjs_appendFloatVec)

``` C
void mjs_appendFloatVec(mjFloatVecVec* dest, const float* array, int size);
```

Append float array to vector of arrays.

### [mjs_setDouble](#mjs_setDouble)

``` C
void mjs_setDouble(mjDoubleVec* dest, const double* array, int size);
```

Copy double array to vector.

### [mjs_setPluginAttributes](#mjs_setPluginAttributes)

``` C
void mjs_setPluginAttributes(mjsPlugin* plugin, void* attributes);
```

Set plugin attributes.

## Attribute getters

### [mjs_getName](#mjs_getName)

``` C
mjString* mjs_getName(mjsElement* element);
```

Get element’s name.

### [mjs_getString](#mjs_getString)

``` C
const char* mjs_getString(const mjString* source);
```

Get string contents.

### [mjs_getInStringVec](#mjs_getInStringVec)

``` C
const char* mjs_getInStringVec(const mjStringVec* source, int i);
```

Get entry in string vector, or NULL if out of bounds.

### [mjs_getDouble](#mjs_getDouble)

``` C
const double* mjs_getDouble(const mjDoubleVec* source, int* size);
```

Get double array contents and optionally its size.

*Nullable:* `size`

### [mjs_getWrapNum](#mjs_getWrapNum)

``` C
int mjs_getWrapNum(const mjsTendon* tendonspec);
```

Get number of elements a tendon wraps.

### [mjs_getWrap](#mjs_getWrap)

``` C
mjsWrap* mjs_getWrap(const mjsTendon* tendonspec, int i);
```

Get mjsWrap element at position i in the tendon path.

### [mjs_getPluginAttributes](#mjs_getPluginAttributes)

``` C
const void* mjs_getPluginAttributes(const mjsPlugin* plugin);
```

Get plugin attributes.

## Spec utilities

### [mjs_setDefault](#mjs_setDefault)

``` C
void mjs_setDefault(mjsElement* element, const mjsDefault* def);
```

Set element’s default.

### [mjs_setFrame](#mjs_setFrame)

``` C
int mjs_setFrame(mjsElement* dest, mjsFrame* frame);
```

Set element’s enclosing frame; return 0 on success.

### [mjs_resolveOrientation](#mjs_resolveOrientation)

``` C
const char* mjs_resolveOrientation(double quat[4], mjtByte degree, const char* sequence,
                                   const mjsOrientation* orientation);
```

Resolve alternative orientations to quat; return error if any.

### [mjs_fuseStatic](#mjs_fuseStatic)

``` C
int mjs_fuseStatic(mjSpec* s, const mjVFS* vfs);
```

Fuse the static bodies of the spec with their parents. A body without joints is replaced by a [frame](../XMLreference.md#frame) in its parent, which has the pose of the body and holds its geoms, sites, cameras, lights, frames and child bodies, in the same coordinates as before. The inertia of the body is added to that of the parent. The compiled model has the same kinematics and dynamics, with fewer bodies. Bodies which cannot be fused without changing the model are kept, see [fusestatic](../XMLreference.md#compiler-fusestatic), which applies this function before compiling. Pointers to the bodies which were fused are no longer valid. Assets are read as in [mj_compile](#mj-compile). Returns the number of bodies fused, 0 if the spec is unchanged, or -1 on error, in which case nothing is fused.

### [mjs_discardVisual](#mjs_discardVisual)

``` C
int mjs_discardVisual(mjSpec* s, const mjVFS* vfs);
```

Discard the elements of the spec which are only visual: materials and textures, the geoms which do not collide, and the meshes which are then not used; an element which another refers to by name is kept. If a discarded geom was used for inferring the inertia of its body, that inertia becomes the explicit inertial of the body, as in [mjs_adoptInertial](#mjs-adoptinertial), so the compiled model has the same dynamics. See [discardvisual](../XMLreference.md#compiler-discardvisual), which applies this function before compiling. Pointers to the elements which were discarded are no longer valid. Assets are read as in [mj_compile](#mj-compile), and only if inertia is inferred from a discarded geom. Returns the number of elements discarded, 0 if the spec is unchanged, or -1 on error, in which case nothing is discarded.

### [mjs_dedupAssets](#mjs_dedupAssets)

``` C
int mjs_dedupAssets(mjSpec* s);
```

Merge the textures and meshes of the spec which would compile to the same asset: textures with the same resolved file or buffer and the same parameters, meshes with the same resolved file or arrays and the same parameters, names excluded. The first asset of each group keeps its name, every reference to the others (materials, lights, geoms, sites, default classes, sensors, tuples) is rewritten to it, and the others are deleted as by [mjs_delete](#mjs-delete), so pointers to them are no longer valid. An unnamed asset is left alone, as is a mesh with a plugin. Nothing is read from disk: a model which attaches the same sub-model several times is merged without its asset files. Returns the number of assets merged, 0 if the spec is unchanged, or -1 on error, in which case nothing is merged.

### [mjs_adoptInertial](#mjs_adoptInertial)

``` C
int mjs_adoptInertial(mjsBody* body, const mjVFS* vfs);
```

Make the inertial which compilation infers for a body part of the spec. The mass, inertia and inertial frame which the compiler calculates from the geoms of the body, as the spec is now, are written as the explicit inertial of the body, so that later changes to its geoms no longer affect them. Compiling before and after gives the same model: the values are those before the scaling of [settotalmass](../XMLreference.md#compiler-settotalmass). Nothing is done if the inertial of the body is not inferred. It is an error when [inertiafromgeom](../XMLreference.md#compiler-inertiafromgeom) is “true”, which infers the inertia of every body whatever its inertial. Assets are read as in [mj_compile](#mj-compile). Returns 0 on success.

To read an inferred inertial without adopting it, compile and look it up in [mjModel](APItypes.md#mjmodel) with [mjs_getId](#mjs-getid).

### [mjs_bodyToFrame](#mjs_bodyToFrame)

``` C
mjsFrame* mjs_bodyToFrame(mjsBody** body);
```

Transform body into a frame.

### [mjs_setUserValue](#mjs_setUserValue)

``` C
void mjs_setUserValue(mjsElement* element, const char* key, const void* data);
```

Set user payload, overriding the existing value for the specified key if present.

### [mjs_setUserValueWithCleanup](#mjs_setUserValueWithCleanup)

``` C
void mjs_setUserValueWithCleanup(mjsElement* element, const char* key,
                                 const void* data,
                                 void (*cleanup)(const void*));
```

Set user payload, overriding the existing value for the specified key if present. This version differs from mjs_setUserValue in that it takes a cleanup function that will be called when the user payload is deleted.

### [mjs_getUserValue](#mjs_getUserValue)

``` C
const void* mjs_getUserValue(mjsElement* element, const char* key);
```

Return user payload or NULL if none found.

### [mjs_deleteUserValue](#mjs_deleteUserValue)

``` C
void mjs_deleteUserValue(mjsElement* element, const char* key);
```

Delete user payload.

### [mjs_sensorDim](#mjs_sensorDim)

``` C
int mjs_sensorDim(const mjsSensor* sensor);
```

Return sensor dimension.

## Element initialization

### [mjs_defaultSpec](#mjs_defaultSpec)

``` C
void mjs_defaultSpec(mjSpec* spec);
```

Default spec attributes.

### [mjs_defaultOrientation](#mjs_defaultOrientation)

``` C
void mjs_defaultOrientation(mjsOrientation* orient);
```

Default orientation attributes.

### [mjs_defaultBody](#mjs_defaultBody)

``` C
void mjs_defaultBody(mjsBody* body);
```

Default body attributes.

### [mjs_defaultFrame](#mjs_defaultFrame)

``` C
void mjs_defaultFrame(mjsFrame* frame);
```

Default frame attributes.

### [mjs_defaultJoint](#mjs_defaultJoint)

``` C
void mjs_defaultJoint(mjsJoint* joint);
```

Default joint attributes.

### [mjs_defaultGeom](#mjs_defaultGeom)

``` C
void mjs_defaultGeom(mjsGeom* geom);
```

Default geom attributes.

### [mjs_defaultSite](#mjs_defaultSite)

``` C
void mjs_defaultSite(mjsSite* site);
```

Default site attributes.

### [mjs_defaultCamera](#mjs_defaultCamera)

``` C
void mjs_defaultCamera(mjsCamera* camera);
```

Default camera attributes.

### [mjs_defaultLight](#mjs_defaultLight)

``` C
void mjs_defaultLight(mjsLight* light);
```

Default light attributes.

### [mjs_defaultFlex](#mjs_defaultFlex)

``` C
void mjs_defaultFlex(mjsFlex* flex);
```

Default flex attributes.

### [mjs_defaultMesh](#mjs_defaultMesh)

``` C
void mjs_defaultMesh(mjsMesh* mesh);
```

Default mesh attributes.

### [mjs_defaultHField](#mjs_defaultHField)

``` C
void mjs_defaultHField(mjsHField* hfield);
```

Default height field attributes.

### [mjs_defaultSkin](#mjs_defaultSkin)

``` C
void mjs_defaultSkin(mjsSkin* skin);
```

Default skin attributes.

### [mjs_defaultTexture](#mjs_defaultTexture)

``` C
void mjs_defaultTexture(mjsTexture* texture);
```

Default texture attributes.

### [mjs_defaultMaterial](#mjs_defaultMaterial)

``` C
void mjs_defaultMaterial(mjsMaterial* material);
```

Default material attributes.

### [mjs_defaultPair](#mjs_defaultPair)

``` C
void mjs_defaultPair(mjsPair* pair);
```

Default pair attributes.

### [mjs_defaultEquality](#mjs_defaultEquality)

``` C
void mjs_defaultEquality(mjsEquality* equality);
```

Default equality attributes.

### [mjs_defaultTendon](#mjs_defaultTendon)

``` C
void mjs_defaultTendon(mjsTendon* tendon);
```

Default tendon attributes.

### [mjs_defaultActuator](#mjs_defaultActuator)

``` C
void mjs_defaultActuator(mjsActuator* actuator);
```

Default actuator attributes.

### [mjs_defaultSensor](#mjs_defaultSensor)

``` C
void mjs_defaultSensor(mjsSensor* sensor);
```

Default sensor attributes.

### [mjs_defaultNumeric](#mjs_defaultNumeric)

``` C
void mjs_defaultNumeric(mjsNumeric* numeric);
```

Default numeric attributes.

### [mjs_defaultText](#mjs_defaultText)

``` C
void mjs_defaultText(mjsText* text);
```

Default text attributes.

### [mjs_defaultTuple](#mjs_defaultTuple)

``` C
void mjs_defaultTuple(mjsTuple* tuple);
```

Default tuple attributes.

### [mjs_defaultKey](#mjs_defaultKey)

``` C
void mjs_defaultKey(mjsKey* key);
```

Default keyframe attributes.

### [mjs_defaultPlugin](#mjs_defaultPlugin)

``` C
void mjs_defaultPlugin(mjsPlugin* plugin);
```

Default plugin attributes.

## Element casting

### [mjs_asBody](#mjs_asBody)

``` C
mjsBody* mjs_asBody(mjsElement* element);
```

Safely cast an element as mjsBody, or return NULL if the element is not an mjsBody.

### [mjs_asGeom](#mjs_asGeom)

``` C
mjsGeom* mjs_asGeom(mjsElement* element);
```

Safely cast an element as mjsGeom, or return NULL if the element is not an mjsGeom.

### [mjs_asJoint](#mjs_asJoint)

``` C
mjsJoint* mjs_asJoint(mjsElement* element);
```

Safely cast an element as mjsJoint, or return NULL if the element is not an mjsJoint.

### [mjs_asSite](#mjs_asSite)

``` C
mjsSite* mjs_asSite(mjsElement* element);
```

Safely cast an element as mjsSite, or return NULL if the element is not an mjsSite.

### [mjs_asCamera](#mjs_asCamera)

``` C
mjsCamera* mjs_asCamera(mjsElement* element);
```

Safely cast an element as mjsCamera, or return NULL if the element is not an mjsCamera.

### [mjs_asLight](#mjs_asLight)

``` C
mjsLight* mjs_asLight(mjsElement* element);
```

Safely cast an element as mjsLight, or return NULL if the element is not an mjsLight.

### [mjs_asFrame](#mjs_asFrame)

``` C
mjsFrame* mjs_asFrame(mjsElement* element);
```

Safely cast an element as mjsFrame, or return NULL if the element is not an mjsFrame.

### [mjs_asActuator](#mjs_asActuator)

``` C
mjsActuator* mjs_asActuator(mjsElement* element);
```

Safely cast an element as mjsActuator, or return NULL if the element is not an mjsActuator.

### [mjs_asSensor](#mjs_asSensor)

``` C
mjsSensor* mjs_asSensor(mjsElement* element);
```

Safely cast an element as mjsSensor, or return NULL if the element is not an mjsSensor.

### [mjs_asFlex](#mjs_asFlex)

``` C
mjsFlex* mjs_asFlex(mjsElement* element);
```

Safely cast an element as mjsFlex, or return NULL if the element is not an mjsFlex.

### [mjs_asPair](#mjs_asPair)

``` C
mjsPair* mjs_asPair(mjsElement* element);
```

Safely cast an element as mjsPair, or return NULL if the element is not an mjsPair.

### [mjs_asEquality](#mjs_asEquality)

``` C
mjsEquality* mjs_asEquality(mjsElement* element);
```

Safely cast an element as mjsEquality, or return NULL if the element is not an mjsEquality.

### [mjs_asExclude](#mjs_asExclude)

``` C
mjsExclude* mjs_asExclude(mjsElement* element);
```

Safely cast an element as mjsExclude, or return NULL if the element is not an mjsExclude.

### [mjs_asTendon](#mjs_asTendon)

``` C
mjsTendon* mjs_asTendon(mjsElement* element);
```

Safely cast an element as mjsTendon, or return NULL if the element is not an mjsTendon.

### [mjs_asNumeric](#mjs_asNumeric)

``` C
mjsNumeric* mjs_asNumeric(mjsElement* element);
```

Safely cast an element as mjsNumeric, or return NULL if the element is not an mjsNumeric.

### [mjs_asText](#mjs_asText)

``` C
mjsText* mjs_asText(mjsElement* element);
```

Safely cast an element as mjsText, or return NULL if the element is not an mjsText.

### [mjs_asTuple](#mjs_asTuple)

``` C
mjsTuple* mjs_asTuple(mjsElement* element);
```

Safely cast an element as mjsTuple, or return NULL if the element is not an mjsTuple.

### [mjs_asKey](#mjs_asKey)

``` C
mjsKey* mjs_asKey(mjsElement* element);
```

Safely cast an element as mjsKey, or return NULL if the element is not an mjsKey.

### [mjs_asMesh](#mjs_asMesh)

``` C
mjsMesh* mjs_asMesh(mjsElement* element);
```

Safely cast an element as mjsMesh, or return NULL if the element is not an mjsMesh.

### [mjs_asHField](#mjs_asHField)

``` C
mjsHField* mjs_asHField(mjsElement* element);
```

Safely cast an element as mjsHField, or return NULL if the element is not an mjsHField.

### [mjs_asSkin](#mjs_asSkin)

``` C
mjsSkin* mjs_asSkin(mjsElement* element);
```

Safely cast an element as mjsSkin, or return NULL if the element is not an mjsSkin.

### [mjs_asTexture](#mjs_asTexture)

``` C
mjsTexture* mjs_asTexture(mjsElement* element);
```

Safely cast an element as mjsTexture, or return NULL if the element is not an mjsTexture.

### [mjs_asMaterial](#mjs_asMaterial)

``` C
mjsMaterial* mjs_asMaterial(mjsElement* element);
```

Safely cast an element as mjsMaterial, or return NULL if the element is not an mjsMaterial.

### [mjs_asPlugin](#mjs_asPlugin)

``` C
mjsPlugin* mjs_asPlugin(mjsElement* element);
```

Safely cast an element as mjsPlugin, or return NULL if the element is not an mjsPlugin.
