---
tags: [attention, origins, seq2seq, rnn]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Origins of Attention]
---

# Origins of Attention

> [!info] TL;DR
> Attention was invented (Bahdanau et al., 2014) to solve a specific problem: RNN-based Seq2Seq models compressed the entire source sentence into a single fixed-length vector, creating an information bottleneck. Attention let the decoder "look back" at the source at every step. This single idea reshaped NLP and eventually became the Transformer.

## The Problem: Seq2Seq Bottleneck

Before attention, neural machine translation used an **encoder-decoder RNN**:

1. An **encoder RNN** (LSTM/GRU) reads the source sentence word by word, updating its hidden state.
2. The **final hidden state** $\mathbf{c}$ is the "thought vector" — a fixed-length summary of the entire source.
3. A **decoder RNN** initializes from $\mathbf{c}$ and generates the target sentence word by word.

$$
\mathbf{h}_t^{enc} = \text{RNN}(\mathbf{h}_{t-1}^{enc}, x_t)
$$

$$
\mathbf{c} = \mathbf{h}_T^{enc}
$$

$$
\mathbf{h}_t^{dec} = \text{RNN}(\mathbf{h}_{t-1}^{dec}, y_{t-1}, \mathbf{c})
$$

### Why this is bad

The bottleneck: **all information about a 50-word source sentence must pass through a single vector** $\mathbf{c}$ of, say, 1024 dimensions. This:

- Limits sentence length — early models degraded sharply past 30 words.
- Forces the encoder to compress at the start of the sentence and remember until the end. RNNs with long dependencies suffer vanishing gradients (see [[04 - Neural Networks/MOC|Neural Networks]]).
- Wastes the per-token hidden states — the decoder only sees the final one.

## The Solution: Attention

Bahdanau, Cho, Bengio (2014) proposed letting the decoder **dynamically look back at all encoder hidden states** at every generation step. Instead of one $\mathbf{c}$, the decoder computes a **weighted average** of encoder states, where the weights depend on the current decoder state.

$$
\mathbf{c}_t = \sum_{i=1}^{T} \alpha_{ti} \mathbf{h}_i^{enc}
$$

$$
\alpha_{ti} = \frac{\exp(e_{ti})}{\sum_j \exp(e_{tj})}
$$

$$
e_{ti} = a(\mathbf{h}_{t-1}^{dec}, \mathbf{h}_i^{enc})
$$

where $a(\cdot, \cdot)$ is a learned alignment function (a small MLP in Bahdanau's original).

### What this gives you

- **Variable-length compression**: the summary $\mathbf{c}_t$ is now different at each step, focused on the relevant source words.
- **Long sentences**: no information bottleneck, so quality doesn't degrade with length.
- **Interpretability**: the attention weights $\alpha_{ti}$ can be visualized as an alignment matrix between source and target. For translation, this often recovers word-alignments that match linguistic intuition.

## Why This Was a Big Deal

Before attention, NMT was losing to phrase-based statistical MT (Moses) on long sentences. After attention, NMT pulled ahead — and within two years, every major MT system was neural. The attention paper has been cited 100,000+ times.

But attention's bigger impact was conceptual: it showed that **the way to handle variable-length sequences is dynamic routing**, not fixed compression. This insight, plus the realization that attention doesn't actually need the RNN, became the Transformer (Vaswani et al., 2017).

## From RNN+Attention to Transformer

The Transformer paper's key insight: **the RNN is unnecessary**. Attention alone, with positional information, can do everything the RNN+attention combo could do — and it's parallelizable.

The Transformer:
1. Removed the RNN entirely.
2. Made the attention the core operation (self-attention instead of encoder-decoder attention).
3. Added positional encoding to compensate for losing the RNN's implicit order processing.

See [[Self-Attention]] for the derivation.

## Variants of Pre-Transformer Attention

The original Bahdanau attention used a small MLP as the alignment function $a(\cdot, \cdot)$ — "additive" attention. Luong et al. (2015) proposed simpler "multiplicative" variants — dot product, general, etc. See [[Bahdanau Attention]] and [[Luong Attention]] for the details.

Other variants explored in this era:

- **Global vs local attention** (Luong et al., 2015) — attend to all source positions (global) or just a window (local).
- **Hard vs soft attention** (Xu et al., 2015) — soft attention is differentiable (weighted average); hard attention picks one position (requires REINFORCE).
- **Monotonic attention** (Raffel et al., 2017) — enforce that attention moves forward, useful for tasks with monotonic alignment (e.g., ASR).

## Why This Matters for AI

- Attention is the **foundation of every modern LLM**. If you don't understand the Seq2Seq bottleneck, you don't understand why attention exists.
- The progression RNN → RNN+attention → Transformer is the canonical example of how architectural ideas evolve. Studying it teaches you how to think about model design.
- Many **modern architectures revisit these ideas**: linear attention, sparse attention, and hybrid SSM-attention models are all exploring different points in the "how to handle variable-length sequences" design space.
- **Cross-attention** (the original Bahdanau idea) is still everywhere: T5, BART, FLAN, diffusion models (cross-attention to text), multimodal models (cross-attention between modalities).

## Production Implications

- For most modern applications, you don't implement attention yourself — you use a Transformer library. But understanding the mechanics is essential for:
  - Choosing between models (GQA vs MHA matters for inference latency).
  - Debugging (why is my model ignoring the end of long context?).
  - Understanding inference cost (KV cache is attention's memory).
- **Long-context failures** often look like the original Seq2Seq bottleneck: the model "forgets" the middle of the context. This is the modern version of the problem attention was invented to solve, and modern long-context architectures (Ring Attention, Infini-Attention) are modern solutions.

## Further Reading

- Bahdanau, Cho, Bengio (2014), *Neural Machine Translation by Jointly Learning to Align and Translate* — the original attention paper.
- Sutskever et al. (2014), *Sequence to Sequence Learning with Neural Networks* — the Seq2Seq model attention fixed.
- Luong et al. (2015), *Effective Approaches to Attention-based Neural Machine Translation* — multiplicative attention.
- Vaswani et al. (2017), *Attention Is All You Need* — the Transformer.

## The Historical Timeline (Detailed)

### 2014 (Sept): Seq2Seq (Sutskever et al.)
- RNN encoder + RNN decoder for translation.
- **Problem**: single fixed-length "thought vector" — information bottleneck.
- Workaround: reverse the source sentence (made relevant info most recent).

### 2014 (Sept): Bahdanau Attention (Bahdanau, Cho, Bengio)
- Added attention to Seq2Seq: decoder computes a weighted average of encoder hidden states at each step.
- **Solved**: the bottleneck — decoder can retrieve any source position.
- Used **additive attention** (alignment score = $\mathbf{v}^T \tanh(\mathbf{W}_s \mathbf{s} + \mathbf{W}_h \mathbf{h})$).

### 2015: Luong Attention (Luong et al.)
- Simplified Bahdanau's attention.
- Used **multiplicative attention** (alignment score = $\mathbf{s}^T \mathbf{W} \mathbf{h}$) — simpler and faster.
- Introduced "local attention" — attend to a window around a predicted position (precursor to sliding window attention).

### 2017: Transformer (Vaswani et al.)
- "Attention Is All You Need" — removed RNNs entirely; attention only.
- **Self-attention**: attend within the same sequence (not cross-attention to another sequence).
- **Multi-head attention**: multiple attention heads in parallel.
- **Scaled dot-product attention**: $\text{softmax}(QK^T / \sqrt{d_k}) V$.
- Solved RNN's sequential bottleneck — fully parallel.

### 2018+: Modern Attention
- **BERT (2018)**: bidirectional self-attention for encoding.
- **GPT (2018+)**: causal self-attention for generation.
- **Efficient attention (2020+)**: FlashAttention, sparse, linear, sliding window.
- **Modern attention (2023+)**: GQA, MQA, MLA for KV cache reduction.

## Why Attention Was Invented (The Specific Problem)

The specific problem Bahdanau et al. (2014) solved: **RNN Seq2Seq's information bottleneck**.

### The bottleneck
Seq2Seq (Sutskever 2014) compressed the entire source sentence into a single fixed-length vector $\mathbf{c}$ (the encoder's final hidden state). The decoder then generated the target from $\mathbf{c}$ alone — no access to intermediate encoder states.

For short sentences, $\mathbf{c}$ has enough capacity. For long sentences, $\mathbf{c}$ can't hold all the information — the decoder "forgets" early parts of the source. Translation quality degraded with sentence length.

### Attention's solution
Bahdanau's insight: instead of one $\mathbf{c}$, give the decoder **per-step access to all encoder hidden states**. At each decoding step, compute a weighted average:

$$
\mathbf{c}_t = \sum_{i=1}^n \alpha_{ti} \mathbf{h}_i
$$

where $\alpha_{ti}$ are attention weights (how much to attend to source position $i$ at target step $t$). The decoder uses $\mathbf{c}_t$ (different at each step) plus its own hidden state to generate the next token.

### Why this was revolutionary
1. **Bottleneck broken**: decoder can retrieve any source position at any time.
2. **Alignment learned**: attention weights $\alpha_{ti}$ learn word alignments (which source word corresponds to which target word) — interpretable.
3. **Long sentences work**: quality no longer degrades with length.
4. **Foundation for Transformers**: self-attention is the natural extension (attend within the same sequence, not cross-sequence).

## From Cross-Attention to Self-Attention (Conceptual Leap)

Bahdanau attention was **cross-attention** — decoder attends to encoder. The leap to **self-attention** (Transformer 2017) was: why not attend within the same sequence?

### Self-attention intuition
In a sentence, each word's meaning depends on other words in the same sentence. "Bank" in "river bank" vs. "bank account" — the meaning depends on context. Self-attention lets each word attend to all other words in the same sequence, building contextual representations.

### Why self-attention replaced RNNs
- **RNN**: sequential — processes one token at a time, hidden state carries information forward.
- **Self-attention**: parallel — every token attends to every other in one step. No sequential bottleneck.
- **Result**: Transformers train 10× faster than RNNs on GPUs (parallelism), and capture long-range dependencies better (no vanishing gradients through time).

The conceptual path: cross-attention (Bahdanau 2014) → self-attention (Transformer 2017) → modern attention (GQA, MLA 2023+). Each step refined the attention mechanism for a new use case.

## Worked Example: Attention Weights as Alignments

One of the most interpretable aspects of attention: the weights $\alpha_{ti}$ form an **alignment matrix** showing which source word corresponds to which target word.

```python
# For English → French translation:
# Source: "the cat sat on the mat"
# Target: "le chat s'est assis sur le tapis"

# Attention weights (simplified):
#         the   cat   sat   on   the   mat
# le     [0.7   0.2   0.0   0.0  0.1    0.0]  # "le" attends to "the"
# chat   [0.1   0.8   0.0   0.0  0.1    0.0]  # "chat" attends to "cat"
# s'est  [0.0   0.0   0.7   0.2  0.0    0.0]  # "s'est" attends to "sat"
# assis  [0.0   0.0   0.8   0.1  0.0    0.0]  # "assis" attends to "sat"
# sur    [0.0   0.0   0.0   0.9  0.0    0.0]  # "sur" attends to "on"
# le     [0.1   0.0   0.0   0.0  0.7    0.2]  # "le" attends to "the"
# tapis  [0.0   0.0   0.0   0.0  0.1    0.8]  # "tapis" attends to "mat"
```

This alignment is **learned** — the model isn't told the alignment, it discovers it through training. The attention weights are interpretable in a way that RNN hidden states are not.

## Connection to Other Concepts

- [[04 - Neural Networks/Architectures/05 - Seq2Seq and the Information Bottleneck|Seq2Seq and the Information Bottleneck]] — the problem attention solved.
- [[06 - Attention Mechanisms/Origins/02 - Bahdanau Attention|Bahdanau Attention]] — the first attention mechanism.
- [[06 - Attention Mechanisms/Origins/03 - Luong Attention|Luong Attention]] — simplified variant.
- [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]] — the Transformer extension.
- [[06 - Attention Mechanisms/Multi-Head Attention/05 - Multi-Head Attention|Multi-Head Attention]] — parallel attention heads.
- [[26 - Papers/Attention Origins/01 - Bahdanau Attention 2014|Bahdanau Attention 2014 paper]] — the original paper.
- [[26 - Papers/Transformers/02 - Vaswani Attention Is All You Need 2017|Vaswani 2017 paper]] — the Transformer.
- [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]] — attention weights as explanations (with caveats).

## Interview Questions

1. **Q: What specific problem was attention invented to solve?**
   A: RNN Seq2Seq's information bottleneck. Seq2Seq compressed the entire source sentence into a single fixed-length vector $\mathbf{c}$. For long sentences, $\mathbf{c}$ couldn't hold all the information — translation quality degraded with length. Attention solved this by giving the decoder per-step access to all encoder hidden states, computed as a weighted average: $\mathbf{c}_t = \sum_i \alpha_{ti} \mathbf{h}_i$. The bottleneck was broken — the decoder could retrieve any source position at any time.

2. **Q: What's the difference between cross-attention and self-attention?**
   A: Cross-attention (Bahdanau 2014): decoder attends to encoder — different sequences. Self-attention (Transformer 2017): a sequence attends to itself — same sequence. Self-attention is the natural extension: each word attends to all other words in the same sentence to build contextual representations. The conceptual leap was realizing that the attention mechanism works within a sequence, not just across sequences.

3. **Q: Why did attention replace RNNs?**
   A: Three reasons. (1) Parallelism: self-attention processes all tokens in parallel; RNNs are sequential. Transformers train 10× faster on GPUs. (2) Long-range dependencies: attention has direct access to any position; RNNs suffer vanishing gradients through time. (3) Bottleneck removal: attention gives per-step access to all positions; RNN compresses into a fixed hidden state. The Transformer (2017) removed RNNs entirely — "Attention Is All You Need".

4. **Q: What do attention weights represent, and are they interpretable?**
   A: In cross-attention (translation), attention weights $\alpha_{ti}$ represent word alignments — which source word corresponds to which target word. This is interpretable and was a major selling point of early attention. In self-attention, attention weights show which tokens each token attends to — useful for analysis but less directly interpretable. Caveat: attention weights are correlational, not causal — high attention doesn't mean the model "uses" that information (see [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]]).

5. **Q: How did Bahdanau attention differ from Luong attention?**
   A: Bahdanau (2014) used **additive attention**: alignment score = $\mathbf{v}^T \tanh(\mathbf{W}_s \mathbf{s} + \mathbf{W}_h \mathbf{h})$ — a small neural network. Luong (2015) used **multiplicative attention**: alignment score = $\mathbf{s}^T \mathbf{W} \mathbf{h}$ — a simple dot product. Luong's is simpler and faster; Bahdanau's is more expressive. Modern Transformers use the multiplicative form (scaled dot-product) for efficiency. Luong also introduced "local attention" — a precursor to sliding window attention.

6. **Q: Trace the evolution from Bahdanau attention to modern Transformers.**
   A: (1) Bahdanau (2014): cross-attention for Seq2Seq translation — solved the bottleneck. (2) Luong (2015): simplified to multiplicative attention; introduced local attention. (3) Transformer (2017): self-attention within a sequence; removed RNNs; multi-head attention; scaled dot-product. (4) BERT/GPT (2018): bidirectional/causal self-attention for pretraining. (5) Efficient attention (2020+): FlashAttention, sparse, linear. (6) Modern attention (2023+): GQA, MQA, MLA for KV cache reduction. Each step refined attention for a new use case — translation, encoding, generation, efficiency, serving.

## See Also

- [[Bahdanau Attention]]
- [[Luong Attention]]
- [[Self-Attention]]
- [[Multi-Head Attention]]
- [[06 - Attention Mechanisms/MOC|Attention Mechanisms MOC]]
- [[04 - Neural Networks/MOC|Neural Networks MOC]] — RNN/LSTM background
