---
tags: [inference, serving, vllm, continuous-batching]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
aliases: [vLLM, Continuous Batching, Serving]
---

# 04 - vLLM and Continuous Batching

> [!info] TL;DR
> vLLM is the dominant open-source LLM serving engine. Continuous batching + PagedAttention give 10–20x throughput vs naive serving. TensorRT-LLM and TGI are alternatives. The standard for production LLM deployment in 2026.

## Why Not Just Use HuggingFace `generate`?

Naive `model.generate()` has three problems:
1. **Batching is static**: a batch of 8 requests must all finish before any new request joins. Long requests delay the whole batch.
2. **No KV cache management**: each request allocates contiguous memory for the max possible length — wastes 60–80% to fragmentation.
3. **No prefix caching**: identical system prompts across requests are processed independently.

Production LLM serving needs to handle 100s–1000s of concurrent requests efficiently. That requires purpose-built infrastructure.

## Continuous Batching (Iteration-Level Batching)

Instead of batching requests for their **entire generation**, batch them **per iteration** (per token):

```
Step 1: requests A, B, C generate token 1, 2, 1 (respectively)
Step 2: A finishes; D joins. B, C, D generate token 3, 2, 1
Step 3: C finishes; E joins. B, D, E generate token 4, 1, 1
...
```

At every step, the batch composition can change — finished requests leave, new requests join. This keeps the GPU saturated and minimizes tail latency.

Combined with PagedAttention ([[02 - PagedAttention]]) for KV cache management, continuous batching gives 10–20x throughput vs static batching.

## vLLM (Kwon et al. 2023)

The dominant open-source LLM serving engine. Key features:
- **PagedAttention**: KV cache as pages (see [[02 - PagedAttention]]).
- **Continuous batching**: iteration-level.
- **Prefix caching**: shared prefixes (system prompts) cached across requests.
- **Tensor parallelism**: split model across GPUs.
- **Quantization support**: GPTQ, AWQ, FP8, INT8 KV cache.
- **LoRA serving**: serve multiple LoRA adapters on a single base model.
- **Speculative decoding**: with draft models.
- **OpenAI-compatible API**: drop-in replacement for OpenAI clients.

### vLLM Usage

```bash
# Serve a model
vllm serve meta-llama/Meta-Llama-3-8B-Instruct \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 8192
```

Or in Python:

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Meta-Llama-3-8B-Instruct")
prompts = ["Hello!", "What is the capital of France?", "Write a poem."]
sampling = SamplingParams(temperature=0.7, max_tokens=100)
outputs = llm.generate(prompts, sampling)
for out in outputs:
    print(out.outputs[0].text)
```

### vLLM API server

```bash
vllm serve meta-llama/Meta-Llama-3-8B-Instruct --port 8000
```

Then use any OpenAI-compatible client:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")
response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

## Alternatives

### TensorRT-LLM (NVIDIA)
- Highest performance on NVIDIA hardware.
- Closed source (with open wrappers).
- Compiles models to optimized NVIDIA kernels.
- Best for pure-NVIDIA production deployments where every % matters.

### TGI (Text Generation Inference, HuggingFace)
- HuggingFace's serving engine.
- Good ecosystem integration (HuggingFace Hub).
- Less performant than vLLM but easier to use.
- Used in HuggingFace's inference endpoints.

### SGLang
- Newer open-source engine.
- RadixAttention for prefix caching (more flexible than vLLM's).
- Often outperforms vLLM on agentic / structured workloads.
- Active development.

### llama.cpp / Ollama
- For local / consumer-GPU inference.
- GGUF format. CPU + GPU.
- Not for high-throughput production serving.

### MLPerf-style custom engines
- For absolute maximum performance: custom CUDA kernels.
- Only worth it for hyperscale deployments.

## Choosing a Serving Engine

| Use case                          | Recommendation         |
|-----------------------------------|------------------------|
| General production                | vLLM                   |
| NVIDIA-only, max performance      | TensorRT-LLM           |
| HuggingFace ecosystem             | TGI                    |
| Agentic / structured output       | SGLang                 |
| Local / single user               | Ollama, llama.cpp      |
| Multi-LoRA serving                | vLLM (best support)    |
| Speculative decoding              | vLLM, SGLang           |

## Performance Considerations

### Throughput vs Latency
- **Throughput**: tokens/sec across all requests. Maximized by large batches.
- **Latency**: time-to-first-token and time-per-output-token for individual requests. Maximized by small batches.

There's a tradeoff: large batches improve throughput but increase per-request latency. Pick based on your use case (interactive chat = latency-sensitive; batch processing = throughput-sensitive).

### Prefill vs Decode
- **Prefill** (process the prompt): compute-bound. Parallelizable across tokens. High GPU utilization.
- **Decode** (generate new tokens): memory-bound. Sequential. Low GPU utilization at batch size 1.

This is why batching matters more for decode — it amortizes the weight reads.

### Tuning knobs
- `--gpu-memory-utilization`: how much GPU memory vLLM can use. Higher = bigger batches.
- `--max-model-len`: max context length. Affects memory and KV cache size.
- `--tensor-parallel-size`: number of GPUs for tensor parallelism.
- `--enable-prefix-caching`: turn on prefix caching (default in recent vLLM).
- `--swap-space`: CPU memory for swapping KV cache (helps with overload).

## Why This Matters for AI

- Production LLM deployment **requires** a proper serving engine. Using `model.generate()` directly is 10–20x slower.
- vLLM is the de facto open standard — knowing it is essential for any AI engineer deploying models.
- The continuous batching + PagedAttention pattern is now industry-standard; even commercial providers use variants of it.

## Production Implications

- **Default to vLLM** for serving open-source LLMs.
- **Enable prefix caching** for chatbot / RAG workloads.
- **Quantize models** (AWQ INT4) before serving — 4x memory reduction.
- **Monitor GPU utilization** — if <50%, increase batch size; if 100%, add GPUs.
- **Use tensor parallelism** for models >40GB (70B in fp16 needs TP=2 on H100).
- **Multi-LoRA serving** for multi-tenant: load base model once, swap adapters per request.

## Common Pitfalls

- **Wrong `gpu-memory-utilization`** — too high → OOM; too low → wasted capacity.
- **Forgetting to set `max-model-len`** — defaults can cause OOM with long prompts.
- **Not enabling prefix caching** — major throughput loss for chatbot workloads.
- **Serving the base model instead of Instruct** — base models don't follow instructions.
- **Using `model.generate()` in production** — 10–20x slower than vLLM.

## Further Reading

- Kwon et al. (2023), *Efficient Memory Management for Large Language Model Serving with PagedAttention* (vLLM).
- vLLM docs: https://docs.vllm.ai
- SGLang: https://github.com/sgl-project/sglang
- TensorRT-LLM: https://github.com/NVIDIA/TensorRT-LLM

## See Also

- [[02 - PagedAttention]]
- [[03 - Quantization]]
- [[05 - Speculative Decoding]]
- [[13 - Inference/MOC|Inference MOC]]


## Interview Questions

1. **Q: Why shouldn't you use HuggingFace `model.generate()` in production?**
   A: Three problems: (1) static batching — a batch of 8 requests must all finish before new ones join (tail latency); (2) no KV cache management — each request allocates contiguous memory for max length (60-80% wasted to fragmentation); (3) no prefix caching — identical system prompts are processed independently. vLLM gives 10-20x throughput via continuous batching + PagedAttention.

2. **Q: What is continuous batching and how does it differ from static batching?**
   A: Static batching: form a batch, process to completion, return all results. The batch's wall-clock time is determined by the longest request. Continuous batching: at every iteration (token), the scheduler can insert new requests and evict finished ones. This keeps the GPU saturated and minimizes tail latency.

3. **Q: How do you choose between vLLM, TGI, TensorRT-LLM, and SGLang?**
   A: vLLM: general production (default). TGI: HuggingFace ecosystem. TensorRT-LLM: NVIDIA-only, max performance (compilation cost). SGLang: agentic/structured workloads (RadixAttention prefix caching). Ollama/llama.cpp: local/single user. For most teams: start with vLLM, switch to TensorRT-LLM only if you need max performance on NVIDIA.

4. **Q: What is prefill vs decode and why does it matter for serving?**
   A: Prefill: process the prompt (compute attention over all prompt tokens). Compute-bound, parallelizable, high GPU utilization. Decode: generate one token at a time (attend to prompt + generated tokens). Memory-bound, sequential, low GPU utilization at batch size 1. Batching matters more for decode (amortizes weight reads). Chunked prefill interleaves prefill chunks with decodes to smooth latency.

5. **Q: How does prefix caching work and when does it help?**
   A: If multiple requests share a common prefix (e.g., the same system prompt), their KV caches can share the prefix blocks. The prefix is computed once and reused. vLLM supports this via `--enable-prefix-caching`. Helps significantly for chatbot/RAG workloads where system prompts are shared. Hit rate: 30-80% depending on workload.

6. **Q: What tuning knobs does vLLM expose?**
   A: `--gpu-memory-utilization` (how much GPU memory vLLM can use; higher = bigger batches). `--max-model-len` (max context length; affects KV cache size). `--tensor-parallel-size` (number of GPUs for TP). `--enable-prefix-caching` (turn on prefix caching). `--swap-space` (CPU memory for KV cache swapping on overload).

## Connection to Other Concepts

- [[13 - Inference/KV Cache/02 - PagedAttention|PagedAttention]] — vLLM's memory management.
- [[13 - Inference/Serving/06 - Continuous Batching Deep Dive|Continuous Batching Deep Dive]] — the scheduling algorithm.
- [[13 - Inference/Speculative Decoding/05 - Speculative Decoding|Speculative Decoding]] — vLLM supports it.
- [[13 - Inference/Quantization/03 - Quantization|Quantization]] — vLLM supports INT4/INT8/FP8.
- [[25 - Frameworks and Tools/Serving/07 - vLLM|vLLM (Ch 25)]] — framework perspective.
- [[22 - Production AI/Architecture/01 - Production AI Stack|Production AI Stack]] — where vLLM fits.
