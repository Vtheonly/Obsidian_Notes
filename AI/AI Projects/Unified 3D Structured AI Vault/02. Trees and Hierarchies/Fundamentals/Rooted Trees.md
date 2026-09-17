---
tags: [trees, rooted]
---

# Rooted Trees

> A **rooted tree** is a tree in which one node is designated as the root, inducing a natural direction (away from the root) on all edges.

Most trees in AI are rooted:

- ASTs are rooted at the program node.
- BIM containment is rooted at the site or building.
- Scene graphs are rooted at the scene.

## Why Rooting Matters

Rooting gives:

- A natural traversal direction (top-down from root to leaves).
- A natural parent-child relation.
- A unique path from root to every node (used for tree positional encodings).
- A natural recursion: solve the problem at the root by recursively solving it at each subtree.

## Rooted vs Unrooted

An unrooted tree is just a graph-theoretic tree (connected acyclic). Rooting it picks a "starting point" and induces a direction. The same unrooted tree can be rooted in $|V|$ different ways.

In AI we almost always work with rooted trees because we need a starting point for generation and a direction for parent-child relations.

## Related Concepts

- [[Tree Terminology]]
- [[Top Down Generation]]
- [[Bottom Up Generation]]
