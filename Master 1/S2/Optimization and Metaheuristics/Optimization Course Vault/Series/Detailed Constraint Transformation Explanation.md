

## Original Problem

$$\text{Minimize: } Z = 2x_1 - 3x_2$$

**Subject to:**
$$\begin{align}
x_1 + x_2 &\geq 5 \quad \text{(Constraint 1: "greater than or equal")}\\
2x_1 - x_2 &\leq 8 \quad \text{(Constraint 2: "less than or equal")}\\
x_1 &\text{ unrestricted (can be negative)}\\
x_2 &\geq 0
\end{align}$$

---

## 🔄 Step-by-Step Transformation

### **Step 1: Fix Minimization** → Maximization

$$\boxed{\text{Min}(Z) = -\text{Max}(-Z)}$$

**Original:** $\text{Min } Z = 2x_1 - 3x_2$

**Transformed:** 
$$\text{Max } W = -Z = -(2x_1 - 3x_2) = -2x_1 + 3x_2$$

**Remember:** At the end, $Z_{\text{optimal}} = -W_{\text{optimal}}$

---

### **Step 2: Fix Unrestricted Variable** $x_1$

**Problem:** Simplex requires ALL variables $\geq 0$, but $x_1$ can be negative.

**Solution:** Substitute using two non-negative variables
$$\boxed{x_1 = x_1' - x_1'' \quad \text{where } x_1', x_1'' \geq 0}$$

**Update objective function:**
$$\begin{align}
W &= -2x_1 + 3x_2\\
&= -2(x_1' - x_1'') + 3x_2\\
&= -2x_1' + 2x_1'' + 3x_2
\end{align}$$

---

### **Step 3: Update Constraints with New Variable**

Replace every occurrence of $x_1$ with $(x_1' - x_1'')$

#### Constraint 1: $x_1 + x_2 \geq 5$
$$\begin{align}
x_1 + x_2 &\geq 5\\
(x_1' - x_1'') + x_2 &\geq 5\\
x_1' - x_1'' + x_2 &\geq 5
\end{align}$$

#### Constraint 2: $2x_1 - x_2 \leq 8$
$$\begin{align}
2x_1 - x_2 &\leq 8\\
2(x_1' - x_1'') - x_2 &\leq 8\\
2x_1' - 2x_1'' - x_2 &\leq 8
\end{align}$$

**Current state:**
$$\text{Maximize: } W = -2x_1' + 2x_1'' + 3x_2$$
$$\text{Subject to:}$$
$$\begin{align}
x_1' - x_1'' + x_2 &\geq 5\\
2x_1' - 2x_1'' - x_2 &\leq 8\\
x_1', x_1'', x_2 &\geq 0
\end{align}$$

---

## 🎯 Step 4: Add Slack/Surplus Variables (Convert to Equalities)

### Understanding the Two Types of Constraints:

| Constraint Type | What to Add | Purpose | Sign |
|---|---|---|---|
| **$\leq$ (less than or equal)** | **Slack variable** (+) | Absorbs unused resources | $+ s_i$ |
| **$\geq$ (greater than or equal)** | **Surplus variable** (−) | Represents excess over minimum | $- s_i$ |

---

### Constraint 1: $x_1' - x_1'' + x_2 \geq 5$

**Type:** Greater than or equal ($\geq$)

**Action:** Add a **surplus variable** $s_1 \geq 0$

**Why subtract?** We need to remove the "surplus" to make it an equality:
$$\begin{align}
x_1' - x_1'' + x_2 &\geq 5\\
x_1' - x_1'' + x_2 - s_1 &= 5
\end{align}$$

**Interpretation:**
- If $x_1' - x_1'' + x_2 = 7$, then we have **2 units excess** over the minimum of 5
- So $s_1 = 2$ (the surplus)
- Check: $7 - 2 = 5$ ✓

**Example values:**
$$\begin{array}{c|c|c|c}
x_1' - x_1'' + x_2 & \text{Surplus } s_1 & \text{Check: LHS} - s_1 & \text{Valid?}\\
\hline
7 & 2 & 7 - 2 = 5 & ✓\\
5 & 0 & 5 - 0 = 5 & ✓\\
10 & 5 & 10 - 5 = 5 & ✓\\
4 & ? & \text{Can't work!} & ✗
\end{array}$$

---

### Constraint 2: $2x_1' - 2x_1'' - x_2 \leq 8$

**Type:** Less than or equal ($\leq$)

**Action:** Add a **slack variable** $s_2 \geq 0$

**Why add?** We need to "fill up" unused capacity to make it an equality:
$$\begin{align}
2x_1' - 2x_1'' - x_2 &\leq 8\\
2x_1' - 2x_1'' - x_2 + s_2 &= 8
\end{align}$$

**Interpretation:**
- If $2x_1' - 2x_1'' - x_2 = 6$, we're using **6 out of 8 available**
- So $s_2 = 2$ (the slack/unused amount)
- Check: $6 + 2 = 8$ ✓

**Example values:**
$$\begin{array}{c|c|c|c}
2x_1' - 2x_1'' - x_2 & \text{Slack } s_2 & \text{Check: LHS} + s_2 & \text{Valid?}\\
\hline
6 & 2 & 6 + 2 = 8 & ✓\\
8 & 0 & 8 + 0 = 8 & ✓\\
3 & 5 & 3 + 5 = 8 & ✓\\
10 & ? & \text{Can't work!} & ✗
\end{array}$$

---

## 📋 Final Standard Form

$$\boxed{\text{Maximize: } W = -2x_1' + 2x_1'' + 3x_2 + 0s_1 + 0s_2}$$

**Subject to:**
$$\begin{align}
x_1' - x_1'' + x_2 - s_1 &= 5 \quad \text{(Constraint 1 with surplus)}\\
2x_1' - 2x_1'' - x_2 + s_2 &= 8 \quad \text{(Constraint 2 with slack)}\\
x_1', x_1'', x_2, s_1, s_2 &\geq 0
\end{align}$$

---

## 🔍 Visual Comparison: Before and After

| **Aspect** | **Original** | **Final Standard Form** |
|---|---|---|
| **Objective** | Min $Z = 2x_1 - 3x_2$ | Max $W = -2x_1' + 2x_1'' + 3x_2$ |
| **Variables** | $x_1$ (unrestricted), $x_2 \geq 0$ | $x_1', x_1'', x_2, s_1, s_2$ all $\geq 0$ |
| **Constraint 1** | $x_1 + x_2 \geq 5$ (inequality) | $x_1' - x_1'' + x_2 - s_1 = 5$ (equality) |
| **Constraint 2** | $2x_1 - x_2 \leq 8$ (inequality) | $2x_1' - 2x_1'' - x_2 + s_2 = 8$ (equality) |
| **Total variables** | 2 | 5 |

---

## 📐 Understanding the Sign Pattern

### For $\geq$ constraints:

$$\text{LHS} \geq \text{RHS} \quad \Rightarrow \quad \text{LHS} - s = \text{RHS}$$

The surplus $s$ is **subtracted** because:
$$\text{LHS} = \text{RHS} + s \quad \text{(LHS is at least RHS, possibly more)}$$

### For $\leq$ constraints:

$$\text{LHS} \leq \text{RHS} \quad \Rightarrow \quad \text{LHS} + s = \text{RHS}$$

The slack $s$ is **added** because:
$$\text{LHS} = \text{RHS} - s \quad \text{(LHS is at most RHS, possibly less)}$$

---

## 🧮 Memory Aid

| Symbol | Type | Sign in Equation | Meaning |
|:---:|---|:---:|---|
| **$\leq$** | **Slack** | **+** | "Slack off" (add unused) |
| **$\geq$** | **Surplus** | **−** | "Subtract excess" (remove surplus) |
| **$=$** | None | (already equal) | No variable needed |

---

## ✅ Now Ready for Tableau!

The initial tableau would look like:

$$\begin{array}{c|ccccc|c}
\text{Basis} & x_1' & x_1'' & x_2 & s_1 & s_2 & \text{RHS}\\
\hline
s_1 & -1 & 1 & 1 & -1 & 0 & 5\\
s_2 & 2 & -2 & -1 & 0 & 1 & 8\\
\hline
W & -2 & 2 & 3 & 0 & 0 & 0
\end{array}$$

**Note:** This has a problem! $s_1$ has a coefficient of $-1$ in its own column (should be $+1$). This is why **$\geq$ constraints require Two-Phase Simplex or Big-M method** — we need artificial variables!

---

## 🎓 Key Takeaways

1. **$\leq$ constraints** → Add slack variable (+)
2. **$\geq$ constraints** → Add surplus variable (−)  
   ⚠️ *Usually requires artificial variables too!*
3. **$=$ constraints** → No slack/surplus, but need artificial variable
4. All slack, surplus, and artificial variables have **coefficient 0** in objective function
