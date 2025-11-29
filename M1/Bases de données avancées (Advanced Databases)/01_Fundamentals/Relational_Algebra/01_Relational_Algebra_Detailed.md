
# Fundamental Relational Algebra Operators

## Overview
Relational Algebra defines the theoretical operations that database systems use to manipulate data. Understanding these is crucial for **TD 2** and **TD 4 (Optimization)**.

> [!NOTE] Relation vs. Table
> In Algebra, we speak of **Relations** (sets of tuples). In SQL, we speak of **Tables** (bags of rows). Algebra strictly removes duplicates; SQL does not unless `DISTINCT` is used.

---

## 1. Unary Operators (Single Table)

These operators act on one relation at a time to filter data horizontally (Selection) or vertically (Projection).

| Operator | Symbol | Description | Schema Change? | SQL Equivalent |
| :--- | :---: | :--- | :--- | :--- |
| **Selection** | $\sigma_{condition}(R)$ | Filters **rows** based on a specific condition (predicate). <br> *Keeps all columns, reduces rows.* | No | `WHERE` clause |
| **Projection** | $\pi_{col1, col2}(R)$ | Filters **columns**. Keeps only specific attributes. <br> *Removes duplicates in pure algebra.* | **Yes** (Fewer columns) | `SELECT col1, col2` |
| **Rename** | $\rho_{NewName}(R)$ | Renames the relation or attributes. Essential for Self-Joins. | No | `AS NewName` |

### Detailed Examples

#### Selection ($\sigma$)
**Goal:** Get details of students aged > 20.
*   **Algebra:** $\sigma_{Age > 20}(Student)$
*   **SQL:** `SELECT * FROM Student WHERE Age > 20;`

#### Projection ($\pi$)
**Goal:** Get only the names of the students.
*   **Algebra:** $\pi_{Name}(Student)$
*   **SQL:** `SELECT DISTINCT Name FROM Student;`
    *   *Note:* We add `DISTINCT` because mathematical projection removes duplicates.

---

## 2. Set Operators (Binary)

These operators combine two relations ($R$ and $S$).
> [!WARNING] Union Compatibility Rule
> To use **Union**, **Intersection**, or **Difference**, relations $R$ and $S$ must be **Union-Compatible**:
> 1. They must have the **same number of attributes**.
> 2. The attributes must have compatible **domains** (types).

| Operator | Symbol | Description | SQL Equivalent |
| :--- | :---: | :--- | :--- |
| **Union** | $R \cup S$ | Combines tuples from both tables. Removes duplicates. | `UNION` |
| **Intersection** | $R \cap S$ | Returns tuples found in **BOTH** tables. | `INTERSECT` (or `INNER JOIN`) |
| **Difference** | $R - S$ | Returns tuples in $R$ that are **NOT** in $S$. | `EXCEPT` (or `NOT IN`) |
| **Cartesian Product** | $R \times S$ | Combines **every** row of $R$ with **every** row of $S$. <br> *Size = $N_R \times N_S$* | `CROSS JOIN` or `FROM R, S` |

### Visual Logic

```mermaid
graph TD
    subgraph Union [R ∪ S]
    A1[Data R] --- B1[Data S]
    end
    
    subgraph Intersection [R ∩ S]
    A2[Data R] -- Only Matching -- B2[Data S]
    end
    
    subgraph Difference [R - S]
    A3[Data R] -- Remove Matches --x B3[Data S]
    end
```

### Practical Example (TD2 Context)
**Scenario:** You have `CS_Students` and `Math_Students`.

1.  **Union:** List all students from both departments.
    *   $\pi_{Name}(CS\_Students) \cup \pi_{Name}(Math\_Students)$
    *   `SELECT Name FROM CS_Students UNION SELECT Name FROM Math_Students;`

2.  **Difference:** List CS students who are **NOT** studying Math.
    *   $\pi_{Name}(CS\_Students) - \pi_{Name}(Math\_Students)$
    *   `SELECT Name FROM CS_Students WHERE Name NOT IN (SELECT Name FROM Math_Students);`
