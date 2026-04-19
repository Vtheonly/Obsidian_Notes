# 6. Comprehensive SQL Join Cheatsheet

## Keywords & Equivalences

| Official SQL       | Short Hand   | Description                                          |
| :----------------- | :----------- | :--------------------------------------------------- |
| `INNER JOIN`       | `JOIN`       | Only matches. Rows without matches are dropped.      |
| `LEFT OUTER JOIN`  | `LEFT JOIN`  | Keeps all Left rows. Fills gaps with NULL.           |
| `RIGHT OUTER JOIN` | `RIGHT JOIN` | Keeps all Right rows. Fills gaps with NULL.          |
| `FULL OUTER JOIN`  | `FULL JOIN`  | Keeps everything. (Not in MySQL).                    |
| `CROSS JOIN`       | `,` (comma)  | Cartesian Product (Every combination).               |
| `NATURAL JOIN`     | (N/A)        | Auto-joins on same-named columns (Use with caution). |

---

## Quick Reference Scenarios

### 1. "I want only the data that connects."

- **Use:** `INNER JOIN`
- **Example:** Listing products that have been sold (connecting Product to Sales).

### 2. "I want a master list of X, with Y details if they exist."

- **Use:** `LEFT JOIN`
- **Example:** Listing all Students, and their grades (if they have any). If they have no grades, show NULL, but don't hide the student.

### 3. "I want to compare rows in the same table."

- **Use:** Self-Join (Table aliases)
- **Example:** Finding employees who earn more than their managers.

### 4. "I want to find X that have relation with ALL Y."

- **Use:** Division Logic (`NOT EXISTS` or `HAVING COUNT`)
- **Example:** Finding customers who bought every single product color available.

---

## Common Exam Syntax Errors

1.  **Ambiguous Columns:**
    - _Wrong:_ `SELECT ID FROM Student, Enrolled ...` (Which ID? Student.ID or Enrolled.ID?)
    - _Right:_ `SELECT Student.ID FROM ...`
2.  **Forgetting Join Conditions:**
    - If you write `SELECT * FROM A, B`, you get a Cartesian Product (Massive result).
    - Always ensure you have `WHERE A.id = B.id` or `ON A.id = B.id`.

3.  **Grouping in Aggregation:**
    - If using the Division method with `HAVING COUNT`, remember that every column in the `SELECT` clause (that isn't an aggregate like COUNT/SUM) must be in the `GROUP BY` clause.
