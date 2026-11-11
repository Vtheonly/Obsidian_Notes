---
tags: [neural-networks, backpropagation, training]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Backpropagation, Backprop]
---

# Backpropagation

> [!info] TL;DR
> Backpropagation ("backprop") is the algorithm used to train neural networks. It computes the gradient of the loss with respect to every parameter by applying the chain rule backward through the network. This note gives the conceptual overview; for the full derivation, see [[04 - Neural Networks/Training/06 - Backpropagation]] (planned).

## What Backprop Computes

Given a loss $L$ that depends on parameters $\boldsymbol{\theta} = \{\mathbf{W}_1, \ldots, \mathbf{W}_L\}$ through a forward computation, backprop computes:

$$
\frac{\partial L}{\partial \mathbf{W}_i} \quad \text{for all } i
$$

These gradients are then used by an optimizer (e.g., [[Optimization Essentials|AdamW]]) to update the parameters.

## The Forward Pass

A 3-layer MLP forward pass:

$$
\mathbf{h}_1 = \sigma(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1) = \sigma(\mathbf{z}_1)
$$

$$
\mathbf{h}_2 = \sigma(\mathbf{W}_2 \mathbf{h}_1 + \mathbf{b}_2) = \sigma(\mathbf{z}_2)
$$

$$
\hat{y} = \mathbf{W}_3 \mathbf{h}_2 + \mathbf{b}_3 = \mathbf{z}_3
$$

$$
L = \ell(\hat{y}, y)
$$

Each layer stores its input (for the backward pass) and computes its output. This builds a **computation graph** — a DAG of operations.

## The Backward Pass

We compute gradients **in reverse topological order**, applying the chain rule at each step. The key quantity at each node is the **upstream gradient** — $\partial L / \partial (\text{node output})$ — which we propagate backward.

For the MLP above:

1. $\partial L / \partial \hat{y}$ — gradient of loss wrt final output.
2. $\partial L / \partial \mathbf{z}_3 = \partial L / \partial \hat{y}$ (identity since $\hat{y} = \mathbf{z}_3$).
3. $\partial L / \partial \mathbf{W}_3 = (\partial L / \partial \mathbf{z}_3) \mathbf{h}_2^T$ and $\partial L / \partial \mathbf{h}_2 = \mathbf{W}_3^T (\partial L / \partial \mathbf{z}_3)$.
4. $\partial L / \partial \mathbf{z}_2 = (\partial L / \partial \mathbf{h}_2) \odot \sigma'(\mathbf{z}_2)$ (element-wise — backprop through activation).
5. $\partial L / \partial \mathbf{W}_2 = (\partial L / \partial \mathbf{z}_2) \mathbf{h}_1^T$ and $\partial L / \partial \mathbf{h}_1 = \mathbf{W}_2^T (\partial L / \partial \mathbf{z}_2)$.
6. Continue to layer 1.

The pattern: each layer's gradient wrt its weights is computed from the upstream gradient and the layer's input. The upstream gradient for the previous layer is computed from the upstream gradient and the layer's weights (transposed).

## Why Reverse Mode?

Reverse-mode autodiff computes the gradient in **one backward pass** — independent of the number of parameters. Forward-mode would require one pass per parameter, which is intractable for models with billions of parameters.

The cost: memory. You must store all intermediate activations (the "forward state") to compute the backward pass. This is why training large models is **memory-bound**, not just compute-bound. See [[Gradient and Chain Rule]].

## Worked Example

```python
import torch

x = torch.tensor([1.0, 2.0], requires_grad=False)
W = torch.tensor([[1.0, 0.0], [0.0, 1.0]], requires_grad=True)
b = torch.tensor([0.0, 0.0], requires_grad=True)
y_true = torch.tensor([0.0, 1.0])

# Forward
z = W @ x + b
y = torch.sigmoid(z)
loss = ((y - y_true) ** 2).sum()

# Backward — PyTorch's autograd
loss.backward()

# Gradients are now populated
print(W.grad)  # dL/dW
print(b.grad)  # dL/db
```

`loss.backward()` traverses the computation graph in reverse, applying the chain rule at each node. The result is `.grad` on every tensor with `requires_grad=True`.

## Vanishing and Exploding Gradients

When you multiply many small numbers (each < 1), the product → 0. When you multiply many large numbers (> 1), the product → ∞. The chain rule is a long product of factors, so deep networks are vulnerable to both:

- **Vanishing gradients** — early layers receive tiny gradients, learn slowly. Classic with sigmoid/tanh.
- **Exploding gradients** — early layers receive huge gradients, weights diverge. Common in RNNs and Transformers.

### Mitigations

- **ReLU family activations** — gradient is 0 or 1, no saturation for positive inputs.
- **Residual connections** — give gradients a "shortcut" path. Critical for Transformer training. See [[Residual Connections]].
- **LayerNorm / RMSNorm** — keep activations normalized.
- **Proper initialization** (Xavier, He) — keep gradient magnitudes stable across layers.
- **Gradient clipping** — cap the gradient norm to prevent explosions.
- **Warmup** — gradually ramp up the learning rate to let early training stabilize.

## Backprop Through Time (BPTT)

For RNNs, the same weights are applied at each timestep. Backprop through the time dimension is called **Backpropagation Through Time (BPTT)**. It's mathematically the same as backprop through a deep network with shared weights — and shares the same vanishing/exploding gradient problems, exacerbated by the long effective depth.

LSTM and GRU were specifically designed with gates to control gradient flow and mitigate these issues. Transformers largely replaced RNNs partly because they avoid BPTT's gradient issues.

## Why This Matters for AI

- **Every neural network is trained with backprop.** Every. Single. One.
- Understanding backprop is essential for:
  - Debugging training (why is my loss NaN? why are early layers not learning?).
  - Designing custom layers (you need to define `backward()`).
  - Understanding optimizer behavior (AdamW's moments depend on the gradient statistics backprop produces).
- **Inference** doesn't use backprop — but understanding backprop is essential for understanding training-time architectural choices that affect inference (e.g., why pre-norm is preferred to post-norm).

## Common Pitfalls

- **Forgetting `zero_grad()`** — PyTorch accumulates gradients; you must zero them before each `backward()` call.
- **Calling `backward()` on a non-scalar** — by default, `backward()` requires a scalar loss. Use `gradient=...` argument for vector losses.
- **Modifying tensors in-place** — can break the computation graph. Use functional style or `torch.no_grad()` for in-place ops.
- **Detaching the wrong tensor** — `.detach()` cuts the gradient flow. Useful for stops, fatal when unintended.
- **Memory leaks from retaining the graph** — `retain_graph=True` keeps the computation graph for re-use; usually you don't need it.

## Production Implications

- **Activation memory dominates training memory**. Storing activations for backprop is the main cost. Gradient checkpointing (recompute activations during backward) trades ~30% more compute for ~50%+ memory savings — critical for long-context training.
- **Mixed precision** (fp16/bf16) halves activation memory but requires care for small gradients (use loss scaling in fp16).
- **Distributed training** shards activations across GPUs (sequence parallel, context parallel) for very large models or long contexts.
- **Inference doesn't need backprop** — you can free activations eagerly. But for spec-decoding or ranking, you may need a backward pass on a draft model.

## Further Reading

- Goodfellow et al., *Deep Learning* — Chapter 6.5.
- Rumelhart, Hinton, Williams (1986), *Learning representations by back-propagating errors* — the original paper.
- Paszke et al. (2017), *Automatic Differentiation in PyTorch*.

## See Also

- [[Gradient and Chain Rule]]
- [[Optimization Essentials]]
- [[Perceptrons and MLPs]]
- [[Activation Functions]]
- [[Residual Connections]]
- [[04 - Neural Networks/MOC|Neural Networks MOC]]
- [[04 - Neural Networks/Training/06 - Backpropagation]] (planned)

## Reverse-Mode Autodiff — The Algorithm

Backprop is **reverse-mode automatic differentiation**. Given a computation graph (DAG of operations), it computes the gradient of a scalar output with respect to all inputs in a single backward pass. The key data structure is the **computation graph** — a DAG where each node is an operation and edges represent data flow.

### Forward pass: build the graph

```python
# Conceptually, each operation records its inputs and outputs
import torch

x = torch.tensor([1.0, 2.0], requires_grad=True)
W = torch.tensor([[1.0, 0.0], [0.0, 1.0]], requires_grad=True)
b = torch.tensor([0.5, 0.5], requires_grad=True)

# Forward pass builds the graph
z = W @ x + b       # node 1: linear
h = torch.sigmoid(z)  # node 2: activation
loss = h.sum()      # node 3: loss (scalar)

# The graph now records: loss <- h <- z <- {W, x, b}
```

### Backward pass: traverse in reverse topological order

At each node, compute the local Jacobian-vector product (JVP) and propagate the upstream gradient backward.

```python
# PyTorch's autograd does this automatically
loss.backward()

# Gradients are now populated on each leaf tensor
print(x.grad)  # dL/dx
print(W.grad)  # dL/dW
print(b.grad)  # dL/db
```

### Why reverse mode (not forward mode)?

- **Forward mode**: one pass computes $\partial L / \partial x_i$ for one input $x_i$. For $n$ inputs, you need $n$ passes. For a 1B-parameter model, that's $10^9$ passes — infeasible.
- **Reverse mode**: one pass computes $\partial L / \partial x_i$ for ALL inputs, given a scalar output $L$. Cost: $O(n)$ memory (store all activations) and $O(n)$ compute (replay the graph backward). For scalar-loss ML, this is optimal.

The tradeoff: reverse mode requires storing all intermediate activations (the "forward state"). This is why training large models is **memory-bound**, not just compute-bound. Activation checkpointing trades ~30% more compute for ~50%+ memory savings by recomputing activations during backward.

## The Forward State and Memory Cost

The activations stored during forward are the main memory cost of training. For a Transformer with $L$ layers, hidden dim $d$, sequence length $n$, batch size $B$:

$$
\text{Activation memory} \approx L \cdot B \cdot n \cdot d \cdot \text{(bytes per element)} \cdot c
$$

where $c$ is a constant accounting for QKV, attention scores, FFN intermediates, etc. (typically $c \approx 10$–$20$).

For Llama 3 70B: $L = 80$, $d = 8192$, $n = 8192$, $B = 4$, bf16 (2 bytes), $c = 15$: activation memory $\approx 80 \times 4 \times 8192 \times 8192 \times 2 \times 15 \approx 6.4 \times 10^{11}$ bytes = 640 GB per micro-batch. This is why you need multiple GPUs even for inference, and why activation checkpointing is essential for training.

### Activation checkpointing tradeoffs

| Strategy                | Memory savings | Compute overhead | When to use                          |
|-------------------------|----------------|------------------|--------------------------------------|
| No checkpointing        | 0%             | 0%               | When memory is sufficient            |
| Every layer checkpoint  | ~50%           | ~30%             | Standard for large models            |
| Every 2 layers          | ~33%           | ~15%             | When you need some memory savings    |
| Selective (skip attention) | ~30%        | ~10%             | When attention is cheap relative to FFN |

## Backprop Through Specific Operations

### Matrix multiplication (the workhorse)

For $C = A B$ (with $A \in \mathbb{R}^{m \times k}$, $B \in \mathbb{R}^{k \times n}$, $C \in \mathbb{R}^{m \times n}$):

$$
\frac{\partial L}{\partial A} = \frac{\partial L}{\partial C} B^T, \quad \frac{\partial L}{\partial B} = A^T \frac{\partial L}{\partial C}
$$

This is why backprop is dominated by matrix multiplications (same as forward). cuBLAS handles both forward and backward matmuls with equal efficiency.

### Softmax + cross-entropy (the trick)

Softmax followed by cross-entropy has a beautifully simple gradient:

$$
\frac{\partial L}{\partial z} = \text{softmax}(z) - y$$

where $y$ is the one-hot label. This is much simpler than computing the softmax Jacobian (which is $O(V^2)$ for vocabulary size $V$). PyTorch's `F.cross_entropy` fuses these operations for numerical stability and efficiency.

### LayerNorm gradient

LayerNorm $y = \gamma \cdot (x - \mu) / \sigma + \beta$ has a complex gradient (involves the Jacobian of the normalization). Fused kernels (like Apex's `FusedLayerNorm`) compute this efficiently.

### Attention gradient

The attention $O = \text{softmax}(QK^T / \sqrt{d}) V$ has gradients that flow back to $Q$, $K$, $V$ through the softmax and the matmuls. FlashAttention computes these in a fused kernel, avoiding the $O(n^2)$ memory of the attention matrix.

## Distributed Backprop: Data, Tensor, Pipeline Parallel

For models too large for one GPU, backprop must be parallelized:

- **Data parallel**: each GPU has a full model copy, processes a different micro-batch, gradients are averaged via All-Reduce. Simple, but limited by model size (must fit on one GPU).
- **Tensor parallel** (Megatron-LM): split each weight matrix across GPUs. Forward and backward involve All-Gather and Reduce-Scatter. Scales to larger models but adds communication overhead.
- **Pipeline parallel**: split layers across GPUs. Forward passes through GPU 0, then GPU 1, etc.; backward reverses. Bubbles (idle time) are the main inefficiency.
- **FSDP** (Fully Sharded Data Parallel): shard parameters, gradients, and optimizer states. All-gather parameters for forward/backward, then free. The modern default for large models.

See [[11 - Training/Distributed Training/02 - Distributed Training|Distributed Training]] for the full treatment.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `RuntimeError: Trying to backward through the graph a second time` | Didn't call `optimizer.zero_grad()`; or `retain_graph=True` was set | Call `optimizer.zero_grad()` before each `backward()`; don't use `retain_graph` unless needed |
| CUDA OOM during backward | Activations too large | Use activation checkpointing; reduce batch size; use FSDP |
| NaN gradients | Numerical instability (e.g., log(0), division by 0) | Use `F.cross_entropy` (handles log(0)); add epsilon; use bf16 instead of fp16 |
| Gradient is None | Tensor doesn't have `requires_grad=True`; or `.detach()` was called | Check `requires_grad`; remove unnecessary `.detach()` |
| Slow backward pass | Non-contiguous tensors; or unfused ops | Call `.contiguous()` before custom kernels; use fused ops (FlashAttention, fused LayerNorm) |
| Memory leak | `retain_graph=True` keeping the graph alive | Don't use `retain_graph`; or call `loss.backward(retain_graph=False)` explicitly |
| In-place operation breaks graph | Modified a tensor in-place after it was used | Use functional style; or wrap in `torch.no_grad()` for in-place ops |

## Connection to Other Concepts

- [[02 - Mathematics/Calculus/10 - Gradient and Chain Rule|Gradient and Chain Rule]] — the mathematical foundation.
- [[02 - Mathematics/Calculus/11 - Jacobians and Hessians|Jacobians and Hessians]] — higher-order derivatives.
- [[02 - Mathematics/Optimization/12 - Optimization Essentials|Optimization Essentials]] — what backprop feeds into.
- [[02 - Mathematics/Optimization/13 - Adam Derivation|Adam Derivation]] — the optimizer that uses backprop's gradients.
- [[04 - Neural Networks/Foundations/01 - Perceptrons and MLPs|Perceptrons and MLPs]] — the simplest backprop target.
- [[04 - Neural Networks/Foundations/02 - Activation Functions|Activation Functions]] — gradients flow through these.
- [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]] — affects early backprop stability.
- [[04 - Neural Networks/Training/08 - Vanishing and Exploding Gradients|Vanishing/Exploding Gradients]] — backprop pathologies.
- [[04 - Neural Networks/Architectures/04 - RNN LSTM GRU|RNN LSTM GRU]] — BPTT is backprop through time.
- [[07 - Transformers/Architecture/03 - Residual Connections|Residual Connections]] — additive gradient highways.
- [[07 - Transformers/Components/04 - Normalization Layers|Normalization Layers]] — gradients through normalization.
- [[11 - Training/Distributed Training/02 - Distributed Training|Distributed Training]] — parallelizing backprop.
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — bf16/fp16 backprop.
- [[13 - Inference/Quantization/03 - Quantization|Quantization]] — backprop with quantized weights.

## Interview Questions

1. **Q: Why does backprop use reverse-mode autodiff instead of forward-mode?**
   A: Forward mode computes $\partial L / \partial x_i$ for one input per pass. For a model with $n$ parameters, you need $n$ passes — infeasible for $n = 10^9$. Reverse mode computes $\partial L / \partial x_i$ for ALL inputs in a single backward pass, given a scalar loss $L$. The cost: $O(n)$ memory (store all activations) and $O(n)$ compute (replay the graph backward). For scalar-loss ML (which is almost all ML), reverse mode is optimal. Forward mode is preferred when you have many outputs and few inputs (e.g., Jacobian computation for a vector-valued function with small input dimension).

2. **Q: Explain the memory cost of backprop and how activation checkpointing helps.**
   A: Backprop must store all intermediate activations from the forward pass (the "forward state") to compute gradients. For a Transformer, this is $O(L \cdot B \cdot n \cdot d)$ — for Llama 3 70B, ~640 GB per micro-batch. Activation checkpointing stores only a subset of activations and recomputes the rest during backward. Tradeoff: ~50% memory savings for ~30% more compute. This is essential for training large models on limited GPU memory. Selective checkpointing (skip cheap layers like attention) gives better tradeoffs.

3. **Q: What is the softmax + cross-entropy gradient trick, and why does it matter?**
   A: Naively, computing the gradient of softmax + cross-entropy involves the softmax Jacobian, which is $O(V^2)$ for vocabulary size $V$. For $V = 50K$, that's $2.5 \times 10^9$ entries per token. The trick: the gradient simplifies to $\partial L / \partial z = \text{softmax}(z) - y$, which is $O(V)$ per token. PyTorch's `F.cross_entropy` fuses these operations, computing the gradient directly without materializing the Jacobian. This is essential for LLM training where $V$ is large.

4. **Q: How does backprop work through a matrix multiplication?**
   A: For $C = AB$, the gradients are $\partial L / \partial A = (\partial L / \partial C) B^T$ and $\partial L / \partial B = A^T (\partial L / \partial C)$. Both are matrix multiplications — same as forward. This is why backprop is dominated by matmuls (cuBLAS handles both directions efficiently). The transpose is free (just a stride change). For batched matmul (used in attention), the same pattern applies with an extra batch dimension.

5. **Q: What goes wrong if you forget `optimizer.zero_grad()`?**
   A: PyTorch accumulates gradients by default — each `backward()` call adds to the existing `.grad` tensor. Without `zero_grad()`, the gradient from step $t$ is added to the gradient from step $t-1$, so the effective gradient grows linearly with the number of steps. This causes the optimizer to take huge steps and training diverges. The fix: call `optimizer.zero_grad()` (or `optimizer.zero_grad(set_to_none=True)` for efficiency) before each `backward()`. The accumulation behavior is intentional for gradient accumulation (compute gradients on multiple micro-batches before stepping), but you must zero after stepping.

6. **Q: How is backprop parallelized in distributed training?**
   A: Four strategies. (1) **Data parallel** — each GPU has a full model copy, processes a different micro-batch, gradients are averaged via All-Reduce. Simple, limited by single-GPU model size. (2) **Tensor parallel** (Megatron) — split each weight matrix across GPUs; forward/backward involve All-Gather and Reduce-Scatter. Scales to larger models. (3) **Pipeline parallel** — split layers across GPUs; forward passes through GPU 0, 1, ...; backward reverses. Bubbles (idle time) are the inefficiency. (4) **FSDP** — shard parameters, gradients, and optimizer states; all-gather parameters for forward/backward, then free. The modern default for large models. Most large-scale training combines all four (3D parallelism).

## See Also

- [[Gradient and Chain Rule]]
- [[Optimization Essentials]]
- [[Perceptrons and MLPs]]
- [[Activation Functions]]
- [[Residual Connections]]
- [[04 - Neural Networks/MOC|Neural Networks MOC]]
- [[04 - Neural Networks/Training/06 - Backpropagation]] (planned)
