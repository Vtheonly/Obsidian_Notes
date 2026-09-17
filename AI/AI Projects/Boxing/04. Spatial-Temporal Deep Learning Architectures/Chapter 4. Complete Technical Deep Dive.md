---
title: Chapter 4 — Complete Technical Deep Dive
tags: [boxing, ai, deep-learning, gcn, st-gcn, transformer, distillation]
---

# Chapter 4: Spatial-Temporal Deep Learning Architectures

## 4.1 Graph Convolution Foundations

### 4.1.1 Graph Laplacian and Spectral Convolutions

Skeleton graph:

$$
G=(V,E).
$$

Adjacency:

$$
A_{ij}
=
1
\quad
\text{if joints i and j are connected}.
$$

Degree:

$$
D_{ii}
=
\sum_j A_{ij}.
$$

Laplacian:

$$
L=D-A.
$$

Normalized Laplacian:

$$
L_{sym}
=
D^{-1/2}LD^{-1/2}
=
I-D^{-1/2}AD^{-1/2}.
$$

Spectral decomposition:

$$
L_{sym}=U\Lambda U^T.
$$

Graph Fourier transform:

$$
\hat{x}=U^Tx.
$$

Spectral graph convolution:

$$
x *_G g
=
Ug(\Lambda)U^Tx.
$$

For efficiency, Chebyshev polynomial approximation can avoid explicit eigendecomposition:

$$
g_\theta(\Lambda)
\approx
\sum_{k=0}^{M}
\theta'_kT_k(\tilde{\Lambda}).
$$

The polynomial recurrence is:

$$
T_0(x)=1,
\quad
T_1(x)=x,
\quad
T_k(x)=2xT_{k-1}(x)-T_{k-2}(x).
$$

The practical consequence is localized neighborhood aggregation without carrying a full spectral basis through mobile inference.

## 4.2 ST-GCN

### 4.2.1 Spatial Configuration Partitioning

Sequence tensor:

$$
X\in\mathbb{R}^{C\times T\times K}.
$$

For each node i, aggregate over a neighborhood B_i.

A spatial configuration partition can separate:

- root node
- centripetal neighbors
- centrifugal neighbors

The intuition matches boxing motion: the body core and distal joints participate in different directions of information flow.

A partitioned convolution can be represented as:

$$
Y
=
\sum_d
\Lambda_d^{-1/2}
(A_d\odot M_d)
\Lambda_d^{-1/2}
XW_d.
$$

Here A_d is a partition adjacency matrix, M_d is a learnable attention mask, and W_d is a learnable transform.

### 4.2.2 Temporal Convolutions

Non-causal temporal convolution:

$$
X_{l+1}(:,t,k)
=
\sum_{\tau=-r}^{r}
W_\tau X_l(:,t+\tau,k).
$$

For live inference use a causal form:

$$
X_{l+1}(:,t,k)
=
\sum_{\tau=0}^{K_t-1}
W_\tau X_l(:,t-\tau,k).
$$

For L layers and kernel K_t with unit dilation:

$$
RF
=
1+
L(K_t-1).
$$

The receptive field must be large enough to observe the relevant punch phase sequence but small enough to remain efficient.

## 4.3 Transformer Attention

### 4.3.1 Scaled Dot-Product and Multi-Head Attention

Given temporal embeddings Z:

$$
Q=ZW_Q,
\quad
K=ZW_K,
\quad
V=ZW_V.
$$

Attention:

$$
Attention(Q,K,V)
=
Softmax
\left(
\frac{QK^T}{\sqrt{d_k}}+M
\right)V.
$$

For causal inference, future positions are masked.

Multi-head attention:

$$
MHA(Z)
=
Concat(head_1,\dots,head_h)W_O.
$$

A motion-model head can learn short-range acceleration patterns while another can learn longer guard or foot-to-hand dependencies.

### 4.3.2 Positional Encoding

Without temporal position information, self-attention does not inherently know chronological order.

Sinusoidal encoding:

$$
E_{pos,2i}
=
\sin
\left(
\frac{pos}{10000^{2i/D}}
\right)
$$

$$
E_{pos,2i+1}
=
\cos
\left(
\frac{pos}{10000^{2i/D}}
\right).
$$

Alternatively use learnable positional vectors for a fixed-size mobile window.

## 4.4 Tiny Temporal Transformer

### 4.4.1 Kinematic Signal Transformer

Initial architecture hypothesis:

| Parameter | Target |
|---|---:|
| Window | 32 frames |
| Model width | 48 |
| Heads | 3 |
| FFN width | 96 |
| Layers | 2 |

Pipeline:

normalized pose
→ feature projection
→ positional encoding
→ causal attention block
→ causal attention block
→ motion embedding
→ movement classifier
→ phase classifier

Candidate feed-forward activation:

$$
SwiGLU(x)
=
(xW_1\odot Swish(xW_2))W_3.
$$

The parameter budget is a design target and must be measured after implementation.

## 4.5 Teacher-Student Knowledge Distillation

### 4.5.1 Distilling Large Motion Models

A large transformer can run offline on the RTX 3060.

Teacher:
MotionBERT/DSTformer-style model
→ teacher embeddings and logits
→ small student
→ mobile quantization

Combined objective:

$$
L_{distill}
=
\alpha L_{task}
+
\beta L_{soft}
+
\gamma L_{hidden}.
$$

Hard task loss:

$$
L_{task}
=
-\sum_c y_c\log p_c.
$$

Soft loss:

$$
L_{soft}
=
T^2
D_{KL}
(
Softmax(z_t/T)
\parallel
Softmax(z_s/T)
).
$$

Feature alignment:

$$
L_{hidden}
=
\frac1T
\sum_t
\|
h_t^{teacher}
-
W_{proj}h_t^{student}
\|_2^2.
$$

The teacher is an offline training component and does not need to ship with the phone.

## Core Connections

- [[03. Signal Conditioning, Normalization, and Kinematics/Chapter 3. Conditioning and Kinematics]]
- [[05. Biomechanical Modeling and Sequence Comparison/Chapter 5. Biomechanical Modeling]]
- [[07. Edge Inference Runtime and Optimization/Chapter 7. Edge Runtime and Optimization]]
