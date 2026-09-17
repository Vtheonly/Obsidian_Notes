---
tags: [research, mamba, ssm, hybrid, reasoning, long-context]
iteration: 8
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Mamba, State Space Models, Research Frontiers Overview]
---

# 01 - Research Frontiers: SSMs, Mamba, Hybrids, Reasoning

> [!info] TL;DR
> The 2024–2026 research frontier: State Space Models (Mamba, Mamba-2) as attention alternatives; hybrid architectures (Jamba, Falcon-Mamba); test-time compute scaling (o1, R1); 1M+ token context; Titans (neural memory). The Transformer's dominance is being challenged.

## State Space Models (SSMs)

### The SSM Foundation
SSMs model sequences via a hidden state that evolves linearly:

$$
\mathbf{h}_t = \mathbf{A} \mathbf{h}_{t-1} + \mathbf{B} \mathbf{x}_t
$$
$$
\mathbf{y}_t = \mathbf{C} \mathbf{h}_t
$$

The structured SSM (S4, Gu et al. 2022) showed these could match Transformers on Long Range Arena benchmarks with $O(n)$ scaling.

### Mamba (Gu & Dao, 2023)
The breakthrough SSM. Key innovation: **selective** state spaces — the matrices $\mathbf{B}$ and $\mathbf{C}$ are input-dependent (not fixed). This lets the model "select" which inputs to remember.

- $O(n)$ compute and memory.
- Parallel scan for training (parallelizable across sequence length).
- $O(1)$ inference per token (state is fixed-size, no growing KV cache).
- Quality matches Transformers on language modeling.

### Mamba-2 (Dao & Gu, 2024)
Improved Mamba with:
- Better hardware utilization (more matmul-friendly).
- Connection to attention via "structured masked attention" framework.
- 2–8x faster than Mamba-1 on H100.

## Hybrid Architectures

### Jamba (AI21, 2024)
- Mixes Mamba layers with attention layers (e.g., 1:7 ratio).
- 52B params (12B active), MoE.
- Combines Mamba's efficiency with attention's precision.

### Falcon-Mamba (TII, 2024)
- Pure Mamba at 7B scale.
- Shows Mamba can stand alone for production LLMs.

### Zamba (Zyphra, 2024)
- Mamba + shared attention layers.
- Higher quality than pure Mamba at small scale.

## Why Hybrids?

Attention has two big advantages over SSMs:
1. **Precise recall**: attention can copy exact tokens; SSMs compress everything into a fixed-size state.
2. **In-context learning**: induction heads (see [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]]) need attention.

SSMs have two big advantages over attention:
1. **$O(n)$ scaling**: no quadratic memory/compute.
2. **Constant inference memory**: no KV cache growth.

Hybrids combine attention's recall with SSMs' efficiency. Most architectures use a few attention layers (for recall and ICL) plus many SSM layers (for efficiency).

## Test-Time Compute Scaling

### The discovery
OpenAI o1 (Sep 2024) showed that **spending more compute at inference** (longer CoT) can dramatically improve reasoning. This is a new dimension of capability.

### The scaling law
Snell et al. (2024) showed test-time compute scales: more thinking → better answers, with diminishing returns.

### The recipe
- Train with RL on verifiable rewards (math, code).
- Model learns to produce long internal CoT.
- At inference, allow the model to think for thousands of tokens.

### Open-source
DeepSeek-R1 (Jan 2025) reproduced this recipe openly. See [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]].

## Long Context (1M+ Tokens)

### The challenge
Full attention's $O(n^2)$ becomes infeasible past ~1M tokens. Even with FlashAttention-3, 10M tokens would need ~50TB of attention intermediates per layer.

### Approaches
- **YaRN / NTK scaling** (RoPE extension): extends RoPE models to 4–32x training length without retraining. See [[06 - Attention Mechanisms/Positional Information/10 - YaRN and NTK-aware Scaling|YaRN]].
- **LongRoPE**: searches for non-uniform frequency scaling; achieves 2M tokens.
- **Ring Attention**: distributes attention across multiple GPUs; each GPU handles a chunk of the sequence.
- **Sparse attention**: Longformer/BigBird patterns for extreme length.
- **SSM hybrids**: Mamba layers for long context, attention for short.

### Models with 1M+ context
- Gemini 1.5 Pro: 2M tokens.
- Claude 3.5: 200k tokens.
- GPT-4 Turbo: 128k tokens.
- Llama 3.1: 128k tokens (extendable to 1M+ with YaRN).

## Titans and Neural Memory

### Titans (Google, 2024)
A new architecture with **neural long-term memory** — a learned memory module that persists across sequences. Combines:
- Attention (short-term).
- Neural memory (long-term).
- Persistent state.

Claims to outperform Transformers and Mamba on long-context tasks.

### Conceptual significance
Titans revive the "memory-augmented network" idea from 2014–2017 (Neural Turing Machines, Differentiable Neural Computers) but with modern training techniques. A potential third way beyond attention and SSMs.

## Other Frontiers (Briefly)

- **Continuous learning**: models that learn at inference without forgetting.
- **Neuro-symbolic**: combining LLMs with symbolic reasoning (knowledge graphs, theorem provers).
- **World models**: models that learn a world simulation (Sora, Genie).
- **Hardware-aware architectures**: designs optimized for specific hardware (Blackwell, Cerebras, Groq).

## Why This Matters for AI

- The Transformer's dominance is no longer assured. SSMs and hybrids are credible alternatives.
- For practitioners, this matters when:
  - You need very long context (1M+ tokens) — Mamba hybrids may be more efficient.
  - You need streaming / online inference — SSMs' constant memory is valuable.
  - You need maximum reasoning — test-time compute scaling (o1, R1) is the new frontier.
- The 2024–2026 research is the most active period since 2017's Transformer paper.

## Production Implications

- **For most 2026 production use**, Transformers + FlashAttention + GQA are still the right choice.
- **Watch Mamba-based models** (Jamba, Falcon-Mamba) for long-context / streaming use cases.
- **Reasoning models** (o1, R1) are the right choice for hard problems — accept the latency.
- **Don't bet everything on Transformers** — keep an eye on SSM and hybrid developments.

## Further Reading

- Gu & Dao (2023), *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*.
- Dao & Gu (2024), *Transformers are SSMs* (Mamba-2).
- Lieber et al. (2024), *Jamba: A Hybrid Transformer-Mamba Language Model*.
- Snell et al. (2024), *Scaling LLM Test-Time Compute Optimally*.
- Behrouz & Hashemi (2024), *Titans: Learning to Memorize at Test Time*.

## SSM Mathematics (Detailed)

The classical state space model is a continuous-time linear system:

$$
\dot{\mathbf{h}}(t) = \mathbf{A} \mathbf{h}(t) + \mathbf{B} \mathbf{x}(t), \quad \mathbf{y}(t) = \mathbf{C} \mathbf{h}(t) + \mathbf{D} \mathbf{x}(t)
$$

Discretizing with step $\Delta$ via zero-order hold gives the discrete-time SSM:

$$
\overline{\mathbf{A}} = \exp(\Delta \mathbf{A}), \quad \overline{\mathbf{B}} = (\Delta \mathbf{A})^{-1} (\exp(\Delta \mathbf{A}) - \mathbf{I}) \cdot \Delta \mathbf{B}
$$

$$
\mathbf{h}_t = \overline{\mathbf{A}} \mathbf{h}_{t-1} + \overline{\mathbf{B}} \mathbf{x}_t, \quad \mathbf{y}_t = \mathbf{C} \mathbf{h}_t
$$

**S4 (Gu et al. 2022)** showed that structuring $\mathbf{A}$ in a specific way (HiPPO initialization) allows the SSM to capture long-range dependencies efficiently. The key trick: the recurrence can be unrolled into a convolution, allowing parallel training.

**Mamba's innovation (selective SSMs)**: make $\overline{\mathbf{B}}$ and $\mathbf{C}$ input-dependent:
$$
\mathbf{h}_t = \overline{\mathbf{A}}(\mathbf{x}_t) \mathbf{h}_{t-1} + \overline{\mathbf{B}}(\mathbf{x}_t) \mathbf{x}_t, \quad \mathbf{y}_t = \mathbf{C}(\mathbf{x}_t) \mathbf{h}_t
$$

This breaks the convolution form (can't parallelize via FFT anymore) but enables a **parallel scan** algorithm that's still $O(n \log n)$ for training. The input-dependence is what makes Mamba "selective" — the model can choose what to remember based on input.

## Mamba vs. Attention: The Fundamental Tradeoff

| Property                  | Attention               | Mamba (SSM)             |
|---------------------------|-------------------------|-------------------------|
| Compute per token         | $O(n)$ (with KV cache)  | $O(1)$ (fixed state)    |
| Training compute          | $O(n^2)$                | $O(n \log n)$ (parallel scan) |
| Memory (inference)        | $O(n)$ (grows with context) | $O(1)$ (fixed state) |
| Exact recall              | Yes (copy via attention) | Approximate (state compresses) |
| In-context learning       | Yes (induction heads)   | Limited (state compresses history) |
| Long-context efficiency   | Expensive past 100K     | Constant cost regardless of length |
| Quality on long-context   | Strong                  | Good but loses exact recall |

The key insight: **attention and SSMs are complementary**. Attention gives exact recall and ICL but is expensive. SSMs are cheap and scale linearly but compress history into a fixed state. **Hybrid architectures** (Jamba, Zamba) combine both: a few attention layers for recall + ICL, many SSM layers for efficiency.

## Mamba-2: Structured Masked Attention (Detailed)

Mamba-2 (Dao & Gu 2024) reframed SSMs as a special case of "structured masked attention" — making the connection to attention explicit. Key insights:
- The SSM's state $\mathbf{h}_t$ can be written as $\mathbf{h}_t = \sum_{i \leq t} \overline{\mathbf{A}}^{t-i} \overline{\mathbf{B}} \mathbf{x}_i$.
- This is equivalent to attention with a structured mask ($\overline{\mathbf{A}}^{t-i}$ plays the role of the attention weight).
- This enables hardware-efficient implementations that reuse FlashAttention-style tiling.

Result: Mamba-2 is 2-8× faster than Mamba-1 on H100, with no quality loss. The connection to attention also enables hybrid attention-SSM layers (some heads attend, some are SSM) with unified infrastructure.

## Why Hybrids Won (the 2024-2026 Consensus)

Pure attention has scaling issues past ~1M tokens (KV cache size, $O(n^2)$ training cost). Pure SSMs lose exact recall and ICL. The empirical finding: **hybrids (1:7 attention:SSM ratio) get the best of both**.

- Jamba (AI21, 2024): 1:7 attention:Mamba ratio, 52B total / 12B active, MoE. Matches Llama 2 70B quality at 5× lower inference memory.
- Zamba (Zyphra, 2024): Mamba layers + shared attention layers. Higher quality than pure Mamba at small scale.
- Falcon-Mamba (TII, 2024): pure Mamba at 7B scale. Shows Mamba can stand alone but hybrids are usually better.

The pattern: at small scale (7B), pure Mamba can compete. At large scale (50B+), hybrids dominate because attention's recall matters more.

## Test-Time Compute Scaling (Detailed)

OpenAI o1 (Sep 2024) and DeepSeek-R1 (Jan 2025) demonstrated a new scaling law:

$$\text{Accuracy} \propto \log(\text{test-time tokens})$$

For hard problems (math olympiad, competitive programming), going from 1K to 100K thinking tokens can take accuracy from 30% to 80%. For easy problems, the curve saturates quickly.

**Why this matters**: pre-2024, capability came from (1) more parameters, (2) more training data, (3) more training compute. Test-time compute is a fourth dimension. A smaller model with more thinking can beat a larger model with less thinking, on hard problems.

**Production implication**: most reasoning-model deployments use **adaptive thinking budgets** — short budget for easy queries, long budget for hard ones. This requires a difficulty classifier or user-specified difficulty. The router-based hybrid pattern (cheap model for easy, reasoning model for hard) is the standard 2026 production pattern.

## Long-Context Approaches (Detailed Comparison)

| Approach                | Mechanism                                  | Max Context Tested | Quality at 1M | Implementation Cost |
|-------------------------|--------------------------------------------|--------------------|---------------|--------------------|
| Full attention          | Standard softmax attention                 | ~256K (with FlashAttn3) | Strong | Trivial (use vLLM) |
| YaRN / NTK scaling      | Interpolate RoPE frequencies              | 4-32× training length | Good | Low (modify RoPE) |
| LongRoPE                | Search for non-uniform RoPE scaling       | 2M                 | Good          | Medium (search)    |
| Ring Attention          | Distribute attention across GPUs           | 10M+ (with enough GPUs) | Strong | High (multi-node) |
| Sparse attention        | Longformer/BigBird patterns                | 1M+                | Decays with length | Medium |
| SSM hybrids             | Mamba layers for long context              | 1M+                | Good (no exact recall) | Medium |
| Titans (neural memory)  | Persistent learned memory                  | Effectively unlimited | TBD (research) | Very high (research) |

For 2026 production:
- Up to 128K: standard attention + FlashAttention-3 (Llama 3.1, Qwen 2.5).
- 128K-1M: YaRN-extended RoPE (Llama 3.1 extended, Qwen 2.5).
- 1M+: Gemini 2.5 (proprietary), Ring Attention (research), or accept SSM hybrid limitations.

## Titans: Neural Memory (Detailed)

Titans (Behrouz & Hashemi, Google, 2024) introduce a **neural long-term memory** module — a small neural network that learns to memorize and retrieve information across sequences. Architecture:

1. **Short-term component**: attention over recent context (standard Transformer).
2. **Long-term memory**: a learned memory module that persists across sequences. The memory is updated via gradient descent on a surprise metric — surprising inputs are memorized, expected inputs are forgotten.
3. **Persistent state**: the memory module's weights are the persistent state, surviving across sequences.

Conceptual significance: Titans revive the "memory-augmented network" idea (Neural Turing Machines, Differentiable Neural Computers) but with modern training. The surprise-based memory update is biologically inspired (the brain consolidates surprising events into long-term memory).

Results (paper claims): Titans outperform Transformers and Mamba on long-context tasks (1M+ tokens). Independent replication is ongoing as of 2026.

## Connection to Other Concepts

- [[06 - Attention Mechanisms/Efficient Attention/13 - Linear Attention|Linear Attention]] — conceptual ancestor of SSMs.
- [[24 - Research Frontiers/State Space Models/02 - Mamba-2 and Structured Attention|Mamba-2]] — detailed treatment.
- [[24 - Research Frontiers/Hybrid Architectures/03 - RWKV and RetNet|RWKV/RetNet]] — alternative hybrids.
- [[24 - Research Frontiers/Hybrid Architectures/04 - Hyena and Long Convolutions|Hyena]] — long-convolution alternative.
- [[24 - Research Frontiers/State Space Models/05 - DeltaNet and Titans|DeltaNet/Titans]] — Titans details.
- [[24 - Research Frontiers/Long-Context/07 - Long-Context Architectures|Long-Context Architectures]] — context extension techniques.
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Test-Time Compute]] — reasoning-model scaling.
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]] — production reasoning models.
- [[06 - Attention Mechanisms/Positional Information/10 - YaRN and NTK-aware Scaling|YaRN]] — RoPE extension.

## Interview Questions

1. **Q: What is the fundamental tradeoff between attention and SSMs?**
   A: Attention gives exact recall (can copy any previous token) and supports in-context learning (via induction heads), but is $O(n^2)$ for training and $O(n)$ for inference (KV cache grows). SSMs compress history into a fixed-size state, giving $O(n \log n)$ training and $O(1)$ inference, but lose exact recall and have weaker ICL. Hybrids combine both: a few attention layers for recall + ICL, many SSM layers for efficiency.

2. **Q: What makes Mamba "selective"?**
   A: In standard SSMs, the matrices $\mathbf{B}$ and $\mathbf{C}$ are fixed (input-independent). In Mamba, they are input-dependent — $\overline{\mathbf{B}}(\mathbf{x}_t)$ and $\mathbf{C}(\mathbf{x}_t)$. This lets the model "select" which inputs to remember based on the input itself. The selection mechanism is what enables Mamba to match Transformer quality on language modeling despite the fixed state size.

3. **Q: Why do hybrid architectures (Jamba, Zamba) outperform pure Mamba at scale?**
   A: At large scale, attention's exact recall and ICL matter more than at small scale. Pure Mamba compresses history into a fixed state, losing exact details. Hybrids add a few attention layers (1:7 ratio is common) for recall and ICL, while using many Mamba layers for efficiency. This gives most of Mamba's efficiency benefit with most of attention's capability benefit.

4. **Q: What is test-time compute scaling, and why is it a "new dimension" of capability?**
   A: Test-time compute = letting the model "think" longer at inference (longer CoT). Snell et al. (2024) showed accuracy scales as $\log(\text{tokens})$ — more thinking gives better answers, with diminishing returns. Pre-2024, capability came from parameters, data, and training compute. Test-time compute is a fourth dimension, and a smaller model with more thinking can beat a larger model with less thinking on hard problems.

5. **Q: How does YaRN extend RoPE to longer contexts?**
   A: YaRN (Yet another RoPE extensioN) interpolates the RoPE frequencies non-uniformly — higher frequencies are interpolated more aggressively, lower frequencies less. This extends RoPE models to 4-32× their training length without retraining. The non-uniform interpolation is critical: uniform interpolation (NTK-aware) loses high-frequency information, while YaRN preserves it. Used by Llama 3.1 to extend from 8K to 128K.

6. **Q: What are Titans, and how do they differ from attention and SSMs?**
   A: Titans (Behrouz & Hashemi 2024) introduce a neural long-term memory module that persists across sequences, updated via gradient descent on a "surprise" metric. Unlike attention (which has no persistent state) or SSMs (which have a fixed state), Titans learn what to memorize and what to forget. Conceptually a third way beyond attention and SSMs, reviving memory-augmented networks with modern training. Paper claims outperform Transformers and Mamba on 1M+ context; independent replication ongoing.

## See Also

- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]]
- [[06 - Attention Mechanisms/Efficient Attention/13 - Linear Attention|Linear Attention]] — conceptual ancestor of SSMs
- [[24 - Research Frontiers/MOC|Research Frontiers MOC]]
- [[00 - Vault Management/Research Queue|Research Queue]]