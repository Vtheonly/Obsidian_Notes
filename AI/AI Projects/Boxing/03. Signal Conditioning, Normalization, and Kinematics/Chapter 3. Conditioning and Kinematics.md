---
title: Chapter 3 — Signal Conditioning, Normalization, and Kinematics
tags: [boxing, ai, signal-processing, filtering, kinematics, normalization]
---

# Chapter 3: Signal Conditioning, Normalization, and Kinematics

## 3.1 Pose Noise and Temporal Artifacts

Common pose-stream problems:

- high-frequency coordinate jitter
- confidence fluctuations
- temporary joint loss
- left/right identity confusion
- derivative spikes
- occlusion during hooks and cross-body movements

The required processing chain is:

raw keypoints
→ confidence-aware conditioning
→ body-relative normalization
→ kinematic features
→ temporal modeling

## 3.2 The One Euro Filter

### 3.2.1 Mathematical Formulation

For sample interval dt, estimate derivative:

dx = (x_i - x_filtered_previous) / dt

Smooth the derivative with a low-pass filter:

alpha_d = 1 / (1 + 1 / (2 pi f_d dt))

dx_filtered = alpha_d dx + (1 - alpha_d) dx_filtered_previous

Make cutoff responsive to movement:

f_c = f_min + beta |dx_filtered|

Then:

alpha = 1 / (1 + 1 / (2 pi f_c dt))

x_filtered = alpha x + (1 - alpha) x_filtered_previous

The design principle is:

- low motion → more smoothing
- high motion → less smoothing
- no fixed large delay during fast punches

## 3.3 Body-Centric Coordinate Invariance

### 3.3.1 Translation, Rotation, and Scale

Define the root as the hip midpoint:

p_root = (p_left_hip + p_right_hip) / 2

Translate:

p'_k = p_k - p_root

Estimate torso orientation and rotate the skeleton into a canonical frame.

Normalize scale with shoulder width:

L_shoulder = ||p_left_shoulder - p_right_shoulder||

p*_k = p''_k / L_shoulder

The resulting representation is less sensitive to camera distance, subject position, and camera tilt.

## 3.4 Kinematic Feature Derivations

Useful derived features:

- elbow angle
- knee angle
- torso inclination
- shoulder rotation
- pelvis rotation
- wrist velocity
- wrist acceleration
- angular velocity
- hand-to-chin distance
- stance width
- foot displacement
- shoulder/pelvis phase difference
- recovery duration

Elbow angle:

theta_elbow = arccos(((wrist - elbow) dot (shoulder - elbow)) /
                     (||wrist - elbow|| ||shoulder - elbow||))

Guard distance:

d_guard = ||rear_wrist - chin||

Kinematic features should complement learned representations rather than replace them.

## 3.5 Real-Time vs Review Analysis

Live mode should use causal derivatives because future frames are unavailable.

Post-repetition review can use the complete buffered motion and non-causal central differences.

| Mode | Primary objective | Derivative strategy |
|---|---|---|
| Live | Low latency | Causal/backward |
| Review | Maximum analytical quality | Buffered central |

## Core Connections

- [[01. Mathematical and Theoretical Foundations/Chapter 1. Foundations]]
- [[04. Spatial-Temporal Deep Learning Architectures/Chapter 4. Spatial-Temporal Deep Learning]]
- [[05. Biomechanical Modeling and Sequence Comparison/Chapter 5. Biomechanical Modeling]]
