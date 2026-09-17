---
tags: [3d, generation, diffusion]
---

# Diffusion 3D

> **Definition.** 3D shape generation via diffusion models.

## How Diffusion Works

Forward process: gradually add noise to data:

$$q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\alpha_t} x_0, (1 - \alpha_t) I)$$

Reverse process: a network $\epsilon_\theta$ learns to denoise:

$$p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$

## 3D Variants

| Variant                | What it diffuses                |
| ---------------------- | ------------------------------- |
| Voxel diffusion        | 3D voxel grid.                  |
| Point cloud diffusion  | Set of 3D points.               |
| Mesh diffusion         | Mesh vertices (fixed topology). |
| Latent 3D diffusion    | Latent code of a 3D VAE.        |
| SDF diffusion          | Neural SDF latent.              |
| Multi-view diffusion   | Multiple views, then reconstruct. |

## Strengths

- High-quality samples.
- Diversity (mode coverage).
- Conditional generation (text, image, partial shape).

## Limitations

- Slow (many denoising steps).
- Topology is not guaranteed (can produce non-watertight meshes).
- Hard to control structure (e.g. "exactly 4 windows on this wall").

## Connection to BIM

Diffusion is good for *geometry* but not for *structure*. To get BIM, combine:

1. Diffusion for raw 3D shape.
2. Segment + fit primitives.
3. Build scene graph.
4. Convert to IFC.

Or use a **structured diffusion** that directly generates scene graphs / hierarchies.

See [[3D Generative Models]], [[Autoregressive 3D]], [[Implicit Generators]].

## Related Concepts

- [[3D Generative Models]]
- [[Autoregressive 3D]]
- [[Implicit Generators]]
- [[Latent 3D]]
