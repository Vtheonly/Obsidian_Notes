---
tags: [3d, representations, point-cloud]
---

# Point Clouds

> A *point cloud* is a set of 3D points $\{p_i \in \mathbb{R}^3\}_{i=1}^N$, possibly with attributes (color, normal, intensity).

## What It Preserves

- Sampled geometry (positions).
- Per-point attributes (color, normal, intensity, class label).

## What It Loses

- Topology (no edges, no faces).
- Connectivity (which points are neighbors).
- Semantics (unless labels are added).
- Hierarchy (no containment).

## Operations

- **Downsampling**: voxel grid, random, FPS (farthest point sampling).
- **Normals estimation**: PCA on local neighborhood.
- **Segmentation**: per-point classification.
- **Registration**: align two point clouds (ICP).
- **Surface reconstruction**: Poisson, ball-pivoting, Delaunay.

## Sources

- LiDAR scanners.
- RGB-D cameras (depth → back-project).
- Multi-view stereo.
- Synthetic generators.

## In AI

- **PointNet**, **PointNet++**: process point clouds directly.
- **Set-based generation**: DeepSets, PointGrow.
- **Diffusion on point clouds**.

## Can It Be Converted to BIM?

Only indirectly:

1. Segment the cloud into objects.
2. Fit primitives (planes, cylinders) to each segment.
3. Build a scene graph from primitives.
4. Convert scene graph to IFC.

See [[3D Reconstruction]], [[Point Cloud to Mesh]].

## Related Concepts

- [[Voxels]]
- [[Meshes]]
- [[3D Representations]]
- [[Representation Comparison]]
- [[Point Cloud to Mesh]]
