---
tags: [transformer, architecture, normalization, pre-norm, post-norm]
iteration: 1
created: 2026-08-07
---

# Pre-Norm vs Post-Norm

> [!info] TL;DR
> Where you put the normalization in a Transformer block matters enormously. The original Transformer used **post-norm** (norm after the residual) — unstable to train without warmup. Modern Transformers use **pre-norm** (norm before the sublayer) — much more stable and the modern default. A third variant, **sandwich-norm**, exists but is rare.

## The Two Designs

### Post-Norm (original Transformer, Vaswani et al. 2017)

$$
\mathbf{y} = \text{Norm}(\mathbf{x} + \text{Sublayer}(\mathbf{x}))
$$

The normalization is applied **after** adding the residual. This was the original design.

### Pre-Norm (GPT-2 onwards)

$$
\mathbf{y} = \mathbf{x} + \text{Sublayer}(\text{Norm}(\mathbf{x}))
$$

The normalization is applied **before** the sublayer. The residual path is "clean" — no normalization in the skip connection.

## Why Pre-Norm Won

The key difference: in pre-norm, the residual path is **uninterrupted**. Gradients can flow directly from the loss to any layer through the residual highway. In post-norm, every layer's output passes through a normalization, which breaks the clean gradient highway.

Concretely:

- **Post-norm**: gradients must pass through Norm's derivative at every layer. Norm's derivative can amplify or attenuate gradients unpredictably, causing instability. Deep post-norm Transformers (12+ layers) are very hard to train without careful warmup.
- **Pre-norm**: the residual is a clean identity path. Gradients flow freely. Training is much more stable, especially for deep models.

Xiong et al. (2020) showed formally that pre-norm's gradients are better-conditioned at initialization, explaining the empirical stability difference.

### The catch: pre-norm's "lazy" sublayers

A subtle downside of pre-norm: because the residual is the identity, the sublayer's contribution is "added on top" of an already-good representation. The sublayer can become **lazy** — learning only small corrections — and the model becomes effectively shallower than its layer count suggests. This is sometimes observed but usually outweighed by the stability benefits.

## The Third Variant: Sandwich-Norm

Some recent models (e.g., Microsoft's Turing-NLG, some Megatron variants) use **sandwich-norm**:

$$
\mathbf{y} = \text{Norm}_2(\mathbf{x} + \text{Sublayer}(\text{Norm}_1(\mathbf{x})))
$$

Normalization both before and after. Combines the stability of pre-norm with the regularization of post-norm. Rare in practice.

## Visual Comparison

```
Post-norm:                      Pre-norm:
  x ──┐                          x ──────────┐
      │                                       │
      v                                       v
  Sublayer                              Norm ──> Sublayer
      │                                       │
      v                                       v
      + <─── x                                 + <────────── x
      │                                       │
      v                                       │
    Norm                                       │
      │                                       │
      v                                       v
      y                                       y
```

## Worked Implementation

```python
class PostNormBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.attn  = MultiHeadAttention(d_model, n_heads)
        self.ffn   = FeedForward(d_model, d_ff)
    
    def forward(self, x):
        # Norm AFTER residual
        x = self.norm1(x + self.attn(x))
        x = self.norm2(x + self.ffn(x))
        return x

class PreNormBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.attn  = MultiHeadAttention(d_model, n_heads)
        self.ffn   = FeedForward(d_model, d_ff)
    
    def forward(self, x):
        # Norm BEFORE sublayer; residual is clean
        x = x + self.attn(self.norm1(x))
        x = x + self.ffn(self.norm2(x))
        return x
```

The difference is just where `norm` is called — but it changes training dynamics completely.

## Which Models Use What?

| Model         | Norm placement |
|---------------|----------------|
| Original Transformer (2017) | Post-norm |
| BERT (2018)   | Post-norm      |
| GPT-2 (2019)  | **Pre-norm**   |
| GPT-3 (2020)  | Pre-norm       |
| Llama 1/2/3   | Pre-norm (RMSNorm) |
| Mistral       | Pre-norm (RMSNorm) |
| Gemma         | Pre-norm (RMSNorm) |
| Qwen          | Pre-norm (RMSNorm) |
| DeepSeek      | Pre-norm (RMSNorm) |

**Pre-norm is universal in modern LLMs.** Post-norm survives only in BERT-family models for historical reasons.

## Why This Matters for AI

- If you train a Transformer from scratch, **always use pre-norm**. Post-norm will likely fail to converge without extensive warmup and tuning.
- Understanding the difference helps you read papers from the 2017–2019 era (which often used post-norm) without confusion.
- The choice of norm placement interacts with initialization, learning rate, and warmup length. Pre-norm is more forgiving — one of the reasons modern LLMs train more reliably than the original Transformer.

## Production Implications

- For inference, pre-norm vs post-norm doesn't matter much (same compute, same memory). The choice is a training-time decision.
- When fine-tuning a pretrained model, **preserve the original norm placement**. Don't try to "fix" it.
- For distributed training, pre-norm's stability matters more — large-batch training is inherently less stable, and pre-norm helps.

## Common Pitfalls

- **Mixing pre-norm and post-norm in the same model** — would be very confusing and probably broken. Pick one.
- **Forgetting the final norm** in pre-norm models — most pre-norm Transformers have a final LayerNorm/RMSNorm after the last block (because the last block's residual output is unnormalized). Don't forget it.
- **Wrong initialization for post-norm** — if you must use post-norm, you need careful initialization and long warmup.

## Further Reading

- Xiong et al. (2020), *On Layer Normalization in the Transformer Architecture* — formal analysis.
- Nguyen & Salazar (2019), *Transformers without Tears* — empirical study.
- Liu et al. (2020), *Understanding the Difficulty of Training Transformers* — more on stability.

## See Also

- [[Transformer Block]]
- [[Normalization Layers]]
- [[Residual Connections]]
- [[07 - Transformers/MOC|Transformers MOC]]
