---
tags: [bim, ifc, spatial]
---

# IFC Spatial Structure

> The IFC spatial containment hierarchy: `IfcSite → IfcBuilding → IfcBuildingStorey → IfcSpace → IfcElement`.

## Hierarchy

```
IfcSite
  - IfcBuilding (via IfcRelAggregates)
      - IfcBuildingStorey (via IfcRelAggregates)
          - IfcSpace (via IfcRelAggregates)
              - IfcElement (via IfcRelContainedInSpatialStructure)
```

## IfcSite

The top-level spatial element: a plot of land. Contains buildings.

## IfcBuilding

A single building. Contains storeys.

## IfcBuildingStorey

A floor / level of a building. Contains spaces and elements.

## IfcSpace

A volume bounded by elements (walls, slabs). Represents a room, corridor, or other usable space.

## IfcElement

A physical building element: `IfcWall`, `IfcSlab`, `IfcColumn`, `IfcBeam`, `IfcDoor`, `IfcWindow`, `IfcRoof`, etc.

## Why It Matters

The spatial structure is the **tree** of the BIM model. It captures containment (what is inside what). It does NOT capture adjacency, connectivity, or support — those are graph relationships (see [[IFC Entity Relationships]]).

For tree-aware AI:

- The spatial structure is the target tree.
- Each node has a type (`IfcWall`, `IfcSlab`, ...).
- Each node has geometry, properties, materials.

See [[BIM Hierarchies]], [[Building Hierarchies]], [[Tree Based BIM]].

## Related Concepts

- [[BIM Hierarchies]]
- [[Building Hierarchies]]
- [[IFC Entity Relationships]]
- [[Tree Based BIM]]
