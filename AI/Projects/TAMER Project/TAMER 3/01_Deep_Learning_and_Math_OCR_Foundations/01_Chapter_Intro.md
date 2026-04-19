# Chapter 1: Deep Learning & Mathematical OCR Foundations

---

## Chapter Introduction

This chapter establishes the fundamental problem that TAMER is designed to solve: converting an image of a mathematical expression into a machine-readable LaTeX string. Unlike classical OCR which reads linear text left-to-right, mathematical OCR must handle two-dimensional spatial structures — fractions, superscripts, subscripts, and matrices — where the visual arrangement is as meaningful as the symbols themselves.

We begin by formalizing mathematical OCR as an **Image-to-Sequence translation** task, where the model learns the conditional probability distribution $P(Y \mid X)$ over LaTeX token sequences $Y$ given an input image $X$. Using the chain rule of conditional probability, this joint distribution is factorized into a product of autoregressive step predictions, which directly motivates the encoder-decoder architecture that TAMER employs.

We then examine the unique structural properties of mathematical notation that make it fundamentally different from natural language. Mathematical expressions exist in two dimensions: numerators sit above denominators, superscripts float to the upper-right, and matrix cells occupy a strict row-column grid. These spatial relationships must be preserved in the output LaTeX, which means the model cannot simply read pixels left-to-right — it must develop an understanding of the 2D grammar of mathematics.

The chapter also introduces TAMER's three-tier complexity classification system (Simple, Medium, Complex), which categorizes formulas by their structural difficulty. This classification directly informs preprocessing, loss weighting, and augmentation strategies throughout the pipeline.

Finally, Section 1.5 presents a critical architectural analysis: **why removing the Tree-Aware Module (TAM) is defensible** when using a Transformer decoder. The original TAMER paper introduced the TAM to compensate for RNNs' limited memory horizon. However, the Transformer's self-attention mechanism provides $O(1)$ lookup to any past position, eliminating the memory bottleneck. This section provides a complete engineering trade-off analysis comparing the explicit tree module against implicit attention-based structural understanding, including what you gain (inference speed, VRAM efficiency, training stability) and what you lose (explicit structural guarantees, peak performance on deeply nested structures).

### Sections in this Chapter

| Section | Title | Key Topics |
|---------|-------|------------|
| 1 | Introduction to Image-to-Sequence Models | Chain rule decomposition, encoder-decoder architecture, autoregressive generation |
| 2 | The Physics of Mathematical Typography | 2D spatial grammar, complexity tiers (Simple/Medium/Complex), structural token challenges |
| 1.5 | The No-Tree Trade-off: Relying on Attention | RNN memory horizon problem, Transformer self-attention as implicit tree parser, engineering trade-offs of removing the TAM |

---
