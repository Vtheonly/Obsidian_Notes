---
tags: [spatial, topology, adjacency, containment]
---

# Adjacency and Containment

> The two most important spatial relations in buildings: **adjacency** (sharing a boundary) and **containment** (one inside another).

## Adjacency

Two regions $A, B$ are **adjacent** if their boundaries share a non-trivial intersection:

$$\partial A \cap \partial B \neq \emptyset, \quad A^\circ \cap B^\circ = \emptyset$$

In buildings:

- Two rooms are adjacent if they share a wall.
- Two walls are adjacent if they share a corner.
- A wall and a slab are adjacent if they touch.

## Containment

Region $A$ **contains** region $B$ if:

$$B \subseteq A$$

In buildings:

- A storey contains its rooms.
- A room contains its furniture.
- A wall contains its windows and doors.

## Directional Adjacency

Adjacency with a direction:

- $A$ is **north of** $B$.
- $A$ is **above** $B$.

Useful for orientation-aware reasoning.

## Graph Representation

Build a graph:

- Nodes: objects (rooms, walls, etc.).
- Edges: typed relations (`adjacent`, `contains`, `supports`, `connects`).

See [[Scene Graph Fundamentals]], [[Why Buildings Are Not Purely Trees]].

## Validation

- **Containment closure**: if $A \supseteq B$ and $B \supseteq C$, then $A \supseteq C$.
- **Adjacency symmetry**: if $A$ is adjacent to $B$, then $B$ is adjacent to $A$.
- **Wall two-sidedness**: an interior wall is adjacent to exactly two rooms.

See [[Topological Validation]], [[Spatial Validation]].

## Related Concepts

- [[Spatial Relations]]
- [[Topological Relations]]
- [[Scene Graph Fundamentals]]
- [[Why Buildings Are Not Purely Trees]]
