---
tags: [discovery, motifs, context]
---

# Contextual Motifs

> **Definition.** A motif that includes its **context** — the surrounding structure in which it appears.

## Why Context Matters

The same sub-structure can be meaningful in one context and meaningless in another:

- A "kitchen island" motif is meaningful in a residential kitchen, less meaningful in a commercial kitchen.
- A "column + beam" motif is meaningful in a structural frame, less meaningful if the column is decorative.

A contextual motif records:

- the motif itself (the sub-structure),
- the context (the surrounding structure),
- the conditions under which it appears.

## Discovery

Contextual motif discovery:

1. Find candidate motifs (subtrees, subgraphs).
2. For each motif, compute its context features (parent type, sibling types, neighbor types).
3. Cluster motifs by context.
4. Keep motifs that appear in consistent contexts.

See [[Structural Motif Discovery]], [[Candidate Component Scoring]].

## Related Concepts

- [[Structural Motif Discovery]]
- [[Candidate Component Scoring]]
- [[Recursive Component Discovery]]
