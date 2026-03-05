
## Theorem: Some Languages Are Not Turing-Recognizable
Not every problem can be solved. The proof relies on comparing the sizes of mathematical infinities.

**The Proof:**
1. **Turing Machines are Countable (Dénombrable):**
   Every TM can be described by a finite string (its 7-uplet or source code). Because strings are finite, we can sort and number them: $M_1, M_2, M_3, \dots$
2. **Languages are Uncountable (Non dénombrable):**
   Every language can be represented by an infinite binary sequence. The set of all infinite binary sequences is uncountable. We prove this via **Diagonalization**.

### The Diagonalization Method
Imagine we map all possible binary languages to all infinite binary sequences in a table:
* $S_1 = \mathbf{0}, 0, 0, 0 \dots$
* $S_2 = 1, \mathbf{0}, 0, 0 \dots$
* $S_3 = 0, 1, \mathbf{0}, 0 \dots$
* $S_4 = 1, 1, 0, \mathbf{0} \dots$

If we take the diagonal values $(\mathbf{0}, \mathbf{0}, \mathbf{0}, \mathbf{0} \dots)$ and flip them, we get a new sequence: $S_{diag} = \mathbf{1}, \mathbf{1}, \mathbf{1}, \mathbf{1} \dots$. 
This new sequence $S_{diag}$ is guaranteed to be missing from the list. Therefore, there are more languages than Turing machines.
**Conclusion:** Certain languages have no TM that recognizes them. Certain problems have no resolution algorithm.

---

## The Halting Problem (Problème de l'arrêt)
Is it possible to write a program that looks at another program and determines if it will eventually halt (stop) or loop forever?

Let's assume a magical TM $H$ exists that solves this. It takes a machine $M$ and an input $w$:
$$
H(\langle M, w \rangle) = 
\begin{cases} 
accept & \text{if } M \text{ accepts } w \\
reject & \text{if } M \text{ does not accept } w 
\end{cases}
$$

Now, we define a malicious TM called $D$ that uses $H$ as a subroutine:
> $D =$ "On input $\langle M \rangle$, where $M$ is a TM:
> 1. Run $H$ on input $\langle M, \langle M \rangle \rangle$.
> 2. Output the **opposite** of what $H$ outputs. That is, if $H$ accepts, $reject$; and if $H$ rejects, $accept$."

$$
D(\langle M \rangle) = 
\begin{cases} 
accept & \text{if } M \text{ does not accept } \langle M \rangle \\
reject & \text{if } M \text{ accepts } \langle M \rangle 
\end{cases}
$$

**The Paradox:** What happens if we pass $D$ into itself? We calculate $D(\langle D \rangle)$.
$$
D(\langle D \rangle) = 
\begin{cases} 
accept & \text{if } D \text{ does not accept } \langle D \rangle \\
reject & \text{if } D \text{ accepts } \langle D \rangle 
\end{cases}
$$
This is a logical contradiction! $D$ accepts if and only if $D$ rejects. 
**Therefore, our assumption was wrong. The machine $H$ cannot exist.**

### High-Level Code Representation
```javascript
function halts(func) {
    // Insert code here that returns "true" if "func" halts and "false" otherwise.
}

function deceiver() {
    if(halts(deceiver)) {
        while(true) { } // loop forever
    }
}
```
If `halts(deceiver)` returns `true`, `deceiver` will run forever (contradicting the true). If it returns `false`, `deceiver` halts (contradicting the false). The function `halts` is impossible.