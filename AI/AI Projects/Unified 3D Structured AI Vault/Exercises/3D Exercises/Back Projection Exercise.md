---
tags: [exercise, 3d, back-projection]
---

# Exercise — Back-Projection

## Problem

Given:

- A pixel at $(u, v) = (320, 240)$ in a $640 \times 480$ image.
- Camera intrinsics: $f_x = f_y = 500$, $c_x = 320$, $c_y = 240$.
- Depth at the pixel: $Z = 5$ m.

(a) Compute the 3D point in camera frame.
(b) If the camera is at world position $(1, 2, 3)$ with orientation $R = I$ (identity), compute the 3D point in world frame.

## Required Background

- The pinhole camera model: see [[Camera Models]].
- Back-projection formula: $X = (u - c_x) Z / f_x$, $Y = (v - c_y) Z / f_y$, $Z = Z$. See [[Back Projection]].
- Camera extrinsics: world point = $R \cdot \text{camera point} + t$.

## Correct Answers

### (a) 3D Point in Camera Frame

$$X = \frac{(u - c_x) Z}{f_x} = \frac{(320 - 320) \cdot 5}{500} = 0$$

$$Y = \frac{(v - c_y) Z}{f_y} = \frac{(240 - 240) \cdot 5}{500} = 0$$

$$Z = 5$$

So the 3D point in camera frame is $(0, 0, 5)$.

This makes sense: the pixel is exactly at the principal point, so the back-projected ray goes straight forward.

### (b) 3D Point in World Frame

With $R = I$ and $t = (1, 2, 3)$:

$$p_{\text{world}} = R \cdot p_{\text{camera}} + t = (0, 0, 5) + (1, 2, 3) = (1, 2, 8)$$

## Step-by-Step Reasoning

1. The principal point $(c_x, c_y) = (320, 240)$ is the image center.
2. The pixel $(320, 240)$ is exactly at the principal point.
3. By the pinhole model, a ray through the principal point is the camera's optical axis.
4. So the 3D point at depth 5 m along the optical axis is $(0, 0, 5)$ in camera frame.
5. With $R = I$ and $t = (1, 2, 3)$, the world point is the camera point translated by $(1, 2, 3)$: $(1, 2, 8)$.

## Common Mistakes

- Using $f_x$ for both $X$ and $Y$ (mixing $f_x$ and $f_y$).
- Forgetting to add the camera translation.
- Confusing camera-to-world vs world-to-camera direction.

## Edge Cases

- If the camera has non-identity rotation $R$, you must apply $R$ to the camera-frame point: $p_{\text{world}} = R p_{\text{camera}} + t$.
- If depth is missing or invalid, the pixel cannot be back-projected.

## Implementation Considerations

In code:

```python
import numpy as np

def back_project(u, v, Z, K, R, t):
    fx, fy = K[0, 0], K[1, 1]
    cx, cy = K[0, 2], K[1, 2]
    X = (u - cx) * Z / fx
    Y = (v - cy) * Z / fy
    p_cam = np.array([X, Y, Z])
    p_world = R @ p_cam + t
    return p_world
```

For a full depth map, vectorize over all pixels.

## Related Concepts

- [[Back Projection]]
- [[Camera Models]]
- [[Image Plus Depth to 3D]]
- [[Coordinate Frames]]
- [[Transformations]]
