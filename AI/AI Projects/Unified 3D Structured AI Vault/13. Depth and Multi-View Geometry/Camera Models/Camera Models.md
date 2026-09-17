---
tags: [3d, vision, camera]
---

# Camera Models

> A *camera model* describes how 3D points project onto a 2D image.

## Pinhole Camera

A 3D point $p = (X, Y, Z)$ in camera frame projects to image point $(u, v)$:

$$u = f_x \frac{X}{Z} + c_x, \quad v = f_y \frac{Y}{Z} + c_y$$

In matrix form:

$$\begin{bmatrix} u \\ v \\ 1 \end{bmatrix} \sim K \begin{bmatrix} R & t \end{bmatrix} \begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}$$

where $K$ is the **intrinsics** matrix:

$$K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$

and $[R | t]$ is the **extrinsics** (camera-to-world rotation and translation).

## Intrinsics

- $f_x, f_y$: focal lengths in pixels.
- $c_x, c_y$: principal point (image center).

## Extrinsics

- $R$: 3D rotation (camera orientation).
- $t$: 3D translation (camera position).

Together: 6 DOF (3 rotation + 3 translation).

## Distortion

Real lenses introduce distortion (radial, tangential). Corrected before projection:

$$p_{\text{corrected}} = \text{undistort}(p_{\text{image}}, \text{distortion coeffs})$$

## Depth

The depth $Z$ of a point is its distance along the camera's optical axis. A depth map stores $Z$ per pixel.

See [[Monocular Depth]], [[Stereo Depth]], [[Multi-View Stereo]], [[Back-Projection]].

## Related Concepts

- [[Camera Models]]
- [[Monocular Depth]]
- [[Stereo Depth]]
- [[Back Projection]]
