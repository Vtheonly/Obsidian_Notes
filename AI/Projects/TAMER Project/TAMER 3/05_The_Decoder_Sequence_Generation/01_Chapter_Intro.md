# Chapter 5: The Decoder - Sequence Generation

---

## Chapter Introduction

This chapter details the Transformer Decoder, the component of TAMER responsible for generating the LaTeX token sequence one token at a time. While the encoder processes the entire image once and produces a spatial feature map (the "memory matrix"), the decoder iteratively reads from this memory and produces a probability distribution over the vocabulary at each step, autoregressively building the output sequence.

Each Transformer Decoder layer contains **three sub-layers**, each followed by Layer Normalization and a residual connection:

1. **Masked Self-Attention**: The decoder attends to the sequence of tokens it has already generated. The causal mask ensures position $t$ cannot see positions $t+1, t+2, \ldots$ — preserving the autoregressive property even though the entire target sequence is processed in one parallel forward pass during training.

2. **Cross-Attention**: The decoder's query vectors attend to the encoder's key and value vectors. This is how the model "looks at" the image while deciding what token to write next — analogous to how a human moves their eyes to the relevant part of a formula while transcribing it.

3. **Feed-Forward Network**: A position-wise fully connected network ($768 \to 3072 \to 768$) that provides non-linear transformation capacity. Without the FFN, the decoder would be limited to linear recombinations of features.

The chapter also covers **1D sinusoidal positional encoding** for the decoder, which injects sequential position information into the token embeddings. Unlike the encoder's learned 2D embeddings, the decoder uses fixed sinusoidal functions that provide unique "fingerprints" for every position and support the relative position property: $PE_{pos+k}$ can be expressed as a linear transformation of $PE_{pos}$.

Finally, the chapter introduces **autoregressive teacher forcing**, the training strategy where the model always receives the correct ground-truth context rather than its own predictions. This enables massive parallelization (all $T$ positions computed in one forward pass) and clean gradient signals, but introduces exposure bias — the subject of a deeper treatment in Chapter 4.6.

### Sections in this Chapter

| Section | Title | Key Topics |
|---------|-------|------------|
| 1 | Transformer Decoder Architecture | Three sub-layers (masked self-attention, cross-attention, FFN), residual connections, LayerNorm |
| 2 | 1D Sinusoidal Positional Encoding | Sin/cos derivation, relative position property, generalization to unseen lengths, token embedding addition |
| 3 | Autoregressive Teacher Forcing | Parallelized training, causal mask, teacher forcing benefits and exposure bias introduction |

---
