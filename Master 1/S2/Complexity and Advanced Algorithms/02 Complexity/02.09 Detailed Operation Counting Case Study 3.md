This third set of documents (**Sujet 01**) uses the exact same **"Detailed Count"** method as the previous ones, where every single primitive operation is assigned a numerical value. 

However, there is a **major twist** in this version of the exam that completely changes the final answers: **The matrix is passed by value, not by reference.**

Here is the exact breakdown of how the instructor assigns complexity in this specific exam version.

---

### 1. The Cost Key (What operations cost what)
Just like the others, we can deduce the costs from the instructor's formulas:
*   **`Init(1)` / `Cond(1)` / `return(1)`:** Basic setup, condition checks, and returns = **1 op**
*   **`Incr(2)` / `Aff(2)`:** Incrementing (`i++`) or simple assignment (`min = M[i][j]`) = **2 ops**
*   **`Cond_si(3)`:** The instructor assigns **3 ops** to the exit condition here. This implies a compound condition, such as `if (min1 == x OR min2 == x)`, which takes two comparisons and one logical OR.
*   **`param(n² + 2)`:** **This is the most important part.** Because the matrix $M$ is passed by *value*, the computer must copy all $n \times n$ elements into a new matrix for the function to use. Therefore, just passing the parameters costs **$n^2$** (for the matrix) + **$2$** (for two normal variables, like `type` and `n`).

---

### 2. The Best Case ($C_{min}$) — *Notice why it's $\mathcal{O}(n^2)$!*
In the best case, the target value `x` is found at the very first cell `M[1][1]`. The program stops immediately.

**Inner Loop (`Boucle i`):**
Because it finds `x` immediately, it does *not* do the assignment `Aff(2)`.
*   Init (`1`) + runs 1 time: Cond (`1`) + Incr (`2`) + Cond (`1`) + Exit Cond (`1`)
*   Formula for the single row: **$4n + 2$** *(The instructor generalizes this to $n$ to show the scale of one loop)*

**Outer Loop (`Boucle K`):**
Runs exactly 1 time before stopping.
*   Setup + Inner Loop + Exit checks = **$4n + 11$**

**Total $C_{min}$ Calculation:**
Even though the loop stops immediately, the computer *already copied the matrix* when the function started.
*   $C_{min} = \text{param} (n^2 + 2) + \text{Init}(5) + \text{Boucle K}(4n + 11)$
*   $C_{min} = \mathbf{n^2 + 4n + 18}$
*   Because $n^2$ is the highest power, the best-case complexity is **$\mathcal{O}(n^2)$**. *(In the previous subject, the best case was $\mathcal{O}(n)$ because passing parameters was free!)*

---

### 3. The Worst Case ($C_{max}$)
The worst case happens when the value `x` is never found, and the minimums must be updated on every single iteration. 
Like the previous subject, this algorithm **alternates** between searching rows (`Boucle i`) and columns (`Boucle j`), so each runs 50% of the time.

**Inner Loops (`Boucle i` / `j`):**
*   Init (`1`) + $\sum$ [Cond(`1`) + Incr(`2`) + Cond(`1`) + Aff(`2`)] + Exit(`1`)
*   $1 + \sum(6) + 1 = 6n + 2$. The instructor subtracts `2` for the final skipped assignment to get **$6n$**.

**Outer Loop (`Boucle k`) — The Alternating Logic:**
Runs $n$ times.
*   Overhead: Cond(`1`) + Incr(`2`) + Cond_si(`1`) = `4`
*   50% Row / 50% Col logic: $\frac{1}{2}(6n) + \frac{1}{2}(6n) = 6n$
*   Other checks inside: Aff(`2`) + Cond_si(`3`) = `5`
*   Formula per iteration: $4 + 6n + 5 = \mathbf{6n + 9}$
*   Multiply by $n$ iterations and add initial/exit ops (`1+1`): $n(6n+9) + 2 = \mathbf{6n^2 + 9n + 2}$

**Total $C_{max1}$ Calculation:**
*   $C_{max} = \text{param}(n^2 + 2) + \text{Init}(5) + \text{Boucle K}(6n^2 + 9n + 2) + \text{Final Aff}(3) + \text{Return}(1)$
*   Add them together: $n^2 + 6n^2 = 7n^2$.
*   $C_{max} = \mathbf{7n^2 + 9n + 13}$, which is **$\mathcal{O}(n^2)$**.

*(Note: The instructor also calculates $C_{max2}$ for when `x` is found on the absolute last iteration, which just saves a few operations at the very end, resulting in $7n^2 + 9n + 7$. Both are $\mathcal{O}(n^2)$).*

---

### 4. Page 3: Asymptotic Complexity "Without Calculation"
Just like the previous subject, this page asks for Big-O notation simply by looking at loop structures, rather than counting `+1` and `+2`.

**Algo 1 (The Trick Question):**
*   `pour i de 1 à n` $\rightarrow \mathcal{O}(n)$
*   `pour j de i à n` $\rightarrow \mathcal{O}(n)$
*   Look closely at the `Tant que` (While) loop:
    *   `l <- j`
    *   `tant que l > 0 faire: l <- l - j`
    *   **The trick:** If `l` equals `j`, and you subtract `j` from `l`, `l` immediately becomes `0`.
    *   Therefore, the `While` loop is an illusion. It only runs **exactly one time**, making it $\mathcal{O}(1)$.
*   Because you only have two nested `for` loops running $n$ times, the complexity is $\mathcal{O}(n) \times \mathcal{O}(n) = \mathbf{\mathcal{O}(n^2)}$.

**Algo 2 (The Logarithmic Loop):**
*   This is identical to the previous subject. 
*   The outer loop runs $n$ times $\rightarrow \mathcal{O}(n)$
*   The inner loop `j` doubles every time (`j = j * 2`), meaning it reaches the limit in $\log_2(n)$ steps $\rightarrow \mathcal{O}(\log n)$
*   Combined, the complexity is **$\mathcal{O}(n \log n)$**.