---
tags: [research, mamba-2, structured-attention, ssm, linear-attention]
iteration: 5
created: 2026-08-08
aliases: [Mamba-2, Structured Attention, SSD]
---

# 02 — Mamba-2 and Structured State Space Duality

> [!info] TL;DR
> Mamba-2 (2024) unified state space models (SSMs) with attention by showing that the SSM's recurrent computation can be expressed as a **structured attention matrix** — a semiseparable matrix. This "structured state space duality" (SSD) lets SSMs leverage attention's efficient kernels and enables hybrid SSM/attention architectures. Mamba-2 also scaled the state dimension dramatically (from 16 to 256+), improving retrieval quality. The unification clarified when SSMs and attention are preferable and inspired hybrid models (Jamba, Zamba).

## Citation

Dao, T., & Gu, A. (2024). *Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality*. ICML 2024. arXiv:2405.21060.

## The Problem Being Solved

[[11 - Mamba 2023|Mamba]] (2023) demonstrated that selective state space models could match Transformer quality at linear cost. But Mamba had two limitations:

1. **Limited state dimension**: Mamba's state was small (typically 16 dimensions per channel), which limited its ability to store detailed information for retrieval. This caused Mamba to underperform attention on "needle in a haystack" tasks.

2. **No connection to attention theory**: Mamba and attention looked like completely different architectures. There was no theoretical framework for understanding when SSMs or attention were preferable, or how to combine them.

Mamba-2 addressed both:
- **Larger state dimension**: Mamba-2 scaled the state to 128–256+ dimensions, dramatically improving retrieval quality.
- **Structured State Space Duality (SSD)**: a theoretical framework showing that SSMs are equivalent to attention with a structured (semiseparable) attention matrix.

## The Key Idea: SSMs Are Structured Attention

### The SSM Recurrence
A selective state space model computes:

```
h_t = A_t · h_{t-1} + B_t · x_t    # state update
y_t = C_t · h_t                     # output
```

Unrolled over a sequence, the output at position `t` depends on all previous inputs through a chain of matrix multiplications. This can be written as:

```
y_t = Σ_{j≤t} C_t · (A_{t} · A_{t-1} · ... · A_{j+1}) · B_j · x_j
```

### The Attention Formulation
Standard attention computes:

```
y_t = Σ_j softmax(Q_t · K_j / sqrt(d)) · V_j
```

### The Connection
Mamba-2 showed that the SSM recurrence is equivalent to attention with a specific attention matrix:

```
y_t = Σ_j M_{t,j} · V_j
```

where `M` is a **semiseparable matrix** — a structured matrix where each lower-triangular block can be factored as `C_t · (A_{t} · ... · A_{j+1}) · B_j`.

This means:
- **SSMs are attention with a semiseparable attention matrix.**
- **Attention is the special case where the matrix is unstructured (any values).**

The semiseparable structure is what makes SSMs O(N) — the structure allows efficient computation that doesn't require materializing the full N×N matrix.

### Implications of the Unification

1. **SSMs can use attention kernels**: the structured attention matrix can be computed using modified attention kernels (like FlashAttention), giving SSMs the same hardware efficiency as attention.

2. **Hybrid architectures are principled**: combining SSM layers (semiseparable attention) with attention layers (unstructured attention) is now a principled choice — you're mixing two structured attention variants.

3. **Design trade-offs are clearer**: attention's unstructured matrix can represent arbitrary token-token interactions (good for retrieval), while SSM's semiseparable matrix is more constrained (good for efficiency, weaker for exact retrieval).

## The Larger State Dimension

Mamba (2023) used a state dimension of 16 per channel — small enough that the state couldn't store much information. This caused Mamba to underperform on retrieval tasks (finding specific facts from far back in the context).

Mamba-2 scaled the state dimension to 128–256+ per channel, a 8–16× increase. This dramatically improved retrieval quality:
- **Needle-in-haystack (Mamba, state=16)**: 60% accuracy at 32K context.
- **Needle-in-haystack (Mamba-2, state=128)**: 90% accuracy at 32K context.

The larger state gives the model more "memory" to store information for later retrieval, closing much of the gap with attention.

### The Hardware Efficiency Trick
Naively, a 128-dimensional state would be expensive to compute (the state matrices are 128×128, and the recurrence involves matrix multiplications). Mamba-2 uses the SSD connection to compute this efficiently using a modified FlashAttention kernel — the semiseparable structure allows the same tiling and IO-awareness as FlashAttention.

## Key Results

Mamba-2 achieved results competitive with attention-based models:

| Benchmark         | Mamba (state=16) | Mamba-2 (state=128) | Transformer |
|-------------------|------------------|---------------------|-------------|
| The Pile (PPL)    | 2.97             | 2.85                | 2.88        |
| Needle-in-haystack| 60%              | 90%                 | 98%         |
| Inference speed (32K) | 1.0×          | 0.95×               | 0.3× (slower)|

Mamba-2 closed most of the quality gap with Transformers while maintaining the inference speed advantage. The remaining gap (needle-in-haystack: 90% vs 98%) is the motivation for hybrid architectures.

## Why It Worked

### The Unification Enables Hardware Co-Design
By expressing SSMs as structured attention, Mamba-2 can use attention's optimized kernels. The same hardware (tensor cores, FlashAttention-style tiling) works for both. This makes SSMs as fast to train and serve as attention.

### Larger State Fixes the Retrieval Weakness
Mamba's small state was the main quality bottleneck. Scaling it (enabled by the efficient kernel) fixed most of the retrieval weakness. The remaining gap is small enough that hybrid architectures can close it.

### Semiseparable Structure Is the Right Abstraction
Semiseparable matrices are well-studied in numerical linear algebra, with efficient algorithms for factorization and inversion. Mamba-2 leveraged this existing theory, rather than inventing new mathematics.

## Limitations

### Still Below Attention on Hard Retrieval
Even with a larger state, Mamba-2 (90% on needle-in-haystack) trails attention (98%). For retrieval-critical applications, attention is still preferred.

### Larger State Increases Memory
A 128-dimensional state uses 8× more memory than a 16-dimensional state. For very long contexts, this can offset some of the efficiency advantage.

### Hybrid Architectures Are More Complex
While the unification makes hybrids principled, implementing a model with both SSM and attention layers requires supporting both kernel types. This adds engineering complexity.

### Theoretical Gaps Remain
The unification explains the connection between SSMs and attention, but doesn't fully predict when each is preferable. Empirical evaluation is still needed.

## Hybrid Architectures (2024–2025)

The SSD unification enabled principled hybrid architectures:

### Jamba (AI21, 2024)
- Interleaves Mamba-2 layers and attention layers (typically 7:1 ratio).
- MoE architecture (52B total, 12B active).
- Combines Mamba-2's efficiency with attention's retrieval quality.
- One of the first production hybrid models.

### Zamba (Zyphra, 2024)
- Mamba blocks with a single shared attention block (repeated).
- More parameter-efficient than full interleaving.
- Demonstrates that even minimal attention (1 in 8 layers) significantly improves retrieval.

### Falcon-Mamba (TII, 2024)
- Pure Mamba-2 (no attention layers).
- Demonstrates that for some workloads, pure SSM is sufficient.

### MiniMax-01 (2025)
- Hybrid linear attention + sparse attention.
- 456B parameters (MoE).
- Scales to 1M+ context.

The 2025 consensus: pure SSMs work for many tasks but attention remains necessary for retrieval-heavy workloads. Hybrids offer the best of both worlds.

## Impact and Legacy

Mamba-2's influence on the field:

1. **Unified SSM and attention theory**. The SSD framework gave researchers a common language for SSMs and attention, enabling principled comparisons and hybrids.

2. **Enabled efficient SSM training**. The attention-kernel-based computation made Mamba-2 as fast to train as Transformers, removing a major adoption barrier.

3. **Catalyzed hybrid architectures**. Jamba, Zamba, and other 2024–2025 hybrids build directly on the SSD framework. The era of pure-attention LLMs is ending; hybrids are the future.

4. **Clarified the SSM/attention trade-off**. The unification made it clear: SSMs trade retrieval precision for efficiency. This is a fundamental trade-off, not a limitation to be "fixed".

5. **Influenced closed-source labs**. The hybrid trend (Gemini 1.5's 1M context, Claude's 200K context) likely uses SSM/attention hybrids, though architectures are not disclosed.

For AI engineers, Mamba-2 matters when:
- Choosing between SSM, attention, or hybrid for a new model.
- Understanding why 2025 LLMs handle long context differently.
- Reasoning about the efficiency/quality trade-off in attention design.

## Further Reading

- Original paper: arXiv:2405.21060
- Mamba-2 code: github.com/state-spaces/mamba
- [[11 - Mamba 2023]] — the original Mamba paper note.
- [[01 - SSMs Mamba and Frontiers]] — concept note in this vault.

## See Also

- [[11 - Mamba 2023]]
- [[01 - SSMs Mamba and Frontiers]]
- [[13 - Linear Attention]]
- [[04 - Self-Attention]]
- [[08 - FlashAttention 2022]]
- [[30 - Kimi Linear 2025]]
- [[24 - Research Frontiers/MOC|24 Research Frontiers MOC]]
