## 1. Convolutional vs Transformer Vision Models

### The CNN Approach to Vision

Convolutional Neural Networks (CNNs, e.g., ResNet, VGG) process images using a sliding window of learned filters. A filter of size $3 \times 3$ pixels slides over the entire image, computing a dot product at every position.

The CNN's strength: it is inherently **local**. A filter learns to detect local patterns like edges, corners, curves. These local patterns are then hierarchically combined in deeper layers to form higher-level concepts.

The CNN's critical weakness for math OCR: **limited receptive field**.

Consider detecting a matched pair of parentheses in a wide formula:
$$( a + b + c + d + e + f + g + h + i + j + k )$$

The opening `(` is at the far left. The closing `)` is at the far right. They must match. A CNN needs many layers to propagate information from one end of the image to the other, and the signal degrades with each layer through mechanisms of vanishing gradients. CNNs are historically poor at these long-range spatial relationships.

---

### The Self-Attention Mechanism: Full Derivation

The Transformer's core innovation is the **Scaled Dot-Product Self-Attention** mechanism, which allows every position to directly communicate with every other position in one operation.

Given an input sequence $X \in \mathbb{R}^{N \times D}$ (N patches, each with D-dimensional features), we compute three matrices:

$$Q = X W_Q, \quad K = X W_K, \quad V = X W_V$$

Where $W_Q, W_K, W_V \in \mathbb{R}^{D \times d_k}$ are learned weight matrices.

The attention output is:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

**Step-by-step interpretation:**
1. $Q K^T$: Computes the dot product between every query-key pair. The $(i,j)$ entry measures "how relevant is patch $j$ to patch $i$?". Result shape: $N \times N$.
2. $/ \sqrt{d_k}$: Scaling factor. Without it, for large $d_k$, the dot products grow large and push softmax into saturation regions with vanishing gradients. $\sqrt{d_k}$ counteracts this.
3. $\text{softmax}(\cdot)$: Converts raw scores to a valid probability distribution over the $N$ patches. Each row sums to 1. This is called the "attention weight matrix".
4. $(\cdot) V$: Weighted sum of all value vectors. For each query position $i$, the output is a weighted blend of all $N$ value vectors, where the weights are the attention scores. Positions with high attention score contribute more to the output.

The result: every patch's output representation is a mixture of all other patches' content, weighted by learned relevance. This directly solves the long-range dependency problem.

---