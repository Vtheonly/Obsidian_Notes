---
tags: [model-architecture, gpt-4, closed-source, inferred]
iteration: 8
created: 2026-08-08
last_updated: 2026-08-08
aliases: [GPT-4 Architecture, GPT-4 Inferred Architecture]
---

# 07 — GPT-4 Inferred Architecture

> [!info] TL;DR
> OpenAI has not officially disclosed GPT-4's architecture. Based on inference costs, capability patterns, and community analysis (notably the "semi-analysis" leak), GPT-4 is **strongly inferred** to be a Mixture-of-Experts model with ~1.7T total parameters and ~280B active per token, using 16 experts. This note summarizes what's publicly known, what's inferred, and what's speculative — per ADR-006 source-labelling requirements.

> [!warning] Source Status
> **Most claims in this note are Strongly Inferred or Speculative.** OpenAI has not officially disclosed GPT-4's architecture. The inferences below are based on:
> - GPT-4's inference cost (much higher than a dense model of similar capability).
> - Capability patterns (specialized strengths suggesting expert specialization).
> - Community analysis (notably the "semi-analysis" report, 2023).
> - Comparison to known MoE models (Mixtral, DeepSeek-V3).
> Treat all specific numbers as unverified.

## What's Officially Confirmed

OpenAI's GPT-4 technical report (March 2023) disclosed almost no architectural details. The only confirmed facts:
- GPT-4 is a Transformer-based model.
- It can process images as well as text (multimodal).
- It was trained with RLHF.
- It passes professional exams at human-expert level.
- It has a knowledge cutoff (originally September 2021, later updated).

Everything else — parameter count, architecture (dense vs MoE), training data, training compute — is **not officially disclosed**.

## What's Strongly Inferred

### Mixture-of-Experts Architecture
**Evidence**:
- GPT-4's inference cost is ~10–30× GPT-3.5's, despite not being 10–30× more capable. This is consistent with a large MoE where only a fraction of parameters are active per token.
- The 128K context variant (GPT-4 Turbo) is expensive, suggesting large per-token compute.
- Mixtral 8x7B and DeepSeek-V3 demonstrated that MoE matches dense quality at lower active compute. GPT-4 likely uses the same approach.

**Inference**: GPT-4 is a MoE model. The number of experts and routing mechanism are not confirmed.

### Parameter Count (~1.7T Total, ~280B Active)
**Evidence** (from the "semi-analysis" report, July 2023):
- The report, based on analysis of GPT-4's behavior and costs, estimated 1.7T total parameters across 16 experts, with 2 experts active per token (~280B active).
- This is consistent with the inference cost (280B active is ~4× GPT-3.5's ~175B, matching the ~4× cost premium at launch).
- The 16-expert, 2-active design mirrors Mixtral (8 experts, 2 active) at larger scale.

**Caveats**:
- The "semi-analysis" report is not peer-reviewed or officially confirmed.
- The numbers may have changed with GPT-4 Turbo (2023), GPT-4o (2024), and subsequent versions.
- OpenAI has never confirmed or denied these estimates.

### Multimodal Training
**Evidence**:
- GPT-4 (original) could process images from launch (March 2023).
- The image understanding is fluent (not bolted-on), suggesting the model was trained on image-text data, not just text.
- GPT-4o (2024) extended to audio, suggesting native multimodal training.

**Inference**: GPT-4 was trained on image-text pairs (and possibly audio for GPT-4o), with vision and language integrated in the same model (not a separate vision encoder).

### RLHF with Process Reward Models
**Evidence**:
- GPT-4's reasoning quality (multi-step math, code) exceeds what outcome-only RLHF typically achieves.
- OpenAI's research on process reward models (PRMs) — which evaluate intermediate reasoning steps, not just final answers — was published around GPT-4's development.
- The strong reasoning suggests PRM-based RLHF, not just outcome-based RLHF.

**Inference**: GPT-4's alignment used process reward models (evaluating reasoning steps), not just outcome reward models (evaluating final answers). This is not confirmed.

## What's Speculative

### Specific Expert Count and Routing
The "16 experts, 2 active" claim is unverified. Other estimates (8 experts, 4 active; 32 experts, 2 active) are also plausible. Without official disclosure, the exact configuration is speculative.

### Training Data Composition
GPT-4's training data is not disclosed. Inferences about specific datasets (CommonCrawl, books, code, proprietary data) are speculative.

### Training Compute
Estimated at ~10²⁵ FLOPs (based on inference cost and capability), but this is a rough estimate. The actual compute is not disclosed.

### Specific Architectural Components
Whether GPT-4 uses GQA, MLA, sliding window attention, or other specific techniques is not known. Inferences based on capability patterns are speculative.

## Why the Architecture Isn't Disclosed

OpenAI's stated reasons for non-disclosure:
1. **Competitive concerns**: disclosing architecture helps competitors replicate GPT-4.
2. **Safety concerns**: disclosing capabilities helps bad actors understand what the model can do.
3. **Commercial strategy**: mystery about architecture maintains perceived value.

Critics argue:
1. **Hinders research**: without architecture, academic research on frontier models is limited.
2. **Concentrates power**: only OpenAI knows how GPT-4 works, creating an information asymmetry.
3. **Safety theater**: the safety benefits of non-disclosure are questionable.

## Comparison to Known MoE Models

If GPT-4 is indeed a 1.7T MoE with 280B active, it compares to:

| Model         | Total Params | Active Params | Experts | Active Experts |
|---------------|--------------|---------------|---------|----------------|
| Mixtral 8x7B  | 46.7B        | 12.9B         | 8       | 2              |
| Mixtral 8x22B | 141B         | 39B           | 8       | 2              |
| DeepSeek-V3   | 671B         | 37B           | 256     | 8              |
| GPT-4 (inferred) | ~1.7T     | ~280B         | ~16     | ~2             |

GPT-4's inferred design (large total, large active) would explain both its capability (large total capacity) and its cost (large active compute).

## How This Compares to Open-Weights

By 2024–2025, open-weights models (Llama 3.1 405B, DeepSeek-V3) matched or exceeded GPT-4 on many benchmarks. The open models have known architectures (dense 405B for Llama; MoE 671B/37B for DeepSeek). This suggests:
- GPT-4's capability is no longer unique — open models have caught up.
- The inferred ~280B active compute is consistent with DeepSeek-V3's 37B active (both are MoE, though at different scales).

## Implications for AI Engineers

### You Don't Need GPT-4's Architecture
For most applications, you don't need to know GPT-4's exact architecture. You need to know:
- Its capabilities (well-documented in the technical report).
- Its API behavior (well-documented in OpenAI's docs).
- Its cost and latency (well-documented in pricing).

### Open Models Are Catching Up
Llama 3.1 405B and DeepSeek-V3 match GPT-4 on many benchmarks, with known architectures. If you need architectural transparency, use open models.

### Closed-Model Inference Is Valid
Even without knowing the architecture, you can build production applications on GPT-4. The API contract (input → output) is stable regardless of internal architecture.

### For Research, Use Open Models
If you're doing interpretability, architecture research, or capability analysis, you need open weights. GPT-4 is unsuitable for these purposes because you can't inspect its internals.

## Future Disclosure

OpenAI is unlikely to disclose GPT-4's architecture. However:
- GPT-4o, o1, and GPT-5 (if released) may have different architectures, and old architectures may become less sensitive to disclose over time.
- OpenAI might disclose GPT-4's architecture years after release (as Google did for some old models).
- The open-source community's reverse-engineering will continue to refine the inferences.

## Evidence-Based Reasoning: How to Infer Architecture Without Disclosure

The methodology behind "inferring" closed-model architectures is itself instructive. Five primary signals are used, each with strengths and weaknesses:

### Signal 1: Inference Cost vs Capability

A dense model's inference cost grows linearly with parameter count. If a model is 10× more expensive than a smaller dense model but only 2× more capable, the gap is consistent with a MoE where the total parameter count is large but the active count is moderate. This was the primary signal for GPT-4: cost ~10-30× GPT-3.5 with capability ~2× GPT-3.5 → consistent with a large MoE.

**Strength**: directly observable from pricing.
**Weakness**: pricing is a business decision, not a pure cost reflection. OpenAI could price GPT-4 at a margin unrelated to its actual compute cost.

### Signal 2: Capability Asymmetries

If a model excels at certain subtasks (e.g., code generation) but is mediocre at others (e.g., creative writing), this suggests expert specialization — different experts may have learned different domains. This is a weak signal because capability differences can also arise from training data composition, not architecture.

### Signal 3: Behavioral Patterns

Specific behavioral quirks (e.g., the model "loses" information at certain context lengths, or has characteristic failure modes) can hint at architectural choices. For example, RoPE-based models have characteristic failure modes at lengths exceeding the training context. Sliding-window models lose long-range dependencies beyond the window. These patterns can be tested via targeted probes.

### Signal 4: Leakage from Employees / Partners

Occasionally, employees or partners leak architectural details. The "semi-analysis" report on GPT-4 was based on partial information from people with knowledge of the system. This is the most direct signal but also the least verifiable — leaks can be wrong, partial, or outdated.

### Signal 5: Comparison to Open Models with Similar Capability

If an open model with known architecture (e.g., DeepSeek-V3, MoE 671B/37B) matches GPT-4's capability, it's reasonable to infer GPT-4 has roughly similar active compute. This is the "anchoring" approach — use open models as calibration points for closed ones.

The combination of all five signals gives the community's best estimate, but the uncertainty is large. **Treat any specific number (parameter count, expert count) as ±50% accurate.**

## Why GPT-4 Turbo and GPT-4o Changed the Picture

GPT-4 Turbo (Nov 2023) and GPT-4o (May 2024) likely changed the underlying architecture. Inferred changes:
- **GPT-4 Turbo**: 128K context (vs original 32K), lower price (~3× cheaper than original GPT-4). The lower price suggests either smaller active compute or improved serving efficiency. The longer context suggests YaRN-style RoPE extension or a separate long-context variant.
- **GPT-4o**: native multimodal (text + image + audio in one model), 2× faster than GPT-4 Turbo, 50% cheaper. The speed improvement suggests architectural changes (possibly smaller active parameters or better attention efficiency). The native multimodality suggests the model was trained end-to-end on text, image, and audio tokens, not bolted-on encoders.
- **o1/o3**: reasoning models, almost certainly a different training recipe (RL on verifiable rewards) on top of a GPT-4-class base. The architecture may be similar; the training and inference differ.

This means the "GPT-4" architecture is not a single fixed thing — it's a moving target. Inferences made about original GPT-4 (Mar 2023) may not apply to GPT-4o (May 2024) or o1 (Sep 2024).

## Open-Weights Comparables to GPT-4 (2024-2026)

By late 2024, several open-weights models matched or exceeded original GPT-4 on common benchmarks. These serve as architectural reference points:

| Model               | Architecture                | Total / Active params | Notable Features                              |
|---------------------|-----------------------------|------------------------|-----------------------------------------------|
| Llama 3.1 405B      | Dense decoder-only           | 405B / 405B            | GQA, RoPE, 128K context, SwiGLU               |
| DeepSeek-V3         | MoE decoder-only             | 671B / 37B             | MLA, 256 experts (8 active), auxiliary-loss-free routing |
| Qwen2.5-72B         | Dense decoder-only           | 72B / 72B              | GQA, RoPE, 128K context, YaRN extension       |
| Mixtral 8x22B       | MoE decoder-only             | 141B / 39B             | GQA, 8 experts (2 active), sliding window + global |
| Kimi K2             | MoE decoder-only             | ~1T / ~32B (inferred)  | MLA, sparse attention, long context           |

If GPT-4 is ~1.7T total / ~280B active (semi-analysis estimate), it would be:
- ~4× larger than Llama 3.1 405B (dense).
- ~2.5× larger total than DeepSeek-V3, but ~7.5× larger active.
- The active compute (280B) is significantly larger than DeepSeek-V3 (37B) — explaining GPT-4's higher cost.

## How to Build Production Systems Without Knowing GPT-4's Architecture

For most AI engineers, GPT-4's architecture is irrelevant. You interact with it via API; the contract is input → output. Build systems that:
1. **Don't depend on architectural assumptions**. If you assume GPT-4 has a 128K context and OpenAI releases a 256K version, your system should benefit, not break.
2. **Pin the model version**. Use `gpt-4o-2024-08-06`, not `gpt-4o`. This protects against silent architectural changes.
3. **Have fallbacks**. If GPT-4 is unavailable, fall back to Claude or an open model. Architectural diversity across providers is itself a form of resilience.
4. **Treat the model as a black box**. Benchmark on your task; if the model is good enough, use it. Don't try to predict quality from architecture.
5. **For research, use open weights**. Interpretability, capability analysis, and architecture research require inspectable models. GPT-4 is unsuitable for these.

## The Disclosure Debate

The non-disclosure of closed-model architectures is a live debate in 2026:

**Arguments for disclosure**:
- Enables academic research on frontier models.
- Allows auditors to assess safety properties.
- Reduces information asymmetry between providers and the public.
- Open models with disclosed architectures (Llama, DeepSeek) demonstrate that disclosure doesn't prevent commercial success.

**Arguments against disclosure**:
- Helps competitors replicate the model.
- Helps adversaries find vulnerabilities.
- Disclosed capabilities may be over-interpreted by regulators.
- Most users don't need the architecture; the API contract is sufficient.

The current equilibrium: closed providers (OpenAI, Anthropic) disclose system cards (high-level capabilities and safety properties) but not architectures. Open providers (Meta, DeepSeek, Mistral, Qwen) disclose architectures fully. This equilibrium is likely to persist — the commercial pressure to disclose is low, and the research community can use open models.

## Interview Questions

1. **Q: What can you infer about GPT-4's architecture from its API behavior?**
   A: Five main inferences: (1) MoE (from cost/capability gap), (2) ~1.7T total / ~280B active (from semi-analysis), (3) multimodal training (from fluent image understanding), (4) RLHF with PRMs (from reasoning quality), (5) RoPE-based positional encoding (from context-length behavior). All inferences are unconfirmed; treat as ±50% accurate.

2. **Q: How would you validate an inference about a closed model's architecture?**
   A: Behavioral probes. Test the model's context-length scaling (RoPE vs ALiBi vs learned), test for sliding-window behavior (long-range dependency failures), test for MoE routing (capability asymmetries across subtasks), measure latency vs input length (linear → dense; sublinear → MoE). No single probe is conclusive; combine many.

3. **Q: Why does the AI community care about GPT-4's architecture if open models match it?**
   A: Three reasons: (1) GPT-4 set the capability benchmark for years; understanding how it works informs architecture research. (2) Closed models still lead on some benchmarks (especially reasoning with o1/o3); the architecture behind this lead is valuable to understand. (3) For interpretability and safety research, knowing the architecture of deployed models matters — most users interact with closed models.

4. **Q: If you needed to replicate GPT-4's capability with open tools in 2026, what would you use?**
   A: DeepSeek-V3 (MoE 671B/37B) or Llama 3.1 405B (dense) for base capability. Add RLHF (DPO or GRPO) for alignment. For reasoning capability, fine-tune with the R1 recipe (RL on verifiable rewards). For multimodal, add a vision encoder (SigLIP-2) and projector. The resulting system would match GPT-4 on most benchmarks at lower inference cost (DeepSeek-V3's 37B active vs GPT-4's inferred 280B active).

5. **Q: What are the risks of treating closed-model architectures as "unknown black boxes" in production?**
   A: Three risks: (1) Provider drift — silent model updates can break your system; pin versions to mitigate. (2) Capability regressions — a new model version may be worse on your specific task; maintain regression evals. (3) Vendor lock-in — if your system depends on a closed model's specific behavior, switching is hard; use open models or maintain multi-provider abstraction.

6. **Q: How does source-labelling (ADR-006) apply to closed-model architectural claims?**
   A: Every claim must be tagged: Officially Confirmed (rare — only what the provider states), Research-Backed (published analysis), Strongly Inferred (technical evidence but no confirmation), or Speculative (insufficient evidence). For GPT-4, most claims are Strongly Inferred. Mixing these levels without tagging misleads readers.

## See Also

- [[24 - GPT-4 Technical Report 2023]] — the official paper note.
- [[03 - Llama Family Architecture]] — open-weights alternative.
- [[28 - DeepSeek-V2 and V3 2024]] — open MoE comparison.
- [[15 - Mixture of Experts Transformer]] — MoE concept.
- [[00 - Vault Management/Research Queue|Research Queue]] — open questions about GPT-4.
- [[10 - Model Architecture Research/MOC|10 Model Architecture MOC]]