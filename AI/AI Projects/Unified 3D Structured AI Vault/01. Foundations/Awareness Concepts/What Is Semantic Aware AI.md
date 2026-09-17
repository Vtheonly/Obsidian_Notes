---
tags: [foundations, awareness, semantic-aware]
---

# What Is Semantic-Aware AI

> **Definition.** A model is *semantic-aware* if it represents or exploits the *meaning* of objects, classes, attributes, and their semantic relationships, beyond raw appearance or geometry.

## What Information Makes the Model Aware?

- **Class labels**: wall, door, window, slab, column, beam, roof.
- **Attributes**: fire-rating, load-bearing, material, finish, U-value.
- **Semantic relations**: `supports`, `separates`, `contains`, `accesses`, `illuminates`.
- **Domain semantics**: structural role, thermal role, acoustic role.
- **Co-occurrence**: a door is usually between two rooms; a window is usually in a wall; a column usually supports a beam.

## Where Does It Enter?

- Semantic embeddings (class embedding, attribute embedding).
- Semantic losses (cross-entropy on classes, attribute regression).
- Semantic constraints (a `door` must connect exactly two `rooms`).
- Semantic attention (attention biased by class compatibility).
- Semantic validators (rule checkers).

## Why It Matters

A geometrically valid model can still be semantically wrong: a "door" floating in mid-air is geometrically fine but semantically meaningless. A "load-bearing wall" made of paper is geometrically fine but violates the structural semantics. See [[Semantic Validation]], [[Semantic Constraints]].

## Related Concepts

- [[What Is Structure Aware AI]]
- [[Semantic Validation]]
- [[Semantic Constraints]]
- [[BIM Objects]]
- [[Property Sets]]
