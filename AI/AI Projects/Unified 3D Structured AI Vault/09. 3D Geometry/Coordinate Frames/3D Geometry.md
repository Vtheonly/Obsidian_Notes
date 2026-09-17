---
tags: [3d, geometry, coordinates]
---

# 3D Geometry

> **Definition.** *3D geometry* studies shapes, positions, distances, angles, and transformations in three-dimensional Euclidean space $\mathbb{R}^3$.

## Coordinate Frames

A coordinate frame is defined by:

- an origin $O$,
- three orthogonal axes $\hat x, \hat y, \hat z$ (usually right-handed).

A point $p$ has coordinates $(x, y, z)$ such that $p = O + x \hat x + y \hat y + z \hat z$.

## Common Frames

| Frame                  | Use                                          |
| ---------------------- | -------------------------------------------- |
| World frame            | Global coordinates of the scene.             |
| Camera frame           | Camera at origin, looking along $+z$ or $-z$.|
| Object frame           | Local to each object (e.g. centroid at origin). |
| Body frame             | For articulated objects (each link).         |
| Building frame         | Aligned with building axes (X = east, Y = north, Z = up). |

See [[Coordinate Frames]], [[Transformations]].

## Vectors and Points

- A **point** is a location.
- A **vector** is a displacement.
- Points and vectors can be added/subtracted: $\vec{AB} = B - A$.

## Lines, Planes, Volumes

- **Line**: $p(t) = p_0 + t \vec d$ for $t \in \mathbb{R}$.
- **Plane**: $\vec n \cdot (p - p_0) = 0$.
- **Half-space**: $\vec n \cdot (p - p_0) \geq 0$.
- **Convex polytope**: intersection of half-spaces.

## Transformations

See [[Transformations]] for rotation, translation, scaling, and their composition as $4 \times 4$ homogeneous matrices.

## Surfaces and Solids

See [[Surfaces and Solids]] for boundary representations (B-rep), constructive solid geometry (CSG), and parametric surfaces.

## Related Concepts

- [[Coordinate Frames]]
- [[Transformations]]
- [[Surfaces and Solids]]
- [[What Is Geometry Aware AI]]
