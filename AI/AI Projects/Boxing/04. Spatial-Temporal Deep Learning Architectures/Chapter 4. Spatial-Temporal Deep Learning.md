---
title: Chapter 4 — Spatial-Temporal Deep Learning Architectures
tags: [boxing, ai, deep-learning, st-gcn, transformer, knowledge-distillation]
---

# Chapter 4: Spatial-Temporal Deep Learning Architectures

## 4.1 Graph Convolution Foundations

Represent the skeleton as a graph G = (V, E):

- vertices V = anatomical joints
- edges E = anatomical connections
- adjacency A = connectivity
- degree matrix D = node degree
- Laplacian L = D - A

Graph modeling matches the physical topology of the human body more directly than treating the skeleton as an ordinary flat vector.

## 4.2 Spatial-Temporal Graph Convolutional Networks

ST-GCN-style processing learns local anatomical relationships first, then temporal relationships across frames.

Conceptual flow:

Joints
→ spatial neighborhood aggregation
→ graph features
→ temporal convolution
→ motion representation

Useful spatial partitions include:

- root joint
- centripetal neighbors
- centrifugal neighbors

For causal temporal inference:

X_next(t) = sum over past offsets of W_offset X(t - offset)

The temporal receptive field should cover complete punch phases while remaining inexpensive on the A30s.

## 4.3 Transformer Attention Mechanisms

### 4.3.1 Scaled Dot-Product Attention

For motion token sequence Z:

Q = Z W_Q
K = Z W_K
V = Z W_V

Attention(Q,K,V) =
Softmax((Q K^T) / sqrt(d_k) + causal_mask) V

Causal masking is important because the live model cannot inspect future frames.

Multi-head attention allows different heads to specialize in different temporal relationships such as:

- wrist acceleration
- guard persistence
- foot-to-hand coordination
- recovery timing

### 4.3.2 Positional Encoding

Self-attention needs explicit sequence order.

Candidate approaches:

- sinusoidal positional encoding
- learnable positional embeddings

For a fixed mobile window, learnable embeddings are a viable baseline; the choice should be validated experimentally.

## 4.4 Tiny Temporal Transformer

Baseline mobile design:

| Parameter | Initial target |
|---|---:|
| Sequence window | 32 frames |
| Model width | 48 |
| Attention heads | 3 |
| FFN width | 96 |
| Encoder depth | 2 |
| Deployment | CPU/mobile |

Pipeline:

normalized pose + kinematics
→ projection
→ positional encoding
→ causal transformer block
→ causal transformer block
→ motion embedding
→ movement and phase heads

SwiGLU is a candidate feed-forward activation.

The exact dimensions are a starting hypothesis, not a permanent specification.

## 4.5 Teacher-Student Knowledge Distillation

Use a larger motion transformer offline on the RTX 3060 and distill its useful representations into a much smaller student.

Teacher
→ teacher logits and motion embeddings
→ student training
→ quantization
→ Galaxy A30s

Combined loss:

L_distill =
alpha L_task
+ beta L_soft
+ gamma L_hidden

Soft-target loss can use KL divergence with a temperature parameter.

Hidden representation loss can align projected teacher and student embeddings.

Candidate teachers include MotionBERT- or DSTformer-style architectures, but model choice must consider licensing, reproducibility, resource usage, and actual boxing-task improvement.

## Architecture Principle

Use the transformer for temporal intelligence, not as a giant end-to-end image/video model on the target phone.

## Core Connections

- [[03. Signal Conditioning, Normalization, and Kinematics/Chapter 3. Conditioning and Kinematics]]
- [[05. Biomechanical Modeling and Sequence Comparison/Chapter 5. Biomechanical Modeling]]
- [[07. Edge Inference Runtime and Optimization/Chapter 7. Edge Runtime and Optimization]]
- [[readme|Final Technical Report — Real-Time AI Boxing Coach]]
