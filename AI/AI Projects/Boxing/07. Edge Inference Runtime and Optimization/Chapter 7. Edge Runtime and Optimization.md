---
title: Chapter 7 — Edge Inference Runtime and Optimization
tags: [boxing, ai, android, on-device, quantization, onnx, optimization, thermals]
---

# Chapter 7: Edge Inference Runtime and Optimization

## 7.1 Exynos 7904 Constraints

The target device is the Samsung Galaxy A30s.

The runtime must account for:

- heterogeneous CPU cores
- limited GPU resources
- no modern dedicated NPU equivalent to flagship hardware
- 4 GB RAM target
- sustained thermal throttling

The physical device is the final authority for performance.

## 7.2 Quantization

### 7.2.1 FP32 to INT8

Uniform affine quantization maps a real tensor into a finite integer range:

q = clip(round(x / S) + Z, q_min, q_max)

and dequantizes as:

x_hat = S(q - Z)

Symmetric weight quantization commonly uses Z = 0.

The main goals are lower memory traffic, smaller model size, and faster mobile kernels.

### 7.2.2 Quantized Matrix Multiplication

Quantized activations and weights are multiplied using integer arithmetic with wider accumulation, then rescaled.

The key design constraint is not “INT8 at any cost”; it is the best measured balance of accuracy, latency, memory, battery, and temperature.

## 7.3 ONNX Runtime Mobile vs LiteRT

ONNX Runtime Mobile is the primary candidate because the expected training pipeline is PyTorch/ONNX-oriented and XNNPACK provides an efficient ARM CPU path.

LiteRT remains a valid alternative if physical-device benchmarks show a meaningful advantage.

Benchmark both where feasible.

## 7.4 Thread Scheduling and Thermal Control

Conceptual execution domains:

CameraX capture
→ inference
→ filtering/kinematics/state
→ UI/audio

Monitor:

- per-stage latency
- end-to-end latency
- effective pose FPS
- CPU
- RAM
- battery drain
- temperature
- thermal throttling

The system can reduce pose processing cadence under sustained thermal pressure.

A 15 FPS target may fall toward 10 FPS while temporal processing bridges the larger gaps.

## 7.5 Model Compression Process

Recommended sequence:

FP32 baseline
→ FP16 experiment
→ INT8 post-training quantization
→ quantization-aware training if needed
→ physical-device validation

Every model revision should be tested against stance, jab, cross, hook, occlusion, slow motion, and fast motion.

## Core Connections

- [[02. Mobile Vision and Real-Time Pose Estimation/Chapter 2. Mobile Vision and Pose]]
- [[04. Spatial-Temporal Deep Learning Architectures/Chapter 4. Spatial-Temporal Deep Learning]]
- [[08. End-to-End System Synthesis and Verification/Chapter 8. System Synthesis and Verification]]
- [[readme|Final Technical Report — Real-Time AI Boxing Coach]]
