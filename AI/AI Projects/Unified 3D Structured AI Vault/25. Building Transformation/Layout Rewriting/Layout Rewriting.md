---
tags: [building, transformation, layout]
---

# Layout Rewriting

> Modify a building's layout: move walls, resize rooms, add/remove rooms, change furniture.

## Operations

- **Move wall**: shift a wall; adjacent rooms resize.
- **Resize room**: change a room's dimensions; geometry updates.
- **Add room**: split a larger room into two.
- **Remove room**: merge two rooms into one.
- **Add/remove furniture**.

## Constraints

- **Containment**: rooms stay inside their storey.
- **Adjacency**: room boundaries still share walls.
- **Topology**: doors still connect two rooms; no isolated rooms.
- **Code**: corridor widths, travel distances still satisfy code.

## In AI

Layout rewriting is a structured editing task:

- Input: building + edit instruction ("make the kitchen larger").
- Output: revised building.

A structure-aware editor must propagate the edit through:

- the tree (containment),
- the graph (adjacency),
- the geometry,
- the properties (areas, volumes).

See [[Cross Representation Consistency]], [[Building Transformation]].

## Related Concepts

- [[Building Transformation]]
- [[Structure Preserving Edits]]
- [[Cross Representation Consistency]]
