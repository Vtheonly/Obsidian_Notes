# 6. Undecidable Problems (PCP and MMP)

The Halting Problem proves that undecidability exists. Using it, we can prove that other concrete mathematical problems are also completely undecidable. The course highlights two famous ones.

## 1. Post Correspondence Problem (PCP)
Proposed in 1946 by Emil Leon Post. Also known as the **Problem of Dominoes**.

### The Data
* A finite alphabet $\Sigma$.
* A finite list of pairs of words (think of them as dominoes with a top string and a bottom string):
  $$P = \{(u_1, v_1), (u_2, v_2), \dots, (u_k, v_k)\}$$
  where $u_i, v_i \in \Sigma^*$.

### The Question
Does there exist a **sequence of indices** $i_1, i_2, \dots, i_m$ (with $m \ge 1$) such that reading the top strings in that order perfectly matches the bottom strings?
$$u_{i_1} u_{i_2} \dots u_{i_m} = v_{i_1} v_{i_2} \dots v_{i_m} ?$$

### Example
Given the dominoes:
1. Top: `B`, Bottom: `CA`
2. Top: `A`, Bottom: `AB`
3. Top: `CA`, Bottom: `A`
4. Top: `ABC`, Bottom: `C`

If we choose the sequence of indices **2, 1, 3, 2, 4**:
* Top string: `A` + `B` + `CA` + `A` + `ABC` = **ABCAAABC**
* Bottom string: `AB` + `CA` + `A` + `AB` + `C` = **ABCAAABC**
They match!

### Decidability
The PCP problem is **undecidable**. There is absolutely no Turing Machine capable of determining, for *any* given instance $P$, whether such a sequence of indices exists.

---

## 2. Matrix Mortality Problem (MMP)
Proposed in 1970 by Michael Stewart Paterson.

### The Data
* An integer $n \ge 3$.
* A finite set of $n \times n$ matrices with integer (or rational) coefficients:
  $$S = \{A_1, A_2, \dots, A_k\} \subseteq \mathbb{Z}^{n \times n}$$

### The Question
Does there exist a **sequence of indices** $i_1, i_2, \dots, i_m$ (with $m \ge 1$) such that multiplying the matrices in that order results in the **Zero Matrix**?
$$A_{i_1} A_{i_2} \dots A_{i_m} = 0_{n \times n} ?$$

### Example
Suppose $n = 3$, and we have two matrices $A$ and $B$:
$$A = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{pmatrix}, \quad B = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}$$

If we verify the sequence $A \cdot A \cdot B$ (which is $A^2B$):
$$A \cdot A \cdot B = A^2B = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}$$
It yields the zero matrix.

### Decidability
The problem is **non décidable (undecidable) for $n \ge 3$**.
> In other words, there is no algorithm capable of determining for *any* finite set of matrices if a finite product of these matrices equals the zero matrix.
