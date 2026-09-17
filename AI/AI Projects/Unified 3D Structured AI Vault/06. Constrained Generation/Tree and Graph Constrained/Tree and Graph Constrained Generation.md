---
tags: [constrained-generation, tree, graph]
---

# Tree- and Graph-Constrained Generation

> **Definition.** Generation that produces only valid trees (or graphs) by construction or by constraint.

## Tree-Constrained Generation

Mechanisms:

- **Tree decoder**: each step attaches a node to an existing parent. Output is a tree by construction.
- **Bracket-sequence constrained**: serialize tree as bracketed sequence; constrain with a grammar of balanced brackets.
- **Parent-pointer constrained**: each generated node is given a parent pointer; constraint: pointer must point to an existing node, no cycles, single root.

## Graph-Constrained Generation

Mechanisms:

- **Edge-by-edge generation**: at each step, add a node or edge. Constraint: no edge between non-existent nodes, no duplicate edges, max degree, etc.
- **Adjacency matrix generation**: generate a matrix with binary constraints (symmetric, no self-loops, max degree).
- **Motif-based**: generate by assembling pre-defined motifs, ensuring motif interfaces match.

## Hard vs Soft

- **Hard**: invalid structures are impossible (constraint mask or decoder shape).
- **Soft**: invalid structures are penalized (loss, attention bias).

See [[Hard Guarantees vs Statistical Preferences]].

## Why It Matters for BIM

A BIM model is a tree (containment) plus a graph (relations). Tree-constrained + graph-constrained generation produces:

- valid containment trees,
- valid relation graphs,
- consistent geometry (if also geometrically constrained).

This is the foundation of [[Constrained BIM]] and [[Verifiable Generation]].

## Related Concepts

- [[Constrained Decoding]]
- [[Tree Generation]]
- [[Constrained BIM]]
- [[Hard Guarantees vs Statistical Preferences]]
