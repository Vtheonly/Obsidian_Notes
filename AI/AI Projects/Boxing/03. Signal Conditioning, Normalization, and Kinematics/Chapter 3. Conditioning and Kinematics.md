---
title: Chapter 3 — Signal Conditioning, Normalization, and Kinematics
tags: [boxing, ai, signal-processing, filtering, normalization, kinematics]
---

# Chapter 3 — Signal Conditioning, Normalization, and Kinematics

## 3.1 Pose Noise and Temporal Artifacts

Keypoint streams contain:

- high-frequency pixel jitter
- independent frame-to-frame perturbations
- confidence fluctuations
- dynamic occlusion
- limb crossing
- temporary left/right identity confusion

These errors become much larger after differentiation because:

noise → velocity error → acceleration error → jerk error.

During a rear hook, for example, the punching hand may cross the torso and cause a confidence collapse or coordinate identity swap.

The motion engine should therefore retain:

(x, y, confidence, timestamp)

for each keypoint.

## 3.2 One Euro Filter

### 3.2.1 Mathematical Formulation

For an incoming coordinate x_i with elapsed time dt:

$$
\dot{x}_i
=
\frac{x_i-\hat{x}_{i-1}}{\Delta t}.
$$

Derivative smoothing coefficient:

$$
\alpha_d
=
\frac{1}
{1+\frac{1}{2\pi f_{c,d}\Delta t}}.
$$

Filtered derivative:

$$
\hat{\dot{x}}_i
=
\alpha_d\dot{x}_i
+
(1-\alpha_d)\hat{\dot{x}}_{i-1}.
$$

Dynamic cutoff:

$$
f_c
=
f_{c,min}
+
\beta|\hat{\dot{x}}_i|.
$$

Signal coefficient:

$$
\alpha
=
\frac{1}
{1+\frac{1}{2\pi f_c\Delta t}}.
$$

Filtered output:

$$
\hat{x}_i
=
\alpha x_i
+
(1-\alpha)\hat{x}_{i-1}.
$$

Reference Kotlin implementation:

```kotlin
class OneEuroFilter(
    private val minCutoff: Float = 1.0f,
    private val beta: Float = 0.007f,
    private val dCutoff: Float = 1.0f
) {
    private var xPrev = 0f
    private var dxPrev = 0f
    private var tPrev = -1L

    fun filter(x: Float, timestampMs: Long): Float {
        if (tPrev < 0L) {
            tPrev = timestampMs
            xPrev = x
            dxPrev = 0f
            return x
        }

        val dt = (timestampMs - tPrev) / 1000f
        if (dt <= 0f) return xPrev

        val dx = (x - xPrev) / dt
        val alphaD = calculateAlpha(dt, dCutoff)
        val dxHat = alphaD * dx + (1f - alphaD) * dxPrev

        val fc = minCutoff + beta * kotlin.math.abs(dxHat)
        val alpha = calculateAlpha(dt, fc)

        val xHat = alpha * x + (1f - alpha) * xPrev

        xPrev = xHat
        dxPrev = dxHat
        tPrev = timestampMs

        return xHat
    }

    private fun calculateAlpha(dt: Float, cutoff: Float): Float {
        val tau = 1.0f / (2f * Math.PI.toFloat() * cutoff)
        return 1.0f / (1.0f + tau / dt)
    }
}
```

The parameters are starting values, not universal constants. They need calibration against actual pose output and latency requirements.

## 3.3 Body-Centric Coordinate Invariance

### 3.3.1 Translation, Rotation, and Scale

Define hip root:

$$
p_{root}
=
\frac{p_{left\_hip}+p_{right\_hip}}{2}.
$$

Translation:

$$
p'_k=p_k-p_{root}.
$$

Torso vector:

$$
v_{torso}
=
\frac{
p_{left\_shoulder}+p_{right\_shoulder}
}{2}
-
p_{root}.
$$

Torso angle:

$$
\psi
=
\operatorname{atan2}
(v_{torso,x},v_{torso,y}).
$$

Rotate by -psi:

$$
p''_k
=
R(-\psi)p'_k.
$$

Scale by shoulder width:

$$
L_{shoulder}
=
\|p''_{left\_shoulder}
-
p''_{right\_shoulder}\|_2.
$$

$$
p^*_k
=
\frac{p''_k}{L_{shoulder}}.
$$

The resulting representation is far less sensitive to where the boxer stands in the image.

## 3.4 Kinematic Feature Derivations

Features include:

- joint positions
- joint angles
- angular velocity
- linear velocity
- acceleration
- torso orientation
- shoulder rotation
- pelvis rotation
- hand-to-chin distances
- stance width
- foot displacement
- shoulder/pelvis torsional differential
- recovery duration

Elbow angle:

$$
\theta_{elbow}
=
\arccos
\left(
\frac{
(p_{wrist}-p_{elbow})^T
(p_{shoulder}-p_{elbow})
}{
\|p_{wrist}-p_{elbow}\|_2
\|p_{shoulder}-p_{elbow}\|_2
}
\right).
$$

Projected pelvis angle:

$$
\phi_{pelvis}
=
\operatorname{atan2}
(y^*_{Rhip}-y^*_{Lhip},
x^*_{Rhip}-x^*_{Lhip}).
$$

Projected shoulder angle:

$$
\phi_{shoulders}
=
\operatorname{atan2}
(y^*_{Rshoulder}-y^*_{Lshoulder},
x^*_{Rshoulder}-x^*_{Lshoulder}).
$$

Torsional differential:

$$
\Delta\phi_{kinetic}
=
\phi_{shoulders}
-
\phi_{pelvis}.
$$

Guard distance:

$$
d_{guard}
=
\|p^*_{rear\_wrist}-p^*_{chin}\|_2.
$$

Feature vector:

$$
f(t)
=
[
p^*(t),
v(t),
a(t),
angles(t),
rotations(t),
distances(t)
].
$$

## 3.5 Real-Time and Review Derivatives

Live inference uses causal approximations:

$$
v[t]
\approx
\frac{p[t]-p[t-1]}{\Delta t}.
$$

Review mode can use:

$$
v[t]
\approx
\frac{p[t+1]-p[t-1]}{2\Delta t}
$$

and equivalent higher-order central differences.

The distinction exists because live inference cannot see future frames while post-session analysis can.

## Core Connections

- [[01. Mathematical and Theoretical Foundations/Chapter 1. Foundations]]
- [[04. Spatial-Temporal Deep Learning Architectures/Chapter 4. Spatial-Temporal Deep Learning]]
- [[05. Biomechanical Modeling and Sequence Comparison/Chapter 5. Biomechanical Modeling]]
