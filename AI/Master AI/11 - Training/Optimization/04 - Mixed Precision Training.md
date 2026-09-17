---
tags: [training, mixed-precision, fp16, bf16, fp8, numerical]
iteration: 12
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Mixed Precision Training, FP16 Training, BF16 Training, FP8 Training]
---

# 04 — Mixed Precision Training

> [!info] TL;DR
> Mixed precision training uses lower-precision floating-point formats (FP16, BF16, FP8) for parts of the computation while keeping master weights in FP32 for accuracy. This reduces memory by 2-4×, increases throughput by 2-4× (via Tensor Core utilization), and enables training larger models on the same hardware. The three formats have different trade-offs: **FP16** has high precision but limited range (requires loss scaling), **BF16** has wide range but lower precision (no loss scaling needed), **FP8** (Hopper+) offers 4× memory reduction but requires careful per-tensor scaling. BF16 is the production default for pretraining; FP8 is emerging for the largest 2025-2026 training runs.

## Why Mixed Precision

Standard FP32 training uses 32 bits per parameter, gradient, and optimizer state. For a 7B model with Adam:

- Parameters: 7B × 4 bytes = 28 GB
- Gradients: 7B × 4 bytes = 28 GB
- Optimizer state (m, v): 7B × 8 bytes = 56 GB
- **Total: 112 GB** — doesn't fit on a single GPU (80GB A100).

Switching to BF16 for parameters and gradients:

- Parameters: 7B × 2 bytes = 14 GB
- Gradients: 7B × 2 bytes = 14 GB
- Optimizer state: 56 GB (still FP32 for stability)
- **Total: 84 GB** — fits on a single 80GB GPU with some headroom.

Beyond memory, mixed precision enables Tensor Cores — specialized GPU hardware that performs matrix multiplications 2-8× faster in FP16/BF16 than in FP32. Without mixed precision, you're leaving most of your GPU's compute capability on the table.

## The Three Formats

### FP16 (IEEE 754 half-precision)

- **Bits**: 1 sign + 5 exponent + 10 mantissa = 16 bits.
- **Range**: ~6e-5 to ~65504. Limited dynamic range.
- **Precision**: ~3 decimal digits.
- **Issue**: the limited range causes underflow (small gradients become zero) and overflow (large activations become inf).

FP16 requires **loss scaling** to work around the limited range. The loss is multiplied by a large scalar (e.g., 1024) before backpropagation, scaling gradients up so they don't underflow. After backprop, gradients are divided by the same scalar before the optimizer step. If gradients still overflow, the scale is reduced; if they don't, the scale is gradually increased.

```python
from torch.cuda.amp import GradScaler, autocast

scaler = GradScaler()
for batch in dataloader:
    with autocast(dtype=torch.float16):
        loss = model(batch)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

Loss scaling is fiddly. If the scale is too high, gradients overflow and the step is skipped; if too low, gradients underflow and the model degrades. The dynamic loss scaler in PyTorch handles this automatically, but it adds complexity.

### BF16 (Brain Float 16, Google)

- **Bits**: 1 sign + 8 exponent + 7 mantissa = 16 bits.
- **Range**: ~1e-38 to ~3e38. Same as FP32.
- **Precision**: ~2 decimal digits. Lower than FP16.

BF16 trades precision for range. The wide range means no underflow or overflow in normal training — no loss scaling needed. The lower precision means slightly higher numerical noise, but this is rarely a problem in practice.

BF16 is the **production default** for pretraining in 2026. NVIDIA Ampere (A100), Hopper (H100), and Blackwell (B100) GPUs all support BF16 Tensor Cores natively. PyTorch's `autocast(dtype=torch.bfloat16)` enables it transparently.

```python
for batch in dataloader:
    with autocast(dtype=torch.bfloat16):
        loss = model(batch)
    loss.backward()  # no GradScaler needed
    optimizer.step()
    optimizer.zero_grad()
```

The simpler API (no loss scaler) and wider range make BF16 strictly better than FP16 for new projects. Use FP16 only on older GPUs (V100 and earlier) that don't support BF16.

### FP8 (Hopper H100+, Blackwell B100+)

- **Bits**: 1 sign + 4-5 exponent + 2-3 mantissa = 8 bits.
- **Two variants**: E4M3 (4 exponent, 3 mantissa) and E5M2 (5 exponent, 2 mantissa). E4M3 has more precision; E5M2 has more range.
- **Range**: E4M3: ~0.0019 to ~448. E5M2: ~6e-8 to ~57344.
- **Precision**: ~1-2 decimal digits.

FP8 doubles the memory savings and throughput of BF16. On H100, FP8 matrix multiplication is ~2× faster than BF16. For 70B+ model training, this is a meaningful cost reduction (weeks of GPU time → days).

But FP8 is harder to use. The limited range and precision require:

- **Per-tensor scaling**: each tensor is scaled by a per-tensor factor that maps its values into the FP8 representable range. The scale is computed from the tensor's absmax.
- **Two-format strategy**: use E4M3 for forward pass (more precision) and E5M2 for backward gradients (more range).
- **Careful initialization**: weights must be initialized so their dynamic range fits FP8. Some standard inits (e.g., large He initialization) can produce values outside FP8 range.

```python
# Using Transformer Engine (NVIDIA's FP8 library)
import transformer_engine.pytorch as te
from transformer_engine.common.recipe import Format, DelayedScaling

model = te.LayerNormMLP(...)
recipe = DelayedScaling(momentum=0.5, fp8_format=Format.HYBRID)

for batch in dataloader:
    with te.fp8_autocast(enabled=True, fp8_recipe=recipe):
        loss = model(batch)
    loss.backward()
    optimizer.step()
```

FP8 training is currently the cutting edge. Most production 2025-2026 training runs use FP8 for the largest models, with BF16 as a fallback when stability issues arise.

## Master Weights in FP32

The key to mixed precision stability is keeping **master weights in FP32**. The forward and backward passes use FP16/BF16, but the optimizer updates FP32 master weights, which are then cast to FP16/BF16 for the next forward pass.

Why? Because small updates (e.g., `weight -= lr * gradient` where `lr * gradient` is small) can be lost when added to FP16 weights. The FP16 representation can't distinguish `weight` from `weight + small_update`. FP32 master weights preserve these small updates.

This means the optimizer state (master weights + Adam's m and v) is always FP32, even when the model parameters are FP16. The memory savings come from activations and gradients, which can be FP16/BF16.

```python
# Conceptual model
master_weights = [p.detach().clone().float() for p in model.parameters()]
for p in master_weights:
    p.requires_grad = True

for batch in dataloader:
    # Cast master weights to FP16 for forward
    for p, master_p in zip(model.parameters(), master_weights):
        p.data = master_p.data.half()
    
    with autocast(dtype=torch.float16):
        loss = model(batch)
    loss.backward()
    
    # Update FP32 master weights
    for master_p, p in zip(master_weights, model.parameters()):
        master_p.grad = p.grad.float()
    optimizer.step()
```

PyTorch's AMP (Automatic Mixed Precision) handles this automatically with `model.half()` and the `GradScaler`. For BF16, the situation is simpler — BF16's range matches FP32, so master weights can sometimes be in BF16 too (though FP32 master is still recommended for stability).

## Common Pitfalls

### Forgetting Master Weights

If you naively use `model.half()` and `optimizer.step()`, you're doing pure FP16 training without master weights. This silently degrades model quality — small updates are lost, the model converges to a worse solution. Always use AMP or manually maintain FP32 master weights.

### Loss Scale Instability (FP16)

If your loss scale is wrong, you'll see one of two symptoms:

- **"Gradient overflow" warnings**: gradients became inf. The optimizer step is skipped. Training stalls.
- **Loss goes to NaN**: underflow in FP16 produced zero gradients, then a bad update, then NaN.

Tune the initial scale (try 2^16) and let the dynamic scaler adjust. If problems persist, switch to BF16.

### Softmax in FP16

Softmax involves `exp(x)`, which overflows in FP16 if `x > 11`. Numerically stable softmax subtracts `max(x)` first, but if your model produces large logits, you can still hit overflow. Use FP32 for the softmax specifically (most frameworks do this automatically).

### LayerNorm in FP16

LayerNorm computes mean and variance, which can be numerically unstable in FP16. Most frameworks compute LayerNorm in FP32 internally even when the rest of the model is FP16. If you implement custom LayerNorm, do the same.

### Initializer Mismatch

Some initializers (He, Glorot) assume FP32. When applied to FP16 weights, they can produce values that overflow (rare) or underflow (common). Initialize in FP32, then cast to FP16.

### Inference vs. Training Precision

A model trained in BF16 can be inferred in BF16 or FP16 (with some accuracy loss). A model trained in FP8 typically needs FP8 inference for best results — the model has adapted to FP8's noise patterns. Document your training precision so users can infer correctly.

## Performance Considerations

### Tensor Core Requirements

Tensor Cores require matrix dimensions to be multiples of 8 (for FP16) or 16 (for FP8, on Hopper). If your model has hidden_size 1024, you're fine. If it's 1023, you're not using Tensor Cores and getting no speedup. Pad to multiples of 8/16.

### Batch Size

Larger batches amortize kernel launch overhead and improve Tensor Core utilization. Mixed precision training benefits more from large batches than FP32 training does.

### Activation Checkpointing

Mixed precision reduces memory for parameters and gradients but not for activations. For long-sequence training, activation checkpointing (recomputing activations during backward instead of storing them) is still needed. Combine the two for maximum memory savings.

### Optimizer Choice

Adam's optimizer state (m and v) is 2× the parameter count. Switching to memory-efficient optimizers (Adafactor, Lion, 8-bit Adam) reduces this. Combined with mixed precision, these can fit much larger models on a single GPU.

## When to Use Which Format

| Format | When to Use                                       | When NOT to Use                          |
|--------|---------------------------------------------------|------------------------------------------|
| FP32   | Final fine-tuning for max stability; debugging    | Large-scale pretraining (too slow)       |
| FP16   | V100 and older GPUs; small models (<1B)           | New projects on A100+ (use BF16 instead) |
| BF16   | Default for A100, H100, B100; most training       | Older GPUs without BF16 support          |
| FP8    | Largest training runs on H100/B100; pretraining   | Fine-tuning (stability matters more)     |

## Practical Recommendations

1. **Use BF16 by default** on A100 or newer GPUs. It's the simplest and most stable.
2. **Use FP8 for the largest pretraining runs** where the 2× speedup matters. Expect some engineering effort for stability.
3. **Always use FP32 master weights** (handled automatically by AMP).
4. **Validate with FP32 periodically**: every N steps, run a few batches in FP32 and compare loss. If they diverge, your mixed precision is unstable.
5. **Use `autocast` rather than manual casting**: PyTorch's autocast handles the FP32-for-softmax-and-layernorm logic automatically.
6. **Match inference precision to training precision** for best results.

## See Also

- [[02 - Distributed Training]] — distributed training uses mixed precision
- [[03 - Data Pipelines and Deduplication]] — what you're training on
- [[05 - Loss Spikes and Stability]] — what happens when precision is wrong
- [[12 - Optimization Essentials]] — optimizers used with mixed precision
- [[14 - Learning Rate Schedules]] — schedules interact with precision
- [[03 - Quantization]] — inference-time quantization (related but distinct)
- [[11 - Training/MOC|11 Training MOC]]


## Interview Questions

1. **Q: Why does BF16 not need loss scaling while FP16 does?**
   A: FP16 has 5 exponent bits (range ~6e-5 to ~65504) — small gradients underflow to zero. Loss scaling multiplies the loss by a large factor before backprop, keeping gradients in range. BF16 has 8 exponent bits (same range as FP32: ~1e-38 to ~3e38) — no underflow, no loss scaling needed. BF16 trades precision (7 mantissa bits vs FP16's 10) for range, which is the right tradeoff for training.

2. **Q: Why are master weights kept in FP32?**
   A: Small updates (e.g., `weight -= lr * gradient` where `lr * gradient` is 0.001) can be lost when added to FP16/BF16 weights — the representation can't distinguish `weight` from `weight + small_update`. FP32 master weights preserve these small updates. The optimizer updates FP32 master weights; they're cast to FP16/BF16 for the next forward pass.

3. **Q: What is FP8 training and what are its challenges?**
   A: FP8 (8-bit) on Hopper+ doubles throughput and halves memory vs BF16. Challenges: (1) limited range requires per-tensor scaling (each tensor scaled by absmax); (2) two formats — E4M3 (precision) for forward, E5M2 (range) for backward; (3) careful init needed (values must fit FP8 range); (4) stability monitoring required. Most 2025-2026 frontier training uses FP8 with BF16 fallback.

4. **Q: When would you use FP16 vs BF16 vs FP8?**
   A: FP16: only on older GPUs (V100) without BF16 support. BF16: default for A100+ (simplest, most stable). FP8: largest training runs on H100/B100 where 2x speedup matters. FP32: debugging or final fine-tuning for max stability.

5. **Q: How do Tensor Cores interact with mixed precision?**
   A: Tensor Cores perform matrix multiplication in FP16/BF16/FP8 (2-8x faster than FP32). They require matrix dimensions to be multiples of 8 (FP16) or 16 (FP8). If your hidden_size is 1023, you're not using Tensor Cores — pad to 1024. This is why LLM dimensions are multiples of 128.

6. **Q: What goes wrong if you naively use `model.half()` without AMP?**
   A: You're doing pure FP16 without master weights. Small updates are lost → model converges to a worse solution silently. Use `torch.autocast` or manually maintain FP32 master weights. AMP handles the FP32-for-softmax-and-LayerNorm logic automatically.

## Connection to Other Concepts

- [[11 - Training/Distributed Training/02 - Distributed Training|Distributed Training]] — distributed + mixed precision together.
- [[11 - Training/Optimization/05 - Loss Spikes and Stability|Loss Spikes]] — mixed precision can cause spikes.
- [[13 - Inference/Quantization/03 - Quantization|Quantization]] — inference-time quantization (related but distinct).
- [[02 - Mathematics/Optimization/13 - Adam Derivation|Adam Derivation]] — optimizer state in FP32.
- [[02 - Mathematics/Linear Algebra/06 - Tensors and Broadcasting|Tensors and Broadcasting]] — Tensor Core alignment.
