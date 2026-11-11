---
tags: [fine-tuning, lora, peft, low-rank, adapter]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [LoRA, Low-Rank Adaptation, PEFT, Adapter Tuning]
---

# LoRA (Low-Rank Adaptation)

> [!info] TL;DR
> LoRA freezes the pretrained weights and learns **low-rank delta matrices** alongside them. This reduces trainable parameters by 100×–1000×, enables fine-tuning on consumer GPUs, and produces small "adapter" files that can be swapped per task. The dominant parameter-efficient fine-tuning (PEFT) method. This note covers the idea, math, parameter accounting, initialization, scaling, where to apply, rank choice, full implementation, merging, variants, production patterns, and common pitfalls.

## The Idea

A full fine-tune updates every parameter: $\mathbf{W}' = \mathbf{W} + \Delta \mathbf{W}$. Hu et al. (2021) observed that the **update $\Delta \mathbf{W}$ has low intrinsic rank** during fine-tuning — you don't need a full-rank update to adapt the model. This empirical observation is the key insight: fine-tuning doesn't move weights very far in the parameter space, and the movement is concentrated in a low-dimensional subspace.

LoRA factorizes $\Delta \mathbf{W}$ as a product of two small matrices:

$$
\Delta \mathbf{W} = \mathbf{B} \mathbf{A}
$$

where $\mathbf{A} \in \mathbb{R}^{r \times d}$, $\mathbf{B} \in \mathbb{R}^{d \times r}$, and $r \ll d$. Only $\mathbf{A}$ and $\mathbf{B}$ are trained; $\mathbf{W}$ is frozen.

The forward pass becomes:

$$
\mathbf{y} = (\mathbf{W} + \mathbf{B} \mathbf{A}) \mathbf{x} = \mathbf{W} \mathbf{x} + \mathbf{B} \mathbf{A} \mathbf{x}
$$

The two terms can be computed in parallel: the base model does $\mathbf{W} \mathbf{x}$, the adapter does $\mathbf{B} \mathbf{A} \mathbf{x}$, and the results are summed.

### Why Low-Rank Works

The empirical observation is that fine-tuning updates have low intrinsic rank. But why?

Several theories:
1. **Pretrained models already know most of what they need**; fine-tuning just "steers" them slightly. The steering direction is low-dimensional.
2. **Tasks are simpler than pretraining**. Pretraining learns language; fine-tuning learns a specific task. The task-specific adjustment is small.
3. **Information bottleneck**: the gradient signal during fine-tuning is concentrated in a few directions. Most of the parameter space doesn't move much.

Whatever the cause, the empirical result is robust: rank 16-64 captures most of the benefit of full fine-tuning, across tasks and model sizes.

## Parameter Count

For a layer of size $d \times d$:
- Full fine-tune: $d^2$ parameters.
- LoRA rank $r$: $2 d r$ parameters (for $\mathbf{A}$ and $\mathbf{B}$).

The ratio: $\frac{2dr}{d^2} = \frac{2r}{d}$. For $r = 8$ and $d = 4096$, this is $16/4096 \approx 0.4\%$.

### Concrete Numbers (Llama 3 8B)

Llama 3 8B has:
- 32 layers.
- Hidden size 4096.
- Per layer: 7 linear layers (Q, K, V, O, gate, up, down) — but with GQA, K and V are smaller.
- Total parameters: ~8.03B.

With LoRA rank 16 on all linear layers:
- Per layer: ~7 × 2 × 4096 × 16 ≈ 917K parameters.
- All 32 layers: ~29M parameters.
- Ratio: 29M / 8B ≈ 0.36%.

A 7B model with LoRA rank 16 on all attention projections: typically ~20–50M trainable parameters, vs 7B for full fine-tuning. That's a 100–300× reduction.

### Memory Savings

The memory savings are even larger than the parameter savings suggest:
- **Full fine-tune**: parameters (4 bytes × 7B = 28 GB) + Adam optimizer state (8 bytes × 7B = 56 GB) + gradients (4 bytes × 7B = 28 GB) = **112 GB**.
- **LoRA rank 16**: base weights (28 GB, frozen, no optimizer state) + adapters (4 bytes × 29M = 116 MB) + Adam for adapters (8 bytes × 29M = 232 MB) + gradients for adapters (4 bytes × 29M = 116 MB) = **~28.5 GB**.

So LoRA fits a 7B model on a single 32 GB GPU (A100 40GB, A100 80GB, H100 80GB). Full fine-tuning needs 8× A100 80GB.

## Initialization

- $\mathbf{A}$ is initialized with a random Gaussian (Kaiming uniform).
- $\mathbf{B}$ is initialized with zeros.

So $\mathbf{B} \mathbf{A} = 0$ at the start of training — the model behaves exactly like the pretrained model. LoRA then "grows" the delta from zero. This is essential for stable training: the model starts from the pretrained state and gradually adapts.

Without this initialization (e.g., both random), the model would start in a random state and might not recover the pretrained behavior.

## Scaling Factor

LoRA scales the delta by $\alpha / r$:

$$
\mathbf{y} = \mathbf{W} \mathbf{x} + \frac{\alpha}{r} \mathbf{B} \mathbf{A} \mathbf{x}
$$

$\alpha$ is a hyperparameter (typically $2r$ or matched to $r$). The scaling lets you change $r$ without re-tuning the learning rate — $\alpha / r$ keeps the effective update magnitude roughly constant.

### Why $\alpha / r$?

The product $\mathbf{B} \mathbf{A}$ has magnitude that scales with $r$ (more parameters → larger potential updates). Dividing by $r$ normalizes this, so the effective update magnitude is independent of $r$. This lets you sweep $r$ without re-tuning LR.

Common choices:
- $\alpha = r$: scaling = 1.0. Simplest.
- $\alpha = 2r$: scaling = 2.0. Slightly stronger updates.
- $\alpha = 16$ (fixed): lets you change $r$ without changing $\alpha$. Common in practice.

## Where to Apply LoRA

In the original paper, LoRA was applied only to attention projections ($\mathbf{W}_Q, \mathbf{W}_V$). Empirically:
- Applying LoRA to **all linear layers** (Q, K, V, O, FFN up, FFN down) gives better quality at the same parameter count.
- Applying LoRA only to attention is cheaper but lower quality.
- Applying LoRA only to FFN misses the attention adjustments.

Modern practice: apply LoRA to all linear layers (sometimes called "LoRA all-linear"). The HuggingFace PEFT library supports this via `target_modules="all-linear"`.

### Why All Linear Layers?

- **Attention** (Q, K, V, O): controls information routing. LoRA here adapts which tokens attend to which.
- **FFN** (gate, up, down): controls feature transformation. LoRA here adapts what features are extracted.

For most tasks, both need adjustment. Skipping either limits the adapter's capacity.

### What About Embeddings?

LoRA can also be applied to embedding layers (token embeddings, output projection). This is less common but useful for vocabulary adaptation (e.g., adding new tokens for a domain).

For most use cases, freeze embeddings. Apply LoRA only to attention and FFN.

## Rank Choice

| Rank $r$ | Trainable params (7B, all-linear) | Use case                              |
|----------|-----------------------------------|---------------------------------------|
| 4–8      | ~10–20M                           | Small adaptations (style, tone)       |
| 16–32    | ~30–60M                           | Standard fine-tuning                  |
| 64–128   | ~100–250M                         | Large domain shifts                   |
| 256+     | ~500M+                            | Approaching full FT quality           |

Higher rank = more capacity but more parameters and more overfitting risk. For most tasks, $r = 16$ or $r = 32$ is a good default.

### How to Choose

- **Start with $r = 16$**. If quality is insufficient, try $r = 32$, then $r = 64$.
- **For style/tone adaptation** (small changes), $r = 8$ is often enough.
- **For domain shifts** (e.g., general → medical), $r = 64$ or higher.
- **For new capabilities** (e.g., learning to use new tools), $r = 128$+ may be needed.
- **If $r = 256$ is needed**, consider full fine-tuning. The PEFT benefit is diminishing.

### Empirical Findings

Studies (and the original LoRA paper) show:
- $r = 8$ captures ~90% of full FT quality on many tasks.
- $r = 32$ captures ~95%.
- $r = 128$ captures ~98-99%.
- Beyond $r = 128$, diminishing returns.

But this varies by task. Hard tasks (large domain shifts) need higher rank.

## Implementation (PyTorch)

### From Scratch

```python
import torch
import torch.nn as nn

class LoRALinear(nn.Module):
    def __init__(self, base_linear: nn.Linear, r=8, alpha=16, dropout=0.0):
        super().__init__()
        self.base = base_linear  # frozen
        for p in self.base.parameters():
            p.requires_grad = False
        
        d_in = base_linear.in_features
        d_out = base_linear.out_features
        self.alpha = alpha
        self.scaling = alpha / r
        self.r = r
        
        # A: (r, d_in), B: (d_out, r)
        self.lora_A = nn.Parameter(torch.zeros(r, d_in))
        self.lora_B = nn.Parameter(torch.zeros(d_out, r))
        nn.init.kaiming_uniform_(self.lora_A, a=5**0.5)
        # B stays zero (so BA = 0 at init)
        
        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()
    
    def forward(self, x):
        # base(x) + scaling * B(A(dropout(x)))
        base_out = self.base(x)
        lora_out = self.dropout(x) @ self.lora_A.T @ self.lora_B.T
        return base_out + self.scaling * lora_out
    
    def merge(self):
        """Merge LoRA into base weights for inference."""
        with torch.no_grad():
            delta = self.scaling * (self.lora_B @ self.lora_A)
            self.base.weight.add_(delta)
            self.lora_A = None
            self.lora_B = None
```

### Using HuggingFace PEFT

In practice, use HuggingFace's `peft` library:

```python
from peft import LoraConfig, get_peft_model, TaskType

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)
model = get_peft_model(base_model, config)

# Print trainable parameters
model.print_trainable_parameters()
# Output: trainable params: 29,491,712 || all params: 8,030,269,440 || trainable%: 0.367%
```

### Training Loop

The training loop is the same as full fine-tuning, but only LoRA parameters are trainable:

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./lora-output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=1e-4,  # higher than full FT (1e-5)
    warmup_steps=100,
    logging_steps=10,
    save_steps=500,
    bf16=True,  # mixed precision
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)
trainer.train()

# Save adapter (small file, ~50 MB for rank 16)
model.save_pretrained("./lora-output")
```

### Inference with LoRA

```python
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B")

# Load adapter
model = PeftModel.from_pretrained(base_model, "./lora-output")

# Option 1: keep adapter separate (swap-able)
output = model.generate(...)

# Option 2: merge adapter into base (faster, no swap)
model = model.merge_and_unload()
output = model.generate(...)
```

## Merging Back

For inference, you can either:
1. **Keep LoRA separate**: run $\mathbf{W} \mathbf{x} + \mathbf{B} \mathbf{A} \mathbf{x}$. Slight overhead (extra matmul), but adapters are swap-able at runtime.
2. **Merge** it back into $\mathbf{W}$: $\mathbf{W}' = \mathbf{W} + \frac{\alpha}{r} \mathbf{B} \mathbf{A}$. Same forward pass as a full fine-tuned model with **zero inference overhead**.

Merging gives the same quality as separate LoRA, with no inference cost. This is one of LoRA's biggest advantages over other PEFT methods (adapters, prefix tuning) which always have inference overhead.

```python
# Merge for deployment
model = model.merge_and_unload()
model.save_pretrained("./merged-model")
```

### When to Merge vs. Keep Separate

- **Merge**: single-task deployment, maximum inference speed, no need to swap adapters.
- **Keep separate**: multi-tenant serving with many adapters, A/B testing, dynamic adapter selection.

vLLM, SGLang, and other serving engines support both modes. Multi-LoRA serving (keeping many adapters in memory and swapping per request) is increasingly common for multi-tenant deployments.

## Why This Matters for AI

- LoRA democratized LLM fine-tuning. You can fine-tune a 7B model on a single 24 GB GPU (vs 8× H100 for full fine-tuning).
- LoRA adapters are tiny (10–500 MB) — you can store many per task and swap them at inference.
- LoRA is the basis for most production fine-tuning today. Custom LLM services (chatbots, coding assistants, RAG) typically use LoRA adapters on top of an open base model.
- The low-rank observation is **deeply true** — it suggests that fine-tuning is mostly small, low-dimensional adjustments rather than full re-learning.
- Multi-LoRA serving enables cost-effective personalization: one base model + many small adapters, each serving a different user or task.

## Production Implications

- **For most fine-tuning tasks, start with LoRA.** Move to full FT only if LoRA quality is insufficient (rare).
- **Use merged weights for inference** — same quality, no overhead. Unless you need multi-LoRA serving.
- **Multi-tenant serving**: load multiple LoRA adapters and swap them per request. vLLM, SGLang, and others support this. This enables per-user or per-task customization at low cost.
- **Storage**: keep base model + many adapter files. A 7B base + 100 LoRAs is ~14 GB + 100 × 50 MB = 19 GB total. Vs. 100 full fine-tuned models = 1.4 TB.
- **Versioning**: version adapters separately from the base model. An adapter is compatible only with the base it was fine-tuned on. Store the base model hash with each adapter.
- **Learning rate**: LoRA typically needs higher LR than full FT (1e-4 to 1e-3 vs 1e-5 to 1e-4). The small parameter count means each parameter needs to move more.
- **Batch size**: LoRA's small memory footprint allows larger batch sizes. This can speed up training significantly.
- **Multi-GPU**: LoRA can be trained on a single GPU, but for large datasets, multi-GPU (DDP) speeds things up. FSDP is overkill for LoRA (the trainable params are small).

## Common Pitfalls

- **Too low rank** — underfits; model can't learn the task. Try $r = 16$ minimum.
- **Too high rank** — overfits and loses the parameter-efficiency benefit. If $r = 256$ is needed, consider full FT.
- **Forgetting to apply to FFN** — FFN has most of the parameters; skipping it limits capacity. Always include FFN modules.
- **Wrong learning rate** — LoRA typically needs higher LR than full FT (1e-4 to 1e-3 vs 1e-5 to 1e-4). Too low → slow convergence; too high → instability.
- **Forgetting to merge for inference** — keeping LoRA separate wastes compute. Merge unless you need multi-LoRA.
- **Mixing adapters across base models** — adapters are tied to a specific base model. Don't mix. The adapter's `base_model_name_or_path` field documents this.
- **Forgetting to save the tokenizer** — LoRA adapters don't include the tokenizer. Save it alongside the adapter.
- **Wrong target modules** — different models name their linear layers differently. Check the model's architecture before specifying `target_modules`.
- **Forgetting dropout** — LoRA dropout (0.05-0.1) helps regularization. Don't set to 0 unless you're sure.
- **Not using bf16** — train in bf16 to halve memory. The base model can stay in fp32; only LoRA params need gradients.
- **Forgetting to set `requires_grad=False` on base** — if you forget, you'll train the full model, defeating the purpose. PEFT handles this automatically.
- **Not validating before merging** — always evaluate the unmerged model first. If quality is bad, merging won't fix it.

## Variants

### QLoRA

LoRA on top of a 4-bit quantized base. The base model is loaded in 4-bit NF4 quantization; LoRA adapters are trained in bf16 on top. This enables fine-tuning a 70B model on a single 48 GB GPU.

See [[02 - QLoRA]] for details.

### DoRA (Weight-Decomposed Low-Rank Adaptation)

Decomposes weights into magnitude and direction, applies LoRA to direction only. Slightly better quality than vanilla LoRA at the same parameter count.

$$
\mathbf{W}' = \frac{\mathbf{W} + \mathbf{B}\mathbf{A}}{\|\mathbf{W} + \mathbf{B}\mathbf{A}\|} \cdot \text{magnitude}
$$

### ReLoRA

Periodically resets $\mathbf{A}, \mathbf{B}$ and merges into $\mathbf{W}$. This allows LoRA to escape its low-rank constraint over training — each "reset" starts a new low-rank adaptation from the current merged weights, accumulating higher-rank updates over time.

### PiSSA

Initializes $\mathbf{A}, \mathbf{B}$ from the SVD of $\mathbf{W}$ rather than randomly. The adapter starts as the principal components of the original weight, leading to faster convergence and slightly better final quality.

### LoRA+

Uses different learning rates for $\mathbf{A}$ and $\mathbf{B}$ ($\mathbf{B}$ gets a higher LR). Theoretically motivated by the observation that $\mathbf{A}$ and $\mathbf{B}$ play asymmetric roles.

### MoLoRA / LoRAMoE

Multiple LoRA adapters as experts with routing. Each token is routed to the most relevant LoRA expert. Enables multi-task adaptation in a single adapter set.

### GaLore

Gradient Low-Rank Projection: applies low-rank to the gradient rather than the weights. Different mechanism, similar memory savings.

## Comparison to Other PEFT Methods

| Method          | Trainable Params | Inference Overhead | Quality | Maturity |
|-----------------|------------------|---------------------|---------|----------|
| LoRA            | 0.1-1%           | Zero (after merge)  | High    | Mature   |
| QLoRA           | 0.1-1%           | Zero (after merge)  | High    | Mature   |
| Adapters        | 1-5%             | Small               | Medium  | Mature   |
| Prefix Tuning   | <0.1%            | Small               | Medium  | Mature   |
| Prompt Tuning   | <0.1%            | Zero                | Low     | Mature   |
| DoRA            | 0.1-1%           | Zero (after merge)  | High    | Newer    |
| Full FT         | 100%             | Zero                | Highest | Mature   |

LoRA dominates because it combines parameter efficiency, zero inference overhead (after merge), and high quality. Most production fine-tuning uses LoRA or QLoRA.

## Worked Example: Fine-Tuning a Chat Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset
from trl import SFTTrainer

# Load base model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B")

# Apply LoRA
config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)
model = get_peft_model(model, config)

# Load dataset
dataset = load_dataset("your-chat-dataset", split="train")

# Train
training_args = TrainingArguments(
    output_dir="./lora-chat",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  # effective batch size 16
    learning_rate=2e-4,
    warmup_steps=100,
    logging_steps=10,
    save_steps=500,
    bf16=True,
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
)
trainer.train()

# Save adapter (~50 MB)
model.save_pretrained("./lora-chat")
tokenizer.save_pretrained("./lora-chat")

# For deployment: merge
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./lora-chat-merged")
```

## Interview Questions

- **Q: Why does LoRA work? Why can a low-rank update approximate full fine-tuning?**  
  A: Empirically, fine-tuning updates have low intrinsic rank. The pretrained model already knows most of what it needs; fine-tuning makes small, low-dimensional adjustments. Rank 16-64 captures most of the benefit.

- **Q: How does LoRA's parameter count compare to full fine-tuning?**  
  A: For a 7B model with rank 16 on all linear layers, LoRA has ~30M trainable parameters vs 7B for full FT — a 200× reduction. Memory savings are even larger (no optimizer state for frozen weights).

- **Q: Why initialize B to zero?**  
  A: So that $\mathbf{B}\mathbf{A} = 0$ at the start, meaning the model behaves exactly like the pretrained model. LoRA then "grows" the delta from zero. Without this, the model would start in a random state and might not recover pretrained behavior.

- **Q: When would you merge LoRA vs. keep it separate?**  
  A: Merge for single-task deployment (zero inference overhead). Keep separate for multi-tenant serving (swap adapters per request), A/B testing, or dynamic adapter selection.

- **Q: How does QLoRA differ from LoRA?**  
  A: QLoRA loads the base model in 4-bit NF4 quantization, then trains LoRA adapters in bf16 on top. This enables fine-tuning a 70B model on a single 48 GB GPU. LoRA assumes the base model is in full precision.

- **Q: Why apply LoRA to all linear layers, not just attention?**  
  A: FFN layers have most of the model's parameters. Skipping FFN limits the adapter's capacity. Applying LoRA to all linear layers (Q, K, V, O, gate, up, down) gives better quality at the same parameter count.

## Further Reading

- Hu et al. (2021), *LoRA: Low-Rank Adaptation of Large Language Models*. See [[06 - LoRA 2021]].
- Dettmers et al. (2023), *QLoRA: Efficient Finetuning of Quantized LLMs*.
- Liu et al. (2024), *DoRA: Weight-Decomposed Low-Rank Adaptation*.
- HuggingFace PEFT docs: https://huggingface.co/docs/peft
- Sebastian Raschka's LoRA analysis: https://magazine.sebastianraschka.com/p/lora-and-dora-from-scratch

## See Also

- [[02 - QLoRA]] — quantized base + LoRA
- [[04 - DPO Derivation]] — fine-tuning with preferences (can be combined with LoRA)
- [[05 - RLHF with PPO]] — RL fine-tuning (can use LoRA)
- [[03 - Instruction Tuning and Chat Templates]] — instruction tuning (typically with LoRA)
- [[12 - Fine-Tuning/MOC|Fine-Tuning MOC]]
- [[04 - Matrix Multiplication]] — the math behind low-rank
- [[05 - Matrix Decomposition]] — SVD, which inspires PiSSA
- [[06 - LoRA 2021]] — the original paper
