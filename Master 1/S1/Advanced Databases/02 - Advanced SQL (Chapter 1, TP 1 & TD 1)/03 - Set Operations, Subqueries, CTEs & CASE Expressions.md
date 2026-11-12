# Set Operations, Subqueries, CTEs & CASE Expressions

This note integrates **Chapter 1 (Slides 30–43, 49)**, **TD 1 (Questions 20\*–29, 31)**, **TP 2 Ex 12 Task 9**, and advanced querying/optimization concepts (`ANY`/`ALL`/`SOME`, Set Ops vs. Joins, Division, and SQL best practices).

---

## 1. Set Operations (`UNION`, `INTERSECT`, `EXCEPT`) vs. Joins

Set operations combine results **vertically** (requiring identical column count and compatible types); joins link rows **horizontally**.

### Course `university` Examples (Ch 1 Slides 31–33)

```sql
-- UNION (removes duplicates; use UNION ALL to keep duplicates & avoid sort/hash overhead)
SELECT last_name FROM student WHERE class_id = 10
UNION
SELECT last_name FROM student WHERE class_id = 20;
-- Result: Ahmed, Ali, Amine, Benali

-- INTERSECT (common rows)
SELECT last_name FROM student WHERE class_id = 10
INTERSECT
SELECT last_name FROM student WHERE class_id = 20;
-- Result: Ali

-- EXCEPT (in first query, absent from second)
SELECT last_name FROM student WHERE class_id = 10
EXCEPT
SELECT last_name FROM student WHERE last_name = 'Ahmed';
-- Result: Ali
```

### Three Critical Differences: `INTERSECT` vs. `INNER JOIN`

1. **Duplicates:** `INTERSECT` (set) returns each matching value **once**. `INNER JOIN` **multiplies** duplicates ($5 \times 5 = 25$ rows if an ID appears 5 times on each side; requires `DISTINCT` to mimic `INTERSECT`).
2. **`NULL` Values:** **`INTERSECT` treats `NULL = NULL` as a match**, whereas **`INNER JOIN` drops `NULL` rows** (because `NULL = NULL` evaluates to `UNKNOWN`).
3. **Column Flexibility:** `INTERSECT` requires identical schemas in both queries; `INNER JOIN` can project arbitrary columns from both tables.
   _(Dialect note: PostgreSQL supports `UNION`, `INTERSECT`, and `EXCEPT` natively. Older MySQL lacks `INTERSECT` and `EXCEPT`, requiring `WHERE col IN (...)` and `WHERE col NOT IN (...)` / `NOT EXISTS`.)_

---

## 2. Subqueries, Correlation & `EXISTS` vs. `JOIN`

- **Non-Correlated Subquery:** Inner query executes independently once and returns a scalar or set (`WHERE salary > (SELECT AVG(salary) FROM teacher)`).
- **Correlated Subquery:** Inner query references a column from the outer row (`WHERE t.department_id = d.department_id`). Logically evaluated per outer row.
- **`EXISTS (SELECT 1 FROM ...)`:** Stops scanning the inner table the instant **one** matching row is found (often much faster than `JOIN` when you only test existence and don't need columns from the inner table; writing `SELECT 1` is standard convention because only row existence matters).
- **The `NOT IN` NULL Trap:** If a subquery inside `NOT IN (...)` returns **even a single `NULL`**, `x NOT IN (1, 2, NULL)` evaluates to `UNKNOWN` for every row and returns **0 rows**! Always prefer **`NOT EXISTS`** (or add `WHERE col IS NOT NULL` inside the subquery).

---

## 3. Quantified Operators: `ANY`, `SOME`, and `ALL` (Ch 1 Slides 40–41)

Multi-row subqueries cannot be compared with plain `>` or `=`. SQL provides `ANY`, `SOME` (exact synonym of `ANY`), and `ALL`:

| Operator                       | Meaning                                                   | Mathematical Equivalent (No `NULL`s) |
| :----------------------------- | :-------------------------------------------------------- | :----------------------------------- |
| `x > ANY (S)` / `x > SOME (S)` | True if $x$ is greater than **at least one** value in $S$ | `x > MIN(S)`                         |
| `x < ANY (S)`                  | True if $x$ is less than **at least one** value in $S$    | `x < MAX(S)`                         |
| `x = ANY (S)`                  | Equal to at least one value in $S$                        | `x IN (S)`                           |
| `x > ALL (S)`                  | True if $x$ is greater than **every** value in $S$        | `x > MAX(S)`                         |
| `x < ALL (S)`                  | True if $x$ is less than **every** value in $S$           | `x < MIN(S)`                         |
| `x <> ALL (S)`                 | Not equal to any value in $S$                             | `x NOT IN (S)`                       |

> [!WARNING] Two `ALL` Traps on Exams!
>
> 1. **The `NULL` Trap:** If the subquery returns `[100, 200, NULL]`, `x > ALL (...)` expands to `x > 100 AND x > 200 AND x > NULL`, yielding **`UNKNOWN`** and returning **0 rows**! Always filter `AND salary IS NOT NULL` inside `ALL` subqueries when `NULL` is possible.
> 2. **Ch 1 Slide 41 (`> ALL` on Department 2):** `SELECT last_name, salary FROM teacher WHERE salary > ALL (SELECT salary FROM teacher WHERE department_id = 2);` returns **0 rows**! Why? Department 2 (`Mathématiques`) contains `Karim` (`48000`) and `Haddad` (`85000`), and `85000` is already the maximum salary across the entire university—no teacher earns strictly more than `85000`.
>    _(Meanwhile, Slide 40 `> ANY` on Department 2 returns the 6 teachers earning $> 48000$: Benali `75000`, Saidi `62000`, Haddad `85000`, Mansouri `55000`, Rahmani `72000`, Ahmed `68000`.)_

---

## 4. Common Table Expressions (`WITH`) & Conditional `CASE`

### Common Table Expressions (`WITH`) — Ch 1 Slides 42–43

A **CTE** defines a named temporary virtual table scoped strictly to a single query, replacing unreadable nested subqueries:

```sql
-- Ch 1 Slide 43: Teachers earning more than the overall average salary
WITH average_salary AS (
    SELECT AVG(salary) AS avg_salary
    FROM teacher
)
SELECT t.last_name, t.salary
FROM teacher t, average_salary a
WHERE t.salary > a.avg_salary;
-- Result: Benali (75000), Haddad (85000), Rahmani (72000), Ahmed (68000)
```

### `CASE` Conditional Expression — Ch 1 Slide 49

Evaluates `WHEN` conditions top-to-bottom and returns the first match:

```sql
SELECT last_name, salary,
       CASE
           WHEN salary >= 70000 THEN 'High'
           WHEN salary >= 50000 THEN 'Medium'
           WHEN salary IS NOT NULL THEN 'Low'
           ELSE 'Not reported'
       END AS category
FROM teacher;
```

_(Notice why `WHEN salary IS NOT NULL THEN 'Low'` works safely after `>= 70000` and `>= 50000`: any `NULL` salary fails all three comparisons and falls cleanly into `ELSE 'Not reported'` for Khelifi Nora.)_

---

## 5. Worked Solutions: TD 1 (Questions 20\*–29, 31) & TP 2 Ex 12 Task 9

```sql
-- 20*. Teachers earning > overall average (using subquery)
SELECT * FROM teacher
WHERE salary > (SELECT AVG(salary) FROM teacher);

-- 21*. Teachers in departments with at least one teacher earning > 70000
SELECT * FROM teacher
WHERE department_id IN (SELECT department_id FROM teacher WHERE salary > 70000);

-- 22*. Students whose class_id belongs to department 1
SELECT * FROM student
WHERE class_id IN (SELECT class_id FROM class WHERE department_id = 1);

-- 23*. Departments for which at least one teacher exists (EXISTS)
SELECT * FROM department d
WHERE EXISTS (SELECT 1 FROM teacher t WHERE t.department_id = d.department_id);

-- 24*. Departments with no teachers (NOT EXISTS)
SELECT * FROM department d
WHERE NOT EXISTS (SELECT 1 FROM teacher t WHERE t.department_id = d.department_id);

-- 25*. Salary > at least one teacher in department 2 (ANY)
SELECT * FROM teacher
WHERE salary > ANY (SELECT salary FROM teacher WHERE department_id = 2);

-- 26*. Rewrite 25 using SOME (ANY and SOME are identical ISO SQL aliases for existential comparison)
SELECT * FROM teacher
WHERE salary > SOME (SELECT salary FROM teacher WHERE department_id = 2);

-- 27*. Salary > EVERY teacher in department 3 (ALL; include IS NOT NULL defensively)
SELECT * FROM teacher
WHERE salary > ALL (
    SELECT salary FROM teacher WHERE department_id = 3 AND salary IS NOT NULL
);

-- 28. Teachers who: (1) > overall avg, (2) belong to dept with >= 2 teachers, (3) > own dept avg
SELECT t.last_name, t.first_name, t.salary, d.department_name
FROM teacher t
JOIN department d ON t.department_id = d.department_id
WHERE t.salary > (SELECT AVG(salary) FROM teacher)
  AND t.department_id IN (
      SELECT department_id FROM teacher GROUP BY department_id HAVING COUNT(*) >= 2
  )
  AND t.salary > (
      SELECT AVG(t2.salary) FROM teacher t2 WHERE t2.department_id = t.department_id
  );

-- 29. Per department stats keeping depts with >= 2 teachers AND avg > overall university avg
SELECT d.department_name,
       COUNT(t.teacher_id) AS number_of_teachers,
       AVG(t.salary) AS average_salary,
       MAX(t.salary) AS maximum_salary
FROM department d
JOIN teacher t ON d.department_id = t.department_id
GROUP BY d.department_id, d.department_name
HAVING COUNT(t.teacher_id) >= 2
   AND AVG(t.salary) > (SELECT AVG(salary) FROM teacher);
```

### TD 1 Q31 & TP 2 Ex 12 Task 9

```sql
-- TP 2 Ex 12 (Task 9): Teachers whose non-NULL salary > average salary of their own department
-- Note: In SQL, t.salary > (...) naturally skips NULL salaries because NULL > x is UNKNOWN
SELECT t.teacher_id, t.last_name, t.first_name, t.salary, d.department_name
FROM teacher t
JOIN department d ON d.department_id = t.department_id
WHERE t.salary > (
    SELECT AVG(t2.salary)
    FROM teacher t2
    WHERE t2.department_id = t.department_id
)
ORDER BY d.department_name, t.salary DESC;

-- TD 1 Q31: Full Teacher Classification & Department Average Comparison Report
WITH dept_avg AS (
    SELECT department_id, AVG(salary) AS dept_avg_salary
    FROM teacher
    GROUP BY department_id
)
SELECT t.teacher_id,
       t.last_name,
       t.first_name,
       d.department_name,
       t.salary,
       ROUND(da.dept_avg_salary, 2) AS department_average_salary,
       CASE
           WHEN t.salary IS NULL THEN 'Not specified'
           WHEN t.salary >= 70000 THEN 'High'
           WHEN t.salary >= 50000 THEN 'Medium'
           ELSE 'Low'
       END AS salary_category,
       CASE
           WHEN t.salary IS NULL OR da.dept_avg_salary IS NULL THEN 'Not specified'
           WHEN t.salary > da.dept_avg_salary THEN 'Above Department Average'
           WHEN t.salary = da.dept_avg_salary THEN 'At Department Average'
           ELSE 'Below Department Average'
       END AS comparison_status
FROM teacher t
LEFT JOIN department d ON t.department_id = d.department_id
LEFT JOIN dept_avg da ON t.department_id = da.department_id
ORDER BY d.department_name, t.salary DESC NULLS LAST;
```

_(Note: For SQL optimization best practices—avoiding `SELECT _`, `EXISTS`/`LIMIT 1`, indexable date ranges instead of `YEAR(col)`, and `UNION ALL`—plus 30 additional Join & Division practice drills, see [[01 - Worked SQL & Relational Algebra Drills (Practice Bank)]].)\*
