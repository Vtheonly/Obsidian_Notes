---
tags: [bim, ifc, relationships]
---

# IFC Entity Relationships

> IFC encodes relationships through `IfcRel*` entities. These are the edges in the building's graph.

## Key Relationship Types

| Relationship                          | From              | To                  | Meaning                                  |
| ------------------------------------- | ----------------- | ------------------- | ---------------------------------------- |
| `IfcRelAggregates`                    | Whole             | Parts               | A building aggregates storeys.           |
| `IfcRelContainedInSpatialStructure`   | Element           | Space               | A wall is contained in a space.          |
| `IfcRelConnectsElements`              | Element A         | Element B           | Two elements are connected (door ↔ wall).|
| `IfcRelDefinesByType`                 | Element           | Type                | An element is an instance of a type.     |
| `IfcRelDefinesByProperties`           | Element           | PropertySet         | An element has these properties.         |
| `IfcRelAssociatesMaterial`            | Element           | Material            | An element has this material.            |
| `IfcRelSpaceBoundary`                 | Space             | Element             | A space is bounded by an element.        |
| `IfcRelFillsElement`                  | Opening           | Element             | An opening is filled by an element (door).|
| `IfcRelVoidsElement`                  | Element           | Opening             | An element has an opening.               |

## Hierarchy (Containment)

```
IfcSite
    - IfcRelAggregates    IfcBuilding
         - IfcRelAggregates    IfcBuildingStorey
              - IfcRelContainedInSpatialStructure    IfcElement
```

## Connectivity (Graph)

```
IfcDoor
    - IfcRelConnectsElements    IfcWall
         - IfcRelConnectsElements    IfcSpace
              - ...
```

## Why This Matters

IFC is **both** a tree (containment via `IfcRelAggregates` + `IfcRelContainedInSpatialStructure`) **and** a graph (connectivity via `IfcRelConnectsElements` and friends).

For AI:

- Tree-aware models target the containment hierarchy.
- Graph-aware models target the connectivity graph.
- Combined models target both — see [[Combining Trees Graphs and Geometry]].

See [[IFC Overview]], [[IFC Spatial Structure]], [[Building Hierarchies]].

## Related Concepts

- [[IFC Overview]]
- [[IFC Spatial Structure]]
- [[Building Hierarchies]]
- [[BIM Relationships]]
- [[Combining Trees Graphs and Geometry]]
