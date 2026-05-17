Based on the second set of documents, the instructor is using the exact same **"Detailed Count" (Décompte détaillé)** methodology as the first one, assigning numerical costs to every basic operation. 

However, the algorithm they are analyzing here is much more complex. According to Page 1, this algorithm searches a matrix by **alternating** between scanning a row (Loop `i`) and scanning a column (Loop `j`). It updates minimum and maximum values, and stops early if `min == max`.

Here is the exact breakdown of how they assigned the complexity on **Page 2** and **Page 4**.

---

### 1. The Cost Key (Based on Page 2)
The annotations reveal the exact costs assigned to operations:
*   **`Init(1)` / `Cond(1)`:** Initialization or checking a condition = **1 op**
*   **`Incr(2)`:** Incrementing a loop counter (e.g., `i++` is `i = i + 1`) = **2 ops**
*   **`Aff(2)` / `Affe(2)`:** Assignment of a value from an array (e.g., `min = M[i][j]`) = **2 ops**
*   **`param(2)`:** Passing parameters to the function = **2 ops**
*   **`return(1)`:** The return statement = **1 op**

---

### 2. The Best Case ($C_{min}$)
The best case occurs if the algorithm finds that `min == max` on the very first try and terminates immediately (1 iteration of the main loop `k`).

**Inner Loop `i` (scanning a row):**
*   Initialization: `1`
*   Inside the loop (runs $n$ times): Condition (`1`) + Increment (`2`) + `If` condition (`1`) = `4` per iteration $\rightarrow 4n$
*   Exit condition: `1`
*   *Formula:* $1 + 4n + 1 = \mathbf{4n + 2}$

**Outer Loop `k` (runs only 1 time before stopping):**
*   It does an initialization (`1`), checks condition (`1`), does an `If` check (`1`), runs Loop `i` (`4n + 2`), does an assignment (`2`), does the final exit `If` check (`1`), and `return`s (`1`).
*   *Formula:* $1 + 1 + 1 + (4n + 2) + 2 + 1 + 1 = \mathbf{4n + 9}$

**Total $C_{min}$:**
*   Parameters (`2`) + General Init (`5`) + Loop `k` (`4n + 9`)
*   *Formula:* $2 + 5 + 4n + 9 = \mathbf{4n + 16}$, which is $\mathbf{\mathcal{O}(n)}$

---

### 3. The Worst Case ($C_{max1}$)
In the worst case, the algorithm never finds `min == max` early, so it processes the entire matrix. 

Because the algorithm *alternates*, it runs Loop `i` (rows) exactly half the time, and Loop `j` (columns) exactly half the time.

**Inner Loops `i` and `j` (Maximum work):**
*   Initialization(`1`) + $\sum$ [Cond(`1`) + Incr(`2`) + Cond si(`1`) + Aff(`2`)] + Exit Cond(`1`)
*   Inside the sum is 6. So it becomes $1 + 6n + 1 = 6n + 2$.
*   *Note:* The instructor writes $\dots - 2 = \mathbf{6n}$. They subtracted 2 operations at the end. This is a common adjustment meaning on the absolute last iteration, it skips an assignment `Aff(2)` or an `Incr(2)` because it hits the end of the data. 

**Main Outer Loop `k` (The Alternation Logic):**
This is where the heavy math happens. Loop `k` runs $n$ times.
*   Standard loop overhead per iteration: Cond(`1`) + Incr(`2`) + Cond Si(`1`) = `4`
*   Alternating logic: Because it alternates, Loop `i` happens 50% of the time ($\frac{1}{2} \times 6n$), and Loop `j` happens 50% of the time ($\frac{1}{2} \times 6n$). 
*   Alternating assignments: An assignment of `3` operations happens half the time ($\frac{1}{2} \times 3$).
*   Other assignments per iteration: `Aff_type(2)` + `Cond(1)` = `3`

**Building the $k$ loop Formula:**
$$C_{loop\_k} = 1 (\text{init}) + \sum_{k=1}^{n} \left[ 4 + \frac{1}{2}(6n) + \frac{1}{2}(6n) + \frac{3}{2} + 3 \right] + 1 (\text{exit})$$
Combine the terms inside the sum:
$$4 + 3n + 3n + 1.5 + 3 = 6n + 8.5$$
Multiply by $n$ (since the loop runs $n$ times):
$$\sum = 6n^2 + 8.5n$$
Add the outside terms ($1 + 1$):
$$C_{loop\_k} = \mathbf{6n^2 + 8.5n + 2} \quad \text{(Written as } 6n^2 + \frac{17}{2}n + 2 \text{)}$$

Adding the parameter/init overhead ($2 + 5$) gives the final $C_{max1} = \mathbf{6n^2 + \frac{17}{2}n + 10}$, which is $\mathbf{\mathcal{O}(n^2)}$.

---

### 4. What is happening on Page 4? (Asymptotic Shortcuts)
Page 4 is entirely different from Page 2. Here, the prompt says *"Donner la complexité asymptotique... sans calcul"* (**Give the asymptotic complexity... WITHOUT calculation**). 

Instead of counting every `+1` and `+2`, the student just looks at how the loops scale with $n$.

**Algo 1: The "Trick" Question**
*   Outer loop runs from $1$ to $n$ $\rightarrow \mathcal{O}(n)$
*   Line 2 sets `k = i`.
*   Line 3 says `Tant que (While) k > n`.
*   **The trick:** Because `i` only goes up to `n`, `k` will *never* be greater than `n`. Therefore, the `While` loop and the `For j` loop inside it **never execute**. It's dead code.
*   Only the outer loop runs, so the complexity is just **$\mathcal{O}(n)$**.

**Algo 2: The Logarithmic Loop**
*   Outer loop runs from $1$ to $n$ $\rightarrow \mathcal{O}(n)$
*   Inner loop: `j` starts at $1$, and instead of `j = j + 1`, it does `j = j * 2`.
*   Because `j` doubles every time, it reaches `i` in $\log_2(i)$ steps. 
*   A loop that runs $n$ times, containing a loop that runs $\log(n)$ times, results in a total complexity of **$\mathcal{O}(n \log n)$**.