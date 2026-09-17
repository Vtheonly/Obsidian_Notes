---
tags: [image-to-3d, scene]
---

# Image to Scene

> **Definition.** Generate a full structured scene (objects + relations + geometry) from images.

## Pipeline

```
RGB image(s)
  ↓
Object detection + segmentation
  ↓
Per-object features
  ↓
Relation prediction
  ↓
Scene graph
  ↓
Geometry estimation (per object)
  ↓
Scene layout
  ↓
3D scene
```

## Components

- **Object detection**: 2D boxes / masks.
- **Depth estimation**: per-pixel depth.
- **3D bounding boxes**: per-object 3D pose + size.
- **Relation prediction**: object pairs → relations.
- **Layout optimization**: arrange objects in 3D consistent with relations.

## Output

A structured scene: scene graph + per-object 3D geometry. Can be:

- rendered from novel views,
- edited,
- converted to BIM (if it's a building scene).

## In Buildings

Image to building scene:

1. Detect walls, doors, windows, slabs, columns from images.
2. Predict relations (adjacency, connectivity).
3. Estimate per-element 3D geometry.
4. Assemble into a building scene graph.
5. (Optional) convert to IFC.

See [[Scene Graph Generation]], [[Multi-View to 3D]].

## Related Concepts

- [[Scene Graph Generation]]
- [[Multi-View to 3D]]
- [[Single Image to 3D]]
