---
name: interop
description: 'MuJoCo integrations with other tools: the Unity plug-in (installation, importing MJCF, design and implementation notes) and OpenUSD support (building with USD, mjcPhysics schemas, the MJCF file format plugin, importing USD into MJCF and exporting to USD). Use when moving MuJoCo models to or from Unity or USD pipelines.'
---

# Interop: Unity and OpenUSD

This skill covers moving MuJoCo models in and out of two outside ecosystems. The **Unity plug-in** lets the Unity Editor and runtime use MuJoCo physics on imported MJCF scenes. **OpenUSD support** loads USD assets into MJCF, describes MuJoCo physics in USD with the `mjcPhysics` schemas, opens MJCF files in USD tools, and exports MuJoCo scenes to USD.

> OpenUSD support is experimental and changes often.

## OpenUSD

### Install

The quickest path is prebuilt bindings. They exist for Python 3.11–3.13 on Linux `x86_64`, Windows `x86_64` and macOS `arm64`:

```shell
pip install mujoco-usd
# or
pip install mujoco[usd]
```

Installing `mujoco-usd` registers the `usd_decoder` plugin automatically when `mujoco` is imported.

On other platforms, or to use your own USD, build MuJoCo against USD. These steps assume MuJoCo is cloned to `~/mujoco`. To build USD with only the needed features:

```bash
cd ~/mujoco
cmake -Bcmake/third_party_deps/openusd/build cmake/third_party_deps/openusd
cmake --build cmake/third_party_deps/openusd/build
```

Or build it yourself with USD's script. Install it outside the repository:

```bash
git clone https://github.com/PixarAnimationStudios/OpenUSD
python OpenUSD/build_scripts/build_usd.py /path/to/my_usd_install_dir
```

Then enable USD in MuJoCo. Add `-Dpxr_DIR` only for a USD you built yourself:

```bash
cd ~/mujoco
cmake -Bbuild -S. -DMUJOCO_WITH_USD=True
# or, with a pre-built USD:
cmake -Bbuild -S. -DMUJOCO_WITH_USD=True -Dpxr_DIR=/path/to/my_usd_install_dir
cmake --build build -j 64
```

After that, the [simulate](../c-programming/SKILL.md) app (`simulate`) accepts drag-and-dropped `.usd`, `.usda`, `.usdc` and `.usdz` files.

### Import USD into MJCF

Reference a USD file from `<asset>` with a `<model>` whose `content_type` is `text/usd`:

```xml
<mujoco>
  <asset>
    <model file="chair.usdz" name="chair" content_type="text/usd"/>
  </asset>

  <worldbody>
    ...
  </worldbody>
</mujoco>
```

This needs `mujoco-usd` or a USD-enabled build. Physics comes mainly from the standard [UsdPhysics](https://openusd.org/dev/api/usd_physics_page_front.html) schemas, and `mjcPhysics` adds the MuJoCo-specific parts. The docs do not cover how to place or attach the imported model in `<worldbody>`. See the [XML reference](../reference/xml-reference/SKILL.md).

### Export to USD

| Route | When | Notes |
|---|---|---|
| `mujoco.usd.writer`, `mujoco.usd.layer_sink` (from `mujoco-usd`) | Python 3.11–3.13 on the platforms above | Native C++ USD stage authoring and trajectory recording, using the `mjcPhysics` schemas. |
| `USDExporter` in the [Python bindings](../python-bindings/SKILL.md) | Any platform or Python version | Pure Python. Needs only `usd-core` and `pillow`. Exports scenes and trajectories. |
| [Newton mujoco-usd-converter](https://github.com/newton-physics/mujoco-usd-converter) | Converting MJCF assets to standalone USD with strict authoring guidelines | Output does not reference the source MJCF. It uses `mjcPhysics` and has no MJCF-to-USD conversion cost at runtime. |

The docs say export is under active development and expected to go mainly through the Python API. They do not show function signatures for `mujoco.usd.writer`, `layer_sink` or `USDExporter` on these pages.

### MJCF file format plugin (MJCF as a USD layer)

An `SdfFileFormat` plugin lets USD-aware tools read MuJoCo `.xml` files as if they were USD. Install it by building with USD as above. With it you can:

1. Reference MJCF from a USD scene with references or payloads.
2. Open, inspect and render MJCF in `usdview` and other USD tools.
3. Use it as a base for converting MJCF to persistent `.usda`/`.usdc`.

```usd
#usda 1.0
(
    upAxis = "Z"
)

def Xform "world"
{
    def "robot" (
        prepend references = @./my_robot.xml@
    )
    {
    }
}
```

```bash
usdview my_robot.xml
```

```python
from pxr import Usd

# Load an MJCF file as a USD stage
stage = Usd.Stage.Open('my_robot.xml')

if stage:
    print(f"Successfully opened {stage.GetRootLayer().identifier}")
    # You can now inspect the stage as any other USD stage
    for prim in stage.TraverseAll():
        print(prim.GetPath())
else:
    print("Failed to open MJCF file")
```

### mjcPhysics schemas

`mjcPhysics` extends UsdPhysics and does not replace it. It adds new types only where needed. Use it codeless or with its C++ bindings. The code is pre-generated with `usdGenSchema` in [src/experimental/usd/mjcPhysics](https://github.com/google-deepmind/mujoco/tree/main/src/experimental/usd/mjcPhysics).

API schemas (applied to existing prims):

| Schema | Apply to | Purpose |
|---|---|---|
| `MjcSceneAPI` | an existing `UsdPhysicsScene` prim | Global options. `mjc:option` maps to `<option>`, `mjc:flag` to `<option/flag>`, `mjc:compiler` to `<compiler>`. |
| `MjcSiteAPI` | `UsdGeomSphere`, `UsdGeomCapsule`, `UsdGeomCylinder`, `UsdGeomCube` | Defines a MuJoCo site. |
| `MjcImageableAPI` | visual-only prims | Purely visual entities (`contype = conaffinity = 0`). |
| `MjcCollisionAPI` | collision prims, with `UsdPhysicsCollisionAPI` | Extra collision attributes. |
| `MjcMeshCollisionAPI` | mesh collision prims, with `UsdPhysicsMeshCollisionAPI` | Extra mesh collision attributes. |
| `MjcJointAPI` | `UsdPhysicsJoint` prims | Fully describes MuJoCo joints. |
| `MjcMaterialAPI` | physics materials (extends `UsdPhysicsMaterialAPI`) | Physical material attributes. |

Type schemas:

| Type | MJCF equivalent | Notes |
|---|---|---|
| `MjcActuator` | actuator | Targets a joint, body or site through a relationship. It does not use `UsdPhysicsDriveAPI`, because those concepts do not map closely. |
| `MjcKeyframe` | `<keyframe>` | The `time` attribute becomes USD timeSamples. Value order follows a depth-first traversal of rigid bodies in the composed stage. |
| `MjcTendon` | `<tendon>` (fixed and spatial) | The path is the ordered `mjc:path` relationship. Per-target data becomes indexed arrays such as `mjc:sideSites` and `mjs:path:divisors`. |

Learn more about USD: [Remedy's Book of USD](https://remedy-entertainment.github.io/USDBook), [OpenUSD docs](https://openusd.org/release/intro.html), [NVIDIA USD resources](https://developer.nvidia.com/usd).

## Unity plug-in

### Install

1. Clone the [mujoco repo](https://github.com/google-deepmind/mujoco/tree/main/unity) and check out the tag that matches your engine version (`git checkout 3.X.Y`). `main` may not match the latest release binary.
2. In Unity's Package Manager, import the `unity` directory's `package.json`. This brings in the C# code.
3. Provide the native library from the [platform release archive](https://github.com/google-deepmind/mujoco/releases). On Unity 2020.2 and later, the Package Manager finds and copies it on import. Otherwise copy and rename it into the package directory, or anywhere under `Assets`:

| OS | Source file | Rename to |
|---|---|---|
| macOS | `/Applications/MuJoCo.app/Contents/Frameworks/mujoco.framework/Versions/Current/libmujoco.4.0.2.dylib` (run MuJoCo.app once first so it is trusted) | `mujoco.dylib` |
| Linux | `~/.mujoco/mujoco-4.0.2/lib/libmujoco.so.4.0.2` (after extracting the `tar.gz` to `~/.mujoco`) | `libmujoco.so` |
| Windows | `MuJoCo\bin\mujoco.dll` (after extracting the `zip` to `MuJoCo` in your user directory) | (keep name) |

Tutorials and an example project: [mj-unity-tutorial](https://github.com/Balint-H/mj-unity-tutorial).

### Use

- **Import:** in the *Asset* menu, choose "Import MuJoCo Scene" and pick the MJCF XML.
- **Geom context menu:** "Add mesh renderer" adds a `MeshRenderer` and an `MjMeshFilter` that rebuilds a procedural mesh when the shape changes. "Convert to free object" works on world geoms only (no `MjBody` parent). It adds a parent `MjBody` and a sibling `MjFreeJoint`.
- **Collider context menu:** "Add a matching MuJoCo geom". Rigidbody, ArticulationBody and Joint setups still have to be rebuilt by hand.
- **Mouse spring:** with an `MjBody` selected, control-left-drag in the Scene view pulls the body toward the cursor. Add shift to project on the world X–Z plane.

### Rules and pitfalls

- Turn on "Error Pause" in the console. After a compile or runtime error, the system state is undefined.
- Give each GameObject **at most one** MuJoCo component. The GameObject hierarchy defines the model hierarchy.
- Component fields map directly to MJCF attributes, so read the [XML reference](../reference/xml-reference/SKILL.md) for their meaning.
- Unlike PhysX, a body moves only if it has an explicit joint.
- There are no trigger colliders. To detect contact, add a touch sensor and read its `SensorReading` (the normal force).
- Unity is left-handed with Y up and MuJoCo is right-handed with Z up, so vectors are swizzled. Skewed cylinders and capsules do not collide (skewed spheres become ellipsoids). Gizmos show the unskewed physics shape.
- Changing component fields at runtime does nothing until the next scene recreation.
- Adding or removing MuJoCo components recreates the whole scene, which is expensive for big models. [mjSpec](../reference/api-types/SKILL.md) editing is not supported yet.
- Gravity comes from Unity's physics settings, and the timestep from the Time Manager's *Fixed Timestep*. Unity handles appearance (meshes, materials, textures, RGBA as material assets).
- MJCF scenes that use [MuJoCo plugins](../c-programming/engine-plugins/SKILL.md) cannot be loaded yet.
- Mesh collisions use the qhull convex hull, which is not shown in Unity. Height fields are Unity terrain objects (the geom context menu adds one) and stay synced with the simulation.

### How it works

- **Importer:** loads the MJCF in MuJoCo and saves it to a temporary file, then imports that file. This validates it against the [schema](../reference/xml-reference/SKILL.md), validates and imports assets, creates materials for geom RGBA, and resolves `<include>`. `<default>` classes are applied and then discarded.
- **Runtime import:** `MjImporterWithAssets` subclasses `MjcfImporter`. `MjcfImporter` turns an MJCF string into components at play time without calling the MuJoCo library, which helps for procedural models or conversion to PhysX or URDF. It ignores all assets (including collision meshes) and all visuals.
- **MjScene:** collects every `MjComponent`, builds one MJCF (Unity poses become `qpos0`), compiles `mjModel`/`mjData` and binds each component by `MjComponent.MujocoId`. `MjScene.FixedUpdate()` calls `mj_step` and syncs transforms. It is added automatically at start if the scene has MuJoCo components. If your initialization ticks physics while adding components, call `MjScene.CreateScene()` when it ends.
- **Recreation:** caches joint positions and velocities, resets to `qpos0`, regenerates the XML with the same `qpos0`, and restores the state of joints that still exist.
- **Global Settings component:** holds the [`<option>`](../reference/xml-reference/SKILL.md) and `<size>` singletons (and later `<compiler>`).
- **External driver:** Unity steps the simulation. An external process can still drive it by setting `qpos`, calling `mj_kinematics` and syncing transforms. For the communication, use [ML-Agents](https://github.com/Unity-Technologies/ml-agents).

### Sensor components

Sensors are grouped by object type and data type:

| Class | Sensors |
|---|---|
| ActuatorScalar | `actuatorpos`, `actuatorvel`, `actuatorfrc` |
| BodyVector | `subtreecom`, `subtreelinvel`, `subtreeangmom`, frame vectors |
| JointScalar | `jointpos`, `jointvel`, `jointlimitpos`, `jointlimitvel`, `jointlimitfrc` |
| SiteScalar | `touch`, `rangefinder` |
| SiteVector | `accelerometer`, `velocimeter`, `force`, `torque`, `gyro`, `magnetometer`, frame vectors |
| Body/Geom/Site Vector | `framepos`, `framexaxis`, `frameyaxis`, `framezaxis`, `framelinvel`, `frameangvel`, `framelinacc`, `frameangacc` |
| Body/Geom/Site Quaternion | `framequat` |

Not implemented yet: `tendonpos`, `tendonvel`, `ballquat`, `ballangvel`, `tendonlimitpos`, `tendonlimitvel`, `tendonlimitfrc`, `user`.

Note: the source's sensor table lists `rangefinder` under Site/Scalar, but its reverse table has no plugin class for it.

## Source docs

Verbatim copies, for details not covered above:

- [unity.md](references/unity.md)
- [OpenUSD/index.md](references/OpenUSD-index.md)
- [OpenUSD/building.md](references/OpenUSD-building.md)
- [OpenUSD/mjcPhysics.md](references/OpenUSD-mjcPhysics.md)
- [OpenUSD/mjcf_file_format_plugin.md](references/OpenUSD-mjcf_file_format_plugin.md)
- [OpenUSD/importing.md](references/OpenUSD-importing.md)
- [OpenUSD/exporting.md](references/OpenUSD-exporting.md)
