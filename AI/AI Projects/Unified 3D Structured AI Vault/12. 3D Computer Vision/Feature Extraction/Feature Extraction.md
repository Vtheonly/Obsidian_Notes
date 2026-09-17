---
tags: [3d, vision, features]
---

# Feature Extraction (3D Vision)

> **Definition.** Extracting informative features from 3D data: points, voxels, meshes, images.

## From Images

- **CNN features**: ResNet, ViT.
- **Dense features**: feature pyramid, FPN.
- **Edge / corner features**: Canny, Harris, SIFT, SURF, ORB.

## From Point Clouds

- **PointNet / PointNet++**: per-point features.
- **FPFH**: fast point feature histograms.
- **SHOT**: signature of histograms of orientations.

## From Meshes

- **MeshCNN**: convolution on mesh edges.
- **Geometric features**: curvature, normal, dihedral angles.

## From Voxel Grids

- **3D CNNs**: 3D convolutions.
- **Sparse 3D CNNs**: only on occupied voxels (MinkowskiNet).

## What Features Capture

- Local appearance (texture, color).
- Local geometry (curvature, normals).
- Contextual information (with receptive field).
- Semantic content (with supervised training).

## In This Vault

Features feed into:

- Depth estimation (image features → depth).
- Reconstruction (features → 3D).
- Scene graph generation (features → objects → relations).
- BIM generation (features → element types → relations).

See [[3D Computer Vision]], [[Semantic Segmentation]], [[Scene Graph Fundamentals]].

## Related Concepts

- [[Semantic Segmentation]]
- [[Scene Graph Fundamentals]]
- [[3D Reconstruction]]
