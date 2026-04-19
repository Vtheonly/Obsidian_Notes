## 4.6 Teacher Forcing and Exposure Bias

### The Training vs. Inference Discrepancy: The Fundamental Problem

To understand why Teacher Forcing exists and why it introduces Exposure Bias, you must first precisely understand the difference between how the decoder operates during training and how it operates during inference.

#### Inference: True Autoregression

During inference, the decoder operates in a strictly sequential, feedback loop:

**Step 0:** Input = `[<sos>]`. Decoder outputs probability distribution. Sample: `\frac`.

**Step 1:** Input = `[<sos>, \frac]`. Decoder outputs probability distribution. Sample: `{`.

**Step 2:** Input = `[<sos>, \frac, {]`. Decoder outputs probability distribution. Sample: `a`.

**Step 3:** Input = `[<sos>, \frac, {, a]`. Decoder outputs probability distribution. Sample: `+`.

Each step's output directly becomes the next step's input. This is called **autoregressive decoding** because the sequence autoregressively generates itself.

The computational cost: if the target sequence has $T$ tokens, you must run the decoder $T$ times sequentially. You cannot run step $t+1$ until step $t$ is complete because you need step $t$'s output as input to step $t+1$. Each decoder forward pass involves matrix multiplications across all attention layers. For $T = 150$ and a deep decoder, this is 150 sequential GPU operations.

#### Naive Training: Sequential Feedback

If you trained using the same autoregressive process, the training loop would look like:

```
For each training sample:
    For t = 1 to T:
        prediction_t = decoder([sos, pred_1, ..., pred_{t-1}])
        loss_t = cross_entropy(prediction_t, ground_truth_t)
    loss = sum(loss_t for all t)
    loss.backward()
```

The problem with this approach has two dimensions:

**Problem 1: Serial computation, no GPU parallelism.**

Modern GPUs are designed for massive parallel computation. Processing one token at a time across 150 sequential steps means the GPU is almost entirely idle, waiting for each step to complete before starting the next. Training would take roughly 150 times longer than necessary.

**Problem 2: Error compounding destroys gradient quality.**

In the first epoch of training, the model's weights are random initialization. A random model predicts essentially random tokens. At step 1, it might predict `z` when the correct token is `\frac`. At step 2, it receives `[<sos>, z]` as context (completely wrong) and predicts `@` (random garbage again). By step 5, the decoder is in a state `[<sos>, z, @, !, *, %]` that it will essentially never see during inference on real data.

The gradients computed from this completely wrong trajectory are nearly meaningless noise. They tell the model "given the state `[<sos>, z, @, !, *, %]`, the output should have been `{`" — which is a training signal for a scenario that will essentially never occur after the model starts learning. The useful training signal (what to predict after a correct prefix) is completely overwhelmed by gradients from impossible garbage states.

---

### Teacher Forcing: The Solution

Teacher Forcing resolves both problems simultaneously by a simple change: instead of using the model's own predictions as context for the next step, always use the correct ground-truth tokens.

**Teacher Forcing conceptual flow:**

```
Ground truth sequence: [<sos>, \frac, {, a, +, b, }, {, c, }, <eos>]

Decoder input:  [<sos>, \frac, {, a, +, b, }, {, c, }]  ← ground truth (shifted right)
Decoder target: [\frac, {, a, +, b, }, {, c, }, <eos>]  ← ground truth (shifted left)

At every position, predict the NEXT token given ALL PREVIOUS CORRECT tokens.
```

**The parallelization trick:**

Because we have the entire target sequence available during training, we can pass the entire "decoder input" sequence into the decoder in a single forward pass, computing predictions for all positions simultaneously:

```python
# Single forward pass, not T sequential passes
all_predictions = decoder(
    tgt=target_sequence_shifted_right,   # [B, T, D]
    memory=encoder_output,               # [B, N_patches, D]
    tgt_mask=causal_mask                 # [T, T] upper-triangular -inf mask
)
# all_predictions has shape [B, T, vocab_size]
# all_predictions[:, t, :] predicts the token at position t+1
# conditioned on positions 0 to t (enforced by causal mask)
```

The causal mask (upper-triangular matrix of $-\infty$) prevents position $t$ from attending to positions $t+1, t+2, \ldots, T$. This ensures that even though all positions are computed in one parallel forward pass, each position's prediction only depends on tokens before it — exactly as in true autoregressive decoding.

**Why this eliminates Problem 1:**

All $T$ positions are computed simultaneously in one GPU operation. Training speed improves by approximately $T \times$ compared to sequential decoding. For $T = 150$, that is a 150× speedup in the decoder computation.

**Why this eliminates Problem 2:**

The model is always conditioned on correct context. At position 3, the context is `[<sos>, \frac, {]` — exactly what the context would be after 3 correct predictions. The training signal is always meaningful: given this correct partial sequence, what is the next token? The gradients converge cleanly and quickly.

---

### Exposure Bias: The Problem Teacher Forcing Creates

Teacher Forcing is not a free lunch. By always providing correct context during training, it creates a systematic discrepancy between the distribution of states the model sees during training and the distribution of states it sees during inference.

**Formal definition of Exposure Bias:**

During training, the model learns the conditional distribution:

$$P_{\text{train}}(y_t \mid y_1^*, y_2^*, \ldots, y_{t-1}^*)$$

Where $y_1^*, \ldots, y_{t-1}^*$ are the ground truth tokens.

During inference, the model must compute:

$$P_{\text{inf}}(y_t \mid \hat{y}_1, \hat{y}_2, \ldots, \hat{y}_{t-1})$$

Where $\hat{y}_1, \ldots, \hat{y}_{t-1}$ are the model's own previous predictions.

If the model is perfect (all $\hat{y}_i = y_i^*$), then $P_{\text{train}} = P_{\text{inf}}$ and there is no problem.

But the model is not perfect. Suppose at position 2, the model predicts `\sqrt` with probability 0.85 but the correct token is `\frac` with probability 0.15. The model made the wrong choice. At position 3, the inference context is now `[<sos>, \sqrt]`. The model has never seen this context during training (because training always used the correct prefix). The model is in a completely unfamiliar state and must extrapolate its predictions to an out-of-distribution input.

**The cascade of errors:**

Each prediction error shifts the context further from the distribution seen during training. The error compounds because:
- Wrong token at step 2 → unfamiliar context at step 3.
- Unfamiliar context at step 3 → higher probability of another wrong prediction at step 3.
- Second wrong token at step 3 → even more unfamiliar context at step 4.

This cascade is called **error propagation** or **compounding errors**. Sequence models trained with Teacher Forcing tend to be well-calibrated for the first few tokens and increasingly unreliable for later tokens in long sequences.

**Why this is particularly bad for mathematical OCR:**

In natural language translation, a sentence with one wrong word might still be partially understandable. In LaTeX, a single misplaced `{` can make the entire formula fail to compile. The cascading error problem is more consequential in LaTeX than in natural language because LaTeX has strict syntactic requirements.

Furthermore, mathematical expressions often have critical structural tokens at positions 3-20 (e.g., `\begin{matrix}` often appears early in the sequence). If the model makes an error before this structural token, the error cascade begins precisely at the moment when the most structurally important decisions are being made.

---

### How TAMER Mitigates Exposure Bias

TAMER uses three complementary mechanisms to counteract the exposure bias introduced by Teacher Forcing.

#### Mechanism 1: Hard Grammar Constraints (Primary Defense)

The grammar mask system (Chapter 6.2) prevents the most consequential exposure bias errors by making structurally invalid token sequences mathematically impossible.

Consider the exposure bias scenario where the model predicts `\sqrt` instead of `\frac`. Under normal circumstances, this starts an error cascade. But TAMER's grammar state machine immediately analyzes the state after `\sqrt` is predicted and enforces that the next token must be `{` (since `\sqrt` requires a brace group argument). 

The grammar mask converts the model's probability distribution at step $t+1$ to:

$$P_{\text{masked}}(y_{t+1}) = \begin{cases} P(y_{t+1}) & \text{if token } y_{t+1} \text{ is grammatically valid} \\ 0 & \text{otherwise} \end{cases}$$

Even though the model is now in an out-of-distribution state (wrong command name), the grammar mask forces the subsequent tokens into a valid structural pattern. The formula may have the wrong function, but it will not catastrophically collapse into grammatically invalid gibberish.

#### Mechanism 2: Beam Search (Secondary Defense)

Beam Search (Chapter 6.1) maintains $K = 5$ candidate sequences simultaneously. When one beam makes a prediction error at step $t$ and enters a low-probability out-of-distribution state, its cumulative sequence score decreases. At some future step, this low-probability beam will be pruned from the top-$K$, and the highest-scoring beam (which made fewer errors and stayed in higher-probability, more in-distribution states) survives.

Effectively, Beam Search runs $K$ parallel autoregressive attempts. Beams that encounter exposure bias errors self-destruct (their score drops). Beams that remain accurate survive. The final output is selected from the surviving beam.

The exposure bias mitigation effectiveness scales with $K$: a larger beam width means more parallel attempts and a higher probability that at least one beam avoids the cascade. This is why increasing beam width from 1 (greedy) to 5 typically improves ExpRate by 3-8 percentage points on math OCR tasks.

#### Mechanism 3: Scheduled Sampling (Optional Advanced Defense)

Scheduled Sampling (Bengio et al., 2015) directly attacks the root cause of Exposure Bias by gradually introducing the model's own predictions as context during training, bridging the gap between training distribution and inference distribution.

The schedule works as follows. During early training epochs, Teacher Forcing is used 100% of the time (fully correct context, rapid convergence). As training progresses, with increasing probability $p_{\text{sample}}$, the model's own prediction from the previous step is used as context instead of the ground truth.

$$p_{\text{sample}}(\text{epoch}) = 1 - \frac{k}{k + \exp(\text{epoch}/k)}$$

Where $k$ is a hyperparameter controlling how fast the schedule increases. The sigmoid-like shape ensures $p_{\text{sample}} \approx 0$ in early training and $p_{\text{sample}} \to 1$ in late training.

The key technical challenge: during Scheduled Sampling, when the model's own prediction is used as context, the computation graph becomes non-differentiable at the token-selection step (argmax or sampling are not differentiable operations). TAMER addresses this using the **Straight-Through Estimator**: during the forward pass, use the sampled token; during the backward pass, approximate the gradient as if the argmax was a differentiable operation (treat it as an identity function for gradient computation). This is a biased gradient estimator but empirically works well.

> **Critical reminder:** Scheduled Sampling should only be enabled after the model has partially converged with full Teacher Forcing. If Scheduled Sampling is enabled from epoch 1, the model receives noisy context from the very beginning, which severely slows convergence. The standard practice in TAMER is to use full Teacher Forcing for the first 20 epochs, then gradually increase $p_{\text{sample}}$ over epochs 21-60. By epoch 60, the model is trained predominantly on its own predictions, which closely matches the inference distribution.

---