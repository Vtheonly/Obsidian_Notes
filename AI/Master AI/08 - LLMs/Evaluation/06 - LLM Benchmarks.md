---
tags: [llms, evaluation, benchmarks, mmlu, gpqa, humaneval]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
aliases: [LLM Benchmarks, MMLU, GPQA, HumanEval, MATH]
---

# 06 - LLM Benchmarks (MMLU, GPQA, HumanEval, MATH, BBH)

> [!info] TL;DR
> LLM benchmarks are standardized tests for measuring model capabilities. MMLU (general knowledge), GPQA (graduate-level Q&A), HumanEval (code), MATH (math), BBH (reasoning) are the core 2024–2026 set. Contamination is a major concern — models can memorize benchmarks during training.

## Why Benchmarks Matter

LLMs are general-purpose — hard to evaluate. Benchmarks provide:
- **Comparable scores** across models.
- **Capability tracking** over time.
- **Regression testing** for new model versions.

But benchmarks have known issues (see "Limitations" below) — they're a useful signal, not ground truth.

## The Core 2026 Benchmark Set

### MMLU (Massive Multitask Language Understanding)
- 57 subjects (STEM, humanities, professional).
- Multiple-choice questions.
- Tests broad knowledge.
- Standard for "is this model smart?"
- **MMLU-Pro**: harder version, 10 options instead of 4.

### GPQA (Google-Proof Q&A)
- PhD-level questions in biology, chemistry, physics.
- "Google-proof": hard even with web search.
- Tests deep reasoning and expertise.
- Frontier model benchmark.

### HumanEval
- 164 hand-written Python programming problems.
- Function signature + docstring → implement.
- Pass@1: does the model get it right on the first try?
- Standard for coding ability.
- **HumanEval+ / MBPP**: extended versions with more tests.

### MATH / GSM8K
- **GSM8K**: grade-school math word problems (~8k problems).
- **MATH**: competition-level math problems.
- Tests mathematical reasoning.
- Frontier models now hit ~90%+ on GSM8K; MATH is still hard.

### BBH (BIG-Bench Hard)
- 23 difficult tasks from the BIG-Bench suite.
- Tests reasoning, common sense, multi-step.
- Standard for "reasoning ability."

### IFEval (Instruction Following Evaluation)
- Tests whether the model follows explicit instructions (e.g., "respond in JSON", "use at most 3 sentences").
- Surprisingly hard for many models.
- Important for production use.

### MT-Bench / AlpacaEval
- Multi-turn conversation benchmarks.
- Judged by GPT-4 (LLM-as-judge).
- Tests chat quality, not just knowledge.

### Chatbot Arena (LMSYS)
- Humans compare two anonymous models side-by-side.
- Elo rating.
- The most trusted "vibe check" for chat quality.
- Real human preferences, not synthetic.

## Specialized Benchmarks

| Domain        | Benchmarks                                    |
|---------------|-----------------------------------------------|
| Code          | HumanEval, MBPP, LiveCodeBench, BigCodeBench  |
| Math          | MATH, GSM8K, AIME                             |
| Reasoning     | BBH, ARC, HellaSwag, Winogrande               |
| Long context  | Needle in a Haystack, RULER, LongBench        |
| Multilingual  | MGSM, multilingual MMLU                       |
| Tool use      | ToolBench, API-Bank, BFCL                     |
| Agents        | AgentBench, WebArena, SWE-Bench               |
| Safety        | TruthfulQA, ToxiGen, AdvBench                 |
| Alignment     | HH-RLHF, MT-Bench, AlpacaEval                 |

## How to Run Benchmarks

### Use `lm-evaluation-harness`
The standard open framework:

```bash
pip install lm-eval
lm_eval --model hf --model_args pretrained=meta-llama/Meta-Llama-3-8B-Instruct \
        --tasks mmlu,gsm8k,humaneval \
        --batch_size auto
```

### Use `lighteval`
HuggingFace's alternative, with good integration for their model hub.

### Vendor-specific
OpenAI, Anthropic, Google all publish their own benchmark numbers — be skeptical, as methodology varies.

## Limitations and Pitfalls

### 1. Contamination
If a benchmark is in the training data, models can memorize it. Their score reflects memorization, not capability.

- MMLU has been heavily contaminated in many models.
- Newer benchmarks (GPQA, MMLU-Pro) try to avoid this with private test sets or recent questions.
- Always check if the model card reports decontaminated scores.

### 2. Multiple-choice bias
Multiple-choice questions are easier than open-ended — the answer is in front of the model. Real-world tasks are open-ended.

### 3. Benchmark gaming
Models can be fine-tuned on benchmark-style questions, inflating scores without real capability gain.

### 4. LLM-as-judge bias
LLM judges (used in MT-Bench, AlpacaEval) have biases:
- Prefer longer responses.
- Prefer their own style.
- Position bias (first response wins more often).

### 5. Stale benchmarks
Once a benchmark is "solved" (most models hit 95%+), it stops being informative. MMLU is approaching this.

### 6. Real-world gap
Benchmark performance doesn't always translate to production. A model that scores well on HumanEval may still write bad code in your specific codebase.

## Worked Example (Running MMLU)

```bash
# Install
pip install lm-eval

# Evaluate a model on MMLU
lm_eval --model hf --model_args pretrained=meta-llama/Meta-Llama-3-8B-Instruct,trust_remote_code=True \
        --tasks mmlu --num_fewshot 5 --batch_size auto
```

Output: per-subject scores + overall average.

## Why This Matters for AI

- Benchmarks are **how we measure progress**. Without them, we couldn't tell if a new model is actually better.
- For **model selection**, benchmarks are the starting point. But always validate on your own task.
- For **research**, benchmarks are the metric. New techniques are validated by benchmark improvements.
- **Chatbot Arena** has emerged as the most trusted signal for chat quality — real human preferences beat synthetic benchmarks.

## Production Implications

- **Don't select models solely on benchmarks.** Run your own eval on your specific task.
- **For internal eval**, build a "golden set" of 50–200 examples representative of your production traffic. Use it for model selection and regression testing.
- **Track benchmark scores over time** — sudden improvements on a benchmark with no architectural change suggest contamination.
- **For high-stakes features**, combine benchmarks with human evaluation. LLM-as-judge is good for cheap iteration; humans for final validation.
- **Watch the SOTA** — capabilities are moving fast. A model that's SOTA today is mediocre in 6 months.

## Common Pitfalls

- **Comparing benchmarks across methodology** — few-shot vs zero-shot, different prompts, different eval frameworks. Numbers aren't comparable.
- **Trusting vendor-reported numbers** — always look for independent verification.
- **Forgetting benchmark drift** — a 70% MMLU score in 2023 meant something different than 70% in 2026.
- **Treating benchmarks as ground truth** — they're a proxy for capability, not the capability itself.
- **Overfitting to benchmarks** — fine-tuning on benchmark-style data improves benchmarks but may not improve real tasks.

## Further Reading

- Hendrycks et al. (2021), *Measuring Massive Multitask Language Understanding* (MMLU).
- Chen et al. (2021), *Evaluating Large Language Models Trained on Code* (HumanEval).
- Suzgun et al. (2022), *BIG-Bench Hard*.
- Chiang et al. (2023), *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*.

## See Also

- [[05 - Hallucination]]
- [[04 - In-Context Learning]]
- [[22 - Production AI/MOC|Production AI MOC]]
- [[08 - LLMs/MOC|LLMs MOC]]

## The Benchmark Saturation Problem

Benchmarks have a lifecycle: they're created, models improve on them, and eventually they saturate (most models hit 90%+). Saturated benchmarks stop being informative.

| Benchmark | Year | Current SOTA | Saturation Level | Replacement |
|-----------|------|-------------|-----------------|-------------|
| MMLU | 2021 | ~88% | Near-saturated | MMLU-Pro |
| GSM8K | 2021 | ~95%+ | Saturated | MATH, AIME |
| HumanEval | 2021 | ~90%+ | Saturated | LiveCodeBench, BigCodeBench |
| HellaSwag | 2019 | ~95%+ | Saturated | — |
| BBH | 2022 | ~85% | Near-saturated | GPQA, ARC-AGI |
| GPQA | 2023 | ~65% | Active | — |
| MMLU-Pro | 2024 | ~75% | Active | — |
| SWE-bench | 2024 | ~50% | Active | — |
| ARC-AGI | 2024 | ~20% | Active | — |

The pattern: every 2-3 years, the field needs new benchmarks as old ones saturate. This is a sign of progress, not a problem — but it means benchmark comparisons across years are not meaningful.

## Chatbot Arena — The Gold Standard

Chatbot Arena (LMSYS) has emerged as the most trusted evaluation for chat quality because it measures **real human preferences**: humans compare two anonymous models side-by-side and pick the better response. Elo ratings are computed from results.

As of 2026, Chatbot Arena Elo is the metric that frontier labs optimize for. A 10-point Elo improvement is significant; 50+ points is a generational leap.

## Reasoning Model Benchmarks — The New Frontier

Reasoning models (o1, R1) changed what benchmarks matter: AIME (competition math), Codeforces (competitive programming), GPQA Diamond (PhD science), ARC-AGI (abstract reasoning), SWE-bench Verified (real software engineering). These are designed to be hard even for frontier models (current SOTA: 50-70%, not 90%+).

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Benchmark scores don't match production quality | Benchmark is contaminated or doesn't match workload | Build custom eval set from production traffic |
| Sudden benchmark improvement | Contamination | Check decontamination; use private test sets |
| LLM-as-judge inconsistent | Judge bias (verbosity, style, position) | Use multiple judges; position-swap; human calibration |
| Benchmark is "solved" (95%+) | Saturation | Move to harder benchmarks (GPQA, MMLU-Pro, SWE-bench) |

## Connection to Other Concepts

- [[08 - LLMs/Capabilities/04 - In-Context Learning|In-Context Learning]] — few-shot benchmark evaluation.
- [[08 - LLMs/Sampling/03 - Sampling Strategies|Sampling Strategies]] — benchmarks use temperature=0.
- [[08 - LLMs/Limitations/05 - Hallucination|Hallucination]] — benchmarks don't capture hallucination well.
- [[21 - LLMOps and MLOps/Evaluation/04 - LLM-as-Judge Evaluation|LLM-as-Judge Evaluation]] — judge-based benchmarks.
- [[21 - LLMOps and MLOps/Deployment/07 - A-B Testing and Shadow Deployment|A/B Testing]] — production evaluation.
- [[02 - Mathematics/Statistics/17 - Hypothesis Testing|Hypothesis Testing]] — statistical significance of benchmark differences.
- [[27 - Projects/Capstones/13 - Build a RAG Evaluation Harness|RAG Eval Harness]] — custom eval implementation.
- [[26 - Papers/2024-2026/42 - Scaling Laws (Kaplan and Chinchilla)|Scaling Laws]] — benchmark scores scale with compute.

## Interview Questions

1. **Q: What is benchmark contamination and how do you detect it?**
   A: Contamination is when benchmark test data appears in the training corpus. Models memorize it, inflating scores. Detection: (1) check if the model card reports decontaminated scores; (2) compare few-shot vs zero-shot — contaminated models may score similarly; (3) use private/held-out test sets; (4) look for suspiciously high scores on specific subsets.

2. **Q: Why has Chatbot Arena become the most trusted benchmark?**
   A: Three reasons. (1) Real human preferences — it measures what humans actually prefer, not a proxy. (2) Blind evaluation — humans don't know which model is which. (3) Elo rating — accounts for opponent difficulty. Limitations: subjective, chat-focused, expensive, small human sample.

3. **Q: How do you build a custom evaluation set for your production LLM?**
   A: (1) Sample 50-200 examples from real production traffic. (2) Label each with expected output. (3) Run the model at temperature=0. (4) Compute accuracy or use LLM-as-judge for open-ended tasks. (5) Track the score over time; alert on regressions. (6) Update quarterly. The eval set is your regression test for model changes.

4. **Q: What is benchmark saturation and why does it matter?**
   A: Saturation is when most models score 90%+ on a benchmark, making it uninformative. MMLU is near-saturated (~88%); GSM8K is saturated (~95%+). When a benchmark saturates, it can't distinguish between models. The field responds by creating harder benchmarks (MMLU-Pro, GPQA, SWE-bench, ARC-AGI).

5. **Q: How do reasoning model benchmarks differ from standard LLM benchmarks?**
   A: Reasoning models are tested on harder benchmarks: AIME, Codeforces, GPQA Diamond, ARC-AGI, SWE-bench. These are designed to be hard even for frontier models (SOTA: 50-70%). They test multi-step reasoning, not memorization. Standard benchmarks (MMLU, GSM8K) saturate immediately for reasoning models.

6. **Q: What are the limitations of LLM-as-judge for benchmark evaluation?**
   A: Four biases: (1) verbosity bias — judges prefer longer responses; (2) self-preference — GPT-4 judges prefer GPT-4-style writing; (3) position bias — judges prefer first or last response; (4) calibration drift — different judges use different scales. Mitigations: use multiple judges, position-swap, calibrate against human labels, use structured rubrics.
