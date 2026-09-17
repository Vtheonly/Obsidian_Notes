---
tags: [3d, representations, meshes]
---

# Meshes

> A *mesh* is a collection of vertices, edges, and faces (typically triangles or quads) that approximates a surface.

## Structure

- Vertices: $V = \{v_i \in \mathbb{R}^3\}$.
- Edges: $E \subseteq V \times V$.
- Faces: $F \subseteq V \times V \times V$ (triangles).

## What It Preserves

- Surface geometry (explicit).
- Topology of the surface (edges, faces).

## What It Loses

- Semantics (unless segments are labeled).
- Hierarchy.
- Volume / interior (it is a surface, not a solid).

## Properties

- **Watertight**: closed surface (every edge has exactly 2 faces).
- **Manifold**: locally homeomorphic to a disk.
- **Consistent orientation**: all face normals point outward.
- **Non-self-intersecting**: no two faces intersect.

## Operations

- Subdivision (Loop, Catmull-Clark).
- Simplification (quadric error metrics).
- Parametrization (for texturing).
- Deformation (as-rigid-as-possible).

## In AI

- **Mesh R-CNN**: detect and reconstruct meshes.
- **Pixel2Mesh**: iterative mesh deformation.
- **Mesh diffusion**: generate meshes by diffusion.
- **AtlasNet**: learn atlas of charts.

## Can It Be Converted to BIM?

Hard:

1. Segment mesh into objects.
2. Fit primitives or parametric surfaces.
3. Build scene graph.
4. Convert to IFC.

Mesh → BIM is the goal of **scan-to-BIM** systems. See [[3D Reconstruction]], [[BuildingBIM from Point Clouds]] (placeholder).

## Related Concepts

- [[Point Clouds]]
- [[Voxels]]
- [[Surfaces and Solids]]
- [[3D Representations]]
