---
tags: [framework, vllm, serving, inference, pagedattention]
iteration: 4
created: 2026-08-08
aliases: [vLLM, vLLM Framework, Inference Server]
---

# 07 — vLLM

> [!info] TL;DR
> vLLM is the dominant open-source LLM inference engine, built around PagedAttention (block-level KV cache management) and continuous batching. It delivers 2–4× higher throughput than naive serving, with prefix caching, tensor parallelism, and support for quantization. vLLM is the default choice for self-hosted LLM serving in 2024–2026 — if you're running an open-weights LLM in production, you're probably using vLLM.

## Overview

- **Developer**: UC Berkeley / vLLM project (2023, now community-maintained).
- **Language**: Python + CUDA kernels.
- **License**: Apache 2.0.
- **Status**: actively developed; the standard for open-source LLM serving.

## Why vLLM Exists

Before vLLM, serving LLMs was inefficient:
- Naive serving allocates a contiguous block of GPU memory per request, sized for the maximum sequence length. This wastes 60–80% of memory to internal fragmentation.
- Requests are batched statically — you wait to fill a batch, then process it together. This adds latency and underutilizes the GPU.
- KV cache cannot be shared across requests, even when they share prefixes (system prompts, few-shot examples).

vLLM (see [[10 - PagedAttention vLLM 2023|the paper]]) solved these with:
1. **PagedAttention**: block-level KV cache management (like OS paging).
2. **Continuous batching**: dynamic, per-iteration batching.
3. **Prefix caching**: share KV cache for common prefixes.

The result: 2–4× throughput improvement on the same hardware, with no quality loss (exact attention computation).

## Core Features

### PagedAttention
The KV cache is divided into fixed-size blocks (typically 16 tokens). Each request has a block table mapping its logical token positions to physical blocks. Blocks are allocated on demand and freed when the request completes.

Benefits:
- No internal fragmentation (only the last block in a request is partially unused).
- No external fragmentation (blocks are allocated from a pool).
- Blocks can be shared across requests (for common prefixes).

See [[02 - PagedAttention]] and [[10 - PagedAttention vLLM 2023]] for details.

### Continuous Batching
At every decoding step, vLLM can:
- Admit new requests (if KV blocks are available).
- Evict completed or preempted requests.
- Reorder requests to maximize GPU utilization.

Unlike static batching (which waits to fill a batch), continuous batching processes whatever is currently active. This dramatically reduces latency for mixed workloads.

### Prefix Caching
vLLM caches the KV blocks for recently seen prompts. If a new request's prompt starts with a cached prefix, the prefix blocks are reused without recomputation.

For chat applications (where each turn repeats the prior conversation), this gives large latency and compute savings — often 50–80% reduction in prefill compute for subsequent turns.

### Tensor Parallelism
For models that don't fit on one GPU, vLLM supports tensor parallelism — splitting each layer's matrices across GPUs. Requires fast GPU-to-GPU interconnect (NVLink preferred).

```bash
# Launch with 4-way tensor parallelism
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4
```

### Quantization
vLLM supports multiple quantization formats:
- **INT8**: 2× memory reduction, minimal quality loss.
- **INT4** (GPTQ, AWQ): 4× memory reduction, small quality loss.
- **FP8** (Hopper GPUs): 2× throughput on H100.
- **GGUF**: for CPU inference (limited support).

Quantization lets you run larger models on smaller GPUs. A 70B model in INT4 fits on a single 80GB GPU; in FP16 it needs 2 GPUs.

### LoRA Serving
vLLM can serve multiple LoRA adapters from a single base model. This is the "one base model + many adapters" deployment pattern:
- Load the base model once.
- Load multiple LoRA adapters (each is small, ~100MB).
- Route requests to the appropriate adapter based on the request.

This is dramatically more efficient than serving each adapter as a separate model.

### OpenAI-Compatible API
vLLM's server implements the OpenAI API:
- `/v1/chat/completions` — chat completions.
- `/v1/completions` — text completions.
- `/v1/embeddings` — embeddings (if the model supports them).

This means any code written for OpenAI works with vLLM by changing the `base_url`.

### Streaming
vLLM supports streaming responses via Server-Sent Events (SSE), compatible with the OpenAI streaming format.

## Usage

### As a Server
```bash
# Start the server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --port 8000

# Use it like OpenAI
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [{"role": "user", "content": "Hello"}]
    }'
```

### As a Library
```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3.1-8B-Instruct")
sampling_params = SamplingParams(temperature=0.7, max_tokens=100)

outputs = llm.generate(["Hello, how are you?"], sampling_params)
print(outputs[0].outputs[0].text)
```

### With Tensor Parallelism
```python
llm = LLM(
    model="meta-llama/Llama-3.1-70B-Instruct",
    tensor_parallel_size=4,
    quantization="awq",  # INT4 quantization
)
```

### With LoRA Adapters
```python
from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest

llm = LLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    enable_lora=True,
    max_loras=4,
    max_lora_rank=16,
)

outputs = llm.generate(
    prompts=["Customer question..."],
    sampling_params=SamplingParams(),
    lora_request=LoRARequest(lora_name="customer_support", lora_int_id=1, lora_local_path="/path/to/lora"),
)
```

## Performance

Typical throughput improvements over naive serving (HuggingFace Transformers):

| Model         | HF Transformers | vLLM  | Speedup |
|---------------|-----------------|-------|---------|
| Llama-7B      | 1.0×            | 3.5×  | 3.5×    |
| Llama-13B     | 1.0×            | 3.0×  | 3.0×    |
| Llama-70B     | 1.0×            | 2.5×  | 2.5×    |

With prefix caching on chat workloads, additional 1.5–2× throughput (because subsequent turns reuse the prefix).

## Strengths

### Performance
vLLM is the fastest open-source LLM server for most workloads. PagedAttention + continuous batching + prefix caching together deliver 2–4× over naive serving.

### OpenAI Compatibility
The OpenAI-compatible API means existing code works without modification. This is a huge adoption advantage — you can switch from OpenAI to self-hosted vLLM by changing one URL.

### Model Support
vLLM supports most popular open-weights models: Llama, Mistral, Qwen, DeepSeek, Gemma, Phi, and many more. New models are added quickly after release.

### Quantization Support
Multiple quantization formats (INT8, INT4, FP8) let you trade quality for memory/throughput. This is essential for running large models on limited hardware.

### LoRA Support
Multi-LoRA serving enables the "one base + many adapters" pattern, which is dramatically more efficient than serving each adapter separately.

### Active Development
vLLM has a large, active community. New features (FP8, speculative decoding, longer context) are added regularly.

## Weaknesses

### GPU-Specific
vLLM is optimized for NVIDIA GPUs. AMD support exists but is less mature. CPU inference is limited.

### Memory Overhead
vLLM's KV cache management has some overhead. For very small models or very short sequences, the overhead may exceed the benefits.

### Configuration Complexity
vLLM has many configuration options (block size, GPU memory utilization, max sequences, swap space). Tuning for optimal performance requires understanding these.

### No Training Support
vLLM is inference-only. For training or fine-tuning, use other frameworks (HuggingFace Transformers, PyTorch FSDP, DeepSpeed).

### Limited Long-Context Optimization
For very long contexts (>32K), vLLM's performance degrades. Specialized long-context servers (Ring Attention, distributed inference) may be better.

## Comparison to Alternatives

| Server           | Strengths                          | Weaknesses                       | Best For                          |
|------------------|------------------------------------|----------------------------------|-----------------------------------|
| vLLM             | Performance, OpenAI-compat, community | GPU-specific, config complexity  | Most production serving           |
| TGI (HuggingFace)| Production features, simple        | Slower than vLLM                 | HuggingFace ecosystem users       |
| TensorRT-LLM     | NVIDIA-optimized, fastest on H100  | Complex setup, NVIDIA-only       | Maximum performance on NVIDIA     |
| Ollama           | Simple, local, CPU+GPU             | Not for high-throughput serving  | Local development, small scale    |
| llama.cpp        | CPU, mobile, embedded              | Low throughput                   | Edge devices, local use           |

vLLM is the default for production serving. TensorRT-LLM may be faster on H100 but is harder to use. Ollama and llama.cpp are for local/edge use.

## Production Patterns

### Right-Size GPU Memory Utilization
vLLM's `gpu_memory_utilization` parameter controls how much GPU memory is used for KV cache. Set it high enough to maximize throughput but low enough to leave room for other processes:

```bash
--gpu-memory-utilization 0.9  # use 90% of GPU memory
```

### Enable Prefix Caching
For chat applications, enable prefix caching (`--enable-prefix-caching`). This gives 1.5–2× throughput on multi-turn conversations.

### Use Quantization for Large Models
For models that don't fit on your GPUs in FP16, use quantization:
- INT8 for 2× reduction (minimal quality loss).
- AWQ or GPTQ INT4 for 4× reduction (small quality loss).
- FP8 on H100 for 2× throughput.

### Monitor Queue Depth
Monitor the request queue depth. If it grows, you need more replicas or a larger GPU. vLLM's metrics endpoint provides this data.

### Use Multiple Replicas Behind a Load Balancer
For high availability and throughput, run multiple vLLM replicas behind a load balancer (NGINX, HAProxy, Kubernetes Service).

### Pin Model Versions
When using HuggingFace model IDs, pin to specific revisions to avoid silent updates:
```bash
--model meta-llama/Llama-3.1-8B-Instruct --revision abc123
```

## See Also

- [[04 - vLLM and Continuous Batching]]
- [[02 - PagedAttention]]
- [[10 - PagedAttention vLLM 2023]]
- [[03 - Quantization]]
- [[05 - Speculative Decoding]]
- [[01 - LoRA]]
- [[04 - GPU Infrastructure and Sizing]]
- [[25 - Frameworks and Tools/MOC|25 Frameworks MOC]]
