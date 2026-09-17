---
tags: [discovery, abstraction]
---

# Component Abstraction

> **Definition.** Replace instances of a recurring pattern with a single abstract component (a "type" or "class"), simplifying the representation.

## Example

Before abstraction:

```
Floor 1
  - Window A (0.9 × 1.2 m, wood frame)
  - Window B (0.9 × 1.2 m, wood frame)
  - Window C (0.9 × 1.2 m, wood frame)
  - Window D (0.9 × 1.2 m, wood frame)
```

After abstraction:

```
Type: "Window_0.9x1.2_wood"
    - dimensions: 0.9 × 1.2 m
    - material: wood frame

Floor 1
  - Window A : Window_0.9x1.2_wood
  - Window B : Window_0.9x1.2_wood
  - Window C : Window_0.9x1.2_wood
  - Window D : Window_0.9x1.2_wood
```

## Why It Matters

- Reduces redundancy.
- Enables type-level reasoning (if I change the type, all instances update).
- Matches BIM's type vs occurrence distinction. See [[Type vs Occurrence]].

## In Discovery

After discovering a recurring pattern:

1. Define a new component type.
2. Replace each instance with a reference to the type.
3. The representation is now simpler (fewer unique entities).

This is the "create component → replace instances" step of [[Recursive Component Discovery]].

## Related Concepts

- [[Recursive Component Discovery]]
- [[Type vs Occurrence]]
- [[Minimum Description Length]]
