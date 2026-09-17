---
tags: [trees, fundamentals]
---

# Tree Terminology

> A **tree** is a connected acyclic undirected graph, or equivalently, a directed graph with one root, every non-root node having exactly one parent, and a unique path from the root to every node.

## Core Vocabulary

| Term           | Definition                                                       |
| -------------- | ---------------------------------------------------------------- |
| Node           | An element of the tree.                                          |
| Edge           | A link between two nodes (parent ↔ child).                       |
| Root           | The unique node with no parent.                                  |
| Leaf           | A node with no children.                                         |
| Internal node  | A node with at least one child.                                  |
| Parent         | The node directly above a given node.                            |
| Child          | A node directly below a given node.                              |
| Sibling        | A node sharing the same parent.                                  |
| Ancestor       | Any node on the path from root to a given node.                  |
| Descendant     | Any node reachable by descending from a given node.              |
| Depth          | Distance (edge count) from the root.                             |
| Height         | Distance from the node to its deepest descendant.                |
| Subtree        | A node and all its descendants.                                  |
| Degree         | Number of children of a node.                                    |

## Formal Definition (Directed)

A directed tree is a pair $T = (V, E)$ where:

- $V$ is a finite non-empty set of nodes,
- $E \subseteq V \times V$ is a set of directed edges,
- there is exactly one node $r \in V$ with in-degree 0 (the root),
- every other node has in-degree exactly 1,
- $T$ is connected when edge directions are ignored.

Equivalently, for every $v \in V \setminus \{r\}$ there is a unique path from $r$ to $v$.

## Why Trees Are Special

- They are the **simplest non-trivial structure** that captures hierarchy.
- They admit **recursive algorithms** naturally (process root, recurse on children).
- They have a **canonical serialization** (pre-order, post-order, bracket notation).
- They are **rigid**: each node has exactly one parent. This is also their main limitation — see [[Why Buildings Are Not Purely Trees]].

## Examples

- A file system: directories contain files and sub-directories.
- An HTML DOM: `<html>` contains `<head>` and `<body>`, etc.
- A LaTeX AST: `\frac` contains numerator and denominator.
- A BIM spatial containment: site → building → storey → space → element.

See [[Parse Trees]], [[Abstract Syntax Trees]], [[Expression Trees]], [[Building Hierarchies]], [[BIM Hierarchies]].

## Related Concepts

- [[Ordered Trees]]
- [[N-ary Trees]]
- [[What Is Tree Aware AI]]
- [[Why Buildings Are Not Purely Trees]]
