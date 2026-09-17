---
tags: [research, rwkv, retnet, linear-attention, efficient-llm]
iteration: 5
created: 2026-08-08
aliases: [RWKV, RetNet, Retentive Network]
---

# 03 — RWKV and RetNet

> [!info] TL;DR
> RWKV and RetNet are alternative linear-time sequence models that preceded Mamba. RWKV combines an RNN-like recurrence (inference is O(1) per token) with Transformer-like parallelism (training is O(N) parallel). RetNet (Microsoft, 2023) uses a similar recurrence with a different formulation, achieving "the best of Transformer and RNN". Both demonstrated that linear-time models could match Transformer quality, paving the way for Mamba and the 2024–2025 hybrid architecture trend.

## RWKV

### Citation
Peng, B., Alcaide, E., Anthony, Q., Albalak, A., Arcadinho, S., Cao, H., et al. (2023). *RWKV: Reinventing RNNs for the Transformer Era*. arXiv:2305.13048.

### Overview
RWKV (named after its four components: R, W, K, V) is a linear RNN that can be trained in parallel like a Transformer and inferred in O(1) memory per token like an RNN. It was developed by Bo Peng and an open-source community, predating Mamba by several months.

### The Key Idea: Linear Attention as RNN
Standard attention is:
```
y_t = Σ_j softmax(q_t · k_j) · v_j
```

RWKV replaces the softmax with a linear (exponential) weighting:
```
y_t = Σ_j w_{t,j} · k_j · v_j
```

where `w_{t,j}` is a decay factor that depends on the relative position `(t - j)`. This linearization allows the sum to be computed recurrently:

```
h_t = a_t · h_{t-1} + k_t · v_t^T    # state update (like an RNN)
y_t = R_t · h_t                       # output
```

The state `h` accumulates past K·V products, weighted by position-dependent decay. This is O(1) per token at inference (just update the state and read the output) but can be parallelized during training (all positions computed simultaneously using the attention-like formulation).

### The Four Components
- **R (Receptance)**: controls how much of the state to use (like a gate).
- **W (Weight)**: the position-dependent decay factor.
- **K (Key)**: like attention keys.
- **V (Value)**: like attention values.

The interaction: R gates the output, W decays the state, K and V update the state.

### Why RWKV Worked
- **Linear time**: O(N) training, O(1) inference per token.
- **Parallelizable**: training uses the attention-like formulation (all positions at once).
- **No quadratic attention matrix**: the recurrence avoids materializing N×N matrices.
- **Transformer-compatible**: RWKV layers can be swapped into Transformer architectures.

### RWKV Results
RWKV-4 (2023) matched comparable-size GPT-2 and small Transformers on language modeling while being faster at inference. RWKV-5, RWKV-6 (2024) improved quality further and scaled to 14B+ parameters.

### Limitations
- **Fixed decay**: the W factor is a fixed function of relative position, less flexible than attention's content-based weighting.
- **Weaker retrieval**: like all linear-time models, RWKV underperforms attention on precise retrieval.
- **Smaller community**: RWKV has a dedicated but smaller community compared to Transformer-based models.

## RetNet

### Citation
Sun, Y., Dong, L., Huang, B., Ma, S., Xia, X., Xue, J., et al. (2023). *Retentive Network: A Successor to Transformer for Large Language Models*. arXiv:2307.08621.

### Overview
RetNet (Microsoft, 2023) was proposed as a "successor to Transformer" — combining Transformer-quality training with RNN-quality inference efficiency. Like RWKV, it's a linear recurrence that can be parallelized for training.

### The Key Idea: Retention
RetNet introduces "retention" — a mechanism that retains information across positions with a decay factor:

```
Retention(Q, K, V) = (Q · D · K^T) · V
```

where D is a decay matrix: `D_{i,j} = γ^{i-j}` for `i ≥ j` (lower triangular), 0 otherwise. This is similar to RWKV's decay but formulated as a matrix operation.

The retention can be computed three ways:
1. **Parallel (training)**: like attention, compute the full matrix at once. O(N²) but parallelizable.
2. **Recurrent (inference)**: maintain a state `S_t = γ · S_{t-1} + K_t^T · V_t`, output `O_t = Q_t · S_t`. O(1) per token.
3. **Chunkwise (long sequences)**: split into chunks, use parallel within chunks and recurrent across chunks. Balances parallelism and memory.

### The Three Forms
The key insight: the same computation has parallel, recurrent, and chunkwise forms. You choose the form based on the use case:
- **Training**: parallel form (fast, uses GPU parallelism).
- **Inference (short)**: recurrent form (O(1) per token, minimal memory).
- **Inference (long)**: chunkwise form (balances parallelism and memory).

### RetNet Results
RetNet matched or exceeded same-size Transformers on language modeling while being 2–4× faster at inference. The theoretical analysis showed RetNet's recurrence is equivalent to attention with an exponential decay — a structured attention matrix.

### Limitations
- **Fixed decay**: like RWKV, the decay is position-based, not content-based. Less flexible than attention.
- **Weaker retrieval**: same limitation as all linear-time models.
- **Limited adoption**: RetNet didn't gain the traction that Mamba did, partly because Microsoft didn't open-source large RetNet models.

## Comparison: RWKV vs RetNet vs Mamba

| Aspect              | RWKV              | RetNet             | Mamba                  |
|---------------------|-------------------|--------------------|------------------------|
| Released            | 2023 (community)  | 2023 (Microsoft)   | 2023 (Stanford/Princeton) |
| Selection mechanism | Fixed decay       | Fixed decay        | Input-dependent (selective) |
| Theoretical basis   | Linear attention  | Retention (structured attention) | Selective SSM |
| Inference           | O(1) per token    | O(1) per token     | O(N) per token (parallel scan) |
| Training            | Parallel          | Parallel           | Parallel scan          |
| Open-source scale   | 14B+              | Limited            | 3B+                    |

The key difference: Mamba's **selectivity** (input-dependent parameters) gives it more flexibility than RWKV/RetNet's fixed decay. This is why Mamba outperformed RWKV/RetNet on most benchmarks and became the dominant linear-time architecture.

## Why RWKV and RetNet Matter

### They Pioneered Linear-Time LLMs
RWKV and RetNet demonstrated that linear-time models could match Transformer quality before Mamba. They established the conceptual foundation that Mamba built upon.

### They Showed the RNN/Attention Connection
Both showed that RNNs and attention are related — attention is a parallel form of an RNN with specific decay. This insight (later formalized by Mamba-2's SSD) originated with RWKV and RetNet.

### They Have Active Communities
RWKV has a dedicated open-source community that continues to develop the architecture (RWKV-6, RWKV-7). While smaller than the Transformer ecosystem, it produces competitive models for specific use cases.

### They Influenced Hybrid Architectures
The demonstration that linear-time models work motivated the hybrid architecture trend. If pure linear models are 90% as good as attention, then hybrids (linear + a little attention) can be 99% as good at half the cost.

## Limitations of the Linear-Time Approach

### Fixed Decay Is Less Expressive
RWKV and RetNet use position-based decay — the same decay for all tokens at a given relative position. This can't represent content-dependent relationships ("attend more to the noun, less to the verb"). Mamba's selectivity addressed this; RWKV-6 added some selectivity later.

### Retrieval Weakness
Like all linear-time models, RWKV and RetNet underperform attention on precise retrieval tasks. The state accumulates information but can't selectively retrieve specific facts as precisely as attention.

### Memory Decay
The exponential decay means old information is gradually forgotten. For tasks requiring exact recall of distant information, this is a limitation. Attention retains all information equally; linear models decay it.

## Impact and Legacy

RWKV and RetNet's influence:

1. **Pioneered linear-time LLMs**. They proved the concept before Mamba, establishing that linear-time models could be competitive.

2. **Influenced Mamba's design**. Mamba's selective mechanism was a direct response to RWKV/RetNet's fixed-decay limitation. The progression RWKV → RetNet → Mamba → Mamba-2 is a clear lineage.

3. **Active open-source ecosystem (RWKV)**. RWKV continues to be developed by its community, with models competitive in specific niches (especially efficient inference).

4. **Informed the hybrid architecture trend**. The demonstration that linear-time models work (with known limitations) motivated hybrids that combine linear efficiency with attention retrieval.

For AI engineers, RWKV and RetNet are mostly of historical interest — Mamba-2 and hybrid architectures have largely superseded them. But understanding the RWKV/RetNet/Mamba progression clarifies how the field arrived at current linear-time architectures and what trade-offs they make.

## Further Reading

- RWKV paper: arXiv:2305.13048
- RWKV project: github.com/BlinkDL/RWKV-LM
- RetNet paper: arXiv:2307.08621
- [[11 - Mamba 2023]] — the successor that dominated.
- [[02 - Mamba-2 and Structured Attention]] — the unification with attention.

## See Also

- [[01 - SSMs Mamba and Frontiers]]
- [[02 - Mamba-2 and Structured Attention]]
- [[11 - Mamba 2023]]
- [[13 - Linear Attention]]
- [[24 - Research Frontiers/MOC|24 Research Frontiers MOC]]
