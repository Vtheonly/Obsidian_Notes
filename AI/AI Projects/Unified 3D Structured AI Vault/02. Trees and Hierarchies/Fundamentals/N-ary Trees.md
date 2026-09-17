---
tags: [trees, n-ary]
---

# N-ary Trees

> An **n-ary tree** is a tree in which every internal node has at most $n$ children. A **binary tree** is the special case $n = 2$.

## Common Special Cases

- **Binary tree** ($n = 2$): used in expression trees (`+` has two operands), decision trees, Huffman trees.
- **Ternary tree** ($n = 3$): used in some parsing formalisms.
- **Unbounded n-ary tree**: every node can have any number of children — typical for ASTs (`if` has 2 or 3 children; `block` has 0 or more).

## Why This Matters for Generation

For an n-ary tree decoder, the model must predict:

1. **When** to stop adding children (a "stop" signal).
2. **What** each child is.
3. (If ordered) **In what order** to add them.

For a binary tree decoder, the model only predicts "left child / right child / stop".

Most modern tree decoders for code, math, and BIM use unbounded n-ary trees because real structures are not naturally binary.

## Mathematical Notation

A binary tree $T$ is either:

- the empty tree $\bot$, or
- a triple $(v, T_L, T_R)$ where $v$ is the root value and $T_L, T_R$ are binary trees.

An n-ary tree $T$ is either:

- a leaf $(v, [])$, or
- a node $(v, [T_1, T_2, \dots, T_k])$ for $k \geq 1$.

## Related Concepts

- [[Tree Terminology]]
- [[Ordered Trees]]
- [[Tree Generation]]
- [[Tree Decoding]]
