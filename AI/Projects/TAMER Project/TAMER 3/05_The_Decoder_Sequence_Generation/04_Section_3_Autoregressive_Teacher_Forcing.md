## 3. Autoregressive Teacher Forcing

### The Training vs Inference Discrepancy

**At inference time**, the decoder is truly autoregressive:
1. Feed `<sos>`.
2. Model predicts token $\hat{y}_1$.
3. Feed `<sos>`, $\hat{y}_1$.
4. Model predicts $\hat{y}_2$.
5. Repeat until `<eos>`.

If $\hat{y}_1$ is wrong (e.g., model predicts `\frac` but the correct token is `\sqrt`), then step 3 feeds the wrong context, and the model produces $\hat{y}_2$ conditioned on wrong information. The error compounds with each step. A mistake at step 1 can corrupt all remaining 99 tokens.

**The training problem:** If we train with the model's own outputs, in the early stages of training the model predicts mostly random garbage. It would always be in error states it has never seen correct versions of, making learning impossible. The gradients would be uninformative noise.

---

### Teacher Forcing: Training-Time Shortcut

During training, instead of using the model's predictions as context, we always use the ground-truth tokens:

- Decoder input at step $t$: $[y_0, y_1, \ldots, y_{t-1}]$ (all ground truth, all correct).
- Decoder output at step $t$: Prediction of $y_t$.

This means even if the model's prediction of $y_{t-1}$ was completely wrong, the input at step $t$ still shows the correct $y_{t-1}$. The model always receives correct context, making learning much faster and more stable.

**Implementation:** Because we know the entire target sequence during training, we can run the full decoder in one forward pass (not T sequential passes) using the causal mask:

```python
# target_ids shape: [Batch, T]
target_input = target_ids[:, :-1]   # All tokens except last: [SOS, y1, y2, ..., yT-1]
target_output = target_ids[:, 1:]   # All tokens except first: [y1, y2, ..., yT, EOS]

# Single forward pass computes predictions for all positions simultaneously
predictions = decoder(target_input, encoder_memory)  # Shape: [Batch, T, Vocab]

# Loss: predictions[:, t, :] should match target_output[:, t]
loss = cross_entropy(predictions, target_output)
```

The causal mask ensures that `predictions[:, t, :]` only used information from `target_input[:, :t]`. This is mathematically identical to running the decoder T times sequentially, but is parallelized and runs in a single GPU kernel call.

> **Critical reminder:** Teacher Forcing creates a training-inference discrepancy called **Exposure Bias**. The model is trained on perfect ground-truth contexts but tested on its own (potentially imperfect) contexts. This is an active research problem. TAMER partially addresses it with **Scheduled Sampling**: in later training epochs, with probability $p$ (which increases over training), the model is forced to use its own predictions instead of ground truth. This bridges the training-inference gap.

---