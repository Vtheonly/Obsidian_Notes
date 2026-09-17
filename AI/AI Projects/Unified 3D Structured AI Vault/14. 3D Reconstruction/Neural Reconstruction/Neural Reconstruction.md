---
tags: [3d, reconstruction, neural]
---

# Neural Reconstruction

> **Definition.** Use neural networks to reconstruct 3D from images, depth, or point clouds.

## Variants

- **NeRF**: reconstruct a radiance field from posed images.
- **Neural surface reconstruction**: reconstruct a mesh via an SDF or occupancy network.
- **Neural SLAM**: reconstruct while tracking (NeuralRecon, NICE-SLAM).
- **Generative reconstruction**: combine reconstruction with a learned shape prior.

## Pipeline (NeRF)

1. Input: posed RGB images.
2. Optimize a network $f_\theta(p, \vec d) \to (c, \sigma)$.
3. Render novel views by volumetric rendering.
4. Loss: photometric error between rendered and real images.

## Pipeline (NeuralRecon)

1. Input: posed RGB-D frames.
2. Per-frame: predict a fragment (TSDF volume).
3. Fuse fragments into a global TSDF via differentiable fusion.
4. Extract mesh.

## Why Neural

- Learned priors help with sparse / noisy data.
- Differentiable: end-to-end training.
- Compact: neural fields instead of large voxel grids.

## Limitations

- Training is slow.
- Generalization to new scenes is hard.
- Recovering exact topology (watertight mesh) is non-trivial.

See [[3D Reconstruction]], [[Neural Fields]], [[Neural Representation Learning]].

## Related Concepts

- [[3D Reconstruction]]
- [[Neural Fields]]
- [[Neural Representation Learning]]
