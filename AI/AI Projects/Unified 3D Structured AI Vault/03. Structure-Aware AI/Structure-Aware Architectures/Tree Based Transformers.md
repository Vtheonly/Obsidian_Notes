---
tags: [structure-aware, architecture, transformer]
---

# Tree-Based Transformers

> **Definition.** A *tree-based transformer* is a Transformer variant whose attention is structured by a tree: positions correspond to tree nodes, and attention is biased (or masked) by tree relationships.

## Architecture

- **Input**: tree of nodes (e.g. AST, expression tree, BIM hierarchy).
- **Embedding**: each node gets `content_embedding + structure_embedding`.
- **Attention**: tree-structured mask or bias (see [[Structural Attention]]).
- **Output**: per-node predictions (e.g. next child, attribute, type).

## Common Variants

- **Tree Transformer** (Tay et al.): constructs a tree over the sequence and uses it as a structural prior for attention.
- **Structure-Aware Transformer** for image-to-markup: uses predicted tree structure to guide markup generation.
- **AST Transformer**: encodes ASTs of code for code completion, translation, summarization.

## When To Use

- When the input or output is naturally a tree (AST, expression, BIM hierarchy).
- When long-range dependencies follow tree paths (parent-descendant).
- When you want to enforce tree structure on the output.

## When Not To Use

- When relationships are graph-like (cycles, many-to-many) — use GAT instead.
- When sequence order is the dominant structure — use standard Transformer.

## Related Concepts

- [[Structural Attention]]
- [[Tree Positional Encodings]]
- [[Structural Embeddings]]
- [[Hierarchical Decoders]]
