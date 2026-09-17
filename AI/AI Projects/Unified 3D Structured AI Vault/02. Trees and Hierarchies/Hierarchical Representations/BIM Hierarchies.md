---
tags: [trees, bim, hierarchy]
---

# BIM Hierarchies

> A **BIM hierarchy** is the spatial containment tree of a BIM model, formalized by IFC as `IfcSite → IfcBuilding → IfcBuildingStorey → IfcSpace → IfcElement`.

## IFC Spatial Containment

```
IfcSite
  - IfcBuilding
      - IfcBuildingStorey (Ground)
          - IfcSpace (Living Room)
              - IfcWall
                  - IfcWindow
                  - IfcDoor
              - IfcSlab (floor)
          - IfcSpace (Kitchen)
              - ...
      - IfcBuildingStorey (First)
          - ...
```

## What the Hierarchy Captures

- **Containment**: each entity is spatially inside its parent.
- **Aggregation**: properties roll up (total floor area = sum of room areas).
- **Decomposition**: a building decomposes into storeys, storeys into spaces, etc.

## What the Hierarchy Does Not Capture

- **Adjacency** (uses `IfcRelConnects`).
- **Connectivity** (uses `IfcRelConnectsElements` for doors between spaces).
- **Type assignment** (uses `IfcRelDefinesByType`).
- **Material assignment** (uses `IfcRelAssociatesMaterial`).

These are **relationships**, not tree edges. See [[IFC Entity Relationships]].

## BIM Hierarchy as a Tree

For tree-aware models, the BIM hierarchy is a tree where:

- **Nodes** are spatial entities.
- **Edges** are containment relations.
- **Node attributes** include type, geometry, properties, materials.
- **Side graph** contains non-containment relations.

See [[What Is Tree Aware AI]], [[Tree Based BIM]], [[BIM Generation]].

## Related Concepts

- [[Building Hierarchies]]
- [[IFC Spatial Structure]]
- [[IFC Entity Relationships]]
- [[Tree Based BIM]]
- [[Combining Trees Graphs and Geometry]]
