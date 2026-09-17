---
tags: [inference, paged-attention, vllm, kv-cache]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
---

# PagedAttention

> [!info] TL;DR
> PagedAttention (vLLM, Kwon et al. 2023) manages the KV cache as **pages** (fixed-size blocks) rather than contiguous memory. Inspired by OS virtual memory paging. Eliminates fragmentation, enables variable-length batching, and gives 2–4x throughput improvement over HuggingFace's `generate`. The foundation of modern LLM serving.

## The Problem: KV Cache Fragmentation

Naive KV cache management pre-allocates a contiguous block per request, sized for the maximum possible sequence length. This causes severe memory fragmentation:

- **Internal fragmentation**: a request that ends up using 500 tokens but was allocated 2048 tokens wastes 1548 tokens of memory.
- **External fragmentation**: freed blocks of varying sizes can't be reused for new requests of different sizes.

Empirically, naive KV cache management wastes 60–80% of GPU memory to fragmentation. This limits batch size and throughput.

## The Inspiration: OS Virtual Memory

Operating systems solved this problem decades ago with **virtual memory paging**:
- Physical memory is divided into fixed-size **pages** (e.g., 4 KB).
- Each process has a virtual address space, mapped to physical pages via a **page table**.
- Pages can be allocated and freed independently; the virtual address space appears contiguous to the process.

PagedAttention applies the same idea to the KV cache.

## How PagedAttention Works

### Block-based KV cache

The KV cache is divided into fixed-size **blocks** (e.g., 16 tokens per block). Each request has a **block table** mapping its logical token positions to physical blocks.

```
Logical:  [t0 t1 t2 t3 | t4 t5 t6 t7 | t8 t9 ...]
            Block 0       Block 1       Block 2
              ↓             ↓             ↓
Physical:  [Block 0]    [Block 5]    [Block 2]
           (slot 12)    (slot 47)    (slot 8)
```

Blocks are allocated on demand as the sequence grows. When a sequence ends, its blocks are returned to a free pool and reused by other sequences.

### Attention with block indexing

The attention kernel is modified to:
1. Look up the block table for each sequence.
2. Gather K, V from the physical blocks.
3. Compute attention normally.

This adds a small indirection but eliminates all fragmentation. The kernel is implemented in CUDA with custom kernel fusion.

### Sharing blocks across sequences

A key benefit: blocks can be **shared** across sequences that share a prefix. For example, two chat completions with the same system prompt share the system prompt's blocks. This is **prefix caching** for free.

Block-level reference counting handles sharing: a block is freed only when its refcount drops to 0.

## Implementation Sketch (Conceptual)

```python
class PagedKVCache:
    def __init__(self, num_blocks, block_size, num_layers, num_heads, head_dim):
        # Pool of physical blocks
        self.kv_pool = torch.zeros(num_blocks, num_layers, 2, block_size, num_heads, head_dim)
        self.free_blocks = list(range(num_blocks))
        self.block_tables = {}  # request_id -> list of block indices
    
    def allocate(self, request_id, num_tokens):
        """Allocate enough blocks for num_tokens."""
        blocks_needed = (num_tokens + self.block_size - 1) // self.block_size
        blocks = [self.free_blocks.pop() for _ in range(blocks_needed)]
        self.block_tables[request_id] = blocks
        return blocks
    
    def append_token(self, request_id, token_pos, k, v):
        """Append a token's K, V to the cache."""
        block_idx = token_pos // self.block_size
        within_block = token_pos % self.block_size
        physical_block = self.block_tables[request_id][block_idx]
        self.kv_pool[physical_block, :, 0, within_block] = k
        self.kv_pool[physical_block, :, 1, within_block] = v
    
    def free(self, request_id):
        """Release all blocks for a request."""
        for block in self.block_tables[request_id]:
            self.free_blocks.append(block)
        del self.block_tables[request_id]
```

The real implementation is in CUDA for performance; see vLLM source.

## Memory Savings

For a workload with variable-length sequences (typical chatbot traffic):

| Method                | KV cache memory efficiency |
|-----------------------|---------------------------|
| Naive (max-size alloc)| 20–40%                    |
| PagedAttention        | 95%+                       |

The 2–4x effective memory increase translates directly to 2–4x larger batches and 2–4x higher throughput.

## Worked Throughput Example

For a Llama 2 7B server on A100 80GB:
- KV cache available: ~50 GB (after model weights and activations)
- Per-token KV: 1 MB
- Naive (2048 max per request): 50 GB / 2 MB = 25000 max concurrent tokens, but with fragmentation effective ~10000
- PagedAttention: 50000 effective concurrent tokens — **5x improvement**

This means 5x more concurrent users, or 5x more requests per second.

## Why This Matters for AI

- PagedAttention made **high-throughput LLM serving** practical. Without it, LLM APIs would be 2–4x more expensive.
- vLLM popularized PagedAttention and is the dominant open-source LLM serving engine.
- The block-based design also enables **prefix caching** (system prompts shared across requests) and **speculative decoding** (draft and target sequences share a prefix).
- The OS-paging analogy is a beautiful example of cross-disciplinary inspiration in systems design.

## Production Implications

- **Use vLLM (or TGI, which has similar techniques)** for production LLM serving. Don't use HuggingFace `generate` directly — it lacks these optimizations.
- **Block size** matters: too small → high block-table overhead; too large → internal fragmentation. vLLM defaults to 16, which works well.
- **Prefix caching** is critical for chatbot workloads. Ensure your serving engine supports it (vLLM does).
- **Continuous batching** (also from vLLM) complements PagedAttention — it lets new requests join a batch as soon as space frees up, rather than waiting for the whole batch to finish.

## Common Pitfalls

- **Forgetting to enable prefix caching** — many vLLM deployments ship with it off by default. Enable explicitly.
- **Block size mismatch** — if you change block size, you must restart vLLM. Don't change at runtime.
- **Running out of blocks** — if you see " KV cache is full" errors, reduce max batch size or upgrade GPU memory.
- **Confusing PagedAttention with model quantization** — they're orthogonal. You can use PagedAttention with INT8 KV cache quantization for even more memory savings.

## Related Techniques

### Continuous batching (iteration-level batching)

Instead of batching all requests together for their entire generation, continuous batching joins/leaves requests at every token (iteration). Combined with PagedAttention, this maximizes GPU utilization.

### RadixAttention (SGLang)

An alternative prefix-cache structure using a radix tree. Provides more flexible prefix sharing (any shared prefix, not just exact-match). Used by SGLang.

### Chunked prefill

For very long prompts, split the prefill into chunks and interleave with decode steps. Reduces prefill latency for long prompts.

## Further Reading

- Kwon et al. (2023), *Efficient Memory Management for Large Language Model Serving with PagedAttention* (vLLM).
- vLLM docs: https://docs.vllm.ai
- SGLang's RadixAttention: https://github.com/sgl-project/sglang

## See Also

- [[KV Cache Mechanics]]
- [[Speculative Decoding]]
- [[13 - Inference/MOC|Inference MOC]]
- [[08 - LLMs/MOC|LLMs MOC]]


## Interview Questions

1. **Q: How does PagedAttention eliminate KV cache fragmentation?**
   A: Instead of pre-allocating contiguous memory per request (which wastes 60-80% to fragmentation), PagedAttention divides the KV cache into fixed-size blocks (e.g., 16 tokens). Each request has a block table mapping logical positions to physical blocks. Blocks are allocated on demand and freed when the request ends. Internal fragmentation is limited to the last partial block (<16 tokens); external fragmentation is eliminated entirely.

2. **Q: How does PagedAttention enable prefix caching?**
   A: Blocks can be shared across sequences with the same prefix (e.g., the same system prompt). Block-level reference counting handles sharing: a block is freed only when its refcount drops to 0. Two chat completions with the same system prompt share the system prompt's blocks — the KV cache is computed once and reused. This is prefix caching for free.

3. **Q: What is the block size tradeoff?**
   A: Smaller blocks (e.g., 4): less internal fragmentation but more block-table overhead (more pointers per sequence). Larger blocks (e.g., 64): less overhead but more internal fragmentation (more wasted tokens in the last partial block). vLLM defaults to 16, which is the empirical sweet spot. The optimal size depends on the workload's sequence length distribution.

4. **Q: How does PagedAttention enable continuous batching?**
   A: Without paging, you can't add new requests to a batch mid-generation because the contiguous KV caches don't have room. With paging, you just allocate new blocks for the new sequence. This lets vLLM process sequences of different lengths and arrival times in the same batch — continuous batching (iteration-level batching).

5. **Q: What is preemption and how does PagedAttention handle it?**
   A: When the KV cache is full, the scheduler must evict a request. Two strategies: (1) recompute — evict the request, recompute its KV when memory frees; (2) swap — evict the KV to CPU memory, swap back when memory frees. PagedAttention supports both. Swap is the production default (faster resume, costs CPU memory).

6. **Q: How much throughput improvement does PagedAttention give?**
   A: 2-4x throughput vs naive serving (which pre-allocates max-size per request). The improvement comes from: (1) 95%+ memory efficiency (vs 20-40% with naive); (2) larger batch sizes (more concurrent requests); (3) prefix caching (shared system prompts). For a 7B model on A100: ~250 concurrent tokens (naive) → ~50000 (PagedAttention) — 5x improvement.

## Connection to Other Concepts

- [[08 - LLMs/Context and KV Cache/02 - KV Cache Mechanics|KV Cache Mechanics]] — what PagedAttention manages.
- [[13 - Inference/Serving/04 - vLLM and Continuous Batching|vLLM]] — implements PagedAttention.
- [[13 - Inference/Serving/06 - Continuous Batching Deep Dive|Continuous Batching]] — enabled by PagedAttention.
- [[13 - Inference/Speculative Decoding/05 - Speculative Decoding|Speculative Decoding]] — shares prefix blocks.
- [[02 - Mathematics/Linear Algebra/06 - Tensors and Broadcasting|Tensors and Broadcasting]] — block indexing.
- [[26 - Papers/Efficient Attention/10 - PagedAttention vLLM 2023|PagedAttention 2023]] — the paper.
