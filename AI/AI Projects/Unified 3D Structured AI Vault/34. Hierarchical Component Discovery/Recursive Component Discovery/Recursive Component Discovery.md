---
tags: [discovery, recursive, components]
---

# Recursive Component Discovery

> **Definition.** Discover components at multiple levels of abstraction, where each level operates on the output of the previous.

## Pipeline

```
Raw representation
  ↓
Discover recurring patterns at level 1 (e.g. recurring element groups)
  ↓
Create components from these patterns
  ↓
Replace instances with component references
  ↓
Simplified representation (with components)
  ↓
Discover larger recurring patterns at level 2
  ↓
Create higher-level components
  ↓
Repeat
```

## Example

```
Primitive geometry (point cloud)
  ↓
Discover recurring objects (chairs, tables)
  ↓
Discover recurring subassemblies (kitchen, bathroom)
  ↓
Discover recurring architectural modules (typical apartment)
  ↓
Discover recurring building structures (typical floor)
```

Each level abstracts the previous. The result is a hierarchy of discovered components.

## Why It's Powerful

- Discovers structure at multiple scales.
- Each level simplifies the representation.
- Naturally produces a hierarchy.
- Components become new "atoms" for the next level.

## Connections

- **Hierarchical clustering**: similar idea, but on feature vectors.
- **Grammar induction**: discover production rules at multiple levels.
- **Program synthesis**: discover subroutines (which are components).
- **Tree induction**: grow a tree by recursively splitting.
- **MDL**: each level should reduce total description length.

See [[Hierarchical Clustering]], [[Grammar Induction]], [[Program Induction]], [[Minimum Description Length]], [[Tree Induction]].

## Challenges

- When to stop? (No more compression.)
- How to handle overlap? (Two components share a sub-component.)
- How to handle approximate matches?

## Related Concepts

- [[Hierarchical Clustering]]
- [[Grammar Induction]]
- [[Program Induction]]
- [[Minimum Description Length]]
- [[Tree Induction]]
- [[Component Abstraction]]
