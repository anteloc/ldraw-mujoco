---
name: cli
description: 'The `ldraw` command-line tool: geometry and model inspection, rendering previews, validating LDraw files (severity levels, checks, exit codes, iter_ldr_issues programmatic API), instruction commands, inventory comparison against CSV, development commands and testing CLI handlers. Use when running or scripting `ldraw` commands, validating .ldr/.mpd files, or comparing a model against an inventory.'
---

# The `ldraw` CLI

Run and script the `ldraw` executable: query parts, inspect exact part and
model geometry, render preview views, validate `.ldr`/`.mpd`/`.dat` files
(also from Python with `iter_ldr_issues`), export bills of materials,
compare a model against an inventory CSV and produce renderer-neutral
instruction data. `ldraw download` / `ldraw generate` basics are in the
[root skill](../SKILL.md); setup details are in
[library-setup](../library-setup/SKILL.md).

```
usage: ldraw [-h] command ...

positional arguments:
  command
    download  Download and unpack an LDraw parts library release.
    generate  Generate the ldraw.library modules from the downloaded library.
    parts     Query the parts catalog.
    validate  Validate an LDraw file (.ldr, .mpd, or .dat).
    bom       Print a bill of materials for an LDraw model file.
    inspect   Inspect exact world bounds, provenance, contacts, and gaps.
    render    Render a deterministic set of standard preview views.
    stubs     Write a type-stub package for ldraw.library into your project.
    instructions
              Inspect, validate, and export renderer-neutral instructions.
    config    Print the current configuration.
    version   Print the installed pyldraw3 version.
```

Run `ldraw <command> --help` for a command's full option list.

## Command summary

| Command | Purpose |
|---|---|
| `ldraw download [--version VERSION] [--yes]` | Download and unpack a release (default `complete`) |
| `ldraw generate [--yes] [--force]` | Regenerate `ldraw.library.*` from the configured release; `--force` even when up to date |
| `ldraw parts search TERM [--limit N]` | Search codes, descriptions, categories, keywords. Every token must match (case-insensitive); ranked by relevance; exit 1 when nothing matches |
| `ldraw parts info CODE` | Description, category, file path, generated-library import |
| `ldraw parts geometry CODE [--format table\|json]` | Exact local bounds, points, connectors, completeness, diagnostics |
| `ldraw validate FILE [--strict]` | Lint a file (see below) |
| `ldraw bom FILE [--format table\|csv\|json] [-o OUT]` | BOM by part and colour, submodels expanded |
| `ldraw inspect FILE [--format table\|json] [--gap-threshold LDU] [--chronological] [--page-marker-prefix TEXT] [-o OUT]` | World geometry, provenance, stud contacts, nearest AABB gaps, skipped geometry, diagnostics |
| `ldraw render FILE [--view front\|isometric\|top] [--size WIDTHxHEIGHT] [--backend auto\|ldview\|leocad] [--output-dir DIR] [--prefix NAME] [--refresh] [--overwrite]` | Staged standard-view previews |
| `ldraw stubs [--out PATH]` | Write `ldraw-stubs/` PEP 561 stubs for IDE autocompletion |
| `ldraw instructions inspect FILE [--section NAME] [--parts]` | One row per section-local step; `--parts` adds the parts tray |
| `ldraw instructions validate FILE [--strict] [--max-parts N]` | LDraw linter plus semantic instruction validation |
| `ldraw instructions export FILE [-o MANIFEST] [--force]` | Manifest schema v1 to stdout or a file |
| `ldraw instructions snapshots FILE --out DIR [--section NAME] [--force]` | Cumulative MPD and flattened LDR files plus `instructions.json` |
| `ldraw config` | Print current configuration as YAML |
| `ldraw version` | Print installed pyldraw3 version |

## Geometry and model inspection

```
ldraw parts geometry 3001 --format json
ldraw inspect model.mpd --chronological --gap-threshold 5 -o inspection.txt
ldraw inspect model.mpd --ldcad-shadow shadow.csl --studio-metadata studio.json
```

- `parts geometry` returns partial geometry when a child part is missing or
  unreadable. Table output labels it incomplete; JSON adds `complete` and
  diagnostics. Unavailable library or unknown root part: exit 1. Reportable
  incomplete geometry: exit 0.
- `inspect` loads tolerantly and keeps valid occurrences around malformed
  lines. Reports include root-to-leaf model, reference, source-line, step and
  attributed-page paths; exact world bounds; skipped geometry; stud contacts;
  nearest AABB gaps.
- Default page marker is `0 // PDF_PAGE NNN`; change with
  `--page-marker-prefix`.
- `inspect` exit codes: error diagnostics write the report but exit 1;
  warnings alone exit 0; missing/undecodable files exit 1 (stderr).
- Both commands accept repeatable `--ldcad-shadow PATH` and
  `--studio-metadata PATH`. JSON then includes metadata coverage, stable
  world-space feature IDs and provenance. `inspect` adds contact
  status/residual evidence and confirmed/optimistic parallel graph edges;
  unresolved occurrences stay graph nodes. Interpretation is in
  [connections](../connections/SKILL.md).

## Rendering previews

`render` shares the optional, cached preview boundary of `render_preview()`.

- No `--view`: renders `front`, `isometric`, `top` at `800x600`. Repeat
  `--view` for an ordered subset.
- `--backend auto` picks the first available backend; explicit `ldview` or
  `leocad` fails if unavailable.
- `--refresh` bypasses cache reads.
- Outputs are `PREFIX.VIEW.png` (default prefix: model stem). All views are
  staged first and promoted only after all succeed.
- Existing outputs are rejected before rendering unless `--overwrite`.

```
$ ldraw render model.mpd --view front --view top --output-dir renders
RENDERED: /work/renders/model.front.png
RENDERED: /work/renders/model.top.png
```

To score renders against references, see
[visual-comparison](../visual-comparison/SKILL.md).

## Validating files

`ldraw validate FILE` lints line by line and reports each problem with file
name and 1-based line number. MPD `0 FILE` sections resolve, so in-file
submodels are not unknown parts. Without a generated library it still runs
but skips unknown-part and colour checks, printing:

```
note: no parts library found; skipping unknown-part and colour checks
```

**Errors** (always exit non-zero):

| Issue | Meaning |
|---|---|
| malformed / unparseable line | Bad token count, non-numeric coordinates, etc. |
| `invalid colour value` | Colour resolves to neither code nor RGB |
| `non-finite numeric fields` | NaN/Infinity in placement, matrix or type-2–5 vertex |
| `unknown colour code N` | No definition in the loaded catalog |
| `unknown part CODE` | Not in the catalog and not an in-file submodel |

**Warnings** (fail only with `--strict`):

| Issue | Meaning |
|---|---|
| `legacy dithered colour code N` | Colour in the legacy range 256–511 |
| `singular transformation matrix (flattens geometry)` | Matrix collapses the part to zero volume |
| `transformation matrix is not orthonormal (scaled or sheared part)` | Matrix scales or shears |
| `unknown meta-command !NAME` | Unrecognised `0 !NAME` command (plain `0 STEP`-style comments are not checked) |
| duplicate placement (`model.duplicate_placement`) | Same reference, colour, position and matrix within one section; group transforms applied first |

```
$ ldraw validate castle.ldr
castle.ldr:12: error: unknown part 9999
castle.ldr:47: warning: singular transformation matrix (flattens geometry)
castle.ldr: 1 error(s), 1 warning(s)

$ ldraw validate castle.ldr
castle.ldr: OK

$ ldraw validate castle.ldr --strict
castle.ldr:47: warning: singular transformation matrix (flattens geometry)
castle.ldr: 0 error(s), 1 warning(s)
$ echo $?
1
```

Exit codes: `0` no issues or only warnings without `--strict`; `1` errors,
any warning with `--strict`, or file does not exist.

### Programmatic validation: `iter_ldr_issues`

Yields `ValidationIssue` records (`line_number`, `message`, `severity`):

```python
from pathlib import Path

from ldraw import iter_ldr_issues
from ldraw.validation import Severity
from ldraw.parts import Parts

parts = Parts.get("~/ldraw/parts.lst")  # optional; enables catalog checks
issues = list(iter_ldr_issues(Path("castle.ldr"), parts))

errors = [i for i in issues if i.severity is Severity.ERROR]
for issue in issues:
    print(f"{issue.line_number}: {issue.severity}: {issue.message}")
```

`parts=None` (or omitted) skips unknown-part and unknown-colour checks, like
the CLI without a library.

## Inventory comparison

```
ldraw bom MODEL.mpd --compare INVENTORY.csv --inventory-mapping MAPPING.json --format json
```

Native BOM CSV needs no mapping. A third-party mapping is JSON:

```json
{
  "columns": {"part": "Part ID", "colour": "Colour ID", "quantity": "Qty"},
  "part_aliases": {"old-part": "new-part"},
  "colour_map": {"red": 4, "custom": "0x2ABCDEF"}
}
```

- Column keys: `part`, `colour`, `quantity`.
- Part aliases apply to model and inventory; colour maps only to inventory.
  An explicit colour map must cover every input colour.
- Repeated rows aggregate. Negative, fractional or missing quantities and
  missing columns are invalid.
- `--format table|csv|json` and `--output PATH` work; `--inventory-mapping`
  requires `--compare`.
- Differences expose part, colour, expected/actual and missing/extra
  quantities.

| Exit | Meaning |
|---|---|
| 0 | Match |
| 1 | Differences |
| 2 | Invalid comparison input or incomplete model counts |

Identifier rules:

- Dotted identifiers such as `custom.v1` are preserved; only a terminal
  `.dat` is removed (case-insensitive).
- After submodel expansion, leaf references without `.dat` must be listed by
  whole reference in the configured `parts.lst`. Use `.dat` references to
  compare without a library.
- Exit 2 for: unknown references, unavailable listing (error names the path
  and recommends `ldraw download`), invalid config, non-finite geometry,
  unresolved `.ldr`/`.mpd` references (aliases cannot rescue them).

The Python API (`compare_inventory`, `read_inventory`) is shown in
[building-models](../building-models/SKILL.md).

## Instruction commands

All four `ldraw instructions` commands require the configured parts catalog;
without it they print the `ldraw download` hint and exit 1.

```
$ ldraw instructions inspect model.mpd --section module.ldr --parts
section  step  direct  expanded  cumulative  rotation  camera  callouts  group  page  suppressed
module.ldr     1       2         2           2  -             -              0      -     -  -
      qty  part         colour               description
        2  3001         Red                  Brick  2 x  4
```

- `inspect` reports direct placements, expanded additions, cumulative leaf
  counts, ROTSTEP, camera, callout/multi-step, page-break and suppression
  state. Section selection is case-insensitive.
- `validate` gives diagnostics with section and source-line context. Errors
  always fail; warnings (missing explicit boundaries, orphan sections,
  `--max-parts` overflow) fail only with `--strict`.
- Manifest schema v1 is snake_case: root-first reachable sections,
  provenance, direct/expanded additions, cumulative count/BOM/bounds,
  ROTSTEP and LPub camera, directives, callouts/groups, suppression and
  page-break flags. Cumulative occurrences appear only as aggregates.
- Part identity: codes omit a terminal `.dat`; `.ldr`/`.mpd` references keep
  their suffix (`body.ldr` stays distinct from `body.dat`).

`snapshots` default layout:

```
output/
  instructions.json
  001-main/
    step-0001.mpd
    step-0001.ldr
  002-module/
    step-0001.mpd
    step-0001.ldr
```

- MPDs keep submodel references plus the transitive dependency closure.
- LDRs flatten `.ldr` submodels into section-local coordinates, keep `.dat`
  references and write embedded `.dat` definitions as relative sidecars.
- Suppressed steps still get artifacts; page breaks do not create steps.
- Without `--force` any collision fails. `--force` only removes paths listed
  in an existing pyldraw3-owned manifest; unrelated files are never touched.
- No PDF, image, HTML or page layout is produced.

## Development commands

```
uv sync
source .venv/bin/activate
uv run ldraw download --yes
uv run ldraw generate --yes

uv run pytest
uv run pytest --cov=ldraw
uv run pytest --integration
uv run ruff format .
uv run ruff check .
uv build

uv sync --group docs
uv run zensical serve
uv run zensical build --clean --strict
```

GitHub Pages must use the "GitHub Actions" publishing source.

## Testing CLI handlers

Historical imports from `ldraw.cli` stay available through a fixed
compatibility manifest; new helpers are not added to it. Mocking a historical
alias does not change the runtime handler. Patch the name in the consuming
module, for example `ldraw.cli._instructions._load_parts` or
`ldraw.cli._download.do_download`.

## Source docs

Verbatim copies, for details not covered above:

- [cli/index.md](references/cli-index.md)
