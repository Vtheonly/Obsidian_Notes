The Simplex Method is a widely used algorithm for solving linear programming (LP) problems. LP problems involve finding the best outcome (such as maximum profit or lowest cost) given a set of constraints represented by linear relationships.

**Maximization Problem**

The notes focus on a maximization problem, where the goal is to find the highest possible value of an objective function.

**Standard Form**

*   **Step 1:  Finding a Basic Feasible Solution (Initial Tableau)**
    *   Before applying the Simplex Method, the LP problem must be converted into **standard form**. This involves:
        *   **Objective function:**  Expressing the objective function to be maximized (e.g., `Max Z = ...`).
        *   **Constraints:** Converting all inequality constraints to equality constraints by introducing **slack variables**. Slack variables represent the difference between the left and right sides of an inequality.
        *   **Non-negativity:** Ensuring all variables are non-negative (greater than or equal to zero).

*   **Step 2: Iterations Through Simplex Tableaus**
    *   Once in standard form, the problem is represented in a **simplex tableau**, which is a table that helps organize the calculations.
    *   The Simplex Method then proceeds through a series of **iterations**, moving from one basic feasible solution to another, improving the objective function value at each step until an optimal solution is reached.

**Key Concepts**

1. **Basic Feasible Solution:** A solution that satisfies all the constraints and has a set of "basic" variables (usually equal to the number of constraints) that are non-zero, while the rest ("non-basic") are zero. The initial basic feasible solution often sets the original variables to zero and the slack variables to the values on the right-hand side of the constraints.

2. **Tableau:** A table representing the system of equations in standard form. It includes:
    *   **Objective function row (Z-row):** Contains the coefficients of the objective function.
    *   **Constraint rows:** Each row represents a constraint equation.
    *   **Basic variables column (B):**  Lists the variables that are currently basic.
    *   **Constants column (b):** Contains the values on the right-hand side of the constraints.
    *   **Cj - Zj row:**  Used to determine which variable to enter into the basis (explained below).

3. **Pivot Element:** The element in the tableau that is used to perform row operations to improve the solution.

4. **Entering Variable:** The non-basic variable that is chosen to become basic (enter the basis) in the next iteration. It's selected based on the most negative value in the `Cj - Zj` row (for maximization problems). The column of the entering variable is called the **pivot column**.

5. **Leaving Variable:** The basic variable that is chosen to become non-basic (leave the basis) in the next iteration. It's determined by the **minimum ratio test** (explained below). The row of the leaving variable is called the **pivot row**.

6. **Minimum Ratio Test:** This test helps identify the leaving variable. For each row, divide the value in the `b` column by the corresponding positive value in the pivot column. The row with the smallest non-negative ratio is the pivot row, and the corresponding basic variable is the leaving variable.

7. **Pivoting:** The process of using the pivot element to transform the tableau. It involves:
    *   Making the pivot element equal to 1 (by dividing the entire pivot row by the pivot element).
    *   Making all other elements in the pivot column equal to 0 (by performing row operations).

**Example Walkthrough**

Let's follow the example provided in the notes:

**Original Problem:**

```
Max Z = 300x1 + 500x2
Subject to:
x1 <= 4
2x2 <= 12
3x1 + 2x2 <= 18
x1 >= 0, x2 >= 0
```

**Standard Form:**

```
Max Z = 300x1 + 500x2 + 0x3 + 0x4 + 0x5
Subject to:
x1 + x3 = 4
2x2 + x4 = 12
3x1 + 2x2 + x5 = 18
x1, x2, x3, x4, x5 >= 0
```

*   `x3`, `x4`, and `x5` are slack variables introduced to convert the inequalities to equalities.

**Initial Tableau:**

| Max | Cj | 300 | 500 | 0   | 0   | 0   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CB  | B   | b   | x1  | x2  | x3  | x4  | x5  |
| 0   | x3  | 4   | 1   | 0   | 1   | 0   | 0   |
| 0   | x4  | 12  | 0   | **2** | 0   | 1   | 0   |
| 0   | x5  | 18  | 3   | 2   | 0   | 0   | 1   |
|     | Zj  | 0   | 0   | 0   | 0   | 0   | 0   |
|     | Cj-Zj|     | 300 | 500 | 0   | 0   | 0   |

*   **Entering Variable:** `x2` (most negative `Cj - Zj`)
*   **Pivot Column:** The column under `x2`
*   **Minimum Ratio Test:** 4/0 (undefined), 12/2 = 6, 18/2 = 9. The smallest is 6, so `x4` is the leaving variable.
*   **Pivot Row:** The row of `x4`
*   **Pivot Element:** 2 (in the intersection of pivot row and pivot column)

**Pivoting (Tableau 2):**

1. Divide the pivot row (x4 row) by 2 to make the pivot element 1.
2. Perform row operations to make other elements in the pivot column 0.
    *   Subtract 2 times the new pivot row from the x5 row.
    *   The x3 row already has 0 in the pivot column, so it doesn't change.

**Tableau 2:**

| Max | Cj    | 300 | 500 | 0   | 0    | 0   |     |
| --- | ----- | --- | --- | --- | ---- | --- | --- |
| CB  | B     | b   | x1  | x2  | x3  | x4   | x5  |
| 0   | x3    | 4   | 1   | 0   | 1   | 0    | 0   |
| 500 | x2    | 6   | 0   | 1   | 0   | 1/2  | 0   |
| 0   | x5    | 6   | 3   | 0   | 0   | -1   | 1   |
|     | Zj    | 3000| 0   | 500 | 0   | 250  | 0   |
|     | Cj-Zj |     | 300 | 0   | 0   | -250 | 0   |

*   **New Entering Variable:**  x1
*   **New Pivot Column:** x1
*   **Minimum ratio test:** 4/1=4, 6/0 (undefined), 6/3=2.
*   **New pivot row:** x5
*   **New pivot element:** 3

**Pivoting (Tableau 3):**
1. Divide pivot row by 3
2. Substract the new pivot row from x3's row.
3. x2 row already has a 0 in the pivot column so it does not change.

**Tableau 3 (Final):**

| Max | Cj    | 300 | 500 | 0    | 0     | 0    |     |
| --- | ----- | --- | --- | ---- | ----- | ---- | --- |
| CB  | B     | b   | x1  | x2  | x3   | x4    | x5   |
| 0   | x3    | 2   | 0   | 0   | 1    | 1/3   | -1/3 |
| 500 | x2    | 6   | 0   | 1   | 0    | 1/2   | 0    |
| 300 | x1    | 2   | 1   | 0   | 0    | -1/3  | 1/3  |
|     | Zj    | 3600| 300 | 500 | 0    | 100   | 100  |
|     | Cj-Zj |     | 0   | 0   | 0    | -100  | -100 |

**Optimal Solution:**

*   The algorithm stops when all `Cj - Zj` values are non-positive (for maximization).
*   **Optimal solution:** `x1 = 2`, `x2 = 6`, `x3 = 2`, `x4 = 0`, `x5 = 0`
*   **Maximum value of Z:** 3600

**In essence, the Simplex Method systematically explores the corners of the feasible region (defined by the constraints) to find the corner that yields the highest objective function value.**
