---
tags: [foundations, awareness, spatially-aware]
---

# What Is Spatially-Aware AI

> **Definition.** A model is *spatially-aware* if it represents or exploits *where* things are in space (2D or 3D), including positions, extents, orientations, and relative placements.

Spatial-awareness is closely related to [[What Is 3D Aware AI|3D-awareness]] but emphasizes *placement* over *geometry*.

## What Information Makes the Model Aware?

- **Positions**: `(x, y, z)` of object centroids.
- **Extents**: bounding boxes, sizes.
- **Orientations**: rotation matrices, quaternions, yaw-pitch-roll.
- **Relative placements**: `above`, `below`, `left-of`, `next-to`, `inside`, `around`.
- **Distances**: between centroids, surfaces, or axes.
- **Spatial indices**: occupancy grids, octrees, BSP trees.

## Where Does It Enter?

- Spatial positional encodings (Fourier features of coordinates).
- Spatial attention (attention biased by 3D distance).
- Spatial losses (e.g. IoU on 3D boxes, distance between centroids).
- Spatial constraints (room must be inside a floor; door must touch exactly two walls).
- Spatial reasoning modules (differentiable geometric solvers).

## Why It Matters for Buildings

A wall has a position. A window has a position *inside the wall*. A door has a position *and an orientation* (which way it swings). A room has a position *and an extent* (which volume it occupies). Without spatial awareness, a model can place a door floating in mid-air, or a room overlapping its neighbour.

See [[Spatial Relations]], [[Adjacency and Containment]], [[Spatial Constraints]].

## Related Concepts

- [[What Is 3D Aware AI]]
- [[What Is Geometry Aware AI]]
- [[What Is Topology Aware AI]]
- [[Spatial Relations]]
- [[Scene Graph Fundamentals]]
