---
tags: [transformer, components, ffn, swiglu, geglu]
iteration: 2
created: 2026-08-07
aliases: [Feed-Forward Network Deep, FFN]
---

# 05 - Feed-Forward Network (FFN) Deep Dive

> [!info] TL;DR
> The FFN sublayer is the "computation" half of every Transformer block (vs attention as the "routing" half). Two linear layers with a nonlinearity in between, expanded to 4x the model dimension. Modern LLMs use SwiGLU or GEGLU instead of plain ReLU/GELU. ~2/3 of a Transformer's parameters live in FFNs.

## The Standard FFN

For input $\mathbf{x} \in \mathbb{R}^d$:

$$
\text{FFN}(\mathbf{x}) = \mathbf{W}_2 \, \sigma(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1) + \mathbf{b}_2
$$

- $\mathbf{W}_1 \in \mathbb{R}^{d_{ff} \times d}$ — projects up to the FFN hidden dim.
- $\sigma$ — activation (ReLU in original, GELU in BERT/GPT, SwiGLU in Llama).
- $\mathbf{W}_2 \in \mathbb{R}^{d \times d_{ff}}$ — projects back to model dim.
- $d_{ff} \approx 4d$ — the "expansion ratio."

This is applied **position-wise**: each token's vector goes through the same FFN independently. There's no cross-token interaction in the FFN (that's attention's job).

## Parameter Count

For a Transformer with $d_{model}$ hidden dim and $d_{ff} = 4 d_{model}$ FFN:

- Attention parameters: $\approx 4 d_{model}^2$ (Q, K, V, O projections).
- FFN parameters: $2 \cdot d_{model} \cdot d_{ff} = 8 d_{model}^2$.

**The FFN is 2/3 of the parameters.** This is why quantization and pruning of FFN layers has the most impact on model size.

## Activation Choices

### ReLU (original Transformer)
$$
\text{FFN}(\mathbf{x}) = \mathbf{W}_2 \max(0, \mathbf{W}_1 \mathbf{x})
$$
Simple, fast, but can produce "dead" neurons.

### GELU (BERT, GPT-2)
$$
\text{FFN}(\mathbf{x}) = \mathbf{W}_2 \, \text{GELU}(\mathbf{W}_1 \mathbf{x})
$$
Smoother than ReLU. See [[04 - Neural Networks/Foundations/02 - Activation Functions|Activation Functions]].

### SwiGLU (Llama, Mistral, Gemma, Qwen)
$$
\text{FFN}(\mathbf{x}) = \mathbf{W}_3 \, (\text{Swish}(\mathbf{W}_1 \mathbf{x}) \odot \mathbf{W}_2 \mathbf{x})
$$

Three weight matrices instead of two. The $\mathbf{W}_2 \mathbf{x}$ is a "gate" that controls which dimensions of $\text{Swish}(\mathbf{W}_1 \mathbf{x})$ pass through. Empirically better than GELU at scale.

To keep parameter count comparable, the hidden dim is reduced by factor $2/3$: $d_{ff} = \frac{8}{3} d_{model}$ (so $3 \cdot d \cdot \frac{8}{3}d = 8d^2$, same as GELU's $2 \cdot d \cdot 4d$).

### GEGLU
Same as SwiGLU but with GELU instead of Swish:
$$
\text{FFN}(\mathbf{x}) = \mathbf{W}_3 \, (\text{GELU}(\mathbf{W}_1 \mathbf{x}) \odot \mathbf{W}_2 \mathbf{x})
$$
Comparable performance to SwiGLU. Used in some models.

## Worked Implementation

```python
import torch.nn as nn
import torch.nn.functional as F

class GELUFFN(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff)
        self.w2 = nn.Linear(d_ff, d_model)
    
    def forward(self, x):
        return self.w2(F.gelu(self.w1(x)))

class SwiGLUFFN(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        # d_ff should be 2/3 of 4*d_model for parameter parity with GELU
        self.w1 = nn.Linear(d_model, d_ff, bias=False)
        self.w2 = nn.Linear(d_ff, d_model, bias=False)
        self.w3 = nn.Linear(d_model, d_ff, bias=False)  # the gate
    
    def forward(self, x):
        # Swish(W1 x) ⊙ W3 x, then W2
        return self.w2(F.silu(self.w1(x)) * self.w3(x))
```

## Why the FFN Matters

### 1. It's where knowledge is stored
Mechanistic interpretability work ([[14 - Interpretability/MOC|14 Interpretability]]) suggests that FFNs act as **key-value memories**: $\mathbf{W}_1$ detects patterns (keys), $\mathbf{W}_2$ produces outputs (values). The model stores factual knowledge in FFN weights.

### 2. It's the parameter bulk
Most of a Transformer's parameters are in FFNs. This is where:
- Quantization gives the biggest memory savings.
- Pruning has the most impact.
- MoE (Mixture of Experts) replaces one FFN with many — scaling parameters without scaling compute.

### 3. It enables per-token computation
Attention routes information across tokens; FFN transforms each token independently. This separation is what makes the Transformer block work — you need both.

## Mixture-of-Experts FFN

In MoE models (Mixtral, DeepSeek-V3), the FFN is replaced by $E$ parallel FFN "experts" plus a router:

$$
\text{MoE}(\mathbf{x}) = \sum_{i=1}^{E} g_i(\mathbf{x}) \cdot \text{FFN}_i(\mathbf{x})
$$

where $g_i(\mathbf{x})$ is the router's gating for expert $i$. Typically only top-2 experts are activated per token, so compute is ~2 FFNs but parameters are $E$ FFNs.

This decouples parameter count from compute — you can have 8x more parameters at the same compute cost. See [[15 - Mixture of Experts Transformer|MoE Transformer]] (planned).

## Why This Matters for AI

- The FFN is **half of every Transformer block**. Understanding it is essential.
- Modern LLMs universally use SwiGLU or GEGLU. If you read model configs, you'll see these terms.
- For inference cost, FFN is the bulk of compute. Optimizing FFN (quantization, MoE, sparsity) has the biggest impact.
- For interpretability, FFN is where the model "stores" knowledge — making it the target of editing and unlearning research.

## Production Implications

- **SwiGLU FFN is standard** for new model designs. Don't use plain ReLU FFN.
- **FFN quantization** gives the biggest memory savings. INT4 FFN weights with FP16 attention is a common pattern.
- **MoE models** are increasingly common (Mixtral, DeepSeek-V3) — they swap one FFN for many, getting more parameters at the same compute.
- **FFN is fully parallel across positions** during prefill — unlike attention, no $n^2$ cost. This means prefill is mostly FFN-bound.

## Common Pitfalls

- **Wrong FFN hidden dimension for SwiGLU** — must be $\frac{2}{3} \cdot 4 d_{model}$ (rounded to a multiple of 256 or so) for parameter parity.
- **Forgetting that FFN is position-wise** — if you accidentally mix positions, you break the architecture.
- **Bias terms** — modern LLMs (Llama, Mistral) often omit bias in FFN. Match the model's choice.
- **Not using fused kernels** — naive PyTorch SwiGLU is slow. Use fused implementations from vLLM / FlashAttention / PyTorch 2+.

## Further Reading

- Shazeer (2020), *GLU Variants Improve Transformer* (SwiGLU, GEGLU).
- Geva et al. (2021), *Transformer Feed-Forward Layers Are Key-Value Memories* (interpretability).
- Shazeer et al. (2017), *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer* (MoE).

## See Also

- [[01 - Transformer Block]]
- [[04 - Normalization Layers]]
- [[04 - Neural Networks/Foundations/02 - Activation Functions|Activation Functions]]
- [[15 - Mixture of Experts Transformer]] (planned)
- [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]] (planned)
- [[07 - Transformers/MOC|Transformers MOC]]
