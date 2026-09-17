# 5. The Division Operator ($\div$)

## Overview

The **Division** operator is often considered the most difficult concept in Relational Algebra. It is used to answer queries involving universal quantifiers like **"ALL"** or **"EVERY"**.

> [!TIP] How to Spot a Division Problem
> Look for these keywords in the requirement:
>
> - "Find students who took **all** courses."
> - "Find pilots who can fly **every** plane model."
> - "Find clients who bought **every** product in the catalog."

---

## Mathematical Definition

Given two relations $R(A, B)$ and $S(B)$, the division $R \div S$ returns the values of $A$ from $R$ that are associated with **every** value of $B$ in $S$.

### The Derivation Formula

Since standard SQL does not have a `DIVIDE BY` command, we must derive it using basic operators. The logic relies on a **Double Negative**.

**Concept:**
To find people who did everything, we find the people who **did not miss anything**.

**Formula:**
$$ R \div S = \pi_A(R) - \pi_A( (\pi_A(R) \times S) - R ) $$

**Step-by-Step Breakdown:**

1.  **$\pi_A(R)$**: Get a list of all candidates (All Students).
2.  **$\pi_A(R) \times S$**: Create a "Perfect World" where every student has taken every course (Cartesian Product).
3.  **$R$**: The "Real World" (what students actually took).
4.  **$(\dots) - R$**: (Perfect World) - (Real World) = **The Missing Rows** (What they failed to take).
5.  **Total - Missed**: (All Students) - (Students with at least one missing course) = **Students who took everything**.

---

## SQL Implementation 1: The Double NOT EXISTS

This is the literal translation of "Find students where there is **no** course that they have **not** taken."

**Scenario:** Find students who enrolled in **all** 'Core' courses.

```sql
SELECT S.Name
FROM Student S
WHERE NOT EXISTS (              -- Negative 1: There is no...
    SELECT C.CourseID
    FROM Courses C
    WHERE C.Type = 'Core'
    AND NOT EXISTS (            -- Negative 2: ...course NOT taken
        SELECT *
        FROM Enrolled E
        WHERE E.StudentID = S.StudentID
        AND E.CourseID = C.CourseID
    )
);
```

**Reading the logic:**
"Select a student `S`. Check the list of Core courses. If you find a Core course `C` where there is NO record in `Enrolled` for this student and this course, then reject the student. If no such 'missing link' exists, keep the student."

---

## SQL Implementation 2: Aggregation (Easier)

For exams, if not restricted to `NOT EXISTS`, the aggregation method is often safer and easier to write.

**Logic:**
Count the total number of distinct Core courses. Then, count how many Core courses each student has taken. If the numbers match, they took them all.

```sql
SELECT StudentID
FROM Enrolled
WHERE CourseID IN (SELECT CourseID FROM Courses WHERE Type = 'Core')
GROUP BY StudentID
HAVING COUNT(DISTINCT CourseID) = (SELECT COUNT(*) FROM Courses WHERE Type = 'Core');
```

---

## Visual Example

**Table R (Who has what)**
| User | Item |
| :--- | :--- |
| A | 1 |
| A | 2 |
| B | 1 |
| C | 1 |
| C | 2 |

**Table S (The Required Set)**
| Item |
| :--- |
| 1 |
| 2 |

**Operation: $R \div S$**

- **User A:** Has 1 and 2. (Complete Match) $\to$ **Keep**
- **User B:** Has 1. Missing 2. $\to$ Drop
- **User C:** Has 1 and 2. (Complete Match) $\to$ **Keep**

**Result:** A, C
