---
tags: [3d, transformations]
---

# Transformations

> Geometric transformations map points to points: translation, rotation, scaling, shear, and their compositions.

## Rigid Transform (SE(3))

Preserves distances and angles:

$$T = \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix}, \quad R \in SO(3), \; t \in \mathbb{R}^3$$

where $R$ is a rotation matrix ($R^T R = I$, $\det R = 1$) and $t$ is a translation.

## Similarity Transform (Sim(3))

Preserves angles, scales distances:

$$T = \begin{bmatrix} sR & t \\ 0 & 1 \end{bmatrix}, \quad s > 0$$

## Affine Transform

Preserves parallelism:

$$T = \begin{bmatrix} A & t \\ 0 & 1 \end{bmatrix}, \quad A \in \mathbb{R}^{3 \times 3}$$

## Projective Transform

Preserves straight lines:

$$T = \begin{bmatrix} A & t \\ a^T & b \end{bmatrix}$$

(Any non-singular $4 \times 4$ matrix.)

## Rotation Representations

| Representation         | Parameters         | Singularity      |
| ---------------------- | ------------------ | ---------------- |
| Rotation matrix        | 9                  | None (but redundant) |
| Euler angles           | 3                  | Gimbal lock      |
| Axis-angle             | 4 (3 axis + 1 angle)| None             |
| Quaternion             | 4                  | Double cover     |
| Twist / log map        | 3 (in $\mathfrak{so}(3)$) | None at identity |

## Composition

Composing two rigid transforms:

$$T_1 \cdot T_2 = \begin{bmatrix} R_1 R_2 & R_1 t_2 + t_1 \\ 0 & 1 \end{bmatrix}$$

Inverse:

$$T^{-1} = \begin{bmatrix} R^T & -R^T t \\ 0 & 1 \end{bmatrix}$$

## In AI

- Camera extrinsics are rigid transforms (camera-to-world).
- Object poses are rigid transforms (object-to-world).
- Building element placements are rigid transforms (element-to-storey).
- IFC stores placement as `IfcLocalPlacement` with `RelativePlacement` (a 3D transform).

See [[Coordinate Frames]], [[Camera Models]], [[Registration]].

## Related Concepts

- [[3D Geometry]]
- [[Coordinate Frames]]
- [[Camera Models]]
- [[Registration]]
