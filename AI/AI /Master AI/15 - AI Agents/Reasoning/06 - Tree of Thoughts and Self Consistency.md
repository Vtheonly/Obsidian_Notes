---
tags: [agents, reasoning, tot, got, self-consistency]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Tree of Thoughts, Graph of Thoughts, Self-Consistency]
---

# 06 - Tree-of-Thoughts, Graph-of-Thoughts, Self-Consistency

> [!info] TL;DR
> Advanced reasoning patterns beyond CoT and ReAct. **Self-consistency**: sample multiple CoTs, majority-vote. **Tree-of-Thoughts (ToT)**: explore multiple reasoning branches, evaluate, prune. **Graph-of-Thoughts (GoT)**: arbitrary graph of reasoning steps. Higher quality, much higher cost.

## Self-Consistency (Wang et al. 2022)

The simplest enhancement to CoT:

1. Sample $N$ CoT chains at temperature > 0 (e.g., $N=5$).
2. Extract the final answer from each.
3. Take the majority answer.

```python
chains = [llm.generate(prompt, temperature=0.7) for _ in range(5)]
answers = [extract_answer(c) for c in chains]
final = Counter(answers).most_common(1)[0][0]
```

**Why it works**: different reasoning chains have independent failure modes. Majority voting cancels out errors.

**Cost**: $N$x the LLM calls. Worth it for high-stakes answers (math, code, factual queries).

**Quality gain**: typically 5–15% absolute improvement on math/reasoning benchmarks.

## Tree-of-Thoughts (Yao et al. 2023)

CoT is a linear chain: $A \to B \to C \to \text{answer}$. ToT explores a tree:

```
              [Problem]
            /     |     \
        [A1]   [A2]   [A3]      ← generate multiple first steps
        / \    /  \    / \
      [B1][B2][B3][B4][B5][B6]  ← for each, generate multiple next steps
      ...                       ← evaluate and prune; expand promising branches
```

### The algorithm
1. **Thought generation**: at each step, generate $k$ candidate next thoughts.
2. **Evaluation**: have the LLM (or a heuristic) score each candidate.
3. **Search**: BFS or DFS over the tree, expanding high-scoring branches and pruning low-scoring ones.

### When ToT helps
- Problems with multiple intermediate steps where backtracking is useful.
- Problems where partial progress can be evaluated (puzzles, math, planning).

### When ToT is overkill
- Most chatbot use cases.
- Problems where CoT already works well.
- Cost-sensitive applications (ToT can be 10–100x CoT cost).

## Graph-of-Thoughts (Besta et al. 2023)

Generalizes ToT to arbitrary graphs:

```
              [Start]
            /         \
        [A]            [B]
        | \          / |
        |  [C]------   |
        | /            |
        [D]            [E]
         \            /
          [Combine]
              |
           [Answer]
```

Different reasoning paths can **merge** (e.g., combine insights from two branches). More flexible than ToT but more complex to implement.

## Other Variants

### Self-Refine (Madaan et al. 2023)
The model generates an answer, then critiques and refines it iteratively:
```
answer → critique → refined answer → critique → refined answer → ...
```
See [[05 - Reflection]].

### Plan-and-Solve
Decompose a problem into sub-problems, solve each. Variant of CoT with explicit planning step.

### Reasoning via Planning (RAP)
Use an MDP framework: states = reasoning steps, actions = next-step proposals, rewards = LLM-evaluated progress. Combine LLMs with classical planning (Monte Carlo Tree Search).

## Worked Example (Self-Consistency)

```python
def self_consistent_answer(question, n=5):
    prompt = f"Q: {question}\nA: Let's think step by step. "
    chains = [llm.generate(prompt, temperature=0.7, max_tokens=500) for _ in range(n)]
    
    # Extract final numeric answers (assuming math question)
    answers = []
    for chain in chains:
        match = re.search(r'answer is (\d+)', chain)
        if match:
            answers.append(int(match.group(1)))
    
    if not answers:
        return None
    return Counter(answers).most_common(1)[0][0]
```

## Why This Matters for AI

- These techniques extend LLM reasoning beyond single-shot CoT. For hard problems, they can dramatically improve quality.
- **Self-consistency is the most practical** — easy to implement, robust improvement, modest cost increase.
- ToT and GoT are research-grade; mostly relevant for benchmark chasing and specialized reasoning tasks.
- For agents, these patterns are sometimes combined with tool use — e.g., an agent that explores multiple plans before acting.

## Production Implications

- **For high-stakes Q&A** (math, code, factual), use self-consistency with $n=3$–5. The cost is worth the accuracy gain.
- **For agents**, consider ToT-style planning for hard multi-step tasks. Cost can be 10x+, so use selectively.
- **Latency matters** — self-consistency adds latency (parallel sampling helps). ToT adds even more.
- **For chat**, these techniques are usually overkill. A single CoT response is fine.

## Common Pitfalls

- **Using ToT where CoT suffices** — 10x cost for marginal gain.
- **Forgetting self-consistency for math/factual** — easy win, often missed.
- **Wrong temperature for self-consistency** — temperature 0 gives identical chains (no diversity). Use 0.7+.
- **Bad evaluation function in ToT** — if the LLM can't reliably evaluate intermediate steps, ToT doesn't help.

## Further Reading

- Wang et al. (2022), *Self-Consistency Improves Chain of Thought Reasoning*.
- Yao et al. (2023), *Tree of Thoughts: Deliberate Problem Solving with Large Language Models*.
- Besta et al. (2023), *Graph of Thoughts: Solving Elaborate Problems with Large Language Models*.
- Madaan et al. (2023), *Self-Refine*.

## See Also

- [[02 - Chain-of-Thought]]
- [[03 - ReAct Pattern]]
- [[05 - Reflection]]
- [[15 - AI Agents/MOC|AI Agents MOC]]


## Interview Questions

1. **Q: What is self-consistency and why does it work?**
   A: Sample N CoT chains at temperature > 0, take the majority answer. Works because different chains have independent failure modes — majority voting cancels errors. The right answer is unique (for closed-answer tasks) but there are many paths to it; wrong answers are scattered. Cost: N× more LLM calls. Typical: N=5-10. Quality gain: 5-15% absolute on math/reasoning benchmarks.

2. **Q: How does ToT differ from CoT?**
   A: CoT explores a single reasoning path: A → B → C → answer. ToT explores a tree: at each step, generate k candidate thoughts, evaluate each, expand high-scoring branches and prune low-scoring ones. This allows backtracking — if a branch looks bad, the search explores alternatives. ToT is 10-100x more expensive than CoT but can solve problems CoT can't (planning, puzzles, crosswords).

3. **Q: When is ToT overkill?**
   A: (1) Most chatbot use cases — CoT is sufficient. (2) Problems where CoT already works well — ToT adds cost without benefit. (3) Cost-sensitive applications — ToT can be 10-100x CoT cost. (4) Tasks where the right next step is obvious — no need to explore alternatives. ToT is for hard multi-step problems where backtracking matters.

4. **Q: What is Graph-of-Thoughts and how does it generalize ToT?**
   A: GoT allows arbitrary graph structures (not just trees): branches can merge (combine insights from two paths), have cycles (refinement loops), and share sub-results. This is more expressive than ToT (which is strictly tree-structured). GoT achieves SOTA on sorting, set intersection, and keyword counting. Cost: 10-1000x CoT. See [[26 - Papers/Agents and RAG/39 - Graph of Thoughts 2023|Graph of Thoughts 2023]].

5. **Q: How do you choose between CoT, self-consistency, ToT, and GoT?**
   A: CoT: default for most tasks (cheap, effective). Self-consistency: high-stakes closed-answer tasks (math, code) — N=5-10, majority vote. ToT: planning/puzzles where backtracking matters — 10-100x cost. GoT: tasks with natural merge structure (sorting, set operations) — 10-1000x cost. Start with CoT; add self-consistency if stakes are high; add ToT/GoT only for specialized tasks.

6. **Q: What is Self-Refine and how does it differ from reflection?**
   A: Self-Refine: the model generates an answer, critiques it, refines it, repeats: answer → critique → refined → critique → refined → ... It's a linear refinement loop, not a tree search. Reflection (Reflexion): the agent attempts a task, evaluates, reflects on what went wrong, and retries with the reflection in context. Self-Refine is about improving a single output; Reflection is about improving across attempts.

## Connection to Other Concepts

- [[15 - AI Agents/Reasoning/02 - Chain-of-Thought|Chain-of-Thought]] — the foundation.
- [[15 - AI Agents/Reasoning/03 - ReAct Pattern|ReAct Pattern]] — reasoning + action.
- [[15 - AI Agents/Patterns/05 - Reflection|Reflection]] — self-critique pattern.
- [[08 - LLMs/Sampling/03 - Sampling Strategies|Sampling Strategies]] — self-consistency needs temperature > 0.
- [[26 - Papers/Agents and RAG/38 - Self-Consistency 2022|Self-Consistency 2022]] — the paper.
- [[26 - Papers/Agents and RAG/34 - Tree of Thoughts 2023|Tree of Thoughts 2023]] — the paper.
- [[26 - Papers/Agents and RAG/39 - Graph of Thoughts 2023|Graph of Thoughts 2023]] — the paper.
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Test-Time Compute Scaling]] — these patterns are forms of test-time compute.
