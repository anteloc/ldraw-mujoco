---
name: accelerated-simulation
description: 'Running MuJoCo on accelerators with batched, parallel simulation: MuJoCo XLA (MJX, JAX) and MuJoCo Warp (MJWarp, NVIDIA Warp). Use when many environments must step in parallel on GPU/TPU, for reinforcement learning, or when choosing between MJX, MJWarp and CPU MuJoCo.'
---

# Accelerated Simulation

MuJoCo has two ways to step many worlds in parallel on accelerators. MJX (`mujoco.mjx`) is a JAX API. MuJoCo Warp (`mujoco_warp`, MJWarp) is MuJoCo written in NVIDIA Warp. Use this skill to choose between them and CPU MuJoCo, then load the matching subskill.

## Mental model

- Both copy a compiled `mjModel`/`mjData` to the device with `put_model` / `put_data` (or `make_data`), then step with `step`. Function names are MuJoCo's, in PEP 8 style.
- Both are built for **throughput** (total steps per unit time over large batches), not **latency** (time for one step). On a single scene, CPU MuJoCo is faster. MJX-JAX can be 10x slower there.
- MJX has two implementations: MJX-JAX (pure JAX, used when no `impl` is passed) and MJX-Warp (`impl='warp'`, which runs MuJoCo Warp under a JAX API).
- On GPU, contact and constraint buffers have a fixed size. Warp-based paths need `naconmax`/`nconmax` and `njmax` set when you create data, and overflowing them is undefined behaviour.

## Which backend

| Need | Pick |
|---|---|
| Real-time control (MPC), interactive tools, teleoperation, single scenes | CPU MuJoCo (`mj_step`) |
| Many CPU simulations with fast, many-core hardware | [`mujoco.rollout`](../python-bindings/SKILL.md), but host-device transfers can be the bottleneck if learning runs on GPU |
| Large batches on NVIDIA GPUs, complex scenes, many contacts, meshes, PyTorch | [MuJoCo Warp](mujoco-warp/SKILL.md) |
| Large batches inside a JAX program on NVIDIA GPUs | [MJX](mjx/SKILL.md) with `impl='warp'` |
| AMD GPUs, Apple Silicon or Google Cloud TPUs | [MJX](mjx/SKILL.md), MJX-JAX implementation |
| Gradients through the dynamics | [MJX](mjx/SKILL.md), MJX-JAX (mostly supported). MJWarp and MJX-Warp are not differentiable. |
| Small scenes where rough gradients are enough | MJX-JAX |

## Key differences

| | MJX-JAX | MJX-Warp | MJWarp |
|---|---|---|---|
| Package | `mujoco-mjx` | `mujoco-mjx[warp]` | `mujoco-warp` |
| Hardware | All XLA backends | NVIDIA GPUs | NVIDIA GPUs |
| Batching | `jax.vmap` / `jax.pmap` | `jax.vmap` | `nworld` in `make_data` |
| Autodiff | Mostly | No | No |
| Feature coverage | Subset (no flex, limited geoms and sensors) | Nearly all | Nearly all |
| Many contacts / large meshes | Slows down, needs tuning | Scales | Scales |
| Precision | not stated | not stated | float32 (MuJoCo: float64) |
| Batch rendering | not documented | Yes | Yes |

MJWarp scales better than MJX on nearly every workload, especially complex scenes. It does not scale as well as CPU MuJoCo for one large connected kinematic tree. Mechanisms above about 60 DoFs are still being worked on. Scenes with hundreds of DoFs work when [sleeping](../physics-computation/SKILL.md) is enabled and the scene splits into independent islands.

## Reinforcement learning entry points

- JAX environments on MJX: [MuJoCo Playground rss2025](https://github.com/google-deepmind/mujoco_playground/tree/main/rss2025).
- PyTorch on MJWarp: [MuJoCo Playground](https://playground.mujoco.org) with [reaf-sim](https://reaf-sim.readthedocs.io), [mjlab](https://github.com/mujocolab/mjlab), or [Isaac Lab](https://github.com/isaac-sim/IsaacLab) via [Newton](https://github.com/newton-physics/newton).

## Subskills

Read the one that matches your task:

- [mjx](mjx/SKILL.md): MuJoCo XLA (mujoco.mjx): installation, mjx.put_model / put_data, jitted mjx.step, vmap batching, implementations (JAX, Warp), reinforcement learning, feature parity, performance tuning and the sharp bits. Use when writing JAX code that simulates MuJoCo models.
- [mujoco-warp](mujoco-warp/SKILL.md): MuJoCo Warp (mujoco_warp): when to use it, installation, basic usage (put_model, put_data, step), feature parity, performance tuning, batched Model fields, batch rendering, FAQ and differences from MuJoCo. Use when simulating many MuJoCo worlds on NVIDIA GPUs with Warp.
