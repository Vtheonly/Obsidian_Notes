---
tags: [interpretability, logit-lens, tuned-lens, probing]
iteration: 4
created: 2026-08-08
aliases: [Logit Lens, Tuned Lens, Intermediate Layer Probing]
---

# 02 — Logit Lens and Tuned Lens

> [!info] TL;DR
> The logit lens applies the model's final unembedding layer (vocabulary projection) to intermediate layer activations, producing probability distributions over the vocabulary at each layer. This reveals what the model is "thinking" at each depth — you can see the prediction forming and updating across layers. The tuned lens extends this with a learned affine transformation per layer to correct for the gap between intermediate and final representations. Together, they provide a simple, model-agnostic window into Transformer computation.

## The Problem Being Solved

[[01 - Mechanistic Interpretability|Mechanistic interpretability]] aims to understand what Transformers compute at each layer. But intermediate activations are high-dimensional vectors with no obvious interpretation — you can't look at a 4096-dimensional vector and tell what it "means".

The final layer's output is interpretable: it's a probability distribution over the vocabulary, and we can read off the top predicted tokens. But by the time we reach the final layer, all the computation is done — we see the result, not the process.

The logit lens (nostalgebraist, 2020) bridges this gap with a simple idea: apply the final unembedding layer (`W_U`) to intermediate activations. This projects each layer's hidden state into the vocabulary space, giving us a probability distribution at every depth.

## The Logit Lens

### The Method
For a Transformer with L layers, hidden dimension d, and vocabulary V:
1. The final layer produces a hidden state `h_L` of shape `(d,)`.
2. The unembedding matrix `W_U` of shape `(V, d)` projects `h_L` to logits: `logits = W_U · h_L` (shape `(V,)`).
3. Softmax over logits gives the output probability distribution.

The logit lens applies this same projection to intermediate hidden states:

```
For each layer l in 1..L:
    h_l = hidden state at layer l  (after the residual stream)
    logits_l = W_U · h_l
    probs_l = softmax(logits_l)
```

Now you have a probability distribution over the vocabulary at each layer. You can:
- Read off the top predicted token at each layer.
- See how the prediction updates across layers.
- Identify layers where the prediction is confident vs. uncertain.
- Detect "prediction flips" — where the model changes its mind.

### What It Reveals
The logit lens revealed several patterns about how Transformers process information:

**Early layers are random-looking**. Layers 1–5 typically produce near-uniform distributions or predict common tokens ("the", "a", "and"). The model is still building up representations.

**Middle layers start predicting the correct token**. Around layer 6–10 (in a 12-layer model), the correct token often appears in the top-K predictions, but not always at rank 1.

**Late layers refine and commit**. The final 2–3 layers sharpen the distribution, moving the correct token to rank 1 and suppressing alternatives.

**Prediction flips are informative**. When the model predicts token A at layer 8 but token B at layer 12, the flip often corresponds to a specific computation (e.g., resolving a coreference, completing an idiom).

### Example Output
For the prompt "The capital of France is", a 12-layer model might show:

| Layer | Top-1 Prediction | Probability |
|-------|------------------|-------------|
| 1     | "the"            | 0.05        |
| 3     | "a"              | 0.04        |
| 5     | "Paris"          | 0.15        |
| 7     | "Paris"          | 0.45        |
| 9     | "Paris"          | 0.78        |
| 11    | "Paris"          | 0.92        |
| 12    | "Paris"          | 0.95        |

This shows the prediction forming at layer 5 and sharpening through layer 12.

## The Tuned Lens

### The Problem with Logit Lens
The logit lens assumes that intermediate hidden states are in the same "space" as the final hidden state — that you can apply `W_U` directly. But this isn't quite right. Each layer's hidden state is transformed by subsequent layers before reaching the output. Applying `W_U` directly to an intermediate state is like applying a translation dictionary to a language it wasn't designed for.

The result: the logit lens works (you can see predictions forming), but the intermediate distributions are noisy and less calibrated than the final distribution.

### The Fix: Learned Affine Transformations
The tuned lens (Belrose et al., 2023) adds a learned affine transformation `T_l` per layer:

```
logits_l = W_U · (T_l(h_l))
         = W_U · (A_l · h_l + b_l)
```

where `A_l` (shape `(d, d)`) and `b_l` (shape `(d,)`) are learned per layer. The transformation "tunes" the intermediate hidden state to be more compatible with the unembedding matrix.

### Training the Tuned Lens
For each layer `l`:
1. Collect hidden states `h_l` on a corpus of text.
2. For each `h_l`, the "target" is the next token `y` (the same target the full model is predicting).
3. Train `A_l, b_l` to minimize cross-entropy between `softmax(W_U · T_l(h_l))` and `y`.

This is a small, fast training loop — you're only learning `A_l, b_l`, not modifying the base model.

### What the Tuned Lens Reveals
The tuned lens produces more calibrated intermediate distributions than the logit lens. Key findings:

**Intermediate layers are more capable than the logit lens suggests**. With proper tuning, layer 6 of a 12-layer model often achieves nearly the same next-token prediction accuracy as the full model. The logit lens underestimates intermediate capability because the untrained `W_U` projection is suboptimal.

**The "capability curve" is smoother**. With the logit lens, capability sometimes appears to jump discontinuously between layers. The tuned lens reveals that capability increases more smoothly — the jumps were artifacts of the projection mismatch.

**Early layers have more information than expected**. Even layer 1–2, with the tuned lens, can sometimes predict the next token above chance — suggesting that the model extracts relevant features very early.

## Comparison

| Aspect                  | Logit Lens             | Tuned Lens                          |
|-------------------------|------------------------|-------------------------------------|
| Method                  | Apply `W_U` directly   | Apply `W_U · T_l` with learned `T_l`|
| Calibration             | Poor at middle layers  | Good across all layers              |
| Training required       | None                   | Small affine model per layer        |
| Computational cost      | Minimal                | Minimal (just a matrix multiply)    |
| Reveals                 | Approximate predictions| Calibrated predictions              |
| Use case                | Quick exploration      | Rigorous analysis                   |

## Applications

### Understanding Model Behavior
For a given prompt, plot the top-K predictions at each layer. This reveals:
- When the model "knows" the answer (which layer first predicts it).
- When the model is uncertain (layers with flat distributions).
- When the model changes its mind (prediction flips).

### Detecting Capabilities and Limitations
Test the model on tasks where you know the answer. The lens reveals whether the model "knows" the answer at intermediate layers even if the final output is wrong — useful for diagnosing where the model fails.

### Comparing Models
Compare the per-layer prediction curves of different models (e.g., GPT-2 vs Llama). This reveals architectural differences in how information is processed.

### Steering Model Behavior
Some research uses the lens to identify layers where specific information is represented, then modifies those activations to steer the model's output (activation patching, representation engineering).

### Training Dynamics
Apply the lens to checkpoints during training. This reveals how the model's internal computation evolves over training — when does it start predicting the correct token at each layer?

## Limitations

### Vocabulary-Biased
Both lenses project to the vocabulary space, which means they can only reveal predictions about tokens. They cannot reveal other information the model computes (syntactic structure, entity tracking, world model) unless that information is reflected in token predictions.

### Layer-Specific, Not Token-Specific
The lens shows what the model predicts at each layer for a specific position, but it doesn't directly reveal what each *attention head* or *neuron* is doing. For that, you need finer-grained techniques (see [[03 - Sparse Autoencoders Deep Dive]] and [[04 - Activation Patching and Causal Tracing]]).

### Tuned Lens Requires Training Data
The tuned lens requires a corpus to train the affine transformations. The choice of corpus affects what the lens reveals — a lens trained on news text might not calibrate well for code.

### Doesn't Explain Causation
The lens shows *what* the model predicts at each layer, not *why*. If the model flips its prediction at layer 8, the lens shows the flip but not which attention heads or neurons caused it.

## Tooling

- **TransformerLens** (Neel Nanda): includes logit lens implementation.
- ** tuned-lens** (Belrose et al.): official implementation of the tuned lens.
- **Ecco** (Explainability for Transformer models): interactive logit lens visualization.
- **Custom**: easy to implement — just apply `W_U` to intermediate hidden states and softmax.

## See Also

- [[01 - Mechanistic Interpretability]]
- [[03 - Sparse Autoencoders Deep Dive]]
- [[04 - Activation Patching and Causal Tracing]]
- [[05 - Probing]]
- [[14 - Interpretability/MOC|14 Interpretability MOC]]
