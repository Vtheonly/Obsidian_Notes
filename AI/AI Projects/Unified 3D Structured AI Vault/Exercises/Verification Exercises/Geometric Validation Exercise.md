---
tags: [exercise, verification, geometric]
---

# Exercise — Geometric Validation

## Problem

You are given a wall with the following geometry:

- A box from $(0, 0, 0)$ to $(5, 0.2, 3)$ (length 5 m, thickness 0.2 m, height 3 m).
- A window opening from $(1, -0.1, 1)$ to $(2, 0.3, 2)$ (width 1 m, depth 0.4 m, height 1 m).

(a) Is the wall watertight (if we consider the opening as a void)?
(b) Is the window opening fully contained in the wall?
(c) Is the wall vertical?
(d) What other geometric checks would you run?

## Required Background

- Geometric validation: see [[Geometric Validation]].
- Containment: see [[Containment]].
- Watertightness: see [[Meshes]].

## Correct Answers

### (a) Watertight

If the opening is properly cut from the wall (the wall's mesh has a hole where the opening is, and the opening is filled with a window frame + glass), then the combined mesh (wall + window) is watertight.

If the opening is just a void (no window fills it), then the wall alone has a hole and is NOT watertight.

For a valid BIM model, the opening should be filled by a window (via `IfcRelFillsElement`), making the combined mesh watertight.

### (b) Window Opening Containment

The window opening goes from $x=1$ to $x=2$, $y=-0.1$ to $y=0.3$, $z=1$ to $z=2$.

The wall goes from $x=0$ to $x=5$, $y=0$ to $y=0.2$, $z=0$ to $z=3$.

Check:
- $x$: opening $[1, 2]$ is inside wall $[0, 5]$. ✓
- $y$: opening $[-0.1, 0.3]$ is NOT inside wall $[0, 0.2]$. The opening extends beyond the wall on both sides (by 0.1 m each).

This is a problem: the opening should be inside the wall. The opening's $y$ range should be $[0, 0.2]$ (or slightly less, to leave a frame).

### (c) Wall Vertical

The wall's geometry is a box from $(0, 0, 0)$ to $(5, 0.2, 3)$. The vertical direction is $z$.

- The wall's height is along $z$ (from 0 to 3). ✓
- The wall's thickness is along $y$ (from 0 to 0.2).
- The wall's length is along $x$ (from 0 to 5).

The wall is vertical (its long dimensions $x, z$ are perpendicular to gravity, and its height is along $z$ which is up).

### (d) Other Geometric Checks

- Self-intersection (does the wall intersect itself? — no for a simple box).
- Manifoldness (is the mesh manifold? — yes for a simple box, but check after cutting the opening).
- Orientation (are normals consistent? — should point outward).
- Alignment with other walls (is this wall aligned with neighboring walls?).
- Connection to floor and ceiling (does the wall's bottom touch the floor slab? does its top touch the ceiling / slab above?).

## Common Mistakes

- Forgetting to check containment in all three dimensions.
- Confusing vertical (along z) with horizontal (along x or y).
- Forgetting that the opening must be filled by a window for the combined mesh to be watertight.

## Edge Cases

- A wall with multiple openings: each must be checked.
- A curved wall: containment checks are more complex.

## Implementation Considerations

Use a library like `trimesh` for geometric checks:

```python
import trimesh

wall = trimesh.creation.box((5, 0.2, 3))
print(wall.is_watertight)  # True
print(wall.euler_number)   # 2 (sphere topology)
```

## Related Concepts

- [[Geometric Validation]]
- [[Containment]]
- [[Meshes]]
- [[Alignment]]
- [[Spatial Validation]]
