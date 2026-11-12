# Recursive Queries (`WITH RECURSIVE`)

This note integrates **Chapter 2 (Slides 77–103)**, **TP 2 (Exercise 11 & Part IV Q17)**, **TD 2 (Exercise 5)**, **TP 3 (Part II Exercises 8–14 & Part III Exercise 16)**, and **TD 3 (Part II Exercises 7*–9)**.

---

## 1. Motivation & Self-Referencing Hierarchies (Ch 2 Slides 77–89)

Hierarchical structures appear everywhere with an **unknown or variable number of levels**:
1. **Company/Organizational charts** (CEO $\to$ Managers $\to$ Team Leads $\to$ Employees).
2. **Folders and directories** (`/` $\to$ `Users` $\to$ `keith` $\to$ subfolders).
3. **E-commerce categories & subcategories** (Category $\to$ Sub-category $\to$ Products).
4. **University management hierarchies** (Board $\to$ Rector $\to$ Pro-Rectors $\to$ Faculties $\to$ Departments).

### Critical Structural Distinction (Ch 2 Slide 83)
- `department` $\to$ `class` $\to$ `student` is **NOT recursive** because it connects **different types of entities** across fixed tables.
- **`manager(manager_id, name, supervisor_id REFERENCES manager(manager_id))`** **IS recursive** because rows of the **same table** reference other rows in that **same table** via a **self-referencing foreign key** (`node_id, parent_id`).
- A single self-join (`FROM manager m LEFT JOIN manager s ON m.supervisor_id = s.manager_id`, Ch 2 Slides 90–91) retrieves **only one level** (the immediate supervisor). Without recursion, traversing arbitrary depth is impossible in standard SQL.

---

## 2. `WITH RECURSIVE` Mechanics, `UNION ALL`, and Termination

```sql
WITH RECURSIVE cte_name AS (
    -- 1. Anchor member: starting row(s) -> T0
    SELECT ...
    FROM source_table
    WHERE root_condition

    UNION ALL

    -- 2. Recursive member: references cte_name -> T1, T2, ...
    SELECT ...
    FROM source_table AS s
    JOIN cte_name AS c ON s.parent_id = c.id
)
SELECT * FROM cte_name;
```

### Key Elements (TP 2 Part IV Q17 & Ch 2 Slides 92, 100, 103)
- **Anchor Member:** Non-recursive base query executed **once** to seed the initial working table $T_0$ (e.g., `WHERE supervisor_id IS NULL` or `WHERE manager_id = 1`).
- **Recursive Member:** Repeatedly joins the source table against **the rows produced by the immediately preceding step** ($T_{i-1} \to T_i$), incrementing `level + 1`.
- **`UNION ALL` vs. `UNION`:** `UNION ALL` combines $T_0, T_1, T_2, \dots$ **without removing duplicates**, which is standard and faster for trees because each depth level contributes new rows. (`UNION` deduplicates rows.)
- **Termination & Cycle Risk (TP 2 Ex 11):** Recursion terminates automatically when an iteration produces **0 new rows** ($T_k = \emptyset$) or a predicate stops matching. **If the data contains a cycle** (A reports to B and B reports to A), `UNION ALL` enters **infinite recursion** unless cycle prevention (e.g., tracking visited IDs in an array `NOT (m.manager_id = ANY(visited_path))` or PostgreSQL `CYCLE` clause) is used!

---

## 3. Worked Hierarchy Trace (`manager` Table: Ch 2, TP 2 Ex 11 & TP 3 Ex 8–9)

> [!NOTE] Schema Difference Between Ch 2 / TP 2 and TP 3
> - **Ch 2 Slides (86–102) & TP 2 Ex 11:** Column is `name`, with **5 rows** (`level` 0 to 4: `1 General Director` $\to$ `2 Dean of Computer Science` $\to$ `3 GL/IA Dept Head` $\to$ `4 M1 GL/IA Manager` $\to$ `5 SQL Module Manager`).
> - **TP 3 Ex 8–16:** Column is `manager_name`, FK constraint `fk_supervisor`, with **6 rows** (`level` 0 to 5, inserting `Head of Informatics` and renaming the bottom coordinator to `Database Module Coordinator`). Drop/recreate `manager` if switching from TP 2 to TP 3!

### TP 3 Ex 8 Setup (6-Row Hierarchy) & Ex 9 Complete Hierarchy
```sql
CREATE TABLE manager (
    manager_id INTEGER PRIMARY KEY,
    manager_name VARCHAR(100) NOT NULL,
    supervisor_id INTEGER,
    CONSTRAINT fk_supervisor FOREIGN KEY (supervisor_id) REFERENCES manager(manager_id)
);

INSERT INTO manager (manager_id, manager_name, supervisor_id) VALUES
(1, 'General Director', NULL),
(2, 'Dean of Computer Science', 1),
(3, 'Head of Informatics', 2),
(4, 'GL Department Head', 3),
(5, 'M1 GL Coordinator', 4),
(6, 'Database Module Coordinator', 5);

-- TP 3 Ex 9 / Ch 2 Slide 102
WITH RECURSIVE hierarchy AS (
    SELECT manager_id, manager_name, supervisor_id, 0 AS level
    FROM manager
    WHERE supervisor_id IS NULL
    UNION ALL
    SELECT m.manager_id, m.manager_name, m.supervisor_id, h.level + 1
    FROM manager m
    JOIN hierarchy h ON m.supervisor_id = h.manager_id
)
SELECT manager_id, manager_name, supervisor_id, level
FROM hierarchy
ORDER BY level, manager_id;
```

### Step-by-Step Execution Trace
| Step | Working Set | Condition Evaluated | Result Tuple Produced | `level` |
| :--- | :--- | :--- | :--- | :---: |
| **$T_0$ (Anchor)** | `manager` | `supervisor_id IS NULL` | `(1, 'General Director', NULL)` | `0` |
| **$T_1$** | $T_0$ (`id=1`) | `m.supervisor_id = 1` | `(2, 'Dean of Computer Science', 1)` | `1` |
| **$T_2$** | $T_1$ (`id=2`) | `m.supervisor_id = 2` | `(3, 'Head of Informatics', 2)` | `2` |
| **$T_3$** | $T_2$ (`id=3`) | `m.supervisor_id = 3` | `(4, 'GL Department Head', 3)` | `3` |
| **$T_4$** | $T_3$ (`id=4`) | `m.supervisor_id = 4` | `(5, 'M1 GL Coordinator', 4)` | `4` |
| **$T_5$** | $T_4$ (`id=5`) | `m.supervisor_id = 5` | `(6, 'Database Module Coordinator', 5)` | `5` |
| **$T_6$** | $T_5$ (`id=6`) | `m.supervisor_id = 6` | **Empty ($\emptyset$) $\to$ Terminates!** | — |

---

## 4. Subtrees, Paths & Aggregations (TP 3 Ex 10–14 & Ex 16)

### Ex 10: All Subordinates of Manager ID 2 (+ Additional Tasks)
```sql
WITH RECURSIVE subordinates AS (
    -- Direct subordinates of manager 2 start at relative level 1
    SELECT manager_id, manager_name, supervisor_id, 1 AS level
    FROM manager
    WHERE supervisor_id = 2
    UNION ALL
    SELECT m.manager_id, m.manager_name, m.supervisor_id, s.level + 1
    FROM manager m
    JOIN subordinates s ON m.supervisor_id = s.manager_id
)
SELECT * FROM subordinates ORDER BY level, manager_id;
-- Expected: (3, Head of Informatics, 2, 1), (4, GL Dept Head, 3, 2), (5, M1 GL Coord, 4, 3), (6, DB Module Coord, 5, 4)
```
- *Additional Task 1 & 2:* Change `WHERE supervisor_id = 2` to `= 1` (returns managers 2–6) or `= 4` (returns managers 5–6).
- *Additional Task 3 (Direct subordinates of manager 1 without recursion):*
  `SELECT * FROM manager WHERE supervisor_id = 1;`

### Ex 11 & Ex 16: Building the Hierarchical Path & Complete Report
In PostgreSQL, cast the anchor string with **`::TEXT`** so `h.path || ' -> ' || m.manager_name` does not fail type checking against `VARCHAR(100)`:
```sql
WITH RECURSIVE hierarchy AS (
    SELECT manager_id, manager_name, supervisor_id, 0 AS level,
           manager_name::TEXT AS path
    FROM manager
    WHERE supervisor_id IS NULL
    UNION ALL
    SELECT m.manager_id, m.manager_name, m.supervisor_id, h.level + 1,
           h.path || ' -> ' || m.manager_name
    FROM manager m
    JOIN hierarchy h ON m.supervisor_id = h.manager_id
)
SELECT manager_id, manager_name, supervisor_id, level, path
FROM hierarchy
ORDER BY level, manager_id;
-- Manager 6 path:
-- General Director -> Dean of Computer Science -> Head of Informatics -> GL Department Head -> M1 GL Coordinator -> Database Module Coordinator
```

### Ex 12, 13, 14: Aggregating & Filtering Over `hierarchy`
Using the `hierarchy` CTE from Ex 9:
```sql
-- Ex 12: Maximum hierarchical level -> returns 5
SELECT MAX(level) AS maximum_level FROM hierarchy;

-- Ex 13: Count managers at each level -> returns 0..5 each with count 1
SELECT level, COUNT(*) AS number_of_managers
FROM hierarchy
GROUP BY level
ORDER BY level;

-- Ex 14: Managers at the deepest level -> returns (6, 'Database Module Coordinator', 5)
SELECT manager_id, manager_name, level
FROM hierarchy
WHERE level = (SELECT MAX(level) FROM hierarchy);
```

---

## 5. Worked Solutions: TD 2 Ex 5 & TD 3 Part II (Ex 7*–9)

### TD 3 Ex 7*: Exploring a `department` Hierarchy
Extending `department(department_id, department_name, parent_department_id)` where `parent_department_id` references `department_id`:
```sql
WITH RECURSIVE dept_hierarchy AS (
    -- Anchor: start at department 1
    SELECT department_id, department_name, parent_department_id, 0 AS level
    FROM department
    WHERE department_id = 1
    UNION ALL
    -- Recursive: find direct subdepartments of already discovered departments
    SELECT d.department_id, d.department_name, d.parent_department_id, dh.level + 1
    FROM department d
    JOIN dept_hierarchy dh ON d.parent_department_id = dh.department_id
)
SELECT * FROM dept_hierarchy ORDER BY level, department_id;
```

### TD 2 Ex 5 & TD 3 Ex 8: Generating Integers 1 to 10 (+ Recursive CTE vs. Loop)
```sql
WITH RECURSIVE numbers(n) AS (
    SELECT 1          -- Anchor member: initial value 1
    UNION ALL
    SELECT n + 1      -- Recursive member: increments previous row
    FROM numbers
    WHERE n < 10      -- Termination condition: stops generating once n reaches 10
)
SELECT n FROM numbers;
```
- **Recursive CTE vs. Procedural Loop (TD 2 Ex 5.4):** A **recursive CTE** is a **declarative SQL query** producing a relation/result set directly inside `SELECT` (no mutable variables or procedural statements), whereas a **procedural loop** (`FOR`, `WHILE`, `LOOP`) is an **imperative control flow** construct inside SQL/PSM or PL/pgSQL used to execute step-by-step instructions, side effects, or DML.

### TD 3 Ex 9: Tracing Recursive Iterations (`WHERE n < 5`)
```sql
WITH RECURSIVE numbers(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1
    FROM numbers
    WHERE n < 5
)
SELECT n FROM numbers;
```
1. **Result:** **`1, 2, 3, 4, 5`** (5 rows!).
2. **Anchor query:** `SELECT 1` (produces `{1}`).
3. **Recursive query:** `SELECT n + 1 FROM numbers WHERE n < 5`.
4. **Iterations:**
   - Iter 1 reads `1` (`1 < 5` true) $\to$ outputs `2`.
   - Iter 2 reads `2` (`2 < 5` true) $\to$ outputs `3`.
   - Iter 3 reads `3` (`3 < 5` true) $\to$ outputs `4`.
   - Iter 4 reads `4` (`4 < 5` true) $\to$ outputs **`5`**.
5. **Why recursion stops:** In Iteration 5, the working row is `5`. Since `5 < 5` is **false**, the recursive query produces **0 rows**, terminating recursion! *(Exam trap: `WHERE n < 5` stops at **5**, not 4, because `4 < 5` generates `4 + 1 = 5`!)*
