# Chapter 3: Sequence Modeling and The Decoder

## 4. Deep Dive: The 10-Layer Decoder Design

**Architectural Choices:**
We utilize a 10-layer standard Transformer Decoder with a hidden dimension (`d_model`) of 768 and 12 attention heads.
*   *Why 10 layers?* The encoder is massive (SwinV2-Base has ~88 million parameters). If the decoder is too shallow (e.g., 3 layers), it creates a bottleneck; it lacks the cognitive capacity to translate the rich visual features into complex LaTeX logic. 10 layers balances capacity with GPU memory constraints.
*   *Why dimension 768?* The SwinV2-Base outputs a channel dimension of 1024. We use a single linear projection layer (`nn.Linear(1024, 768)`) in the encoder to compress this down to match the decoder. 768 is highly divisible (by 12 heads = 64 dimensions per head), which is optimal for GPU memory alignment and Tensor Core utilization.

**The Pre-Norm Residual Stream:**
Inside `DecoderBlock`, the data flows through a specific path:
`x = x + Attention(LayerNorm(x))`
This means the main "trunk" of the network (the residual stream) is completely untouched by normalization or attention matrices. The attention heads merely *read* from the stream, calculate updates, and *add* them back. This allows the gradient from the loss function to flow unimpeded directly back to the 1st layer, solving the vanishing gradient problem in deep decoders.