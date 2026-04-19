# Normalization and Functional Dependencies

The relational model relies on proper schema design to prevent data anomalies. When a table is designed poorly, it suffers from redundancy, which leads to anomalies when performing DML operations. 

## 1. Data Anomalies
If a database is not normalized, three types of anomalies might occur:
*   **Insertion Anomaly:** Inability to add a valid piece of information to the database unless another related piece of information is also added. *(e.g., You cannot add a new course until a student enrolls in it).*
*   **Deletion Anomaly:** Deleting a record unintentionally deletes other, unrelated data. *(e.g., Deleting the last student in a course also deletes the existence of the course from the DB).*
*   **Update Anomaly:** Updating a single logical fact requires updating multiple rows. If one row misses the update, the database becomes inconsistent. *(e.g., Changing a Professor's office number requires updating 50 student enrollment rows).*

## 2. Functional Dependencies (FD)
A **Functional Dependency** describes the relationship between attributes. 
We denote an FD as $X \rightarrow Y$ (read as "X determines Y").
*   **Definition:** If two tuples (rows) have the same value for $X$, they **must** have the same value for $Y$. 
*   **Example:** `SSN -> Name`. If two rows have the same SSN, they must refer to the same Name.

### Armstrong's Axioms
These are the formal rules used to infer new FDs from existing ones:
1.  **Reflexivity:** If $Y$ is a subset of $X$, then $X \rightarrow Y$. *(Trivial FD)*
2.  **Augmentation:** If $X \rightarrow Y$, then $XZ \rightarrow YZ$. 
3.  **Transitivity:** If $X \rightarrow Y$ and $Y \rightarrow Z$, then $X \rightarrow Z$.

*Derived rules:*
*   **Union:** If $X \rightarrow Y$ and $X \rightarrow Z$, then $X \rightarrow YZ$.
*   **Decomposition:** If $X \rightarrow YZ$, then $X \rightarrow Y$ and $X \rightarrow Z$.

## 3. The Normal Forms (NF)
Normalization is the step-by-step process of decomposing a large table into smaller, less redundant tables without losing information ("lossless decomposition").

### First Normal Form (1NF)
*   **Rule:** Every attribute must be **atomic** (indivisible) and single-valued.
*   **Violation:** A `Phone_Numbers` column containing "555-1234, 555-9876".
*   **Fix:** Create a separate row or table for each phone number.

### Second Normal Form (2NF)
*   **Rule:** Must be in 1NF **AND** contain no **partial dependencies**.
*   **Partial Dependency:** When an attribute depends on only a *part* of a composite Primary Key.
*   **Example:** PK is `{StudentID, CourseID}`. The attribute `CourseName` depends only on `CourseID`, not on `StudentID`. This violates 2NF.
*   **Fix:** Decompose into a `Course` table and an `Enrollment` table.

### Third Normal Form (3NF)
*   **Rule:** Must be in 2NF **AND** contain no **transitive dependencies**.
*   **Transitive Dependency:** When a non-key attribute depends on another non-key attribute. ($PK \rightarrow A \rightarrow B$).
*   **Example:** PK is `EmployeeID`. Attribute `DepartmentCode` specifies the department, and `DepartmentName` depends on `DepartmentCode`. (`EmployeeID -> DepartmentCode -> DepartmentName`). This violates 3NF.
*   **Fix:** Move the transitively dependent column to a new `Department` table.

### Boyce-Codd Normal Form (BCNF)
BCNF is a stricter version of 3NF. 
*   **Rule:** Must be in 3NF **AND** for every non-trivial functional dependency $X \rightarrow Y$, $X$ must be a **Superkey**.
*   **When does 3NF fail but BCNF applies?** This only happens if a table has overlapping candidate keys. Generally, if $A \rightarrow B$ determines a part of the Primary Key from a non-key attribute, it violates BCNF.

> [!TIP] The Quick Rule of Thumb for 3NF
> Every non-key attribute must provide a fact about **the key**, **the whole key**, and **nothing but the key**, so help me Codd.
