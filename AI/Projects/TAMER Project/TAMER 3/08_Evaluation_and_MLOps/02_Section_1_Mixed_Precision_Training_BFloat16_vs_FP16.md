## 1. Mixed Precision Training (BFloat16 vs FP16)

### The Case for Reduced Precision

Standard neural network training uses 32-bit floating-point (FP32). Every parameter, gradient, and activation is stored as a 32-bit number. For the TAMER model with 100M parameters:

$$100 \times 10^6 \text{ parameters} \times 4 \text{ bytes/param} = 400 \text{ MB for parameters}$$

But training also requires:
- Gradients: 400 MB (same size as parameters).
- Optimizer state (Adam): 800 MB (two moment estimates per parameter).
- Activations (for backprop): varies, but often 2-4× parameters.

Total: ~3-4 GB for the model alone, before the data batch.

Using 16-bit precision cuts each of these by 2×, approximately halving VRAM usage and doubling GPU throughput (16-bit arithmetic is faster on modern GPU tensor cores).

---

### FP16 vs BFloat16: The Numerical Range Problem

**FP32 format:** 1 sign bit, 8 exponent bits, 23 fraction bits.
- Largest representable value: ~$3.4 \times 10^{38}$
- Smallest positive: ~$1.2 \times 10^{-38}$

**FP16 format:** 1 sign bit, 5 exponent bits, 10 fraction bits.
- Largest representable value: 65,504
- Smallest positive: ~$6 \times 10^{-8}$

The narrow range of FP16 causes **gradient overflow**: if a gradient value exceeds 65,504, it becomes `inf`. Operations with `inf` produce `NaN`. One `NaN` gradient propagated back through the network corrupts all weights connected to it. The entire training run is destroyed.

Standard FP16 training uses **Loss Scaling** to work around this: multiply the loss by a large constant (e.g., 1024) before backprop, so gradients are artificially inflated to lie in the FP16 range, then divide after. This works but is fragile (the scale factor must be tuned) and occasionally fails.

**BFloat16 format:** 1 sign bit, 8 exponent bits, 7 fraction bits.
- Largest representable value: ~$3.4 \times 10^{38}$ (same exponent range as FP32)
- Smallest positive: ~$1.2 \times 10^{-38}$ (same as FP32)

BF16 has the same exponent range as FP32 (8 exponent bits), so it can represent the same magnitude of numbers. It just has lower precision in the fraction (less decimal accuracy). This means:
- Gradient overflow: **impossible** (same range as FP32).
- Loss Scaling: **not needed**.
- Training stability: **equivalent to FP32**.
- Memory/speed savings: **same as FP16** (still 16 bits total).

**The only downside of BF16:** Lower decimal precision. For gradient accumulation over many steps, rounding errors can accumulate. TAMER mitigates this by keeping optimizer states in FP32 (the "mixed" in mixed precision: forward/backward in BF16, parameter update in FP32).

---

### PyTorch AMP (Automatic Mixed Precision) with BF16

```python
# Context manager automatically casts operations to BF16
with torch.autocast(device_type='cuda', dtype=torch.bfloat16):
    predictions = model(images, target_tokens)
    loss = criterion(predictions, targets)

# No GradScaler needed for BF16 (unlike FP16)
loss.backward()
optimizer.step()
```

> **Important reminder:** Not all operations benefit from BF16. Operations that require high numerical precision (e.g., the final Softmax in the attention mechanism, layer normalization, loss computation) are automatically kept in FP32 by PyTorch's AMP. PyTorch's autocasting handles this routing automatically. You do not need to manually specify which layers use BF16.

---