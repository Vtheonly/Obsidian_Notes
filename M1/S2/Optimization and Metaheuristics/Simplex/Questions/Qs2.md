what is the Basis?

Here is the explanation of **Basis ($B$)** broken down into three perspectives, followed by a numerical example.

### **The Example: The Furniture Factory**
Let's assume a factory with **2 constraints** (Wood and Glue).
You have **4 variables** to choose from:
1.  Make Tables ($x_1$)
2.  Make Chairs ($x_2$)
3.  Leave Wood unused ($s_1$)
4.  Leave Glue unused ($s_2$)

The Algebra ($A$) looks like this:
$$ \begin{bmatrix} 4 & 1 & 1 & 0 \\ 2 & 2 & 0 & 1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ s_1 \\ s_2 \end{bmatrix} = \begin{bmatrix} 20 \\ 10 \end{bmatrix} $$
*   **$m = 2$** (Rows/Constraints)
*   **$n = 4$** (Columns/Variables)

---

### **1. Explanation: The Selection View (Simplest)**
A "Basis" is simply **picking exactly $m$ active variables** to solve the system.
Since we have 2 constraints ($m=2$), we can only solve for 2 variables at a time. The Basis is the **group of 2 columns** you have currently selected to be non-zero.
*   Everything *in* the Basis gets calculated (Basic Variables).
*   Everything *not* in the Basis is set to zero (Non-Basic Variables).

### **2. Explanation: The Matrix View (Visual)**
The matrix $A$ is a wide rectangle ($2 \times 4$). You cannot calculate the "inverse" or "solution" of a rectangle.
To do math, you need a **Square**.
The Basis ($B$) is formed by **cutting out** $m$ specific columns from $A$ to create a square ($2 \times 2$) matrix.
*   **"Nonsingular"** means this square matrix isn't broken; it has a valid inverse so you can actually find a solution.

### **3. Explanation: The Geometric View (Corners)**
In Linear Programming, the solution is always at a "Corner" (Vertex) of the feasible region.
The **Basis** is the mathematical coordinate of that corner.
*   Corner 1 might be "Make nothing" (Basis = $\{s_1, s_2\}$).
*   Corner 2 might be "Make only Tables" (Basis = $\{x_1, s_2\}$).
*   Changing the Basis means moving from one corner to the next.

---

### **How it looks in the Example**

We need to pick **2 columns** ($m$) to form matrix $B$.

#### **Scenario A: The "Do Nothing" Basis (Starting Point)**
We choose the slack variables ($s_1, s_2$). These are columns 3 and 4.
$$ B = \text{Columns } 3, 4 = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} $$
*   **Is it square?** Yes ($2 \times 2$).
*   **Is it nonsingular?** Yes (It's an Identity matrix).
*   **Result:** We solve for $s_1, s_2$. We set $x_1, x_2 = 0$.

#### **Scenario B: The "Make Tables" Basis**
We want to solve for Tables ($x_1$) and leftover Glue ($s_2$). We pick Column 1 and Column 4.
$$ B = \text{Columns } 1, 4 = \begin{bmatrix} 4 & 0 \\ 2 & 1 \end{bmatrix} $$
*   **Is it square?** Yes ($2 \times 2$).
*   **Is it nonsingular?** Yes. (Determinant is $4 \times 1 \neq 0$).
*   **Result:** We can algebraically solve this system to find the exact number of Tables.

#### **Scenario C: A "Singular" (Bad) Basis**
What if we pick Column 1 ($x_1$) and a column that is just a copy of it (let's pretend Column 2 was $[8, 4]$)?
$$ B = \begin{bmatrix} 4 & 8 \\ 2 & 4 \end{bmatrix} $$
*   **Problem:** The second column is just $2 \times$ the first. They are **Linearly Dependent**.
*   **Result:** This matrix is **Singular** (Determinant is 0). You cannot solve it. This is not a valid Basis.