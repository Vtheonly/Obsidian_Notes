# Chapter 9: The Complete Architecture Blueprint

---

## Chapter Introduction

This chapter is the definitive technical reference for the TAMER architecture as implemented in the codebase. Every box in the architecture diagram corresponds to a real class, method, or operation; every arrow represents a tensor transformation with explicit shapes tracked throughout. The goal is that after reading this chapter, you can mentally simulate a complete forward pass without running the code.

The chapter begins with the **Master Architecture Diagram** (Section 9.1), which maps the entire system across four phases: the Input Pipeline, the Swin-v2 Vision Encoder, the Spatial Bridge and Boundary Injection, and the Transformer Decoder with output projection and inference.

Section 9.2 traces the **layer-by-layer tensor flow** through every mathematical transformation — from raw pixel normalization through the Swin backbone's four hierarchical stages, through the spatial bridge (projection, LayerNorm, 2D positional encoding), and into the decoder's stacked attention layers.

Section 9.3 provides a deep dive into the **Row Boundary Marker**, the architectural innovation that replaces the Tree-Aware Module. Instead of making the decoder infer row transitions entirely from text context, the encoder literally marks where each visual row ends in the spatial memory by computing row summary vectors, projecting them through an MLP, and interleaving boundary markers between visual rows. The decoder's cross-attention learns to attend to these markers when generating `\\` tokens.

Section 9.4 explains why **Pre-Norm (`norm_first=True`)** is essential for training stability at TAMER's scale (10-layer decoder, batch size 864, BFloat16 precision). Pre-Norm guarantees a direct identity-mapping path for gradients through the residual connection, preventing the vanishing gradient problem that makes Post-Norm diverge at this depth and scale.

Section 9.5 provides the **complete forward pass specification** with every intermediate tensor shape tracked explicitly for both the encoder and decoder.

Section 9.6 compares the **training loop vs inference loop side by side**, highlighting the critical differences (teacher forcing vs autoregressive, parallel vs sequential, grammar masks on/off, augmentation on/off, model.train() vs model.eval()).

Section 9.7 specifies the **Grammar State Machine** in full detail — the per-beam Python state machine that tracks brace depth, argument stacks, environment stacks, and matrix column counts to enforce structurally valid LaTeX output at inference time.

### Sections in this Chapter

| Section | Title | Key Topics |
|---------|-------|------------|
| 9.1 | The Master TAMER Architecture Diagram | Full system diagram across 4 phases: Input, Encoder, Bridge, Decoder, Output |
| 9.2 | Layer-by-Layer Tensor Flow and Mathematics | Pixel normalization, patch partition, 4 Swin stages, spatial bridge, projection, LayerNorm |
| 9.3 | The Row Boundary Marker: Deep Dive | Row mean computation, boundary projection MLP, row_boundary_base, interleaving operation, 264-token memory |
| 9.4 | Why norm_first Matters at Scale | Post-Norm gradient instability, Pre-Norm identity mapping, practical convergence at depth 10 + BFloat16 |
| 9.5 | The Complete Forward Pass | Every tensor, every shape — encoder (B x 264 x 768) and decoder (B x T x 522) traced step by step |
| 9.6 | The Training Loop vs Inference Loop: Side by Side | Teacher forcing vs autoregressive, grammar masks, augmentation, model.eval() requirements |
| 9.7 | The Grammar State Machine: Full Specification | Brace depth, argument stack, environment stack, matrix constraints, per-beam state, EOS suppression |

---
