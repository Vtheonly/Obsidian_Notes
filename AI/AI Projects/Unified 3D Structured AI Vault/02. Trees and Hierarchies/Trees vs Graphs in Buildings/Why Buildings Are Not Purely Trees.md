---
tags: [trees, graphs, buildings]
---

# Why Buildings Are Not Purely Trees

> A pure tree can capture **containment** but cannot capture **adjacency**, **connectivity**, **support**, **alignment**, or any many-to-many relationship. Real buildings are full of such relationships.

## The Problem

Consider a simple building with:

- 2 floors,
- 6 rooms per floor,
- 12 walls per floor,
- 4 doors between rooms per floor,
- 1 staircase connecting the floors.

If we represent this as a containment tree:

```
Building
  - Floor 1
      - Room 1.1
      - Room 1.2
      - ...
  - Floor 2
      - ...
```

then we **cannot** express:

- Room 1.1 is adjacent to Room 1.2 (they share a wall).
- Door D1 connects Room 1.1 and Room 1.2 (one door, two parents — forbidden in a tree).
- Wall W1 is shared between Room 1.1 and Room 1.2 (one wall, two spaces — forbidden in a tree).
- Staircase S1 connects Floor 1 and Floor 2 (one staircase, two floors — forbidden in a tree).
- Column C1 supports beams on both Floor 1 and Floor 2 (one column, two floors — forbidden in a tree).

## The Solution

Buildings need **three** representations, kept consistent:

1. **A tree** for containment (the spatial hierarchy).
2. **A graph** for adjacency, connectivity, support, alignment.
3. **Geometry** for actual positions, sizes, shapes.

These three representations must be synchronized. See [[Combining Trees Graphs and Geometry]], [[Cross Representation Consistency]].

## Edge Cases

Some relationships *can* be coerced into a tree:

- A wall shared between two rooms can be assigned to one room and *referenced* by the other (a "back-pointer" that breaks the tree abstraction but is implementable).
- A door can be assigned to one room and have a "connects-to" attribute pointing to the other.

But this is exactly the moment you have left pure trees and entered trees-with-graph-side-relations.

## Mathematical Note

Formally, a building is best modeled as a **stratified topological cell complex**:

- 0-cells: vertices (corners),
- 1-cells: edges (wall axes, slab boundaries),
- 2-cells: faces (wall surfaces, floor surfaces),
- 3-cells: volumes (rooms, spaces).

The **boundary operator** ∂ maps each k-cell to its (k-1)-cell boundary. This gives a *chain complex* that captures containment, adjacency, and connectivity in one structure.

See [[Topological Relations]], [[Adjacency and Containment]].

## Related Concepts

- [[Combining Trees Graphs and Geometry]]
- [[What Is Graph Aware AI]]
- [[What Is Topology Aware AI]]
- [[Scene Graph Fundamentals]]
- [[Cross Representation Consistency]]
