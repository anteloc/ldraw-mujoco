---
name: model-editing
description: 'Programmatic model construction with mjSpec: parsing and loading (mj_parseXML, mj_loadXML), compiling (mj_compile, recompile), encoding and saving (mj_saveXML), attaching subtrees, MJZ archives, custom formats and the virtual file system. Use when building or modifying models in code instead of hand-written XML, attaching one model into another, or saving a compiled model back to XML.'
---

# Model Editing

Create and modify MuJoCo models in code with the `mjSpec` struct and its API,
instead of (or on top of) hand-written XML. Use this skill to parse files into
a spec, add and edit elements, compile to `mjModel`, recompile in place during
simulation, attach one model into another, and save specs or models as MJCF,
MJZ, MJB or text. `mjSpec` maps one-to-one to MJCF; MuJoCo's own MJCF and URDF
parsers use this API. For MJCF semantics see
[MJCF modeling](../mjcf-modeling/SKILL.md); for core concepts see the
[root skill](../SKILL.md).

## Workflow

Traditional: write an XML file, call `mj_loadXML`, get an `mjModel`.

With `mjSpec`:

1. Create an empty spec with `mj_makeSpec`, or parse a file (`mj_parseXML` /
   `mj_parse`).
2. Edit the spec: add, modify and remove elements.
3. Compile to an `mjModel` with `mj_compile`.

The spec stays editable after compilation, so repeat steps 2 and 3 freely.
Parsing and compilation are fast (typically under a second).

## Parsing and loading

Model files (MJCF, MJZ, URDF, USD) are parsed into an `mjSpec` with
`mj_parse`. In Python use `mjSpec.from_file()` / `mjSpec.from_string()`. The
format is inferred from the content type or file extension, and parsing is
delegated to the matching [decoder plugin](../c-programming/engine-plugins/SKILL.md).

```C
char error[1000] = "";
mjSpec* spec = mj_parse(vfs, "robot.xml", NULL, NULL, error, sizeof(error));
```

`vfs` is a virtual file system pointer. The docs here show it as an argument
but do not explain it further; see the
[API functions reference](../reference/api-functions/SKILL.md).

Shortcuts:

| Goal | C | Python |
|----|----|----|
| Parse + compile XML or `.mjz` in one step | `mj_loadXML` | `MjModel.from_xml_path()` |
| Load a precompiled binary MJB | `mj_loadModel` | `MjModel.from_binary_path()` |

## Compiling

```C
mjSpec* spec = mj_makeSpec();
spec->opt.timestep = 0.01;
...
mjModel* model = mj_compile(spec, NULL);
```

- Compilation works the same however the spec was built.
- Parser and compiler both stop at the first error. The parser validates
  structure, elements and attributes against a schema; the compiler applies
  semantic checks and runs a test simulation step.
- `mj_compile` returns a new `mjModel` each call.
- `mj_recompile` updates an existing `mjModel` and `mjData` pair in place and
  preserves the simulation state. Use it to edit the model **during
  simulation**, e.g. adding or removing bodies.

## Editing elements

Editing is setting attributes. Variable-length attributes are C++ vectors and
strings, exposed to C as opaque types; use getters and setters in C:

```C
mjs_setString(spec->modelname, "my_model");
```

In C++, use them directly:

```C++
std::string modelname = "my_model";
*spec->modelname = modelname;
```

Elements are C structs with the `mjs` prefix (MJCF `geom` is `mjsGeom`); see
the Model Editing section of the [API types reference](../reference/api-types/SKILL.md).
You cannot allocate elements yourself; constructors such as `mjs_addGeom`
return them:

```C
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

- The second constructor argument (`NULL` above) is the optional default class.
- Global element defaults come from initializers like `mjs_defaultGeom`,
  defined in [user_init.c](https://github.com/google-deepmind/mujoco/blob/main/src/user/user_init.c),
  the source of truth for default values.
- Name elements with `mjs_setName`. Elements are referenced by name.
- Assets added with `mjs_addMesh`, `mjs_addTexture` or `mjs_addHField` **must**
  be named, even when loaded from a file. Naming an asset after its file is
  only an XML parser convenience.

### Memory management

The library owns all elements and frees them when the spec is deleted with
`mj_deleteSpec`. You only free `mjSpec` structs (and the `mjModel`s you
compiled).

### Default classes

Defaults are applied explicitly, at element creation:

```C
mjSpec* spec = mj_makeSpec();
mjsDefault* main = mjs_getSpecDefault(spec);
main->geom.type = mjGEOM_BOX;
mjsGeom* geom = mjs_addGeom(mjs_findBody(spec, "world"), main);
```

Changing a default class after it initialized elements does **not** change
those elements. (The docs note this may change in a future API version.)

## Attaching and deleting subtrees

`mjs_attach` moves or copies a subtree from one model into another, along with
referenced assets and referencing elements outside the tree (actuators,
sensors). Deleting a subtree (`mjs_delete`) removes all associated elements.
This powers the MJCF `attach` and `replicate` elements.

- Default is shallow: the child is moved into the parent, so later changes to
  the child also change the parent.
- Call `mjs_setDeepCopy` to make an independent copy instead. The flag is
  temporarily true while parsing XML.
- The last two arguments are a name prefix and suffix.

Attach a body (or spec) to a frame:

```C
mjSpec* parent = mj_makeSpec();
mjSpec* child = mj_makeSpec();
parent->compiler.degree = 0;
child->compiler.degree = 1;
mjsElement* frame = mjs_addFrame(mjs_findBody(parent, "world"), NULL)->element;
mjsElement* body = mjs_addBody(mjs_findBody(child, "world"), NULL)->element;
mjsBody* attached_body_1 = mjs_asBody(mjs_attach(frame, body, "attached-", "-1"));
```

Attach a body (or spec) to a site:

```C
mjsElement* site = mjs_addSite(mjs_findBody(parent, "world"), NULL)->element;
mjsElement* body = mjs_addBody(mjs_findBody(child, "world"), NULL)->element;
mjsBody* attached_body_2 = mjs_asBody(mjs_attach(site, body, "attached-", "-2"));
```

Attach a frame (or spec) to a body:

```C
mjsElement* body = mjs_addBody(mjs_findBody(parent, "world"), NULL)->element;
mjsElement* frame = mjs_addFrame(mjs_findBody(child, "world"), NULL)->element;
mjsFrame* attached_frame = mjs_asFrame(mjs_attach(body, frame, "attached-", "-1"));
```

Rules:

- Compiler flags carry over: the child's elements compile with the child's
  flags (e.g. `compiler.degree`, i.e. `compiler/angle`), the parent's with the
  parent's.
- A child attached by reference cannot be compiled alone or attached again as
  a whole. Its not-yet-attached bodies and frames can be attached if they
  contain nothing already attached.
- An element of the parent (including one attached by reference) can be
  attached to the parent only as a copy.

Known issues:

- If parent and child are different specs, all child assets are copied in,
  referenced or not.
- A child attached by reference more than once moves its assets with the first
  attachment; later attachments find them only with the same prefix and suffix.
- Circular references are not checked and cause infinite loops.
- Keyframes of an attached model are added right away, but their vectors (and
  the parent's) stay empty until the next compilation.

### Attribute merging

When both parent and child author different values for the same global field,
`compiler/conflict` decides. In XML, writing a value explicitly counts as
authoring, even if it equals the default. Fields authored on one side only
never conflict.

| `conflict` | Behavior |
|----|----|
| `warning` (default) | Parent value kept; warning emitted. |
| `merge` | Per-field strategy below; child-only values are adopted. |
| `error` | Any conflict is a compile error. |

Merge strategy:

| Behavior | Fields |
|----|----|
| Minimum | option: `timestep`, `tolerance`, `ls_tolerance`, `noslip_tolerance`, `ccd_tolerance`, `sleep_tolerance`; visual: `znear`, `realtime` |
| Maximum | option: `iterations`, `ls_iterations`, `noslip_iterations`, `ccd_iterations`, `sdf_iterations`, `sdf_initpoints`; size: `memory`, `nkey`, `nuserdata`, `nuser_body`, `nuser_jnt`, `nuser_geom`, `nuser_site`, `nuser_cam`, `nuser_tendon`, `nuser_actuator`, `nuser_sensor`; visual: `zfar` |
| OR (union) | option: `disableflags`, `enableflags`, `disableactuator` |
| Error | option: `gravity`, `wind`, `magnetic`, `density`, `viscosity`, `integrator`, `cone`, `jacobian`, `solver`, `impratio`, `o_margin`, `o_solref`, `o_solimp`, `o_friction` (raised if non-default values conflict) |

## Encoding and saving

Save with `mj_encode`, or to XML directly with `mj_saveXML` /
`mj_saveXMLString`.

```C
char error[1024] = "";
mjtSize bytes_written = mj_encode(spec, model, "robot.mjz", NULL, vfs, error, sizeof(error));
```

The format comes from the extension (case-insensitive) or explicit
`content_type`:

| Extension | Output | Needs |
|----|----|----|
| `.xml` | Single flattened MJCF via `mj_saveXML`. If a `model` is passed, modified values are copied from it back into the spec first. | spec |
| `.mjz` / `.zip` | Zip with the spec and all external assets (meshes, textures, included XMLs), via `mjz_encoder`. | spec |
| `.mjb` | Binary `mjModel` via `mj_saveModel`. Standalone, loads faster, version-specific, cannot be decompiled to XML. | compiled model only |
| `.txt` | Human-readable dump via `mj_printModel`, for diffing and debugging. | compiled model only |

### Compiled values vs. as written

Compiler attribute `savecompiled` selects how a spec is saved as MJCF:

- `"true"` (default): values from the last compilation, in canonical notation
  (e.g. a body aligned with its free joint is saved with its aligned pose, a
  mesh-fitted geom with its fitted size). The spec must have been compiled.
- `"false"`: the spec as written. Poses are relative to their frames, explicit
  default-valued attributes are kept, numbers saved exactly. Orientations,
  angles and `fromto` keep their notation unless `savecanonical` is `"true"`.
  No compilation needed, except: `saveinertial` inertials come from the last
  compilation (which must follow any structural edit), and keyframes pending
  after `mjs_attach`/`mjs_delete` are saved only once compilation assembled
  them.

Both compile to the same model, except where MJCF cannot express the spec. One
`compiler` element is saved even if attached models had their own settings.
Saved as written, an attached model's angle unit and Euler sequence are
converted, and a differing inference setting such as `inertiafromgeom` is an
error; saved as compiled values, such a model may compile differently.

Not saved: comments other than the top-of-file one, `include` elements, and
elements expanded by the parser (`replicate`, `flexcomp`, `attach`, actuator
shortcuts).

Saved XML uses defined defaults. To tidy a URDF import (URDF has no
defaults), add default classes, set element classes, and save.

## MJZ archives

An `.mjz` (or `.zip`) bundles the main MJCF, included XMLs and assets. On
decode, the root XML is searched in order:

1. `model.xml` at the archive root (what the MJZ encoder writes; most portable).
2. `<archive_stem>.xml` at the root.
3. `<archive_stem>/<archive_stem>.xml`.
4. `<archive_stem>/model.xml`.

Options 2–4 are for legacy layouts and break if the archive is renamed.

## Custom formats

Register new formats with `mjp_registerDecoder` and `mjp_registerEncoder`.
For non-native extensions or content types, `mj_parse` and `mj_encode` find
plugins via `mjp_findDecoder` and `mjp_findEncoder`. See
[engine plugins](../c-programming/engine-plugins/SKILL.md) for writing them.

## More examples

The same API is in the [Python bindings](../python-bindings/SKILL.md). For
more C usage see
[user_api_test.cc](https://github.com/google-deepmind/mujoco/blob/main/test/user/user_api_test.cc)
and the MJCF parser
[xml_native_reader.cc](https://github.com/google-deepmind/mujoco/blob/main/src/xml/xml_native_reader.cc).

## Source docs

Verbatim copies, for details not covered above:

- [programming/modeledit.md](references/programming-modeledit.md)
