# MuJoCo Studio

**MuJoCo Studio** is a Python and C++ SDK for building interactive simulations, research tools, and custom visualizers that run in a native desktop window or in a web browser with no changes to user code. It is the next iteration of the [simulate](../programming/samples.md) application and [mujoco.viewer](../python.md), replacing the classic OpenGL renderer and fixed [mjUI](../programming/ui.md) panels with [Filament](../programming/rendering.md) physically based rendering, [Dear ImGui](https://github.com/ocornut/imgui) immediate-mode UI, and a modular plugin system.

## Quick Start

- **In the browser (zero install)**: Open [live.mujoco.org](https://live.mujoco.org) and drag-and-drop any `.xml`, `.mjb`, or `.mjz` model onto the canvas, or share a model URL via `?model=github:<org>/<repo>/<branch>/<path>` (see [MuJoCo Live](web_viewers.md)).

- **Standalone desktop app**: Download the [latest release](https://github.com/google-deepmind/mujoco/releases) and open `MuJoCoStudio.app` on macOS, `bin\mujoco_studio.exe` on Windows, or `bin/mujoco_studio` on Linux (see [Standalone Application](native_viewers.md)).

- **From the Python CLI**: Launch the Studio viewer in a [native window](native_viewers.md) or stream it headlessly to a [browser](web_viewers.md):

  ``` shell
  python -m mujoco.studio.viewer --model=humanoid.xml            # native desktop window
  python -m mujoco.studio.viewer --model=humanoid.xml --gfx=web  # headless web viewer
  ```

- **Inside a Python simulation loop**: Attach a non-blocking viewer (`launch_native.launch` or `launch_web.launch`) without locking `model` or `data`; see [custom_sim_loop.py](https://github.com/google-deepmind/mujoco/blob/main/python/mujoco/sample/studio/custom_sim_loop.py) and [Non-Blocking Mode](native_viewers.md).

## Overview

MuJoCo also ships self-contained [agent SKILL files](https://github.com/google-deepmind/mujoco/tree/main/doc/skills) under `doc/skills/`—including [mujoco-studio](https://github.com/google-deepmind/mujoco/blob/main/doc/skills/studio/SKILL.md) and [mujoco-gui](https://github.com/google-deepmind/mujoco/blob/main/doc/skills/gui/SKILL.md)—with idiomatic API patterns and common pitfalls for both developers and AI coding assistants.

- [Web Viewers](web_viewers.md)
- [Native Viewers](native_viewers.md)
- [Architecture](architecture.md)
- [Python Plugins](python_plugins.md)
- [C++](cpp.md)

### Core Components

MuJoCo Studio is organized around five building blocks shared across C++ and Python:

- **Studio Viewer Application**: The full-featured interactive visualizer, implemented as `mujoco::studio::App` ([app.h](https://github.com/google-deepmind/mujoco/blob/main/studio/app.h)) in [C++](cpp.md) and `studio_app.App` ([app/plugins.py](https://github.com/google-deepmind/mujoco/blob/main/python/mujoco/studio/app/plugins.py)) in [Python](python_plugins.md). It provides model loading, simulation history scrubbing, step controls, performance profiling, an integrated log and warning console, and scene hierarchy inspection.
- **Composable Plugins**: Modular components that extend the viewer UI, 3D scene, and physics stepping. In Python, the standard Studio UI ([studio_app.App](python_plugins.md)), real-time physics stepping ([StepControl](python_plugins.md)), and trajectory history recording ([SimHistory](python_plugins.md)) are themselves implemented as [ViewerPlugin and SimPlugin](python_plugins.md) subclasses communicating over non-blocking [message channels](architecture.md).
- **Immediate-mode UI**: Powered by [Dear ImGui](https://github.com/ocornut/imgui), the [immediate-mode GUI (IMGUI) paradigm](https://github.com/ocornut/imgui/wiki#about-the-imgui-paradigm) minimizes superfluous state duplication, state synchronization, and UI-side state retention—making it less error-prone than traditional retained-mode interfaces and well suited for fast iteration on dynamic visualization and debugging tools that directly reflect live simulation data. Rather than touching GPU state directly, widget calls output compact vertex buffers and draw command lists that can be rendered locally or streamed remotely (see [WebViewer](web_viewers.md)).
- **Running in the Browser**: Studio offers two web viewers: [MuJoCo Live](web_viewers.md) runs entirely in the browser and can be hosted on a static page, whereas [WebViewer](web_viewers.md) streams a host-driven Python simulation and UI to the browser with no GPU or display server required on the host.
- **Physically Based Rendering**: Hardware-accelerated physically based rendering (PBR) via [Filament](../programming/rendering.md) across OpenGL, Vulkan, and WebGL, plus headless and software rasterizers for automated testing. For background on Filament and physically based rendering theory, see the [Filament documentation](https://google.github.io/filament/), the online [Physically Based Rendering in Filament](https://google.github.io/filament/Filament.html) guide, and [Physically Based Rendering: From Theory to Implementation](https://www.pbr-book.org/).

### Legacy Visualizers

| Feature | Legacy [mujoco.viewer](../python.md) | MuJoCo Studio |
|----|----|----|
| **GUI Framework** | Fixed custom C [mjUI](../programming/ui.md) panels ([simulate](../programming/samples.md)) | Dockable [Dear ImGui](https://github.com/ocornut/imgui) windows (`studio_app.App` is the port of [simulate](../programming/samples.md)) |
| **3D Renderer** | Fixed-function [classic OpenGL](../programming/rendering.md) (`mjr_`) | [Filament](../programming/rendering.md) (OpenGL, Vulkan, WebGL, headless/software) |
| **Web Support** | None (requires local display or X11/VNC) | [MuJoCo Live](web_viewers.md) (standalone WASM) & Python [WebViewer](web_viewers.md) (streamed ImGui + WASM) |
| **Architecture** | Monolithic loop with coupled UI and physics | Composable [ViewerPlugin / SimPlugin](python_plugins.md) classes (Python) and [callback plugins](cpp.md) (C++) |
| **Synchronization** | Shared [mjModel](../APIreference/APItypes.md) / [mjData](../APIreference/APItypes.md) under `viewer.lock()` | [Message passing](architecture.md) in Python; internal physics mutex in C++ (`mujoco::studio::App`) |
| **Live Iteration** | Static model reload only | Model file watching and live Python plugin [hot reload](python_plugins.md) |
