---
tags: [discovery, motifs]
---

# Structural Motif Discovery

> **Definition.** Discover recurring structural patterns (motifs) in a building or scene.

## What Is a Motif?

A motif is a **recurring pattern of relations** between objects. Examples:

```
Wall + Window + Window + Door           → facade motif
Column + Beam + Column + Beam           → structural bay motif
Room + Door + Corridor + Door + Room    → room-pair motif
Sink + Stove + Fridge                   → kitchen motif
```

A motif is **not** just a cluster of similar objects. It is a *graph pattern* — a small subgraph that recurs.

## Methods

- **Frequent subgraph mining** (gSpan, FFSM).
- **Subgraph isomorphism** (find instances of a query subgraph).
- **Graphlet counting** (count small subgraph patterns).
- **Embedding-based**: embed subgraphs, cluster them.
- **MDL-based**: find motifs that compress the graph.

## Why It's Hard

- Subgraph isomorphism is NP-hard.
- Motifs may be approximate (not exact matches).
- Motifs may overlap.
- Number of candidate motifs is exponential.

## Connection to Discovery

Motif discovery is the **graph** analog of [[Subtree Discovery]]. Together they cover the two main structural views (graph and tree).

See [[Subgraph Discovery]], [[Subtree Discovery]], [[Recursive Component Discovery]].

## Related Concepts

- [[Subgraph Discovery]]
- [[Subtree Discovery]]
- [[Contextual Motifs]]
- [[Recursive Component Discovery]]
- [[Minimum Description Length]]
