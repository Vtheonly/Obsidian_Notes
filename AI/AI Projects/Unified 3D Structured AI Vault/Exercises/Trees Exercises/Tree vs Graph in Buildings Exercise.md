---
tags: [exercise, trees, graphs, buildings]
---

# Exercise — Tree vs Graph in Buildings

## Problem

Consider a simple building:

- 2 storeys.
- Storey 1 has 3 rooms (R1, R2, R3) connected by a corridor C1.
- Storey 2 has 2 rooms (R4, R5) connected by a corridor C2.
- A staircase S connects C1 and C2.
- Wall W1 is shared between R1 and R2.
- Door D1 connects R1 and C1.
- Door D2 connects R2 and C1.
- Door D3 connects R3 and C1.
- Door D4 connects R4 and C2.
- Door D5 connects R5 and C2.

(a) Draw the containment tree.
(b) Draw the connectivity graph.
(c) Identify which relationships cannot be represented in the tree alone.
(d) Explain why a building representation needs both.

## Required Background

- A **tree** captures parent-child containment (each node has one parent).
- A **graph** captures arbitrary pairwise relations.
- See [[Why Buildings Are Not Purely Trees]], [[Combining Trees Graphs and Geometry]].

## Correct Answers

### (a) Containment Tree

```
Building
  - Storey 1
      - R1 (contains Wall W1 part, Door D1)
      - R2 (contains Wall W1 part, Door D2)
      - R3 (contains Door D3)
      - C1 (corridor)
  - Storey 2
      - R4 (contains Door D4)
      - R5 (contains Door D5)
      - C2 (corridor)
  - Staircase S (special: spans both storeys)
```

Note: Wall W1 is shared between R1 and R2 — a pure tree cannot represent this. We must assign W1 to one room (e.g. R1) and add a back-reference (which is a graph edge). Staircase S is similarly shared between Storey 1 and Storey 2.

### (b) Connectivity Graph

Nodes: R1, R2, R3, R4, R5, C1, C2, S.

Edges:
- R1 — D1 — C1 (R1 connected to C1 via D1)
- R2 — D2 — C1
- R3 — D3 — C1
- R4 — D4 — C2
- R5 — D5 — C2
- C1 — S — C2 (staircase connects the two corridors)

Also: adjacency edges:
- R1 —adj— R2 (shared wall W1)
- (other adjacencies as applicable)

### (c) Relationships That Cannot Be in the Tree Alone

1. **Wall W1 shared between R1 and R2**: in a pure tree, W1 can only have one parent (either R1 or R2). The other room cannot "contain" W1.

2. **Door D1 connects R1 and C1**: in a pure tree, D1 can only have one parent (either R1 or C1). The connection to the other room is a graph edge.

3. **Staircase S connects Storey 1 and Storey 2**: S can only have one parent. The connection to the other storey is a graph edge.

4. **Adjacency between R1 and R2**: adjacency is a graph relation; not a tree relation.

### (d) Why Both Are Needed

A pure tree captures containment but loses:

- connectivity (which rooms are reachable from which),
- adjacency (which rooms share walls),
- support (which elements support which),
- multi-parent relations (shared walls, connecting doors, spanning staircases).

A pure graph captures connectivity but loses:

- hierarchy (which element is in which storey),
- aggregation (total area of a storey = sum of room areas),
- editing semantics (moving a storey moves all its rooms).

Buildings need **both**: a tree for containment/hierarchy, and a graph for connectivity/adjacency. Geometry is needed on top.

## Common Mistakes

- Forcing everything into a tree (assigning W1 to R1 and forgetting R2's claim).
- Forcing everything into a graph (losing hierarchy).
- Confusing adjacency with containment.

## Edge Cases

- A column supporting beams on two storeys: shared like the staircase.
- A pipe running through multiple rooms: shared like the wall.

## Implementation Considerations

In IFC, containment is encoded via `IfcRelContainedInSpatialStructure` (tree edge), and connectivity via `IfcRelConnectsElements` (graph edge). Both coexist.

## Related Concepts

- [[Why Buildings Are Not Purely Trees]]
- [[Combining Trees Graphs and Geometry]]
- [[Building Hierarchies]]
- [[BIM Hierarchies]]
- [[IFC Entity Relationships]]
