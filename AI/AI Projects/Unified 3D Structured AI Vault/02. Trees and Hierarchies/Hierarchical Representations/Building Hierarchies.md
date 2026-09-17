---
tags: [trees, building, hierarchy]
---

# Building Hierarchies

> A **building hierarchy** organizes a building into nested spatial entities: site → building → storey → space → element → component.

## Canonical Hierarchy

```
Site
  - Building
      - Storey
          - Space (room)
              - Element (wall, slab, column)
                  - Component (window, door)
                      - Sub-component (frame, glass)
```

## Why Hierarchy Matters

- **Containment**: each entity is *inside* exactly one parent.
- **Aggregation**: properties (area, volume, material) can be rolled up the tree.
- **Editing**: changing a storey's height propagates to all its spaces and elements.
- **Validation**: a window must be inside a wall; a wall must be inside a storey; etc.

## Why Buildings Are Not Purely Trees

The hierarchy captures **containment** but not:

- **Adjacency** (room A is next to room B).
- **Connectivity** (door connects room A and room B).
- **Support** (column supports beam).
- **Alignment** (wall is aligned with column axis).

These are **graph** relationships, not tree relationships. See [[Why Buildings Are Not Purely Trees]].

## IFC Spatial Structure

IFC formalizes the building hierarchy as `IfcSite → IfcBuilding → IfcBuildingStorey → IfcSpace → IfcElement`. See [[IFC Spatial Structure]].

## Related Concepts

- [[BIM Hierarchies]]
- [[Why Buildings Are Not Purely Trees]]
- [[Combining Trees Graphs and Geometry]]
- [[IFC Spatial Structure]]
