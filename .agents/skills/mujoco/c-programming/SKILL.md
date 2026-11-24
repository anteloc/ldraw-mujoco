---
name: c-programming
description: 'Using MuJoCo from C/C++: getting started, building from source and with Bazel, header files, versions and compatibility, naming conventions and the sample programs (testspeed, simulate, compile, basic, render). Use when writing or building native code against libmujoco, or when C-API conventions explain behaviour also seen from Python.'
---

# MuJoCo C/C++ Programming

Use this skill to write, build and link native code against the MuJoCo
library: get the pre-built distribution or build from source (CMake or Bazel),
pick the right headers, check versions, read the C API naming scheme, and run
or study the bundled sample programs (`testspeed`, `simulate`, `compile`,
`basic`, `render`). The core concepts (mjModel, mjData, mjSpec, MJCF) are in
the [parent skill](../SKILL.md).

## What the library is

MuJoCo is a dynamic library for Windows, Linux and macOS. It needs a
processor with AVX instructions. It exposes the full simulator through a
compiler-independent shared-memory C API, which can also be used from C++.

| Component | Language | Role |
|----|----|----|
| Engine | C | The simulator; all runtime computations. |
| Parser | C++ | Parses MJCF and URDF into an internal mjCModel C++ object, exposed to the user via mjSpec. |
| Compiler | C++ | Converts the mjCModel object into the mjModel C structure used at runtime. |
| Thread | C++, exposed in C | Thread pool for asynchronous tasks. Call `mju_threadpool` to enable it in MuJoCo. |
| Abstract visualizer | C | Graphics-library independent. Mouse hooks for camera and perturbation, selection, visualization options, list of abstract geometric entities. Shared by both renderers. |
| Rendering | C (classic, OpenGL 1.5) / C++ (Filament) | Two renderers; see [visualization-rendering](visualization-rendering/SKILL.md). |
| UI framework | C | Works with the classic OpenGL renderer. Own event mechanism and abstract keyboard/mouse hooks. Samples use it with GLFW; other window libraries work too. |

## Getting started with the pre-built distribution

1. Download a release from the
   [GitHub Releases page](https://github.com/google-deepmind/mujoco/releases).
   Builds exist for x86_64 and arm64 on Windows, Linux and macOS.
2. Extract it. There is no installer: a `.dmg` on macOS, a `.zip` on Windows,
   a `.tar.gz` on Linux.
3. Run a viewer from the `bin` directory to check it works:

``` Text
Windows:   mujoco_studio ..\model\humanoid\humanoid.xml
Linux:     ./mujoco_studio ../model/humanoid/humanoid.xml
```

Prefer the pre-built libraries unless you develop or modify core MuJoCo code.
They bundle the tested dependency versions, use tuned build flags, need
nothing beyond the standard C runtime, and hide every symbol outside the
public API, so they coexist with other libraries in the process (including
other versions of MuJoCo's dependencies).

Windows/Linux archive layout:

``` Text
bin     - dynamic libraries, executables, MUJOCO_LOG.TXT
doc     - README.txt and REFERENCE.txt
include - header files needed to develop with MuJoCo
model   - model collection
sample  - code samples and CMakeLists.txt needed to build them
```

- The only file created automatically is `MUJOCO_LOG.TXT` in the executable
  directory. It holds error and warning messages and can be deleted any time.
- You may reorganize the tree or install the dynamic libraries elsewhere;
  set the path accordingly.
- Rebuild the samples to verify your development environment, using the
  cross-platform
  [sample CMakeLists.txt](https://github.com/google-deepmind/mujoco/blob/main/sample/CMakeLists.txt),
  which builds them independently of the library itself.
- On macOS and Windows, MuJoCo Studio and `simulate` are also standalone
  desktop apps (`MuJoCoStudio.app` and `MuJoCo.app` in the `.dmg`;
  `bin\mujoco_studio.exe` and `bin\simulate.exe` in the `.zip`). See
  [studio-viewers](../studio-viewers/SKILL.md).
- On macOS the DMG contains `mujoco.framework` (dynamic library plus all
  public headers). In Xcode, import it as a framework dependency (works for
  Swift too). Building manually, use `-F` and `-framework mujoco` for the
  header search path and library search path.

To try MuJoCo with nothing installed, visit [mujoco.org](https://mujoco.org)
or drop models on [live.mujoco.org](https://live.mujoco.org) (WebAssembly
MuJoCo Studio).

## Building from source (CMake)

You need CMake and a working C++17 compiler.

1. `git clone https://github.com/google-deepmind/mujoco.git`
2. Create a build directory and `cd` into it.
3. `cmake $PATH_TO_CLONED_REPO` to configure.
4. `cmake --build .` to build.

Dependencies are fetched from upstream repositories over the Internet with
CMake's [FetchContent](https://cmake.org/cmake/help/latest/module/FetchContent.html).
This builds the library and all samples, but not the Python bindings (see
[python-bindings](../python-bindings/SKILL.md)).

To install:

1. Configure with `cmake $PATH_TO_CLONED_REPO -DCMAKE_INSTALL_PREFIX=<my_install_dir>`
2. After building, run `cmake --install .`

Notes:

- Build with `-DCMAKE_BUILD_TYPE=Release` for runtime performance.
- With MSVC, use Visual Studio 2019 or later and Windows SDK 10.0.22000 or
  later.
- On Windows, performance is best when building with Clang rather than MSVC.
- A working configuration is in the
  [CI setup](https://github.com/google-deepmind/mujoco/blob/main/.github/workflows/build.yml).

## Building with Bazel

Requires Bazel 8.0 or later. The tested version is pinned in
`.bazelversion`, which [Bazelisk](https://github.com/bazelbuild/bazelisk)
uses automatically. From the repository root:

``` shell
bazel build //...
bazel test //...
```

MuJoCo is not in the Bazel Central Registry yet. Depend on it from your own
`MODULE.bazel` with an override:

``` python
bazel_dep(name = "mujoco")
git_override(
    module_name = "mujoco",
    remote = "https://github.com/google-deepmind/mujoco.git",
    commit = "<commit>",
)
```

| Target | What it is |
|----|----|
| `@mujoco` | The MuJoCo library. Include headers as `#include <mujoco/mujoco.h>`. |
| `@mujoco//:mujoco_shared` | Shared library (`libmujoco.so`, `libmujoco.dylib` on macOS) exporting only the MuJoCo API. Add it to `dynamic_deps` of a `cc_binary` or `cc_shared_library` that depends on `@mujoco` to link dynamically, e.g. to share one copy with the Python bindings. |
| `@mujoco//plugin/<name>:register` | Bundled plugins (`<name>` is `actuator`, `elasticity`, `sdf` or `sensor`); they register themselves when linked in. |
| `@mujoco//python/mujoco` | Python bindings. |

Build your own plugin as a shared library with the `mujoco_plugin` macro. It
links against `@mujoco//:mujoco_shared` and exports no symbols. Load it at
run time with `mj_loadPluginLibrary`, which runs its registration code (see
[engine-plugins](engine-plugins/SKILL.md)):

``` python
load("@mujoco//plugin:mujoco_plugin.bzl", "mujoco_plugin")

cc_library(
    name = "my_plugin_lib",
    srcs = ["my_plugin.cc"],
    deps = ["@mujoco"],
    alwayslink = True,
)

# Builds libmy_plugin.so (libmy_plugin.dylib on macOS).
mujoco_plugin(
    name = "my_plugin",
    deps = [":my_plugin_lib"],
)
```

- Single precision (`mjUSESINGLE`): build with `--@mujoco//:single_precision`.
- The Bazel build is tested on Linux and macOS. It covers the library,
  `simulate`, the plugins, the samples and the core Python bindings.
- The `sample` directory is itself a standalone Bazel module depending on
  MuJoCo this way; use it as a template.

## Building the docs locally

Clone the repo, `cd mujoco/doc`, `pip install -r requirements.txt` (MuJoCo
Warp API docs need extra dependencies, see
[.readthedocs.yml](https://github.com/google-deepmind/mujoco/blob/main/.readthedocs.yml)),
`make html`, then open `_build/html/index.html`.

## Header files

Headers are identical on all platforms. Include `mujoco.h` in every program;
it includes all others except `mjxmacro.h` and `mjspecmacro.h`.

| Header | Contents |
|----|----|
| [mujoco.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mujoco.h) | Main header. All API functions and global variables. |
| [mjmodel.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjmodel.h) | `mjModel`, the runtime model. |
| [mjdata.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjdata.h) | `mjData`, the workspace all computations read from and write to. |
| [mjvisualize.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjvisualize.h) | Abstract visualizer types. |
| [mjrender.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjrender.h) | OpenGL renderer types. |
| [mjrfilament.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjrfilament.h) | Filament renderer types. |
| [mjui.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjui.h) | UI framework types. |
| [mjtype.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjtype.h) | Primitive types and enums, including `mjtNum` (`double` or `float`). |
| [mjspec.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjspec.h) | Enums and structs for procedural model editing ([model-editing](../model-editing/SKILL.md)). |
| [mjplugin.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjplugin.h) | Engine plugin data structures. |
| [mjmacro.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjmacro.h) | C macros useful in user code. |
| [mjxmacro.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjxmacro.h) | Optional, not included by `mujoco.h`. X Macros mapping all mjModel/mjData fields, e.g. into scripting languages. |
| [mjspecmacro.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjspecmacro.h) | Optional, not included by `mujoco.h`. X Macros for mjSpec and its element structs. |
| [mjexport.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjexport.h) | Symbol export macros. Do not use directly. |
| [mjsan.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjsan.h) | Definitions for sanitizer builds. |
| [mjassert.h](https://github.com/google-deepmind/mujoco/blob/main/include/mujoco/mjassert.h) | Compile-time size assertions for ABI stability across C and C++ compilers. |

Batched simulation functions (`mjb_`) are declared in `mujoco/mjbatch.h`.

## Versions and compatibility

If API function definitions changed between the version you wrote code for
and the one you link, the compiler or linker reports errors. Even when they
did not change, assert that header and library match. `mujoco.h` defines
`mjVERSION_HEADER`; the library provides `mj_version`:

``` C
// recommended version check
if (mjVERSION_HEADER != mj_version())
  complain();
```

- Only the main header defines `mjVERSION_HEADER`. Keep the headers of one
  release together; never mix headers across versions.
- Both values are integers, avoiding floating-point comparison problems.
- The encoding formula and version semantics are in
  [VERSIONING.md](https://github.com/google-deepmind/mujoco/blob/main/VERSIONING.md).

## Naming convention

Every API symbol starts with `mj`. The next character selects the family.

Type prefixes:

| Prefix | Family | Example |
|----|----|----|
| `mj` | Core simulation data structure (C struct). All-capitals after the prefix means a macro/`#define`. | `mjModel`; `mjMIN` |
| `mjt` | Primitive type, mostly enums | `mjtNum`, `mjtGeom` |
| `mjf` | Callback function type | `mjfGeneric` |
| `mjs` | Procedural model editing struct | `mjsJoint` |
| `mjv` | Abstract visualization struct | `mjvCamera` |
| `mjrf` | Filament rendering struct | `mjrfContext` |
| `mjr` | OpenGL rendering struct | `mjrContext` |
| `mjui` | UI framework struct | `mjuiSection` |

Function prefixes (always end with an underscore):

| Prefix | Family | Example |
|----|----|----|
| `mj_` | Core simulation. Almost all take pointers to mjModel and mjData as the first two arguments; outputs usually go to mjData. | `mj_step` |
| `mju_` | Utility; self-contained, no mjModel/mjData arguments | `mju_mulMatVec` |
| `mjv_` | Abstract visualization | `mjv_updateScene` |
| `mjrf_` | Filament rendering | `mjrf_render` |
| `mjr_` | OpenGL rendering | `mjr_render` |
| `mjui_` | UI framework | `mjui_update` |
| `mjcb_` | Global callback pointer; set it to your own function to install a callback | `mjcb_control` |
| `mjd_` | Derivatives | `mjd_transitionFD` |
| `mjs_` | Procedural model editing | `mjs_addJoint` |
| `mjb_` | Batched simulation (`mujoco/mjbatch.h`) | `mjb_step` |

The same names appear in the Python bindings, which explains behaviour seen
from Python; see [python-bindings](../python-bindings/SKILL.md).

## Code samples

The samples live in the `sample` directory (and `simulate` in its own
directory) of the distribution and repository.

### testspeed: time a model

Rolls out passive dynamics (with optional control noise) for N steps and
prints contacts, scalar constraints and CPU times from internal profiling.
For controlled dynamics, install `mjcb_control` or set controls explicitly
(see [simulation-loop](simulation-loop/SKILL.md)).

``` Shell
testspeed [options] model
```

| Option | Default | Meaning |
|----|----|----|
| `model` | (required) | path to model (positional argument) |
| `--nstep=N` | 10000 | number of steps per rollout |
| `--nthread=N` | 1 | number of threads running parallel rollouts |
| `--noisestd=X` | 0.01 | scale of pseudo-random noise injected into actuators |
| `--noiserate=X` | 0.1 | rate of convergence to ctrl keyframe/midpoint |
| `--nenginethread=N` | 0 | number of worker threads in engine-internal threadpool |
| `--solver=S` | Newton | override constraint solver algorithm (PGS, CG, Newton) |
| `--cone=C` | Pyramidal | override friction cone type (Pyramidal, Elliptic) |
| `--jacobian=J` | Auto | override constraint Jacobian type (Dense, Sparse, Auto) |
| `--integrator=I` | Euler | override integration mode (Euler, RK4, Implicit, ImplicitFast, Discrete) |
| `--iterations=N` | 100 | override solver iterations limit |
| `--tolerance=X` | 1e-8 | override solver convergence tolerance |
| `--sleep_tolerance=X` | 1e-4 | override sleep tolerance |
| `--noslip_iterations=N` | 0 | override noslip solver iterations limit |
| `--ctrl=PATH` | (none) | replay control trajectory from file instead of pseudo-random noise |
| `--format=F` | text | output format (text, json) |

- `--ctrl=PATH`: plain text, one row of `nu` whitespace- or comma-separated
  numbers per timestep; empty lines and `#` comments ignored; bypasses the
  noise options. Without `--nstep`, `nstep` is the row count; if `--nstep`
  exceeds it, the last row is held.
- `nthread > 1`: one mjModel, per-thread mjData, `nthread` identical parallel
  simulations (RL-style). Optimal value is usually the number of logical
  cores.
- A keyframe named `"test"`, if present, is the initial state; otherwise the
  reference configuration with zero velocities.
- Physics overrides (`--solver` etc.) apply only when given explicitly;
  otherwise the XML options are kept.
- Control noise keeps models from settling into a static state, which with
  warmstarts would give artificially fast timings.
- `nenginethread > 0` creates an engine-internal thread pool (workers in
  addition to the calling thread) for large scenes. Combining it with
  `nthread` is possible, but the use cases are usually mutually exclusive.
- For repeatable numbers use the Linux `performance` governor or the Windows
  `High Performance` plan, and pin to one core type (`taskset` on Linux,
  `start /affinity` on Windows; not possible via documented API on macOS).

### simulate: full interactive simulator

Opens an OpenGL window with GLFW and renders the simulation, with built-in
help, statistics, profiler and sensor plots, using the native UI framework.
Load a model from the command line or by drag-and-drop. Press `F1` for help.
Double-click selects; Ctrl+drag applies forces/torques to the selection;
plain drag moves the camera. The Python viewer (`mujoco.viewer`) uses the
same `Simulate` UI and shortcuts; stepping/pausing shortcuts do nothing in
passive mode. Hold the right mouse button over the UI to see each control's
shortcut.

Most-used keys:

| Key | Action |
|----|----|
| `Space` | Play / pause |
| `Right arrow` / `Left arrow` | Step forward / step back through history |
| `=` / `-` | Speed up / slow down |
| `Backspace` | Reset |
| `Ctrl L` | Reload the model (handy while editing XML) |
| `Ctrl C` | Copy state to clipboard |
| `Ctrl A` / `Esc` | Align free camera / switch to free camera |
| `[` / `]` | Cycle fixed cameras |
| `Page Up` | Select parent of selected body |
| `Tab` / `Shift Tab` | Toggle left / right UI panel |
| `F1` … `F7` | Help, info, profiler, sensor plots, fullscreen, frame vis, label vis |
| `Ctrl M` / `Ctrl D` | Print model to `MJMODEL.TXT` / data to `MJDATA.TXT` |
| `Ctrl P` / `Ctrl Q` | Screenshot / quit |
| `0` … `5` / `Shift 0` … `Shift 5` | Toggle geom / site group |
| `Alt` + letter | Expand/collapse section: `F` File, `O` Option, `S` Simulation, `W` Watch, `P` Physics, `R` Rendering, `V` Visualization, `G` Group enable, `L` Logging, `J` Joint, `C` Control, `E` Equality |

Visualization-flag keys follow `mjVISSTRING` (e.g. `H` convex hull, `J`
joint, `C` contact point, `F` contact force, `T` transparent, `M` center of
mass); rendering-flag keys follow `mjRNDSTRING` (`S` shadow, `W` wireframe,
`R` reflection, `L` additive, `K` skybox, `G` fog, `/` haze).

Mouse: left drag orbits; right drag pans vertically, `Shift` right drag
horizontally; scroll or middle drag zooms; right double-click centers on a
point; `Ctrl` right double-click tracks the selected body; `Ctrl` drag
rotates the selection; `Ctrl` (+`Shift`) right drag translates it in the
vertical (horizontal) plane.

Code structure: `main()` initializes MuJoCo and GLFW, opens a window and
installs mouse/keyboard callbacks. There is no render callback; the main loop
handles UI events and rendering, while simulation runs in a background thread
synchronized with the main thread. Callbacks drive the abstract visualizer's
camera and perturbation control. The profiler and sensor plots use
`mjr_figure`; the profiler reads mjData diagnostics and helps tune the
constraint solver.

Pitfall: on Windows, power settings may lower CPU frequency because
`simulate` sleeps to stay real-time, which makes profiler timings inaccurate.
Set the minimum processor state to 100%.

### compile: convert models

Runs the parser and compiler. Converts (MJCF, URDF, MJB) to (MJCF, MJB, TXT).

- MJCF output is by default the compiled values in a canonical subset of the
  format, so MJCF-to-MJCF yields a different file. With `savecompiled`
  "false" it is written as authored: notation kept, but not comments,
  `include` elements or parser-expanded elements (see
  [model-editing](../model-editing/SKILL.md)).
- TXT is a human-readable road-map in one-to-one correspondence with the
  compiled mjModel. MuJoCo cannot load it. `mj_printData` produces the
  equivalent for mjData (not done by the sample).
- With MJCF/URDF input and an empty output file, it compiles twice to show
  the impact of the compiler's asset cache, printing total time, asset
  processing wall time and per-category CPU times for meshes and textures.
  These come from the `mjtCTimer` fields via `mjs_getTimer`, readable after
  any `mj_compile`.

### basic: minimal interactive simulator

Takes the model file as a required argument, opens a GLFW OpenGL window,
renders at 60 fps and simulates in real time. Backspace resets. Left drag
rotates, right drag translates vertically, shift right drag horizontally,
scroll or middle drag zooms. It is the minimal illustration of the concepts
in [visualization-rendering](visualization-rendering/SKILL.md).

### render: headless offscreen rendering

Renders a model offscreen to one PNG or a stream of raw RGB24 frames
(`.rgb` file or stdout for `ffmpeg`). Supports the Filament backend
(`mjrf`, PBR) and the classic OpenGL renderer (`mjrContext`), without an
interactive window.

``` Shell
render model [output] [options]
```

| Option | Default | Meaning |
|----|----|----|
| `model` | (required) | path to model (positional) |
| `output` | (default) | `.png`, `.rgb`, or `-` for stdout; defaults to `<model>.png`, or `<model>.rgb` when `--duration > 0` |
| `--backend=B` | `filament` | `filament` or `classic` |
| `--width=N` / `--height=N` | 640 / 480 | image size in pixels |
| `--duration=T` | 0 | recording seconds (`0` = single frame) |
| `--fps=F` | 60 | frames per second when `--duration > 0` |
| `--camera=C` | (free) | camera name or integer index |
| `--lookat=X,Y,Z` | (center) | free camera lookat |
| `--distance=D` | (fit) | free camera distance |
| `--azimuth=A` | `90` | free camera azimuth (degrees) |
| `--elevation=E` | `-45` | free camera elevation (degrees) |
| `--key=K` | (none) | keyframe name or index to load first |
| `--steps=N` | 0 | simulation steps before rendering |
| `--geomgroup=G` | `111000` | 6-char string enabling geom groups 0-5 |
| `--sitegroup=S` | `111000` | 6-char string enabling site groups 0-5 |
| `--label=L` | (none) | label type, e.g. `geom`, `body`, `site` |
| `--frame=F` | (none) | frame type, e.g. `geom`, `body`, `site` |
| `--<visflag>=0|1` | (default) | flag from `mjVISSTRING`, e.g. `--joint=1`, `--contactpoint=1` |
| `--<rndflag>=0|1` | (default) | flag from `mjRNDSTRING`, e.g. `--shadow=0`, `--wireframe=1` |

Pipe a 5-second 60 fps video into `ffmpeg`:

``` Shell
render humanoid.xml - --duration=5 --fps=60 --width=1280 --height=720 | \
  ffmpeg -f rawvideo -pixel_format rgb24 -video_size 1280x720 -framerate 60 \
         -i - -pix_fmt yuv420p video.mp4
```

- No arguments, `--help` or `-h` prints help.
- With `-` as output, frames go to stdout and status messages to stderr.
- Both backends emit top-down RGB24 (row 0 at top); `ffmpeg` needs no `vflip`.
- Integer camera indices select fixed cameras in definition order.
- `--key` resets to that keyframe before kinematics and rendering; without
  it, a keyframe named `test` is used if present. `--steps` runs after the
  reset.
- `--label` takes a name from `mjLABELSTRING` or an index; `--frame` a name
  from `mjFRAMESTRING` (`world` too) or an index.

## Which subskill for which task

| Task | Subskill |
|----|----|
| Load a model, step, reset, set controls, read contacts, Jacobians, threads, errors/warnings | [simulation-loop](simulation-loop/SKILL.md) |
| Cameras, picking, perturbation, `mjv_updateScene`, OpenGL/Filament rendering, offscreen buffers, UI framework | [visualization-rendering](visualization-rendering/SKILL.md) |
| Custom actuators, sensors, passive forces, SDF collision, resource providers | [engine-plugins](engine-plugins/SKILL.md) |
| Build or edit models in code with mjSpec | [model-editing](../model-editing/SKILL.md) |
| Exact function signatures, struct fields, globals | [reference](../reference/SKILL.md) |

## Subskills

Read the one that matches your task:

- [simulation-loop](simulation-loop/SKILL.md): Running simulations with the MuJoCo API: initialization, the simulation loop, state and control (mjtState, qpos, qvel, ctrl), forward and inverse dynamics, multi-threading, changing mjModel at runtime, data layout and the internal stack, errors/warnings/logging, diagnostics, Jacobians (mj_jac), reading contacts (data.contact, mj_contactForce), sleeping islands and coordinate frames. Use when stepping, resetting, saving/restoring state, reading contact forces, computing Jacobians or diagnosing simulation warnings.
- [visualization-rendering](visualization-rendering/SKILL.md): Visualizing and rendering MuJoCo scenes: cameras (mjvCamera), selection and perturbation, visualization options (mjvOption), scene update (mjv_updateScene), OpenGL rendering (mjrContext, offscreen buffers), Filament rendering, virtual reality and the UI framework. Use when rendering images or video, configuring cameras or visual flags, picking objects, or building a custom viewer.
- [engine-plugins](engine-plugins/SKILL.md): Extending MuJoCo with engine plugins: plugin types (actuators, sensors, passive forces, SDF collision), registration, plugin configuration in MJCF, and resource providers. Use when adding custom physics, sensors or collision shapes through the plugin API.

## Source docs

Verbatim copies, for details not covered above:

- [programming/index.md](references/programming-index.md)
- [programming/samples.md](references/programming-samples.md)
