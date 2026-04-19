# Chapter 6: Objective Functions (Loss)

---

## Chapter Introduction

This chapter covers the loss functions that drive the TAMER model's learning, and how they are designed to emphasize the structural elements that matter most for mathematical OCR accuracy.

The primary training objective is **Cross-Entropy Loss with Label Smoothing**. The cross-entropy loss is not an arbitrary choice — it is mathematically derived from the maximum likelihood objective $P(Y \mid X)$. Minimizing the negative log-likelihood of the correct token at each position is equivalent to maximizing the joint probability of the entire target sequence. Label smoothing (setting a small probability mass $\epsilon$ uniformly across all tokens) serves two purposes: it prevents the model from becoming overconfident (which leads to brittle predictions), and it provides a regularization effect that improves generalization to unseen data.

However, standard cross-entropy treats all token positions equally. In mathematical OCR, this is suboptimal because **not all errors are equally damaging**. A wrong digit in a coefficient is a minor error — the formula still compiles and is approximately correct. But a missing `\\` (row separator) or `&` (column separator) in a matrix collapses the entire structure, making the formula unrecognizable. This motivates **Structure-Aware Loss Weighting**, which multiplies the loss contribution at structural token positions by a factor of 3.0x. This creates a stronger gradient signal at the moments when structural decisions are being made, forcing the model to be extremely careful about these critical tokens.

The chapter explains how the padding mask integrates with the loss computation (positions containing `<pad>` tokens contribute zero to the loss), and how the structure-aware weighting interacts with label smoothing to produce a balanced training signal.

### Sections in this Chapter

| Section | Title | Key Topics |
|---------|-------|------------|
| 1 | Cross-Entropy and Label Smoothing | MLE derivation, label smoothing regularization, overconfidence prevention, smoothing parameter choice |
| 2 | Structure-Aware Loss Functions | Unequal error costs, 3.0x structural token weighting, padding mask integration, interaction with label smoothing |

---
