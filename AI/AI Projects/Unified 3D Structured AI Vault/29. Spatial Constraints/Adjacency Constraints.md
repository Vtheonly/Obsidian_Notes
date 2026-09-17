---
tags: [constraints, spatial, adjacency]
---

# Adjacency Constraints

> **Definition.** Constraints on which elements must (or must not) be adjacent.

## Examples

- Kitchen adjacent to dining room (preferred).
- Bathroom not adjacent to kitchen (preferred).
- Bedrooms adjacent to a corridor (preferred).
- Staircase adjacent to a corridor on each floor.

## Enforcement

- Build adjacency graph.
- Check (per pair) whether adjacency holds.

## Hard vs Soft

- Hard: e.g. "every room adjacent to a corridor".
- Soft: e.g. "kitchen preferably adjacent to dining".

See [[Spatial Constraints]], [[Spatial Adjacency]].

## Related Concepts

- [[Spatial Constraints]]
- [[Spatial Adjacency]]
- [[Spatial Validation]]
