## 9.4 Why norm-first Matters at Scale

### The Original Transformer: Post-Norm

In the original "Attention Is All You Need" paper, Layer Normalization was applied after the residual connection:

$$x_{out} = \text{LayerNorm}(x + \text{Sublayer}(x))$$

This is called **Post-Norm** or **Post-LN** architecture.

**The problem with Post-Norm in deep networks:**

Consider the gradient flow through a 10-layer Post-Norm decoder during backpropagation. The gradient at layer $l$ depends on the gradient at layer $l+1$ multiplied by the Jacobian of layer $l$'s operations. In a deep Post-Norm network, these Jacobians can have eigenvalues either very large (gradient explosion) or very small (gradient vanishing).

The LayerNorm in Post-Norm is placed after the residual addition, which means it normalizes the combined output. But during the backward pass, the gradient flows through the LayerNorm's normalization operation, which can still produce vanishing gradients in the sub-components.

Empirically: Post-Norm networks of depth 6 or less train stably. At depth 8+, training often requires careful learning rate warmup schedules and is sensitive to hyperparameter choices. At depth 12+, Post-Norm training commonly diverges without extensive tuning.

### Pre-Norm: Your Architecture's Choice

Your architecture uses `norm_first=True` in PyTorch's `nn.TransformerDecoderLayer`. This implements **Pre-Norm** or **Pre-LN**:

$$x_{out} = x + \text{Sublayer}(\text{LayerNorm}(x))$$

The LayerNorm is applied to $x$ before the sublayer computation, and the result is added back to the unnormalized $x$.

**Why Pre-Norm is more stable:**

The critical difference is in the gradient of the residual connection. In Pre-Norm, the gradient through the residual path is:

$$\frac{\partial x_{out}}{\partial x} = I + \frac{\partial}{\partial x}\text{Sublayer}(\text{LayerNorm}(x))$$

The identity matrix $I$ ensures that the gradient always has a direct path from the output back to the input, regardless of what the Sublayer gradient contributes. Even if the Sublayer Jacobian is very small (vanishing), the gradient still flows through the $I$ term. Even if it is very large (exploding), the $I$ term provides a baseline stable signal.

This is the mathematical reason why Pre-Norm enables training much deeper networks. With Pre-Norm, 10-layer, 20-layer, and even 100-layer Transformer decoders can be trained stably without gradient instability.

**The practical consequence for TAMER:**

Your 10-layer decoder with `norm_first=True` trains stably under:
- Batch size 864 (very large batch, larger gradient variance per step).
- BFloat16 precision (lower numerical precision, more rounding in arithmetic).
- Learning rates up to $3 \times 10^{-4}$ (higher LR increases gradient magnitude).

Any of these three factors would likely cause gradient instability in a Post-Norm equivalent. Together, all three simultaneously would almost certainly cause a Post-Norm model to diverge within the first few hundred steps.

> **Important reminder:** Pre-Norm has one known trade-off compared to Post-Norm. Pre-Norm models sometimes achieve slightly lower final accuracy than equivalent Post-Norm models, when training is done very carefully and slowly (low LR, small batch). Post-Norm, at its best, can produce slightly better representations. For TAMER's scale (large batch, high LR, BFloat16), Pre-Norm is strictly superior in practice because Post-Norm simply does not converge reliably under these conditions.

---