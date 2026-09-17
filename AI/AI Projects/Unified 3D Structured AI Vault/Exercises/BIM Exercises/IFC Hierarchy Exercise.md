---
tags: [exercise, bim, ifc]
---

# Exercise — IFC Hierarchy

## Problem

Given the following IFC entities (in pseudo-IFC):

```
#1 = IfcSite
#2 = IfcBuilding
#3 = IfcBuildingStorey (Ground)
#4 = IfcBuildingStorey (First)
#5 = IfcSpace (Living Room)
#6 = IfcSpace (Kitchen)
#7 = IfcWall (W1)
#8 = IfcWall (W2)
#9 = IfcDoor (D1)
#10 = IfcWindow (V1)
```

(a) Draw the spatial containment tree using `IfcRelAggregates` and `IfcRelContainedInSpatialStructure`.
(b) Where would you put D1 and V1 in the tree?
(c) What relationships would you add (using `IfcRelConnectsElements`, `IfcRelSpaceBoundary`)?

## Required Background

- IFC spatial structure: see [[IFC Spatial Structure]].
- IFC relationships: see [[IFC Entity Relationships]].

## Correct Answers

### (a) Spatial Containment Tree

```
IfcSite (#1)
  - IfcBuilding (#2)
      - IfcBuildingStorey Ground (#3)
          - IfcSpace Living Room (#5)
              - IfcWall W1 (#7)  [via IfcRelContainedInSpatialStructure]
          - IfcSpace Kitchen (#6)
              - IfcWall W2 (#8)
      - IfcBuildingStorey First (#4)
          - (no spaces yet)
```

### (b) Where to Put D1 and V1

- D1 (door): typically contained in a wall (e.g. W1) via `IfcRelVoidsElement` (the wall has an opening) and `IfcRelFillsElement` (the opening is filled by the door). The door itself is usually *not* contained in a space directly; rather, it connects two spaces.
- V1 (window): similarly, contained in a wall via opening/filling relations.

So:

- W1 has an opening (via `IfcRelVoidsElement`).
- The opening is filled by D1 (via `IfcRelFillsElement`).
- Optionally, V1 is in another wall (e.g. W2) similarly.

### (c) Additional Relationships

- `IfcRelConnectsElements` between D1 and W1 (door is in wall).
- `IfcRelSpaceBoundary` between Living Room (#5) and W1 (wall bounds the living room).
- `IfcRelSpaceBoundary` between Kitchen (#6) and W2.
- `IfcRelConnectsElements` between D1 and the two spaces it connects (e.g. Living Room and Kitchen, if D1 is between them).
- `IfcRelDefinesByType` for each element (assign a type).
- `IfcRelDefinesByProperties` for property sets.
- `IfcRelAssociatesMaterial` for materials.

## Common Mistakes

- Putting doors and windows directly in spaces (they go in walls).
- Forgetting the opening/filling relations.
- Confusing containment (`IfcRelContainedInSpatialStructure`) with connectivity (`IfcRelConnectsElements`).

## Edge Cases

- A door between two storeys (e.g. an exterior door on a stair landing) needs careful placement.
- A window spanning two storeys is unusual but possible.

## Implementation Considerations

When building IFC programmatically (e.g. with IfcOpenShell), you must create both the elements and the relationship objects. Forgetting the relationships leaves elements "floating" without context.

## Related Concepts

- [[IFC Spatial Structure]]
- [[IFC Entity Relationships]]
- [[BIM Hierarchies]]
- [[BIM Relationships]]
- [[IFC Parsing With IfcOpenShell]]
