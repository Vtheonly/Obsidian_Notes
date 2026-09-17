---
tags: [discovery, hierarchical, concepts]
---

# Hierarchical Concept Discovery

> **Definition.** Discover concepts at multiple levels of abstraction, where higher-level concepts are composed of lower-level ones.

## Pipeline

1. Start with raw data (e.g. building elements).
2. Discover recurring patterns at level 1 (e.g. windows, doors).
3. Abstract them as concepts.
4. Discover recurring patterns of concepts at level 2 (e.g. facades).
5. Abstract them as higher-level concepts.
6. Repeat.

This is essentially [[Recursive Component Discovery]] applied to concept learning.

## Why It Matters

- Concepts at higher levels capture more abstract structure.
- Hierarchy matches human cognition (we think in concepts at multiple scales).
- Hierarchical concepts support transfer learning.

## Methods

- **Hierarchical clustering** on concept embeddings.
- **MDL-based**: keep concepts that reduce total description length.
- **Neural**: hierarchical VAE, hierarchical contrastive learning.

See [[Recursive Component Discovery]], [[Hierarchical Clustering]], [[Minimum Description Length]].

## Related Concepts

- [[Recursive Component Discovery]]
- [[Hierarchical Clustering]]
- [[Minimum Description Length]]
- [[Embedding Spaces for Structure]]
