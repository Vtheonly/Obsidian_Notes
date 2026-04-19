# Course: TAMER Math OCR - Deep Learning Theory & Architecture

---

## Course Overview

This course covers the complete theory and architecture behind TAMER (Tree-Aware Math Expression Recognition), a deep learning system for converting images of mathematical expressions into LaTeX source code. The material spans the full pipeline from raw pixel input to structured LaTeX output, covering data engineering, vision encoders, sequence decoders, loss functions, inference algorithms, hardware optimization, and deployment.

The course is organized into nine chapters, each building on the previous:

- **Chapters 1-2:** Foundational concepts — the mathematical OCR problem, image-to-sequence modeling, data representation, and memory management.
- **Chapters 3-4:** The encoder-decoder architecture — Swin Transformer vision encoders, positional encodings, and Transformer decoder sequence generation.
- **Chapters 5-6:** Training objectives and inference — loss functions, decoding algorithms, and grammar constraints.
- **Chapters 7-8:** Optimization at scale — mixed precision training, multi-GPU setups, curriculum learning, evaluation metrics, and cloud persistence.
- **Chapter 9:** The complete architecture blueprint — end-to-end tensor flow, row boundary markers, and the grammar state machine specification.

---

## Vault Structure

```
Course: TAMER Math OCR - Deep Learning Theory & Architecture {

    Chapter 1: Deep Learning & Mathematical OCR Foundations
        - Introduction to Image-to-Sequence Models
        - The Physics of Mathematical Typography

    Chapter 2: Data Representation and Caching Physics
        - Image Processing for OCR Constraints
        - Python Memory Leaks and The OOM Caching Bug
        - Data Augmentation Theory

    Chapter 3: The Tokenizer - Mapping Math to Discrete Tokens
        - Lexical Analysis of LaTeX
        - Vocabulary and Special Tokens

    Chapter 4: The Encoder - Vision Transformers (Swin-v2)
        - Convolutional vs Transformer Vision Models
        - Swin Transformer v2 Architecture
        - 2D Positional Encoding and Spatial Awareness

    Chapter 5: The Decoder - Sequence Generation
        - Transformer Decoder Architecture
        - 1D Sinusoidal Positional Encoding
        - Autoregressive Teacher Forcing

    Chapter 6: Objective Functions (Loss)
        - Cross-Entropy and Label Smoothing
        - Structure-Aware Loss Functions

    Chapter 7: Inference Algorithms
        - Batched Greedy Decoding
        - Beam Search Decoding

    Chapter 8: Hardware Optimization & Distributed Training
        - Mixed Precision Training (BFloat16 vs FP16)
        - PyTorch DataLoaders and RAM Saturation
        - Multi-GPU Training (DataParallel)
}
```

---

## Extended Vault Structure

```
Course: TAMER Math OCR - Deep Learning Theory & Architecture {

    Chapter 1: Foundations of Mathematical OCR
        - 1.1 HMER Overview and Challenges
        - 1.2 Sequence vs Tree Decoding
        - 1.3 Tokenization and Mathematical Grammar
        - 1.5 The No-Tree Trade-off: Relying on Attention

    Chapter 2: Data Engineering and Memory Physics
        - 2.1 Python Memory Management and OOM Prevention
        - 2.2 Caching Physics and Path Resolution
        - 2.3 Image Processing for OCR Constraints
        - 2.4 Synthetic Data and Augmentation

    Chapter 3: Vision Encoders (The Eyes)
        - 3.1 CNNs and Spatial Precision
        - 3.2 Vision Transformers and Attention Basics
        - 3.3 Swin Transformer V2 Architecture
        - 3.4 2D Positional Encodings
        - 3.5 Feature Pyramid Networks and Fusion
        - 3.7 What is Positional Encoding (1D vs 2D)

    Chapter 4: Sequence Generation (The Voice)
        - 4.1 Transformer Decoder Fundamentals
        - 4.2 Cross Attention and Context Mapping
        - 4.3 Coverage Attention Mechanism
        - 4.6 Teacher Forcing and Exposure Bias
        - 4.7 Scheduled Sampling: Bridging the Training-Inference Gap
        - 4.8 The Full Decoder Training Loop End to End

    Chapter 5: Tree Aware Module and Structural Logic
        - 5.1 Tree Representation and Annotation
        - 5.2 Tree Aware Module Implementation
        - 5.3 Joint Optimization and Loss Functions

    Chapter 6: Inference Algorithms and Decoding
        - 6.1 Beam Search and Greedy Decoding
        - 6.2 LaTeX Grammar Constraints
        - 6.3 Tree Based Structural Scoring
        - 6.4 Constrained Beam Search Synthesis

    Chapter 7: Hardware Optimization and Training Dynamics
        - 7.1 BFloat16 vs FP16 and Tensor Cores
        - 7.2 Multi GPU Training and DataLoaders
        - 7.3 Two Stage Pretraining and Curriculum Learning

    Chapter 8: Evaluation and MLOps
        - 8.1 Datasets and Evaluation Metrics
        - 8.2 Performance and Complexity Analysis
        - 8.3 Cloud Integration and Persistence

    Chapter 9: The Complete Architecture Blueprint
        - 9.1 The Master TAMER Architecture Diagram
        - 9.2 Layer-by-Layer Tensor Flow and Mathematics
        - 9.3 The Row Boundary Marker: Deep Dive
        - 9.4 Why norm_first=True Matters at Scale
        - 9.5 The Complete Forward Pass: Every Tensor, Every Shape
        - 9.6 The Training Loop vs Inference Loop: Side by Side
        - 9.7 The Grammar State Machine: Full Specification
}
```
