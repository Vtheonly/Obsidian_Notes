# 6. Practice Exercises

This note contains structured problems to test your SQL knowledge, ranging from basic joins to complex "Division" queries.

## The Practice Schema

Assume 4 Tables:

1.  **Employees** (`EID`, `Name`, `Salary`, `DID` (Dept ID))
2.  **Departments** (`DID`, `DName`, `ManagerID`)
3.  **Projects** (`PID`, `PName`, `Budget`)
4.  **WorksOn** (`EID`, `PID`, `Hours`) - _The Join Table_

---

## Part A: Joins (10 Easy, 15 Medium, 5 Hard)

### 10 Easy Problems (Basic Mechanics)

1.  List all Employees and their Department Names. (Inner Join)
2.  List all Departments and the name of their Manager. (Inner Join on `ManagerID`)
3.  List all Projects and the EIDs of people working on them. (Inner Join)
4.  Show every Employee and every Project (Cartesian Product).
5.  List all Employees, including those not assigned to a Department. (Left Join)
6.  List all Departments, including those with no employees. (Right/Left Join)
7.  Find pairs of Employees who work in the same Department. (Self Join)
8.  List Employees who have worked more than 0 hours on any project.
9.  Find the total hours worked per project. (Join + Group By)
10. List Projects that have no one working on them. (Left Join + NULL check)

### 15 Medium Problems (Filtering & Aggregation)

11. List Employee Names and Project Names they work on. (3-Table Join: Emp -> WorksOn -> Proj)
12. Find the total salary of each Department.
13. Find the average hours worked per Employee.
14. List Employees who work on 'Project X'.
15. Find Departments that have more than 5 Employees.
16. List the Project with the highest budget.
17. Find Employees who do _not_ work on any project. (Subquery or Left Join)
18. Find the name of the Manager of the 'Sales' department.
19. Calculate the total cost (Salary) of the 'IT' department.
20. List names of Employees who work on projects with a budget > 100k.
21. Find Employees who work more than 10 hours on a single project.
22. List Departments where the average salary is > 50k.
23. Find the Project name with the most employees assigned.
24. List Employees who have the same name as their Manager.
25. Find the Employee with the highest salary in the 'HR' department.

### 5 Hard Problems (Complex Logic)

26. **The "Better Than Average":** List Employees who earn more than the average salary of their _own_ department.
    - _Hint:_ Join Employee with a subquery of Avg salaries grouped by DID.
27. **The "Second Highest":** Find the second highest salary in the company.
28. **The "Exclusive Worker":** Find Employees who work on _only_ one project.
29. **The "Budget Buster":** List Projects where the sum of hours \* 100 (assume hourly rate) exceeds the Project Budget.
30. **The "Manager's Burden":** List Managers who manage a department but are not assigned to work on any project themselves.

---

## Part B: Division Problems (The "ALL" Query)

**Concept:** Division is used when you want to find entities that relate to **every** member of a set.

- _Key Phrase:_ "Find students who took **ALL** Biology courses."

### 4 Easy (Concept Checks)

1.  Find Employees who work on **ALL** projects listed in the Projects table.
2.  Find Students who have taken **ALL** courses offered by the 'CS' department.
3.  Find Customers who have bought **ALL** products in the 'Electronics' category.
4.  Find Players who have played in **ALL** stadiums.

### 4 Difficult (Logic Construction)

5.  Find Employees who work on every project that 'John Doe' works on. (Subset division).
6.  Find Departments where **ALL** employees earn > 50k.
7.  Find Projects that are worked on by **ALL** employees of the 'IT' department.
8.  Find Students who have taken every course required for the 'Math' major.

### 2 Hard (SQL Implementation)

**9. The SQL Code for "Employees on ALL Projects":**

```sql
SELECT Name FROM Employees E
WHERE NOT EXISTS (
    SELECT PID FROM Projects
    EXCEPT
    SELECT PID FROM WorksOn W WHERE W.EID = E.EID
);
```

- _Translation:_ "Find Employees where there is NO project that they have NOT worked on."

**10. The "Double Negative" Logic:**
Find Students who took all CS courses.

```sql
SELECT S.Name FROM Student S
WHERE NOT EXISTS (
    SELECT C.CID FROM Course C WHERE C.Dept = 'CS'
    AND NOT EXISTS (
        SELECT * FROM Enrollment E
        WHERE E.SID = S.SID AND E.CID = C.CID
    )
);
```

---

## Part C: Optimization and Best Practices

### What to Do vs. What Not to Do

**1. SELECT \***

- **BAD:** `SELECT * FROM BigTable;`
  - _Why:_ Transfers unnecessary data, slows down network, prevents Index-Only scans.
- **GOOD:** `SELECT ID, Name FROM BigTable;`
  - _Why:_ Only fetches what is needed.

**2. EXISTENCE CHECKS**

- **BAD:** `SELECT COUNT(*) FROM Users WHERE ID = 5;` (Then checking if result > 0 in code)
  - _Why:_ The DB counts everything.
- **GOOD:** `SELECT 1 FROM Users WHERE ID = 5 LIMIT 1;` (Or usage of `EXISTS`)
  - _Why:_ The DB stops searching after finding the first match.

**3. INDEXING on Functions**

- **BAD:** `WHERE YEAR(OrderDate) = 2023;`
  - _Why:_ Applying a function (`YEAR()`) to a column usually disables the index. The DB must scan every row.
- **GOOD:** `WHERE OrderDate BETWEEN '2023-01-01' AND '2023-12-31';`
  - _Why:_ Uses the standard index on the Date column.

**4. UNION vs UNION ALL**

- **BAD:** `SELECT ... UNION SELECT ...` (When you know there are no duplicates).
  - _Why:_ The DB wastes time trying to find and remove duplicates.
- **GOOD:** `SELECT ... UNION ALL SELECT ...`
  - _Why:_ Simply appends the data. Much faster.
