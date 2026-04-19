Here is the complete, easy-to-understand guide on exactly how to determine which variables go into that first column (the **Base Var** column) of your initial Simplex tableau, and why certain variables are absolutely forbidden from being there.

---

# 🏗️ Choosing Initial Basic Variables

## 1. The Golden Rule of Basic Variables
To start the Simplex algorithm, you need an **Initial Basic Feasible Solution (IBFS)**. This corresponds to starting at the origin (zero) on a graph. 

The rule is strictly this: **You must have exactly ONE basic variable for EVERY constraint row.** 
* If you have 2 constraints, your `Base Var` column will have 2 variables.
* If you have 3 constraints, your `Base Var` column will have 3 variables.

All **non-basic variables** (the ones not in that first column) are automatically set to **0**.

---

## 2. The Visual Test: The "Unit Vector" Rule
For a variable to be allowed in the `Base Var` column, **its column in the math equations must look like an identity matrix (a unit vector).** 
This means it must have a coefficient of **`+1`** in its own row, and **`0`** in every other row.

Let's look at the "Who's Who" of variables to see who passes this test.

### ❌ Who CANNOT be an initial Basic Variable?

#### 1. The Original Decision Variables ($x_1, x_2$)
* **Why:** They represent the products you are making. At the very beginning of the problem (before you start optimizing), you assume you are making *nothing*. Therefore, $x_1 = 0$ and $x_2 = 0$. Because they are zero, they are **non-basic**.
* **Visual reason:** Their coefficients are messy (like $3x_1 + 2x_2$). They do not have a clean `+1` and `0`s.

#### 2. Surplus Variables ($-s_i$ or $-x_i$) from $\ge$ constraints
* **Why:** This is the most common trap! If you have $x_1 + x_2 - s_1 = 4$, and you set $x_1=0, x_2=0$, then you are left with $-s_1 = 4 \implies s_1 = -4$. 
* **The Rule of LP:** ALL variables must be $\ge 0$. You cannot have a negative variable. Therefore, surplus variables **cannot** be basic variables.

---

### ✅ Who CAN be an initial Basic Variable?

#### 1. Slack Variables ($+s_i$ or $+x_i$) from $\le$ constraints
* **Why:** If a constraint is $x_1 + x_2 + s_1 = 10$, and you set $x_1=0, x_2=0$, you are left with exactly **$s_1 = 10$**. It is positive, it is legal, and its coefficient is $+1$. 
* **Verdict:** Slack variables are **always** the initial basic variable for their row.

#### 2. Artificial Variables ($+a_i$) from $\ge$ or $=$ constraints
* **Why:** Because surplus variables fail the test (see above), mathematicians invented Artificial Variables. If you have $x_1 + x_2 - s_1 + a_1 = 4$, you set $x_1, x_2, s_1$ all to zero. You are left with exactly **$a_1 = 4$**. 
* **Verdict:** Artificial variables are **always** the initial basic variable for their row.

---

## 3. The Ultimate Cheat Sheet
When you are building your initial tableau, just look at the **original sign of the constraint**. That tells you exactly what goes in the `Base Var` column.

| Original Constraint Sign | What do you add algebraically? | **Which one goes in the `Base Var` column?** |
| :---: | :--- | :--- |
| **$\le$** | Add Slack ($+s_1$) | **The Slack Variable** ($s_1$) |
| **$\ge$** | Subtract Surplus ($-s_2$), Add Artificial ($+a_1$) | **The Artificial Variable** ($a_1$) |
| **$=$** | Add Artificial ($+a_2$) | **The Artificial Variable** ($a_2$) |

---

## 4. Let's Look at an Example from Your Notes

Let's look at **Example 5** from your notes:
1. $1x_1 + 0x_2 \le 4$  **(Row 1)**
2. $0x_1 + 2x_2 \le 12$ **(Row 2)**
3. $3x_1 + 2x_2 \le 18$ **(Row 3)**

Because these are all **$\le$** constraints, we add three positive slack variables ($x_3, x_4, x_5$):
1. $1x_1 + 0x_2 \mathbf{+ 1x_3} = 4$
2. $0x_1 + 2x_2 \mathbf{+ 1x_4} = 12$
3. $3x_1 + 2x_2 \mathbf{+ 1x_5} = 18$

**How to pick the base variables:**
* For Row 1, $x_3$ has the `+1`. It becomes the basic variable.
* For Row 2, $x_4$ has the `+1`. It becomes the basic variable.
* For Row 3, $x_5$ has the `+1`. It becomes the basic variable.

That is why your initial tableau's first column looks exactly like this:
| Base Var |
| :--- |
| **$x_3$** |
| **$x_4$** |
| **$x_5$** |

### What if Row 2 was a $\ge$ constraint?
If row 2 was $0x_1 + 2x_2 \ge 12$, you would subtract surplus and add artificial:
2. $0x_1 + 2x_2 - 1x_4 \mathbf{+ 1a_1} = 12$

Your `Base Var` column would instantly change to:
| Base Var |
| :--- |
| **$x_3$** *(from row 1 slack)* |
| **$a_1$** *(from row 2 artificial)* |
| **$x_5$** *(from row 3 slack)* |

> [!success] Summary
> You don't have to guess. You just read the equations. 
> Every row must contribute exactly one variable to the `Base Var` column. That variable is simply whichever one you added with a **$+1$ coefficient** ($+s$ or $+a$) to make the equation an equality!
