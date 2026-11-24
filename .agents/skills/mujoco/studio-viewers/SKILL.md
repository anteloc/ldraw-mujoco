---
name: studio-viewers
description: 'MuJoCo Studio: web viewers (MuJoCo Live, WebViewer, browser sandboxing), native viewers (standalone app, Python NativeViewer, rendering backends), architecture (thread model, message passing), Python viewer and simulation plugins with lifecycle events and hot reload, and C++/WebAssembly builds. Use when viewing models interactively, embedding a viewer, or writing Studio plugins.'
---

# MuJoCo Studio viewers

Use MuJoCo Studio to view models interactively in a native window or a browser, attach a viewer to your own Python simulation loop, and extend the viewer with Python or C++ plugins. Studio is the successor of the [simulate](../c-programming/SKILL.md) app and the legacy [mujoco.viewer](../python-bindings/SKILL.md): it uses [Filament](../c-programming/visualization-rendering/SKILL.md) physically based rendering, [Dear ImGui](https://github.com/ocornut/imgui) immediate-mode UI and a modular plugin system. The same user code runs in a desktop window or a browser. Core MuJoCo concepts are in the [root skill](../SKILL.md).

MuJoCo also ships agent skill files for Studio: [mujoco-studio](https://github.com/google-deepmind/mujoco/blob/main/doc/skills/studio/SKILL.md) and [mujoco-gui](https://github.com/google-deepmind/mujoco/blob/main/doc/skills/gui/SKILL.md).

## Quick start

| Goal | How |
|---|---|
| Zero install | Open [live.mujoco.org](https://live.mujoco.org), drop a `.xml`, `.mjb` or `.mjz` model, or use `?model=github:<org>/<repo>/<branch>/<path>` |
| Desktop app | From a [release](https://github.com/google-deepmind/mujoco/releases): `MuJoCoStudio.app` (macOS), `bin\mujoco_studio.exe` (Windows), `bin/mujoco_studio` (Linux) |
| Python, native window | `python -m mujoco.studio.viewer --model=humanoid.xml` |
| Python, headless web viewer | `python -m mujoco.studio.viewer --model=humanoid.xml --gfx=web` |
| Inside your own Python loop | Non-blocking `launch_native.launch` or `launch_web.launch`; see [custom_sim_loop.py](https://github.com/google-deepmind/mujoco/blob/main/python/mujoco/sample/studio/custom_sim_loop.py) |

Studio vs. the legacy `mujoco.viewer`:

| Feature | Legacy `mujoco.viewer` | MuJoCo Studio |
|---|---|---|
| GUI | Fixed C `mjUI` panels | Dockable Dear ImGui windows (`studio_app.App` ports simulate) |
| Renderer | Classic OpenGL (`mjr_`) | Filament (OpenGL, Vulkan, WebGL, headless/software) |
| Web | None | MuJoCo Live (WASM) and Python WebViewer |
| Architecture | Monolithic loop | `ViewerPlugin` / `SimPlugin` (Python), callback plugins (C++) |
| Sync | Shared mjModel/mjData under `viewer.lock()` | Message passing (Python); internal physics mutex (C++) |
| Live iteration | Static model reload | Model file watching and Python plugin hot reload |

## Python native viewer (`NativeViewer`)

Renders the scene and UI in an SDL2 window or offscreen buffer.

**Blocking mode** (Studio drives the loop):

``` shell
python -m mujoco.studio.viewer \
  --model=path/to/model.xml \
  --gfx=opengl \
  --plugins=path/to/my_plugin.py \
  --hot_reload=all
```

``` python
from mujoco.studio import app as studio_app
from mujoco.studio import launch_native
from mujoco.studio import viewer_protocol

config = viewer_protocol.ViewerConfig(title='MuJoCo Studio', gfx='opengl')

launch_native.run(
    config,
    model_path='humanoid.xml',  # Or model=model, data=data for an in-memory model.
    plugins=[studio_app.App(), *studio_app.SIM_PLUGINS],
)
```

Pass `model_path=...` so UI **Reload** and model hot reload work (the model is loaded on the simulation thread); or pass `model=...` with optional `data=...`.

**Non-blocking mode** (attach to your loop, e.g. RL training, replay, tests). `launch_native.launch` is a context manager that starts the viewer on a daemon thread and returns a `ViewerHandle`:

``` python
import time
import mujoco
from mujoco.studio import app as studio_app
from mujoco.studio import launch_native

model = mujoco.MjModel.from_xml_path('humanoid.xml')
data = mujoco.MjData(model)

with launch_native.launch(plugins=[studio_app.App()]) as handle:
  while handle.is_running():
    tick = time.perf_counter()
    model, data = handle.sync(model, data)
    mujoco.mj_step(model, data)
    time.sleep(max(0.0, model.opt.timestep - (time.perf_counter() - tick)))
```

This loop has no simulation plugins, so no history recording and no pause/speed controls; see `custom_sim_loop.py` for wiring them.

Rules for a `ViewerHandle` loop:

- **Always rebind** `model, data = handle.sync(model, data)` each iteration. It returns new objects after UI Reload, a dropped file, or a plugin's `handle.set_model()`.
- `handle.sync()` **never sleeps**. Without `StepControl()`, step and pace yourself. With `*studio_app.SIM_PLUGINS`, `StepControl()` steps and paces inside `handle.sync()` during `StepEvent`.
- Mutate `model.opt` inside step-event handlers so diff-based sync forwards it.
- **macOS:** blocking mode works under `python`; non-blocking `launch_native.launch` requires `mjpython`. `launch_web` works under standard `python`.

### Rendering backends

Set `ViewerConfig.gfx` or `--gfx`:

| Value | Backend |
|---|---|
| `''` (default) | Platform default native Filament backend |
| `'opengl'` / `'vulkan'` | Hardware-accelerated window |
| `'opengl_headless'` | Offscreen OpenGL, no window (tests, offscreen rendering) |
| `'opengl_software'` / `'vulkan_software'` | Software rasterizer for GPU-less CI |
| `--gfx=web` (CLI) | Headless WebViewer instead of a native window |

On Linux, windows need X11: `'opengl'` is rejected under Wayland, and omitting `gfx` there falls back to `'opengl_headless'`.

## Web viewers

| | MuJoCo Live | Python `WebViewer` |
|---|---|---|
| What runs where | Whole C++ Studio compiled to WASM, client-side, static page | Python sim and plugins on the host (no GPU or display needed); browser rasterizes |
| Backgrounded tab | Pauses the simulation (`requestAnimationFrame` loop) | Only pauses rendering; host keeps simulating |
| Files | Dropped files/`.zip`/`.mjz` go to an in-memory VFS for the tab's lifetime | Dropped files upload over `/drop` to a host temp dir |
| Memory | Simulation and history in the WASM heap (4 GiB desktop, 512 MiB iOS) | Limit applies only to the browser render scene |

### MuJoCo Live

- Drop a `.xml`, `.mjb`, or self-contained `.mjz` / `.zip` on the canvas.
- `?model=<url>` accepts `https://`, `http://` or `github:`, e.g. <https://live.mujoco.org/?model=github:google-deepmind/mujoco/main/model/humanoid/humanoid.xml>. Dependencies (meshes, textures, `<include>`) are found via `mju_getXMLDependencies` and prefetched. An empty `?model=` opens a blank scene.
- Remote model servers must send `Access-Control-Allow-Origin` (as `raw.githubusercontent.com` does); with `COEP: require-corp`, assets also need a permissive `Cross-Origin-Resource-Policy`.
- Without COOP/COEP headers on a static host, or on iOS WebKit, it runs single-threaded and the *Threads* slider is disabled.

### WebViewer

Everything is served over one `http_port` (default `0` = first free port `>= 8080`). Set `open_browser=True` on `ViewerConfig` to open a tab.

``` python
from mujoco.studio import app as studio_app
from mujoco.studio import launch_web
from mujoco.studio import viewer_protocol

config = viewer_protocol.ViewerConfig(title='MuJoCo Studio')

launch_web.run(
    config,
    model_path='humanoid.xml',
    plugins=[studio_app.App(), *studio_app.SIM_PLUGINS],
)
```

Use `launch_web.launch` for non-blocking mode. `studio_app.App` is optional: omit it for a bare viewport defined by your plugins (see [slideshow.py](https://github.com/google-deepmind/mujoco/blob/main/python/mujoco/sample/studio/overview/slideshow.py)).

Streams (the host-to-browser protocol is fixed, independent of plugin messages):

- `/ui`: host runs all `BuildGuiEvent` handlers in a headless ImGui context and streams delta-compressed draw lists; browser input flows back.
- `/model`: compiled model (`.mjb`) and resources. Models announced via `PreloadModelEvent` are prefetched by content hash.
- `/state`: per-frame integration state, camera, `mjvOption`, `mjvPerturb`, `extra_geoms` (latest-wins); the browser runs *mj_forward* and renders with Filament WebGL 2.0.
- `/drop`: uploads dropped files and triggers `LoadModelEvent`.

Multi-viewer sessions: one **Controller** (`CONTROLLING`) owns `/ui`; others are **Spectators** (`SPECTATING`) with cameras `Free: tumble`, `Free: wasd` or `Follow Controller`. Spectators can **Request control** (FIFO queue) or **Steal Control**. **Max Spectators** is `0`–`32` (default `8`). An idle controller (90 s, with a queue) loses control; a spectator without heartbeat for 5 minutes is disconnected and reconnects on focus.

**Security:** WebViewer serves plain HTTP/WebSockets with no authentication or encryption, on all interfaces. Anyone reaching the port can take control, upload files and see logs and paths. Use it on `localhost`, trusted networks, or through `ssh -L 8080:localhost:8080`.

**Secure context:** `SharedArrayBuffer` (needed by the threaded WASM client) only works on `http://localhost`, `127.0.0.1` or `https://`. For a remote host, forward the port with `ssh -L 8080:localhost:8080` and open `http://localhost:8080`, or use an `https://` reverse proxy that forwards the COOP/COEP headers. WebViewer adds `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` itself.

**Persistent C++ state:** WASM modules and Python C++ extensions stay loaded across viewer sessions, so C++ globals and `static` state persist (and leak) across `deinit`/`init`, notebook cells and tests. Custom C++ plugins must reset their global state; WASM memory never shrinks until reload.

## Architecture

- Simulation and viewer run on separate threads with **no shared mutable state** (`SimEndpoint` ↔ `ViewerEndpoint`). The simulation thread owns the authoritative structs. After each step `ViewerHandle.sync()` sends `StateSnapshot(state, state_sig)` from *mj_getState* (`mjSTATE_INTEGRATION`); the viewer applies it with *mj_setState* and runs *mj_forward* on its own copy.
- Launchers run the viewer on a daemon thread; viewer exceptions are logged and re-raised on the simulation thread at `ViewerHandle.close()`.
- C++ desktop runs physics on a background thread; WASM runs everything sequentially in `requestAnimationFrame`.
- Shared C++ components under [studio/](https://github.com/google-deepmind/mujoco/tree/main/studio): `ux/` (panels, `interaction.h`, `imgui_widgets.h`; Python `mujoco.studio.ux`, GIL released), `sim/` (`StepControl`, `SimHistory`, `SimProfiler`, `ModelHolder`), `hal/` and `render/` (`FilamentRenderer`, `ModelScene`). Write components shared across C++, Python and the browser in C++.

### Messages

Defined in [messages.py](https://github.com/google-deepmind/mujoco/blob/main/python/mujoco/studio/messages.py). Name subclasses `*Snapshot` or `*Event`.

| Base | Channel | Delivery | Use for |
|---|---|---|---|
| `messages.Snapshot` | `SnapshotChannel`, one slot per type | Latest only | Continuous values (sliders, toggles, settings): `StateSnapshot`, `StepControlSnapshot`, `SimHistorySnapshot`, `MjOptionSnapshot`, `PerturbSnapshot` |
| `messages.Event` | `EventChannel`, FIFO | Every event, in order | Buttons, one-shot commands, partial updates: `ModelEvent`, `LoadModelEvent`, `StateEvent`, `KeyframeEvent`, `ResetEvent`, `SingleStepEvent`, `RequestPauseEvent`, `ThreadPoolEvent`, `HotReloadEvent` |

## Python plugins

Subclass and decorate methods with `@messages.handler` (the type annotation selects the message):

- `plugin.ViewerPlugin`: viewer thread; UI, input, 3D overlays. `self.viewer` gives the local `model`/`data`; send with `self.viewer.send_to_sim(...)`.
- `plugin.SimPlugin`: simulation thread; stepping, controllers, model/state mutation. `self.handle` gives authoritative `model`/`data`, `self.handle.set_model(...)`, `self.handle.send_to_viewer(...)`.

Pass instances via `plugins=[...]`, or files with `--plugins=my_plugin.py --hot_reload=all`.

``` python
from mujoco.studio.dear_imgui import dear_imgui as imgui
from mujoco.studio import messages, plugin


class StatusWindow(plugin.ViewerPlugin):

  @messages.handler
  def on_build_gui(self, _: messages.BuildGuiEvent) -> None:
    if imgui.Begin('Simulation Time'):
      if self.viewer.data is not None:
        imgui.TextUnformatted(f't = {self.viewer.data.time:.3f} s')
    imgui.End()
```

Patterns: full UI (`studio_app.App()` + `*studio_app.SIM_PLUGINS` + yours); minimal viewport (only your `ViewerPlugin`); custom stepping (replace `step_control.StepControl()` to drive [MJX](../accelerated-simulation/mjx/SKILL.md), [MuJoCo Warp](../accelerated-simulation/mujoco-warp/SKILL.md), RL envs or recordings). Samples: [python/mujoco/sample/studio/](https://github.com/google-deepmind/mujoco/tree/main/python/mujoco/sample/studio). For a feature needing UI and sim changes, pair both plugin types in one file and talk via custom messages.

`studio_app.App` is an ordinary `ViewerPlugin` (menu bar, hierarchy, inspector, options, profiler, timeline, status bar, Console). It dispatches `studio_app.InitEvent(app)` at startup.

### 3D overlays

In `UpdateEvent`, clear and fill `self.viewer.extra_geoms` with `mujoco.MjvGeom` built by *mjv_initGeom* / *mjv_connector* (per-frame, does not touch mjModel):

``` python
class VelocityCommandOverlay(plugin.ViewerPlugin):
  """Draws a 3D arrow above the torso showing the desired XY velocity."""

  def __init__(self, cmd_vel: tuple[float, float] = (1.0, 0.0)) -> None:
    self.cmd_vel = np.array([cmd_vel[0], cmd_vel[1], 0.0])

  @messages.handler
  def on_update(self, _: messages.UpdateEvent) -> None:
    self.viewer.extra_geoms.clear()
    if self.viewer.data is None or self.viewer.model.nbody < 2:
      return

    origin = self.viewer.data.xpos[1] + np.array([0.0, 0.0, 0.3])
    geom = mujoco.MjvGeom()
    mujoco.mjv_initGeom(
        geom,
        int(mujoco.mjtGeom.mjGEOM_ARROW),
        np.zeros(3),
        np.zeros(3),
        np.eye(3).flatten(),
        np.array([0.2, 0.8, 0.3, 0.9], dtype=np.float32),
    )
    mujoco.mjv_connector(
        geom,
        int(mujoco.mjtGeom.mjGEOM_ARROW),
        0.02,
        origin,
        origin + 0.5 * self.cmd_vel,
    )
    self.viewer.extra_geoms.append(geom)
```

Persistent scene objects go through `mujoco.mjrf` instead. Full sample: [ghost.py](https://github.com/google-deepmind/mujoco/blob/main/python/mujoco/sample/studio/ghost.py).

### Python scenes and custom stepping

These snippets assume `import time`, `import mujoco` and `from mujoco.studio import messages, plugin`.

``` python
class MyScene(plugin.SimPlugin):
  height: int = 5

  @messages.handler
  def on_load_model(self, event: messages.LoadModelEvent) -> bool:
    if event.path:
      return False  # Let ViewerHandle load --model or dropped files.
    spec = mujoco.MjSpec()
    ...  # Populate spec from self.height.
    self.handle.set_model(spec)
    return True

  @messages.handler
  def on_hot_reload(self, event: messages.HotReloadEvent) -> None:
    if self in event.plugins:
      self.handle.reload()
```

Use `self.handle.set_model(spec, watch=['robot.xml'])` so edits to base XMLs (and their includes/meshes) also reload. Sample: [python_scene.py](https://github.com/google-deepmind/mujoco/blob/main/python/mujoco/sample/studio/python_scene.py).

``` python
class CustomStepperPlugin(plugin.SimPlugin):
  """Applies PD joint torques and replaces default StepControl stepping."""

  kp: float = 50.0
  kd: float = 5.0

  @messages.handler
  def on_pre_step(self, event: messages.PreStepEvent) -> None:
    qpos_err = -event.data.qpos[: event.model.nu]
    qvel_err = -event.data.qvel[: event.model.nu]
    event.data.ctrl[:] = self.kp * qpos_err + self.kd * qvel_err

  @messages.handler(priority=messages.Priority.USER)
  def on_step(self, event: messages.StepEvent) -> bool:
    # Runs before StepControl (Priority.INTERNAL); returning True consumes StepEvent.
    mujoco.mj_step(event.model, event.data)
    time.sleep(event.model.opt.timestep)
    return True
```

Built-ins in `studio_app.SIM_PLUGINS`: `step_control.StepControl` (real-time *mj_step* in `StepEvent`, control noise, pause, single step) and `sim_history.SimHistory` (ring buffer recorded on `PostStepEvent`; `SimHistory(min_seconds=10.0)` records every Nth step to span at least that much time).

### Lifecycle events

| Viewer thread | When |
|---|---|
| `ViewerInitEvent(viewer)` | Startup; `self.viewer` cached |
| `ModelEvent(model, path)` | Sim published a model; viewer copies it, runs *mj_forward*, clears `extra_geoms` |
| `PostModelEvent(model, data, path)` | Viewer model/data ready: reset plugin state here |
| `PreloadModelEvent(model)` | Hint of an upcoming model |
| `HotReloadEvent(plugins)` | Between frames after a class swap |
| `UpdateEvent()` | Every frame: visuals, `extra_geoms`, GUI data, `viewer.upload_image` |
| `BuildGuiEvent()` | Right after `UpdateEvent`: submit widgets only |
| `ExitEvent(reason)` | Shutdown: release resources, never return `True` |

| Simulation thread | When |
|---|---|
| `SimInitEvent(handle)` | In `ViewerHandle.__init__`; `self.handle` cached |
| `LoadModelEvent(path)` | Startup, Reload, model hot reload, drop; return `True` to supply your own model |
| `ModelEvent` / `PostModelEvent` | After `set_model(...)` or a new object in `sync`; reset state in `PostModelEvent` |
| `HotReloadEvent(plugins)` | Inside `handle.sync()` |
| `PreStepEvent(model, data)` | After viewer resets/overrides/perturbations: controls, forces, `model.opt`, `set_model` |
| `StepEvent(model, data)` | Advance physics |
| `PostStepEvent(model, data)` | Before `StateSnapshot` is sent |
| `ExitEvent(reason)` | In `ViewerHandle.close()`; never return `True` |

### Sync, priorities, return values

- Bidirectional snapshots must be sent only by the side that changed them. Wrap edits in `send_if_changes(*make_messages)` (on `Viewer` and `ViewerHandle`); each zero-arg lambda is evaluated before and after:

  ``` python
  with self.viewer.send_if_changes(
      lambda: messages.StepControlSnapshot.from_step_control(self.step_control_state),
      lambda: messages.MjOptionSnapshot(opt=copy.deepcopy(self.model.opt)),
  ):
    ux.build_options_gui(self.model, self.viewer.vis_options)
  ```

- Priorities run highest first: `Priority.CRITICAL` (1000), `Priority.USER` (100, default), `Priority.LIBRARY` (10), `Priority.INTERNAL` (1, `StepControl`, `SimHistory`, `Viewer`, `ViewerHandle`). Prefer lifecycle phases; use priority only to override a handler of the same event.
- Returning `True` consumes the message. Otherwise return `None`/`False`.

### Best practices

- Viewer: treat `self.viewer.model`/`data` as read-only. Never load or compile models on the viewer thread; send `LoadModelEvent` or a custom event to a `SimPlugin`. Keep the viewer at 60 Hz (slow handlers drop frames and stall WebViewer heartbeats).
- GUI: one or two `imgui.Begin(...)` windows per plugin; prepare data in `UpdateEvent`; use `##` to disambiguate labels and `###` for stable IDs (`f'Bodies ({n})###Bodies'`); prefer `imgui.BeginTable`; virtualize long lists with `imgui.ListClipper`; use `imgui.GetStyleColorVec4(imgui.Col.Text)`; check `not imgui.GetIO().WantCaptureKeyboard` for shortcuts; try `imgui.ShowDemoWindow()`.
- WebViewer drag tools: make the host capture the mouse (window with `imgui.InvisibleButton`, or `imgui.SetNextFrameWantCaptureMouse(True)`); set camera mode via `self.viewer.camera`.
- Sim: mutate `self.handle.model`/`data` only on the sim thread; republish structural changes via `self.handle.set_model(new_model, path=self.handle.model_path)`; edit `model.opt`/`data` inside step events; pace your own `StepEvent` if you drop `StepControl`; `.copy()` NumPy views you keep.

### Hot reload

`--hot_reload=all` or `ViewerConfig(hot_reload='all')`. Scope: `'all'`, `'plugins'`, `'model'`, or class names like `'VelocityCommandOverlay'` / `'model,App'`. Saving a plugin file (or a helper in its directory) swaps `plugin.__class__` in place, keeping state, camera, layout and browser connections, then dispatches `HotReloadEvent`. Saving the model, `watch` files or their assets calls `handle.reload()`. Errors keep the old code/model running. Framework modules, `__main__`, C++ code and the set of plugin instances do not reload.

## C++

Build from the repo root:

``` shell
bash .github/workflows/build_steps.sh build_studio_cpp_viewer
./build_host/bin/mujoco_studio model/humanoid/humanoid.xml
```

Or run [studio/build.sh](https://github.com/google-deepmind/mujoco/blob/main/studio/build.sh) (supports Git Bash on Windows, `debug`/`configure`/`build` arguments and `CMAKE_ARGS`), or configure CMake manually:

``` shell
cmake -B build-studio \
  -DCMAKE_BUILD_TYPE=Release \
  -DUSE_STATIC_LIBCXX=OFF \
  -DBUILD_SHARED_LIB=OFF \
  -DMUJOCO_USE_FILAMENT=ON \
  -DMUJOCO_BUILD_EXAMPLES=OFF \
  -DMUJOCO_BUILD_SIMULATE=OFF \
  -DMUJOCO_BUILD_TESTS=OFF \
  -DMUJOCO_TEST_PYTHON_UTIL=OFF \
  -DMUJOCO_WITH_USD=OFF \
  -DMUJOCO_BUILD_STUDIO=ON \
  -DFILAMENT_SKIP_SAMPLES=ON \
  -DCMAKE_CXX_FLAGS=-Wno-error=deprecated-declarations \
  -DFILAMENT_SHORTEN_MSVC_COMPILATION=OFF
cmake --build build-studio --config Release --target mujoco_studio --parallel
./build-studio/bin/mujoco_studio model/humanoid/humanoid.xml
```

Fonts and Filament assets are resolved relative to the executable. The app accepts a model path (positional or `--model_file`) and `--gfx` (`opengl`, `opengl_headless`, `opengl_software`, `vulkan`, `vulkan_software`).

Embed with `mujoco::studio::LaunchStudio(argc, argv, config)` ([launcher.h](https://github.com/google-deepmind/mujoco/blob/main/studio/launcher.h)) after `absl::ParseCommandLine`. Plugins are POD structs with function pointers ([ux/plugin.h](https://github.com/google-deepmind/mujoco/blob/main/studio/ux/plugin.h)), registered by value with `mujoco::studio::RegisterPlugin(plugin)`; keep state in `void* data`, do not subclass:

| Struct | Callbacks |
|---|---|
| `GuiPlugin` | `update(GuiPlugin* self)` |
| `ScenePlugin` | `enhance_scene(ScenePlugin* self, const mjModel* model, mjData* data, mjvScene* scene)` |
| `ModelPlugin` | `get_model_to_load`, `post_model_loaded`, `do_update`, `pre_step`, `post_step` |
| `KeyHandlerPlugin` | `on_key_pressed(KeyHandlerPlugin* self)` |
| `SpecEditorPlugin` | `pre_compile`, `post_compile` (`true` from `pre_compile` recompiles) |

``` C++
#include "absl/flags/parse.h"
#include <imgui.h>
#include <mujoco/mujoco.h>
#include "studio/launcher.h"
#include "studio/ux/plugin.h"

struct TelemetryState {
  float gain = 1.0f;
};

void RegisterTelemetryPlugin() {
  static TelemetryState state;

  mujoco::studio::GuiPlugin gui_plugin;
  gui_plugin.name = "Telemetry";
  gui_plugin.active = true;
  gui_plugin.data = &state;
  gui_plugin.update = [](mujoco::studio::GuiPlugin* self) {
    auto* s = static_cast<TelemetryState*>(self->data);
    ImGui::SliderFloat("Gain", &s->gain, 0.0f, 10.0f);
  };
  mujoco::studio::RegisterPlugin(gui_plugin);
}

// Option A: Register automatically when linked or loaded as a plugin library.
mjPLUGIN_LIB_INIT(telemetry_plugin) {
  RegisterTelemetryPlugin();
}

// Option B: Register explicitly in a custom executable before LaunchStudio.
int main(int argc, char** argv) {
  absl::ParseCommandLine(argc, argv);
  RegisterTelemetryPlugin();

  mujoco::studio::LauncherConfig config;
  config.title = "Custom Studio";
  config.model_file = "path/to/robot.xml";
  return mujoco::studio::LaunchStudio(argc, argv, config);
}
```

**WebAssembly:** MuJoCo Live compiles `mujoco::studio::App` with Emscripten ([emscripten.cc](https://github.com/google-deepmind/mujoco/blob/main/studio/emscripten.cc)). JavaScript drives it via Embind: `init`, `loadFile`, `loadUrl`, `loadKeyframe`, `renderFrame`, `deinit`. Resource providers handle `http:`, `https:` and `github:` URLs.

## Source docs

Verbatim copies, for details not covered above:

- [studio/index.md](references/studio-index.md)
- [studio/web_viewers.md](references/studio-web_viewers.md)
- [studio/native_viewers.md](references/studio-native_viewers.md)
- [studio/architecture.md](references/studio-architecture.md)
- [studio/python_plugins.md](references/studio-python_plugins.md)
- [studio/cpp.md](references/studio-cpp.md)
