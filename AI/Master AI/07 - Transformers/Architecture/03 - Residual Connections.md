---
tags: [transformer, architecture, residual, skip-connection]
iteration: 1
created: 2026-08-07
---

# Residual Connections

> [!info] TL;DR
> A residual (skip) connection adds the input of a sublayer to its output: $\mathbf{y} = \mathbf{x} + \text{Sublayer}(\mathbf{x})$. This gives gradients a direct path backward, making deep networks trainable. Without residuals, Transformers beyond ~10 layers don't converge.

## Definition

A residual connection (He et al., 2016 — ResNet) wraps a sublayer as:

$$
\mathbf{y} = \mathbf{x} + \text{Sublayer}(\mathbf{x})
$$

In Transformers, both sublayers (attention and FFN) are wrapped in residuals:

$$
\mathbf{h} = \mathbf{x} + \text{MHA}(\text{Norm}(\mathbf{x}))
$$

$$
\mathbf{y} = \mathbf{h} + \text{FFN}(\text{Norm}(\mathbf{h}))
$$

See [[Transformer Block]].

## Why Residuals Matter

### 1. Gradient highway

In a deep network without residuals, the gradient must pass through every layer's derivative. By the chain rule, this multiplies many Jacobians:

$$
\frac{\partial L}{\partial \mathbf{x}_0} = \frac{\partial L}{\partial \mathbf{x}_N} \prod_{l=1}^{N} \frac{\partial \mathbf{x}_l}{\partial \mathbf{x}_{l-1}}
$$

If each $\frac{\partial \mathbf{x}_l}{\partial \mathbf{x}_{l-1}}$ has norm < 1, the product → 0 (vanishing gradient). If > 1, it → ∞ (exploding gradient).

With residuals, $\mathbf{x}_l = \mathbf{x}_{l-1} + \text{Sublayer}(\mathbf{x}_{l-1})$, so $\frac{\partial \mathbf{x}_l}{\partial \mathbf{x}_{l-1}} = I + \frac{\partial \text{Sublayer}}{\partial \mathbf{x}_{l-1}}$. The identity $I$ gives gradients a direct path backward, bypassing the sublayer's derivative.

### 2. Incremental learning

The sublayer learns the **delta** from the input — what to add. This is easier to learn than the full transformation. Early in training, sublayers can be near-identity (small weights) and the network behaves like a shallow model. As training progresses, sublayers learn richer transformations.

### 3. Identity initialization is natural

A network of pure residual blocks initialized with zero sublayer weights is the identity function. Training then "adds complexity" incrementally. This is a much better starting point than a random initialization.

## Visual

```
Without residual:              With residual:

  x → Sublayer → y              x ──────────────┐
                                                v
                                Sublayer → +  → y
                                            ^
                                            │
                                            └─ (from x)
```

## Worked Implementation

```python
# A residual block in PyTorch
class ResidualBlock(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.norm = nn.LayerNorm(d)
        self.sublayer = SomeSublayer(d)
    
    def forward(self, x):
        # Pre-norm residual
        return x + self.sublayer(self.norm(x))
```

## Variants

### Standard residual
$$
\mathbf{y} = \mathbf{x} + \text{Sublayer}(\mathbf{x})
$$

### Gated residual (rare)
$$
\mathbf{y} = \mathbf{x} + g \cdot \text{Sublayer}(\mathbf{x})
$$
where $g$ is a learned gate (scalar or per-channel). Lets the model turn off a sublayer. Rare in Transformers.

### Multi-scale residual (rare)
Residuals that combine multiple skip lengths. Used in some computer vision architectures; not common in NLP Transformers.

### Dense connections (DenseNet-style)
Concatenate the input with the output instead of adding. Used in some encoder designs; not in standard Transformers.

## Why This Matters for AI

- Residuals are **essential** for training deep Transformers. The deepest current LLMs have 100+ layers; without residuals, none would train.
- The residual highway is also where **information accumulates** across layers. Token representations "evolve" by adding successive sublayer contributions.
- [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic interpretability]] often analyzes the residual stream — treating it as the "main memory" of the network and each sublayer as a "read-modify-write" operation on that memory. This is a powerful conceptual frame.

## Residual Stream as Memory (Analogical Intuition)

A useful way to think about a Transformer (from Anthropic's interpretability work):

- The **residual stream** is a memory bus running through the model.
- Each **attention head** reads from the stream (Q, K, V projections) and writes to it (output projection).
- Each **FFN** reads from the stream and writes to it.
- The model's computation is a sequence of read-modify-write operations on this shared memory.

This perspective explains why residual connections are so important — they're not just a training trick, they're the model's memory architecture.

## Production Implications

- Residual connections add **zero parameters** and negligible compute (just an addition). Always include them.
- For inference, residuals are easy to fuse with adjacent operations in custom kernels.
- **Gradient checkpointing** works by recomputing the residual sublayer's output during the backward pass. The residual itself is trivially recomputable (just save the input).
- **Speculative decoding** uses the residual stream structure — when a draft model's prediction matches the target, you can skip ahead through the residual stream computation.

## Common Pitfalls

- **Forgetting the residual** — a "Transformer block" without residuals is just an MLP+attention MLP, and it won't train past a few layers.
- **Wrong dimension** — the sublayer's output must match the input's dimension for the addition. Always check shapes.
- **Adding normalization in the residual path** — in pre-norm, the residual is clean (no norm). Putting a norm in the residual path is "post-norm" or "sandwich-norm", which is a different architecture. Be intentional.

## Further Reading

- He et al. (2016), *Deep Residual Learning for Image Recognition* (ResNet) — the original.
- Veit et al. (2016), *Residual Networks Behave Like Ensembles of Relatively Shallow Networks*.
- Anthropic's "Mathematical Framework for Transformer Circuits" — residual stream as memory.

## See Also

- [[Transformer Block]]
- [[Pre-Norm vs Post-Norm]]
- [[Normalization Layers]]
- [[07 - Transformers/MOC|Transformers MOC]]
- [[Backpropagation]] — residuals give gradients a shortcut
