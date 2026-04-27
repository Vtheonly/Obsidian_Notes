# Chapter 4: Text Processing and Tokenization

## 3. Algorithmic Complexity Scoring for Math Equations

We previously established that the trainer uses Curriculum Learning (Simple $\rightarrow$ Medium $\rightarrow$ Complex). But how does the system objectively know if a mathematical equation is "simple" or "complex" before it even looks at the image?

In `latex_normalizer.py`, you wrote a highly specific heuristic scoring algorithm: `get_complexity(latex)`.

**1. Immediate Complex Triggers:**
If the LaTeX string contains elements that break standard 1D left-to-right reading, it bypasses the scoring and is instantly flagged as `complex`. These include matrices (`\begin{matrix}`), multiline alignments (`\begin{aligned}`), row separators (`\\`), and column separators (`&`).

**2. The Point System:**
If there are no immediate triggers, the algorithm calculates a float score:
*   **Length Penalty:** `+1 point` for every 25 characters. Long sequences stress the Transformer's attention matrix.
*   **Spatial Shifts (Up/Down):** `+1 point` for every superscript (`^`) or subscript (`_`). These require the model to learn localized vertical relationships.
*   **Heavy Vertical Structures:** `+2 points` for symbols that drastically alter the 2D bounding box of the equation, such as `\frac`, `\sqrt`, `\int`, `\sum`, `\prod`.
*   **Grouping Depth:** `+0.5 points` for every opening brace `{`. Deeply nested braces (e.g., `\frac{1}{x^{2}}`) require the decoder to track long-range bracket-matching syntax.

**3. Classification Thresholds:**
*   **Score < 4.0 (`simple`):** Basic algebra, e.g., $x^2 + y = 3$. Used in Epochs 1-10.
*   **Score 4.0 to 12.0 (`medium`):** Standard college math with multiple fractions or integrals.
*   **Score > 12.0 (`complex`):** Heavily nested, nightmare equations.