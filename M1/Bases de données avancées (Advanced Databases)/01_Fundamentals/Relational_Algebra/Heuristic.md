Here is the breakdown of the provided text into detailed, structured notes. I have created a dedicated folder for the **Relational Algebra** portion as requested, and distributed the other topics (Concurrency, Physical Design) to their relevant chapters.

---

### 1. Create Folder: `04_Exercises_and_Scenarios/Relational_Algebra_Heuristics`

This folder contains the core logic needed for **TD 4 (Query Optimization)**.

#### File 1: `04_Exercises_and_Scenarios/Relational_Algebra_Heuristics/01_Query_Transformation_Rules.md`

```markdown
# Query Optimization Heuristics

These heuristics are transformations applied to the **Algebraic Tree** to reduce the amount of data processed before execution. They are the primary focus of **TD 4**.

## 1. Core Transformation Rules

| Rule | Symbol | Description | Goal |
| :--- | :---: | :--- | :--- |
| **Selection Pushdown** | $\sigma$ | Move filtering conditions as far down the tree as possible (towards the leaves/tables). | Reduce row count ($N$) early to minimize intermediate result sizes. |
| **Projection Pushdown** | $\pi$ | Move column selection as far down as possible. | Reduce tuple width (bytes) early to save memory and I/O. |
| **Cartesian $\to$ Join** | $\times \to \bowtie$ | Replace a Cartesian Product followed by a Selection with a specific Join operator. | Avoid generating $N \times M$ rows. |
| **Merge Selections** | $\sigma \land \sigma$ | Combine cascaded selections ($\sigma_A(\sigma_B(R))$) into one ($\sigma_{A \land B}(R)$) or split them to push specific parts down. | Optimize filter processing. |

### MySQL Implementation Example

**Scenario:** Find employees older than 30 working in the 'IT' department.

**Naive Approach (Algebra):**
$$ \sigma_{Age > 30 \land DeptName = 'IT'} (Employee \bowtie Department) $$
*SQL Equivalent:*
```sql
SELECT * 
FROM Employee E, Department D
WHERE E.DeptID = D.DeptID
AND E.Age > 30 AND D.Name = 'IT';
-- The engine might join ALL employees to ALL departments first!
```

**Optimized Approach (Heuristic Applied):**
$$ (\sigma_{Age > 30}(Employee)) \bowtie (\sigma_{Name = 'IT'}(Department)) $$
*SQL Logic:*
1. Filter `Employee` table first (Keep only Age > 30).
2. Filter `Department` table first (Keep only 'IT').
3. **Then** Join the two small results.

---

## 2. Query Rewriting Heuristics

Techniques to rewrite SQL structure for better performance without changing the result.

| Heuristic | Description | Example |
| :--- | :--- | :--- |
| **Subquery Flattening** | Convert correlated subqueries into **Joins** (Semi-joins). | `EXISTS` often runs once per row. A `JOIN` runs as a set operation (faster). |
| **Materialization** | Save the result of a complex sub-expression if it is used multiple times in the same query. | Using `WITH` clause (Common Table Expressions) in SQL. |
| **Redundancy Removal** | Detect and remove duplicate projections or identity joins. | Removing `DISTINCT` if the result is already unique via Primary Key. |

### Example: Subquery vs. Join

**Correlated Subquery (Slow):**
```sql
SELECT * FROM Products P 
WHERE EXISTS (SELECT 1 FROM Sales S WHERE S.ProductID = P.ID);
```

**Rewritten as Join (Fast):**
```sql
SELECT DISTINCT P.* 
FROM Products P 
INNER JOIN Sales S ON P.ID = S.ProductID;
```
```

---

#### File 2: `04_Exercises_and_Scenarios/Relational_Algebra_Heuristics/02_Join_Strategies.md`

```markdown
# Join Ordering and Method Heuristics

Joins are the most expensive operations in a database. Optimizing them is critical.

## 1. Join Ordering Heuristics

The order in which tables are joined affects the size of intermediate results.

| Strategy | Description | Mathematical Justification |
| :--- | :--- | :--- |
| **Smallest First** | Join the smallest or most selective relations first. | If $|A| \ll |B|$, computing $A \bowtie C$ generates fewer rows than $B \bowtie C$. |
| **Restrictive First** | If a table has a strict `WHERE` clause, join it early. | Filters reduce $N$, making the join cheaper. |
| **Greedy Approach** | In multi-way joins ($A \bowtie B \bowtie C \dots$), pick the best pair, join them, then pick the next best pair. | avoids checking all $N!$ permutations. |

**Example:**
You have tables `A` (10 rows), `B` (1,000,000 rows), and `C` (100,000 rows).
*   **Bad Order:** $(B \bowtie C) \bowtie A$ $\to$ Generates massive intermediate table.
*   **Good Order:** $(A \bowtie C) \bowtie B$ $\to$ Generates small intermediate table (limited by A's 10 rows).

---

## 2. Physical Join Algorithms

The optimizer chooses *how* to perform the join based on data characteristics.

| Algorithm | When to use (Heuristic) | SQL Context |
| :--- | :--- | :--- |
| **Nested-Loop Join** | One input is very small, or the join column is indexed. | `SELECT * FROM Small A JOIN Large B ON ...` |
| **Hash Join** | Both inputs are large, unsorted, and it's an equi-join ($=$). | Large Analytical queries (OLAP). |
| **Merge Join** | Both inputs are already **sorted** on the join key (e.g., Primary Keys). | Extremely fast, essentially a linear scan. |

```

---

#### File 3: `04_Exercises_and_Scenarios/Relational_Algebra_Heuristics/03_Algebraic_Equivalence_Reference.md`

```markdown
# Algebraic Equivalence Rules

These mathematical laws allow the optimizer to safely restructure the Query Tree (TD 4) without changing the final data output.

| Rule Name | Algebraic Notation | Explanation |
| :--- | :--- | :--- |
| **Commutativity** | $R \bowtie S \equiv S \bowtie R$ | You can swap the left and right tables in a join. |
| **Associativity** | $(R \bowtie S) \bowtie T \equiv R \bowtie (S \bowtie T)$ | You can change the grouping of joins. |
| **Selection Cascade** | $\sigma_{p \land q}(R) \equiv \sigma_p(\sigma_q(R))$ | A complex `AND` condition can be split into steps. |
| **Selection Pushdown (Join)** | $\sigma_p(R \bowtie S) \equiv (\sigma_p(R)) \bowtie S$ | If condition $p$ applies only to attributes of $R$, apply it *before* the join. |
| **Projection Pushdown** | $\pi_{List}(R \bowtie S) \equiv \pi_{L1}(R) \bowtie \pi_{L2}(S)$ | Project only needed columns from $R$ and $S$ before joining. |
| **Product to Join** | $\sigma_{cond}(R \times S) \equiv R \bowtie_{cond} S$ | Never do a raw Cross Product if a condition exists. |

> [!TIP] Exam Tip
> In **TD 4 exercises**, simply citing "Selection Pushdown" or "Associativity" is often the justification required when drawing the optimized tree.

```

---

### 2. Update: `03_Transactions_and_Security` Folder

This relates to transaction management and locking.

#### File: `03_Transactions_and_Security/04_Concurrency_Heuristics.md`

```markdown
# Concurrency Control Heuristics

Strategies used by the DBMS to manage locks and isolation levels efficiently.

## 1. Locking Strategies (Pessimistic)

| Strategy | Condition | Description |
| :--- | :--- | :--- |
| **Fine-Grained** | High concurrency, small writes. | Lock only specific **Rows**. Reduces contention but increases lock management overhead. |
| **Coarse-Grained** | Low contention, massive updates. | Lock the entire **Table**. Blocks others but has very low overhead. |
| **Lock Escalation** | Too many row locks. | If a transaction locks > 5000 rows, the DBMS upgrades it to a Table lock automatically. |

## 2. MVCC (Multi-Version Concurrency Control)
Used by **Oracle** and **PostgreSQL**.
*   **Heuristic:** "Readers do not block Writers".
*   **Mechanism:** The DB keeps old versions of updated rows. A reader sees the version that existed when their transaction started.
*   **Benefit:** Huge performance boost for Read-Heavy workloads.

## 3. Deadlock Handling
*   **Wait-Die / Wound-Wait:** Heuristics based on transaction timestamps to decide who gets killed immediately to prevent a deadlock.
*   **Timeout:** If a transaction waits > $X$ seconds for a lock, assume deadlock and abort.

```

---

### 3. Update: `01_Fundamentals` Folder

This covers physical design and system architecture concepts.

#### File: `01_Fundamentals/05_Physical_Design_Heuristics.md`

```markdown
# Physical Design & Tuning Heuristics

Rules for Indexes, Partitioning, and Caching.

## 1. Indexing Heuristics

| Rule | Best Practice | SQL Example |
| :--- | :--- | :--- |
| **High Selectivity** | Index columns used in `WHERE` clauses that filter out most rows (e.g., IDs, Emails). | `CREATE INDEX idx_email ON Users(email);` |
| **Composite Index** | Index columns that frequently appear together in `WHERE` or `ORDER BY`. | `CREATE INDEX idx_name_date ON Orders(cust_id, date);` |
| **Avoid Over-indexing** | Do NOT index columns frequently updated. | Every `UPDATE` requires updating the index tree (Overhead). |
| **Covering Index** | Create an index containing ALL columns needed by a query to avoid reading the table. | `SELECT name FROM Users WHERE id=5` (If index has ID & Name). |

## 2. Partitioning Heuristics

Splitting large tables into smaller physical pieces.

| Strategy | Use Case | Example |
| :--- | :--- | :--- |
| **Range** | Queries often filter by date ranges. | `PARTITION BY RANGE (Year)`: 2020, 2021, 2022... |
| **List** | Queries filter by distinct categories (Region, Status). | `PARTITION BY LIST (Region)`: North, South, East... |
| **Hash** | Data needs to be evenly distributed (Load balancing). | Distributing user data across 4 shards based on `UserID`. |

## 3. Cost Estimation Heuristics
When the optimizer lacks exact statistics (histograms), it uses defaults:
*   **Equality (`=`):** Assumes it returns ~10% of rows (Selectivity 0.1).
*   **Inequality (`>`):** Assumes it returns ~33% of rows (Selectivity 0.33).
*   **Unknown:** Assumes Uniform Distribution of data.

> [!WARNING] Stale Statistics
> If statistics are old, these heuristics might lead to bad plans (e.g., doing a Full Table Scan when an Index would be better). Run `ANALYZE TABLE` frequently.
```