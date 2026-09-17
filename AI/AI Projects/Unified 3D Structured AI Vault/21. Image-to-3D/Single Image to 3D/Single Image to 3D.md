---
tags: [image-to-3d, generation]
---

# Single Image to 3D

> **Definition.** Reconstruct or generate a 3D model from a single RGB image.

## Why It's Hard

A single image is a 2D projection of a 3D scene. The 3D structure is **ambiguous** — many 3D scenes project to the same 2D image. The model must use learned priors.

## Approaches

- **Monocular depth + back-projection**: predict depth, then back-project to a point cloud.
- **3D reconstruction networks**: directly predict a mesh / voxel / SDF.
- **Generative models**: diffusion or autoregressive over 3D latents.
- **NeRF from one image**: needs strong priors; works for seen categories.

## Pipeline (Depth-Based)

```
RGB image
  ↓
Monocular depth network
  ↓
Depth map
  +
Camera intrinsics (estimated or known)
  ↓
Back-projection
  ↓
Point cloud
  ↓
Surface reconstruction (Poisson, etc.)
  ↓
Mesh
```

## Pipeline (Generative)

```
RGB image
  ↓
Encoder
  ↓
Latent code
  ↓
3D generator (diffusion, autoregressive)
  ↓
3D shape (mesh / SDF / voxels)
```

## In Buildings

Single image to BIM is very hard:

1. Most of the building is not visible from one image.
2. The 3D structure must be inferred from priors.
3. BIM requires semantics (element types), which are not directly visible.

Practical systems use multiple images (multi-view) and/or depth sensors.

See [[Multi-View to 3D]], [[Image + Depth-to-3D]], [[Image to Scene]].

## Related Concepts

- [[Multi-View to 3D]]
- [[Image + Depth-to-3D]]
- [[Image to Scene]]
- [[Monocular Depth]]
