"""Import a large LDraw model, check once that it holds, then look at the result.

Run with: .venv/bin/mjpython mall_view.py MODEL.mpd   (plain python on Linux)
With uv's Python on macOS, first export DYLD_FALLBACK_LIBRARY_PATH as the README shows.
"""

import sys

from ldraw_mujoco import import_ldraw
from ldraw_mujoco.simulation import hold, show

# Thousands of touching individual parts form one contact island: CG scales, Newton does not.
result = import_ldraw(sys.argv[1], individual_parts=True, solver="cg")
data, report = hold(result.model, seconds=5)
moved = [body["name"] for body in report["moved_bodies"]]
print(f"holds={report['holds']} after {report['held_s']:.2f} s ({report['wall_s']:.1f} s wall)")
print("moved:", moved[:10])
show(result.model, data, highlight=moved)
