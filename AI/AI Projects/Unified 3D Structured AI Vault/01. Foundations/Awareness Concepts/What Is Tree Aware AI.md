---
tags: [foundations, awareness, tree-aware]
---

# What Is Tree-Aware AI

> **Definition.** A model is *tree-aware* if it incorporates information about hierarchical parent-child relationships represented by a tree.

A tree is one particular kind of structure. Tree-awareness is therefore a specialization of [[What Is Structure Aware AI|structure-awareness]].

## What Information Makes the Model Aware?

The model must somehow know, for each node:

- its **parent** (if any),
- its **children** (if any),
- its **siblings** (other children of the same parent),
- its **depth** (distance from the root),
- whether it is a **leaf** or an **internal node**,
- and possibly its **position** among its siblings (in ordered trees).

See [[Tree Terminology]] for the formal vocabulary.

## Where Does the Information Come From?

| Source                | Example                                                                |
| --------------------- | ---------------------------------------------------------------------- |
| Parser                | LaTeX → AST, code → AST, HTML → DOM.                                   |
| Schema                | BIM spatial containment tree, CAD feature tree.                        |
| Annotation            | Scene graph tree with manual labels.                                   |
| Learned               | Predicted parent-of relation from data.                                |
| Implicit              | Tree-structured positional encoding derived from a sequence of tokens. |

## How Is It Represented?

- Explicit pointer / edge list `(parent, child)`.
- Adjacency matrix on a tree-shaped graph.
- Sequence with bracket tokens (e.g. `(`, `)` in S-expressions).
- Position encoding that encodes the path from the root.
- Embedding concatenated with structural features.

## Where Does It Enter the Architecture?

- **Input embeddings** (token + structure position).
- **Attention mask** (tree-structured mask, parent/child/sibling bias).
- **Decoder** (top-down tree decoder predicting children of a node).
- **Loss** (tree-structured loss comparing predicted and target trees).
- **Constraints** (grammar or schema restricting next tokens).

## Does It Create Hard Guarantees?

Not necessarily. Common forms:

- **Soft**: tree embeddings bias attention statistically; invalid trees can still occur.
- **Hard**: a tree decoder literally cannot emit a non-tree because each node is generated as a child of an existing parent.
- **Verified**: a validator rejects invalid candidates at decode time.

See [[Hard Guarantees vs Statistical Preferences]].

## Example: Image-to-LaTeX

Consider the expression:

```text
\frac{x + 1}{y - 2}
```

A sequence decoder sees tokens `\frac { x + 1 } { y - 2 }`. A tree-aware decoder additionally knows:

- The fraction has two children: numerator and denominator.
- `x + 1` belongs to the numerator subtree.
- `y - 2` belongs to the denominator subtree.

See [[What Is Structure Aware AI]] for the broader context and [[Paper — Tree Based Structure Aware Transformer Decoder for Image To Markup]] for a concrete paper.

## Related Concepts

- [[Tree Terminology]]
- [[Parse Trees]]
- [[Abstract Syntax Trees]]
- [[Expression Trees]]
- [[Tree Generation]]
- [[Tree Based Transformers]]
- [[Tree Positional Encodings]]
