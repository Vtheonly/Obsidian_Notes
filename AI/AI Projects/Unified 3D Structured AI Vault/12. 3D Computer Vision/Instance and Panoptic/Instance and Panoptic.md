---
tags: [3d, vision, instance, panoptic]
---

# Instance and Panoptic Segmentation

> Two refinements of semantic segmentation that distinguish *instances* of the same class.

## Semantic vs Instance vs Panoptic

| Task                | Output per pixel                     |
| ------------------- | ------------------------------------ |
| Semantic            | Class label only.                    |
| Instance            | Object instance (within "thing" classes). |
| Panoptic            | Class label + instance ID for everything. |

## Architectures

- **Instance**: Mask R-CNN, YOLOv8-seg.
- **Panoptic**: Panoptic FPN, Mask2Former.

## In Buildings

- Identify each individual window (instance), not just "window" pixels.
- Identify each individual door.
- Identify each individual piece of furniture.

## Connection to Scene Graphs

Instance segmentation produces object instances, which become nodes in a scene graph. Relation prediction then produces edges.

See [[Semantic Segmentation]], [[Scene Graph Fundamentals]].

## Related Concepts

- [[Semantic Segmentation]]
- [[Feature Extraction]]
- [[Scene Graph Fundamentals]]
