---
tags: [image-depth, structured]
---

# Structured Lift

> **Definition.** Lift a 2D image + depth into a *structured* 3D representation (not just a point cloud).

## Pipeline

```
Image + Depth
  ↓
2D detection + segmentation
  ↓
Per-object 2D mask + depth
  ↓
Per-object 3D bounding box (back-project)
  ↓
Per-object 3D mesh / primitive
  ↓
Pairwise relations (predicted)
  ↓
Scene graph with 3D geometry
  ↓
Hierarchy (cluster objects into groups, rooms)
  ↓
Structured 3D scene (BIM-like)
```

## Why It's Better Than Naive Back-Projection

Naive back-projection gives a point cloud. Structured lift gives:

- segmented objects,
- per-object geometry,
- relations between objects,
- hierarchy.

This is directly useful for BIM generation.

## In Buildings

Structured lift from indoor RGB-D scans:

1. Detect walls, floors, ceilings (planar primitives).
2. Detect doors, windows (openings).
3. Detect furniture.
4. Estimate room boundaries.
5. Build a building scene graph.
6. Convert to IFC.

See [[Image to Scene]], [[Scene Graph Generation]], [[BIM Generation]].

## Related Concepts

- [[Image to Scene]]
- [[Scene Graph Generation]]
- [[BIM Generation]]
