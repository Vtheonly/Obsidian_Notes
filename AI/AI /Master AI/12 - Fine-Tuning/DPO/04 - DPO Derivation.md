---
tags: [fine-tuning, dpo, alignment, preference-learning]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
---

# DPO Derivation

> [!info] TL;DR
> Direct Preference Optimization (Rafailov et al., 2023) simplifies RLHF by skipping the reward model and the PPO loop. It directly optimizes the policy from preference data via a closed-form loss. DPO and its variants (IPO, KTO, SimPO) are the dominant alignment methods in 2024–2026.

## The Problem with RLHF

Classical RLHF (see [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO|RLHF]] (planned)) has three stages:
1. Train a **reward model** $r_\phi(x, y)$ on preference data.
2. Train a **policy** $\pi_\theta$ with PPO to maximize $r_\phi(x, y) - \beta \text{KL}(\pi_\theta \| \pi_{\text{ref}})$.
3. The reference model $\pi_{\text{ref}}$ is the SFT model, kept frozen.

PPO is finicky: it requires two extra models in memory (reward + reference), needs careful hyperparameter tuning, and has stability issues (reward hacking, KL divergence blowing up). Many practitioners report PPO taking weeks to converge.

## The DPO Insight

Rafailov et al. observed that the **RLHF objective has a closed-form optimal policy**. So instead of solving for the policy with PPO, you can write the policy in terms of the reward, then derive a loss that directly trains the policy to match that closed form — no reward model needed.

## The Derivation

### Step 1: The RLHF objective

The RLHF objective is:

$$
\max_{\pi_\theta} \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(\cdot | x)} \left[ r(x, y) - \beta \log \frac{\pi_\theta(y | x)}{\pi_{\text{ref}}(y | x)} \right]
$$

The KL term keeps the policy close to the reference (prevents reward hacking).

### Step 2: The closed-form solution

This is a standard KL-constrained optimization. The optimal policy is:

$$
\pi^*(y | x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y | x) \exp\left( \frac{r(x, y)}{\beta} \right)
$$

where $Z(x) = \sum_y \pi_{\text{ref}}(y | x) \exp(r(x, y) / \beta)$ is the partition function (intractable to compute, but it cancels out — see next step).

### Step 3: Solve for the reward

Rearranging:

$$
r(x, y) = \beta \log \frac{\pi^*(y | x)}{\pi_{\text{ref}}(y | x)} + \beta \log Z(x)
$$

### Step 4: Plug into the preference model

The reward model is trained on preference pairs $(y_w, y_l)$ (winner, loser) using the Bradley-Terry model:

$$
p(y_w \succ y_l | x) = \sigma(r(x, y_w) - r(x, y_l))
$$

where $\sigma$ is the sigmoid. Substituting the closed-form reward:

$$
p_\theta(y_w \succ y_l | x) = \sigma\left( \beta \log \frac{\pi_\theta(y_w | x)}{\pi_{\text{ref}}(y_w | x)} - \beta \log \frac{\pi_\theta(y_l | x)}{\pi_{\text{ref}}(y_l | x)} \right)
$$

The $\log Z(x)$ terms cancel — this is the key trick.

### Step 5: The DPO loss

Maximum likelihood of this gives the DPO loss:

$$
\mathcal{L}_{\text{DPO}}(\theta) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma\left( \beta \log \frac{\pi_\theta(y_w | x)}{\pi_{\text{ref}}(y_w | x)} - \beta \log \frac{\pi_\theta(y_l | x)}{\pi_{\text{ref}}(y_l | x)} \right) \right]
$$

That's the entire DPO loss. Just compute log-probabilities of $y_w$ and $y_l$ under both $\pi_\theta$ and $\pi_{\text{ref}}$, take the difference, sigmoid, negative log-likelihood.

## Implementation Sketch

```python
import torch
import torch.nn.functional as F

def dpo_loss(policy_logps_w, policy_logps_l, 
             ref_logps_w, ref_logps_l, beta=0.1):
    """
    policy_logps_w: log p_theta(y_w | x), shape (B,)
    policy_logps_l: log p_theta(y_l | x), shape (B,)
    ref_logps_w:    log p_ref(y_w | x), shape (B,)
    ref_logps_l:    log p_ref(y_l | x), shape (B,)
    """
    # The "implicit reward" is beta * (log p_theta - log p_ref)
    pi_w = policy_logps_w - ref_logps_w  # log ratio for winner
    pi_l = policy_logps_l - ref_logps_l  # log ratio for loser
    
    # DPO loss = -log sigmoid(beta * (pi_w - pi_l))
    logits = beta * (pi_w - pi_l)
    loss = -F.logsigmoid(logits).mean()
    return loss
```

The training loop:
1. Sample a batch of preference pairs $(x, y_w, y_l)$.
2. Forward pass $y_w$ and $y_l$ through the policy to get $\log \pi_\theta(y_w | x)$ and $\log \pi_\theta(y_l | x)$.
3. Forward pass through the frozen reference model to get $\log \pi_{\text{ref}}(y_w | x)$ and $\log \pi_{\text{ref}}(y_l | x)$.
4. Compute the DPO loss and backprop into $\theta$.

## Why DPO Replaced PPO

| Aspect                | RLHF (PPO)                      | DPO                                |
|-----------------------|---------------------------------|------------------------------------|
| Number of models      | 4 (policy, ref, reward, value)  | 2 (policy, ref)                    |
| Online RL?            | Yes (samples from policy)       | No (offline)                       |
| Stability             | Tuning-sensitive                | Very stable                        |
| Hyperparameters       | Many (KL coeff, PPO clip, etc.) | Few (just $\beta$)                 |
| Training time         | Weeks                           | Hours–days                         |
| Compute               | High                            | Much lower                         |
| Quality               | Slightly higher (with tuning)   | Comparable                         |

DPO is now the default for most open-source alignment work. PPO survives in frontier lab training (where every last bit of quality matters) but is rare elsewhere.

## The $\beta$ Hyperparameter

$\beta$ controls the strength of the KL constraint:
- Small $\beta$ (e.g., 0.05): more aggressive — policy can drift far from reference. Risk: reward hacking, degenerate outputs.
- Large $\beta$ (e.g., 0.5): more conservative — policy stays close to reference. Risk: underfitting preferences.

Typical values: 0.1–0.3 for most workloads. Tune on a validation set.

## Variants

### IPO (Identity Preference Optimization)
A small modification that prevents DPO from overfitting when preferences are deterministic (every $y_w$ always beats every $y_l$):

$$
\mathcal{L}_{\text{IPO}} = \left( \log \frac{\pi_\theta(y_w | x)}{\pi_{\text{ref}}(y_w | x)} - \log \frac{\pi_\theta(y_l | x)}{\pi_{\text{ref}}(y_l | x)} - \frac{1}{2\beta} \right)^2
$$

Regression loss instead of classification. More robust to noisy or deterministic preferences.

### KTO (Kahneman-Tversky Optimization)
Doesn't need paired preferences — only needs binary "good" / "bad" labels per output. Uses prospect theory (loss aversion) to derive a loss. Useful when you have unary feedback (thumbs up / thumbs down) rather than pairwise comparisons.

### SimPO (Simple Preference Optimization)
Drops the reference model entirely. Uses a length-normalized reward:

$$
r(x, y) = \frac{\beta}{|y|} \log \pi_\theta(y | x)
$$

Simpler, faster, no reference model. Slight quality differences — some papers report better, some worse.

### ORPO
Combines SFT and preference optimization in a single stage — no separate SFT step needed.

## Worked Example

Suppose for one preference pair $(x, y_w, y_l)$:
- $\log \pi_\theta(y_w | x) = -5.0$, $\log \pi_{\text{ref}}(y_w | x) = -7.0$ → $\pi_w = +2.0$
- $\log \pi_\theta(y_l | x) = -10.0$, $\log \pi_{\text{ref}}(y_l | x) = -8.0$ → $\pi_l = -2.0$
- $\beta = 0.1$

$$
\text{logit} = 0.1 \cdot (2.0 - (-2.0)) = 0.4
$$

$$
\text{loss} = -\log \sigma(0.4) \approx -\log 0.599 \approx 0.513
$$

The model has increased $\pi_\theta(y_w)$ relative to reference and decreased $\pi_\theta(y_l)$ — the loss is moderately low (sigmoid of 0.4 ≈ 0.6).

As training progresses, the model amplifies this gap → logit grows → loss shrinks toward 0.

## Why This Matters for AI

- DPO made alignment **practical for open-source**. Pre-DPO, alignment was a frontier-lab game. Post-DPO, any research group with preference data can align a model.
- Most open-source chat models (Zephyr, OpenHermes, Tulu, many Llama fine-tunes) use DPO or a variant.
- DPO is the basis for **self-improvement loops** — generate outputs, label them with another model (RLAIF-style), train with DPO. No humans needed.
- The closed-form derivation is a beautiful example of theoretical insight leading to practical simplification. Studying it teaches you how to think about alignment.

## Production Implications

- **For alignment**: start with DPO. Move to PPO only if you've exhausted DPO variants and need the extra quality.
- **Preference data quality matters more than the algorithm**. Garbage in, garbage out. Invest in data.
- **Reference model must be the SFT checkpoint**. Don't use the base model as reference — that drifts too far.
- **Monitor KL** during training: $\log \pi_\theta - \log \pi_{\text{ref}}$. If it grows too large, you're drifting too far; reduce $\beta$.
- **Beta is sensitive**. Sweep $\beta \in \{0.05, 0.1, 0.2, 0.5\}$ on a validation set.

## Common Pitfalls

- **Forgetting the reference model** — DPO needs log-probs from both the policy and the frozen reference. Easy to forget.
- **Padding tokens in log-probs** — when computing $\log \pi(y | x)$, mask out padding tokens. Otherwise the loss is dominated by padding.
- **Reference model not in eval mode** — if the reference has dropout, log-probs are noisy.
- **Using base model instead of SFT as reference** — causes the policy to drift wildly.
- **Too aggressive $\beta$** — causes the model to exploit preference artifacts rather than learn true preferences.
- **Length bias** — DPO can prefer longer outputs (more tokens → more negative log-prob → "lower" reward). Mitigate with length normalization (SimPO) or length penalties.

## Further Reading

- Rafailov et al. (2023), *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*.
- Azar et al. (2023), *A General Theoretical Paradigm to Understand Learning from Human Preferences* (IPO).
- Ethayarajh et al. (2024), *KTO: Model Alignment as Prospect Theoretic Optimization*.
- Meng et al. (2024), *SimPO: Simple Preference Optimization with a Reference-Free Reward*.

## See Also

- [[LoRA]] — usually combined with DPO
- [[12 - Fine-Tuning/MOC|Fine-Tuning MOC]]
- [[Entropy Cross-Entropy KL]]
- [[Probability Essentials]]
- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO|RLHF]] (planned) — what DPO replaces


## Interview Questions

1. **Q: Derive the DPO loss from the RLHF objective.**
   A: (1) RLHF objective: maximize $E[r(x,y)] - \beta KL(\pi_\theta || \pi_{ref})$. (2) Closed-form optimal policy: $\pi^*(y|x) \propto \pi_{ref}(y|x) \exp(r(x,y)/\beta)$. (3) Solve for reward: $r(x,y) = \beta \log(\pi^*(y|x)/\pi_{ref}(y|x)) + \beta \log Z(x)$. (4) Plug into Bradley-Terry: $P(y_w \succ y_l) = \sigma(r(y_w) - r(y_l))$. (5) The $\log Z(x)$ terms cancel. (6) DPO loss: $-\log \sigma(\beta(\log \pi_\theta(y_w)/\pi_{ref}(y_w) - \log \pi_\theta(y_l)/\pi_{ref}(y_l)))$.

2. **Q: Why does DPO not need a reward model?**
   A: The key insight: the RLHF objective has a closed-form optimal policy that expresses the reward in terms of the policy and reference. By substituting this into the Bradley-Terry preference model, the reward (and the partition function Z(x)) cancel out. The resulting loss is purely in terms of policy and reference log-probabilities — no reward model needed.

3. **Q: What is the role of $\beta$ in DPO?**
   A: $\beta$ controls the KL constraint strength. Small $\beta$ (0.05): aggressive — policy can drift far from reference, risking reward hacking. Large $\beta$ (0.5): conservative — policy stays close to reference, risking underfitting. Typical: 0.1-0.3. Sweep on validation set. Monitor KL during training — if it grows too large, increase $\beta$.

4. **Q: What are DPO variants (IPO, KTO, SimPO)?**
   A: IPO: regression loss instead of classification — more robust to noisy/deterministic preferences. KTO: doesn't need paired preferences — only binary good/bad labels (thumbs up/down). SimPO: drops the reference model entirely, uses length-normalized reward — simpler, faster, no reference model. ORPO: combines SFT and preference optimization in one stage.

5. **Q: What are common pitfalls in DPO training?**
   A: (1) Forgetting the reference model — need log-probs from both policy and frozen reference. (2) Padding tokens in log-probs — mask them out or they dominate the loss. (3) Using base model instead of SFT as reference — causes wild drift. (4) Length bias — DPO can prefer longer outputs. (5) Too aggressive $\beta$ — model exploits preference artifacts.

6. **Q: When would you use DPO vs RLHF (PPO)?**
   A: Use DPO by default — simpler (2 models vs 4), stable, hours vs weeks. Use PPO only if: (1) you have frontier-scale compute; (2) you have active data collection (continuously updating reward model); (3) DPO quality is insufficient and you've exhausted DPO variants. PPO survives at frontier labs; DPO dominates open-source.

## Connection to Other Concepts

- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO|RLHF with PPO]] — what DPO replaces.
- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] — usually combined with DPO.
- [[02 - Mathematics/Probability/07 - Probability Essentials|Probability Essentials]] — Bradley-Terry model.
- [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Entropy, Cross-Entropy, KL]] — KL divergence in the objective.
- [[26 - Papers/Alignment/09 - DPO 2023|DPO 2023]] — the paper.
- [[29 - Interview Prep/Coding/04 - Coding Interview Questions 2|Coding Interview Q2]] — GRPO loss implementation.
