---
title: Chapter 1 — Complete Technical Deep Dive
tags: [boxing, ai, mathematics, linear-algebra, calculus, probability, signal-processing]
---

# Chapter 1: Mathematical and Theoretical Foundations

This is the complete detailed companion to [[Chapter 1. Foundations]]. It preserves the mathematical material used by the boxing coach architecture.

## 1.1 Linear Algebra for Pose Geometry

### 1.1.1 Vectors, Norms, and Metric Spaces in R² and R³

At time t, keypoint i is represented as:

$$
\mathbf{p}_i(t)=
\begin{bmatrix}
x_i(t)\\
y_i(t)
\end{bmatrix}
\in\mathbb{R}^2
$$

or in 3D:

$$
\mathbf{P}_i(t)=
\begin{bmatrix}
X_i(t)\\
Y_i(t)\\
Z_i(t)
\end{bmatrix}
\in\mathbb{R}^3.
$$

For K tracked landmarks, the complete 2D skeleton can be concatenated:

$$
\mathbf{x}(t)=
[x_1(t),y_1(t),x_2(t),y_2(t),\dots,x_K(t),y_K(t)]^T
\in\mathbb{R}^{2K}.
$$

Difference vector:

$$
\mathbf{d}_{ij}=\mathbf{p}_j-\mathbf{p}_i.
$$

Norms:

$$
\|\mathbf{d}\|_1=|d_x|+|d_y|
$$

$$
\|\mathbf{d}\|_2=\sqrt{d_x^2+d_y^2}
=\sqrt{\mathbf{d}^T\mathbf{d}}
$$

$$
\|\mathbf{d}\|_\infty=\max(|d_x|,|d_y|).
$$

The Euclidean norm is the primary spatial metric for limb length, clearance, and trajectory deviation.

For a joint angle, with limb vectors u and v:

$$
\theta
=
\arccos
\left(
\frac{\mathbf{u}^T\mathbf{v}}
{\|\mathbf{u}\|_2\|\mathbf{v}\|_2}
\right).
$$

For a signed angle in 2D:

$$
\theta_{signed}
=
\operatorname{atan2}
(u_xv_y-u_yv_x,\,
u_xv_x+u_yv_y).
$$

This provides the basis for elbow flexion, knee flexion, torso orientation, and limb articulation.

### 1.1.2 Affine Transformations and Change of Basis

A general affine transformation is:

$$
\mathbf{p}'=\mathbf{A}\mathbf{p}+\mathbf{t}.
$$

Using homogeneous coordinates:

$$
\tilde{\mathbf{p}}=
\begin{bmatrix}
x\\y\\1
\end{bmatrix}
$$

and:

$$
\mathbf{M}
=
\begin{bmatrix}
a_{11}&a_{12}&t_x\\
a_{21}&a_{22}&t_y\\
0&0&1
\end{bmatrix}.
$$

Translation:

$$
\mathbf{T}(t_x,t_y)=
\begin{bmatrix}
1&0&t_x\\
0&1&t_y\\
0&0&1
\end{bmatrix}.
$$

Scale:

$$
\mathbf{S}(s)=
\begin{bmatrix}
s&0&0\\
0&s&0\\
0&0&1
\end{bmatrix}.
$$

Rotation:

$$
\mathbf{R}(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta&0\\
\sin\theta&\cos\theta&0\\
0&0&1
\end{bmatrix}.
$$

For body-centric normalization, let c be the anatomical center and phi the torso tilt:

$$
\phi
=
\operatorname{atan2}
(x_{neck}-x_{mid\_hip},
y_{neck}-y_{mid\_hip})
$$

and:

$$
s=
\frac{1}
{\|\mathbf{p}_{neck}-\mathbf{p}_{mid\_hip}\|_2}.
$$

Then:

$$
\mathbf{M}_{norm}
=
\mathbf{S}(s)
\mathbf{R}(-\phi)
\mathbf{T}(-c_x,-c_y).
$$

Applied to every joint, this reduces dependence on subject position, camera distance, and camera orientation.

### 1.1.3 SVD and PCA

For a centered temporal pose matrix:

$$
\mathbf{X}\in\mathbb{R}^{T\times2K}
$$

define:

$$
\tilde{\mathbf{X}}
=
\mathbf{X}
-
\mathbf{1}_T\boldsymbol\mu^T
$$

with:

$$
\mu_j=
\frac1T\sum_{t=1}^T X_{tj}.
$$

Covariance:

$$
\boldsymbol\Sigma
=
\frac1{T-1}
\tilde{\mathbf{X}}^T\tilde{\mathbf{X}}.
$$

SVD:

$$
\tilde{\mathbf{X}}
=
\mathbf{U}
\boldsymbol\Sigma_{svd}
\mathbf{V}^T.
$$

The singular values relate to covariance eigenvalues:

$$
\sigma_i=\sqrt{(T-1)\lambda_i}.
$$

Low-rank embedding:

$$
\mathbf{Z}_r
=
\tilde{\mathbf{X}}\mathbf{V}_r.
$$

Reconstruction:

$$
\hat{\mathbf{X}}
=
\mathbf{Z}_r\mathbf{V}_r^T
+
\mathbf{1}_T\boldsymbol\mu^T.
$$

Anomaly residual:

$$
\epsilon_{anomaly}(t)
=
\left\|
\tilde{\mathbf{x}}(t)
-
\mathbf{V}_r\mathbf{V}_r^T\tilde{\mathbf{x}}(t)
\right\|_2^2.
$$

PCA/SVD is useful for exploratory motion analysis, denoising, compression, and anomaly detection. Any fixed statement such as "six components always capture 95%" must instead be validated on the actual boxing dataset.

## 1.2 Multivariate Calculus and Optimization

### 1.2.1 Gradient Descent and Backpropagation

The learning problem can be written:

$$
\theta^*
=
\arg\min_\theta
\left[
\frac1N
\sum_{i=1}^N
\ell(f(x^{(i)};\theta),y^{(i)})
+
\lambda\Omega(\theta)
\right].
$$

Gradient:

$$
\nabla_\theta\mathcal{L}
=
\begin{bmatrix}
\frac{\partial\mathcal{L}}{\partial\theta_1}
&
\cdots
&
\frac{\partial\mathcal{L}}{\partial\theta_D}
\end{bmatrix}^T.
$$

Gradient descent:

$$
\theta_{t+1}
=
\theta_t-\eta\nabla_\theta\mathcal{L}(\theta_t).
$$

Adam-style moving averages:

$$
m_t
=
\beta_1m_{t-1}
+
(1-\beta_1)g_t
$$

$$
v_t
=
\beta_2v_{t-1}
+
(1-\beta_2)g_t^2.
$$

Bias corrections:

$$
\hat m_t
=
\frac{m_t}{1-\beta_1^t},
\qquad
\hat v_t
=
\frac{v_t}{1-\beta_2^t}.
$$

AdamW-style update:

$$
\theta_{t+1}
=
\theta_t
-
\eta_t
\left(
\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
+
\gamma\theta_t
\right).
$$

For a neural layer:

$$
a^{(l)}
=
\sigma(W^{(l)}a^{(l-1)}+b^{(l)}).
$$

Backpropagation:

$$
\delta^{(L)}
=
\nabla_{a^{(L)}}\ell
\odot
\sigma'(z^{(L)})
$$

$$
\delta^{(l)}
=
((W^{(l+1)})^T\delta^{(l+1)})
\odot
\sigma'(z^{(l)}).
$$

Parameter gradients:

$$
\frac{\partial\mathcal{L}}{\partial W^{(l)}}
=
\delta^{(l)}(a^{(l-1)})^T
$$

$$
\frac{\partial\mathcal{L}}{\partial b^{(l)}}
=
\delta^{(l)}.
$$

### 1.2.2 Kinematic Derivatives

For p(t):

$$
v(t)=\frac{dp(t)}{dt}
$$

$$
a(t)=\frac{d^2p(t)}{dt^2}
$$

$$
j(t)=\frac{d^3p(t)}{dt^3}.
$$

Discrete approximations:

| Quantity | Approximation | Error order |
|---|---|---|
| Velocity | (p[t+1] - p[t]) / dt | O(dt) |
| Velocity | (p[t] - p[t-1]) / dt | O(dt) |
| Velocity | (p[t+1] - p[t-1]) / (2dt) | O(dt²) |
| Acceleration | (p[t+1] - 2p[t] + p[t-1]) / dt² | O(dt²) |
| Jerk | (p[t+2] - 2p[t+1] + 2p[t-1] - p[t-2]) / (2dt³) | O(dt²) |

Causal/backward differences are appropriate for live inference. Central differences can be used in post-repetition review because the complete trajectory is then available.

## 1.3 Probability, Information Theory, and Confidence Modeling

### 1.3.1 Heatmaps as Spatial Probability Densities

A Gaussian keypoint target is:

$$
p(\mathbf{u}\mid\mathbf{g}_k)
=
\frac{1}{2\pi\sigma^2}
\exp
\left(
-\frac{\|\mathbf{u}-\mathbf{g}_k\|_2^2}{2\sigma^2}
\right).
$$

Standard heatmap decoding:

$$
\hat{\mathbf{p}}_k
=
\arg\max_{(u,v)}H_k(u,v).
$$

Soft-argmax:

$$
\tilde H_k(u,v)
=
\frac{\exp(\beta H_k(u,v))}
{\sum_{u',v'}\exp(\beta H_k(u',v'))}
$$

and:

$$
\hat{\mathbf{p}}_k
=
\sum_{u,v}
\begin{bmatrix}
u\\v
\end{bmatrix}
\tilde H_k(u,v).
$$

SimCC instead predicts one-dimensional coordinate distributions:

$$
p_x\in\mathbb{R}^{N_x},
\qquad
p_y\in\mathbb{R}^{N_y}.
$$

With coordinate split factor k:

$$
N_x=Wk,
\qquad
N_y=Hk.
$$

A Gaussian-smoothed target for x:

$$
T_x(i)
=
\frac{1}{\sqrt{2\pi}\sigma}
\exp
\left(
-\frac{(i-x^*k)^2}{2\sigma^2}
\right).
$$

SimCC loss:

$$
\mathcal{L}_{SimCC}
=
\frac1K
\sum_{k=1}^K
\left(
\mathcal{L}_{CE}(p_{x,k},T_{x,k})
+
\mathcal{L}_{CE}(p_{y,k},T_{y,k})
\right).
$$

### 1.3.2 Confidence Weighting and Uncertainty Propagation

Each keypoint has confidence:

$$
c_i(t)\in[0,1].
$$

A confidence-aware Gaussian model is:

$$
\mathbf{P}_i(t)
\sim
\mathcal{N}
(\hat{\mathbf{p}}_i(t),\Sigma_i(t))
$$

with an illustrative confidence-to-covariance mapping:

$$
\Sigma_i(t)
=
\sigma_0^2
\left(
\frac{1-c_i(t)+\epsilon}
{c_i(t)+\epsilon}
\right)I_2.
$$

For a linear combination:

$$
y=Ap_1+Bp_2
$$

the covariance is:

$$
\Sigma_y
=
A\Sigma_1A^T+B\Sigma_2B^T.
$$

For nonlinear f(p), first-order propagation uses:

$$
f(p)
\approx
f(\hat p)
+
J_f(\hat p)(p-\hat p).
$$

Thus:

$$
\sigma_f^2
\approx
J_f\Sigma_pJ_f^T.
$$

The coaching engine should suppress feedback when propagated uncertainty is too high.

### 1.3.3 Information Entropy and Feature Relevance

Differential entropy:

$$
H(X)
=
-\int_{\mathcal X}
p(x)\log_2p(x)\,dx.
$$

Conditional entropy:

$$
H(X|Y)
=
-\sum_y p(y)
\int
p(x|y)\log_2p(x|y)\,dx.
$$

Mutual information:

$$
I(X;Y)
=
H(X)-H(X|Y).
$$

This can be used to rank engineered kinematic features for mobile inference.

## 1.4 Classical Signal Processing

### 1.4.1 Nyquist-Shannon Sampling and Aliasing

Sampling:

$$
x[n]=x(nT_s)
$$

with:

$$
f_s=\frac1{T_s}.
$$

Nyquist condition:

$$
f_s>2f_{max}.
$$

At 30 FPS:

$$
f_{Nyquist}=15Hz.
$$

Fast hand movement can therefore be undersampled. A discrete alias may be expressed as:

$$
f_{alias}
=
|f_{signal}-kf_s|.
$$

Mitigation strategies described by the curriculum:

1. Interpolate around inflection points.
2. Use adaptive pose extraction frequency based on movement magnitude.
3. Apply responsive temporal filtering such as the One Euro Filter.

### 1.4.2 LTI Systems and Group Delay

An LTI system satisfies linearity and time invariance and is characterized by its impulse response h[n].

Convolution:

$$
y[n]=(x*h)[n]
=
\sum_kx[k]h[n-k].
$$

Transfer function:

$$
H(z)
=
\frac{\sum_{k=0}^{M}b_kz^{-k}}
{1+\sum_{k=1}^{N}a_kz^{-k}}.
$$

Frequency response:

$$
H(e^{j\omega})
=
|H(e^{j\omega})|
e^{j\Phi(\omega)}.
$$

Phase delay:

$$
\tau_p(\omega)
=
-\frac{\Phi(\omega)}{\omega}.
$$

Group delay:

$$
\tau_g(\omega)
=
-\frac{d\Phi(\omega)}{d\omega}.
$$

For an M-tap moving average:

$$
\tau_g=\frac{M-1}{2}
$$

samples.

At 30 FPS, a 5-tap filter produces about 66.7 ms of group delay, illustrating why fixed long-window smoothing is undesirable for live boxing feedback.

## Chapter 1 Technical Connections

- [[Chapter 1. Foundations]]
- [[03. Signal Conditioning, Normalization, and Kinematics/Chapter 3. Conditioning and Kinematics]]
- [[04. Spatial-Temporal Deep Learning Architectures/Chapter 4. Spatial-Temporal Deep Learning]]
- [[Chapter 2. Full Technical Deep Dive]]
