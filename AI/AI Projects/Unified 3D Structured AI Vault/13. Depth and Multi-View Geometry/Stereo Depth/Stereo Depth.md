---
tags: [3d, depth, stereo]
---

# Stereo Depth

> **Definition.** Estimate depth from two images taken from horizontally offset cameras.

## Principle

A 3D point $p$ projects to $(u_L, v_L)$ in the left image and $(u_R, v_R)$ in the right image. The **disparity** is:

$$d = u_L - u_R$$

The depth is:

$$Z = \frac{f \cdot b}{d}$$

where $f$ is the focal length and $b$ is the baseline (distance between cameras).

## Stereo Matching

For each pixel in the left image, find the matching pixel in the right image (along the epipolar line). The disparity gives the depth.

## Algorithms

- **Block matching**: compare windows.
- **SGM** (Semi-Global Matching): dynamic programming along multiple directions.
- **PSMNet**: deep stereo matching with 3D convolutions.
- **CRE-Stereo**: recurrent stereo.

## Output

- A disparity map (and hence a depth map, given calibration).

## Limitations

- Requires calibrated stereo rig (intrinsics + extrinsics).
- Fails in textureless regions.
- Fails at occlusions (points visible in one image only).

See [[Monocular Depth]], [[Multi-View Stereo]].

## Related Concepts

- [[Monocular Depth]]
- [[Multi-View Stereo]]
- [[Camera Models]]
- [[Consistency]]
