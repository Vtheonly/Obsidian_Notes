---
tags: [paper, tree-aware, image-to-markup]
---

# Paper — A Tree-Based Structure-Aware Transformer Decoder for Image-to-Markup Generation

## Problem

Image-to-markup systems (image → LaTeX, image → HTML, image → music notation) traditionally generate markup as a flat sequence of tokens. This ignores the natural hierarchical structure of the markup (e.g. nested tags in HTML, fractions in LaTeX). The paper asks: can structure-aware generation improve quality?

## Input

A rendered image of a markup expression (e.g. a screenshot of a LaTeX equation).

## Output

A markup string (e.g. LaTeX) that, when rendered, matches the input image.

## 3D Representation

N/A (this paper is about 2D images → 1D markup).

## Structural Representation

A tree (the AST of the markup). The paper represents the markup as a tree where each node is a markup construct (e.g. `Fraction`, `Superscript`, `Radical`) and children are sub-expressions.

## Tree Representation

An AST-like tree of markup constructs. Each node has a type and attributes; children are sub-expressions.

## Graph Representation

N/A (tree only).

## BIM Representation

N/A.

## Geometry Representation

N/A.

## How Is Structure Represented?

Explicitly as a tree data structure. The decoder predicts tree nodes (type, parent, attributes) rather than tokens.

## How Is Structure Learned?

Learned from data (paired image-tree examples).

## Where Does Structural Information Enter?

In the decoder: the decoder is a tree decoder that, at each step, decides to attach a new node to an existing parent. Structural information is also used in attention (the decoder attends to ancestor nodes preferentially).

## Where Does 3D Information Enter?

N/A.

## Training Objective

Maximize the likelihood of the correct tree given the image.

## Loss Functions

Per-node cross-entropy (predicted node type vs. target).

## Generation Process

Tree decoding: start from a root, predict children of the root, recurse.

## Constraints

Implicit in the tree decoder: the output is always a tree by construction. No explicit grammar mask is mentioned.

## Validation

Implicit: the output is parseable because it's a tree.

## Verification

N/A.

## Search

Beam search over tree expansions.

## Repair

N/A.

## Failure Modes

- Wrong tree structure (wrong parent for a node).
- Wrong node attributes (wrong type, wrong parameters).
- Long expressions may have compounding errors.

## What Is Guaranteed?

The output is a tree (by construction).

## What Is Merely Probabilistic?

The tree is the correct one for the image (probabilistic).

## Main Contribution

A tree-based decoder for image-to-markup that explicitly generates the markup tree, improving over sequence-based decoders.

## Limitations

- Only tree structure (no graph).
- No hard semantic constraints (only structural).
- No verification of correctness (only parseability).

## Related Concepts

- [[What Is Tree Aware AI]]
- [[What Is Structure Aware AI]]
- [[Tree Generation]]
- [[Tree Decoding]]
- [[Tree Based Transformers]]
- [[Structural Attention]]
- [[How Structure Enters Models]]

## My Interpretation

This paper is a clean example of "tree-aware by construction": the decoder cannot emit a non-tree. The guarantee is structural (it's a tree), not semantic (it's the right tree). For BIM generation, this suggests that a tree decoder for BIM hierarchy would give structural guarantees for free, but semantic and geometric properties would still need explicit constraints or verification.
