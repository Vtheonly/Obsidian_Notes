---
tags: [3d, representations, neural-fields]
---

# Neural Fields

> A *neural field* is a neural network that represents a continuous field over 3D space: $f_\theta: \mathbb{R}^3 \to \mathbb{R}^k$.

## Variants

- **Occupancy network**: $f_\theta(p) \to [0, 1]$ (probability of inside).
- **DeepSDF**: $f_\theta(p) \to \mathbb{R}$ (signed distance).
- **NeRF** (Neural Radiance Field): $f_\theta(p, \vec d) \to (c, \sigma)$ (color and density).
- **Instant-NGP**: hash-grid accelerated NeRF.

## Why Neural Fields

- **Continuous**: arbitrary resolution at query time.
- **Compact**: a few MB of weights instead of GB of voxels.
- **Differentiable**: end-to-end training from images.
- **Composable**: latent codes can be combined.

## What They Preserve / Lose

| Property        | Preserved?                              |
| --------------- | --------------------------------------- |
| Geometry        | Yes (continuous).                       |
| Topology        | Implicit (must be extracted).           |
| Semantics       | No (unless conditioned on labels).      |
| Hierarchy       | No (single field).                      |
| Editability     | Hard (editing requires retraining).     |

## In AI

- **NeRF** for novel-view synthesis.
- **Neural shape priors** for shape completion.
- **Generative neural fields** for shape generation.
- **Neural scene graphs**: combine NeRFs with scene graph structure.

## Can They Be Converted to BIM?

Very hard:

1. Render the field to a mesh (Marching Cubes on the density field).
2. Segment the mesh.
3. Fit primitives.
4. Build IFC.

Research direction: neural fields that *directly* produce structured BIM. See [[Neural Representation Learning]], [[Verifiable Generation]].

## Related Concepts

- [[SDF]]
- [[Implicit Representations]]
- [[3D Representations]]
- [[Neural Representation Learning]]
