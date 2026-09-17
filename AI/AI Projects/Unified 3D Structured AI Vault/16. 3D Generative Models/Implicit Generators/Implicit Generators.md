---
tags: [3d, generation, implicit]
---

# Implicit Generators

> **Definition.** Generators that produce implicit 3D representations (SDF, occupancy, neural fields).

## Variants

- **DeepSDF** (auto-decoder): each shape has a latent code; the network decodes a signed distance field.
- **OccNet**: occupancy network.
- **IM-Net**: implicit field decoder.
- **NeRF generators**: GAN or diffusion over NeRF latents.

## Strengths

- Continuous (arbitrary resolution at query time).
- Compact (network weights + latent).
- Differentiable (end-to-end training).

## Limitations

- Hard to edit (editing requires retraining).
- Hard to validate (must extract mesh first).
- Hard to convert to BIM (must segment + fit primitives).

## Connection to BIM

Implicit generators are good for *appearance* (rendering) but not for *structure*. BIM requires explicit elements.

See [[Neural Fields]], [[3D Generative Models]], [[Diffusion 3D]].

## Related Concepts

- [[Neural Fields]]
- [[3D Generative Models]]
- [[Diffusion 3D]]
