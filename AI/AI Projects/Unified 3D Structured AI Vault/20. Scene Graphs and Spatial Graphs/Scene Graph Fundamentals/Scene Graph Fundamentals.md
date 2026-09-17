---
tags: [scene-graph, fundamentals]
---

# Scene Graph Fundamentals

> **Definition.** A *scene graph* is a directed graph where nodes are objects (with attributes) and edges are typed relations between objects.

## Structure

```
Nodes: {object_1: {type: "chair", pos: (1,2,3), ...},
        object_2: {type: "table", pos: (1.5,2,3), ...},
        ...}

Edges: {(object_1, "on", object_2),
        (object_3, "next-to", object_2),
        ...}
```

## Common Relations

- **Spatial**: `on`, `next-to`, `above`, `below`, `inside`, `around`.
- **Support**: `supported-by`, `supports`.
- **Possession**: `has`, `part-of`.
- **Semantic**: `used-for`, `made-of`.

## Why It Matters

- **Compact**: a few hundred nodes/edges replace millions of pixels.
- **Editable**: change a node's attribute; geometry / appearance updates.
- **Queryable**: "find all chairs next to a table".
- **Generatable**: predict nodes and edges from images or text.

## Scene Graph + Hierarchy

A scene graph can be augmented with a **hierarchy** (groups, regions). Then it's both a graph (relations) and a tree (containment).

See [[Hierarchical Scene Representations]], [[Spatial Graph Construction]].

## In Buildings

A building scene graph:

- Nodes: walls, doors, windows, slabs, columns, beams, furniture, spaces.
- Edges: `adjacent-to`, `connects`, `supports`, `contains`, `part-of`.

This is essentially a BIM model without the parametric geometry. See [[BIM Fundamentals]].

## In AI

- **Scene graph generation**: image → scene graph. See [[Scene Graph Generation]].
- **Scene graph to image**: scene graph → image (image synthesis).
- **Scene graph to 3D**: scene graph → 3D scene.
- **Scene graph to BIM**: scene graph → IFC.

See [[Scene Graph Generation]], [[Spatial Graph Construction]].

## Related Concepts

- [[Scene Graph Generation]]
- [[Spatial Graph Construction]]
- [[Hierarchical Scene Representations]]
- [[Why Buildings Are Not Purely Trees]]
- [[BIM Fundamentals]]
