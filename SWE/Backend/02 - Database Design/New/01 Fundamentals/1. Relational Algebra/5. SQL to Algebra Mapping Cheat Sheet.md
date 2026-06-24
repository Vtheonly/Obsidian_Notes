# SQL to Algebra Mapping Cheat Sheet

This mapping is essential for **TD 2** (translating SQL queries to Algebra).

## Basic Mapping Table

| SQL Clause             | Algebraic Operator         | Notes                         |
| :--------------------- | :------------------------- | :---------------------------- |
| `SELECT DISTINCT x, y` | $\pi_{x, y}$ (Projection)  | Algebra is always distinct.   |
| `FROM A, B`            | $A \times B$ (Product)     |                               |
| `WHERE x = 5`          | $\sigma_{x=5}$ (Selection) |                               |
| `UNION`                | $\cup$ (Union)             | Requires union-compatibility. |
| `EXCEPT` / `MINUS`     | $-$ (Difference)           |                               |
| `INTERSECT`            | $\cap$ (Intersection)      |                               |
| `JOIN ... ON ...`      | $\bowtie_{cond}$ (Join)    |                               |
| `AS`                   | $\rho$ (Rename)            |                               |

## Complex Mapping Examples

### 1. The "Double Negation" (Division)

**Query:** Find students who have taken ALL courses.

- **SQL Logic:** Find students where there is NOT a course that they have NOT taken.

```sql
SELECT S.Name FROM Student S
WHERE NOT EXISTS (
    SELECT C.ID FROM Course C
    WHERE NOT EXISTS (
        SELECT * FROM Grades G
        WHERE G.SID = S.ID AND G.CID = C.ID
    )
);
```

- **Algebra:**
  $$ \pi*{SID, CID}(Grades) \div \pi*{CID}(Course) $$

### 2. Self-Join

**Query:** Find employees earning more than their manager.

- **SQL Logic:**

```sql
SELECT E.Name
FROM Employee E, Employee M
WHERE E.ManagerID = M.ID
AND E.Salary > M.Salary;
```

- **Algebra:**
  We need to rename `Employee` to `M` (Manager) to join it with `Employee` (E).
  $$ \pi*{E.Name} ( \sigma*{E.Salary > M.Salary} ( \rho*E(Employee) \bowtie*{E.ManagerID = M.ID} \rho_M(Employee) ) ) $$

> [!TIP] Constructing the Algebra
> When writing Algebra for TD2:
>
> 1.  Start from the inside (Relations/Tables).
> 2.  Apply **Selection** ($\sigma$) conditions (the `WHERE`).
> 3.  Apply **Joins** ($\bowtie$) to connect tables.
> 4.  Apply **Projection** ($\pi$) last (the `SELECT`) to define what you output.
