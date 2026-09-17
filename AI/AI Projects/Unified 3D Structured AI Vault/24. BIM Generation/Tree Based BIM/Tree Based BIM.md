---
tags: [bim-generation, tree]
---

# Tree-Based BIM Generation

> **Definition.** Generate a BIM model as a **tree** (the spatial containment hierarchy), then fill in geometry, properties, and relations.

## Pipeline

```
Predict root (IfcBuilding)
  ↓
Predict storeys (children of root)
  ↓
For each storey, predict spaces (children of storey)
  ↓
For each space, predict elements (walls, slabs, doors, windows)
  ↓
For each element, predict geometry, properties, materials
  ↓
Predict non-tree relations (adjacency, connectivity) as a graph
  ↓
Validate
```

## Why It's Natural

- BIM is naturally a tree (containment) + a graph (relations).
- A tree decoder naturally produces the containment tree.
- The graph can be predicted separately (or alongside the tree).
- Constraints are easy to enforce (a wall must be in a storey; a door must be in a wall; etc.).

## Architectures

- **Tree Transformer**: encode partial tree, predict next node.
- **Tree RNN**: recursive generation.
- **Hierarchical Decoder**: predict layers (storeys → rooms → elements).

## Strengths

- Output is a valid BIM hierarchy by construction (if tree decoder is used).
- Easy to constrain.
- Easy to validate.
- Easy to convert to IFC.

## Limitations

- Requires custom architecture (no standard tree Transformer in most libraries).
- Hard to do end-to-end differentiability.
- May miss cross-hierarchy dependencies (e.g. door connects two rooms in different storeys — but actually this is rare).

See [[BIM Generation]], [[Tree Generation]], [[Hierarchical Decoders]], [[Constrained BIM]].

## Related Concepts

- [[BIM Generation]]
- [[Tree Generation]]
- [[Hierarchical Decoders]]
- [[Constrained BIM]]
- [[BIM Hierarchies]]
