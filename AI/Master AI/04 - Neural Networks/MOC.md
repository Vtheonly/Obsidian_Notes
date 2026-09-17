---
tags: [neural-networks, moc]
iteration: 2
created: 2026-08-07
---

# 04 — Neural Networks MOC

> [!info] The bridge from classical ML to deep learning. Covers the building blocks (perceptrons, MLPs, activations, backprop) and the pre-Transformer architectures (CNNs, RNNs, Seq2Seq) that motivate attention.

## Reading Order

| #   | Note                                              | Sub-domain    | Purpose                                            |
|-----|---------------------------------------------------|---------------|----------------------------------------------------|
| 01  | [[01 - Perceptrons and MLPs]]                     | Foundations   | The universal function approximator.               |
| 02  | [[02 - Activation Functions]]                     | Foundations   | ReLU, GELU, SwiGLU; nonlinearity matters.          |
| 03  | [[03 - CNNs]]                                     | Architectures | Convolutions, ResNet, vision foundation.           |
| 04  | [[04 - RNN LSTM GRU]]                             | Architectures | Sequence modeling pre-Transformer.                 |
| 05  | [[05 - Seq2Seq and the Information Bottleneck]]   | Architectures | The problem attention was invented to fix.         |
| 06  | [[06 - Backpropagation]]                          | Training      | The algorithm that trains every NN.                |
| 07  | [[07 - Initialization Schemes]]                   | Training      | Xavier, He; bad init = no training.                |
| 08  | [[08 - Vanishing and Exploding Gradients]]        | Training      | Why deep networks are hard; how to fix.            |
| 09  | [[03 - Machine Learning/Generalization/06 - Regularization Techniques]]                 | Regularization| (planned — see [[03 - Machine Learning/Generalization/06 - Regularization Techniques|ML regularization]] for now)|

## Why This Chapter Matters

Modern Transformers are "just" stacked neural network layers with a clever routing mechanism (attention). To understand Transformers, you need to understand:

- What a neural layer is (perceptron → MLP).
- How training works (backprop + optimizer).
- Why deep networks are hard (vanishing/exploding gradients).
- What came before (RNNs, CNNs, Seq2Seq) — and why attention was invented to fix their problems.

## See Also

- [[02 - Mathematics/MOC|02 Mathematics]] — the math behind NNs
- [[03 - Machine Learning/MOC|03 Machine Learning]] — ML fundamentals
- [[05 - NLP Fundamentals/MOC|05 NLP Fundamentals]] — NLP background
- [[06 - Attention Mechanisms/MOC|06 Attention Mechanisms]] — attention is the bridge to Transformers
