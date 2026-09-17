---
tags: [building, hierarchy]
---

# Building Hierarchy (in Building Rep)

See [[Building Hierarchies]] for the canonical note.

## Quick Recap

```
Site
    - Building
        - Storey
            - Space (room)
                - Element (wall, slab, column)
                    - Component (window, door)
                        - Sub-component (frame, glass)
```

Each level is a layer of abstraction. Buildings are simultaneously:

- a tree (containment),
- a graph (adjacency, connectivity, support),
- a collection of geometry.

See [[Building Hierarchies]], [[BIM Hierarchies]], [[Why Buildings Are Not Purely Trees]].

## Related Concepts

- [[Building Hierarchies]]
- [[BIM Hierarchies]]
- [[Why Buildings Are Not Purely Trees]]
- [[Combining Trees Graphs and Geometry]]
