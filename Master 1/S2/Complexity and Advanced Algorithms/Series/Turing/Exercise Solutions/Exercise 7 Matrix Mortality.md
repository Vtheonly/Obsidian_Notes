# Exercise 7: Modified Matrix Mortality Problem

## 1. Problem Statement
The Matrix Mortality Problem (MMP) is a famous problem in theoretical computer science. It asks: 
> *Given a finite set of $n \times n$ matrices (with integer entries), is there a sequence of matrix multiplications—allowing repetitions of the same matrix—that results in the Zero Matrix?*

For matrices of size $n \ge 3$, the standard MMP is mathematically proven to be **Undecidable** (Post's Correspondence Problem can be reduced to it).

**The Modification:**
We are given the same problem ($n=3$), but a strict condition is explicitly added: The length of the sequence of matrix multiplications, let's call it $m$, is bounded such that **$1 \le m \le 1000$**. 

**The Question:**
Is this modified problem Decidable or Undecidable? Justify your answer rigorously.

---

## 2. Deep Methodological Breakdown

To solve this, we must detach from the advanced linear algebra of matrices and focus exclusively on the core definitions of Computability Theory.

### What does "Decidable" actually mean?
* A problem is **Decidable** if there exists a Turing Machine (an algorithm) that will **always halt** for *every single possible input*, and output either "YES" or "NO".
* A problem is **Undecidable** if no such algorithm can exist. Usually, this happens because the algorithm can get trapped in an infinitely large search space. If it hasn't found the answer yet, it doesn't know if the answer is "It's just taking a while" or "The answer is NO". Thus, it runs forever.

### Why is the Original MMP Undecidable?
In the original problem, there is no limit on $m$. You could multiply 5 matrices. If the result isn't zero, maybe you need to multiply 10. If not 10, maybe a million. If not a million, maybe a gazillion. Because there is no upper bound, an algorithm brute-forcing the combinations will never know when to give up. If the answer is `NO`, the algorithm will run into infinity searching for a `YES`. That infinite loop makes it Undecidable.

### Analyzing the Modification
The modified problem places a hard ceiling on the search space: $m \le 1000$.

Let's do the math. 
Let $k$ be the number of matrices provided in the given finite set.
How many possible sequences of length 1 exist? $k$.
How many possible sequences of length 2 exist? $k^2$.
How many possible sequences of length 3 exist? $k^3$.
...
How many possible sequences of length 1000 exist? $k^{1000}$.

Therefore, the **Total Number of Sequences** we are allowed to check is exactly:
$$ Total = k^1 + k^2 + k^3 + \dots + k^{1000} $$

---

## 3. The Rigorous Solution

**Answer: YES, the modified problem is DECIDABLE.**

**Justification:**

1. **Strictly Finite Search Space:** As proven by the math above, the total number of matrix multiplications we are permitted to check is $k^1 + \dots + k^{1000}$. While astronomically massive from a human perspective, this number is strictly, mathematically **finite**.
2. **Construction of a Validating Algorithm:** Because the search space is finite, it is trivial to design a Turing Machine that acts as a Brute-Force Validator.
   * *Step 1:* Generate the 1st sequence combination. Multiply the matrices.
   * *Step 2:* Is the result the Zero Matrix? If yes, Halt and return `YES`.
   * *Step 3:* If not, generate the next sequence.
   * *Step n:* Continue until sequence $k^{1000}$ is calculated.
3. **Guaranteed Halting:** Because our brute-force TM has a hard, predefined stop limit at iteration $k^1 + \dots + k^{1000}$, the machine is **guaranteed to halt**. It will either find a Zero Matrix during its checks and halt on `YES`, or it will complete its finite list of chores, realize no combinations work, and cleanly halt on `NO`.
4. **Conclusion:** Since we have successfully theorized an algorithm that will always halt and always provide the correct answer, the problem fits the exact definition of Decidability.

> [!warning] Common Pitfall
> **Complexity $\neq$ Undecidability.** 
> It is extremely tempting to think: *"Wait, if $k=50$, then $50^{1000}$ combinations would take all the supercomputers on Earth a billion years to calculate. Therefore it's impossible, therefore it's undecidable."*
> **This is a fallacy.** Computability Theory *does not care about time.* Time is a property of Complexity Theory. Computability Theory only cares about *finiteness*. Because there is an end to the list, the machine Halts. Whether it halts in 1 second or 10 billion years is irrelevant to its Decidability.
