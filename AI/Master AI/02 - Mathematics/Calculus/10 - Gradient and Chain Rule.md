---
tags: [mathematics, calculus, gradient, chain-rule, backpropagation]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Gradient and Chain Rule]
---

# Gradient and Chain Rule

> [!info] TL;DR
> The **gradient** is a vector of partial derivatives — the direction of steepest ascent. The **chain rule** tells us how to differentiate compositions of functions. Together, they are the mathematical foundation of **backpropagation**, the algorithm that trains every neural network.

## Partial Derivatives

For a function $f(x_1, \ldots, x_n)$, the **partial derivative** with respect to $x_i$ is the derivative holding all other variables constant:

$$
\frac{\partial f}{\partial x_i} = \lim_{h \to 0} \frac{f(\ldots, x_i + h, \ldots) - f(\ldots, x_i, \ldots)}{h}
$$

In PyTorch, partial derivatives are computed automatically via autograd — you almost never compute them by hand in code.

## The Gradient

The **gradient** of $f: \mathbb{R}^n \to \mathbb{R}$ is the vector of all partial derivatives:

$$
\nabla f = \left( \frac{\partial f}{\partial x_1}, \ldots, \frac{\partial f}{\partial x_n} \right)
$$

### Geometric meaning

The gradient points in the direction of **steepest ascent** of $f$. Its negation $-\nabla f$ points in the direction of steepest **descent**. This is why gradient descent updates parameters by $\theta \leftarrow \theta - \eta \nabla f$ — to minimize $f$.

The gradient is always **perpendicular to the level sets** of $f$ (the surfaces where $f$ is constant).

### For vector-valued functions: the Jacobian

If $f: \mathbb{R}^n \to \mathbb{R}^m$, the derivative is the **Jacobian matrix**:

$$
J_f = \begin{pmatrix} \frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_1}{\partial x_n} \\ \vdots & \ddots & \vdots \\ \frac{\partial f_m}{\partial x_1} & \cdots & \frac{\partial f_m}{\partial x_n} \end{pmatrix}
$$

Each row is the gradient of one output component.

## The Chain Rule

The chain rule tells us how to differentiate **compositions** of functions.

### Scalar case

If $y = f(g(x))$, then:

$$
\frac{dy}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}
$$

### Multivariable case

If $y = f(g_1(x), g_2(x), \ldots, g_k(x))$, then:

$$
\frac{dy}{dx} = \sum_{i=1}^{k} \frac{\partial f}{\partial g_i} \cdot \frac{dg_i}{dx}
$$

### Vector case (Jacobian composition)

If $\mathbf{z} = f(\mathbf{y})$ and $\mathbf{y} = g(\mathbf{x})$, then:

$$
J_{f \circ g}(\mathbf{x}) = J_f(g(\mathbf{x})) \cdot J_g(\mathbf{x})
$$

The Jacobian of a composition is the **matrix product** of the Jacobians. This is the foundation of backpropagation.

## Backpropagation = Chain Rule Applied to a Computation Graph

A neural network is a composition of functions:

$$
L = \ell(f_n(f_{n-1}(\cdots f_1(\mathbf{x}; \mathbf{W}_1) \cdots ; \mathbf{W}_{n-1}); \mathbf{W}_n), y)
$$

To compute $\partial L / \partial \mathbf{W}_i$ for every $i$, we apply the chain rule from the output backward to the input. This is **backpropagation**. See [[Backpropagation]].

The key insight: each layer only needs to know (a) its own local derivative and (b) the gradient of the loss with respect to its output. The upstream gradient is "passed back" through the network.

```python
# In PyTorch, this is automatic:
loss = model(inputs).loss(labels)
loss.backward()  # populates .grad on every parameter
```

## Numerical Differentiation (and why we don't use it)

You can approximate gradients numerically:

$$
\frac{\partial f}{\partial x_i} \approx \frac{f(\mathbf{x} + h \mathbf{e}_i) - f(\mathbf{x} - h \mathbf{e}_i)}{2h}
$$

For an $n$-parameter model, this requires $2n$ forward passes per gradient step. For a 1B-parameter model, that's 2 billion forward passes — completely intractable.

**Automatic differentiation** (autograd) computes exact gradients in a single backward pass, with the same asymptotic cost as the forward pass. This is what makes modern deep learning possible.

## Automatic Differentiation: Reverse Mode

PyTorch (and TensorFlow, JAX) use **reverse-mode autodiff**:

1. **Forward pass**: compute the output and build a computation graph (a DAG of operations).
2. **Backward pass**: traverse the graph in reverse, applying the chain rule at each node and accumulating gradients.

Reverse mode is efficient when the output is a scalar (like a loss) and the input has many dimensions (like model parameters): one forward + one backward = full gradient.

**Forward-mode autodiff** (less common in ML) is efficient when the input is scalar and output is high-dimensional (rare in ML).

## Worked Example

Let $f(x, y) = (x + y)^2$. Decompose as:
- $u = x + y$
- $f = u^2$

Forward pass:
- $u = x + y$
- $f = u^2$

Backward pass:
- $\frac{\partial f}{\partial u} = 2u$
- $\frac{\partial u}{\partial x} = 1$, $\frac{\partial u}{\partial y} = 1$
- $\frac{\partial f}{\partial x} = \frac{\partial f}{\partial u} \cdot \frac{\partial u}{\partial x} = 2u \cdot 1 = 2(x+y)$
- $\frac{\partial f}{\partial y} = 2(x+y)$

At $(x, y) = (1, 2)$: $\nabla f = (6, 6)$. Verify: $f(1, 2) = 9$, $f(1.01, 2) \approx 9.0601$, so $\Delta f / \Delta x \approx 6.01$. ✓

## Why This Matters for AI

- **Every training step is a gradient computation.** Without gradients, no learning.
- **Gradient quality determines training stability.** Vanishing/exploding gradients are caused by the chain rule multiplying many small/large factors. See [[04 - Neural Networks/Training|NN Training]] (planned).
- **Attention gradients** flow through softmax (which can saturate) and through large matrix multiplications (which can amplify). This is why we scale attention by $\sqrt{d_k}$ — see [[Self-Attention]].
- **Custom gradients** are sometimes needed for numerical stability (e.g., log-sum-exp, gradient clipping). PyTorch lets you define custom `backward()` for any function.

## Common Pitfalls

- **Forgetting to detach** — when you don't want gradients to flow through part of the graph (e.g., a target value in DPO), call `.detach()`. Forgetting this leads to memory leaks and unintended training.
- **In-place operations break autograd** — PyTorch's autograd relies on the forward values; in-place ops can overwrite them. Use functional style where possible.
- **`requires_grad=True` on inputs** — by default, model parameters have `requires_grad=True` and inputs don't. Flip this for gradient-based input optimization (e.g., adversarial attacks, prompt tuning).
- **Confusing `grad` with `grad_fn`** — `grad_fn` is the backward function in the graph; `grad` is the accumulated gradient value.

## Production Implications

- **Gradient clipping** is essential for transformer training — without it, loss spikes will destabilize training. Typical max norm: 1.0.
- **Mixed-precision training** computes gradients in fp16/bf16 with fp32 master weights. Gradient scalers handle underflow.
- **Gradient accumulation** lets you simulate large batch sizes on limited GPU memory by accumulating gradients over several forward passes before updating.
- **Gradient checkpointing** trades compute for memory by recomputing activations during the backward pass instead of storing them. Critical for long-context training and inference.

## Further Reading

- Goodfellow et al., *Deep Learning* — Chapter 6.5 (Backpropagation).
- Baydin et al., *Automatic Differentiation in Machine Learning: a Survey* (2018).
- PyTorch autograd docs: https://pytorch.org/docs/stable/autograd.html

## Why the Gradient Points in the Steepest Direction (Proof)

The gradient $\nabla f(\mathbf{x})$ points in the direction of steepest ascent. Proof: consider a unit vector $\mathbf{u}$ (direction). The directional derivative of $f$ in direction $\mathbf{u}$ is:

$$
D_{\mathbf{u}} f(\mathbf{x}) = \nabla f(\mathbf{x}) \cdot \mathbf{u}
$$

By Cauchy-Schwarz, $|D_{\mathbf{u}} f| \le \|\nabla f\| \cdot \|\mathbf{u}\| = \|\nabla f\|$ (since $\|\mathbf{u}\| = 1$). Equality holds when $\mathbf{u} = \nabla f / \|\nabla f\|$. So the direction maximizing $D_{\mathbf{u}} f$ is $\nabla f / \|\nabla f\|$ — the gradient direction.

This is why gradient **descent** updates $\theta \leftarrow \theta - \eta \nabla f$ — we move in $-\nabla f$, the direction of steepest **descent**.

## Reverse-Mode Autodiff in Detail

Reverse-mode autodiff (backpropagation) computes gradients in $O(\text{forward cost})$ time and $O(\text{graph size})$ memory. The algorithm:

### Forward pass
1. Execute the computation graph node by node, computing outputs.
2. Store intermediate values (activations) for the backward pass.
3. Build a DAG (directed acyclic graph) of operations.

### Backward pass
1. Start at the output (loss $L$); set $\bar{L} = \partial L / \partial L = 1$.
2. Traverse the graph in reverse topological order.
3. At each node, apply the chain rule: $\bar{x} = \sum_{y \in \text{outputs}(x)} \bar{y} \cdot \frac{\partial y}{\partial x}$.
4. Accumulate gradients in `.grad` for leaf nodes (parameters).

### Why reverse mode is efficient for ML

For a function $f: \mathbb{R}^n \to \mathbb{R}^m$:
- **Reverse mode**: $O(n)$ backward passes to compute all $n$ partial derivatives. Efficient when $n \gg m$ (many inputs, few outputs) — exactly the ML case ($n$ = billions of parameters, $m$ = 1 scalar loss).
- **Forward mode**: $O(m)$ forward passes to compute the full Jacobian. Efficient when $m \gg n$ (many outputs, few inputs) — rare in ML.

For a 1B-parameter model, reverse mode computes all 1B gradients in one backward pass. Forward mode would need 1B forward passes. This asymmetry is why reverse mode dominates ML.

### Memory cost

Reverse mode stores all intermediate activations from the forward pass — for a 70B model with 32K context, this can be 100+ GB. **Gradient checkpointing** trades memory for compute by recomputing activations during the backward pass instead of storing them. Reduces memory by ~$\sqrt{L}$ (where $L$ is the number of layers) at the cost of ~30% more compute.

## Worked Example: Backprop Through a 2-Layer Network

```python
import torch

# 2-layer network: y = W2 @ relu(W1 @ x + b1) + b2
# Loss: MSE
x = torch.randn(784)
y = torch.randn(10)
W1 = torch.randn(256, 784, requires_grad=True)
b1 = torch.randn(256, requires_grad=True)
W2 = torch.randn(10, 256, requires_grad=True)
b2 = torch.randn(10, requires_grad=True)

# Forward pass (builds computation graph)
h = torch.relu(W1 @ x + b1)       # (256,)
y_pred = W2 @ h + b2              # (10,)
loss = ((y_pred - y) ** 2).mean() # scalar

# Backward pass (reverse-mode autodiff)
loss.backward()

# Gradients now populated
print(f"dL/dW1 shape: {W1.grad.shape}")  # (256, 784)
print(f"dL/dW2 shape: {W2.grad.shape}")  # (10, 256)
print(f"dL/db1 shape: {b1.grad.shape}")  # (256,)
print(f"dL/db2 shape: {b2.grad.shape}")  # (10,)
```

What PyTorch does internally during `loss.backward()`:
1. $\bar{L} = 1$ (gradient of loss w.r.t. itself).
2. $\bar{y_{\text{pred}}} = \nabla_{y_{\text{pred}}} L = \frac{2}{10}(y_{\text{pred}} - y)$.
3. $\bar{W_2} = \bar{y_{\text{pred}}} \cdot h^T$ (outer product).
4. $\bar{b_2} = \bar{y_{\text{pred}}}$.
5. $\bar{h} = W_2^T \bar{y_{\text{pred}}}$.
6. Apply ReLU mask: $\bar{h} \leftarrow \bar{h} \odot \mathbb{1}[h > 0]$.
7. $\bar{W_1} = \bar{h} \cdot x^T$.
8. $\bar{b_1} = \bar{h}$.

Each step is a local derivative multiplied by the upstream gradient — pure chain rule.

## Common Gradient Pathologies in Deep Learning

### Vanishing gradients
In deep networks, the chain rule multiplies many Jacobians. If each Jacobian has spectral radius < 1, the product shrinks exponentially: $\|\nabla\| \sim \rho^L$ where $\rho$ is the typical spectral radius and $L$ is depth.

Causes:
- **Sigmoid/tanh saturation**: derivative ≈ 0 in saturation regime.
- **Bad initialization**: weights too small.
- **No residual connections**: each layer's contribution is multiplicative.

Fixes: ReLU family (derivative 1 in active regime), residual connections (additive skip), proper initialization (He, Xavier), normalization (LayerNorm, BatchNorm).

### Exploding gradients
If each Jacobian has spectral radius > 1, the product grows exponentially: $\|\nabla\| \sim \rho^L$.

Causes:
- Weights too large.
- Recurrent networks (long sequences multiply many Jacobians).
- No gradient clipping.

Fixes: gradient clipping (cap the norm), smaller learning rate, normalization layers.

### The attention scaling fix
Self-attention computes $\text{softmax}(QK^T / \sqrt{d_k}) V$. Without the $1/\sqrt{d_k}$ scaling, $QK^T$ has variance $\propto d_k$, pushing softmax into saturation (one entry → 1, others → 0). In saturation, softmax's gradient is ~0, causing vanishing gradients. Scaling keeps the variance at 1, keeping softmax in its non-saturated regime where gradients flow.

## Gradient Computation in Modern AI (Detailed)

### Mixed-precision gradients
FP16/BF16 gradients can underflow (small gradients → 0) or overflow (large gradients → inf). Solutions:
- **Gradient scaling** (FP16): multiply loss by a large factor before backward, divide before optimizer step. Keeps small gradients above FP16's minimum.
- **BF16**: same exponent range as FP32, so no overflow/underflow. Preferred on H100+.

### Gradient accumulation
When GPU memory limits batch size, accumulate gradients over multiple micro-batches:

```python
optimizer.zero_grad()
for i, micro_batch in enumerate(large_batch.split(micro_batch_size)):
    loss = model(micro_batch)
    (loss / accumulation_steps).backward()  # scale to maintain correct average
optimizer.step()
```

This simulates a larger batch size — important for stable training and accurate BatchNorm statistics.

### Gradient checkpointing
Trade memory for compute by recomputing activations during backward:

```python
from torch.utils.checkpoint import checkpoint

# Instead of: y = layer(x)
y = checkpoint(layer, x)  # recomputes layer(x) during backward
```

Reduces memory by ~$\sqrt{L}$ (with checkpointing every $\sqrt{L}$ layers) at the cost of ~30% more compute. Essential for long-context training (32K+ tokens).

### Gradient clipping
Two variants:
- **Norm clipping**: $\mathbf{g} \leftarrow \mathbf{g} \cdot \min(1, c / \|\mathbf{g}\|)$. Caps the total norm. Standard for Transformers (typical $c = 1.0$).
- **Value clipping**: $\mathbf{g} \leftarrow \text{clip}(\mathbf{g}, -c, c)$. Caps each element. Less common; can distort gradient direction.

Norm clipping is preferred because it preserves gradient direction while capping magnitude.

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| NaN gradients | Numerical instability (log(0), div by 0, overflow) | Add epsilon; clip gradients; use BF16 |
| Gradients all zero | ReLU dead neurons; broken autograd graph | Check `requires_grad`; use LeakyReLU |
| Loss not decreasing | Learning rate too high/low; vanishing gradients | Tune LR; check gradient norms per layer |
| Training unstable (loss spikes) | Exploding gradients; bad batch | Gradient clip; reduce LR; check data |
| Memory OOM | Storing too many activations | Gradient checkpointing; smaller batch; micro-batching |
| Backward too slow | Large graph; many small ops | Fuse ops; use torch.compile; reduce sequence length |

## Connection to Other Concepts

- [[02 - Mathematics/Calculus/11 - Jacobians and Hessians|Jacobians and Hessians]] — higher-order derivatives.
- [[02 - Mathematics/Optimization/12 - Optimization Essentials|Optimization Essentials]] — gradient descent, momentum, Adam.
- [[02 - Mathematics/Optimization/13 - Adam Derivation|Adam Derivation]] — adaptive gradient methods.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — the algorithm built on chain rule.
- [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]] — affects gradient flow.
- [[04 - Neural Networks/Training/08 - Vanishing and Exploding Gradients|Vanishing/Exploding Gradients]] — gradient pathologies.
- [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]] — gradient-aware scaling.
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — gradient scaling.
- [[11 - Training/Optimization/05 - Loss Spikes and Stability|Loss Spikes and Stability]] — gradient clipping.

## Interview Questions

1. **Q: Why does the gradient point in the direction of steepest ascent?**
   A: The directional derivative in direction $\mathbf{u}$ (unit) is $D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$. By Cauchy-Schwarz, this is maximized when $\mathbf{u} = \nabla f / \|\nabla f\|$. So the gradient direction maximizes the rate of increase of $f$. Gradient descent moves in $-\nabla f$ for steepest descent.

2. **Q: Why is reverse-mode autodiff preferred over forward-mode in ML?**
   A: Reverse mode computes all $n$ partial derivatives in one forward + one backward pass — $O(\text{forward cost})$. Forward mode needs $n$ passes for $n$ inputs. For ML (1B parameters, 1 scalar loss), reverse mode is 1B× faster. The trade-off: reverse mode needs $O(\text{graph size})$ memory to store activations; forward mode needs $O(1)$.

3. **Q: How does gradient checkpointing work, and when should you use it?**
   A: Instead of storing all forward activations for the backward pass, recompute them on-the-fly during backward. Reduces memory by ~$\sqrt{L}$ at the cost of ~30% more compute. Use when memory is the bottleneck (long-context training, large batch sizes, big models). Don't use when compute is the bottleneck and memory is plentiful.

4. **Q: Why does self-attention scale by $1/\sqrt{d_k}$?**
   A: Without scaling, $QK^T$ has variance $\propto d_k$. For large $d_k$, softmax saturates (one entry → 1, others → 0). In saturation, softmax's gradient is ~0, causing vanishing gradients. Scaling by $1/\sqrt{d_k}$ brings variance back to 1, keeping softmax in its non-saturated regime where gradients flow. This is a gradient-aware design choice.

5. **Q: What causes vanishing/exploding gradients, and how do you fix them?**
   A: The chain rule multiplies many Jacobians. If each has spectral radius < 1, the product vanishes ($\sim \rho^L$); if > 1, it explodes. Fixes: (1) ReLU family (derivative 1 in active regime), (2) residual connections (additive skip, not multiplicative), (3) proper initialization (He, Xavier — control spectral radius), (4) normalization (LayerNorm, BatchNorm), (5) gradient clipping (cap norm for exploding).

6. **Q: How does mixed-precision training handle gradient underflow?**
   A: FP16 has limited range — small gradients underflow to 0. Solution: **gradient scaling** — multiply the loss by a large factor (e.g., 1024) before backward, so small gradients are above FP16's minimum. The optimizer divides by the scale before updating weights. BF16 (H100+) avoids this entirely — same exponent range as FP32, so no underflow/overflow.

## See Also

- [[Optimization Essentials]]
- [[Probability Essentials]]
- [[Backpropagation]]
- [[02 - Mathematics/MOC|Mathematics MOC]]
- [[Self-Attention]] — example of gradient-aware design (scaling)
