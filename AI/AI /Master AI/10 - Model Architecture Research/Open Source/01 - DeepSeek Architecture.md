---
tags: [model-arch-research, deepseek, mla, moe]
iteration: 2
created: 2026-08-07
aliases: [DeepSeek Architecture]
---

# 01 - DeepSeek Architecture (V2/V3/R1)

> [!info] TL;DR
> DeepSeek-V2 introduced MLA (Multi-head Latent Attention) and V3 added auxiliary-loss-free MoE load balancing. These innovations made DeepSeek-V3 (671B params, 37B active) cheaper to serve than dense 70B models. R1 is V3 with reasoning training. **Officially Confirmed** in DeepSeek technical reports.

## MLA: Multi-head Latent Attention

Standard attention caches K and V per head — the KV cache grows linearly with both sequence length and number of heads. GQA reduces this by sharing K/V across head groups. MLA goes further.

### The Compression Trick

MLA compresses K and V into a **low-rank latent vector**:

$$
\mathbf{c}_t = \mathbf{W}_{DKV} \mathbf{x}_t \quad \text{(down-project to latent, dim } d_c \ll h \cdot d_k\text{)}
$$

The latent $\mathbf{c}_t$ is what's cached. At attention time, K and V are reconstructed:

$$
\mathbf{K}_t = \mathbf{W}_{UK} \mathbf{c}_t, \quad \mathbf{V}_t = \mathbf{W}_{UV} \mathbf{c}_t
$$

### The Absorb Trick

Reconstructing K every step is expensive. MLA's key insight: the K projection $\mathbf{W}_{UK}$ can be **absorbed into Q's projection** at the start of attention. The attention computation becomes:

$$
\text{scores} = (\mathbf{Q} \mathbf{W}_{UK}) \mathbf{c}_t^T = \mathbf{Q}' \mathbf{c}_t^T
$$

So you don't need to reconstruct K — just compute $\mathbf{Q}'$ once at the start and use the latent $\mathbf{c}_t$ directly.

### KV Cache Savings

For DeepSeek-V2: latent dim $d_c = 512$, vs full K/V which would be $128 \cdot 128 = 16k$. ~32x reduction in KV cache.

This is what makes DeepSeek-V3 able to serve long contexts cheaply.

## DeepSeek-V3's MoE: Auxiliary-Loss-Free Load Balancing

### The Problem with Standard MoE
Standard MoE uses an auxiliary loss to balance expert utilization:

$$
L_{\text{aux}} = E \cdot \sum_i f_i \cdot P_i
$$

This competes with the main loss and can hurt quality.

### DeepSeek's Solution: Bias-Adjusted Routing

Instead of an auxiliary loss, DeepSeek-V3 adds a per-expert **bias** to the router logits:

$$
\text{router}(\mathbf{x}) = \text{Softmax}(\text{TopK}(\mathbf{W}_g \mathbf{x} + \mathbf{b}))
$$

The bias $\mathbf{b}$ is **dynamically adjusted** based on recent expert load:
- If expert $i$ is overloaded → decrease $b_i$ (less likely to be picked).
- If expert $i$ is underloaded → increase $b_i$ (more likely).

This achieves load balancing without any auxiliary loss. Quality improves.

### Other V3 MoE Innovations
- **Fine-grained experts**: more, smaller experts (256 total) rather than fewer big ones.
- **Shared experts**: a few experts always active (route to them + top-k fine-grained). Captures common patterns.
- **Multi-token prediction (MTP)**: predict multiple future tokens during training — improves data efficiency.

## DeepSeek-R1: Reasoning on V3

R1 is V3 with reasoning training:
1. **R1-Zero**: pure RL on verifiable rewards (math correctness, code tests) — no SFT first. The model spontaneously develops long CoT.
2. **R1**: SFT on cold-start data, then RL. Better readability and safety.

R1 matches or beats o1 on most reasoning benchmarks. Full weights and recipe are open.

## Architecture Summary (DeepSeek-V3)

| Property             | Value                                              |
|----------------------|----------------------------------------------------|
| Total parameters     | 671B                                               |
| Active parameters    | 37B (per token)                                    |
| Layers               | 61                                                 |
| Hidden dim           | 7168                                               |
| Attention            | MLA (Multi-head Latent Attention)                  |
| MoE experts          | 256 routed + 1 shared                              |
| Active experts       | 8 routed + 1 shared                                |
| Positional           | RoPE                                               |
| Norm                 | RMSNorm (pre-norm)                                 |
| Activation           | SwiGLU                                             |

## Worked Example (Loading R1)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "deepseek-ai/DeepSeek-R1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="flash_attention_2",
)

# R1 produces reasoning_content + content
# Use the chat template
messages = [{"role": "user", "content": "Prove that √2 is irrational."}]
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True).to(model.device)
outputs = model.generate(inputs, max_new_tokens=8000)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

For serving: use vLLM with `--model deepseek-ai/DeepSeek-R1` and MoE + MLA support.

## Why This Matters for AI

- DeepSeek-V3/R1 showed that **frontier-quality open models are achievable** at low cost. The V3 training cost was ~$5.6M (vs hundreds of millions for GPT-4).
- MLA is a major architectural innovation — the first serious alternative to GQA for KV cache reduction.
- Auxiliary-loss-free balancing is a cleaner MoE training recipe that other models are adopting.
- R1's open recipe enabled a wave of open-source reasoning model research.

## Production Implications

- **DeepSeek-V3 / R1** are extremely cost-effective for their quality. Use them when serving cost matters.
- **MoE serving** requires expert parallelism across GPUs. vLLM and SGLang support this.
- **MLA support**: requires recent vLLM or SGLang. Check version compatibility.
- **Memory**: 671B params is too big for a single GPU. Multi-GPU (8x H100 or equivalent) is required.

## Common Pitfalls

- **Assuming MLA is the same as GQA** — it's fundamentally different (latent compression, not head sharing).
- **Forgetting to apply the absorb trick** — naive MLA is much slower.
- **Mixing up V3 base and R1** — R1 has reasoning training; V3 doesn't.
- **Trying to serve V3 on consumer GPUs** — won't fit; use the API or a serious cluster.

## Further Reading

- DeepSeek-AI (2024), *DeepSeek-V2 Technical Report* (MLA).
- DeepSeek-AI (2024), *DeepSeek-V3 Technical Report* (aux-loss-free MoE).
- DeepSeek-AI (2025), *DeepSeek-R1 Technical Report* (reasoning).

## See Also

- [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA|GQA MQA MLA]]
- [[07 - Transformers/Variants/15 - Mixture of Experts Transformer|MoE Transformer]]
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]]
- [[10 - Model Architecture Research/MOC|Model Architecture Research MOC]]
