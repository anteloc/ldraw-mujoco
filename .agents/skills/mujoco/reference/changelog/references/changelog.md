# Changelog

## Upcoming Version (not yet released)

### General

- Added *mju_QP*, a dual active-set solver for dense convex quadratic programs with bounds and two-sided linear constraints. Constraints can be soft: a soft constraint holds exactly up to a threshold on its multiplier and then yields with a given compliance, so problems with soft constraints remain feasible. The solver can be warmstarted from a previous active set. The Hessian can be singular or zero (a linear program).

### Deformables

- Added `mjModel.flex_cellempty` (`nflexcell x 1`) and `mjModel.flex_celladr`, flagging the empty (pruned) cells of interpolated flexes. Points of an interpolated flex, such as contact points, are now evaluated in their active cell: their natural cell, or the nearest non-empty cell if it is empty, consistently with the vertex positions (`flex_vertcell`). Previously contact weights near pruned cells could weight the pinned nodes of the empty cell.

### Compiler

- Sequentially appending elements to an [mjSpec](APIreference/APItypes.md) body tree now runs in $`O(1)`$ instead of rebuilding the model's tree lists, making procedural model construction up to ~250x faster.
- [strippath](XMLreference.md) no longer strips file names that match a registered [resource provider](programming/extension.md), such as `package://` URIs. These names are not filesystem paths, and the compiler already treats them as absolute when combining them with [meshdir](XMLreference.md).

### Rendering


Breaking changes

- Planar reflections in the Filament renderer are now energy conserving: diffuse base color is attenuated by one minus the Fresnel reflection weight (dielectrics only; metals are unchanged), so a surface with `reflectance="1"` is a pure mirror regardless of its base color. Previously, reflections were added on top of the fully lit diffuse surface, washing out reflections on bright materials.

- Orthographic free and tracking cameras now derive their vertical view height from the camera distance and [global/fovy](XMLreference.md) (matching the perspective view height at the lookat point) and place the eye behind the model's bounding sphere so zooming scales the view without near-plane clipping. Previously, `global/fovy` was used directly as a fixed view height in length units (45 by default), so zooming had no visible effect and toggling orthographic made the view jump. Fixed orthographic cameras ([camera/fovy](XMLreference.md)) are unchanged. In Studio and [simulate](programming/samples.md), the Free Camera field-of-view control shows the vertical view height in length units while in orthographic mode, and editing it changes the camera distance rather than `global/fovy`. For these cameras *mjv_cameraFrustum* now returns a vertical extent that depends on `mjvCamera.distance`.

  **Migration:** Models that set `global/fovy` to a length for an orthographic free camera now render zoomed in. Set `global/fovy` back to an angle in degrees (the default is 45); the view height then follows the camera distance.


- Added [mjGEOM_DISC](APIreference/APItypes.md) rendering-only geom type for flat double-sided discs and annuli (`size = [r_out, r_in, 0]`).
- Fixed Filament planar reflections leaking geometry behind or crossing the mirror plane by clipping the reflection camera at the mirror plane with an oblique near-plane projection (`3902`).

### Python bindings

- Fixed a memory leak in `mujoco-core` (introduced in 4.0.0) where `import mujoco` without `glfw` installed stored the `ImportError` in `mujoco.rendering.classic.gl_context` and kept every local variable on the importing call stack alive for the life of the process (`3928`, reported by `adenzler-nvidia`).

### Plugins

- Added a first-party [resource provider](programming/extension.md) plugin, `plugin/package_uri`, that serves ROS-style `package://` URIs by locating packages through `AMENT_PREFIX_PATH` and `ROS_PACKAGE_PATH` without depending on ROS. It is not included in release packages: build it from source and load the resulting shared library with *mj_loadPluginLibrary* before parsing a model, so that URDF and MJCF files can reference ROS package assets unchanged. Contribution by `noah-wardlow`.

### OpenUSD

- The native C++ [OpenUSD exporter](OpenUSD/exporting.md) and `LayerSink` now author `xformOp:translate` (`double3`) and `xformOp:orient` (`quatd`) instead of `xformOp:transform` (`matrix4d`), avoiding shear artifacts when USD or external renderers interpolate between time samples.

## Version 4.0.1 (November 11, 2026)

### Compiler

1.  `21a076966` Added *mjs_getInStringVec* to read entries from an [mjStringVec](APIreference/APItypes.md) by index.

### Python bindings

2.  `a937a4f91` Enabled the MuJoCo Studio Web Viewer (`mujoco-studio --gfx=web` and `mujoco.studio.launch_web`) on Windows by shipping the precompiled browser client in a platform-independent `mujoco-studio-wasm` wheel installed automatically by `mujoco-studio`.

### Bug fixes

3.  `9ae9bad01` Fixed a bug in the sparse Cholesky factorization introduced in 4.0.0, which merged rows with different descendants into one supernode and gave the Newton solver a wrong Hessian factor when the constraint Jacobian is sparse, causing slow convergence, wrong accelerations and divergence (`3767`).
4.  `144ede984` *mj_loadAllPluginLibraries* now skips a dynamic library that fails to load with a warning instead of calling *mju_error*, so one unloadable library in the plugin directory no longer aborts [simulate](programming/samples.md) at startup. In the 4.0.0 macOS and Linux archives this happened with the USD decoder plugin, which can only be loaded from a Python process.
5.  `409f981ab` Fixed issues in single-shot [multicontact](computation/index.md) for cylinder edge collisions (`3748`, `3752`).

## Version 4.0.0 (November 6, 2026)

[<img src="images/changelog/speculative_advancement_light.svg" class="only-light only-lightalign-right" style="width:50.0%" alt="image" />](https://mujoco.readthedocs.io/en/latest/computation/speculative.html#spadvancement)

[<img src="images/changelog/speculative_advancement_dark.svg" class="only-dark only-darkalign-right" style="width:50.0%" alt="image" />](https://mujoco.readthedocs.io/en/latest/computation/speculative.html#spadvancement)

### Significant new features

1.  `89daf8d19` Added the [speculative](XMLreference.md) enable flag for [speculative contacts](computation/speculative.md) to prevent fast-moving convex geoms from tunneling through thin obstacles within a single timestep. On the right, one step of conservative advancement between two rotating boxes. See [model/speculative/](https://github.com/google-deepmind/mujoco/tree/main/model/speculative/) for examples.


</div>


2.  Added elasto-plasticity, with stateful plastic deformation stored in `mjData.plastic` (`mjSTATE_PLASTIC`):

    - `e140c026f` Ideal elasto-plasticity for joint ([springyield](XMLreference.md)) and tendon ([spatial](XMLreference.md), [fixed](XMLreference.md)) springs (left).
    - `0c0f63b3f`, `c39fe6f02`, `e3bd72742`, `7cb32488b` Continuum elasto-plasticity ([yield](XMLreference.md)) for 2D and 3D [flexes](XMLreference.md), with separate stretching and bending yield strains for 2D shells, volumetric-deviatoric (von Mises $`J_2`$) stretching and 2D shell bending return mapping (right).
    - See [model/plastic/](https://github.com/google-deepmind/mujoco/tree/main/model/plastic/) for examples.

    [<img src="https://www.gstatic.com/mujoco/model/plastic/wire.webp" class="align-left" style="width:45.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/model/plastic/wire.xml)

    [<img src="https://www.gstatic.com/mujoco/model/plastic/clay.webp" class="align-right" style="width:45.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/model/plastic/clay.xml)


</div>


3.  `abaf8d518` Split the Python distribution into `mujoco-core` (minimal bindings and C library depending only on `numpy`), `mujoco-studio` (Studio and Filament renderer bindings), and `mujoco` (default package installing both). When upgrading from a pre-split `mujoco` installation with `pip`, uninstall first (`pip uninstall -y mujoco && pip install mujoco`) or run `pip install --force-reinstall --no-deps mujoco mujoco-core mujoco-studio` after upgrading so `pip` does not remove files moved to `mujoco-core`. To switch an existing `mujoco` installation to core-only, run `pip uninstall -y mujoco mujoco-studio && pip install --force-reinstall --no-deps mujoco-core`.

### Engine


Breaking changes

4.  `a65050166` Changed the semantics of [sidesite](XMLreference.md): the tendon now goes around the geom the same way as the path from the first endpoint, through the side site, to the second endpoint (thin grey line below). Formally, the tendon is the shortest path homotopic to this polyline in the wrapping plane with the geom removed.

    <img src="images/XMLreference/sidesite_homotopy_light.svg" class="only-light only-lightalign-center" style="width:90.0%" alt="image" />

    <img src="images/XMLreference/sidesite_homotopy_dark.svg" class="only-dark only-darkalign-center" style="width:90.0%" alt="image" />

    Previously, a half-plane test was used, which could make the tendon jump onto the geom, a discontinuity in tendon length, when the segment between the endpoints moved away from the side site while clear of the geom. It could also select the wrong side for wraps longer than 180 degrees. Top row: old rule; bottom row: new rule.

    <img src="images/changelog/sidesite_old_vs_new_light.svg" class="only-light only-lightalign-center" style="width:90.0%" alt="image" />

    <img src="images/changelog/sidesite_old_vs_new_dark.svg" class="only-dark only-darkalign-center" style="width:90.0%" alt="image" />

    The new rule has a single discontinuity: when an endpoint crosses the ray opposite the side site, the path through the side site changes its winding around the geom and the tendon snaps off. This can change the behavior of existing models.

    **Migration:** Place side sites so that the endpoints do not cross this ray over the range of motion, typically near the middle of the wrapped arc. For example, the side sites of the [two-link arm](https://github.com/google-deepmind/mujoco/blob/main/model/tendon_arm/arm26.xml) were moved from directly below the joints to 45 degrees below the arm, which reproduces the previous tendon lengths exactly.


5.  `9a7f240f0` The `RK4` [integrator](XMLreference.md) is now fourth-order accurate for the orientations of ball and free joints. Previously, the angular velocities of the Runge-Kutta stages were combined without the Runge-Kutta-Munthe-Kaas correction, so orientations converged only at second order. This changes the simulation of models with ball or free joints that use `RK4`.
6.  `9916cc5f7` Added `surfacevel[3]` to [mjContact](APIreference/APItypes.md), storing the relative [surface velocity](XMLreference.md) (`geom[1]` minus `geom[0]`) in the contact frame `(tangent1, tangent2, spin)`. Collision detection populates it from `geom_surfacevel` when `mjModel.flg_surfacevel` is set, and external contact generators can write it directly (setting `flg_surfacevel = 1` if no geom specifies `surfacevel`). Contact-point visualization now draws a single relative tangential velocity arrow per active frictional contact.
7.  `629feb74b` Added `xiquat`, `geom_xquat`, and `site_xquat` to [mjData](APIreference/APItypes.md), storing the Cartesian quaternion orientations of body inertias, geoms, and sites alongside `ximat`, `geom_xmat`, and `site_xmat`.
8.  `64af6504f` Added `mjModel.tendon_type` with values from the new [mjtTendon](APIreference/APItypes.md) enum, distinguishing fixed and spatial tendons. Previously, the type was implied by whether the first path element was a joint.

### Deformables


Breaking changes

9.  `1d6cc8ff5` Removed the `cable` plugin (`plugin/elasticity`) and the `composite` element, which are superseded by 1D [flexcomp](XMLreference.md) with [elasticity](XMLreference.md).

    **Migration:**

    - `count` and `curve` / `size` / `vertex`: use [flexcomp](XMLreference.md) `dim="1"` with `type="grid"`, `count`, and `spacing` (or `type="circle"` for closed loops), or `type="direct"` with `point`. Add `<edge equality="true"/>` to keep edges inextensible.
    - Geom `size` (capsule radius): set flexcomp `radius`. For geom `type="box"`, set `<elasticity section="box" sectionsize="..."/>`.
    - Plugin `bend` and `twist`: set `<elasticity young="..." shear="..."/>`.
    - Root attachment `initial`: `initial="none"` maps to `<pin id="0 1"/>` (clamps the first edge's material frame to the parent body and omits `<name>_twist_0`); `initial="ball"` maps to `<pin id="0"/>` (spherical anchor at the first vertex, keeping `<name>_twist_0` free); `initial="free"` maps to no `<pin/>`.
    - Plugin `flat="true"`: define the rod straight in `qpos0` (e.g., `type="grid"`) and set the curved initial pose via `qpos` or a [keyframe](XMLreference.md) (curves defined directly in `point` are at rest in `qpos0`, corresponding to `flat="false"`).
    - Plugin `vmax` stress coloring: not supported.
    - Integrator: use `integrator="discrete"` for implicit integration (or `Euler` / `RK4`; `implicit` and `implicitfast` are not supported for 1D rod elasticity).
    - Body names `B_first` / `B_<i>` / `B_last`: unpinned vertices create bodies `<name>_<i>` (pinned vertices attach directly to the parent body), plus per-edge twist bodies and joints (see the next entry).

10. `95cf15e58` Open elastic 1D [flexcomps](XMLreference.md) with at least two elements now create per-edge twist bodies with hinge joints `<name>_twist_0`, ..., `<name>_twist` under the world body (omitting the joint of an edge clamped by pinning both of its points: `<name>_twist_0` for `<pin id="0 1"/>`, and `<name>_twist` for the last two points of a rod with at least three elements), and store their time-parallel reference frames and reference twists in `mjData.plastic`. This changes `nq`, `nv`, `nbody`, `nplastic` and the `qpos` layout of such models, shifts the indices of bodies and joints declared after the flexcomp, and changes the simulation: rods now roll on surfaces and twist in grippers. Box sections (<span class="at">section</span> **box**) require these joints, so raw [flexes](XMLreference.md) with box sections now need them too, and their collision <span class="at">radius</span> is set to the minor half-size of the section (an explicit <span class="at">radius</span> that differs from it is now a compile error).

    **Migration:** Update keyframes and any code that indexes `qpos`, `qvel` or bodies by number, preferably addressing vertex bodies (`<name>_<i>`) and twist joints by name. Save and restore rod state with `mjSTATE_PLASTIC`. Raw box-section flexes need hinge joints named as above (see [elasticity](XMLreference.md)).

11. `7ba52b533` Fixed the elastic constants of non-interpolated [flexes](XMLreference.md) (**full** and **radial** [dofs](XMLreference.md)), which now match [young](XMLreference.md), [poisson](XMLreference.md) and [thickness](XMLreference.md) as documented, and the interpolated flexes:

    - 3D Saint Venant-Kirchhoff stretching used twice the first Lamé parameter $`\lambda`$.
    - 2D stretching used a quarter of the shear modulus $`\mu`$ and half of the 3D $`\lambda`$, instead of $`\mu`$ and the plane-stress $`\lambda^* = E \nu / (1 - \nu^2)`$.
    - 2D bending used $`\tfrac{3}{4}(1-\nu) D`$ instead of the plate bending rigidity $`D = E t^3 / (12 (1 - \nu^2))`$.

    Models with these flexes become stiffer, except 3D models with zero Poisson's ratio, which are unchanged.

    **Migration:** To keep the previous behavior, use these parameters:

    - 3D: $`\nu' = 2\nu / (1 + 2\nu)`$ and $`E' = E (1 + \nu') / (1 + \nu)`$.
    - 2D bending only (`elastic2d="bend"`): $`E' = \tfrac{3}{4}(1 - \nu) E`$.
    - 2D stretching (`elastic2d="stretch"` or `"both"`): $`\nu' = 2\nu`$, which is exact for $`\nu < 1/4`$ (so that $`\nu' < 1/2`$). Then:
      - `"stretch"`: $`E' = E (1 + 2\nu) / (4 (1 + \nu))`$.
      - `"both"`: $`t' = t \sqrt{3 (1 - 2\nu)}`$ and $`E' = E t (1 + 2\nu) / (4 (1 + \nu) t')`$.

    The flex models in `model/flex` were remapped in this way, so their behavior is unchanged.

12. `c0e6b15fd` 1D rod bending [elasticity](XMLreference.md) (`dim="1"` with positive `young`) is no longer supported under `implicit` and `implicitfast`, matching 2D and 3D flex elasticity.

    **Migration:** Use `integrator="discrete"` for implicit integration, or `integrator="Euler"` with a small timestep for explicit integration.

13. `c0e6b15fd` Flex [edge stiffness](XMLreference.md) and [damping](XMLreference.md) are no longer supported under `integrator="discrete"` (where they were integrated explicitly rather than in the effective metric).

    **Migration:** Use [elasticity](XMLreference.md) (or [edge equality](XMLreference.md)), or use `Euler`/`RK4`/`implicitfast`.

14. `b2577a630` Unpinned [flexcomp](XMLreference.md) models (with **full**, **trilinear**, or **quadratic** [dofs](XMLreference.md)) now fail to compile if their parent or ancestor body has joints when no active vertices or nodes are [pinned](XMLreference.md) to it.

    **Migration:** Remove joints from the parent/ancestor body of an unpinned flex, or pin at least one vertex/node to the parent body with [pin](XMLreference.md).

15. `145cdc2be` Removed `flexvert` equality constraints (`<equality><flexvert>` and `<edge equality="vert"/>` in [flexcomp](XMLreference.md)), along with the associated [mjModel](APIreference/APItypes.md) fields (`nJfv`, `flex_vertedgeadr`, `flex_vertedgenum`, `flex_vertedge`, `flex_vertmetric`, `flexvert_J_rownnz`, `flexvert_J_rowadr`, `flexvert_J_colind`) and [mjData](APIreference/APItypes.md) fields (`flexvert_length`, `flexvert_J`). `mjEQ_FLEXVERT` is retained as an unsupported placeholder in [mjtEq](APIreference/APItypes.md) and causes an error if used.

    **Migration:** Use continuum [elasticity](XMLreference.md) with `integrator="discrete"` or [edge equality](XMLreference.md) for 2D cloth models.

16. `6f28d4adf` Flexes now support per-element visual materials: `mjModel.flex_matid` is now `(nflexelem x 1)` instead of `(nflex x 1)`, and the `material` attribute on [flex](XMLreference.md) and [flexcomp](XMLreference.md) (`mjsFlex.material`) is now `mjStringVec` rather than `mjString` (accepting either a single material name broadcast to all elements or one material name per element).

    **Migration:** Index `mjModel.flex_matid` by element `m->flex_elemadr[f] + e` rather than by flex `f`. In C, set `mjsFlex.material` with `mjs_setStringVec` (or `mjs_appendString`) instead of `mjs_setString`; in Python, assign a list of material names (e.g. `flex.material = ['mat']`).

17. `7ba5d6732` Records of 1D flexes in `mjModel.flex_bending` grow from 4 to 10 values, to store curved reference configurations and pairs of adjacent bent vertices. Previously, each record was `[v_prev, v, v_next, k]`.

    **Migration:** Read 1D records with stride 10. A record whose fourth value is negative is a single hinge `[v0, v1, v2, -1, k1, k2 - k1, |kb0|, jnt, kt, b]`: principal bending stiffnesses `k1 <= k2`, the twist hinge joint `jnt` of the edge `(v1, v2)` (-1 if none; the joint of the first edge, when present, is that of the first record minus one), torsional stiffness `kt`, and the signed minor half-size `b` of a box section (0 for circular sections). Otherwise it is a hinge pair `[v0, v1, v2, v3, w0, w1, om0[4]]`.


18. `8892bf44b`, `0d8a109de`, `f9a589361` Sparse `Newton` ([solver](XMLreference.md)) is 1.4-3x faster on [flex](XMLreference.md) models, using fill-reducing DOF ordering, incremental active-set Hessian updates, direct [elliptic cone](XMLreference.md) folding, and pre-ordered sparse Cholesky for the 2D `discrete` [integrator](XMLreference.md) smooth solve. Most flex models in `model/flex` now use `solver="Newton"`, and the experimental [ipc](XMLreference.md) flag now supports `solver="Newton"` in addition to `solver="CG"`.
19. `57d9b960f` `solver="Newton"` with the `discrete` [integrator](XMLreference.md) now supports [flex](XMLreference.md) vertices and nodes (both standard and interpolated) attached to articulated bodies. Previously, such models required `solver="CG"`. The `model/flex/gripper_trilinear.xml` gripper now uses `solver="Newton"`. MuJoCo Warp still requires `solver="CG"` for such models.
20. `7ba5d6732` 1D rod bending [elasticity](XMLreference.md) now supports curved reference configurations and torsional stiffness: vertices bent by more than $`10^{-4}`$ rad in `qpos0` keep their reference curvature and dihedral twist angle, so that rods such as rings, arcs, and coil springs are at rest in their compiled shape. Previously, such models failed to compile. The new [shear](XMLreference.md) attribute optionally overrides the shear modulus used for torsion. Open rods carry per-edge twist joints (see the breaking change above) with per-edge polar inertia, frame-indifferent relative Rayleigh torsional damping, time-parallel reference frames, and frictional contact lever-arm coupling. Box sections additionally use anisotropic principal stiffnesses with equalized damping ratio ($`\sqrt{k_1 k_2}`$ on the weak axis) and an oriented box in the DER material frame for rendering and collision detection. See the [documentation](XMLreference.md).
21. `9ca6b7171` Volumetric interpolated flexes (**trilinear** or **quadratic** [dofs](XMLreference.md) with `elastic2d="none"`) now integrate cell stiffness and lump nodal masses over the mesh volume using Finite Cell Method (FCM) subcell quadrature instead of treating every non-empty grid cell as a full cube. This changes the stiffness and nodal mass distribution of volumetric interpolated flexes whose mesh does not fill its bounding box, as well as the nodal mass distribution of multi-cell **trilinear** flexes.
22. `f9f3ee653` Contacts with flex elements now distribute the contact to the element vertices with the barycentric coordinates of the point on the element closest to the contact. Previously the vertex weights were inversely proportional to the distances from the contact, which do not interpolate the contact point: the contact Jacobian measured the velocity of a different material point, and the contact force exerted a spurious torque on the element. This changes the simulation of models with flex contacts.
23. `115907e6d` Interpolated flexes (**trilinear** or **quadratic** [dofs](XMLreference.md)) now support [passive](XMLreference.md) contact.
24. `51572eab0` Flex [edge damping](XMLreference.md) is now integrated explicitly under `implicit` and `implicitfast` (previously it also damped rigid translation).
25. `9fb4eca48` Fixed contact Jacobians of quadratic flexes, which dropped nodes with negative basis weights.
26. `b16e09838` Sphere and capsule contacts with 3D flex elements are now computed analytically instead of the general convex pipeline.
27. `3bbf510d4` Improved numerical stability of [nativeccd](XMLreference.md) convex collision detection and [multiccd](XMLreference.md) contact generation. This can slightly change contacts for models with convex or mesh collisions.

### Compiler


Breaking changes

28. `00057bcef` Models that [include](XMLreference.md) the same file through different paths, which previously loaded, are now rejected with `already included`.

    **Migration:** Remove redundant `<include>` elements referencing the same file.

29. The compiler now rejects the following invalid models, which previously loaded:

    - `b6192732b` [Height fields](XMLreference.md) with [nrow](XMLreference.md) or [ncol](XMLreference.md) less than 2.
    - `a4c699040` [Fixed tendons](XMLreference.md) referencing `ball`/`free` or duplicate joints, or with negative [armature](XMLreference.md).
    - `a4c699040` [Spatial tendon](XMLreference.md) [pulleys](XMLreference.md) with non-positive [divisor](XMLreference.md).
    - `a4c699040` [camprojection](XMLreference.md) or camera-attached [rangefinder](XMLreference.md) sensors referencing an invalid camera or a camera with non-positive [resolution](XMLreference.md).
    - `881e53e2e` [Skins](XMLreference.md) with out-of-range face vertex indices.
    - `881e53e2e` *mjs_makeMesh* `mjMESH_BUILTIN_CONE` calls with fewer than 3 edges or `radius` outside `[0, 1]`.

    **Migration:** Ensure height fields have `nrow >= 2` and `ncol >= 2`, fixed tendons wrap distinct `slide` or `hinge` joints with non-negative armature, pulley divisors are positive, cameras referenced by `camprojection` or `rangefinder` sensors have positive resolution, skin face indices are in `[0, nvert)`, and cone meshes have at least 3 edges and a radius in `[0, 1]`.


30. `432376a59` [fullinertia](XMLreference.md) and inertias inferred from geoms which are not positive definite are now bounded by [boundinertia](XMLreference.md) when it is positive. Previously they gave a compile error.
31. `a4c699040` *mj_encode* now supports binary MJB output for [mjSpec](APIreference/APItypes.md) via the `model/vnd.mujoco.mjb` content type.

### Rendering

32. `1edd2c67d` Added a [castshadow](XMLreference.md) attribute to [geom](XMLreference.md) (`mjsGeom.castshadow`, `mjModel.geom_castshadow`, `mjvGeom.castshadow`; default `true`) to disable shadow casting per geom in both the classic OpenGL and Filament renderers, and *mjrf_setRenderableCastShadow* (`mjrf.Renderable.set_cast_shadow` in Python) to toggle shadow casting of Filament renderables dynamically.
33. `c831b97d6` Added horizon haze and skybox visibility support to Filament rendering: infinite planes are centered beneath the camera and blend smoothly into the skybox horizon according to [visual/map/haze](XMLreference.md) and [visual/rgba/haze](XMLreference.md), toggled per view via `haze` and `skybox` on [mjrfRenderRequest](APIreference/APItypes.md) ([mjRND_HAZE](APIreference/APItypes.md) and [mjRND_SKYBOX](APIreference/APItypes.md)).
34. `939bc882e` When no light specifies an [intensity](XMLreference.md), the fallback intensity given to each light in Filament rendering is now scaled by the brightness of its diffuse color, which is factored out of the light's color. Lights look the same, but the brightest directional light now casts the shadows, rather than an arbitrary one that could differ between runs.
35. `0fc0b44d6` Added [filament.material.base_color_type](programming/rendering.md) flag for configuring how the base color material parameter is interpreted.
36. `e19117325` Added *mjrf_flush* (`mjrf.Context.flush` in Python) to flush pending operations to the rendering backend and invoke any completed callbacks.
37. `93033f5ba` Added [mjRND_POST_PROCESSING](APIreference/APItypes.md) rendering flag.
38. `e66b53380` Allow [headlight.active](XMLreference.md) to be set to "false", "true", or "auto" while continuing to support integer values (0=false, 1=true, 2=auto). Change the default to "auto" instead of "true".

### Python bindings

39. `68390c316` Removed support for Python 3.10, now that it's [deprecated upstream](https://devguide.python.org/versions).
40. `a1b9fce44` Bundled the MuJoCo Sphinx manual (`doc/**/*.rst`) and agent skills (`doc/skills/**/*.md`) inside the `mujoco` package under `mujoco/doc/`.

### Samples


Breaking changes

41. `006586d30` Removed `sample/record.cc`; multi-frame raw RGB24 video recording is now supported by [sample/render.cc](programming/samples.md) across both the Filament and classic OpenGL backends via `--duration` and `--fps`.

    **Migration:** Replace `record model.xml T F out.rgb 0` with `render model.xml out.rgb --duration=T --fps=F` (or pass `-` as the output path to pipe top-down RGB24 frames directly to `ffmpeg`; `vflip` is no longer needed).


### Models

42. `9647e0290` Added six [elasto-plasticity](https://github.com/google-deepmind/mujoco/tree/main/model/plastic/) example models, each placing an elastic reference next to a plastic counterpart: joint and tendon springs, 2D shells and 3D continua.
43. `89daf8d19` Added [speculative contacts](https://github.com/google-deepmind/mujoco/tree/main/model/speculative/) example models: a Newton's cradle of thin plates, an interlocking chain, and a ball struck by a hinged flipper.

### Documentation

44. `74ad32d20` Added documentation for [MuJoCo Studio](studio/index.md), covering [web](studio/web_viewers.md) and [native](studio/native_viewers.md) viewers, [architecture](studio/architecture.md), and [Python](studio/python_plugins.md) and [C++](studio/cpp.md) development.
45. `0f1092ebb` Added a [Model tuning](modeling.md) guide to the Modeling chapter---covering the fidelity--speed trade-off, [tuning defaults](modeling.md), priority-ordered [global](modeling.md) and [model-level](modeling.md) parameters, [deformables](modeling.md), and [system identification](modeling.md)---along with module documentation for [mujoco.sysid](python.md).

### Bug fixes

46. `fdf141238` [accelerometer](XMLreference.md) and [framelinacc](XMLreference.md) sensors and *mj_objectAcceleration* on static and mocap bodies now report the gravitational proper acceleration, like a dynamic body at rest. Previously they returned zero, a regression introduced in 3.3.7.
47. `c4137ef7c`, `aeb871ba1` Actuators saturated by joint or tendon actuator force limits ([joint](XMLreference.md) and [tendon](XMLreference.md) <span class="at">actuatorfrcrange</span>) no longer contribute implicit actuator derivatives, changing integration under `implicit`, `implicitfast`, and `discrete`. Because saturated actuators no longer contribute implicit damping, models with light links and no armature may need joint armature or a smaller timestep.
48. `aaf2abaa7`, `1b46a496e` Fixed [sleep](programming/simulation.md) filtering bugs in history sensors (<span class="at">nsample</span>, <span class="at">delay</span>, <span class="at">interval</span>), *mj_energyPos*, flex passive forces, tendon limit and frictionloss constraints, two-tree tendon [armature](XMLreference.md) and bias, *mj_subtreeVel*, and caller-supplied *mj_rne* buffers.
49. `13fb7844e` *mj_setConst* now wakes all [sleeping](programming/simulation.md) trees, since it recomputes their kinematics at `qpos0` and `qpos_spring`. Previously their cached poses could be left at `qpos_spring`. It also no longer overwrites `cam_xpos`, `cam_xmat`, `light_xpos` and `light_xdir` in [mjData](APIreference/APItypes.md), which left static cameras and lights with tracking or targeting at their fixed-mode poses.
50. `432376a59` Contact pairs created with an undefined `mjsPair.solref` now mix the `solref` of their geoms using `solmix` when both are positive, like contacts not defined by pairs. Previously they always took the element-wise minimum.
51. `18d65f4e0`, `ea6aa8214` Filament depth and segmentation renders no longer apply post-processing (tone mapping, dithering), which corrupted depth values and segment ID colors; perspective depth renders now project with the finite [zfar](XMLreference.md) plane instead of Filament's infinite far plane, matching orthographic depth and the classic renderer; and the `mjr_` compatibility API now respects `readDepthMap` ([mjtDepthMap](APIreference/APItypes.md)) on [mjrContext](APIreference/APItypes.md) in *mjr_readPixels* and colors geoms by `segid + 1` like [mjRND_IDCOLOR](APIreference/APItypes.md) so a geom with `segid` 0 no longer renders as background.
52. `9b19fd07c`, `ef34acbee` File paths on Windows are now interpreted as UTF-8 rather than the active ANSI code page, fixing loading and saving files, plugin library discovery and loading (*mj_loadPluginLibrary*, *mj_loadAllPluginLibraries*), and [simulate](programming/samples.md) executable directory lookup when paths contain non-ASCII UTF-8 characters (`3139`). Contribution by `mar-yan24`.
53. `a5ff8f6c7` Fixed [dcmotor](XMLreference.md) parameter handling: allow zero [motorconst](XMLreference.md) for `input="none"`, reject negative constants (e.g. `motorconst="-a b"` is now rejected instead of silently using `K = b`), replace capacitance when an inconsistent [thermal](XMLreference.md) triple is given, clear inherited [forcerange](XMLreference.md) when [saturation](XMLreference.md) is authored, let zero `saturation` or `inductance` clear class defaults, and validate [actdim](XMLreference.md) at compile time.
54. `8694cc9ce` Improved numerical stability of sphere and cylinder [spatial tendon](XMLreference.md) [geom](XMLreference.md) wrapping at wrap onset. Thanks to `M-Colley` for reporting and analyzing the issue in [MJWarp](mjwarp/index.md) issue [1772](https://github.com/google-deepmind/mujoco_warp/issues/1772).
55. `b6192732b` *mj_ray* now scales SDF hit distances by `1 / ||vec||` for non-unit ray vectors, and `mju_rayTriangle` rejects triangle intersections behind the ray origin.
56. `00c19f04b` *mj_resetData*, *mj_copyData*, and *mj_recompile* now preserve the destination [mjData](APIreference/APItypes.md) thread pool instead of dropping and leaking it.
57. `a206daa42` `mju_mat2Rot` now normalizes the input quaternion and escapes 180-degree stationary points (saddles and minima) that do not maximize $`\operatorname{tr}(R^\top M)`$.
58. `afa16414c` Fixed the cotangent weight and length scale of the curved reference term of 2D [flex](XMLreference.md) bending ([elastic2d](XMLreference.md) **bend** or **both**), so out-of-plane bending forces vanish at curved rest configurations and scale consistently with model size.
59. `a4c699040` Fixed several bugs when editing or copying an [mjSpec](APIreference/APItypes.md):
    - *mjs_delete* (`MjSpec.delete` in Python) now removes deleted default classes from the class lookup map instead of leaving dangling pointers.
    - *mj_copyBack* (`MjSpec.copy_back` in Python) preserves material `metallic`, `roughness`, and `texuniform` attributes.
    - *mjs_findChild* no longer matches a non-world body against itself.
    - *mjs_setToMuscle* accepts `NULL` `timeconst` and `range` pointers.
60. `00057bcef` Fixed several MJCF XML loading and saving bugs:
    - [include](XMLreference.md) no longer double-prefixes the model directory on nested or relative paths.
    - Loading MJCF now applies enclosing [frame](XMLreference.md) transforms to [flexcomp](XMLreference.md), and allows explicit <span class="at">range</span> or [inheritrange](XMLreference.md) attributes on actuator shortcuts to override conflicting defaults.
    - [default/tendon](XMLreference.md) now accepts [armature](XMLreference.md), [actuatorfrclimited](XMLreference.md), and [actuatorfrcrange](XMLreference.md), which were previously emitted when saving XML and then failed schema validation on reload.
    - Saving MJCF (*mj_saveLastXML*, *mj_saveXML*, *mj_saveXMLString*) now preserves [texture](XMLreference.md) [nchannel](XMLreference.md) and clamps emitted [gridlayout](XMLreference.md) to `gridsize` (while loading resets `gridlayout` when an authored `gridsize` differs from the inherited default), compares material [layer](XMLreference.md) textures, camera [sensorsize](XMLreference.md), and light [texture](XMLreference.md) against default classes, and writes all attributes on plugin-backed meshes and <span class="at">reftype</span>/<span class="at">refname</span> on plugin sensors.
61. `881e53e2e` Legacy `.msh` meshes with mirrored [scale](XMLreference.md) no longer double-flip face winding (which inverted faces), and `.msh` files without vertex normals no longer populate empty face normals or reject custom normals on recompilation.

## Version 3.17.0 (October 22, 2026)

### Significant new features

1.  `c00ed8153` Added a [batch API](programming/simulation.md) in `mujoco/mjbatch.h` (in Python as [mujoco.batch](python.md)): many simulations of one model stepped on a thread pool of its own, each held as its integration state and loaded into an `mjData` for each call, so memory scales with threads and results are bit-identical to a plain loop at any thread count. It supports per-simulation model and option fields or models of the caller's, observations of the state after a step, recorded trajectories, persistent simulations (required for sleep), and arbitrary per-simulation functions. Follows the design of [mjbatch](https://github.com/kevinzakka/mjbatch) by `kevinzakka`.

### Engine

2.  Flex improvements:
    - `94483e166` Added bending [elasticity](XMLreference.md) for 1D flexes, using a twist-free isotropic discrete elastic rod model. The cross-section is selected with the new [section](XMLreference.md) attribute: a circle of the flex radius, or a box with half-sizes [sectionsize](XMLreference.md) that uses the stiffness of its weak axis. It is enabled by a positive [young](XMLreference.md) modulus, requires a straight reference configuration (curved initial poses can be set with `qpos` or keyframes), is compatible with edge equality constraints, and is integrated implicitly by the [discrete](XMLreference.md) integrator. Previously `young` was ignored for 1D flexes: existing models that set it now bend, and fail to compile if the cross-section is degenerate (zero radius with the default circle section), if a vertex joins a zero-length edge, or if the rod is not straight.
    - `36d0df9a5`, `897e3fcb1` Interpolated flexes (**trilinear** or **quadratic** [dofs](XMLreference.md)) now support [self-collision](XMLreference.md), excluding elements in the same or neighboring cells.
    - `39dd10f2d` The default arena [memory](XMLreference.md) for flex models is now much smaller, sized from the flex mesh topology instead of `nv^2`. If the Newton solver runs out of arena memory it falls back to CG with a warning.
3.  *mj_setConst* now computes only quantities derived from other fields of [mjModel](APIreference/APItypes.md), while the compiler alone resolves spec-level conventions:
    - `55c1b585a`, `d6d41f324` The damping of position actuators from [dampratio](XMLreference.md), the spring length of tendons from `(-1, -1)`, and model statistics are now resolved only at compile time, not by *mj_setConst*. Set the model fields directly when editing a compiled model (*mj_copyBack* now copies tendon spring lengths back to the spec).

    - `c8362756d` Constraint solvers now scale their termination criteria by the trace of the current inertia matrix (of the model or island) instead of `mjModel.stat.meaninertia`. Models solved with PGS, noslip or islands disabled can stop at slightly different iterations. The [meaninertia](XMLreference.md) attribute is deprecated and now emits a compile warning; remove it to migrate.

    - `abddec5b9` For body-based [weld](XMLreference.md) constraints without a specified [relpose](XMLreference.md), the relative pose in `qpos0` is now recomputed by *mj_setConst* when the model is modified after compilation (matching the second body's [anchor](XMLreference.md) in body-based `connect` constraints). The compiler marks such welds with a nonzero `eq_data[11]`, and [mjNEQDATA](APIreference/APIglobals.md) increased from 11 to 12.


      Breaking ABI changes

      [mjNEQDATA](APIreference/APIglobals.md) increased from 11 to 12, and *mj_setConst* overwrites `eq_data[3:10]` of body-based welds that had no `relpose` at compile time. Zero `eq_data[11]` before calling *mj_setConst* to set the relative pose of such a weld directly.


    - `865316f19` Added `MJSETCONST_ARRAYS` and `MJSETCONST_SCALARS` in `mjxmacro.h`, listing the [mjModel](APIreference/APItypes.md) arrays and scalars read and written by each phase of *mj_setConst*.
4.  `e15ecd842` Added single-shot [multicontact](computation/index.md) for geoms with positive contact [margins](XMLreference.md).
5.  `7394a8672` *mju_boxQP* now updates its Cholesky factor incrementally with *mju_cholUpdate*, making cold-started solves 1.4-1.6x faster and warm-started solves 1.9-2.9x faster.
6.  `aa0f88e77` Trees marked [sleep="init"](XMLreference.md) which cannot be put to sleep now cause a warning rather than an error, and start awake. See [Sleeping](programming/simulation.md) for details.

### Compiler


Breaking API changes

7.  `aad2e2982` *mjs_fuseStatic* and *mjs_discardVisual* now return the number of bodies fused or elements discarded, and -1 on error. Previously they returned 0 on success, so a caller could not tell whether the spec changed. In Python, `MjSpec.fuse_static` and `MjSpec.discard_visual` return the same number instead of `None`.

    **Migration:** Test for an error with `< 0` rather than `!= 0`.

8.  `084828896` *mjs_addTexture* now takes a default class, like *mjs_addMesh* and *mjs_addMaterial*.

    **Migration:** `mjs_addTexture(spec)` → `mjs_addTexture(spec, NULL)`. `MjSpec.add_texture` is unchanged.


9.  `3576818f5`, `b0f206d04` Textures can be left [by reference](modeling.md) instead of being decoded into [mjModel](APIreference/APItypes.md). With [compiler/passthrough](XMLreference.md) set to "textures", or [texture/embed](XMLreference.md) set to "false", a single-file texture is not read at compile time; the model holds its path instead of its pixels, so a scene that attaches many textured sub-models loads in a fraction of the memory and time. In addition, a compiled [mjSpec](APIreference/APItypes.md) no longer keeps the decoded pixels of its textures between compilations.
    - `3576818f5` What the model holds: `tex_adr` is -1, `tex_width` and `tex_height` are 0, `ntexdata` excludes the texture, the resolved path is at `tex_pathadr`, and any authored [content_type](XMLreference.md) is at the new `tex_contenttypeadr`. Flipped, composite, six-file, procedural, buffer and in-memory textures stay embedded, as does any texture with <span class="at">embed</span> "true".
    - `1be762d0c` Getting the pixels: *mj_loadTexture* decodes a texture of either kind, and *mj_embedAssets* returns a copy of the model with every by-reference texture loaded (which followed by *mj_saveModel* gives a hermetic MJB). Both are in Python as `mujoco.mj_loadTexture` and `mujoco.mj_embedAssets`.
    - `fd92ba1db` Rendering: the built-in and Filament renderers load by-reference textures on demand, and Filament uploads each file once for all textures that share it. A file that fails to resolve produces a warning and an untextured material.
10. `084828896` Textures can have [default classes](XMLreference.md): `mjsDefault` has a `texture` member and [texture](XMLreference.md) takes a [class](XMLreference.md).
11. `4e9a2de2d` Added *mjs_dedupAssets* (`MjSpec.dedup_assets`), which merges the textures and meshes of an [mjSpec](APIreference/APItypes.md) that would compile to the same asset, as those of a sub-model attached several times do: the first of each group is kept and every reference to the others is rewritten to it. Like *mjs_fuseStatic*, it returns the number of assets merged.
12. `027cb3dd8` The asset paths in [mjModel](APIreference/APItypes.md) (`paths` at `mesh_pathadr`, `hfield_pathadr`, `skin_pathadr` and `tex_pathadr`) now store the resolved path or URI from which the compiler read the asset (combining the model file's directory and `meshdir` or `texturedir` with <span class="at">file</span>, unless <span class="at">file</span> is an absolute path or URI), so *mju_openResource* can open them directly even after [attaching](XMLreference.md) models with different asset directories. Code that prefixed these paths with its own directory should pass them to *mju_openResource* as is.
13. `9f035384d` Mesh polygon normals (`mjModel.mesh_polynormal`) are now computed from the whole polygon outline using Newell's method rather than the first three vertices (`3691`).

### Python bindings

14. `08330629b` Added a [mujoco.batch](python.md) module over the batch API: `Batch(model, nsim)` with live `(nsim, ...)` arrays from `bind()` and named views such as `joint(name)`, per-simulation model fields from `expand()`, `step`, `forward`, `reset`, `set_const` and `rollout` with the GIL released, and `jac` and `ray` queries.
15. `1313ef78e` Added support for building the Python bindings with [Bazel](https://bazel.build/) (initially covers the core bindings, without rendering or the viewer).
16. `39b7193e8` Fixed several bugs in [named access](python.md) (`data.actuator('a')`, `model.joint('j')`, `data.bind(...)`), and the corresponding generated accessors in the JavaScript bindings:
    - Multi-control or multi-output actuators (such as [orientation](XMLreference.md)) now follow `actuator_ctrladr` and `actuator_outadr` with leading dimension `ctrlnum` or `outnum`, instead of reading a single row at the actuator index.
    - `data.actuator('a').moment` is now a read-only dense copy of the actuator's moment arm of shape `(nv,)` or `(outnum, nv)`, instead of reading the sparse `actuator_moment` array as if it were dense.
    - Views of multi-column per-dof fields (`cdof`, `cdof_dot`, `dof_dampingpoly`) on joints after the first now index the right rows.
17. `7cdc8857e` Unallocated arena arrays of `MjData` (such as `efm_*` when the `discrete` integrator is not used, or island arrays when no islands are formed) are now filled with zeros, or -1 for index fields, instead of returning uninitialized memory.

### Bug fixes

18. Fixed several bugs in interpolated [flexcomp](XMLreference.md) elasticity:
    - `4bbc96957` Volume (solid) interpolated flexes whose first cell is empty (e.g. a trilinear [flexcomp](XMLreference.md) from a mesh that does not fill the corner of its bounding box) now retain their elasticity; previously elasticity was gated on the first cell's stiffness.
    - `b0b20166d` Editing a flex to remove a strain [equality](XMLreference.md) (e.g. from `body.make_flex`) and recompiling now recomputes stiffness instead of keeping the strain constraint eigenmodes.
    - `08bf94b18` Shell-mode interpolated flexes with [elastic2d](XMLreference.md) set to `"stretch"` or `"both"` now apply membrane stretch forces and implicit stiffness, and `"bend"` shells without strain constraints no longer allocate `flex_stiffness`.
19. Fixed several bugs in the Filament renderer:
    - `5c7c1e3ae` Textures now allocate mipmap levels (including sRGB textures), fixing minification aliasing.
    - `e81c8aed4` Skins that share vertices across faces no longer fail with an index count mismatch (`3719`).
    - `001aa3203` Material colors now apply only when an object has the default color, instead of overwriting custom object colors.
    - `6cfc76e32` Textures with an unsupported number of channels are now skipped with a warning, matching the classic renderer, instead of calling *mju_error*.
20. Fixed several bugs on error paths which called *mju_error* while C++ objects or locks were held (an error handler that does not return, as in the Python bindings and the model compiler, skips C++ destructors):
    - `4cc38db84`, `8c1e45559`, `526583e5b` Invalid configurations of the touch grid, cable and SDF plugins leaked more than 10 MB per failed compilation (they now fail plugin initialization with a warning); *mju_getXMLDependencies* and unknown material layer [roles](XMLreference.md) also leaked memory on invalid XML, and unsupported equality types in the XML writer are now reported as write errors instead of calling *mju_error*.
    - `4cc38db84` An error while compiling meshes or textures on the compiler's worker threads crashed the process, and a failed library load in *mj_loadAllPluginLibraries* left its mutex locked.
    - `ae15ab978` *mj_recompile* freed the given [mjData](APIreference/APItypes.md) and called *mju_error* if a plugin failed to initialize, and did not delete the model and data on some other failures, contrary to its documentation.

### Models

21. `94483e166` The [elastic mechanism](https://github.com/google-deepmind/mujoco/tree/main/model/flex/mechanisms/) example models now use 1D flex rods: the cantilever comparison of quadratic flexes adds a rod, and the elastic slider-crank and the tendon-loaded dipper arm are built from rods.

## Version 3.16.0 (October 14, 2026)

### Significant new features

1.  `cf89a6375`, `4316935b3`, `6d98d9fab`, `5f17e92eb`, `89d59b11f`, `147dc67d0` [Frames](XMLreference.md) can now scale their contents at compile time—without modifying the [mjSpec](APIreference/APItypes.md)—via the new [scale](XMLreference.md), [scaling](XMLreference.md), and [massscale](XMLreference.md) attributes. The default `similar` policy scales all physical quantities so that dynamics are preserved under proportionally scaled gravity, whereas `geometry` scales only spatial dimensions and inertias (and supports anisotropic scaling). Masses scale with volume unless overridden by `massscale`. External references to scaled elements—including actuators, tendons, constraints, sensors, keyframes, and deformable/mesh assets—are scaled consistently, and *mj_copyBack* maps values back into unscaled spec coordinates. See [frame/scale](XMLreference.md) for details.
2.  `592c54ad3`, `92b8f4b27`, `d4595d020` Added compiler attributes [savecompiled](XMLreference.md) and [savecanonical](XMLreference.md) (both defaulting to `"true"`) to preserve original authoring when saving models to XML. Setting `savecompiled="false"` saves the uncompiled [mjSpec](APIreference/APItypes.md) directly—retaining default classes, frames, and authored numeric values—so the saved XML reloads into an identical spec. Setting `savecanonical="false"` additionally preserves the original input conventions, such as orientation representations, degree/radian units, and actuator shortcuts; see [Model Encoding & Saving](programming/modeledit.md). *mj_copyBack* (`MjSpec.copy_back` in Python) now updates only the modified fields in the spec while leaving all other authored values untouched.
3.  `9d953b40c` Added support for building MuJoCo with [Bazel](https://bazel.build/) (initially covers core library, `simulate`, plugins, and samples).

### General


Breaking API changes

4.  `ea5e711c1` [mjfDecode](APIreference/APItypes.md), the `decode` callback of [mjpDecoder](APIreference/APItypes.md) plugins, and *mju_decodeResource* now take `char* error, int error_sz` arguments. A decoder which fails writes its reason into `error`, which is then reported by *mj_parse* and in mesh compilation errors, rather than only as a warning with a generic error.

    **Migration:** Add the two arguments to custom decoders and write failure messages into `error` (if not `NULL`) instead of calling *mju_warning*. Pass an error buffer, or `NULL, 0`, to *mju_decodeResource*.

5.  `2757493d9` Shortened the names of [mjpResourceProvider](APIreference/APItypes.md) functions. `mjp_getResourceProvider` is renamed to *mjp_findProvider*, consistent with other prefix and extension lookups.

    **Migration:** Rename as follows: <br/> `mjp_defaultResourceProvider` → *mjp_defaultProvider* <br/> `mjp_registerResourceProvider` → *mjp_registerProvider* <br/> `mjp_resourceProviderCount` → *mjp_providerCount* <br/> `mjp_getResourceProvider` → *mjp_findProvider* <br/> `mjp_getResourceProviderAtSlot` → *mjp_getProviderAtSlot* <br/> `mjp_registerArchiveResourceProvider` → *mjp_registerArchiveProvider* <br/> `mjp_findArchiveResourceProvider` → *mjp_findArchiveProvider* <br/> `mjp_archiveResourceProviderCount` → *mjp_archiveProviderCount*


### Engine

6.  `0998957cf` The [contact](XMLreference.md) sensor now supports `linvel` and `angvel` [data](XMLreference.md) fields for reporting relative contact velocities, and its computation stage ([mjtStage](APIreference/APItypes.md)) is now inferred from the requested [data](XMLreference.md) and [reduce](XMLreference.md) attributes.
7.  `d823f9212` *mj_setConst* now computes the bounding volumes of geoms and bodies, the collision masks and margins of bodies, and the added mass of geoms in the ellipsoid [fluid model](computation/fluid.md). Changes to the size, pose, margin and gap of geoms, to the inertial frames of bodies and to the size of height fields are then safe; previously contacts could be missed. *mj_setConst* also computes the constants of sleeping bodies, which it skipped, and resolves the automatic [sleep policy](XMLreference.md) of trees anew.
8.  `52824daf6` Corrected the shear contribution to solid and membrane stiffness for interpolated flexes, and the three-point Gauss quadrature used by quadratic flexes. Material parameters now produce the standard isotropic linear-elastic stiffness; existing models using these flexes can change behavior.
9.  `3bc4b769a` Improved numerical stability of sphere and cylinder [spatial tendon](XMLreference.md) [geom](XMLreference.md) wrapping near wrap onset and for inside wrapping. Thanks to `M-Colley` for reporting and analyzing the issues in [MJWarp](mjwarp/index.md) issues [1713](https://github.com/google-deepmind/mujoco_warp/issues/1713) and [1714](https://github.com/google-deepmind/mujoco_warp/issues/1714).
10. `871e3725b` Flex contacts are now reduced to `mjMAXCONPAIR` per geom only for rigid and interpolated flexes; other flexes keep all their contacts. Previously, cloth resting on a plane or on many static geoms could be held by at most 50 contacts and fall through.
11. `efffd3a5f` Fixed floating-point cancellation in capsule-capsule collision detection for parallel and near-parallel axes. Thanks to `ayonga` for reporting the issue in [MJWarp](mjwarp/index.md) issue [1758](https://github.com/google-deepmind/mujoco_warp/issues/1758).

### Compiler


Breaking API changes

12. `592c54ad3` *mj_copyBack* and *mj_saveLastXML* now fail, with an error which names the element, if a value was changed in the model which the spec cannot express, for example the mass of a body when [inertiafromgeom](XMLreference.md) is "true". Nothing is copied or saved then; previously such a change was left out of the saved file without notice. *mj_saveLastXML* also fails if it is given a model which was not compiled from the XML that was loaded last, and a save which fails no longer empties the file.

    **Migration:** Undo the change in the model, or change what makes it inexpressible, as listed for *mj_copyBack*.

13. `2267bf299` An asset added to an [mjSpec](APIreference/APItypes.md) through the API is no longer named after its `file` when the spec is compiled. A mesh, height field or texture which is left without a name is now a compilation error, as it already was for one without a file. MJCF is unaffected: the XML parser still names assets after their files.

    **Migration:** Name the asset when adding it, e.g. `spec.add_mesh(name='link', file='link.stl')` in Python or *mjs_setName* in C.

14. `1961e8a2d` [Keyframes](XMLreference.md) in MJCF are no longer copied by [replicate](XMLreference.md): a keyframe describes the model with all replicas in place, as in a model without replicates. Previously each replica received a copy of every keyframe, setting only the joints of that replica, and a keyframe written for the complete model failed to load (`3071`, reported by `eholum-nasa`).

    **Migration:** Write the vectors of a keyframe for the complete model. A keyframe which was written for a single replica still loads, as one keyframe whose vectors are completed with the default configuration.

15. `1db889162` With [inertiafromgeom](XMLreference.md) "true", [discardvisual](XMLreference.md) is now a compilation error if a geom which it discards has mass. Previously the first compilation kept the inertia of the discarded geoms, while compiling the same spec again, or saving it and loading the file, dropped it.

    **Migration:** Use `inertiafromgeom="auto"`, the default, under which the inertia is kept as an explicit [inertial](XMLreference.md), or give the visual geoms zero mass.


16. `0696cdc85` [flexcomp](XMLreference.md) can now reference a [mesh asset](XMLreference.md) directly using the [mesh](XMLreference.md) attribute, in place of <span class="at">file</span>. Volumetric meshes (e.g. from GMSH) supply nodes and tetrahedra directly; surface meshes can create 1D or 2D flexes or extrude to volumetric tetrahedra using <span class="at">origin</span>. Added the `mesh` parameter to Python `body.make_flex`; in *mjs_makeFlex*, the `file` parameter can also be the name of a mesh asset.

17. `ea019c212`, `0696cdc85` Added procedural mesh types `grid`, `box`, `cylinder`, `ellipsoid`, `square` and `disc` to [mesh/builtin](XMLreference.md) and *mjs_makeMesh*, generating the same shapes as the corresponding [flexcomp](XMLreference.md) types, which flexcomp and geoms can use directly. Types without volume change a `legacy` mesh inertia to `shell`. Added Python convenience methods `mjsMesh.make_*`.

18. `dc8210572`, `08490e897`, `831994e2a` Added *mjs_fuseStatic*, which fuses the static bodies of an [mjSpec](APIreference/APItypes.md) with their parents as an operation on the spec: each fused body becomes a frame in its parent. The [fusestatic](XMLreference.md) compiler option now applies it and then compiles; previously it fused inside compilation and left the spec inconsistent with the model. Static bodies whose fusing would change the forces on the model (a plugin, a sleep policy, another gravcomp, a fluid), or which a flex or skin refers to, are now kept, and cameras and lights are no longer misplaced. Elements which refer by name to a geom, site, camera or light are no longer bound to a different one, and referencing a body by name no longer leaves other static bodies unfused. The new [fuse](XMLreference.md) body attribute keeps a static body when set to "false".

19. `1db889162` Added *mjs_discardVisual*, which discards the visual elements of an [mjSpec](APIreference/APItypes.md) as an operation on the spec. The [discardvisual](XMLreference.md) compiler option now applies it and then compiles; previously it discarded inside compilation and left references to what it discarded in the spec, so that some models failed to compile. Visual meshes are no longer loaded unless body inertia is inferred from them, and geoms which use the ellipsoid [fluid model](XMLreference.md) are kept.

20. `d48b586ae` Added *mjs_adoptInertial*, which makes the inertial that compilation infers from the geoms of a body part of the [mjSpec](APIreference/APItypes.md), so that it no longer follows later changes to the geoms.

21. `5558bd783` The [settotalmass](XMLreference.md) compiler attribute is deprecated and will be removed in a future release. It still scales the masses, and compiling a model which sets it now gives a warning.

    **Migration:** Scale the masses and densities in the model, or call *mj_setTotalmass* on the compiled model, followed by *mj_setConst*.

### Compiler bug fixes

22. `9fd6ee025` The `quat` of a geom, site or camera is no longer ignored when its [default class](XMLreference.md) gives an orientation as `euler`, `axisangle`, `xyaxes` or `zaxis`.
23. `9fd6ee025`, `92b8f4b27`, `239647a1d` Saving MJCF no longer changes or loses the following: the order of the elements of a body which has [frames](XMLreference.md), which gave the saved model other ids; `class="main"` inside another `childclass`; the [nchannel](XMLreference.md) of a texture; the names of energy sensors, which could not be loaded; `inertiafromgeom="false"`, and the inertia of the bodies of an attached model which has another `inertiafromgeom`; the frame of the [surfacevel](XMLreference.md) of mesh geoms; the precision of mesh, flex, skin and height field data; and the empty cells of a [flexcomp](XMLreference.md) with trilinear or quadratic dofs.
24. `592c54ad3` *mj_saveXML* and *mj_saveXMLString* now save the compiled values of an [mjSpec](APIreference/APItypes.md) as *mj_saveLastXML* does, including those which are computed at the end of compilation, such as the damping which [dampratio](XMLreference.md) gives, and no longer lose the scaling of [settotalmass](XMLreference.md).
25. `1961e8a2d` [Keyframes](XMLreference.md) of an [mjSpec](APIreference/APItypes.md) now keep their place and their values when its kinematic tree changes (*mjs_delete*, *mjs_attach*) and when the spec is copied; previously the next compilation created them again, and values were lost or misplaced in several cases. A vector which is shorter than the model is completed with the default configuration of the compiled model.
26. `3a35e7712` *mjs_attach* and the [attach](XMLreference.md) element now apply the prefix and suffix to the name and material of skins and to the material of tendons and meshes. Attaching a model in which one of these has a material used to fail to compile.
27. `cbd16feac` Fixed attaching by reference, the default of *mjs_attach*: *mj_recompile* gave the attached elements the state of other elements of the parent, and attaching another body or frame of the same model failed or left out the elements which refer to it. Attaching what the parent already has is now an error.
28. Fixed several bugs when editing or copying an [mjSpec](APIreference/APItypes.md):
    - `239647a1d` Saving the compiled values of a spec which was structurally edited since it was compiled (elements added, deleted or attached) is now an error until it is compiled again; it used to crash or save wrong values.
    - `2267bf299`, `dc8210572` Compiling no longer reorders contact [pairs](XMLreference.md) and [excludes](XMLreference.md), writes into authored fields such as the data of a texture, or keeps references removed since the last compilation.
    - `2267bf299`, `dc8210572` *mjs_findElement* now finds elements added or renamed after compilation, and returns the named element for contact pairs, excludes and after [discardvisual](XMLreference.md).
    - `3a9b10a3c`, `3a35e7712` *mjs_delete* now deletes a [plugin instance](XMLreference.md) together with the last element referencing it, and deleting a body removes the elements referencing it after [discardvisual](XMLreference.md) or later edits. Both cases used to make the next compilation fail or crash.
    - `592c54ad3` *mj_copyBack* and *mj_saveLastXML* no longer lose a change to the reference pose of a free joint, or write out of bounds for a [numeric](XMLreference.md) which has less data than its `size`.

### Actuation

29. `ab7f005c9` Actuator [shortcuts](modeling.md) now inherit their parameters (`kp`, `kv`, `area`, ...) only from a [default](XMLreference.md) written with the same shortcut or with [general](XMLreference.md), looking up the class hierarchy for one, and otherwise use their documented defaults; mechanical attributes like `ctrlrange` and `gear` are inherited from any default, as before. A [motor](XMLreference.md) in a class with a [position](XMLreference.md) default used to be a position servo (`3561`). Every shortcut now sets its full documented table, including its dynamics and activation layout, and a [pid](XMLreference.md) without `kp` has the documented gain of 1, not 0. Added `mjsActuator.type` ([mjtActuator](APIreference/APItypes.md)), the element an actuator is written with.

    **Migration:** Write the gains on the actuator itself, or in a default of the same shortcut or of [general](XMLreference.md).

30. `fcb83a173` Actuators with "fixed" or "affine" [gaintype](XMLreference.md) can declare what their control is with [input](XMLreference.md): a position setpoint ("pos"), a velocity setpoint ("vel") or a pressure ("pressure"); without a declaration it is a command. The declaration does not affect the simulation. The [position](XMLreference.md), [velocity](XMLreference.md), [intvelocity](XMLreference.md) and [cylinder](XMLreference.md) shortcuts declare their inputs, which are recorded in `mjModel.actuator_ctrlspec` and kept when a model is saved; *mj_actuatorInputName* returns the declaration. An input signature inherited from a default class is now discarded when the gaintype changes.

31. `92b8f4b27` Added the [inheritrange](XMLreference.md) attribute to the [general](XMLreference.md) actuator, which so far only the [position](XMLreference.md), [intvelocity](XMLreference.md) and [pid](XMLreference.md) shortcuts had.

### Filament Rendering


Breaking API changes

32. `4419c1be6`, `6678efd66`, `39b17ef2f`, `6c2137fe0` Renamed `mjrf` functions and types so that the owning object appears first (`mjrf_<verb><Owner><Thing>`) and names match MJCF attributes and existing MuJoCo vocabulary (cf. *mjr_uploadMesh*, `mjModel.light_active`).

    **Migration:** Rename as follows: <br/> `mjrf_addRenderableToScene` → *mjrf_addSceneRenderable* <br/> `mjrf_removeRenderableFromScene` → *mjrf_removeSceneRenderable* <br/> `mjrf_addLightToScene` → *mjrf_addSceneLight* <br/> `mjrf_removeLightFromScene` → *mjrf_removeSceneLight* <br/> `mjrf_setMeshData` → *mjrf_uploadMesh* <br/> `mjrf_setTextureData` → *mjrf_uploadTexture* <br/> `mjrf_setRenderableTransform` → *mjrf_setRenderablePose* <br/> `mjrf_setLightTransform` → *mjrf_setLightPose* <br/> `mjrf_setLightEnabled` → *mjrf_setLightActive* <br/> `mjrf_setLightCutoffAngle` → *mjrf_setLightCutoff* <br/> `mjrf_setLightShadowsEnabled` → *mjrf_setLightCastShadow* <br/> `mjrfReadPixelsRequest` → [mjrfReadRequest](APIreference/APItypes.md) <br/> [mjrfLightParams](APIreference/APItypes.md): `spot_cone_angle` → `cutoff`, `spot_softness` → `softness`, `cast_shadows` → <br/> `cast_shadow` <br/> [mjrfRenderableParams](APIreference/APItypes.md): `cast_shadows` → `cast_shadow`, `receive_shadows` → `receive_shadow` <br/> [mjrfRenderRequest](APIreference/APItypes.md): `enable_post_processing`, `enable_reflections`, `enable_shadows` and <br/> `enable_headlight` drop the `enable_` prefix <br/> [mjrfContextConfig](APIreference/APItypes.md): `force_software_rendering` → `software_rendering` <br/> [mjrfMaterial](APIreference/APItypes.md): `decor_ux` → `decor` <br/> Support class `ModelObjects` → `ModelResources`

    Python names changed accordingly, e.g. `mjrf.ReadPixelsRequest` → `mjrf.ReadRequest`, `Light.set_cutoff_angle` → `Light.set_cutoff`, `Light.set_shadows_enabled` → `Light.set_cast_shadow`, `Mesh.set_data`/`Texture.set_data` → `upload`, `set_transform` → `set_pose`, `Light.set_enabled` → `set_active`, `Material.decor_ux` → `decor`, `mjrf.ModelObjects` → `mjrf.ModelResources`.

33. `e87cafb26` Renamed [custom flags](programming/rendering.md) for consistency, and changed enum flags to take strings instead of integers.

    **Migration:** Rename as follows: <br/> `filament.clearColor` → `filament.clear_color` <br/> `filament.fog.cutOffDistance` → `filament.fog.cut_off_distance` <br/> `filament.fog.maximumOpacity` → `filament.fog.maximum_opacity` <br/> `filament.fog.heightFalloff` → `filament.fog.height_falloff` <br/> `filament.fog.inScatteringStart` → `filament.fog.in_scattering_start` <br/> `filament.fog.inScatteringSize` → `filament.fog.in_scattering_size`

    `filament.ao.quality`, `filament.ao.low_pass_filter`, `filament.ao.upsampling` and `filament.bloom.quality` take "low", "medium", "high" or "ultra" instead of 0-3; `filament.shadows.type` takes "pcf", "vsm" or "pcss" instead of 0-2.

34. `e7b0bc104` Removed `mjrf_setLightBlurWidth` and `mjrfLightParams::vsm_blur_width`, and their Python counterparts `mjrf.Light.setBlurWidth` and `mjrf.LightParams.vsm_blur_width`. This removes soft shadows with VSM.

    **Migration:** Use PCSS shadows instead by setting the custom flag `filament.shadows.type` to `pcss`. PCSS shadows provide similar quality and are more performant.

35. `e71e9f6db` Removed the `filament.msaa.enabled` custom flag; multi-sample anti-aliasing is now controlled by [visual/quality/offsamples](XMLreference.md) (`<= 1` disables MSAA) and can be changed at runtime with *mjrf_setSceneMsaa*.

36. `6c2137fe0` Removed `mjrf_DEBUG_drawImguiEditor` from the public API; the ImGui scene editor is an internal debugging aid for MuJoCo Studio.


### Python bindings

37. `43eff4c76` The `opt`, `vis` and `stat` attributes of `MjModel`, and the sub-struct attributes of `MjVisual`, can now be assigned to (e.g. `model.opt = new_opt`); previously this raised `AttributeError`. Assignment copies the fields into the underlying C struct in place, so existing references and NumPy array views into the destination remain valid.

### Models

38. `dc0c237df` Added three [elastic mechanism](https://github.com/google-deepmind/mujoco/tree/main/model/flex/mechanisms/) example models using multicell trilinear flexes: a cantilever material comparison, an elastic slider-crank, and a tendon-loaded dipper arm. Inspired by [Miles Macklin's Reduced Elastic Links experiments](https://reports.mmacklin.com/newton-reduced/reduced_elastic_links_implementation.html).

### Documentation

39. `641652525` Added documentation for [Filament rendering](programming/rendering.md).
40. `1b7d9e83b` The [XML reference](XMLreference.md) now gives the physical dimension of every real-valued attribute, declared in the MJCF schema.

## Version 3.15.0 (October 5, 2026)

### General

1.  `1aa68e1ca` [.mjz](programming/modeledit.md) archives written on Windows now always use `/` separators.
2.  `1aa68e1ca` Assets in a [meshdir](XMLreference.md) or [texturedir](XMLreference.md) now resolve correctly in [.mjz](programming/modeledit.md) archives when rewritten or when the directory path is absolute, uses `..`, or uses a URI scheme.

### Engine


Breaking API changes

3.  `b3dd9e617` Actuator [dampratio](XMLreference.md) now computes the reflected inertia $`m`$ at `mjModel.qpos0` as the operational-space inertia $`(J M^{-1} J^T)^{-1}`$ (averaged across force outputs for multi-output actuators such as [orientation](XMLreference.md)), rather than summing $`\text{dof\_M0}_j / J_j^2`$ across degrees of freedom. This accounts for tendon and actuator armature as well as off-diagonal inertial coupling, and avoids extreme damping values when a multi-DOF transmission has small Jacobian entries. In practice, actuators using `dampratio` on multi-link kinematic chains may exhibit lower damping than before, while actuators driving tendons or sites that span multiple joints will be damped much more accurately instead of being overdamped.
4.  `5023a4a50` Removed the deprecated `internal` flex collision option and associated `evpair` structures.


5.  `1b973add4` Added experimental simplified Stable Neo-Hookean elasticity for non-interpolated 3D flexes, enabled only through `mjsFlex.elastic3d = 1`. It projects the material Hessian to positive semidefiniteness for the solver and Rayleigh damping, and preserves the Saint Venant-Kirchhoff (StVK) default (`0`). SNH requires the discrete integrator. The setting is not available in MJCF.
6.  `2742de438` The cached flex bending factor now retains cross-coordinate couplings between differently oriented vertex bodies.
7.  `eed008905` Flex bending and stretching now include the motion and reaction forces of articulated vertex attachments. The discrete integrator supports these attachments with the CG solver; fixed and independent XYZ-slide attachments retain their optimized assembly. Elastic flexes attached to mocap bodies produce a compiler error.
8.  `6224e95f6` Added single-shot [multicontact](computation/index.md) for collisions with capsule geoms.
9.  `ebfb4662d` Added the [enclosed](XMLreference.md) attribute to [insidesite](XMLreference.md) sensors, measuring how much an object juts out of a site (using directed Hausdorff distance) and reporting signed clearance/protrusion.
10. `f80ef4244` Fixed 64-bit model size narrowing in binary MJB serialization: *mj_saveModel* and *mj_loadModelBuffer* now accept [mjtSize](APIreference/APItypes.md) for `buffer_sz`, supporting models larger than 2 GiB.

## Version 3.14.0 (September 22, 2026)

### General

1.  `458189298` Added the `ipc` [flag](XMLreference.md), an experimental contact mode of the `discrete` integrator for penetration-free flex contact. Each step minimizes an incremental potential subject to linearized contact constraints, using a barrier-free augmented Lagrangian whose subproblems are the discrete solve. Every committed position update is verified intersection-free by continuous collision detection, so flex contact cannot tunnel. Supported for dim-2 flexes: a flex with edge equality constraints keeps its elasticity in the constraint solver, while `elastic2d` elasticity is integrated implicitly through the effective metric. The contacts the mode resolves are frictionless. The mode keeps contact multipliers across steps that no state specification covers, so `mj_getState`/`mj_setState` do not capture its full state and exact replay is not supported.
2.  `2fec92237` Introduced *archive resource providers* (`mjp_registerArchiveResourceProvider`). Archive providers use the [mjpResourceProvider](APIreference/APItypes.md) interface to mount and read archive containers (such as `.mjz`/`.zip`), decoupling container handling from format decoders and enabling on-demand asset extraction without requiring a pre-allocated *VFS*.
3.  `e312ce82d` [Frames](XMLreference.md) are now preserved when saving MJCF: `<frame>` elements are written with their `pos` and `quat` and their contents in frame-relative coordinates, so a saved model reloads with the same frames. Previously the frame transformation was accumulated into the children on save and only the frame's name was kept. Changes to the `pos` or `quat` of a frame in an [mjSpec](APIreference/APItypes.md) now also take effect when the spec is recompiled.

### Engine


Breaking API changes

4.  `dc8bb1364` *mj_readCtrl* now matches the signature and semantics of *mj_readSensor* to support multi-input actuators (e.g., [pid](XMLreference.md), [dcmotor](XMLreference.md), [orientation](XMLreference.md)): it takes an output buffer `result` of size `actuator_ctrlnum[id]` and returns `const mjtNum*` (a pointer into `mjData.ctrl` or `mjData.history` on zero-order-hold or exact timestamp matches, or `NULL` when interpolated values are written to `result`). Actuator history buffers now store `actuator_ctrlnum[id]` values per sample, and *mj_initCtrlHistory* expects `nsample * actuator_ctrlnum[id]` values (`3597`).


5.  `9e0c6b577` The [mjWARN_INERTIA](APIreference/APItypes.md) warning is now also raised by the modified-inertia factorizations of the <span class="at">implicitfast</span> and damped-<span class="at">Euler</span> integrators (previously silent) and of the <span class="at">implicit</span> integrator (previously a fatal error).
6.  `35c0631de` The sparse Newton solver no longer aborts with a "rank-deficient sparse Hessian" error when rounding loses a pivot of its Hessian, as can happen in single precision with ill-conditioned inertia. The pivot is now clamped and its row decoupled, as in the dense factorization.

### Bug fixes

7.  `2a3f1f5a4` Procedural model editing is no longer quadratic in the number of elements. `mjSpec` previously recomputed the compilation signature on every *mjs_addGeom*-like call, and *mjs_setName* rescanned every name of the element's type. Both are now incremental. Building a spec with 8000 geoms is roughly 10x faster.


    Breaking API changes

    `mjsElement.signature` is now `0` whenever the spec has been structurally edited since it was last compiled, rather than being eagerly recomputed on each edit. It is still equal to `mjModel.signature` after a successful *mj_compile*, which is what *mj_copyBack* and the Python `bind` methods rely on. Code that compared the signature of an uncompiled spec against anything other than `0` must compile first. Additionally, when *mjs_setName* fails on a duplicate name, the element's previous name is now preserved rather than being overwritten with the duplicate name.


8.  `ac329bd17` Fixed the torque applied by [weld](XMLreference.md) constraints in *mj_rnePostConstraint*. The rotational constraint force was used directly as a world-frame torque, missing the scaling by `0.5 * torquescale` and the rotation into the world frame. [Force](XMLreference.md) and [torque](XMLreference.md) sensors on bodies held by a weld that carries torque were wrong (`2533`).

9.  `263c638c0` *mj_rnePostConstraint* now accounts for the forces of spatial tendons (spring, damper, actuator, limit, friction loss, equality and armature), so [force](XMLreference.md) and [torque](XMLreference.md) sensors register the forces that tendons apply to bodies (`832`).

10. `eb662fcaf` Tendon [actuatorfrclimited](XMLreference.md) now defaults to "auto" as documented. Previously the default was "false" and <span class="at">actuatorfrcrange</span> was silently ignored unless <span class="at">actuatorfrclimited</span> was set explicitly.

11. `54be9cce6` *mjd_transitionFD* and *mjd_inverseFD* now raise an error when [sleeping](computation/index.md) is enabled. Previously, their repeated evaluations changed the sleep state, leading to internal errors or wrong derivatives.

12. `e38573c64` Fixed a memory leak in *mjs_delete* where deleted elements and subtrees were retained in `mjSpec` until *mj_deleteSpec* (`2882`).

13. `65ea54c3c` Fixed an out-of-bounds read when parsing the header of a *GMSH file* loaded by [flexcomp](XMLreference.md). Truncated headers are now reported as an error.

## Version 3.13.0 (September 8, 2026)

### General

1.  `eb18d77ca` The [.mjz](programming/modeledit.md) encoder now writes the root file as `model.xml` in the archive as this is less susceptible to breakage due to file renaming.
2.  `4affbb64a` Site geometries can now also be associated with meshes ([type="mesh"](XMLreference.md) with [mesh="name"](XMLreference.md)), supporting visualization, the [insidesite](XMLreference.md) sensor, and the new *mj_insideSite* function.
3.  `b59b07fae` Added support for Python 3.15 (GIL and Free-Threading).

### Engine

4.  `5660353ec` Added a new integrator `discrete`: the constraint solve and the implicit velocity update merge into one operation, performed in the effective metric $`\widehat{M} = M + hD + h^2K`$, which incorporates both implicit damping $`hD`$ and implicit position stiffness $`h^2 K`$. Under this integrator `mjData.qacc` is the discrete step map $`(v^+ - v)/h`$, and joint, tendon and actuator stiffness and damping join the solver's metric, making passive springs and actuator position gains stable at timesteps far beyond the explicit stability limit. Constraint rows are treated implicitly as well: <span class="at">solref</span> spring--dampers are evaluated at the end of the step, so constraints are stable at any `timeconst`; under this integrator the [refsafe](XMLreference.md) flag replaces contact and limit rows stiffer than the timestep can resolve by the stiffest zero-restitution row instead of clamping `timeconst`. The actuator-gain treatment resolves the stiff-servo timestep limitation of `3443` (analysis contributed by `qiayuanl`). See the [integrator documentation](computation/index.md) for semantics and current limitations.


    Breaking API changes

    Removed the implicit flex effective-metric special case under `implicit`/`implicitfast` with the `CG` solver, introduced in 3.11.0. This behavior now requires `integrator="discrete"` (with a primal solver: `CG` or `Newton`), which additionally treats joint damping and stiffness implicitly inside the solve. Models relying on the old behavior should set [integrator](XMLreference.md) to `discrete`; models with flex elasticity or passive flex contact under `implicit`/`implicitfast` now raise a runtime error carrying this migration note.


5.  `0b4e17747` Restored clamping of non-positive pivots in the sparse inertia factorization, along with the associated `mjWARN_INERTIA` warning. The guard was inadvertently dropped in the 3.3.0 conversion of `qLD` to CSR format; since then, models with singular mass matrices silently produced non-finite accelerations, typically surfacing as divergence warnings and automatic resets.

6.  `c9d997610` Added single-shot [multicontact](computation/index.md) for collisions with cylinder geoms.

7.  `10eeb8289` The Newton solver with [elliptic cones](XMLreference.md) now rebuilds the cone-augmented Hessian factor with a single refactorization instead of per-contact rank-1 updates when a flop-count model predicts this is faster. Scenes with many simultaneously sliding contacts speed up by 1.4-2x on average and 3-4x on the slowest steps. Contribution by `kevinzakka`.

### Compiler

8.  `2a3957558` Custom text fields ([custom/text](XMLreference.md)) in MJCF now accept their values inside a `<![CDATA[ ... ]]>` block in addition to the `data` attribute. When saving a model via *mj_saveXML*, custom text containing newlines or XML characters is exported as CDATA.
9.  `47ebfe48a` Added [cutoff](XMLreference.md) attribute to [sensor/tactile](XMLreference.md).

### Samples

10. `834983fbb` Added [render.cc](programming/samples.md): a headless offscreen rendering sample that saves an image to a PNG image. Supports both the Filament and classic OpenGL backends, with command-line options for camera, resolution, keyframe, simulation steps, geom/site groups, visualization and rendering flags, labels, and frames.

### Bug fixes

11. `67562d95f` Rewrote the Plane-Mesh collider to fix bugs and improve performance. Fixes `3524`.


MNQsV_etq24


### Models

12. `f6c1004b7` Added [house of cards](https://github.com/google-deepmind/mujoco/tree/main/model/cards/) example model and three [free-standing arch](https://github.com/google-deepmind/mujoco/tree/main/model/arch/) models: roman, gothic, and hyperbolic. Inspired by [Song et al](https://www.cs.ubc.ca/research/fbf-friction/).

### Rendering


Breaking API changes

13. `cb57b526f` For materials with physically-based rendering parameters that do *not* provide a metallic texture the fallback is now white. Previously the fallback was black, which caused scalar metallic values to be discarded when multiplied in the PBR shader.


## Version 3.12.0 (August 20, 2026)

### General

1.  `3f8db4c1` The MJCF grammar is now defined in a single source of truth schema file, [src/xml/mjcf.schema](https://github.com/google-deepmind/mujoco/tree/main/src/xml/mjcf.schema). The parser's grammar table, presence constraints, keyword maps, typed attribute bindings and save policies are generated from it and gated by tests, as are the schema's enum keywords and declared defaults against the C headers and default-constructors.


Breaking API changes

2.  `6fe04aa8` Removed the custom binary texture format (`image/vnd.mujoco.texture`) and the automatic fallback to custom textures when loading files with unrecognized extensions. Textures can now only be loaded from PNG (`image/png`) and KTX (`image/ktx`) files.


### Actuation

3.  `279df98c` Added the [pid](XMLreference.md) actuator: a PID controller with real position and velocity setpoint inputs, optional integral action ([ki](XMLreference.md), integrating the position error with [imax](XMLreference.md) anti-windup), setpoint rate limiting ([slewmax](XMLreference.md)), and an optional feedforward input. This subsumes the functionality of the `mujoco.pid` plugin with proper activation state: correct under all integrators and visible to keyframes and sensors. With a zero velocity setpoint it is identical to [position](XMLreference.md). The input signature is any subset of `[pos, vel, ff]`, selected by [input](XMLreference.md); absent setpoint inputs are fixed at zero, so the control vector contains no inert entries.
4.  `2f1843f4` The [dcmotor](XMLreference.md) on-board controller is redesigned: the [input](XMLreference.md) attribute selects any subset of `[pos, vel, ff, voltage]`, where `pos` and `vel` are setpoints for the controller, `ff` is a torque feedforward, and `voltage` is the raw terminal voltage (the default, a plain voltage-commanded motor). Controller gains are in torque space, as for [pid](XMLreference.md), and the drive voltage compensates back-EMF as in a current-controlled driver: commanded torque is delivered exactly until a limit is reached. The keyword `input="none"` selects the empty signature: the actuator has no control inputs and is purely passive, so friction, cogging and back-EMF braking can be used as passive joint forces.


Breaking API changes

5.  `2f1843f4` The mode-flag semantics of [dcmotor/input](XMLreference.md) ("voltage", "position", "velocity", selecting the interpretation of a single control) are replaced by input signatures, and the controller gains changed from voltage space to torque space. The old velocity mode's integral term (integrated-velocity tracking) is retired without replacement; the integrator always accumulates position error.

    **Migration:** Voltage-commanded motors (the default) are unchanged. Replace `input="position"` with `input="pos"` and `input="velocity"` with `input="vel"`, and multiply the controller gains by $`K/R`$ (torque per volt). The motor's back-EMF damping, previously felt in addition to the controller's damping, is now compensated: to preserve behavior when the velocity setpoint is zero, add $`K^2/R`$ to the converted <span class="at-val">kd</span>.


### Engine

6.  `83e621d7` Optimized large-mesh convex collision detection with up to 2x speedup in certain cases.
7.  `55d13aec` Replaced the per-step sparse Cholesky factorization of the flex block of the implicit effective metric M + K with its prefactored per-vertex 3x3 diagonal blocks. The blocks precondition the CG constraint solver and drive an iterative solve for `qacc_smooth`, which now converges on [tolerance](XMLreference.md) rather than a fixed threshold. Flexes with [elastic2d](XMLreference.md) stretch stiffness step roughly twice as fast; bending-only flexes keep the exact constant factor and are unchanged.
8.  `86e98601` Rewrote cleaner box-box SAT collider.


Breaking API changes

9.  `2a3554c8` Contacts of a flex with [passive](XMLreference.md) collisions are now integrated implicitly: their stiffness is carried by the effective metric rather than applied as an explicit spring, and can be far stiffer than the timestep would otherwise permit. Models using passive collisions should be re-checked: the feature now requires <span class="at">implicit</span> or <span class="at">implicitfast</span> with the CG solver, pyramidal cones and sleep disabled; passive handling covers flex-flex, self-, and static-geometry contact, while contact with a moving body stays on the constraint solver; and the stiffness is now a mass-scaled natural frequency rather than a fixed 1e4.
10. `55d13aec` Removed `mjData.efm_L_rownnz`, `mjData.efm_L_rowadr` and `mjData.efm_L_colind`. They described the sparsity of the effective-metric Cholesky factor, which no longer exists; `mjData.efm_L` now holds dense 3x3 blocks, 9 numbers per covered vertex. `mjData.efm_active` no longer takes the value 2: nothing selects a solve path on preconditioner exactness, so it is now a plain 0/1 flag.
11. `1362a8bd` Changed the default value of [bvactive](XMLreference.md) from "true" to "false". This avoids unnecessarily clearing bounding volume hierarchy visualization flags at every simulation step, which can be a bottleneck for models with large meshes.
12. `ed13bf56` Mocap bodies and their dof-less descendants are now the root of their own weld group: `mjModel.body_weldid` of a mocap body equals its own id rather than 0. Consequences: dragging a mocap body into sleeping objects now wakes them; children of mocap bodies receive standard [parent-child collision filtering](overview.md); mocap bodies no longer count as static geometry for ray casting, and contact-matching sensors aggregate their contacts under the mocap body rather than the world; and geom pairs where neither body can move no longer generate contacts.


### Models

13. `2a3554c8` Added [drape](https://github.com/google-deepmind/mujoco/blob/main/model/flex/drape.xml) example model: three cloths draped over a sphere, demonstrating [passive](XMLreference.md) collisions. It replaces the `sphere_passive` model, which has been removed.
14. `55d13aec` Added [bag](https://github.com/google-deepmind/mujoco/blob/main/model/flex/bag.xml) example model: a cloth bag, held open by pinning the ring of vertices around its mouth, catching the standard humanoid dropped in from above. Unlike the poncho models, which are bending-only, this model exercises the 2D [stretch](XMLreference.md) elasticity of a flex.

### Rendering


Breaking API changes

<img src="https://www.gstatic.com/mujoco/doc/images/changelog/primitives_textured.gif" class="align-right" style="width:40.0%" alt="image" />

15. `cc7fb98c` Added explicit texture coordinates to built-in geometries (Plane, Box, Sphere, Ellipsoid, Capsule, Cylinder) in both the Classic renderer and Filament. 2D textures applied to primitive shapes will look different as textures are mapped using canonical UV parameterizations rather than projecting onto the $`x,y`$ plane.

    For finite planes, textures are now anchored to the bottom-left corner instead of the center. This will cause the most common visual breakage, as common procedural checker textures will be phase shifted. Infinite planes continue to be anchored at the origin with no visual changes.

    <img src="images/changelog/plane_uv_tiling.png" class="align-center" style="width:70.0%" alt="image" />

16. `f9a00bd5` Added [light/softness](XMLreference.md): edge softness for spotlights under physically-based lighting models, given as the fraction of the cone over which intensity falls to zero. The default of 0.2 is a semi-soft cone which delivers the full [intensity](XMLreference.md) everywhere inside it, so that illuminance follows $`E = I/d^2`$ independent of the [cutoff](XMLreference.md) angle. Previously the filament renderer treated the entire cone as penumbra, dimming spotlights well below their rated intensity, increasingly so for narrow cutoffs.

    **Migration:** Set <span class="at">softness</span> to 1 to reproduce the previous appearance of existing models.


### MJX


Breaking API changes

17. `5e3464f4` `mjx.render` and `mjx.render_with_segmentation` now return the updated `mjx.Data` as the last element in their return tuple (i.e. `(rgb, depth, d)` and `(rgb, depth, seg, d)`). This ensures JAX/XLA strictly enforces causal scheduling between sequential `refit_bvh` and `render` calls.

    **Migration:** Update unpacking calls from `pixels, depth = mjx.render(mx, d, rc)` to `pixels, depth, d = mjx.render(mx, d, rc)`.


### Bug fixes

18. `95539261` Fixed a bug where models with pinned interpolated flex nodes (e.g. a [flexcomp](XMLreference.md) with <span class="at">dof</span> "trilinear" and pinned vertices) could not be reloaded after saving: node coordinates within their body frames were not saved, degenerating the interpolation grid. They are now saved in the new flex [nodecoord](XMLreference.md) attribute.
19. `8655446f` Fixed a bug in the box-box collider where near-degenerate face clipping could generate contacts with spuriously large penetration depth between nearly touching thin boxes with positive margin, causing resting stacks to explode.
20. `fb07a9ca` Fixed a bug in the box-box collider where penetrations deeper than a box's smallest half-size could produce no contacts, letting boxes tunnel through thin boxes. Fixes `1800`.
21. `54979947` Fixed the flex stretch stiffness operator, which was the Gauss-Newton Hessian of the stretch force rather than its Jacobian: the geometric (stress-proportional) term was missing. Only the tensile part of that term is added, since it is positive semi-definite exactly when the edge is in tension, and its consumers require an SPD operator; the stretch force itself is unchanged. This affects the implicit integrators and the implicit effective metric, so flexes using `elastic2d="stretch"` integrate slightly differently. Bending-only flexes are unaffected.

### OpenUSD

22. `39e44588` Upgraded Newton USD schemas support to version 0.4.0:
    - `NewtonJointAPI` (`newton:armature`, `newton:damping`, `newton:friction`) deprecates the `MjcJointAPI` equivalent `mjc:armature`, `mjc:damping`, and `mjc:frictionloss` attributes.
    - `NewtonMassAPI` (`newton:massModel`, `newton:inertia`) deprecates the `MjcCollisionAPI` equivalent `mjc:shellinertia` and `MjcMeshCollisionAPI` `mjc:inertia` attributes. This completes the deprecation of all `MjcMeshCollisionAPI` attributes, slating it for removal in a future release.
    - Added support for `NewtonSiteAPI` to declare sites, `MjcSiteAPI` auto applies this schema, but remains as an extension for the `mjc:group` attribute.
    - Added support for `NewtonMaterialAPI` (`newton:contactAdhesion`, `newton:torsionalFriction`, `newton:rollingFriction`). This deprecates `MjcMaterialAPI` which will be removed in a future release.
    - Added support for `NewtonMimicAPI` (`newton:mimicJoint`, `newton:mimicCoef0`, `newton:mimicCoef1`) as a base for `MjcEqualityJointAPI`, this deprecates the `mjc:coef0` and `mjc:coef1` attributes and the `mjc:target` relationship.
    - Added support for `NewtonArticulationRootAPI` (`newton:jointsAddMobility`).


Breaking ABI changes

23. `279df98c` [mjsActuator](APIreference/APItypes.md) gained `velrange` and `ffrange` fields, changing its size and layout. The [mjtGain](APIreference/APItypes.md) and [mjtDyn](APIreference/APItypes.md) enums gained `pid` members, shifting the values of `mjGAIN_USER` and `mjDYN_USER`.
24. `596b6f43` [mjResource](APIreference/APItypes.md) gained an `args` field (changing its size and layout), used to hold optional extra encoding and decoding arguments formatted as URI query parameters (separated by `&`).


## Version 3.11.0 (July 27, 2026)

### Engine


PdSdrqhSiZA


1.  `4787c809` Added [geom/surfacevel](XMLreference.md): the velocity of a geom's surface as seen by contacts, given as a velocity field with a constant component and a rotational component about the geom frame origin. This allows conveyor belts, treadmills and turntables to be modeled with static geoms and no degrees of freedom: friction drives touching bodies along the motion of the surface, with the field projected onto each contact's tangent plane. Surface velocities compose correctly with each other and with body motion. Note that the contact rows of `mjData.efc_vel`, and the constraint-state sensors that read them, report the velocity relative to the moving surface rather than to the geom, since that is the quantity the constraint acts on; for geoms without <span class="at">surfacevel</span> the two are identical. Contact-point visualization draws an arrow along the surface velocity at contacts with moving surfaces.


GioWwB36XHI


2.  `a264d0bc` Added [geom/adhesion](XMLreference.md) and [pair/adhesion](XMLreference.md): an adhesive force associated with a contact, useful for modeling sticky materials. Contacts can pull with up to the given force before breaking, and the friction budget becomes $`\mu(f_N + \text{adhesion})`$. Combined with [gap](XMLreference.md), adhesive contacts apply "adhesion at a distance", useful for modeling magnets. Resting penetration is unaffected by adhesion. *mj_contactForce* reports the net interface force, whose normal component can now be negative.
3.  `f0fa3d82` Replaced midpoint integration of free bodies with [gyroscopic derivatives](computation/index.md) in the `implicitfast` [integrator](computation/index.md): the bias-force derivative of every standalone free body is applied via a local unsymmetric solve of its decoupled block, making `implicitfast` identical to `implicit` for such bodies. Unlike midpoint integration, which required vacuum and no constraints, this applies in all environments (contacts, fluid, constraints), and is compatible with discrete-time inverse dynamics. Spinning free bodies no longer gain energy, but tumbling motion is now mildly damped; models requiring long-horizon energy conservation of tumbling bodies in vacuum should use `RK4`. The [invdiscrete](XMLreference.md) flag no longer has any effect on forward dynamics.
4.  `5618666a` Added [body/simple](XMLreference.md) attribute ("false"/"auto") to disable the *simple body* mass matrix optimization. This is useful for domain randomization, where model parameters may change post-compilation.
5.  `14c0b0c9` *mj_setConst* now recomputes the `mjModel.{body,geom,site}_sameframe` flags, to account for changes in body/geom/site frames after compilation.
6.  `2444defc` Added support for [multiccd](computation/index.md) with arbitrarily large meshes.
7.  `a04b0c5b` Added `flg_gravcomp` and `flg_surfacevel` boolean flags to `mjModel`. These flags replace the fast-path checks as originally guarded by `ngravcomp`. Since the engine uses these integers as flags (zero vs. non-zero), the new flags are honest boolean properties, writeable from the Python bindings at runtime. The field `ngravcomp` is deprecated and will be removed in a future release.
8.  `a1f38c8e` Replaced quadratic scratch in DFS flood-fill island discovery with a linear-memory Union-Find (disjoint set). Contribution by `teerthsharma`.


Breaking API changes

9.  `ff629889` Changed the default value of [sleep_tolerance](XMLreference.md) from 1e-4 to 1e-3 (1mm/sec in SI units).
10. `315bcfbf` Removed the legacy sparse ancestor-walk inertia matrix `mjData.qM`. The joint-space inertia matrix is now stored exclusively in the compressed sparse row (CSR) format `mjData.M`.
11. `7e9ac58f` Switched *mjd_inverseFD* to use the CSR-format `mjData.M` representation instead of the legacy `mjData.qM` for the mass matrix derivative. This changes the shape of the `DmDq` parameter from `(nv x nM)` to `(nv x nC)`.
12. `1ea2d884` *mju_round* now breaks ties away from zero rather than towards $`+\infty`$. This only affects negative half-integers, e.g. `mju_round(-2.5)` now returns -3 rather than -2.
13. `fa36015b` Removed unneeded <span class="title-ref">mjvScene</span> argument from *mjv_moveCamera*.
14. `ba9a6503` Split up [mjrfMeshData](APIreference/APItypes.md) into <span class="title-ref">mjrfMeshData</span> and <span class="title-ref">mjrfMeshConfig</span> to allow reuploading of mesh data without having to recreate the mesh object. Introduces `mjrf_defaultMeshConfig` and `mjrf_setMeshData` functions.
15. `ba9a6503` Removed <span class="title-ref">bytes</span> field from [mjrVertexAttribute](APIreference/APItypes.md).



Breaking ABI changes

16. `072e963f` [mjModel](APIreference/APItypes.md) gained the `actuator_ctrlspec` field (input signature of each actuator), and [mjsActuator](APIreference/APItypes.md) gained `ctrlspec`, changing their size and layout. The [mjtGain](APIreference/APItypes.md) and [mjtBias](APIreference/APItypes.md) enums gained `so3` members, shifting the values of `mjGAIN_USER` and `mjBIAS_USER`.
17. `d43c3ed4` Added `texid`, `texuniform` and `texrepeat` fields to [mjvGeom](APIreference/APItypes.md).
18. `a264d0bc` The [mjContact](APIreference/APItypes.md) struct gained an `adhesion` member, changing its size and layout.



Bug fixes

19. `dddb2767` Fixed a bug where `body_margin` excluded `gap`, causing the mid-phase collision filter to incorrectly prune in-gap contacts on multi-geom bodies.


### Actuation

20. `d507e921` Refactored actuator infrastructure in preparation for MIMO (multi-input multi-output) actuator support. Each actuator now has `ctrlnum` (number of controls) and `outnum` (number of force outputs). The total counts `nu = sum(ctrlnum)` and `nout = sum(outnum)` dimension `mjData.ctrl` and `mjData.actuator_force`, respectively, `nactuator` is the number of actuators. For existing actuators `ctrnum = outnum = 1`, so `nactuator == nu == nout` and existing code is unaffected.
21. `56a93979` Setpoints of [position](XMLreference.md) and [intvelocity](XMLreference.md) servos acting on 3D rotational transmissions (ball joints, or site transmissions with a [refsite](XMLreference.md) and purely rotational gear) are now interpreted on the circle: the force uses the setpoint representative nearest the current angle, so targets winding beyond half a turn are tracked continuously instead of slipping by full turns. Behavior is identical whenever the error does not exceed π. Relatedly, `intvelocity` actuators now expose [actlimited](XMLreference.md), which was previously hardcoded to "true": as for [general](XMLreference.md) actuators it defaults to "auto", so activation clamping is enabled by specifying `actrange`. Unclamped integrated setpoints are well-behaved on rotational transmissions, where they wrap.


17XpwnqyCXs


22. `072e963f` Added the [orientation](XMLreference.md) actuator: a geodesic servo on a new SO(3) transmission (ball joints, or a site with a [refsite](XMLreference.md)), acting jointly on the full relative orientation with an exact equilibrium at every commanded orientation. This is the first actuator with multiple force outputs (3), and, with `input="quat"`, the first with different input and output dimensions (4 controls, 3 outputs). The input signature is recorded in the new `mjModel.actuator_ctrlspec`, exposed as the [input](XMLreference.md) attribute.
23. `072e963f` Added *mj_actuatorInputName*, returning the name of an actuator input (e.g. "qw" for the first control of a quaternion-commanded orientation actuator). The control sliders in [simulate](programming/samples.md) and MuJoCo Studio are now generated per control and labeled with the actuator name plus the input name suffix.
24. `072e963f` Viewer control sliders now use a defined [ctrlrange](XMLreference.md) even when [ctrllimited](XMLreference.md) is "false": the range sets the slider span, while clamping remains controlled by <span class="at">ctrllimited</span>.
25. `072e963f` Added *mj_resetCtrl*, setting controls to neutral values: zero, except quaternion inputs which reset to the identity quaternion. Called by *mj_resetData* and the viewers' "Clear All".

### Solvers

26. `ea230a95` Flex elasticity (stretch, bending, interpolation stiffness) is now integrated implicitly inside the CG constraint solver via an *effective metric*: the mass matrix is augmented with the stiffness Hessian, so contact and elastic forces are solved against one consistent metric. This replaces the previous post-hoc CG correction, which modified `qacc` after the constraint solve. The gate is `solver="CG"` with an implicit integrator and flex stiffness present; Newton and PGS are unaffected. Bending-only models pay zero per-step factorization cost (the factor is precomputed in *mj_setConst*). Inverse dynamics (*mj_inverse*) is now discrete-consistent with forward dynamics for gated models.
27. `c499f7f2` Added Nesterov momentum extrapolation with adaptive gradient restart (O'Donoghue-Candès) to the PGS solver, significantly improving convergence. Overall PGS now requires ~2x fewer iterations.
28. `1e66efd1` Added the Newton decrement -- the quadratic model's predicted cost improvement of the next iteration -- as a third early-termination criterion of the [Newton solver](computation/index.md), alongside cost improvement and gradient norm. This reduces iteration counts at no accuracy cost. Proposed by `adenzler-nvidia` in [MJWarp](mjwarp/index.md) pull request [1520](https://github.com/google-deepmind/mujoco_warp/pull/1520).
29. `c69ef030` The CG and Newton solvers now terminate with zero iterations when a duality-gap certificate proves that the warmstarted solution already satisfies the tolerance. The certificate requires only the existing mass-matrix factorization, so quiescent scenes skip Hessian construction, factorization and the line search entirely. Newton zero-iteration exits additionally require the gradient criterion, preserving Newton's characteristic force-level accuracy. See [Warmstart](computation/index.md) in the Computation chapter for details.

### Compiler

30. `4e1795b9` *mj_encode* now supports encoding of MJB and TXT files.
31. `c6c3ec31` The [attach](XMLreference.md) element now supports self-attachment (attaching elements of the current model to itself) by omitting the [model](XMLreference.md) attribute. It also supports attaching a frame via the new [frame](XMLreference.md) attribute, which is mutually exclusive with [body](XMLreference.md).
32. `040872fd` Fixed loading of [.mjz](programming/modeledit.md) archives in [simulate](programming/samples.md): the archive was unmounted before model compilation, so assets failed to load. Failures in the [mjz](programming/modeledit.md) decoder now emit a warning with the underlying error instead of the generic "could not decode content" message.
33. `ebd4abae` The [mjz](programming/modeledit.md) decoder now searches for `model.xml` and `<stem>/model.xml` as a fallback if `<stem>.xml` and `<stem>/<stem>.xml` are not found.
34. `dc7581ac` Added support for resource writing via *mju_writeResource* and the `write` callback in [mjpResourceProvider](APIreference/APItypes.md).


Breaking API changes

35. `d83ef0b6` The return type of *mj_encode* and the [mjfEncode](APIreference/APItypes.md) callback changed from `int` to `mjtSize` (64-bit).



Bug fixes

36. `f5f9d9ef` Fixed a bug in the mesh compiler where normals were scaled as vectors rather than covectors.


### Python bindings

37. `a07ae6f8` The bindings now support free threading ([PEP 703](https://peps.python.org/pep-0703/)) for Python 3.14.

### Documentation

38. `1f1bfa9e` Expanded documentation for [spec.encode](programming/modeledit.md) workflows and added detailed documentation for the [MJZ Archive](programming/modeledit.md) format (`.mjz` / `.zip`).

## Version 3.10.0 (June 22, 2026)

### General

1.  `b935d415` Added *mju_threadpool*, a new function for creating a thread pool on an `mjData` instance. When a thread pool is initialized, parts of the simulation pipeline, such as collision detection and constraint solving across islands, are parallelized. The thread pool is automatically destroyed when the `mjData` is freed.

2.  `58f6d524` Added a unified [logging API](programming/simulation.md):

    - All errors, warnings, and informational messages are now routed through a single [mjfLogHandler](APIreference/APItypes.md) callback receiving a structured [mjLogMessage](APIreference/APItypes.md).
    - Users can install a custom handler via *mju_setLogHandler*, configure the default handler's behavior (console/file output, topic filtering) via *mju_setLogConfig*.
    - Messages can be emitted via *mju_info* and *mju_message*.
    - New types: [mjtLogLevel](APIreference/APItypes.md), [mjtLogTopic](APIreference/APItypes.md), [mjLogMessage](APIreference/APItypes.md), [mjLogConfig](APIreference/APItypes.md).
    - The legacy callbacks [mju_user_error](APIreference/APIglobals.md) and [mju_user_warning](APIreference/APIglobals.md) are deprecated but remain functional.

3.  `6f8bb5ef` Added *mjs_numWarnings* and *mjs_getWarning* for retrieving all warnings accumulated during model compilation and attachment. Deprecated *mjs_isWarning* in favor of `mjs_numWarnings(s) > 0`.

4.  `410c7316` Added the [compiler/conflict](XMLreference.md) attribute for controlling how conflicting global attributes are resolved during *attachment*. Possible values are "warning" (default: parent values take precedence, warnings emitted on conflicts), "merge" (per-field min/max/error strategy), and "error" (any conflict raises an error). See [Attribute Merging](programming/modeledit.md) for details.


    Future breaking API changes

    The current default conflict resolution policy "warn" (ignore the child model) is backward compatible. However, the default policy will change to "merge" in a future release.


5.  `cd6db9eb` Improved primal solver convergence under float32. Improvements initially proposed by `n3b` in `2313` and `adenzler-nvidia` in [MJWarp](mjwarp/index.md) pull request [1374](https://github.com/google-deepmind/mujoco_warp/pull/1374).

6.  `828052e6` The [CG solver](computation/index.md) now uses the Hager-Zhang conjugate direction update instead of the Polak-Ribiere-Plus formula. This improves convergence and leads to a significant speedup under float32.

7.  `4c381635` Added *mjs_makeFlex*, a new C API function equivalent to the [flexcomp](XMLreference.md) element for programmatically creating flex objects with auto-generated bodies, joints, and equality constraints. Exposed as `body.make_flex()` in Python.

8.  `7a7dc7cc` Added support for loading 1D flex components from OBJ line segments

9.  `ea2d785e` Significantly improved the quality of coarse convex hulls produced by the [maxhullvert](XMLreference.md) attribute by invoking Qhull's [Q9](http://www.qhull.org/html/qh-optq.htm#Q9) option.


Breaking API changes

10. `b935d415` The header file `mjthread.h` was removed along with the old engine threading API. <br/> **Migration:** Use *mju_threadpool* to set number of worker threads for the engine.

11. `96bf8aea` Moved island sparse matrix construction from *mj_island* (single threaded) into *mj_fwdConstraint* (multi-threaded). The island-specific matrices `iM, iLD, iefc_J` were removed from the arena and are now allocated on the stack.

12. `4548e81e` Following the introduction of the [diagexact](XMLreference.md) flag, the `mjData` field `efc_diagApprox` was renamed to `efc_diagA`, as it can now be either the exact or approximate diagonal of the $`A`$ ("Delassus") matrix.

13. `062b0f1e` The deprecated functions `mju_{error,warning}_{i,s}` have been removed.

14. `7b9b8806` Changed the signature of *mj_fullM* from `mj_fullM(m, dst, M)` to `mj_fullM(m, d, dst)` as part of the planned deprecation of `mjData.qM` in favor of the CSR-format `mjData.M`.

    **Migration:** For inertia matrix conversion, replace `mj_fullM(m, dst, d->qM)` with `mj_fullM(m, d, dst)` or `mju_sym2dense(dst, d->M, m->nv, m->M_rownnz, m->M_rowadr, m->M_colind)`.


### Bug fixes

15. `a8eaccd2` Fixed a vulnerability in the System Identification toolbox where loading a trajectory or time series called `np.load` with `allow_pickle=True`, allowing arbitrary code execution from a malicious `.npz` file. Signal metadata is now serialized as JSON and loaded with `allow_pickle=False`.
16. `b9fb817a` Fixed a bug in the [mjz](programming/modeledit.md) [decoder](APIreference/APItypes.md) where unnormalized paths would fail to be read.
17. `986d73c0` Fixed a bug where the mesh compiler would produce non-unit convex hull polygon normals.

## Version 3.9.0 (May 27, 2026)

### General

1.  `71d1014e` Added `mjData.efc_Y`, the whitened constraint Jacobian $`Y = J M^{-1/2}`$, allocated in the arena when dual solvers (PGS or NoSlip) are used or when [diagexact](XMLreference.md) is enabled.
2.  `71d1014e` Added the [diagexact](XMLreference.md) enable flag, which computes the exact diagonal of the constraint-space inertia matrix at the current configuration, replacing the default compile-time approximation. This improves solver quality for models with anisotropic inertias or complex kinematic coupling. See [Exact diagonal](computation/index.md) for details.
3.  `7bfdbad8` The pseudo-random constraint visitation order in the [PGS solver](computation/index.md), introduced in the previous release, now uses a fixed seed. The previous implementation seeded with `mjData.time`, which introduced subtle yet undesirable time dependence.
4.  `f712eed4` Flexes are now allowed to sleep, with the exception of completely passive (constraint-free) flexes.
5.  `bdf00966` Added compiler timing diagnostics via the new [mjtCTimer](APIreference/APItypes.md) enum and the *mjs_getTimer* C API. After *mj_compile*, per-category timings (total, assets, mesh loading, convex hull, normals, inertia, BVH, octree, textures) are available via `mjs_getTimer(spec)`. The [compile](programming/samples.md) sample prints a detailed timing breakdown when run without an output file.
6.  `393c1e42` Added [mjtBool](APIreference/APItypes.md) to represent boolean variables, replacing [mjtByte](APIreference/APItypes.md) across all boolean fields in [mjModel](APIreference/APItypes.md), [mjData](APIreference/APItypes.md), and public C API function signatures.


Breaking API changes

7.  `a4e49f2d` The semantics of the contact `margin` and `gap` parameters have been redesigned for conceptual clarity and consistency with [Newton](https://github.com/newton-physics/newton). See the new [margin and gap](computation/index.md) documentation section for details.

    Previously, `margin` controlled the *detection threshold* (contacts exist when `dist < margin`) and `gap` was subtracted from it to produce the *force threshold* (forces generated when `dist < margin - gap`). This was unintuitive: users expected `margin` to mean geometric inflation and `gap` to mean a spatial gap.

    Under the new semantics, `margin` is the geometric inflation of the geom surface and `gap` is an additional detection buffer beyond the inflated surface:

    - **Detection**: contacts are created when `dist < margin + gap`.
    - **Force generation**: constraint forces are applied when `dist < margin`.
    - **Inactive contacts**: contacts with `margin < dist ≤ margin + gap` are included in `mjData.contact` but generate no force (`efc_address = -1`). This is useful for [adhesion](XMLreference.md) actuators and custom callbacks.

    With the default values `margin = 0`, `gap = 0`, the behavior is unchanged.

    <img src="images/modeling/margin_gap_light.svg" class="only-light only-lightalign-center" style="width:80.0%" alt="image" />

    <img src="images/modeling/margin_gap_dark.svg" class="only-dark only-darkalign-center" style="width:80.0%" alt="image" />

    **Migration:** Models that use the default `gap="0"` (the vast majority) require no changes. For models with `gap > 0`, apply the following transformation to preserve identical behavior:

    ``` 
    margin_new = margin_old - gap_old
    gap_new    = gap_old
    ```

    For example, a geom with the old attributes `margin="0.1" gap="0.1"` should be changed to `margin="0" gap="0.1"`.

    Negative `margin` values are now permitted (corresponding to `gap > margin` under the old semantics). The constraint `margin + gap >= 0` should be maintained to ensure valid collision detection.

8.  `7174d33f` The [mjfCollision](APIreference/APItypes.md) functions now populate the [mjPreContact](APIreference/APItypes.md) struct instead of the [mjContact](APIreference/APItypes.md) struct. The [mjPreContact](APIreference/APItypes.md) only contains the necessary fields needed for the narrowphase collision detection.

9.  `2810edd2` The header file `mjtnum.h` was renamed to <span class="title-ref">mjtype.h \<https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjtype.h\></span> and now includes all enum type definitions.

10. `f6cd0234` The [tactile](XMLreference.md) sensor now reports raw depth instead of an estimated pressure.

11. `072125c4` MJX: Removed the deprecated `nconmax` argument from `mjx.make_data` and `mjx.put_data` in favor of `naconmax`.

12. `15d27b36` Maybe-breaking: Added [mjassert.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjassert.h), a new header containing compile-time assertions that verify the sizes of MuJoCo's public types for ABI stability. This is a first step towards replacing `int` with strongly-typed enums in the public API. If these assertions fail on your compiler or platform, please report the issue on GitHub.


## Version 3.8.1 (May 11, 2026)

### General

1.  `647af382` Added island support for the [PGS solver](computation/index.md).
2.  `4ed69b5c` The [PGS solver](computation/index.md) now iterates over constraints in pseudo-random order, improving performance by ~20%.
3.  `b9c1877e` Added support for [elastic2d](XMLreference.md) for trilinear and quadratic flex [dofs](XMLreference.md).
4.  `910b3336` Midpoint integration is now restricted to the `implicitfast` [integrator](computation/index.md) and is disabled when fluid forces are active (nonzero [density](XMLreference.md) or [viscosity](XMLreference.md)). Midpoint integration treats external forces as zero-order-hold constants, which causes energy gain in the presence of contacts and in fluid media.
5.  `ec50260e` Added *mjs_getOriginSpec*, returning the spec that originally defined an element, prior to attachment. This is in contrast to *mjs_getSpec* which returns the spec currently owning the element. If the element is not the result of an attach operation, the functions are identical.
6.  `767c607f` Added *mju_sym2dense*, converting a lower-triangular, implicitly symmetric CSR matrix to a dense symmetric matrix. The inertia matrix `mjData.M` is an example of such a matrix.


Future breaking API changes

7.  `767c607f` The introduction of *mju_sym2dense* is a step towards the removal of the legacy-format `mjData.qM` in favor of the CSR-format `mjData.M`. This removal will involve a future breaking change to *mj_fullM* (which currently accepts a `qM`-like matrix as an argument). To prevent a future breakage, replace `mj_fullM(m, dst, d->qM)` with <br/> `mju_sym2dense(dst, d->M, m->nv, m->M_rownnz, m->M_rowadr, m->M_colind)`.


### Bug fixes

8.  `3e960ba3` Fixed default for multiccd in [mjcPhysics](OpenUSD/mjcPhysics.md).

### Python

9.  `d92fe081` Added `MjSpec.encode` method, wrapping *mj_encode*.

10. `723b8b1e` Added `mujoco.MjVfs` Python binding to interact with the Virtual File System directly from Python. See [Virtual File System](python.md) for usage details.

    > [!WARNING]
    > The previous way of passing assets via a dictionary mapping asset names to bytes is **deprecated** and will be removed in an upcoming release. You cannot specify both the `assets` dictionary and the `vfs` argument at the same time. `MjVfs` should be used as a drop-in replacement.

## Version 3.8.0 (April 24, 2026)

### General

1.  `a04cf1b2` Added support for Python 3.14.
2.  `2f2d00da` Added [multi-cell support](XMLreference.md) for trilinear and quadratic flexes. Note that the implicit integrator uses a dense solver for the flex degrees of freedom, which can be slow for multi-cell flexes.
3.  `3d45a331` Refactored `strain` flex [equality constraints](XMLreference.md) to be instantiated per cell instead of per flex object, reducing the number of degrees of freedom per constraint row. The equality can be associated with a specific cell with the new attribute [cell](XMLreference.md)
4.  `33259718` Added new *mj_maxContact* function to get the maximum number of possible contacts returned by colliding two geoms.
5.  `4cfebcc3` Added `mj_containsBufferVFS` and `mj_containsFileVFS` to check for existence of buffers and files in VFS.


Breaking API changes

6.  `6cb6e5a9` The [multiccd](computation/index.md) option (multiple contacts returned from the convex collision detection pipeline) is now enabled by default. The new implementation (as opposed to the legacy pipeline) has little performance overhead and improves stability.

    **Migration:** Disable [multiccd](XMLreference.md) to recover the previous behavior.


### Documentation

7.  `2f5e5d3d` Added [documentation](programming/extension.md) for [mjpDecoder](APIreference/APItypes.md) plugins.

### Bug fixes

8.  `da01bd37` Asset paths in attached child specs are now resolved relative to the model file directory of the child spec, rather than the parent spec. This prevents the origin of the parent spec to affect the resolution of asset paths in the child spec.

## Version 3.7.0 (April 14, 2026)

### General

1.  `70a7647a` Added the [dcmotor](XMLreference.md) actuator for modeling DC motors. Supports optional electrical dynamics (inductance), cogging torque, thermal resistance variation, and LuGre friction. See the [technical note](_static/dcmotor.pdf) for more details.
2.  `510d75f4` Actuators with joint or tendon transmissions can now contribute [damping](XMLreference.md) and [armature](XMLreference.md) to their transmission target. These are applied during the passive force and inertia computations, respectively, and are scaled by gear<sup>2</sup> ("reflected" damping/inertia).


aKa3ZlEF9_Y


3.  `efae9157` Stiffness in [joints](XMLreference.md) and [tendons](XMLreference.md) and damping in [joints](XMLreference.md) and [tendons](XMLreference.md) now support nonlinear polynomial [force profiles](computation/index.md). New `mjModel` arrays (`jnt_stiffnesspoly`, `tendon_stiffnesspoly`, `dof_dampingpoly`, `tendon_dampingpoly`) hold higher-order coefficients. The existing scalar arrays (`jnt_stiffness`, `dof_damping`, etc.) continue to hold the linear coefficient and are unchanged. The polynomial order is defined by the new constant [mjNPOLY](APIreference/APIglobals.md). A future breaking C-API change may unify the linear and higher-order coefficients into a single array.
4.  `0c337799` Added midpoint integration for standalone free bodies in `implicit` and `implicitfast` [integrators](computation/index.md). This applies the implicit midpoint rule to the rotational dynamics of free bodies with no children, conserving kinetic energy to machine precision in the absence of external torques. The [invdiscrete](XMLreference.md) flag now also disables midpoint integration, providing an opt-out mechanism.
5.  `412cee20` Added the centripetal/Coriolis acceleration term $`\dot{J}v`$ to the constraint solver bias for [connect](XMLreference.md) and [weld](XMLreference.md) equality constaints. This significantly improves the stability of constrained mechanisms like four-bar linkages. See [Dual problem](computation/index.md) for details.
6.  `f5d3ce34` Introduced [mjpEncoder](APIreference/APItypes.md), the counterpart to [mjpDecoder](APIreference/APItypes.md) for encoding of [mjSpec](APIreference/APItypes.md) and [mjModel](APIreference/APItypes.md) into [mjResource](APIreference/APItypes.md).
7.  `f5d3ce34` Added *mj_encode*, *mjp_registerEncoder*, *mjp_defaultEncoder*, and *mjp_findEncoder*.


Breaking API changes

8.  `efae9157` The `mjs` layer fields `stiffness` and `damping` in [mjsJoint](APIreference/APItypes.md) and [mjsTendon](APIreference/APItypes.md) have been widened from `mjtNum` scalars to `mjtNum[mjNPOLY+1]` arrays. The first element is the linear coefficient (previously the scalar), and subsequent elements are the higher-order [polynomial](computation/index.md) coefficients.

    **Migration:** Replace assignments like `joint.stiffness = val` with `joint.stiffness[0] = val`.

9.  `15ca42ff` `.obj` and `.stl` decoders are now included as source when building MuJoCo with CMake. This fixes the behaviour from the previous release where it required downstream code to load these plugins explicitly.

10. `4b1667e4` The `vertcollide` field in [mjsFlex](APIreference/APItypes.md) has been removed. It is no longer required since [MuJoCo Warp](mjwarp/index.md) supports native flex collisions.

11. `f2461f9c` [mjPLUGIN_LIB_INIT](APIreference/APIglobals.md) macro now requires a name argument to avoid initialization function name collisions. When building with MSVC, we now use the C runtime initialization section to initialize plugins instead of `DllMain`. See [plugin registration](programming/extension.md) for more details.

12. `0e04436d` The [mjtWarning](APIreference/APItypes.md) enum value `mjWARN_VGEOMFULL` is removed. Exhaustion of visual geoms is now handled internally by the [mjvScene](APIreference/APItypes.md).

13. `7ae07d81` URDF parsing no longer hardcodes [strippath](XMLreference.md) to "true". The setting is now respected and the default is "false". Setting this is attribute is now the responsibility of the user.

    **Migration:** Set [strippath](XMLreference.md) to "true" in MJCF or programmatically using

    ``` python
    spec = mujoco.MjSpec.from_file("path/to/model.urdf")
    spec.compiler.strippath = True
    ```


### Bug fixes

14. `ecc22667` The compiler now correctly accounts for negative scaling when loading user specified mesh data.

## Version 3.6.0 (March 10, 2026)

### General


Breaking API changes

1.  `9efe41c0` The tendon Jacobian `ten_J` is now always sparse. The fields `ten_J_rownnz`, `ten_J_rowadr`, and `ten_J_colind` have been moved from [mjData](APIreference/APItypes.md) to [mjModel](APIreference/APItypes.md) and are no longer computed at run time by `mj_tendon` but at compile time.


2.  `6890e133` Added *mjs_getCompiler* C API function and a `compiler` read-only property to all Python spec element types. This allows querying the compiler settings (e.g., `meshdir`) from any element, with the correct originating spec's compiler preserved after attachment.
3.  `713b5524` Added a new `strain` [equality constraint](XMLreference.md) type for trilinear and quadratic [dofs](XMLreference.md).
4.  `bf74d01d` Flexes now support collisions with SDF geoms.
5.  `5903d482` Improved memory requirements for `ten_J` and `ten_J_colind` by reducing the upper bound for the number of non-zeros `nJten`.
6.  `37e993f6` Improved memory requirements for `actuator_moment` and `moment_colind` by reducing the upper bound for the number of non-zeros `nJmom`.

### MJX

7.  `62a32386` Add batch rendering support for MJX-Warp. See the [MJX-Warp batch rendering](mjx.md) section for details.

### Bug fixes

8.  `6ec808e2` Fixed a bug where *mjs_attach* silently dropped spatial tendons with wrapping geometries that had no `sidesite` attribute (`3119`, reported by `tomstewart89`).

## Version 3.5.0 (February 12, 2026)

### Significant new features

1.  `b64b527e` [MuJoCo Warp](mjwarp/index.md) is now officially released.
2.  `146a5c08` Added a new **System Identification** toolbox (Python), see [README](https://github.com/google-deepmind/mujoco/blob/main/python/mujoco/sysid/README.md) for details. <br/> A Colab notebook demonstrating the toolbox is available here: [![sysid_colab](https://colab.research.google.com/assets/colab-badge.png)](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/mujoco/sysid/sysid.ipynb) <br/> Contribution by `kevinzakka`, `aftersomemath`, `jonathanembleyriches`, `qiayuanl`, `spjardim` and `gizemozd`.

<!-- -->

3.  `6419534b` Actuators and sensors now support arbitrary delays via history buffers, and sensor values can be computed at intervals larger than the simulation timestep. Using a delay or interval introduces a new `mjData.history` variable to the [Physics state](programming/simulation.md). See [Delays](modeling.md) for details.

[<img src="images/changelog/poncho.png" class="align-right" style="width:45.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/model/flex/poncho.xml)

4.  `7da271c6` Added new `flexvert` equality constraints that enable cloth simulations with coarser meshes. This adds a new attribute value `vert` to flexcomp edge [equality](XMLreference.md) and the new equality type `flexvert`. Uses the method described in [Chen, Kry and Vouga, 2019](https://arxiv.org/abs/1911.05204).
5.  `0041fdcb` Added implicit integration support for deformable objects (flex) in `implicit` and `implicitfast` [integrators](computation/index.md). This method extracts the flex degrees of freedom and solves them as a dense block, enabling increased stability for stiff flex objects without reducing the timestep. It is compatible with the `trilinear` and `quadratic` [dof](XMLreference.md) types.

[<img src="images/XMLreference/rfcamera.png" class="align-right" style="width:45.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/sensor/rfcamera.xml)

6.  `9d646e65` Rangefinder sensors can now be attached to a camera using the [rangefinder/camera](XMLreference.md) attribute. In this case, the sensor respects the [camera/resolution](XMLreference.md) attribute and casts multiple rays, one for each pixel.
7.  `ed15493a` [Rangefinders](XMLreference.md) can now report various kinds of information besides ray distances, including surface normals and intersection points.


</div>


### General


Breaking API changes

8.  `218226fc` Ray-cast functions now optionally compute the surface normal at the ray intersection. This is a breaking change due to the addition of the `mjtNum normal[3]` argument. The modified functions are *mj_ray*, *mj_multiRay*, *mju_rayGeom*, *mj_rayFlex*, *mj_rayHfield* and *mj_rayMesh*.

    **Migration:** In C/C++, pass `NULL` to the `normal` argument. In Python, in all functions except *mj_multiRay*, it defaults to `None`, so no action is required.

9.  `218226fc` `mju_rayFlex` has been renamed to *mj_rayFlex* for consistency with other functions that take `mjModel*` and `mjData*` arguments.

10. `b8a4ac5d` The `mjModel.cam_orthographic` field has been renamed to `cam_projection`, with the semantic of a new enum type [mjtProjection](APIreference/APItypes.md). This will allow for more projection types in the future like fisheye cameras. Relatedly, the `camera/orthographic` MJCF attribute for cameras has been renamed to [camera/projection](XMLreference.md) and now accepts the values `orthographic` and `perspective`.

    **Migration:** Replace `orthographic = "false/true"` with `projection="perspective/orthographic"`, respectively.

11. `cb9a9c15` Removed `getdir` from the `mjpResourceProvider` struct. All Resource Providers now use the same shared implementation.

12. `6af0d4c8` When combining the `margin` or `gap` [parameters](modeling.md) of two geoms to obtain the parameters of a contact, the respective values are now **summed** rather than taking the maximum. This allows geom margins to be a proper "inflation" of the geom.


13. `c7f57663` Camera frustum visualization is now triggered by setting [resolution](XMLreference.md) to values larger than 1. Relatedly, frustum visualization also works for [orthographic](XMLreference.md) cameras. See [rangefinder](XMLreference.md) for details.
14. `608115ab` Cameras now have an [output](XMLreference.md) attribute, parsed into the `mjModel.cam_output` bitfield. Unused by the renderer, it serves as a convenient location to store a camera's supported output types.
15. `37762e3f` Added *mj_mountVFS* and *mj_unmountVFS* functions for mounting a custom VFS provider. Mounting allows providers to be used to open/read/close resources dynamically at arbitrary paths.
16. `1d2d0b1c` The optimization whereby sequential [collision sensors](XMLreference.md) with identical attributes shared computation has been removed. This results in a (likely minor) performance regression for models which exploited this optimization. To recover the performance, use the [fromto](XMLreference.md) and compute the other values manually. If `from = fromto[0:3]` and `to = fromto[3:6]` then `distance = norm(to-from)` and `normal = normalize(to-from)`.
17. `a5dc57c0` [OpenUSD](OpenUSD/index.md):
    - Parsing has been moved out of experimental into a mjpDecoder plugin. (documentation pending)
    - OpenUSD can now be built with the [third_party_deps/openusd](https://github.com/google-deepmind/mujoco/tree/main/cmake/third_party_deps/openusd) CMake utility project.
    - `USD_DIR` is no longer used by the MuJoCo CMake project, instead use `pxr_DIR` if you have a pre-built USD library.
    - Users no longer have to set `PXR_PLUGINPATH_NAME` environment variable, MuJoCo should load USD plugins automatically.
18. `1ff74ba8` Non-breaking ABI changes:
    - The type of the `sig` (signature) argument of *mj_stateSize* and related functions has been changed from `unsigned int` to `int`. Before this change, invalid negative arguments passed to this function would result in a silent implicit cast; now, negativity will trigger an error.
    - Added a [depth](APIreference/APItypes.md) rendering flag.
    - Allocation sizes in [mjModel](APIreference/APItypes.md) now use 64-bit rather than 32-bit integers to accommodate larger scenes.

### MJX

19. `1483aefe` Added `actuator_length`, `cdof` and `cdof_dof` fields to `mjx.Data`.
20. `d07f39b4` Add `graph_mode` argument to `put_model` to support multiple Warp graph capture modes.

### Documentation

21. `b77977a9` General improvements to the [Programming/Simulation](programming/simulation.md) chapter. Notably, the main discussion of [state](programming/simulation.md) has been moved there, and the section on [mjModel changes](programming/simulation.md) has been expanded.
22. `c5925e7b` The usability of the [MJCF schema](XMLreference.md) is improved with a collapsible dropdown menu with links to elements and attributes.
23. `c54f1fe3` MuJoCo version numbering is now based on Semantic Versioning, see [VERSIONING.md](https://github.com/google-deepmind/mujoco/blob/main/VERSIONING.md).

### Bug fixes

24. `b4668294` Fixed a bug in [implicit integrator](computation/index.md) derivatives where actuator velocity derivatives were incorrectly computed when the force was clamped by [forcerange](XMLreference.md).
25. `7f74487a` Fixed a bug in [implicit integrator](computation/index.md) derivatives where actuator velocity derivatives did not account for the [actearly](XMLreference.md) flag.
26. `64a2345c` Multi-threaded mesh processing, enabled by the [usethread](XMLreference.md) compiler flag (on by default), was in fact disabled by the flag. Fixing this bug speeds up compilation of mesh-heavy models by (up to) the number of available cores.
27. `223ba99e` The `vertid` argument of *mj_rayFlex* and *mju_raySkin* was marked as nullable but was not; it is now nullable.
28. `c1b3b306` Fixed [gravcomp](XMLreference.md) being ignored for bodies with no joints nested inside jointed parent bodies (`3066`, reported by `Alex108306`).

## Version 3.4.0 (December 5, 2025)

### General


vct493lGQ8Q


1.  `8734cab3` Introduced a major new feature: [sleeping islands](computation/index.md). Preliminary release for early testing, see documentation for details.
2.  `3a7aa84e` Added "quadratic" option to [flexcomp/dof](XMLreference.md). This type of fast [deformable](modeling.md) flex object is similar to the "trilinear" option, but it includes curved deformations.
3.  `b6f25ca6` Raise an error if there are name collisions also during parsing.
4.  `b6f25ca6` Increase Windows stack size to 16MB to enable models with deep nested body hierarchies.
5.  `19e2d0ae` Added a new pipeline component function *mj_fwdKinematics* that combines all kinematics-like sub-components. Relatedly, added a clarifying table at the top of the [Simulation Pipeline](computation/index.md) chapter.
6.  `2f65e237` Added a new *mj_extractState* function that allows a subset of a state that was previously returned by *mj_getState* to be extracted without having to be written back into `mjData` first.
7.  `888d3a7b` Added a new *mj_copyState* function that copies state components from one `mjData` to another.
8.  `ac2cd5df` Tendon paths can now be queried from Python via `MjsTendon.path`, the returned object is iterable and indexing it will give the `MjsWrap` at the given index in the path.
9.  `ac2cd5df` `MjsWrap` now exposes:
    - `type -> mujoco.mjtWrap`
    - `target -> MjsSite|MjsJoint|MjsGeom|None`
    - `sidesite -> MjsSite|None`
    - `coef -> real`
    - `divisor -> real`
10. `86a77ff8` Non-breaking ABI changes:
    - [mjtSize](APIreference/APItypes.md) is now defined as `int64_t` rather than `uint64_t` to avoid future type-promotion bugs.
    - *mj_sizeModel* now returns an [mjtSize](APIreference/APItypes.md) rather than an `int`.

### MJX

11. `c34ac712` `warp-lang` optional dependency is updated to 1.10.0. `pmap` now works with MuJoCo Warp from MJX.


Breaking ABI changes

12. `d0f32a7f` `mjx.Model.tex_data` is now a numpy ndarray instead of a jax.Array, to avoid vmapping over this potentially large array. This may break certain use-cases with Madrona MJX, but we are no longer supporting this codepath. We will be migrating users to a Warp-based batch renderer.


### Bug fixes

13. `88383684` Fixed a bug in the box-box distance computation. Reported by `nvtw`.

## Version 3.3.7 (October 13, 2025)

### General


Breaking API changes

1.  `77e025ea` The mjSpec C API fields [meshdir](XMLreference.md) and [texturedir](XMLreference.md) have been moved to [compiler.meshdir](https://github.com/google-deepmind/mujoco/blob/0baac589993220095cf09e153f194f35ca0f0738/include/mujoco/mjspec.h#L154) and [compiler.texturedir](https://github.com/google-deepmind/mujoco/blob/0baac589993220095cf09e153f194f35ca0f0738/include/mujoco/mjspec.h#L155) respectively. For backwards compatibility, the old fields are still available in the Python API but will be removed in a future release.

    **Migration:** Replace `meshdir` and `texturedir` with `compiler.meshdir` and `compiler.texturedir`.

2.  `192da874` Remove `_full_compat` from `mjx.put_data` and `mjx.put_model`.

3.  `b56cf98e` `nconmax` and `njmax` fields in `mjx.make_data` now default to `None` instead of -1. `nconmax` will be deprecated in favor of `naconmax` in a future release.

4.  `401bf431` The `Simulate::InjectNoise` method needs to set the target of exponential decay to a value from `key_ctrl` if a valid key is provided as input, else -1.


5.  `fe8384b6` Joint decorators and spatial tendons which have limits defined and whose current value (angle or length) exceeds the limit, are recolored by using the [constraint impedance](computation/index.md) $`d`$ to mix the existing color with [visual/rgba/constraint](XMLreference.md). For spatial tendons, this visualization aid is active only if no [material](XMLreference.md) is set and [rgba](XMLreference.md) is default.
6.  `6320b959` Added *mju_getXMLDependencies* for computing a list of unique asset dependencies from an MJCF file.
7.  `e4704cd2` Added the code sample `dependencies` which provides command line utility for printing the result of *mju_getXMLDependencies*.
8.  `bd68f0c6` The minimum C++ standard required to compile MuJoCo is now C++20, this has been the case within Google since 2023 but the CMake update was forgotten.


Breaking ABI changes

9.  `431f9657` The attribute `mjOption.apirate` was unused and has been removed.
10. `b56cf98e` MJX `nconmax` and `njmax` fields in `mjx.make_data` now default to `None` instead of -1.


### MJX

11. `6ae9cc80` Fix `2508`, `qLD` shapes mismatched mjModel during `get_data_into`.
12. `b56cf98e` Pull in MuJoCo Warp update to `io.py`, and use `naconmax` instead of `nconmax` to set the maximum number of contacts over all environments.

### Bug fixes

13. `98682ae2` Fix `2881`, <span class="at">fitaabb</span> was adding an offset to the mesh and applying an incorrect frame transformation. Also, unify the meaning of fitting a geom to a mesh AABB: it now means to find the smallest geom such that its AABB contains the mesh AABB.

## Version 3.3.6 (September 15, 2025)

### General

1.  `ec94bb49` Constraint island discovery and construction, previously an experimental feature, is now [documented](computation/index.md) and promoted to default; disable it with [option/flag/island](XMLreference.md). We expect islanding to be a strict improvement over the monolithic constraint solver, please let us know if you experience any issues.
2.  `7443e685` [Contact sensor](XMLreference.md) <span class="at-val">subtree1/subtree2</span> specification is now available for any body, not just direct children of the world.


Breaking API changes

3.  `6ec5f8b9` The update of `mjData.qacc_warmstart` was moved from the end of the solver call (*mj_fwdConstraint*) to the end of *mj_step*, and is now updated with all other state variables. This change makes *mj_forward* fully idempotent.

    Before this change, calling *mj_forward* repeatedly would make the constraint solver converge, since each subsequent call would start from the previously updated `qacc_warmstart` value. Indeed, this is precisely what happened in the viewer, which calls *mj_forward* repeatedly in PAUSE mode.

    **Migration:** If your code depended on this behavior, you can recover it by updating manually after each *mj_forward*: `qacc_warmstart ← qacc`. The behavior is available in [simulate](programming/samples.md) by clicking the "Pause update" toggle (off by default).

    Furthermore, this change has a numerical impact on the output of the [RK4](computation/index.md) integrator. Before this change, due to the `qacc_warmstart` update occurring after each of the four Runge-Kutta substeps, the solver convergence of RK4 was faster, at the cost of unprincipled integration. This change makes the RK4 integration principled and well-defined. Since this change to RK4 is effectively a bug fix, migration to the previous behavior is not provided.

4.  `b092563c` The `mjDSBL_PASSIVE` flag for disabling passive forces was removed and replaced by [mjDSBL_SPRING](APIreference/APItypes.md) and [mjDSBL_DAMPER](APIreference/APItypes.md) with corresponding [mjcf](XMLreference.md) [attributes](XMLreference.md). Each flag disables only joint and tendon springs or dampers, respectively. When both flags are set, **all** passive forces are disabled, including gravity compensation, fluid forces, forces computed by the [mjcb_passive](APIreference/APIglobals.md) callback, and forces computed by [plugins](programming/extension.md) when passed the [mjPLUGIN_PASSIVE](APIreference/APItypes.md) capability flag.

    **Migration:** Set both flags to recover the behavior of the previous flag.



Breaking ABI changes

5.  `ed6fa7fe` Removed `mjMOUSE_SELECT` flag for [mjtMouse](APIreference/APItypes.md) as it is no longer in use.
6.  `ec94bb49` The promotion of islanding to default involved removing the enable flag `mjENBL_ISLAND` and converting it to a disable flag [mjDSBL_ISLAND](APIreference/APItypes.md).


7.  `b66175eb` Added support for shells with a curved reference configuration. See this [example](https://github.com/google-deepmind/mujoco/blob/main/model/flex/basket.xml).
8.  `8acd83f3` Added experimental option for [passive](XMLreference.md) contacts involving flexes.
9.  `1fb1810b` Added support for assigning a default material to a mesh asset using the [mesh/material](XMLreference.md) attribute.

### MJX

10. `1763fa53` Promote `ten_length` to the public MJX API. Add Warp support for `mjx.tendon`.


Breaking API changes

11. `1763fa53` `ten_length` was moved from `mjx.Data._impl.ten_length` to a public field `mjx.Data.ten_length`.


### Bug fixes

12. `ec94bb49` Fixed a latent bug where MjData objects were not serialized correctly by the Python bindings when islanding was enabled.

## Version 3.3.5 (August 8, 2025)

### General

1.  `e6c57159` Added the [insidesite](XMLreference.md) sensor, for checking if an object is inside the volume of a site. It is useful for triggering events in surrounding environment logic.
2.  `d0e4771c` Added the [contact](XMLreference.md) sensor, for reporting contact information according to user-defined criteria. The purpose of the <span class="el">contact</span> sensor is to report contact-related information in a fixed-size array. This is useful as input to learning-based agents and in environment logic.
3.  `51babec9` Added the [tactile](XMLreference.md) sensor, for measuring the penetration depth between two objects at given points and the sliding velocities in the tangent frame. The sensor reports tactile data only when colliding with SDFs.
4.  `0b11e3e3` Removed the SdfLib plugin and the dependency on [SdfLib](https://github.com/UPC-ViRVIG/SdfLib). SDFs are now supported natively in mjModel.
5.  `5e666635` Removed `oct_depth` from [mjvOption](APIreference/APItypes.md) (unused).
6.  `89f47890` Added the functionality to create a builtin meshes, see [mesh/builtin](XMLreference.md).
7.  `ad0dc0de` Inertia computation in MuJoCo C is now performed by a new [pipeline](computation/index.md) function *mj_makeM*, which combines the Composite Rigid Body algorithm in *mj_crb* and additional terms related to [tendon armature](XMLreference.md). Code that uses *mj_crb* to compute the inertia should now use *mj_makeM* instead.


Breaking API changes

8.  `5e666635` Removed the `mjVIS_FLEXBVH` enum value, its functionality is now provided by [mjVIS_MESHBVH](APIreference/APItypes.md).


### Bug fixes

9.  `6e7aaacb` Fixed a bug that caused object lists in the child to have missing elements after attaching an mjSpec. This was caused by adding to the lists only the objects that belong to the tree of the requested body, but this causes to skip objects that were attached, since they belong to the tree of the parent.
10. `3434f5d9` Fixed a bug where the convex hull of a collision mesh was not being computed if the mesh could only collide via a [contact pair](XMLreference.md).

### Python

11. `2e60d058` On Linux, built distribution packages (wheels) now target the `manylinux_2_28` platform tag. Previously MuJoCo wheels targeted `manylinux2014` based on CentOS 7, which reached end-of-life in June 2024.

### MJX

12. `47bc16a3` Add Warp as a backend implementation for MJX. The implementation can be specified via `mjx.put_model(m, impl='warp')` and `mjx.make_data(m, impl='warp')`. The warp implementation requires a CUDA device and `warp-lang` to be installed (`pip install mujoco-mjx[warp]`). This feature is available in "beta" and some bugs are expected.

## Version 3.3.4 (July 8, 2025)


Breaking API changes

1.  `18d5d5d0` The functions `mjs_detachBody` and `mjs_detachDefault` have been replaced by *mjs_delete*.
2.  `0488d9f4` The Python functions `element.delete` have been replaced by `spec.delete(element)`.
3.  `564c51dd` In the mjSpec C API, directly setting an element's name using *mjs_setString* has been replaced with a new function *mjs_setName* which allows checking for naming collisions at set-time rather than compile-time, for earlier catching of errors. Relatedly, the `name` attribute has been removed from all mjs elements. Known issue: the error is not raised during parsing.
4.  `47bc16a3` For MJX, the `mjx.Option` dataclass now has private and public fields similar to `mjx.Model` and `mjx.Data`. Some fields are no longer publicly available due to differences in the underlying implementations of this data structure.


### General

5.  `14dc7c2a` Added support for setting the initial camera in the viewer using [visual/global/cameraid](XMLreference.md).
6.  `09f7154e` Added support to only sync the state in the Python [passive viewer](python.md)'s `Sync` method, this is useful to improve performance. The default behavior is unchanged and copies the entire model and data.

### Bug fixes

7.  `4ce62932` Inverse dynamics were not being computed correctly when [tendon armature](XMLreference.md) was present, now fixed.
8.  `45d4cacc` Fix bug in `mjx.put_data` where `actuator_moment` was not being copied correctly for the C implementation.

### Documentation

9.  `7548d370` Added missing item documentation and clarified the nature of breaking changes in the 3.3.3 changelog. See items 3 and 4 below.

## Version 3.3.3 (June 10, 2025)

### General

1.  `ecb769fc` Refactored island implementation so that island data is memory-contiguous. This speeds up island processing in the solver and clears the way for the addition of the Newton and PGS solvers (currently only CG is supported).
2.  `7edbdd0a` Removed the <span class="at">shell</span> plugin. This is now supported by [flexcomp](XMLreference.md) and is active depending on the [elastic2d](XMLreference.md) attribute (off by default).


Breaking API changes

3.  `74cc904e` Replaced the [directional](XMLreference.md) (boolean) field for lights with a [type](XMLreference.md) field (of type [mjtLightType](APIreference/APItypes.md)) to allow for additional lighting types.

    **Migration:** Replace light/directional="false/true" with light/type="spot/directional", respectively.

4.  `3e9bc79b` Added [mjtColorSpace](APIreference/APItypes.md) enum and associated [colorspace](XMLreference.md) attribute that allows to specify the color space of textures (either linear or [sRGB](https://en.wikipedia.org/wiki/SRGB)). Since this property is now read correctly from PNG files, textures files which use sRGB will now be rendered differently.

    **Migration:** Set [colorspace](XMLreference.md) to "linear" for all textures that should look like they did before this change.


5.  `89e39dc0` Added new sub-component *mj_makeM* which combines the *mj_crb* call with additional logic to support the introduction in 3.3.1 of [tendon armature](XMLreference.md). In addition to the traditional `mjData.qM`, *mj_makeM* also computes `mjData.M`, a CSR representation of the same matrix.
6.  `84ad22a5` Added a new function *mj_copyBack* to copy real-valued arrays in an mjModel to a compatible mjSpec.
7.  `b8768aa1` Removed the limitation of [fusestatic](XMLreference.md) to models which contain no references. The fusestatic flag will now fuse all bodies which are not referenced and ignore bodies which are referenced.

### Simulate

8.  `ced63018` The struct `mjv_sceneState` has been removed. This struct was used for partial synchronization of `mjModel` and `mjData` when the Python viewer is used in passive mode. This functionality is now provided by *mjv_copyModel* and *mjv_copyData*, which don't copy arrays which are not required for visualization.

<img src="images/changelog/procedural_terrain_generation.png" class="align-right" style="width:33.0%" alt="image" />

### Python bindings

9.  `3a4b6e6c` Added examples of procedural terrain generation to the Model Editing tutorial: [![mjspec_colab](https://colab.research.google.com/assets/colab-badge.png)](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/mjspec.ipynb)

### MJX

10. `caaf7b3a` Added tendon armature.

## Version 3.3.2 (April 28, 2025)

### MJX

1.  `51c489fc` Added inverse dynamics.
2.  `f317bd17` Added tendon actuator force sensor.
3.  `421c487d` Fix `2606` such that `make_data` copies over `mocap_pos` and `mocap_quat` from `body_pos` and `body_quat`.

## Version 3.3.1 (Apr 9, 2025)


Breaking API changes

1.  `f25fc63f` The default value of the flag for toggling `internal flex contacts` was changed from "true" to "false". This feature has proven to be counterintuitive for users.
2.  `a02a27d4` All of the attach functions (`mjs_attachBody`, `mjs_attachFrame`, `mjs_attachToSite`, `mjs_attachFrameToSite`) have been removed and replaced by a single function *mjs_attach*.


### General

3.  `d05251af` Added [tendon armature](XMLreference.md): inertia associated with changes in tendon length.
4.  `f96f3e1c` Added the [compiler/saveinertial](XMLreference.md) flag, writing explicit inertial clauses for all bodies when saving to XML.
5.  `e8c67ca5` Added `quat` orientation attribute to `composite`. Moreover, allow the composite to be the direct child of a frame.
6.  `96dda6ea` Added [tendon actuator force limits](XMLreference.md) and [tendon actuator force sensor](XMLreference.md).

### MJX

7.  `8fc616bf` Added tendon actuator force limits.

### Bug fixes

8.  `de48f417` *mj_jacDot* was missing a term that accounts for the motion of the point with respect to which the Jacobian is computed, now fixed.
9.  `1bf24e9f` Fixed a bug that caused the parent frame of elements in the child worldbody to be incorrectly set when attaching an mjSpec to a frame or a site.
10. `40393f46` Fixed a bug that caused shadow rendering to flicker on platforms (e.g., MacOS) that do not support ARB_clip_control. Fixed in collaboration with `aftersomemath`.

### Python bindings


LbANnKMDOHg


11. `16e49f27` Added examples of procedural model creation to the Model Editing tutorial: [![mjspec_colab](https://colab.research.google.com/assets/colab-badge.png)](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/mjspec.ipynb)
12. `ebd30493` Added support for nameless [mjSpec](APIreference/APItypes.md) objects in the `bind` method, see the corresponding [section](python.md) in the documentation.

## Version 3.3.0 (Feb 26, 2025)

### Feature promotion


qJFbx-FR7Bc


1.  `7cdf1806` Introduced a new kind of **fast deformable body**, activated by setting [flexcomp/dof](XMLreference.md) to "trilinear". This type of [deformable](modeling.md) flex object has the same collision geometry as a regular flex, but has far fewer degrees of freedom. Instead of 3 dofs per vertex, only the corners of the bounding box are free to move, with the positions of the interior vertices computed with trilinear interpolation of the 8 corners, for a total of 24 dofs for the entire flex object (or less, if some of the corners are pinned). This limits the types of deformation achievable by the flex, but allows for much faster simulation. For example, see the video on the right comparing [full](https://github.com/google-deepmind/mujoco/blob/main/model/flex/gripper.xml) and [trilinear](https://github.com/google-deepmind/mujoco/blob/main/model/flex/gripper_trilinear.xml) flexes for modeling deformable gripper pads.

<img src="images/computation/ccd_light.gif" class="only-light only-lightalign-right" style="width:20.0%" alt="image" />

<img src="images/computation/ccd_dark.gif" class="only-dark only-darkalign-right" style="width:20.0%" alt="image" />

2.  `ed16f2da` The native convex collision detection pipeline introduced in 3.2.3 and enabled by the [nativeccd](XMLreference.md) flag, is now the default. See the section on [Convex Collision Detection](computation/index.md) for more details.

    **Migration:** If the new pipeline breaks your workflow, set [nativeccd](XMLreference.md) to "disable".

### General

3.  `37d7591c` Add support for custom plots in the MuJoCo viewer by exposing a `viewport` property, a `set_figures` method, and a `clear_figures` method.
4.  `7cdf1806` Separate collision and deformation meshes for [flex](XMLreference.md). This enables a fixed cost for the soft body computations, while preserving the fidelity of high-resolution collisions.
5.  `240a7afd` Added [potential](XMLreference.md) and [kinetic](XMLreference.md) energy sensors.
6.  `ac2a324f` Improved shadow rendering in the native renderer.
7.  `b0e9d086` Moved `introspect` to `python/introspect`.


Breaking API changes

8.  `ed16f2da` As mentioned above, the native convex collision detection pipeline is now the default, which may break some workflows. In this case, set [nativeccd](XMLreference.md) to "disable" to restore the old behavior.

9.  `c2138c3f` Added *mjs_setDeepCopy* API function. When the deep copy flag is 0, attaching a model will not copy it to the parent, so the original references to the child can be used to modify the parent after attachment. The default behavior is to perform such a shallow copy. The old behavior of creating a deep copy of the child model while attaching can be restored by setting the deep copy flag to 1.

10. `89253d95` Changes to inertia inference from meshes:

    Previously, in order to specify that the mass lies on the surface, [geom/shellinertia](XMLreference.md) could be used for any geom type. Now this attribute is ignored if the geom is a mesh; instead, inertia inference for meshes is specified in the asset, using the [asset/mesh/inertia](XMLreference.md) attribute.

    Previously, if the volumetric inertia computation failed (for example due to a very flat mesh), the compiler would silently fall back to surface inertia computation. Now, the compiler will throw an informative error.

11. `0fcd20f0` Removed the composite type `grid`. Users should instead use [flexcomp](XMLreference.md).

12. `c52d1b39` Removed the `particle` composite type. It is recommended to use the more generic [replicate](XMLreference.md) instead, see for example [this model](https://github.com/google-deepmind/mujoco/blob/main/model/replicate/particle.xml).


### MJX

13. `f4096bca` Added support for spatial tendons with internal sphere and cylinder wrapping.
14. `e0664b1b` Fix a bug with box-box collisions `2356`.

### Python bindings

15. `7a2ad8fd` Added a pedagogical colab notebook for `mujoco.rollout`, a Python module for multithreaded simulation rollouts. It is available here [![rollout_colab](https://colab.research.google.com/assets/colab-badge.png)](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/rollout.ipynb). <br/> Contribution by `aftersomemath`.

## Version 3.2.7 (Jan 14, 2025)

### Python bindings

1.  `a7eb6efd` [rollout](python.md) now features native multi-threading. If a sequence of `MjData` instances of length `nthread` is passed in, `rollout` will automatically create a thread pool and parallelize the computation. The thread pool can be reused across calls, but then the function cannot be called simultaneously from multiple threads. To run multiple threaded rollouts simultaneously, use the new class `Rollout` which encapsulates the thread pool. Contribution by `aftersomemath`.
2.  `40ef08c8` Fix global namespace pollution when using `mjpython` (`2265`).

### General


Breaking API changes (minor)

3.  `69c9ac07` The field `mjData.qLDiagSqrtInv` has been removed. This field is only required for the dual solvers. It is now computed as-needed rather than unconditionally. Relatedly, added the corresponding argument to *mj_solveM2*.


4.  `d4ca66a4` Reduced the memory footprint of the PGS solver's [A matrix](computation/index.md). This was the last remaining dense-memory allocation in MuJoCo, allowing for a significant reduction of the [dynamic memory allocation heuristic](modeling.md).

### Bug fixes

5.  `0e7d2ef6` Fixed a bug in the box-sphere collider, depth was incorrect for deep penetrations (`2206`).
6.  `ec322641` Fixed a bug in *mj_mulM2* and added a test.

## Version 3.2.6 (Dec 2, 2024)

### General

1.  `300450f8` Removed rope and loop from `composite`. The user is encouraged to instead use the <span class="at">cable</span> plugin or [flexcomp](XMLreference.md), respectively.

### MJX

2.  `0f381a9e` Added muscle actuators.

### Python bindings

3.  `74dcd51d` Provide prebuilt wheels for Python 3.13.
4.  `3a12db9a` Added `bind` method and removed id attribute from [mjSpec](APIreference/APItypes.md) objects. Using ids is error prone in scenarios of repeated attachment and detachment. Python users are encouraged to use names for unique identification of model elements.
5.  `943eb6bc` [rollout](python.md) can now accept sequences of MjModel of length `nroll`. Also removed the `nroll` argument because its value can always be inferred.

### Bug fixes

6.  `f9569cda` Fixed `2212`, type error in `mjx.get_data`.
7.  `5c23ae11` Fixed bug introduced in 3.2.0 in handling of [texrepeat](XMLreference.md) attribute, was mistakenly cast from `float` to `int`, (fixed `2223`).

## Version 3.2.5 (Nov 4, 2024)

### Feature promotion

1.  `b6037d17` The [Model Editing](programming/modeledit.md) framework afforded by [mjSpec](APIreference/APItypes.md), introduced in 3.2.0 as an in-development feature, is now stable and recommended for general use.
2.  `298ce31e` The native convex collision detection pipeline introduced in 3.2.3 and enabled by the [nativeccd](XMLreference.md) flag, is not yet the default but is already recommended for general use. Please try it when encountering collision-related problems and report any issues you encounter.

### General

3.  `b598d79b` The global compiler flag `exactmeshinertia` has been removed and replaced with the mesh-specific [inertia](XMLreference.md) attribute.
4.  `7dc8aef8` The not-useful `convexhull` compiler option (to disable computation of mesh convex hulls) has been removed.
5.  `d8494fef` Removed the deprecated `mju_rotVecMat`, `mju_rotVecMatT` and `mjv_makeConnector` functions.
6.  `2b0629d7` Sorting now uses a faster, native sort function (fixes `1638`).
7.  `61cb552f` The PBR texture layers introduced in 3.2.1 were refactored from separate sub-elements to a single [layer](XMLreference.md) sub-element.
8.  `831d9881` The composite types box, cylinder, and sphere have been removed. Users should instead use the equivalent types available in [flexcomp](XMLreference.md).

### MJX

9.  `680fb3e5` Added `apply_ft`, `jac`, and `xfrc_accumulate` as public functions.
10. `b00a7c67` Added `TOUCH` sensor.
11. `f24de91c` Added support for `eq_active`. Fixes `2173`.
12. `3c21abc0` Added ray intersection with ellipsoid.

### Bug fixes

13. `864b805a` Fixed several bugs related to connect and weld constraints with site semantics (fixes `2179`, reported by `yinfanyi`). The introduction of site specification to connects and welds in 3.2.3 conditionally changed the semantics of <span class="title-ref">mjData.eq_obj1id</span> and <span class="title-ref">mjData.eq_obj2id</span>, but these changes were not properly propagated in several places leading to incorrect computations of constraint inertia, readings of affected force/torque sensors and runtime enabling/disabling of such constraints.
14. `7620aef5` Fixed a bug in slider-crank [transmission](computation/index.md). The bug was introduced in 3.0.0.
15. `831d9881` Fixed a bug in flex texture coordinates that prevented the correct allocation of textures in mjModel.

### Documentation

16. `1d58576d` Function headers in the *API reference* now link to their source definitions in GitHub.

## Version 3.2.4 (Oct 15, 2024)

### General


e8lUuykQPGs


1.  `2dd51873` The Newton solver no longer requires `nv*nv` memory allocation, allowing for much larger models. See e.g., [100_humanoids.xml](https://github.com/google-deepmind/mujoco/blob/main/model/humanoid/100_humanoids.xml). Two quadratic-memory allocations still remain to be fully sparsified: `mjData.actuator_moment` and the matrices used by the PGS solver.
2.  `4998e7b3` Removed the <span class="at">solid</span> and <span class="at">membrane</span> plugins and moved the associated computations into the engine. See [3D example model](https://github.com/google-deepmind/mujoco/blob/main/model/flex/floppy.xml) and [2D example model](https://github.com/google-deepmind/mujoco/blob/main/model/flex/trampoline.xml) for examples of flex objects that previously required these plugins.
3.  `6832df30` Replaced the function `mjs_setActivePlugins` with *mjs_activatePlugin*.

### MJX

4.  `1a9d3070` Added `mocap_pos` and `mocap_quat` in kinematics.
5.  `160ed9bf` Added support for [spatial tendons](XMLreference.md) with pulleys and external sphere and cylinder wrapping.
6.  `fa22e6d0` Added sphere-cylinder and sphere-ellipsoid collision functions (`2126`).
7.  `22e4f7fc` Fixed a bug with frictionloss constraints.
8.  `ac91a763` Added `TENDONPOS` and `TENDONVEL` sensors.
9.  `19459263` Fixed a bug with the computation of tangential contact forces in `_decode_pyramid`.
10. `096853e1` Added `JOINTINPARENT` actuator transmission type.

### Python bindings

11. `6881ce24` Removed support for Python 3.8, now that it's [deprecated upstream](https://devguide.python.org/versions).

### Bug fixes

12. `ab3954d8` Fixed a bug where `actuator_force` was not set in MJX (`2068`).
13. `5838f847` Fixed bug where MJX data tendon fields were incorrect after calling `mjx.put_data`.
14. `8d84b5f6` The compiler now returns an error if height fields are used with [collision sensors](XMLreference.md) as they are not yet supported.

## Version 3.2.3 (Sep 16, 2024)

### General


Breaking API changes

1.  `088079ef` The runtime options `mpr_tolerance` and `mpr_iterations` were renamed to [ccd_tolerance](XMLreference.md) and [ccd_iterations](XMLreference.md), both in XML and in the [mjOption](APIreference/APItypes.md) struct. This is because the new convex collision detection pipeline (see below) does not use the MPR algorithm. The semantics of these options remain identical.
2.  `d3dfa6f9` The functions `mjs_findMesh` and `mjs_findKeyframe` were replaced by `mjs_findElement`, which allows to look for any object type.
3.  `4862b9e7` The experimental use of 2D/3D elasticity plugins with `composite` has been removed. Users should instead use [flexcomp](XMLreference.md), which provides the correct collision behavior.


4.  `0bffd744` Added the [nativeccd](XMLreference.md) flag. When this flag is enabled, general convex collision detection is handled with a new native code path, rather than [libccd](https://github.com/danfis/libccd). This feature is in early stages of testing, but users who've experienced issues related to collision detection are welcome to experiment with it and report any issues.


kcM_oauk3ZA


5.  `60a1921b` Added a new way of defining [connect](XMLreference.md) and [weld](XMLreference.md) equality constraints, using two sites. The new semantic is useful when the assumption that the constraint is satisfied in the base configuration does not hold. In this case the sites will "snap together" at the beginning of the simulation. Additionally, changing the site positions (`mjModel.site_pos`) and orientations ( `mjModel.site_quat`) at runtime will correctly modify the constraint definition. This [example model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/equality_site.xml) using the new semantic is shown in the video on the right.

6.  `8954a088` Introduced **free joint alignment**, an optimization that applies to bodies with a free joint and no child bodies (simple free-floating bodies): automatically aligning the body frame with the inertial frame. This feature can be toggled individually using the [freejoint/align](XMLreference.md) attribute or globally using the compiler [alignfree](XMLreference.md) attribute. The alignment diagonalizes the related 6x6 inertia sub-matrix, leading to both faster and more stable simulation of free bodies.

    While this optimization is a strict improvement, it changes the semantics of the joint's degrees-of-freedom. Therefore, `qpos` and `qvel` values saved in older versions (for example, in [keyframes](XMLreference.md)) will become invalid. The global compiler attribute currently defaults to "false" due to this potential breakage, but could be changed to "true" in a future release. Aligned free joints are recommended for all new models.

7.  `851bb6ee` Added an [mjSpec](APIreference/APItypes.md) option for creating a texture directly from a buffer.

8.  `466368ef` [shell (surface) inertia](XMLreference.md) is now supported by all geom types.

9.  `afd7c73f` When [attaching](programming/modeledit.md) sub-models, [keyframes](XMLreference.md) will now be correctly merged into the parent model, but only on the first attachment.

10. `8b03daa0` Added the [mjtSameFrame](APIreference/APItypes.md) enum which contains the possible frame alignments of bodies and their children. These alignments are used for computation shortcuts in *mj_kinematics*.

11. `2d3d5415` Added *mj_jacDot* for computing time-derivatives of kinematic Jacobians. Fixes `411`.

### MJX

12. `a74c184f` Added `efc_pos` to `mjx.Data` (`1388`).
13. `6a12787a` Added position-dependent sensors: `MAGNETOMETER`, `CAMPROJECTION`, `RANGEFINDER`, `JOINTPOS`, `ACTUATORPOS`, `BALLQUAT`, `FRAMEPOS`, `FRAMEXAXIS`, `FRAMEYAXIS`, `FRAMEZAXIS`, `FRAMEQUAT`, `SUBTREECOM`, `CLOCK`.
14. `9805df61` Added velocity-dependent sensors: `VELOCIMETER`, `GYRO`, `JOINTVEL`, `ACTUATORVEL`, `BALLANGVEL`, `FRAMELINVEL`, `FRAMEANGVEL`, `SUBTREELINVEL`, `SUBTREEANGMOM`.
15. `9d732117` Added acceleration/force-dependent sensors: `ACCELEROMETER`, `FORCE`, `TORQUE`, `ACTUATORFRC`, `JOINTACTFRC`, `FRAMELINACC`, `FRAMEANGACC`.
16. `390bce23` Changed default policy to avoid placing unused (MuJoCo-only) arrays on device.
17. `390bce23` Added `device` parameter to `mjx.make_data` to bring it to parity with `mjx.put_model` and `mjx.put_data`.
18. `a68141ee` Added support for [implicitfast integration](computation/index.md) for all cases except [fluid drag](computation/fluid.md).
19. `494e166f` Fixed a bug where `qLDiagInv` had the wrong size for sparse mass matrices.
20. `49711fa1` Added support for joint and tendon [frictionloss](computation/index.md).
21. `cd8ff440` Added support for [connect](XMLreference.md) equality constraints using two sites.
22. `e3d3a24b` Added support for [spatial tendons](XMLreference.md) with site wrapping.

### Bug fixes

23. `39896f80` Fixed a performance regression introduced in 3.1.7 in mesh Bounding Volume Hierarchies (`1875`, contribution by `michael-ahn`).
24. `0bcaa856` Fixed a bug wherein, for models that have both muscles and stateless actuators and used one of the implicit integrators, wrong derivatives would be computed.
25. `3e701b21` Fixed a bug in tendon wrapping around spheres. Before this fix, tendons that wrapped around spheres with an externally-placed [sidesite](XMLreference.md) could jump inside the sphere instead of wrapping around it.
26. `567793c2` Fixed a bug that caused <span class="at">meshdir</span> and <span class="at">texturedir</span> to be overwritten during model [attachment](programming/modeledit.md), preventing model attachment for models with assets in different directories.

### Python bindings

27. `cfc7dc98` Added support for engine plugins in [mjSpec](APIreference/APItypes.md) (`1903`).
28. `9a27fc14` Better error reporting for issues with the assets dictionary, when loading models.

## Version 3.2.2 (Aug 8, 2024)

### General

1.  `9db9df73` Increase texture and material limit back to 1000. 3.2.0 inadvertently reduced this limit to 100, breaking some existing models (`1877`).

## Version 3.2.1 (Aug 5, 2024)

### General

1.  `e92af73c` Renamed `mjModel.tex_rgb` to `mjModel.tex_data`.
2.  `24a55506` Added a new [autoreset](XMLreference.md) flag to disable automatic reset when NaNs or infinities are detected.
3.  `33e59606` Added sub-elements to the MJCF [material](XMLreference.md) element, to allow specification of multiple textures for rendering (e.g., `occlusion, roughness, metallic`). Note that the MuJoCo renderer doesn't support these new features, and they are made available for use with external renderers.
4.  `82c27165` Sorting (`mjQUICKSORT`) now calls `std::sort` when building with C++ (`1638`).

### MJX

5.  `dbe18f57` Added more fields to `mjx.Model` and `mjx.Data` for further compatibility with the corresponding MuJoCo structs.
6.  `2d24c588` Added support for [fixed tendons](XMLreference.md).
7.  `2d24c588` Added support for tendon length limits (`mjCNSTR_LIMIT_TENDON` in [mjtConstraint](APIreference/APItypes.md)).
8.  `2d24c588` Added support for tendon equality constraints (`mjEQ_TENDON` in [mjtEq](APIreference/APItypes.md)).
9.  `2d24c588` Added support for tendon actuator transmission (`mjTRN_TENDON` in [mjtTrn](APIreference/APItypes.md)).

### Python bindings

10. `70ac76bb` Added support for asset dictionary argument in `mujoco.spec.from_file`, `mujoco.spec.from_string` and `mujoco.spec.compile`.

### Bug fixes

11. `a4bd2bec` Fixed a bug where implicit integrators did not take into account disabled actuators (`1838`).

## Version 3.2.0 (Jul 15, 2024)

### New features

1.  `e13ddfa2` Introduced a major new feature: **procedural model creation and editing**, using a new top-level data-structure [mjSpec](APIreference/APItypes.md). See the [Model Editing](programming/modeledit.md) chapter for details. Note that as of this release this feature is still in testing and subject to future breaking changes. Fixes `364`.

### General


Breaking API changes

2.  `e66b9a36` Removed deprecated `mj_makeEmptyFileVFS` and `mj_findFileVFS` functions. The constants `mjMAXVFS` and `mjMAXVFSNAME` are also removed as they are no longer needed.

    **Migration:** Use *mj_addBufferVFS* to copy a buffer into a VFS file directly.

3.  `57e6760e` Calls to *mj_defaultVFS* may allocate memory inside VFS, and the corresponding *mj_deleteVFS* must be called to deallocate any internal allocated memory.

4.  `60670485` Deprecated `mju_rotVecMat` and `mju_rotVecMatT` in favor of *mju_mulMatVec3* and *mju_mulMatTVec3*. These function names and argument order are more consistent with the rest of the API. The older functions have been removed from the Python bindings and will be removed from the C API in the next release.

5.  `393895bb` Removed the `actuator_actdim` callback from actuator plugins. They now have the `actdim` attribute, which must be used with actuators that write state to the `act` array. This fixed a crash which happened when keyframes were used in a model with stateful actuator plugins. The PID plugin will give an error when the wrong value of actdim is provided.


6.  `27b9ddda` Added [attach](XMLreference.md) meta-element to MJCF, which allows [attaching](programming/modeledit.md) a subtree from a different model to a body in the current model.
7.  `57e6760e` The *VFS* implementation has been rewritten in C++ and is now considerably more efficient in speed and memory footprint.


ZXBTEIDWHhs


8.  `07fc95ca` Added support for orthographic cameras. This is available for both fixed cameras and the free camera, using the `camera/orthographic` and [global/orthographic](XMLreference.md) attributes, respectively.

9.  `ace0c8f0` Added [maxhullvert](XMLreference.md), the maximum number of vertices in a mesh's convex hull.

10. `c9bcf837` Added *mj_setKeyframe* for saving the current state into a model keyframe.

11. `5ed464b4` Added support for `ball` joints in the URDF parser ("spherical" in URDF).

12. `3f3b39bb` Replaced `mjUSEDOUBLE` which was previously hard-coded in [mjtnum.h](https://github.com/google-deepmind/mujoco/blob/3577e2cf8bf841475b489aefff52276a39f24d51/include/mjtnum.h) with the build-time flag `mjUSESINGLE`. If this symbol is not defined, MuJoCo will use double-precision floating point, as usual. If `mjUSESINGLE` is defined, MuJoCo will use single-precision floating point. See [mjtNum](APIreference/APItypes.md).

    Relatedly, fixed various type errors that prevented building with single-precision.

13. `22a10fd2` Quaternions in `mjData.qpos` and `mjData.mocap_quat` are no longer normalized in-place by *mj_kinematics*. Instead they are normalized when they are used. After the first step, quaternions in `mjData.qpos` will be normalized.

14. `3d1d1d07` Mesh loading in the compiler, which is usually the slowest part of the loading process, is now multi-threaded.

#### MJX

15. `4c3d9461` Added support for [elliptic friction cones](XMLreference.md).
16. `4c3d9461` Fixed a bug that resulted in less-optimal linesearch solutions for some difficult constraint settings.
17. `4c3d9461` Fixed a bug in the Newton solver that sometimes resulted in less-optimal gradients.


P83tKA1iz2Y


### Simulate

18. `1eb70864` Added improved tutorial video.
19. `f37f8408` Improved the Brownian noise generator.
20. `3d1d1d07` Now displaying model load times if they are longer than 0.25 seconds.

### Python bindings

21. `2188cba4` Fixed a memory leak when using `copy.deepcopy()` on a `mujoco.MjData` instance (`1572`).

### Bug fixes

22. `e7301edd` Fix an issue where `mj_copyData` (or `copy.copy()` in the Python bindings) was not copying contact information correctly (`1710`).
23. `8e827d0d` Fix an issue with saving to XML that caused frames to be written multiple times (`1802`).

## Version 3.1.6 (Jun 3, 2024)

### General

1.  `02d01545` Added *mj_geomDistance* for computing the shortest signed distance between two geoms and optionally a segment connecting them. Relatedly, added the 3 sensors: [distance](XMLreference.md), [normal](XMLreference.md), [fromto](XMLreference.md). See the function and sensor documentation for details. Fixes `51`.
2.  `2830a407` Improvements to position actuators:
    - Added [timeconst](XMLreference.md) attribute to the [position actuator](XMLreference.md). When set to a positive value, the actuator is made stateful with <span class="at">filterexact</span> dynamics.
    - Added [dampratio](XMLreference.md) to both <span class="el">position</span> and <span class="el">intvelocity</span> actuators. An alternative to the <span class="at">kv</span> attribute, it provides a convenient way to set actuator damping using natural units. See attribute documentation for details.

### MJX

3.  `c511d022` Add height-field collision support. Fixes `1491`.
4.  `c511d022` Add a pre-compiled field `mesh_convex` to `mjx.Model` so that mesh properties can be vmapped over. Fixes `1655`.
5.  `c511d022` Fix a bug in convex mesh collisions, where erroneous edge contacts were being created even though face separating axes were found. Fixes `1695`.

### Bug fixes

6.  `96844db9` Fixed a bug the could cause collisions to be missed when [fusestatic](XMLreference.md) is enabled, as is often the case for URDF imports. Fixes `1069`, `1577`.
7.  `1d181786` Fixed a bug that was causing the visualization of SDF iterations to write outside the size of the vector storing them. Fixes `1539`.

## Version 3.1.5 (May 7, 2024)

### General


5k0_wsIRAFc


1.  `26f23066` Added the [replicate](XMLreference.md) to MJCF, a [meta-element](XMLreference.md) which permits to repeat a subtree with incremental translational and rotational offsets.
2.  `ad045968` Enabled an internal cache in the MuJoCo compiler resulting in recompilation speedup. Currently, processed textures, hfields, and OBJ meshes are cached. Support for Unity environments is not yet available.
3.  `6481a838` Added `mjModel.mesh_scale`: the scaling applied to asset vertices, as specified in the [scale](XMLreference.md) attribute.
4.  `caf215e3` Added visual properties which are ignored by the native renderer, but can be used by external renderers:
    - [light/bulbradius](XMLreference.md) attribute and corresponding `mjModel.light_bulbradius` field.
    - [material/metallic](XMLreference.md) attribute and corresponding `mjModel.material_metallic` field.
    - [material/roughness](XMLreference.md) attribute and corresponding `mjModel.material_roughness` field.
5.  `546a27ca` The type of the `size` argument of *mj_stackAllocNum* and *mj_stackAllocInt* was changed from `int` to `size_t`.
6.  `131b1745` Added support for gmsh format version 2.2 surface meshes in [flexcomp](XMLreference.md).

### MJX


Breaking API changes

7.  `718e079c` Removed deprecated `mjx.device_get_into` and `mjx.device_put` functions as they lack critical new functionality.

    **Migration:** Use `mjx.get_data_into` instead of `mjx.device_get_into`, and `mjx.put_data` instead of `mjx.device_put`.


8.  `0cd28d24` Added cylinder plane collisions.
9.  `71333938` Added `efc_type` to `mjx.Data` and `dim`, `efc_address` to `mjx.Contact`.
10. `71333938` Added `geom` to `mjx.Contact` and marked `geom1`, `geom2` deprecated.
11. `3b64217b` Added `ne`, `nf`, `nl`, `nefc`, and `ncon` to `mjx.Data` to match `mujoco.MjData`.
12. `a4df9120` Given the above added fields, removed `mjx.get_params`, `mjx.ncon`, and `mjx.count_constraints`.
13. `a4df9120` Changed the way meshes are organized on device to speed up collision detection when a mesh is replicated for many geoms.
14. `a4df9120` Fixed a bug where capsules might be ignored in broadphase colliision checking.
15. `c2d0c5dd` Added cylinder collisions using SDFs.
16. `71333938` Added support for all [condim](computation/index.md): 1, 3, 4, 6.
17. `d15db545` Add support functions for `id2name` and `name2id`, MJX versions of *mj_id2name* and *mj_name2id*.
18. `e9709900` Added support for [gravcomp](XMLreference.md) and [actuatorgravcomp](XMLreference.md).
19. `719476c2` Fixed a bug in `mjx.ray` for sometimes allowed negative distances for ray-mesh tests.
20. `24bc1c8b` Added a new [differentiable physics tutorial](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/mjx/training_apg.ipynb) that demonstrates training locomotion policies with analytical gradients automatically derived from the MJX physics step. Contribution by `Andrew-Luo1`.

### Bug fixes

21. `0cd28d24` Defaults of lights were not being saved, now fixed.
22. `4b6c07cd` Prevent overwriting of frame names by body names when saving an XML. Bug introduced in 3.1.4.
23. `2b497581` Fixed bug in Python binding of *mj_saveModel*: `buffer` argument was documented as optional but was actually not optional.
24. `546a27ca` Fixed bug that prevented memory allocations larger than 2.15 GB. Fixes `1606`.

## Version 3.1.4 (April 10th, 2024)

### General


Breaking API changes

1.  `5d26b50f` Removed the ability to natively add noise to sensors. Note that the `mjModel.sensor_noise` field and [corresponding attribute](modeling.md) are kept and now function as a convenient location for the user to save standard-deviation information for their own use. This feature was removed because:

    - There was no mechanism to seed the random noise generator.
    - It was not thread-safe, even if seeding would have been provided, sampling on multiple threads would lead to non-reproducible results.
    - This feature was seen as overreach by the engine. Adding noise should be the user's responsibility.
    - We are not aware of anyone who was actually using the feature.

    **Migration:** Add noise to sensor values yourself.


2.  `47ba72ea` Added the [actuatorgravcomp](XMLreference.md) joint attribute. When enabled, gravity compensation forces on the joint are treated as applied by actuators. See attribute documentation for more details. The example model [refsite.xml](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/actuation/refsite.xml), which demonstrates Cartesian actuation of an arm, has been updated to use this attribute.
3.  `4f0293c6` Added support for gmsh format 2.2 , tetrahedral mesh, as generated by e.g. [fTetwild](https://github.com/wildmeshing/fTetWild).
4.  `5a365603` Added *mju_euler2Quat* for converting an Euler-angle sequence to quaternion.

### MJX

5.  `22cd96fb` Improved performance of SAT for convex collisions.
6.  `f2e107f7` Fixed bug for sphere/capsule-convex deep penetration.
7.  `02c62c11` Fixed bug where `mjx.Data` produced by `mjx.put_data` had different treedef than `mjx.make_data`.
8.  `2386353b` Throw an error for margin/gap for convex mesh collisions, since they are not supported.
9.  `2b3f336b` Added ellipsoid plane collisions.
10. `b4419235` Added support for userdata.
11. `2b3f336b` Added ellipsoid-ellipsoid and ellipsoid-capsule collisions using signed distance functions (SDFs).

### Simulate

12. `bb42ff16` Fixed bug in order of enable flag strings. Before this change, using the simulate UI to toggle the [invdiscrete](XMLreference.md) or the (now removed) `sensornoise` flags would actually toggle the other flag.

### Python bindings


xHDS0n5DpqM


13. `adc4b92c` Added the `mujoco.minimize` Python module for nonlinear least-squares, designed for System Identification (sysID). The sysID tutorial is work in progress, but a pedagogical colab notebook with examples, including Inverse Kinematics, is available here: [![ls_colab](https://colab.research.google.com/assets/colab-badge.png)](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/least_squares.ipynb) <br/> The video on the right shows example clips from the tutorial.

## Version 3.1.3 (March 5th, 2024)

### General

1.  `05150546` Added the <span class="at">inheritrange</span> attribute to [position](XMLreference.md) and [intvelocity](XMLreference.md) actuators, allowing convenient setting of the actuator's <span class="at">ctrlrange</span> or <span class="at">actrange</span> (respectively), according to the range of the transmission target (joint or tendon). See [position/inheritrange](XMLreference.md) for details.
2.  `a4a621f6` Deprecated `mj_makeEmptyFileVFS` in favor of *mj_addBufferVFS*. [mjVFS](APIreference/APItypes.md) now computes checksums of its internal file buffers. *mj_addBufferVFS* allocates an empty buffer with a given name in an mjVFS and copies the data buffer into it, combining and replacing the deprecated two-step process of calling `mj_makeEmptyFileVFS` followed by a direct copy into the given mjVFS internal file buffer.
3.  `6b7d7142` Added *mj_angmomMat* which computes the `3 x nv` angular momentum matrix $`H(q)`$, providing the linear mapping from generalized velocities to subtree angular momentum $`h = H \dot q`$. Contribution by `v-r-a`.

### MJX

4.  `4933a2c7` Improved performance of getting and putting device data.
    - Use `tobytes()` for numpy array serialization, which is orders of magnitude faster than converting to tuples.
    - Avoid reallocating host `mjData` arrays when array shapes are unchanged.
    - Speed up calculation of `mjx.ncon` for models with many geoms.
    - Avoid calling `mjx.ncon` in `mjx.get_data_into` when `nc` can be derived from `mjx.Data`.
5.  `e77c3cb2` Fixed a bug in `mjx-viewer` that prevented it from running. Updated `mjx-viewer` to use newer `mjx.get_data_into` function call.
6.  `47bb4a82` Fixed a bug in `mjx.euler` that applied incorrect damping when using dense mass matrices.
7.  `47bb4a82` Fixed a bug in `mjx.solve` that was causing slow convergence when using `mjSOL_NEWTON` in [mjtSolver](APIreference/APItypes.md).
8.  `6a346c42` Added support for [mjOption.impratio](APIreference/APItypes.md) to `mjx.Model`.
9.  `2067e208` Added support for cameras in `mjx.Model` and `mjx.Data`. Fixes `1422`.
10. `419be4c6` Added an implementation of broadphase using <span class="title-ref">top_k</span> and bounding spheres.

### Python bindings

11. `abf6d41b` Fixed incorrect data types in the bindings for the `geom`, `vert`, `elem`, and `flex` array members of the `mjContact` struct, and all array members of the `mjrContext` struct.

## Version 3.1.2 (February 05, 2024)

### General

1.  `e0864ab7` Improved the [discardvisual](XMLreference.md) compiler flag, which now discards all visual-only assets. See [discardvisual](XMLreference.md) for details.
2.  `2feefbc5` Removed the [timer](APIreference/APItypes.md) for midphase colllision detection, it is now folded in with the narrowphase timer. This is because timing the two phases separately required fine-grained timers inside the collision functions; these functions are so small and fast that the timer itself was incurring a measurable cost.
3.  `fea7c10b` Added the flag [bvactive](XMLreference.md) to `visual/global`, allowing users to turn off visualisation of active bounding volumes (the red/green boxes in this [this changelog item](changelog.md)). For models with very high-resolution meshes, the computation required for this visualization can slow down simulation speed. Fixes `1279`.
    - Added color of [bounding volumes](XMLreference.md) and [active bounding volumes](XMLreference.md) to [visual/rgba](XMLreference.md).
4.  `e143b3db` Height-field elevation data can now be specified directly in XML with the [elevation](XMLreference.md) attribute (and not only with PNG files). See [example model](https://github.com/google-deepmind/mujoco/blob/main/test/user/testdata/hfield_xml.xml).

### MJX

5.  `80f50c94` Added [dyntype](XMLreference.md) `filterexact`.
6.  `8ce2c920` Added <span class="at">site</span> transmission.
7.  `feb92bf5` Updated MJX colab tutorial with more stable quadruped environment.
8.  `a02fc405` Added `mjx.ray` which mirrors *mj_ray* for planes, spheres, capsules, boxes, and meshes.
9.  `0a7be173` Added `mjx.is_sparse` which mirrors *mj_isSparse* and `mjx.full_m` which mirrors *mj_fullM*.
10. `0a7be173` Added support for specifying sparse or dense mass matrices via <span class="title-ref">:el-prefix:\`option/</span> ⁠ **flag** `dot` \<XMLreference.md\>\`\_\_.
11. `508669a9` Raise a not implemented error when nonzero frictionloss is present. Fixes `1344`.

### Python bindings

12. `aceb52bd` Improved the implementation of the [rollout](python.md) module. Note the changes below are breaking, dependent code will require modification.
    - Uses [mjSTATE_FULLPHYSICS](programming/simulation.md) as state spec, enabling divergence detection by inspecting time.
    - Allows user-defined control spec for any combination of [user input](programming/simulation.md) fields as controls.
    - Outputs are no longer squeezed and always have dim=3.
13. `7bb0ce42` The `sync` function for the [passive viewer](python.md) can now pick up changes to rendering flags in `user_scn`, as requested in `1190`.

### Bug fixes

14. `1e2e0b30` Fixed a bug that prevented the use of pins with plugins if flexes are not in the worldbody. Fixes `1270`.
15. `a14a584f` Fixed a bug in the [muscle model](modeling.md) that led to non-zero values outside the lower bound of the length range. Fixes `1342`.

## Version 3.1.1 (December 18, 2023)

### Bug fixes

1.  `d39ed1d3` Fixed a bug (introduced in 3.1.0) where box-box collisions produced no contacts if one box was deeply embedded in the other.
2.  `dc0d0c59` Fixed a bug in [simulate](programming/samples.md) where the "LOADING..." message was not showing correctly.
3.  `d39ed1d3` Fixed a crash in the Python [passive viewer](python.md), when used with models containing Flex objects.
4.  `0915d69c` Fixed a bug in MJX where `site_xmat` was ignored in `get_data` and `put_data`
5.  `d39ed1d3` Fixed a bug in MJX where `efc_address` was sometimes incorrectly calculated in `get_data`.

## Version 3.1.0 (December 12, 2023)

### General

1.  `8ca51b53` Improved convergence of Signed Distance Function (SDF) collisions by using line search and a new objective function for the optimization. This allows to decrease the number of initial points needed for finding the contacts and is more robust for very small or large geom sizes.
2.  `eb9568a4` Added [frame](XMLreference.md) to MJCF, a [meta-element](XMLreference.md) which defines a pure coordinate transformation on its direct children, without requiring a [body](XMLreference.md).
3.  `762371c3` Added the <span class="at">kv</span> attribute to the [position](XMLreference.md) and [intvelocity](XMLreference.md) actuators, for specifying actuator-applied damping. This can be used to implement a PD controller with 0 reference velocity. When using this attribute, it is recommended to use the implicitfast or implicit [integrators](computation/index.md).

### Plugins

4.  `f2025c6a` Allow actuator plugins to use activation variables in `mjData.act` as their internal state, rather than `mjData.plugin_state`. Actuator plugins can now specify [callbacks](APIreference/APItypes.md) that compute activation variables, and they can be used with built-in [dyntype](XMLreference.md) actuator dynamics.
5.  `ca046cbf` Added the [pid](https://github.com/deepmind/mujoco/blob/main/plugin/actuator/README.md) actuator plugin, a configurable PID controller that implements the Integral term, which is not available with native MuJoCo actuators.

### MJX

6.  `35c90844` Added `site_xpos` and `site_xmat` to MJX.
7.  `67fa7c1d` Added `put_data`, `put_model`, `get_data` to replace `device_put` and `device_get_into`, which will be deprecated. These new functions correctly translate fields that are the result of intermediate calculations such as `efc_J`.

### Bug fixes

8.  `cd56a41f` Fix bug in Cartesian actuation with movable refsite, as when using body-centric Cartesian actuators on a quadruped. Before this fix such actuators could lead to non-conservation of momentum.
9.  `cd56a41f` Fix bug that prevented using flex with [simulate](programming/samples.md).
10. `7d8d4d39` Fix bug that prevented the use of elasticity plugins in combination with pinned flex vertices.
11. `3c05f9fa` Release Python wheels targeting macOS 10.16 to support x86_64 systems where `SYSTEM_VERSION_COMPAT` is set. The minimum supported version is still 11.0, but we release these wheels to fix compatibility for those users. See `1213`.
12. `49ddb7ca` Fixed mass computation of meshes: Use the correct mesh volume instead of approximating it using the inertia box.

## Version 3.0.1 (November 15, 2023)

### General

1.  `a89412bb` Added sub-terms of total passive forces in `mjData.qfrc_passive` to [mjData](APIreference/APItypes.md): `qfrc_{spring, damper, gravcomp, fluid}`. The sum of these vectors equals `qfrc_passive`.


H9qG9Zf2W44


2.  `893c4042` Added [actuatorgroupdisable](XMLreference.md) attribute and associated [mjOption.disableactuator](APIreference/APItypes.md) integer bitfield, which can be used to disable sets of actuators at runtime according to their [group](XMLreference.md). Fixes `1092`. See [Group disable](modeling.md).
    - The first 6 actuator groups are toggleable in the [simulate](programming/samples.md) viewer. See [example model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/actuation/actuator_group_disable.xml) and associated screen-capture on the right.
3.  `7e419276` Increased `mjMAXUIITEM` (maximum number of UI elements per section in Simulate) to 200.

### MJX

4.  `3c0a56c1` Added support for Newton solver (`mjSOL_NEWTON` in [mjtSolver](APIreference/APItypes.md)). The Newton solver significantly speeds up simulation on GPU:

    | Model | CG | Newton | Speedup |
    |----|----|----|----|
    | [Humanoid](https://github.com/google-deepmind/mujoco/tree/56006355b29424658b56aedb48a4269bd4361c68/mjx/mujoco/mjx/benchmark/model/humanoid) | 640,000 | 1,020,000 | **1.6 x** |
    | [Barkour v0](https://github.com/google-deepmind/mujoco/tree/56006355b29424658b56aedb48a4269bd4361c68/mjx/mujoco/mjx/benchmark/model/barkour_v0) | 1,290,000 | 1,750,000 | **1.35 x** |
    | [Shadow Hand](https://github.com/google-deepmind/mujoco/tree/56006355b29424658b56aedb48a4269bd4361c68/mjx/mujoco/mjx/benchmark/model/shadow_hand) | 215,000 | 270,000 | **1.25 x** |

    Steps-per-second, Conjugate Gradient vs. Newton on A100

    Humanoid is the standard MuJoCo humanoid, [Google Barkour](https://blog.research.google/2023/05/barkour-benchmarking-animal-level.html) and the Shadow Hand are both available in the [MuJoCo Menagerie](models.md).

5.  `70699765` Added support for joint equality constraints (`mjEQ_JOINT` in [mjtEq](APIreference/APItypes.md)).

6.  `f6ed57e9` Fixed bug where mixed `jnt_limited` joints were not being constrained correctly.

7.  `e4a9f535` Made `device_put` type validation more verbose (fixes `1113`).

8.  `843360b7` Removed empty EFC rows from `MJX`, for joints with no limits (fixes `1117`).

9.  `c8146372` Fixed bug in `scan.body_tree` that led to incorrect smooth dynamics for some kinematic tree layouts.

### Python bindings

10. `4c24be9e` Fix the macOS `mjpython` launcher to work with the Python interpreter from Apple Command Line Tools.
11. `084facc9` Fixed a crash when copying instances of `mujoco.MjData` for models that use plugins. Introduced a `model` attribute to `MjData` which is reference to the model that was used to create that `MjData` instance.

### Simulate

12. `f6ed57e9` [simulate](programming/samples.md): correct handling of "Pause update", "Fullscreen" and "VSync" buttons.

### Documentation


cE3s_IfO4g4


13. `8d5966ee` Added cell to the [tutorial colab](https://github.com/google-deepmind/mujoco#getting-started) providing an example of procedural camera control:
14. `2bb8652b` Added documentation for the [User Interface](programming/ui.md) framework.
15. `dc8bac2f` Fixed typos and supported fields in docs (fixes `1105` and `1106`).

### Bug fixes

16. `86d9c84e` Fixed bug relating to welds modified with [torquescale](XMLreference.md).

## Version 3.0.0 (October 18, 2023)

### New features

1.  `8f9c690c` Added simulation on GPU and TPU via the new [MuJoCo XLA (MJX)](mjx.md) (MJX) Python module. Python users can now natively run MuJoCo simulations at millions of steps per second on Google TPU or their own accelerator hardware.
    - MJX is designed to work with on-device reinforcement learning algorithms. This Colab notebook demonstrates using MJX along with reinforcement learning to train humanoid and quadruped robots to locomote: [![colab](https://colab.research.google.com/assets/colab-badge.png)](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/mjx/tutorial.ipynb)
    - The MJX API is compatible with MuJoCo but is missing some features in this release. See the outline of [MJX feature parity](mjx.md) for more details.


QewlEqIZi1o


2.  `fdb04158` Added new signed distance field (SDF) collision primitive. SDFs can take any shape and are not constrained to be convex. Collision points are found by minimizing the maximum of the two colliding SDFs via gradient descent.
    - Added new SDF plugin for defining implicit geometries. The plugin must define methods computing an SDF and its gradient at query points. See the [documentation](programming/extension.md) for more details.


ra2bTiZHGlw


3.  `139a8ae2` Added new low-level model element called `flex`, used to define deformable objects. These [simplicial complexes](https://en.wikipedia.org/wiki/Simplicial_complex) can be of dimension 1, 2 or 3, corresponding to stretchable lines, triangles or tetrahedra. Two new MJCF elements are used to define flexes. The top-level [deformable](XMLreference.md) section contains the low-level flex definition. The [flexcomp](XMLreference.md) element, similar to `composite` is a convenience macro for creating deformables, and supports the GMSH tetrahedral file format.

    - Added [shell](https://github.com/google-deepmind/mujoco/blob/45fc15b8447b56d3e6f12d3a158e2bc0d4d30dc8/plugin/elasticity/shell.cc) passive force plugin, computing bending forces using a constant precomputed Hessian (cotangent operator).

    **Note**: This feature is still under development and subject to change. In particular, deformable object functionality is currently available both via [deformable](modeling.md) and `composite`, and both are modifiable by the first-party [elasticity plugins](https://github.com/google-deepmind/mujoco/tree/45fc15b8447b56d3e6f12d3a158e2bc0d4d30dc8/plugin/elasticity). We expect some of this functionality to be unified in the future.


Vc1tq0fFvQA


4.  `3e034e38` Added constraint island discovery with *mj_island*. Constraint islands are disjoint sets of constraints and degrees-of-freedom that do not interact. The only solver which currently supports islands is [CG](XMLreference.md). Island discovery can be activated using a new [enable flag](XMLreference.md). If island discovery is enabled, geoms, contacts and tendons will be colored according to the corresponding island, see video. Island discovery is currently disabled for models that have deformable objects (see previous item).

5.  `62251869` Added `mjThreadPool` and `mjTask` which allow for multi-threaded operations within the MuJoCo engine pipeline. If engine-internal threading is enabled, the following operations will be multi-threaded:

    - Island constraint resolution, if island discovery is [enabled](XMLreference.md) and the [CG solver](XMLreference.md) is selected. The [22 humanoids](https://github.com/deepmind/mujoco/blob/main/model/humanoid/22_humanoids.xml) model shows a 3x speedup compared to the single threaded simulation.
    - Inertia-related computations and collision detection will happen in parallel.

    Engine-internal threading is a work in progress and currently only available in first-party code via the [testspeed](programming/samples.md) utility, exposed with the `npoolthread` flag.

6.  `139a8ae2` Added capability to initialize `composite` particles from OBJ files. Fixes `642` and `674`.

### General


Breaking API changes

7.  `ba66bd4f` Removed the macros `mjMARKSTACK` and `mjFREESTACK`.

    **Migration:** These macros have been replaced by new functions *mj_markStack* and *mj_freeStack*. These functions manage the [mjData stack](programming/simulation.md) in a fully encapsulated way (i.e., without introducing a local variable at the call site).

8.  `9902b735` Renamed `mj_stackAlloc` to *mj_stackAllocNum*. The new function *mj_stackAllocByte* allocates an arbitrary number of bytes and has an additional argument for specifying the alignment of the returned pointer.

    **Migration:** The functionality for allocating `mjtNum` arrays is now available via *mj_stackAllocNum*.

9.  `49290772` Renamed the `nstack` field in [mjModel](APIreference/APItypes.md) and [mjData](APIreference/APItypes.md) to `narena`. Changed `narena`, `pstack`, and `maxuse_stack` to count number of bytes rather than number of [mjtNum](APIreference/APItypes.md) ⁠ s.

10. `86d8b912` Changed [mjData.solver](APIreference/APItypes.md), the array used to collect solver diagnostic information. This array of [mjSolverStat](APIreference/APItypes.md) structs is now of length `mjNISLAND * mjNSOLVER`, interpreted as as a matrix. Each row of length `mjNSOLVER` contains separate solver statistics for each constraint island. If the solver does not use islands, only row 0 is filled.

    - The new constant [mjNISLAND](APIreference/APIglobals.md) was set to 20.
    - [mjNSOLVER](APIreference/APIglobals.md) was reduced from 1000 to 200.
    - Added [mjData.solver_nisland](APIreference/APItypes.md): the number of islands for which the solver ran.
    - Renamed `mjData.solver_iter` to `solver_niter`. Both this member and `mjData.solver_nnz` are now integer vectors of length `mjNISLAND`.

11. `9cf1f6eb` Removed `mjOption.collision` and the associated `option/collision` attribute.

    **Migration:**

    - For models which have `<option collision="all"/>`, delete the attribute.
    - For models which have `<option collision="dynamic"/>`, delete all [pair](XMLreference.md) elements.
    - For models which have `<option collision="predefined"/>`, disable all dynamic collisions (determined via contype/conaffinity) by first deleting all [contype](XMLreference.md) and [conaffinity](XMLreference.md) attributes in the model and then setting them globally to `0` using <br/> `<default> <geom contype="0" conaffinity="0"/> </default>`.

12. `d3d46e16` Removed the <span class="at">rope</span> and <span class="at">cloth</span> composite objects.

    **Migration:** Users should use the <span class="at">cable</span> and <span class="at">shell</span> elasticity plugins.

13. `ee78b8f7` Added [mjData.eq_active](APIreference/APItypes.md) user input variable, for enabling/disabling the state of equality constraints. Renamed `mjModel.eq_active` to [mjModel.eq_active0](APIreference/APItypes.md), which now has the semantic of "initial value of `mjData.eq_active`". Fixes `876`.

    **Migration:** Replace uses of `mjModel.eq_active` with `mjData.eq_active`.

14. `d88675a0` Changed the default of [autolimits](XMLreference.md) from "false" to "true". This is a minor breaking change. The potential breakage applies to models which have elements with "range" defined and "limited" not set. Such models cannot be loaded since version 2.2.2 (July 2022).


15. `2c3297b3` Added a new [dyntype](XMLreference.md), `filterexact`, which updates first-order filter states with the exact formula rather than with Euler integration.
16. `2c3297b3` Added an actuator attribute, [actearly](XMLreference.md), which uses semi-implicit integration for actuator forces: using the next step's actuator state to compute the current actuator forces.
17. `a276c49c` Renamed `actuatorforcerange` and `actuatorforcelimited`, introduced in the previous version to [actuatorfrcrange](XMLreference.md) and [actuatorfrclimited](XMLreference.md), respectively.
18. `b7cf479a` Added the flag [eulerdamp](XMLreference.md), which disables implicit integration of joint damping in the Euler integrator. See the [Numerical Integration](computation/index.md) section for more details.
19. `819b5cb9` Added the flag [invdiscrete](XMLreference.md), which enables discrete-time inverse dynamics for all [integrators](XMLreference.md) other than `RK4`. See the flag documentation for more details.
20. `1a3215e3` Added [ls_iterations](XMLreference.md) and [ls_tolerance](XMLreference.md) options for adjusting linesearch stopping criteria in CG and Newton solvers. These can be useful for performance tuning.
21. `ccda87aa` Added `mesh_pos` and `mesh_quat` fields to [mjModel](APIreference/APItypes.md) to store the normalizing transformation applied to mesh assets. Fixes `409`.
22. `8064ad59` Added camera [resolution](XMLreference.md) attribute and [camprojection](XMLreference.md) sensor. If camera resolution is set to positive values, the camera projection sensor will report the location of a target site, projected onto the camera image, in pixel coordinates.
23. `36d2ffe4` Added [camera](XMLreference.md) calibration attributes:
    - The new attributes are [resolution](XMLreference.md), [focal](XMLreference.md), [focalpixel](XMLreference.md), [principal](XMLreference.md), [principalpixel](XMLreference.md) and [sensorsize](XMLreference.md).
    - Visualize the calibrated frustum using the [mjVIS_CAMERA](APIreference/APItypes.md) visualization flag when these attributes are specified. See the following [example model](https://github.com/deepmind/mujoco/blob/main/test/engine/testdata/vis_visualize/frustum.xml).
    - Note that these attributes only take effect for offline rendering and do not affect interactive visualisation.
24. `59164702` Implemented reversed Z rendering for better depth precision. An enum [mjtDepthMap](APIreference/APItypes.md) was added with values `mjDEPTH_ZERONEAR` and `mjDEPTH_ZEROFAR`, which can be used to set the new `readDepthMap` attribute in [mjrContext](APIreference/APItypes.md) to control how the depth returned by *mjr_readPixels* is mapped from `znear` to `zfar`. Contribution `978` by [Levi Burner](https://github.com/aftersomemath).
25. `fb4cf472` Deleted the code sample `testxml`. The functionality provided by this utility is implemented in the [WriteReadCompare](https://github.com/google-deepmind/mujoco/blob/main/test/xml/xml_native_writer_test.cc) test.
26. `a1b6026b` Deleted the code sample `derivative`. Functionality provided by *mjd_transitionFD*.

### Python bindings

27. `631b16e7` Fixed `870` where calling `update_scene` with an invalid camera name used the default camera.
28. `2e15574b` Added `user_scn` to the [passive viewer](python.md) handle, which allows users to add custom visualization geoms (`1023`).
29. `a1d0cbd6` Added optional boolean keyword arguments `show_left_ui` and `show_right_ui` to the functions `viewer.launch` and `viewer.launch_passive`, which allow users to launch a viewer with UI panels hidden.

### Simulate


YSvWn_poqWs


30. `3e12f0d5` Added **state history** mechanism to [simulate](programming/samples.md) and the managed [Python viewer](python.md). State history can be viewed by scrubbing the History slider and (more precisely) with the left and right arrow keys. See screen capture:
31. `93d1c3c9` The `LOADING...` label is now shown correctly. Contribution `1070` by [Levi Burner](https://github.com/aftersomemath).

### Documentation


nljr0X79vI0


32. `18e4e101` Added [detailed documentation](computation/fluid.md) of fluid force modeling, and an illustrative example model showing [tumbling cards](https://github.com/google-deepmind/mujoco/blob/main/model/cards/cards.xml) using the ellipsoid-based fluid model.

### Bug fixes

33. `b0077e40` Fixed a bug that was causing [geom margin](XMLreference.md) to be ignored during the construction of midphase collision trees.
34. `1bd6c94e` Fixed a bug that was generating incorrect values in `efc_diagApprox` for weld equality constraints.

## Version 2.3.7 (July 20, 2023)

### General

1.  `a7021df6` Added primitive collider for sphere-cylinder contacts, previously this pair used the generic convex-convex collider.
2.  `51aa375a` Added [joint-actuatorforcerange](XMLreference.md) for clamping total actuator force at joints and [sensor-jointactuatorfrc](XMLreference.md) for measuring total actuation force applied at a joint. The most important use case for joint-level actuator force clamping is to ensure that [Cartesian actuator](XMLreference.md) forces are realizable by individual motors at the joints. See [Force limits](modeling.md) for details.
3.  `5fcdae77` Added an optional `content_type` attribute to hfield, texture, and mesh assets. This attribute supports a formatted [Media Type](https://www.iana.org/assignments/media-types/media-types.xhtml) (previously known as MIME type) string used to determine the type of the asset file without resorting to pulling the type from the file extension.
4.  `5cfbb6ac` Added analytic derivatives for quaternion *subtraction* and *integration* (rotation with an angular velocity). Derivatives are in the 3D tangent space.
5.  `c50c92cc` Added *mjv_connector* which has identical functionality to `mjv_makeConnector`, but with more convenient "from-to" argument parametrization. `mjv_makeConnector` is now deprecated.
6.  `242aea93` Bumped oldest supported MacOS from version 10.12 to 11. MacOS 11 is the oldest version still maintained by Apple.

### Python bindings

7.  `0ccfef73` The [passive viewer](python.md) handle now exposes `update_hfield`, `update_mesh`, and `update_texture` methods to allow users to update renderable assets. (Issues `812`, `958`, `965`).
8.  `06b70832` Allow a custom keyboard event callback to be specified in the [passive viewer](python.md) (`766`).
9.  `f7847ba7` Fix GLFW crash when Python exits while the passive viewer is running (`790`).

### Models

10. `51aa375a` Added simple [car](https://github.com/google-deepmind/mujoco/blob/main/model/car/car.xml) example model.

## Version 2.3.6 (June 20, 2023)

> [!NOTE]
> MuJoCo 2.3.6 is the last version to officially support Python 3.7.


ZppeDArq6AU


### Models

1.  `3d71b160` Added [3x3x3 cube](https://github.com/google-deepmind/mujoco/blob/main/model/cube/cube_3x3x3.xml) example model. See [README](https://github.com/google-deepmind/mujoco/blob/main/model/cube/README.md) for details.

### Bug fixes

2.  `41a70499` Fixed a bug that was causing an incorrect computation of the mesh bounding box and coordinate frame if the volume was invalid. In such case, now MuJoCo only accepts a non-watertight geometry if [shellinertia](XMLreference.md) is equal to `true`.
3.  `55c7f45d` Fixed the sparse Jacobian multiplication logic that is used to compute derivatives for tendon damping and fluid force, which affects the behaviour of the [implicit and implicitfast integrators](computation/index.md).
4.  `c66d7940` Fixes to *mj_ray*, in line with geom visualisation conventions:
    - Planes and height-fields respect the `geom_group` and `flg_static` arguments. Before this change, rays would intersect planes and height-fields unconditionally.
    - `flg_static` now applies to all static geoms, not just those which are direct children of the world body.


hqIMTNGaLF4


### Plugins

5.  `b397b312` Added touch-grid sensor plugin. See [documentation](https://github.com/google-deepmind/mujoco/blob/main/plugin/sensor/README.md) for details, and associated [touch_grid.xml](https://github.com/google-deepmind/mujoco/blob/main/model/plugin/sensor/touch_grid.xml) example model. The plugin includes [in-scene visualisation](https://youtu.be/0LOJ3WMnqeA).

### Simulate


mXVPbppGk5I


6.  `d40c3959` Added Visualization tab to simulate UI, corresponding to elements of the [visual](XMLreference.md) MJCF element. After modifying values in the GUI, a saved XML will contain the new values. The modifiable members of [mjStatistic](APIreference/APItypes.md) ([extent](XMLreference.md), [meansize](XMLreference.md) and [center](XMLreference.md)) are computed by the compiler and therefore do not have defaults. In order for these attributes to appear in the saved XML, a value must be specified in the loaded XML.

<img src="images/changelog/simulate_text_width.png" class="align-right" width="380" alt="Before / After" />

7.  `d40c3959` Increased text width for UI elements in the default spacing. \[before / after\]:

### General

8.  `f67e3595` Added *mj_getState* and *mj_setState* for getting and setting the simulation state as a concatenated vector of floating point numbers. See the [State](computation/index.md) section for details.

9.  `d82f5ce5` Added [mjContact.solreffriction](APIreference/APItypes.md), allowing different [solref](modeling.md) parameters for the normal and frictional axes of contacts when using [elliptic friction cones](XMLreference.md). This attribute is required for elastic frictional collisions, see associated [example model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/spin_recoil.xml) mimicking the spin-bounce recoil behaviour of [elastic rubber balls](https://www.youtube.com/watch?v=uFLJcRegIVQ&t=3s). This is an advanced option currently only supported by explicit [contact pairs](XMLreference.md), using the [solreffriction](XMLreference.md) attribute.

10. `c50177d3` Added *mjd_inverseFD* for finite-differenced inverse-dynamics derivatives.

11. `49efa9cc` Added functions for operations on banded-then-dense "arrowhead" matrices. Such matrices are common when doing direct trajectory optimization. See *mju_cholFactorBand* documentation for details.

12. `2ad82d59` Added *mj_multiRay* function for intersecting multiple rays emanating from a single point. This is significantly faster than calling *mj_ray* multiple times.

13. `9d1a21f9` Ray-mesh collisions are now up to 10x faster, using a bounding volume hierarchy of mesh faces.

14. `3d82d2a4` Increased `mjMAXUIITEM` (maximum number of UI elements per section in Simulate) to 100.

15. `67f0f515` Added [documentation](programming/extension.md) for resource providers.

16. `49efa9cc` Changed the formula for *mju_sigmoid*, a finite-support sigmoid $`s \colon \mathbf R \rightarrow [0, 1]`$. Previously, the smooth part consisted of two stitched quadratics, once continuously differentiable. It is now a single quintic, twice continuously differentiable:

    ``` math
    \begin{aligned}
    s(x) =
    \begin{cases}
    0,                    &       & x \le 0  \\
    6x^5 - 15x^4 + 10x^3, & 0 \lt & x \lt 1  \\
    1,                    & 1 \le & x \qquad
    \end{cases}
    \end{aligned}
    ```

17. `770b4b36` Added optional [tausmooth](XMLreference.md) attribute to muscle actuators. When positive, the time-constant $`\tau`$ of muscle activation/deactivation uses *mju_sigmoid* to transition smoothly between the two extremal values given by the [Millard et al. (2013)](https://doi.org/10.1115/1.4023390) muscle model, within a range of width tausmooth. See [Muscle actuators](modeling.md) for more details. Relatedly, *mju_muscleDynamics* now takes 3 parameters instead of 2, adding the new smoothing-width parameter.

18. `f887c1e9` Moved public C macro definitions out of mujoco.h into a new public header file called  
    [mjmacro.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjmacro.h). The new file is included by mujoco.h so this change does not break existing user code.

19. `f887c1e9` Added instrumentation for the  
    [Address Sanitizer (ASAN)](https://clang.llvm.org/docs/AddressSanitizer.html) and [Memory Sanitizer (MSAN)](https://clang.llvm.org/docs/MemorySanitizer.html) to detect memory bugs when allocating from the `mjData` stack and arena.

20. `f887c1e9` Removed `pstack` and `parena` from the output of `mj_printData`, since these are  
    implementation details of the `mjData` allocators that are affected by diagnostic paddings in instrumented builds.

21. `466c9aca` Removed the `mj_activate` and `mj_deactivate` functions. These had been kept around for  
    compatibility with old user code from when MuJoCo was closed source, but have been no-op functions since open sourcing.

## Version 2.3.5 (April 25, 2023)

### Bug fixes

1.  `d23c5e78` Fix asset loading bug that prevented OBJ and PNG files from being read from disk when [mjVFS](APIreference/APItypes.md) is used.
2.  `d23c5e78` Fix occasional segmentation faults on macOS when mouse perturbations are applied in the Python passive viewer.

### Plugins

3.  `d23c5e78` The `visualize` callback in [mjpPlugin](APIreference/APItypes.md) now receives an [mjvOption](APIreference/APItypes.md) as an input argument.

## Version 2.3.4 (April 20, 2023)

> [!NOTE]
> This version is affected by an asset loading bug that prevents OBJ and PNG files from being read from disk when `mjVFS` is used. Users are advised to skip to version 2.3.5 instead.

### General

1.  `7cc42ecf` Removed the "global" setting of the [compiler/coordinate](XMLreference.md) attribute. This rarely-used setting complicates the compiler logic and is blocking future improvements. In order to convert older models which used this option, load and save them in MuJoCo 2.3.3 or older.

<img src="images/changelog/ellipsoidinertia.gif" class="align-right" width="240" alt="image" />

2.  `7cc42ecf` Added [visual-global](XMLreference.md) flag [ellipsoidinertia](XMLreference.md) to visualize equivalent body inertias with ellipsoids instead of the default boxes.
3.  `5f132af6` Added midphase and broadphase collision statistics to [mjData](APIreference/APItypes.md).
4.  `01b84089` Added documentation for [engine plugins](programming/extension.md).
5.  `2e23594f` Added struct information to the `introspect` module.
6.  `fe3dccfd` Added a new extension mechanism called [resource providers](programming/extension.md). This extensible mechanism allows MuJoCo to read assets from data sources other than the local OS filesystem or the *Virtual file system*.

### Python bindings

7.  `6d63e046` Offscreen rendering on macOS is no longer restricted to the main thread. This is achieved by using the low-level Core OpenGL (CGL) API to create the OpenGL context, rather than going via GLFW which relies on Cocoa's NSOpenGL. The resulting context is not tied to a Cocoa window, and is therefore not tied to the main thread.
8.  `34226bf5` Fixed a race condition in `viewer.launch_passive` and `viewer.launch_repl`. These functions could previously return before an internal call to `mj_forward`. This allows user code to continue and potentially modify physics state concurrently with the internal `mj_forward`, resulting in e.g. [MuJoCo stack overflow error](https://github.com/google-deepmind/mujoco/issues/783) or [segmentation fault](https://github.com/google-deepmind/mujoco/issues/790).
9.  `0db9a453` The `viewer.launch_passive` function now returns a handle which can be used to interact with the viewer. The passive viewer now also requires an explicit call to `sync` on its handle to pick up any update to the physics state. This is to avoid race conditions that can result in visual artifacts. See [documentation](python.md) for details.
10. `b362cb49` The `viewer.launch_repl` function has been removed since its functionality is superseded by `launch_passive`.
11. `2e23594f` Added a small number of missing struct fields discovered through the new `introspect` metadata.

### Bug fixes

12. `101c647a` Fixed bug in the handling of ellipsoid-based fluid model forces in the new implicitfast integrator.

13. `0db9a453` Removed spurious whole-arena copying in <span class="title-ref">mj_copyData</span>, which can considerably  
    [slow down](https://github.com/google-deepmind/mujoco/issues/568) the copying operation.

14. `2d69b158` Make [shellinertia](XMLreference.md) ignore `exactmeshinertia`, which is  
    only used for legacy volume computations ([\#759](https://github.com/google-deepmind/mujoco/issues/759)).

## Version 2.3.3 (March 20, 2023)

### General

1.  `8c7f6ce5` Improvements to implicit integration:

    - The derivatives of the RNE algorithm are now computed using sparse math, leading to significant speed improvements for large models when using the [implicit integrator](computation/index.md).
    - A new integrator called `implicitfast` was added. It is similar to the existing implicit integrator, but skips the derivatives of Coriolis and centripetal forces. See the [numerical integration](computation/index.md) section for a detailed motivation and discussion. The implicitfast integrator is recommended for all new models and will become the default integrator in a future version.

    The table below shows the compute cost of the 627-DoF [humanoid100](https://github.com/google-deepmind/mujoco/blob/main/model/humanoid/humanoid100.xml) model using different integrators. "implicit (old)" uses dense RNE derivatives, "implicit (new)" is after the sparsification mentioned above. Timings were measured on a single core of an AMD 3995WX CPU.

| timing        | Euler | implicitfast | implicit (new) | implicit (old) |
|---------------|-------|--------------|----------------|----------------|
| one step (ms) | 0.5   | 0.53         | 0.77           | 5.0            |
| steps/second  | 2000  | 1900         | 1300           | 200            |

<img src="images/computation/midphase.gif" class="align-right" width="350" alt="image" />


2.  `70959c1a` Added a collision mid-phase for pruning geoms in body pairs, see [documentation](computation/index.md) for more details. This is based on static AABB bounding volume hierarchy (a BVH binary tree) in the body inertial frame. The GIF on the right is cut from [this longer video](https://youtu.be/e0babIM8hBo).
3.  `49c939ea` The `mjd_transitionFD` function no longer triggers sensor calculation unless explicitly requested.
4.  `c57a588a` Corrected the spelling of the `inteval` attribute to `interval` in the [mjLROpt](APIreference/APItypes.md) struct.
5.  `9756ed0d` Mesh texture and normal mappings are now 3-per-triangle rather than 1-per-vertex. Mesh vertices are no longer duplicated in order to circumvent this limitation as they previously were.
6.  `50bebcb4` The non-zeros for the sparse constraint Jacobian matrix are now precounted and used for matrix memory allocation. For instance, the constraint Jacobian matrix from the [humanoid100](https://github.com/google-deepmind/mujoco/blob/main/model/humanoid/humanoid100.xml) model, which previously required ~500,000 `mjtNum`'s, now only requires ~6000. Very large models can now load and run with the CG solver.
7.  `d3d789cf` Modified *mju_error* and *mju_warning* to be variadic functions (support for printf-like arguments). The functions `mju_error_i`, `mju_error_s`, `mju_warning_i`, and `mju_warning_s` are now deprecated.
8.  `056e8492` Implemented a performant `mju_sqrMatTDSparse` function that doesn't require dense memory allocation.
9.  `8696247f` Added `mj_stackAllocInt` to get correct size for allocating ints on mjData stack. Reducing stack memory usage by 10% - 15%.


### Python bindings

10. `e58d53e7` Fixed IPython history corruption when using `viewer.launch_repl`. The `launch_repl` function now provides seamless continuation of an IPython interactive shell session, and is no longer considered experimental feature.

11. `7a0def97` Added `viewer.launch_passive` which launches the interactive viewer in a passive, non-blocking  
    mode. Calls to `launch_passive` return immediately, allowing user code to continue execution, with the viewer automatically reflecting any changes to the physics state. (Note that this functionality is currently in experimental/beta stage, and is not yet described in our [viewer documentation](python.md).)

12. `7a0def97` Added the `mjpython` launcher for macOS, which is required for `viewer.launch_passive` to function there.

13. `71c5f179` Removed `efc_` fields from joint indexers. Since the introduction of arena memory, these fields  
    now have dynamic sizes that change between time steps depending on the number of active constraints, breaking strict correspondence between joints and `efc_` rows.

14. `e20ab6c9` Added a number of missing fields to the bindings of `mjVisual` and `mjvPerturb` structs.

### Simulate

15. `2f0fb1e4` Implemented a workaround for [broken VSync](https://github.com/glfw/glfw/issues/2249) on macOS so that the frame rate is correctly capped when the Vertical Sync toggle is enabled.

<img src="images/changelog/contactlabel.png" class="align-right" width="400" alt="image" />

16. `2607e67f` Added optional labels to contact visualization, indicating which two geoms are contacting (names if defined, ids otherwise). This can be useful in cluttered scenes.

<br/>

## Version 2.3.2 (February 7, 2023)

### General

1.  `c741dfce` A more performant mju_transposeSparse has been implemented that doesn't require dense memory allocation. For a constraint Jacobian matrix from the [humanoid100.xml](https://github.com/google-deepmind/mujoco/blob/main/model/humanoid/humanoid100.xml) model, this function is 35% faster.
2.  `f1007df0` The function *mj_name2id* is now implemented using a hash function instead of a linear search for better performance.
3.  `929e09f8` Geom names are now parsed from URDF. Any duplicate names are ignored. `mj_printData` output now contains contacting geom names.

### Bug fixes

4.  `6ba4d6f0` Fixed a bug that for <span class="at">shellinertia</span> equal to `true` caused the mesh orientation to be overwritten by the principal components of the shell inertia, while the vertex coordinates are rotated using the volumetric inertia. Now the volumetric inertia orientation is used also in the shell case.
5.  `19b6c70e` Fixed misalignment bug in mesh-to-primitive fitting when using the bounding box fitting option <span class="at">fitaabb</span>.

<img src="images/changelog/meshfit.png" class="align-right" width="300" alt="image" />

6.  `d022cd1a` The `launch_repl` functionality in the Python viewer has been fixed.
7.  `06557c14` Set `time` correctly in `mjd_transitionFD`, to support time-dependent user code.
8.  `6b80b010` Fixed sensor data dimension validation when `user` type sensors are present.
9.  `093125c2` Fixed incorrect plugin error message when a null `nsensordata` callback is encountered during model compilation.
10. `e9869d3b` Correctly end the timer (`TM_END`) `mj_fwdConstraint` returns early.
11. `436fc6e7` Fixed an infinite loop in `mj_deleteFileVFS`.

### Simulate

12. `bc0184d6` Increased precision of simulate sensor plot y-axis by 1 digit ([\#719](https://github.com/google-deepmind/mujoco/issues/719)).
13. `79fffdc0` Body labels are now drawn at the body frame rather than inertial frame, unless inertia is being visualised.

### Plugins

14. `5c021d04` The `reset` callback now receives instance-specific `plugin_state` and `plugin_data` as arguments, rather than the entire `mjData`. Since `reset` is called inside `mj_resetData` before any physics forwarding call has been made, it is an error to read anything from `mjData` at this stage.

15. `30b4309a` The `capabilities` field in `mjpPlugin` is renamed `capabilityflags` to more clearly  
    indicate that this is a bit field.

## Version 2.3.1 (December 6, 2022)

### Python bindings

1.  `0846f38c` The `simulate` GUI is now available through the `mujoco` Python package as `mujoco.viewer`. See [documentation](python.md) for details. (Contribution by [Levi Burner](https://github.com/aftersomemath).)
2.  `ef695bb8` The `Renderer` class from the MuJoCo tutorial Colab is now available directly in the native Python bindings.

### General

3.  `893942a7` The tendon <span class="at">springlength</span> attribute can now take two values. Given two non-decreasing values, <span class="title-ref">springlength</span> specifies a [deadband](https://en.wikipedia.org/wiki/Deadband) range for spring stiffness. If the tendon length is between the two values, the force is 0. If length is outside this range, the force behaves like a regular spring, with the spring resting length corresponding to the nearest <span class="at">springlength</span> value. This can be used to create tendons whose limits are enforced by springs rather than constraints, which are cheaper and easier to analyse. See [tendon_springlength.xml](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/tendon_springlength.xml) example model.



    Attention


    This is a minor breaking API change. `mjModel.tendon_lengthspring` now has size `ntendon x 2` rather than `ntendon x 1`.



    `-PJ6afdETUg`  


4.  `0eb7f871` Removed the requirement that stateless actuators come before stateful actuators.

5.  `f905c7fb` Added *mju_fill*, *mju_symmetrize* and *mju_eye* utility functions.

6.  `23092a11` Added <span class="at">gravcomp</span> attribute to [body](XMLreference.md), implementing gravity compensation and buoyancy. See [balloons.xml](https://github.com/google-deepmind/mujoco/blob/main/model/balloons/balloons.xml) example model.

7.  `36b30e45` Renamed the `cable` plugin library to `elasticity`.

8.  `0b45129c` Added <span class="at">actdim</span> attribute to [general actuators](XMLreference.md). Values greater than 1 are only allowed for dyntype <span class="at-val">user</span>, as native activation dynamics are all scalar. Added example test implementing 2nd-order activation dynamics to [engine_forward_test.cc](https://github.com/google-deepmind/mujoco/blob/main/test/engine/engine_forward_test.cc).

9.  `3b89b0fd` Improved particle `composite` type, which now permits a user-specified geometry and multiple joints. See the two new examples: [particle_free.xml](https://github.com/google-deepmind/mujoco/blob/0fcd20f0da67ede7b16ef7e439a28be67505a037/model/composite/particle_free.xml) and [particle_free2d.xml](https://github.com/google-deepmind/mujoco/blob/0fcd20f0da67ede7b16ef7e439a28be67505a037/model/composite/particle_free2d.xml).

10. `7b0fbc63` Performance improvements for non-AVX configurations:

    - 14% faster `mj_solveLD` using [restrict](https://en.wikipedia.org/wiki/Restrict). See [engine_core_smooth_benchmark_test](https://github.com/google-deepmind/mujoco/blob/main/test/benchmark/solveLD_benchmark_test.cc).
    - 50% faster `mju_dotSparse` using manual loop unroll. See [engine_util_sparse_benchmark_test](https://github.com/google-deepmind/mujoco/blob/main/test/benchmark/engine_util_sparse_benchmark_test.cc).

11. `d0b1a973` Added new <span class="at">solid</span> passive force plugin:


    AGcTGHbbze4


    - This is new force field compatible with the `composite` particles.
    - Generates a tetrahedral mesh having particles with mass concentrated at vertices.
    - Uses a piecewise-constant strain model equivalent to finite elements but expressed in a coordinate-free formulation. This implies that all quantities can be precomputed except edge elongation, as in a mass-spring model.
    - Only suitable for small strains (large displacements but small deformations). Tetrahedra may invert if subject to large loads.

12. `9ecade07` Added API functions `mj_loadPluginLibrary` and `mj_loadAllPluginLibraries`. The first function is identical to `dlopen` on a POSIX system, and to `LoadLibraryA` on Windows. The second function scans a specified directory for all dynamic libraries file and loads each library found. Dynamic libraries opened by these functions are assumed to register one or more MuJoCo plugins on load.

13. `0d52feaa` Added an optional `visualize` callback to plugins, which is called during `mjv_updateScene`. This callback allows custom plugin visualizations. Enable stress visualization for the Cable plugin as an example.

14. `dee1d602` Sensors of type [user](XMLreference.md) no longer require <span class="at">objtype</span>, <span class="at">objname</span> and <span class="at">needstage</span>. If unspecified, the objtype is now [mjOBJ_UNKNOWN](APIreference/APItypes.md). `user` sensors <span class="at">datatype</span> default is now <span class="at-val">"real"</span>, <span class="at">needstage</span> default is now <span class="at-val">"acc"</span>.

15. `638c9a69` Added support for capsules in URDF import.

16. `df25d7d6` On macOS, issue an informative error message when run under [Rosetta 2](https://support.apple.com/en-gb/HT211861) translation on an Apple Silicon machine. Pre-built MuJoCo binaries make use of [AVX](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions) instructions on x86-64 machines, which is not supported by Rosetta 2. (Before this version, users only get a cryptic "Illegal instruction" message.)

### Bug fixes

17. `89185b4a` Fixed bug in `mj_addFileVFS` that was causing the file path to be ignored (introduced in 2.1.4).

### Simulate

18. `2ebc5f09` Renamed the directory in which the `simulate` application searches for plugins from `plugin` to `mujoco_plugin`.
19. `165e72f7` Mouse force perturbations are now applied at the selection point rather than the body center of mass.

## Version 2.3.0 (October 18, 2022)

### General

1.  `58fd72f5` The `contact` array and arrays prefixed with `efc_` in `mjData` were moved out of the `buffer` into a new `arena` memory space. These arrays are no longer allocated with fixed sizes when `mjData` is created. Instead, the exact memory requirement is determined during each call to *mj_forward* (specifically, in *mj_collision* and *mj_makeConstraint*) and the arrays are allocated from the `arena` space. The `stack` now also shares its available memory with `arena`. This change reduces the memory footprint of `mjData` in models that do not use the PGS solver, and will allow for significant memory reductions in the future. See the [Memory allocation](modeling.md) section for details.


    RHnXD6uO3Mg


2.  `f151e84a` Added colab notebook tutorial showing how to balance the humanoid on one leg with a Linear Quadratic Regulator. The notebook uses MuJoCo's native Python bindings, and includes a draft `Renderer` class, for easy rendering in Python. <br/> Try it yourself: [![LQRopenincolab](https://colab.research.google.com/assets/colab-badge.png)](https://colab.research.google.com/github/deepmind/mujoco/blob/main/python/LQR.ipynb)

3.  `04d44e1e` Updates to humanoid model:

    - Added two keyframes (stand-on-one-leg and squat).
    - Increased maximum hip flexion angle.
    - Added hamstring tendons which couple the hip and knee at high hip flexion angles.
    - General cosmetic improvements, including improved use of defaults and better naming scheme.

4.  `89579766` Added *mju_boxQP* and allocation function *mju_boxQPmalloc* for solving the box-constrained Quadratic Program:

    ``` math
    x^* = \text{argmin} \; \tfrac{1}{2} x^T H x + x^T g \quad \text{s.t.} \quad l \le x \le u
    ```

    The algorithm, introduced in [Tassa et al. 2014](https://doi.org/10.1109/ICRA.2014.6907001), converges after 2-5 Cholesky factorisations, independent of problem size.

5.  `f4e7fa97` Added *mju_mulVecMatVec* to multiply a square matrix $`M`$ with vectors $`x`$ and $`y`$ on both sides. The function returns $`x^TMy`$.

6.  `1e2a9a53` Added new plugin API. Plugins allow developers to extend MuJoCo's capability without modifying core engine code. The plugin mechanism is intended to replace the existing callbacks, though these will remain for the time being as an option for simple use cases and backward compatibility. The new mechanism manages stateful plugins and supports multiple plugins from different sources, allowing MuJoCo extensions to be introduced in a modular fashion, rather than as global overrides. Note the new mechanism is currently undocumented except in code, as we test it internally. If you are interested in using the plugin mechanism, please get in touch first.

7.  `cce35e18` Added <span class="at">assetdir</span> compiler option, which sets the values of both <span class="at">meshdir</span> and <span class="at">texturedir</span>. Values in the latter attributes take precedence over <span class="at">assetdir</span>.

8.  `84d16844` Added <span class="at">realtime</span> option to [visual](XMLreference.md) for starting a simulation at a slower speed.

9.  `e250ff0d` Added new <span class="at">cable</span> composite type:

    - Cable elements are connected with ball joints.
    - The <span class="title-ref">initial</span> parameter specifies the joint at the starting boundary: <span class="at">free</span>, <span class="at">ball</span>, or <span class="at">none</span>.
    - The boundary bodies are exposed with the names <span class="at">B_last</span> and <span class="at">B_first</span>.
    - The vertex initial positions can be specified directly in the XML with the parameter <span class="at">vertex</span>.
    - The orientation of the body frame **is** the orientation of the material frame of the curve.

10. `e250ff0d` Added new <span class="at">cable</span> passive force plugin:

    - Twist and bending stiffness can be set separately with the parameters <span class="at">twist</span> and <span class="at">bend</span>.
    - The stress-free configuration can be set to be the initial one or flat with the flag <span class="at">flat</span>.
    - New [cable.xml](https://github.com/google-deepmind/mujoco/blob/e250ff0d/model/plugin/elasticity/cable.xml) example showing the formation of plectoneme.
    - New [coil.xml](https://github.com/google-deepmind/mujoco/blob/e250ff0d/model/plugin/elasticity/coil.xml) example showing a curved equilibrium configuration.
    - New [belt.xml](https://github.com/google-deepmind/mujoco/blob/e250ff0d/model/plugin/elasticity/belt.xml) example showing interaction between twist and anisotropy.
    - Added test using cantilever exact solution.

    <table style="width:99%;">
    <colgroup>
    <col style="width: 32%" />
    <col style="width: 32%" />
    <col style="width: 32%" />
    </colgroup>
    <tbody>
    <tr>
    <td><div class="youtube" data-align="center" height="140px">
    <p>25kQP671fJE</p>
</td>
    <td><div class="youtube" data-align="center" height="140px">
    <p>4DvGe-BodFU</p>
</td>
    <td><div class="youtube" data-align="center" height="140px">
    <p>QcGdpUd5H0c</p>
</td>
    </tr>
    </tbody>
    </table>

### Python bindings

11. `c13979cd` Added `id` and `name` properties to [named accessor](https://mujoco.readthedocs.io/en/latest/python.html#named-access) objects. These provide more Pythonic API access to `mj_name2id` and `mj_id2name` respectively.
12. `58fd72f5` The length of `MjData.contact` is now `ncon` rather than `nconmax`, allowing it to be straightforwardly used as an iterator without needing to check `ncon`.
13. `ec6ea6a6` Fix a memory leak when a Python callable is installed as callback ([\#527](https://github.com/google-deepmind/mujoco/issues/527)).

## Version 2.2.2 (September 7, 2022)

### General


BcHZ5BFeTmU


1.  `3d77eb1e` Added [adhesion actuators](XMLreference.md) mimicking vacuum grippers and adhesive biomechanical appendages.

2.  `3d77eb1e` Added related [example model](https://github.com/google-deepmind/mujoco/tree/main/model/adhesion) and video:

3.  `fcf41317` Added *mj_jacSubtreeCom* for computing the translational Jacobian of the center-of-mass of a subtree.

4.  `d26501c0` Added <span class="at">torquescale</span> and <span class="at">anchor</span> attributes to <span class="el">weld</span> constraints. <span class="at">torquescale</span> sets the torque-to-force ratio exerted by the constraint, <span class="at">anchor</span> sets the point at which the weld wrench is applied. See [weld](XMLreference.md) for more details.

5.  `d26501c0` Increased `mjNEQDATA`, the row length of equality constraint parameters in `mjModel.eq_data`, from 7 to 11.

6.  `d26501c0` Added visualisation of anchor points for both <span class="el">connect</span> and <span class="el">weld</span> constraints (activated by the 'N' key in `simulate`).

7.  `8ca5887c` Added [weld.xml](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/weld.xml) showing different uses of new weld attributes.


    s-0JHanqV1A


8.  `46da1285` Cartesian 6D end-effector control is now possible by adding a reference site to actuators with <span class="at">site</span> transmission. See description of new <span class="at">refsite</span> attribute in the [actuator](XMLreference.md) documentation and [refsite.xml](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/actuation/refsite.xml) example model.

9.  `a693a2d9` Added <span class="at">autolimits</span> compiler option. If `true`, joint and tendon <span class="at">limited</span> attributes and actuator <span class="at">ctrllimited</span>, <span class="at">forcelimited</span> and <span class="at">actlimited</span> attributes will automatically be set to `true` if the corresponding range *is defined* and `false` otherwise.

    If `autolimits="false"` (the default) models where a <span class="at">range</span> attribute is specified without the <span class="at">limited</span> attribute will fail to compile. A future release will change the default of <span class="at">autolimits</span> to `true`, and this compilation error allows users to catch this future change of behavior.



    Attention


    This is a breaking change. In models where a range was defined but <span class="at">limited</span> was unspecified, explicitly set limited to `false` or remove the range to maintain the current behavior of your model.


10. `8ca5887c` Added moment of inertia computation for all well-formed meshes. This option is activated by setting the compiler flag <span class="at">exactmeshinertia</span> to `true` (defaults to `false`). This default may change in the future.

11. `5c5449bf` Added parameter <span class="at">shellinertia</span> to <span class="at">geom</span>, for locating the inferred inertia on the boundary (shell). Currently only meshes are supported.

12. `833dc740` For meshes from which volumetric inertia is inferred, raise error if the orientation of mesh faces is not consistent. If this occurs, fix the mesh in e.g., MeshLab or Blender.


    I2q7D0Vda-A


13. `ae0ac86e` Added catenary visualisation for hanging tendons. The model seen in the video can be found [here](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/catenary.xml).

14. `b966a378` Added `azimuth` and `elevation` attributes to [visual/global](XMLreference.md), defining the initial orientation of the free camera at model load time.

15. `b966a378` Added `mjv_defaultFreeCamera` which sets the default free camera, respecting the above attributes.

16. `80b4ffdd` `simulate` now supports taking a screenshot via a button in the File section or via `Ctrl-P`.

17. `834e8dd5` Improvements to time synchronisation in <span class="title-ref">simulate</span>, in particular report actual real-time factor if different from requested factor (if e.g., the timestep is so small that simulation cannot keep up with real-time).

18. `090fe2db` Added a disable flag for sensors.

19. `fdbbc8bb` *mju_mulQuat* and *mju_mulQuatAxis* support in place computation. For example <br/> `mju_mulQuat(a, a, b);` sets the quaternion `a` equal to the product of `a` and `b`.

20. `e3a82247` Added sensor matrices to `mjd_transitionFD` (note this is an API change).

### Deleted/deprecated features

21. `c8ff7b3d` Removed `distance` constraints.

### Bug fixes

22. `f71daed6` Fixed rendering of some transparent geoms in reflection.
23. `0b2f19bb` Fixed `intvelocity` defaults parsing.

## Version 2.2.1 (July 18, 2022)

### General

1.  `228264c9` Added `mjd_transitionFD` to compute efficient finite difference approximations of the state-transition and control-transition matrices, [see here](computation/index.md) for more details.
2.  `373cc894` Added derivatives for the ellipsoid fluid model.
3.  `09a5efc0` Added `ctrl` attribute to [keyframes](XMLreference.md).
4.  `c14a7ef4` Added `clock` sensor which [measures time](XMLreference.md).
5.  `2d0995b4` Added visualisation groups to skins.
6.  `6ead1461` Added actuator visualisation for `free` and `ball` joints and for actuators with `site` transmission.
7.  `d3a86bb7` Added visualisation for actuator activations.
8.  `d3a86bb7` Added `<actuator-intvelocity>` actuator shortcut for "integrated velocity" actuators, documented [here](XMLreference.md).
9.  `d3a86bb7` Added `<actuator-damper>` actuator shortcut for active-damping actuators, documented [here](XMLreference.md).
10. `ec7133b0` `mju_rotVecMat` and `mju_rotVecMatT` now support in-place multiplication.
11. `d3a86bb7` `mjData.ctrl` values are no longer clamped in-place, remain untouched by the engine.
12. `d3a86bb7` Arrays in mjData's buffer now align to 64-byte boundaries rather than 8-byte.
13. `f887c1e9` Added memory poisoning when building with [Address Sanitizer (ASAN)](https://clang.llvm.org/docs/AddressSanitizer.html) and [Memory Sanitizer (MSAN)](https://clang.llvm.org/docs/MemorySanitizer.html). This allows ASAN to detect reads and writes to regions in `mjModel.buffer` and `mjData.buffer` that do not lie within an array, and for MSAN to detect reads from uninitialised fields in `mjData` following `mj_resetData`.
14. `373cc894` Added a [slider-crank example model](https://github.com/google-deepmind/mujoco/tree/main/model/slider_crank).

### Bug fixes

15. `d3a86bb7` [Activation clamping](modeling.md) was not being applied in the [implicit integrator](computation/index.md).
16. `d3a86bb7` Stricter parsing of orientation specifiers. Before this change, a specification that included both `quat` and an [alternative specifier](modeling.md) e.g., `<geom ... quat=".1 .2 .3 .4" euler="10 20 30">`, would lead to the `quat` being ignored and only `euler` being used. After this change a parse error will be thrown.
17. `f3453cf8` Stricter parsing of XML attributes. Before this change an erroneous XML snippet like `<geom size="1/2 3 4">` would have been parsed as `size="1 0 0"` and no error would have been thrown. Now throws an error.
18. `d3a86bb7` Trying to load a `NaN` via XML like `<geom size="1 NaN 4">`, while allowed for debugging purposes, will now print a warning.
19. `d5672639` Fixed null pointer dereference in `mj_loadModel`.
20. `dbef8e6c` Fixed memory leaks when loading an invalid model from MJB.
21. `d3a86bb7` Integer overflows are now avoided when computing `mjModel` buffer sizes.
22. `d3a86bb7` Added missing warning string for `mjWARN_BADCTRL`.

### Packaging

23. `d3a86bb7` Changed MacOS packaging so that the copy of `mujoco.framework` embedded in `MuJoCo.app` can be used to build applications externally.

## Version 2.2.0 (May 23, 2022)

### Open Sourcing

1.  `1913a02b` MuJoCo is now fully open-source software. Newly available top level directories are:

    a\. `src/`: All source files. Subdirectories correspond to the modules described in the Programming chapter [introduction](programming/index.md):

    - `src/engine/`: Core engine.
    - `src/xml/`: XML parser.
    - `src/user/`: Model compiler.
    - `src/visualize/`: Abstract visualizer.
    - `src/ui/`: UI framework.

    2.  `test/`: Tests and corresponding asset files.
    3.  `dist/`: Files related to packaging and binary distribution.

2.  `1913a02b` Added [contributor's guide](https://github.com/google-deepmind/mujoco/blob/main/CONTRIBUTING.md) and [style guide](https://github.com/google-deepmind/mujoco/blob/main/STYLEGUIDE.md).

### General

3.  `64bc6d27` Added analytic derivatives of smooth (unconstrained) dynamics forces, with respect to velocities:
    - Centripetal and Coriolis forces computed by the Recursive Newton-Euler algorithm.
    - Damping and fluid-drag passive forces.
    - Actuation forces.
4.  `64bc6d27` Added `implicit` integrator. Using the analytic derivatives above, a new implicit-in-velocity integrator was added. This integrator lies between the Euler and Runge Kutta integrators in terms of both stability and computational cost. It is most useful for models which use fluid drag (e.g. for flying or swimming) and for models which use [velocity actuators](XMLreference.md). For more details, see the [Numerical Integration](computation/index.md) section.
5.  `1913a02b` Added <span class="at">actlimited</span> and <span class="at">actrange</span> attributes to [general actuators](XMLreference.md), for clamping actuator internal states (activations). This clamping is useful for integrated-velocity actuators, see the [Activation clamping](modeling.md) section for details.
6.  `1913a02b` `mjData` fields `qfrc_unc` (unconstrained forces) and `qacc_unc` (unconstrained accelerations) were renamed `qfrc_smooth` and `qacc_smooth`, respectively. While "unconstrained" is precise, "smooth" is more intelligible than "unc".
7.  `1913a02b` Public headers have been moved from `/include` to `/include/mujoco/`, in line with the directory layout common in other open source projects. Developers are encouraged to include MuJoCo public headers in their own codebase via `#include <mujoco/filename.h>`.
8.  `1913a02b` The default shadow resolution specified by the [shadowsize](XMLreference.md) attribute was increased from 1024 to 4096.
9.  `1913a02b` Saved XMLs now use 2-space indents.

### Bug fixes

10. `1913a02b` Antialiasing was disabled for segmentation rendering. Before this change, if the [offsamples](XMLreference.md) attribute was greater than 0 (the default value is 4), pixels that overlapped with multiple geoms would receive averaged segmentation IDs, leading to incorrect or non-existent IDs. After this change <span class="at">offsamples</span> is ignored during segmentation rendering.

11. `1913a02b` The value of the enable flag for the experimental multiCCD feature was made sequential with other  
    enable flags. Sequentiality is assumed in the `simulate` UI and elsewhere.

12. `1913a02b` Fix issue of duplicated meshes when saving models with OBJ meshes using mj_saveLastXML.

## Version 2.1.5 (Apr. 13, 2022)

### General

1.  `87539dbd` Added an experimental feature: multi-contact convex collision detection, activated by an enable flag. See full description [here](XMLreference.md).

### Bug fixes

2.  `87539dbd` GLAD initialization logic on Linux now calls `dlopen` to load a GL platform dynamic library if a `*GetProcAddress` function is not already present in the process' global symbol table. In particular, processes that use GLFW to set up a rendering context that are not explicitly linked against `libGLX.so` (this applies to the Python interpreter, for example) will now work correctly rather than fail with a `gladLoadGL` error when `mjr_makeContext` is called.
3.  `87539dbd` In the Python bindings, named indexers for scalar fields (e.g. the `ctrl` field for actuators) now return a NumPy array of shape `(1,)` rather than `()`. This allows values to be assigned to these fields more straightforwardly.

## Version 2.1.4 (Apr. 4, 2022)

### General

1.  `90dea1bd` MuJoCo now uses GLAD to manage OpenGL API access instead of GLEW. On Linux, there is no longer a need to link against different GL wrangling libraries depending on whether GLX, EGL, or OSMesa is being used. Instead, users can simply use GLX, EGL, or OSMesa to create a GL context and `mjr_makeContext` will detect which one is being used.
2.  `90dea1bd` Added visualisation for contact frames. This is useful when writing or modifying collision functions, when the actual direction of the x and y axes of a contact can be important.

### Binary build

3.  `90dea1bd` The `_nogl` dynamic library is no longer provided on Linux and Windows. The switch to GLAD allows us to resolve OpenGL symbols when `mjr_makeContext` is called rather than when the library is loaded. As a result, the MuJoCo library no longer has an explicit dynamic dependency on OpenGL, and can be used on system where OpenGL is not present.

### Simulate

4.  `90dea1bd` Fixed a bug in simulate where pressing '\[' or '\]' when a model is not loaded causes a crash.
5.  `90dea1bd` Contact frame visualisation was added to the Simulate GUI.
6.  `90dea1bd` Renamed "set key", "reset to key" to "save key" and "load key", respectively.
7.  `90dea1bd` Changed bindings of F6 and F7 from the not very useful "vertical sync" and "busy wait" to the more useful cycling of frames and labels.

### Bug fixes

8.  `90dea1bd` `mj_resetData` zeroes out the `solver_nnz` field.
9.  `90dea1bd` Removed a special branch in `mju_quat2mat` for unit quaternions. Previously, `mju_quat2mat` skipped all computation if the real part of the quaternion equals 1.0. For very small angles (e.g. when finite differencing), the cosine can evaluate to exactly 1.0 at double precision while the sine is still nonzero.

## Version 2.1.3 (Mar. 23, 2022)

### General

1.  `df048e54` `simulate` now supports cycling through cameras (with the `[` and `]` keys).
2.  `df048e54` `mjVIS_STATIC` toggles all static bodies, not just direct children of the world.

### Python bindings

3.  `df048e54` Added a `free()` method to `MjrContext`.
4.  `df048e54` Enums now support arithmetic and bitwise operations with numbers.

### Bug fixes

5.  `df048e54` Fixed rendering bug for planes, introduced in 2.1.2. This broke maze environments in [dm_control](https://github.com/google-deepmind/dm_control).

## Version 2.1.2 (Mar. 15, 2022)

### New modules

1.  `3577e2cf` Added new [Python bindings](python.md), which can be installed via `pip install mujoco`, and imported as `import mujoco`.
2.  `3577e2cf` Added new [Unity plug-in](unity.md).
3.  `3577e2cf` Added a new `introspect` module, which provides reflection-like capability for MuJoCo's public API, currently describing functions and enums. While implemented in Python, this module is expected to be generally useful for automatic code generation targeting multiple languages. (This is not shipped as part of the `mujoco` Python bindings package.)

### API changes

4.  `3577e2cf` Moved definition of `mjtNum` floating point type into a new header [mjtnum.h](https://github.com/google-deepmind/mujoco/blob/3577e2cf8bf841475b489aefff52276a39f24d51/include/mjtnum.h).
5.  `3577e2cf` Renamed header <span class="title-ref">mujoco_export.h</span> to [mjexport.h](programming/index.md).
6.  `3577e2cf` Added `mj_printFormattedData`, which accepts a format string for floating point numbers, for example to increase precision.

### General

7.  `3577e2cf` MuJoCo can load [OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file) mesh files.
    1.  Meshes containing polygons with more than 4 vertices are not supported.

    2.  In OBJ files containing multiple object groups, any groups after the first one will be ignored.

    3.  Added (post-release, not included in the 2.1.2 archive) textured [mug](https://github.com/google-deepmind/mujoco/blob/main/model/mug/mug.xml) example model:

        <img src="images/changelog/mug.png" width="300" alt="image" />
8.  `3577e2cf` Added optional frame-of-reference specification to [framepos](XMLreference.md), [framequat](XMLreference.md), [framexaxis](XMLreference.md), [frameyaxis](XMLreference.md), [framezaxis](XMLreference.md), [framelinvel](XMLreference.md), and [frameangvel](XMLreference.md) sensors. The frame-of-reference is specified by new <span class="at">reftype</span> and <span class="at">refname</span> attributes.
9.  `3577e2cf` Sizes of [user parameters](modeling.md) are now automatically inferred.
    1.  Declarations of user parameters in the top-level [size](XMLreference.md) clause (e.g. <span class="at">nuser_body</span>, <span class="at">nuser_jnt</span>, etc.) now accept a value of -1, which is the default. This will automatically set the value to the length of the maximum associated <span class="at">user</span> attribute defined in the model.
    2.  Setting a value smaller than -1 will lead to a compiler error (previously a segfault).
    3.  Setting a value to a length smaller than some <span class="at">user</span> attribute defined in the model will lead to an error (previously additional values were ignored).
10. `3577e2cf` Increased the maximum number of lights in an [mjvScene](APIreference/APItypes.md) from 8 to 100.
11. `3577e2cf` Saved XML files only contain explicit [inertial](XMLreference.md) elements if the original XML included them. Inertias that were automatically inferred by the compiler's [inertiafromgeom](XMLreference.md) mechanism remain unspecified.
12. `3577e2cf` User-selected geoms are always rendered as opaque. This is useful in interactive visualizers.
13. `3577e2cf` Static geoms now respect their [geom group](XMLreference.md) for visualisation. Until this change rendering of static geoms could only be toggled using the [mjVIS_STATIC](APIreference/APItypes.md) visualisation flag . After this change, both the geom group and the visualisation flag need to be enabled for the geom to be rendered.
14. `3577e2cf` Pointer parameters in function declarations in [mujoco.h](programming/index.md) that are supposed to represent fixed-length arrays are now spelled as arrays with extents, e.g. `mjtNum quat[4]` rather than `mjtNum* quat`. From the perspective of C and C++, this is a non-change since array types in function signatures decay to pointer types. However, it allows autogenerated code to be aware of expected input shapes.
15. `147efb51` Experimental stateless fluid interaction model. As described [here](computation/index.md), fluid forces use sizes computed from body inertia. While sometimes convenient, this is very rarely a good approximation. In the new model forces act on geoms, rather than bodies, and have a several user-settable parameters. The model is activated by setting a new attribute: `<geom fluidshape="ellipsoid"/>`. The parameters are described succinctly [here](XMLreference.md), but we leave a full description or the model and its parameters to when this feature leaves experimental status.

### Bug fixes

16. `3577e2cf` `mj_loadXML` and `mj_saveLastXML` are now locale-independent. The Unity plugin should now work correctly for users whose system locales use commas as decimal separators.

17. `3577e2cf` XML assets in VFS no longer need to end in a null character. Instead, the file size is determined  
    by the size parameter of the corresponding VFS entry.

18. `3577e2cf` Fix a vertex buffer object memory leak in `mjrContext` when skins are used.

19. `3577e2cf` Camera quaternions are now normalized during XML compilation.

### Binary build

20. `3577e2cf` Windows binaries are now built with Clang.

## Version 2.1.1 (Dec. 16, 2021)

### API changes

1.  `a499b381` Added `mj_printFormattedModel`, which accepts a format string for floating point numbers, for example to increase precision.

2.  `a499b381` Added `mj_versionString`, which returns human-readable string that represents the version of the MuJoCo binary.

3.  `a499b381` Converted leading underscores to trailing underscores in private instances of API struct definitions, to conform to reserved identifier directive, see [C standard: Section 7.1.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).



    Attention


    This is a minor breaking change. Code which references private instances will break. To fix, replace leading underscores with trailing underscores, e.g. `_mjModel` |rarr| `mjModel_`.


### General

4.  `a499b381` Safer string handling: replaced `strcat`, `strcpy`, and `sprintf` with `strncat`, `strncpy`, and `snprintf` respectively.
5.  `ee39340a` Changed indentation from 4 spaces to 2 spaces, K&R bracing style, added braces to one-line conditionals.

### Bug Fixes

6.  `a499b381` Fixed reading from uninitialized memory in PGS solver.

7.  `a499b381` Computed capsule inertias are now exact. Until this change, capsule masses and inertias computed by the [compiler](XMLreference.md)'s <span class="at">inertiafromgeom</span> mechanism were approximated by a cylinder, formed by the capsule's cylindrical middle section, extended on both ends by half the capsule radius. Capsule inertias are now computed with the [Parallel Axis theorem](https://en.wikipedia.org/wiki/Parallel_axis_theorem), applied to the two hemispherical end-caps.



    Attention


    This is a minor breaking change. Simulation of a model with automatically-computed capsule inertias will be numerically different, leading to, for example, breakage of golden-value tests.


8.  `a499b381` Fixed bug related to [force](XMLreference.md) and [torque](XMLreference.md) sensors. Until this change, forces and torques reported by F/T sensors ignored out-of-tree constraint wrenches except those produced by contacts. Force and torque sensors now correctly take into account the effects of [connect](XMLreference.md) and [weld](XMLreference.md) constraints.

    > [!NOTE]
    > Forces generated by [spatial tendons](XMLreference.md) which are outside the kinematic tree (i.e., between bodies which have no ancestral relationship) are still not taken into account by force and torque sensors. This remains a future work item.

### Code samples

9.  `a499b381` `testspeed`: Added injection of pseudo-random control noise, turned on by default. This is to avoid settling into some fixed contact configuration and providing an unrealistic timing measure.
10. `a499b381` `simulate`:
    1.  Added slower-than-real-time functionality, which is controlled via the '+' and '-' keys.
    2.  Added sliders for injecting Brownian noise into the controls.
    3.  Added "Print Camera" button to print an MJCF clause with the pose of the current camera.
    4.  The camera pose is not reset when reloading the same model file.

### Updated dependencies

11. `a499b381` `TinyXML` was replaced with `TinyXML2` 6.2.0.
12. `a499b381` `qhull` was upgraded to version 8.0.2.
13. `a499b381` `libCCD` was upgraded to version 1.4.
14. `a499b381` On Linux, `libstdc++` was replaced with `libc++`.

### Binary build

15. `a499b381` MacOS packaging. We now ship Universal binaries that natively support both Apple Silicon and Intel CPUs.
    1.  MuJoCo library is now packaged as a [Framework Bundle](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPFrameworks/Concepts/FrameworkAnatomy.html), allowing it to be incorporated more easily into Xcode projects (including Swift projects). Developers are encouraged to compile and link against MuJoCo using the `-framework mujoco` flag, however all header files and the `libmujoco.2.1.1.dylib` library can still be directly accessed inside the framework.
    2.  Sample applications are now packaged into an Application Bundle called `MuJoCo.app`. When launched via GUI, the bundle launches the `simulate` executable. Other precompiled sample programs are shipped inside that bundle (in `MuJoCo.app/Contents/MacOS`) and can be launched via command line.
    3.  Binaries are now signed and the disk image is notarized.
16. `a499b381` Windows binaries and libraries are now signed.
17. `a499b381` Link-time optimization is enabled on Linux and macOS, leading to an average of ~20% speedup when benchmarked on three test models (`cloth.xml`, `humanoid.xml`, and `humanoid100.xml`).
18. `a499b381` Linux binaries are now built with LLVM/Clang instead of GCC.
19. `a499b381` An AArch64 (aka ARM64) Linux build is also provided.
20. `a499b381` Private symbols are no longer stripped from shared libraries on Linux and MacOS.

### Sample models

21. `a499b381` Clean-up of the `model/` directory.
    1.  Rearranged into subdirectories which include all dependencies.
    2.  Added descriptions in XML comments, cleaned up XMLs.
    3.  Deleted some composite models: `grid1`, `grid1pin`, `grid2`, `softcylinder`, `softellipsoid`.
22. `a499b381` Added descriptive animations in `docs/images/models/` :

<img src="images/models/humanoid.gif" width="270" alt="humanoid" /> <img src="images/models/particle.gif" width="270" alt="particle" />

## Version 2.1.0 (Oct. 18, 2021)

### New features

1.  Keyframes now have `mocap_pos` and `mocap_quat` fields (mpos and quat attributes in the XML) allowing mocap poses to be stored in keyframes.
2.  New utility functions: `mju_insertionSortInt` (integer insertion sort) and `mju_sigmoid` (constructing a sigmoid from two half-quadratics).

### General

3.  The preallocated sizes in the virtual file system (VFS) increased to 2000 and 1000, to allow for larger projects.
4.  The C structs in the `mjuiItem` union are now named, for compatibility.
5.  Fixed: `mjcb_contactfilter` type is `mjfConFilt` (was `mjfGeneric`).
6.  Fixed: The array of sensors in `mjCModel` was not cleared.
7.  Cleaned up cross-platform code (internal changes, not visible via the API).
8.  Fixed a bug in parsing of XML `texcoord` data (related to number of vertices).
9.  Fixed a bug in [simulate.cc](https://github.com/google-deepmind/mujoco/blob/main/simulate/simulate.cc) related to `nkey` (the number of keyframes).
10. Accelerated collision detection in the presence of large numbers of non-colliding geoms (with `contype==0 and conaffinity==0`).

### UI

11. Figure selection type changed from `int` to `float`.
12. Figures now show data coordinates, when selection and highlight are enabled.
13. Changed `mjMAXUIMULTI` to 35, `mjMAXUITEXT` to 300, `mjMAXUIRECT` to 25.
14. Added collapsible sub-sections, implemented as separators with state: `mjSEPCLOSED` collapsed, `mjSEPCLOSED+1` expanded.
15. Added `mjITEM_RADIOLINE` item type.
16. Added function `mjui_addToSection` to simplify UI section construction.
17. Added subplot titles to `mjvFigure`.

### Rendering

18. `render_gl2` guards against non-finite floating point data in the axis range computation.
19. `render_gl2` draws lines from back to front for better visibility.
20. Added function `mjr_label` (for text labels).
21. `mjr_render` exits immediately if `ngeom==0`, to avoid errors from uninitialized scenes (e.g. `frustrum==0`).
22. Added scissor box in `mjr_render`, so we don't clear the entire window at every frame.

### License manager

23. Removed the entire license manager. The functions `mj_activate` and `mj_deactivate` are still there for backward compatibility, but now they do nothing and it is no longer necessary to call them.
24. Removed the remote license certificate functions `mj_certXXX`.

## Earlier versions

For changelogs of earlier versions please see [roboti.us](https://www.roboti.us/download.html).
