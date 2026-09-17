---
tags: [exercise, verification, formal]
---

# Exercise — Formal Verification on a Wall

## Problem

Formally verify that a wall $W$ in a BIM model satisfies the property:

> "The wall is vertical: its height direction is parallel to the Z axis within 1° tolerance."

## Required Background

- Formal verification: see [[Formal Verification]].
- The wall's geometry is a box. The "height direction" is the axis along which the box is longest in the Z dimension.

## Correct Answers

### Step 1: Formalize the Property

Let $W$ have placement $P = (R, t)$ where $R$ is the rotation matrix and $t$ is the translation.

Let the wall's local geometry be a box with axes aligned to the local $x, y, z$.

The wall's local $z$ axis (its height direction) is, in world frame:

$$\hat z_{\text{world}} = R \cdot (0, 0, 1)^T$$

The property to verify:

$$\arccos(\hat z_{\text{world}} \cdot (0, 0, 1)^T) \leq 1^\circ$$

i.e. the angle between the wall's height direction and the world Z axis is ≤ 1°.

### Step 2: Encode as a Formal Property

In an SMT solver (e.g. Z3 with floating-point theory):

```
; Define R as a 3x3 rotation matrix
; Define z_world = R * (0, 0, 1)
; Assert: angle(z_world, (0,0,1)) <= 1 degree
; Equivalently: z_world . (0,0,1) >= cos(1 degree)
```

### Step 3: Provide the Model

Encode the wall's placement (R, t) as constants in the solver.

### Step 4: Check

Ask the solver: is the property satisfied?

- If YES: emit a proof certificate.
- If NO: emit a counter-example (the actual angle).

### Step 5: Result

For a wall with $R = I$ (identity rotation), $\hat z_{\text{world}} = (0, 0, 1)$, and the angle is 0° ≤ 1°. Property holds.

For a wall rotated by 5° around the X axis, $\hat z_{\text{world}} = (0, \sin 5^\circ, \cos 5^\circ)$, and the angle is 5° > 1°. Property fails.

## Common Mistakes

- Confusing the wall's local axes with world axes.
- Forgetting to apply the placement rotation.
- Using degrees vs radians incorrectly.

## Edge Cases

- A wall that is intentionally tilted (e.g. a retaining wall) may legitimately fail this property. Use a different property or relax the tolerance.
- A curved wall has no single "height direction"; use a different property.

## Implementation Considerations

For a single wall, formal verification is overkill — a simple geometric check suffices. Formal verification is valuable when:

- The property is complex (involves multiple elements).
- You need a proof certificate (for regulatory compliance).
- You want to verify properties of a generated model at scale.

## Related Concepts

- [[Formal Verification]]
- [[Geometric Validation]]
- [[Alignment]]
- [[Constraint Solvers]]
- [[Verifiable Generation]]
