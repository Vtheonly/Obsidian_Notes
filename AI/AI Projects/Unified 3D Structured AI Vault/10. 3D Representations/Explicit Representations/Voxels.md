---
tags: [3d, representations, voxels]
---

# Voxels

> A *voxel grid* is a 3D array where each cell (voxel) holds a value (occupancy, density, feature vector).

## What It Preserves

- Volumetric occupancy.
- Dense spatial structure (regular grid).

## What It Loses

- Sharp surfaces (limited by grid resolution).
- Fine details (memory blows up as $O(n^3)$).

## Variants

- **Occupancy grid**: 0/1 per voxel.
- **Density grid**: continuous value.
- **TSDF**: truncated signed distance per voxel.
- **Feature grid**: per-voxel feature vector (used in neural radiance fields and Voxel NeRF).

## In AI

- **3D CNNs**: process voxel grids with 3D convolutions.
- **Voxel GANs**: 3D-GAN, etc.
- **Voxel diffusion**: generate voxels, then mesh.
- **Sparse voxels**: only store occupied voxels; efficient for large scenes.

## Resolution vs Memory

A $256^3$ voxel grid at 4 bytes per voxel = 64 MB. A $1024^3$ grid = 4 GB. Sparse representations (octrees, hash grids) are needed for high resolution.

## Can It Be Converted to BIM?

Indirectly:

1. Run Marching Cubes to extract a mesh.
2. Segment the mesh.
3. Fit primitives.
4. Build IFC.

See [[Meshes]], [[TSDF]], [[3D Representations]].

## Related Concepts

- [[Occupancy Grids]]
- [[TSDF]]
- [[SDF]]
- [[Meshes]]
- [[Point Clouds]]
