---
tags: [foundations, awareness, hierarchy-aware]
---

# What Is Hierarchy-Aware AI

> **Definition.** A model is *hierarchy-aware* if it represents or exploits multiple levels of abstraction, where each level is composed of elements of the level below.

Hierarchy-awareness is more general than [[What Is Tree Aware AI|tree-awareness]]: a hierarchy can be a tree, but it can also be a partially ordered set of layers (e.g. pixels → segments → objects → rooms → floors → building) without strict parent-child pointers.

## Examples of Hierarchies

- **Math**: digits → terms → factors → summands → expression.
- **Code**: tokens → expressions → statements → functions → modules.
- **HTML**: text → inline → block → section → document.
- **Buildings**: element → component → room → storey → building → site.
- **Cities**: building → block → district → city.
- **Scene graphs**: primitive → object → group → scene.

See [[Building Hierarchies]], [[BIM Hierarchies]], [[Hierarchical Scene Representations]].

## What Information Makes the Model Aware?

- The **level** of each element.
- The **composition rule** between levels (what counts as a member of what).
- The **decomposition rule** (how to break a higher-level element into lower-level ones).
- The **boundary** between levels (where one stops and the next begins).

## Where Does It Enter?

- Hierarchical encoders (e.g. U-Net, Hourglass).
- Hierarchical decoders (e.g. coarse-to-fine).
- Hierarchical attention (between levels).
- Hierarchical losses (one loss per level).
- Hierarchical embeddings (level-encoding concatenated to content).

## Related Concepts

- [[What Is Tree Aware AI]]
- [[Hierarchical Scene Representations]]
- [[Building Hierarchies]]
- [[Recursive Component Discovery]]
- [[Hierarchical Clustering]]
