---
tags: [validation, geometric]
---

# Geometric Validation

> **Definition.** *Geometric validation* checks that the geometry of a generated or reconstructed structure satisfies geometric constraints: distances, angles, areas, volumes, containment, manifoldness, etc.

## Checks

| Check                   | Description                                                            |
| ----------------------- | --------------------------------------------------------------------- |
| Self-intersection       | No two surfaces of the same object intersect.                         |
| Manifoldness            | Mesh is watertight (closed); every edge has exactly two faces.        |
| Orientation             | Normals are consistent (no flipped faces).                            |
| Distance bounds         | Wall thickness within `[min, max]`; room dimensions within bounds.    |
| Angle bounds            | Walls are vertical; floors are horizontal; corners are right angles.  |
| Containment             | Each object's geometry lies inside its parent's geometry.             |
| Non-overlap             | Sibling objects do not overlap.                                       |
| Alignment               | Adjacent walls are aligned; columns sit on beams; etc.                |

## Algorithms

- **Mesh manifoldness**: count edge-face incidences; check each edge has exactly 2.
- **Self-intersection**: BVH-accelerated triangle-triangle intersection test.
- **Containment**: point-in-mesh test for object centroids; ray casting for surfaces.
- **Alignment**: dot product of normals with expected axes (e.g. `< 1e-3` from `(0,0,1)` for floors).

## When It Catches Errors

Geometric validation catches:

- Walls not vertical.
- Doors floating in mid-air.
- Rooms overlapping.
- Meshes that are not watertight.
- Surfaces with wrong orientation.

## When It Misses

Geometric validation does **not** catch:

- Topological errors (bedroom only reachable through bathroom).
- Semantic errors (a "door" that is actually a wall).
- Structural errors (a load-bearing wall that cannot bear load).

See [[Topological Validation]], [[Semantic Validation]], [[Structural Validation]].

## Related Concepts

- [[Topological Validation]]
- [[Spatial Validation]]
- [[Structural Validation]]
- [[Semantic Validation]]
- [[Looks Plausible vs Is Valid]]
