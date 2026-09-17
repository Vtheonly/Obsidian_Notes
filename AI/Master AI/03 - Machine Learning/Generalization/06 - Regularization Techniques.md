---
tags: [ml, regularization, dropout, weight-decay]
iteration: 2
created: 2026-08-07
aliases: [Regularization Techniques]
---

# 06 - Regularization Techniques

> [!info] TL;DR
> Regularization = any technique that prevents overfitting by constraining the model. L1/L2 penalties, dropout, weight decay, early stopping, data augmentation, label smoothing, batch norm. Each addresses a different failure mode.

## Why Regularize?

Models can fit training data perfectly but generalize poorly ([[01 - Bias Variance Tradeoff|Bias-Variance]]). Regularization trades a small increase in training loss for a larger reduction in test loss by:
- Limiting model capacity.
- Adding noise during training.
- Encouraging simpler solutions.

## L1 and L2 Regularization (Weight Penalties)

Add a penalty to the loss:

$$
L_{\text{reg}} = L + \lambda \cdot R(\mathbf{w})
$$

### L2 (Ridge, Weight Decay)
$$
R(\mathbf{w}) = \|\mathbf{w}\|_2^2 = \sum_i w_i^2
$$

Shrinks weights toward zero (but rarely to exactly zero). Equivalent to MAP with a Gaussian prior ([[02 - Mathematics/Probability/08 - Bayes Theorem Deep Dive|Bayes]]). The standard for neural networks.

In optimizers like AdamW, L2 is implemented as **decoupled weight decay** (multiply weights by $1 - \eta \lambda$ each step) rather than as a gradient penalty. See [[02 - Mathematics/Optimization/13 - Adam Derivation|Adam Derivation]].

### L1 (Lasso)
$$
R(\mathbf{w}) = \|\mathbf{w}\|_1 = \sum_i |w_i|
$$

Produces **sparse** weights (many exactly zero). Useful for feature selection. Equivalent to MAP with a Laplace prior.

### Elastic Net
Combination of L1 and L2:
$$
R(\mathbf{w}) = \alpha \|\mathbf{w}\|_1 + (1-\alpha) \|\mathbf{w}\|_2^2
$$

Useful when features are correlated (L1 alone picks one randomly; Elastic Net keeps groups).

## Dropout (Srivastava et al., 2014)

During training, randomly set a fraction $p$ of activations to zero. At test time, use all activations (scaled to compensate).

```python
# Pseudocode
def dropout_forward(x, p, training):
    if training:
        mask = (torch.rand_like(x) > p).float() / (1 - p)
        return x * mask
    return x
```

### Why it works

- **Ensemble effect**: each forward pass uses a different sub-network. Like bagging, but at the activation level.
- **Noise injection**: prevents co-adaptation (no neuron can rely on any other specific neuron being present).
- **Approximates model averaging** over exponentially many sub-networks.

### Typical rates
- Input layer: 0.1–0.2.
- Hidden layers: 0.3–0.5.
- Attention weights: 0.0–0.1.
- Transformer FFN: 0.0–0.1.

Modern LLMs use **very little dropout** because they rely on data scale and other regularizers. But for small-data fine-tuning, dropout is still valuable.

## Early Stopping

Halt training when validation loss stops improving (or starts worsening):

```python
best_val = float('inf')
patience, waited = 3, 0
for epoch in range(max_epochs):
    train_one_epoch()
    val_loss = evaluate(val_loader)
    if val_loss < best_val:
        best_val = val_loss
        waited = 0
        save_checkpoint()
    else:
        waited += 1
        if waited >= patience:
            break  # early stop
```

**The cheapest, most reliable regularizer.** Always use it unless you have a strong reason not to.

## Data Augmentation

Artificially expand the training data via label-preserving transformations:

- **Images**: flip, crop, rotate, color jitter, mixup, cutmix.
- **Text**: synonym replacement, back-translation, random deletion.
- **Audio**: time stretch, pitch shift, noise injection.

Effective when data is limited. Especially powerful for vision — ImageNet training relies heavily on augmentation.

## Label Smoothing

Instead of one-hot targets `[0, 0, 1, 0]`, use smoothed targets `[0.033, 0.033, 0.9, 0.033]` (smoothing factor $\epsilon = 0.1$).

- Prevents the model from becoming overconfident.
- Acts as calibration regularization.
- Standard in modern image classification (since Szegedy et al. 2016) and used in some LLM training.

## Batch Normalization (Side Effect: Regularization)

BatchNorm normalizes activations using batch statistics. As a side effect, the noise from batch statistics acts as a regularizer. This is part of why BatchNorm improves generalization beyond just faster training.

**Note**: in NLP/Transformers, BatchNorm is rarely used — LayerNorm/RMSNorm is preferred because sequence lengths vary. See [[07 - Transformers/Components/Normalization Layers|Normalization Layers]].

## Weight Tying

Share weights across layers (e.g., input and output embeddings in language models). Reduces parameters, acts as a regularizer (forces the embedding space and output space to be the same).

## Specific to Transformers

- **Dropout** on attention weights and FFN activations.
- **Weight decay** (AdamW).
- **Label smoothing** in classification heads.
- **Attention dropout**: critical for preventing the model from over-relying on a few tokens.

## Specific to LLM Fine-Tuning

- **LoRA's low-rank constraint** is itself a regularizer (limits the rank of weight updates). See [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]].
- **KL penalty in RLHF** prevents the policy from drifting too far from the reference. See [[12 - Fine-Tuning/RLHF/RLHF with PPO|RLHF]] (planned).
- **LoRA dropout**: apply dropout to LoRA's A/B matrices.

## Worked Example

```python
import torch.nn as nn

class RegularizedModel(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.fc1 = nn.Linear(d, d*2)
        self.drop1 = nn.Dropout(0.3)
        self.fc2 = nn.Linear(d*2, d)
        self.drop2 = nn.Dropout(0.1)
    
    def forward(self, x):
        x = self.drop1(torch.relu(self.fc1(x)))
        x = self.drop2(self.fc2(x))
        return x

# Weight decay via optimizer
opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
```

## Why This Matters for AI

- Without regularization, deep networks overfit catastrophically. With it, they generalize across domains.
- The "regularization recipe" is part of what makes modern LLM training work — weight decay + dropout + label smoothing + (implicit) regularization from SGD + scale of data.
- For **fine-tuning** specifically, regularization matters more than for pretraining — you have less data and want to preserve the pretrained model's behavior.

## Production Implications

- **Always use early stopping.** It's free regularization.
- **Weight decay of 0.01–0.1** is a reasonable default for most training. Tune on validation.
- **Dropout in fine-tuning** can help, especially with small data. 0.1 is a good starting point.
- **For LoRA fine-tuning**: keep dropout low (0.05–0.1); the low-rank constraint is already regularizing.
- **Don't apply weight decay to biases or norm parameters** — they don't have a regularization interpretation. Use parameter groups in your optimizer.

## Common Pitfalls

- **Dropout at test time** — never apply dropout during inference. Always check `model.eval()`.
- **Wrong dropout scaling** — PyTorch's `nn.Dropout` uses "inverted dropout" (scales during training), so no test-time adjustment is needed. Old frameworks scaled at test time.
- **Too much regularization** — underfits. Watch training loss; if it can't go down, regularize less.
- **Forgetting to apply regularization to all relevant layers** — typically you skip the output layer.
- **Mixing L1 and L2 without intent** — be deliberate about which you're using and why.

## Further Reading

- Srivastava et al. (2014), *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*.
- Szegedy et al. (2016), *Rethinking the Inception Architecture for Computer Vision* (label smoothing).
- Zhang et al. (2017), *mixup: Beyond Empirical Risk Minimization*.
- Kukačka et al. (2017), *Regularization for Deep Learning: A Taxonomy* (great survey).

## See Also

- [[01 - Bias Variance Tradeoff]]
- [[02 - Mathematics/Optimization/13 - Adam Derivation|Adam Derivation]] (weight decay)
- [[07 - Transformers/Components/Normalization Layers|Normalization Layers]]
- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]]
- [[03 - Machine Learning/MOC|ML MOC]]
