---
tags: [3d, generation, latent]
---

# Latent 3D Generation

> **Definition.** Compress 3D content into a latent space, then generate in latent space.

## Pipeline

1. Train a 3D auto-encoder (VAE, VQ-VAE) that compresses 3D content (voxels, mesh, SDF) into a latent code.
2. Train a generator (transformer, diffusion) on the latent codes.
3. At inference: sample a latent, decode to 3D.

## Why Latent

- Latent space is compact → faster generation.
- Latent space is continuous → smoother interpolation.
- Latent space can be conditioned → controllable generation.

## Examples

- **IM-Net** latent.
- **VQ-Diffusion on 3D voxels**.
- **Latent NeRF**: GAN over NeRF latents.
- **3DShape2VecSet**: vector-quantized 3D latents for diffusion.

## Limitations

- Latent space loses information (reconstruction error).
- Hard to interpret (what does a latent dimension mean?).
- Hard to constrain (must decode to check).

## Connection to BIM

Latent 3D generation is good for *shape* but not for *structure*. For BIM, prefer tree-structured generation that emits explicit elements.

See [[3D Generative Models]], [[Autoregressive 3D]], [[Diffusion 3D]].

## Related Concepts

- [[3D Generative Models]]
- [[Diffusion 3D]]
- [[Autoregressive 3D]]
