# Speculative contacts

Because standard collision detection only inspects geom poses at discrete timesteps, geoms can *tunnel* through each other whenever their displacement over a single step exceeds their thickness, passing from one side to the other without overlapping at either step. This is especially problematic for simulations with fast-moving bodies, thin geoms, or large timesteps.

Speculative contacts work by *speculating* contacts that would have occurred between the current and the next timestep. This feature can be enabled using the [speculative](../XMLreference.md) flag. Speculative contacts work like normal contacts and are treated the same by the solver. They are produced by the following pipeline:

1.  [Broadphase and sphere filtering](speculative.md) expands the sweep-and-prune AABBs and bounding-sphere tests to account for each fast-moving geom's linear and rotational motion over the step.
2.  [Conservative advancement](speculative.md) sweeps candidate geom pairs to determine the time of impact (TOI) $`0 < t < 1`$ as a fraction of the timestep.
3.  [Line-of-sight raycasting](speculative.md) casts a ray between the two geoms to exclude speculative contacts obscured by another geom in the middle.
4.  [Effective contact distance](speculative.md) inverts the solver's reference acceleration equation ($`\ari = -b_i (J v)_i - k_i r_i`$) to compute a synthetic contact distance `dist` so that the constraint solver arrests $`(1 - t)`$ of the relative normal velocity over the step and lands the geom on the contact surface at $`t = 1`$.

Example models demonstrating speculative contacts can be found in [model/speculative/](https://github.com/google-deepmind/mujoco/tree/main/model/speculative).

Enabling speculative contacts adds scene-dependent collision overhead per step, scaling with the number of geoms whose single-step travel exceeds their thickness and the candidate pairs they sweep across. At the same time, preventing tunneling often allows a larger timestep than discrete collision detection would tolerate, reducing overall wall-clock time.

> [!NOTE]
> Speculative sweeps extrapolate geom motion using only pre-step velocities (`mjData.qvel`) and ignore acceleration. This is both because collision detection runs in the position stage before forces and accelerations are evaluated, and because acceleration contributes an $`O(\Delta t^2)`$ displacement over a single step compared to the $`O(\Delta t)`$ velocity term. Consequently, the timestep $`\Delta t`$ cannot be made arbitrarily large: if a slow or stationary geom is accelerated across an obstacle within a single step by a large applied force, gravity, or another body pushing it during the constraint solve, its pre-step velocity will not predict the motion and it can still tunnel.

## Broadphase and sphere filtering

To avoid overhead on slow-moving objects, a geom is only treated as fast-moving if the maximum distance traveled by any point on its surface over the timestep $`\Delta t`$ exceeds the minimum dimension of its local AABB half-extents. Given pre-step linear displacement $`\Delta x = \Delta t \, v`$ and angular displacement $`\Delta \omega = \Delta t \, \omega`$ about the geom center $`c`$, any point $`p`$ on the geom surface moves over the step by

``` math
\Delta p = \Delta x + \Delta \omega \times (p - c)
```

Since $`\|p - c\| \le r_{\text{bound}}`$, where $`r_{\text{bound}}`$ is the geom's bounding-sphere radius, this surface travel is bounded above via the triangle inequality by the sweep distance

``` math
s = \|\Delta x\| + \|\Delta \omega\| \, r_{\text{bound}}
```

Geoms whose sweep distance $`s`$ is smaller than the minimum dimension of their local AABB half-extents cannot tunnel in a single step and use standard discrete bounds.

### Swept bounding-sphere filter

For each candidate geom pair, the bounding-sphere filter tests whether the two bounding spheres can overlap at any fraction $`t \in [0, 1]`$ of the timestep. Writing $`p = x_2 - x_1`$ for the initial center separation and $`v = \Delta x_2 - \Delta x_1`$ for the relative linear displacement over the step, the relative center trajectory is $`r(t) = p + t v`$. We find the global minimizer $`\tau`$ of $`\|r(t)\|^2`$ on $`[0, 1]`$ by finding the root $`t^*`$ of the derivative $`\frac{d}{dt}\|r(t)\|^2 = 2(p + t v) \cdot v = 0`$:

``` math
\begin{aligned}
\tau =
\begin{cases}
0,   & \phantom{0 \lt {}} t^* \le 0 \\
t^*, & 0 \lt t^* \lt 1 \\
1,   & 1 \le t^*
\end{cases}
\qquad \text{where } t^* = -\frac{p \cdot v}{\|v\|^2}
\end{aligned}
```

The pair is pruned if $`\|r(\tau)\| > r_{\text{bound},1} + r_{\text{bound},2} + \text{margin} + \text{gap}`$. When one of the geoms is a plane with unit normal $`n`$, the filter checks the minimum signed distance at the endpoints $`t \in \{0, 1\}`$, pruning the pair if $`\min(d_0,\, d_0 + n \cdot \Delta x) > r_{\text{bound}} + \text{margin} + \text{gap}`$.

### Swept broadphase AABBs

During sweep-and-prune ([Selection](index.md)), each geom's oriented bounding box is projected onto the three principal axes $`\hat{u}_j`$ of the scene covariance frame. For a fast-moving geom, the static half-projection along $`\hat{u}_j`$ is first inflated by its rotational sweep radius $`\|\Delta \omega\| \, r_{\text{bound}}`$ and intersected with its bounding sphere radius $`r_{\text{bound}}`$ (since rotation about the geom center cannot move any point outside $`r_{\text{bound}}`$). The resulting interval $`[\text{lo}_j, \text{hi}_j]`$ is then extended directionally by the linear displacement projection $`\Delta x \cdot \hat{u}_j`$:

``` math
\big[\text{lo}_j + \min(0, \Delta x \cdot \hat{u}_j) - \text{margin},\;
\text{hi}_j + \max(0, \Delta x \cdot \hat{u}_j) + \text{margin}\big]
```

Because per-body bounding volume hierarchies (`mjModel.bvh_aabb`) are precomputed statically in the body frame at compile time, mid-phase BVH tree traversal is bypassed for body pairs containing a fast-moving geom so that swept geom pairs are not culled by uninflated internal tree nodes.

## Conservative advancement

There are many approaches to computing the time of impact (see Erin Catto's [GDC 2013 presentation](https://box2d.org/files/ErinCatto_ContinuousCollision_GDC2013.pdf) for an overview). In MuJoCo, when discrete narrowphase collision detection finds no active surface contact (`dist < margin`) and at least one geom in the pair exceeds the fast-sweep threshold, we use a unilateral, *directed conservative advancement* algorithm to find the time of impact $`t \in (0, 1)`$.

<style>
  .ca-widget {
    border: 1px solid var(--color-background-border, #e2e8f0);
    border-radius: 10px;
    background: var(--color-background-secondary, #f8fafc);
    padding: 12px 14px;
    margin: 1em 0;
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  }
  .ca-scenes {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin-bottom: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--color-background-border, #e2e8f0);
  }
  .ca-controls {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 4px;
    margin-bottom: 10px;
  }
  .ca-btn {
    border: 1px solid var(--color-background-border, #cbd5e1);
    background: var(--color-background-primary, #ffffff);
    color: var(--color-foreground-primary, #1e293b);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12.5px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    font-family: inherit;
  }
  .ca-btn:hover {
    border-color: #3b82f6;
    color: #2563eb;
  }
  .ca-btn.ca-active {
    background: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
  }
  .ca-svg-wrap {
    background: var(--color-background-primary, #ffffff);
    border: 1px solid var(--color-background-border, #e2e8f0);
    border-radius: 8px;
    overflow: hidden;
  }
  .ca-svg-wrap svg {
    width: 100%;
    height: auto;
    display: block;
  }
  .ca-caption {
    margin: 10px 0 0 0;
    font-size: 13px;
    line-height: 1.5;
    color: var(--color-foreground-primary, #334155);
  }
  /* Theme-aware SVG classes */
  .ca-widget .ca-txt { fill: #334155; }
  .ca-widget .ca-muted { fill: #64748b; }
  .ca-widget .ca-g1-fill { fill: #dbeafe; fill-opacity: 0.75; stroke: #2563eb; }
  .ca-widget .ca-g2-fill { fill: #ede9fe; fill-opacity: 0.75; stroke: #7c3aed; }
  .ca-widget .ca-sphere1 { fill: none; stroke: #60a5fa; stroke-opacity: 0.45; }
  .ca-widget .ca-sphere2 { fill: none; stroke: #a78bfa; stroke-opacity: 0.45; }
  .ca-widget .ca-path1 { stroke: #93c5fd; stroke-opacity: 0.6; }
  .ca-widget .ca-path2 { stroke: #c4b5fd; stroke-opacity: 0.6; }
  .ca-widget .ca-plane { stroke: #10b981; stroke-opacity: 0.75; }
&#10;  body[data-theme="dark"] .ca-widget .ca-txt { fill: #e2e8f0; }
  body[data-theme="dark"] .ca-widget .ca-muted { fill: #94a3b8; }
  body[data-theme="dark"] .ca-widget .ca-g1-fill { fill: #1e3a8a; fill-opacity: 0.65; stroke: #60a5fa; }
  body[data-theme="dark"] .ca-widget .ca-g2-fill { fill: #4c1d95; fill-opacity: 0.65; stroke: #a78bfa; }
  body[data-theme="dark"] .ca-widget .ca-sphere1 { stroke: #60a5fa; stroke-opacity: 0.35; }
  body[data-theme="dark"] .ca-widget .ca-sphere2 { stroke: #a78bfa; stroke-opacity: 0.35; }
  body[data-theme="dark"] .ca-widget .ca-path1 { stroke: #3b82f6; stroke-opacity: 0.4; }
  body[data-theme="dark"] .ca-widget .ca-path2 { stroke: #8b5cf6; stroke-opacity: 0.4; }
  body[data-theme="dark"] .ca-widget .ca-plane { stroke: #34d399; stroke-opacity: 0.75; }
  @media (prefers-color-scheme: dark) {
    body[data-theme="auto"] .ca-widget .ca-txt { fill: #e2e8f0; }
    body[data-theme="auto"] .ca-widget .ca-muted { fill: #94a3b8; }
    body[data-theme="auto"] .ca-widget .ca-g1-fill { fill: #1e3a8a; fill-opacity: 0.65; stroke: #60a5fa; }
    body[data-theme="auto"] .ca-widget .ca-g2-fill { fill: #4c1d95; fill-opacity: 0.65; stroke: #a78bfa; }
    body[data-theme="auto"] .ca-widget .ca-sphere1 { stroke: #60a5fa; stroke-opacity: 0.35; }
    body[data-theme="auto"] .ca-widget .ca-sphere2 { stroke: #a78bfa; stroke-opacity: 0.35; }
    body[data-theme="auto"] .ca-widget .ca-path1 { stroke: #3b82f6; stroke-opacity: 0.4; }
    body[data-theme="auto"] .ca-widget .ca-path2 { stroke: #8b5cf6; stroke-opacity: 0.4; }
    body[data-theme="auto"] .ca-widget .ca-plane { stroke: #34d399; stroke-opacity: 0.75; }
  }
</style>
&#10;<div class="ca-widget" id="mj-ca-widget">
    <button type="button" class="ca-btn ca-scene-btn ca-active" data-scene="0">Basic: Sphere &amp; Box (Δω = 0)</button>
    <button type="button" class="ca-btn ca-scene-btn" data-scene="1">Complex: Two Rotating Boxes (Δω ≠ 0)</button>
</div>
&#10;  <div class="ca-svg-wrap">
    <svg viewBox="0 0 660 255" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="ca-arr-b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">
          <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#3b82f6"/>
        </marker>
        <marker id="ca-arr-p" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">
          <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#8b5cf6"/>
        </marker>
        <marker id="ca-arr-g" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">
          <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#10b981"/>
        </marker>
      </defs>
&#10;      <!-- Dynamic layer populated by script -->
      <g id="ca-layer-Main"></g>
    </svg>
&#10;  <p class="ca-caption" id="ca-status-text"></p>
&#10;<script>

// Copyright 2026 DeepMind Technologies Limited
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
&#10;(function() {
  const cBlue = (s) => `<span style="color:#3b82f6;font-weight:600;">${s}</span>`;
  const cPurple = (s) => `<span style="color:#8b5cf6;font-weight:600;">${s}</span>`;
  const cGreen = (s) => `<span style="color:#10b981;font-weight:600;">${s}</span>`;
  const cAmber = (s) => `<span style="color:#d97706;font-weight:600;">${s}</span>`;
&#10;  function rot(x, y, th) {
    const c = Math.cos(th), s = Math.sin(th);
    return [c * x - s * y, s * x + c * y];
  }
  function boxVerts(cx, cy, hx, hy, th) {
    return [[-hx, -hy], [hx, -hy], [hx, hy], [-hx, hy]].map(([x, y]) => {
      const [rx, ry] = rot(x, y, th);
      return [cx + rx, cy + ry];
    });
  }
  function ptSegClosest(px, py, ax, ay, bx, by) {
    const abx = bx - ax, aby = by - ay;
    const t = Math.max(0, Math.min(1, ((px - ax) * abx + (py - ay) * aby) / (abx * abx + aby * aby)));
    const qx = ax + t * abx, qy = ay + t * aby;
    return { d: Math.hypot(px - qx, py - qy), q: [qx, qy] };
  }
  function polyClosest(v1, v2) {
    let best = { d: 1e9, p1: [0, 0], p2: [0, 0] };
    for (const p1 of v1) {
      for (let i = 0; i < 4; i++) {
        const a = v2[i], b = v2[(i + 1) % 4];
        const res = ptSegClosest(p1[0], p1[1], a[0], a[1], b[0], b[1]);
        if (res.d < best.d) best = { d: res.d, p1: p1, p2: res.q };
      }
    }
    for (const p2 of v2) {
      for (let i = 0; i < 4; i++) {
        const a = v1[i], b = v1[(i + 1) % 4];
        const res = ptSegClosest(p2[0], p2[1], a[0], a[1], b[0], b[1]);
        if (res.d < best.d) best = { d: res.d, p1: res.q, p2: p2 };
      }
    }
    const nx = (best.p2[0] - best.p1[0]) / best.d;
    const ny = (best.p2[1] - best.p1[1]) / best.d;
    return { ...best, n: [nx, ny] };
  }
  function ptsStr(verts) {
    return verts.map(p => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
  }
  function arcPath(cx, cy, radius, a1, a2, ccw) {
    const x1 = cx + radius * Math.cos(a1), y1 = cy + radius * Math.sin(a1);
    const x2 = cx + radius * Math.cos(a2), y2 = cy + radius * Math.sin(a2);
    const sweep = ccw ? 0 : 1;
    return `M ${x1.toFixed(1)} ${y1.toFixed(1)} A ${radius} ${radius} 0 0 ${sweep} ${x2.toFixed(1)} ${y2.toFixed(1)}`;
  }
&#10;  // Scene 0: Basic example (Sphere gliding across a box corner onto its top face, dw = 0)
  function buildBasicScene() {
    const c0 = [135, 68], dx = [380, 118], r = 32;
    const box = { xmin: 230, xmax: 520, ymin: 162, ymax: 226 };
    const d_target = 3.0;
    const steps = [];
    let t = 0;
    for (let k = 0; k <= 2; k++) {
      const c1 = [c0[0] + t * dx[0], c0[1] + t * dx[1]];
      const bx = Math.max(box.xmin, Math.min(box.xmax, c1[0]));
      const by = Math.max(box.ymin, Math.min(box.ymax, c1[1]));
      const dc = Math.hypot(bx - c1[0], by - c1[1]);
      const n = [(bx - c1[0]) / dc, (by - c1[1]) / dc];
      const p1 = [c1[0] + r * n[0], c1[1] + r * n[1]];
      const p2 = [bx, by];
      const d = dc - r;
      const v_bound = n[0] * dx[0] + n[1] * dx[1];
      const dt = k < 2 ? Math.max(0, (d - d_target) / v_bound) : 0;
      steps.push({ k, t, c1, r, box, p1, p2, n, d, v_bound, dt, t_next: t + dt, c0, dx });
      t += dt;
    }
    return {
      steps,
      renderStep(s, idx) {
        const v1End = [s.c1[0] + s.dx[0] * 0.20, s.c1[1] + s.dx[1] * 0.20];
        const mid = [(s.p1[0] + s.p2[0]) / 2, (s.p1[1] + s.p2[1]) / 2];
        const tx = -s.n[1], ty = s.n[0];
        const planeHalf = 85;
        const pl1 = [s.p2[0] - tx * planeHalf, s.p2[1] - ty * planeHalf];
        const pl2 = [s.p2[0] + tx * planeHalf, s.p2[1] + ty * planeHalf];
        const nBase = [s.p2[0] - tx * 52, s.p2[1] - ty * 52];
        const nEnd = [nBase[0] + s.n[0] * 24, nBase[1] + s.n[1] * 24];
&#10;        const svg = `
          <!-- Swept center trajectory t in [0, 1] -->
          <line x1="${s.c0[0]}" y1="${s.c0[1]}" x2="${s.c0[0] + s.dx[0]}" y2="${s.c0[1] + s.dx[1]}" class="ca-path1" stroke-width="0.9" stroke-dasharray="3 3"/>
&#10;          <!-- Static Box (geom 2) -->
          <rect x="${s.box.xmin}" y="${s.box.ymin}" width="${s.box.xmax - s.box.xmin}" height="${s.box.ymax - s.box.ymin}" class="ca-g2-fill" stroke-width="1.2"/>
          <text x="${(s.box.xmin + s.box.xmax) / 2}" y="${(s.box.ymin + s.box.ymax) / 2 + 4}" text-anchor="middle" class="ca-txt" font-size="11" font-weight="600">static box (geom 2)</text>
&#10;          <!-- Moving Sphere (geom 1) -->
          <circle cx="${s.c1[0].toFixed(1)}" cy="${s.c1[1].toFixed(1)}" r="${s.r}" class="ca-g1-fill" stroke-width="1.2"/>
          <circle cx="${s.c1[0].toFixed(1)}" cy="${s.c1[1].toFixed(1)}" r="2.2" fill="#2563eb"/>
          <line x1="${s.c1[0].toFixed(1)}" y1="${s.c1[1].toFixed(1)}" x2="${v1End[0].toFixed(1)}" y2="${v1End[1].toFixed(1)}" stroke="#3b82f6" stroke-width="1.15" marker-end="url(#ca-arr-b)"/>
          <text x="${(s.c1[0] - 28).toFixed(1)}" y="${(s.c1[1] - s.r - 8).toFixed(1)}" class="ca-txt" font-size="11" font-weight="600">sphere (t=${s.t.toFixed(2)})</text>
&#10;          <!-- SAT separating plane perpendicular to n -->
          <line x1="${pl1[0].toFixed(1)}" y1="${pl1[1].toFixed(1)}" x2="${pl2[0].toFixed(1)}" y2="${pl2[1].toFixed(1)}" class="ca-plane" stroke-width="1.0" stroke-dasharray="4 3"/>
          <line x1="${nBase[0].toFixed(1)}" y1="${nBase[1].toFixed(1)}" x2="${nEnd[0].toFixed(1)}" y2="${nEnd[1].toFixed(1)}" stroke="#10b981" stroke-width="1.25" marker-end="url(#ca-arr-g)"/>
          <text x="${(nEnd[0] + 4).toFixed(1)}" y="${(nEnd[1] + 4).toFixed(1)}" fill="#10b981" font-size="11" font-weight="700">n</text>
&#10;          <!-- GJK closest segment dist(t) -->
          <line x1="${s.p1[0].toFixed(1)}" y1="${s.p1[1].toFixed(1)}" x2="${s.p2[0].toFixed(1)}" y2="${s.p2[1].toFixed(1)}" stroke="#f59e0b" stroke-width="1.1" stroke-dasharray="3 2"/>
          <circle cx="${s.p1[0].toFixed(1)}" cy="${s.p1[1].toFixed(1)}" r="2.5" fill="#2563eb"/>
          <circle cx="${s.p2[0].toFixed(1)}" cy="${s.p2[1].toFixed(1)}" r="2.5" fill="#7c3aed"/>
          <text x="${(mid[0] + tx * 28).toFixed(1)}" y="${(mid[1] + ty * 28).toFixed(1)}" text-anchor="middle" fill="#d97706" font-size="11" font-weight="600">dist = ${(s.d / 100).toFixed(2)}</text>
        `;
&#10;        const descriptions = [
          `Step 0 (t = 0.000): The ${cBlue('sphere')} starts above and to the left of the ${cPurple("box's top-left corner")}, so GJK's closest witness point on the box is the corner (${cAmber(`dist = ${(s.d/100).toFixed(2)}`)}) and the ${cGreen('separating normal n')} is tilted diagonally. By the Separating Axis Theorem (SAT), the ${cGreen('dashed green plane')} perpendicular to ${cGreen('n')} through the corner separates the two geoms; projecting ${cBlue('Δx₁')} onto ${cGreen('n')} gives v_bound = ${(s.v_bound/100).toFixed(2)}, allowing the sphere to safely advance up to that tilted plane (Δt = ${s.dt.toFixed(3)}).`,
          `Step 1 (t = ${s.t.toFixed(3)}): Advancing to the tilted plane carries the ${cBlue('sphere')} past the corner so it now sits directly above the ${cPurple('flat top face')} with minimal distance ${cAmber(`dist = ${(s.d/100).toFixed(2)}`)}. Because the closest feature on the box is now the top face, the ${cGreen('normal n')} rotates to vertical and the new ${cGreen('dashed green separating plane')} is horizontal. With Δω = 0 and a flat face, one more step Δt = ${s.dt.toFixed(3)} advances straight to target clearance.`,
          `Step 2 — Converged at TOI (t = ${s.t.toFixed(3)}): The ${cBlue('sphere')} lands at target clearance ${cAmber(`dist = ${(s.d/100).toFixed(2)}`)} just above the ${cPurple('top face')} in 2 iterations. Even with zero angular velocity, multiple iterations are needed whenever tangential motion glides a geom past a vertex or edge onto a new feature with a different ${cGreen('separating normal n')}.`
        ];
        return { svg, desc: descriptions[idx] };
      }
    };
  }
&#10;  // Scene 1: Complex example (Two boxes with different linear and angular velocities)
  function buildComplexScene() {
    const hx1 = 42, hy1 = 20, r1 = Math.hypot(hx1, hy1);
    const c1_0 = [105, 165], dx1 = [240, -45], th1_0 = -0.65, dw1 = 1.45;
&#10;    const hx2 = 28, hy2 = 46, r2 = Math.hypot(hx2, hy2);
    const c2_0 = [545, 115], dx2 = [-205, 40], th2_0 = 0.55, dw2 = -2.10;
&#10;    const d_target = 8.0;
    const steps = [];
    let t = 0;
    for (let k = 0; k <= 4; k++) {
      const c1 = [c1_0[0] + t * dx1[0], c1_0[1] + t * dx1[1]];
      const th1 = th1_0 + t * dw1;
      const c2 = [c2_0[0] + t * dx2[0], c2_0[1] + t * dx2[1]];
      const th2 = th2_0 + t * dw2;
      const v1 = boxVerts(c1[0], c1[1], hx1, hy1, th1);
      const v2 = boxVerts(c2[0], c2[1], hx2, hy2, th2);
      const gjk = polyClosest(v1, v2);
      const v_lin = gjk.n[0] * (dx1[0] - dx2[0]) + gjk.n[1] * (dx1[1] - dx2[1]);
      const v_rot = Math.abs(dw1) * r1 + Math.abs(dw2) * r2;
      const v_bound = v_lin + v_rot;
      const dt = k < 4 ? Math.max(0, (gjk.d - d_target) / v_bound) : 0;
      steps.push({ k, t, c1, th1, c2, th2, v1, v2, ...gjk, v_lin, v_rot, v_bound, dt, t_next: t + dt, r1, r2, dx1, dx2 });
      t += dt;
    }
&#10;    return {
      steps,
      renderStep(s, idx) {
        const v1End = [s.c1[0] + s.dx1[0] * 0.22, s.c1[1] + s.dx1[1] * 0.22];
        const v2End = [s.c2[0] + s.dx2[0] * 0.22, s.c2[1] + s.dx2[1] * 0.22];
        const mid = [(s.p1[0] + s.p2[0]) / 2, (s.p1[1] + s.p2[1]) / 2];
&#10;        const tx = -s.n[1], ty = s.n[0];
        const planeHalf = 78;
        const pl1 = [mid[0] - tx * planeHalf, mid[1] - ty * planeHalf];
        const pl2 = [mid[0] + tx * planeHalf, mid[1] + ty * planeHalf];
&#10;        const nBase = [mid[0] - tx * 48, mid[1] - ty * 48];
        const nEnd = [nBase[0] + s.n[0] * 26, nBase[1] + s.n[1] * 26];
&#10;        const svg = `
          <!-- Swept center trajectories t in [0, 1] -->
          <line x1="105" y1="165" x2="345" y2="120" class="ca-path1" stroke-width="0.9" stroke-dasharray="3 3"/>
          <line x1="545" y1="115" x2="340" y2="155" class="ca-path2" stroke-width="0.9" stroke-dasharray="3 3"/>
&#10;          <!-- Bounding spheres r_bound,1 and r_bound,2 -->
          <circle cx="${s.c1[0].toFixed(1)}" cy="${s.c1[1].toFixed(1)}" r="${s.r1.toFixed(1)}" class="ca-sphere1" stroke-width="0.85" stroke-dasharray="3 3"/>
          <circle cx="${s.c2[0].toFixed(1)}" cy="${s.c2[1].toFixed(1)}" r="${s.r2.toFixed(1)}" class="ca-sphere2" stroke-width="0.85" stroke-dasharray="3 3"/>
&#10;          <!-- Active Geoms -->
          <polygon points="${ptsStr(s.v1)}" class="ca-g1-fill" stroke-width="1.2"/>
          <polygon points="${ptsStr(s.v2)}" class="ca-g2-fill" stroke-width="1.2"/>
&#10;          <!-- Centers & velocity arrows -->
          <circle cx="${s.c1[0].toFixed(1)}" cy="${s.c1[1].toFixed(1)}" r="2.2" fill="#2563eb"/>
          <line x1="${s.c1[0].toFixed(1)}" y1="${s.c1[1].toFixed(1)}" x2="${v1End[0].toFixed(1)}" y2="${v1End[1].toFixed(1)}" stroke="#3b82f6" stroke-width="1.15" marker-end="url(#ca-arr-b)"/>
          <text x="${(s.c1[0] - 28).toFixed(1)}" y="${(s.c1[1] + s.r1 + 15).toFixed(1)}" class="ca-txt" font-size="11" font-weight="600">geom 1 (t=${s.t.toFixed(2)})</text>
&#10;          <!-- Angular velocity arc 1 (clockwise) -->
          <path d="${arcPath(s.c1[0], s.c1[1], s.r1 + 7, -2.3, -1.0, false)}" fill="none" stroke="#3b82f6" stroke-width="1.0" marker-end="url(#ca-arr-b)"/>
          <text x="${(s.c1[0] - 24).toFixed(1)}" y="${(s.c1[1] - s.r1 - 11).toFixed(1)}" fill="#3b82f6" font-size="10.5" font-style="italic">Δω₁, r₁</text>
&#10;          <circle cx="${s.c2[0].toFixed(1)}" cy="${s.c2[1].toFixed(1)}" r="2.2" fill="#7c3aed"/>
          <line x1="${s.c2[0].toFixed(1)}" y1="${s.c2[1].toFixed(1)}" x2="${v2End[0].toFixed(1)}" y2="${v2End[1].toFixed(1)}" stroke="#8b5cf6" stroke-width="1.15" marker-end="url(#ca-arr-p)"/>
          <text x="${(s.c2[0] - 28).toFixed(1)}" y="${(s.c2[1] + s.r2 + 15).toFixed(1)}" class="ca-txt" font-size="11" font-weight="600">geom 2 (t=${s.t.toFixed(2)})</text>
&#10;          <!-- Angular velocity arc 2 (counter-clockwise, faster) -->
          <path d="${arcPath(s.c2[0], s.c2[1], s.r2 + 7, -0.7, -2.1, true)}" fill="none" stroke="#8b5cf6" stroke-width="1.0" marker-end="url(#ca-arr-p)"/>
          <text x="${(s.c2[0] - 18).toFixed(1)}" y="${(s.c2[1] - s.r2 - 11).toFixed(1)}" fill="#8b5cf6" font-size="10.5" font-style="italic">Δω₂, r₂</text>
&#10;          <!-- Separating plane perpendicular to n (SAT) -->
          <line x1="${pl1[0].toFixed(1)}" y1="${pl1[1].toFixed(1)}" x2="${pl2[0].toFixed(1)}" y2="${pl2[1].toFixed(1)}" class="ca-plane" stroke-width="1.0" stroke-dasharray="4 3"/>
&#10;          <!-- Separating unit normal n anchored on the separating plane -->
          <line x1="${nBase[0].toFixed(1)}" y1="${nBase[1].toFixed(1)}" x2="${nEnd[0].toFixed(1)}" y2="${nEnd[1].toFixed(1)}" stroke="#10b981" stroke-width="1.25" marker-end="url(#ca-arr-g)"/>
          <text x="${(nEnd[0] + 4).toFixed(1)}" y="${(nEnd[1] + 3).toFixed(1)}" fill="#10b981" font-size="11" font-weight="700">n</text>
&#10;          <!-- GJK closest segment dist(t) -->
          <line x1="${s.p1[0].toFixed(1)}" y1="${s.p1[1].toFixed(1)}" x2="${s.p2[0].toFixed(1)}" y2="${s.p2[1].toFixed(1)}" stroke="#f59e0b" stroke-width="1.1" stroke-dasharray="3 2"/>
          <circle cx="${s.p1[0].toFixed(1)}" cy="${s.p1[1].toFixed(1)}" r="2.5" fill="#2563eb"/>
          <circle cx="${s.p2[0].toFixed(1)}" cy="${s.p2[1].toFixed(1)}" r="2.5" fill="#7c3aed"/>
          <text x="${(mid[0] + tx * 26).toFixed(1)}" y="${(mid[1] + ty * 26).toFixed(1)}" text-anchor="middle" fill="#d97706" font-size="11" font-weight="600">dist = ${(s.d / 100).toFixed(2)}</text>
        `;
&#10;        const descriptions = [
          `Step 0 (t = 0.000): GJK finds the closest witness points and ${cGreen('separating normal n')} with initial distance ${cAmber(`dist = ${(s.d/100).toFixed(2)}`)}. By the Separating Axis Theorem (SAT), the ${cGreen('dashed green plane')} perpendicular to ${cGreen('n')} separates ${cBlue('geom 1')} and ${cPurple('geom 2')}. Projecting the relative linear displacement onto ${cGreen('n')} (${(s.v_lin/100).toFixed(2)}) and adding both rotational sweep bounds (${(s.v_rot/100).toFixed(2)}) gives v_bound = ${(s.v_bound/100).toFixed(2)}, so both geoms can safely advance to that separating plane by Δt = (dist − dist_target) / v_bound = ${s.dt.toFixed(3)}.`,
          `Step 1 (t = ${s.t.toFixed(3)}): Advancing both geoms linearly and rotationally by Δt = 0.539 brings them up to the previous separating plane without overlapping. Because ${cBlue('geom 1')} rotates clockwise (${cBlue('Δω₁')}) and ${cPurple('geom 2')} rotates faster counter-clockwise (${cPurple('Δω₂')}), their new closest points are still separated by ${cAmber(`dist = ${(s.d/100).toFixed(2)}`)} across a new ${cGreen('dashed green separating plane')} perpendicular to ${cGreen('n')}, allowing a second safe step of Δt = ${s.dt.toFixed(3)}.`,
          `Step 2 (t = ${s.t.toFixed(3)}): At the updated poses, the rotating corners swing closer together and the ${cGreen('SAT separating plane')} tilts as ${cGreen('n')} rotates upward. GJK measures ${cAmber(`dist = ${(s.d/100).toFixed(2)}`)} and bounds the closing rate across the new separating plane by v_bound = ${(s.v_bound/100).toFixed(2)}, advancing both geoms by Δt = ${s.dt.toFixed(3)}.`,
          `Step 3 (t = ${s.t.toFixed(3)}): As the gap narrows to ${cAmber(`dist = ${(s.d/100).toFixed(2)}`)}, the ${cGreen('dashed green separating plane')} aligns with the approaching vertex-face contact and the projected closing rate drops to v_bound = ${(s.v_bound/100).toFixed(2)}, giving a refinement step of Δt = ${s.dt.toFixed(3)}.`,
          `Step 4 — Converged at TOI (t = ${s.t.toFixed(3)}): Minimal distance ${cAmber(`dist = ${(s.d/100).toFixed(2)}`)} reaches the target clearance dist_target just above margin and the search terminates. Keeping this small positive clearance guarantees that a valid ${cGreen('separating plane')} still exists at TOI, so GJK directly returns well-defined witness points and ${cGreen('contact normal n')} without invoking EPA.`
        ];
        return { svg, desc: descriptions[idx] };
      }
    };
  }
&#10;  const scenes = [buildBasicScene(), buildComplexScene()];
  let curScene = 0;
  let curStep = 0;
&#10;  const gMain = document.getElementById('ca-layer-Main');
  const statusEl = document.getElementById('ca-status-text');
  const stepBtnContainer = document.getElementById('ca-step-btn-container');
&#10;  function rebuildStepButtons() {
    const steps = scenes[curScene].steps;
    stepBtnContainer.innerHTML = steps.map((s, i) => {
      const label = i === 0 ? 'Step 0 (t=0)' : (i === steps.length - 1 ? `Step ${i} (TOI)` : `Step ${i}`);
      return `<button type="button" class="ca-btn ca-step-btn" data-step="${i}">${label}</button>`;
    }).join('');
    stepBtnContainer.querySelectorAll('.ca-step-btn').forEach((btn, i) => {
      btn.addEventListener('click', () => render(i));
    });
  }
&#10;  function render(idx) {
    const scene = scenes[curScene];
    curStep = idx;
    const s = scene.steps[idx];
&#10;    document.querySelectorAll('#mj-ca-widget .ca-scene-btn').forEach((b, i) => {
      b.classList.toggle('ca-active', i === curScene);
    });
    stepBtnContainer.querySelectorAll('.ca-step-btn').forEach((b, i) => {
      b.classList.toggle('ca-active', i === idx);
    });
&#10;    const out = scene.renderStep(s, idx);
    gMain.innerHTML = out.svg;
    statusEl.innerHTML = out.desc;
  }
&#10;  document.querySelectorAll('#mj-ca-widget .ca-scene-btn').forEach((btn, i) => {
    btn.addEventListener('click', () => {
      curScene = i;
      rebuildStepButtons();
      render(0);
    });
  });
&#10;  rebuildStepButtons();
  render(0);
})();

</script>

At each iteration, GJK evaluates the minimal distance $`\text{dist}(t)`$ between the two geoms, closest witness points $`(x_1(t), x_2(t))`$, and separating unit normal $`n = (x_2(t) - x_1(t)) / \text{dist}(t)`$ (pointing from geom 1 to geom 2) at the current advanced poses. By the Separating Axis Theorem (SAT), the supporting planes perpendicular to $`n`$ at $`x_1(t)`$ and $`x_2(t)`$ bound every pair of points $`p_1(t) \in \text{geom } 1`$ and $`p_2(t) \in \text{geom } 2`$ along $`n`$:

``` math
(p_2(t) - p_1(t)) \cdot n \;\ge\; (x_2(t) - x_1(t)) \cdot n \;=\; \text{dist}(t)
```

As each geom translates and rotates about its center $`c_i`$ with step displacements $`(\Delta x_i, \Delta \omega_i)`$, any point $`p_i`$ on geom $`i`$ moves with velocity $`\dot{p}_i = \Delta x_i + \Delta \omega_i \times (p_i - c_i)`$ with respect to $`t`$. Because every point on geom $`i`$ lies within its bounding sphere of radius $`r_{\text{bound},i}`$ centered at $`c_i`$ ($`\|p_i - c_i\| \le r_{\text{bound},i}`$) and $`\|n\| = 1`$, each rotational term satisfies $`\big|n \cdot (\Delta \omega_i \times (p_i - c_i))\big| \le \|\Delta \omega_i\| \, r_{\text{bound},i}`$. Projecting the relative closing velocity $`\dot{p}_1 - \dot{p}_2`$ onto the fixed axis $`n`$ therefore gives an upper bound $`v_{\text{bound}}`$ on how fast any two points on the geoms can close across the separating plane:

``` math
\begin{aligned}
\begin{aligned}
n \cdot (\dot{p}_1 - \dot{p}_2)
&= n \cdot (\Delta x_1 - \Delta x_2)
+ n \cdot \big(\Delta \omega_1 \times (p_1 - c_1)\big)
- n \cdot \big(\Delta \omega_2 \times (p_2 - c_2)\big) \\
&\le n \cdot (\Delta x_1 - \Delta x_2)
+ \|\Delta \omega_1\| \, r_{\text{bound},1}
+ \|\Delta \omega_2\| \, r_{\text{bound},2}
\;\equiv\; v_{\text{bound}}
\end{aligned}
\end{aligned}
```

Unlike the worst-case isotropic sweep $`s_1 + s_2`$—which bounds linear motion in all directions and stalls when a geom moves rapidly tangentially while grazing a surface—projecting $`\Delta x_1 - \Delta x_2`$ onto $`n`$ discards tangential linear motion parallel to the separating plane.

If $`v_{\text{bound}} \le 0`$, the geoms cannot close along $`n`$ and the search terminates without contact. Otherwise, advancing by $`\Delta t \ge 0`$ can reduce the projection along $`n`$ by at most $`\Delta t \, v_{\text{bound}}`$, so the true separation at $`t + \Delta t`$ is bounded below by

``` math
\text{dist}(t + \Delta t) \;\ge\; \min_{p_1, p_2}\,(p_2(t + \Delta t) - p_1(t + \Delta t)) \cdot n
\;\ge\; \text{dist}(t) - \Delta t \, v_{\text{bound}}
```

Setting this lower bound equal to a target clearance $`\text{dist}_{\text{target}} = \text{margin} + 0.02\,(\text{dist}(0) - \text{margin})`$ just above `margin` ($`\text{dist}(t) - \Delta t \, v_{\text{bound}} = \text{dist}_{\text{target}}`$) yields the largest guaranteed-safe step:

``` math
\Delta t = \frac{\text{dist}(t) - \text{dist}_{\text{target}}}{v_{\text{bound}}}, \qquad t \leftarrow t + \Delta t
```

Unlike *bilateral advancement*—which can overshoot into overlap and step both forward and backward using signed penetration depth queries—this unilateral advancement approaches $`\text{dist}_{\text{target}}`$ strictly from the separated side ($`\text{dist}(t) > \text{margin}`$), so GJK always returns well-defined witness points and a separating normal without invoking EPA. When [multiccd](../XMLreference.md) is enabled (or one geom is a plane), polygon clipping extracts up to four contact points at the advanced impact pose.

## Line-of-sight raycasting

The witness points $`x_1(t)`$ and $`x_2(t)`$ found at impact time $`t`$ are mapped from each geom's advanced local frame back to its $`t = 0`$ world pose $`x_1(0)`$ and $`x_2(0)`$, and interpolated by each geom's sweep fraction $`w_i = s_i / (s_1 + s_2)`$ to form the contact position:

``` math
x_{\text{contact}} = w_1 \, x_1(0) + w_2 \, x_2(0)
```

Because narrowphase evaluates each geom pair independently, a fast-moving geom could otherwise generate a speculative contact with a second object sitting *behind* an intervening obstacle (for example, a falling box registering a speculative contact with the floor underneath a thin tabletop it is about to strike). To enforce line-of-sight, a ray segment is cast between the $`t = 0`$ witness points $`x_1(0)`$ and $`x_2(0)`$ and tested against all other collidable geoms compatible with both bodies; if any intervening geom intersects the segment, the occluded speculative contact is discarded.

## Effective contact distance

Because a speculative contact is created at $`t = 0`$ before geometric overlap occurs, its true separation exceeds `margin`. Passing the true distance to the constraint solver would either leave the contact inactive or, if activated with zero penetration, cause the velocity damper in the reference acceleration

``` math
\ari = -b_i (J v)_i - k_i r_i
```

to arrest $`100\%`$ of the closing speed immediately—freezing the body in mid-air at $`t = 0`$.

Instead, collision detection inverts this reference acceleration equation to solve for an effective contact distance $`\text{dist} = \text{margin} - \delta`$ such that the constraint solver arrests $`(1 - t)`$ of the incoming normal speed $`|v_n|`$ over the timestep, leaving the remaining fraction $`t`$ of the velocity to carry the geom onto the contact surface at the end of the step ($`z_1 = z_0 + h v_1 = 0`$).

Under the standard Euler integrator, a contact with dimensionless single-step stiffness $`k_0 = h^2 k`$ and damping $`b_0 = h b`$ (derived from <span class="at">solref</span> and <span class="at">solimp</span>) produces a single-step normal velocity change

``` math
h \ari = b_0 |v_n| + k_0 \frac{\delta}{h}
```

Setting $`h \ari = (1 - t)|v_n|`$ and solving for the effective penetration depth $`\delta`$ yields

``` math
\delta = \frac{1 - t - b_0}{k_0} \, h |v_n|, \qquad \text{dist} = \text{margin} - \delta
```

Under the implicit [discrete](../XMLreference.md) integrator, where the spring-damper is evaluated at the end-of-step position and divided by the implicit factor $`1 + b_0 + k_0`$, the numerator $`1 - t - b_0`$ is replaced by $`1 - t - t(b_0 + k_0)`$:

``` math
\delta_{\text{discrete}} = \frac{1 - t - t(b_0 + k_0)}{k_0} \, h |v_n|
```

Notice that for default critically damped contacts ($`b_0 = 1`$), $`1 - t - b_0 = -t < 0`$, so $`\delta < 0`$ and $`\text{dist} > \text{margin}`$: the spring term pulls *back* against the damper by $`t |v_n|`$ so that only $`(1 - t)|v_n|`$ is removed during the approach step. Speculative contacts remain active even when $`\text{dist} \ge \text{margin}`$.

### Modeling notes

- **Elastic restitution:** Standard speculative contacts split impact across two steps—arresting $`(1 - t)|v_n|`$ to land on the surface on the first step, and resolving surface contact on the next. When modeling nearly elastic collisions via direct negative <span class="at">solref</span> (e.g. $`b_0 \approx 2`$ so the damper reverses $`v_n \to -v_n`$ in a single step, as in [newton.xml](https://github.com/google-deepmind/mujoco/blob/main/model/speculative/newton.xml)), set the stiffness to zero (e.g. `solref="0 -499"`) with a stiff impedance (`solimp="0.995 0.995 0.001"`) so the speculative position spring term does not cancel out the elastic damper during the approach step (noting that zero stiffness provides no static position spring for resting contacts).
- **Single-pass pre-step velocities:** Because speculative sweeps use pre-step velocities (`mjData.qvel`), a stationary intermediate body struck by a fast neighbor acquires its post-impact velocity only after the solver runs. In multi-body impact chains (such as Newton's cradle), keep a small clearance between adjacent bodies or choose a timestep where a single step's travel does not jump across two gaps at once.
