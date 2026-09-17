---
tags: [paper, scaling-laws, chinchilla, kaplan, compute-optimal, training]
iteration: 10
created: 2026-08-08
aliases: [Scaling Laws, Kaplan 2020, Chinchilla, Hoffmann 2022, Compute-Optimal Training]
---

# 42 — Scaling Laws (Kaplan 2020 + Hoffmann 2022 Chinchilla)

> [!info] TL;DR
> Two papers defined how we think about LLM training compute. **Kaplan et al. (2020)** showed that loss scales as a power law in parameters, data, and compute — empirically validating that "bigger is better" follows predictable rules. **Hoffmann et al. (2022, "Chinchilla")** revised Kaplan's data-to-parameter ratio: the optimal ratio is ~20 tokens per parameter, not ~5. This means most 2020–2021 models (GPT-3, Jurassic-1) were severely undertrained — they could have matched their quality with far fewer parameters and far more data. Chinchilla (70B parameters trained on 1.4T tokens) outperformed GPT-3 (175B on 300B tokens) using the same compute. This finding reshaped how every lab trains LLMs: smaller models, more data.

## Citations

Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., & Amodei, D. (2020). *Scaling Laws for Neural Language Models*. arXiv:2001.08361.

Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., Casas, D. de L., Hendricks, L. A., Welbl, J., Clark, S., Hennigan, T., Noland, E., Klimczak, K., Drogosz, M., Sifre, L., Lillicrap, T., Simonyan, K., & Glaese, D. (2022). *Training Compute-Optimal Large Language Models*. NeurIPS 2022. arXiv:2203.15556 (Chinchilla).

## Part 1 — Kaplan 2020: Power-Law Scaling

### The Question

Kaplan et al. asked: how does the test loss of an LLM scale with its size, the amount of training data, and the compute used? Is the relationship predictable, or does it depend on architecture / optimization details?

### The Finding

The test loss $L$ scales as a power law in each of:

- $N$ — number of (non-embedding) parameters.
- $D$ — number of training tokens.
- $C$ — total compute (FLOPs).

$$
L(N) = \left(\frac{N_c}{N}\right)^{\alpha_N}, \quad L(D) = \left(\frac{D_c}{D}\right)^{\alpha_D}, \quad L(C) = \left(\frac{C_c}{C}\right)^{\alpha_C}
$$

with empirically estimated exponents $\alpha_N \approx 0.076$, $\alpha_D \approx 0.095$, $\alpha_C \approx 0.05$.

The key implications:

1. **Loss decreases smoothly with scale** — there are no "phase transitions" or sudden jumps. Bigger is better, predictably.
2. **Sample efficiency improves with size** — larger models reach a given loss with fewer tokens per parameter.
3. **Performance is bottlenecked by whichever of $N$ or $D$ is smaller** — to scale efficiently, both must grow together.

### The Compute-Optimal Allocation

Kaplan's analysis suggested: given a fixed compute budget $C$, the optimal allocation is to scale parameters and data together, but with **parameters growing faster than data**. Specifically, Kaplan estimated that the compute-optimal ratio is roughly $D \propto N^{0.74}$ — i.e., doubling parameters should be accompanied by ~1.7× more data, not 2×.

This led to the "Kaplan recipe": large models, modest data. GPT-3 (175B parameters, 300B tokens) followed this recipe — a ratio of ~1.7 tokens per parameter.

### Why Kaplan Mattered

- **Made scaling predictable**: instead of guessing, you could estimate how much improvement a 10× compute investment would buy.
- **Justified the 2020–2022 scale-up**: GPT-3, Jurassic-1, Gopher, MT-NLG all followed Kaplan's recipe.
- **Set the foundation for Chinchilla's revision**: Kaplan established the framework; Chinchilla refined the constants.

## Part 2 — Hoffmann 2022 (Chinchilla): The Revision

### The Question

Hoffmann et al. noticed that Kaplan's experiments trained each model for a fixed number of tokens but didn't search over the data-to-parameter ratio. They asked: for a fixed compute budget, what's the actual optimal ratio of parameters to data?

### The Method

They trained ~400 models at various scales (70M to 16B parameters, 5B to 500B tokens) and fit a 2D iso-loss surface over $(N, D)$. For each compute budget $C$, they found the $(N^*, D^*)$ that minimizes loss.

### The Finding

The optimal data-to-parameter ratio is **~20 tokens per parameter**, not ~5. This means:

- GPT-3 (175B params, 300B tokens) was **severely undertrained** — at 1.7 tokens/param, it should have used ~3.5T tokens.
- The compute-optimal Chinchilla model is 70B parameters trained on 1.4T tokens (20 tokens/param), using the same compute as GPT-3.

$$
N^* \propto C^{0.5}, \quad D^* \propto C^{0.5}
$$

Both parameters and data should scale equally with compute — Kaplan's $N^{0.74}$ was wrong; it should be $N^{0.5}$.

### Chinchilla: The Proof

To validate the recipe, DeepMind trained Chinchilla: 70B parameters on 1.4T tokens (20:1 ratio), using the same compute as Gopher (280B parameters on 300B tokens, ~1:1 ratio).

| Benchmark            | Gopher 280B | Chinchilla 70B |
|----------------------|-------------|----------------|
| MMLU                 | 41.2%       | 67.5%          |
| BigBench             | 64.4%       | 67.5%          |
| Reading comprehension| 71.6%       | 76.0%          |
| Common sense         | 67.3%       | 72.6%          |

Chinchilla beat Gopher on every benchmark despite being 4× smaller, because it was trained on 4.6× more data. This proved the Chinchilla recipe: smaller models, more data, same compute.

## Why This Mattered

The Chinchilla finding reshaped LLM training across the industry:

- **Llama 1 (2023)**: 7B/13B/33B/65B, all trained with ~20 tokens/param. Llama 65B was trained on 1.4T tokens — same as Chinchilla.
- **Llama 2 (2023)**: similar recipe, 2T tokens.
- **Llama 3 (2024)**: 8B/70B/405B. Llama 3 8B was trained on 15T tokens (1875 tokens/param — far beyond Chinchilla). Llama 3 70B was trained on 15T tokens (214 tokens/param).
- **Mistral 7B (2023)**: trained on ~8T tokens (~1100 tokens/param).
- **Qwen 2.5 (2024)**: similar overtraining.

The trend post-Chinchilla: **overtrain small models**. The Chinchilla ratio of 20:1 is the *compute-optimal* ratio for a single training run, but for models that will be deployed widely (serving millions of users), it's worth spending extra compute at training time to make inference cheaper. A 8B model trained on 15T tokens has the quality of a Chinchilla-optimal 30B model, but inference is 4× cheaper.

## The Three Scaling Regimes

1. **Compute-optimal (Chinchilla)**: 20 tokens per parameter. Best for one-shot training where you don't care about inference cost.
2. **Overtrained (Llama 3)**: 200+ tokens per parameter. Best for models that will be deployed widely — extra training cost is amortized over billions of inference calls.
3. **Undertrained (GPT-3, Gopher)**: <5 tokens per parameter. Almost always a mistake — you're wasting parameters.

## How to Use Scaling Laws in Practice

### Estimating training compute

For a model with $N$ parameters trained on $D$ tokens, the total compute is approximately:

$$
C \approx 6 \cdot N \cdot D \quad \text{FLOPs}
$$

The factor 6 comes from: forward pass is ~2 FLOPs per parameter (1 multiply + 1 add), backward pass is ~4 FLOPs per parameter, and forward+backward together is ~6 FLOPs per parameter per token.

Example: Llama 3 70B trained on 15T tokens: $C = 6 \times 70 \times 10^9 \times 15 \times 10^{12} = 6.3 \times 10^{24}$ FLOPs.

### Estimating training time

On H100 GPUs at ~50% MFU (model FLOPs utilization), each GPU delivers ~500 TFLOPs/s for bf16 training. With 16,000 H100s:

$$
\text{Time} = \frac{6.3 \times 10^{24}}{16000 \times 500 \times 10^{12}} \approx 7.9 \times 10^5 \text{ seconds} \approx 9 \text{ days}
$$

This matches reported Llama 3 70B training times.

### Estimating cost

At ~$2/GPU-hour for H100 spot pricing:

$$
\text{Cost} = 16000 \text{ GPUs} \times 9 \text{ days} \times 24 \text{ hr/day} \times \$2/\text{hr} \approx \$6.9M
$$

For frontier models, the cost is dominated by GPU rental. Chinchilla scaling laws let you estimate this before training, which is essential for budgeting.

## Empirical Comparison

| Model       | Parameters | Training tokens | Tokens/param | Compute (FLOPs) | Notes                  |
|-------------|------------|-----------------|--------------|-----------------|------------------------|
| GPT-3       | 175B       | 300B            | 1.7          | 3.1 × 10²³       | Kaplan recipe, undertrained |
| Gopher      | 280B       | 300B            | 1.1          | 5.0 × 10²³       | Kaplan recipe, undertrained |
| Chinchilla  | 70B        | 1.4T            | 20           | 5.9 × 10²³       | Chinchilla-optimal     |
| Llama 2 70B | 70B        | 2T              | 28.6         | 8.4 × 10²³       | Slight overtrain       |
| Llama 3 8B  | 8B         | 15T             | 1875         | 7.2 × 10²³       | Heavily overtrained    |
| Llama 3 70B | 70B        | 15T             | 214          | 6.3 × 10²⁴       | Heavily overtrained    |
| Llama 3 405B| 405B       | 15T             | 37           | 3.6 × 10²⁵       | Slight overtrain       |
| DeepSeek-V3 | 671B (37B active) | 14.8T    | 22 (effective)| ~6 × 10²⁵       | Compute-optimal for MoE |

## Why This Matters for AI

- **Scaling laws made LLM training predictable**: instead of guessing, you can compute how much compute a target quality requires. This is essential for budgeting, planning, and comparing models.
- **Chinchilla reshaped the field**: every lab now trains with the Chinchilla ratio (or overtrains beyond it). Undertrained models like GPT-3 are a thing of the past.
- **Overtraining is the new normal**: for deployed models, the Chinchilla ratio is a lower bound. Spending extra training compute to reduce inference cost is the dominant strategy.
- **Scaling laws inform hardware design**: knowing that compute scales as $6ND$ tells you how much FLOP/s you need, which drives GPU design (Tensor Cores, FP8, NVLink).
- **Scaling laws predict capability emergence**: certain capabilities (in-context learning, chain-of-thought) emerge at specific scales predicted by the loss curves. This is debated but suggestive.

## Production Implications

- **For training a new model**: use the Chinchilla ratio (20 tokens/param) as a minimum. For models you'll deploy widely, overtrain 5–50× (Llama 3 style).
- **For estimating training cost**: $C \approx 6ND$ FLOPs. Divide by GPU FLOP/s and MFU to get GPU-hours. Multiply by $/GPU-hour to get cost.
- **For choosing a model for deployment**: prefer overtrained small models (Llama 3 8B) over compute-optimal larger models (Chinchilla 70B) — same quality, cheaper inference.
- **For fine-tuning**: scaling laws apply to fine-tuning too, but with different constants. LoRA fine-tuning typically uses 1–10% of the data that full fine-tuning would use.
- **For budgeting**: scaling laws let you answer "how much compute do I need to reach quality X?" before training. This is essential for project planning.

## Common Pitfalls

- **Undertraining**: training a 7B model on 100B tokens (14 tokens/param) — below Chinchilla. The model will be ~30% worse than it could be.
- **Ignoring MFU**: $6ND$ is the theoretical FLOPs. Actual training time is $6ND / (\text{MFU} \times \text{GPU FLOP/s})$. MFU is typically 30–50%, not 100%.
- **Comparing compute across architectures**: a 70B Transformer and a 70B MoE have different effective compute. MoE with 16 experts, top-2 routing has ~12B active parameters; compute per token is $6 \times 12B \times D$, not $6 \times 70B \times D$.
- **Forgetting embedding parameters**: Kaplan's law is for non-embedding parameters. For modern LLMs with large vocabularies (128k), embedding parameters can be ~10% of total — include or exclude consistently.
- **Assuming scaling laws predict emergence**: scaling laws predict loss, not specific capabilities. Capability emergence (ICL, CoT) is correlated with loss but not perfectly predicted by it.

## Further Reading

- Kaplan et al. (2020), *Scaling Laws for Neural Language Models*. arXiv:2001.08361.
- Hoffmann et al. (2022), *Training Compute-Optimal Large Language Models*. arXiv:2203.15556 (Chinchilla).
- DeepSeek-AI (2024), *DeepSeek-V3 Technical Report* — section on scaling laws and MoE.
- Hoffmann et al. follow-up blog posts on Chinchilla implications.
- Wei et al. (2022), *Emergent Abilities of Large Language Models* — capability emergence and scaling.

## Connection to Other Concepts

- [[11 - Training/Pretraining/01 - Pretraining Objectives and Scaling Laws|Pretraining Objectives and Scaling Laws]] — the chapter-11 deep dive.
- [[11 - Training/Data/03 - Data Pipelines and Deduplication|Data Pipelines and Deduplication]] — Chinchilla increased the demand for high-quality training data.
- [[11 - Training/Distributed Training/02 - Distributed Training|Distributed Training]] — scaling laws drive the need for distributed training.
- [[11 - Training/Optimization/05 - Loss Spikes and Stability|Loss Spikes and Stability]] — large-scale training can have loss spikes despite scaling laws.
- [[08 - LLMs/Evaluation/06 - LLM Benchmarks|LLM Benchmarks]] — how scaling laws translate to benchmark performance.
- [[02 - Mathematics/Optimization/14 - Learning Rate Schedules|Learning Rate Schedules]] — interact with scaling (larger models need more careful LR).
- [[26 - Papers/LLMs/04 - GPT-3 2020|GPT-3 2020]] — the undertrained model Chinchilla corrected.

## Interview Questions

1. **Q: What did Chinchilla (Hoffmann 2022) find that Kaplan (2020) got wrong?**
   A: Kaplan estimated that compute-optimal training scales parameters faster than data ($D \propto N^{0.74}$), suggesting ~5 tokens per parameter. Chinchilla's revised experiments showed both should scale equally ($D \propto N^{0.5}$), giving ~20 tokens per parameter. This means most 2020–2021 models (GPT-3 at 1.7 tokens/param, Gopher at 1.1 tokens/param) were severely undertrained — they could have matched their quality with far fewer parameters and far more data. Chinchilla (70B on 1.4T tokens) outperformed Gopher (280B on 300B tokens) using the same compute.

2. **Q: Estimate the training compute for Llama 3 70B (15T tokens).**
   A: $C \approx 6 \times N \times D = 6 \times 70 \times 10^9 \times 15 \times 10^{12} = 6.3 \times 10^{24}$ FLOPs. The factor 6 comes from: forward pass is ~2 FLOPs per parameter, backward pass is ~4 FLOPs per parameter, total ~6 FLOPs per parameter per token. To convert to time: divide by GPU FLOP/s × MFU. With 16,000 H100s at 500 TFLOPs/s each and 50% MFU: time = $6.3 \times 10^{24} / (16000 \times 500 \times 10^{12} \times 0.5) \approx 1.6 \times 10^6$ seconds ≈ 18 days. Actual Llama 3 70B training took ~6M GPU-hours, which matches this estimate.

3. **Q: Why do modern models like Llama 3 overtrain beyond the Chinchilla ratio?**
   A: For models that will be deployed widely, the Chinchilla ratio is a lower bound. The Chinchilla ratio is optimal for a single training run where you don't care about inference cost. But if you'll serve billions of inference calls, extra training cost is amortized — a 8B model trained on 15T tokens (1875 tokens/param) has the quality of a Chinchilla-optimal 30B model, but inference is 4× cheaper. The tradeoff: spend 5× more at training time to save 4× at inference time, multiplied by billions of calls. For frontier models served at scale, overtraining is the dominant strategy.

4. **Q: How do scaling laws apply to MoE models?**
   A: MoE models have two parameter counts: total (all experts) and active (per-token). Compute per token is $6 \times N_{\text{active}} \times D$, not $6 \times N_{\text{total}} \times D$. For DeepSeek-V3 (671B total, 37B active, 14.8T tokens): compute = $6 \times 37 \times 10^9 \times 14.8 \times 10^{12} = 3.3 \times 10^{24}$ FLOPs. The Chinchilla ratio applies to active parameters, not total — so DeepSeek-V3 is at ~400 tokens per active parameter, heavily overtrained for inference efficiency. MoE lets you decouple quality (total params) from compute (active params), which is why it's so effective for deployed models.

5. **Q: Can scaling laws predict capability emergence (ICL, CoT)?**
   A: Not directly. Scaling laws predict loss, which correlates with capabilities but doesn't perfectly predict them. Some capabilities (basic grammar, common facts) emerge smoothly with loss; others (in-context learning, chain-of-thought) appear to emerge more abruptly at certain scales. The relationship is debated — some researchers argue emergence is an artifact of discontinuous evaluation metrics, others argue it's a real phenomenon. Scaling laws tell you "the model will get better", but not exactly when specific capabilities will appear.

6. **Q: What is the 6ND rule and where does the factor 6 come from?**
   A: The 6ND rule: training a model with $N$ parameters on $D$ tokens requires ~$6ND$ FLOPs of compute. The factor 6 comes from: (a) forward pass = 2 FLOPs per parameter (1 multiply + 1 add) per token, so $2ND$; (b) backward pass = ~4 FLOPs per parameter per token (gradients require more computation than the forward), so $4ND$; (c) total = $2ND + 4ND = 6ND$. This assumes dense models with standard optimizers (no MoE, no second-order methods). For MoE, replace $N$ with $N_{\text{active}}$. For inference-only compute (no backward), use $2ND$.

## See Also

- [[26 - Papers/MOC|Papers MOC]]
- [[11 - Training/Pretraining/01 - Pretraining Objectives and Scaling Laws|Pretraining Objectives and Scaling Laws]]
- [[11 - Training/Data/03 - Data Pipelines and Deduplication|Data Pipelines and Deduplication]]
- [[11 - Training/Distributed Training/02 - Distributed Training|Distributed Training]]
- [[11 - Training/Optimization/05 - Loss Spikes and Stability|Loss Spikes and Stability]]
- [[08 - LLMs/Evaluation/06 - LLM Benchmarks|LLM Benchmarks]]
- [[26 - Papers/LLMs/04 - GPT-3 2020|GPT-3 2020]]
- [[26 - Papers/2024-2026/28 - DeepSeek-V2 and V3 2024|DeepSeek-V2 and V3 2024]]
