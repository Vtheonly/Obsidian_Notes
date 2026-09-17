---
tags: [3d, representations, sdf]
---

# SDF (Signed Distance Function)

> An *SDF* maps each point $p$ to the signed distance to the nearest surface: positive outside, negative inside, zero on the surface.

## Mathematical Form

$$f: \mathbb{R}^3 \to \mathbb{R}, \quad f(p) = \text{signed distance to surface}$$

Properties:

- $|\nabla f| = 1$ almost everywhere.
- $\nabla f(p)$ points outward from the surface.

## Advantages

- Smooth, continuous representation.
- Cheap to query at any point.
- Differentiable (good for optimization).
- Easy to combine shapes: $\min(f_1, f_2)$ for union, $\max$ for intersection.

## Disadvantages

- Memory-heavy if discretized as a voxel grid.
- Hard to edit individual parts.
- Doesn't naturally encode semantics or hierarchy.

## Neural SDFs

A neural network $f_\theta(p)$ learns the SDF:

- **DeepSDF**: a single network for a class of shapes; latent code per shape.
- **OccNet**: predicts occupancy (binary version of SDF).

## Rendering

SDFs can be rendered by **ray marching**: step along a ray, evaluate $f$ at each step, stop when $|f|$ is small.

## Can It Be Converted to BIM?

Hard. SDFs are implicit; BIM is explicit. Conversion requires:

1. Marching Cubes to get a mesh.
2. Segment and fit primitives.
3. Build IFC.

See [[Surfaces and Solids]], [[Meshes]], [[Neural Fields]].

## Related Concepts

- [[TSDF]]
- [[Voxels]]
- [[Implicit Representations]]
- [[Neural Fields]]
