---
tags: [inference, quantization, int8, int4, gptq, awq, gguf, fp8]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Quantization, GPTQ, AWQ, GGUF, INT8, INT4, FP8, SmoothQuant]
---

# 03 - Quantization (INT8, INT4, GPTQ, AWQ, GGUF, FP8)

> [!info] TL;DR
> Quantization reduces model precision (FP16 → INT8 → INT4) to cut memory and increase speed. Modern methods (GPTQ, AWQ, GGUF, FP8) preserve quality at 4-bit. **The biggest single inference optimization** — a 70B model goes from 140GB to 35GB at INT4. This note covers why quantize, the precision spectrum, quantization methods, what to quantize, quality impact, production patterns, common pitfalls, and decision frameworks.

## Why Quantize?

A 70B model in FP16: 140 GB of weights. Doesn't fit on a single 80GB H100.

- INT8: 70 GB. Fits on one H100.
- INT4: 35 GB. Fits on a 48GB GPU with room for KV cache.

Plus: lower memory bandwidth → faster inference. INT4 matmuls are 4× faster than FP16 (on supporting hardware).

### The Three Benefits

1. **Memory reduction**: lower precision = fewer bytes per parameter. Enables larger models on available GPUs.
2. **Speed improvement**: lower precision = faster matrix multiplications. Tensor Cores on H100 reach ~989 TFLOPs in FP8 vs ~1979 TFLOPs in FP4 (with sparsity).
3. **Energy reduction**: lower precision = less energy per operation. Important for large-scale deployment and edge inference.

### The Trade-off

Quantization reduces precision, which can hurt model quality. The art is finding the right balance:
- Too high precision: wastes memory and compute.
- Too low precision: quality degrades unacceptable.
- The sweet spot: 4-8 bits for most use cases.

Modern quantization methods (GPTQ, AWQ, FP8) preserve quality well at 4-8 bits, making the trade-off favorable for most production deployments.

## The Quantization Spectrum

| Precision | Bytes/param | 70B model size | 7B model size | Hardware support        |
|-----------|-------------|----------------|---------------|-------------------------|
| FP32      | 4           | 280 GB         | 28 GB         | All                     |
| FP16/BF16 | 2           | 140 GB         | 14 GB         | All GPUs                |
| FP8 (E4M3)| 1           | 70 GB          | 7 GB          | Hopper (H100)+, Ada     |
| INT8      | 1           | 70 GB          | 7 GB          | Most modern GPUs        |
| INT4      | 0.5         | 35 GB          | 3.5 GB        | Hopper, Ada, some older |
| INT3      | 0.375       | 26 GB          | 2.6 GB        | Limited                 |
| INT2      | 0.25        | 18 GB          | 1.8 GB        | Experimental            |

### Floating-Point Formats

- **FP32**: 1 sign + 8 exponent + 23 mantissa = 32 bits. The training default.
- **FP16**: 1 + 5 + 10 = 16 bits. Range ~6e-5 to ~65504. Requires loss scaling.
- **BF16**: 1 + 8 + 7 = 16 bits. Same range as FP32, lower precision. No loss scaling needed.
- **FP8 E4M3**: 1 + 4 + 3 = 8 bits. More precision, less range. Used for forward pass.
- **FP8 E5M2**: 1 + 5 + 2 = 8 bits. More range, less precision. Used for backward gradients.
- **FP4 E2M1**: 1 + 2 + 1 = 4 bits. Very low precision; experimental on Blackwell.

### Integer Formats

- **INT8**: 8-bit signed integer, range -128 to 127. Requires a scale factor to map to FP16 range.
- **INT4**: 4-bit signed integer, range -8 to 7. Even more aggressive scaling required.
- **INT2**: 2-bit, range -2 to 1. Mostly experimental.

Integer quantization requires a **scale factor** per tensor (or per group) that maps the integer range to the floating-point range. The scale is typically computed from the tensor's absmax.

## Quantization Methods

### Naive Round-to-Nearest (RTN)

Just round FP16 weights to INT8/INT4. Fast, simple, but loses significant quality at INT4.

```python
def quantize_rtn(weights, bits=8):
    """Naive round-to-nearest quantization."""
    if bits == 8:
        scale = weights.abs().max() / 127
        q = (weights / scale).round().clamp(-128, 127).to(torch.int8)
    elif bits == 4:
        scale = weights.abs().max() / 7
        q = (weights / scale).round().clamp(-8, 7).to(torch.int8)
    return q, scale

def dequantize(q, scale):
    return q.float() * scale
```

RTN is the baseline; everything else improves on it. At INT8, RTN is often acceptable. At INT4, RTN loses significant quality.

### GPTQ (Frantar et al., 2022)

**Post-training quantization** that uses second-order information to compensate for quantization error. Quantizes weights layer-by-layer, using the input activations to determine optimal quantization.

**How it works**:
1. For each layer, compute the Hessian of the loss with respect to the weights (using a calibration dataset).
2. Quantize weights one column at a time, using the Hessian to predict and compensate for the quantization error.
3. The compensation updates the remaining (not-yet-quantized) weights to offset the error introduced.

**Properties**:
- One-shot quantization (no training needed).
- Excellent quality at INT4 — near-FP16 perplexity.
- Supported by AutoGPTQ, vLLM, HuggingFace.
- Slow to apply (~hours for 70B).

**Use case**: production serving where quality matters and you can afford the upfront quantization time.

### AWQ (Lin et al., 2023)

**Activation-aware Weight Quantization**. Observes that not all weights are equally important — those that produce large activations matter more. AWQ scales these "salient" weights up before quantization (and scales them back at inference).

**How it works**:
1. Run the model on a calibration dataset and observe activation magnitudes.
2. Identify "salient" weight channels (those that produce large activations).
3. Scale these channels up before quantization (so they're better represented in INT4).
4. At inference, scale activations down to compensate.

**Properties**:
- One-shot quantization.
- Better than GPTQ on some benchmarks, comparable on others.
- Faster to apply than GPTQ.
- Supported by vLLM, HuggingFace.

**Use case**: production serving, especially when GPTQ is too slow to apply.

### GGUF (formerly GGML)

Format for **llama.cpp** — quantization designed for CPU and consumer GPU inference. Multiple precision options (Q4_K_M, Q5_K_M, Q8_0, etc.) with different quality/speed tradeoffs.

**Properties**:
- Block-wise quantization with per-block scales.
- Multiple variants: Q4_0 (basic 4-bit), Q4_K_M (4-bit with k-quant, mixed precision), Q5_K_M, Q8_0.
- Designed for CPU inference (SIMD-optimized).
- Works on consumer GPUs (CUDA, Metal, ROCm).

**Use case**: local / consumer-GPU inference. Ollama, LM Studio, and most local LLM tools use GGUF.

### FP8 (Hopper, Blackwell)

Native hardware support on H100 and B200. Two formats: E4M3 (more precision) and E5M2 (more range). Almost FP16 quality at half the memory.

**Properties**:
- Native hardware support (no software emulation).
- Used in training (FP8 training) and inference.
- Requires Hopper+ hardware.
- Supported by vLLM, TensorRT-LLM, TransformerEngine.
- Per-tensor or per-channel scaling for stability.

**Use case**: H100+ deployments where quality is critical. The new standard for Hopper-based production.

### SmoothQuant (Xiao et al., 2022)

For INT8 quantization of activations + weights. Smooths activation outliers (which cause quantization issues) by migrating difficulty from activations to weights.

**How it works**:
- Activations have outliers (a few very large values) that make INT8 quantization hard.
- SmoothQuant scales down the outlier channels in activations and scales up the corresponding weights.
- Result: both activations and weights are "smoother" and quantize better.

**Use case**: when you need to quantize activations (not just weights). Common for INT8 weight+activation quantization.

### QLoRA's NF4

4-bit NormalFloat — a quantization designed for normally-distributed weights. Used in QLoRA fine-tuning (see [[02 - QLoRA]]). Not typically used for inference (GPTQ/AWQ are better for serving).

**Properties**:
- 16 quantization levels optimized for the normal distribution of weights.
- Better than uniform INT4 for weight-only quantization.
- Used in QLoRA to enable fine-tuning of 70B models on a single 48GB GPU.

## What to Quantize

### Weights (Standard)

Most methods focus on weights. Weight quantization is straightforward because weights are static (known at quantization time).

- **Per-tensor**: one scale for the whole tensor. Simplest, lowest metadata overhead.
- **Per-channel**: one scale per output channel. Better quality, more metadata.
- **Per-group**: one scale per group of N elements. Balance between quality and metadata. GPTQ/AWQ typically use group size 128.

### Activations (Harder)

Activations depend on input, so they can't be pre-quantized. They must be quantized on-the-fly during inference.

- Harder because activation distributions vary with input.
- Outliers in activations cause quantization issues (SmoothQuant addresses this).
- Less common than weight quantization; usually only for INT8.

### KV Cache

INT8 or FP8 KV cache halves memory. Critical for long-context inference where the KV cache dominates memory.

- vLLM: `--kv-cache-dtype fp8`.
- TensorRT-LLM: native support.
- Quality impact: minimal (KV cache values are well-behaved).

For 128K context on Llama 3 8B: FP16 KV cache = 16 GB; FP8 KV cache = 8 GB. The difference determines whether you fit on one GPU.

### Optimizer State (Training)

FP8 optimizer state is a research area. Adam's m and v are 2× parameter count; quantizing them to FP8 halves their memory. Useful for training very large models.

- Less mature than inference quantization.
- Supported by some training frameworks (TransformerEngine).

## Worked Example (vLLM with AWQ)

```bash
# Serve an AWQ-quantized model with vLLM
vllm serve TheBloke/Llama-2-70B-Chat-AWQ \
    --quantization awq \
    --dtype half
```

Or in Python:

```python
from vllm import LLM, SamplingParams

llm = LLM(
    model="TheBloke/Llama-2-70B-Chat-AWQ",
    quantization="awq",
    dtype="float16",
    gpu_memory_utilization=0.9,
    max_model_len=4096,
)

sampling_params = SamplingParams(temperature=0.7, max_tokens=100)
outputs = llm.generate(["Hello!"], sampling_params)
```

For local use:

```bash
# Ollama with GGUF
ollama run llama3:8b-q4_K_M

# llama.cpp directly
./main -m llama-3-8b-q4_K_M.gguf -p "Hello!"
```

### Quantizing Your Own Model

```python
# GPTQ quantization with AutoGPTQ
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
from transformers import AutoTokenizer

model_path = "meta-llama/Llama-3-8B"
quant_path = "Llama-3-8B-GPTQ-4bit"

quant_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    desc_act=False,
)

tokenizer = AutoTokenizer.from_pretrained(model_path)
examples = load_calibration_data(tokenizer, n_samples=128, seq_len=512)

model = AutoGPTQForCausalLM.from_pretrained(model_path, quant_config)
model.quantize(examples)
model.save_quantized(quant_path)
```

## Quality Impact

| Method      | Bits | Perplexity change vs FP16 | Notes                          |
|-------------|------|---------------------------|--------------------------------|
| FP8         | 8    | <0.5%                     | Near-lossless.                 |
| INT8 (RTN)  | 8    | ~1%                       | Acceptable.                    |
| INT8 (SQ)   | 8    | <0.5%                     | Better than RTN.               |
| INT4 (RTN)  | 4    | Significant degradation   | Not recommended.               |
| INT4 (GPTQ) | 4    | ~1-2%                     | Excellent for 4-bit.           |
| INT4 (AWQ)  | 4    | ~1-2%                     | Comparable to GPTQ.            |
| INT4 (GGUF Q4_K_M) | 4 | ~2-3%                  | Good for local use.            |
| INT3 (GPTQ) | 3    | ~3-5%                     | Noticeable degradation.        |
| INT2        | 2    | Significant degradation   | Experimental.                  |

### Quality Varies by Task

Quantization impact varies by task:
- **Generation**: more sensitive (small errors compound).
- **Classification**: less sensitive (just need the right argmax).
- **Retrieval**: depends on the embedding model.
- **Math/code**: more sensitive (small numerical errors break correctness).

Always benchmark on your specific task, not just aggregate benchmarks.

## Why This Matters for AI

- Quantization is **the** biggest inference optimization. Without it, serving 70B models would require multi-GPU setups everywhere.
- The open-source ecosystem (vLLM, Ollama, llama.cpp) is built on quantization — most local LLM use is INT4.
- For production, quantization enables 4-8× more concurrent requests per GPU.
- FP8 is the new standard for Hopper+ — combines INT8's speed with FP16's quality.
- Quantization enables edge deployment (mobile, browser, embedded) where memory is constrained.

## Production Implications

- **For production serving**: use AWQ or GPTQ INT4 on vLLM. Best quality/speed/memory balance.
- **For local / consumer GPU**: use GGUF (Q4_K_M) with llama.cpp or Ollama.
- **For H100 clusters**: use FP8 (better quality than INT4, similar memory).
- **For 7B models**: INT8 is often enough; quality loss is minimal.
- **For 70B+ models**: INT4 is usually necessary to fit on available GPUs.
- **Always benchmark quality** on your specific task after quantization. Aggregate benchmarks may not reflect your use case.
- **KV cache quantization**: for long-context, also quantize the KV cache (FP8 or INT8). Often the difference between fitting and OOM.
- **Mixed precision**: some layers (e.g., embeddings, output projection) are more sensitive. Keep them in higher precision; quantize the rest.
- **Calibration data**: GPTQ/AWQ need calibration data. Use representative data from your domain; don't use random text.
- **Versioning**: store the quantization method with the model. A "GPTQ-4bit" model needs GPTQ inference; don't try to load it as AWQ.

## Common Pitfalls

- **Using RTN for INT4** — significant quality loss. Always use GPTQ/AWQ for INT4.
- **Forgetting to apply the same quantization to merged LoRA** — fine-tune in BF16, merge, then quantize for inference. Don't quantize before merging.
- **Mixing quantization formats** — a model quantized with AWQ needs AWQ inference. Don't try to load with GPTQ.
- **Ignoring activation quantization** — for some workloads, activations (not weights) are the bottleneck. Profile before assuming weights are the issue.
- **Wrong group size** — GPTQ/AWQ use block-wise quantization; smaller groups = better quality but more metadata. 128 is a common default.
- **Bad calibration data** — GPTQ/AWQ are only as good as their calibration data. Use representative data; don't use random text.
- **Forgetting KV cache quantization** — for long-context, weight quantization alone isn't enough. Quantize the KV cache too.
- **Numerical instability** — INT4 can produce NaNs in rare cases. Have a fallback to FP16.
- **Wrong dtype in serving** — vLLM/TGI need the right `quantization` and `dtype` flags. Mismatched flags cause errors or quality degradation.
- **Not benchmarking** — aggregate benchmarks don't reflect your task. Always benchmark on your specific workload.
- **Ignoring hardware support** — INT4 requires specific GPU features. Don't assume INT4 works on all GPUs.

## Decision Framework

| Use Case | Recommended Method | Why |
|----------|-------------------|-----|
| Production serving (H100) | FP8 | Best quality at INT8 memory |
| Production serving (A100) | AWQ INT4 | Best quality at INT4 memory |
| Production serving (consumer GPU) | GGUF Q4_K_M | Designed for consumer hardware |
| Local development | GGUF Q4_K_M | Easy to use with Ollama |
| Fine-tuning (memory-constrained) | QLoRA NF4 | Designed for training |
| Maximum quality | FP16/BF16 | No quantization |
| Maximum throughput | INT4 (AWQ or GPTQ) | Fastest matmuls |
| Long-context | INT4 weights + FP8 KV cache | Both matter |
| Edge / mobile | INT2/INT4 (experimental) | Memory-constrained |

## Interview Questions

- **Q: What's the difference between GPTQ and AWQ?**  
  A: GPTQ uses second-order information (Hessian) to compensate for quantization error, processing weights column-by-column. AWQ identifies "salient" weights (those producing large activations) and scales them up before quantization. Both achieve similar quality at INT4; AWQ is faster to apply.

- **Q: Why is INT4 RTN bad but INT4 GPTQ is good?**  
  A: RTN just rounds, losing information about which weights matter. GPTQ uses calibration data to identify important weights and compensates for the quantization error of those weights. The compensation preserves quality.

- **Q: How does FP8 differ from INT8?**  
  A: INT8 is a signed integer (-128 to 127) with a scale factor. FP8 is a floating-point format (E4M3 or E5M2) with exponent and mantissa. FP8 has better dynamic range and precision for the same 8 bits, but requires hardware support (Hopper+).

- **Q: How would you quantize a 70B model to fit on a single 80GB H100?**  
  A: Use FP8 for weights (70 GB) + FP8 KV cache. Total: ~70 GB weights + ~10 GB KV cache (for 8K context) = 80 GB. Just fits. For more context, use INT4 weights (35 GB) + FP8 KV cache.

- **Q: What is the KV cache, and why quantize it?**  
  A: The KV cache stores keys and values for all previous tokens during autoregressive generation. For long contexts (128K+), it can be larger than the model weights. Quantizing it to FP8/INT8 halves its memory, enabling longer contexts on the same GPU.

## Further Reading

- Frantar et al. (2022), *GPTQ: Accurate Post-Training Quantization*.
- Lin et al. (2023), *AWQ: Activation-aware Weight Quantization*.
- Xiao et al. (2022), *SmoothQuant: Accurate and Efficient Post-Training Quantization*.
- Micikevicius et al. (2022), *FP8 Formats for Deep Learning*.
- llama.cpp's GGUF documentation.
- Dettmers et al. (2023), *QLoRA: Efficient Finetuning of Quantized LLMs*.

## See Also

- [[02 - QLoRA|QLoRA (NF4 for training)]]
- [[02 - KV Cache Mechanics]] — what gets cached
- [[02 - PagedAttention]] — memory management for KV cache
- [[05 - Speculative Decoding]] — complementary inference optimization
- [[04 - Mixed Precision Training]] — training-side precision
- [[13 - Inference/MOC|Inference MOC]]
- [[08 - LLMs/MOC|LLMs MOC]]
