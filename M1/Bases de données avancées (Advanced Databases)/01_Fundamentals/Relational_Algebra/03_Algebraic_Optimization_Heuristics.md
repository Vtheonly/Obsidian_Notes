
# Algebraic Optimization & Query Trees

## 1. The Query Tree
SQL queries are parsed into **Algebraic Trees** by the DBMS before execution. The structure of this tree determines the speed of the query.

**Structure:**
*   **Leaves:** Base Relations (Tables).
*   **Internal Nodes:** Intermediate operations ($\sigma, \pi, \bowtie$).
*   **Root:** The final result.

---

## 2. Optimization Heuristics
In **TD 4**, you are asked to transform a "Bad Tree" into a "Good Tree". You do this by applying specific rules (heuristics).

### Rule #1: Push Selections Down ($\sigma$)
**The most important rule.**
*   **Why?** Applying a filter early reduces the number of rows.
*   **Action:** Move $\sigma$ conditions as close to the leaves (tables) as possible.
*   **Impact:** Reducing rows before a Join ($\bowtie$) drastically lowers computational cost.

### Rule #2: Push Projections Down ($\pi$)
*   **Why?** Applying projection early reduces the width (size in bytes) of the tuples.
*   **Action:** If you only need the `Name` column, don't carry `Address`, `Phone`, and `Bio` through the whole tree.
*   **Impact:** Saves memory (RAM) and I/O.

### Rule #3: Join Ordering
*   **Action:** When joining multiple tables ($A \bowtie B \bowtie C$), join the most restrictive (smallest) tables first.
*   **Impact:** Keeps intermediate results small.

---

## 3. Example: Optimizing a Query (TD 4 Style)

**Query:** Find the names of students who got an 'A' in 'Database'.

```sql
SELECT S.Name
FROM Student S, Grade G, Course C
WHERE S.ID = G.StudentID 
  AND G.CourseID = C.CourseID
  AND C.Title = 'Database'
  AND G.Score = 'A';
```

### The "Bad" Tree (Canonical)
1.  Product: $Student \times Grade \times Course$ (Huge size!)
2.  Select: Apply all conditions at the end.
3.  Project: Get Name.

### The "Optimized" Tree
1.  **Selection on Course:** $\sigma_{Title='Database'}(Course)$ (Returns 1 row).
2.  **Selection on Grade:** $\sigma_{Score='A'}(Grade)$ (Returns subset).
3.  **Join 1:** Result of (1) $\bowtie$ Result of (2).
4.  **Join 2:** Result of (3) $\bowtie$ Student.
5.  **Projection:** $\pi_{Name}$.

### Comparison Table

| Strategy | Operation Order | Intermediate Data Size | Efficiency |
| :--- | :--- | :--- | :--- |
| **Canonical (Naive)** | Join All $\to$ Filter | **Huge** (Millions of rows) | 🔴 Very Slow |
| **Optimized** | Filter First $\to$ Join | **Tiny** (Only relevant rows) | 🟢 Very Fast |
