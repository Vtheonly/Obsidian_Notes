---
tags: [topology, relations]
---

# Topological Relations

> **Definition.** *Topological relations* describe connectivity, adjacency, containment, and incidence — properties that are invariant under continuous deformation.

## RCC8 (Region Connection Calculus)

A standard set of 8 topological relations between two regions:

| Relation            | Meaning                                                  |
| ------------------- | -------------------------------------------------------- |
| DC (disconnected)   | A and B do not touch.                                    |
| EC (externally connected) | A and B share a boundary, no interior overlap.      |
| PO (partial overlap)| A and B overlap partially.                               |
| EQ (equal)          | A and B are the same.                                    |
| TPP (tangential proper part) | A is inside B and touches B's boundary.          |
| NTPP (non-tangential proper part) | A is strictly inside B, no touching.           |
| TPPi (inverse of TPP) | B is inside A and touches A's boundary.                |
| NTPPi (inverse of NTPP) | B is strictly inside A.                                |

## 9-Intersection Model

For two regions $A, B$ with interiors $A^\circ, B^\circ$, boundaries $\partial A, \partial B$, and exteriors $A^-, B^-$:

The 9 intersections $A^\circ \cap B^\circ, A^\circ \cap \partial B, \dots$ determine the topological relation.

## In Buildings

- Two rooms can be **DC** (no shared wall), **EC** (shared wall), **PO** (overlap — impossible for proper rooms).
- A window **TPP** a wall (inside, touching boundary).
- A column **NTPP** a room (strictly inside, not touching).

## Why It Matters

Topological relations are invariant under deformation (a stretched room is still the same room topologically). This makes them robust to geometric noise.

See [[Spatial Relations]], [[Adjacency and Containment]], [[Topological Validation]].

## Related Concepts

- [[Spatial Relations]]
- [[Adjacency and Containment]]
- [[Topological Validation]]
- [[What Is Topology Aware AI]]
