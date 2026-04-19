## 8.2 Performance and Complexity Analysis

### Complexity-Stratified Performance

The key claim of the TAMER architecture is that it maintains high accuracy across all complexity tiers, while standard sequence models' accuracy degrades significantly on complex structures.

Understanding why standard models fail on complex structures:

**The Attention Dilution Problem:**

In a 200-token sequence representing a large matrix, the decoder's cross-attention must correctly identify which image region corresponds to which matrix cell. With 200 tokens and a 256-patch image, the attention matrix has $200 \times 256 = 51,200$ entries. For the model to correctly attend to the right cell while generating each token, the attention weights for that specific region must dominate over the other 255 regions.

As matrix complexity increases, more tokens share visually similar surrounding context (multiple cells in the same column look visually similar). The attention mechanism struggles to disambiguate them. The model begins predicting content from the wrong cell, causing systematic column or row shifts.

TAMER's TAM provides an additional structural regularization signal: the model's attention patterns are implicitly regularized to be consistent with the predicted parent-child relationships. If the model predicts that token $i$ is the child of token $j$, the cross-attention at step $i$ should focus on the image region where token $j$'s referent is located. The TAM loss enforces this consistency, reducing attention dilution on complex matrices.

**Quantitative Performance Comparison:**

| Complexity Tier | Standard Transformer | TAMER |
|---|---|---|
| Tier 1 (Simple) | ~95% ExpRate | ~97% ExpRate |
| Tier 2 (Fractions, Integrals) | ~88% ExpRate | ~93% ExpRate |
| Tier 3 (Multi-line, Cases) | ~81% ExpRate | ~90% ExpRate |
| Tier 4 (Matrices, Deep Nesting) | ~67% ExpRate | ~85% ExpRate |

The gap between Standard Transformer and TAMER widens as complexity increases. This is precisely the expected behavior of an architecture that explicitly models mathematical structure.

### Computational Complexity Analysis

Understanding the computational cost of each component helps make informed deployment decisions:

**Swin Encoder Complexity:**

For an image of $H \times W$ pixels with patch size $p$ and window size $M$:

$$\text{Number of patches: } N = \frac{H \times W}{p^2}$$

$$\text{Swin Attention Complexity: } O\left(\frac{N \cdot M^2}{1}\right) = O(N \cdot M^2)$$

For TAMER's configuration ($H=256$, $W=1024$, $p=4$, $M=7$):
$$N = \frac{256 \times 1024}{16} = 16{,}384 \text{ patches}$$
$$\text{Complexity} = O(16{,}384 \times 49) = O(802{,}816)$$

Compare to standard ViT: $O(N^2) = O(268{,}435{,}456)$. Swin is approximately 334× more efficient.

**Decoder Attention Complexity:**

At decoding step $t$, with $N_{enc}$ encoder tokens and $t$ decoder tokens:

- Self-attention: $O(t^2)$ (quadratic in sequence length)
- Cross-attention: $O(t \cdot N_{enc})$ (linear in both)

For a 150-token formula with 256 encoder patches:
- Self-attention cost at step 150: $O(150^2) = O(22{,}500)$
- Cross-attention cost at step 150: $O(150 \times 256) = O(38{,}400)$

The decoder's total cost over all 150 steps: $\sum_{t=1}^{150} O(t^2) = O(T^3/3) = O(150^3/3) = O(1{,}125{,}000)$.

This $O(T^3)$ scaling is the reason very long formulas are expensive to decode and why maximum sequence length is capped (typically at 256 tokens).

**Beam Search Multiplier:**

Beam search with width $K$ multiplies all decoder costs by exactly $K$. For $K=5$:
- Self-attention: $O(5 \cdot T^3/3)$
- Cross-attention: $O(5 \cdot T \cdot N_{enc})$

For time-sensitive applications, the beam width is the most direct lever for trading accuracy against speed.

---