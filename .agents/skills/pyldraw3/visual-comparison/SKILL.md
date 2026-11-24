---
name: visual-comparison
description: 'Comparing renders of LDraw models against reference images with pyldraw3: comparing one view, ranking existing renders, generating and ranking a LeoCAD camera grid, cropping important regions, multi-view reports and interpreting scores. Use when checking that a reconstructed or converted model looks like a reference photo or render.'
---

# Visual Comparison

Check that an LDraw or LeoCAD render looks like a reference image: compare
one view, rank a set of renders, sweep a LeoCAD camera grid to find the best
camera, score named regions and build multi-view reports. The tool only reads
images; it never modifies the model or the program that generated it. To
produce standard preview renders first, use `ldraw render` (see
[cli](../cli/SKILL.md)).

## How it works

1. Estimate the flat background from the image border (or use PNG alpha).
2. Extract both silhouettes.
3. For each scale in a configurable range, find the translation with the
   largest silhouette overlap.
4. Pick the registration with the highest intersection over union (IoU).

## Install

Pillow and the tool are not in the base install:

```
pip install "pyldraw3[visual-compare]"
```

From a repository checkout: `uv sync --extra visual-compare`. Run it as
`python -m ldraw.visual_compare` or the equivalent repository script
`python scripts/visual_compare.py`.

| Subcommand | Use for |
|---|---|
| `compare` | One reference vs one render (optionally with regions) |
| `rank` | Order any set of existing PNGs against one reference |
| `camera-grid` | Render a LeoCAD latitude/longitude grid and rank it |
| `report` | Several reference views, several candidates each, from a manifest |

## Compare one view

```
uv run --extra visual-compare python scripts/visual_compare.py compare \
  references/front.png renders/scout.front.png \
  --output-dir comparison/front \
  --min-scale 0.75 --max-scale 1.30 --scale-steps 56
```

Outputs:

| File | Content |
|---|---|
| `comparison.json` | Registration and metrics |
| `aligned.png` | Isolated candidate foreground on the estimated reference background |
| `overlay.png` | Red = reference-only silhouette, cyan = candidate-only silhouette |
| `difference.png` | Black-to-red-to-yellow heatmap; silhouette mismatches use the maximum value |

Metrics (normalized to `0..1` where applicable):

- silhouette IoU, Dice, precision and recall;
- candidate/reference foreground area ratio;
- RGB mean absolute error (MAE) and root mean square error (RMSE) on the
  intersecting foreground.

| Option | Purpose |
|---|---|
| `--min-scale`, `--max-scale`, `--scale-steps` | Scale search range and resolution |
| `--background-tolerance` | Tune for opaque images when anti-aliasing, shadows or off-white backgrounds count as foreground |
| `--regions FILE` | Named crop regions (below) |
| `--output-dir DIR` | Where artifacts go |

PNG alpha gives the most reliable foreground.

## Rank existing renders

Works with PNGs from any renderer:

```
uv run --extra visual-compare python scripts/visual_compare.py rank \
  references/front.png renders/camera-*.png \
  --output-dir comparison/front-cameras --columns 5
```

`ranking.json` holds each candidate's alignment and metrics. `ranking.png` is
a contact sheet ordered by silhouette IoU, ties broken by RGB MAE.

## Generate and rank a LeoCAD camera grid

LeoCAD must be on `PATH` or given with `--leocad`:

```
uv run --extra visual-compare python scripts/visual_compare.py camera-grid model.mpd \
  --reference references/front.png \
  --output-dir comparison/camera-grid \
  --latitudes 10,20,30,40 \
  --longitudes=-70,-55,-40,-25 \
  --size 1200x900
```

- Renders the Cartesian product of the latitude and longitude lists.
  Filenames encode the exact angles.
- `camera-grid.json` records the full LeoCAD command. With `--reference` it
  also holds ranked registrations, and `camera-grid.png` is the ordered
  contact sheet.
- `--skip-existing` resumes an interrupted grid without rerendering.
- `--timeout` bounds each render in seconds (default 240).
- Render metadata is written before ranking starts, so it survives a failed
  ranking pass.

LeoCAD is invoked as:

```
leocad MODEL --image OUTPUT --width WIDTH --height HEIGHT \
  --camera-angles LATITUDE LONGITUDE
```

## Crop important regions

Pass a JSON list of named regions. Boxes are `[x, y, width, height]`,
normalized by default; set `"relative": false` for pixels:

```json
[
  {"name": "front grille", "box": [0.28, 0.57, 0.44, 0.22]},
  {"name": "roof", "box": [240, 80, 520, 260], "relative": false}
]
```

```
uv run --extra visual-compare python scripts/visual_compare.py compare \
  reference.png render.png \
  --output-dir comparison --regions regions.json
```

Each region gets reference, aligned, overlay and difference crops under
`regions/`, plus its own metrics in `comparison.json`.

## Report several reference views

Paths in the manifest are relative to the manifest. A view takes either
`candidates` (labelled list) or a single `candidate`:

```json
{
  "alignment": {
    "min_scale": 0.70,
    "max_scale": 1.35,
    "scale_steps": 66,
    "background_tolerance": 24
  },
  "views": [
    {
      "name": "front",
      "reference": "references/front.png",
      "candidates": [
        {"label": "current", "path": "renders/scout.front.png"},
        {"label": "alternate", "path": "renders/scout.front-alt.png"}
      ],
      "regions": [
        {"name": "bumper", "box": [0.20, 0.68, 0.60, 0.22]}
      ]
    },
    {
      "name": "rear three-quarter",
      "reference": "references/rear.png",
      "candidate": "renders/scout.rear.png"
    }
  ]
}
```

```
uv run --extra visual-compare python scripts/visual_compare.py report \
  comparison-manifest.json \
  --output-dir comparison/report
```

Output: `report.json`, a concise `report.html` and per-view artifacts under
`views/VIEW/CANDIDATE/`. Candidates are ranked within each view; the
aggregate section gives the mean of every metric across all comparisons.

## Interpreting scores

- Registration removes framing differences, so IoU reflects shape and camera
  orientation, not canvas placement. Check the recorded scale and offsets
  when framing matters.
- RGB metrics are sensitive to renderer lighting, materials and reference
  compression. Use silhouette metrics to choose the camera; use region crops
  and heatmaps to find local geometry differences.
- The foreground estimator assumes the border is mostly flat background. For
  photographs with textured backgrounds, objects touching the frame or strong
  cast shadows, use transparent renders or pre-masked inputs.

## Source docs

Verbatim copies, for details not covered above:

- [visual-comparison/index.md](references/visual-comparison-index.md)
