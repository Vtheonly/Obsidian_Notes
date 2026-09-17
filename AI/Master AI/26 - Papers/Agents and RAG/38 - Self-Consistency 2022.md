---
tags: [paper, self-consistency, reasoning, cot, ensemble, sampling]
iteration: 10
created: 2026-08-08
aliases: [Self-Consistency, Wang 2022, SC CoT]
---

# 38 — Self-Consistency (Wang et al., 2022)

> [!info] TL;DR
> Self-Consistency (SC) is a decoding strategy for chain-of-thought reasoning: sample N different reasoning paths from the same model with the same prompt (using temperature > 0), then take a **majority vote** on the final answer. The insight is that there are many wrong paths to a wrong answer but only one right path to the right answer — so the right answer tends to be the modal one across samples. SC gives a 10–20% absolute improvement on arithmetic and reasoning benchmarks at the cost of N× more compute. It is the cheapest universally-applicable reasoning boost for LLMs.

## Citation

Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., & Zhou, D. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. ICLR 2023. arXiv:2203.11171.

## The Problem Being Solved

[[02 - Chain-of-Thought|Chain-of-thought]] (CoT) prompting dramatically improved LLM reasoning by asking the model to think step-by-step before answering. The original CoT paper used **greedy decoding** — sample one reasoning path, take its answer. But greedy decoding is fragile: if the single sampled path goes wrong at step 2, the final answer is wrong, even if the model could have produced a correct path with slightly different sampling.

Wang et al. observed that for many reasoning problems, the correct answer is unique (e.g., "What is 27 × 13?" has one answer: 351), but there are many correct paths to it (different intermediate arithmetic) and many wrong paths to wrong answers. Greedy CoT picks one path; if it's wrong, you're stuck. Sampling N paths and voting should do better — if the model has any reasonable probability of producing the right answer, the right answer should appear in multiple samples while wrong answers are scattered.

## The Key Idea: Marginalize Over Reasoning Paths

The correct framing is **marginalization**. The probability of the answer $a$ given the question $q$ is:

$$
P(a \mid q) = \sum_{r} P(a, r \mid q) = \sum_{r} P(a \mid r, q) P(r \mid q)
$$

where $r$ is a reasoning path. Greedy CoT approximates this with the single most likely $r$. Self-consistency approximates it by sampling $N$ reasoning paths $r_1, \ldots, r_N \sim P(r \mid q)$ and voting:

$$
\hat{a} = \arg\max_{a} \sum_{i=1}^{N} \mathbb{1}[a_i = a]
$$

where $a_i$ is the answer extracted from path $r_i$. This is a Monte Carlo estimate of $P(a \mid q)$, marginalized over reasoning paths.

The key assumption: the model's $P(a \mid q)$ (marginally) is more correct than its $P(a \mid r, q)$ for any single $r$. This holds when the model "knows" the answer in distribution but individual reasoning paths are noisy.

## The Algorithm

1. **Construct a CoT prompt** — same as standard CoT (few-shot examples with reasoning).
2. **Sample N reasoning paths** from the model with temperature $T > 0$ (typically $T = 0.5$ to $0.7$ and $N = 10$ to $40$). Use nucleus sampling ($p = 0.95$) to keep paths coherent.
3. **Extract the final answer** from each path (parse the last number, the multiple-choice letter, the yes/no, etc.).
4. **Majority vote** — pick the most common answer. Ties broken arbitrarily (or by average path probability).

```python
import re
from collections import Counter

def self_consistent_answer(model, prompt, n_samples=20, temperature=0.7):
    """Sample N CoT paths and majority-vote on the final answer."""
    answers = []
    for _ in range(n_samples):
        response = model.generate(
            prompt,
            temperature=temperature,
            top_p=0.95,
            max_tokens=512,
        )
        # Extract the final answer (e.g., the last number in the response)
        match = re.search(r"answer is[:\s]*([\d\-\.]+)", response, re.IGNORECASE)
        if match:
            answers.append(match.group(1))

    if not answers:
        return None
    # Majority vote
    return Counter(answers).most_common(1)[0][0]
```

## Why It Works — Intuition

Imagine a model with $P(\text{correct answer}) = 0.6$ on a hard arithmetic problem. With greedy decoding, you take one sample and you have a 60% chance of being right. With $N = 20$ samples and majority vote, the probability that the correct answer is the plurality winner is much higher (assuming wrong answers are spread across many distinct values).

Concretely: if the correct answer appears with probability 0.6 per sample, and wrong answers are spread across 5 distinct values each appearing with probability 0.08, then by sampling 20 paths the correct answer is expected to appear ~12 times, while each wrong answer appears ~1.6 times. The correct answer wins the vote with overwhelming probability.

This is why SC works well for **closed-answer** tasks (arithmetic, multiple choice, yes/no) and poorly for **open-ended** tasks (creative writing, summarization) — open-ended tasks have no unique answer to converge on.

## Empirical Results

On the GSM8K benchmark (grade-school math word problems):

| Method                      | GPT-3 (175B) accuracy |
|-----------------------------|----------------------|
| Standard prompting          | 17.7%                |
| CoT (greedy)                | 56.9%                |
| **Self-Consistency (N=40)** | **74.4%**            |

That's a +17.5% absolute improvement from sampling + voting alone — no model changes, no fine-tuning, no extra training data. Just N× more compute at inference.

On other benchmarks (MultiArith, SVAMP, AQuA, commonsense QA), SC consistently improves over greedy CoT by 10–20% absolute.

## Cost-Benefit Analysis

| N (samples) | Quality gain (approximate) | Cost (relative to greedy) |
|-------------|-----------------------------|---------------------------|
| 1           | Baseline (greedy CoT)       | 1×                        |
| 5           | +5–10% absolute             | 5×                        |
| 10          | +10–15% absolute            | 10×                       |
| 20          | +13–17% absolute            | 20×                       |
| 40          | +15–20% absolute            | 40×                       |

Diminishing returns: doubling $N$ from 10 to 20 gives a smaller gain than going from 1 to 10. Most production deployments use $N = 5$ to $10$ as the cost-quality sweet spot.

## When Self-Consistency Helps

- **Closed-answer reasoning**: arithmetic, math, multiple-choice, yes/no. The right answer is unique; wrong answers are spread out.
- **Hard problems**: SC's gain scales with problem difficulty. On easy problems, greedy already gets 95%+; SC can't help much. On hard problems, greedy gets 30%; SC can push to 50%.
- **Models with non-trivial reasoning ability**: if the model has $P(\text{correct}) < 0.1$, sampling won't help because the correct answer is too rare to win votes.

## When Self-Consistency Doesn't Help

- **Open-ended generation**: creative writing, summarization, translation. There's no single "right answer" to converge on.
- **Trivia / lookup**: if the model knows the fact, greedy gets it; if it doesn't, sampling won't invent the fact.
- **Very easy or very hard problems**: at the extremes, the marginal probability is already close to 0 or 1, so voting doesn't change the outcome.
- **Production latency-critical apps**: 10× more compute is often unacceptable for user-facing applications. SC is better suited for batch eval, where latency doesn't matter.

## Variants and Successors

- **Universal Self-Consistency** (Chen et al. 2023) — extends SC to open-ended tasks by using an LLM to vote on the best answer (instead of exact-match voting). Useful when answers can't be extracted by regex.
- **Self-Consistency with diverse prompts** — sample not just with different random seeds but with different prompt phrasings. Increases diversity, slightly improves quality.
- **Speculative self-consistency** — use a small model to generate many cheap paths, then verify the most common answer with a large model. Reduces cost at small quality loss.
- **Best-of-N with verifier** — instead of voting, train a verifier model to score each path, take the highest-scoring one. Used in RLHF and reasoning model training. More expensive than SC but better for open-ended tasks.

## Comparison with Other Reasoning Techniques

| Technique                | Cost (vs greedy CoT) | Quality gain | Best for                          |
|--------------------------|----------------------|--------------|-----------------------------------|
| Greedy CoT               | 1×                   | Baseline     | Latency-critical                  |
| **Self-Consistency**     | 5–40×                | +10–20%      | Closed-answer reasoning, batch    |
| Tree of Thoughts         | 10–100×              | +15–25%      | Planning, search                  |
| Best-of-N + verifier     | 10–100× + verifier   | +15–25%      | Open-ended, RLHF                  |
| Reasoning model (o1/R1)  | 10–1000×             | +20–40%      | Hard reasoning, agentic           |

SC is the cheapest of these — no verifier training, no search, just sample and vote. It is the universally-applicable reasoning boost: works on any model, any task with closed answers.

## Why This Matters for AI

- **SC is the lowest-effort reasoning improvement**: change one line of code (sampling N times instead of once), add a vote. 10–20% quality gain on reasoning benchmarks.
- **SC composes with everything**: works with any base model, any CoT prompt, any task with closed answers. No fine-tuning, no verifier, no architectural changes.
- **SC is the foundation for reasoning models**: o1/R1-style reasoning models use RL to push the model's marginal $P(\text{correct answer})$ higher, which makes SC-style test-time compute more effective. The "test-time compute scaling law" is essentially "more samples + better verification = better answers".
- **SC is the baseline for reasoning eval**: when benchmarking a new model on GSM8K / MATH, always compare against SC with $N = 10$ or $N = 40$. If your model can't beat SC with greedy, the model isn't better — it's just doing what SC does internally.

## Production Implications

- **Batch eval**: always use SC for offline evaluation of reasoning ability. The gain is too large to ignore.
- **Latency-critical**: avoid SC in user-facing apps where 10× latency is unacceptable. Use a smaller N (3–5) or switch to a stronger single-pass model.
- **Cost**: at $N = 40$, SC costs 40× more tokens than greedy. For GPT-4-class pricing, that's $40 × $0.06/1K = $2.40 per query — unacceptable for high-volume use. For Llama-3.1-70B self-hosted, the cost is GPU time, which is much cheaper.
- **Caching**: many reasoning problems share a structure (e.g., "solve $a + b$"). Cache answers by problem hash to avoid recomputing.
- **Verification**: for safety-critical applications (math, code), verify the SC answer with a separate verifier (e.g., re-do the computation, run the code). SC reduces error rates but doesn't eliminate them.

## Common Pitfalls

- **Using temperature 0** — SC requires stochastic sampling. With $T = 0$, all $N$ samples are identical and the vote is meaningless. Use $T = 0.5$ to $0.7$.
- **Too few samples** — $N = 1$ is just greedy. $N = 3$ gives marginal gains. $N \geq 10$ is where SC starts to pay off.
- **Bad answer extraction** — if your regex fails on 30% of samples, you've effectively reduced $N$ by 30%. Test extraction on a sample of paths and iterate.
- **Applying SC to open-ended tasks** — majority voting on free-form text doesn't work (every answer is unique). Use Universal SC (LLM-as-voter) or skip SC for open-ended tasks.
- **Counting tokens in the budget** — $N$ CoT paths each have their own reasoning. Total tokens = $N \times$ avg path length. Easy to underestimate cost.

## Further Reading

- Wang et al. (2022), *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv:2203.11171.
- Chen et al. (2023), *Universal Self-Consistency for Language Models*. arXiv:2311.17311.
- Wei et al. (2022), *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. (The original CoT paper.)
- Snell et al. (2024), *Scaling LLM Test-Time Compute Optimally*. (SC is one form of test-time compute.)

## Connection to Other Concepts

- [[15 - AI Agents/Reasoning/02 - Chain-of-Thought|Chain-of-Thought]] — SC builds on CoT.
- [[26 - Papers/Agents and RAG/34 - Tree of Thoughts 2023|Tree of Thoughts 2023]] — search-based extension of SC.
- [[26 - Papers/Agents and RAG/33 - Self-Refine 2023|Self-Refine 2023]] — iterative refinement instead of sampling.
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Test-Time Compute Scaling]] — SC is one form of test-time compute.
- [[08 - LLMs/Sampling/03 - Sampling Strategies|Sampling Strategies]] — temperature, top-p, nucleus sampling.
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]] — reasoning models push $P(\text{correct})$ higher, making SC more effective.

## Interview Questions

1. **Q: Explain the marginalization framing of self-consistency. Why does it work?**
   A: The probability of an answer $a$ given a question $q$ is $P(a \mid q) = \sum_r P(a, r \mid q) = \sum_r P(a \mid r, q) P(r \mid q)$ — marginalize over reasoning paths $r$. Greedy CoT approximates this with the single most likely $r$. SC approximates it by sampling $N$ paths and voting — a Monte Carlo estimate of $P(a \mid q)$. It works because the right answer is unique (so it accumulates votes across correct paths) while wrong answers are spread across many distinct values (so no single wrong answer accumulates enough votes to win).

2. **Q: When does self-consistency NOT help?**
   A: Four cases. (1) Open-ended generation (creative writing, summarization) — no unique answer to converge on. (2) Trivia / lookup — if the model knows the fact, greedy gets it; if it doesn't, sampling won't invent it. (3) Very easy or very hard problems — at the extremes, $P(\text{correct})$ is already near 0 or 1. (4) Latency-critical user-facing apps — 10× more compute is often unacceptable.

3. **Q: What's the cost-quality tradeoff for different N (number of samples)?**
   A: Diminishing returns. Going from $N=1$ (greedy) to $N=10$ gives +10–15% absolute quality. Going from $N=10$ to $N=20$ gives +3–5% more. Going from $N=20$ to $N=40$ gives +2–3% more. The cost scales linearly with $N$. Most production deployments use $N = 5$ to $10$ as the cost-quality sweet spot; offline eval uses $N = 40$ for maximum quality.

4. **Q: How does self-consistency relate to reasoning models like o1 and DeepSeek-R1?**
   A: Reasoning models are trained with RL to push their marginal $P(\text{correct answer})$ higher. This makes SC-style test-time compute more effective: a reasoning model with $P(\text{correct}) = 0.8$ per sample, sampled 10 times, will vote correctly much more often than a base model with $P(\text{correct}) = 0.4$. The "test-time compute scaling law" (Snell et al. 2024) formalizes this: more samples + better verification = better answers, and reasoning models make better use of each sample.

5. **Q: How would you implement self-consistency for a multiple-choice QA task?**
   A: (1) Construct a CoT prompt with few-shot examples. (2) Sample $N = 10$ to $20$ paths with $T = 0.5$ to $0.7$ and top-p $= 0.95$. (3) Extract the multiple-choice letter (A/B/C/D) from each path with a regex. (4) Majority vote on the letters. (5) Return the winning letter. The key implementation details: temperature must be > 0 (otherwise all samples are identical), the extraction regex must be robust (test on a sample), and the vote should handle ties (e.g., by averaging path log-probs).

6. **Q: What is Universal Self-Consistency and why is it needed?**
   A: Universal SC (Chen et al. 2023) extends SC to open-ended tasks by using an LLM to vote on the best answer instead of exact-match voting. For tasks like summarization or creative writing, every sample produces a unique answer, so majority voting doesn't work. Universal SC prompts a separate LLM call: "Here are N candidate answers. Which is best?" This lets SC-style marginalization apply to open-ended tasks, at the cost of one extra LLM call per query.

## See Also

- [[26 - Papers/MOC|Papers MOC]]
- [[15 - AI Agents/Reasoning/02 - Chain-of-Thought|Chain-of-Thought]]
- [[26 - Papers/Agents and RAG/34 - Tree of Thoughts 2023|Tree of Thoughts 2023]]
- [[26 - Papers/Agents and RAG/33 - Self-Refine 2023|Self-Refine 2023]]
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Test-Time Compute Scaling]]
- [[08 - LLMs/Sampling/03 - Sampling Strategies|Sampling Strategies]]
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]]
