---
source_collections:
  - "TAMER 2"
  - "TAMER 3"
original_paths:
  - "TAMER 2/Chapter 9 - Training Infrastructure and Techniques/2. Multi-GPU Training with DataParallel.md"
  - "TAMER 3/08_Evaluation_and_MLOps/04_Section_3_Multi-GPU_Training_DataParallel.md"
roles_in_master:
  - "canonical"
  - "supplement"
topic: "multi_gpu"
master_chapter: "100_Training_Infrastructure_and_Techniques"
master_filename: "02_Multi_GPU_Training_DataParallel.md"
n_source_files_merged: 2
merged: True
---

# 2. Multi-GPU Training with DataParallel

## 2.1 Why Multi-GPU Training Is Necessary

The TAMER OCR model is a large vision-language architecture consisting of a Swin-V2 encoder (roughly 88 million parameters) and a RoBERTa-based decoder (roughly 125 million parameters). Combined with the cross-attention bridge, the total model size exceeds **200 million parameters**. At a batch size of 864 images, the memory requirements are staggering:

- **Model parameters**: ~200M × 4 bytes (FP32 master copy) = ~800 MB
- **Model gradients**: ~200M × 2 bytes (BF16) = ~400 MB
- **Optimizer state** (AdamW: momentum + variance): ~200M × 4 bytes × 2 = ~1.6 GB
- **Activations** (forward pass intermediates for backprop): several GB depending on image resolution
- **Input data**: 864 images × 3 channels × 384 × 384 × 4 bytes = ~1.4 GB

A single GPU cannot hold all of this. The RTX 6000 Ada has 48 GB of VRAM, which sounds generous, but even with gradient checkpointing and mixed precision, the peak memory during training comfortably exceeds what one GPU can provide. Multi-GPU training is not a luxury — it is a **necessity**.

## 2.2 DataParallel: The Simplest Multi-GPU Strategy

PyTorch's `torch.nn.DataParallel` (DP) is the simplest way to distribute training across multiple GPUs. It wraps an existing model and transparently handles the distribution of data and collection of results. The usage is delightfully simple:

```python
model = TamerOCR(config)
model = torch.nn.DataParallel(model, device_ids=[0, 1, 2, 3])
```

That single wrapping line transforms the model from a single-GPU model to a multi-GPU model. No code changes to the training loop, no process spawning, no distributed samplers.

### How DataParallel Works

The mechanism of DataParallel follows a clear **scatter–replicate–parallel–gather** pattern:

1. **Scatter**: The input batch is split into roughly equal chunks along the batch dimension. With 4 GPUs and batch_size=864, each GPU receives 216 samples.

2. **Replicate**: The model is copied to each GPU. Each replica holds a full copy of the model parameters. This is a significant memory overhead — each GPU stores the entire model — but it is necessary because PyTorch's autograd needs a local computation graph.

3. **Parallel Forward**: Each GPU independently runs the forward pass on its chunk of data. The computation is truly parallel; all GPUs compute simultaneously.

4. **Gather**: The outputs from all GPUs are collected back on the primary GPU (device 0), where the loss is computed and the backward pass begins. Gradients from each replica are then averaged and applied to the model on the primary GPU, and the updated parameters are broadcast to all replicas at the start of the next iteration.

This pattern repeats every training step. The key limitation is that the **gradient averaging and parameter broadcast** happen through Python-level threading, which introduces overhead. Additionally, GPU 0 does more work (it handles the gather, loss computation, and broadcast), leading to a **load imbalance** where GPU 0 is often the bottleneck.

## 2.3 The .module Attribute and Model Unwrapping

When you wrap a model with `DataParallel`, the original model becomes accessible as the `.module` attribute of the DataParallel object. This means:

```python
# Before wrapping:
model.encoder  # Direct access to the encoder

# After wrapping:
model.module.encoder  # Must go through .module first
```

This is not just a cosmetic inconvenience. Many operations require accessing the raw model directly:

- **Freezing/unfreezing layers**: `model.module.encoder.requires_grad_(False)`
- **Accessing model configuration**: `model.module.config`
- **Saving checkpoints**: You want to save `model.module.state_dict()`, not `model.state_dict()`, to avoid the `module.` prefix in key names
- **Computing parameter counts**: `sum(p.numel() for p in model.module.parameters())`

If you forget the `.module` and try `model.encoder`, you get an `AttributeError`, because `DataParallel` does not forward arbitrary attribute access to the wrapped model.

## 2.4 The _unwrap_model() Helper

TAMER OCR introduces a `_unwrap_model()` helper function that recursively unwraps a model from any combination of DataParallel and `torch.compile` wrappers:

```python
def _unwrap_model(model):
    """Unwrap model from DataParallel and torch.compile wrappers."""
    if hasattr(model, "module"):
        return _unwrap_model(model.module)
    if hasattr(model, "_orig_mod"):
        return _unwrap_model(model._orig_mod)
    return model
```

This recursive function handles two layers of wrapping:

1. **DataParallel wrapping**: The `.module` attribute stores the original model.
2. **torch.compile wrapping**: The `._orig_mod` attribute stores the pre-compilation model.

By recursing, `_unwrap_model` works correctly regardless of the wrapping order. Whether the model is `DataParallel(torch.compile(raw_model))` or `torch.compile(DataParallel(raw_model))`, calling `_unwrap_model` always returns the raw `TamerOCR` instance.

This function is used throughout the codebase wherever direct model access is needed:

```python
# Freezing the encoder during early training:
_unwrap_model(model).encoder.requires_grad_(False)

# Saving a checkpoint (no "module." prefix in keys):
torch.save(_unwrap_model(model).state_dict(), path)

# Accessing the tokenizer for decoding:
tokenizer = _unwrap_model(model).tokenizer
```

## 2.5 DataParallel vs DistributedDataParallel

It is worth understanding why TAMER OCR uses DataParallel instead of the more commonly recommended DistributedDataParallel (DDP):

| Feature | DataParallel | DistributedDataParallel |
|---|---|---|
| Setup complexity | One line of code | Requires process spawning, dist.init_process_group |
| Code changes | Minimal | Must use DistributedSampler, adjust rank-aware logic |
| Performance | Thread-based, GIL-limited | Process-based, true parallelism |
| Memory efficiency | Each GPU holds full model + optimizer | Same (unless using FSDP or model parallelism) |
| Gradient sync | After backward, on GPU 0 | During backward, all-reduce across GPUs |
| Load balance | GPU 0 is the bottleneck | Perfectly balanced |

For TAMER OCR, DataParallel was chosen for **simplicity**. The project was initially developed on a single machine with 4 GPUs, and the overhead of setting up DDP was not justified for that scale. The training speed with DP on 4 GPUs was sufficient — the model trained in reasonable time, and the GPU utilization was acceptable.

However, if the project were to scale to more GPUs or multiple machines, migrating to DDP would be recommended. DDP's `all-reduce` gradient synchronization overlaps with backward computation, providing significantly better scaling efficiency, especially beyond 4 GPUs.

## 2.6 Batch Splitting in Practice

When using DataParallel, the effective per-GPU batch size is:

$$\text{batch\_per\_gpu} = \frac{\text{total\_batch\_size}}{\text{num\_gpus}}$$

With `batch_size=864` and 4 GPUs, each GPU processes 216 images per step. This is important for:

- **Memory planning**: Each GPU needs enough VRAM for 216 forward/backward passes.
- **Batch normalization**: If the model uses batch norm, the statistics are computed per-GPU on 216 samples, not 864. Swin-V2 uses LayerNorm, so this is not an issue for TAMER OCR.
- **Gradient accumulation**: If the effective batch size is achieved through gradient accumulation, the accumulation steps operate on the per-GPU batch size.

## 2.7 Wrapping Order: Raw Model → DataParallel → torch.compile

The correct wrapping order for combining DataParallel with `torch.compile` is:

```python
# Step 1: Create the raw model
model = TamerOCR(config)

# Step 2: Wrap with DataParallel
model = torch.nn.DataParallel(model, device_ids=[0, 1, 2, 3])

# Step 3: Compile with torch.compile
model = torch.compile(model)
```

This order matters because `torch.compile` traces the computation graph and applies optimizations (operator fusion, memory planning) to the entire DataParallel-wrapped model. If you compiled first and then wrapped with DataParallel, each GPU would receive a separately compiled replica, and the compilation overhead would multiply by the number of GPUs.

By compiling the DataParallel wrapper, PyTorch can optimize the scatter/gather operations alongside the model computation, potentially fusing data transfer with computation for better pipeline utilization.

## 2.8 DataParallel Flow Diagram

The following Mermaid diagram illustrates the complete DataParallel flow for a single training step:

```mermaid
flowchart TD
    A[Input Batch: 864 images] --> B[Scatter: Split into 4 chunks of 216]
    B --> C1[GPU 0: 216 images]
    B --> C2[GPU 1: 216 images]
    B --> C3[GPU 2: 216 images]
    B --> C4[GPU 3: 216 images]

    D1[Model Replica 0] --> E1[Forward on GPU 0]
    D2[Model Replica 1] --> E2[Forward on GPU 1]
    D3[Model Replica 2] --> E3[Forward on GPU 2]
    D4[Model Replica 3] --> E4[Forward on GPU 3]

    C1 --> E1
    C2 --> E2
    C3 --> E3
    C4 --> E4

    E1 --> F[Gather: Collect outputs on GPU 0]
    E2 --> F
    E3 --> F
    E4 --> F

    F --> G[Compute Loss on GPU 0]
    G --> H[Backward Pass: Gradients computed on each GPU]
    H --> I[Average Gradients on GPU 0]
    I --> J[Optimizer Step on GPU 0]
    J --> K[Broadcast Updated Parameters to All GPUs]

    style B fill:#4a90d9,color:#fff
    style F fill:#e8a838,color:#000
    style G fill:#e8a838,color:#000
    style I fill:#4ad94a,color:#000
    style K fill:#d94a4a,color:#fff
```

## 2.9 Key Takeaways

1. **DataParallel is the simplest multi-GPU solution** — a single line of code enables multi-GPU training.
2. **Always use `_unwrap_model()`** when you need to access the raw model for freezing, saving, or configuration.
3. **The wrapping order matters**: raw model → DataParallel → torch.compile.
4. **DP has limitations**: GPU 0 is a bottleneck, and GIL contention reduces efficiency. For >4 GPUs, consider DDP.
5. **Batch splitting is automatic**: DataParallel handles it transparently, but be aware of per-GPU memory constraints.

---

## Supplementary Perspective — from TAMER 3

> **Original file:** `TAMER 3/08_Evaluation_and_MLOps/04_Section_3_Multi-GPU_Training_DataParallel.md`  
> **Role in master vault:** supplement perspective from TAMER 3 — T3 supplement.  
> **Preservation policy:** full original text reproduced verbatim below; nothing omitted.

---

### 3. Multi-GPU Training (DataParallel)

#### The Parallelism Strategy

`torch.nn.DataParallel` implements **Data Parallelism**: the same model is replicated on multiple GPUs, and different mini-batches of data are processed simultaneously on each GPU.

**Step-by-step operation for 4 GPUs:**

1. **Scatter:** The mega-batch of size $B_{total} = 864$ is split into 4 chunks of $B_{chunk} = 216$. Each chunk is sent to one GPU.

2. **Replicate:** The model weights (which live on GPU 0) are copied to GPUs 1, 2, 3 at the start of every forward pass.

3. **Forward:** Each GPU runs its forward pass independently with its chunk. GPU 0 processes images 0-215, GPU 1 processes 216-431, etc.

4. **Gather:** The outputs from all GPUs are gathered back to GPU 0.

5. **Loss:** The combined loss is computed on GPU 0.

6. **Backward:** Gradients are computed on GPU 0 (for the gathered batch) and then scattered back to GPUs 1, 2, 3 to allow parallel gradient computation... but in `DataParallel`, the backward pass actually happens entirely on GPU 0 after gathering. This is a known inefficiency.

7. **Update:** The optimizer step updates weights on GPU 0. On the next iteration, these updated weights are recopied to all GPUs.

```mermaid
flowchart TD
    A["Mega Batch: 864 Images\nGPU 0 Main Memory"] --> B["Split into 4 chunks\n216 images each"]
    B --> C["GPU 0: Images 0-215\nForward Pass"]
    B --> D["GPU 1: Images 216-431\nForward Pass"]
    B --> E["GPU 2: Images 432-647\nForward Pass"]
    B --> F["GPU 3: Images 648-863\nForward Pass"]
    C --> G["Gather Outputs\non GPU 0"]
    D --> G
    E --> G
    F --> G
    G --> H["Compute Loss\non GPU 0"]
    H --> I["Backward Pass\non GPU 0"]
    I --> J["Optimizer Step\non GPU 0"]
    J --> K["Copy Updated Weights\nto GPU 1, 2, 3"]
```

> **Important reminder:** `DataParallel` has a known inefficiency: GPU 0 is the bottleneck. It gathers all outputs, computes loss, and runs the full backward pass. GPU 0 always has higher memory usage than GPUs 1-3. The effective batch size per GPU is $B_{total} / N_{GPUs}$, but GPU 0's VRAM must hold the full gathered tensor. The production solution for extreme multi-GPU training is `DistributedDataParallel` (DDP), which does not have this bottleneck. Each GPU computes its own loss and gradients, and gradients are all-reduced (averaged) across GPUs using NCCL. DDP is strictly superior but requires more complex setup. TAMER uses `DataParallel` as a simpler baseline and switches to DDP for training runs with 4+ GPUs.

---

#### Effective Batch Size and Learning Rate Scaling

When using $N$ GPUs with batch size $B$ per GPU, the effective batch size is $N \times B$. The model sees $N$ times more data per optimizer step.

This changes the optimal learning rate. The **Linear Scaling Rule** (from the Facebook Research paper on large-batch training) states: if the batch size is multiplied by $k$, the learning rate should also be multiplied by $k$.

**Intuition:** With a larger batch, the gradient estimate is more accurate (lower variance). You can take a larger step in the direction of the true gradient without overshooting. A learning rate optimal for batch size 64 will cause overshooting instability at batch size 864.

**TAMER's Warmup Strategy:**
Even with the linear scaling rule, starting at the full large-batch learning rate causes instability in early training (the model weights are random, gradient magnitudes are unpredictable). TAMER uses a **warmup schedule**:

- Epochs 1-10: Linearly increase from $\text{LR}_{min} = 10^{-6}$ to $\text{LR}_{max} = k \times \text{LR}_{base}$.
- Epochs 10-100: Cosine anneal from $\text{LR}_{max}$ back to $\text{LR}_{min}$.

$$\text{LR}(t) = \text{LR}_{min} + \frac{1}{2}(\text{LR}_{max} - \text{LR}_{min})\left(1 + \cos\left(\frac{\pi t}{T_{total}}\right)\right)$$

This prevents gradient explosion in early training and allows fine-grained convergence in late training.

---

*End of TAMER Math OCR - Deep Learning Theory & Architecture Vault*
