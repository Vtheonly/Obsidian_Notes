---
tags: [foundations, awareness, geometry-aware]
---

# What Is Geometry-Aware AI

> **Definition.** A model is *geometry-aware* if it explicitly represents and reasons about geometric quantities: lengths, areas, volumes, angles, curvatures, normals, and the relationships between them (parallelism, orthogonality, tangency, symmetry).

## What Information Makes the Model Aware?

- **Shape descriptors**: mesh, SDF, occupancy, parametric surface.
- **Geometric primitives**: planes, cylinders, cones, spheres, tori.
- **Geometric relations**: parallel, perpendicular, tangent, coaxial, coplanar.
- **Geometric invariants**: distances, angles under rigid transforms.
- **Normals and tangents**: surface orientation.

## Where Does It Enter?

- Geometric losses (Chamfer distance, normal consistency, Hausdorff).
- Geometric constraints (walls must be vertical, floors must be horizontal).
- Primitive fitting (RANSAC, deep primitive fitting).
- Differentiable rendering (the geometry affects the rendered image).
- Manifold constraints (meshes must be closed, watertight).

## Why It Matters for BIM

A BIM wall is not just a box. It has:

- a base curve (often a line segment),
- a height,
- a thickness,
- a material layer set,
- openings (doors, windows),
- connections to other walls.

Geometry-awareness lets a generator produce walls that are actually plumb, level, and square — not just visually plausible boxes.

See [[3D Geometry]], [[Surfaces and Solids]], [[Geometric Constraints]].

## Related Concepts

- [[What Is 3D Aware AI]]
- [[What Is Spatially Aware AI]]
- [[What Is Topology Aware AI]]
- [[3D Geometry]]
- [[Geometric Constraints]]
- [[Surfaces and Solids]]
