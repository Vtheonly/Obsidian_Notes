---
tags: [agents, reasoning, chain-of-thought, cot]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
---

# Chain-of-Thought

> [!info] TL;DR
> Chain-of-Thought (CoT) prompting asks the model to "think step by step" before answering. CoT dramatically improves performance on multi-step reasoning tasks (math, logic, code). The foundation of all modern agent reasoning patterns.

## The Idea

Standard prompting asks for a direct answer:

> Q: A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?
> A: $0.10

(Wrong — but this is what most people, and un-CoT'd models, say.)

Chain-of-Thought prompting asks for reasoning first:

> Q: A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?
> A: Let me think step by step. The bat costs $1.00 more than the ball, so if the ball costs $x$, the bat costs $x + 1.00$. Together they cost $x + (x + 1.00) = 2x + 1.00 = 1.10$. So $2x = 0.10$, $x = 0.05$. The ball costs $0.05.

(Now correct.)

Wei et al. (2022) showed this simple trick dramatically improves performance on math, logic, and multi-step reasoning benchmarks. On GSM8K (grade-school math), PaLM 540B jumped from 18% to 57% with CoT.

## Variants

### Zero-shot CoT
Just append "Let's think step by step." to the prompt. Surprisingly effective.

```python
prompt = f"{question}\n\nLet's think step by step."
```

### Few-shot CoT
Provide examples that include reasoning, not just answers:

```
Q: Roger has 5 tennis balls. He buys 2 cans of 3 balls each. How many balls does he have?
A: Roger starts with 5. He buys 2 cans × 3 balls = 6. Total: 5 + 6 = 11.

Q: <new question>
A:
```

### Self-consistency
Sample multiple CoT chains (with temperature > 0), take the majority answer. Reduces variance and improves accuracy.

```python
chains = [llm(cot_prompt, temperature=0.7) for _ in range(5)]
answers = [extract_final_answer(c) for c in chains]
final = majority_vote(answers)
```

### Auto-CoT
Automatically construct few-shot CoT examples by clustering questions and sampling zero-shot CoT outputs. Avoids hand-crafting examples.

## Why Does CoT Work?

Several theories:

### 1. More compute per token
CoT generates more tokens, which means more forward passes through the model. More compute → better reasoning. This is the "test-time compute" view — see [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Reasoning]] (planned).

### 2. Decomposition
CoT breaks a hard problem into easier sub-problems. Each step is simpler than the full problem. This is the "decomposition" view — also the basis of [[15 - AI Agents/Planning/07 - Planner-Executor Pattern|Planning]].

### 3. Attention over intermediate results
The model attends to its own intermediate reasoning when producing the final answer. This effectively gives it a "scratchpad" to work in.

### 4. Training data bias
Models are trained on text that includes reasoning (math solutions, code, explanations). CoT elicits this learned behavior.

All four likely contribute. The first (more compute) is supported by the observation that CoT's benefit scales with model size — small models don't benefit (they can't reason well enough even with CoT).

## Limitations

- **Doesn't fix fundamental capability gaps**. If a model can't do arithmetic, CoT won't make it able to.
- **Can amplify errors**. If the first step is wrong, the rest of the chain is built on a false premise.
- **Can be unfaithful**. The model's stated reasoning may not match its actual computation. The model can produce a correct answer with wrong reasoning, or vice versa. See [[14 - Interpretability/Probing/05 - Probing|Probing]] (planned).
- **Token cost**. CoT produces longer outputs, which cost more.

## When CoT Helps Most

- Multi-step arithmetic and math.
- Logical reasoning (syllogisms, conditional reasoning).
- Code understanding and debugging.
- Planning problems.
- Any task where intermediate results would help a human too.

## When CoT Doesn't Help (or Hurts)

- Simple factual recall.
- Single-step tasks.
- Tasks where the model already has strong pattern-matching (no reasoning needed).
- Tasks where the reasoning would be longer than the answer (pure overhead).

## Implementation

```python
def cot_prompt(question, examples=None):
    prompt = ""
    if examples:
        for q, a in examples:
            prompt += f"Q: {q}\nA: {a}\n\n"
    prompt += f"Q: {question}\nA: Let's think step by step. "
    return prompt

# Use
response = llm.chat(cot_prompt(question, examples=cot_examples))
```

For tool use, CoT pairs naturally with [[ReAct Pattern|ReAct]] — the model reasons (Thought), then acts (Action), then observes (Observation), then repeats.

## Modern Evolution: Reasoning Models

In 2024–2025, models like OpenAI o1/o3, DeepSeek-R1, and Claude "extended thinking" are trained specifically to produce long CoT chains. These chains can be thousands of tokens and involve:

- Trying multiple approaches.
- Catching and correcting mistakes mid-chain.
- Backtracking when a path doesn't work.
- Verifying the final answer.

This is "test-time compute scaling" — using more inference-time compute for harder problems. See [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Reasoning]] (planned) and [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]] (planned).

## Why This Matters for AI

- CoT is the **single most impactful prompting technique**. Almost every production LLM feature uses CoT in some form.
- The discovery of CoT (Wei et al. 2022) was a turning point — it showed that prompting alone could unlock new capabilities, leading to the prompting-engineering field.
- Reasoning models (o1, R1) are essentially CoT at training time — they learn to produce CoT chains as part of training, not just from prompting.
- For agents, CoT is the foundation. Every agent reasoning pattern (ReAct, ToT, GoT, reflection) builds on CoT.

## Production Implications

- **Default to CoT for reasoning tasks**. Always prompt with "Let's think step by step." or similar for multi-step problems.
- **Hide CoT from end users** unless they want it. CoT chains are verbose and can confuse non-technical users. Show only the final answer in the UI; log the full chain for debugging.
- **Use self-consistency for high-stakes answers**. Sample 3–5 chains and majority-vote. Cuts error rate substantially.
- **For reasoning models** (o1, R1), don't prompt with CoT — they do it themselves. Just ask the question directly.
- **Cost**: CoT produces more tokens, which costs more. For high-volume low-difficulty tasks, skip CoT.

## Common Pitfalls

- **Forgetting CoT for math/logic** — single biggest prompting mistake. Always CoT for multi-step.
- **CoT for trivial tasks** — wastes tokens. Use CoT only when the task has multiple steps.
- **Trusting CoT as explanation** — CoT is the model's *stated* reasoning, which may not match its actual computation. See "unfaithful CoT" literature.
- **Forcing CoT into a fixed format** — let the model produce natural language reasoning. Strict formats (like "Step 1: ... Step 2: ...") can hurt quality.
- **Not using CoT in agents** — agents without CoT are essentially random. CoT (or ReAct) is the minimum viable reasoning for agents.

## Further Reading

- Wei et al. (2022), *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*.
- Kojima et al. (2022), *Large Language Models are Zero-Shot Reasoners* (zero-shot CoT).
- Wang et al. (2022), *Self-Consistency Improves Chain of Thought Reasoning in Language Models*.
- Turpin et al. (2023), *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting*.

## See Also

- [[ReAct Pattern]]
- [[Reflection]]
- [[15 - AI Agents/MOC|AI Agents MOC]]
- [[Agent vs Workflow vs LLM Application]]


## Interview Questions

1. **Q: Why does CoT work? What are the theories?**
   A: Four theories: (1) more compute per token (more forward passes → better reasoning); (2) decomposition (breaks hard problems into easier sub-problems); (3) attention over intermediate results (model attends to its own reasoning as a "scratchpad"); (4) training data bias (models trained on text with reasoning, CoT elicits this). All four likely contribute. The first is supported by CoT's benefit scaling with model size.

2. **Q: When does CoT NOT help?**
   A: (1) Simple factual recall — no reasoning needed. (2) Single-step tasks — decomposition is unnecessary. (3) Tasks where the model already has strong pattern-matching. (4) Tasks where reasoning is longer than the answer (pure overhead). (5) Small models (<1B) — they can't reason well enough even with CoT. CoT's benefit is an emergent property that appears above ~10B parameters.

3. **Q: What is unfaithful CoT and why does it matter?**
   A: The model's stated reasoning (CoT chain) may not match its actual computation. The model can produce correct answers with wrong reasoning, or wrong answers with plausible reasoning. This matters for: (1) trust — you can't rely on CoT as an explanation; (2) debugging — you can't fix reasoning by fixing the CoT; (3) safety — the model might hide its true reasoning process. See Turpin et al. (2023).

4. **Q: How do reasoning models (o1, R1) differ from CoT prompting?**
   A: CoT prompting: you prompt a standard LLM to "think step by step." The model produces CoT as a response to the prompt. Reasoning models: the model is trained (via RL) to produce long CoT chains internally. The chains can be thousands of tokens, involve trying multiple approaches, catching errors, backtracking. The model learns to reason during training, not just from prompting.

5. **Q: What is self-consistency and when should you use it?**
   A: Sample N CoT chains at temperature > 0, take the majority answer. Works because different chains have independent failure modes — majority voting cancels errors. Cost: N× more LLM calls. Use for high-stakes answers (math, code, factual queries) where accuracy matters more than cost. Typical N=5-10. Not worth it for chat or creative tasks.

6. **Q: How does CoT interact with tool use (ReAct)?**
   A: CoT pairs naturally with ReAct: the model reasons (Thought), then acts (Action), then observes (Observation), then repeats. The CoT is the "Thought" step — it helps the model decide what action to take. Without CoT, agents are essentially random. CoT (or ReAct) is the minimum viable reasoning for agents.

## Connection to Other Concepts

- [[15 - AI Agents/Reasoning/03 - ReAct Pattern|ReAct Pattern]] — CoT + tool use.
- [[15 - AI Agents/Reasoning/06 - Tree of Thoughts and Self Consistency|ToT and Self-Consistency]] — extensions of CoT.
- [[15 - AI Agents/Patterns/05 - Reflection|Reflection]] — CoT + self-critique.
- [[08 - LLMs/Capabilities/04 - In-Context Learning|In-Context Learning]] — few-shot CoT.
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]] — trained CoT.
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Test-Time Compute Scaling]] — CoT as test-time compute.
- [[26 - Papers/Agents and RAG/38 - Self-Consistency 2022|Self-Consistency 2022]] — the paper.
- [[26 - Papers/Agents and RAG/34 - Tree of Thoughts 2023|Tree of Thoughts 2023]] — search over CoT.
- [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Entropy]] — CoT reduces output entropy.
