---
tags: [mathematics, statistics, hypothesis-testing, p-values, confidence-intervals]
iteration: 11
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Hypothesis Testing, p-values, Confidence Intervals, Multiple Testing]
---

# 17 — Hypothesis Testing

> [!info] TL;DR
> Hypothesis testing is the statistical framework for deciding whether observed data supports a claim. You formulate a null hypothesis (H₀: no effect), compute a p-value (probability of seeing data this extreme if H₀ is true), and reject H₀ if the p-value is below a threshold (typically 0.05). Confidence intervals estimate a range that contains the true parameter with high probability. **Multiple testing correction** (Bonferroni, FDR) is essential when running many tests — without it, false positives explode. Understanding hypothesis testing is critical for evaluating ML experiments and interpreting benchmark results.

## Why Hypothesis Testing Matters for AI

AI engineers constantly need to answer questions like:
- "Is model A better than model B, or is the difference noise?"
- "Did this prompt change improve quality, or is it random variation?"
- "Is the new feature's impact statistically significant?"

These are hypothesis testing questions. Without proper testing, you'll ship changes that don't actually work (false positives) or miss changes that do (false negatives). Understanding hypothesis testing prevents both errors.

## The Framework

### Null and Alternative Hypotheses
- **Null hypothesis (H₀)**: the default assumption — typically "no effect" or "no difference."
- **Alternative hypothesis (H₁ or Hₐ)**: what you're testing for — typically "there is an effect."

Examples:
- H₀: model A and model B have the same accuracy. H₁: they differ.
- H₀: the prompt change has no effect on quality. H₁: it improves quality.
- H₀: the new feature doesn't increase conversion. H₁: it does.

### The p-value
The p-value is the probability of observing data as extreme as (or more extreme than) what you saw, **assuming the null hypothesis is true**.

- **Low p-value** (< 0.05): the observed data is unlikely under H₀, so we reject H₀.
- **High p-value** (≥ 0.05): the observed data is plausible under H₀, so we fail to reject H₀.

Important: a high p-value does **not** prove H₀ is true. It just means we don't have enough evidence to reject it.

### Significance Level (α)
The threshold for rejecting H₀, typically 0.05 (5%). This means: if H₀ is true, we'll falsely reject it 5% of the time.

### Types of Errors
- **Type I error (false positive)**: rejecting H₀ when it's true. Probability = α.
- **Type II error (false negative)**: failing to reject H₀ when it's false. Probability = β.
- **Statistical power**: 1 - β, the probability of correctly rejecting H₀ when it's false.

There's a tradeoff: lowering α reduces Type I errors but increases Type II errors (and vice versa).

## Common Tests

### t-test (Comparing Two Means)
Tests whether two groups have different means.

```python
from scipy import stats

# Two-sample t-test: are model A and model B accuracies different?
acc_a = [0.85, 0.87, 0.84, 0.86, 0.83]  # model A accuracies across folds
acc_b = [0.88, 0.89, 0.87, 0.90, 0.86]  # model B accuracies

t_stat, p_value = stats.ttest_ind(acc_a, acc_b)
print(f"p-value: {p_value:.4f}")
if p_value < 0.05:
    print("Reject H₀: the models have significantly different accuracies.")
else:
    print("Fail to reject H₀: no significant difference detected.")
```

### Paired t-test
When the same examples are evaluated by both models (paired comparison), use a paired t-test — it's more powerful because it controls for example difficulty.

### Chi-Square Test (Categorical Data)
Tests whether categorical variables are independent.

### Mann-Whitney U Test (Non-Parametric)
Non-parametric alternative to the t-test. Use when data isn't normally distributed or sample sizes are small.

### Wilcoxon Signed-Rank Test (Paired, Non-Parametric)
Non-parametric alternative to the paired t-test.

## Confidence Intervals

A confidence interval gives a range that contains the true parameter with high probability (e.g., 95%).

### Interpretation
A 95% confidence interval [a, b] means: if we repeated the experiment many times, 95% of the intervals would contain the true parameter. It does **not** mean "there's a 95% chance the true parameter is in [a, b]" — the true parameter is fixed; the interval is random.

### Calculation
For a mean with known standard deviation:
```
CI = x̄ ± z * (σ / √n)
```
where `z` is the z-score (1.96 for 95% confidence), `σ` is the standard deviation, and `n` is the sample size.

### Why Confidence Intervals Are Better Than p-values
- **Effect size**: CIs show the magnitude of the effect, not just "significant or not."
- **Uncertainty**: CIs show the uncertainty in the estimate.
- **Practical significance**: a statistically significant difference of 0.1% might be practically irrelevant. CIs make this visible.

Modern statistical practice prefers CIs over bare p-values.

## Multiple Testing Correction

### The Problem
When you run many tests, the chance of at least one false positive grows. With 20 tests at α=0.05, the probability of at least one false positive is:
```
P(at least one false positive) = 1 - (1 - 0.05)^20 ≈ 0.64
```

You're almost guaranteed a false positive. This is why "p-hacking" (running many tests until one is significant) produces false results.

### Bonferroni Correction
The simplest correction: divide α by the number of tests.
```
α_corrected = α / n_tests
```

For 20 tests at α=0.05, use α_corrected = 0.0025. This is very conservative — it controls the family-wise error rate (probability of any false positive) but reduces power.

### False Discovery Rate (FDR) — Benjamini-Hochberg
A less conservative correction: controls the proportion of false positives among rejected hypotheses, rather than the probability of any false positive.

```python
from statsmodels.stats.multitest import multipletests

p_values = [0.001, 0.04, 0.03, 0.20, 0.01]  # p-values from 5 tests

# Benjamini-Hochberg FDR correction
rejected, p_corrected, _, _ = multipletests(p_values, method='fdr_bh', alpha=0.05)
print(f"Rejected: {rejected}")  # [True, False, False, False, True]
print(f"Corrected p-values: {p_corrected}")
```

FDR is preferred when you have many tests (e.g., genomics, A/B testing at scale) and want to find as many true effects as possible while controlling false positives.

### When to Use Which
- **Few tests (<10)**: Bonferroni is fine.
- **Many tests (>10)**: FDR (Benjamini-Hochberg).
- **Pre-registered hypotheses**: no correction needed if you specified the tests in advance.

## Practical Guidelines for AI Engineers

### Always Report Effect Sizes
Don't just say "significant." Report the magnitude: "Model A is 2.3% more accurate than Model B (95% CI: [1.1%, 3.5%], p < 0.001)."

### Use Paired Tests When Possible
Paired tests (same examples evaluated by both models) are more powerful than unpaired tests. Always use paired tests when you can.

### Check Assumptions
t-tests assume normality. For large samples (>30), the Central Limit Theorem makes this OK. For small samples, check normality or use non-parametric tests.

### Pre-Register Your Tests
Decide what you're testing before running the experiment. Don't look at the data and then decide what to test — this inflates false positives.

### Correct for Multiple Comparisons
If you compare many models or many metrics, correct for multiple comparisons. Otherwise, you'll ship "improvements" that are actually noise.

### Don't Confuse Statistical and Practical Significance
A 0.01% improvement with p < 0.001 is statistically significant but practically irrelevant. Always consider the effect size, not just the p-value.

### Sample Size Matters
Small samples have low power — you'll miss real effects. Use power analysis to determine the sample size needed to detect a given effect size.

## Common Pitfalls

### p-Hacking
Running many tests and only reporting the significant ones. This inflates false positives. Pre-register tests; report all tests, not just significant ones.

### Confusing p-value with Probability H₀ Is True
The p-value is P(data | H₀), not P(H₀ | data). A low p-value doesn't mean H₀ is probably false — it means the data is unlikely under H₀. These are different (see [[08 - Bayes Theorem Deep Dive]] for the difference).

### Ignoring Multiple Testing
Running 20 A/B tests and finding one "significant" result is almost certainly a false positive. Correct for multiple testing.

### Using One-Tailed Tests Inappropriately
One-tailed tests (testing only for improvement, not difference) have more power but can miss effects in the unexpected direction. Use two-tailed tests unless you have a strong reason for one-tailed.

### Stopping Early
Stopping an A/B test when it reaches significance (optional stopping) inflates false positives. Pre-determine the sample size and run to completion.

### Overinterpreting Non-Significance
"Failing to reject H₀" is not the same as "proving H₀." You might just lack power. A non-significant result doesn't mean there's no effect — it means you can't rule out no effect.

## See Also

- [[16 - Estimators and Bias]]
- [[08 - Bayes Theorem Deep Dive]]
- [[01 - Bias Variance Tradeoff]]
- [[05 - ML Evaluation Metrics]]
- [[07 - A-B Testing and Shadow Deployment]]
- [[04 - LLM-as-Judge Evaluation]]
- [[06 - LLM Benchmarks]]
- [[02 - Mathematics/MOC|02 Mathematics MOC]]

## Sequential Testing — Stopping Without Inflating False Positives

The classical hypothesis test fixes the sample size in advance. But in production A/B testing, you want to peek and stop early if there's a clear winner. Naive peeking inflates false positives: with 20 peeks at $\alpha = 0.05$, you're almost guaranteed a false positive.

**Sequential testing** methods adjust the threshold over time:

- **SPRT (Wald's Sequential Probability Ratio Test)**: stop when the likelihood ratio exceeds a bound. Optimal in theory, but requires known effect size.
- **Group sequential designs** (O'Brien-Fleming, Pocock): pre-specify peek times with adjusted $\alpha$ at each. O'Brien-Fleming is conservative early, liberal late.
- **Always-valid p-values** (Howard et al. 2021): use confidence sequences that are valid under any stopping rule. Modern production systems (Statsig, Optimizely) use these.

For production A/B testing, always-valid p-values (or the Bayesian equivalent — Beta posteriors) let you stop at any time without inflating false positives. This is essential for fast iteration.

## Bayesian vs. Frequentist Hypothesis Testing

| Aspect              | Frequentist                        | Bayesian                              |
|---------------------|------------------------------------|---------------------------------------|
| Question answered   | $P(\text{data} \mid H_0)$          | $P(H \mid \text{data})$               |
| Output              | p-value (reject $H_0$ or not)      | posterior over hypotheses             |
| Prior               | None                               | Required                              |
| Multiple testing    | Needs correction (Bonferroni, FDR) | Automatic (posterior is calibrated)   |
| Optional stopping   | Inflates false positives           | Valid (posterior updates correctly)   |
| Interpretation      | "Reject $H_0$ at $\alpha = 0.05$" | "87% probability B is better than A"  |
| Sample size         | Pre-determined (power analysis)    | Flexible (stop when posterior is confident) |

For production A/B testing in 2026, Bayesian methods (Beta-Bernoulli posteriors) are increasingly preferred because they're interpretable ("87% probability B is better") and handle optional stopping naturally. Frequentist methods are still standard in academia and regulated industries (FDA, clinical trials).

## Worked Example: Comparing Two LLMs

```python
import numpy as np
from scipy import stats

# Per-query correctness for two models on 100 queries
model_a = np.random.binomial(1, 0.70, 100)  # 70% accuracy
model_b = np.random.binomial(1, 0.78, 100)  # 78% accuracy

# 1. Paired t-test (each query is evaluated by both models)
diff = model_b - model_a  # +1 if B wins, -1 if A wins, 0 if tie
t_stat, p_value = stats.ttest_1samp(diff, 0)
print(f"Paired t-test: t={t_stat:.3f}, p={p_value:.4f}")
print(f"Mean diff: {diff.mean():.3f} (B beats A by {diff.mean()*100:.1f} percentage points)")

# 2. Effect size (Cohen's d)
cohens_d = diff.mean() / diff.std()
print(f"Cohen's d: {cohens_d:.3f} (small effect if <0.2, medium if <0.5, large if >0.8)")

# 3. 95% confidence interval on the difference
mean_diff = diff.mean()
sem_diff = diff.std() / np.sqrt(len(diff))
ci = (mean_diff - 1.96 * sem_diff, mean_diff + 1.96 * sem_diff)
print(f"95% CI on difference: [{ci[0]:.3f}, {ci[1]:.3f}]")

# 4. Power analysis: how many queries to detect a 5% difference with 80% power?
from statsmodels.stats.power import ttest_power
power = ttest_power(0.05, nobs=100, alpha=0.05, alternative='two-sided')
print(f"Power with n=100: {power:.3f}")
# To get 80% power:
from statsmodels.stats.power import tt_solve_power
n_needed = tt_solve_power(0.05, alpha=0.05, power=0.8, alternative='two-sided')
print(f"n needed for 80% power: {n_needed:.0f}")
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
|--------|--------------|-----|
| p-value is significant but effect is tiny | Large sample size makes tiny effects significant | Always report effect size; don't trust p-values alone |
| A/B test gives contradictory results across days | Multiple testing; or day-of-week effects | Pre-register; correct for multiple comparisons; stratify by day |
| Stopping early gives false positives | Optional stopping inflates $\alpha$ | Use sequential testing; or Bayesian methods |
| "No significant difference" reported as "no effect" | Low power; small sample | Compute power; report confidence intervals, not just p-values |
| LLM-as-judge gives inconsistent ratings | Judge bias; prompt ambiguity | Ensemble multiple judges; calibrate against humans |
| Benchmark scores differ by <1% | Within noise; not a real difference | Run multiple seeds; compute confidence intervals |

## Connection to Other Concepts

- [[02 - Mathematics/Probability/07 - Probability Essentials|Probability Essentials]] — Bayes' theorem and conditional probability.
- [[02 - Mathematics/Probability/08 - Bayes Theorem Deep Dive|Bayes Theorem Deep Dive]] — Bayesian vs. frequentist interpretation.
- [[02 - Mathematics/Statistics/16 - Estimators and Bias|Estimators and Bias]] — properties of estimators.
- [[03 - Machine Learning/Evaluation/05 - ML Evaluation Metrics|ML Evaluation Metrics]] — accuracy, precision, recall, calibration.
- [[03 - Machine Learning/Generalization/01 - Bias Variance Tradeoff|Bias Variance Tradeoff]] — bias-variance decomposition.
- [[08 - LLMs/Evaluation/06 - LLM Benchmarks|LLM Benchmarks]] — hypothesis testing for benchmark comparison.
- [[21 - LLMOps and MLOps/Evaluation/04 - LLM-as-Judge Evaluation|LLM-as-Judge Evaluation]] — using LLMs as judges.
- [[21 - LLMOps and MLOps/Deployment/07 - A-B Testing and Shadow Deployment|A/B Testing and Shadow Deployment]] — production A/B testing.
- [[21 - LLMOps and MLOps/Monitoring/05 - Production Monitoring|Production Monitoring]] — detecting quality regressions.
- [[22 - Production AI/Reliability/06 - Failure Modes and Graceful Degradation|Failure Modes and Graceful Degradation]] — when to alert.

## Interview Questions

1. **Q: What is the multiple testing problem, and how do you correct for it?**
   A: When you run many tests, the probability of at least one false positive grows. With 20 tests at $\alpha = 0.05$, $P(\geq 1 \text{ false positive}) = 1 - (1 - 0.05)^{20} \approx 0.64$. Two corrections: (1) **Bonferroni** — divide $\alpha$ by the number of tests (very conservative, controls family-wise error rate). (2) **Benjamini-Hochberg FDR** — controls the proportion of false positives among rejected hypotheses (less conservative, preferred for many tests). For LLM benchmarking, where you compare many model pairs across many benchmarks, FDR is the standard.

2. **Q: What's the difference between a p-value and the probability that the null hypothesis is true?**
   A: A p-value is $P(\text{data} \mid H_0)$ — the probability of observing data this extreme if the null is true. It is NOT $P(H_0 \mid \text{data})$ — the probability that the null is true given the data. These are related by Bayes' theorem but require a prior. Confusing them is the "prosecutor's fallacy". A low p-value doesn't mean the null is probably false — it means the data is unlikely under the null. With a strong enough prior, even a low p-value can leave the null quite probable. Bayesian methods give you $P(H \mid \text{data})$ directly.

3. **Q: How would you design an A/B test for an LLM feature?**
   A: (1) **Pre-register the hypothesis and metric** — decide what you're testing and the success metric before looking at data. (2) **Power analysis** — compute the sample size needed to detect the smallest effect you care about with 80% power. (3) **Use paired tests** — evaluate both variants on the same set of queries, so you control for query difficulty. (4) **Use sequential testing or Bayesian methods** — to allow early stopping without inflating false positives. (5) **Report effect sizes and confidence intervals**, not just p-values. (6) **Stratify by segment** — the feature might help some users and hurt others. (7) **Watch for novelty effects** — early gains may fade as users adapt.

4. **Q: When would you use a Bayesian test instead of a frequentist one?**
   A: Use Bayesian when: (1) you need to stop early (Bayesian posteriors are valid under any stopping rule); (2) you want an interpretable answer ("87% probability B is better" vs. "reject $H_0$ at $\alpha = 0.05$"); (3) you have prior information you want to incorporate; (4) you're doing many comparisons (Bayesian methods handle multiple testing naturally). Use frequentist when: (1) you're in a regulated industry (FDA, clinical trials); (2) you don't want to specify a prior; (3) the audience expects p-values. For production A/B testing in tech, Bayesian is increasingly the default.

5. **Q: What is the Bonferroni correction and when is it too conservative?**
   A: Bonferroni divides $\alpha$ by the number of tests: $\alpha_{\text{corrected}} = \alpha / n$. For 20 tests at $\alpha = 0.05$, use $\alpha = 0.0025$. It controls the family-wise error rate (probability of any false positive). It's too conservative when: (1) you have many tests (>10) — power drops dramatically; (2) tests are correlated — Bonferroni assumes independence; (3) you're willing to accept some false positives in exchange for more true positives. In those cases, use FDR (Benjamini-Hochberg) instead.

6. **Q: How do you evaluate whether two LLMs have statistically different benchmark scores?**
   A: Don't just compare aggregate scores — they hide variance. (1) **Run multiple seeds** for each model to estimate variance. (2) **Use paired tests** — evaluate both models on the same set of test examples, computing per-example correctness. (3) **Compute effect size** (Cohen's d) — a 1% difference might be statistically significant with enough samples but practically irrelevant. (4) **Report confidence intervals** on the difference, not just p-values. (5) **Correct for multiple comparisons** if you're comparing many model pairs or many benchmarks (FDR). (6) **Stratify by category** — model A might win on math but lose on coding; the aggregate hides this.

## See Also

- [[16 - Estimators and Bias]]
- [[08 - Bayes Theorem Deep Dive]]
- [[01 - Bias Variance Tradeoff]]
- [[05 - ML Evaluation Metrics]]
- [[07 - A-B Testing and Shadow Deployment]]
- [[04 - LLM-as-Judge Evaluation]]
- [[06 - LLM Benchmarks]]
- [[02 - Mathematics/MOC|02 Mathematics MOC]]
