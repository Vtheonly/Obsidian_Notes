# Chapter 4: The Encoder - Vision Transformers (Swin-v2)

---

## Chapter Introduction

This chapter covers the visual encoding pipeline — how TAMER transforms raw pixel data into the spatial feature representations that the decoder will later read from. It also extends into the critical training mechanisms for the decoder's sequence generation.

The chapter opens with a comparison between **CNNs and Transformers** for vision. CNNs process images through local sliding filters, which makes them inherently strong at detecting local patterns (edges, corners) but weak at capturing long-range spatial relationships. A CNN needs many layers to propagate information from an opening parenthesis on the far left to a closing parenthesis on the far right, and the signal degrades through vanishing gradients. The Transformer's self-attention mechanism solves this by allowing every position to directly communicate with every other position in a single operation, regardless of distance.

However, standard Vision Transformers (ViT) apply global self-attention across all patches, resulting in $O(N^2)$ complexity that is computationally impossible for TAMER's 16,384-patch feature maps. The **Swin Transformer v2** solves this with **window-based attention**: attention is computed only within local windows of size $M \times M$, reducing complexity from $O(N^2)$ to $O(N \cdot M^2)$ — a 334x improvement. The **shifted window mechanism** alternates window positions between layers, allowing information to propagate globally despite local computation.

Swin-v2 introduces two key improvements over v1: **scaled cosine attention** (more stable when fine-tuning at different resolutions) and **log-spaced continuous positional bias** (smooth extrapolation to larger inputs).

The chapter then extends into decoder-related topics that are critical for training: **2D positional encoding** for the encoder (separate learned row and column embeddings concatenated to form spatial coordinates), and three sections on decoder training challenges:

- **Teacher Forcing and Exposure Bias** (Section 4.6): Why training with ground-truth context creates a distribution mismatch at inference time, and how TAMER mitigates this with grammar masks, beam search, and scheduled sampling.
- **Scheduled Sampling** (Section 4.7): The inverse sigmoid decay schedule that gradually introduces the model's own predictions as context during training.
- **The Full Decoder Training Loop** (Section 4.8): End-to-end walkthrough of the complete training loop.

### Sections in this Chapter

| Section | Title | Key Topics |
|---------|-------|------------|
| 1 | Convolutional vs Transformer Vision Models | CNN receptive field limitations, self-attention full derivation, scaled dot-product attention |
| 2 | Swin Transformer v2 Architecture | Quadratic complexity problem, window-based attention, shifted window mechanism, v2 improvements |
| 3 | 2D Positional Encoding and Spatial Awareness | Why Transformers need positional encoding, factored learned 2D encoding, parameter efficiency |
| 4.6 | Teacher Forcing and Exposure Bias | Training vs inference discrepancy, error cascade, grammar mask mitigation, beam search defense |
| 4.7 | Scheduled Sampling: Bridging the Training-Inference Gap | Inverse sigmoid decay schedule, mixed teacher forcing implementation, straight-through estimator |
| 4.8 | The Full Decoder Training Loop End to End | Complete training loop walkthrough, step-by-step |

---
