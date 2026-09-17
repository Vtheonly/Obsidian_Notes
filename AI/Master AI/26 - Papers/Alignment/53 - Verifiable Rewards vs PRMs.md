---
tags: [paper, reasoning, verifiable-rewards, prms, rlhf, alignment, 2025]
iteration: 13
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Verifiable Rewards vs PRMs, RLVR vs PRM, Process vs Outcome Rewards]
---

# 53 — Verifiable Rewards vs Process Reward Models (Comparison Note, 2025)

> [!info] TL;DR
> Two paradigms emerged in 2024–2025 for training reasoning models: **Verifiable Rewards (RLVR)** — reward the model only when its answer is provably correct (math, code tests); and **Process Reward Models (PRMs)** — train a separate model to score each step of the reasoning trace. DeepSeek-R1 (2025) demonstrated that RLVR alone produces frontier reasoning capability, calling into question the need for PRMs. By 2026, the field has largely converged on RLVR for math/code (where verification is cheap) and PRMs for domains where step-level verification is hard (creative writing, open-ended reasoning). This note compares the two approaches, when to use each, and what the open research questions are.

## Citations

**Verifiable Rewards (RLVR)**:
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability via Reinforcement Learning*. arXiv:2501.12948.
- OpenAI (2024). *Learning to Reason with LLMs* (o1 system card / blog post).

**Process Reward Models (PRMs)**:
- Lightman et al. (2023). *Let's Verify Step by Step* (OpenAI, PRM800K paper). arXiv:2305.20050. See [[26 - Papers/Alignment/50 - Process Reward Models 2023]].
- Wang et al. (2024). *Helping or Herding? Reward Model Ensembles in RLHF*.
- SnapshotK et al. (2024). *Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations*.

## The Problem Being Solved

Standard RLHF (InstructGPT-style) uses an **outcome reward model** (ORM): a model trained on human preferences over complete responses. The ORM scores the entire response; the policy is updated via PPO to maximize the ORM's score. This works for chat (where preferences are subjective) but has issues for reasoning:

1. **Sparse signal**: the ORM scores only the final answer, not the reasoning steps. The model can reach the right answer via wrong reasoning (and get rewarded) or reach a wrong answer via correct reasoning (and get penalized).
2. **Reward hacking**: the policy learns to exploit the ORM's biases (longer responses, sycophantic phrasing) rather than improving reasoning quality.
3. **No credit assignment**: when the final answer is wrong, the ORM gives no signal about *which* step failed. The model can't learn from its mistakes efficiently.

PRMs and RLVR are two responses to these issues.

## Approach A: Process Reward Models (PRMs)

### What PRMs Do
A PRM is a separate model trained to score each step of a reasoning trace. For a CoT with K steps, the PRM produces K scores (one per step). During RL, the policy is updated to maximize the sum (or weighted average) of step scores, not just the final answer.

### Training the PRM
- Collect human-annotated step-level labels: "this step is correct / incorrect / neutral".
- OpenAI's PRM800K dataset: 800K step-level labels over 75K math problems.
- Train a separate model (often the base LLM with a regression head) to predict the step label.
- Or use automated labels: Math-Shepherd uses a stronger model (GPT-4) to label steps automatically.

### Inference
At inference, the PRM can be used for **best-of-N sampling**: generate N candidate CoTs, score each step with the PRM, pick the CoT with the highest average step score. This is the inference-time use of PRMs (vs the training-time use of RL with PRM rewards).

### Strengths
- **Dense signal**: every step gets a reward, not just the final answer. Faster, more stable RL training.
- **Credit assignment**: when the final answer is wrong, the PRM tells you which step failed.
- **Works for any domain**: PRMs can be trained on any reasoning trace, not just verifiable ones.

### Weaknesses
- **Expensive to train**: requires step-level labels (either human-annotated, which is costly, or auto-labeled by a stronger model, which can be wrong).
- **PRM hacking**: the policy learns to exploit the PRM's biases (longer steps, certain phrasings the PRM scores highly).
- **PRM quality ceiling**: the PRM is only as good as its labels. If labels are wrong, the PRM teaches the policy wrong things.
- **Two-model system**: PRM + policy is more complex to serve and update than a single model.

## Approach B: Verifiable Rewards (RLVR)

### What RLVR Does
RLVR (Reinforcement Learning with Verifiable Rewards) doesn't use a separate reward model at all. The reward is computed by an external verifier that checks whether the final answer is correct:

- **Math**: parse the final answer, check if it matches the ground truth.
- **Code**: run the code against test cases, check if it passes.
- **Formal logic**: check the proof with a theorem prover.

The reward is binary (1 if correct, 0 if wrong) or scaled (partial credit for partially correct answers). No step-level scoring.

### Training
- Generate a CoT, parse the final answer, compute the reward via the verifier.
- Update the policy via PPO or GRPO (DeepSeek-R1 uses GRPO) to maximize the verifier's reward.
- No separate PRM; the verifier is rule-based (math grader, test runner, theorem prover).

### Inference
At inference, no PRM is needed — the model just generates a CoT and a final answer. The verifier can be used for best-of-N sampling (pick the CoT whose final answer is correct), but this is less common than with PRMs.

### Strengths
- **No reward model to train**: the verifier is rule-based, so there's no separate model to label, train, or update.
- **No reward hacking**: the verifier is rule-based, so the policy can't exploit it (only by actually being correct).
- **Cheap**: only need problem-answer pairs, not step-level labels.
- **Strong results**: DeepSeek-R1 (RLVR alone) matches o1 (RLVR + PRM) on most reasoning benchmarks.

### Weaknesses
- **Requires verifiable answers**: only works for math, code, formal logic. Not directly applicable to creative writing, open-ended reasoning, or subjective tasks.
- **Sparse signal**: only the final answer gets a reward. Credit assignment is harder.
- **Long training time**: with sparse rewards, RL takes longer to converge than with dense PRM rewards.
- **No step-level debugging**: when the model fails, you don't know which step failed.

## Key Results

### DeepSeek-R1 (2025, RLVR alone)
- Matches or beats o1 on AIME 2024, MATH-500, GPQA, LiveCodeBench.
- R1-Zero: pure RL on verifiable rewards (no SFT first) — produces emergent CoT.
- R1: SFT on cold-start data, then RL — better readability, similar reasoning quality.

### o1 (2024, RLVR + PRM)
- OpenAI disclosed high-level approach: RL on verifiable rewards + PRM800K step-level data.
- Specifics of how PRM is used in training are not disclosed.

### Math-Shepherd (2024, PRM alone)
- Auto-labeled step-level data using GPT-4.
- Shows PRM-based best-of-N sampling improves math accuracy.
- But the PRM-trained policy doesn't match RLVR-trained policy on the same benchmarks.

## When to Use Each

| Use Case                                | Recommended Approach                 |
|-----------------------------------------|---------------------------------------|
| Math (algebra, calculus, competition)   | RLVR (verifiable)                     |
| Code generation (with test cases)      | RLVR (verifiable)                     |
| Formal logic / theorem proving         | RLVR (verifiable)                     |
| Scientific reasoning (with known answers)| RLVR (verifiable)                   |
| Creative writing                        | PRM or ORM (no clean verifier)       |
| Open-ended reasoning (no ground truth)  | PRM or ORM                            |
| Multi-step planning                     | PRM (credit assignment matters)       |
| Conversational alignment                | ORM (RLHF, classic InstructGPT)       |

### Hybrid Approaches
- **RLVR + PRM** (o1-style): use RLVR as the main reward, PRM as a dense auxiliary reward for credit assignment. Most reasoning models in 2026 use this hybrid.
- **RLVR + ORM** (R1-style): use RLVR as the main reward, ORM as auxiliary reward for non-verifiable dimensions (helpfulness, format). DeepSeek-R1 uses this.
- **PRM + ORM**: use PRM for reasoning steps, ORM for overall quality. Used for general chat models that also do reasoning.

## Why This Comparison Matters

### The R1-Zero Surprise
DeepSeek-R1-Zero demonstrated that pure RL on verifiable rewards (no SFT, no PRM) produces emergent chain-of-thought capability. Before R1-Zero, the field assumed PRMs were necessary for reasoning RL. R1-Zero showed that the verifier alone provides enough signal for the model to develop reasoning.

This is a major architectural simplification: training a reasoning model doesn't require collecting step-level labels or training a separate PRM. It just requires a verifier (math grader, test runner) and a lot of compute.

### The Cost Question
- **PRM cost**: collecting 800K step-level labels (PRM800K) costs ~$1M+ in human annotation. Auto-labeling (Math-Shepherd) costs less but introduces label noise.
- **RLVR cost**: free — the verifier is rule-based. Just need problem-answer pairs (which exist in abundance for math, code, formal logic).

For labs without PRM-scale annotation budgets, RLVR is the only viable path to reasoning models. This explains why most open-source reasoning models (DeepSeek-R1, Qwen3-Thinking, Kimi K1.5) use RLVR alone or RLVR + ORM.

### The Domain Question
RLVR works only where answers are verifiable. For domains without verifiers (creative writing, open-ended reasoning, conversational alignment), PRMs remain valuable. The 2026 frontier models likely use:
- RLVR for math/code/scientific reasoning.
- PRM or ORM for chat alignment and creative tasks.
- Hybrid (RLVR + PRM) for reasoning + chat.

## Limitations and Open Questions

### For PRMs
- **PRM hacking**: policies exploit PRM biases. Mitigation: ensemble PRMs, regularize, or use PRM only for best-of-N (not for RL).
- **Label noise**: auto-labeled PRMs are noisy. Mitigation: active learning, label-quality filtering.
- **PRM drift**: as the policy improves, the PRM (trained on older data) becomes stale. Mitigation: periodic PRM retraining.

### For RLVR
- **Domain restriction**: only works for verifiable domains. Extending to non-verifiable domains is an open problem.
- **Sparse signal**: slower RL convergence than PRMs. Mitigation: GRPO (group-relative advantages) provides denser signal than vanilla PPO.
- **No step-level debugging**: when the model fails, you don't know which step failed. Mitigation: combine with PRM for evaluation (not training).

### Open Research Questions
- Can RLVR be extended to non-verifiable domains via "soft verifiers" (LLM-as-judge for non-math)?
- Is there a theoretical limit to reasoning capability from RLVR alone, or does it scale indefinitely with compute?
- How do RLVR and PRMs interact in hybrid training? Does the PRM help or hurt when combined with a strong verifier?
- For very long CoT (10K+ tokens), does PRM's dense signal become essential, or does RLVR's sparse signal suffice?

## Comparison Table

| Aspect                       | RLVR (Verifiable Rewards)         | PRM (Process Reward Model)         |
|------------------------------|------------------------------------|------------------------------------|
| Reward source                | Rule-based verifier                | Trained neural model               |
| Signal density               | Sparse (final answer only)         | Dense (per-step)                   |
| Domains                      | Math, code, formal logic            | Any (including non-verifiable)     |
| Annotation cost              | Free (verifier is rule-based)      | High (human labels) or moderate (auto-labels) |
| Reward hacking risk          | Low (verifier is rule-based)       | High (PRM has biases)              |
| Training stability           | Slower convergence (sparse signal) | Faster convergence (dense signal)  |
| Credit assignment            | None (only final answer scored)    | Yes (per-step scores)              |
| Inference-time use           | Best-of-N with verifier             | Best-of-N with PRM                 |
| Examples                     | DeepSeek-R1, Qwen3-Thinking        | OpenAI o1 (rumored), Math-Shepherd |
| Production maturity (2026)    | Standard for math/code reasoning   | Used for hybrid RLVR+PRM training  |

## Connection to Other Concepts

- [[26 - Papers/Alignment/50 - Process Reward Models 2023]] — the PRM800K paper.
- [[26 - Papers/2024-2026/12 - DeepSeek-R1 2025]] — R1's RLVR recipe.
- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO]] — classic RLHF (outcome reward).
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models]] — reasoning model category.
- [[27 - Projects/Capstones/07 - Build a Reasoning Model Fine-Tune]] — practical implementation.
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling]] — test-time compute context.
- [[26 - Papers/MOC]] — papers index.

## Reception and Follow-Ups

The R1-Zero result (RLVR alone produces emergent CoT) was a paradigm shift:

- **Before R1 (2024)**: PRMs were considered essential for reasoning RL. OpenAI's o1 used PRM800K. Math-Shepherd used auto-labeled PRMs. The field assumed PRMs were the path.
- **After R1 (Jan 2025)**: PRMs became optional. Most open-source reasoning models (Qwen3-Thinking, Kimi K1.5, GLM-Z1) use RLVR alone. Closed-source models (o1, Claude thinking, Gemini 2.0 thinking) likely use hybrid RLVR+PRM but haven't disclosed details.
- **2026 frontier**: the field has converged on RLVR as the default for verifiable domains, with PRMs used for non-verifiable alignment. The hybrid (RLVR + PRM) is the most powerful but most complex.

## Interview Questions

1. **Q: When would you use a PRM vs RLVR?**
   A: Use **RLVR** when the answer is verifiable — math (you can check the answer), code (you can run tests), formal logic (you can check the proof). RLVR is free (no reward model to train), robust (no reward hacking), and works well (DeepSeek-R1 matches o1). Use **PRM** when the answer is NOT verifiable — creative writing, open-ended reasoning, subjective tasks. PRMs give dense per-step signal but require labeled data and are susceptible to reward hacking. For most production reasoning models (math/code), RLVR is the default. For chat alignment (non-verifiable), PRMs or ORMs remain valuable.

2. **Q: Why was R1-Zero surprising?**
   A: Before R1-Zero, the field assumed PRMs were necessary for reasoning RL — the dense per-step signal was thought essential for stable training. R1-Zero (pure RL on verifiable rewards, no SFT, no PRM) produced emergent chain-of-thought capability. This showed that the verifier alone provides enough signal: the model learns to reason because correct reasoning correlates with correct answers, and the verifier rewards correct answers. The implication: training a reasoning model doesn't require collecting step-level labels or training a separate PRM. Just need a verifier and a lot of compute.

3. **Q: What's the reward hacking risk for PRMs vs RLVR?**
   A: **PRMs** are highly susceptible to reward hacking because they're neural models with biases (longer steps, certain phrasings, certain vocabulary). The policy can exploit these biases to increase the PRM score without actually improving reasoning. Mitigation: ensemble PRMs, regularize, use PRM only for best-of-N (not RL). **RLVR** is largely immune to reward hacking because the verifier is rule-based — the policy can't exploit a math grader or test runner; it can only actually be correct. This is a major reason R1's results are robust.

## See Also

- [[26 - Papers/MOC|Papers MOC]]
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]]
