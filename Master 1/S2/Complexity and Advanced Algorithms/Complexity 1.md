Based on the provided exam corrections, the instructor is using a **"Detailed Count" (Décompte détaillé)** method to calculate time complexity. This method assigns a specific numerical cost to every single primitive operation the computer executes (assignments, comparisons, math, array accesses, etc.).

Here is a detailed breakdown of exactly how they are assigning complexity to each operation and how they build the formulas for the loops.

---

### 1. The Cost of Basic Operations
By looking closely at the handwritten annotations (like `init j (1)`, `increm j (2)`), we can deduce the "cost" the professor assigns to basic instructions:

*   **Initialization / Assignment:** 1 operation (e.g., `s <- 0` is **1**)
*   **Condition / Comparison:** 1 operation (e.g., `j <= n` or `M[i][j] > 0` is **1**)
*   **Increment / Decrement:** 2 operations (e.g., `j++` is actually `j <- j + 1`, which is 1 addition + 1 assignment = **2**)
*   **Math + Assignment:** 2 operations (e.g., `s <- s + M[i][j]` is 1 addition + 1 assignment = **2**)
*   **Return statement:** Treated as a jump/exit (often offsets other skipped operations).
*   **Parameter Passing:**
    *   *Group 1 (Pages 1-2):* Passed by **Reference**. Passing `M` and `n` takes **2** operations total.
    *   *Group 3 (Pages 3-4):* Passed by **Value**. A matrix of size $n \times n$ takes $n^2$ operations to copy. Passing `n` takes 1. Total: **$n^2 + 1$** operations.

---

### 2. How the Inner Loop is Counted ($C_{loop2}$)
Let's look at the inner loop in the **Worst Case** from Page 2. The worst case happens when the `0` is at the very last position checked, meaning the loop runs normally almost the entire time.

**Code:**
```text
pour j <- 1 à n faire          // Loop 2
    si M[i][j] > 0 alors
        s <- s + M[i][j]
```

**The Professor's Formula Breakdown for a Normal Iteration:**
A standard `for` loop consists of: Initialization + $\sum$ (Condition + Body + Increment) + Final Exit Condition.

1.  `init j (1)`: Setting $j = 1$ $\rightarrow$ **1 op**
2.  **Inside the loop (runs $n$ times):**
    *   `Cond acces loop2 (1)`: Check if $j \le n$ $\rightarrow$ **1 op**
    *   `Cond Si (1)`: Check if `M[i][j] > 0` $\rightarrow$ **1 op**
    *   `affect et som (2)`: `s <- s + ...` $\rightarrow$ **2 ops**
    *   `increm j (2)`: `j <- j + 1` (hidden by the `pour` syntax) $\rightarrow$ **2 ops**
    *   *Sum inside loop = 1 + 1 + 2 + 2 = **6 ops per iteration***
3.  `cond sortie loop2 (1)`: The final check where $j > n$ and the loop breaks $\rightarrow$ **1 op**

**Math for normal inner loop:**
$$C_{loop2} = 1 (\text{init}) + [ \sum_{1}^{n} 6 ] + 1 (\text{exit check})$$
$$C_{loop2} = 1 + 6n + 1 = \mathbf{6n + 2}$$

---

### 3. The "Last Iteration" Quirk ($C_{loop\_last}$)
The professor notes that because there is *always* exactly one `0` in the matrix, the absolute final iteration of the program will never finish normally. It will hit the `sinon` (else) statement and `return s`.

When it hits the `0`:
*   It does **not** do `s <- s + M[i][j]` (saves 2 ops)
*   It does **not** increment `j` (saves 2 ops)
*   It executes `return s` instead.
*   The professor notes: *"Lors de la rencontre du zero, return saute 4 opérations"* (When meeting zero, return skips 4 operations).

Therefore, the final time the inner loop runs, it takes $(6n + 2) - 4 = \mathbf{6n - 2}$ operations.

---

### 4. How the Outer Loop is Counted ($C_{loop1}$)
Now we nest $C_{loop2}$ inside the outer loop (`pour i <- 1 à n faire`).

**The Outer Loop structure:**
1.  `init i (1)` $\rightarrow$ **1 op**
2.  **Runs normally for $n-1$ rows:**
    *   `Cond acces loop1 (1)` $\rightarrow$ **1 op**
    *   $C_{loop2}$ (the normal inner loop) $\rightarrow$ **$6n + 2$ ops**
    *   `increm i (2)` $\rightarrow$ **2 ops**
    *   *Total per normal row: $1 + (6n+2) + 2 = 6n + 5$*
3.  **The final row ($n^{th}$ iteration):**
    *   `Cond acces loop1 (1)` $\rightarrow$ **1 op**
    *   $C_{loop\_last}$ (the aborted inner loop) $\rightarrow$ **$6n - 2$ ops**
    *   (It does not increment `i` because the program `return`s and ends).

**Math for the outer loop:**
$$C_{loop1} = 1 + \sum_{1}^{n-1}[6n + 5] + [1 + 6n - 2]$$
$$C_{loop1} = 1 + (n-1)(6n + 5) + (6n - 1)$$
$$C_{loop1} = 1 + (6n^2 + 5n - 6n - 5) + 6n - 1$$
$$C_{loop1} = \mathbf{6n^2 + 5n - 5}$$
*(This perfectly matches the professor's box on Page 2).*

---

### 5. Final Total Worst Case ($C_{max}$)
To get the final formula, they add the initial program setup to the outer loop.

*   `Envoi de parametres (2)`: Passing `M` and `n` by reference $\rightarrow$ **2 ops**
*   `init s (1)`: Setting $s = 0$ $\rightarrow$ **1 op**
*   $C_{loop1}$ $\rightarrow$ **$6n^2 + 5n - 5$ ops**

$$C_{max} = 2 + 1 + 6n^2 + 5n - 5$$
$$C_{max} = \mathbf{6n^2 + 5n - 2}$$

### Summary of Differences Between Exam Versions
If you look at Page 4 (Group 3), the counting logic for the loops is exactly the same, but the final $C_{max}$ is **$7n^2 + 5n - 3$**.

Why? Because on Page 3, the prompt says *"Le mode de transmission de M est par valeur"* (Passed by value). Therefore, instead of `Envoi de parametres (2)`, the cost to pass the parameters is $(n^2 + 1)$. Adding $n^2$ to the formula changes $6n^2$ to $7n^2$.

Regardless of the exact number, the highest power of $n$ is 2, which is why the asymptotic complexity for both versions is evaluated as **$\mathcal{O}(n^2)$**.