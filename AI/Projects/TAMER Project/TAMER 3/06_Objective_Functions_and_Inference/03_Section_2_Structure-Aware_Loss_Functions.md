## 2. Structure-Aware Loss Functions

### Motivation: Not All Errors Are Equal

In a 100-token LaTeX sequence representing a matrix, consider two errors:
1. The model predicts `3` instead of `2` in one entry. The rendered formula has the wrong number in one cell. The LaTeX compiles correctly.
2. The model predicts `+` instead of `&` between two matrix entries. The LaTeX compiler throws an error. The entire formula fails to render.

Standard cross-entropy assigns identical loss weight to both errors (they are both wrong tokens with equal contribution to $\mathcal{L}_{CE}$). This is semantically incorrect. Error 2 is far more damaging and the model should be penalized much more heavily for it.

---

### Implementation of Structure-Aware Loss

TAMER's `StructureAwareLoss` wraps the standard label-smoothed cross-entropy and applies per-token weights based on token identity.

**Structural tokens and their weights:**

| Token | Category | Weight |
|---|---|---|
| `\\` | Row separator | 3.0 |
| `&` | Column separator | 3.0 |
| `\begin{...}` | Environment open | 3.0 |
| `\end{...}` | Environment close | 3.0 |
| `{`, `}` | Group delimiters | 1.5 |
| `^`, `_` | Script markers | 1.5 |
| All others | Content tokens | 1.0 |

**Computation:**

```python
def forward(self, logits, targets, padding_mask):
    # logits: [B, T, V], targets: [B, T]
    base_loss = label_smoothed_cross_entropy(logits, targets)  # [B, T]
    
    # Build weight matrix
    weights = torch.ones_like(targets, dtype=torch.float)
    for token_id, weight in self.structural_weights.items():
        weights[targets == token_id] = weight
    
    # Zero out padding positions
    weights[padding_mask] = 0.0
    
    # Weighted mean loss
    weighted_loss = (base_loss * weights).sum() / weights.sum()
    return weighted_loss
```

**The mathematical effect:**
The gradient for structural token positions is scaled by 3.0:

$$\nabla_\theta \mathcal{L}_{struct} = \sum_{t: y_t \in \text{struct}} 3.0 \cdot \nabla_\theta \mathcal{L}_{CE,t} + \sum_{t: y_t \notin \text{struct}} 1.0 \cdot \nabla_\theta \mathcal{L}_{CE,t}$$

The model receives 3× stronger gradient signal at structural token positions. Over thousands of training steps, this causes the model to allocate disproportionately more of its representational capacity to correctly identifying structural boundaries.

---