---
tags: [spatial, relations]
---

# Spatial Relations

> **Definition.** *Spatial relations* describe how objects are placed relative to each other in space.

## Categories

| Category                | Examples                                              |
| ----------------------- | ----------------------------------------------------- |
| Topological             | adjacent, contains, inside, overlaps, touches.        |
| Directional             | above, below, left-of, right-of, in-front-of, behind. |
| Distance                | near, far, within R.                                  |
| Orientation             | parallel-to, perpendicular-to, aligned-with.          |
| Order                   | first, second, ..., before, after.                    |

## In Buildings

- Room A is **adjacent to** room B (shared wall).
- Wall W is **contained in** storey S.
- Door D **connects** room A and room B.
- Window V is **in** wall W.
- Column C **supports** beam B.
- Staircase S **connects** storey 1 and storey 2.

## Representation

- **Graph**: nodes are objects, edges are typed relations.
- **Coordinate-based**: derive relations from positions (e.g. adjacent if shared boundary).
- **Hybrid**: combine graph and coordinate-based.

See [[Scene Graph Fundamentals]], [[Topological Relations]].

## Related Concepts

- [[Topological Relations]]
- [[Adjacency and Containment]]
- [[Scene Graph Fundamentals]]
- [[What Is Spatially Aware AI]]
