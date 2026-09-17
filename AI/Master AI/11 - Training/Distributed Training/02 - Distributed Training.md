---
tags: [training, distributed, zero, fsdp, tensor-parallel]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Distributed Training, ZeRO, FSDP]
---

# 02 - Distributed Training (DP, TP, PP, ZeRO, FSDP)

> [!info] TL;DR
> Training a 70B+ model requires distributed training across many GPUs. The four main parallelism strategies — data parallel, tensor parallel, pipeline parallel, and ZeRO/FSDP — can be combined. Modern LLM training uses 3D parallelism (DP + TP + PP) plus ZeRO-style sharding.

## Why Distributed Training?

A 70B model in fp16: 140 GB of weights. Optimizer state (AdamW): 4x = 560 GB. Activations: 100+ GB. Total: ~800 GB per replica — way past an 80GB H100.

So you need to **shard the model across multiple GPUs**, and you need to **parallelize the computation** across them.

## The Four Parallelism Strategies

### 1. Data Parallelism (DP)

Each GPU has a **full copy** of the model. Each processes a different batch. Gradients are averaged across GPUs (all-reduce) before the optimizer step.

```
GPU 0: model + batch 0 → grads → all-reduce → update
GPU 1: model + batch 1 → grads → all-reduce → update
GPU 2: model + batch 2 → grads → all-reduce → update
GPU 3: model + batch 3 → grads → all-reduce → update
```

- Simple, works for any model that fits in one GPU.
- Memory: each GPU needs full model + optimizer + activations.
- Doesn't help if the model is too big for one GPU.

### 2. Tensor Parallelism (TP)

Split individual weight matrices across GPUs. For $\mathbf{y} = \mathbf{W}\mathbf{x}$ with $\mathbf{W} \in \mathbb{R}^{n \times m}$:

- **Column parallel**: each GPU holds $\mathbf{W}_i \in \mathbb{R}^{n \times m/k}$, computes $\mathbf{y}_i = \mathbf{W}_i \mathbf{x}$. Concatenate the $\mathbf{y}_i$s.
- **Row parallel**: each GPU holds $\mathbf{W}_i \in \mathbb{R}^{n/k \times m}$, computes a partial sum. All-reduce to combine.

For a Transformer block: attention Q/K/V/O projection split column-parallel, then FFN split row-parallel (or vice versa), with one all-reduce per block.

- Memory: weights sharded across $k$ GPUs.
- Communication: all-reduce per layer (high bandwidth required).
- Typically combined with NVLink-connected GPUs (within a node).

### 3. Pipeline Parallelism (PP)

Split the layers across GPUs. GPU 0 has layers 1–10, GPU 1 has 11–20, etc. Activations flow forward through the pipeline; gradients flow backward.

```
GPU 0: layers 1-10 → activations → GPU 1
GPU 1: layers 11-20 → activations → GPU 2
GPU 2: layers 21-30 → activations → GPU 3
GPU 3: layers 31-40 → loss → backward
```

- Memory: layers sharded across GPUs.
- **Bubble problem**: while GPU 1 processes batch 1, GPU 0 is idle (or processing batch 2). "Pipeline bubble" = wasted compute.
- **Micro-batching**: split each batch into smaller micro-batches and pipeline them. Reduces the bubble.

### 4. ZeRO (Zero Redundancy Optimizer)

DP replicates the full model + optimizer + gradients on every GPU. ZeRO shards these:

- **ZeRO-1**: shard optimizer state (the biggest chunk — Adam's m and v are 8x params in fp32).
- **ZeRO-2**: shard optimizer state + gradients.
- **ZeRO-3**: shard optimizer state + gradients + parameters (full sharding).

ZeRO-3 is essentially what FSDP (Fully Sharded Data Parallel) does in PyTorch.

With ZeRO-3 / FSDP, each GPU only holds $1/k$ of the model. Before each layer's forward, the shards are gathered (all-gather); after backward, they're reduced (reduce-scatter).

### FSDP (PyTorch's ZeRO-3)

PyTorch's native implementation of ZeRO-3. Standard for modern LLM training in PyTorch.

## Combining: 3D Parallelism

For very large models (70B+), combine all three:

- **TP within a node** (8 GPUs connected by NVLink, fast all-reduce).
- **PP across nodes** (slower communication, but pipeline can hide it).
- **DP / ZeRO across the cluster** (scale to many nodes).

Example for a 70B model on 64 H100 GPUs (8 nodes × 8 GPUs):
- TP=8 (within each node).
- PP=4 (across 4 pipeline stages = 4 nodes per stage... actually 8 nodes total so 2 stages of 4 nodes each, but let's say PP=4 = 4 stages of 2 nodes each).
- DP=2 (data parallel replicas).

Plus ZeRO-1 for optimizer state sharding.

## Worked Example (FSDP)

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import ShardingStrategy, MixedPrecision

model = AutoModelForCausalLM.from_pretrained(...)
model = FSDP(
    model,
    sharding_strategy=ShardingStrategy.FULL_SHARD,  # ZeRO-3
    mixed_precision=MixedPrecision(
        param_dtype=torch.bfloat16,
        reduce_dtype=torch.bfloat16,
    ),
    auto_wrap_policy=...,
)
```

In practice, use a framework like Megatron-LM, DeepSpeed, or TorchTitan that handles the 3D parallelism setup.

## Why This Matters for AI

- If you train large models, **distributed training is mandatory**. Understanding the tradeoffs is essential.
- For fine-tuning with LoRA, you usually don't need distributed training — LoRA params are small enough for a single GPU.
- For inference, **tensor parallelism** is the most common (vLLM supports it natively).
- The shift from DP-only to 3D parallelism is what enabled 100B+ model training.

## Production Implications

- **Fine-tuning (LoRA)**: usually single-GPU. No distributed setup needed.
- **Full fine-tuning of 7B+**: use FSDP across multiple GPUs.
- **Continued pretraining**: use a framework (DeepSpeed, Megatron, TorchTitan). Don't roll your own.
- **Communication is the bottleneck** for distributed training. NVLink within a node (300+ GB/s) >> InfiniBand between nodes (50-100 GB/s) >> Ethernet (10-25 GB/s). Plan cluster topology accordingly.

## Common Pitfalls

- **Wrong TP size** — too high (e.g., TP=8 across nodes) kills performance due to slow inter-node all-reduce. TP should be within a node.
- **Pipeline bubble too large** — too few micro-batches. Increase micro-batch count.
- **Forgetting activation checkpointing** — long-context training OOMs without it.
- **Mixed precision issues** — fp16 needs loss scaling; bf16 doesn't. Don't mix.
- **Wrong learning rate for distributed** — when you scale batch size, scale LR too (linear scaling rule, see [[02 - Mathematics/Optimization/14 - Learning Rate Schedules|LR Schedules]]).

## Further Reading

- Rajbhandari et al. (2020), *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*.
- Shoeybi et al. (2019), *Megatron-LM*.
- Narayanan et al. (2021), *Efficient Large-Scale Language Model Training on GPU Clusters* (3D parallelism).
- PyTorch FSDP docs: https://pytorch.org/docs/stable/fsdp.html

## See Also

- [[01 - Pretraining Objectives and Scaling Laws|Pretraining & Scaling Laws]]
- [[12 - Fine-Tuning/MOC|Fine-Tuning MOC]]
- [[11 - Training/MOC|Training MOC]]
- [[13 - Inference/MOC|Inference MOC]] — distributed inference uses similar techniques


## Interview Questions

1. **Q: What's the difference between DP, TP, PP, and ZeRO/FSDP?**
   A: DP replicates the full model on each GPU, processing different batches. TP splits individual weight matrices across GPUs (column-parallel or row-parallel). PP splits layers across GPUs (pipeline stages). ZeRO/FSDP shards optimizer state, gradients, and parameters across GPUs (like DP but without replication). Modern training combines all four (3D parallelism): TP within a node, PP across nodes, DP/ZeRO across the cluster.

2. **Q: When would you use FSDP vs DeepSpeed ZeRO-3?**
   A: FSDP is PyTorch-native and simpler. DeepSpeed offers more features (CPU offload, NVMe offload, custom configs). For most new projects, FSDP is sufficient. Choose DeepSpeed when you need CPU/NVMe offload or specific ZeRO configurations.

3. **Q: What is the pipeline bubble and how do you reduce it?**
   A: The pipeline bubble is idle time when earlier pipeline stages wait for later stages to finish. Reduce it with micro-batching: split each batch into smaller micro-batches and pipeline them, so GPU 0 can start on micro-batch 2 while GPU 1 processes micro-batch 1. More micro-batches = smaller bubble but more memory for activations.

4. **Q: How does tensor parallelism work for a Transformer block?**
   A: QKV projection is column-parallel (each GPU computes a subset of heads). The attention output is row-parallel (each GPU computes a partial sum). One all-reduce per block combines the partial sums. This requires NVLink-connected GPUs (within a node) for low-latency communication.

5. **Q: How much memory does ZeRO-3/FSDP save?**
   A: ZeRO-3 shards parameters + gradients + optimizer state across $k$ GPUs. Each GPU holds $1/k$ of the total. For a 70B model with AdamW: ~280 GB total → ~35 GB per GPU on 8 GPUs. Without ZeRO-3, you'd need 280 GB on each GPU.

6. **Q: What's the linear scaling rule for distributed training?**
   A: When you multiply batch size by $k$, multiply LR by $k$ (with proportional warmup). Works for moderate changes (2-8x). For very large batches (>8x), use sqrt scaling or LARS/LAMB. The rule assumes gradient noise variance scales as $1/B$.

## Connection to Other Concepts

- [[27 - Projects/Capstones/11 - Build a Distributed Training Pipeline|Build a Distributed Training Pipeline]] — hands-on FSDP implementation.
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — distributed + mixed precision together.
- [[02 - Mathematics/Optimization/12 - Optimization Essentials|Optimization Essentials]] — the optimizer being distributed.
- [[02 - Mathematics/Optimization/14 - Learning Rate Schedules|Learning Rate Schedules]] — LR scaling with batch size.
- [[11 - Training/Pretraining/01 - Pretraining Objectives and Scaling Laws|Pretraining Objectives]] — what's being trained.
- [[13 - Inference/Serving/04 - vLLM and Continuous Batching|vLLM]] — tensor parallelism at inference.
- [[26 - Papers/2024-2026/42 - Scaling Laws (Kaplan and Chinchilla)|Scaling Laws]] — compute-optimal training at scale.
