# Model Editing

It is possible to create and modify models using the [mjSpec](../APIreference/APItypes.md) struct and related API. This data structure is in one-to-one correspondence with MJCF and indeed, MuJoCo's own XML parsers (both MJCF and URDF) use this API when loading a model.

## Overview

The API augments the traditional workflow of creating and editing models using XML files, breaking up the *parse* and *compile* steps. As summarized in the [Overview chapter](../overview.md), the traditional workflow is:

> 1.  Create an XML model description file (MJCF or URDF) and associated assets. <br/>
> 2.  Call *mj_loadXML*, obtain an [mjModel](../APIreference/APItypes.md) instance.

The workflow using [mjSpec](../APIreference/APItypes.md) is:

> 1.  Create an empty [mjSpec](../APIreference/APItypes.md) using *mj_makeSpec* or parse an existing XML file using *mj_parseXML*.
> 2.  Programmatically edit the [mjSpec](../APIreference/APItypes.md) data structure by adding, modifying, and removing elements.
> 3.  Compile the [mjSpec](../APIreference/APItypes.md) to an [mjModel](../APIreference/APItypes.md) instance using *mj_compile*.
>
> After compilation, the [mjSpec](../APIreference/APItypes.md) remains editable, so steps 2 and 3 are interchangeable.

## Model Parsing & Loading<span id="Load"></span>

As summarized in [Model instances](../overview.md), model description files (MJCF, MJZ, URDF, USD) are parsed into an [mjSpec](../APIreference/APItypes.md) using *mj_parse* (or `mjSpec.from_file()` / `mjSpec.from_string()` in Python). The model format is inferred from the content type or file extension, and parsing into an [mjSpec](../APIreference/APItypes.md) is delegated to the appropriate [decoder](extension.md) plugin.

``` C
char error[1000] = "";
mjSpec* spec = mj_parse(vfs, "robot.xml", NULL, NULL, error, sizeof(error));
```

For convenience, *mj_loadXML* (or Python `MjModel.from_xml_path()`) combines parsing and compilation into a single step, returning a compiled [mjModel](../APIreference/APItypes.md) directly from an XML file or `.mjz` archive.

Alternatively, a pre-compiled [mjModel](../APIreference/APItypes.md) can be loaded directly from a binary MJB file using *mj_loadModel* (or Python `MjModel.from_binary_path()`).

## Model Compilation<span id="Compile"></span>

Once a high-level [mjSpec](../APIreference/APItypes.md) is created---by parsing a file, loading an archive, or constructing it programmatically---it is compiled into an [mjModel](../APIreference/APItypes.md) using *mj_compile*.

Compilation is independent of loading, working in the exact same way regardless of how [mjSpec](../APIreference/APItypes.md) was constructed. Both the parser and the compiler perform extensive error checking and abort when the first error is encountered. The parser uses a custom schema to validate file structure, elements, and attributes, while the compiler applies semantic checks and executes a test simulation step to catch runtime errors.

Parsing and compilation are extremely fast—typically less than a second—making interactive model design, live editing, and rapid reloading seamless.

## Model Encoding & Saving<span id="Save"></span>

Model specs and compiled models can be serialized to files using *mj_encode*, or directly saved to XML strings using *mj_saveXMLString* or *mj_saveXML*.

The *mj_encode* function provides a unified entry point for serializing models:

``` C
char error[1024] = "";
mjtSize bytes_written = mj_encode(spec, model, "robot.mjz", NULL, vfs, error, sizeof(error));
```

The output format is selected automatically based on the file extension (case-insensitive) or explicit `content_type`:

- **MJCF XML** (`.xml`): Flattens the spec into a single MJCF XML file using *mj_saveXML*. If an explicit [mjModel](../APIreference/APItypes.md) argument is passed, *mj_encode* will copy modified values back from `mjModel` into the spec prior to saving. In the Computation chapter we show an [example](_static/example.xml) MJCF file and the corresponding [saved example](_static/example_saved.xml).
- **MJZ Archive** (`.mjz` or `.zip`): Bundles the spec and all associated external assets (meshes, textures, included XMLs) into a self-contained Zip archive via the built-in `mjz_encoder`.
- **MJB Binary** (`.mjb`): Serializes the compiled [mjModel](../APIreference/APItypes.md) in MuJoCo binary format via *mj_saveModel*. MJB files are standalone, do not refer to external files, and load faster than XML, but are version-specific and cannot be decompiled back to XML. Requires a compiled `model`; does **not** serialize anything from `spec`.
- **TXT** (`.txt`): Writes a human-readable text dump via *mj_printModel*. Useful for diffing and debugging. Requires a compiled `model`; does **not** serialize anything from `spec`.

A spec is saved as MJCF in one of two ways, selected by its compiler attribute [savecompiled](../XMLreference.md):

- "true", the default: the values which the last compilation made of the model, in the canonical notation. For example a body which is [aligned](../XMLreference.md) with its free joint is saved with its aligned pose, and a geom which was fitted to a mesh with the size of the fit. The spec must have been compiled.
- "false": the model as it is written in the spec. Poses are those of the elements in their [frames](../XMLreference.md), attributes which were written with their default values are kept, and every number is saved exactly. Orientations, angles and `fromto` are saved in the notation in which they were written, unless [savecanonical](../XMLreference.md) is "true". The spec need not have been compiled.

In both cases the saved file compiles to the same model, except where MJCF cannot say what the spec holds. For example, the elements of an attached model are compiled with its own compiler settings, while the saved file has one [compiler](../XMLreference.md) element. Saved as written, the angle unit and the Euler sequence of an attached model are converted, and a difference in a setting which changes what compilation infers, such as [inertiafromgeom](../XMLreference.md), is an error which says so; saved as compiled values, such a model may compile differently. What the parser does not keep in a spec is not saved: comments other than the one at the top of the file, the [include](../XMLreference.md) elements, and the elements which it expands into others, such as [replicate](../XMLreference.md), [flexcomp](../XMLreference.md), [attach](../XMLreference.md) and the actuator shortcuts.

A spec which is saved as written needs a compilation in two cases. The inertials which compilation calculates, which [saveinertial](../XMLreference.md) saves, are those of the last compilation, which must follow any structural edit (elements added, deleted or attached), as for compiled values. And [keyframes](../XMLreference.md) which await compilation, as they do once *mjs_attach* or *mjs_delete* changed the kinematic tree of a spec which has keyframes, are saved once compilation has assembled their vectors.

Importantly, saved XML will take into account any defined defaults. This is useful when a model has many repeated values, for example if loaded from URDF, which does not support defaults. In such a case one can add default classes, set the class of the relevant elements, and save; the resulting XML will use the defaults and be more human-readable.

## MJZ Archives

Complex MuJoCo models often consist of multiple files: a main MJCF XML file, included XML sub-trees, and external asset files (meshes, textures, height fields). The **MJZ** format (extension `.mjz` or `.zip`) provides a convenient way to bundle an entire model and all of its referenced assets into a single **Zip archive**.

### Root XML Discovery

When decoding an `.mjz` archive, MuJoCo searches for the root model XML file in the following order:

1.  `model.xml` at the root of the archive. This is the default format produced by the **MJZ** [encoder](extension.md) and is the most portable option.
2.  `<archive_stem>.xml` at the root of the archive (e.g. `my_model.xml` inside `my_model.mjz`).
3.  `<archive_stem>/<archive_stem>.xml` inside a top-level directory matching the archive name (e.g. `my_model/my_model.xml`).
4.  `<archive_stem>/model.xml` inside a top-level directory matching the archive name (e.g. `my_model/model.xml`).

Options 2-4 exist for backwards compatibility with legacy archives and common zip packaging layouts, but are susceptible to failure if the archive file is renamed.

## Custom formats

Adding support for new file formats can be done with *mjp_registerDecoder* and *mjp_registerEncoder*. When *mj_parse* and *mj_encode* are called for a non-native extension or content type, the appropriate plugins are found via *mjp_findDecoder* and *mjp_findEncoder*. For further details on writing custom format plugins, see [Decoders](extension.md) and [Encoders](extension.md).

## Usage

Here we describe the C API for procedural model editing, but it is also exposed in the [Python bindings](../python.md). Advanced users can refer to [user_api_test.cc](https://github.com/google-deepmind/mujoco/blob/main/test/user/user_api_test.cc) and the MJCF parser in [xml_native_reader.cc](https://github.com/google-deepmind/mujoco/blob/main/src/xml/xml_native_reader.cc) for more usage examples. After creating a new [mjSpec](../APIreference/APItypes.md) or parsing an existing XML file to an [mjSpec](../APIreference/APItypes.md), procedural editing corresponds to setting attributes. For example, in order to change the timestep, one can do:

``` C
mjSpec* spec = mj_makeSpec();
spec->opt.timestep = 0.01;
...
mjModel* model = mj_compile(spec, NULL);
```

Attributes which have variable length are C++ vectors and strings, [exposed to C as opaque types](../APIreference/APItypes.md). In C one uses the provided *getters* and *setters*:

``` C
mjs_setString(spec->modelname, "my_model");
```

In C++, one can use vectors and strings directly:

``` C++
std::string modelname = "my_model";
*spec->modelname = modelname;
```

### Model elements

Model elements corresponding to MJCF are exposed to the user as C structs with the `mjs` prefix. The definitions are listed under the [Model Editing](../APIreference/APItypes.md) section of the struct reference. For example, an MJCF [geom](../XMLreference.md) corresponds to an [mjsGeom](../APIreference/APItypes.md).

Global defaults for all elements are set by *initializers* like *mjs_defaultGeom*. These functions are defined in [user_init.c](https://github.com/google-deepmind/mujoco/blob/main/src/user/user_init.c) and are the source of truth for all default values.

Elements cannot be created directly; they are returned to the user by the corresponding constructor function, e.g. *mjs_addGeom*. For example, to add a box geom to the world body, one would do

``` C
mjSpec* spec = mj_makeSpec();                                  // make an empty spec
mjsBody* world = mjs_findBody(spec, "world");                  // find the world body
mjsGeom* my_geom = mjs_addGeom(world, NULL);                   // add a geom to the world
my_geom->type = mjGEOM_BOX;                                    // set geom type
my_geom->size[0] = my_geom->size[1] = my_geom->size[2] = 0.5;  // set box size
mjModel* model = mj_compile(spec, NULL);                       // compile to mjModel
...
mj_deleteModel(model);                                         // free model
mj_deleteSpec(spec);                                           // free spec
```

The `NULL` second argument to *mjs_addGeom* is the optional default class pointer. When using defaults procedurally, default classes are passed in explicitly to element constructors. The global defaults of all elements (used when no default class is passed in) can be inspected in [user_init.c](https://github.com/google-deepmind/mujoco/blob/main/src/user/user_init.c).

Elements are referenced by name, and names are set with *mjs_setName*. Assets are no exception: a mesh, texture or height field added with *mjs_addMesh*, *mjs_addTexture* or *mjs_addHField* must be given a name, even when it is loaded from a file. Naming an asset after its file when the name is omitted is a convenience of the XML parser only.

### Memory management

As seen in the examples above, model elements are never allocated by the user directly, but rather returned by a constructor. The library takes ownership of all elements and frees them when the parent [mjSpec](../APIreference/APItypes.md) is deleted using *mj_deleteSpec*. The user is only responsible for freeing [mjSpec](../APIreference/APItypes.md) structs.

### Attachment

This framework introduces a powerful new feature: attaching and deleting model subtrees. This feature is already used to power the [attach](../XMLreference.md) and [replicate](../XMLreference.md) meta-elements in MJCF. Attachment allows the user to move or copy a subtree from one model into another, while also copying or moving related referenced assets and referencing elements from outside the kinematic tree (e.g., actuators and sensors). Similarly, deleting a subtree will remove all associated elements from the model. The default behavior ("shallow copy") is to move the child into the parent while attaching, so subsequent changes to the child will also change the parent. Alternatively, the user can choose to make an entirely new copy during attach using *mjs_setDeepCopy*. This flag is temporarily set to true while parsing XMLs. It is possible to *attach a body or an mjSpec to a frame*:

``` C
mjSpec* parent = mj_makeSpec();
mjSpec* child = mj_makeSpec();
parent->compiler.degree = 0;
child->compiler.degree = 1;
mjsElement* frame = mjs_addFrame(mjs_findBody(parent, "world"), NULL)->element;
mjsElement* body = mjs_addBody(mjs_findBody(child, "world"), NULL)->element;
mjsBody* attached_body_1 = mjs_asBody(mjs_attach(frame, body, "attached-", "-1"));
```

or *attach a body or an mjSpec to a site*:

``` C
mjSpec* parent = mj_makeSpec();
mjSpec* child = mj_makeSpec();
mjsElement* site = mjs_addSite(mjs_findBody(parent, "world"), NULL)->element;
mjsElement* body = mjs_addBody(mjs_findBody(child, "world"), NULL)->element;
mjsBody* attached_body_2 = mjs_asBody(mjs_attach(site, body, "attached-", "-2"));
```

or *attach a frame or an mjSpec to a body*:

``` C
mjSpec* parent = mj_makeSpec();
mjSpec* child = mj_makeSpec();
mjsElement* body = mjs_addBody(mjs_findBody(parent, "world"), NULL)->element;
mjsElement* frame = mjs_addFrame(mjs_findBody(child, "world"), NULL)->element;
mjsFrame* attached_frame = mjs_asFrame(mjs_attach(body, frame, "attached-", "-1"));
```

Note that in the above examples, the parent and child models have different values for `compiler.degree`, corresponding to the [compiler/angle](../XMLreference.md) attribute, specifying the units in which angles are interpreted. Compiler flags are carried over during attachment, so the child model will be compiled using the child flags, while the parent will be compiled using the parent flags.

Note also that once a child is attached by reference to a parent, the child cannot be compiled on its own or attached again as a whole. Its bodies and frames which are not attached yet can be attached, if they contain nothing which is attached already. An element of the parent, including one attached to it by reference, can be attached to the parent only as a copy, see *mjs_setDeepCopy*.


Known issues

The following known limitations exist:

- All assets from the child model will be copied in, whether they are referenced or not, if the parent and the child are not the same mjSpec.
- A child attached by reference more than once moves its assets to the parent with the first attachment. The elements of a later attachment find them only if it has the same prefix and suffix.
- Circular references are not checked for and will lead to infinite loops.
- When attaching a model with [keyframes](../XMLreference.md), its keyframes are added to the parent right away, but their vectors, and those of the keyframes of the parent, are assembled for the combined model only by the next compilation. Until then they are empty.


### Attribute Merging

When attaching a child spec (or an element from a child spec) to a parent spec using *mjs_attach*, global attributes from the child may conflict with those in the parent. A conflict occurs when both the parent and child specify authored values for the same field and those values differ. Note that for XML-based models, explicitly writing a value (even if it matches the default value) counts as authoring and can trigger conflicts. The [compiler/conflict](../XMLreference.md) attribute controls how such conflicts are resolved. Fields where only one side specifies an authored value never conflict.

<span class="at-val">warning</span> (default)  
Parent values take precedence. Whenever a conflict is detected, a warning is emitted but the parent value is not modified. This preserves the pre-existing attachment behavior.

<span class="at-val">merge</span>  
Attribute values are merged using a per-field strategy as described in the table below. When only the child specifies an authored value, it is adopted by the parent.

<span class="at-val">error</span>  
Any conflict results in a compile error. No values are modified.

The table below describes the per-field merge strategy used in <span class="at-val">merge</span> mode.

| Behavior | Fields | Justification |
|----|----|----|
| **Minimum** | **option**: [timestep](../XMLreference.md), [tolerance](../XMLreference.md), [ls_tolerance](../XMLreference.md), [noslip_tolerance](../XMLreference.md), [ccd_tolerance](../XMLreference.md), [sleep_tolerance](../XMLreference.md), <br/> **visual**: [znear](../XMLreference.md), [realtime](../XMLreference.md) | Preserves precision and stability. |
| **Maximum** | **option**: [iterations](../XMLreference.md), [ls_iterations](../XMLreference.md), [noslip_iterations](../XMLreference.md), [ccd_iterations](../XMLreference.md), [sdf_iterations](../XMLreference.md), [sdf_initpoints](../XMLreference.md), <br/> **size**: [memory](../XMLreference.md), [nkey](../XMLreference.md), [nuserdata](../XMLreference.md), [nuser_body](../XMLreference.md), [nuser_jnt](../XMLreference.md), [nuser_geom](../XMLreference.md), [nuser_site](../XMLreference.md), [nuser_cam](../XMLreference.md), [nuser_tendon](../XMLreference.md), [nuser_actuator](../XMLreference.md), [nuser_sensor](../XMLreference.md) <br/> **visual**: [zfar](../XMLreference.md) | Ensures sufficient resources and limits. |
| **OR (union)** | **option**: [disableflags](../XMLreference.md), [enableflags](../XMLreference.md), [disableactuator](../XMLreference.md) | Flags from both models are combined. |
| **Error** | **option**: [gravity](../XMLreference.md), [wind](../XMLreference.md), [magnetic](../XMLreference.md), [density](../XMLreference.md), [viscosity](../XMLreference.md), [integrator](../XMLreference.md), [cone](../XMLreference.md), [jacobian](../XMLreference.md), [solver](../XMLreference.md), [impratio](../XMLreference.md), [o_margin](../XMLreference.md), [o_solref](../XMLreference.md), [o_solimp](../XMLreference.md), [o_friction](../XMLreference.md) | Raised if non-default values conflict. |

Attribute Merging Behavior (<span class="at-val">merge</span> mode)

### Default classes

Default classes are fully supported in the new API, however using them requires an understanding of how defaults are implemented. As explained in the [Default settings](../modeling.md) section, default classes are first loaded as a tree of dummy elements, which are then used to initialize elements which reference them. When editing models with defaults, this initialization is explicit:

``` C
mjSpec* spec = mj_makeSpec();
mjsDefault* main = mjs_getSpecDefault(spec);
main->geom.type = mjGEOM_BOX;
mjsGeom* geom = mjs_addGeom(mjs_findBody(spec, "world"), main);
```

Importantly, changing a default class after it has been used to initialize elements will not change the properties of already initialized elements.


Possible future change

The behavior described above, where defaults are only applied at initialization, is a remnant of the old, XML-only loading pipeline. A future API change could allow defaults to be changed and applied after initialization. If you think this feature is important to you, please let us know on GitHub.


### In-place recompilation

Compilation with *mj_compile* can be called at any point to obtain a new mjModel instance. In contrast, *mj_recompile* updates an existing mjModel and mjData pair in-place, while preserving the simulation state. This allows model editing to occur **during simulation**, for example adding or removing bodies.
