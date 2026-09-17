---
tags: [llms, limitations, hallucination, faithfulness, grounding]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Hallucination, LLM Hallucination, Fabrication, Confabulation]
---

# 05 - Hallucination

> [!info] TL;DR
> Hallucination is when an LLM produces confident but false information. The fundamental cause: LLMs generate plausible text, not verified truth. This note covers the types of hallucination, root causes, mitigation strategies (RAG, prompting, fine-tuning, verification, calibration), detection methods, the spectrum of severity, agent-specific concerns, production patterns, and open research questions. No complete solution exists in 2026 — the goal is mitigation, not elimination.

## What Is Hallucination?

Hallucination takes many forms:

- **Factual hallucination**: "The Eiffel Tower is in Berlin." (Confidently wrong about a fact.)
- **Source hallucination**: "According to a 2023 study by Smith et al..." (No such study exists.)
- **Capability hallucination**: "I've verified this code compiles." (It doesn't.)
- **Self-knowledge hallucination**: "I don't have personal experiences." (Sometimes followed by a personal anecdote.)
- **Citation hallucination**: "See [Smith 2020]" (Fabricated reference.)
- **Date/time hallucination**: "Today is March 15, 2025." (It's not; the model has no clock.)
- **API hallucination**: "The `numpy.calculate_mean()` function..." (No such function exists.)
- **Logical hallucination**: "Since A > B and B > C, therefore C > A." (Wrong logical conclusion.)

### Hallucination vs. Other Failure Modes

Hallucination is distinct from:
- **Errors**: wrong answers due to lack of knowledge (model "knows" it doesn't know, but guesses wrong).
- **Bias**: systematic skew in outputs (e.g., always assuming doctors are male).
- **Toxicity**: harmful or offensive content.
- **Inconsistency**: different answers to the same question asked differently.

Hallucination specifically is **confident fabrication** — the model produces wrong content as if it were true, without signaling uncertainty.

## Why LLMs Hallucinate

### 1. They're trained on next-token prediction, not truth
The training objective is "predict the next token given context", not "produce true statements." The model learns statistical patterns of text, not facts. Plausibility is the goal, not truth.

The objective $\mathcal{L} = -\sum_t \log p(x_t | x_{<t})$ maximizes the likelihood of training text. If the training text contains errors (and it does), the model learns those errors. If the training text is silent on a topic, the model learns the *pattern* of plausible-sounding text on that topic, even without facts.

### 2. They don't know what they don't know
An LLM has no internal "I don't know" signal. It will produce a confident-sounding answer regardless of whether it knows. Calibrated uncertainty is rare and hard to elicit.

The model's probability distribution over tokens doesn't distinguish "high confidence because I know" from "high confidence because the pattern is common." Both produce fluent, confident output.

### 3. Training data contains errors
If the training corpus has wrong facts, the model learns them. Wikipedia has errors; web text is full of misinformation; even authoritative sources disagree. The model has no way to distinguish reliable from unreliable sources.

Common data issues:
- Wikipedia "citation needed" tags get stripped during training.
- Satire (The Onion) is indistinguishable from news.
- Old information persists even after corrections.
- Multiple sources repeat the same error (echo chamber effect).

### 4. Generalization produces new (false) patterns
The model doesn't just memorize — it generalizes. Sometimes generalization creates patterns that look right but are wrong (e.g., plausible-sounding but nonexistent book titles).

For example, if the model has seen many book titles like "The [Adjective] [Noun]: A [Topic] Journey", it can generate "The Crimson Path: A Mathematical Journey" — a plausible title for a book that doesn't exist. The pattern is right; the specific instance is fabricated.

### 5. Prompting can induce hallucination
Leading questions ("Why did the US invade Canada in 1812?") presuppose false premises. The model often plays along rather than correcting. This is sometimes called **sycophancy** — the model agrees with the user's framing, even when wrong.

### 6. The model has no ground truth at inference time
At inference, the model has only its parameters and the prompt. There's no mechanism to "look up" facts; everything comes from memory. If the memory is wrong or incomplete, the output is wrong.

### 7. Sampling introduces randomness
At temperature > 0, sampling can produce low-probability tokens that lead the model into unfamiliar territory, where it hallucinates. Lower temperature reduces this but doesn't eliminate it.

### 8. Long-form generation drifts
As the model generates longer outputs, early hallucinations propagate: the model conditions on its own fabricated content, producing more hallucinations consistent with the first. This "snowball" effect is why long-form generation is more hallucination-prone than short-form.

## Types of Hallucination

### Intrinsic vs Extrinsic
- **Intrinsic**: contradicts the source (if RAG is used, contradicts retrieved context). Easier to detect — compare output to context.
- **Extrinsic**: produces content not supported by the source (might be true, might be false — can't verify from context alone). Harder to detect — requires external verification.

### Open-domain vs Closed-domain
- **Open-domain**: any fact in the world. Hard to verify.
- **Closed-domain**: facts about a specific document (RAG setting). Easier to detect via faithfulness metrics.

### Factuality vs Faithfulness
- **Factuality**: the output is true in the real world. Requires external verification.
- **Faithfulness**: the output is supported by the provided context. Requires only comparing output to context.

A model can be faithful but not factual (the context is wrong), or factual but not faithful (the model adds correct facts not in the context). RAG evaluation focuses on faithfulness; broader evaluation focuses on factuality.

### Severity Levels

Hallucination isn't binary — it's a spectrum:

- **L1 - Minor inaccuracy**: small factual error that doesn't change the answer's utility. ("The Eiffel Tower was built in 1887" — actually 1889.)
- **L2 - Misleading**: error that could lead to wrong conclusions. ("Aspirin cures cancer" — wrong and harmful.)
- **L3 - Fabricated source**: invented citation, study, or quote. ("According to Smith 2020..." — no such study.)
- **L4 - Complete fabrication**: entirely made-up content presented as fact. ("The 1947 Treaty of Lisbon established the European Space Agency." — totally false.)
- **L5 - Dangerous fabrication**: false content in a high-stakes domain (medical, legal, financial) that could cause harm.

Production systems should track hallucination rates by severity, not just count.

## Mitigations

### Retrieval-Augmented Generation (RAG)
Retrieve relevant documents; condition generation on them. See [[01 - RAG Pipeline Overview]].

- **Helps**: grounds the model in real data; provides source attribution.
- **Doesn't fully solve**: the model can still hallucinate from the retrieved context (especially if the context is ambiguous or the model misreads it).
- **Best practice**: prompt explicitly to "answer only from the context; say 'I don't know' if the context doesn't contain the answer." Use reranking to ensure relevant context. Validate citations.

### Prompt Engineering
- "If you don't know, say 'I don't know'." — helps but not perfectly reliable. The model's threshold for "knowing" is unclear.
- "Cite your sources." — produces citations but they may be hallucinated. Always validate citations programmatically.
- Chain-of-thought: helps the model reason but can also rationalize false answers. Use with caution.
- "Verify each claim against the context before including it." — encourages step-by-step checking.
- Few-shot examples of refusing unanswerable questions — teaches the "I don't know" behavior.

### Fine-tuning
- RLHF/DPO with "I don't know" as a valid response for unanswerable questions. The model learns to refuse rather than fabricate.
- Constitutional AI / RLAIF: a critic model flags hallucinations; the policy learns to avoid them.
- Factuality fine-tuning: train on (question, verified answer) pairs to reinforce factual recall.
- RAG-specific fine-tuning: train on (context, question, grounded answer) triples to teach grounded generation.

### Post-hoc Verification
- Use another LLM (or the same one) to fact-check the response. The verifier reads the answer and the sources, flags unsupported claims.
- Cross-reference with search results. Retrieve fresh sources for each claim.
- Use structured output (JSON with citation fields) and validate citations programmatically. Each citation must point to a real chunk ID with matching content.
- Code execution for math / data questions. If the model claims "2+2=5", execute the calculation.

### Calibration
- Temperature scaling to make the model's confidence match empirical accuracy. A calibrated model that says "90% confident" is right 90% of the time.
- Reject low-confidence outputs. Set a threshold (e.g., if top-1 probability < 0.3, refuse).
- Ask for confidence explicitly ("On a scale of 1-10, how confident?"). Models are surprisingly good at self-assessment when asked directly.
- **Verbalized uncertainty**: ask the model to express uncertainty in language ("I'm not sure, but I think..."). Studies show this correlates with actual accuracy.

### Tool Use
- Let the model use a search tool when unsure. The model decides "I don't know, let me search" and invokes a tool.
- Function calling for fact-checking APIs (e.g., a Wikipedia API, a fact-check database).
- Code execution for math / data questions. Don't trust the model to do arithmetic; execute it.
- Database queries for structured data. Don't trust the model to recall numbers; query the database.

### Architectural Mitigations
- **Retrieval-augmented training**: during training, the model retrieves from a memory and conditions on it. Different from inference-time RAG.
- **Faithfulness training**: train the model to produce only content supported by retrieved context. Self-RAG and Corrective RAG are examples.
- **Verifier models**: train a separate model to verify factual claims. Use it as a post-hoc filter.

## Detection

### Self-consistency
Sample multiple responses (e.g., 5 samples at temperature 0.7); if they disagree, the model is uncertain (and possibly hallucinating). The disagreement rate correlates with hallucination rate.

Implementation: run the model N times, compare outputs (semantically, not just string match), flag queries with high disagreement for review.

### Perplexity-based detection
High perplexity on the model's own output suggests it's "off distribution" — possibly hallucinated. The model is less sure of fabricated content than factual content.

Implementation: compute the model's perplexity on its own output. High perplexity → flag for review.

### External fact-checking
Use a search engine or knowledge base to verify claims. For each claim in the output, search for evidence; flag claims with no supporting evidence.

Tools:
- Google Fact Check API.
- Snopes, Politifact for political claims.
- Custom knowledge bases for domain-specific fact-checking.

### Faithfulness metrics (RAG)
- **RAGAS faithfulness**: fraction of claims in the answer that are supported by retrieved context. Decomposes the answer into atomic claims, checks each against context.
- **TruLens**: similar metrics, with production monitoring.
- **DeepEval**: integrates with pytest for CI/CD.

Example: answer "Llama 3 has 70B parameters and was released in 2024." Decompose into claims: (1) Llama 3 has 70B parameters, (2) Llama 3 was released in 2024. Check each against retrieved context.

### LLM-as-Judge
Use a strong LLM (GPT-4, Claude) to evaluate the output for hallucination. The judge reads the output and the sources, flags unsupported claims. Cheaper than human review, more accurate than automated metrics.

### Human Review
The gold standard. Sample outputs, have human reviewers flag hallucinations. Use this to calibrate automated metrics and to catch systematic issues.

## Why This Matters for AI

- Hallucination is **the** biggest blocker to LLM adoption in high-stakes domains (medicine, law, finance).
- Every LLM feature needs a hallucination strategy. Pretending the model "is usually right" is not a strategy.
- For **agents**, hallucination compounds: hallucinated tool arguments, hallucinated observations, hallucinated final answers. Each step can fail, and the failure propagates.
- The lack of a complete solution is why RAG is so widely adopted — it's the best mitigation we have, even though it's not perfect.
- Hallucination rate is a key metric for LLM evaluation. Models are compared on TruthfulQA, HaluEval, and other hallucination benchmarks.
- Hallucination erodes user trust. A single confident wrong answer can destroy a user's confidence in the system, even if 99 prior answers were correct.

## Agent-Specific Hallucination Concerns

In agent systems, hallucination manifests in additional ways:

- **Hallucinated tool arguments**: the model calls `search(query="...")` with arguments that don't match the tool's schema. Causes tool errors or wrong results.
- **Hallucinated observations**: the model "remembers" a tool result that didn't happen. ("I searched for X and found Y..." — but no search was run.)
- **Hallucinated plan**: the model produces a plan that includes impossible steps (e.g., "Step 3: Access the user's bank account" without any such tool).
- **Hallucinated state**: the model believes it has completed a step it hasn't, or vice versa.
- **Hallucinated final answer**: the final answer references steps that didn't happen or results that weren't obtained.

Mitigations for agent hallucination:
- Validate tool arguments against the schema before execution. Reject and ask the model to retry.
- Log all tool results; include them in subsequent prompts so the model doesn't need to "remember".
- Verify the plan against available tools before execution. Reject impossible steps.
- Use structured state tracking (e.g., LangGraph's `AgentState`) rather than relying on the model to track state.
- Verify the final answer against the tool log. Each claim should trace to a tool result.

## Production Implications

- **Always assume hallucination is possible.** Design features that are robust to wrong answers (cite sources, allow user correction, fall back to human review for critical paths).
- **For fact-grounded features**, use RAG with explicit "answer only from context" prompts. Validate citations.
- **For high-stakes features** (medical, legal, financial), add human review for any critical output. Don't auto-approve.
- **Monitor hallucination in production** — sample responses, have human reviewers flag hallucinations, track the rate over time. Alert on rate increases.
- **Citations**: if you cite sources, validate the citations exist. Hallucinated citations are worse than no citations — they erode trust faster.
- **User feedback**: let users flag wrong answers. Use this signal to improve prompts, fine-tune, or update RAG indexes.
- **Calibration**: monitor the model's confidence vs. its accuracy. If confident answers are often wrong, the model is miscalibrated.
- **Model versioning**: hallucination rates change between model versions. Re-evaluate on every upgrade.
- **Domain-specific mitigation**: for medical, legal, or financial domains, fine-tune on verified data and use domain-specific fact-checkers.
- **User expectations**: set expectations clearly. "This AI provides information, not authoritative advice. Verify important facts."
- **Refusal rates**: track how often the model says "I don't know". Too low → hallucinating. Too high → not useful. Find the right balance.

## Common Pitfalls

- **Trusting the model's confidence** — confident wrong answers are common. Confidence is not calibration.
- **Forgetting that RAG doesn't fully solve it** — RAG reduces hallucination but doesn't eliminate it. The model can still misread context or hallucinate from ambiguous context.
- **Prompting once and assuming it works** — "say I don't know" prompts help but leak; test the failure rate empirically.
- **Treating hallucination as a binary** — it's a spectrum. Some answers are partly right, partly wrong. Track severity.
- **Blaming the model only** — bad prompts, missing context, and ambiguous questions all contribute. Fix the system, not just the model.
- **Ignoring the user's role** — leading questions, vague prompts, and unrealistic expectations all increase hallucination.
- **Assuming fine-tuning fixes it** — fine-tuning on factual data helps but doesn't generalize to unseen facts. RAG is still needed.
- **Not validating citations** — a citation to a non-existent source is worse than no citation. Always validate.
- **Confusing factuality with faithfulness** — a faithful answer (supported by context) can still be wrong if the context is wrong. Track both.
- **Not testing for hallucination** — without measuring hallucination rate, you can't tell if mitigations work. Build hallucination eval into your test suite.

## Worked Example: Mitigating Hallucination in a Customer Support Bot

Suppose you're building an LLM-based customer support bot for a SaaS product. The bot answers questions about pricing, features, and troubleshooting.

### Baseline (high hallucination)
- Use GPT-4o directly, no RAG.
- Prompt: "Answer the user's question about our product."
- Hallucination rate: ~15-20% (model invents features, prices, troubleshooting steps).

### Add RAG (medium hallucination)
- Index product docs, pricing page, FAQ.
- Retrieve top 5 chunks per query.
- Prompt: "Answer based on the context. Cite sources."
- Hallucination rate: ~5-10% (model still adds details not in context).

### Add explicit refusal (lower hallucination)
- Prompt: "Answer only from the context. If the context doesn't contain the answer, say 'I don't know.' Cite sources."
- Fine-tune on (context, question, refusal) examples for unanswerable questions.
- Hallucination rate: ~2-5%.

### Add citation validation (lower hallucination)
- Use structured output: each claim must have a citation field.
- Programmatically validate citations: each citation must point to a real chunk with matching content.
- Reject answers with invalid citations; ask model to retry.
- Hallucination rate: ~1-3%.

### Add post-hoc verification (lowest hallucination)
- Use a second LLM to verify each claim against the context.
- Flag and filter unsupported claims.
- Human review for flagged answers.
- Hallucination rate: <1%.

Each step adds cost and latency but reduces hallucination. The right trade-off depends on the use case's risk tolerance.

## Interview Questions

- **Q: Why do LLMs hallucinate, even when they "know" the right answer?**  
  A: LLMs are trained on next-token prediction, not truth. They generate plausible text, which may be wrong even when the model has seen the correct information. The model has no mechanism to distinguish "high confidence because I know" from "high confidence because the pattern is common."

- **Q: How would you reduce hallucination in a RAG system?**  
  A: Use explicit "answer only from context; say I don't know if not in context" prompts. Validate citations programmatically. Use reranking for relevant context. Fine-tune on (context, question, grounded answer) triples. Use post-hoc verification (LLM-as-judge) for high-stakes outputs.

- **Q: What's the difference between faithfulness and factuality?**  
  A: Faithfulness = the output is supported by the provided context. Factuality = the output is true in the real world. A faithful answer can be unfactual (if the context is wrong); a factual answer can be unfaithful (if it adds correct facts not in the context). RAG evaluation focuses on faithfulness; broader evaluation focuses on factuality.

- **Q: How would you measure hallucination rate in production?**  
  A: Sample outputs, have human reviewers flag hallucinations (gold standard). Use LLM-as-judge for cheaper evaluation. Track faithfulness metrics (RAGAS). Track user feedback (thumbs down, corrections). Track by severity (L1-L5). Alert on rate increases.

- **Q: Why does RAG not fully solve hallucination?**  
  A: The model can still misread context, hallucinate from ambiguous context, or add details not in the context. RAG grounds the model but doesn't prevent fabrication. Explicit prompts ("answer only from context") and citation validation are needed.

- **Q: How does temperature affect hallucination?**  
  A: Higher temperature → more randomness → more hallucination (the model explores low-probability tokens that may lead to unfamiliar territory). Lower temperature → more deterministic → less hallucination but also less diverse. For factual tasks, use temperature 0-0.3. For creative tasks, higher is fine.

## Further Reading

- Ji et al. (2023), *Survey of Hallucination in Natural Language Generation*.
- Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (RAG as hallucination mitigation). See [[35 - RAG 2020]].
- Lin et al. (2022), *TruthfulQA: Measuring How Models Mimic Human Falsehoods*.
- Asai et al. (2023), *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*.
- Kadavath et al. (2022), *Language Models (Mostly) Know What They Know* — on calibration.

## See Also

- [[04 - In-Context Learning]]
- [[17 - RAG/MOC|RAG MOC]]
- [[01 - RAG Pipeline Overview]]
- [[03 - Sampling Strategies]] — temperature affects confidence
- [[05 - Reflection]] — agents that self-critique (helps reduce hallucination)
- [[08 - LLMs/MOC|LLMs MOC]]
- [[22 - Production AI/MOC|Production AI MOC]]
- [[22 - Production AI/Security/04 - Guardrails|Guardrails]] — output filtering
