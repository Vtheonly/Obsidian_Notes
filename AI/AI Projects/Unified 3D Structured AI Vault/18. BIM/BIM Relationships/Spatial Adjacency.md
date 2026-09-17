---
tags: [bim, adjacency]
---

# Spatial Adjacency

> Two spatial elements are **adjacent** if they share a boundary. This is a graph relation, not a tree relation.

## Examples

- Two rooms adjacent if they share a wall.
- A room adjacent to a corridor if they share a wall.
- Two storeys adjacent if they share a slab.

## IFC Encoding

- `IfcRelConnectsElements` (generic connection).
- `IfcRelSpaceBoundary` (space bounded by element; gives adjacency between spaces).

## Why It Matters

Adjacency enables:

- Path planning (which rooms are reachable?).
- Acoustic analysis (sound transmission between rooms).
- Thermal analysis (heat transfer between rooms).
- Code compliance (e.g. minimum corridor width to adjacent rooms).

## Validation

- Adjacency is symmetric: if A is adjacent to B, B is adjacent to A.
- Adjacency must be consistent with geometry (the shared boundary must exist geometrically).

See [[BIM Relationships]], [[Adjacency and Containment]], [[Spatial Validation]].

## Related Concepts

- [[BIM Relationships]]
- [[Adjacency and Containment]]
- [[Connectivity Relationships]]
- [[Spatial Validation]]
