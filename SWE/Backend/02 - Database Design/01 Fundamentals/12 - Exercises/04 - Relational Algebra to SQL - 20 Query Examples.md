# Relational Algebra to SQL — 20 Query Examples

This note maps mathematical relational algebra concepts to actual SQL code. Each of the 20 queries below includes a quiz-style question, the equivalent relational algebra expression, and the SQL implementation (including MySQL-specific variants where the standard syntax is not supported).

## The Schema (4 Tables)

To make these queries concrete, assume we are using a **University Database** with these four tables:

1. **Students** (`SID`, `Name`, `Major`, `Age`)
2. **Courses** (`CID`, `Title`, `Credits`)
3. **Enrollments** (`SID`, `CID`, `Grade`) — *Links Students and Courses*
4. **Instructors** (`IID`, `Name`, `Department`)

## Key Symbols

- $\pi$ (Pi) = **Projection** (Select specific columns).
- $\sigma$ (Sigma) = **Selection** (Filter rows / WHERE).
- $\bowtie$ (Bowtie) = **Join**.
- $\cup$ (Union), $\cap$ (Intersection), $-$ (Difference).
- $\rho$ (Rho) = **Rename**.
- $\Im$ (or $\mathcal{G}$) = **Aggregation** operator (notation varies between texts).

---

## Basic Operations

### 1. Projection (Specific Columns)

**Quiz:** List only the names and majors of all students.

- **Algebra:** $\pi_{Name, Major}(Students)$
- **SQL:**

```sql
SELECT Name, Major FROM Students;
```

### 2. Selection (Filtering Rows)

**Quiz:** List details of students who are strictly older than 21.

- **Algebra:** $\sigma_{Age > 21}(Students)$
- **SQL:**

```sql
SELECT * FROM Students WHERE Age > 21;
```

### 3. Selection + Projection

**Quiz:** Find the names of students studying 'Computer Science'.

- **Algebra:** $\pi_{Name}(\sigma_{Major='CS'}(Students))$
- **SQL:**

```sql
SELECT Name FROM Students WHERE Major = 'CS';
```

[[Qs5]] , [[Qs6]]

## Set Operations

### 4. Cartesian Product

**Quiz:** Show every possible combination of Students and Courses (regardless of whether they are enrolled).

- **Algebra:** $Students \times Courses$
- **SQL:**

```sql
SELECT * FROM Students, Courses;
-- OR --
SELECT * FROM Students CROSS JOIN Courses;
```

[[Qs7]]

### 5. Union

**Quiz:** List all unique names present in either the Student table or the Instructor table.

- **Algebra:** $\pi_{Name}(Students) \cup \pi_{Name}(Instructors)$
- **SQL:**

```sql
SELECT Name FROM Students
UNION
SELECT Name FROM Instructors;
```

[[Qs8]]

### 6. Intersection

**Quiz:** Find names that appear in both the Student list and the Instructor list (e.g., TAs or common names).

- **Algebra:** $\pi_{Name}(Students) \cap \pi_{Name}(Instructors)$
- **SQL:**

```sql
SELECT Name FROM Students
INTERSECT
SELECT Name FROM Instructors;
-- Note: MySQL uses "WHERE Name IN (...)" instead of INTERSECT
SELECT Name FROM Students WHERE Name IN (SELECT Name FROM Instructors);
```

[[Qs9]]

### 7. Set Difference

**Quiz:** Find courses that have never been enrolled in by any student.

- **Algebra:** $\pi_{CID}(Courses) - \pi_{CID}(Enrollments)$
- **SQL:**

```sql
SELECT CID FROM Courses
EXCEPT
SELECT CID FROM Enrollments;
-- OR (MySQL) --
SELECT CID FROM Courses WHERE CID NOT IN (SELECT CID FROM Enrollments);
```

[[Qs10]]

## Joins and Products

### 8. Natural Join

**Quiz:** List students and their enrollment details (matches IDs automatically).

- **Algebra:** $Students \bowtie Enrollments$
- **SQL:**

```sql
SELECT * FROM Students NATURAL JOIN Enrollments;
```

[[Qs11]]

> [!WARNING] Natural Join in Production
> Natural Join auto-matches columns by name and removes duplicates. Adding a same-named column to either table later (e.g., a `Notes` column on both) silently changes the join semantics and can break queries. Prefer explicit `JOIN ... ON ...` in production code.

### 9. Theta Join (Inner Join)

**Quiz:** List Student Names and the Course Titles they are taking.

- **Algebra:** $\pi_{Name, Title}(Students \bowtie_{Students.SID=Enrollments.SID} (Enrollments \bowtie_{Enrollments.CID=Courses.CID} Courses))$
- **SQL:**

```sql
SELECT S.Name, C.Title
FROM Students S
JOIN Enrollments E ON S.SID = E.SID
JOIN Courses C ON E.CID = C.CID;
```

### 10. Left Outer Join

**Quiz:** List all students and their grades, including students who have no grades (no enrollments).

- **Algebra:** $Students \leftouterjoin Enrollments$
- **SQL:**

```sql
SELECT Students.Name, Enrollments.Grade
FROM Students
LEFT JOIN Enrollments ON Students.SID = Enrollments.SID;
```

## Aggregation and Advanced Logic

### 11. Rename

**Quiz:** Return the list of courses but rename the column 'Title' to 'CourseName' in the result.

- **Algebra:** $\rho_{CourseName/Title}(\pi_{Title}(Courses))$
- **SQL:**

```sql
SELECT Title AS CourseName FROM Courses;
```

### 12. Aggregation (Count)

**Quiz:** Count the total number of students.

- **Algebra:** $\Im_{COUNT(SID)}(Students)$ (Note: Notation varies, sometimes $\mathcal{G}$)
- **SQL:**

```sql
SELECT COUNT(SID) FROM Students;
```

### 13. Aggregation (Average)

**Quiz:** Find the average age of all students.

- **Algebra:** $\Im_{AVG(Age)}(Students)$
- **SQL:**

```sql
SELECT AVG(Age) FROM Students;
```

### 14. Grouping

**Quiz:** Count how many students are in each Major.

- **Algebra:** $_{Major}\Im_{COUNT(SID)}(Students)$
- **SQL:**

```sql
SELECT Major, COUNT(SID)
FROM Students
GROUP BY Major;
```

### 15. Division (The "All" Query)

**Quiz:** Find students who are enrolled in **ALL** available courses.

- **Algebra:** $Students \div \pi_{CID}(Courses)$
- **SQL:** (Conceptually difficult in SQL — uses a double `NOT EXISTS`)

```sql
SELECT Name FROM Students S
WHERE NOT EXISTS (
    SELECT CID FROM Courses
    EXCEPT
    SELECT CID FROM Enrollments E WHERE E.SID = S.SID
);
```

See [[10 - The Division Operator]] for a full breakdown of the division pattern, including a `HAVING COUNT(DISTINCT ...)` alternative.

### 16. Filtering with Logic (AND)

**Quiz:** List CS students who are also enrolled in Course 'C101'.

- **Algebra:** $\pi_{Name}(\sigma_{Major='CS'}(Students) \bowtie \sigma_{CID='C101'}(Enrollments))$
- **SQL:**

```sql
SELECT S.Name
FROM Students S
JOIN Enrollments E ON S.SID = E.SID
WHERE S.Major = 'CS' AND E.CID = 'C101';
```

### 17. NULL Handling

**Quiz:** Find students who have enrolled but haven't received a grade yet (Grade is NULL).

- **Algebra:** $\sigma_{Grade=null}(Enrollments)$
- **SQL:**

```sql
SELECT * FROM Enrollments WHERE Grade IS NULL;
```

> [!WARNING] Use `IS NULL`, never `= NULL`
> The comparison `Grade = NULL` evaluates to `UNKNOWN` for every row and matches nothing. The correct test is `Grade IS NULL` (or `Grade IS NOT NULL`).

### 18. Pattern Matching

**Quiz:** Find Instructors whose names start with the letter 'J'.

- **Algebra:** $\sigma_{Name \text{ like } 'J\%'}(Instructors)$
- **SQL:**

```sql
SELECT * FROM Instructors WHERE Name LIKE 'J%';
```

### 19. Distinct (Duplicate Removal)

**Quiz:** List all unique Departments found in the Instructor table.

- **Algebra:** $\pi_{Department}(Instructors)$ (Note: Algebra implicitly removes duplicates, SQL does not).
- **SQL:**

```sql
SELECT DISTINCT Department FROM Instructors;
```

### 20. Conditional Join (Non-equi Join)

**Quiz:** List Students who are older than their Instructors (assuming we join them by matching Student Major to Instructor Dept).

- **Algebra:** $\pi_{S.Name, I.Name}(\sigma_{S.Age > I.Age} (Students \bowtie_{Major=Department} Instructors))$
- **SQL:**

```sql
SELECT S.Name, I.Name
FROM Students S
JOIN Instructors I ON S.Major = I.Department
WHERE S.Age > I.Age;
```

This is a *non-equi join* because the join condition (`S.Major = I.Department`) is equality, but the row-level filter (`S.Age > I.Age`) uses a non-equality comparison to express the actual business rule.

---

## See Also

- [[04 - SQL to Algebra Mapping Cheat Sheet]] — The reverse mapping (SQL → Algebra) with worked examples
- [[02 - Relational Algebra Operators]] — Formal definitions of σ, π, ρ, ⋈, ÷
- [[10 - The Division Operator]] — Deep dive on the division pattern used in query 15
- [[06 - Practice Exercises]] — More practice problems with full solutions
