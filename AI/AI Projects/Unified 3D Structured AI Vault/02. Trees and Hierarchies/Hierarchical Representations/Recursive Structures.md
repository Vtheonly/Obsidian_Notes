---
tags: [trees, recursive]
---

# Recursive Structures

> A **recursive structure** is one whose parts have the same type as the whole. Trees are the canonical example: a subtree is itself a tree.

## Why Recursion Matters

- Trees are recursive by definition: a tree is either a leaf or a node with subtrees.
- Recursive algorithms (DFS, divide-and-conquer) operate naturally on trees.
- Recursive generation (top-down) produces a tree by recursively generating subtrees.
- Recursive discovery ([[Recursive Component Discovery]]) finds motifs by repeatedly applying discovery to simplified representations.

## Examples

- ASTs: a function body is a list of statements; each statement is itself an AST.
- Scene graphs: a group is itself a scene (with sub-objects).
- CAD feature trees: a feature's input is the result of a previous feature (itself a tree).
- Building hierarchy: a storey is a building-like structure (rooms, walls, slabs).
- Recursive neural networks: each subtree is encoded by the same network applied recursively.

## Recursive Neural Networks

A recursive neural network (RecNN) encodes a tree by:

1. Encoding each leaf.
2. For each internal node, combining its children's encodings using a learned combination function.

Output: a single vector for the whole tree, plus per-node vectors.

This is the tree analogue of an RNN (sequence) or CNN (grid).

## Related Concepts

- [[Hierarchical Scene Representations]]
- [[Recursive Component Discovery]]
- [[Tree Generation]]
- [[Tree Embeddings and Attention]]
