---
tags: [clustering, graph, community]
---

# Graph Community Detection

> **Definition.** Find groups of nodes in a graph that are densely connected internally and sparsely connected externally.

## Algorithms

- **Modularity maximization** (Louvain, Leiden).
- **Spectral clustering** on graph Laplacian.
- **Label propagation**.
- **Girvan-Newman** (edge betweenness).

## Strengths

- Works directly on graphs.
- Does not require $k$.
- Finds natural communities.

## Limitations

- Resolution limit (small communities may be merged).
- Modularity is not always the best objective.
- Hard to validate (no ground truth).

## In Buildings

Community detection on building scene graphs:

- Find zones (groups of rooms with high internal adjacency).
- Find structural bays (groups of columns + beams).
- Find MEP subsystems (pipes, ducts, wires).

See [[Spectral Clustering]], [[Structural Motif Discovery]].

## Related Concepts

- [[Spectral Clustering]]
- [[Structural Motif Discovery]]
- [[Subgraph Discovery]]
