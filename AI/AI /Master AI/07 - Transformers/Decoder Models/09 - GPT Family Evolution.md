---
tags: [transformer, decoder, gpt, llama, mistral]
iteration: 2
created: 2026-08-07
aliases: [GPT Family Evolution, GPT, Llama, Mistral]
---

# 09 - GPT Family Evolution

> [!info] TL;DR
> GPT (Generative Pre-trained Transformer) is the decoder-only architecture that powers modern LLMs. From GPT-1 (2018, 117M params) to GPT-4 (2023, ~1T params estimated) to modern open models (Llama 3, Mistral, DeepSeek, Qwen), the architecture has converged on a standard recipe: RMSNorm + SwiGLU + RoPE + GQA + pre-norm.

## The GPT Recipe

A modern decoder-only LLM has:

- **Token embeddings** (often untied from output).
- **N Transformer blocks**, each with:
  - Pre-norm (RMSNorm in modern models).
  - Causal multi-head self-attention (GQA in modern models).
  - Residual.
  - Pre-norm.
  - SwiGLU FFN.
  - Residual.
- **Final norm**.
- **Output projection** (linear to vocab).

Plus architectural choices:
- **RoPE** positional encoding (not learned absolute).
- **No bias terms** in linear layers (Llama, Mistral).
- **GQA** for inference efficiency.

This recipe was popularized by Llama (2023) and is now the default.

## The GPT Family

### GPT-1 (2018, 117M params)
- 12 layers, 768 dim, 12 heads.
- Learned positional embeddings.
- Pre-norm.
- GELU activation.
- Demonstrated that pretraining + fine-tuning works for many tasks.

### GPT-2 (2019, 1.5B params)
- 48 layers, 1600 dim, 25 heads.
- Pre-norm (vs original Transformer's post-norm).
- Demonstrated zero-shot task transfer (no fine-tuning needed for some tasks).
- Initially deemed "too dangerous to release" by OpenAI.

### GPT-3 (2020, 175B params)
- Same architecture as GPT-2, just bigger.
- Demonstrated **few-shot in-context learning** — the model learns new tasks from a few examples in the prompt, without weight updates.
- Defined the "scale is all you need" era.

### GPT-3.5 / InstructGPT (2022)
- Same base architecture, but aligned with **RLHF** (PPO).
- The model behind ChatGPT (launched Nov 2022).
- Demonstrated that alignment transforms a base LM into a useful chatbot.

### GPT-4 (2023, architecture not officially disclosed)
- **MoE** (strong inference, not officially confirmed).
- **Multimodal** (vision input).
- Tool use, function calling, structured outputs.
- Significantly stronger reasoning than GPT-3.5.

### GPT-4o / o1 / o3 (2024–2025)
- GPT-4o: native multimodal (audio + vision + text in one model).
- o1: **reasoning model** — extended internal CoT via test-time compute.
- o3: further reasoning improvements.

## Open-Source LLMs

### Llama family (Meta)
- **Llama 1** (Feb 2023): 7B/13B/33B/65B. RoPE, RMSNorm, SwiGLU. The kick-off of the open LLM era.
- **Llama 2** (Jul 2023): same architecture, more data, commercial license. 70B uses GQA.
- **Llama 3** (Apr 2024): 8B/70B/405B. GQA across all sizes, RoPE base 500000 for 8k→128k extension.
- **Llama 3.1/3.2/3.3** (2024): multilingual, multimodal, longer context.

### Mistral
- **Mistral 7B** (Sep 2023): introduced SWA (sliding window attention), GQA.
- **Mixtral 8x7B** (Dec 2023): MoE, 8 experts with top-2 routing.
- **Mixtral 8x22B** (Apr 2024): bigger MoE.
- **Mistral Large / Nemo**: commercial models.

### DeepSeek
- **DeepSeek-V2** (2024): introduced MLA (Multi-head Latent Attention). MoE.
- **DeepSeek-V3** (2024): 671B params (37B active). Auxiliary-loss-free MoE load balancing.
- **DeepSeek-R1** (Jan 2025): open-source reasoning model trained with RL on verifiable rewards.

### Qwen (Alibaba)
- **Qwen 2 / 2.5** (2024): strong multilingual, code, math models.
- **Qwen 3** (2025, planned): rumored to add linear attention hybrids.

### Gemma (Google)
- **Gemma 1 / 2 / 3** (2024–2025): Google's open weights, derived from Gemini research.
- Gemma 2 uses alternating SWA + full attention.

## Architectural Evolution

| Feature                | GPT-2 (2019) | GPT-3 (2020) | Llama 2 (2023) | Llama 3 (2024) | DeepSeek-V3 (2024) |
|------------------------|--------------|--------------|----------------|----------------|---------------------|
| Norm                   | LayerNorm    | LayerNorm    | RMSNorm        | RMSNorm        | RMSNorm             |
| Norm placement         | Pre-norm     | Pre-norm     | Pre-norm       | Pre-norm       | Pre-norm            |
| Activation             | GELU         | GELU         | SwiGLU         | SwiGLU         | SwiGLU              |
| Positional             | Learned abs  | Learned abs  | RoPE           | RoPE           | RoPE                |
| Attention              | MHA          | MHA          | GQA (70B)      | GQA            | MLA                 |
| Bias in linear layers  | Yes          | Yes          | No             | No             | No                  |
| Architecture type      | Dense        | Dense        | Dense          | Dense          | MoE                 |

The trend: simpler (no bias), more efficient (GQA, MLA), better positional encoding (RoPE with longer context), more parameters via MoE.

## Worked Example (Loading a Modern LLM)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
    device_map="auto",
)

inputs = tokenizer("Hello!", return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Why This Matters for AI

- The GPT family is **the** lineage of modern LLMs. Every chat model you use is descended from this lineage.
- The architectural convergence (RMSNorm + SwiGLU + RoPE + GQA) means a single recipe works across many model families. You can switch between Llama, Mistral, Qwen, Gemma with minimal code changes.
- Understanding the evolution helps you read model cards and configs — `rope_theta`, `num_key_value_heads`, `hidden_act` all make sense once you know the architecture.
- For inference, the modern recipe (GQA especially) is what makes consumer-GPU inference feasible.

## Production Implications

- **Default to a modern Llama-family model** (Llama 3.1, Mistral, Qwen 2.5) for most applications. They're well-supported, efficient, and competitive.
- **DeepSeek-V3** for cost-sensitive MoE workloads — extremely cheap per token.
- **GPT-4 / Claude / Gemini** for closed-source quality peaks.
- For new model training, **follow the Llama recipe** unless you have a specific reason to deviate.

## Common Pitfalls

- **Mixing up base vs instruct models** — base models don't follow instructions; use `-Instruct` variants for chat.
- **Forgetting the chat template** — each model has its own. Use the tokenizer's `apply_chat_template` to apply it correctly.
- **Wrong `rope_theta`** when extending context — use the model's specified value.
- **Assuming GPT-4 is open** — it's not. Open-source alternatives are Llama, Mistral, DeepSeek, Qwen.

## Further Reading

- Radford et al. (2018), *Improving Language Understanding by Generative Pre-Training* (GPT-1).
- Radford et al. (2019), *Language Models are Unsupervised Multitask Learners* (GPT-2).
- Brown et al. (2020), *Language Models are Few-Shot Learners* (GPT-3).
- Touvron et al. (2023), *LLaMA* and *Llama 2*.
- DeepSeek-AI (2024), *DeepSeek-V3 Technical Report*.

## See Also

- [[01 - Transformer Block]]
- [[07 - BERT]]
- [[12 - T5 and BART]]
- [[15 - Mixture of Experts Transformer]]
- [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA|GQA/MQA/MLA]]
- [[10 - Model Architecture Research/MOC|Model Architecture Research MOC]]
- [[07 - Transformers/MOC|Transformers MOC]]
