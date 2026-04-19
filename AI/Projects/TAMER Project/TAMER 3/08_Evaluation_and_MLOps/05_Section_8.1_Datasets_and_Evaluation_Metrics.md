## 8.1 Datasets and Evaluation Metrics

### The Datasets

#### CROHME (Competition on Recognition of Online Handwritten Mathematical Expressions)

CROHME is the academic standard benchmark for HMER research. It has been maintained since 2011 and updated with new test sets in 2014, 2016, 2019, and 2023.

**Key characteristics:**
- Approximately 8,000-12,000 training formulas, 986-2,000 test formulas depending on the year.
- Collected from human writers using digital styluses (online data: raw pen trajectories captured as time series).
- Offline versions (images rendered from the pen trajectories) are also provided.
- Formulas range from simple arithmetic to moderately complex expressions. Very deep nesting and large matrices are rare.
- Ground truth is provided in both LaTeX and MathML formats.

**The CROHME Limitation:**
Because CROHME is an academic competition dataset, its formulas are relatively controlled in complexity. A model achieving high ExpRate on CROHME may still perform poorly on real-world math from textbooks, handwritten student assignments, or photographed whiteboards.

#### HME100K

HME100K is a large-scale real-world dataset released by researchers at Tencent. It contains approximately 100,000 formula images.

**Key characteristics:**
- Images collected from real examination papers, textbooks, and assignment sheets via smartphone camera.
- Includes natural scene noise: shadows, perspective distortion, background textures.
- Higher complexity distribution than CROHME: more matrices, more deeply nested expressions.
- More variable writer styles: different pen types, paper types, lighting conditions.
- Significantly harder than CROHME for this reason.

A model that achieves good performance on HME100K is genuinely production-ready for real-world mathematical OCR deployment.

#### Im2LaTeX Datasets (Pretraining)

Used exclusively in Stage 1 pretraining:
- **Im2LaTeX-100K:** LaTeX expressions from arXiv papers, rendered with a LaTeX compiler.
- **Im2LaTeX-230K:** Extended version. Higher diversity of expression types.
- These datasets are not used in evaluation because they are printed (not handwritten).

---

### Evaluation Metrics

#### ExpRate (Expression Recognition Rate)

$$ExpRate = \frac{\text{Number of expressions predicted 100\% correctly}}{\text{Total number of test expressions}} \times 100\%$$

This is the strictest possible metric. A single missing token, a single extra space (in environments where spacing matters), or a single wrong character means the entire expression is counted as a failure.

**Why this matters:** In real applications, a partially correct LaTeX formula is still a broken LaTeX formula. If you are building a tool to convert textbook images to editable LaTeX, a formula with one wrong token cannot be compiled. It is not "90% correct". It is broken. ExpRate measures the only thing that matters in production: does the formula compile and render correctly?

**The nuance of LaTeX equivalence:**
Some LaTeX expressions are semantically equivalent but syntactically different. For example, `x^{2}` and `x^2` render identically (the braces are optional for single-character superscripts). When computing ExpRate, TAMER normalizes both the ground truth and prediction through a canonical LaTeX simplifier before comparing, to avoid penalizing the model for stylistic differences that do not affect the rendered output.

#### ExpRate at Token Error Rate Thresholds

In addition to strict ExpRate, evaluation often reports relaxed metrics:

- **ExpRate@1:** Exactly correct (standard ExpRate).
- **ExpRate@0.95:** At least 95% of tokens correct.
- **ExpRate@0.90:** At least 90% of tokens correct.

These relaxed metrics help diagnose the model's failure modes. If ExpRate@1 is 85% but ExpRate@0.95 is 98%, the model is almost always nearly correct, failing only due to very small errors (a missing subscript, a slightly wrong coefficient). If ExpRate@1 is 85% and ExpRate@0.95 is 86%, the model is either completely correct or completely wrong, with few partial successes. This second pattern indicates the model is failing on categorically different types of formulas rather than making small systematic errors.

#### Structural Recall

Standard ExpRate penalizes all errors equally. A wrong number in a formula is treated the same as a missing `\\` that collapses an entire matrix row. TAMER tracks **Structural Recall** separately to measure specifically how well the model handles structural elements.

$$\text{Structural Recall} = \frac{\text{Correctly predicted structural tokens}}{\text{Total ground truth structural tokens}}$$

Where structural tokens are: `\\`, `&`, all `\begin{...}` variants, all `\end{...}` variants.

A model with high ExpRate but low Structural Recall is good at simple formulas but falls apart on matrices. A model with low ExpRate but high Structural Recall is doing well on structure but making many content errors.

#### BLEU Score (Character-Level)

Borrowed from machine translation evaluation, BLEU (Bilingual Evaluation Understudy) measures the overlap between the predicted and reference token sequences using n-gram matching.

$$BLEU = BP \cdot \exp\left(\sum_{n=1}^{N} w_n \log p_n\right)$$

Where $p_n$ is the modified precision of n-grams, $w_n = 1/N$ are uniform weights, and $BP$ is the brevity penalty (penalizes sequences shorter than the reference).

BLEU is useful for understanding the gradient of model quality (is one model strictly better than another across all formula lengths?) but is not the primary metric because a formula with BLEU 0.97 might still fail to compile.

#### Tree Edit Distance (TED)

For evaluating the structural quality of predictions independent of surface token accuracy, TAMER reports Tree Edit Distance between the predicted AST and the ground-truth AST.

TED measures the minimum number of node insertions, deletions, and substitutions required to transform the predicted tree into the ground-truth tree. A TED of 0 means the trees are structurally identical. A TED of 1 means one structural relationship is wrong (e.g., a subscript classified as a superscript).

$$TED(T_1, T_2) = \min_{\text{edit operations}} \sum \text{cost}(\text{operation})$$

TED specifically measures what TAMER is designed to improve: mathematical structural accuracy beyond surface-level token matching.

---