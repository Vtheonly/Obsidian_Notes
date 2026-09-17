---
title: Chapter 2 — Mobile Vision and Real-Time Pose Estimation
tags: [boxing, ai, computer-vision, pose-estimation, rtmpose, camerax, mobile]
---

# Chapter 2: Mobile Vision and Real-Time Pose Estimation

## 2.1 Camera Acquisition and Memory Pipelines

### 2.1.1 CameraX Architecture

The Android camera layer should use CameraX ImageAnalysis. The key real-time rule is KEEP_ONLY_LATEST so the analyzer never builds a queue of stale frames.

Recommended baseline:

ImageAnalysis.Builder()
    .setTargetResolution(Size(1280, 720))
    .setBackpressureStrategy(STRATEGY_KEEP_ONLY_LATEST)
    .setOutputImageFormat(YUV_420_888)
    .build()

Every ImageProxy must be closed as soon as analysis finishes.

### 2.1.2 YUV 420 and Tensor Conversion

CameraX normally exposes YUV 4:2:0. Avoid repeated JVM allocations and Bitmap conversion.

Preferred path:

CameraX YUV frame
→ direct/native buffer
→ accelerated YUV conversion
→ model tensor

A C++/JNI + SIMD path is an optimization candidate when profiling demonstrates that JVM conversion is a bottleneck.

## 2.2 2D Human Pose Estimation Paradigms

Top-down pose estimation is a natural fit for a single-person boxing application. A lightweight ROI/person tracker identifies the boxer, then the pose model operates on the crop.

| Characteristic | Top-Down | Bottom-Up |
|---|---|---|
| Single boxer | Excellent fit | Extra grouping work |
| Spatial precision | High | More shared-image tradeoffs |
| Background people | Easier to ignore | Must be grouped/filtered |
| Mobile use | Appropriate | Less attractive for one boxer |

## 2.3 RTMPose Deep Dive

### 2.3.1 Heatmap, Regression, and SimCC

Pose heads can use:

1. 2D heatmap regression
2. direct Cartesian regression
3. SimCC coordinate classification

SimCC predicts independent one-dimensional coordinate distributions for x and y instead of a dense 2D heatmap. This is valuable for edge inference because the output representation is compact.

The project baseline is RTMPose-S, fine-tuned on boxing data.

### 2.3.2 RTMPose Deployment Considerations

The pose model should be evaluated on the physical Galaxy A30s using:

- pose latency
- wrist stability
- ankle stability
- occlusion behavior
- memory
- thermal behavior
- effective inference FPS

Results published for other processors must not be treated as A30s measurements.

## 2.4 Boxing-Specific Keypoint Semantics

Generic COCO keypoints provide the main anatomical skeleton but boxing may require richer semantics.

Important additions:

- glove or hand endpoints
- heel and forefoot/metatarsal landmarks
- better head/chin representation
- torso orientation
- foot-axis orientation

A chin proxy may be formed from nose and neck positions, but the coefficient should be calibrated experimentally.

## 2.5 Separation of Capture, Inference, and Rendering Rates

The camera can operate around 30 FPS while pose inference runs around 10–15 updates/s initially.

Camera FPS != pose inference FPS != UI FPS.

This separation lets the application remain responsive while the expensive vision pipeline runs at a realistic rate.

## Core Connections

- [[01. Mathematical and Theoretical Foundations/Chapter 1. Foundations]]
- [[03. Signal Conditioning, Normalization, and Kinematics/Chapter 3. Conditioning and Kinematics]]
- [[07. Edge Inference Runtime and Optimization/Chapter 7. Edge Runtime and Optimization]]
- [[readme|Final Technical Report — Real-Time AI Boxing Coach]]
