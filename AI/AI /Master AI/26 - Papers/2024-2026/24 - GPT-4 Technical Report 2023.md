---
tags: [paper, gpt-4, multimodal, closed-model]
iteration: 4
created: 2026-08-08
aliases: [GPT-4 2023, GPT-4 Technical Report]
---

# 24 — GPT-4 Technical Report (OpenAI, 2023)

> [!info] TL;DR
> GPT-4 was a major capability leap over GPT-3.5: it could process images as well as text, passed professional exams at human-expert level (bar exam top 10%, SAT 1410/1600), and was substantially more reliable on reasoning and instruction-following. The technical report is unusual in that it disclosed **almost no architectural details** — no parameter count, no training data size, no architecture description. This opacity set a precedent for closed-source frontier model releases and motivated the open-source community to reverse-engineer GPT-4's likely design.

## Citation

OpenAI (2023). *GPT-4 Technical Report*. arXiv:2303.08774.

## The Problem Being Solved

GPT-3.5 (InstructGPT, ChatGPT) was a significant capability leap over GPT-3, but it had clear limitations: weak reasoning, frequent hallucination, no multimodal capability, and brittle instruction-following. The frontier in early 2023 was moving toward:
- **Multimodal**: models that can process images and text together.
- **Stronger reasoning**: reliable multi-step reasoning for math, code, logic.
- **Better alignment**: fewer hallucinations, more helpful responses, safer behavior.
- **Professional-grade capability**: passing professional exams (bar, medical, coding certifications).

GPT-4 was OpenAI's response — a model that addressed all four. The technical report focused on capabilities and alignment, not architecture.

## What the Report Disclosed

The GPT-4 technical report is notable for what it did *not* say:
- **No parameter count**. Not disclosed. (Widely believed to be ~1.7T parameters as a mixture of experts, but this is unconfirmed.)
- **No architecture details**. Not disclosed. (Assumed to be a Transformer with MoE, but unconfirmed.)
- **No training data**. Not disclosed. (Assumed to be a large web crawl plus proprietary data.)
- **No training compute**. Not disclosed. (Estimated at ~10²⁵ FLOPs based on inference cost and capability.)

What the report did disclose:
- **Capabilities**: benchmark results across a wide range of tasks.
- **Multimodal**: GPT-4 can process images and text.
- **Alignment approach**: RLHF with a focus on factuality, helpfulness, and safety.
- **Evaluation methodology**: how the model was tested.

This opacity was a significant departure from prior OpenAI papers (GPT-2, GPT-3 disclosed architecture and parameters). It set the pattern for subsequent frontier model releases from OpenAI (GPT-4o, o1, GPT-5) and Anthropic (Claude 3, 3.5, 4) — capabilities disclosed, architecture withheld.

## Capabilities

GPT-4's capability improvements over GPT-3.5 were substantial:

### Professional Exams
| Exam                          | GPT-3.5  | GPT-4    | Human Percentile |
|-------------------------------|----------|----------|------------------|
| Uniform Bar Exam              | ~10%     | ~90%     | top 10%          |
| SAT (Verbal + Math)           | ~70%     | ~93%     | 1410/1600        |
| GRE (Verbal)                  | ~63%     | ~99%     | 169/170          |
| USMLE (medical)               | ~60%     | ~85%     | passing          |
| LeetCode (hard)               | ~10%     | ~30%     | —                |

The bar exam result was particularly striking: GPT-4 scored in the top 10% of human test-takers, while GPT-3.5 was in the bottom 10%. This was a clear demonstration that frontier LLMs had reached professional-grade capability on knowledge-intensive tasks.

### Multimodal
GPT-4 could process images: describe them, answer questions about them, read text in images (OCR), and reason about diagrams, charts, and screenshots. This was the first widely-available multimodal LLM and opened up applications in education (solving math problems from photos), accessibility (describing images for blind users), and productivity (analyzing screenshots).

### Reasoning
GPT-4 was substantially better at multi-step reasoning than GPT-3.5. On math benchmarks (GSM8K, MATH), coding benchmarks (HumanEval, MBPP), and logic puzzles, GPT-4 consistently outperformed GPT-3.5 by 10–30 points. The model could reliably follow chain-of-thought prompts and produce correct intermediate steps.

### Alignment
GPT-4 was trained with RLHF focused on factuality, helpfulness, and safety. Compared to GPT-3.5, GPT-4:
- Hallucinated less (though still significantly).
- Refused harmful requests more reliably.
- Followed instructions more precisely.
- Was less sycophantic (less likely to agree with false user statements).

The report included a detailed "system card" documenting the model's failure modes, biases, and safety considerations — a level of disclosure that became standard for subsequent frontier model releases.

## What the Report Did Not Disclose (and Why It Matters)

The lack of architectural disclosure was controversial:

### The "Closed Frontier" Precedent
Before GPT-4, frontier LLM papers typically disclosed architecture (GPT-2, GPT-3, Chinchilla, PaLM all disclosed parameters and architecture). GPT-4 broke this norm. Subsequent frontier releases from OpenAI (GPT-4o, o1, GPT-5) and Anthropic (Claude 3, 3.5, 4) followed the same pattern: capabilities disclosed, architecture withheld.

The motivation (per OpenAI's statements): competitive concerns and safety concerns. Disclosing architecture helps competitors and potentially helps bad actors replicate the model. Critics argued that the opacity hindered research and concentrated power in a few labs.

### Reverse-Engineering Attempts
The open-source community attempted to infer GPT-4's likely design:
- **Mixture of Experts**: GPT-4's inference cost (much higher than a dense model of similar capability) suggested MoE. The widely-cited "GPT-4 Architecture" leak (semi-analysis, 2023) estimated 1.7T parameters across 16 experts, ~280B active per token. This is unconfirmed.
- **Multimodal training**: likely trained on image-text pairs from web data, possibly using a ViT-family encoder fused into the Transformer.
- **RLHF with process rewards**: the strong reasoning and instruction-following suggested RLHF with process reward models (PRMs), not just outcome rewards.

These inferences are **strongly inferred, not officially confirmed** per [[00 - Vault Management/Architecture Decisions|ADR-006]]. The open-source community treated them as design hypotheses, not facts.

### Impact on Open-Source
GPT-4's opacity motivated the open-source community to build equivalent models openly. Llama (Meta, 2023), Mistral (2023), and DeepSeek (2024) all aimed to match GPT-4-class capability with full architectural disclosure. By 2024–2025, open-source models (Llama 3.1 405B, DeepSeek-V3) had largely closed the gap.

## Why It Worked (Inferred)

Since OpenAI did not disclose the architecture, the following is inferred from capability patterns and community analysis:

### Scale (Likely)
GPT-4's capability jump over GPT-3.5 likely came from substantially more parameters and training compute. The MoE hypothesis (1.7T parameters, ~280B active) is consistent with the inference cost and capability.

### Multimodal Pretraining
GPT-4's image understanding likely came from pretraining on image-text pairs, not from a separate vision encoder bolted on at fine-tuning. The model could reason about images fluently, suggesting deep integration.

### Improved RLHF
GPT-4's improved alignment (less hallucination, more helpful) likely came from a more sophisticated RLHF pipeline — possibly with process reward models (PRMs) that evaluate intermediate reasoning steps, not just final answers.

### Better Data
GPT-4's strong performance on professional exams (bar, medical) suggests training data that included high-quality technical content (legal documents, medical textbooks, code repositories). Data quality, not just scale, was likely a factor.

### Chain-of-Thought at Inference
GPT-4's reasoning improvements likely came from training the model to produce explicit chain-of-thought (especially for math and code), then using that chain at inference. This is the same pattern that o1 (2024) and R1 (2025) would later make explicit.

## Limitations

- **Hallucination**: GPT-4 hallucinated less than GPT-3.5 but still significantly. The model confidently invented facts, citations, and API methods.
- **Closed architecture**: the lack of disclosure hindered research and concentrated capability in OpenAI.
- **Cost**: GPT-4 was 10–30× more expensive than GPT-3.5 per token, limiting use in cost-sensitive applications.
- **Context window**: initially 8K, later extended to 32K and 128K. Still shorter than some competitors (Claude 200K).
- **Knowledge cutoff**: GPT-4's training data had a cutoff (initially September 2021, later updated), so it lacked knowledge of recent events.
- **No tool use natively** (initially): GPT-4 could not call tools, search the web, or execute code at launch. These capabilities were added later (function calling, code interpreter, web browsing).

## Impact and Legacy

GPT-4 was a watershed moment for AI:

1. **Frontier capability benchmark**. GPT-4 became the reference point for "frontier LLM capability" in 2023–2024. Open-source models were measured against it (Llama 2 was "60% of GPT-4 quality"; Llama 3 was "GPT-4 class").

2. **Multimodal as default**. GPT-4's image capability made multimodal a default expectation for frontier models. By 2024, every frontier model (Claude 3, Gemini, Llama 3.2) had multimodal capability.

3. **Closed-source precedent**. GPT-4's opacity normalized architectural secrecy for frontier models. This shaped the industry: OpenAI and Anthropic disclose capabilities, Meta and Mistral disclose architecture.

4. **Catalyst for open-source**. GPT-4's capability gap over open-source models motivated massive investment in open LLMs. Llama 2, Mistral, DeepSeek, and Qwen all aimed to close the gap, and by 2025 they largely had.

5. **Professional AI applications**. GPT-4's exam-passing capability enabled professional AI applications: legal research, medical diagnosis support, coding assistance. This drove enterprise adoption of AI in 2023–2024.

6. **Reasoning as a research direction**. GPT-4's reasoning improvements (chain-of-thought, multi-step problem solving) motivated the reasoning-model research that produced o1 (2024) and R1 (2025).

For AI engineers, GPT-4 remains the reference point for frontier capability. Even if you use open-source models, you measure them against GPT-4. Understanding GPT-4's capabilities (and limitations) is essential for designing production AI systems — it's the bar that all models are compared against.

## Further Reading

- Original paper: arXiv:2303.08774
- "GPT-4 Architecture" (semi-analysis, 2023) — the widely-cited reverse-engineering analysis. **Strongly inferred, not officially confirmed.**
- [[04 - GPT-3 2020]] — the predecessor.
- [[12 - DeepSeek-R1 2025]] — the open-source reasoning model that approached GPT-4-class reasoning.

## See Also

- [[09 - GPT Family Evolution]]
- [[04 - GPT-3 2020]]
- [[01 - Multimodal AI Overview]]
- [[06 - LLM Benchmarks]]
- [[05 - Hallucination]]
- [[26 - Papers/MOC|Papers MOC]]
