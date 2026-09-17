---
tags: [3d, depth, back-projection]
---

# Back-Projection

> **Definition.** *Back-projection* converts a depth map + camera parameters into a 3D point cloud.

## Formula

For a pixel $(u, v)$ with depth $Z$:

$$X = \frac{(u - c_x) Z}{f_x}, \quad Y = \frac{(v - c_y) Z}{f_y}, \quad Z = Z$$

where $f_x, f_y, c_x, c_y$ are the camera intrinsics.

Equivalently:

$$p = Z \cdot K^{-1} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}$$

## Pipeline

```
RGB image
  +
Depth map
  +
Camera intrinsics K
  +
Camera extrinsics [R | t]
        ↓
3D point cloud (in world frame)
```

Steps:

1. Back-project depth to 3D points in camera frame using $K^{-1}$.
2. Transform to world frame using $[R | t]$.

## Use Cases

- RGB-D scanning.
- Multi-view reconstruction.
- Image-to-3D pipelines.

See [[Image + Depth-to-3D]], [[3D Reconstruction]].

## Related Concepts

- [[Image + Depth-to-3D]]
- [[3D Reconstruction]]
- [[Camera Models]]
- [[Monocular Depth]]
