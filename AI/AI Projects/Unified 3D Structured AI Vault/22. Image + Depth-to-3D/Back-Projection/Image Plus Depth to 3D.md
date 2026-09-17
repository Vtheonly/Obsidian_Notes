---
tags: [image-depth, generation]
---

# Image + Depth to 3D

> **Definition.** Generate 3D content from RGB images + depth maps (RGB-D).

See [[Back Projection]] for the basic operation.

## Pipeline

```
RGB image(s)
  +
Depth map(s)
  +
Camera intrinsics K
  +
Camera extrinsics [R | t]
        ↓
Back-projection (per pixel)
        ↓
3D point cloud
        ↓
Surface reconstruction
        ↓
Mesh / scene
```

## Extended Pipeline (Structured)

```
Image
  ↓
Visual understanding (detection, segmentation)
  +
Depth
  ↓
Geometry (per-pixel 3D)
  ↓
Objects (per-instance 3D)
  ↓
Relationships (adjacency, connectivity)
  ↓
Hierarchy (containment tree)
  ↓
BIM / structured representation
  ↓
Validation
```

## Why It's Stronger Than Image-Only

- Depth removes the 2D-to-3D ambiguity.
- Multi-view consistency is easier to enforce.
- Geometry can be directly measured, not inferred.

## Why It's Still Hard

- Depth sensors have limited range and accuracy.
- Depth may be missing (transparent surfaces, mirrors).
- Multi-view registration is still needed.
- Structured output (BIM) requires additional inference (semantics, hierarchy).

See [[Back Projection]], [[Depth Consistency]], [[Image to Scene]].

## Related Concepts

- [[Back Projection]]
- [[Depth Consistency]]
- [[Image to Scene]]
- [[3D Reconstruction]]
