---
tags: [structure-aware, generation]
---

# Generate Structure First

> **Definition.** A generation strategy that predicts the structural skeleton first, then fills in the content.

## Pattern

```
Input
  ↓
Predict skeleton (tree shape, node types, edge list)
  ↓
Fill node attributes (text, geometry, properties)
  ↓
Finalize
```

## Examples

- **Code generation**: predict AST skeleton, then fill expressions.
- **BIM generation**: predict spatial hierarchy (building → floors → rooms), then fill geometry.
- **Scene generation**: predict scene graph (objects + relations), then generate images.
- **SQL generation**: predict clause structure, then fill column names and predicates.

## Why It Helps

- The skeleton is a smaller, easier target than the full structure.
- Constraints can be enforced on the skeleton (e.g. tree shape) before expensive content generation.
- Errors are localized: a wrong skeleton is caught early; a wrong content can be repaired without touching the skeleton.

See [[Hierarchical Decoders]], [[Tree Generation]].

## Related Concepts

- [[How Structure Enters Models]]
- [[Hierarchical Decoders]]
- [[Tree Generation]]
