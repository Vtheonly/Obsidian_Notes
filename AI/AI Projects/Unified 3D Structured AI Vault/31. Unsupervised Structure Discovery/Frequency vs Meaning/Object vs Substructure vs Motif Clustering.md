---
tags: [discovery, clustering-levels]
---

# Object vs Substructure vs Motif Clustering

> Three levels of structural clustering.

## Level 1: Object-Level Clustering

Cluster individual objects by similarity:

```
Chair  Chair  Chair  Chair  →  "chair" cluster
Table  Table                →  "table" cluster
Lamp   Lamp                 →  "lamp" cluster
```

Standard clustering (K-Means, HDBSCAN, etc.) on object features.

## Level 2: Substructure Clustering

Cluster substructures — groups of objects that form a coherent sub-component:

```
Window + Frame + Glass + Sill     →  "window assembly" substructure
Door + Frame + Handle + Hinge     →  "door assembly" substructure
Kitchen = Sink + Stove + Fridge   →  "kitchen" substructure
```

Requires:

- identifying groups (not just individual objects),
- comparing groups (not just features),
- handling variable group sizes.

## Level 3: Structural Motif Clustering

Cluster motifs — recurring patterns of relations between objects:

```
Wall + Window + Window + Door          →  "facade motif"
Room + Room + Corridor                 →  "room-cluster motif"
Column + Beam + Column + Beam          →  "structural bay motif"
```

A motif is a **graph pattern**. Motif discovery = frequent subgraph mining.

## Why the Distinction Matters

- Object clustering finds elements.
- Substructure clustering finds components.
- Motif clustering finds patterns.

Each level corresponds to a different granularity of structure. A complete discovery system operates at all three levels and combines them hierarchically.

See [[Structural Motif Discovery]], [[Recursive Component Discovery]], [[Object vs Substructure vs Motif Clustering]].

## Related Concepts

- [[Structural Motif Discovery]]
- [[Subtree Discovery]]
- [[Subgraph Discovery]]
- [[Recursive Component Discovery]]
