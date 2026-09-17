---
tags: [3d, vision, segmentation]
---

# Semantic Segmentation

> **Definition.** Per-pixel (or per-point, per-voxel) classification: assign a class label to each element.

## Variants by Input

- **2D image**: per-pixel class.
- **Point cloud**: per-point class.
- **Voxel grid**: per-voxel class.
- **Mesh**: per-face class.

## Architectures

- **2D**: U-Net, DeepLab, Mask2Former.
- **Point cloud**: PointNet++, KPConv.
- **Voxel**: 3D U-Net, MinkowskiNet.
- **Mesh**: MeshSegNet.

## Use Cases in Buildings

- Identify walls, floors, ceilings, columns, beams.
- Identify rooms (room segmentation).
- Identify openings (windows, doors).

## Output

- Per-element class label.
- Optionally: confidence per class.

## Connection to BIM

Semantic segmentation is the first step of scan-to-BIM:

1. Segment point cloud into elements.
2. Fit primitives to each segment.
3. Build IFC entities.

See [[Feature Extraction]], [[Instance and Panoptic]].

## Related Concepts

- [[Feature Extraction]]
- [[Instance and Panoptic]]
- [[3D Reconstruction]]
