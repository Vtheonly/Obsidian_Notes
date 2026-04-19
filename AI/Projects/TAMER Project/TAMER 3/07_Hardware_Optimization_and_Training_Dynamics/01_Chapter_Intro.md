# Chapter 7: Inference Algorithms

---

## Chapter Introduction

This chapter covers the decoding algorithms used at inference time to convert the model's probability distributions into actual LaTeX sequences, as well as the advanced training strategies that make TAMER's training feasible at scale.

The chapter begins with the two fundamental decoding strategies:

- **Batched Greedy Decoding**: At each step, select the single highest-probability token. This is the simplest and fastest approach but has no mechanism for recovering from errors — once a wrong token is selected, all subsequent predictions are conditioned on that mistake.

- **Beam Search Decoding**: Maintain $K$ candidate sequences (beams) simultaneously. At each step, expand each beam into all possible next tokens, compute scores, and keep only the top $K$ sequences. This provides $K$ parallel attempts at generating the correct formula, with error-prone beams naturally falling out of the top-$K$ due to lower cumulative scores. Beam search with width $K=5$ typically improves ExpRate by 3-8 percentage points over greedy decoding.

The chapter then shifts to the most critical training strategy: **Two-Stage Pretraining and Curriculum Learning** (Section 7.3). Training a mathematical OCR model from scratch on handwritten data is one of the hardest optimization problems in applied deep learning because the model must simultaneously learn visual features, LaTeX grammar, mathematical structure, and noise tolerance — four objectives with contradictory gradient signals. TAMER decomposes this into:

- **Stage 1**: Train on clean printed data (Im2LaTeX-100K/230K) with no augmentation. The model learns LaTeX grammar, mathematical structure, and canonical symbol archetypes in a noise-free environment.
- **Stage 2**: Fine-tune on handwritten data (CROHME, HME100K) with full augmentation. The model adapts its visual features to recognize noisy, variable handwriting while preserving the structural understanding from Stage 1.

**Curriculum learning** further structures training by organizing data from simple to complex using a complexity score based on sequence length, nesting depth, structural token count, and environment count. The sampling distribution shifts from 70% simple formulas in early epochs to 35% complex formulas in late epochs, ensuring clean gradient signals during initial convergence.

### Sections in this Chapter

| Section | Title | Key Topics |
|---------|-------|------------|
| 1 | Batched Greedy Decoding | Greedy token selection, batched inference, no error recovery |
| 2 | Beam Search Decoding | K-beam maintenance, length penalty, beam pruning, ExpRate improvement |
| 7.3 | Two Stage Pretraining and Curriculum Learning | Stage 1 (printed), Stage 2 (handwritten), curriculum complexity scoring, epoch schedule, differential learning rates, catastrophic forgetting prevention |

---
