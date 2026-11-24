---
name: visualization-rendering
description: 'Visualizing and rendering MuJoCo scenes: cameras (mjvCamera), selection and perturbation, visualization options (mjvOption), scene update (mjv_updateScene), OpenGL rendering (mjrContext, offscreen buffers), Filament rendering, virtual reality and the UI framework. Use when rendering images or video, configuring cameras or visual flags, picking objects, or building a custom viewer.'
---

# Visualization and Rendering (C API)

Use this skill to turn a simulation into pixels from C/C++: control cameras
(`mjvCamera`), pick objects, apply mouse perturbations, choose what is shown
(`mjvOption`), build the abstract scene (`mjv_updateScene`), and render it
with the classic OpenGL renderer (`mjr`, onscreen or offscreen) or the
Filament PBR renderer (`mjrf`). It also covers VR integration and the native
UI framework. The `basic`, `simulate` and `render` samples are described in
[c-programming](../SKILL.md); stepping is in
[simulation-loop](../simulation-loop/SKILL.md).

## Architecture

The abstract visualizer (`mjv`, `mjvisualize.h`) is independent of any
graphics library. Both renderers share its cameras, selection, perturbation
and options:

| Type | Role |
|----|----|
| `mjvCamera` / `mjvGLCamera` | High-level interactive camera / low-level frustum camera (`mjvGLCamera` is aliased `mjrCamera`) |
| `mjvOption` | Which element categories, groups and diagnostic overlays are visible |
| `mjvPerturb` | Interactive selection and mouse-applied forces/torques |
| `mjvScene`, `mjvGeom` | Complete per-frame geometric description of the scene and decorations |

| | OpenGL (`mjr`) | Filament (`mjrf`) |
|----|----|----|
| Status | Maintenance mode; powers classic `simulate` and `basic` | Recommended for new apps; powers MuJoCo Studio |
| Mode | Immediate: `mjv_updateScene` fills `mjvScene` every frame, `mjr_render` draws it | Retained, asynchronous: objects created once, updated in place from mjData; `mjvScene` only for decorations (`mjCAT_DECOR`) |
| GPU context | `mjrContext`, needs an externally created OpenGL context | `mjrfContext`, owns its graphics context (OpenGL or Vulkan, windowed or headless) |
| Model resources | Uploaded by `mjr_makeContext` | `mjrfMesh`, `mjrfTexture`, created by `ModelResources` |
| Per-frame scene | `mjv_updateScene` fills `mjvScene` | `ModelRenderables::Update` updates `mjrfRenderable` objects |
| Offscreen buffer | `mjFB_OFFSCREEN`, sized by `mjModel.vis` | `mjrfRenderTarget`, any size and format |
| Pixel readback | `mjr_readPixels` | `mjrfReadRequest`, submitted with the render request |
| Modes/effects | `mjvScene.flags` (`mjtRndFlag`), `mjvScene.stereo` | `mjrDrawMode` and per-request flags in `mjrfRenderRequest`; stereo = two requests |
| 2D overlays/text | `mjr_overlay`, `mjr_text`, `mjr_rectangle`, `mjr_figure` | None; labels reported via callback, drawn by the app |

Third-party renderers can consume `mjvScene` directly.

## Minimal OpenGL viewer (GLFW)

Short version of `basic.cc`:

``` C
// MuJoCo data structures
mjModel* m = NULL;                  // MuJoCo model
mjData* d = NULL;                   // MuJoCo data
mjvCamera cam;                      // abstract camera
mjvOption opt;                      // visualization options
mjvScene scn;                       // abstract scene
mjrContext con;                     // custom GPU context
// ... load model and data
// init GLFW, create window, make OpenGL context current, request v-sync
glfwInit();
GLFWwindow* window = glfwCreateWindow(1200, 900, "Demo", NULL, NULL);
glfwMakeContextCurrent(window);
glfwSwapInterval(1);
// initialize visualization data structures
mjv_defaultCamera(&cam);
mjv_defaultPerturb(&pert);
mjv_defaultOption(&opt);
mjr_defaultContext(&con);
// create scene and context
mjv_makeScene(m, &scn, 1000);
mjr_makeContext(m, &con, mjFONTSCALE_100);
// ... install GLFW keyboard and mouse callbacks
// run main loop, target real-time simulation and 60 fps rendering
while( !glfwWindowShouldClose(window) ) {
  // advance interactive simulation for 1/60 sec
  //  Assuming MuJoCo can simulate faster than real-time, which it usually can,
  //  this loop will finish on time for the next frame to be rendered at 60 fps.
  //  Otherwise add a cpu timer and exit this loop when it is time to render.
  mjtNum simstart = d->time;
  while( d->time - simstart < 1.0/60.0 )
      mj_step(m, d);
  // get framebuffer viewport
  mjrRect viewport = {0, 0, 0, 0};
  glfwGetFramebufferSize(window, &viewport.width, &viewport.height);
  // update scene and render
  mjv_updateScene(m, d, &opt, NULL, &cam, mjCAT_ALL, &scn);
  mjr_render(viewport, &scn, &con);
  // swap OpenGL buffers (blocking call due to v-sync)
  glfwSwapBuffers(window);
  // process pending GUI events, call GLFW callbacks
  glfwPollEvents();
}
// close GLFW, free visualization storage
glfwTerminate();
mjv_freeScene(&scn);
mjr_freeContext(&con);
// ... free MuJoCo model and data
```

(The source excerpt calls `mjv_defaultPerturb(&pert)` without declaring
`pert`; declare an `mjvPerturb pert;` if you keep that line.)

## Cameras

`mjvCamera.type` takes an `mjtCamera` value:

| Type | Behaviour |
|----|----|
| `mjCAMERA_FREE` | Most common. Lookat point, distance, azimuth, elevation; no twist. Mouse hook: `mjv_moveCamera`. |
| `mjCAMERA_TRACKING` | Like free, but lookat follows the subtree CoM of body `trackbodyid` (with smoothing). Distance/azimuth/elevation stay user-controlled. |
| `mjCAMERA_FIXED` | Model camera `fixedcamid`. The visualizer cannot change it; it moves if attached to a moving body or tracking/targeting. |
| `mjCAMERA_USER` | Abstract camera ignored; low-level cameras untouched. Same as passing NULL. |

- `mjvScene` embeds two `mjvGLCamera`s, one per eye. Forward is the camera's
  -Z axis, up is +Y. The frustum stores the average of left/right edges; the
  real edges come from the viewport aspect ratio (1:1 pixels assumed).
- Eye distance is the ipd. From an abstract camera, ipd and `fovy` come from
  `mjModel.vis.global.ipd`/`fovy` (free, tracking) or
  `mjModel.cam_ipd`/`fovy` (model cameras).
- Without stereo (`mjvScene.stereo`), the two eye cameras are averaged.
- `mjv_camera2GLCamera` computes one `mjvGLCamera` without a scene.

## Selection

`mjv_select` returns the geom index at window coordinates (or -1) and the 3D
point. It calls `mj_ray`, which calls `mj_rayMesh`, `mj_rayHfield` and
`mju_rayGeom`; call those directly for custom picking (e.g. a VR controller
as a laser pointer). See `simulate.cc` for usage.

## Perturbations

You can always set `mjData.qfrc_applied` or `mjData.xfrc_applied` yourself.
With `mjvPerturb`:

1. Select a body; `mjv_initPerturb` sets the reference pose (`refpos`,
   `refquat`) to the body pose at onset, avoiding jumps.
2. Move the reference with the mouse hook `mjv_movePerturb`.
3. Apply it: `mjv_applyPerturbPose` moves the body directly (paused
   simulation or mocap body); `mjv_applyPerturbForce` writes a force to
   `xfrc_applied` of the selected body.

Pitfall: `mjv_applyPerturbForce` does not clear `xfrc_applied` of other
bodies. Clear it yourself, especially when the selection changes or several
sources apply perturbations. The visualizer draws the perturbation (a visual string
for the position offset, a rotating cube for the reference orientation);
forces are drawn when the matching `mjvOption` flag is on.

## Visualization options (`mjvOption`)

Consumed by `mjv_updateScene`, and read directly by the Filament renderer.

| Field | Meaning |
|----|----|
| `flags` | Indexed by `mjtVisFlag`: contact points/forces, joint/actuator axes, constraint violations, inertia boxes, convex hulls, skins, tendons, perturbation forces, ... |
| `geomgroup`, `sitegroup`, `jointgroup`, `tendongroup`, `actuatorgroup`, `flexgroup`, `skingroup` | Visibility by the element's `group` attribute |
| `label` (`mjtLabel`), `frame` (`mjtFrame`) | Which objects get text labels / which frames are drawn |
| `bvh_depth`, `flex_layer` | BVH level and 3D flex layer to show |

`mjv_defaultOption` makes groups 0, 1, 2 visible and sets flags to the
defaults in `mjVISSTRING`.

## Scene update

Call `mjv_updateScene` once per frame. Pass NULL for `mjvCamera` or
`mjvPerturb` to disable those features. It reads mjModel/mjData, builds
abstract `mjvGeom`s in `mjvScene.geoms` (not one-to-one with model geoms),
and copies up to `mjMAXLIGHT` lights (headlight at position 0 when present).

Finer control:

- `mjv_updateCamera` updates only the camera, not geoms or lights (e.g.
  moving the camera while paused).
- `mjv_camera2GLCamera` returns an `mjvGLCamera` without a scene (used for
  `mjrfRenderRequest.camera`).
- Append your own geoms to the end of the list.
- `mjv_addGeoms` adds the current state's geoms to the existing list (lights
  unchanged), filtered by an `mjtCatBit` mask:

| Category | Selects |
|----|----|
| `mjCAT_STATIC` | Geoms and sites of the world body (id 0) |
| `mjCAT_DYNAMIC` | Geoms and sites of other bodies |
| `mjCAT_DECOR` | Decorations: force arrows, skeletons, inertia boxes, ... |
| `mjCAT_ALL` | All of the above |

`mjv_updateScene` normally uses `mjCAT_ALL`: it clears the list and calls
`mjv_addGeoms`. To render a trajectory, render one frame with `mjCAT_ALL`
and the others with `mjCAT_DYNAMIC` (static objects repeated only cost GPU
time and cause aliasing); include `mjCAT_DECOR` if you want e.g. contact
force history.

## OpenGL rendering (`mjr`)

### OpenGL requirements

- OpenGL 1.5 compatibility profile with `ARB_framebuffer_object` and
  `ARB_vertex_buffer_object`. Symbols are loaded via GLAD on the first
  `mjr_makeContext`; MuJoCo works without OpenGL as long as no `mjr_`
  function is called.
- You must link a context-creation library and make an OpenGL context
  current on the calling thread. Linux supports GLX (X11 window), OSMesa
  (headless software) and EGL (headless hardware).

### Context lifecycle

``` C
mjModel* m;
mjrContext con;
// clear mjrContext only once before first use
mjr_defaultContext(&con);
// create window with OpenGL context, make it current
GLFWwindow* window = glfwCreateWindow(1200, 900, "Demo", NULL, NULL);
glfwMakeContextCurrent(window);
// ... load MuJoCo model
// make model-specific mjrContext
mjr_makeContext(m, &con, mjFONTSCALE_100);
// ... load another MuJoCo model
// make mjrContext for new model (old context freed automatically)
mjr_makeContext(m, &con, mjFONTSCALE_100);
// free context when done
mjr_freeContext(&con);
```

- `mjr_makeContext` uploads meshes, textures, fonts, shadow and offscreen
  FBOs; call it again for each new model (it frees the old one).
- Never call `mjr_defaultContext` after `mjr_makeContext`: it forgets the
  resources without freeing them.
- Never modify `mjrContext` directly; read-only access is fine (e.g. to blit
  the offscreen buffer into a VR SDK texture). Only `currentBuffer` changes
  after creation.
- Update GPU resources with `mjr_uploadTexture`, `mjr_uploadMesh`,
  `mjr_uploadHField` (e.g. video feeds, terrain); OpenGL names are reused.

### Buffers and offscreen rendering

- Two buffers: `mjFB_WINDOW` and `mjFB_OFFSCREEN` (`mjtFramebuffer`). Select
  with `mjr_setBuffer`; `mjr_makeContext` starts with the window. A missing
  buffer falls back to the other (headless Linux may have no window buffer).
- Window properties (resolution, double-buffering, stereo, multisampling,
  v-sync) are set by the OS/GLFW. The offscreen buffer uses the resolution
  and multisampling from `mjModel.vis`.
- `mjr_readPixels` / `mjr_drawPixels` move pixels between the active buffer
  and the CPU. `mjr_blitBuffer` copies on the GPU from the active to the
  inactive buffer (much faster; viewports may differ in size to scale).

### Drawing

- `mjr_render(viewport, &scn, &con)` draws `mjvScene.geom`. `mjr_maxViewport`
  gives the whole active buffer. Window size changes, so do not assume a
  fixed viewport.
- On scaled displays (notably macOS) use `glfwGetFramebufferSize` for the
  viewport, but `glfwGetWindowSize` to normalize mouse motion for the mouse
  hooks.
- `mjvOption` is already baked in; render flags live in `mjvScene.flags`
  (`mjtRndFlag`: wireframe, shadows, reflections, skybox, fog, ...). Shadows
  and reflections cost extra passes; disable them if needed.
- `mjvScene.stereo` (`mjtStereo`): `mjSTEREO_NONE` (averages both cameras,
  which must still be defined), `mjSTEREO_QUADBUFFERED` (window with
  quad-buffered OpenGL only; else falls back to side-by-side),
  `mjSTEREO_SIDEBYSIDE` (splits the viewport; works with most HMDs).
- 2D decorations: `mjr_overlay`, `mjr_text`, `mjr_rectangle`, `mjr_figure`.
  Draw custom OpenGL after `mjr_render`, which clears the viewport.
- `mjr_finish` (glFinish) and `mjr_getError` (glGetError) for sync and error
  checks.

## Filament rendering (`mjrf`)

- Optional library `mujoco_filament`, API in
  [mjrfilament.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjrfilament.h).
  Built on [Filament](https://github.com/google/filament) (OpenGL, Vulkan,
  Metal, WebGL).
- From source, set the CMake option `MUJOCO_USE_FILAMENT`. Add
  `MUJOCO_USE_FILAMENT_MJR_COMPAT` to replace the `mjr` functions with
  Filament implementations (no code changes; fewer features, slight
  overhead).
- Example: `RenderFilament()` in `render.cc`.

Offscreen outline (C++, using the support layer):

``` C
// create Filament context and scene
mjrfContextConfig context_cfg;
mjrf_defaultContextConfig(&context_cfg);
auto ctx = mujoco::CreateContext(context_cfg);
mjrfSceneParams scene_params;
mjrf_defaultSceneParams(&scene_params);
auto scene = mujoco::CreateScene(ctx.get(), scene_params);
mjrf_configureSceneFromModel(scene.get(), m);
// create retained model components and decoration helper
auto model_resources   = std::make_unique<ModelResources>(m, ctx.get());
auto model_lights      = std::make_unique<ModelLights>(scene.get(), model_resources.get());
auto model_renderables = std::make_unique<ModelRenderables>(scene.get(), model_resources.get());
auto model_decorations = std::make_unique<ModelDecorations>(ctx.get(), scene.get(), m);
// create offscreen render target
mjrfRenderTargetConfig target_cfg;
mjrf_defaultRenderTargetConfig(&target_cfg);
target_cfg.width        = width;
target_cfg.height       = height;
target_cfg.color_format = mjPIXEL_FORMAT_RGB8;
target_cfg.depth_format = mjPIXEL_FORMAT_DEPTH32F;
auto render_target      = mujoco::CreateRenderTarget(ctx.get(), target_cfg);
// update retained lights, renderables, and transient decorations from mjData
mjrRect viewport = {0, 0, width, height};
model_renderables->SetOptions(opt);
model_lights->Update(d);
model_renderables->Update(d);
model_decorations->Update(d, &opt, nullptr, &cam, viewport);
// submit render and pixel-readback requests and wait for completion
mjrfRenderRequest request;
mjrf_defaultRenderRequest(&request);
request.scene               = scene.get();
request.camera              = mjv_camera2GLCamera(m, d, &cam);
request.viewport            = viewport;
request.target              = render_target.get();
request.headlight    = m->vis.headlight.active;
request.headlight_intensity = model_lights->GetHeadlightIntensity();
mjrfReadRequest read_request;
mjrf_defaultReadRequest(&read_request);
read_request.target    = render_target.get();
read_request.output    = rgb.data();
read_request.num_bytes = width * height * 3;
mjrfFrameHandle frame = mjrf_render(ctx.get(), &request, 1, &read_request, 1);
mjrf_waitForFrame(ctx.get(), frame);
// remove transient decorations before destroying the scene
model_decorations->Clear();
```

### Core objects

Seven opaque types, each made with `mjrf_create*` and freed with
`mjrf_destroy*`: `mjrfContext`, `mjrfScene`, `mjrfMesh`, `mjrfTexture`,
`mjrfRenderable`, `mjrfLight`, `mjrfRenderTarget`. Creation structs come
from `mjrf_default*`: a `*Config` (context, texture, mesh, render target) is
fixed for the object's lifetime; `*Params` (scene, light, renderable) are
initial values changeable with `mjrf_set*`.

- **Context:** owns its graphics context (`mjrGraphicsApi` in
  `mjrfContextConfig`, optional window handle or headless software);
  independent of any mjModel.
- **Scene:** lights, renderables, optional skybox. Apply model options and
  `filament.*` flags with `mjrf_configureSceneFromModel`.
- **Meshes/textures:** uploaded via `mjrf_uploadMesh` / `mjrf_uploadTexture`
  (2D, cubemap, KTX) with an optional completion callback to free host
  memory; `mjrf_flush` flushes pending work and runs completed callbacks
  before the next `mjrf_render`.
- **Renderables:** geometry via `mjrf_setRenderableMesh` or a built-in
  primitive via `mjrf_setRenderableGeomMesh`; material via
  `mjrf_setRenderableMaterial` (`mjrfMaterial`: metallic-roughness PBR,
  specular-glossiness Phong, or unlit `decor`); per frame
  `mjrf_setRenderablePose`, `mjrf_setRenderableSize`,
  `mjrf_setRenderableCastShadow`. Add/remove with `mjrf_addSceneRenderable`
  / `mjrf_removeSceneRenderable`.
- **Lights:** directional, spot, point or image-based, via
  `mjrf_addSceneLight`; intensities in candela. The headlight is set on
  `mjrfRenderRequest` (in lux), so multiple cameras do not cross-illuminate.
- **Rendering:** `mjrf_render` takes a batch of `mjrfRenderRequest`s (scene,
  camera, viewport, target or NULL for the window, `mjrDrawMode`: default,
  no-textures, wireframe, depth, solver islands, segmentation; per-view
  flags) plus `mjrfReadRequest`s, returns an `mjrfFrameHandle`; wait with
  `mjrf_waitForFrame`. One scene can be rendered from many cameras/modes in
  one call.
- **Threading:** the API is not thread-safe; make all calls from one thread
  (it uses an internal render thread).

### Support layer

C++ in
[src/render/filament/support](https://github.com/google-deepmind/mujoco/blob/main/src/render/filament/support)
(RAII wrappers in `support/mjrf_ptr.h`), also in Python as `mujoco.mjrf`:

| Class | Role |
|----|----|
| `ModelResources` | Creates/owns meshes, hulls, heightfields and textures from mjModel; can re-upload modified assets |
| `ModelLights` | Creates/updates lights; adds fallback lighting; `GetHeadlightIntensity()` gives the value for the render request |
| `ModelRenderables` | Renderables for geoms, sites, skins, flexes, spatial tendons. `Update(data)` updates in place; `SetOptions(opt)` applies `mjvOption` visibility |
| `ModelDecorations` | Calls `mjv_updateScene` and converts `mjCAT_DECOR` geoms into temporary renderables. Text labels go to an optional callback passed to `Update()`; the app draws them (see `DrawBitmapText()` in `render.cc`) |

### Materials and lighting

- A material uses PBR if it defines any physical property (non-negative
  `metallic` or `roughness`, or PBR texture layers); otherwise Phong,
  rescaled by `filament.phong.specular_multiplier` (0.2),
  `phong.shininess_multiplier` (0.1), `phong.emissive_multiplier` (0.3).
- **Lighting switch (whole scene):** if any light has positive `intensity`,
  all lights are photometric (candela), lights at zero go dark, the
  headlight is off, and there is no ambient light unless an `image` light
  exists (`bulbradius` softens shadows). Otherwise a fallback environment
  light is added, the headlight is on, and a total intensity is split among
  lights: `fallback.environment_light_intensity` (5000),
  `fallback.scene_light_intensity` (80000),
  `fallback.head_light_intensity` (40000 lux).

### Rendering options (`filament.*` custom elements)

Set with MJCF `custom` numerics/text; read by
`mjrf_configureSceneFromModel`. Booleans are 0/1 numerics; enums are
strings.

``` xml
<custom>
  <numeric name="filament.clear_color" data="0.5 0.6 0.7 1"/>
</custom>
```

| Group | Flags (default) |
|----|----|
| Shadows | `shadows.type` ("pcf"; "vsm", "pcss"), `shadows.map_size` (min(shadowsize, 2048)) |
| SSAO | `ao.enabled` (1), `ao.quality`, `ao.low_pass_filter`, `ao.upsampling` ("ultra"), `ao.bent_normals` (0), `ao.ssct` (0) |
| Bloom | `bloom.enabled` (0), `bloom.strength`, `bloom.quality` ("low"), `bloom.levels` |
| Color grading | `cg.exposure` (0), `cg.temperature` (0), `cg.tint` (0), `cg.slope`/`offset`/`power` (ASC CDL), `cg.shadows`/`midtones`/`highlights`, `cg.tonal_ranges`, `cg.shadow_gamma`, `cg.mid_point`, `cg.highlight_scale`, `cg.contrast`/`vibrance`/`saturation` (1), `cg.tone_mapping` ("pbr_neutral"; "aces", "aces_legacy", "filmic", "linear"), `cg.output_color_space` ("srgb") |
| Fog | `fog.enabled` (0), `fog.color`, `fog.distance`, `fog.density`, `fog.cut_off_distance`, `fog.maximum_opacity`, `fog.height`, `fog.height_falloff` |
| Vignette | `vignette.enabled` (0), `vignette.midpoint` |
| Material | `material.base_color_type` ("srgb"; "linear") |
| Background | `clear_color` (0 0 0 1) |

Unlisted defaults are Filament's own. `filament.clear_color` is not read by
the library: apps rendering one scene (Studio, `mjr` compat mode) apply it
with `mjrf_setClearColor`; with your own render targets, set it yourself.

## Virtual reality

MuJoCo has no built-in VR app but supports VR in user code.

- The user moves the model relative to the room (model transformation in
  `mjvScene`, mouse hook `mjv_moveModel`). Using an abstract camera sets
  `mjvScene.enabletransform = 0` without clearing the parameters, so you can
  switch between VR and desktop modes.
- Only the `mjvGLCamera` parameters live in room space. Convert with
  `mjv_room2model`, `mjv_model2room`, `mjv_cameraInModel`,
  `mjv_cameraInRoom`.
- Head tracking: each frame, copy tracked eye poses into
  `mjvScene.camera[0]` (left) and `camera[1]` (right), and set the frustum
  from the display, outside `mjv_updateScene`.
- Controllers: map poses with `mjv_room2model` and drive mocap bodies
  (`mjData.mocap_pos`, `mocap_quat`), ideally coupled to regular bodies by
  soft equality constraints rather than direct contact.

## UI framework (`mjui`)

The native UI used by `simulate.cc`, drawn directly in OpenGL alongside the
classic renderer.

- Each UI is a virtual rectangle (can be taller than the window) rendered
  offscreen in auxiliary buffers, only when changed, then copied to the
  window on the GPU with scroll bars as needed.
- Layers: OpenGL rendering; pure virtual `PlatformUIAdapter` for windows,
  keyboard and mouse; `GlfwAdapter` implementation. Replace only
  `GlfwAdapter` to swap GLFW.
- Themes set colors and spacing; layout is automatic. Elements: check boxes,
  radio groups, selection lists, sliders, text edit boxes, static text,
  buttons, separators, grouped in collapsible sections.
- Visible rectangles (3D view, figures, custom) live in `mjuiState` and
  route mouse events; a user callback updates the layout.
- `mjUI` is one statically allocated struct; build it from `mjuiDef` tables
  (one row per element) or programmatically.
- Elements store pointers to user data (e.g. a slider on `d->qpos+7`):
  update the UI when the simulation changes and disable editing while it
  runs. `mjfItemEnable` callbacks enable/disable items by integer category.

| API | Purpose |
|----|----|
| `mjUI` | An entire UI |
| `mjuiState` | Global UI state |
| `mjuiDef` | One definition-table entry |
| `mjui_update` | Main update |
| `mjui_render` | Render the UI |
| `mjui_event` | Low-level event handler |
| `mjui_add` | Helper to construct a UI |

Signatures and struct fields: [api-functions](../../reference/api-functions/SKILL.md),
[api-types](../../reference/api-types/SKILL.md).

## Source docs

Verbatim copies, for details not covered above:

- [programming/visualization.md](references/programming-visualization.md)
- [programming/rendering.md](references/programming-rendering.md)
- [programming/ui.md](references/programming-ui.md)
