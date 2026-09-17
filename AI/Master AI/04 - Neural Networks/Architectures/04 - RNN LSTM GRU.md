---
tags: [neural-networks, rnn, lstm, gru, sequence]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [RNN LSTM GRU]
---

# 04 - RNN, LSTM, GRU

> [!info] TL;DR
> Recurrent Neural Networks (RNNs) process sequences by maintaining a hidden state across timesteps. Vanilla RNNs suffer from vanishing/exploding gradients. **LSTM** and **GRU** add gating mechanisms to control gradient flow. Largely replaced by Transformers for NLP, but still relevant for streaming, low-latency, and small-model use cases.

## Vanilla RNN

At each timestep, the RNN updates its hidden state:

$$
\mathbf{h}_t = \tanh(\mathbf{W}_h \mathbf{h}_{t-1} + \mathbf{W}_x \mathbf{x}_t + \mathbf{b})
$$

The same weights $\mathbf{W}_h, \mathbf{W}_x$ are used at every timestep (weight sharing across time, like CNNs across space).

The output can be:
- The hidden state itself (e.g., for sequence labeling).
- A transformation of the hidden state: $\mathbf{y}_t = \mathbf{W}_y \mathbf{h}_t$ (e.g., for next-token prediction).
- The final hidden state (e.g., for sequence classification).

### Why RNNs seemed great

- Handle variable-length sequences naturally.
- Share weights across time (parameter-efficient).
- Maintain a "memory" of past inputs.
- Can process streaming data (one token at a time).

### The problem: vanishing/exploding gradients

When you backpropagate through time (BPTT), the gradient flows through the recurrence $\mathbf{h}_t = \tanh(\mathbf{W}_h \mathbf{h}_{t-1} + \ldots)$. The gradient is multiplied by $\mathbf{W}_h$ (and the tanh derivative) at each step.

- If $\|\mathbf{W}_h\| < 1$ (in the relevant sense), the gradient decays exponentially with sequence length — **vanishing gradient**. The model can't learn long-range dependencies.
- If $\|\mathbf{W}_h\| > 1$, the gradient explodes — **exploding gradient**. Training diverges.

Practically, vanilla RNNs can't reliably learn dependencies past ~20 timesteps.

## LSTM (Long Short-Term Memory)

Hochreiter & Schmidhuber (1997) introduced LSTMs to solve the vanishing gradient problem. The key idea: **gates** that control what enters, stays in, and exits the memory.

LSTM has a **cell state** $\mathbf{c}_t$ (long-term memory) and three gates:

### Forget gate
$$
\mathbf{f}_t = \sigma(\mathbf{W}_f [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f)
$$
What fraction of the cell state to forget.

### Input gate
$$
\mathbf{i}_t = \sigma(\mathbf{W}_i [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i)
$$
$$
\tilde{\mathbf{c}}_t = \tanh(\mathbf{W}_c [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_c)
$$
What new information to write to the cell state.

### Cell state update
$$
\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t
$$
The cell state is a sum — gradients flow through it without multiplication, mitigating vanishing gradients.

### Output gate
$$
\mathbf{o}_t = \sigma(\mathbf{W}_o [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o)
$$
$$
\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t)
$$
What to output as the hidden state.

### Why LSTMs work

The cell state $\mathbf{c}_t$ provides an uninterrupted gradient highway (just additions and forget-gate multiplications). Gradients can flow across hundreds of timesteps. LSTMs were SOTA for sequence tasks from ~2014 to 2017 (when Transformers took over).

## GRU (Gated Recurrent Unit)

Cho et al. (2014) simplified the LSTM:

### Update gate (combines forget + input)
$$
\mathbf{z}_t = \sigma(\mathbf{W}_z [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_z)
$$

### Reset gate
$$
\mathbf{r}_t = \sigma(\mathbf{W}_r [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_r)
$$

### Hidden state update
$$
\tilde{\mathbf{h}}_t = \tanh(\mathbf{W} [\mathbf{r}_t \odot \mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b})
$$
$$
\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t
$$

GRU has fewer parameters than LSTM (no separate cell state, fewer gates) and often matches LSTM quality on practical tasks. Many practitioners default to GRU for simpler deployment.

## Bidirectional RNNs

Process the sequence in both directions and concatenate the hidden states:

$$
\overrightarrow{\mathbf{h}_t} = \text{RNN}(x_1, \ldots, x_t)
$$
$$
\overleftarrow{\mathbf{h}_t} = \text{RNN}(x_T, \ldots, x_t)
$$
$$
\mathbf{h}_t = [\overrightarrow{\mathbf{h}_t}; \overleftarrow{\mathbf{h}_t}]
$$

Useful for tasks where the whole sequence is available (e.g., classification, NER). Can't be used for generation (you don't know the future).

## Multi-layer RNNs (Stacked RNNs)

Stack RNN layers like Transformer blocks: the hidden states of layer $l$ become the inputs of layer $l+1$. Typically 2–4 layers. Each layer learns a higher-level representation.

## Worked Example

```python
import torch.nn as nn

class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes, num_layers=2):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers=num_layers,
                            batch_first=True, bidirectional=True, dropout=0.3)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)  # *2 for bidirectional
    
    def forward(self, x):
        e = self.embed(x)                       # (B, T, embed_dim)
        out, (h, c) = self.lstm(e)              # out: (B, T, 2*hidden_dim)
        # Concatenate final forward and backward hidden states
        h = torch.cat([h[-2], h[-1]], dim=-1)   # (B, 2*hidden_dim)
        return self.fc(h)
```

## Why RNNs Were Replaced by Transformers

| Aspect                | RNN/LSTM                  | Transformer                       |
|-----------------------|---------------------------|-----------------------------------|
| Long-range deps       | Limited (~100s of steps)  | Excellent (direct attention)      |
| Parallelism           | Sequential (slow)         | Fully parallel across positions   |
| Memory                | Constant per step         | O(n²) for attention               |
| Sample efficiency     | Reasonable                | Higher (more efficient training)  |

Transformers win on quality and training speed. RNNs win on:
- **Streaming inference**: RNNs process one token at a time with constant memory.
- **Tiny models**: for small parameter budgets, RNNs can match Transformer quality.
- **Long sequences with limited memory**: Transformers' O(n²) attention is a problem; RNNs are O(n).

This is why **state space models** (Mamba, S4) — which combine RNN-like linear scaling with Transformer-like quality — became a major research direction in 2023+. See [[24 - Research Frontiers/State Space Models/Mamba|Mamba]] (planned).

## Why This Matters for AI

- LSTMs were **SOTA for sequence modeling for years** — translation, speech, text classification. Understanding them helps you read older papers.
- The gating pattern (input/forget/output gates) appears in modified forms in modern architectures (e.g., Mamba's selective gate).
- For **streaming ASR** (Whisper), **on-device speech**, and **tiny models**, RNNs/LSTMs are still used.
- The **ReAct pattern** and many agent loops are conceptually recurrent: state at step $t$ depends on state at step $t-1$.

## Production Implications

- For most new NLP work, **use Transformers**, not RNNs.
- For **streaming / low-latency** applications (real-time ASR, on-device), GRU/LSTM may be the right choice.
- For **tiny models** (mobile, edge), RNNs can be more efficient than Transformers.
- For **very long sequences with bounded memory**, consider Mamba or other SSMs.

## Common Pitfalls

- **Forgetting to detach hidden states between sequences** — gradient flows across sequences, causing instability.
- **Wrong batch dimension** — `batch_first=True` vs `False` is a common bug.
- **Not padding / packing variable-length sequences** — use `pack_padded_sequence` for efficiency.
- **Bidirectional for generation** — can't use bidirectional RNNs for autoregressive generation.

## Further Reading

- Hochreiter & Schmidhuber (1997), *Long Short-Term Memory*.
- Cho et al. (2014), *Learning Phrase Representations using RNN Encoder-Decoder* (GRU).
- Goodfellow et al., *Deep Learning*, Chapter 10 (Sequence Modeling).

## See Also

- [[03 - CNNs]]
- [[05 - Seq2Seq and the Information Bottleneck]]
- [[06 - Backpropagation]]
- [[24 - Research Frontiers/State Space Models/Mamba|Mamba]] (planned)
- [[04 - Neural Networks/MOC|Neural Networks MOC]]

## The Vanishing Gradient Derivation for Vanilla RNNs

For a vanilla RNN, the hidden state at step $t$ is $h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$. The gradient of the loss $L$ with respect to $h_t$ involves a product of Jacobians:

$$
\frac{\partial L}{\partial h_0} = \frac{\partial L}{\partial h_T} \prod_{t=1}^{T} \frac{\partial h_t}{\partial h_{t-1}} = \frac{\partial L}{\partial h_T} \prod_{t=1}^{T} \text{diag}(\tanh'(z_t)) W_h$$

The spectral norm $\|W_h\|$ (largest singular value) determines whether this product grows or shrinks:
- If $\|W_h\| < 1$ (with the tanh' factor, which is $\leq 1$), the product decays exponentially — vanishing gradients. The model can't learn dependencies past ~20 steps.
- If $\|W_h\| > 1$, the product grows exponentially — exploding gradients. Training diverges.

The condition for stable training is $\|W_h\| \approx 1$, which is hard to maintain across all layers and training steps. This is why vanilla RNNs are rarely used for sequences longer than ~20 tokens.

### How LSTMs solve this

The LSTM cell state $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$ is an additive update, not a multiplicative one. The gradient through the cell state is:

$$
\frac{\partial c_t}{\partial c_{t-1}} = f_t$$

This is a simple element-wise multiplication by the forget gate $f_t \in [0, 1]$. The product over $T$ steps is $\prod_{t=1}^{T} f_t$. If $f_t \approx 1$ (forget gate mostly open), the gradient flows through unchanged. The model can learn to keep $f_t$ near 1 for long-range dependencies, allowing gradients to flow across hundreds of steps.

This is the key insight of LSTMs: the additive cell state creates a "gradient highway" that bypasses the vanishing gradient problem. The same idea appears in residual connections (which are additive) and in the residual stream of Transformers.

## GRU vs LSTM: When to Choose Which

| Aspect                  | LSTM                          | GRU                            |
|-------------------------|-------------------------------|--------------------------------|
| Parameters              | $4(d_h + d_x) d_h + 4 d_h$    | $3(d_h + d_x) d_h + 3 d_h$     |
| Gates                   | 3 (forget, input, output)     | 2 (update, reset)              |
| Cell state              | Separate from hidden state    | Combined with hidden state     |
| Training speed          | Slower (more params)          | Faster                         |
| Quality (most tasks)    | Slightly better               | Comparable                     |
| Long-range dependencies | Better (separate cell state)  | Slightly worse                 |
| Memory                  | More                           | Less                           |

For most modern use cases, GRU is preferred over LSTM because: (1) fewer parameters train faster; (2) quality is comparable; (3) the simpler architecture is easier to reason about. Choose LSTM if you specifically need the separate cell state (e.g., very long sequences where the cell state's gradient highway matters).

Both are largely superseded by Transformers for NLP. For streaming, on-device, or tiny models, GRU/LSTM are still relevant. For research on linear-time sequence models (Mamba, RWKV, RetNet), the gating pattern is the conceptual ancestor.

## Worked Example: LSTM Forward Pass Step by Step

```python
import torch
import torch.nn as nn

class LSTMCell(nn.Module):
    """A single LSTM cell, implemented explicitly."""
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        # All 4 gates in one linear layer for efficiency
        self.W = nn.Linear(input_dim + hidden_dim, 4 * hidden_dim, bias=True)
        self.hidden_dim = hidden_dim

    def forward(self, x, h_prev, c_prev):
        # x: (batch, input_dim), h_prev: (batch, hidden_dim), c_prev: (batch, hidden_dim)
        combined = torch.cat([x, h_prev], dim=-1)
        gates = self.W(combined)

        # Split into 4 gates
        i, f, g, o = gates.chunk(4, dim=-1)

        # Apply activations
        input_gate = torch.sigmoid(i)      # What to write
        forget_gate = torch.sigmoid(f)     # What to keep
        candidate = torch.tanh(g)          # New candidate values
        output_gate = torch.sigmoid(o)     # What to output

        # Cell state update (the additive highway)
        c_new = forget_gate * c_prev + input_gate * candidate

        # Hidden state update
        h_new = output_gate * torch.tanh(c_new)

        return h_new, c_new

# Use it
batch_size, input_dim, hidden_dim = 4, 10, 20
lstm_cell = LSTMCell(input_dim, hidden_dim)

x = torch.randn(batch_size, input_dim)
h = torch.zeros(batch_size, hidden_dim)
c = torch.zeros(batch_size, hidden_dim)

# Process 5 timesteps
for t in range(5):
    h, c = lstm_cell(x, h, c)
    print(f"Step {t}: h_mean={h.mean().item():.4f} c_mean={c.mean().item():.4f}")
```

The key things to notice: (1) the cell state `c` changes additively (forget * old + input * candidate), which is why gradients flow through it well; (2) all 4 gates are computed in a single matmul for efficiency; (3) the hidden state `h` is a gated version of tanh(c), which keeps it bounded.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Training diverges | Gradient explosion | Gradient clipping (max norm 1-5) |
| Model can't learn long dependencies | Vanishing gradients; sequence too long | Use LSTM/GRU (not vanilla RNN); add residual connections |
| Hidden states blow up | No activation bounding; or bad init | Use tanh for hidden state; proper init (Xavier for tanh) |
| Slow training | Sequential forward (no parallelism) | Use Transformers if you can; or process multiple sequences in parallel |
| Memory grows with sequence length | Storing all hidden states for BPTT | Use truncated BPTT (process in chunks of ~100 steps) |
| Bidirectional on generation | Can't use bidirectional for autoregressive | Use unidirectional for generation; bidirectional only for encoding |

## Connection to Other Concepts

- [[04 - Neural Networks/Architectures/05 - Seq2Seq and the Information Bottleneck|Seq2Seq and the Information Bottleneck]] — what RNNs were built for.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — BPTT is backprop through time.
- [[04 - Neural Networks/Training/08 - Vanishing and Exploding Gradients|Vanishing and Exploding Gradients]] — the RNN vulnerability.
- [[06 - Attention Mechanisms/Origins/01 - Origins of Attention|Origins of Attention]] — attention was invented to fix Seq2Seq's bottleneck.
- [[06 - Attention Mechanisms/Origins/02 - Bahdanau Attention|Bahdanau Attention]] — used with RNN encoders.
- [[07 - Transformers/Architecture/01 - Transformer Block|Transformer Block]] — what replaced RNNs.
- [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers|SSMs Mamba and Frontiers]] — the modern linear-time successor.
- [[24 - Research Frontiers/Hybrid Architectures/03 - RWKV and RetNet|RWKV and RetNet]] — RNN-like modern architectures.
- [[26 - Papers/Attention Origins/01 - Bahdanau Attention 2014|Bahdanau 2014]] — used LSTMs.

## Interview Questions

1. **Q: Why do vanilla RNNs suffer from vanishing gradients, and how do LSTMs fix this?**
   A: Vanilla RNNs: the gradient through $T$ steps is a product of Jacobians $\prod_{t=1}^{T} \text{diag}(\tanh'(z_t)) W_h$. The spectral norm of $W_h$ determines whether this grows (exploding) or shrinks (vanishing). Maintaining $\|W_h\| \approx 1$ across training is hard. LSTMs fix this with an additive cell state: $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$. The gradient through the cell state is just $f_t$ (the forget gate), which the model can learn to keep near 1 for long-range dependencies. This creates a "gradient highway" that bypasses the vanishing gradient problem. The same idea appears in residual connections and Transformer residual streams.

2. **Q: When would you choose GRU over LSTM, and vice versa?**
   A: Choose GRU for most modern use cases: fewer parameters (3 gates vs 4), faster training, comparable quality. Choose LSTM if: (1) you need very long-range dependencies (LSTM's separate cell state is a cleaner gradient highway); (2) you're working with legacy code that expects LSTM; (3) you've validated that LSTM outperforms GRU on your specific task (rare). Both are largely superseded by Transformers for NLP. For streaming, on-device, or tiny models, GRU/LSTM are still relevant.

3. **Q: Explain BPTT (Backpropagation Through Time) and its challenges.**
   A: BPTT unfolds the RNN through time into a deep feedforward network with shared weights, then applies standard backprop. Challenges: (1) **Memory** — storing all hidden states for $T$ steps uses $O(T \cdot d_h)$ memory per sequence. Truncated BPTT (process in chunks of ~100 steps) mitigates this. (2) **Vanishing/exploding gradients** — the product of Jacobians over $T$ steps causes the pathologies that motivated LSTMs. (3) **Sequential computation** — you can't parallelize across time steps (each depends on the previous), unlike Transformers which parallelize across positions. This is the main reason Transformers replaced RNNs for training efficiency.

4. **Q: Why can't you use a bidirectional RNN for generation?**
   A: A bidirectional RNN processes the sequence in both directions, so the hidden state at position $t$ depends on positions $t+1, t+2, \ldots$ (the future). For generation, you don't know the future — you're producing it one token at a time. A bidirectional RNN would require knowing the entire sequence before producing the first token, defeating the purpose of autoregressive generation. Use unidirectional RNNs (or causal Transformers) for generation; bidirectional only for encoding (classification, NER, machine translation encoder).

5. **Q: How do RNNs relate to modern state space models like Mamba?**
   A: Mamba is a modern "RNN-like" architecture that fixes RNNs' weaknesses. The connection: (1) Mamba has a hidden state that updates sequentially (like RNNs); (2) Mamba uses selective gating (like LSTM's gates, but input-dependent); (3) Mamba's parallel scan algorithm enables $O(n)$ training (unlike RNNs' $O(n)$ sequential). The differences: Mamba is based on state space models (continuous-time math discretized), not explicit gates; Mamba's selective scan allows input-dependent gating, which vanilla SSMs (S4) lacked. Conceptually, Mamba is what RNNs should have been — linear-time inference with Transformer-like quality.

6. **Q: Why did Transformers replace RNNs for NLP?**
   A: Three reasons. (1) **Parallelism** — Transformers process all positions simultaneously, enabling GPU parallelization. RNNs are sequential (each step depends on the previous), so they can't use GPU parallelism effectively. This makes Transformer training 10-100× faster. (2) **Long-range dependencies** — attention gives direct access to any position, so long-range dependencies are $O(1)$ to learn. RNNs need $O(T)$ steps, with vanishing gradients along the way. (3) **Quality** — Transformers empirically outperform RNNs on most NLP tasks, especially at scale. RNNs still win on: streaming inference (constant memory per step), tiny models (parameter efficiency), and very long sequences where attention's $O(n^2)$ is prohibitive.

## See Also

- [[03 - CNNs]]
- [[05 - Seq2Seq and the Information Bottleneck]]
- [[06 - Backpropagation]]
- [[24 - Research Frontiers/State Space Models/Mamba|Mamba]] (planned)
- [[04 - Neural Networks/MOC|Neural Networks MOC]]
