---
tags: [neural-networks, mlp, perceptron, foundations, universal-approximation]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Perceptrons and MLPs, Perceptron, MLP, Multi-Layer Perceptron, Feed-Forward Network]
---

# Perceptrons and MLPs

> [!info] TL;DR
> A perceptron is the simplest neural unit: a weighted sum of inputs plus a bias, passed through an activation. A Multi-Layer Perceptron (MLP) stacks perceptrons into layers and layers into a network. The MLP is the universal building block — every Transformer's feed-forward layer is an MLP. This note covers the perceptron, MLP architecture, universal approximation, activation functions, the FFN in Transformers, MoE variants, worked examples, production considerations, and historical context.

## The Perceptron

A single perceptron computes:

$$
y = \sigma\left( \sum_{i=1}^{n} w_i x_i + b \right) = \sigma(\mathbf{w} \cdot \mathbf{x} + b)
$$

where:
- $\mathbf{x} \in \mathbb{R}^n$ is the input vector.
- $\mathbf{w} \in \mathbb{R}^n$ is the weight vector.
- $b \in \mathbb{R}$ is the bias.
- $\sigma$ is a (possibly nonlinear) activation function.

### Geometric Interpretation

Without the activation, $\mathbf{w} \cdot \mathbf{x} + b$ is a linear function. The set $\{\mathbf{x} : \mathbf{w} \cdot \mathbf{x} + b = 0\}$ is a **hyperplane** that divides $\mathbb{R}^n$ into two half-spaces. A perceptron with a step activation is a linear classifier — it labels points based on which side of the hyperplane they fall.

The weight vector $\mathbf{w}$ is the **normal vector** to the hyperplane — it points in the direction the perceptron is "looking for". The bias $b$ shifts the hyperplane away from the origin.

### The Decision Rule

For binary classification (with step activation $\sigma(z) = \mathbb{1}[z > 0]$):

$$
y = \begin{cases} 1 & \text{if } \mathbf{w} \cdot \mathbf{x} + b > 0 \\ 0 & \text{otherwise} \end{cases}
$$

The perceptron fires (outputs 1) when the input is on the "positive" side of the hyperplane.

### Historical Context

The perceptron was introduced by Rosenblatt in 1958. It was the first machine learning model with a learning algorithm (the perceptron learning rule) that could learn from data.

Early excitement was dampened by Minsky and Papert's 1969 book *Perceptrons*, which showed perceptrons couldn't learn XOR (a function that's not linearly separable). This led to the "AI winter" of the 1970s.

The fix — stacking perceptrons into multi-layer networks — was known but training was hard. The resurgence came with backpropagation in the 1980s (Rumelhart, Hinton, Williams, 1986), which made training multi-layer networks practical.

### The Perceptron Learning Rule

The original perceptron learning rule (Rosenblatt, 1958):

$$
\mathbf{w}_{t+1} = \mathbf{w}_t + \eta (y - \hat{y}) \mathbf{x}
$$

where:
- $\eta$ is the learning rate.
- $y$ is the true label.
- $\hat{y}$ is the predicted label.

If the prediction is correct ($y = \hat{y}$), no update. If wrong, move the weight vector toward the input (if $y = 1, \hat{y} = 0$) or away (if $y = 0, \hat{y} = 1$).

The **perceptron convergence theorem** guarantees that if the data is linearly separable, the perceptron learning rule converges in finite steps.

### Limitations

- **Linear only**: a single perceptron can only learn linearly separable functions. Cannot learn XOR.
- **No probabilistic output**: the step activation gives 0 or 1, not a probability.
- **No hidden representations**: the perceptron is a single layer; it can't learn features.

These limitations motivated multi-layer networks.

## Multi-Layer Perceptron (MLP)

An MLP stacks layers of perceptrons:

$$
\mathbf{h}_1 = \sigma(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1)
$$

$$
\mathbf{h}_2 = \sigma(\mathbf{W}_2 \mathbf{h}_1 + \mathbf{b}_2)
$$

$$
\vdots
$$

$$
\mathbf{y} = \mathbf{W}_L \mathbf{h}_{L-1} + \mathbf{b}_L
$$

Each layer applies a linear transformation (matrix multiplication — see [[04 - Matrix Multiplication]]) followed by a nonlinearity (the activation).

### Why Hidden Layers?

Without the nonlinearity, a stack of linear layers collapses to a single linear layer: $\mathbf{W}_2 \mathbf{W}_1 = \mathbf{W}$. The nonlinearity is what gives MLPs their power — it allows the network to learn nonlinear functions.

With nonlinearity, each layer can learn a transformation that the next layer composes with. Depth enables hierarchical feature composition: early layers learn simple features, later layers compose them into complex ones.

### Solving XOR

XOR is the classic example that motivated MLPs. XOR is not linearly separable — no single hyperplane can separate {(0,0), (1,1)} from {(0,1), (1,0)}.

A 2-layer MLP with 2 hidden units can solve XOR:

```
Hidden layer:
  h1 = σ(w11*x1 + w12*x2 + b1)   # detects (1,0) or (0,1)
  h2 = σ(w21*x1 + w22*x2 + b2)   # detects (1,1)
Output layer:
  y = σ(v1*h1 + v2*h2 + c)       # combines
```

With appropriate weights, this computes XOR. The hidden layer learns a nonlinear representation that makes XOR linearly separable in the hidden space.

### Universal Approximation Theorem

A feedforward network with a single hidden layer of sufficient width can approximate any continuous function on a compact domain to arbitrary accuracy (Cybenko 1989, Hornik 1991).

Formally: for any continuous function $f: [0,1]^n \to \mathbb{R}^m$ and any $\epsilon > 0$, there exists an MLP with one hidden layer of width $N$ such that:

$$
\sup_{\mathbf{x} \in [0,1]^n} \|f(\mathbf{x}) - \text{MLP}(\mathbf{x})\| < \epsilon
$$

**Important caveats**:
1. The theorem says an MLP *can* approximate any function, not that you can *train* one to do so. Finding the right weights is hard.
2. The required width $N$ may be exponentially large. A single hidden layer wide enough to approximate a complex function may be impractical.
3. In practice, deep narrow networks are easier to train than wide shallow ones, and depth provides hierarchical feature composition.

### Why Depth?

The "depth vs. width" question: for the same parameter count, is it better to have many shallow layers or fewer deep ones?

Empirically, deep networks are more parameter-efficient for complex functions. Theoretical results (Telgarani, 2016; Eldan & Shamir, 2016) show that some functions require exponential width with shallow networks but only polynomial width with deep networks.

Intuition: depth enables **hierarchical composition**. Each layer builds on the previous layer's features. For functions with hierarchical structure (which most natural functions have), this is exponentially more efficient.

### The Forward Pass in Detail

For an MLP with $L$ layers:

$$
\mathbf{h}^{(0)} = \mathbf{x}
$$
$$
\mathbf{h}^{(l)} = \sigma(\mathbf{W}^{(l)} \mathbf{h}^{(l-1)} + \mathbf{b}^{(l)}) \quad \text{for } l = 1, \ldots, L-1
$$
$$
\mathbf{y} = \mathbf{W}^{(L)} \mathbf{h}^{(L-1)} + \mathbf{b}^{(L)}
$$

The last layer typically has no activation (or a softmax for classification) because the output is a prediction, not a hidden representation.

### Parameter Count

For an MLP with layers of sizes $d_0, d_1, \ldots, d_L$:
- Layer $l$ has $d_{l-1} \times d_l$ weights + $d_l$ biases.
- Total: $\sum_{l=1}^L (d_{l-1} d_l + d_l)$.

For a Transformer FFN with $d = 4096$ and hidden $4d = 16384$:
- Layer 1: $4096 \times 16384 + 16384 \approx 67M$ parameters.
- Layer 2: $16384 \times 4096 + 4096 \approx 67M$ parameters.
- Total: ~134M parameters per FFN.

For a 32-layer model: $32 \times 134M \approx 4.3B$ parameters — more than half of an 8B model's parameters.

## Activation Functions

The choice of activation function matters. See [[02 - Activation Functions]] for the full treatment. Common choices:

| Activation | Formula | Pros | Cons |
|------------|---------|------|------|
| ReLU | $\max(0, x)$ | Simple, fast, no saturation | "Dying ReLU" (neurons can go to 0 forever) |
| GELU | $x \cdot \Phi(x)$ | Smooth, works well in Transformers | Slightly more compute |
| SwiGLU | $\text{SwiGLU}(x) = \text{SiLU}(\mathbf{W}_1 x) \odot \mathbf{W}_2 x$ | Gating improves quality | 3 matrices instead of 2 |
| Sigmoid | $\frac{1}{1 + e^{-x}}$ | Smooth, bounded | Vanishing gradient for large inputs |
| Tanh | $\tanh(x)$ | Zero-centered | Vanishing gradient |
| Leaky ReLU | $\max(0.01x, x)$ | No dying ReLU | Slightly more compute |

For Transformer FFNs, **SwiGLU** is the modern default (Llama, Mistral, Qwen). For general MLPs, GELU or ReLU are common.

## The Feed-Forward Network in Transformers

The feed-forward sublayer of a Transformer block is a 2-layer MLP with a wider hidden dimension:

$$
\text{FFN}(\mathbf{x}) = \mathbf{W}_2 \, \sigma(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1) + \mathbf{b}_2
$$

The hidden dimension is typically 4× the model dimension (e.g., 4096 → 16384). Modern LLMs use SwiGLU or GEGLU activations instead of plain ReLU/GELU.

### SwiGLU

SwiGLU (Swish-Gated Linear Unit) replaces the standard FFN with a gated version:

$$
\text{SwiGLU}(\mathbf{x}) = \text{SiLU}(\mathbf{W}_1 \mathbf{x}) \odot (\mathbf{W}_2 \mathbf{x})
$$

where $\text{SiLU}(x) = x \cdot \sigma(x)$ is the SiLU (Swish) activation.

This requires **three** matrices (gate $\mathbf{W}_1$, up $\mathbf{W}_2$, down $\mathbf{W}_3$) instead of two, but the gating improves quality. To keep parameter count constant, the hidden dimension is reduced by a factor of $\frac{2}{3}$ (so $d_{ff} = \frac{8}{3} d \approx 2.67 d$ instead of $4d$).

### Why FFN Matters

The FFN is where the Transformer does most of its "computation". Attention is routing; FFN is transformation. Empirically:

- FFN accounts for ~2/3 of the FLOPs in a Transformer forward pass.
- FFN accounts for ~2/3 of the parameters.
- FFN is where most "knowledge" is stored (per mechanistic interpretability research).

This is why MoE models replace the FFN with multiple experts — it's the highest-leverage place to add capacity.

## Worked Examples

### A 2-Layer MLP in PyTorch

```python
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, activation='gelu'):
        super().__init__()
        self.fc1 = nn.Linear(in_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, out_dim)
        if activation == 'gelu':
            self.act = nn.GELU()
        elif activation == 'relu':
            self.act = nn.ReLU()
        elif activation == 'silu':
            self.act = nn.SiLU()
        else:
            raise ValueError(f"Unknown activation: {activation}")
    
    def forward(self, x):
        return self.fc2(self.act(self.fc1(x)))

model = MLP(768, 3072, 768)  # like a transformer FFN
```

### A Transformer-Style FFN with SwiGLU

```python
class SwiGLUFFN(nn.Module):
    def __init__(self, d_model, d_ff=None):
        super().__init__()
        d_ff = d_ff or int(8 * d_model / 3)  # SwiGLU uses 2/3 factor
        self.w_gate = nn.Linear(d_model, d_ff, bias=False)
        self.w_up = nn.Linear(d_model, d_ff, bias=False)
        self.w_down = nn.Linear(d_ff, d_model, bias=False)
        self.act = nn.SiLU()
    
    def forward(self, x):
        gated = self.act(self.w_gate(x)) * self.w_up(x)
        return self.w_down(gated)
```

### Solving XOR

```python
import torch
import torch.nn as nn
import torch.optim as optim

# XOR data
X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = torch.tensor([[0.], [1.], [1.], [0.]])

# 2-layer MLP with 2 hidden units
model = nn.Sequential(
    nn.Linear(2, 2),
    nn.Tanh(),
    nn.Linear(2, 1),
    nn.Sigmoid()
)

optimizer = optim.Adam(model.parameters(), lr=0.1)
loss_fn = nn.BCELoss()

for epoch in range(1000):
    optimizer.zero_grad()
    pred = model(X)
    loss = loss_fn(pred, y)
    loss.backward()
    optimizer.step()

print(model(X))  # should be ~[[0], [1], [1], [0]]
```

## Mixture of Experts (MoE)

MoE replaces the single FFN with multiple parallel FFNs ("experts") and routes each token to a subset:

$$
\text{MoE}(\mathbf{x}) = \sum_{i \in \text{top-k}} \text{gate}(\mathbf{x})_i \cdot \text{FFN}_i(\mathbf{x})
$$

The gating function (router) decides which experts to use for each token. Only the top-k experts (typically k=2) are evaluated per token, so compute scales with k, not with the number of experts.

MoE models (Mixtral 8x7B, DeepSeek-V3) have many more parameters than dense models of the same compute, because most experts are inactive per token. This enables larger model capacity at fixed inference cost.

See [[15 - Mixture of Experts Transformer]] and [[04 - Build a Mini MoE]] for details.

## Why This Matters for AI

- The MLP is the **universal function approximator** that all deep learning rests on.
- Every Transformer block has an MLP sublayer that does the "computation" — the attention sublayer does the "routing". See [[01 - Transformer Block]].
- MLPs are also used as standalone models (tabular data, classical supervised learning), as classification heads (pooling + linear), and as the readout layer in most architectures.
- **Mixture-of-Experts** models (Mixtral, DeepSeek-V3) replace a single FFN with multiple parallel FFNs ("experts") and route each token to a subset. See [[10 - Model Architecture Research/MOC|Model Architecture Research]].
- Understanding MLPs is foundational for understanding any neural network — they're the building block of everything else.

## Production Implications

- MLPs are **compute-dense** — the FFN typically accounts for ~2/3 of the FLOPs in a Transformer forward pass. Optimizing FFN computation (kernel fusion, quantization) has high impact.
- MLP weights are the largest portion of model parameters. This is where quantization and pruning have the most impact. INT4 FFN quantization can halve model size with minimal quality loss.
- **Sparse MLPs** (MoE) let you scale parameters without scaling compute. See [[15 - Mixture of Experts Transformer]].
- **FFN width** is a key architectural choice. Wider FFN = more capacity but more compute. The 4× ratio (or 8/3× for SwiGLU) is empirically optimal for most models.
- **Initialization** matters more for MLPs than for attention. Use He initialization for ReLU, Glorot for tanh/sigmoid.
- **Dropout** in FFN (typically 0.0-0.1 in modern LLMs) helps regularization. Don't overdo it — too much dropout hurts quality.

## Common Pitfalls

- **Forgetting the activation**: without it, your "deep" network is just a linear model. Always check that the activation is applied between layers.
- **Wrong hidden dimension**: too small → underfits; too large → overfits and slow. For transformer FFNs, 4× (or 8/3× for SwiGLU) is a good default.
- **Forgetting bias**: bias terms are small but matter. Some modern architectures (e.g., Llama) omit bias entirely — be intentional about this choice.
- **Initialization matters**: random small weights are fine for shallow MLPs but cause training instability in deep ones. Use [[07 - Initialization Schemes|proper initialization]].
- **Vanishing gradients**: deep MLPs with sigmoid/tanh activations suffer from vanishing gradients. Use ReLU/GELU/SiLU and residual connections.
- **Dying ReLU**: ReLU neurons can output 0 forever if their input is always negative. Use Leaky ReLU or GELU to avoid.
- **Too many layers**: very deep MLPs (without residual connections) are hard to train. For standalone MLPs, 3-5 layers is usually enough. Deeper networks need residual connections (ResNet-style).
- **Wrong learning rate**: MLPs are sensitive to LR. Too high → divergence; too low → slow convergence. Use learning rate warmup and cosine decay.
- **Forgetting normalization**: for deep MLPs, add LayerNorm or BatchNorm between layers to stabilize training.

## Historical Context

- **1943**: McCulloch & Pitts introduce the first mathematical model of a neuron.
- **1958**: Rosenblatt introduces the perceptron with a learning rule.
- **1969**: Minsky & Papert's *Perceptrons* shows perceptrons can't learn XOR. AI winter begins.
- **1986**: Rumelhart, Hinton, Williams publish backpropagation, making multi-layer networks trainable.
- **1989**: Cybenko proves universal approximation theorem for sigmoid networks.
- **1991**: Hornik extends universal approximation to arbitrary activations.
- **2012**: AlexNet (deep CNN) wins ImageNet, kicking off the deep learning era.
- **2017**: Transformer paper shows MLP + attention is enough for sequence modeling.
- **2024+: SwiGLU** becomes the standard FFN activation for LLMs.

## Interview Questions

- **Q: Why can't a single perceptron learn XOR?**  
  A: XOR is not linearly separable — no single hyperplane can separate {(0,0), (1,1)} from {(0,1), (1,0)}. A perceptron is a linear classifier; it can only learn linearly separable functions.

- **Q: What does the universal approximation theorem say, and what are its caveats?**  
  A: A single-hidden-layer MLP can approximate any continuous function to arbitrary accuracy. Caveats: (1) it says "can", not "can train to"; (2) the required width may be exponential; (3) in practice, deep narrow networks are easier to train.

- **Q: Why does the FFN in Transformers use a wider hidden dimension (4×)?**  
  A: The wider hidden dimension gives the FFN more capacity to learn complex transformations. 4× is empirically optimal — smaller underfits, larger overfits and is wasteful.

- **Q: What is SwiGLU, and why is it used in modern LLMs?**  
  A: SwiGLU is a gated FFN: $\text{SiLU}(\mathbf{W}_1 \mathbf{x}) \odot \mathbf{W}_2 \mathbf{x}$. The gating mechanism improves quality over plain ReLU/GELU FFNs. It requires 3 matrices instead of 2, but the hidden dimension is reduced by 2/3 to keep parameter count constant.

- **Q: Why does the FFN account for most of a Transformer's parameters?**  
  A: The FFN has two (or three for SwiGLU) large matrices: $d \times 4d$ and $4d \times d$. For $d = 4096$, that's $2 \times 4096 \times 16384 = 134M$ per layer. Attention has smaller matrices ($d \times d$ for Q, K, V, O), totaling ~67M per layer. FFN is ~2× the attention parameter count.

## Further Reading

- Goodfellow et al., *Deep Learning* — Chapter 6 (Deep Feedforward Networks).
- Cybenko (1989), *Approximation by superpositions of a sigmoidal function*.
- Hornik (1991), *Approximation capabilities of multilayer feedforward networks*.
- Shazeer (2020), *GLU Variants Improve Transformer* (SwiGLU paper).
- Rumelhart, Hinton, Williams (1986), *Learning representations by back-propagating errors*.

## See Also

- [[02 - Activation Functions]] — ReLU, GELU, SwiGLU, etc.
- [[06 - Backpropagation]] — how MLPs are trained
- [[07 - Initialization Schemes]] — He, Glorot initialization
- [[04 - Matrix Multiplication]] — what a linear layer actually is
- [[01 - Transformer Block]] — where the FFN lives
- [[05 - Feed-Forward Network Deep]] — deeper treatment of Transformer FFN
- [[15 - Mixture of Experts Transformer]] — sparse FFNs
- [[04 - Neural Networks/MOC|Neural Networks MOC]]
