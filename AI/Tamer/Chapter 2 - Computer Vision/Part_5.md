# Chapter 2: Computer Vision and The Encoder

## 11. The SwinV2 Advantage: Solving the Resolution-Stability Paradox

In your project, the transition from standard backbones to **SwinV2** was the primary driver of your "close to SOTA" performance. Regular CNNs and even SwinV1 often fail at the 384x1280 resolution required for math. Here is why SwinV2 worked.

**1. The Scaled Cosine Attention (SCA):**
In standard Transformers (including SwinV1), attention is calculated using the Dot Product: $QK^T$. As the model grows or the resolution increases, the values in the attention matrix can become extremely large. This pushes the Softmax function into its "saturated" regions, where gradients are nearly zero. 
*   **The V2 Fix:** SwinV2 uses **Scaled Cosine Attention**. Instead of a raw dot product, it calculates the cosine similarity between the Query and Key:
    $$\text{Attention}(Q, K) = \frac{\cos(\theta)}{\tau}$$
    where $\tau$ is a learnable scaling parameter. Because a cosine is mathematically bounded between -1 and 1, the attention scores can *never* explode. This provided the "Vibe-Coding" stability you observed—the model doesn't crash or produce NaNs even during high-LR training.

**2. Log-Spaced Continuous Position Bias (Log-CPB):**
Math equations are often very wide but short. SwinV1 used a fixed-size "bias table" for positions. If you trained on a square image and tried to run inference on your wide 1280px image, the model would become "disoriented" because the relative positions were outside its table.
*   **The V2 Fix:** SwinV2 uses a small Neural Network (an MLP) to generate positional biases. It uses **Log-spaced coordinates**, which means it perceives distance on a logarithmic scale. This allows the model to "extrapolate" its understanding of space. It can handle the massive 1280px width even if it only saw shorter equations during early curriculum training.

**3. Hierarchical Windowing for "Ink-Dense" Regions:**
Unlike a regular ViT which looks at the whole image as a flat sequence, SwinV2 acts like a microscope. 
*   **Stage 1 & 2:** These layers focus on small 4x4 and 8x8 pixel patches. This is where the model learns the "shape" of a character (the curve of an `\int` or the cross of a `+`).
*   **Stage 3 & 4:** These layers merge those small patches into larger semantic blocks. This is where the model learns that a horizontal line with a character above it and a character below it constitutes a `\frac`.
This hierarchical structure is perfectly suited for LaTeX, which is fundamentally a hierarchical language (superscripts inside fractions inside square roots).
