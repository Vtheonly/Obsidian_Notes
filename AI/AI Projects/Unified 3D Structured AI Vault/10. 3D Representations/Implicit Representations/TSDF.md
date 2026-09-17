---
tags: [3d, representations, tsdf]
---

# TSDF (Truncated Signed Distance Function)

> A *TSDF* is a voxel grid where each voxel stores the signed distance to the nearest surface, truncated at some maximum distance.

## Definition

For a point $p$ and a surface $S$:

$$\text{SDF}(p) = \begin{cases} +d(p, S) & p \text{ outside} \\ -d(p, S) & p \text{ inside} \end{cases}$$

Truncated:

$$\text{TSDF}(p) = \max(-\delta, \min(+\delta, \text{SDF}(p)))$$

where $\delta$ is the truncation distance.

## Why Truncate

- Far from the surface, the exact distance doesn't matter (it's "definitely outside").
- Truncation saves memory and focuses computation near the surface.

## Use Cases

- **RGB-D integration**: fuse multiple depth maps into a TSDF volume (KinectFusion).
- **SLAM**: build a TSDF map of the environment.
- **Surface reconstruction**: Marching Cubes on the TSDF gives a mesh.

## In AI

- Neural TSDF: a neural network predicts the TSDF.
- Voxel hashing: sparse TSDF for large scenes.

See [[SDF]], [[Voxels]], [[3D Reconstruction]], [[TSDF Fusion]].

## Related Concepts

- [[SDF]]
- [[Voxels]]
- [[TSDF Fusion]]
- [[3D Reconstruction]]
