---
tags: [3d, generation, awareness]
---

# 3D-Aware Generation

> **Definition.** Generation that produces 3D-consistent outputs (meshes, voxels, point clouds, neural fields, BIM) rather than 2D images.

## Why It Matters

A 2D image generator can produce a beautiful building image with:

- floating windows,
- inconsistent geometry across views,
- depth that doesn't make sense.

A 3D-aware generator produces a real 3D structure that:

- can be rendered from any viewpoint,
- can be edited,
- can be validated,
- can be converted to BIM.

## Approaches

- **Voxel generation**: 3D-GAN, voxel diffusion.
- **Point cloud generation**: PointGrow, SetVAE.
- **Mesh generation**: MeshDiffusion, Mesh R-CNN.
- **Implicit generation**: DeepSDF, NeRF diffusion.
- **Latent 3D**: VQ-VAE on 3D, then transformer / diffusion in latent space.
- **Tree-structured generation**: scene graph → 3D.

See [[3D Generative Models]], [[Diffusion 3D]], [[Autoregressive 3D]].

## Trade-offs

| Approach             | Resolution | Memory        | Editable | BIM-ready |
| -------------------- | ---------- | ------------- | -------- | --------- |
| Voxel                | Low        | High          | Medium   | No        |
| Point cloud          | Medium     | Low           | Hard     | No        |
| Mesh                 | High       | Medium        | Hard     | Maybe     |
| Implicit / Neural    | High       | Low           | Hard     | No        |
| Tree + geometry      | Variable   | Low           | Easy     | Yes       |

Tree-structured generation (e.g. predict building hierarchy, then geometry per element) is the most BIM-ready approach. See [[Tree Based BIM]], [[BIM Generation]].

## Related Concepts

- [[3D Generative Models]]
- [[BIM Generation]]
- [[3D Consistency]]
