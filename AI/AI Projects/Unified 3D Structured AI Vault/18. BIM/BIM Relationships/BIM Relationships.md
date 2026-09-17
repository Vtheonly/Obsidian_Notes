---
tags: [bim, relationships]
---

# BIM Relationships

> The graph edges of a BIM model. See [[IFC Entity Relationships]] for the full enumeration.

## Major Categories

```mermaid
mindmap
  root((BIM Relationships))
    Containment
      Site contains Building
      Building contains Storey
      Storey contains Space
      Space contains Element
    Connectivity
      Door connects Spaces
      Wall touches Wall
      Column supports Beam
    Type
      Element has Type
    Material
      Element has Material
    Property
      Element has PropertySet
    Spatial Boundary
      Space bounded by Elements
    Opening
      Element has Opening
      Opening filled by Element
```

## Why It Matters

A BIM model is a tree (containment) **plus** a graph (other relations). Tree-aware AI captures the tree; graph-aware AI captures the graph; full BIM-aware AI captures both.

See [[IFC Entity Relationships]], [[Combining Trees Graphs and Geometry]].

## Related Concepts

- [[IFC Entity Relationships]]
- [[Combining Trees Graphs and Geometry]]
- [[Containment Relationships]]
- [[Spatial Adjacency]]
