---
tags: [llms, inference, sampling, decoding]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Sampling Strategies, Decoding Strategies]
---

# Sampling Strategies

> [!info] TL;DR
> How to turn an LLM's output logits into actual tokens. Covers greedy, beam search, temperature, top-k, top-p (nucleus), repetition penalties, and the modern defaults that most LLM APIs use.

## The Problem

At each generation step, the LLM outputs a **logit vector** $\mathbf{z} \in \mathbb{R}^{|V|}$ over the vocabulary. To produce the next token, we need to convert this distribution into a single choice (or a sample).

The choice of conversion is the **sampling strategy**. It dramatically affects output quality, diversity, and tone.

## Greedy Decoding

Pick the highest-probability token at every step:

$$
\hat{y}_t = \arg\max_{y} p(y \mid \hat{y}_{<t})
$$

- **Pros**: deterministic, fast, simple.
- **Cons**: prone to repetition loops ("I am I am I am..."); produces generic, low-diversity text.
- **Use**: when you need determinism (e.g., code generation with a fixed seed) or for short outputs.

Most production LLM APIs default to **greedy when temperature=0**.

## Beam Search

Maintain $k$ "beams" (partial sequences) at each step, expand each by one token, keep the top $k$ by cumulative log-probability. At the end, return the highest-scoring beam.

- **Pros**: better than greedy for tasks with a clear objective (translation, summarization).
- **Cons**: expensive ($k \times$ compute); still prone to generic outputs; bad for open-ended generation.
- **Use**: classical MT, summarization; rare in modern LLM chat.

Beam search has largely fallen out of favor for chat/agentic LLMs. Sampling-based methods produce more natural text.

## Temperature Scaling

Divide the logits by a temperature $T$ before softmax:

$$
p(y) = \text{softmax}(\mathbf{z} / T)
$$

- $T = 1$: original distribution.
- $T < 1$ (e.g., 0.7): **sharper** distribution — more confident, less diverse. Greedy in the limit $T \to 0$.
- $T > 1$ (e.g., 1.5): **flatter** distribution — more random, more diverse.

Temperature is the single most important sampling parameter. Most APIs expose it.

### Rule of thumb

| Task                        | Temperature |
|-----------------------------|-------------|
| Code generation             | 0.0–0.2     |
| Factual Q&A                 | 0.0–0.3     |
| Summarization               | 0.3–0.5     |
| General chat                | 0.7–0.9     |
| Creative writing            | 0.9–1.2     |
| Brainstorming               | 1.0–1.5     |

## Top-k Sampling

Sample only from the top $k$ most likely tokens at each step:

1. Sort tokens by probability, keep top $k$.
2. Renormalize their probabilities to sum to 1.
3. Sample from this restricted distribution.

- **Pros**: prevents sampling extremely unlikely tokens (which temperature alone allows).
- **Cons**: $k$ is fixed — bad when the distribution is sharp (top 1 is enough) or flat (top 50 isn't enough).
- **Typical $k$**: 40–50.

## Top-p (Nucleus) Sampling

Sample from the smallest set of tokens whose cumulative probability $\geq p$:

1. Sort tokens by probability (descending).
2. Take tokens until cumulative probability $\geq p$.
3. Renormalize and sample from this set.

- **Pros**: adaptive — small set when distribution is sharp, large set when flat.
- **Cons**: slightly more expensive than top-k.
- **Typical $p$**: 0.9–0.95.

Top-p is generally preferred over top-k for chat applications. Most modern LLM APIs default to top-p = 0.9 or 1.0 with a temperature.

## Combined: Temperature + Top-k + Top-p

The standard recipe:

1. Divide logits by temperature.
2. Apply top-k filter (if $k < |V|$).
3. Apply top-p filter (if $p < 1$).
4. Softmax the filtered logits (with $-\infty$ for excluded tokens).
5. Sample.

```python
def sample(logits, temperature=0.7, top_k=50, top_p=0.9):
    if temperature == 0:
        return logits.argmax(dim=-1)
    
    logits = logits / temperature
    
    # Top-k
    if top_k > 0:
        top_k = min(top_k, logits.size(-1))
        vals, _ = torch.topk(logits, top_k)
        thresh = vals[..., -1, None]
        logits = torch.where(logits < thresh, float('-inf'), logits)
    
    # Top-p
    if top_p < 1.0:
        sorted_logits, sorted_idx = torch.sort(logits, descending=True)
        cum_probs = F.softmax(sorted_logits, dim=-1).cumsum(dim=-1)
        # Shift right so we always keep at least one token
        sorted_remove = cum_probs > top_p
        sorted_remove[..., 1:] = sorted_remove[..., :-1].clone()
        sorted_remove[..., 0] = False
        indices_to_remove = sorted_remove.scatter(-1, sorted_idx, sorted_remove)
        logits = logits.masked_fill(indices_to_remove, float('-inf'))
    
    probs = F.softmax(logits, dim=-1)
    return torch.multinomial(probs, num_samples=1).squeeze(-1)
```

## Repetition Penalties

To discourage repeating recent tokens, apply a penalty to tokens that already appeared:

### Frequency penalty
Subtract a constant from each token's logit proportional to how many times it has appeared:

$$
z_i' = z_i - \lambda \cdot \text{count}(i)
$$

### Presence penalty
Subtract a constant from any token that has appeared at least once:

$$
z_i' = z_i - \lambda \cdot \mathbb{1}[\text{count}(i) > 0]
$$

### Original CTRL penalty (Keskar et al., 2019)
Multiply the log-probability by a factor $< 1$ for tokens that appeared:

$$
p_i' = p_i / \lambda^{\text{count}(i)}
$$

This is what HuggingFace's `RepetitionPenaltyLogitsProcessor` implements.

OpenAI's API exposes `frequency_penalty` and `presence_penalty` (separately). Most local LLM libraries expose a single `repetition_penalty`.

## Other Sampling Strategies (Briefly)

### Typical sampling (Meister et al., 2022)
Sample from tokens whose per-token information is close to the expected information. Theoretically motivated; rare in production.

### Mirostat (Basu et al., 2020)
Adaptive temperature that maintains a target "surprise" level. Good for keeping output diverse without going off the rails. Used by some local LLM libraries (llama.cpp).

### Constrained decoding
Restrict the output to a formal grammar (regex, JSON schema, context-free grammar). Used for structured output. Implemented by Outlines, Guidance, lm-format-enforcer, and OpenAI's "structured outputs".

### Classifier-free guidance (CFG)
For conditional generation (e.g., with a system prompt), scale the difference between conditional and unconditional logits:

$$
\mathbf{z}' = \mathbf{z}_{\text{uncond}} + \alpha (\mathbf{z}_{\text{cond}} - \mathbf{z}_{\text{uncond}})
$$

Larger $\alpha$ → more "guidance" toward the condition. Common in image diffusion; less common in LLMs but gaining traction.

## Why This Matters for AI

- Sampling strategy is one of the **highest-leverage production knobs**. A bad choice can make a good model look terrible (greedy → repetitive; high temperature → incoherent).
- Different tasks need different strategies. Don't use the same defaults for code, chat, and creative writing.
- **Structured output** (JSON, function calls) requires constrained decoding. This is becoming a standard feature of LLM APIs.
- For agentic systems, sampling strategy affects reliability — slightly lower temperatures often improve tool-call correctness.

## Production Implications

- **Default recipe for chat**: temperature 0.7, top_p 0.9, top_k 50, repetition_penalty 1.1. Most users won't tune these.
- **For code / structured output**: temperature 0.0–0.2, with constrained decoding if applicable.
- **For RAG**: temperature 0.0–0.3 — you want grounded, low-creativity answers.
- **For agents**: temperature 0.0–0.5 for tool calling (reliability matters), but maybe 0.7+ for exploratory planning steps.
- **Streaming**: sample one token at a time, decode incrementally. Most APIs do this.
- **Seeding**: pass a seed for reproducibility. Useful for testing.

## Common Pitfalls

- **Temperature = 0 with sampling** — different libraries handle this differently. Some return argmax, some divide by zero. Be explicit.
- **Forgetting to apply the same chat template** that the model was trained with — produces silent quality loss.
- **Aggressive repetition penalty** (>1.3) — degrades output quality, makes it harder to use domain terms that legitimately repeat.
- **Top-p = 1.0 with high temperature** — can produce incoherent text because very unlikely tokens get sampled.
- **Mixing strategies inconsistently** across prompts in a batch — vectorized sampling assumes all sequences use the same parameters.

## Further Reading

- Holtzman et al. (2019), *The Curious Case of Neural Text Degeneration* — nucleus sampling.
- Keskar et al. (2019), *CTRL: A Conditional Transformer Language Model for Controllable Generation* — repetition penalty.
- Meister et al. (2022), *Typical Decoding for Natural Language Generation*.
- Fan et al. (2018), *Hierarchical Neural Story Generation* — top-k sampling.

## See Also

- [[KV Cache Mechanics]]
- [[08 - LLMs/MOC|LLMs MOC]]
- [[13 - Inference/MOC|Inference MOC]]
- [[Entropy Cross-Entropy KL]] — softmax's foundation

## Mirostat — Adaptive Surprise Control

Mirostat (Basu et al., 2020) is an adaptive sampling algorithm that maintains a target "surprise" level (entropy). The key insight: text quality correlates with consistent surprise — too little surprise means repetitive text; too much means incoherent text.

The algorithm:
1. Track the running average surprise $S$ of generated tokens.
2. Adjust temperature dynamically: if $S$ is below target $\tau$, increase temperature; if above, decrease.
3. Use a feedback loop: $\mu \leftarrow \mu - \eta (S - \tau)$, where $\mu$ controls the effective temperature.

Mirostat-3 (2024) improves on the original with better feedback control and supports top-k/top-p filtering alongside the adaptive temperature. Used by llama.cpp and some local LLM libraries. Not widely adopted in API-based serving because it requires per-token adaptation that doesn't batch well.

## Min-P Sampling — The New Alternative

Min-P (Minimum-P) sampling (TODO: cite, 2024) is a newer alternative to top-p that sets a minimum probability threshold relative to the top token:

$$
\text{threshold} = p_{\text{min}} \cdot \max_i p_i$$

Only tokens with $p_i \geq \text{threshold}$ are kept. This is adaptive: when the distribution is sharp (one dominant token), the threshold is high (few tokens survive); when flat, the threshold is low (many tokens survive).

Advantages over top-p:
- **Simpler to reason about**: one parameter ($p_{\text{min}} = 0.05$) vs. top-p's $p = 0.9$.
- **Better at avoiding bad tokens**: top-p can include unlikely tokens when the distribution is flat; min-p naturally excludes them.
- **Increasing adoption**: some local LLM libraries (llama.cpp) now support min-p.

## The Probability Distribution View

All sampling strategies modify the same underlying distribution $p(y) = \text{softmax}(z / T)$. The modifications are:

| Strategy | Modification | Effect |
|----------|-------------|--------|
| Temperature | $z \to z / T$ | Sharpen (T<1) or flatten (T>1) |
| Top-k | $p_i = 0$ for $i \notin \text{top-}k$ | Truncate tail |
| Top-p | $p_i = 0$ for $i$ outside nucleus | Adaptive truncation |
| Min-p | $p_i = 0$ for $p_i < p_{\text{min}} \cdot \max_j p_j$ | Relative threshold |
| Repetition | $z_i \to z_i - \lambda \cdot \text{count}(i)$ | Penalize repeats |
| CFG | $z \to z_{\text{uncond}} + \alpha (z_{\text{cond}} - z_{\text{uncond}})$ | Amplify conditioning |

These are all **logit-level transformations** followed by softmax and sampling. The order matters: typically temperature → top-k → top-p → repetition penalty → sample.

## Worked Example: Comparing Strategies

```python
import torch
import torch.nn.functional as F

logits = torch.tensor([5.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.1, -0.5, -1.0, -2.0])

# Temperature
for T in [0.5, 1.0, 2.0]:
    probs = F.softmax(logits / T, dim=-1)
    print(f"T={T}: {probs.tolist()}")

# Top-k=3
vals, idx = torch.topk(logits, 3)
mask = torch.full_like(logits, float('-inf'))
mask[idx] = 0
print(f"Top-k=3: {F.softmax(logits + mask, dim=-1).tolist()}")

# Top-p=0.9
sorted_logits, sorted_idx = torch.sort(logits, descending=True)
cum_probs = F.softmax(sorted_logits, dim=-1).cumsum(dim=-1)
sorted_remove = cum_probs > 0.9
sorted_remove[1:] = sorted_remove[:-1].clone()
sorted_remove[0] = False
indices_to_remove = sorted_remove.scatter(-1, sorted_idx, sorted_remove)
print(f"Top-p=0.9: {F.softmax(logits.masked_fill(indices_to_remove, float('-inf')), dim=-1).tolist()}")

# Min-p=0.05 (relative to max probability)
probs = F.softmax(logits, dim=-1)
threshold = 0.05 * probs.max()
min_p_mask = probs < threshold
print(f"Min-p=0.05: {F.softmax(logits.masked_fill(min_p_mask, float('-inf')), dim=-1).tolist()}")
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Repetitive output | Temperature too low; or no repetition penalty | Increase T to 0.7+; add repetition penalty 1.1-1.2 |
| Incoherent output | Temperature too high; or top-p too permissive | Lower T to 0.3-0.7; set top-p=0.9 |
| Hallucinated tokens | Top-p=1.0 allows very unlikely tokens | Set top-p=0.9 or top-k=50 |
| Boring/generic output | Temperature=0 (greedy) | Increase T to 0.7+ for creative tasks |
| Cannot produce valid JSON | Free-form sampling includes invalid tokens | Use constrained decoding (JSON schema) |
| Different results on rerun | Stochastic sampling without seed | Set seed; or use temperature=0 for determinism |

## Connection to Other Concepts

- [[13 - Inference/Decoding/07 - Constrained Decoding and CFG|Constrained Decoding and CFG]] — restricting output to valid formats.
- [[13 - Inference/Speculative Decoding/05 - Speculative Decoding|Speculative Decoding]] — draft model must match target's sampling.
- [[08 - LLMs/Context and KV Cache/02 - KV Cache Mechanics|KV Cache Mechanics]] — sampling happens after KV cache lookup.
- [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Entropy, Cross-Entropy, KL]] — temperature scales the softmax, affecting entropy.
- [[02 - Mathematics/Probability/07 - Probability Essentials|Probability Essentials]] — softmax and sampling are probability operations.
- [[08 - LLMs/Capabilities/04 - In-Context Learning|In-Context Learning]] — sampling affects ICL consistency.
- [[08 - LLMs/Evaluation/06 - LLM Benchmarks|LLM Benchmarks]] — benchmark evaluation uses temperature=0.
- [[22 - Production AI/Architecture/03 - Gateway and Router Patterns|Gateway and Router Patterns]] — per-request sampling params.
- [[26 - Papers/Agents and RAG/38 - Self-Consistency 2022|Self-Consistency]] — sampling multiple chains at T>0.

## Interview Questions

1. **Q: What's the difference between top-k and top-p sampling? When would you use each?**
   A: Top-k keeps a fixed number of tokens (e.g., top 50); top-p keeps a variable number whose cumulative probability exceeds p (e.g., 0.9). Top-k is bad when the distribution is very sharp (only 1-2 good tokens, but k=50 lets in noise) or very flat (k=50 isn't enough). Top-p is adaptive: sharp distribution → few tokens kept; flat distribution → many kept. Use top-p for most chat applications; top-k for code generation where you want to limit to plausible completions.

2. **Q: How does temperature affect the output distribution?**
   A: Temperature divides the logits before softmax: $p = \text{softmax}(z/T)$. T<1 sharpens the distribution (more confident, less diverse); T>1 flattens it (less confident, more diverse); T=0 is greedy (argmax). The key insight: temperature doesn't change which token is most likely — it changes the spread. Low temperature → more deterministic; high temperature → more creative but potentially incoherent.

3. **Q: What is min-p sampling and why might it be better than top-p?**
   A: Min-p sets a minimum probability threshold relative to the top token: threshold = $p_{\text{min}} \cdot \max_i p_i$. Only tokens above this threshold survive. It's better than top-p because: (1) it naturally excludes unlikely tokens even when the distribution is flat (top-p can include them); (2) it's simpler to tune (one parameter); (3) it's more robust across different model sizes and vocabularies.

4. **Q: How do repetition penalties work and what are their trade-offs?**
   A: Repetition penalties reduce the logit of tokens that already appeared: $z_i' = z_i - \lambda \cdot \text{count}(i)$. This discourages loops ("I am I am I am"). Trade-offs: (1) too high a penalty (>1.3) hurts quality — domain terms that legitimately repeat get suppressed; (2) frequency penalty (proportional to count) is more aggressive than presence penalty (binary); (3) doesn't distinguish between content words ("the") and meaningful repetitions (technical terms). Use sparingly; default 1.1-1.2.

5. **Q: When should you use beam search vs sampling?**
   A: Beam search for tasks with a clear objective (translation, summarization) where there's one best answer. Sampling for open-ended generation (chat, creative writing) where diversity matters. In practice, beam search has largely fallen out of favor for chat LLMs because it produces generic, low-diversity text. Most modern APIs default to sampling (temperature + top-p).

6. **Q: How does constrained decoding interact with temperature and top-p?**
   A: Constrained decoding masks invalid tokens to $-\infty$ before softmax. Temperature and top-p are applied after masking. The order: (1) compute logits, (2) apply constraint mask, (3) divide by temperature, (4) apply top-k/top-p, (5) softmax, (6) sample. The constraint reduces the effective vocabulary, so temperature may need to be lower than unconstrained (the model has fewer choices, so less need for randomness).
