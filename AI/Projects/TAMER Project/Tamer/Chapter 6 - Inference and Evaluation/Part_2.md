# Chapter 6: Inference and Evaluation

## 3. Deep Dive: The Mechanics of Beam Search vs Greedy Decoding

**Greedy Decoding (The Local Optimum Trap):**
At step $t$, Greedy asks: "What is the most likely token *right now*?"
Imagine the image is poorly written, and looks like either `x` or `\times`. 
*   Step 1: The model guesses `\times` (51% probability) over `x` (49%). 
*   Step 2: Having output `\times`, the model must output a valid equation. It outputs `2`. (Total: `\times 2`).
Because it made a greedy choice at Step 1, it fell into a trap and generated an invalid mathematical phrase.

**Beam Search (The Global Optimum):**
Beam Search (with width $B=5$) explores multiple parallel universes.
*   **Step 1:** It keeps the top 5 guesses. Universe A starts with `\times` (prob 0.51). Universe B starts with `x` (prob 0.49).
*   **Step 2:** It expands all 5 universes into 25 possibilities. 
    *   Universe A expands to `\times 2`. The model realizes this makes no mathematical sense, so the probability of `2` given `\times` is 0.01. Cumulative score: $0.51 \times 0.01 = 0.0051$.
    *   Universe B expands to `x =`. This makes perfect sense. The probability of `=` given `x` is 0.99. Cumulative score: $0.49 \times 0.99 = 0.4851$.
*   **Pruning:** Beam Search sorts the 25 paths by their cumulative log-probability and discards the bottom 20. Universe B (`x =`) now outranks Universe A, successfully avoiding the local trap.

```mermaid
graph TD
    Start[Start: SOS] --> B1[Beam 1: \times (0.51)]
    Start --> B2[Beam 2: x (0.49)]
    
    B1 --> B1_1[\times 2 (0.01) -> Total: 0.005]
    B1 --> B1_2[\times y (0.05) -> Total: 0.025]
    
    B2 --> B2_1[x = (0.99) -> Total: 0.485]
    B2 --> B2_2[x + (0.90) -> Total: 0.441]
    
    B2_1 -.-> |Pruning: Highest Score Survives| Winner[x =]
```

## 4. Evaluation Metrics: Justifications and Edge Cases

Why do we need four different metrics? Because math is unforgiving.

*   **Exact Match (ExpRate):** This is the ultimate benchmark. We strip all whitespace (because `x + y` and `x+y` render identically) and do a pure string comparison. 
    *   *Edge Case:* If the model outputs `\mathbf{x}` instead of `\boldsymbol{x}`, they mean the same thing visually, but ExpRate gives it a 0%.
*   **Edit Distance:** We run Levenshtein distance on the *tokenized* arrays, not characters. 
    *   *Justification:* If the ground truth is `\frac{a}{b}`, and the model predicts `\frac{a}{c}`, the token edit distance is 1 (swapped `b` for `c`). If we used character distance, the penalty would be arbitrary.
*   **Symbol Error Rate (SER):** Normalizes the Edit Distance by the length of the equation. An edit distance of 5 on a 100-token matrix is excellent (5% error). An edit distance of 5 on a 6-token equation is a catastrophic failure.
*   **Leq1 (Less than or equal to 1 Edit):** In Mathematical OCR, an edit distance of 1 almost always represents a single ambiguous character (e.g., misreading a badly written `1` as an `l`). Leq1 gives us the "Usable Prediction Rate"—formulas that a human could fix with a single keystroke.