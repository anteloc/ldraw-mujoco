---
name: speculative-contacts
description: 'Speculative contacts in MuJoCo: broadphase and sphere filtering, conservative advancement, line-of-sight raycasting and effective contact distance for detecting contacts before penetration. Use when fast-moving or thin objects tunnel through each other, or when tuning contact margins for early detection.'
---

# MuJoCo Speculative Contacts

Use this skill to stop fast-moving or thin geoms from *tunneling* through each
other. Discrete collision detection only checks poses at timesteps, so a geom
whose displacement over one step exceeds its thickness can pass from one side
to the other without ever overlapping. Speculative contacts predict collisions
between the current and next timestep and add contacts before penetration.
Collision detection basics (broadphase, filters, margin/gap, CCD) are in
[physics computation](../SKILL.md).

## Enable

Turn on the [speculative](../../reference/xml-reference/SKILL.md) flag.

Requirements and support:

- Requires the [nativeccd](../../reference/xml-reference/SKILL.md) pipeline
  (the default CCD pipeline).
- Supported: planes, spheres, capsules, ellipsoids, cylinders, boxes, convex
  meshes, and [multiccd](../../reference/xml-reference/SKILL.md) multi-point
  surface contacts.
- Not supported: height fields, SDFs, flexes.

Speculative contacts behave like normal contacts and are treated the same by
the solver. Example models:
[model/speculative/](https://github.com/google-deepmind/mujoco/tree/main/model/speculative).

**Cost.** Collision overhead per step depends on the scene: it scales with the
number of geoms whose single-step travel exceeds their thickness and with the
candidate pairs they sweep. Preventing tunneling often allows a larger
timestep, which can reduce total wall-clock time.

## Pipeline

1. **Broadphase and sphere filtering**: expand sweep-and-prune AABBs and
   bounding-sphere tests by each fast geom's motion over the step.
2. **Conservative advancement**: sweep candidate pairs to find the time of
   impact (TOI) `0 < t < 1` as a fraction of the timestep.
3. **Line-of-sight raycasting**: drop contacts hidden behind another geom.
4. **Effective contact distance**: invert the reference acceleration
   `aref_i = −b_i (J v)_i − k_i r_i` to get a synthetic `dist`, so the solver
   arrests `(1 − t)` of the normal velocity and lands the geom on the surface
   at `t = 1`.

### 1. Fast-geom test and swept bounds

A geom counts as fast-moving only if its sweep distance

```
s = ‖Δx‖ + ‖Δω‖ r_bound,   Δx = Δt v,   Δω = Δt ω
```

(an upper bound on the travel of any surface point; `r_bound` is the
bounding-sphere radius) exceeds the minimum of its local AABB half-extents.
Other geoms use standard discrete bounds, so slow objects add no overhead.

**Swept sphere filter.** With initial centre separation `p = x₂ − x₁` and
relative displacement `v = Δx₂ − Δx₁`, the closest approach on `[0, 1]` is at
`τ = clamp(t*, 0, 1)`, `t* = −(p · v)/‖v‖²`. The pair is pruned if
`‖p + τ v‖ > r_bound,1 + r_bound,2 + margin + gap`. Against a plane with unit
normal `n`, it is pruned if `min(d₀, d₀ + n · Δx) > r_bound + margin + gap`.

**Swept AABBs.** In sweep-and-prune, a fast geom's half-projection on each
principal axis `û_j` is inflated by `‖Δω‖ r_bound` (capped at `r_bound`), then
extended by the linear motion:
`[lo_j + min(0, Δx·û_j) − margin, hi_j + max(0, Δx·û_j) + margin]`. Mid-phase
BVH traversal (`mjModel.bvh_aabb`, static, body frame) is bypassed for body
pairs containing a fast geom, so swept pairs are not culled by uninflated
nodes.

### 2. Conservative advancement

Runs when discrete narrowphase finds no active surface contact
(`dist < margin`) and at least one geom of the pair exceeds the fast-sweep
threshold. It is unilateral and *directed*:

- Each iteration, GJK gives `dist(t)`, witness points `x₁(t)`, `x₂(t)` and the
  separating normal `n` (from geom 1 to geom 2).
- Closing-speed bound across the separating plane:
  `v_bound = n · (Δx₁ − Δx₂) + ‖Δω₁‖ r_bound,1 + ‖Δω₂‖ r_bound,2`.
  Tangential linear motion is discarded, so grazing fast motion does not stall
  the search.
- If `v_bound ≤ 0` the geoms cannot close: no contact.
- Otherwise step `Δt = (dist(t) − dist_target)/v_bound`, `t ← t + Δt`, with
  `dist_target = margin + 0.02 (dist(0) − margin)`.

The search approaches the target strictly from the separated side, so GJK
always returns well-defined witness points and a normal without EPA. With
multiccd enabled (or when one geom is a plane), polygon clipping extracts up
to four contact points at the impact pose.

### 3. Line-of-sight raycasting

Witness points at TOI are mapped back to each geom's `t = 0` pose and blended
by sweep fraction `w_i = s_i/(s₁ + s₂)`:
`x_contact = w₁ x₁(0) + w₂ x₂(0)`. A ray segment between `x₁(0)` and `x₂(0)`
is tested against all other collidable geoms compatible with both bodies; if
anything intersects it, the speculative contact is discarded. This prevents,
for example, a falling box registering a contact with the floor beneath a thin
tabletop it is about to hit.

### 4. Effective contact distance

A speculative contact exists at `t = 0`, before overlap, so its true distance
exceeds `margin`. Using it would leave the contact inactive, or (if activated
at zero penetration) make the damper stop 100% of the closing speed at once,
freezing the body in mid-air. Instead, `dist = margin − δ` is chosen so the
solver removes `(1 − t)|v_n|` over the step.

With single-step stiffness `k₀ = h² k` and damping `b₀ = h b` (from `solref`
and `solimp`):

| Integrator | Effective penetration δ |
|----|----|
| Euler (standard) | `δ = (1 − t − b₀)/k₀ · h |v_n|` |
| [discrete](../../reference/xml-reference/SKILL.md) | `δ = (1 − t − t(b₀ + k₀))/k₀ · h |v_n|` |

For default critically damped contacts (`b₀ = 1`), `1 − t − b₀ = −t < 0`, so
`δ < 0` and `dist > margin`. Speculative contacts stay active even when
`dist ≥ margin`.

## Pitfalls

- **Pre-step velocities only.** Sweeps use `mjData.qvel` and ignore
  acceleration (collision runs in the position stage, and acceleration adds
  only an O(Δt²) displacement). A slow or stationary geom accelerated across
  an obstacle within one step (large applied force, gravity, a body pushing it
  in the constraint solve) can still tunnel. The timestep cannot be made
  arbitrarily large.
- **Sensors fire early.** Speculative contacts appear in `mjData.contact`
  before surface contact, so contact and touch sensors can trigger a step
  early.
- **Elastic restitution.** Impact is split over two steps: land on the surface,
  then resolve surface contact. For nearly elastic collisions via direct
  negative `solref` (`b₀ ≈ 2`, as in
  [newton.xml](https://github.com/google-deepmind/mujoco/blob/main/model/speculative/newton.xml)),
  set the stiffness to zero, e.g. `solref="0 -499"`, with a stiff impedance
  `solimp="0.995 0.995 0.001"`, so the speculative spring term does not cancel
  the elastic damper. Zero stiffness gives no static position spring for
  resting contacts.
- **Impact chains.** A stationary body struck by a fast neighbour gets its
  post-impact velocity only after the solver runs. In chains such as Newton's
  cradle, keep a small clearance between neighbours, or choose a timestep
  where one step's travel does not jump across two gaps at once.

## Source docs

Verbatim copies, for details not covered above:

- [computation/speculative.md](references/computation-speculative.md)
