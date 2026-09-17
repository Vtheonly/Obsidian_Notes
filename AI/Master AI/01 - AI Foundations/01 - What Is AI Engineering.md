---
tags: [ai-foundations, orientation, career]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [What Is AI Engineering, AI Engineering Discipline, AI Engineer Role]
---

# 01 - What Is AI Engineering

> [!info] TL;DR
> AI Engineering is the discipline of building production systems whose core component is a trained neural model — usually a Transformer-based LLM. It sits at the intersection of ML engineering, software engineering, distributed systems, and product. It is not "training GPT-5 from scratch" — it's "shipping reliable products on top of pretrained models." This note covers what AI engineering actually is, the skill stack, what makes it hard, how it differs from adjacent fields, the maturity model, common mistakes, career paths, and a day-in-the-life view.

## What AI Engineering Actually Is

AI Engineering is the **applied engineering discipline** of taking pretrained AI models (mostly LLMs, but also embedding models, vision models, audio models, diffusion models) and building useful, reliable, cost-effective systems on top of them. The job is rarely to invent new architectures; it's almost always to combine existing components — models, retrieval, tools, infrastructure — into a coherent product.

Concretely, an AI engineer's day-to-day includes:

- **Prompting and fine-tuning** models for specific tasks.
- **Designing retrieval pipelines** (RAG) to ground model outputs in real data.
- **Building agent systems** that use tools and iterate toward goals.
- **Serving models at scale** with low latency and acceptable cost.
- **Monitoring production systems** for drift, hallucination, and abuse.
- **Integrating AI features** into existing software systems.
- **Evaluating model outputs** systematically (offline + online).
- **Managing cost**: token budgets, model routing, caching.
- **Building data pipelines** for fine-tuning, evaluation, and continuous improvement.
- **Working with product and design** to translate model capabilities into user value.

What an AI engineer does **not** typically do:

- Train foundation models from scratch (that's research at frontier labs).
- Invent new neural network architectures (that's ML research).
- Build the GPU hardware (that's systems engineering).
- Label training data (that's data ops).
- Train diffusion models for image generation (unless that's their specific focus).

## The Skill Stack

A working AI engineer needs roughly:

1. **Software engineering** — Python, APIs, databases, version control, testing, deployment. This is non-negotiable; without it, nothing ships. See [[04 - The Modern AI Stack]].
2. **ML fundamentals** — what models are, how they're trained, what they can and can't do. See [[02 - Mathematics/MOC|02 Mathematics]] through [[04 - Neural Networks/MOC|04 Neural Networks]].
3. **Transformer / LLM specifics** — attention, tokenization, sampling, fine-tuning, evaluation. See [[06 - Attention Mechanisms/MOC|06]] through [[08 - LLMs/MOC|08]].
4. **Inference engineering** — KV cache, batching, quantization, serving frameworks. See [[13 - Inference/MOC|13 Inference]].
5. **Applied AI patterns** — RAG, agents, memory, tool use. See [[15 - AI Agents/MOC|15]] through [[19 - MCP/MOC|19]].
6. **Production systems** — infrastructure, observability, cost, security. See [[20 - AI Infrastructure/MOC|20]] through [[22 - Production AI/MOC|22]].

You don't need to be an expert in all six before starting. Most working AI engineers are deep in 2–3 and competent in the rest.

### The T-Shaped AI Engineer

The "T-shaped" model applies well to AI engineering:

- **Horizontal bar (breadth)**: enough understanding of all six areas to make architectural decisions, communicate with specialists, and integrate components.
- **Vertical bar (depth)**: deep expertise in one area. Common specializations:
  - **Inference engineer**: focuses on serving, quantization, kernel optimization.
  - **RAG engineer**: focuses on retrieval, embeddings, evaluation.
  - **Agent engineer**: focuses on agent frameworks, tool use, multi-agent systems.
  - **Fine-tuning engineer**: focuses on LoRA, RLHF, dataset curation.
  - **AI infra engineer**: focuses on GPU clusters, distributed training, Kubernetes.
  - **Applied ML engineer**: focuses on the model-product gap, prompt engineering, evaluation.

Pick a depth area based on your background and interests. Breadth comes with time.

## What Makes AI Engineering Hard

Traditional software engineering is hard because of complexity, scale, and changing requirements. AI engineering adds three more dimensions:

### 1. Non-determinism
The same input can produce different outputs. A model might answer correctly 95% of the time and fail mysteriously the other 5%. This breaks traditional testing, monitoring, and debugging approaches. You can't write a unit test that says `assert model.answer("2+2") == "4"` because the model might say "4", "four", "The answer is 4", or "2+2=4".

**Implications**:
- Tests become probabilistic: "the model should answer correctly 95%+ of the time on this eval set".
- Monitoring tracks distributions, not just points: token usage, latency percentiles, faithfulness scores.
- Debugging requires tracing: why did the model produce *this* output *this* time? Look at the prompt, retrieved context, temperature, model version.

### 2. Capability shifts
A model that worked great in January might be replaced by a better one in March, but the new one behaves differently — different prompt formats, different failure modes, different cost. You're building on a moving foundation.

**Implications**:
- Pin model versions in production. Don't auto-upgrade.
- Build an abstraction layer over model providers (LiteLLM, internal gateway) so you can swap models without rewriting application code.
- Run your eval set on every model upgrade. A "better" model may regress on your specific use case.
- Track model behavior over time: latency, cost, failure modes, user satisfaction.

### 3. Evaluation is hard
For a CRUD app, you can write tests: "create user → user exists." For an LLM feature, what's the test? "Summarize this article" has no single right answer. You need new evaluation techniques — LLM-as-judge, golden datasets, human review, online A/B tests.

**Implications**:
- Build an eval set early. Even 50 hand-labeled examples are better than nothing.
- Use multiple evaluation methods: automated metrics, LLM-as-judge, human spot-checks, user feedback.
- Treat evaluation as a first-class engineering problem, not an afterthought.
- Online metrics (user satisfaction, thumbs up/down, retention) are the ultimate ground truth, but they lag behind deployment.

### 4. Cost is variable and unpredictable
A traditional API call costs the same whether the input is 10 bytes or 10KB. An LLM call costs proportional to input + output tokens, which can vary 10× across requests. A single "summarize this 100K-token document" call costs 100× a normal call.

**Implications**:
- Set per-request token budgets.
- Cache aggressively (query cache, semantic cache).
- Route easy queries to cheaper models, hard queries to expensive ones.
- Monitor token usage in real-time; alert on spikes.

### 5. Latency is variable
LLM latency varies with output length, model load, prompt complexity. A "summarize this" request might take 500ms or 5s. Users notice.

**Implications**:
- Stream outputs to mask latency.
- Set per-request timeouts.
- Use speculative decoding or smaller models for low-latency paths.
- Monitor p50, p95, p99 latency separately.

## How AI Engineering Differs from Adjacent Fields

| Field                  | Focus                                            | Overlap with AI Eng                                |
|------------------------|--------------------------------------------------|----------------------------------------------------|
| ML Engineering         | Training models on data                          | High — same math, same code, different scale       |
| Data Science           | Insights from data; statistics                   | Medium — DS informs what models should do          |
| Software Engineering   | Building reliable software                       | High — AI features ship in software                |
| MLOps                  | Pipelines, deployment, monitoring for ML         | High — LLMOps is the LLM-specific variant          |
| Data Engineering       | Building data pipelines                          | Medium — RAG needs good data pipelines             |
| DevOps / SRE           | Operating distributed systems                    | Medium — AI systems run on distributed infra       |
| AI Research            | Inventing new architectures, training new models | Low overlap; high inspiration                      |
| Product Engineering    | Building user-facing products                    | High — AI features must serve user needs           |

### Concrete Distinctions

- **AI Engineer vs. ML Engineer**: ML engineers train models on data (often tabular, often smaller scale). AI engineers build systems on top of pretrained foundation models. The skills overlap (both know PyTorch, both understand ML), but the day-to-day is different. ML engineers worry about feature engineering, model selection, hyperparameter tuning. AI engineers worry about retrieval, prompting, evaluation, serving.

- **AI Engineer vs. Data Scientist**: Data scientists extract insights from data, often with statistical methods. AI engineers build production systems. Data scientists inform what the AI should do; AI engineers make it work in production.

- **AI Engineer vs. MLOps Engineer**: MLOps engineers build pipelines for training, deploying, and monitoring ML models. LLMOps (the LLM variant) is a subset. AI engineers do some LLMOps but also build the application logic, retrieval, and agent systems on top.

## The AI Engineering Maturity Model

Organizations and individuals progress through maturity levels:

### Level 1: Prompt Engineering
- Can call an LLM API and get a response.
- Writes effective prompts (few-shot, chain-of-thought).
- Uses a single model for everything.
- Builds prototypes, not production systems.

### Level 2: RAG and Basic Production
- Builds RAG pipelines with vector databases.
- Uses multiple models (different sizes for different tasks).
- Implements caching, rate limiting, basic monitoring.
- Ships AI features to production, with manual monitoring.

### Level 3: Fine-tuning and Evaluation
- Fine-tunes models with LoRA/QLoRA for specific tasks.
- Builds systematic evaluation pipelines.
- Implements cost optimization (model routing, quantization).
- Has automated monitoring with alerts.

### Level 4: Agents and Multi-Model Systems
- Builds agent systems with tool use.
- Orchestrates multiple models (router + specialists).
- Implements human-in-the-loop for high-stakes actions.
- Has comprehensive observability (traces, metrics, logs).

### Level 5: AI Platform Engineering
- Builds internal AI platforms (model serving, fine-tuning, eval, monitoring).
- Supports multiple AI product teams.
- Implements advanced techniques (speculative decoding, custom kernels).
- Sets organizational standards for AI reliability and cost.

Most working AI engineers are at Level 2-3. Senior engineers and tech leads are at Level 3-4. Platform teams operate at Level 5.

## Common Mistakes

### 1. Treating AI Engineering as Prompt Engineering
Prompting is a small part. The bulk of the work is the system around the model: retrieval, tools, memory, monitoring, cost control. Engineers who focus only on prompts ship fragile systems.

### 2. Skipping Evaluation
"I tested it on 3 examples and it worked" is not evaluation. Without a systematic eval set, you can't tell if changes help or hurt, can't catch regressions, and can't communicate quality to stakeholders.

### 3. Over-Engineering
Adding graph RAG, agentic loops, and multi-model routing when simple vector RAG would suffice. Start simple, measure, add complexity only when needed.

### 4. Under-Investing in Data
Fine-tuning on low-quality data makes the model worse. RAG on garbage documents retrieves garbage. Data quality is the #1 determinant of AI system quality.

### 5. Ignoring Cost
LLM costs add up fast. A feature that costs $0.05 per query and gets 1M queries/month costs $50K/month. Without cost monitoring and optimization, AI features become unsustainable.

### 6. Treating the LLM as a Database
LLMs hallucinate. They're not authoritative sources of facts. Use RAG to ground them in real data. Don't trust model outputs for factual claims without verification.

### 7. Not Pinning Model Versions
"Use GPT-4" is not a spec. "Use `gpt-4-0613`" is. Models change behavior between versions. Pin versions in production; test upgrades carefully.

### 8. Building Instead of Buying
For many use cases, off-the-shelf tools (LangChain, LlamaIndex, vLLM, RAGAS) are good enough. Don't rebuild these from scratch unless you have a specific need.

## Day in the Life

A typical day for a mid-level AI engineer at a product company:

**Morning (9-11am)**:
- Check overnight monitoring: latency, cost, error rates, faithfulness scores.
- Triage user feedback: thumbs-down reviews, support tickets.
- Standup: share progress, raise blockers.

**Midday (11am-2pm)**:
- Work on the current feature: maybe adding reranking to the RAG pipeline.
- Write code, run evals, iterate.
- Pair with a product manager on requirements for the next feature.

**Afternoon (2-5pm)**:
- Code review for a teammate's PR.
- Investigate a production issue: why did the agent loop forever on this query?
- Read a paper or blog post on a new technique (continuous learning is essential).

**Late afternoon (5-6pm)**:
- Deploy a small improvement to staging.
- Document what you learned today (internal wiki or personal notes).

This varies by team and seniority, but the rhythm — monitoring, building, evaluating, deploying — is consistent.

## Why This Matters

If you're reading this vault, you're probably aiming for an AI engineering role or already in one. Understanding the discipline's scope prevents two common mistakes:

1. **Trying to learn everything** — there's too much. Pick a depth area and breadth the rest.
2. **Treating AI engineering as "prompt engineering"** — prompting is a small part. The bulk of the work is the system around the model: retrieval, tools, memory, monitoring, cost control.

## Production Implications

- The AI engineer's value is in the **system**, not the prompt. A great prompt with a bad system fails; a mediocre prompt with a great system can succeed.
- Most production AI features spend 80% of effort on infrastructure, evaluation, and monitoring — not on the model itself.
- The pace of change means **learning velocity** matters more than current knowledge. Build the habit of reading papers and trying new tools continuously.
- **Reliability is harder than capability**. Getting an LLM to do something once is easy. Getting it to do something reliably 99.9% of the time, at acceptable cost and latency, with monitoring and rollback — that's the job.

## Career Path

Common career paths into AI engineering:

### From Software Engineering
- **Path**: SWE → SWE with AI features → AI Engineer → Senior AI Engineer.
- **Strengths**: production systems, testing, deployment.
- **Gaps to fill**: ML fundamentals, Transformer specifics, evaluation methodologies.
- **Time**: 6-12 months of focused learning to transition.

### From ML Engineering / Data Science
- **Path**: ML Engineer → ML Engineer with LLM focus → AI Engineer.
- **Strengths**: ML fundamentals, experimentation, statistics.
- **Gaps to fill**: production software engineering, distributed systems, modern serving stacks.
- **Time**: 3-9 months to fill software engineering gaps.

### From Research
- **Path**: PhD/Postdoc → Applied Researcher → AI Engineer.
- **Strengths**: deep ML knowledge, ability to read papers.
- **Gaps to fill**: production engineering, product thinking, moving fast.
- **Time**: 6-12 months; the cultural shift from "thorough" to "shipped" is the hardest part.

### From Adjacent Fields (DevOps, Data Engineering, etc.)
- **Path**: DevOps → MLOps → LLMOps → AI Engineer.
- **Strengths**: infrastructure, operations.
- **Gaps to fill**: ML fundamentals, application logic.
- **Time**: 9-18 months; the ML learning curve is steep.

## Interview Questions

- **Q: What's the difference between AI engineering and ML engineering?**  
  A: ML engineers train models on data. AI engineers build systems on top of pretrained foundation models. The skills overlap, but the day-to-day is different.

- **Q: How would you decide between RAG and fine-tuning for a new feature?**  
  A: Use RAG for knowledge that changes frequently, for attribution, and for multi-tenancy. Use fine-tuning for style, behavior, and domain-specific patterns. They're complementary — fine-tune the model's behavior, then RAG for facts.

- **Q: How do you evaluate an LLM feature?**  
  A: Build an eval set with (input, expected output) pairs. Use automated metrics (faithfulness, relevance) for fast iteration, LLM-as-judge for nuanced quality, and human review for ground truth. Track online metrics (user satisfaction, retention) as the ultimate signal.

- **Q: How do you handle model upgrades in production?**  
  A: Pin model versions. Run your eval set on the new version before deploying. Use shadow deployment (run new model in parallel, compare outputs). Roll out gradually (canary, A/B test). Have a rollback plan.

- **Q: What's the hardest part of production AI?**  
  A: Reliability at scale. Getting an LLM to do something once is easy. Getting it to do it 99.9% of the time, at acceptable cost and latency, with monitoring and rollback — that's the job.

## Further Reading

- Andrej Karpathy, *Software 2.0* (essay) — the shift from explicit code to learned models.
- Eugene Yan, *Machine Learning Systems Design*.
- Chip Huyen, *Designing Machine Learning Systems*.
- Hannes Hapke, *Machine Learning Engineering in Action*.
- The rest of this vault.

## See Also

- [[02 - AI vs ML vs DL vs GenAI vs Agentic AI]]
- [[03 - A Brief History of AI]]
- [[04 - The Modern AI Stack]]
- [[05 - AI Engineer Roles]]
- [[06 - Map of the Field]]
- [[01 - AI Foundations/MOC|AI Foundations MOC]]
- [[22 - Production AI/MOC|22 Production AI]] — production concerns in depth
- [[21 - LLMOps and MLOps/MOC|21 LLMOps]] — operational concerns
