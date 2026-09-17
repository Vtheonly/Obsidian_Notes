---
tags: [foundations, awareness, topology-aware]
---

# What Is Topology-Aware AI

> **Definition.** A model is *topology-aware* if it represents or exploits connectivity, adjacency, incidence, and containment relations independent of exact metric positions.

Topology is geometry *without distances*. Two rooms are adjacent whether or not their shared wall is exactly 0.20 m thick.

## What Information Makes the Model Aware?

- **Adjacency**: room A shares a boundary with room B.
- **Connectivity**: there is a path from room A to room B through doors.
- **Containment**: window W is inside wall K, which is inside floor F.
- **Incidence**: edge E is incident to vertex V.
- **Boundary**: surface S bounds volume V.
- **Genus / holes**: how many tunnels through the object.

## Where Does It Enter?

- Graph/topology encoders (cell complexes, simplicial complexes).
- Topological losses (Betti numbers, persistent homology).
- Topological constraints (every room must be reachable; every wall must bound exactly two spaces).
- Topological validators (a watertight mesh must have genus matching its boundary).

## Why It Matters for Buildings

A floor plan is *topologically* wrong if a bedroom is only reachable by walking through a bathroom — even if all walls are geometrically perfect. Topological-awareness catches these errors that geometric validation alone misses.

See [[Topological Validation]], [[Topological Relations]], [[Adjacency and Containment]].

## Related Concepts

- [[What Is Graph Aware AI]]
- [[What Is Spatially Aware AI]]
- [[Topological Relations]]
- [[Topological Validation]]
