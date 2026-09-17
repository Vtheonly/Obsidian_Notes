---
tags: [3d, surfaces, solids]
---

# Surfaces and Solids

> Two ways to represent 3D shapes: as **surfaces** (2D manifolds in 3D) or as **solids** (3D volumes with interiors).

## Boundary Representations (B-rep)

A solid is represented by its boundary: a closed surface (or set of surfaces) that separates inside from outside.

- **Polygon mesh**: triangles or quads. See [[Meshes]].
- **Parametric surface**: e.g. NURBS, B-splines.
- **Subdivision surface**: smooth limit of recursive refinement.

## Constructive Solid Geometry (CSG)

A solid is built by combining primitives (sphere, box, cylinder, cone) using boolean operations (union, intersection, difference):

```
S = (Box - Cylinder) ∪ Sphere
```

CSG is naturally represented as a tree — see [[Constructive Solid Geometry]].

## Implicit Representations

A solid is the set $\{p : f(p) \leq 0\}$ for some implicit function $f$:

- **Signed distance function (SDF)**: $f(p)$ = signed distance to the surface.
- **Occupancy field**: $f(p) \in [0, 1]$ = probability the point is inside.
- **Neural field**: $f$ is a neural network.

See [[SDF]], [[Implicit Representations]], [[Neural Fields]].

## Volumetric Representations

A solid is discretized into voxels (3D pixels):

- **Occupancy grid**: each voxel is inside or outside.
- **TSDF**: truncated signed distance per voxel.
- **Voxel grid**: density or feature per voxel.

See [[Voxels]], [[Occupancy Grids]], [[TSDF]].

## Comparison

| Representation   | Geometry | Topology | Editable | Generatable | BIM convertible |
| ---------------- | -------- | -------- | -------- | ----------- | --------------- |
| Mesh (B-rep)     | Explicit | Implicit | Hard     | Yes (diffusion) | Hard            |
| Parametric / NURBS | Explicit | Explicit | Easy     | Hard        | Medium          |
| CSG tree         | Implicit | Explicit | Easy     | Yes (program synthesis) | Medium   |
| SDF / Occupancy  | Implicit | Implicit | Medium   | Yes (neural) | Hard            |
| Voxel grid       | Discrete | Discrete | Medium   | Yes (3D conv) | Medium          |
| Point cloud      | Sampled  | None     | Hard     | Yes (set gen) | Hard            |

See [[3D Representations]], [[Representation Comparison]].

## Related Concepts

- [[Meshes]]
- [[Constructive Solid Geometry]]
- [[SDF]]
- [[Voxels]]
- [[Point Clouds]]
- [[Neural Fields]]
