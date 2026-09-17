---
tags: [discovery, subgraph]
---

# Subgraph Discovery

> **Definition.** Discover recurring subgraphs in a graph-structured representation (e.g. scene graph).

See [[Structural Motif Discovery]] for the canonical treatment.

## Methods

- **Frequent subgraph mining**: gSpan, FFSM, GASTON.
- **Maximum common subgraph** (MCS).
- **Graphlet counting**.
- **Approximate subgraph matching**.

## Why It's Hard

- Subgraph isomorphism is NP-complete.
- Number of candidate subgraphs is exponential.
- Real graphs are noisy.

## Use Cases

- Find recurring facade motifs.
- Find recurring structural bays.
- Find recurring MEP subsystems.

See [[Structural Motif Discovery]], [[Subtree Discovery]].

## Related Concepts

- [[Structural Motif Discovery]]
- [[Subtree Discovery]]
- [[Recursive Component Discovery]]
