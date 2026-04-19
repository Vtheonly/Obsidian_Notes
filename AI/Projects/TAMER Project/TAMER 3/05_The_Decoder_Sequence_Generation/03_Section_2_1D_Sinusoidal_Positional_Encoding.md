## 2. 1D Sinusoidal Positional Encoding

### Mathematical Definition

For the decoder, the positional encoding is fixed (not learned), using sine and cosine waves at different frequencies:

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i / d_{model}}}\right)$$

$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i / d_{model}}}\right)$$

Where:
- $pos$ is the position index in the sequence (0, 1, 2, ...).
- $i$ is the dimension index within the embedding (0, 1, ..., $d_{model}/2 - 1$).
- $d_{model}$ is the embedding dimension (e.g., 768).

---

### Why Sinusoidal and Why These Frequencies?

Each dimension of the positional encoding oscillates at a different frequency:
- Dimension 0 oscillates with period $2\pi$ (changes every 1 position).
- Dimension 768 oscillates with period $2\pi \times 10000$ (changes every ~62,832 positions).

This is similar to a binary counter where the lowest bit flips every 1 step and the highest bit flips every $2^{bits}$ steps, except it uses continuous sinusoids instead of binary.

The key property that motivated this design: for any fixed offset $k$, the position encoding at $pos + k$ can be expressed as a linear function of the position encoding at $pos$:

$$PE_{pos+k} = A_k \cdot PE_{pos}$$

Where $A_k$ is a fixed rotation matrix (independent of $pos$). This means the model can learn to compute relative distances just by applying a linear transformation. The model learns "token at position $t+5$ is an offset of 5 from token at position $t$" through learned attention weights, and the sinusoidal encoding makes this a linear problem.

**Why does this generalize to unseen lengths?**
A learned positional embedding only has entries for positions seen during training (e.g., up to length 256). If at inference time we encounter a formula with 300 tokens, positions 257-300 have no learned embedding. The sinusoidal encoding is a mathematical function defined for any $pos$, so it naturally extrapolates.

---