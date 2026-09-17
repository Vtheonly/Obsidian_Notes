---
tags: [foundation-models, reasoning-models, o1, r1, test-time-compute]
iteration: 8
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Reasoning Models, o1, R1]
---

# 03 - Reasoning Models (o1, R1)

> [!info] TL;DR
> Reasoning models (OpenAI o1/o3, DeepSeek-R1, Claude extended thinking, Gemini 2.5) are LLMs trained to produce long internal chain-of-thought before answering. They spend more compute at inference ("test-time compute scaling") to solve harder problems. SOTA on math, coding, and multi-step reasoning in 2025–2026.

## What Makes a Reasoning Model

A reasoning model is a standard LLM (decoder-only Transformer) plus:
1. **Training to produce long CoT**: RL on verifiable-reward signals (math, code) or process-reward models.
2. **Inference-time "thinking"**: the model generates a hidden chain-of-thought before the final answer.
3. **Higher test-time compute**: more tokens generated = more compute = better answers (for hard problems).

The architecture is unchanged from a regular LLM. The training and inference pattern differ.

## OpenAI o1 / o3 (Sep 2024 – 2025)

- **o1** (Sep 2024): first major reasoning model. Internal CoT (hidden from user). SOTA on math, coding, science.
- **o1-pro**: higher compute budget per query.
- **o3** (Dec 2024 / Jan 2025): significantly stronger; frontier on ARC-AGI, math olympiad, competitive programming.
- **o3-mini**: smaller, cheaper, near-o1 quality.

The training recipe: RL with verifiable rewards (math correctness, code passing tests) plus a process reward model that rewards correct intermediate steps.

The CoT is hidden from users (only a summary is shown) — OpenAI cites safety and competitive reasons.

## DeepSeek-R1 (Jan 2025)

Open-source reasoning model from DeepSeek. Based on DeepSeek-V3 (MoE).

**Training recipe** (R1-Zero → R1):
1. **R1-Zero**: pure RL on verifiable rewards, no SFT first. The model spontaneously learns to produce long CoT.
2. **R1**: add SFT on cold-start data, then RL. Better readability, formatting, and safety.

R1's full training details and weights are open. This was a major moment — it showed that the reasoning-model recipe was reproducible without OpenAI's full pipeline.

## Claude Extended Thinking (Anthropic, Feb 2025)

Claude 3.7+ supports "extended thinking" mode: the model produces visible CoT before answering. Users can see the thinking (unlike OpenAI's hidden CoT) and even guide it.

## Gemini Thinking Mode (Google, Mar 2025)

Gemini 2.5+ has a similar "thinking" mode. Available in the API and the consumer Gemini app.

## How to Use Reasoning Models

### When to use
- **Math olympiad, competitive programming, scientific reasoning** — these models are dramatically better.
- **Multi-step planning** — agents that need to think through complex sequences.
- **Hard debugging** — code that requires deep understanding.
- **Research-style questions** — open-ended problems needing exploration.

### When NOT to use
- **Simple Q&A** — overkill; a regular LLM is faster and cheaper.
- **High-volume / low-latency** — reasoning models are slow (30s+ per query) and expensive.
- **Tasks where standard LLMs are already SOTA** — translation, summarization, basic classification.

## Worked Example (DeepSeek-R1 via OpenAI-compatible API)

```python
from openai import OpenAI
client = OpenAI(api_key="your-key", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",  # R1
    messages=[{"role": "user", "content": "Prove that the sum of two odd numbers is even."}],
)

# The response has both reasoning_content (the CoT) and content (the answer)
print("Reasoning:")
print(response.choices[0].message.reasoning_content)
print("\nAnswer:")
print(response.choices[0].message.content)
```

## Why This Matters for AI

- Reasoning models represent the **biggest capability jump of 2024–2025**. They open up tasks previously inaccessible to LLMs (competition math, complex code refactoring, scientific problem-solving).
- The recipe (RL on verifiable rewards) is **reproducible** — R1 proved this. Open-source reasoning models are now viable.
- Test-time compute scaling is a **new dimension** of capability. Instead of just training bigger models, you can also let models think longer at inference.
- For agents, reasoning models enable longer horizons and more reliable tool use.

## Production Implications

- **Cost**: reasoning models are 5–50x more expensive per query than standard LLMs (due to long CoTs).
- **Latency**: responses take 10s–2min. Not suitable for real-time chat; suitable for batch / async tasks.
- **Don't prompt with CoT** — reasoning models do their own CoT. Just ask the question directly.
- **For agents**, reasoning models improve planning but cost more. Use selectively for hard planning steps.
- **Hybrid systems**: route easy queries to a standard LLM, hard queries to a reasoning model. Cost optimization.

## Common Pitfalls

- **Forcing CoT in the prompt** — reasoning models do this themselves; extra CoT instructions can confuse them.
- **Using reasoning models for everything** — 10x cost for tasks where a standard LLM suffices.
- **Trusting the CoT as explanation** — the CoT may not reflect actual computation. See [[15 - AI Agents/Reasoning/Chain-of-Thought|Chain-of-Thought]] § unfaithfulness.
- **Forgetting that thinking is hidden in some APIs** (o1) — you can't see or guide the model's reasoning.

## Further Reading

- OpenAI (2024), *Learning to Reason with LLMs* (o1 announcement).
- DeepSeek-AI (2025), *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*.
- Snell et al. (2024), *Scaling LLM Test-Time Compute Optimally Can Be More Effective Than Scaling Model Parameters*.

## The Training Recipe in Detail

The reasoning-model recipe (o1, R1, o3) differs from standard instruction tuning in three key ways. Understanding the recipe clarifies why these models suddenly outperform much larger non-reasoning models on math/code.

### 1. Verifiable Rewards (the key innovation)

Standard RLHF uses a learned reward model trained on human preference data. This works for "is response A better than response B" but is unreliable for math/code because:
- Human labelers often can't tell which math proof is correct.
- Reward models can be gamed (reward hacking) — they reward confident-sounding wrong answers.

Reasoning models use **verifiable rewards**: a function that checks correctness objectively:
- Math: does the final answer match the known answer?
- Code: do the unit tests pass?
- Logic puzzles: does the solution satisfy all constraints?

The reward is binary (1 if correct, 0 if wrong) or graded (partial credit for some tests passing). This gives a clean, unhackable signal.

### 2. Process Reward Models (PRMs) — sometimes

For some reasoning models (especially o1, plausibly), an additional **process reward model** evaluates intermediate reasoning steps, not just the final answer. A PRM is trained on (step, correctness) labels from human annotators or from rollouts that lead to correct/incorrect final answers.

PRMs help when the model is "on the wrong track" early in a long CoT — the PRM can detect this and the policy can correct course. They are expensive to train (need step-level labels) and not always used; R1 uses outcome-only rewards and still works.

### 3. RL on long rollouts

The actual RL training samples long CoT trajectories (10K-100K tokens) from the model, scores them with the verifiable reward, and updates the policy. This is technically PPO or GRPO (Group Relative Policy Optimization, DeepSeek's variant).

GRPO simplifies PPO by:
- Sampling N completions per prompt (typically 4-16).
- Computing rewards for each.
- Using the **group baseline** (mean reward of the N samples) as the value estimate.
- No separate value model needed (PPO needs a value model; GRPO doesn't).

This makes GRPO cheaper than PPO and more stable for the binary-reward setting common in reasoning training.

### Cold Start vs Pure RL

R1-Zero showed that pure RL (no SFT first) on a base model can produce emergent CoT. But R1-Zero had readability issues — the CoT was sometimes incoherent or repeated. R1 (full) uses a **cold start**: a small amount of high-quality CoT data is used for SFT before RL, which produces a more polished final model.

The o1/o3 training recipe is not fully disclosed; the community consensus is that they use SFT on high-quality reasoning data + RL on verifiable rewards + (possibly) PRMs.

## Test-Time Compute Scaling Law

Snell et al. (2024) showed that test-time compute scales: more thinking → better answers, with diminishing returns. The relationship is approximately:

$$\text{Accuracy} \propto \log(\text{test-time tokens})$$

So doubling the thinking budget gives a roughly constant accuracy improvement. This means:
- For easy problems, a small thinking budget suffices.
- For hard problems, the budget matters a lot — going from 1K to 100K thinking tokens can take accuracy from 30% to 80%.
- For inference-time problems where the user has a budget, you can trade cost for accuracy.

Practical implication: most production deployments of reasoning models use **adaptive thinking budgets** — short budget for easy queries, long budget for hard ones. This requires a classifier or the user to specify difficulty.

## When Reasoning Models Fail

Reasoning models are not universally better. They fail on:
- **Tasks with no verifiable answer**: open-ended writing, brainstorming, emotional support. The long CoT adds nothing and may make the output more rigid.
- **Tasks where the model's training data was already sufficient**: translation between common languages, simple factual Q&A, basic classification. The CoT overhead is pure cost.
- **Tasks requiring multiple agent turns**: a single long CoT is not the same as a multi-step agent that observes intermediate results. For tool-use with external state, agents beat reasoning models.
- **Tasks with tight latency budgets**: a 60-second response is unacceptable for real-time chat, autocomplete, or interactive UI.

The hybrid pattern (route easy queries to a fast model, hard queries to a reasoning model) is the dominant production pattern in 2026.

## Detailed Cost Analysis

Concrete cost comparison (2026 pricing, approximate):

| Model                | Input $/1M tokens | Output $/1M tokens | Avg CoT length | Cost per query (avg) |
|----------------------|-------------------|--------------------|----------------|----------------------|
| GPT-4o               | $2.50             | $10.00             | 0              | ~$0.005              |
| Claude 3.5 Sonnet    | $3.00             | $15.00             | 0              | ~$0.008              |
| Llama 3.1 70B (self) | ~$0.50            | ~$0.50             | 0              | ~$0.001              |
| o1-mini              | $3.00             | $12.00             | ~10K           | ~$0.12               |
| o1                   | $15.00            | $60.00             | ~30K           | ~$1.80               |
| o3-mini              | $3.00             | $12.00             | ~15K           | ~$0.18               |
| DeepSeek-R1          | $0.55             | $2.19              | ~20K           | ~$0.04               |

(Average query = 500 input tokens + CoT + 500 output tokens.)

Key observations:
- Reasoning models are 10-100× more expensive per query than standard LLMs.
- DeepSeek-R1 is dramatically cheaper than o1 because of (a) lower base prices and (b) MoE efficiency.
- The dominant cost is the CoT itself — 20K thinking tokens at $60/1M is $1.20 alone.
- For batch workloads, this is fine. For real-time chat, it's a non-starter for most use cases.

## Production Patterns for Reasoning Models

### Pattern 1: Router-Based Hybrid

```python
def route_query(query: str) -> str:
    if is_simple(query):  # classifier or rules
        return "gpt-4o"
    elif is_hard_reasoning(query):
        return "o3-mini"
    else:
        return "claude-3.5-sonnet"

model = route_query(user_query)
response = call_llm(model, user_query)
```

The router can be a small classifier, an LLM-as-judge, or rule-based on query length/keywords. This pattern typically reduces cost by 5-10× while preserving quality on hard queries.

### Pattern 2: Caching Verified Answers

For math/code problems with verifiable answers, cache (query → answer) pairs. A user asking the same problem later gets the cached answer instantly, with no reasoning cost. This works well for educational platforms and coding tools.

### Pattern 3: Reasoning Model as Planner

For agent systems, use a reasoning model only for the planning step (which is hard and benefits from long thinking), then execute the plan with a fast model. This combines the reasoning quality of o1 with the speed of Llama 3 for execution.

### Pattern 4: Distillation to Fast Models

Train a smaller, faster model (Llama 3 8B) on the outputs of a reasoning model (R1). The distilled model learns to produce the answer directly, without the long CoT, but inherits some of the reasoning quality. This is the standard recipe for "reasoning-capable small models" in 2026.

## Connection to Other Concepts

- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Test-Time Compute Scaling]] — the formal scaling law.
- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO|RLHF with PPO]] — the underlying RL method.
- [[03 - Machine Learning/Reinforcement Learning/10 - PPO Deep Treatment|PPO]] — the policy gradient algorithm.
- [[15 - AI Agents/Reasoning/02 - Chain-of-Thought|Chain-of-Thought]] — the prompting technique that reasoning models internalize.
- [[15 - AI Agents/Reasoning/06 - Tree of Thoughts and Self Consistency|Self-Consistency]] — non-RL approach to similar problems.
- [[08 - LLMs/Capabilities/04 - In-Context Learning|In-Context Learning]] — reasoning models extend ICL with explicit thinking.
- [[26 - Papers/2024-2026/12 - DeepSeek-R1 2025|DeepSeek-R1 paper note]] — full paper details.
- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] — used for distillation of reasoning models.

## Interview Questions

1. **Q: What is a verifiable reward, and why is it critical for reasoning models?**
   A: A verifiable reward is a function that objectively checks answer correctness — math answer matches, code passes tests, logic puzzle satisfies constraints. Critical because (1) human labelers can't reliably judge math/code correctness, (2) learned reward models can be gamed (reward hacking) by confident-sounding wrong answers, (3) the binary signal is unbiased, providing clean gradient for RL.

2. **Q: What is GRPO, and how does it differ from PPO?**
   A: Group Relative Policy Optimization (DeepSeek's variant) samples N completions per prompt, computes their rewards, and uses the group mean as the baseline. Unlike PPO, GRPO doesn't need a separate value model — the group statistics serve as the baseline. This is simpler, cheaper, and more stable for the binary-reward setting common in reasoning training. PPO is more general; GRPO is optimized for the reasoning case.

3. **Q: Why does R1-Zero's emergent CoT matter?**
   A: It showed that you don't need supervised CoT data to train a reasoning model. Pure RL on verifiable rewards, starting from a base model, spontaneously produces long CoT. This was surprising — the field assumed you needed to teach the model to "think" with SFT first. R1-Zero proved the recipe was simpler than expected, opening the door to cheap replication.

4. **Q: How do you choose between o1, o3-mini, and a standard LLM for a query?**
   A: Route by difficulty. Simple queries (translation, factual lookup, basic Q&A) → standard LLM (cheaper, faster). Hard reasoning (math competition, multi-step debugging, scientific proof) → o3-mini or R1 (cheaper than o1, near-o1 quality). Use o1 only for the hardest problems where the marginal quality justifies 10× cost. The router can be a small classifier or an LLM-as-judge.

5. **Q: Why are reasoning models' CoTs sometimes hidden from users?**
   A: Three reasons cited by OpenAI: (1) competitive — disclosing the CoT helps competitors replicate, (2) safety — the CoT may reveal capabilities the model has but shouldn't expose, (3) user experience — long CoTs are hard to read and the user only needs the answer. Anthropic and DeepSeek show the CoT (or a summary), arguing that transparency helps debugging and trust. The trade-off is open.

6. **Q: How would you distill a reasoning model into a smaller, faster model?**
   A: Generate (prompt, full CoT, answer) triples from the reasoning model on a large dataset. Fine-tune a smaller model (e.g., Llama 3 8B) on these triples with SFT. The distilled model learns to produce the answer with a much shorter CoT (or none), inheriting some reasoning quality. Optionally, follow with DPO on (correct, incorrect) pairs from the distilled model's own samples. This typically gives 80% of the reasoning model's quality at 1/10 the cost.

7. **Q: Why is test-time compute scaling a "new dimension" of capability?**
   A: Pre-2024, capability came from (1) more parameters, (2) more training data, (3) more training compute. Test-time compute adds a fourth: more inference compute. The Snell et al. scaling law shows this dimension has its own scaling curve, and it can substitute for parameter scaling — a smaller model with more thinking can beat a larger model with less thinking, on hard problems. This opens a new design space for AI systems.

## See Also

- [[04 - In-Context Learning]]
- [[15 - AI Agents/Reasoning/Chain-of-Thought|Chain-of-Thought]]
- [[12 - Fine-Tuning/DPO/DPO Derivation|DPO]]
- [[03 - Machine Learning/Reinforcement Learning/10 - PPO Deep Treatment|PPO]]
- [[09 - Foundation Models/MOC|Foundation Models MOC]]
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Research Frontiers: Reasoning]] (planned)