# Chapter 3: Sequence Modeling and The Decoder

## 5. Decoder Architecture: The 10-Layer Sequential Decoding Tower

Your decoder is a **Transformer Decoder** consisting of 10 identical blocks.

**Structure of a Single Block:**
Each of your 10 blocks contains exactly four primary components:
1.  **Masked Multi-Head Self-Attention:** This allows the decoder to look at the tokens it has already generated. It ensures the LaTeX syntax is correct (e.g., if it just output `\begin{matrix}`, it knows it must eventually output `\end{matrix}`).
2.  **Multi-Head Cross-Attention:** This is the "bridge." The decoder uses its current state as a **Query** to look at the Encoder's $12 \times 40$ feature grid (**Keys** and **Values**). This is where the model "looks" at the ink to decide which symbol to write next.
3.  **Position-Wise Feed-Forward Network (FFN):** A two-layer MLP that processes the attention output. 
4.  **Layer Normalization:** Applied *before* each sub-layer (Pre-Norm architecture) to keep gradients stable.

**The Output Head:**
After the 10th block, the tensor passes through a final LayerNorm and an `output_proj` (`nn.Linear(768, vocab_size)`). This maps the 768-dimensional latent vector back into the probability of each token in your vocabulary (approx. 500-1000 tokens).

## 6. Dimensional Rationale: The Math of 768 and 3072

You did not choose these numbers at random; they follow the mathematical "Power of 2" logic optimized for NVIDIA hardware.

*   **$d_{model} = 768$:** 
    *   *Why?* This is the "Standard Base" dimension. It is large enough to represent complex math but small enough to fit 36 images in 96GB VRAM. 
    *   *Head Logic:* You have 12 attention heads. $768 / 12 = 64$. 64 is a "magic number" for GPU kernels (WARP size is 32). An attention head dimension of 64 is perfectly optimized for the way CUDA handles memory coalescing.
*   **$dim_{feedforward} = 3072$:**
    *   *Why?* Transformers traditionally use an FFN expansion ratio of **4x**. $768 \times 4 = 3072$. 
    *   *Reasoning:* The attention layers find *relationships* between tokens, but the FFN layers are where the *knowledge* is stored. The 4x expansion allows the model to project features into a higher-dimensional space where they are linearly separable before compressing them back down.
