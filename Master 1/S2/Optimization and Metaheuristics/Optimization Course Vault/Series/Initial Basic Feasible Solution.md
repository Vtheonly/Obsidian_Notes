#  Detailed Explanation: Initial Basic Feasible Solution

##  What We're Working With

**Our system after transformation:**

$$\text{Maximize: } Z = 2x_1 + 3x_2 + 0x_3 + 0x_4 - Ma_1$$

**Constraints:**
$$\begin{align}
x_1 + x_2 - x_3 + 0x_4 + a_1 &= 4 \quad \text{(Equation 1)}\\
x_1 + 3x_2 + 0x_3 + x_4 + 0a_1 &= 6 \quad \text{(Equation 2)}
\end{align}$$

---

##  The Mathematics: Variables vs. Equations

**We have:**
- **5 variables:** $x_1, x_2, x_3, x_4, a_1$
- **2 equations**

**Basic linear algebra fact:**
- We can only solve for **2 variables** directly (one per equation)
- The other **3 variables** must be assigned values
- **Standard choice:** Set 3 variables to **zero** (these are "non-basic")
- Solve for the remaining 2 (these are "basic")

---

##  Why These Specific Variables?

### Which Variables Should Be Basic?

We need to choose 2 variables that are **easy to solve for**. 

**Look at the constraint matrix:**

$$\begin{array}{c|ccccc|c}
 & x_1 & x_2 & x_3 & x_4 & a_1 & \text{RHS}\\
\hline
\text{Row 1} & 1 & 1 & -1 & 0 & \boxed{1} & 4\\
\text{Row 2} & 1 & 3 & 0 & \boxed{1} & 0 & 6\\
\end{array}$$

**Notice:**
- Column $a_1$ has: $\begin{bmatrix}1\\0\end{bmatrix}$ 
- Column $x_4$ has: $\begin{bmatrix}0\\1\end{bmatrix}$

These form an **identity matrix**! This makes them perfect for basic variables.

---

##  Step-by-Step Calculation

### Step 1: Set Non-Basic Variables to Zero

**Non-basic variables:** $x_1, x_2, x_3$

$$x_1 = 0, \quad x_2 = 0, \quad x_3 = 0$$

**Why these?** Because $a_1$ and $x_4$ are easier to solve for (they have the identity matrix structure).

---

### Step 2: Solve for Basic Variables

#### From Equation 1:
$$x_1 + x_2 - x_3 + a_1 = 4$$

Substitute $x_1 = 0, x_2 = 0, x_3 = 0$:

$$\begin{align}
0 + 0 - 0 + a_1 &= 4\\
a_1 &= 4 \quad 
\end{align}$$

#### From Equation 2:
$$x_1 + 3x_2 + x_4 = 6$$

Substitute $x_1 = 0, x_2 = 0$:

$$\begin{align}
0 + 3(0) + x_4 &= 6\\
x_4 &= 6 \quad 
\end{align}$$

---

### Step 3: Calculate the Objective Value Z

$$Z = 2x_1 + 3x_2 + 0x_3 + 0x_4 - Ma_1$$

Substitute all values:

$$\begin{align}
Z &= 2(\color{blue}{0}) + 3(\color{blue}{0}) + 0(\color{blue}{0}) + 0(\color{green}{6}) - M(\color{red}{4})\\
Z &= 0 + 0 + 0 + 0 - 4M\\
Z &= -4M
\end{align}$$

**Where does $-4M$ come from?**
- The artificial variable $a_1 = \color{red}{4}$
- Its coefficient in the objective is $-M$
- So: $-M \times 4 = -4M$

---

##  Summary Table

| Variable | Type | Value | Why? |
|:---:|:---:|:---:|---|
| $x_1$ | **Non-basic** | $0$ | Set to zero to simplify |
| $x_2$ | **Non-basic** | $0$ | Set to zero to simplify |
| $x_3$ | **Non-basic** | $0$ | Set to zero to simplify |
| $x_4$ | **Basic** | $6$ | Solved from Equation 2 |
| $a_1$ | **Basic** | $4$ | Solved from Equation 1 |

**Objective:** $Z = -4M$

---

##  Why Is This Called "Feasible"?

A solution is **feasible** if:
1.  All constraints are satisfied
2.  All variables are non-negative

**Check Constraint 1:** $x_1 + x_2 - x_3 + a_1 = 0 + 0 - 0 + 4 = 4$ 

**Check Constraint 2:** $x_1 + 3x_2 + x_4 = 0 + 0 + 6 = 6$ 

**Check non-negativity:** $x_1=0≥0$, $x_2=0≥0$, $x_3=0≥0$, $x_4=6≥0$, $a_1=4≥0$ 

---

##  Visual Understanding

Think of it like this:

```
We have 5 variables and 2 equations.

┌─────────────────────────────────────┐
│  5 variables total                  │
│  ├─── 2 basic (non-zero)           │
│  │    • a₁ = 4                     │
│  │    • x₄ = 6                     │
│  │                                  │
│  └─── 3 non-basic (zero)           │
│       • x₁ = 0                      │
│       • x₂ = 0                      │
│       • x₃ = 0                      │
└─────────────────────────────────────┘
```

---

##  Why Is Z = -4M So Bad?

If $M = 1{,}000{,}000$, then:
$$Z = -4(1{,}000{,}000) = -4{,}000{,}000$$

**This is terrible!** We're trying to **maximize** Z, and we're at $-4$ million!

**The Simplex algorithm will:**
1. See this horrible objective value
2. Notice it's because $a_1 = 4$ is in the solution
3. Work to **kick out $a_1$** and replace it with a real variable
4. This will improve Z dramatically

---

##  The Big Picture

| Stage | Basic Variables | Non-Basic Variables | Z Value |
|---|---|---|---|
| **Initial** (now) | $a_1=4, x_4=6$ | $x_1=0, x_2=0, x_3=0$ | $-4M$  |
| **After iteration 1** | $x_2=?, x_4=?$ | $x_1=0, x_3=0, a_1=0$ | Better! |
| **Optimal** | Real variables only | $a_1=0$ (artificial gone!) | Maximum  |

---

##  Key Takeaways

1. **Why zero some variables?** 
   - We have more variables (5) than equations (2)
   - We choose 3 to set to zero (non-basic)
   - We solve for the other 2 (basic)

2. **Why these specific variables as basic?**
   - $a_1$ and $x_4$ have identity matrix columns
   - They're easiest to solve for

3. **How did we get -4M?**
   - Substitute all variable values into objective
   - $Z = -M \times a_1 = -M \times 4 = -4M$

4. **Why is it "bad"?**
   - $-4M$ is hugely negative (we want to maximize!)
   - This motivates the algorithm to remove $a_1$

**Next step:** Run Simplex iterations to improve this terrible initial solution!
