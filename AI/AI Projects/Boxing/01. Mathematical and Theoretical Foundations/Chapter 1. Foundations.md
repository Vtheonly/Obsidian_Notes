---
title: Chapter 1 — Mathematical and Theoretical Foundations
tags: [boxing, ai, mathematics, linear-algebra, optimization, probability, signal-processing]
---

# Chapter 1: Mathematical and Theoretical Foundations

This chapter supplies the mathematical language used by every later stage of the boxing coach.

## 1.1 Linear Algebra for Pose Geometry

### 1.1.1 Vectors, Norms, and Metric Spaces in R² and R³

A tracked anatomical landmark is represented as a spatial vector:

$$
\mathbf{p}_i(t)=
\begin{bmatrix}
x_i(t)\\
y_i(t)
\end{bmatrix}
\in\mathbb{R}^2
$$

or, where depth is available,

$$
\mathbf{P}_i(t)=
\begin{bmatrix}
X_i(t)\\
Y_i(t)\\
Z_i(t)
\end{bmatrix}
\in\mathbb{R}^3.
$$

A full 2D skeleton with $K$ joints can be unrolled into:

$$
\mathbf{x}(t)=
[x_1,y_1,x_2,y_2,\ldots,x_K,y_K]^T
\in\mathbb{R}^{2K}.
$$

For two landmarks:

$$
\mathbf{d}_{ij}=\mathbf{p}_j-\mathbf{p}_i.
$$

Relevant norms are:

$$
\|\mathbf{d}\|_1=|d_x|+|d_y|,
$$

$$
\|\mathbf{d}\|_2=\sqrt{d_x^2+d_y^2},
$$

$$
\|\mathbf{d}\|_\infty=\max(|d_x|,|d_y|).
$$

The Euclidean norm is the main geometric metric for limb lengths, clearances, and trajectory deviations.

For joint angles, use two limb vectors:

$$
\theta=
\arccos
\left(
\frac{\mathbf{u}^T\mathbf{v}}
{\|\mathbf{u}\|_2\|\mathbf{v}\|_2}
\right).
$$

For a signed two-dimensional angle, use:

$$
\theta_{signed}=\operatorname{atan2}
(u_xv_y-u_yv_x,\,
u_xv_x+u_yv_y).
$$

This is the basis for elbow articulation, knee flexion, torso tilt, and other boxing kinematics.

### 1.1.2 Affine Transformations and Body-Centric Change of Basis

Raw image coordinates depend on camera translation, distance, scale, and orientation. The coaching engine therefore transforms the skeleton into a canonical body-relative frame.

General affine transform:

$$
\mathbf{p}'=\mathbf{A}\mathbf{p}+\mathbf{t}.
$$

Using homogeneous coordinates:

$$
\tilde{\mathbf{p}}=
[x,y,1]^T
$$

and

$$
\mathbf{M}=
\begin{bmatrix}
a_{11}&a_{12}&t_x\\
a_{21}&a_{22}&t_y\\
0&0&1
\end{bmatrix}.
$$

Elementary transforms include translation:

$$
\mathbf{T}=
\begin{bmatrix}
1&0&t_x\\
0&1&t_y\\
0&0&1
\end{bmatrix},
$$

isotropic scale:

$$
\mathbf{S}=
\begin{bmatrix}
s&0&0\\
0&s&0\\
0&0&1
\end{bmatrix},
$$

and planar rotation:

$$
\mathbf{R}(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta&0\\
\sin\theta&\cos\theta&0\\
0&0&1
\end{bmatrix}.
$$

A body-relative normalization can be built as:

$$
\mathbf{M}_{norm}
=
\mathbf{S}(s)
\mathbf{R}(-\phi)
\mathbf{T}(-c_x,-c_y).
$$

This makes downstream analysis more sensitive to movement mechanics and less sensitive to where the athlete is standing in the camera view.

### 1.1.3 SVD and PCA for Motion Signals

For a temporal sequence:

$$
\mathbf{X}\in\mathbb{R}^{T\times2K}
$$

subtract the temporal mean and compute covariance:

$$
\boldsymbol\Sigma=
\frac{1}{T-1}\tilde{\mathbf{X}}^T\tilde{\mathbf{X}}.
$$

SVD gives:

$$
\tilde{\mathbf{X}}
=
\mathbf{U}
\boldsymbol\Sigma_{svd}
\mathbf{V}^T.
$$

A low-rank representation is:

$$
\mathbf{Z}_r=\tilde{\mathbf{X}}\mathbf{V}_r.
$$

Reconstruction:

$$
\hat{\mathbf{X}}
=
\mathbf{Z}_r\mathbf{V}_r^T+
\mathbf{1}_T\boldsymbol\mu^T.
$$

The same projection can support anomaly analysis:

$$
\epsilon_{anomaly}(t)
=
\|
\tilde{\mathbf{x}}(t)
-
\mathbf{V}_r\mathbf{V}_r^T
\tilde{\mathbf{x}}(t)
\|_2^2.
$$

For this project, PCA/SVD is best treated as an analysis, compression, and exploratory tool rather than a hard assumption that a fixed six-dimensional representation will always capture a jab.

## 1.2 Multivariate Calculus and Optimization

### 1.2.1 Gradient Descent and Backpropagation

The learned components minimize an objective such as:

$$
\theta^*
=
\arg\min_\theta
\left[
\frac1N
\sum_i
\ell(f(x^{(i)};\theta),y^{(i)})
+
\lambda\Omega(\theta)
\right].
$$

Gradient descent:

$$
\theta_{t+1}
=
\theta_t-
\eta\nabla_\theta\mathcal{L}(\theta_t).
$$

For Adam/AdamW:

$$
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t
$$

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2
$$

with bias correction:

$$
\hat m_t=\frac{m_t}{1-\beta_1^t},
\quad
\hat v_t=\frac{v_t}{1-\beta_2^t}.
$$

The backpropagation recursion for a feed-forward layer is:

$$
\delta^{(L)}
=
\nabla_{a^{(L)}}\ell
\odot
\sigma'(z^{(L)})
$$

and

$$
\delta^{(l)}
=
((W^{(l+1)})^T\delta^{(l+1)})
\odot
\sigma'(z^{(l)}).
$$

These concepts matter when fine-tuning the boxing pose front-end and training the temporal motion models.

### 1.2.2 Kinematic Derivatives

For a tracked point $p(t)$:

$$
v(t)=\frac{dp(t)}{dt},
\qquad
a(t)=\frac{d^2p(t)}{dt^2},
\qquad
j(t)=\frac{d^3p(t)}{dt^3}.
$$

At discrete frame spacing $\Delta t$:

Forward difference:

$$
v[t]\approx\frac{p[t+1]-p[t]}{\Delta t}.
$$

Backward difference:

$$
v[t]\approx\frac{p[t]-p[t-1]}{\Delta t}.
$$

Central difference:

$$
v[t]\approx
\frac{p[t+1]-p[t-1]}{2\Delta t}.
$$

Second derivative:

$$
a[t]\approx
\frac{p[t+1]-2p[t]+p[t-1]}{\Delta t^2}.
$$

Third derivative:

$$
j[t]\approx
\frac{p[t+2]-2p[t+1]+2p[t-1]-p[t-2]}
{2\Delta t^3}.
$$

Real-time processing favors causal/backward approximations; post-repetition analysis can use buffered non-causal central differences.

## 1.3 Probability, Information Theory, and Confidence Modeling

### 1.3.1 Heatmaps and Coordinate Distributions

A keypoint target may be represented with a spatial Gaussian:

$$
p(u,v|g_k)
=
\frac{1}{2\pi\sigma^2}
\exp
\left(
-\frac{\|(u,v)-g_k\|_2^2}{2\sigma^2}
\right).
$$

Typical decoding paradigms include:

- Argmax
- Soft-argmax / integral regression
- SimCC's independent 1D coordinate classification

SimCC predicts:

$$
p_x\in\mathbb{R}^{N_x},
\qquad
p_y\in\mathbb{R}^{N_y}
$$

instead of a full 2D heatmap.

### 1.3.2 Confidence Weighting and Uncertainty Propagation

Each keypoint is associated with confidence:

$$
c_i(t)\in[0,1].
$$

A useful uncertainty abstraction is:

$$
P_i(t)
\sim
\mathcal{N}
(\hat p_i(t),\Sigma_i(t)).
$$

For a linear combination $y=Ap_1+Bp_2$:

$$
\Sigma_y
=
A\Sigma_1A^T+
B\Sigma_2B^T.
$$

For a nonlinear quantity $\theta=f(p)$, first-order propagation uses the Jacobian:

$$
\sigma_\theta^2
\approx
J_f\Sigma_pJ_f^T.
$$

The coaching engine should reduce or suppress technical feedback when the visual uncertainty becomes too large.

### 1.3.3 Information Entropy and Feature Relevance

For a continuous feature $X$:

$$
H(X)
=
-\int p(x)\log_2p(x)dx.
$$

Mutual information with a coaching label $Y$:

$$
I(X;Y)=H(X)-H(X|Y).
$$

This provides a principled method for evaluating whether engineered features actually carry diagnostic value.

## 1.4 Classical Signal Processing

### 1.4.1 Sampling and Aliasing

A discrete pose stream is:

$$
x[n]=x(nT_s)
$$

with

$$
f_s=\frac1{T_s}.
$$

Nyquist-Shannon requires:

$$
f_s>2f_{max}.
$$

A 30 FPS camera has a 15 Hz Nyquist frequency. Fast boxing motion can therefore be undersampled, which is important when interpreting wrist acceleration, retraction, and very short impact events.

The application should distinguish between:

- camera sampling
- pose inference rate
- temporal model update rate
- visual rendering rate

These do not need to be identical.

### 1.4.2 LTI Systems and Group Delay

An LTI system produces:

$$
y[n]=(x*h)[n].
$$

Its transfer function is:

$$
H(z)
=
\frac{\sum_{k=0}^M b_kz^{-k}}
{1+\sum_{k=1}^Na_kz^{-k}}.
$$

Group delay:

$$
\tau_g(\omega)
=
-\frac{d\Phi(\omega)}{d\omega}.
$$

A five-tap moving average introduces approximately:

$$
\tau_g=\frac{M-1}{2}
$$

samples, which is about 66.7 ms at 30 FPS. For real-time boxing feedback, excessive fixed smoothing is undesirable, motivating adaptive filtering.

## Core Connections

- [[02. Mobile Vision and Real-Time Pose Estimation/Chapter 2. Mobile Vision and Pose]]
- [[03. Signal Conditioning, Normalization, and Kinematics/Chapter 3. Conditioning and Kinematics]]
- [[04. Spatial-Temporal Deep Learning Architectures/Chapter 4. Spatial-Temporal Deep Learning]]
- [[readme|Final Technical Report — Real-Time AI Boxing Coach]]
