# 1. Set Operations vs Joins

This note details the fundamental differences between combining data vertically (Sets) and horizontally (Joins), a common source of confusion in SQL.

## 1. The Core Concept: Vertical vs. Horizontal

When you have data in two tables, there are two primary ways to combine them.

### A. The Intersection (Set Operation)

Think of this as **Vertical Stacking**. You are looking for rows that exist in _both_ piles.

- **Direction:** Vertical.
- **Goal:** Find common shared values (e.g., "Which IDs are on list A AND list B?").
- **Constraint:** The columns must match exactly in number and data type.

### B. The Inner Join (Relational Operation)

Think of this as **Horizontal Stitching**. You are linking a row from Table A to a row in Table B based on a key.

- **Direction:** Horizontal.
- **Goal:** Extend the information (e.g., "Get the Student Name from Table A and their Department Name from Table B").
- **Constraint:** You can select any columns you want from either table.

```mermaid
flowchart TD
    subgraph SET_OP [Set Operation: INTERSECT]
    A1[Table A Col1] --- match((Match?))
    B1[Table B Col1] --- match
    match --> Result1[Result List]
    end

    subgraph JOIN_OP [Relational: INNER JOIN]
    RowA[Row Table A] -- Key -- RowB[Row Table B]
    RowA --> Result2[Combined Row: A + B]
    RowB --> Result2
    end
```

---

## 2. When are they the SAME?

They appear to be the same only in one specific scenario: **Filtering for existence.**

If you only want to know **"Which IDs exist in both tables?"** and you do not need any other columns, both methods produce the same list of IDs.

**The Scenario:**

- `Table_A`: Has `ID` [1, 2, 3]
- `Table_B`: Has `ID` [2, 3, 4]

**Option 1: INTERSECT**

```sql
SELECT ID FROM Table_A
INTERSECT
SELECT ID FROM Table_B;
-- Result: 2, 3
```

**Option 2: INNER JOIN**

```sql
SELECT DISTINCT A.ID
FROM Table_A AS A
INNER JOIN Table_B AS B ON A.ID = B.ID;
-- Result: 2, 3
```

> [!INFO] Note on DISTINCT
> We must add `DISTINCT` to the JOIN to make it mimic `INTERSECT`. Without it, duplicates might appear (see section 3).

---

## 3. When are they NOT the same? (The 3 Differences)

In professional environments and interviews, distinguishing these is critical.

### Difference 1: Handling Duplicates

- **INTERSECT (Mathematical Set):** Removes duplicates by default. If ID `101` is in Table A 5 times and Table B 5 times, `INTERSECT` returns `101` **once**.
- **INNER JOIN (Multiplication):** Multiplies duplicates. If ID `101` is in Table A 5 times and Table B 5 times, the Join creates $5 \times 5 = 25$ rows.

### Difference 2: Handling NULL Values

This is the biggest "Gotcha."

- **INTERSECT:** Treats `NULL` as a valid value. If both tables have a `NULL`, it considers them a match.
- **INNER JOIN:** Drops `NULL` values. In SQL, `NULL = NULL` is "Unknown/False". The join condition fails, and the row is lost.

> [!WARNING] Important
> If your data contains NULLs and you want to find them, `INNER JOIN` will silently hide them from you.

### Difference 3: Flexibility (Columns)

- **INTERSECT:** Rigid. You cannot grab `Table_A.Name` and `Table_B.Department` simultaneously because the schemas of the two queries must be identical.
- **INNER JOIN:** Flexible. You can mix and match columns from both tables in the `SELECT` clause.

---

## 4. How to Simulate Set Operations in MySQL

MySQL does not natively support `INTERSECT` or `EXCEPT` (Set Difference). You must use workarounds.

### Simulating INTERSECT

Use the `IN` clause.
_Logic:_ "Give me names from Students where the Name is found INSIDE the list of Instructor names."

```sql
SELECT Name FROM Students
WHERE Name IN (SELECT Name FROM Instructors);
```

### Simulating EXCEPT (Set Difference)

_Scenario:_ Find Courses (Table A) that are NOT in Enrollments (Table B).
Use `NOT IN` or `NOT EXISTS`.

```sql
SELECT CID FROM Courses
WHERE CID NOT IN (SELECT CID FROM Enrollments);
```

> [!TIP] Pro Tip: Retrieving Details
> If you perform a set difference (finding IDs in A but not B) and you want the **full details** of those items, the `NOT IN` approach is perfect because you are already selecting from the main table.
>
> ```sql
> SELECT * FROM Courses -- You get all columns here
> WHERE CID NOT IN (SELECT CID FROM Enrollments);
> ```

---

## 5. Union vs. Distinct

A `UNION` combines results from two queries.

- **UNION:** Automatically performs a `DISTINCT`. It removes duplicates.
- **UNION ALL:** Keeps everything, including duplicates (Much faster because it doesn't sort/check).

**Comparison:**

- `SELECT DISTINCT` applies to a single query's output.
- `UNION` applies to the combination of two queries' outputs.
