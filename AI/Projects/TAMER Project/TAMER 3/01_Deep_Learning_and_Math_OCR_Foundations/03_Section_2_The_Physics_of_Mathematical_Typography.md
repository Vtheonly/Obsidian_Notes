## 2. The Physics of Mathematical Typography

### Why Math Is Structurally Different

Standard written language exists in one dimension: time flows left to right, top to bottom in a consistent linear grid. Mathematical notation intentionally breaks this linearity. A neural network trained on plain text has no concept of the 2D spatial grammar of mathematics and will completely fail.

The key structural constructs in LaTeX that break linearity are:

**Vertical stacking (Fractions):**
$$\frac{a + b}{c - d}$$
The numerator lives spatially above the denominator. Their horizontal centers must be aligned. There is no left-to-right ordering between them; they exist simultaneously in different vertical zones.

**Superscripts and subscripts:**
$$x_i^2$$
The subscript $i$ lives below and to the right of $x$. The superscript $2$ lives above and to the right. A model must learn that these three symbols have a specific 2D spatial hierarchy, not just a linear sequence.

**Environments (Matrices, Arrays):**
$$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$$
This is a fully 2D data structure. The `&` character separates columns. The `\\` separates rows. Misplacing either character collapses the entire matrix structure.

---

### Complexity Classification in TAMER

The TAMER data pipeline classifies all formulas into three tiers of structural complexity. This classification is not merely aesthetic. It directly informs:
- How the image is preprocessed (aspect ratio logic).
- What structural weights the loss function applies.
- What kinds of augmentation are safe to apply.

**Tier 1: Simple**
- Single-line expressions.
- No `\\` row separators.
- No multi-column `&` separators.
- Examples: $E = mc^2$, $\int_0^\infty f(x)\,dx$, $\sqrt{x^2 + y^2}$.
- Challenge: Nested commands like `\frac`, `\sqrt`, requiring correct bracket matching.

**Tier 2: Medium**
- Multi-line expressions using `\\` as a row separator.
- May use `\begin{aligned}`, `\begin{cases}`, `\begin{gather}`.
- Examples:
$$\begin{aligned} a &= b + c \\ d &= e - f \end{aligned}$$
- Challenge: The model must predict the `\\` token at the correct moment, then continue on the next line. The model must implicitly track which row it is on.

**Tier 3: Complex**
- Grid structures using both `\\` and `&`.
- Environments: `matrix`, `pmatrix`, `bmatrix`, `array`, `tabular`.
- Challenge: Strict 2D coordinate tracking. Every cell occupies a unique `(row, column)` address. If the model predicts `&` one step too early, it shifts all subsequent columns. If it predicts `\\` one step too early, it shifts all subsequent rows. A single structural error cascades into a completely wrong output.

> **Critical reminder:** When you look at a TAMER training log and see a formula with high loss, it is almost always a Tier 3 formula. The structural weight in the loss function (multiplied by 3.0 for `&` and `\\`) is specifically designed to force the model to be extremely careful about these tokens. Do not be alarmed by higher loss values on complex formulas. This is expected and intentional.

---