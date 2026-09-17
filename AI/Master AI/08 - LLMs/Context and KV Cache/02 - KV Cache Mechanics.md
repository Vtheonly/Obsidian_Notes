---
tags: [llms, inference, kv-cache, transformer, memory-management]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [KV Cache Mechanics, KV Cache, Key-Value Cache, Attention Cache]
---

# KV Cache Mechanics

> [!info] TL;DR
> The KV cache stores the keys and values of all previous tokens so that autoregressive generation only recomputes the new token's Q, K, V — not the entire context. Without the KV cache, generating 1000 tokens from a 4096-token prompt would cost ~4M attention computations instead of ~4K. The KV cache is what makes LLM inference tractable. This note covers the problem, solution, memory layout, GQA/MQA/MLA impact, prefill vs decode, optimizations, production considerations, and common pitfalls.

## The Problem: Naive Autoregressive Generation

To generate token $t+1$, the model computes attention over all previous tokens $1, \ldots, t$. Naively, this means recomputing the K and V vectors for **all** previous tokens at every step.

For a 4096-token prompt generating 1000 new tokens:
- Step 1: recompute K, V for 4096 tokens.
- Step 2: recompute K, V for 4097 tokens.
- ...
- Step 1000: recompute K, V for 5096 tokens.

Total work: $\approx 1000 \times 4500 \approx 4.5M$ token-equivalent K/V computations, even though there are only 5096 unique tokens. The vast majority of this work is **redundant** — the K and V for token $i$ never change once computed.

In concrete terms, naive generation of 1000 tokens from a 4K prompt on a 7B model would take ~30 minutes (vs ~5 seconds with KV cache). The KV cache isn't an optimization — it's a necessity.

## The Solution: Cache the K and V

The K and V for each token depend only on that token (through the input-dependent projections $\mathbf{W}_K, \mathbf{W}_V$). Once computed, they're fixed. So we **cache** them.

At step $t+1$:
1. Compute Q, K, V **only for the new token** $t+1$.
2. Append the new K, V to the cache.
3. Compute attention: $\text{softmax}(Q_{t+1} K_{1:t+1}^T / \sqrt{d_k}) V_{1:t+1}$.

Now each step is $O(t \cdot d_k)$ work (the attention itself), not $O(t \cdot d_{\text{model}})$ work (the projections). For long sequences, this is a 10–100× speedup.

### Why K and V But Not Q?

The query Q changes every step — we need a new Q for the new token. But the K and V for past tokens are computed once and reused. We don't cache Q because:
- Q is only needed for the current token's attention computation.
- Past Q values aren't needed for future tokens.

This asymmetry (cache K, V but not Q) is what makes the KV cache work.

### Mathematical Justification

For token $i$, the key is $\mathbf{k}_i = \mathbf{x}_i \mathbf{W}_K$ and the value is $\mathbf{v}_i = \mathbf{x}_i \mathbf{W}_V$. These depend only on $\mathbf{x}_i$ (the input at position $i$), which is fixed once generated. So $\mathbf{k}_i$ and $\mathbf{v}_i$ are constant after generation — caching is correct.

The query $\mathbf{q}_t = \mathbf{x}_t \mathbf{W}_Q$ is also constant for token $t$, but we don't cache it because we only need it for the current step's attention.

## Memory Layout

For each layer $l$ and each head $h$, we store:

- $\mathbf{K}_{l,h} \in \mathbb{R}^{n \times d_k}$ — keys for all $n$ tokens.
- $\mathbf{V}_{l,h} \in \mathbb{R}^{n \times d_k}$ — values for all $n$ tokens.

Total KV cache size:

$$
\text{KV cache bytes} = 2 \cdot n_{\text{layers}} \cdot n_{\text{kv\_heads}} \cdot n \cdot d_k \cdot \text{bytes\_per\_element}
$$

The factor of 2 is for K and V. The `n_kv_heads` is the number of KV heads (less than `n_heads` for GQA).

### Concrete Examples

For Llama 3 8B (32 layers, 8 KV heads, 128 head dim, fp16):
- Per token: $2 \cdot 32 \cdot 8 \cdot 128 \cdot 2 = 131,072$ bytes = 128 KiB per token.
- For 8192 tokens: 1 GiB of KV cache.
- For 128k tokens: 16 GiB of KV cache — **larger than the model itself** (~16 GB).

For Llama 3 70B (80 layers, 8 KV heads, 128 head dim, fp16):
- Per token: $2 \cdot 80 \cdot 8 \cdot 128 \cdot 2 = 327,680$ bytes = 320 KiB per token.
- For 8192 tokens: 2.5 GiB KV cache.
- For 128k tokens: 40 GiB KV cache — needs multi-GPU.

For Llama 3 70B with INT8 KV cache:
- Per token: 160 KiB (half of FP16).
- For 128k tokens: 20 GiB — fits on a single H100 80GB (barely).

This is why long-context inference is **memory-bound**, not compute-bound. See [[13 - Inference/MOC|Inference MOC]].

### Why KV Cache Grows with Context

The KV cache size is proportional to sequence length $n$. As $n$ grows:
- Memory: linear growth ($O(n)$).
- Attention compute: quadratic growth ($O(n^2)$) — but FlashAttention makes this $O(n)$ memory.
- Decode bandwidth: linear growth (must read the entire cache per token).

Long contexts are expensive in three ways: memory to store the cache, bandwidth to read it per token, and compute for attention. All three scale with $n$.

## Why GQA / MQA / MLA Matter for KV Cache

The KV cache size is proportional to $n_{\text{kv\_heads}}$. Reducing the number of KV heads directly reduces the cache:

| Variant  | $n_{\text{kv\_heads}}$ | KV cache (relative to MHA) | Quality Impact |
|----------|------------------------|----------------------------|----------------|
| MHA      | $h$ (all heads)        | 1.0                        | Baseline       |
| GQA      | $g < h$                | $g/h$                      | Minimal (if $g \geq 4$) |
| MQA      | 1                      | $1/h$                      | Noticeable     |
| MLA      | latent dim $\ll h d_k$ | $\ll 1/h$                  | Minimal        |

Llama 3 8B uses GQA with 8 KV heads (vs 32 Q heads) — a 4× reduction in KV cache size vs MHA. This is what makes 128k-token context feasible on a single H100.

DeepSeek-V2's MLA (Multi-head Latent Attention) compresses K and V into a low-rank latent vector, reducing the cache by ~10× compared to MHA. This is a key innovation enabling DeepSeek's efficient long-context inference.

See [[14 - GQA MQA MLA]] for the full comparison.

## Implementation Sketch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class CachedAttention(nn.Module):
    def __init__(self, d_model, n_heads, n_kv_heads=None):
        super().__init__()
        n_kv_heads = n_kv_heads or n_heads
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.n_rep = n_heads // n_kv_heads  # for GQA
        self.d_k = d_model // n_heads
        
        self.W_qkv = nn.Linear(d_model, d_model + 2 * n_kv_heads * self.d_k, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)
    
    def forward(self, x, kv_cache=None, position_ids=None, cache_position=None):
        B, N, _ = x.shape
        qkv = self.W_qkv(x)
        q, k, v = qkv.split([self.n_heads * self.d_k, 
                              self.n_kv_heads * self.d_k,
                              self.n_kv_heads * self.d_k], dim=-1)
        q = q.view(B, N, self.n_heads, self.d_k).transpose(1, 2)
        k = k.view(B, N, self.n_kv_heads, self.d_k).transpose(1, 2)
        v = v.view(B, N, self.n_kv_heads, self.d_k).transpose(1, 2)
        
        # Apply RoPE (rotary positional encoding)
        q, k = apply_rope(q, k, position_ids)
        
        # Append to KV cache
        if kv_cache is not None:
            cache_k, cache_v = kv_cache
            # Write new K, V into the cache at the correct position
            cache_k[:, :, cache_position:cache_position+N, :] = k
            cache_v[:, :, cache_position:cache_position+N, :] = v
            k = cache_k[:, :, :cache_position+N, :]
            v = cache_v[:, :, :cache_position+N, :]
        new_kv_cache = (k, v)
        
        # Repeat K, V for GQA (each KV head serves multiple Q heads)
        if self.n_rep > 1:
            k = k.repeat_interleave(self.n_rep, dim=1)
            v = v.repeat_interleave(self.n_rep, dim=1)
        
        # Standard scaled dot-product attention
        # In production, use F.scaled_dot_product_attention (FlashAttention)
        scores = (q @ k.transpose(-2, -1)) * (self.d_k ** -0.5)
        attn = F.softmax(scores, dim=-1)
        out = attn @ v
        
        out = out.transpose(1, 2).contiguous().view(B, N, -1)
        return self.W_o(out), new_kv_cache
```

The key bits:
1. Compute Q, K, V only for the new tokens.
2. Concatenate the new K, V with the cached K, V.
3. Return the updated cache for the next step.

### Pre-allocated Cache (Production)

In production (vLLM, TGI), the cache is pre-allocated to the maximum sequence length and filled in-place:

```python
class KVCache:
    def __init__(self, batch_size, max_seq_len, n_layers, n_kv_heads, d_k, dtype=torch.float16):
        self.cache = {
            layer: (
                torch.zeros(batch_size, n_kv_heads, max_seq_len, d_k, dtype=dtype, device='cuda'),
                torch.zeros(batch_size, n_kv_heads, max_seq_len, d_k, dtype=dtype, device='cuda'),
            )
            for layer in range(n_layers)
        }
        self.length = 0
    
    def append(self, layer, k_new, v_new):
        cache_k, cache_v = self.cache[layer]
        N = k_new.size(2)
        cache_k[:, :, self.length:self.length+N, :] = k_new
        cache_v[:, :, self.length:self.length+N, :] = v_new
        self.length += N
        return cache_k[:, :, :self.length, :], cache_v[:, :, :self.length, :]
```

This avoids memory allocation during generation — critical for throughput.

## Two Phases: Prefill and Decode

LLM inference has two distinct phases with very different compute profiles:

### Prefill (compute-bound)

Process the prompt: compute Q, K, V for all $n$ prompt tokens, populate the KV cache. This is essentially a forward pass over the prompt — it does $O(n^2)$ attention work but is fully parallelizable across tokens.

For a 4096-token prompt: ~14 GFLOPs/param of work (for a 7B model, ~100 TFLOPs). At 100 TFLOP/s on an H100, this takes ~1 second.

Characteristics:
- **High GPU utilization**: parallel across all prompt tokens.
- **Compute-bound**: matrix multiplications dominate.
- **Batch size 1**: typically one prompt at a time (or a few).
- **Latency**: proportional to prompt length.

### Decode (memory-bound)

Generate new tokens one at a time. Each step computes Q, K, V for 1 token, then attention against the cached $n$ tokens. The arithmetic intensity is low — you're reading the entire model weights + KV cache from HBM to compute a single token.

For a 7B model at batch size 1: ~14 GB of weights read per token. HBM bandwidth ~3 TB/s → ~5 ms per token = 200 tokens/sec. This is **memory-bandwidth-bound**, not compute-bound.

Characteristics:
- **Low GPU utilization**: one token at a time.
- **Memory-bound**: weight and KV cache reads dominate.
- **Batch size matters**: batching amortizes weight reads over multiple requests.
- **Latency**: ~5-50 ms per token (depending on model size and batch).

### Implications

- **Prefill** is where GPU utilization is high (parallel across tokens).
- **Decode** is where GPU utilization is low (one token at a time). This is where optimizations like continuous batching, GQA, and speculative decoding matter most.
- **The prefill/decode asymmetry drives inference optimization**: continuous batching interleaves them, chunked prefill avoids stalling decode, speculative decoding uses prefill-style verification.
- See [[13 - Inference/Serving/04 - vLLM and Continuous Batching|Serving]] for production techniques.

## Optimizations

### PagedAttention (vLLM)

Manages the KV cache as **pages** (fixed-size blocks) rather than contiguous memory. This avoids memory fragmentation from variable-length sequences and lets you batch many requests efficiently.

Without paging: each request reserves a contiguous block of memory for its worst-case sequence length. Most of this memory is wasted (sequences are usually shorter than max). With paging: each request uses only the blocks it needs; blocks are allocated and freed dynamically.

PagedAttention achieves 2-4× higher throughput than non-paged KV cache management. See [[02 - PagedAttention]].

### Prefix caching

If many requests share a common prefix (e.g., a system prompt), cache the K, V for that prefix and reuse across requests. Major speedup for chatbot workloads.

- vLLM: `--enable-prefix-caching`.
- SGLang: automatic via RadixAttention (see [[14 - SGLang]]).
- TGI: limited support.

For chatbot workloads where 90% of requests share a 2K-token system prompt, prefix caching reduces prefill cost by 90%.

### KV cache quantization

Store the KV cache in INT8 or FP8 instead of FP16. Halves memory. Slight quality loss; well-supported in vLLM and TensorRT-LLM.

- vLLM: `--kv-cache-dtype fp8`.
- TensorRT-LLM: native support.

For long contexts, KV cache quantization is often the difference between fitting on one GPU and needing two.

### KV cache offloading

For very long contexts, offload KV cache to CPU memory or NVMe when not actively used. Slower but enables contexts that don't fit in GPU memory.

Implementation: keep the most recent N tokens in GPU, offload older tokens to CPU. Swap back when needed. Adds latency but enables 1M+ token contexts.

### MLA (DeepSeek)

DeepSeek's MLA (Multi-head Latent Attention) compresses K and V into a low-rank latent vector, drastically reducing the cache size. Instead of storing $h \cdot d_k$ per token, MLA stores a latent vector of dimension $d_c \ll h \cdot d_k$.

For DeepSeek-V2: $h = 128$, $d_k = 128$, $d_c = 512$. Cache is reduced from $128 \cdot 128 = 16384$ to $512$ per token — a 32× reduction.

See [[14 - GQA MQA MLA]] and [[28 - DeepSeek-V2 and V3 2024]] for details.

### Sliding Window Attention (Mistral)

For long contexts, use sliding window attention: each token attends only to the previous W tokens (e.g., W=4096). The KV cache only needs to store the last W tokens, not the full sequence.

- Cache size: $O(W)$ instead of $O(n)$.
- Attention compute: $O(n \cdot W)$ instead of $O(n^2)$.
- Trade-off: loses long-range attention.

Mistral 7B uses SWA with W=4096. Combined with global attention at certain layers, it achieves good long-context performance with bounded cache.

### Ring Attention

For extremely long contexts (1M+ tokens), distribute the KV cache across multiple GPUs. Each GPU holds a portion of the sequence; attention is computed via ring communication.

- Enables 1M+ token contexts on multi-GPU setups.
- Adds communication overhead but breaks the single-GPU memory limit.
- Used by Gemini 1.5 Pro and similar long-context models.

## Memory Budget Calculation

A critical production calculation: how many concurrent requests can a GPU serve?

```
Available memory = GPU memory - model weights - framework overhead
Usable for KV cache = Available memory

KV cache per request = 2 * n_layers * n_kv_heads * max_seq_len * d_k * bytes_per_element
Concurrent requests = Usable for KV cache / KV cache per request
```

### Example: Llama 3 8B on H100 80GB

- Model weights (FP16): 16 GB
- Framework overhead: 4 GB
- Available: 80 - 16 - 4 = 60 GB
- KV cache per request (8K context, FP16): 1 GB
- Concurrent requests: 60 / 1 = 60

For 128K context: 16 GB per request → 3-4 concurrent requests.

For 128K context with FP8 KV cache: 8 GB per request → 7-8 concurrent requests.

This calculation drives capacity planning. Double the GPU memory → double the throughput (roughly). Halve the context length → double the throughput.

## Why This Matters for AI

- KV cache is **the** key concept for understanding LLM inference. Without it, you can't reason about inference cost, memory, or why certain optimizations work.
- The KV cache is the main reason **context length matters for cost** — both at training (memory) and inference (memory + bandwidth).
- GQA / MQA / MLA are architectural innovations specifically targeting the KV cache. They exist because the cache is the bottleneck.
- Understanding KV cache is essential for:
  - Estimating serving costs (memory per concurrent request).
  - Choosing between models (GQA matters more than MHA for inference).
  - Understanding why batching helps (amortizes weight reads over multiple requests).
  - Reading inference engine docs (vLLM, TGI, TensorRT-LLM).
  - Choosing quantization strategies (KV cache quantization vs. weight quantization).

## Production Implications

- **Memory budget per request** = model weights / batch + KV cache size. For a 7B model on 1 H100 (80 GB) with 8k context: weights = 14 GB, KV cache = 1 GB → ~80 concurrent requests fit.
- **Long-context serving is expensive**. 128k context on Llama 3 8B = 16 GB KV cache per request. You can serve ~5 concurrent requests on a single H100.
- **Batch aggressively during decode** — continuous batching (vLLM) is the standard. It can 10× throughput.
- **Quantize the KV cache** to INT8 — easy 2× memory reduction with minimal quality loss.
- **Use prefix caching** for chatbot / RAG workloads where prompts share prefixes.
- **Monitor KV cache utilization** — if it's near 100%, you're throughput-limited; if it's low, you're leaving capacity unused.
- **Pre-allocate cache** to avoid memory allocation during generation. Allocation is slow and causes fragmentation.
- **Use FlashAttention** — it's KV-cache-aware and avoids materializing the $n \times n$ attention matrix.

## Common Pitfalls

- **Forgetting that KV cache grows with context** — easy to OOM at long contexts. Always set a max context length and pre-allocate.
- **Using MHA when GQA would do** — for new model designs, prefer GQA. The 4× KV cache reduction is significant.
- **Not batching decode** — single-request decode is 10–100× slower per token than batched decode. Use continuous batching.
- **Forgetting to apply RoPE to cached K** — when you concatenate cached K with new K, both must use the same positional encoding. New K must be rotated with the correct position. This is a subtle bug that produces silent quality degradation.
- **Recomputing the prompt's K, V every step** — defeats the entire point of the cache. Always populate the cache once during prefill and reuse.
- **Cache position tracking bugs** — when appending to the cache, you must track the current position. Off-by-one errors produce silent quality issues.
- **Not clearing the cache between requests** — if the cache isn't cleared, the next request sees the previous request's K, V. Produces nonsense output.
- **Batch size mismatch in cache** — the cache's batch dimension must match the input's. If you change batch size, you must reallocate the cache.
- **Numerical issues with FP16 KV cache** — for long contexts, FP16 KV cache can accumulate errors. Use FP32 for the cache in sensitive applications, or use FP8 with careful scaling.
- **Multi-GPU cache sharding bugs** — when sharding the cache across GPUs (tensor parallelism), the head dimension must be split correctly. Off-by-one produces silent corruption.

## Interview Questions

- **Q: Why do we cache K and V but not Q?**  
  A: K and V for past tokens are needed for future attention computations (every future token attends to all past keys). Q for past tokens isn't needed — only the current token's Q is used. Caching Q would waste memory.

- **Q: How much memory does the KV cache use for Llama 3 8B at 128K context?**  
  A: $2 \cdot 32 \cdot 8 \cdot 128000 \cdot 128 \cdot 2$ bytes = 16 GB. Larger than the model itself (16 GB FP16).

- **Q: Why does GQA reduce KV cache size?**  
  A: GQA has fewer KV heads ($n_{kv} < n_{heads}$). The cache is proportional to $n_{kv}$, so for Llama 3 8B with $n_{heads}=32$, $n_{kv}=8$, the cache is 4× smaller than MHA.

- **Q: What's the difference between prefill and decode?**  
  A: Prefill processes all prompt tokens in parallel (compute-bound, high GPU utilization). Decode generates one token at a time (memory-bound, low GPU utilization). The asymmetry drives inference optimization.

- **Q: How does PagedAttention help?**  
  A: It manages the KV cache as pages (fixed-size blocks) instead of contiguous memory. This avoids fragmentation from variable-length sequences, enabling 2-4× higher throughput via better memory utilization.

- **Q: How would you serve 1M-token contexts?**  
  A: Use MLA (DeepSeek) for cache compression, KV cache quantization (FP8), Ring Attention to distribute across GPUs, and possibly KV cache offloading to CPU. Even with all these, 1M context is expensive — only for high-value use cases.

## Further Reading

- Vaswani et al. (2017), *Attention Is All You Need* — the original (no KV cache, but the foundation).
- Kwon et al. (2023), *Efficient Memory Management for Large Language Model Serving with PagedAttention* (vLLM). See [[10 - PagedAttention vLLM 2023]].
- Shazeer (2019), *Fast Transformer Decoding with One Write-Head* (MQA — motivated by KV cache).
- DeepSeek-V2 paper — MLA. See [[28 - DeepSeek-V2 and V3 2024]].
- Dao et al. (2022), *FlashAttention* — IO-aware attention. See [[08 - FlashAttention 2022]].

## See Also

- [[04 - Self-Attention]] · [[05 - Multi-Head Attention]]
- [[01 - Transformer Block]]
- [[02 - PagedAttention]]
- [[03 - Sampling Strategies]]
- [[14 - GQA MQA MLA]] — modern attention variants
- [[11 - FlashAttention]] — IO-aware attention
- [[13 - Inference/MOC|Inference MOC]]
- [[06 - Continuous Batching Deep Dive]] — batching with KV cache
- [[08 - LLMs/MOC|LLMs MOC]]
