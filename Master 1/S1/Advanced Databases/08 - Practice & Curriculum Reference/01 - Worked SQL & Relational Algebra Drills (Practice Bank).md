# Worked SQL & Relational Algebra Drills (Practice Bank)

This note preserves **all 20 Relational Algebra $\leftrightarrow$ SQL Query Examples**, **the complete 40-problem SQL Join & Division Practice Bank**, **SQL Performance Anti-Patterns**, and the **Master Verification Checklist** mapping every 2026/2027 TP and TD question across this vault.

---

## 1. Relational Algebra to SQL — 20 Worked Examples

Schema: `Students(SID, Name, Major, Age)`, `Courses(CID, Title, Credits)`, `Enrollments(SID, CID, Grade)`, `Instructors(IID, Name, Department)`.

| # | Question | Relational Algebra | SQL Equivalent |
| :---: | :--- | :--- | :--- |
| **1** | Names & majors of all students | $\pi_{Name, Major}(Students)$ | `SELECT Name, Major FROM Students;` |
| **2** | Students strictly older than 21 | $\sigma_{Age > 21}(Students)$ | `SELECT * FROM Students WHERE Age > 21;` |
| **3** | Names of `'CS'` students | $\pi_{Name}(\sigma_{Major='CS'}(Students))$ | `SELECT Name FROM Students WHERE Major = 'CS';` |
| **4** | Every Student–Course combination | $Students \times Courses$ | `SELECT * FROM Students CROSS JOIN Courses;` |
| **5** | Unique names in Students or Instructors | $\pi_{Name}(Students) \cup \pi_{Name}(Instructors)$ | `SELECT Name FROM Students UNION SELECT Name FROM Instructors;` |
| **6** | Names in both Students and Instructors | $\pi_{Name}(Students) \cap \pi_{Name}(Instructors)$ | `SELECT Name FROM Students INTERSECT SELECT Name FROM Instructors;` |
| **7** | Courses with zero enrollments | $\pi_{CID}(Courses) - \pi_{CID}(Enrollments)$ | `SELECT CID FROM Courses EXCEPT SELECT CID FROM Enrollments;` *(or `NOT EXISTS`)* |
| **8** | Natural join Students & Enrollments | $Students \bowtie Enrollments$ | `SELECT * FROM Students NATURAL JOIN Enrollments;` |
| **9** | Student names & enrolled course titles | $\pi_{Name, Title}(Students \bowtie Enrollments \bowtie Courses)$ | `SELECT S.Name, C.Title FROM Students S JOIN Enrollments E ON S.SID=E.SID JOIN Courses C ON E.CID=C.CID;` |
| **10** | All students & grades (incl. unenrolled) | $Students \leftouterjoin Enrollments$ | `SELECT S.Name, E.Grade FROM Students S LEFT JOIN Enrollments E ON S.SID=E.SID;` |
| **11** | Rename `Title` to `CourseName` | $\rho_{CourseName/Title}(\pi_{Title}(Courses))$ | `SELECT Title AS CourseName FROM Courses;` |
| **12** | Total number of students | $\lambda_{COUNT(SID)}(Students)$ | `SELECT COUNT(SID) FROM Students;` |
| **13** | Average student age | $\lambda_{AVG(Age)}(Students)$ | `SELECT AVG(Age) FROM Students;` |
| **14** | Count students per major | $_{Major}\lambda_{COUNT(SID)}(Students)$ | `SELECT Major, COUNT(SID) FROM Students GROUP BY Major;` |
| **15** | Students enrolled in ALL courses | $\pi_{SID, CID}(Enrollments) \div \pi_{CID}(Courses)$ | `SELECT S.Name FROM Students S WHERE NOT EXISTS (SELECT CID FROM Courses EXCEPT SELECT CID FROM Enrollments E WHERE E.SID = S.SID);` |
| **16** | `'CS'` students enrolled in `'C101'` | $\pi_{Name}(\sigma_{Major='CS'}(Students) \bowtie \sigma_{CID='C101'}(Enrollments))$ | `SELECT S.Name FROM Students S JOIN Enrollments E ON S.SID=E.SID WHERE S.Major='CS' AND E.CID='C101';` |
| **17** | Enrollments with ungraded (`NULL`) grade | $\sigma_{Grade \text{ IS NULL}}(Enrollments)$ | `SELECT * FROM Enrollments WHERE Grade IS NULL;` *(never `= NULL`!)* |
| **18** | Instructors whose names start with `'J'` | $\sigma_{Name \text{ LIKE } 'J\%'}(Instructors)$ | `SELECT * FROM Instructors WHERE Name LIKE 'J%';` |
| **19** | Unique departments in `Instructors` | $\pi_{Department}(Instructors)$ | `SELECT DISTINCT Department FROM Instructors;` |
| **20** | Students older than instructors in their major | $\pi_{S.Name, I.Name}(\sigma_{S.Age > I.Age}(Students \bowtie_{Major=Department} Instructors))$ | `SELECT S.Name, I.Name FROM Students S JOIN Instructors I ON S.Major=I.Department WHERE S.Age > I.Age;` |

---

## 2. SQL Join & Division Practice Bank (40 Problems + Key Solutions)

Practice Schema: `Employees(EID, Name, Salary, DID)`, `Departments(DID, DName, ManagerID)`, `Projects(PID, PName, Budget)`, `WorksOn(EID, PID, Hours)`.

### Part A: 30 Join & Aggregation Drills
- **10 Easy:** (1) Employees & dept names (`INNER JOIN`); (2) Depts & manager name (`JOIN Employees ON D.ManagerID = E.EID`); (3) Projects & worker EIDs (`JOIN WorksOn`); (4) Cartesian product (`CROSS JOIN`); (5) All employees incl. unassigned (`LEFT JOIN Departments`); (6) All depts incl. empty (`RIGHT`/`LEFT JOIN`); (7) Employee pairs in same dept (`Self Join` with `E1.EID < E2.EID`); (8) Employees with `Hours > 0`; (9) Total hours per project (`GROUP BY PID`); (10) Projects with no workers (`LEFT JOIN WorksOn ... WHERE W.EID IS NULL`).
- **15 Medium:** (11) 3-table join `Employees -> WorksOn -> Projects`; (12) Total salary per dept; (13) Avg hours per employee; (14) Workers on `'Project X'`; (15) Depts with `> 5` employees (`HAVING COUNT(*) > 5`); (16) Project with `MAX(Budget)`; (17) Employees not on any project (`NOT EXISTS`); (18) Manager of `'Sales'`; (19) Total salary cost of `'IT'`; (20) Workers on projects with `Budget > 100000`; (21) Workers with `Hours > 10` on a single project; (22) Depts where `AVG(Salary) > 50000`; (23) Project with most assigned employees; (24) Employees sharing same name as their manager; (25) Highest-paid employee in `'HR'`.
- **5 Hard (Worked SQL):**
```sql
-- 26. Better Than Own Dept Average
SELECT E.Name, E.Salary, E.DID
FROM Employees E
WHERE E.Salary > (SELECT AVG(E2.Salary) FROM Employees E2 WHERE E2.DID = E.DID);

-- 27. Second Highest Salary
SELECT MAX(Salary) AS second_highest FROM Employees
WHERE Salary < (SELECT MAX(Salary) FROM Employees);

-- 28. Exclusive Worker (works on ONLY one project)
SELECT E.EID, E.Name FROM Employees E JOIN WorksOn W ON E.EID = W.EID
GROUP BY E.EID, E.Name HAVING COUNT(DISTINCT W.PID) = 1;

-- 29. Budget Buster (SUM(Hours * 100) > Budget)
SELECT P.PID, P.PName FROM Projects P JOIN WorksOn W ON P.PID = W.PID
GROUP BY P.PID, P.PName, P.Budget HAVING SUM(W.Hours * 100) > P.Budget;

-- 30. Manager's Burden (manages a dept, assigned to NO project)
SELECT E.EID, E.Name FROM Employees E
JOIN Departments D ON E.EID = D.ManagerID
WHERE NOT EXISTS (SELECT 1 FROM WorksOn W WHERE W.EID = E.EID);
```

### Part B: 10 Relational Division Drills
- **4 Easy:** (1) Employees on ALL projects; (2) Students in ALL `'CS'` courses; (3) Customers who bought ALL `'Electronics'` products; (4) Players who played in ALL stadiums.
- **4 Difficult:** (5) Employees on every project `'John Doe'` works on (replace inner `Projects` with `WorksOn` filtered to `'John Doe'`); (6) Depts where ALL employees earn `> 50000` (`NOT EXISTS (SELECT 1 FROM Employees E WHERE E.DID = D.DID AND (E.Salary <= 50000 OR E.Salary IS NULL))`); (7) Projects worked on by ALL `'IT'` employees; (8) Students who took all `'Math'` major courses.
- **2 Hard SQL Implementations:**
```sql
-- 9. Employees on ALL Projects (EXCEPT form)
SELECT E.Name FROM Employees E
WHERE NOT EXISTS (
    SELECT P.PID FROM Projects P
    EXCEPT
    SELECT W.PID FROM WorksOn W WHERE W.EID = E.EID
);

-- 10. Students taking ALL CS courses (Double NOT EXISTS form)
SELECT S.Name FROM Student S
WHERE NOT EXISTS (
    SELECT C.CID FROM Course C WHERE C.Dept = 'CS'
    AND NOT EXISTS (
        SELECT 1 FROM Enrollment E WHERE E.SID = S.SID AND E.CID = C.CID
    )
);
```

---

## 3. SQL Optimization Best Practices (4 Core Rules)

1. **Avoid `SELECT *`:** Transfers wasted network bytes and prevents **Index-Only Scans**; specify needed columns explicitly.
2. **Use `EXISTS` or `LIMIT 1` for existence checks:** `SELECT 1 FROM Users WHERE ID = 5 LIMIT 1;` stops on the very first match instead of scanning/counting everything via `COUNT(*)`.
3. **Never wrap indexed columns in functions:** `WHERE YEAR(OrderDate) = 2023` disables the B-tree index; rewrite as `WHERE OrderDate BETWEEN '2023-01-01' AND '2023-12-31'`.
4. **Use `UNION ALL` instead of `UNION` when duplicates are impossible or unwanted:** Skips the expensive sort/hash deduplication step.

---

## 4. Master 2026/2027 Curriculum Verification Map

Every exercise across all six 2026/2027 PDFs is integrated into the corresponding note:
- **TP 1 (Parts A–S):** [[01 - The University Database Setup, Constraints & DML]] + [[02 - Querying, Filtering, Aggregation & Joins]] (Part L, N) + [[03 - Keys, Data Types & Static Constraints (PostgreSQL)]] (Part F, H) + [[04 - Relationships & ER Modeling]] (Part E).
- **TD 1 (`1*`–`31`):** `1*–19*, 30` $\to$ [[02 - Querying, Filtering, Aggregation & Joins]]; `20*–29, 31` $\to$ [[03 - Set Operations, Subqueries, CTEs & CASE Expressions]].
- **TP 2 (Ex 1–12 & Part IV) & TD 2 (Ex 1*–18*):**
  - Views & Materialized Views (TP 2 Ex 1–3, Ex 12.4, Part IV Q10–11; TD 2 Ex 1*–2*) $\to$ [[01 - Standard Views, Updatability & Materialized Views]].
  - Procedural Blocks, Loops, Exceptions (TP 2 Ex 4–7, Part IV Q12–14; TD 2 Ex 3*–4, 6–8) $\to$ [[02 - Procedural SQL (SQL-PSM & PL-pgSQL), Control Flow & Exceptions]].
  - Functions & Procedures (TP 2 Ex 8–9, Ex 12.5–7, Part IV Q12, Q18–19; TD 2 Ex 9*–15) $\to$ [[03 - Stored Functions, Stored Procedures & Dynamic SQL]].
  - Audit Triggers & Constraints vs Triggers (TP 2 Ex 10, Ex 12.8, Part IV Q15–16; TD 2 Ex 16*–18*) $\to$ [[01 - Triggers, Automatic Auditing & Constraints vs Triggers]].
  - Recursive Queries (TP 2 Ex 11, Part IV Q17; TD 2 Ex 5) $\to$ [[05 - Recursive Queries (WITH RECURSIVE)]].
- **TP 3 (Ex 1–16) & TD 3 (Ex 1*–9):**
  - Cursors (TP 3 Ex 1–7, 15; TD 3 Ex 1*–6) $\to$ [[04 - Cursors & Row-by-Row Processing]].
  - Recursive Queries (TP 3 Ex 8–14, 16; TD 3 Ex 7*–9) $\to$ [[05 - Recursive Queries (WITH RECURSIVE)]].
- **Archival Exam & TD Practice:** Past `Exams/` (2008–2025) and `Quiz/` remain in their folders for extra drill (keeping in mind that older exams use MySQL/Oracle syntax).
