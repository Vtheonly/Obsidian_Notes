---
tags: [validation, topological]
---

# Topological Validation

> **Definition.** *Topological validation* checks connectivity, adjacency, containment, and incidence relations — independent of exact metric positions.

## Checks

| Check                        | Description                                                            |
| ---------------------------- | --------------------------------------------------------------------- |
| Reachability                 | Every room is reachable from the entrance (no isolated rooms).        |
| Door connectivity            | Every door connects exactly two spaces.                               |
| Wall two-sidedness           | Every interior wall bounds exactly two spaces.                        |
| Containment closure          | If A contains B and B contains C, then A contains C.                  |
| Closed boundary              | The boundary of a space is a closed surface.                          |
| Genus / holes                | Number of tunnels through the building matches expectation.           |
| Adjacency symmetry           | If A is adjacent to B, then B is adjacent to A.                       |

## Algorithms

- **Graph BFS/DFS**: build a connectivity graph; check all nodes are reachable.
- **Cell complex boundary operator**: $\partial \circ \partial = 0$ ensures boundary consistency.
- **Persistent homology**: compute Betti numbers; check expected counts.

## When It Catches Errors

- A bedroom only reachable through a bathroom.
- A door that connects to only one room (missing graph edge).
- A wall that bounds three spaces (topological impossibility for a planar wall).
- A building with an unexpected tunnel.

## When It Misses

- Walls of wrong thickness (geometric, not topological).
- Wrong material (semantic).
- Insufficient structural support (structural).

See [[Geometric Validation]], [[Semantic Validation]], [[Structural Validation]].

## Related Concepts

- [[Geometric Validation]]
- [[Spatial Validation]]
- [[Topological Relations]]
- [[Adjacency and Containment]]
