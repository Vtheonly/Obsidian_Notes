## 4.7 Scheduled Sampling: Bridging the Training-Inference Gap

### Why Beam Search Alone Is Insufficient

Beam Search and Grammar Masks reduce the consequences of Exposure Bias but do not eliminate the underlying distribution mismatch. The model's internal attention states when processing an incorrect context are still different from what it was trained on, even if the grammar mask prevents catastrophic token output.

Scheduled Sampling directly addresses the distribution mismatch by training the model on mixed correct and incorrect contexts. After Scheduled Sampling training, the model has seen many examples of "what to do when you are in a slightly wrong state." Its attention mechanism has learned to be more robust to context imperfections.

### The Probability Schedule: Mathematical Detail

TAMER uses the **inverse sigmoid decay** schedule for $p_{\text{sample}}$:

$$p_{\text{use\_own\_prediction}}(\text{epoch}) = \frac{k}{k + \exp(-(\text{epoch} - \text{epoch}_{start}) / k)}$$

With $k = 10$ and $\text{epoch}_{start} = 20$:

| Epoch | $p_{\text{use\_own\_prediction}}$ | Context Source |
|---|---|---|
| 1-20 | 0.0 | Always ground truth |
| 25 | 0.18 | 18% model predictions |
| 30 | 0.38 | 38% model predictions |
| 40 | 0.62 | 62% model predictions |
| 50 | 0.78 | 78% model predictions |
| 60+ | 0.88 | 88% model predictions |

The schedule never reaches 1.0 (100% own predictions). Keeping 10-15% ground truth prevents the model from fully drifting during late training and maintains a stable anchor to the correct token distribution.

### Implementation: The Token Selection Decision

At each decoding step during training, the decision of whether to use the ground truth or the model's own prediction is made stochastically:

```python
def mixed_teacher_forcing_step(decoder, context, ground_truth_token,
                                 p_sample, encoder_memory):
    # Compute prediction based on current context
    logits = decoder(context, encoder_memory)  # [B, V]
    probs = F.softmax(logits, dim=-1)
    
    # Stochastic decision: use model's prediction or ground truth?
    use_own = torch.bernoulli(torch.full((B,), p_sample))  # [B] binary
    
    # Model's best prediction
    predicted_token = probs.argmax(dim=-1)  # [B]
    
    # Select: own prediction or ground truth, per sample in batch
    next_token = torch.where(use_own.bool(), predicted_token,
                              ground_truth_token)
    
    return next_token, logits
```

Note: the `logits` are still computed and used for the loss regardless of whether the predicted token or ground truth was used as the next context. The loss always measures "given the current context, how good was the prediction of the correct next token?" The Scheduled Sampling only affects what becomes the next context, not what target the loss is computed against.

---