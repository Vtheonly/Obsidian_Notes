---
tags: [training, pretraining, scaling-laws, chinchilla, clm, mlm]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Pretraining Objectives, Scaling Laws, Chinchilla, CLM, MLM, Span Corruption]
---

# 01 - Pretraining Objectives and Scaling Laws

> [!info] TL;DR
> Three pretraining objectives dominate: causal LM (GPT family), masked LM (BERT), and span corruption (T5). The Chinchilla scaling law (2022) showed most models were undertrained — compute-optimal training uses ~20 tokens per parameter. Modern LLMs train on 15–30T tokens. This note covers objectives, scaling laws (Kaplan vs Chinchilla), overtraining, the modern training recipe, hyperparameters, cost analysis, production implications, and common pitfalls.

## Pretraining Objectives

The pretraining objective is the self-supervised task the model learns before any human annotation. It determines what the model can do after pretraining.

### Causal Language Modeling (CLM)

Predict the next token given previous tokens:

$$
\mathcal{L} = -\frac{1}{T} \sum_{t=1}^{T} \log p_\theta(x_t \mid x_{<t})
$$

This is maximum likelihood estimation: maximize the probability the model assigns to the training data, factored autoregressively.

Used by all decoder-only LLMs (GPT, Llama, Mistral, Qwen, DeepSeek). The model learns to generate by predicting what comes next.

**Properties**:
- **Autoregressive**: tokens are generated left-to-right.
- **Causal masking**: each token can only attend to previous tokens (and itself).
- **Generative**: the model can generate text by sampling.
- **Single forward pass for all positions**: thanks to causal masking, training computes all positions' losses in one pass.

**Why CLM dominates**:
- Simple: one objective, one architecture.
- Generative: can do all tasks (chat, code, reasoning, translation).
- Scales predictably: scaling laws are well-understood.
- Composable: easy to add fine-tuning (SFT, RLHF, DPO) on top.

### Masked Language Modeling (MLM)

Randomly mask tokens; predict them from context (both directions):

$$
\mathcal{L} = -\sum_{t \in \text{masked}} \log p(x_t \mid x_{\neq t})
$$

Typically 15% of tokens are masked. The model uses both left and right context to predict the masked token.

Used by BERT-family (BERT, RoBERTa, DeBERTa). Great for representation learning; can't generate.

**Properties**:
- **Bidirectional**: tokens attend to both left and right context.
- **Non-generative**: the model can't generate text (it predicts masked tokens, not next tokens).
- **Good for classification**: the [CLS] token's representation is a strong sentence embedding.
- **Multiple forward passes**: each masked position requires its own prediction; less efficient than CLM.

**Use cases**: classification, NER, embeddings, retrieval (BERT-style encoders).

### Span Corruption

Mask random spans (multiple tokens); predict the spans:

$$
\mathcal{L} = -\sum_{\text{spans}} \log p(\text{span} \mid \text{rest})
$$

Used by T5. Hybrid of CLM and MLM: the model generates the masked spans (like CLM) but uses bidirectional context (like MLM).

**Properties**:
- **Span-based**: masks are contiguous spans of tokens, not single tokens.
- **Generative**: the model generates the spans (uses a decoder).
- **Bidirectional context**: the encoder sees the unmasked context.
- **Sentinel tokens**: special tokens (`<extra_id_0>`, `<extra_id_1>`, ...) mark span boundaries.

**Use cases**: text-to-text tasks (T5 frames everything as text-to-text).

### Prefix LM

A variant of CLM where the prefix is bidirectional and the suffix is causal. Used by PaLM and some other models.

$$
\mathcal{L} = -\sum_{t > \text{prefix}} \log p(x_t \mid x_{<t}, x_{\text{prefix}})
$$

The prefix gets bidirectional attention; the suffix is generated causally. Combines MLM's bidirectional context with CLM's generative capability.

**Use cases**: instruction-tuned models where the prompt (prefix) benefits from bidirectional context.

### Fill-in-the-Middle (FIM)

A training objective for code models: given prefix, middle, and suffix, predict the middle. The model learns to fill in code between two existing blocks.

```
<prefix>def add(a, b):<suffix>    return result<middle>    c = a + b
```

See [[04 - Code Models]] for details. FIM is essential for code completion in IDEs.

### Comparison

| Objective | Architecture | Generative | Use Case |
|-----------|--------------|------------|----------|
| CLM | Decoder-only | Yes | General LLMs (GPT, Llama) |
| MLM | Encoder-only | No | Classification, embeddings (BERT) |
| Span corruption | Encoder-decoder | Yes | Text-to-text (T5) |
| Prefix LM | Decoder-only | Yes | Instruction-tuned (PaLM) |
| FIM | Decoder-only | Yes | Code completion (StarCoder) |

CLM dominates because it's simple, generative, and scales well. The other objectives have niche uses.

## Scaling Laws

Scaling laws predict how model loss (and thus quality) scales with parameters, data, and compute. They're the quantitative foundation of LLM planning.

### Kaplan et al. (2020) — Original Scaling Law

Loss scales as a power law in parameters $N$, data $D$, and compute $C$:

$$
L(N, D, C) = L_\infty + A N^{-\alpha} + B D^{-\beta}
$$

where $L_\infty$ is the irreducible loss (the data's entropy), and $A, B, \alpha, \beta$ are fitted constants.

Kaplan's key findings:
- Loss decreases predictably with scale (parameters, data, compute).
- **Parameters and data should scale together**, but Kaplan recommended scaling parameters faster than data.
- Most models at the time trained ~1.7 tokens per parameter.

### Chinchilla (Hoffmann et al., 2022) — The Corrective

Re-derived the scaling law with a different methodology (training over 400 models from 70M to 16B parameters, on 5B to 400B tokens). Found that **compute-optimal training uses ~20 tokens per parameter** — far more than Kaplan suggested.

The Chinchilla scaling law:
- For compute $C$, optimal parameters $N^*$ and data $D^*$ satisfy $D^* / N^* \approx 20$.
- Train smaller models on more data.

**The implication**: most models at the time (GPT-3, original Llama) were undertrained. GPT-3 (175B params, 300B tokens) trained at 1.7 tokens/param — far below the optimal 20. Chinchilla (70B params, 1.4T tokens) trained at 20 tokens/param and outperformed GPT-3.

### Why Chinchilla Beat GPT-3

| Model | Params | Tokens | Tokens/Param | Loss |
|-------|--------|--------|--------------|------|
| GPT-3 | 175B | 300B | 1.7 | Higher |
| Chinchilla | 70B | 1.4T | 20 | Lower |

Same compute, but Chinchilla allocated it differently: smaller model, more data. The result: better quality at the same compute cost.

This was a major finding: the field had been training models wrong for years. Post-Chinchilla, all serious pretraining uses ~20 tokens/param.

### Modern Practice (2024–2026)

- Compute-optimal is ~20 tokens/param (Chinchilla).
- Many models train **beyond compute-optimal** (overtraining) because inference cost dominates total cost.
- Llama 3 8B was trained on 15T tokens (~1875 tokens/param) — far beyond Chinchilla-optimal.
- Overtraining a small model is cheaper at inference than training a Chinchilla-optimal large model.

### Why Overtrain?

The Chinchilla scaling law optimizes for **training compute**. But in production, **inference compute** often dominates. A smaller model that's overtrained:
- Costs less per inference (fewer parameters).
- Costs more to train (more tokens).
- But total cost (training + inference over the model's lifetime) is lower if inference volume is high.

For a model served billions of times, inference cost dominates. Overtraining the small model saves on every inference call.

**Llama 3 8B** (15T tokens, ~1875 tokens/param): overtrained by Chinchilla standards, but the inference savings (vs. a Chinchilla-optimal 70B) more than make up for the training cost over the model's lifetime.

### Scaling Law Implications

| Goal | Strategy |
|------|----------|
| Best quality at fixed compute | Chinchilla-optimal: ~20 tokens/param |
| Best inference cost | Overtrain a small model |
| Best quality regardless of cost | Train the largest model you can, on as much data as you have |
| Specialized domain | Continued pretraining on domain data |

### Limitations of Scaling Laws

- **Empirical, not theoretical**: scaling laws are fitted to data, not derived from first principles. They may not hold outside the fitted range.
- **Data quality matters**: scaling laws assume high-quality data. Noisy data breaks the scaling.
- **Architecture-specific**: Kaplan and Chinchilla studied decoder-only Transformers. Different architectures may scale differently.
- **Diminishing returns**: power laws eventually plateau. The "irreducible loss" $L_\infty$ is the data's entropy; you can't go below it.
- **Capability emergence**: some capabilities (in-context learning, reasoning) emerge suddenly at certain scales, not gradually. Scaling laws predict loss, not capabilities.

## What Pretraining Looks Like in Practice

### 1. Data Preparation

Collect trillions of tokens from web, books, code, papers. Filter, deduplicate, remove PII, balance domains.

See [[03 - Data Pipelines and Deduplication]] for details.

Typical data mix (Llama 3):
- ~50% web text (Common Crawl, filtered).
- ~20% code (GitHub).
- ~17% books.
- ~5% scientific papers (arXiv).
- ~8% other (math, reference, etc.).

### 2. Tokenizer Training

Train BPE/SentencePiece on a sample of the data. The tokenizer is frozen after this — choosing it is a high-stakes one-way decision.

See [[01 - Tokenization Overview]] and [[02 - BPE]] for details.

### 3. Architecture Setup

Choose model config (layers, heads, dim, FFN dim, vocab). The modern recipe (see [[01 - Decoder-Only Architecture]]):

| Component | Choice |
|-----------|--------|
| Norm | RMSNorm (pre-norm) |
| Attention | GQA |
| Positional | RoPE |
| FFN | SwiGLU |
| Bias | None |
| Dropout | None (regularize via data) |

### 4. Training Hyperparameters

| Hyperparameter | Typical Value (7B) | Typical Value (70B) |
|----------------|---------------------|---------------------|
| Optimizer | AdamW | AdamW |
| $\beta_1, \beta_2$ | 0.9, 0.95 | 0.9, 0.95 |
| Weight decay | 0.1 | 0.1 |
| Peak LR | 3e-4 | 2e-4 |
| LR schedule | Cosine decay to 10% | Cosine decay to 10% |
| Warmup steps | 2000 | 2000 |
| Batch size | 4M-8M tokens | 4M-8M tokens |
| Sequence length | 4K-8K (extend to 32K+ late) | 4K-8K (extend to 32K+ late) |
| Precision | BF16 | BF16 |
| Gradient clipping | 1.0 | 1.0 |

### 5. Training Schedule

1. **Warmup** (2000 steps): linearly increase LR from 0 to peak.
2. **Main training**: cosine decay LR from peak to 10% of peak.
3. **Long-context annealing** (last ~10%): extend sequence length to 32K+ for long-context capability.
4. **Cooldown** (last ~5%): constant low LR to stabilize.

### 6. Checkpointing

Save every ~1B tokens; eval on held-out; select best. Training runs fail; without checkpoints, you lose days of work.

### Cost Analysis

Llama 3 8B training: ~15T tokens, 1.3M H100-hours, ~$130M compute cost (at ~$100/H100-hour).

For comparison:
- GPT-3 (2020): ~$5M (estimated).
- Llama 2 70B (2023): ~$20M (estimated).
- Llama 3 70B (2024): ~$50M (estimated).
- GPT-4 (2023): ~$60M (estimated).

Pretraining costs are growing but the resulting models are also more capable.

## Why This Matters for AI

- Pretraining is **the** expensive step of LLM creation. Most teams will never pretrain from scratch — they'll consume pretrained models.
- Understanding pretraining explains **why models behave the way they do**: their knowledge comes from the data distribution; their fluency from the CLM objective.
- Scaling laws are **the** quantitative foundation of LLM planning. They let you predict how much compute/data/params you need for a target quality.
- For fine-tuning, you're starting from a pretrained model — understanding pretraining helps you reason about what the model already knows.
- The choice of objective (CLM vs MLM) determines what the model can do. Decoder-only + CLM is the default for generative LLMs.

## Production Implications

- **Don't pretrain from scratch** unless you have $10M+ and a real reason. Use Llama 3 / Mistral / Qwen.
- **Continued pretraining** (more pretraining on domain data) can help for specialized domains (medical, legal). Use a small LR (1e-5) and limited steps.
- **Data quality >> data quantity** — a clean 1T-token dataset beats a noisy 10T-token dataset. Invest in data pipelines.
- **Tokenizers are frozen after pretraining** — choosing the right tokenizer is a high-stakes one-way decision. Vocabulary size, special tokens, and byte-level vs word-level all matter.
- **Model size vs. inference cost**: if inference is your bottleneck, overtrain a smaller model. If training is your bottleneck (rare), use Chinchilla-optimal sizing.
- **Checkpoint strategy**: save frequently, eval frequently, keep multiple checkpoints. Training runs fail; be prepared.
- **Monitoring**: track loss, gradient norm, LR, throughput. Set up alerts for loss spikes, NaN, OOM.
- **Distributed training**: for >7B models, use FSDP or 3D parallelism. See [[02 - Distributed Training]].

## Common Pitfalls

- **Underestimating data requirements** — Chinchilla says 20 tokens/param; many people try with much less and get poor quality.
- **Bad data filtering** — duplicates, low-quality text, PII all hurt quality. Invest in data pipelines.
- **Wrong LR schedule** — no warmup, no decay → unstable training. Always use warmup + cosine decay.
- **Forgetting to checkpoint** — training runs fail; without checkpoints, you lose days. Save every ~1B tokens.
- **Mixing training data domains badly** — wrong proportions of code/web/books hurts specific capabilities. Ablate the mix.
- **Numerical instability** — loss spikes, NaN. Use gradient clipping, BF16, and stability techniques (see [[05 - Loss Spikes and Stability]]).
- **Wrong batch size** — too small → slow; too large → instability. 4M-8M tokens is typical.
- **Sequence length too short** — short sequences limit long-context capability. Extend to 32K+ late in training.
- **Forgetting to extend context** — models trained only on 4K context can't do 32K context at inference without RoPE scaling or fine-tuning.
- **Not evaluating during training** — without intermediate eval, you don't know if the model is improving. Eval every ~1B tokens.
- **Forgetting to deduplicate** — duplicates in training data cause the model to memorize, not generalize. Always deduplicate.

## Worked Example: Estimating Training Cost

Suppose you want to train a 7B model on 15T tokens (Llama 3 8B scale).

**Compute estimate**:
- FLOPs per token (forward + backward): $6 \times N = 6 \times 7 \times 10^9 = 4.2 \times 10^{10}$.
- Total FLOPs: $4.2 \times 10^{10} \times 15 \times 10^{12} = 6.3 \times 10^{23}$.
- At H100 BF16 throughput ~700 TFLOPs: $6.3 \times 10^{23} / 7 \times 10^{14} = 9 \times 10^8$ H100-seconds = ~250K H100-hours.
- At $2/H100-hour: ~$500K.

But this assumes 100% MFU (model FLOPs utilization). Real MFU is 40-60%, so actual cost is ~$850K-$1.25M.

For a 70B model on 15T tokens: 10× the parameters, ~10× the cost → ~$10M.

For a 405B model (Llama 3 405B): ~60× the 7B cost → ~$60M.

These are rough estimates; actual costs vary with hardware, optimization, and data pipeline efficiency.

## Interview Questions

- **Q: What is the Chinchilla scaling law, and why was it important?**  
  A: Chinchilla (2022) showed that compute-optimal training uses ~20 tokens per parameter, far more than the ~1.7 tokens/param used by GPT-3. This meant most models were undertrained. Post-Chinchilla, all serious pretraining uses ~20 tokens/param.

- **Q: Why do modern models overtrain beyond Chinchilla-optimal?**  
  A: Chinchilla optimizes for training compute. But in production, inference compute dominates. A smaller overtrained model is cheaper at inference, and the inference savings over the model's lifetime outweigh the extra training cost.

- **Q: What's the difference between CLM and MLM?**  
  A: CLM (causal LM) predicts the next token given previous tokens; used by decoder-only models (GPT, Llama). MLM (masked LM) predicts masked tokens from bidirectional context; used by encoder-only models (BERT). CLM is generative; MLM is not.

- **Q: How much compute does it take to train a 7B model?**  
  A: Rough rule: $6 \times N \times D$ FLOPs, where $N$ is parameters and $D$ is tokens. For 7B model on 15T tokens: $6 \times 7e9 \times 15e12 = 6.3 \times 10^{23}$ FLOPs. At H100 BF16 (~700 TFLOPs, 50% MFU), that's ~500K H100-hours, ~$1M.

- **Q: Why is the LR schedule important?**  
  A: Warmup stabilizes early training (when gradients are large). Cosine decay helps the model settle into a good minimum. Without warmup, training diverges; without decay, the model oscillates near the end.

## Further Reading

- Kaplan et al. (2020), *Scaling Laws for Neural Language Models*.
- Hoffmann et al. (2022), *Training Compute-Optimal Large Language Models* (Chinchilla).
- Llama 3 paper (2024) — modern training recipe with overtraining.
- Touvron et al. (2023), *Llama 2: Open Foundation and Fine-Tuned Chat Models*.
- Brown et al. (2020), *Language Models are Few-Shot Learners* (GPT-3).

## See Also

- [[02 - Distributed Training]] — how to actually run pretraining at scale
- [[03 - Data Pipelines and Deduplication]] — data preparation
- [[04 - Mixed Precision Training]] — BF16, FP8
- [[05 - Loss Spikes and Stability]] — handling training instability
- [[12 - Fine-Tuning/MOC|12 Fine-Tuning]] — what happens after pretraining
- [[11 - Training/MOC|Training MOC]]
- [[08 - LLMs/MOC|LLMs MOC]]
- [[02 - Mathematics/Optimization/14 - Learning Rate Schedules|LR Schedules]]
- [[13 - Adam Derivation]] — the optimizer
- [[01 - Decoder-Only Architecture]] — the architecture being trained
