---
tags: [paper, flashattention-2, flashattention-3, efficient-attention, hopper]
iteration: 5
created: 2026-08-08
aliases: [FlashAttention-2 2023, FlashAttention-3 2024, FA2, FA3]
---

# 27 — FlashAttention-2 and FlashAttention-3 (Dao, 2023–2024)

> [!info] TL;DR
> FlashAttention-2 (2023) rewrote the FlashAttention kernel to better parallelize across GPU streaming multiprocessors, achieving 2× speedup over FA1. FlashAttention-3 (2024) was redesigned for NVIDIA Hopper (H100) GPUs, using asynchronous warpgroups (WGMMA), overlapped matmul-softmax, and FP8 support to reach 1.5–2.0 PFLOPS — close to theoretical peak. Together, they pushed exact attention to the hardware limit and made long-context LLMs economically viable.

## Citations

- **FlashAttention-2**: Dao, T. (2023). *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*. arXiv:2307.08691.
- **FlashAttention-3**: Shah, S., Bikshandi, G., Zhang, Y., & Dao, T. (2024). *FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision*. arXiv:2407.08608.

## The Problem Being Solved

[[08 - FlashAttention 2022|FlashAttention-1]] (2022) introduced IO-aware exact attention — same math as standard attention, but reordered to minimize HBM traffic. It delivered 2–4× speedup and made long-context training practical.

But FA1 had inefficiencies:
- **Poor work partitioning**: it parallelized across batch and heads, but not across the sequence length. For long sequences, this underutilized the GPU's streaming multiprocessors (SMs).
- **Non-matmul FLOPs**: the rescaling operations (tracking running max and sum for online softmax) added overhead that wasn't tensor-core-friendly.
- **No Hopper-specific optimizations**: FA1 was designed for Ampere (A100). Hopper (H100) introduced new features (WGMMA, asynchronous warpgroups, FP8) that FA1 couldn't use.

FA2 addressed the first two issues; FA3 addressed the third. Together, they pushed FlashAttention to near-peak hardware performance.

## FlashAttention-2: Better Parallelism and Work Partitioning

### Key Improvements Over FA1

#### 1. Sequence-Parallel Partitioning
FA1 parallelized across batch and heads: each (batch, head) pair was one thread block. For long sequences with few heads, this underutilized the GPU (not enough thread blocks to fill all SMs).

FA2 adds parallelism across the sequence length: the sequence is split into chunks, each processed by a different thread block. The partial results are reduced at the end. This gives much better GPU utilization for long sequences.

#### 2. Reduced Non-Matmul FLOPs
FA1 had overhead from the online softmax rescaling: each block required recomputing the running max and sum, which involved non-matmul operations. These operations don't use tensor cores and are relatively slow.

FA2 restructured the computation to minimize non-matmul FLOPs. The rescaling is fused into the matmul operations where possible, reducing the overhead. On A100, this gave ~2× speedup over FA1.

#### 3. Better Work Partitioning Within a Thread Block
FA1 used all threads in a thread block for both matmul and softmax. FA2 partitions threads: some do matmul (using tensor cores), others do softmax (using CUDA cores). This overlap improves throughput.

### FA2 Results

| Sequence Length | FA1 (A100) | FA2 (A100) | Speedup |
|-----------------|------------|------------|---------|
| 1024            | 0.6 ms     | 0.4 ms     | 1.5×    |
| 4096            | 4.5 ms     | 2.5 ms     | 1.8×    |
| 16384           | 75 ms      | 40 ms      | 1.9×    |

FA2 achieved ~2× speedup over FA1, reaching 50–70% of A100's theoretical peak FLOPs for attention. This made 32K–128K context training practical.

### Adoption
FA2 became the default attention kernel in PyTorch 2.0+, HuggingFace Transformers, vLLM, TGI, and most major training frameworks. By 2024, it was the most widely-used attention implementation.

## FlashAttention-3: Hopper-Specific Optimization

### The Hopper GPU Context
NVIDIA Hopper (H100) introduced several features that Ampere (A100) lacked:
- **WGMMA** (Warp Group Matrix Multiply Accumulate): a new tensor-core instruction that performs matmul asynchronously — the warpgroup can do other work while the matmul runs.
- **Asynchronous warpgroups**: a warpgroup (4 warps) can overlap matmul with softmax and other operations.
- **FP8 tensor cores**: 2× throughput compared to FP16/BF16.
- **TMA (Tensor Memory Access)**: asynchronous memory copies that overlap with compute.

FA1 and FA2 couldn't use these features — they were designed for Ampere's synchronous execution model. FA3 was redesigned from scratch for Hopper.

### Key FA3 Innovations

#### 1. WGMMA for Asynchronous Matmul
FA3 uses Hopper's WGMMA instruction: the warpgroup issues a matmul instruction, then immediately moves on to other work (softmax, rescaling) while the matmul executes. When the matmul completes, the warpgroup collects the result. This overlaps matmul with softmax — a 1.5–2× throughput improvement.

#### 2. Ping-Pong Scheduling
Two warpgroups alternate: while warpgroup A does matmul, warpgroup B does softmax (and vice versa). This keeps both the tensor cores and CUDA cores busy continuously.

#### 3. FP8 Support
FA3 supports FP8 (e8m0) inputs, using Hopper's FP8 tensor cores. FP8 has 2× throughput compared to FP16, and for attention (where precision requirements are lower than for weight multiplication), the quality impact is minimal. FA3 with FP8 reaches 1.5–2.0 PFLOPS on H100.

#### 4. Low-Precision Accumulation
FA3 accumulates the attention matrix in FP32 (for numerical stability) but stores intermediate results in FP16 or FP8. This balances precision and throughput.

### FA3 Results

| Configuration        | FA2 (H100, FP16) | FA3 (H100, FP16) | FA3 (H100, FP8) |
|----------------------|------------------|------------------|-----------------|
| Sequence 4096        | 1.0×             | 1.5×             | 2.5×            |
| Sequence 8192        | 1.0×             | 1.7×             | 3.0×            |
| Sequence 16384       | 1.0×             | 1.8×             | 3.2×            |
| Peak FLOPS           | ~30%             | ~50%             | ~75%            |

FA3 with FP8 reaches 75% of H100's theoretical peak FLOPS for attention — a remarkable achievement for an exact (non-approximate) algorithm.

### Quality with FP8
FP8 attention has minimal quality impact compared to FP16:
- Perplexity increase: <0.5% on standard benchmarks.
- No measurable difference on downstream task accuracy.
- The precision loss is in the attention scores, not the value aggregation, so the impact is small.

## Why They Worked

### FA2: Better GPU Utilization
FA1's bottleneck was GPU utilization — for long sequences, not enough thread blocks to fill the GPU. FA2's sequence-parallel partitioning solved this, giving near-linear scaling with sequence length.

### FA3: Hardware Co-Design
FA3 is co-designed with Hopper's architecture. Every feature (WGMMA, async warpgroups, FP8, TMA) is exploited. This is the deepest level of hardware-aware algorithm design — the algorithm is rewritten to match the hardware's execution model.

### Exact Computation
Both FA2 and FA3 compute *exact* attention — same result as standard attention, up to floating-point precision. No approximation, no quality loss. This made adoption frictionless — models trained with FA2/FA3 converge to the same loss as with standard attention.

## Limitations

### FA2: Ampere-Bound
FA2 is optimized for Ampere (A100). On Hopper (H100), it doesn't use the new features — FA3 is needed for full H100 utilization.

### FA3: Hopper-Only
FA3 uses Hopper-specific instructions (WGMMA, async warpgroups). It cannot run on Ampere or older GPUs. For non-Hopper hardware, FA2 remains the best option.

### FP8 Quality Edge Cases
While FP8 attention is generally fine, some edge cases (very long sequences with many near-zero attention scores) can have numerical issues. FA3 includes a heuristic to fall back to FP16 for these cases.

### Complexity
FA3 is significantly more complex than FA2 (ping-pong scheduling, warpgroup coordination, async operations). Maintaining and extending the kernel requires deep GPU expertise.

## Impact and Legacy

FA2 and FA3 are foundational to modern LLM training and serving:

1. **Enabled 100K+ context lengths**. Without FA2/FA3, training models with 128K+ context (Llama 3.1, Claude 3, Gemini 1.5) would be economically infeasible. The O(N²) cost of attention is still there, but the constant factor is 5–10× smaller.

2. **Made H100 economics work**. FA3's 75% peak FLOPS utilization means H100 GPUs are actually profitable for LLM training. Without FA3, H100s would be underutilized and the ROI wouldn't justify the cost.

3. **Set the standard for kernel engineering**. FA2/FA3 demonstrated that hand-tuned CUDA kernels could deliver 5–10× speedups over framework-default implementations. This created a new class of "kernel engineer" role at frontier labs.

4. **Influenced hardware design**. The FA team's work informed NVIDIA's subsequent GPU designs. Hopper's WGMMA and async warpgroups were partly motivated by the FA team's analysis of what attention needed.

5. **Open-source kernel as competitive advantage**. The kernels were open-sourced, but the expertise to write them remained scarce. This created a moat for labs with kernel engineers.

For AI engineers, FA2/FA3 are invisible infrastructure: you almost never call them directly, but every LLM you train or serve uses them. Understanding FA2/FA3 matters when you need to debug a slow training run, choose between GPUs (A100 vs H100), or reason about long-context cost.

## Further Reading

- FA2 paper: arXiv:2307.08691
- FA3 paper: arXiv:2407.08608
- Tri Dao's `flash-attn` PyPI package — production implementation.
- [[08 - FlashAttention 2022]] — the original FA1 paper note.

## See Also

- [[08 - FlashAttention 2022]]
- [[11 - FlashAttention]]
- [[04 - Self-Attention]]
- [[12 - Sparse Attention]]
- [[13 - Linear Attention]]
- [[10 - PagedAttention vLLM 2023]]
- [[26 - Papers/MOC|Papers MOC]]
