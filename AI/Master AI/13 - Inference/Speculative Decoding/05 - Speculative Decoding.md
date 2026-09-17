---
tags: [inference, speculative-decoding, acceleration]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
---

# Speculative Decoding

> [!info] TL;DR
> Speculative decoding accelerates autoregressive LLM inference by using a small "draft" model to propose multiple tokens, then having the large "target" model verify them in a single forward pass. Accepted tokens come free (one forward pass produces multiple tokens); rejected tokens are resampled. 2–3x speedup with no quality loss.

## The Problem: Autoregressive Decode is Slow

During decode, each new token requires a full forward pass through the model. For a 7B model at batch size 1, this is ~5 ms per token (memory-bound on weights). Generating 1000 tokens takes ~5 seconds.

The key observation: during decode at batch size 1, the GPU is **massively underutilized**. The weights are read once per token, but only a tiny amount of compute is done. There's room to do more work per weight read.

## The Insight

If we had a smaller "draft" model that's 5–10x faster, it could propose the next few tokens cheaply. The large "target" model could then verify all those tokens in **one forward pass** (which costs the same as generating one token).

- If the draft's tokens match what the target would have produced: accept them all — got 4 tokens for the price of 1.
- If the draft's tokens mismatch: reject and resample from the target's distribution.

Because verification can be done in parallel (just compute the target's distribution at each position), this is much faster than serial generation.

## The Algorithm

```
1. Draft model generates k candidate tokens: y_1, y_2, ..., y_k
2. Target model runs ONE forward pass over (prompt + y_1, ..., y_k)
   → produces distributions p_1, p_2, ..., p_k at each position
3. For each i from 1 to k:
   - If y_i was sampled from draft's q_i with probability q_i(y_i)
   - And target's p_i(y_i) > q_i(y_i) → accept y_i
   - Else: accept with probability p_i(y_i) / q_i(y_i)
     - If accepted: continue
     - If rejected: resample from adjusted distribution and stop
4. If all k accepted: bonus sample one more from p_k (free!)
5. Repeat
```

The acceptance criterion (step 3) is **importance sampling**. The math guarantees that the final distribution is **exactly the same** as sampling from the target model alone — no quality loss.

### Why no quality loss?

The acceptance/rejection resampling is mathematically equivalent to sampling from $p$ directly. The draft model only affects speed (how often tokens are accepted), not the output distribution. This is the key result from Leviathan et al. (2023) and Chen et al. (2023).

## Speedup Analysis

If the draft model has acceptance rate $\alpha$ (fraction of tokens accepted) and proposes $k$ tokens per round:

- Expected tokens per target forward pass: $\frac{1 - \alpha^{k+1}}{1 - \alpha}$ (geometric series).
- If $\alpha = 0.7, k = 4$: ~2.5 tokens per target pass — **2.5x speedup**.
- If $\alpha = 0.5, k = 4$: ~1.94 tokens per target pass — ~2x speedup.
- If $\alpha = 0.9, k = 7$: ~4.5 tokens per target pass — **4.5x speedup**.

The key is having a good draft model — high acceptance rate is what drives speedup.

## Draft Model Choices

### Same family, smaller version
- Target: Llama 3 70B, Draft: Llama 3 8B.
- Pros: same tokenizer, same training distribution, high acceptance rate.
- Cons: 8B is still relatively large for a draft.

### Distilled draft
- Train a small model to mimic the target's output distribution.
- Pros: small, fast, can be very accurate.
- Cons: requires training; per-target.

### N-gram draft (lookahead)
- Use simple statistics (e.g., n-gram frequencies from the prompt) to predict the next tokens.
- Pros: no model needed; very fast.
- Cons: low acceptance rate for non-repetitive text.

### Self-speculation (layer skip)
- Use the target model itself but skip early — only run the first $L'$ layers, then predict.
- Pros: no separate draft model.
- Cons: requires model architecture support (e.g., Medusa heads).

### Medusa heads
- Add extra "tree" heads to the target model that predict multiple future tokens directly.
- Pros: no separate draft model; high acceptance.
- Cons: requires fine-tuning the target.

### EAGLE
- A learned draft model that takes the target's hidden states as input. Higher acceptance than vanilla spec decoding.
- EAGLE-2 and EAGLE-3 improve further with dynamic draft trees.

## Tree-based Speculation

Modern speculative decoding (EAGLE, Medusa) uses **tree-structured** drafts instead of linear sequences. The draft proposes multiple candidate continuations in a tree, the target verifies all in parallel using a single attention mask.

```
Linear: y_1 → y_2 → y_3 → y_4

Tree:
       y_1
      / | \
    y_2 y_2' y_2''
    /   |    \
  y_3  y_3'  y_3''
```

This is much more efficient because the draft can hedge its bets. The target's forward pass handles all branches via a custom attention mask.

## Implementation Sketch

```python
def speculative_decode(target_model, draft_model, prompt, max_tokens, k=4):
    generated = prompt
    while len(generated) < max_tokens:
        # 1. Draft k tokens
        draft_tokens = []
        draft_dists = []
        context = generated
        for _ in range(k):
            logits = draft_model(context)
            next_dist = F.softmax(logits[:, -1] / 0.7, dim=-1)
            next_token = torch.multinomial(next_dist, 1)
            draft_tokens.append(next_token)
            draft_dists.append(next_dist)
            context = torch.cat([context, next_token], dim=-1)
        
        # 2. Target forward pass over all k+1 positions (parallel)
        target_logits = target_model(context)  # one forward pass
        target_dists = F.softmax(target_logits[:, -k-1:-1] / 0.7, dim=-1)
        
        # 3. Accept/reject
        accepted = 0
        for i in range(k):
            y = draft_tokens[i]
            q = draft_dists[i][..., y]
            p = target_dists[i][..., y]
            
            if p >= q or torch.rand(1) < p / q:
                # Accept
                accepted += 1
            else:
                # Reject; resample from (p - q)_+ normalized
                adjusted = (target_dists[i] - draft_dists[i]).clamp(min=0)
                adjusted = adjusted / adjusted.sum()
                new_token = torch.multinomial(adjusted, 1)
                generated = torch.cat([generated] + draft_tokens[:accepted] + [new_token], dim=-1)
                break
        else:
            # All accepted; bonus sample from p_k
            bonus = torch.multinomial(target_dists[-1], 1)
            generated = torch.cat([generated] + draft_tokens + [bonus], dim=-1)
    
    return generated
```

## Why This Matters for AI

- Speculative decoding is **the** inference acceleration technique for memory-bound (batch-size-1) generation. It's increasingly standard in production.
- The "no quality loss" guarantee is critical — you get speedup without changing model behavior.
- The draft model is a new architectural choice. As of 2026, most open models ship with a recommended draft model (e.g., Llama 3 70B + Llama 3 8B as draft).
- Spec decoding interacts with batching in complex ways. At high batch sizes, the GPU becomes compute-bound and spec decoding helps less (or hurts). At low batch sizes, it's pure win.

## Production Implications

- **For interactive (batch size 1) generation**: spec decoding gives 2–3x speedup. Always enable if you have a good draft model.
- **For batched (high-throughput) generation**: spec decoding may not help. The GPU is already compute-bound; the extra draft work just adds load.
- **Use vLLM or TGI's built-in spec decoding** — they handle the implementation correctly, including tree-based speculation.
- **Draft model choice** matters more than the algorithm. A bad draft (low acceptance) gives no speedup.
- **Memory cost**: you need to load both target and draft in GPU memory. For a 70B + 8B pair, that's ~150 GB in fp16 — multi-GPU required.

## Common Pitfalls

- **Bad draft model** — if acceptance rate is < 30%, spec decoding is slower than no spec decoding.
- **Forgetting to verify** — a common bug is to just accept the draft tokens without verification. This produces wrong outputs (the draft's distribution, not the target's).
- **Wrong temperature in draft** — the draft and target must use the same temperature for the acceptance criterion to be correct.
- **Non-deterministic verification** — must verify in a single batched forward pass; per-token verification loses the speedup.
- **Token-by-token attention** — must use causal attention across all draft tokens in a single pass; this requires careful mask construction.

## Further Reading

- Leviathan, Kalman, Matias (2023), *Fast Inference from Transformers via Speculative Decoding*.
- Chen et al. (2023), *Accelerating Large Language Model Decoding with Speculative Sampling*.
- Cai et al. (2024), *Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads*.
- Li et al. (2024), *EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty*.

## See Also

- [[KV Cache Mechanics]]
- [[PagedAttention]]
- [[Sampling Strategies]]
- [[13 - Inference/MOC|Inference MOC]]


## Interview Questions

1. **Q: How does speculative decoding achieve no quality loss?**
   A: The acceptance/rejection criterion is importance sampling: accept token $y_i$ with probability $\min(1, p(y_i)/q(y_i))$, where $p$ is the target's distribution and $q$ is the draft's. If rejected, resample from the adjusted distribution $(p - q)_+$ normalized. This is mathematically equivalent to sampling from $p$ directly — the draft model only affects speed (acceptance rate), not the output distribution.

2. **Q: What acceptance rate do you need for speculative decoding to be worth it?**
   A: With $k=4$ draft tokens: acceptance rate $\alpha = 0.7$ gives ~2.5x speedup; $\alpha = 0.5$ gives ~2x; $\alpha = 0.3$ gives ~1.3x (barely worth it). Below 30% acceptance, the draft overhead exceeds the verification savings. A good draft model (same family, smaller) typically achieves 60-80% acceptance.

3. **Q: How does tree-based speculation (EAGLE, Medusa) improve on linear speculation?**
   A: Linear: draft proposes one sequence $y_1 \to y_2 \to y_3 \to y_4$. If $y_2$ is rejected, $y_3$ and $y_4$ are wasted. Tree: draft proposes multiple branches at each position. The target verifies all branches in one forward pass using a custom attention mask. This hedges bets — if one branch is rejected, another may succeed. EAGLE-2/3 achieve 3-5x speedup vs 2-3x for linear.

4. **Q: When does speculative decoding NOT help?**
   A: (1) High batch sizes — the GPU is already compute-bound; the extra draft work just adds load. Spec decoding helps most at batch size 1 (memory-bound). (2) Bad draft model — if acceptance rate is <30%, it's slower. (3) Short sequences — the setup cost exceeds the speedup. (4) Non-repetitive text — lower acceptance rate than repetitive/code text.

5. **Q: What is EAGLE and how does it differ from vanilla speculative decoding?**
   A: EAGLE uses a learned draft model that takes the target's hidden states as input, achieving higher acceptance than vanilla (which uses a separate small model). EAGLE-2 adds dynamic draft trees (the tree structure adapts based on context). EAGLE-3 further improves with better feature extraction. EAGLE typically achieves 3-5x speedup vs 2-3x for vanilla.

6. **Q: How does n-gram speculative decoding work?**
   A: Build an n-gram model on-the-fly from the prompt (count n-gram frequencies). Use it to predict the next $k$ tokens. The n-gram model is essentially free ($O(N)$ to build, $O(1)$ to query). Hit rate: 30-60% for repetitive content (code, structured output). No separate model to load — just prompt statistics. Used by some vLLM configurations.

## Connection to Other Concepts

- [[13 - Inference/KV Cache/02 - PagedAttention|PagedAttention]] — draft and target share prefix blocks.
- [[13 - Inference/Serving/04 - vLLM and Continuous Batching|vLLM]] — supports speculative decoding.
- [[08 - LLMs/Sampling/03 - Sampling Strategies|Sampling Strategies]] — draft and target must use same temperature.
- [[05 - NLP Fundamentals/Language Modeling/07 - N-gram Language Models|N-gram LMs]] — n-gram draft models.
- [[13 - Inference/Serving/08 - TensorRT-LLM|TensorRT-LLM]] — supports speculative decoding.
