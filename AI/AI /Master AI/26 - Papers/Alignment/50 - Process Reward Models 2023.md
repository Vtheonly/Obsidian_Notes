---
tags: [paper, process-reward-model, prm, reasoning, math]
iteration: 12
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Process Reward Models, PRM, PRM800K, OpenAI PRM, Let's Verify Step by Step]
---

# 50 — Process Reward Models: Let's Verify Step by Step (Lightman et al., 2023)

> [!info] TL;DR
> Lightman et al. (OpenAI, 2023) introduced **Process Reward Models (PRMs)** — reward models that score each *step* of a reasoning chain rather than just the final answer. PRMs dramatically outperform Outcome Reward Models (ORMs) on math reasoning because they provide denser training signal and can identify exactly where a solution went wrong. The paper shipped with **PRM800K**, a 800k-step human-annotated dataset that became the standard for PRM training. PRMs underpin modern reasoning models (o1, DeepSeek-R1).

## Citation

Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike, J., Schulman, J., Sutskever, I., Cobbe, K. (OpenAI). (2023). *Let's Verify Step by Step*. arXiv:2305.20050.

## The Problem Being Solved

Standard Reinforcement Learning from Human Feedback (RLHF) uses an **Outcome Reward Model (ORM)**: the reward is a single scalar for the entire response. For math reasoning, this has problems:

1. **Sparse signal**: a 10-step math solution gets one reward. If the answer is wrong, which step was the bug?
2. **Credit assignment**: the ORM can't tell whether step 2 or step 8 caused the wrong answer.
3. **Reward hacking**: the model learns to produce plausible-looking steps that lead to the right answer by luck (or wrong steps that happen to produce right answers).
4. **Hard to debug**: when an RL-trained model fails, you can't trace the failure to a specific step.

The paper's question: **what if we had a reward for each step, not just the final answer?** A Process Reward Model (PRM) scores each step independently, providing dense, localized signal.

## The Approach: Process Reward Models

### Step-Level Annotation
The authors collected **PRM800K** — 800,000 human-annotated reasoning steps across 75,000 math problems. Annotators labeled each step as:
- **Good**: step is correct and useful.
- **Bad**: step is incorrect or unhelpful.
- **Neutral**: step is correct but unnecessary (e.g., redundant).

### PRM Architecture
The PRM is a transformer that takes the problem + solution-so-far + current-step and outputs a single scalar: P(step is good | problem, solution-so-far). Trained on PRM800K with cross-entropy loss.

### Inference: Best-of-N Selection
At inference, generate N candidate solutions (e.g., N=64). Score each solution by **min over steps** (the worst step determines the score — a chain is only as strong as its weakest link) or by **product over steps**. Pick the highest-scoring solution.

This Best-of-N + PRM approach beats both Best-of-N + ORM and standard RLHF on math benchmarks.

## Key Results

- **GSM8K (grade-school math)**: PRM Best-of-N (N=64) achieves 78% accuracy vs 70% for ORM Best-of-N. A 8-point improvement from better reward signal.
- **MATH (competition math)**: PRM Best-of-N achieves 33% vs 27% for ORM.
- **PRM vs ORM at scale**: PRMs scale better with more annotation — each step-level label provides more signal than a single outcome label.

### What Made PRMs Win
- **Dense supervision**: 800k step labels vs ~75k outcome labels — 10x more supervision signal.
- **Localized error detection**: PRM identifies the exact step where a solution fails.
- **Step-level reward shaping**: when used in RL, the per-step reward provides gradient signal that helps the model learn each step correctly, not just the final answer.

## Why This Paper Matters

### Foundation for Reasoning Models
PRMs are a key ingredient in modern reasoning models:
- **OpenAI o1 (2024)**: uses PRMs (or PRM-like reward shaping) for test-time search.
- **DeepSeek-R1 (2025)**: uses verifiable rewards (a generalized PRM where the "step verifier" is a deterministic checker, not a learned model) for RL training.
- **Anthropic Claude thinking (2024)**: uses step-level rewards for thinking supervision.

### Test-Time Search Becomes Practical
PRMs enable test-time best-of-N search: generate many candidate solutions, score each, pick the best. This is a form of **test-time compute scaling** — spend more compute at inference for better results. o1 takes this to the extreme with tree search + PRM.

### Shifted RLHF from Outcomes to Processes
The paper shifted the RLHF literature from outcome-based to process-based rewards. Subsequent work (RLAIF, Constitutional AI, DPO variants) increasingly considers step-level signals.

### Open Dataset (PRM800K)
The PRM800K dataset is open. Researchers can train their own PRMs without the expensive annotation. This democratized PRM research and enabled many follow-up papers (Math-Shepherd, Skywork-PRM, Qwen-Math-PRM).

## Limitations

- **Annotation cost**: 800k human step labels cost ~$1M+ at OpenAI's annotation rates. Hard to replicate without significant budget.
- **Domain restriction**: PRM800K is math-only. PRMs for code, science, and general reasoning are still maturing.
- **PRM != verifier**: a learned PRM can be wrong; it's not a ground-truth verifier. Adversarial solutions can fool the PRM (e.g., plausible-looking steps that are actually wrong).
- **Verifiable rewards are better when possible**: for domains where step correctness can be checked deterministically (code execution, math proof verification), verifiable rewards >> learned PRMs. DeepSeek-R1 uses this approach.

## Variants and Extensions

### Math-Shepherd (2024)
Automatic PRM training data generation: use a stronger model to label steps as good/bad. Eliminates the need for human annotation. Quality is lower but scales better.

### Skywork-PRM (2024)
Open-source PRM trained on a mix of human and synthetic data. Comparable quality to OpenAI's PRM but fully reproducible.

### Process-supervised DPO (2024)
Extends DPO to step-level preferences. Instead of preferring one full response over another, prefer one step over another. Combines PRM-style supervision with DPO's simplicity.

### Verifiable Rewards (DeepSeek-R1, 2025)
Replace the learned PRM with a deterministic verifier (e.g., for math, check the final answer; for code, run tests). Eliminates PRM training entirely and is immune to reward hacking. The current (2025–2026) state of the art for math/code reasoning.

## Comparison With Related Approaches

| Method                       | Reward Granularity | Annotation Cost | Quality on MATH | Notes                                  |
|------------------------------|---------------------|-----------------|-----------------|----------------------------------------|
| ORM (outcome RM)             | 1 per response      | Low             | 27% (Best-of-64) | Sparse signal; reward hacking         |
| PRM (Lightman 2023)          | 1 per step          | High (~$1M)     | 33% (Best-of-64) | Dense signal; requires PRM800K-style data |
| Math-Shepherd PRM (2024)     | 1 per step          | Low (automatic) | 31%             | Synthetic labels; slightly lower quality |
| Verifiable Rewards (R1 2025) | 1 per response      | None (deterministic) | 35%+ | Best for math/code; immune to hacking |

## Connection to Other Concepts

- [[26 - Papers/2024-2026/12 - DeepSeek-R1 2025]] — uses verifiable rewards, a PRM generalization.
- [[26 - Papers/Alignment/07 - InstructGPT 2022]] — outcome-based RLHF that PRMs improve upon.
- [[26 - Papers/Alignment/09 - DPO 2023]] — direct preference optimization; can be extended to step-level.
- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO]] — the RL framework PRMs plug into.
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling]] — PRMs enable test-time search.
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models]] — reasoning models use PRMs.
- [[15 - AI Agents/Reasoning/02 - Chain-of-Thought]] — PRMs score CoT steps.
- [[15 - AI Agents/Reasoning/06 - Tree of Thoughts and Self Consistency]] — PRMs guide tree search.
- [[26 - Papers/MOC]] — papers index.

## Reception and Follow-Ups

Process Reward Models (PRMs) became foundational for the 2024–2025 reasoning model wave:
- **OpenAI o1 (2024)**: uses PRMs (or PRM-like reward shaping) for test-time search during reasoning.
- **DeepSeek-R1 (2025)**: uses **verifiable rewards** — a generalization where the "PRM" is a deterministic checker (math verifier, code executor), not a learned model. Eliminates reward hacking.
- **Open-source PRMs**: Math-Shepherd (2024), Skywork-PRM (2024), Qwen-Math-PRM (2024) — all open-weights, trained on synthetic or partially-human-labeled data.
- **Process-supervised DPO** (2024): extends DPO to step-level preferences.
- **PRM800K dataset**: became the standard for PRM training; ~800k human-annotated steps.

By 2025, the trend shifted from learned PRMs to verifiable rewards (for math/code) and LLM-as-judge rewards (for open-ended tasks). PRMs remain influential but are no longer the state-of-the-art for verifiable domains.

## Limitations and Open Questions

- **Annotation cost**: 800k human step labels cost ~$1M+ at OpenAI's annotation rates. Hard to replicate without significant budget.
- **Domain restriction**: PRM800K is math-only. PRMs for code, science, and general reasoning are still maturing.
- **PRM != verifier**: a learned PRM can be wrong; it's not a ground-truth verifier. Adversarial solutions can fool the PRM (e.g., plausible-looking steps that are actually wrong).
- **Verifiable rewards are better when possible**: for domains where step correctness can be checked deterministically (code execution, math proof verification), verifiable rewards >> learned PRMs. DeepSeek-R1 uses this approach.
- **Reward hacking**: learned PRMs can be hacked — the model learns to produce steps that look good to the PRM but are actually wrong. Verifiable rewards eliminate this.
- **Open question**: can PRMs be made adversarially robust? Current approaches (ensemble PRMs, adversarial training) help but don't fully solve.
- **Open question**: what's the optimal granularity for step-level rewards? Per-token? Per-sentence? Per-reasoning-step? PRM800K uses per-step (human-defined), but automatic step segmentation is an open problem.

## Interview Questions

1. **Q: What's the key difference between a PRM and an ORM?**
   A: An **ORM (Outcome Reward Model)** scores the entire response with one scalar — sparse signal, hard to debug. A **PRM (Process Reward Model)** scores each reasoning step independently — dense signal, localized error detection. For a 10-step math solution, the ORM gives 1 reward; the PRM gives 10. The PRM can identify exactly which step went wrong; the ORM cannot. This denser signal makes PRMs dramatically better for math reasoning (Lightman 2023 showed 8-point improvement on GSM8K).

2. **Q: Why have verifiable rewards (DeepSeek-R1) largely replaced learned PRMs?**
   A: Three reasons. (1) **No reward hacking**: a deterministic math checker can't be tricked; a learned PRM can be fooled by plausible-looking but wrong reasoning. (2) **No annotation cost**: verifiers are code, not human-labeled data. (3) **Perfect calibration**: verifier reward = ground truth quality; PRM rewards are noisy. Learned PRMs are still useful for non-verifiable domains (writing, helpfulness) but for math/code, verifiable rewards win. DeepSeek-R1 (2025) demonstrated this conclusively.

3. **Q: How are PRMs used at inference time (not just training)?**
   A: PRMs enable **test-time search**: generate N candidate solutions, score each with the PRM, pick the highest-scoring. This is "Best-of-N with PRM" — a form of test-time compute scaling. OpenAI o1 takes this further with tree search + PRM, exploring reasoning branches and pruning low-PRM-score paths. The PRM acts as a search heuristic, guiding the model toward correct reasoning. This is why o1 can solve problems the base model can't — it's not just generating; it's searching with PRM guidance.
