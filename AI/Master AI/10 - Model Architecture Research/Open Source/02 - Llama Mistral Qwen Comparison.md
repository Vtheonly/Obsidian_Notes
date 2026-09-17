---
tags: [model-arch-research, llama, mistral, qwen, architecture]
iteration: 2
created: 2026-08-07
aliases: [Llama Mistral Qwen Architecture Comparison]
---

# 02 - Llama, Mistral, Qwen Architecture Comparison

> [!info] TL;DR
> The three dominant open-source LLM families (Llama, Mistral, Qwen) share the same core recipe (RMSNorm + SwiGLU + RoPE + GQA) but differ in details: Mistral adds sliding window attention; Qwen emphasizes multilingual; Llama popularized the recipe. All **Officially Confirmed** via technical reports.

## The Common Recipe (2024+)

All three families have converged on:
- **Pre-norm** with **RMSNorm**.
- **SwiGLU** FFN (with $d_{ff} \approx \frac{8}{3} d_{model}$).
- **RoPE** positional encoding.
- **GQA** attention (grouped-query).
- **No bias** in linear layers.
- **Final norm** after the last block.

This is the **Llama recipe**, adopted by Mistral, Qwen, Gemma, and most modern open LLMs.

## Llama (Meta)

### Llama 1 (Feb 2023)
- 7B / 13B / 33B / 65B.
- Introduced the modern recipe (RoPE, RMSNorm, SwiGLU).
- MHA (no GQA).

### Llama 2 (Jul 2023)
- 7B / 13B / 70B.
- 70B uses GQA.
- Commercial license.
- Llama 2 Chat: RLHF-aligned.

### Llama 3 (Apr 2024)
- 8B / 70B / 405B.
- All sizes use GQA.
- RoPE base 500000 (for 8k→128k extension).
- Vocabulary: 128k (larger than Llama 2's 32k).
- Llama 3.1: 128k context. Llama 3.2: multimodal. Llama 3.3: improved 70B.

### Llama 4 (2025–2026, if released)
- Likely MoE (based on Meta research papers).
- Native multimodal.

## Mistral

### Mistral 7B (Sep 2023)
- 7B params.
- **Sliding Window Attention** (window=4096) in all layers.
- GQA.
- RoPE.
- Strong performance per parameter.

### Mixtral 8x7B (Dec 2023)
- MoE: 8 experts, top-2 routing, 47B total params, 13B active.
- SWA + GQA.
- Apache 2.0 license.

### Mixtral 8x22B (Apr 2024)
- Bigger MoE: 141B total, 39B active.

### Mistral Large / Nemo / Small 3
- Commercial models, dense.
- Mistral Small 3 (2025): competitive with Llama 3.3 70B at 24B params.

## Qwen (Alibaba)

### Qwen 2 / 2.5 (2024)
- Sizes: 0.5B / 1.5B / 7B / 14B / 32B / 72B.
- Strong multilingual (Chinese, English, code, math).
- GQA, RoPE, SwiGLU.
- Specialized variants: Qwen-Math, Qwen-Coder, Qwen-VL.

### Qwen 2.5 Max / Qwen 3 (2025)
- MoE variants (Qwen 2.5 Max).
- Longer context (1M tokens in some variants).
- Reasoning models (QwQ).

## Comparison Table

| Feature              | Llama 3 8B  | Mistral 7B  | Qwen 2.5 7B |
|----------------------|-------------|-------------|-------------|
| Parameters           | 8B          | 7B          | 7B          |
| Layers               | 32          | 32          | 28          |
| Hidden dim           | 4096        | 4096        | 3584        |
| Attention            | GQA         | GQA + SWA   | GQA         |
| Q heads / KV heads   | 32 / 8      | 32 / 8      | 28 / 4      |
| RoPE base            | 500000      | 1000000     | 1000000     |
| Vocab                | 128k        | 32k         | 152k        |
| Context              | 128k (3.1+) | 32k (SWA-based) | 128k+  |
| Norm                 | RMSNorm     | RMSNorm     | RMSNorm     |
| FFN                  | SwiGLU      | SwiGLU      | SwiGLU      |

All three are **architecturally very similar**. Differences are in scale, hyperparameters, training data, and specific features (SWA, vocab size).

## Worked Example

```python
# All three load the same way
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

for model_id in [
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen/Qwen2.5-7B-Instruct",
]:
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, torch_dtype=torch.bfloat16, device_map="auto",
        attn_implementation="flash_attention_2",
    )
    # Same API; same usage pattern.
```

## Why This Matters for AI

- The architectural convergence means you can **swap between Llama / Mistral / Qwen with minimal code changes**. Choose based on quality, cost, license, and ecosystem.
- For **multilingual** (especially Chinese): Qwen typically wins.
- For **maximum efficiency at small scale**: Mistral (SWA helps).
- For **broad ecosystem and tooling**: Llama (largest community).
- For **commercial use without restrictions**: Llama 3 has a permissive license (with caveats for >700M MAU).

## Production Implications

- **Default to Llama 3.1 8B** for small, **Llama 3.1 70B** for medium, **Llama 3.1 405B** for large. Solid all-around.
- **For Chinese / Asian markets**, use Qwen.
- **For very long context with memory constraints**, use Mistral (SWA) or Llama 3.1 (with YaRN).
- **For multi-tenant serving**, all three work with vLLM, TGI, TensorRT-LLM.
- **Fine-tune compatibility**: LoRA / QLoRA / DPO all work the same across the three families.

## Common Pitfalls

- **Mixing up base and instruct versions** — base models don't follow instructions.
- **Wrong RoPE config** — each model has its own `rope_theta`. Don't mix.
- **Wrong chat template** — each model has its own. Use `tokenizer.apply_chat_template`.
- **Forgetting SWA on Mistral** — some serving frameworks default to full attention; explicitly enable SWA.
- **Vocab size differences** — tokenizers aren't interchangeable.

## Further Reading

- Touvron et al. (2023), *Llama 2 paper*.
- Jiang et al. (2023), *Mistral 7B*.
- Bai et al. (2023), *Qwen Technical Report*.

## See Also

- [[01 - DeepSeek Architecture]]
- [[07 - Transformers/Decoder Models/09 - GPT Family Evolution|GPT Family Evolution]]
- [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA|GQA MQA MLA]]
- [[10 - Model Architecture Research/MOC|Model Architecture Research MOC]]
