---
tags: [transformer, moe, mixture-of-experts, mixtral, deepseek]
iteration: 2
created: 2026-08-07
aliases: [MoE Transformer, Mixture of Experts]
---

# 15 - Mixture-of-Experts (MoE) Transformer

> [!info] TL;DR
> MoE Transformers replace each FFN with multiple parallel FFN "experts" plus a router. Each token activates only 2 experts — so you get more parameters (more capacity) at the same compute cost. Mixtral 8x7B and DeepSeek-V3 are flagship MoE LLMs.

## The Idea

In a dense Transformer, each token goes through one FFN per layer. In an MoE Transformer, each token is routed to **a small subset** of $E$ parallel FFN "experts":

$$
\text{MoE}(\mathbf{x}) = \sum_{i=1}^{E} g_i(\mathbf{x}) \cdot \text{FFN}_i(\mathbf{x})
$$

where $g_i(\mathbf{x})$ is the router's gating for expert $i$. Typically only top-$k$ experts (usually $k=2$) have non-zero gates — so only $k$ FFNs are computed per token.

## The Router

The router is a small linear layer + softmax/top-k:

$$
\mathbf{g}(\mathbf{x}) = \text{Softmax}(\text{TopK}(\mathbf{W}_g \mathbf{x}))
$$

- $\mathbf{W}_g \in \mathbb{R}^{E \times d}$ maps the token to $E$ logits.
- TopK selects the top-$k$ (e.g., 2) experts.
- Softmax normalizes their gates (other experts get gate 0).

The router is the only MoE-specific learned component. The experts are just standard FFNs.

## Parameter and Compute Scaling

For an MoE with $E$ experts, top-$k$ routing, FFN hidden dim $d_{ff}$:

- **Parameters**: $E \cdot 2 \cdot d \cdot d_{ff}$ (E FFNs).
- **Compute per token**: $k \cdot 2 \cdot d \cdot d_{ff}$ (only k FFNs computed).

For Mixtral 8x7B ($E=8, k=2$): parameters are ~47B (8x the FFN), compute is ~13B (2x the FFN). You get a 47B-capacity model at the compute cost of a 13B dense model.

## Load Balancing: The Critical Problem

If the router sends all tokens to the same few experts, the others are wasted and the active experts are overworked. **Load balancing** ensures tokens are distributed evenly across experts.

### Auxiliary loss (original MoE)
Add a regularization term to the loss that penalizes imbalanced routing:

$$
L_{\text{aux}} = E \cdot \sum_{i=1}^{E} f_i \cdot P_i
$$

where $f_i$ is the fraction of tokens routed to expert $i$ and $P_i$ is the average gate probability for expert $i$. The loss is minimized when tokens are uniformly distributed.

This works but has problems: the auxiliary loss competes with the main loss and can hurt quality.

### Auxiliary-loss-free balancing (DeepSeek-V3)
DeepSeek-V3 introduced a clever alternative: **per-expert bias** that's adjusted based on recent load. If an expert is overloaded, its bias is decreased (fewer tokens routed to it); if underloaded, increased. No auxiliary loss needed.

This is one of DeepSeek-V3's key innovations and a reason it's so efficient.

## Worked Example (Mixtral-style)

```python
import torch.nn as nn
import torch.nn.functional as F

class MoELayer(nn.Module):
    def __init__(self, d_model, d_ff, n_experts=8, top_k=2):
        super().__init__()
        self.n_experts = n_experts
        self.top_k = top_k
        self.router = nn.Linear(d_model, n_experts, bias=False)
        self.experts = nn.ModuleList([
            SwiGLUFFN(d_model, d_ff) for _ in range(n_experts)
        ])
    
    def forward(self, x):
        # x: (B, T, d)
        B, T, D = x.shape
        x_flat = x.view(B * T, D)
        
        # Router logits and top-k selection
        router_logits = self.router(x_flat)  # (B*T, n_experts)
        gates, selected_experts = torch.topk(router_logits, self.top_k, dim=-1)
        gates = F.softmax(gates, dim=-1)  # (B*T, top_k)
        
        # Compute (in practice, this is batched by expert for efficiency)
        out = torch.zeros_like(x_flat)
        for i in range(self.top_k):
            for tok_idx in range(B * T):
                expert_idx = selected_experts[tok_idx, i].item()
                out[tok_idx] += gates[tok_idx, i] * self.experts[expert_idx](x_flat[tok_idx:tok_idx+1]).squeeze(0)
        return out.view(B, T, D)
```

Real implementations use grouped GEMM kernels and avoid the per-token Python loop.

## MoE Models

| Model              | Experts | Active | Total Params | Notes                              |
|--------------------|---------|--------|--------------|------------------------------------|
| Mixtral 8x7B       | 8       | 2      | 47B          | Top-2 routing, dense experts       |
| Mixtral 8x22B      | 8       | 2      | 141B         | Bigger version                     |
| DeepSeek-V2        | 160     | 6      | 236B         | Fine-grained experts, shared experts |
| DeepSeek-V3        | 256     | 8      | 671B         | Aux-loss-free balancing, 37B active |
| DeepSeek-R1        | 256     | 8      | 671B         | Reasoning model on V3 base         |
| Qwen-MoE           | 60      | 4      | 14B (3B active) | Fine-grained experts            |

## Why This Matters for AI

- MoE is **the** way to scale parameters without scaling compute. The biggest open models (DeepSeek-V3, Mixtral 8x22B) are MoE.
- The economics: MoE models are cheaper to **serve** than dense models of the same quality, because only a fraction of experts activate per token.
- MoE creates new system challenges: load balancing, expert parallelism, sparse gradient updates. The DeepSeek-V3 paper is essential reading for these.
- For inference, MoE models need careful **expert parallelism** (different experts on different GPUs) to fit in memory.

## Production Implications

- **For high-quality open models**, DeepSeek-V3 and Mixtral offer better quality-per-FLOP than dense models.
- **Memory**: MoE models need more total memory (all experts must be loaded) even though active compute is lower. Plan GPU memory accordingly.
- **Serving**: use vLLM or SGLang with MoE support. Expert parallelism across multiple GPUs is essential for large MoE.
- **Fine-tuning MoE**: possible but more complex. LoRA on MoE is supported by PEFT; usually applied to attention layers (not experts).
- **Routing bugs are silent** — if the router collapses (always picks the same experts), quality degrades without an obvious error. Monitor expert utilization.

## Common Pitfalls

- **Forgetting to monitor expert load** — if one expert gets 80% of tokens, your MoE is essentially a dense model with wasted parameters.
- **Wrong expert count** — too few experts = no benefit; too many = routing overhead and per-expert undertraining.
- **Inefficient routing implementation** — the naive per-token Python loop is 100x slower than grouped GEMM. Always use the framework's MoE kernel.
- **Forgetting to handle tokens that need to be re-routed** (when an expert is at capacity) — some MoE implementations drop tokens or re-route.

## Further Reading

- Shazeer et al. (2017), *Outrageously Large Neural Networks: The Sparsely-Gated MoE Layer*.
- Fedus et al. (2022), *Switch Transformers*.
- Jiang et al. (2024), *Mixtral of Experts*.
- DeepSeek-AI (2024), *DeepSeek-V2 / DeepSeek-V3 Technical Reports*.

## See Also

- [[05 - Feed-Forward Network Deep]]
- [[09 - GPT Family Evolution]]
- [[14 - GQA MQA MLA]] — DeepSeek also introduced MLA
- [[10 - Model Architecture Research/MOC|Model Architecture Research MOC]]
- [[07 - Transformers/MOC|Transformers MOC]]
