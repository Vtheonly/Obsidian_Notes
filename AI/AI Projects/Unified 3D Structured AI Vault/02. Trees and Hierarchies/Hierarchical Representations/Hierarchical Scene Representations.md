---
tags: [trees, scene, hierarchy]
---

# Hierarchical Scene Representations

> A **hierarchical scene representation** organizes a scene into multiple levels of abstraction, typically: primitives → objects → groups → regions → scene.

## Levels

| Level     | Example                                  |
| --------- | ---------------------------------------- |
| Primitive | A point, polygon, voxel, SDF sample.     |
| Object    | A chair, a table, a wall.                |
| Group     | A dining set (table + chairs).           |
| Region    | A room (floor + walls + furniture).      |
| Scene     | A building, a floor, a city block.       |

## Why Hierarchy Matters

- **Attention**: a model can attend to objects, not pixels.
- **Generation**: a model can generate coarse-to-fine (room first, then furniture).
- **Reasoning**: a model can ask "is this chair inside this room?" without re-checking pixels.
- **Editing**: a user can move a room and all its contents move together.

## How It Is Built

- Bottom-up: cluster primitives into objects, objects into groups, etc.
- Top-down: predict the scene tree first, then refine each node.
- Hybrid: detect objects bottom-up, predict relations top-down.

See [[Scene Graph Fundamentals]], [[Recursive Component Discovery]], [[Hierarchical Clustering]].

## Related Concepts

- [[Building Hierarchies]]
- [[Scene Graph Fundamentals]]
- [[Recursive Component Discovery]]
- [[Hierarchical Clustering]]
