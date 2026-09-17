---
tags: [bim-generation, diffusion]
---

# Diffusion-Based BIM Generation

> **Definition.** Generate BIM content via diffusion models.

## What to Diffuse

- **Voxels**: diffuse a voxel grid of the building.
- **Latent 3D**: diffuse a 3D latent code, then decode.
- **Scene graph latents**: diffuse a latent representation of the scene graph.
- **Building latents**: a learned VAE compresses BIM models into latents.

## Strengths

- High-quality samples.
- Diversity.
- Conditional generation (text, partial building, sketch).

## Limitations

- Diffusion produces unstructured output; need to post-process to get a valid BIM.
- Hard to enforce constraints during diffusion.
- Slow (many denoising steps).

## Hybrid

Combine diffusion with structured generation:

1. Diffuse a coarse 3D shape.
2. Segment + fit primitives.
3. Build scene graph.
4. Convert to IFC.

Or: use diffusion to generate the **latent code** of a structured generator.

See [[BIM Generation]], [[Diffusion 3D]], [[Autoregressive BIM]].

## Related Concepts

- [[BIM Generation]]
- [[Diffusion 3D]]
- [[Autoregressive BIM]]
