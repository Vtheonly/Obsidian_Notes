# 3NF - Third Normal Form

Third Normal Form (3NF) addresses transitive dependencies, which occur when a non-key column depends on another non-key column rather than directly on the primary key. A transitive dependency creates a chain: column A (the primary key) determines column B, and column B determines column C. In this chain, column C transitively depends on column A through column B, rather than directly. 3NF requires that every non-key column depend on the primary key directly, with no intermediate dependencies. See [[05 - 2NF Second Normal Form]] for the prerequisite and [[01 - Introduction to Database Normalization]] for the overall normalization framework.

## The Rule of 3NF

A table is in 3NF if and only if:

1. It is already in 2NF
2. No non-key column depends on another non-key column (no transitive dependencies exist)

Equivalently, every non-key column must depend on the primary key, the whole primary key, and nothing but the primary key. This memorable formulation combines the requirements of 1NF, 2NF, and 3NF into a single statement.

## Understanding Transitive Dependencies

A **transitive dependency** occurs when:

- Column A determines column B (B depends on A)
- Column B determines column C (C depends on B)
- Therefore, column A transitively determines column C

The problem with transitive dependencies is that column C can be determined without reference to the primary key at all -- knowing column B is sufficient. This means column C is functionally dependent on the wrong column, creating redundancy and the risk of inconsistency.

Transitive dependencies can form longer chains (A determines B, B determines C, C determines D), but the principle remains the same: any non-key column that depends on another non-key column rather than directly on the primary key violates 3NF.

## Example: Product Reviews

Consider a `review` table for an e-commerce website:

**Before 3NF:**

| review_id | review_text | star_rating | star_meaning | user_id |
|---|---|---|---|---|
| 1 | Great product | 5 | Excellent | 72 |
| 2 | Average quality | 3 | Average | 84 |
| 3 | Poor experience | 1 | Terrible | 91 |
| 4 | Pretty good | 4 | Good | 72 |

The primary key is `review_id`. Now examine the dependencies:

- `review_text` depends on `review_id` (each review has unique text). Correct.
- `user_id` depends on `review_id` (each review is written by one user). Correct.
- `star_rating` depends on `review_id` (each review has one rating). Correct.
- `star_meaning` depends on `star_rating`, not on `review_id`. A rating of 5 always means "Excellent," regardless of which review it belongs to. This is a transitive dependency: `review_id` determines `star_rating`, and `star_rating` determines `star_meaning`.

The transitive dependency causes `star_meaning` to be repeated for every review with the same star rating. If the meaning of a 4-star rating changes from "Good" to "Very Good," every row with `star_rating = 4` must be updated. Missing any row creates inconsistent data.

**After 3NF:**

Remove the transitively dependent columns to their own table:

| review_id | review_text | star_rating | user_id |
|---|---|---|---|
| 1 | Great product | 5 | 72 |
| 2 | Average quality | 3 | 84 |
| 3 | Poor experience | 1 | 91 |
| 4 | Pretty good | 4 | 72 |

| star_rating | star_meaning |
|---|---|
| 1 | Terrible |
| 2 | Poor |
| 3 | Average |
| 4 | Good |
| 5 | Excellent |

The `review` table now contains only columns that depend directly on `review_id`. The `star_meaning` column has been moved to a new `star_rating` table where it depends on `star_rating` as the primary key. The `star_rating` column in the `review` table now serves as a foreign key referencing the `star_rating` table.

Note that the `star_rating` column was kept in the `review` table because it depends directly on `review_id` (each review has its own rating). Only `star_meaning` was removed, because it depended on `star_rating` rather than on `review_id`.

## How to Identify Transitive Dependencies

To check a table for 3NF compliance, follow these steps:

1. Confirm the table is in 2NF
2. For each non-key column, ask: does this column depend on the primary key directly, or does it depend on another non-key column?
3. If a non-key column depends on another non-key column, move the dependent column (along with the column it depends on) to a separate table
4. Replace the moved columns with a foreign key reference to the new table

A practical test: if changing the value of non-key column B would force a change in non-key column C, then C transitively depends on B, and the table violates 3NF.

## Example: Employee and Department

**Before 3NF:**

| employee_id | name | department_id | department_name | department_location |
|---|---|---|---|---|
| 101 | Alice | D01 | Engineering | Floor 3 |
| 102 | Bob | D02 | Marketing | Floor 5 |
| 103 | Carol | D01 | Engineering | Floor 3 |

Here, `department_name` and `department_location` depend on `department_id`, not on `employee_id`. Since `department_id` is a non-key column, this is a transitive dependency.

**After 3NF:**

| employee_id | name | department_id |
|---|---|---|
| 101 | Alice | D01 |
| 102 | Bob | D02 |
| 103 | Carol | D01 |

| department_id | department_name | department_location |
|---|---|---|
| D01 | Engineering | Floor 3 |
| D02 | Marketing | Floor 5 |

The department information has been moved to its own `department` table, and the `employee` table retains `department_id` as a foreign key.

## Summary of the Three Normal Forms

| Normal Form | Eliminates | Key Question |
|---|---|---|
| 1NF | Non-atomic values and repeating groups | Is every column value atomic? |
| 2NF | Partial dependencies | Does every non-key column depend on the whole primary key? |
| 3NF | Transitive dependencies | Does every non-key column depend only on the primary key? |

Cross-reference: [[05 - 2NF Second Normal Form]], [[01 - Introduction to Database Normalization]], [[10 - Lookup Table]]
