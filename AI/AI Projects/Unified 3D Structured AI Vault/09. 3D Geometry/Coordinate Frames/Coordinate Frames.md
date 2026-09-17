---
tags: [3d, coordinates, frames]
---

# Coordinate Frames

> A *coordinate frame* defines a reference for measuring positions and orientations in 3D space.

## Hierarchy of Frames

A typical building scene has multiple nested frames:

```
World frame
    - Building frame
        - Storey frame
            - Room frame
                - Wall frame
                    - Window frame
                        - Glass frame
```

Each frame has a transformation relative to its parent. Composing transformations gives world coordinates.

## Transformations Between Frames

If frame $B$ is described in frame $A$ by translation $t_{AB}$ and rotation $R_{AB}$, then a point $p^B$ in frame $B$ becomes in frame $A$:

$$p^A = R_{AB} p^B + t_{AB}$$

In homogeneous coordinates:

$$\begin{bmatrix} p^A \\ 1 \end{bmatrix} = \begin{bmatrix} R_{AB} & t_{AB} \\ 0 & 1 \end{bmatrix} \begin{bmatrix} p^B \\ 1 \end{bmatrix}$$

## Building Frame Convention

In BIM and architecture, common conventions:

- $+Z$ = up,
- $+X$ = east,
- $+Y$ = north,
- Origin = building reference point (often a corner).

IFC uses a right-handed convention with these axes.

## Camera Frame

In computer vision:

- Origin = camera center,
- $+Z$ = forward (looking direction),
- $+X$ = right,
- $+Y$ = down.

(NB: Some libraries use $-Z$ forward; check conventions.)

## Why This Matters

- All geometric operations assume a frame. Mixing frames silently produces wrong results.
- BIM uses building frame; point clouds use scanner frame; images use camera frame. Aligning them requires calibration.
- See [[Registration]].

## Related Concepts

- [[3D Geometry]]
- [[Transformations]]
- [[Camera Models]]
- [[Registration]]
