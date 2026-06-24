# 3. SQL Syntax Rules and Best Practices

This note covers specific keywords, punctuation rules, and aliasing standards.

## 1. Quotation Marks in MySQL

Standard SQL is strict, but MySQL is forgiving. This often leads to bad habits.

| Type             |  Symbol   | Standard SQL Use               | MySQL Behavior                       |
| :--------------- | :-------: | :----------------------------- | :----------------------------------- |
| **Single Quote** |   `' '`   | **String Literals** (Data)     | Used for Data (Correct)              |
| **Double Quote** |   `" "`   | **Identifiers** (Column Names) | Allows for Data (Incorrect practice) |
| **Backticks**    | `` ` ` `` | N/A                            | **Identifiers** (Table/Col names)    |

**The Rule:**
Always use **Single Quotes** for values: `WHERE Major = 'CS'`.
Only use Backticks or Double Quotes if your table name has a space (e.g., `"Order Table"`), which you should avoid anyway.

---

## 2. Aliasing (`AS`) and Qualifiers

When should you rename tables (`Students AS S`)?

### A. Simple Queries

- `SELECT Name FROM Students WHERE Major = 'CS';`
- **Verdict:** Aliasing is optional. It works fine without it.

### B. Joins (Recommended)

- `SELECT S.Name, D.Name FROM Students S JOIN Departments D...`
- **Verdict:** Highly recommended. It makes typing faster and code clearer.

### C. Self Joins (Mandatory)

- If you join a table to itself (e.g., Employees managing Employees), you **must** use aliases to distinguish the two instances.
  ```sql
  SELECT E.Name, M.Name
  FROM Employee E
  JOIN Employee M ON E.ManagerID = M.ID;
  ```

### D. Ambiguity (Mandatory)

- If both tables have a column named `ID`, `SELECT ID...` will crash. You **must** specify `S.ID`.

---

## 3. The `CHECK` Constraint

Used to enforce domain integrity (limiting valid values) at the table level.

**Scenarios:**

1.  **Age Restriction:** `CHECK (Age >= 18)`
2.  **Valid Options:** `CHECK (Grade IN ('A', 'B', 'C', 'F'))`
3.  **Complex Logic:** `CHECK (Credit > 0 AND Title != '')`

**Implementation:**

```sql
/* During Creation */
CREATE TABLE Student (
    ID int PRIMARY KEY,
    Age int CHECK (Age >= 18)
);

/* After Creation */
ALTER TABLE Student
ADD CONSTRAINT CheckAge CHECK (Age >= 18);
```
