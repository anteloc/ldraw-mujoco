---
name: reference
description: 'MuJoCo reference material: the MJCF XML element and attribute reference, the C API types, functions and globals, and the changelog. Use when an exact XML attribute, default value, struct field, function signature, enum or version change is needed.'
---

# MuJoCo Reference

Use this skill to find the exact spelling, type, default or signature of a
MuJoCo symbol: an MJCF XML attribute, a C API struct field or enum value, a
function signature, a global callback or constant, or the release in which
something changed. For concepts and the canonical load/step pattern, see the
root skill [mujoco](../SKILL.md).

## How the API reference is organized

The API reference is the manual for the MuJoCo C API. It is kept in sync with
MuJoCo's header files automatically, and adds information that is not in the
headers. The API has 3 categories:

| Category | Contents | Subskill |
|----|----|----|
| Types | primitive types, enums (`mjt*`), structs (`mjModel`, `mjData`, `mjOption`, `mjContact`, `mjs*` spec elements, `mjv*`/`mjr*` structs), function types (`mjf*`) | [api-types](api-types/SKILL.md) |
| Functions | `mj_*`, `mjv_*`, `mjr_*`, `mjui_*`, `mju_*`, `mjd_*`, `mjp_*`, `mjs_*` functions, by group | [api-functions](api-functions/SKILL.md) |
| Globals | `mjcb_*` callbacks, `mjCOLLISIONFUNC`, string and numeric constants, macros, X macros | [api-globals](api-globals/SKILL.md) |

The MJCF XML format and the release notes are separate references:

| Need | Subskill |
|----|----|
| An MJCF element or attribute, its type and default (`solref`, `condim`, `margin`, `density`, `<option>` flags, ...) | [xml-reference](xml-reference/SKILL.md) |
| Whether a feature, attribute or function exists in a given MuJoCo version, or what broke between versions | [changelog](changelog/SKILL.md) |

## Pick the right reference

| Question | Look in |
|----|----|
| "What is the field name / array shape in `mjModel` or `mjData`?" | [api-types](api-types/SKILL.md) |
| "What are the members of `mjtGeom` / `mjtDisableBit`?" | [api-types](api-types/SKILL.md) (enums) |
| "What arguments does `mj_jac` / `mj_contactForce` / `mjs_addBody` take?" | [api-functions](api-functions/SKILL.md) |
| "How do I install a control or passive-force callback?" | [api-globals](api-globals/SKILL.md) |
| "What is `mjMINVAL`, `mjMAXIMP` or `mjNEQDATA`?" | [api-globals](api-globals/SKILL.md) |
| "Which XML attribute sets joint friction loss and what is its default?" | [xml-reference](xml-reference/SKILL.md) |
| "Does my pinned 3.x release support this?" | [changelog](changelog/SKILL.md) |

## Conventions shared by the references

- The references describe the C API. For how it surfaces in Python, see
  [python-bindings](../python-bindings/SKILL.md).
- The version is the integer `(S * 1e6) + (M * 1e3) + P` for version
  "S.M.P"; compare `mjVERSION_HEADER` (headers) with `mj_version()` (compiled
  library). Details are in [api-globals](api-globals/SKILL.md).
- Model editing through `mjSpec` (`mjs_*` functions, `mjs*` structs) is
  covered as a task in [model-editing](../model-editing/SKILL.md); its
  signatures are in [api-functions](api-functions/SKILL.md) and
  [api-types](api-types/SKILL.md).
- For the long tail, open the verbatim source docs attached to each subskill
  rather than guessing a name or default.

## Subskills

Read the one that matches your task:

- [xml-reference](xml-reference/SKILL.md): Complete MJCF XML reference: every element (mujoco, compiler, option, size, visual, statistic, default, asset, mesh, worldbody, body, joint, geom, site, camera, light, contact pair/exclude, equality connect/weld/joint, tendon, actuator, sensor, keyframe, extension, plugin) with all attributes, types and defaults. Use when writing or checking any MJCF attribute such as solref, solimp, solimpfriction, margin, condim, friction, frictionloss, damping, armature, density, mass, inertia, meshdir or option flags.
- [api-types](api-types/SKILL.md): MuJoCo C API types: primitive types, enums (mjtObj, mjtGeom, mjtJoint, mjtSolver, mjtCone, mjtDisableBit, mjtState, ...), structs (mjModel, mjData, mjOption, mjContact, mjSpec elements such as mjsBody, mjsGeom, mjsJoint, visualization and rendering structs) and function types. Use when the exact field name, array shape or enum value of a MuJoCo struct is needed, in C or through the Python bindings.
- [api-functions](api-functions/SKILL.md): MuJoCo C API functions by group: parse and compile, main simulation (mj_step, mj_forward), support (mj_jac, mj_contactForce, mj_name2id), components, ray casting, printing, virtual file system, initialization, visualization, OpenGL/Filament rendering, UI, derivatives, plugins, threads, batched simulation, math and quaternion utilities, and the mjSpec editing functions (mjs_addBody, mjs_attach, attribute setters/getters, find utilities). Use when looking up the signature or semantics of a mj_*, mjv_*, mjr_*, mju_*, mjd_* or mjs_* function.
- [api-globals](api-globals/SKILL.md): MuJoCo C API globals: error, memory and physics callbacks (mjcb_*), the collision function table, string and numeric constants (mjMINVAL, mjNEQDATA, ...), macros and X macros. Use when installing callbacks or needing a MuJoCo constant or macro.
- [changelog](changelog/SKILL.md): MuJoCo release notes from early versions up to 4.0.1 and upcoming changes: new features, breaking API and MJCF changes, bug fixes and deprecations per version. Use when code targets a specific MuJoCo version (e.g. a pinned 3.x), when behaviour differs between versions, or to check whether an attribute or function exists in a given release.

## Source docs

Verbatim copies, for details not covered above:

- [APIreference/index.md](references/APIreference-index.md)
