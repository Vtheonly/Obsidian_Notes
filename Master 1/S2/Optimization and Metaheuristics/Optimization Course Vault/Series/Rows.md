# Complete Guide: Which Rows Change and Why

##  The Universal Formula for ALL Rows

During each pivot operation, **every row follows one of these formulas**:

| Row Type           | Formula                                       | When Used                         |
| ------------------ | --------------------------------------------- | --------------------------------- |
| **Pivot Row**      | New Pivot Row = Old Pivot Row ÷ Pivot Element | For the leaving variable's row    |
| **All Other Rows** | New Row = Old Row − (c × New Pivot Row)       | For every other row (including Z) |

Where **c** = coefficient in the pivot column for that row

---

##  Key Insight: Why Some Rows "Don't Change"

**They actually DO follow the formula, but:**

$$\text{If } c = 0, \text{ then: New Row} = \text{Old Row} - (0 \times \text{New Pivot Row}) = \text{Old Row}$$

**Subtracting zero makes it appear unchanged!**

---

##  Detailed Example: Example 1, Iteration 1→2

### Setup
- **Pivot Column:** $x_2$ 
- **Pivot Row:** $x_5$ row (leaving variable)
- **Pivot Element:** 1

---

### Step 1: Create the New Pivot Row

$$\text{New } x_2 \text{ row} = \frac{\text{Old } x_5 \text{ row}}{\text{Pivot Element}}$$

$$= \frac{[0, 1, 0, 0, 1 \mid 600]}{1} = [0, 1, 0, 0, 1 \mid 600]$$

---

### Step 2: Update x₃ Row

**Check coefficient in pivot column (x₂):** Old $x_3$ row has **2** in the $x_2$ column

$$\text{New } x_3 = \text{Old } x_3 - (2 \times \text{New } x_2)$$

$$\begin{align}
&= [3, 2, 1, 0, 0 \mid 1800] - 2 \times [0, 1, 0, 0, 1 \mid 600]\\
&= [3, 2, 1, 0, 0 \mid 1800] - [0, 2, 0, 0, 2 \mid 1200]\\
&= [3, 0, 1, 0, -2 \mid 600] \quad  \text{ CHANGED}
\end{align}$$

---

### Step 3: Update x₄ Row

**Check coefficient in pivot column (x₂):** Old $x_4$ row has **0** in the $x_2$ column

$$\text{New } x_4 = \text{Old } x_4 - (0 \times \text{New } x_2)$$

$$\begin{align}
&= [1, 0, 0, 1, 0 \mid 400] - 0 \times [0, 1, 0, 0, 1 \mid 600]\\
&= [1, 0, 0, 1, 0 \mid 400] - [0, 0, 0, 0, 0 \mid 0]\\
&= [1, 0, 0, 1, 0 \mid 400] \quad  \text{ UNCHANGED}
\end{align}$$

**This row appears unchanged because we subtracted zero!**

---

### Step 4: Update Z Row

**Check coefficient in pivot column (x₂):** Old Z row has **50** in the $x_2$ column

$$\text{New } Z = \text{Old } Z - (50 \times \text{New } x_2)$$

$$\begin{align}
&= [30, 50, 0, 0, 0 \mid 0] - 50 \times [0, 1, 0, 0, 1 \mid 600]\\
&= [30, 50, 0, 0, 0 \mid 0] - [0, 50, 0, 0, 50 \mid 30000]\\
&= [30, 0, 0, 0, -50 \mid -30000] \quad  \text{ CHANGED}
\end{align}$$

---

##  Summary Table for Example 1, Iteration 1→2

| Row | Coefficient in Pivot Column (x₂) | Formula Used | Result |
|---|:---:|---|---|
| **x₅ (Pivot)** | 1 | Old row ÷ 1 | Becomes new x₂ row |
| **x₃** | **2** ≠ 0 | Old − (2 × New x₂) | **CHANGED** |
| **x₄** | **0** | Old − (0 × New x₂) | **UNCHANGED** |
| **Z** | **50** ≠ 0 | Old − (50 × New x₂) | **CHANGED** |

---

##  Another Example: Example 5, Iteration 2→3

### Setup
- **Pivot Column:** $x_1$
- **Pivot Row:** $x_5$ row
- **Pivot Element:** 3

---

### Step 1: New Pivot Row

$$\text{New } x_1 = \frac{[3, 0, 0, -1, 1 \mid 6]}{3} = [1, 0, 0, -1/3, 1/3 \mid 2]$$

---

### Step 2: Check Each Row's Coefficient in x₁ Column

| Old Row | Coefficient in x₁ | Calculation | Changed? |
|---|:---:|---|:---:|
| **x₃** | **1** | [1,0,1,0,0\|4] − 1×[1,0,0,−1/3,1/3\|2] = [0,0,1,1/3,−1/3\|2] |  YES |
| **x₂** | **0** | [0,1,0,1/2,0\|6] − 0×[1,0,0,−1/3,1/3\|2] = [0,1,0,1/2,0\|6] |  NO |
| **Z** | **3** | [3,0,0,−5/2,0\|−30] − 3×[1,0,0,−1/3,1/3\|2] = [0,0,0,−3/2,−1\|−36] |  YES |

---

##  General Algorithm

For **every** iteration:

```
1. Identify pivot column (entering variable)
2. Identify pivot row (leaving variable)  
3. Identify pivot element (intersection)

4. Create new pivot row:
   New Pivot Row = Old Pivot Row ÷ Pivot Element

5. For EACH other row (including Z):
   a. Find coefficient c in pivot column
   b. New Row = Old Row − (c × New Pivot Row)
   
    If c = 0, the row stays the same!
```

---

##  Visual Pattern Recognition

**Look at the pivot column before updating:**

```
Pivot Column (x₂)
    ↓
    2  ← Non-zero → Row will CHANGE
    0  ← ZERO → Row stays SAME  
    1  ← This is pivot row
   50  ← Non-zero → Row will CHANGE
```

---

##  Quick Reference: Formula Cheat Sheet

| Situation | Formula | Example |
|---|---|---|
| **Pivot row** | New = Old ÷ pivot | [6,4,1,0\|24] ÷ 6 |
| **c ≠ 0** | New = Old − c×(New Pivot) | Old − 3×(New Pivot) |
| **c = 0** | New = Old − 0×(New Pivot) = Old | Row unchanged |
| **Z row** | New Z = Old Z − c×(New Pivot) | Same formula! |

---

##  Pro Tip

**You can predict which rows change before calculating:**
- Count non-zero entries in the pivot column
- Those rows (plus the pivot row) will change
- Zero entries = no change needed (but formula still applies!)

