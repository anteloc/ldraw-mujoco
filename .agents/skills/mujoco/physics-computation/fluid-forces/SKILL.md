---
name: fluid-forces
description: 'MuJoCo fluid dynamics: the inertia-box model and the ellipsoid model for drag, lift and added mass, with the fluidshape/fluidcoef parameters, density and viscosity options. Use when simulating bodies moving through air or water.'
---

# MuJoCo Fluid Forces

Use this skill to make bodies fly or swim: add drag, viscous resistance, lift
and added mass from a surrounding medium. MuJoCo does not simulate the fluid.
It provides two *stateless* phenomenological models (no extra state for the
fluid) that capture the salient forces on rigid bodies moving through air or
water. Fluid forces are passive forces, part of `mjData.qfrc_passive`; see
[physics computation](../SKILL.md) for where they enter the pipeline.

## Quick start

1. Set the medium's [density](../../reference/xml-reference/SKILL.md) (ρ) and
   [viscosity](../../reference/xml-reference/SKILL.md) (β) options to positive
   values. This enables fluid forces.
2. Pick a model:
   - **Inertia model** (default): uses only density and viscosity and infers
     shape from each body's equivalent inertia box.
   - **Ellipsoid model**: set the geom attribute
     [fluidshape](../../reference/xml-reference/SKILL.md) to `ellipsoid`. This
     disables the inertia model for the parent body. Tune the 5 per-geom
     [fluidcoef](../../reference/xml-reference/SKILL.md) numbers.
3. Use the `implicit` or `implicitfast`
   [integrator](../../reference/xml-reference/SKILL.md). Fluid forces are
   velocity-dependent, implicit integration greatly improves stability, and
   the analytic derivatives for both models are fully implemented.
4. Optionally set [wind](../../reference/xml-reference/SKILL.md), a 3D vector
   subtracted from the body linear velocity in the fluid computation.

Reference viscosities from the docs: about `1.48e-5 m²/s` for
ambient-temperature air and `0.89e-4 m²/s` for water.

Example models: [cards.xml](https://github.com/deepmind/mujoco/blob/main/model/cards/cards.xml)
(falling playing cards). The motivating use case for the ellipsoid model is
insect flight (a flight-capable Drosophila model, Vaxenburg2024).

## Choosing a model

| | Inertia model | Ellipsoid model |
|----|----|----|
| Activation | density/viscosity > 0 | plus `fluidshape="ellipsoid"` per geom |
| Shape | body equivalent-inertia box | ellipsoid approximation of each geom |
| Terms | quadratic drag, viscous resistance | added mass, drag, Magnus lift, Kutta lift, viscous resistance |
| Tunable per element | none | 5 `fluidcoef` values |
| Granularity | per body | per geom |

Use the ellipsoid model when you need lift (wings, plates, spinning balls) or
finer control of individual force types.

## Inertia model

For a body with mass `𝓜` and inertia `𝓘`, the half-dimensions of the
equivalent inertia box (which can also be visualized) are

```
r_x = sqrt( 3/(2𝓜) · (I_yy + I_zz − I_xx) )
r_y = sqrt( 3/(2𝓜) · (I_zz + I_xx − I_yy) )
r_z = sqrt( 3/(2𝓜) · (I_xx + I_yy − I_zz) )
```

With `v`, `ω` the body-local linear and angular velocity (aligned with the
box), force `f = f_D + f_V` and torque `g = g_D + g_V`:

| Term | Formula (component i; j, k the other axes) | Regime |
|----|----|----|
| Quadratic drag force | `f_D,i = −2 ρ r_j r_k |v_i| v_i` | high Reynolds number |
| Quadratic drag torque | `g_D,i = −½ ρ r_i (r_j⁴ + r_k⁴) |ω_i| ω_i` | high Reynolds number |
| Viscous force | `f_V,i = −6 β π r_eq v_i` | low Reynolds number |
| Viscous torque | `g_V,i = −8 β π r_eq³ ω_i` | low Reynolds number |

`r_eq = (r_x + r_y + r_z)/3` (equivalent sphere). Viscosity can be used
without density just to make a simulation more damped.

## Ellipsoid model

### fluidcoef

| Index | Description | Symbol | Default |
|----|----|----|----|
| 0 | Blunt drag coefficient | `C_D,blunt` | 0.5 |
| 1 | Slender drag coefficient | `C_D,slender` | 0.25 |
| 2 | Angular drag coefficient | `C_D,angular` | 1.5 |
| 3 | Kutta lift coefficient | `C_K` | 1.0 |
| 4 | Magnus lift coefficient | `C_M` | 1.0 |

Force `f = f_A + f_D + f_M + f_K + f_V`; torque `g = g_A + g_D + g_V`
(Added mass, Drag, Magnus, Kutta, Viscous). Drag, Magnus and Kutta scale with
their coefficients, viscous resistance with β; **added mass cannot be scaled**.

Notation: ellipsoid semi-axes `r = {r_x, r_y, r_z}` in a frame aligned with
the ellipsoid; `r_max`, `r_min`, `r_mid` the sorted semi-axes; volume
`V = 4π r_x r_y r_z / 3`. Reynolds number `Re = u l / β`.

### Projected area (used by drag and Kutta lift)

Area of the ellipsoid projected onto the plane normal to unit vector `u`:

```
A_proj(u) = π sqrt( (r_y⁴ r_z⁴ u_x² + r_z⁴ r_x⁴ u_y² + r_x⁴ r_y⁴ u_z²)
                  / (r_y² r_z² u_x² + r_z² r_x² u_y² + r_x² r_y² u_z²) )
```

### Added mass

Inertia of the fluid moved by the body (from potential flow, present even for
inviscid flow); zero for constant linear velocity. Assuming three planes of
symmetry (`∘` is element-wise):

```
f_A = −m_A ∘ v̇ + (m_A ∘ v) × ω
g_A = −I_A ∘ ω̇ + (m_A ∘ v) × v + (I_A ∘ ω) × ω
```

With the non-dimensional coefficients
`κ_i = ∫₀^∞ r_i r_j r_k / sqrt((r_i² + λ)³ (r_j² + λ)(r_k² + λ)) dλ`:

```
m_A,i = ρ V κ_i / (2 − κ_i)
I_A,i = (ρ V / 5) · (r_j² − r_k²)² (κ_k − κ_j) / (2(r_j² − r_k²) + (r_j² + r_k²)(κ_j − κ_k))
```

### Drag (quadratic)

Uses the projected area `A_proj(v)` and the maximum projected area
`A_max = π r_max r_mid`:

```
f_D = −ρ [ C_D,blunt A_proj(v) + C_D,slender (A_max − A_proj(v)) ] ‖v‖ v
```

Angular drag uses the moment of inertia of the maximum swept ellipsoid per
axis, `I_D,ii = (8π/15) r_i max(r_j, r_k)⁴`, and `I_max` (each entry the
largest component of `I_D`):

```
g_D = −ρ ω ( [ C_D,angular I_D + C_D,slender (I_max − I_D) ] · ω )
```

The viscous terms were chosen conservatively and may overestimate
dissipation, because they also reduce the stiffness of the equations of
motion. Drag coefficients and reference areas generally need tuning to the
problem's physics and scales (e.g. `C_D` decreases with Reynolds number).

### Viscous resistance (linear drag)

Stokes' law for the equivalent sphere, `r_D = (r_x + r_y + r_z)/3`; accurate
for Reynolds numbers around or below O(10):

```
f_V = −6 π r_D β v
g_V = −8 π r_D³ β ω
```

For room-temperature air Stokes' law becomes accurate if
`u · l ≲ 2e-4 m²/s` (`u` speed, `l` characteristic length).

### Magnus lift

Force on a spinning body moving through the fluid (`C_M` typically 1):

```
f_M = C_M ρ V ω × v
```

Magnus and added-mass forces can have opposite signs; for `ω = {0,0,ω_z}`,
`v = {v_x, v_y, 0}` the x component of their sum is
`f / (π ρ r_z) = v_y ω_z (2 r_x min{r_x, r_z} − (r_x + r_z)²)`.

### Kutta lift

Lift from circulation that holds the rear stagnation point at a sharp trailing
edge (slender bodies, airfoil edges). With the cross-section normal
`n_s,v = {r_y r_z/r_x v_x, r_z r_x/r_y v_y, r_x r_y/r_z v_z}`, its unit vector
`n̂_s,v`, and `v = v_∥ + v_⊥` where `v_⊥ = (v · n̂_s,v) n̂_s,v`:

```
f_K = (C_K ρ A_proj(v) / ‖v‖) (v × v_∥) × v
    = C_K ρ A_proj(v) (v̂ · n̂_s,v) (n̂_s,v × v) × v
```

For spheres `n̂_s,v ≡ v̂`, so `f_K = 0` by construction. Motion in a plane
where the body is blunt (equal semi-axes) produces no circulation.

## Pitfalls

- Fluid forces are off unless density and/or viscosity are positive.
- Setting `fluidshape="ellipsoid"` on a geom switches its parent body away
  from the inertia model; the inertia model then no longer applies to that body.
- The inertia model sees only each body's mass and inertia (its equivalent
  inertia box), not the geom shapes.
- `Euler` treats only joint damping implicitly; prefer `implicitfast` or
  `implicit` with fluid forces.
- Both models are phenomenological and stateless: the fluid has no state of
  its own. Drag coefficients and reference areas need tuning to the problem.

## Source docs

Verbatim copies, for details not covered above:

- [computation/fluid.md](references/computation-fluid.md)
