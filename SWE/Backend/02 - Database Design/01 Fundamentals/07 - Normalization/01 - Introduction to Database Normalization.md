# Introduction to Database Normalization

Database normalization is a systematic process for refining a database schema to eliminate redundancy, prevent data anomalies, and ensure that each piece of data is stored in exactly the right place. The process follows a sequence of normal forms, each building upon the previous one, that serve as a checklist for evaluating and improving your table designs. Normalization does not dictate what data to store -- it dictates how to structure the tables so the data is stored correctly.

## Why Normalization Matters

Without normalization, a database is prone to three categories of data anomalies:

- **Insertion anomaly**: You cannot insert a new piece of data without also inserting unrelated data. For example, if employee details and department details are stored in the same table, you cannot add a new department until at least one employee is assigned to it.
- **Update anomaly**: Updating a single piece of data requires modifying multiple rows. If a department name appears in every employee row for that department, changing the department name means updating every affected employee row. If any row is missed, the data becomes inconsistent.
- **Deletion anomaly**: Deleting one piece of data unintentionally removes other unrelated data. If you delete the last employee in a department, you also lose the department's information entirely.

Normalization eliminates these anomalies by ensuring that each fact is stored in exactly one place, that each table represents a single subject, and that every non-key column depends directly and fully on the primary key.

## The Normal Forms

The three most commonly used normal forms form a progressive sequence. Each form adds a constraint on top of the previous one:

| Normal Form | Focus | Rule |
|---|---|---|
| **1NF** (First Normal Form) | Atomicity | Every column contains atomic (indivisible) values; no repeating groups |
| **2NF** (Second Normal Form) | Partial dependencies | Every non-key column depends on the entire primary key, not just part of it |
| **3NF** (Third Normal Form) | Transitive dependencies | No non-key column depends on another non-key column |

Additional normal forms exist (BCNF, 4NF, 5NF, 6NF, DKNF), but for the vast majority of practical applications, achieving 3NF is sufficient. The higher normal forms address edge cases that rarely arise in typical business database design.

## The Progressive Nature of Normal Forms

Normal forms are cumulative: a table must satisfy 1NF before it can be evaluated for 2NF, and it must satisfy 2NF before it can be evaluated for 3NF. You cannot skip steps. If a table is in 3NF, it is guaranteed to also be in 2NF and 1NF. This progressive structure means you can address one class of problem at a time, building toward a fully normalized design methodically.

```
Unnormalized data
       |
       v
   1NF: Ensure atomicity
       |
       v
   2NF: Remove partial dependencies
       |
       v
   3NF: Remove transitive dependencies
```

## The Concept of Dependency

Normalization is fundamentally about understanding and managing dependencies between columns. A **dependency** exists when the value of one column determines the value of another. In a properly normalized table, every non-key column depends on the primary key and only on the primary key. When non-key columns depend on each other or on only part of a composite key, the table contains redundancy that normalization addresses.

For example, in an `employee` table with `employee_id` as the primary key, the `employee_name` column depends on `employee_id` -- if you change the employee ID, you are referring to a different person. This is a correct dependency. But if the table also includes `department_name` and `department_location`, then `department_location` depends on `department_name` rather than directly on `employee_id`, creating a transitive dependency that 3NF would address.

## Normalization in the Design Workflow

Normalization is typically applied during the logical design phase, after entities and relationships have been identified in the ER diagram but before the physical schema is implemented. The workflow proceeds as follows:

1. Identify entities and relationships (ER modeling)
2. Define initial table structures with columns and keys
3. Apply 1NF: ensure all values are atomic
4. Apply 2NF: remove partial dependencies
5. Apply 3NF: remove transitive dependencies
6. Consider denormalization for performance (if necessary)

Denormalization is sometimes applied after normalization when read performance demands it, but this is a deliberate trade-off that should be made only after the schema is fully normalized and performance testing reveals specific bottlenecks.

Cross-reference: [[04 - 1NF First Normal Form]], [[05 - 2NF Second Normal Form]], [[06 - 3NF Third Normal Form]], [[11 - Atomic Values]]
