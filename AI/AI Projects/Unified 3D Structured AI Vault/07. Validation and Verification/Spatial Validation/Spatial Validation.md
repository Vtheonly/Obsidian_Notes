---
tags: [validation, spatial]
---

# Spatial Validation

> **Definition.** *Spatial validation* checks that objects are placed where they should be: positions, orientations, extents, relative placements.

## Checks

| Check                       | Description                                                          |
| --------------------------- | ------------------------------------------------------------------- |
| Inside parent               | Each object's bounding box is inside its parent's.                  |
| Non-overlap                 | Sibling objects do not overlap (unless overlapping is allowed).     |
| On supporting surface       | Furniture sits on the floor; columns sit on the slab.              |
| Orientation                 | Doors face the right way; windows face outward.                     |
| Distance bounds             | Toilet is not in the middle of a corridor.                          |
| Reachable                   | Door swing arc does not intersect walls.                            |

## Algorithms

- AABB / OBB intersection tests.
- Ray casting for "is this point inside the room".
- Distance fields for clearance checks.

## When It Catches Errors

- Furniture floating in mid-air.
- Door swinging into a wall.
- Furniture blocking a doorway.
- Toilet in the middle of a corridor.

## When It Misses

- Wrong room type (semantic).
- Wrong material (semantic).
- Insufficient support (structural).

See [[Geometric Validation]], [[Semantic Validation]].

## Related Concepts

- [[Geometric Validation]]
- [[Topological Validation]]
- [[Semantic Validation]]
- [[Spatial Constraints]]
