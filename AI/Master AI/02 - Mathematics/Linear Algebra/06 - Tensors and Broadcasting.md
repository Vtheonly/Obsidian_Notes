---
tags: [mathematics, linear-algebra, tensors, broadcasting]
iteration: 10
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Tensors and Broadcasting]
---

# 06 - Tensors and Broadcasting

> [!info] TL;DR
> A tensor is a multi-dimensional array — a generalization of vectors (1D) and matrices (2D) to any number of dimensions. Broadcasting is the rule that lets you combine tensors of different (but compatible) shapes without writing loops. Both are essential for writing clean, fast deep learning code.

## What Is a Tensor?

A **tensor** is an $n$-dimensional array of numbers. The dimensionality is called the **rank** (or **order** or **ndim**):

| Rank | Name         | Example                                  |
|------|--------------|------------------------------------------|
| 0    | Scalar       | `5`                                      |
| 1    | Vector       | `[1, 2, 3]`                              |
| 2    | Matrix       | `[[1,2],[3,4]]`                          |
| 3    | 3D tensor    | A batch of matrices (e.g., RGB image)    |
| 4    | 4D tensor    | A batch of RGB images (B, C, H, W)       |
| 5+   | Higher       | Video batches, attention weights, etc.   |

In PyTorch / NumPy / TensorFlow, "tensor" means an n-d array, not the mathematical object from differential geometry. The two concepts are related but distinct.

## Shape Conventions in Deep Learning

Standard shape conventions:

- **Dense layer input**: `(batch, features)`.
- **Image**: `(batch, channels, height, width)` (PyTorch) or `(batch, height, width, channels)` (TensorFlow).
- **Sequence**: `(batch, seq_len, hidden_dim)`.
- **Attention weights**: `(batch, num_heads, seq_len, seq_len)`.
- **KV cache**: `(batch, num_layers, num_kv_heads, seq_len, head_dim)`.

These conventions are not arbitrary — they're chosen so that batched matrix multiplications work efficiently on GPUs. Mismatching conventions is a common source of bugs.

## Broadcasting

Broadcasting lets you combine tensors of different shapes by virtually "expanding" the smaller one. The rule:

1. Align shapes from the right.
2. Each dimension must be equal, or one of them must be 1.
3. Dimensions of size 1 are "stretched" to match the other.

### Example

```python
A = torch.randn(4, 3)     # shape (4, 3)
b = torch.randn(3)        # shape (3,)
A + b                     # shape (4, 3) — b is broadcast to (4, 3)
```

Step-by-step:
- Align: `A: (4, 3)`, `b: (—, 3)` → `b: (1, 3)`.
- Stretch `b` to `(4, 3)`.
- Add element-wise.

### More examples

```python
A = torch.randn(4, 3, 2)  # shape (4, 3, 2)
B = torch.randn(    3, 2)  # shape (3, 2)
A + B                      # shape (4, 3, 2)

A = torch.randn(4, 1, 5)  # shape (4, 1, 5)
B = torch.randn(1, 3, 5)  # shape (1, 3, 5)
A + B                      # shape (4, 3, 5) — both broadcast

A = torch.randn(4, 3)
B = torch.randn(4,)        # shape (4,)
A + B                      # ERROR — shapes (4,3) and (4,) don't broadcast
                            # Fix: B.unsqueeze(-1) → (4, 1)
```

### When broadcasting fails

If neither dimension is 1 and they're unequal, broadcasting fails. The fix is usually to `unsqueeze` or `reshape` to add a size-1 dimension in the right place.

## Broadcasting in Practice

Broadcasting is everywhere in deep learning:

```python
# Add bias to a linear layer output
logits = X @ W + b           # X: (B, in), W: (in, out), b: (out,) → logits: (B, out)

# LayerNorm: subtract mean and divide by std
mean = x.mean(dim=-1, keepdim=True)   # (B, D, 1)
x_norm = (x - mean) / std             # broadcast over last dim

# Attention scaling
scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)  # scalar broadcasting

# Softmax over the last dim
attn = torch.softmax(scores, dim=-1)
```

Without broadcasting, every operation would need explicit loops or `expand` calls — code would be 5x longer and 100x slower.

## Tensor Operations Beyond Matmul

### Element-wise
`+`, `-`, `*`, `/`, `torch.sqrt`, `torch.exp`, etc. Same shape (or broadcastable).

### Reductions
`sum`, `mean`, `max`, `min`, `norm`. Takes a `dim` argument for which axis to reduce. Use `keepdim=True` to preserve the reduced dimension as size 1 (important for broadcasting).

```python
x = torch.randn(4, 5)
x.sum()                  # scalar
x.sum(dim=0)             # shape (5,) — sum over rows
x.sum(dim=1)             # shape (4,) — sum over columns
x.sum(dim=1, keepdim=True)  # shape (4, 1) — keeps dim for broadcasting
```

### Reshaping
`reshape`, `view` (only on contiguous tensors), `transpose`, `permute`. These change the shape without changing the data.

```python
x = torch.randn(2, 3, 4)
x.reshape(2, 12)         # (2, 12)
x.reshape(-1)            # (24,) — flatten
x.transpose(1, 2)        # (2, 4, 3) — swap dims 1 and 2
x.permute(2, 0, 1)       # (4, 2, 3) — reorder dims
```

### Tensor contraction (einsum)
Generalization of matmul. Powerful for expressing complex multi-tensor operations:

```python
# Matmul: A (m,k) @ B (k,n) = C (m,n)
C = torch.einsum('mk,kn->mn', A, B)

# Attention: Q (B, h, n, d) @ K (B, h, n, d) → scores (B, h, n, n)
scores = torch.einsum('bhnd,bhmd->bhnm', Q, K)

# Bilinear: sum over two axes
result = torch.einsum('bn,bnm,bm->b', X, W, Y)
```

## Memory Layout

Tensors are stored as contiguous 1D arrays in memory. The shape and strides determine how indices map to memory positions.

For a tensor of shape `(d0, d1, d2)` with strides `(s0, s1, s2)`, the element at `(i, j, k)` is at memory position `i*s0 + j*s1 + k*s2`.

- **Row-major (C order)**: PyTorch / NumPy default. Last dim varies fastest.
- **Column-major (Fortran order)**: MATLAB, some BLAS. First dim varies fastest.

After some operations (e.g., `transpose`), tensors become non-contiguous. Operations like `view` require contiguous tensors; use `contiguous()` or `reshape` if needed.

## Why This Matters for AI

- Every deep learning model is a sequence of tensor operations. Reading and writing model code requires fluent tensor manipulation.
- Broadcasting is the difference between 1-line code and 20-line code for common operations.
- Tensor shape bugs are the most common error in deep learning. Get used to printing shapes (`x.shape`) and reasoning about them.
- **Performance**: tensor operations are heavily optimized in PyTorch / CUDA. Vectorized tensor code is 100x faster than Python loops.

## Production Implications

- **Always check shapes** when debugging. Most "model broke" issues are shape mismatches.
- **`keepdim=True`** is essential for broadcasting-friendly reductions. Forgetting it is a common bug.
- **Memory layout matters** for performance. After `transpose`, calling `.contiguous()` may be needed before `view`. Avoid unnecessary `.contiguous()` calls — they copy data.
- **Mixed precision** (fp16/bf16) — most tensor ops work in mixed precision, but some (like reductions) should stay in fp32 for stability. Use `torch.autocast`.

## Common Pitfalls

- **Wrong axis for `dim`** — `x.sum(dim=0)` vs `dim=1` do very different things. Print shapes.
- **Forgetting `keepdim=True`** — `(B, D, 1)` and `(B, D)` behave differently in broadcasting.
- **Confusing `view` and `reshape`** — `view` requires contiguous, `reshape` works always.
- **In-place operations on broadcasted tensors** — can silently produce wrong results or errors. Avoid `+=` on broadcasted results.
- **Wrong dtype** — int vs float, fp16 vs fp32. Mismatched dtypes often cause silent upcasts or errors.

## Further Reading

- PyTorch tensor docs: https://pytorch.org/docs/stable/tensors.html
- NumPy broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
- `einsum` tutorial: https://rockt.github.io/2018/04/30/einsum

## Strides and Memory Layout — Deep Dive

A tensor's **strides** specify how many bytes (or elements) to skip to advance by one position along each axis. For a tensor of shape `(d0, d1, d2)` with strides `(s0, s1, s2)` stored in row-major (C) order, the element at index `(i, j, k)` is at linear memory offset `i*s0 + j*s1 + k*s2`. Strides let PyTorch/NumPy perform many shape operations — `transpose`, `permute`, `slice`, `view` — **without copying data**: they simply adjust the strides and shape metadata while pointing at the same underlying buffer. This is why a transposed 1 GB tensor takes essentially zero time to produce.

The trade-off is that **non-contiguous** tensors have poor memory access patterns. GPUs (and CPUs) fetch memory in cache lines (typically 128 bytes on GPU, 64 bytes on CPU). If your access pattern strides across memory (e.g., reading column 0 of a row-major matrix), each cache line fetch returns mostly useless data, wasting bandwidth. This is why `transpose` followed by a `matmul` is slow unless you call `.contiguous()` first or use a kernel (like cuBLAS) that handles the transpose internally via stride arguments.

### Contiguity rules of thumb

| Operation                | Resulting contiguity                  | When to call `.contiguous()` |
|--------------------------|---------------------------------------|------------------------------|
| `view`, `reshape`        | Same as input (view requires contiguous) | Use `reshape` if unsure |
| `transpose(a, b)`        | Non-contiguous                        | Before `view`, before custom CUDA kernels |
| `permute(...)`           | Non-contiguous                        | Before `view`, before custom CUDA kernels |
| `slice` (`x[:, 1:]`)     | Non-contiguous (typically)            | Before `view`, sometimes before `.flatten()` |
| `expand` (broadcast)     | Non-contiguous (stride 0)             | Never (defeats the purpose) |
| `unsqueeze`              | Non-contiguous (stride 0 in new dim)  | Never |

A stride of 0 in a dimension means "don't actually move in memory when you advance along this axis" — this is how `expand` (and broadcasting) is implemented without copying data. The same data is conceptually repeated along that axis.

## Formal Broadcasting Specification

NumPy, PyTorch, JAX, and TensorFlow all follow the same broadcasting rules. Formally, two shapes are **broadcast-compatible** iff, after right-aligning them and padding the shorter with leading 1s, every dimension pair is either equal or one of them is 1. The output shape is the element-wise maximum:

```
shape_C[i] = max(shape_A[i], shape_B[i])  for each axis i
```

A dimension of size 1 is "stretched" (logically repeated) to the max size. The actual memory cost of the broadcast is zero — the implementation uses stride-0 tricks. This is why broadcasting a `(D,)` bias into a `(B, D)` activation is free, but broadcasting a `(B, 1, D)` tensor against a `(B, N, D)` tensor is also free (no extra memory).

### Broadcasting pitfalls in higher dimensions

The right-alignment rule bites people regularly. Consider `A: (4, 3)` and `b: (4,)`. Intuition says "add b to each row of A" — but the shapes are incompatible! The fix is `b.unsqueeze(-1)` to get `(4, 1)`, which then broadcasts to `(4, 3)`. Always right-align mentally: a `(4,)` tensor is treated as `(1, 4)` after padding, not `(4, 1)`.

```python
# Wrong — ValueError
A = torch.randn(4, 3); b = torch.randn(4)
A + b  # ❌ shapes (4,3) and (4,) not broadcastable

# Right — add trailing dim
A + b.unsqueeze(-1)  # ✅ (4,3) + (4,1) → (4,3)

# Or: A + b[:, None]  (numpy-style)
```

## einsum — Patterns Beyond Matmul

`torch.einsum` (and `np.einsum`, `jax.numpy.einsum`) is the most expressive tensor operation primitive. It performs arbitrary tensor contractions specified by an Einstein-summation string. Below are the patterns every AI engineer should recognize.

```python
import torch
B, H, N, D = 8, 12, 1024, 64
Q = torch.randn(B, H, N, D)
K = torch.randn(B, H, N, D)
V = torch.randn(B, H, N, D)

# 1. Scaled dot-product attention scores: (B, H, N, N)
scores = torch.einsum('bhnd,bhmd->bhnm', Q, K) / (D ** 0.5)

# 2. Attention output: (B, H, N, D)
attn = torch.softmax(scores, dim=-1)
out  = torch.einsum('bhnm,bhmd->bhnd', attn, V)

# 3. Combined attention (single einsum, two contractions):
#    scores @ V in one expression
out2 = torch.einsum('bhnd,bhmd,bhme->bhne', Q, K, V)  # not common — see note below

# 4. Bilinear form: tr(X^T W Y) → scalar per batch
X = torch.randn(B, N); W = torch.randn(B, N, M); Y = torch.randn(B, M)
bilinear = torch.einsum('bn,bnm,bm->b', X, W, Y)  # (B,)

# 5. Outer product (no contraction): build a rank-1 matrix
u = torch.randn(3); v = torch.randn(4)
outer = torch.einsum('i,j->ij', u, v)  # (3, 4)

# 6. Diagonal extraction
diag = torch.einsum('ii->i', torch.randn(5, 5))  # (5,)

# 7. Trace
trace = torch.einsum('ii->', torch.randn(5, 5))  # scalar

# 8. Batched matrix multiply with explicit batch dim
A = torch.randn(B, N, D); W = torch.randn(B, D, D)
C = torch.einsum('bnd,bde->bne', A, W)  # == torch.bmm(A, W)
```

### When to prefer einsum vs. `@` / `bmm` / `matmul`

| Situation | Best choice | Why |
|-----------|-------------|-----|
| Simple A @ B | `A @ B` | Readable; cuBLAS path is optimal |
| Batched matmul | `torch.bmm` or `A @ B` | Both call cuBLAS strided batched gemm |
| Multi-tensor contraction (3+ tensors) | `einsum` | Otherwise need chained matmuls + temp tensors |
| Permuting axes as part of the op | `einsum` | Avoids an explicit `transpose` + matmul |
| Performance-critical path | `matmul` / `bmm` | einsum can be slower without `opt_einsum` |

`einsum` is a productivity tool, not a performance tool. For hot paths, prefer `matmul`, `bmm`, or specialized kernels (FlashAttention).

## Tensor Cores and Mixed Precision

Modern GPUs (Volta V100 onward) have **Tensor Cores** — hardware units that perform a `D = A × B + C` operation on small matrix tiles (16×16 or 8×8 in shape) in a single cycle. They require:

- **Input dtype**: fp16 or bf16 (some support fp8 on Hopper/Blackwell).
- **Input shape alignment**: the contracting dimension must be a multiple of 8 (or 16 for fp8).
- **Output dtype**: fp16, bf16, or fp32 (accumulator).

If your matmul shapes aren't multiples of 8, the GPU falls back to slower CUDA cores or pads internally. This is why embedding dimensions in LLMs are usually multiples of 128 (e.g., 4096, 8192) — to maximize Tensor Core utilization.

### Mixed precision training pattern

```python
# Standard mixed-precision pattern
scaler = torch.cuda.amp.GradScaler()

for x, y in dataloader:
    with torch.autocast(device_type='cuda', dtype=torch.bfloat16):
        # Forward + loss run in bf16 (Tensor Cores engaged)
        logits = model(x)
        loss = loss_fn(logits, y)

    # Backward in bf16; gradients scaled to fp32 for stability
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    scaler.step(optimizer)
    scaler.update()
    optimizer.zero_grad()
```

With bf16 you don't strictly need the `GradScaler` (bf16 has the same exponent range as fp32, unlike fp16). But the pattern is still useful for clarity. Mixed precision gives 1.5–3× throughput on Ampere/Hopper and halves activation memory.

## Real-World Shape Patterns in LLMs

These shapes come up constantly when working with LLMs. Memorizing them makes debugging much faster.

| Concept | Shape | Notes |
|---------|-------|------|
| Token embeddings | `(B, N, D)` | batch, seq_len, hidden_dim |
| QKV projections | `(B, N, 3*D)` | often packed together for one matmul |
| Multi-head reshape | `(B, N, H, D_h)` where `D_h = D/H` | then transpose to `(B, H, N, D_h)` |
| Attention scores | `(B, H, N, N)` | before softmax; masked with `(1, 1, N, N)` causal mask |
| Attention weights | `(B, H, N, N)` | after softmax; sum to 1 along last dim |
| Attention output | `(B, H, N, D_h)` | then reshape back to `(B, N, D)` |
| KV cache (per layer) | `(B, H_kv, S_max, D_h)` | S_max = max sequence length, grows during generation |
| GQA reshape | `(B, H_q, N, D_h)` → `(B, H_kv, H_q/H_kv, N, D_h)` | repeat_kv broadcasts K/V across query-head groups |
| Logits | `(B, N, V)` | V = vocab size, often 32k–256k |
| Logits (for sampling) | `(B, V)` | only the last token's logits needed at generation time |

The GQA (Grouped Query Attention) reshape is a particularly common source of bugs. The trick is that `H_q` query heads share `H_kv` key/value heads, so K and V are repeated `H_q/H_kv` times before the attention matmul. HuggingFace implements this as `repeat_kv`:

```python
def repeat_kv(hidden_states: torch.Tensor, n_rep: int) -> torch.Tensor:
    """Repeat K/V across query-head groups (GQA)."""
    batch, num_kv_heads, slen, head_dim = hidden_states.shape
    if n_rep == 1:
        return hidden_states
    hidden_states = hidden_states[:, :, None, :, :].expand(batch, num_kv_heads, n_rep, slen, head_dim)
    return hidden_states.reshape(batch, num_kv_heads * n_rep, slen, head_dim)
```

Note the use of `expand` (broadcast, no copy) followed by `reshape` (which does copy because the result is non-contiguous). This is the only way to actually materialize the repeated K/V in memory for the cuBLAS matmul.

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `RuntimeError: view size is not compatible with input tensor's size and stride` | Calling `.view()` on a non-contiguous tensor | Use `.reshape()` instead, or call `.contiguous()` first |
| Silent performance collapse (10× slower matmul) | Non-contiguous tensor passed to a kernel that doesn't handle strides | Call `.contiguous()` before the kernel; check with `x.is_contiguous()` |
| Wrong broadcasting result (no error) | Right-aligned shapes when you meant left-aligned | `unsqueeze(-1)` to add trailing 1-dim; print shapes |
| NaN in mixed-precision training | fp16 overflow in attention scores (large QK^T) | Use bf16 instead of fp16; or compute scores in fp32 via `with torch.autocast(enabled=False)` |
| CUDA OOM after a reshape | Reshape created a copy that wasn't expected | Use `view` if contiguous, or check intermediate shapes with `torch.cuda.memory_allocated()` |
| Wrong gradient shape | `keepdim=False` in a reduction that gets broadcast later | Use `keepdim=True` to preserve dim for broadcasting |
| einsum silently produces wrong shape | Wrong arrow notation string | Always print output shape and compare to expectation |
| Tensor Core underutilization (low TFLOPS) | Shape not a multiple of 8 (or 16) | Pad to multiple of 8; use `torch.compile` for automatic fusion |

## Connection to Other Concepts

- [[02 - Mathematics/Linear Algebra/01 - Vectors|Vectors]] — tensors of rank 1.
- [[02 - Mathematics/Linear Algebra/04 - Matrix Multiplication|Matrix Multiplication]] — tensor contraction along one axis.
- [[02 - Mathematics/Linear Algebra/05 - Matrix Decomposition|Matrix Decomposition]] — operates on rank-2 tensors.
- [[02 - Mathematics/Calculus/10 - Gradient and Chain Rule|Gradient and Chain Rule]] — gradients are tensors with the same shape as the parameters.
- [[02 - Mathematics/Calculus/11 - Jacobians and Hessians|Jacobians and Hessians]] — higher-rank derivative tensors.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — implemented entirely as tensor operations.
- [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]] — weight tensors initialized via broadcasting.
- [[07 - Transformers/Components/04 - Normalization Layers|Normalization Layers]] — LayerNorm broadcasts mean/std over the last dim.
- [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]] — QKV are reshaped/broadcast constantly.
- [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA|GQA/MQA/MLA]] — KV cache reshape patterns.
- [[08 - LLMs/Context and KV Cache/02 - KV Cache Mechanics|KV Cache Mechanics]] — KV cache tensor shapes and growth.
- [[13 - Inference/Serving/06 - Continuous Batching Deep Dive|Continuous Batching]] — per-sequence padding and broadcasting across batch.
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — fp16/bf16 dtype handling for tensors.

## Interview Questions

1. **Q: What's the difference between `view`, `reshape`, and `contiguous`? When would you use each?**
   A: `view` requires a contiguous tensor and never copies data — it just reinterprets the strides. `reshape` will call `view` if possible, otherwise it makes a copy. `contiguous()` materializes a new contiguous copy of the data (O(n) memory and time). Use `view` when you know the tensor is contiguous (e.g., right after `linear()` or `matmul()`), `reshape` when you're not sure (it gracefully falls back to a copy), and `.contiguous()` explicitly when you need contiguous data for a downstream op (e.g., before a custom CUDA kernel, or before `view`).

2. **Q: Explain why broadcasting a `(D,)` bias against a `(B, N, D)` activation is essentially free in memory.**
   A: The bias tensor has shape `(D,)`, which is right-aligned against `(B, N, D)` as `(1, 1, D)`. The broadcasting implementation uses stride-0 tricks: it sets the strides for the B and N axes to 0, so advancing along those axes doesn't move the memory pointer. The same `D` bias values are conceptually repeated `B × N` times without any actual data duplication. Memory cost is `O(D)` (just the bias itself); compute cost is the same as if you had materialized the full `(B, N, D)` tensor because the kernel reads each bias element `B × N` times.

3. **Q: You have `Q: (B, H, N, D)` and `K: (B, H, M, D)`. Write the einsum for attention scores, then for the attention output.**
   A: Scores: `torch.einsum('bhnd,bhmd->bhnm', Q, K)` — contract over the `d` axis. Output shape `(B, H, N, M)`. After softmax over the last axis, the output is `torch.einsum('bhnm,bhmd->bhnd', attn, V)` — contract over the `m` axis. Output shape `(B, H, N, D)`. Note the reuse of `d` as the output dim — einsum allows the same letter to appear in input and output.

4. **Q: Why does mixed-precision training require dimensions to be multiples of 8?**
   A: NVIDIA Tensor Cores process small matrix tiles — typically 16×16 (fp16/bf16) or 8×16/16×8 (fp8) — in a single hardware instruction. If your contracting dimension isn't a multiple of 8, the GPU either pads internally (wasting compute) or falls back to slower CUDA cores. By designing model dimensions as multiples of 128 (e.g., d_model = 4096), you ensure every matmul in the model is fully Tensor-Core-aligned, maximizing throughput. This is why virtually all modern LLMs use dimensions like 4096, 8192, 12288 — not arbitrary sizes.

5. **Q: A user reports their model trained correctly but is 10× slower than expected. How would you diagnose a tensor-contiguity issue?**
   A: First, check whether any non-contiguous tensors are entering the matmul: instrument the forward pass with `if not x.is_contiguous(): print(f"non-contig at {name}")`. The most common culprit is `transpose(1, 2)` on QKV for multi-head attention — without `.contiguous()` afterward, the subsequent `matmul` runs on strided memory and skips the optimized cuBLAS path. Other suspects: slicing (`x[:, 1:]`), `permute`, and certain `view` calls after a transpose. Fix with `.contiguous()` calls (or by restructuring to avoid the transpose). Profile with `torch.profiler` and look for `aten::_scaled_dot_product_flash_attention` (good) vs. `aten::matmul` with non-contiguous inputs (bad).

6. **Q: Explain how GQA's `repeat_kv` function works and why it uses `expand` then `reshape` instead of `repeat`.**
   A: GQA has `H_q` query heads but only `H_kv` key/value heads (with `H_q = n_rep × H_kv`). Each KV head is shared by `n_rep` query heads. `repeat_kv` takes the KV tensor of shape `(B, H_kv, N, D)` and produces `(B, H_q, N, D)`. It first uses `unsqueeze(2)` to insert a new axis: `(B, H_kv, 1, N, D)`. Then `expand` broadcasts along that new axis to `(B, H_kv, n_rep, N, D)` — this is free (stride 0, no copy). Finally `reshape` to `(B, H_kv × n_rep, N, D) = (B, H_q, N, D)` — this DOES copy because the data is non-contiguous (the n_rep axis has stride 0). Using `torch.repeat` would also copy but be less explicit about the broadcast-then-materialize pattern. The two-step pattern is idiomatic and slightly more memory-efficient during the broadcast phase.

## See Also

- [[01 - Vectors]]
- [[04 - Matrix Multiplication]]
- [[10 - Gradient and Chain Rule]]
- [[11 - Jacobians and Hessians]]
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]]
- [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]]
- [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]]
- [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA|GQA / MQA / MLA]]
- [[08 - LLMs/Context and KV Cache/02 - KV Cache Mechanics|KV Cache Mechanics]]
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]]
- [[02 - Mathematics/MOC|Mathematics MOC]]
