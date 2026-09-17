---
tags: [foundations, awareness, 3d-aware]
---

# What Is 3D-Aware AI

> **Definition.** A model is *3D-aware* if it explicitly uses 3D geometric, spatial, or volumetric information, rather than treating the world as a flat 2D image or a sequence of tokens.

## What Information Makes the Model Aware?

3D-awareness can mean any of:

- **Geometric awareness**: knowing distances, angles, areas, volumes.
- **Spatial awareness**: knowing where things are relative to each other in 3D.
- **Volumetric awareness**: knowing that a wall has thickness, a room has interior, a building contains space.
- **Depth awareness**: knowing that objects farther from the camera appear smaller.
- **Multi-view consistency awareness**: knowing that two images of the same scene must agree on a shared 3D structure.
- **Topological awareness**: knowing adjacency, containment, connectivity in 3D.
- **Pose awareness**: knowing camera extrinsics, object poses, world frames.

See also [[What Is Spatially Aware AI]], [[What Is Geometry Aware AI]], [[What Is Topology Aware AI]].

## Where Does the Information Come From?

- **Cameras**: intrinsics, extrinsics, depth sensors.
- **Point clouds**: LiDAR, structured-light scans.
- **Meshes**: 3D models.
- **Volumetric grids**: occupancy, TSDF, SDF.
- **Implicit fields**: neural radiance fields, occupancy networks.
- **Multi-view observations**: posed RGB images.
- **BIM / CAD**: explicit 3D parametric or relational models.

## Where Does It Enter the Architecture?

- **3D features**: voxelized features, point features, neural fields.
- **3D attention**: attention weighted by 3D distance or ray direction.
- **3D constraints**: hard geometric constraints (parallelism, orthogonality, support).
- **3D losses**: Chamfer distance, IoU on voxels, EMD on points.
- **3D decoders**: explicit mesh decoders, voxel decoders, implicit field decoders.
- **Camera conditioning**: NeRF-style ray encoding, epipolar attention.

## Hard vs Soft

- **Soft**: a 2D diffusion model that *prefers* depth-consistent outputs.
- **Hard**: a 3D-aware decoder that emits a TSDF volume — geometry is *guaranteed* to be a real volume.
- **Verified**: a multi-view consistency check that rejects inconsistent candidates.

## Why It Matters

A 2D image generator can produce a beautiful picture of a building whose windows float in mid-air when back-projected into 3D. A 3D-aware generator cannot — at least not without failing its own consistency objective.

See [[3D Consistency]], [[What Is 3D Aware]], and [[3D-Aware AI]].

## Related Concepts

- [[What Is Spatially Aware AI]]
- [[What Is Geometry Aware AI]]
- [[What Is Topology Aware AI]]
- [[3D Consistency]]
- [[3D Representations]]
- [[Depth and Multi-View Geometry]]
- [[3D Reconstruction]]
