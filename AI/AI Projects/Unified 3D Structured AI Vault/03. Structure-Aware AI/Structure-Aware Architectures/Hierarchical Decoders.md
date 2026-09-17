---
tags: [structure-aware, architecture, decoder]
---

# Hierarchical Decoders

> **Definition.** A *hierarchical decoder* generates output in layers, from coarse to fine, where each layer conditions on the previous.

## Pattern

```
Layer 1: predict top-level structure (e.g. rooms).
Layer 2: for each room, predict its walls.
Layer 3: for each wall, predict its openings.
Layer 4: for each opening, predict its geometry.
```

## Examples

- **Layout generation**: predict room rectangles, then furniture per room.
- **BIM generation**: predict building tree, then fill geometry per element.
- **Code generation**: predict function signatures, then bodies.
- **Document generation**: predict section structure, then content per section.

## Why It Helps

- Each layer has a smaller, easier decision space.
- Constraints can be enforced layer by layer.
- Errors at one layer are caught before propagating deeper.
- Naturally produces hierarchical outputs.

## Trade-offs

- **Pro**: strong structure, easy to constrain, easy to validate.
- **Con**: more complex training (multi-layer loss), harder to do end-to-end differentiability, can lose fine-grained coupling between layers.

See [[Generate Structure First]], [[Tree Generation]].

## Related Concepts

- [[Generate Structure First]]
- [[Tree Generation]]
- [[Hierarchical Decoders]]
- [[Top Down Generation]]
