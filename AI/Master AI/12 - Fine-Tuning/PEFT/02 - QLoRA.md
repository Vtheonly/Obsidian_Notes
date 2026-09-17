---
tags: [fine-tuning, qlora, peft, quantization]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
---

# QLoRA

> [!info] TL;DR
> QLoRA (Dettmers et al., 2023) combines 4-bit NormalFloat quantization of the base model with LoRA fine-tuning. This lets you fine-tune a 65B model on a single 48 GB GPU. The trick: store base weights in 4-bit, but compute LoRA gradients in bf16 — only the tiny LoRA parameters are trained.

## The Problem LoRA Alone Doesn't Solve

LoRA reduces trainable parameters by 100x, but you still need to **load the base model in memory**. A 7B model in fp16 is 14 GB; in fp32 it's 28 GB. A 65B model is 130 GB in fp16. Even with LoRA, you need that much GPU memory just to load the base.

QLoRA solves this by **quantizing the base model to 4 bits** (4 GB for a 7B model, 33 GB for a 65B). The LoRA adapters are still trained in bf16.

## The Three Innovations

### 1. 4-bit NormalFloat (NF4)

A new quantization data type optimized for normally-distributed weights. Standard INT4 quantization assumes uniform distribution; NF4 is designed for the bell-curve distribution that neural network weights actually have.

NF4 has 16 quantization levels chosen so that the values are equally likely under a standard normal distribution. This minimizes quantization error for weight distributions that match (which most Transformer weights do, after normalization).

### 2. Double Quantization

Quantize the **quantization constants themselves**. Standard 4-bit quantization stores a per-block scaling factor (typically fp32, one per 64 weights). Double quantization stores these scaling factors as 8-bit integers (with their own scaling factor), saving ~0.5 bits per parameter on average.

Net effect: 4-bit + double quant ≈ 3.5 bits per parameter effective.

### 3. Paged Optimizers

Use NVIDIA's unified memory to handle the optimizer state's memory spikes. When the optimizer state would OOM, it pages to CPU memory and back. This prevents OOM during the backward pass when gradient moments are accumulated.

## How QLoRA Fits Together

```
Base model weights: stored in 4-bit NF4 (frozen)
LoRA adapters (A, B matrices): bf16, trainable
Optimizer state (Adam moments for A, B): bf16, paged
Forward pass:
  - Dequantize base weights to bf16 on-the-fly
  - Compute base layer output
  - Compute LoRA delta in bf16
  - Sum and continue
Backward pass:
  - Gradients to LoRA params in bf16
  - Base weights stay frozen (no gradients)
```

The dequantization happens on-the-fly per layer during the forward pass — you never materialize the full bf16 model in memory. This is the key memory saving.

## Memory Footprint

For Llama 2 7B (7 billion parameters):
- fp16 base: 14 GB
- 4-bit QLoRA base: ~3.5 GB
- LoRA adapters (r=16, all-linear): ~50 MB
- Optimizer state: ~200 MB
- Activations (batch 4, seq 2048): ~2 GB
- **Total: ~6 GB** → fits on a single 8 GB consumer GPU

For Llama 2 70B (70 billion parameters):
- 4-bit QLoRA base: ~35 GB
- LoRA + optimizer + activations: ~5 GB
- **Total: ~40 GB** → fits on a single 48 GB GPU (A6000, A100 80GB has plenty of room)

This is the breakthrough — fine-tuning a 70B model on a single GPU was previously impossible.

## Quality

QLoRA's quality is **nearly identical to full bf16 LoRA fine-tuning**. The 4-bit quantization adds a small amount of noise to the base model's forward pass, but this acts as a mild regularizer and doesn't hurt downstream task performance.

The original paper showed QLoRA matches full FT quality on a wide range of benchmarks (MMLU, GSM8K, etc.).

## Implementation

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# Load base model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto",
)

# Prepare for k-bit training (important — enables gradients, etc.)
model = prepare_model_for_kbit_training(model)

# Add LoRA
config = LoraConfig(
    r=16, lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, config)
```

Then train with the standard HuggingFace `Trainer`.

## Why This Matters for AI

- QLoRA **democratized LLM fine-tuning**. Before QLoRA, fine-tuning a 65B model required 8x A100 80GB (~$30k/month on cloud). After QLoRA, it requires a single 48GB GPU (~$2k/month or even a workstation).
- The "fine-tune a model on your laptop" use case is real — QLoRA lets you fine-tune 7B models on a single RTX 4090.
- QLoRA-based adapters can be **merged into the base model** for inference, just like regular LoRA. The merged model can then be served normally (the 4-bit quantization was only for training; the merged inference model can be any precision).
- QLoRA is the basis for most open-source fine-tuning today. Custom models on HuggingFace are typically trained with QLoRA.

## Production Implications

- **For custom fine-tuning**: always try QLoRA first. Only move to full FT if you have the compute and need the extra quality.
- **For inference**: QLoRA-trained adapters can be merged into the base model and served in any precision (fp16, INT8, INT4). The training-time quantization doesn't bind the inference-time choice.
- **For multi-tenant serving**: load multiple QLoRA-trained adapters on a single base model and swap per request. See vLLM's LoRA support.
- **For long-context training**: QLoRA + gradient checkpointing + small batch + gradient accumulation can fit surprisingly long contexts in modest memory.

## Common Pitfalls

- **Forgetting `prepare_model_for_kbit_training`** — without this, gradient checkpointing won't work correctly with quantized models.
- **Wrong `bnb_4bit_compute_dtype`** — should be `bfloat16` (or `float16`) for stability. Don't use `float32`.
- **Forgetting to merge for inference** — keeping the 4-bit base + LoRA separate at inference is slower than merging and serving in your target precision.
- **Mixing QLoRA with other quantization schemes** — once trained, the adapter is a regular LoRA adapter. Don't try to re-quantize the merged model with the same NF4 scheme — use a fresh quantization method (e.g., AWQ or GPTQ) for inference.
- **Too low rank for big domain shifts** — QLoRA's quantization noise slightly reduces adapter capacity. Use $r = 32$ or $r = 64$ if you see underfitting.

## Further Reading

- Dettmers et al. (2023), *QLoRA: Efficient Finetuning of Quantized LLMs*.
- `bitsandbytes` library: https://github.com/bitsandbytes-foundation/bitsandbytes
- HuggingFace docs: https://huggingface.co/docs/peft/en/developer_guides/quantization

## See Also

- [[LoRA]]
- [[DPO Derivation]]
- [[12 - Fine-Tuning/MOC|Fine-Tuning MOC]]
- [[13 - Inference/Quantization/03 - Quantization|Quantization]] (planned)


## Interview Questions

1. **Q: What are the three innovations in QLoRA?**
   A: (1) **4-bit NormalFloat (NF4)** — quantization type optimized for normally-distributed weights (16 levels chosen for equal likelihood under standard normal). (2) **Double Quantization** — quantize the scaling factors themselves to 8-bit, saving ~0.5 bits per parameter (effective ~3.5 bits). (3) **Paged Optimizers** — use NVIDIA unified memory to page optimizer state to CPU on OOM, preventing crashes during backward.

2. **Q: How does QLoRA achieve near-full-quality fine-tuning with 4-bit base weights?**
   A: The 4-bit quantization adds small noise to the base model's forward pass, but this acts as a mild regularizer. The LoRA adapters are trained in BF16, so the gradient computation is full-precision. The original paper showed QLoRA matches full BF16 LoRA quality on MMLU, GSM8K, and other benchmarks. The key: only the base is quantized; the trainable parameters are full-precision.

3. **Q: How much memory does QLoRA save?**
   A: For Llama 2 7B: fp16 base = 14 GB → 4-bit QLoRA base = ~3.5 GB. Total with LoRA + optimizer + activations: ~6 GB (fits on 8 GB consumer GPU). For 70B: 4-bit base = ~35 GB, total ~40 GB (fits on 48 GB GPU). This democratized LLM fine-tuning — 70B on a single GPU was previously impossible.

4. **Q: Can you use QLoRA-trained adapters with a different quantization at inference?**
   A: Yes. QLoRA-trained adapters are regular LoRA adapters. Merge them into the base model, then serve in any precision (fp16, INT8, INT4). The training-time NF4 quantization doesn't bind the inference-time choice. Use a fresh quantization method (AWQ, GPTQ) for inference.

5. **Q: What is `prepare_model_for_kbit_training` and why is it needed?**
   A: It prepares a quantized model for fine-tuning by: (1) enabling gradient computation through the quantized weights; (2) setting up input embedding gradient checkpointing; (3) ensuring the model is in training mode. Without it, gradient checkpointing won't work correctly with quantized models, and training silently fails.

6. **Q: When would you use QLoRA vs full fine-tuning?**
   A: Always try QLoRA first. Only move to full FT if: (1) you have the compute (multi-GPU); (2) QLoRA quality is insufficient; (3) the domain shift is large enough that the adapter capacity is the bottleneck. For most use cases (chat, instruction following, domain adaptation), QLoRA is sufficient and 10x cheaper.

## Connection to Other Concepts

- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] — the base method QLoRA builds on.
- [[12 - Fine-Tuning/DPO/04 - DPO Derivation|DPO]] — can be combined with QLoRA.
- [[13 - Inference/Quantization/03 - Quantization|Quantization]] — inference-time quantization (related but distinct).
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — BF16 compute dtype.
- [[27 - Projects/Capstones/07 - Build a Reasoning Model Fine-Tune|Reasoning Model Fine-Tune]] — uses QLoRA.
