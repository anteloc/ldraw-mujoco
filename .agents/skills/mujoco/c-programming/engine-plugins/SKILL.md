---
name: engine-plugins
description: 'Extending MuJoCo with engine plugins: plugin types (actuators, sensors, passive forces, SDF collision), registration, plugin configuration in MJCF, and resource providers. Use when adding custom physics, sensors or collision shapes through the plugin API.'
---

# Engine Plugins and Extensions

Use this skill to extend MuJoCo with user code: engine plugins (custom
actuators, sensors, passive forces, SDF collision shapes), their declaration
and configuration in MJCF, plugin state, registration and loading, plus
asset decoders, encoders and resource providers. Building a plugin shared
library with Bazel (`mujoco_plugin` macro) is in
[c-programming](../SKILL.md).

## Why plugins instead of callbacks

Global physics callbacks (`mjcb_*`, see
[simulation-loop](../simulation-loop/SKILL.md)) remain useful for prototyping
or Python code, but are deprecated as a stable extension mechanism. Plugins
offer:

- **Thread safety:** plugin instances are thread-local.
- **Statefulness:** plugin state is (de)serialized correctly.
- **Interoperability:** plugins coexist without interference.

## Concepts

| Term | Meaning |
|----|----|
| Plugin | Functions plus static attributes in an `mjpPlugin` struct. Functions are **stateless**; state is declared and managed by MuJoCo and passed in. Often a C library. Not a model element. |
| Plugin instance | Runtime state the plugin operates on. A model element of type `mjOBJ_PLUGIN`; `mjModel.nplugin` instances with ids `[0 nplugin-1]`; names via `mj_name2id` / `mj_id2name`. |

Instances relate to model elements:

- **one-to-one:** each instance referenced once (e.g. two sensors, two
  instances, computed separately).
- **one-to-many:** one instance backs several elements, either because they
  share one physical entity (a motor with a thermometer: actuator + sensor)
  or to batch computation (N motors modelled by one neural network forward
  pass).

### Capabilities

`mjpPlugin.capabilityflags` is a bitfield with bits from
`mjtPluginCapabilityBit`, so one plugin can do several things:

- Actuator plugin
- Sensor plugin
- Passive force plugin
- Signed distance field plugin

## Declare plugins in MJCF

Declare each dependency in `<extension><plugin>`. A declared but unregistered
plugin is a compile error. A single backed element may create its instance
implicitly; elements sharing one instance need an explicit `<instance>`:

``` xml
<mujoco>
  <extension>
    <plugin plugin="mujoco.test.simple_sensor_plugin"/>
    <plugin plugin="mujoco.test.actuator_sensor_plugin">
      <instance name="explicit_instance"/>
    </plugin>
  </extension>
  ...
  <sensor>
    <plugin name="sensor0" plugin="mujoco.test.simple_sensor_plugin"/>
    <plugin name="sensor1" plugin="mujoco.test.simple_sensor_plugin"/>
    <plugin name="sensor2" instance="explicit_instance"/>
  </sensor>
  ...
  <actuator>
    <plugin name="actuator2" instance="explicit_instance"/>
  </actuator>
</mujoco>
```

`sensor0` and `sensor1` reference the plugin directly and each get an
implicit instance; `sensor2` and `actuator2` share `explicit_instance`.

## Configure plugins in MJCF

Plugins declare custom attributes at registration, so the compiler can
reject invalid values. Set them with `<config key=... value=...>`:

``` xml
<mujoco>
  <extension>
    <plugin plugin="mujoco.test.simple_actuator_plugin">
      <instance name="explicit_instance">
        <config key="resistance" value="1.0"/>
        <config key="inductance" value="2.0"/>
      </instance>
    </plugin>
  </extension>
  ...
  <actuator>
    <plugin name="actuator0" instance="explicit_instance"/>
    <plugin name="actuator1" plugin="mujoco.test.simple_actuator_plugin">
        <config key="resistance" value="3.0"/>
        <config key="inductance" value="4.0"/>
    </plugin>
  </actuator>
</mujoco>
```

Pitfall: `<config>` goes only where an instance is created (in `<instance>`
or on an element using `plugin=`). Adding it to `actuator0`, which references
an existing instance, is an error.

## Plugin state and plugin data

| | Plugin state | Plugin data |
|----|----|----|
| What | Time-dependent floating-point values evolving with physics (e.g. temperature) | Arbitrary memoized structures (e.g. preloaded network weights) |
| Storage | `mjData.plugin_state`, at offset `mjModel.plugin_stateadr[instance]` | Pointer in `mjData.plugin_data` |
| Size | Declared per instance by the `nstate` callback (may depend on config) | Opaque to MuJoCo |
| Serialized/copied | Yes, an integral part of the physics state | No; must be reconstructible from config, plugin state and MuJoCo state |

Lifecycle callbacks of `mjpPlugin`:

- `init`: called in `mj_makeData`; allocate plugin data and store its pointer
  in `plugin_data`. On invalid configuration, call `mju_warning` and return
  -1; `mj_makeData` (and compilation) then fails.
- `destroy`: called in `mj_deleteData`; free the instance's resources.
- `copy`: called per instance by `mj_copyData` (which copies plugin state
  itself) so the plugin can set up data for the new mjData.

Never call `mju_error` from plugin callbacks: non-returning error handlers
(Python bindings, the model compiler) skip C++ destructors on the stack, in
the plugin and in MuJoCo.

### Actuator states

Two options for stateful actuator plugins:

1. Use `plugin_state` as above.
2. Use `mjData.act` by implementing the corresponding `mjpPlugin` callback.
   MuJoCo integrates `act_dot` automatically and finite differencing such as
   `mjd_transitionFD` works as for native actuators. `mjpPlugin.advance` is
   called after `act_dot` is integrated and may overwrite `act`.

If a plugin actuator sets `dyntype`, that state variable is placed *after*
the plugin's own state variables in `act`.

The docs do not yet fully document the `mjpPlugin` struct fields; see
[api-types](../../reference/api-types/SKILL.md).

## Register and load plugins

Register before any MJCF references the plugin.

- **Statically linked (one-off/debug):** fill an `mjpPlugin` in `main` and
  pass it to `mjp_registerPlugin`.
- **Library:** register at load time. With GCC-compatible compilers call
  `mjp_registerPlugin` from an `__attribute__((constructor))` function; with
  MSVC inject into C runtime initialization. The `mjPLUGIN_LIB_INIT` macro
  expands to the right construct.
- **Loading a plugin library:** call `mj_loadPluginLibrary` rather than
  `dlopen`/`LoadLibraryA`; it tracks how MuJoCo expects auto-registration to
  work.
- **Scan a directory:** `mj_loadAllPluginLibraries` loads every dynamic
  library in a directory (as `simulate` does). Libraries that fail to load
  are skipped with a warning.

## Writing plugins

This part of the docs is incomplete; the MuJoCo team invites developers to
contact them. Start from the
[plugin tests](https://github.com/google-deepmind/mujoco/blob/main/test/engine/engine_plugin_test.cc)
and the [first-party plugins](https://github.com/google-deepmind/mujoco/tree/main/plugin):

| Directory | Contents |
|----|----|
| [actuator/](https://github.com/google-deepmind/mujoco/tree/main/plugin/actuator) | Custom actuators; so far a PID controller ([README](https://github.com/google-deepmind/mujoco/blob/main/plugin/actuator/README.md)) |
| [sensor/](https://github.com/google-deepmind/mujoco/tree/main/plugin/sensor) | Custom sensors; currently the touch grid sensor ([README](https://github.com/google-deepmind/mujoco/blob/main/plugin/sensor/README.md)) |
| [sdf/](https://github.com/google-deepmind/mujoco/tree/main/plugin/sdf) | Mesh-free shapes via signed distance fields ([README](https://github.com/google-deepmind/mujoco/blob/main/plugin/sdf/README.md)) |

### SDF plugins

An SDF plugin defines a shape by its signed distance and gradient; it acts as
a new geom type in the collision table of
[engine_collision_driver.c](https://github.com/google-deepmind/mujoco/blob/main/src/engine/engine_collision_driver.c).

Required methods:

| Method | Purpose |
|----|----|
| `sdf_distance` | Signed distance of a query point in local coordinates. Also used by the compiler to make a visual mesh via marching cubes ([MarchingCubeCpp](https://github.com/aparis69/MarchingCubeCpp)). |
| `sdf_staticdistance` | Static version taking config attributes as extra inputs; needed because mesh creation happens at compile time, before the plugin is instantiated. |
| `sdf_gradient` | Gradient of the SDF at the query point, local coordinates. |
| `sdf_aabb` | Axis-aligned bounding box in local coordinates; voxelized uniformly before marching cubes. |

Collision algorithm:

- Contact points minimize `A + B + abs(max(A, B))` (A, B the two SDFs) by
  gradient descent.
- SDFs are non-convex, so several starting points are used: `sdf_initpoints`
  sets how many (Halton sequence inside the intersection of the AABBs);
  `sdf_iterations` sets the descent iterations.
- Exact SDFs are preferred, but any function that vanishes at the surface,
  grows monotonically away from it and is negative inside works (possibly
  with more starting points). Keep the gradient norm near 1 close to the
  surface; otherwise penetration depth is scaled and projection steps are
  distorted.

## Decoders (asset loading)

Decoder plugins load asset formats beyond MJCF and URDF. Built in: OBJ
(`plugin/obj_decoder`, the simplest example) and STL
(`plugin/stl_decoder`). Optional: USD (`plugin/usd_decoder`, whole scenes).

`mjpDecoder` fields:

| Field | Meaning |
|----|----|
| `content_type` | MIME-like string, e.g. `"model/obj"`, `"model/stl"`; matched against a mesh asset's `content-type` attribute |
| `extension` | Extension(s) including the dot, used when no content type is given; separate several with `|`, e.g. `.usd|.usda|.usdc|.usdz` |
| `can_decode` | `mjfCanDecode`; returns nonzero if the resource can be handled (may inspect contents, e.g. URDF vs MJCF both `.xml`) |
| `decode` | `mjfDecode`; returns a newly allocated `mjSpec` (caller frees with `mj_deleteSpec`) or `NULL`, writing a reason into `error` (size `error_sz`) if `error` is not `NULL` |

- The message reaches the user, e.g. via the `error` argument of `mj_parse`
  or as a compiler error for mesh assets. Report non-fatal issues with
  `mju_warning`; never call `mju_error`.
- For a mesh asset, the compiler uses the first mesh element of the returned
  spec. For a model asset, the spec may contain any elements.
- Register with `mjp_registerDecoder`; initialize with `mjp_defaultDecoder`;
  use `mjPLUGIN_LIB_INIT` to register at library load.

Minimal decoder for a hypothetical binary mesh format:

``` C
#include <stdio.h>
#include <mujoco.h>

static mjSpec* MyDecode(mjResource* resource, const mjVFS* vfs, char* error, int error_sz) {
  const void* bytes = NULL;
  int nbytes = mju_readResource(resource, &bytes);
  if (nbytes < 0) {
    if (error) snprintf(error, error_sz, "failed to read resource '%s'", resource->name);
    return NULL;
  }

  /* ... parse bytes into vertex/face arrays ... */

  mjSpec* spec = mj_makeSpec();
  mjsMesh* mesh = mjs_addMesh(spec, NULL);
  mjs_setString(mesh->file, resource->name);
  mjs_setFloat(mesh->uservert, vertices, nvert * 3);
  mjs_setInt(mesh->userface, faces, nface * 3);
  return spec;
}

static int MyCanDecode(const mjResource* resource) {
  /* check file extension */
  const char* name = resource->name;
  int len = strlen(name);
  return len > 4 && strcmp(name + len - 4, ".myf") == 0;
}

mjPLUGIN_LIB_INIT(my_format_decoder) {
  mjpDecoder decoder;
  mjp_defaultDecoder(&decoder);
  decoder.content_type = "model/my-format";
  decoder.extension = ".myf";
  decoder.decode = MyDecode;
  decoder.can_decode = MyCanDecode;
  mjp_registerDecoder(&decoder);
}
```

Once registered, matching assets use it automatically:

``` xml
<asset>
  <mesh file="my_mesh.myf"/>
</asset>
```

## Encoders (model saving)

Encoder plugins serialize models beyond XML, MJB and TXT. Built in: a Zip
encoder for `.mjz` archives (`src/xml/mjz/mjz_encoder.cc`).

`mjpEncoder` fields:

| Field | Meaning |
|----|----|
| `content_type` | MIME-like output type, e.g. `"application/zip"`; used when `mj_encode` gets an explicit `content_type` |
| `extension` | Extension(s) including the dot, `|`-separated, used when no content type is given (the Zip example lists `.mjz` and `.zip`; the source text is garbled here) |
| `encode` | `mjfEncode`; receives an `mjSpec`, an optional compiled `mjModel`, an optional `mjVFS` and an output `mjResource`; returns bytes written or -1 |
| `close_resource` | Optional; frees memory the `encode` callback allocated in `mjResource.data` |

Register with `mjp_registerEncoder` (initialize with `mjp_defaultEncoder`)
before using `mj_encode`:

``` C
mjPLUGIN_LIB_INIT(my_format_encoder) {
  mjpEncoder encoder;
  mjp_defaultEncoder(&encoder);
  encoder.content_type = "application/x-myformat";
  encoder.extension = ".myf";
  encoder.encode = MyEncode;
  encoder.close_resource = MyCloseResource;
  mjp_registerEncoder(&encoder);
}
```

## Resource providers

An `mjpResourceProvider` loads assets (XML, meshes, textures, ...) from
sources other than the filesystem or `mjVFS`, e.g. the Internet, through the
abstract `mjResource`. Register it in a global table with
`mjp_registerProvider`; all loading functions can then use it.

- **Prefix:** a URI scheme. A resource named `{prefix}:{filename}` matches
  (case-insensitive). The colon is required: with prefix `http`,
  `http://www.example.com/myasset.obj` matches but
  `https://www.example.com/myasset.obj` does not.
- **Data pointer:** opaque pointer passed to the callbacks, constant within a
  model.
- **Callbacks:**

| Callback | Type | Required | Contract |
|----|----|----|----|
| `open` | `mjfOpenResource` | Yes | Check `resource->name` exists, fill `resource->data`; return 1 on success, 0 on failure |
| `read` | `mjfReadResource` | Yes | Point `*buffer` at the bytes and return their count; -1 on failure |
| `close` | `mjfCloseResource` | Yes | Free memory allocated in `resource->data` |
| `getdir` | `mjfGetResourceDir` | No | Directory of a resource name (`http://www.example.com/` for `http://www.example.com/myasset.obj`) |
| `modified` | `mjfResourceModified` | No | Whether an opened resource changed at its source |

Example: a provider for the [data URI scheme](https://en.wikipedia.org/wiki/Data_URI_scheme)
(helper functions are placeholders):

``` C
int str_open_callback(mjResource* resource) {
  // call some util function to validate
  if (!is_valid_data_uri(resource->name)) {
    return 0; // return failure
  }

  // some upper bound for the data
  resource->data = mju_malloc(get_data_uri_size(resource->name));
  if (resource->data == NULL) {
    return 0; // return failure
  }

  // fill data from string (some util function)
  get_data_uri(resource->name, &data);
}

int str_read_callback(mjResource* resource, const void** buffer) {
  *buffer = resource->data;
  return get_data_uri_size(resource->name);
}

void str_close_callback(mjResource* resource) {
  mju_free(resource->data);
}
```

Note: as written in the docs, `str_open_callback` never returns 1 on
success; add `return 1;` at the end in real code.

``` C
mjpResourceProvider provider = {
  .prefix = "data",
  .open = str_open_callback,
  .read = str_read_callback,
  .close = str_close_callback,
};

// return positive number on success
if (!mjp_registerProvider(&provider)) {
  // ...
  // return failure
}
```

Assets can now be inline strings in MJCF:

``` xml
<asset>
  <texture name="grid" file="grid.png" type="2d"/>
  <mesh content-type="model/obj" file="data:model/obj;base64,I215IG9iamVjdA0KdiAxIDAgMA0KdiAwIDEgMA0KdiAwIDAgMQ=="/>
  ...
</asset>
```

## Source docs

Verbatim copies, for details not covered above:

- [programming/extension.md](references/programming-extension.md)
