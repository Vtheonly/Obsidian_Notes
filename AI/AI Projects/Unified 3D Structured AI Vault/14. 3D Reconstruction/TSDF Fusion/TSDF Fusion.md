---
tags: [3d, reconstruction, tsdf]
---

# TSDF Fusion

> **Definition.** Fuse multiple depth maps into a single TSDF volume, then extract a mesh.

## Algorithm (KinectFusion)

1. Initialize a TSDF volume (all zeros).
2. For each new depth map:
   - Back-project to 3D points.
   - For each voxel in the volume, compute the signed distance to the nearest point.
   - Truncate and integrate into the existing TSDF (running average).
3. Extract a mesh with Marching Cubes.

## Why TSDF Fusion

- **Denoising**: averaging across many views reduces sensor noise.
- **Completion**: areas seen in some views fill in gaps from other views.
- **Compact**: a single volume replaces many depth maps.

## Extensions

- **Voxel hashing**: sparse TSDF for large scenes (Kintinuous, InfiniTAM).
- **Color TSDF**: also fuse color into the volume.
- **Neural TSDF**: a network predicts the TSDF.

See [[TSDF]], [[3D Reconstruction]], [[Point Cloud to Mesh]].

## Related Concepts

- [[TSDF]]
- [[3D Reconstruction]]
- [[Point Cloud to Mesh]]
