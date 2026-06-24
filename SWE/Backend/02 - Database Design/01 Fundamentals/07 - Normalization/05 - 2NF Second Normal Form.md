# 2NF - Second Normal Form

Second Normal Form (2NF) addresses partial dependencies, which occur when a non-key column depends on only part of a composite primary key rather than on the entire key. A table can only violate 2NF if it has a composite primary key (a primary key consisting of two or more columns). Tables with a simple (single-column) primary key are automatically in 2NF, because a column cannot depend on "part" of a single column. See [[04 - 1NF First Normal Form]] for the prerequisite and [[06 - 3NF Third Normal Form]] for the next step.

## The Rule of 2NF

A table is in 2NF if and only if:

1. It is already in 1NF
2. Every non-key column depends on the entire primary key, not just a portion of it

A **partial dependency** exists when a non-key column is functionally dependent on only a subset of the columns that make up the composite primary key. When this occurs, the partially dependent column should be moved to a separate table where it depends on a complete primary key.

## Understanding Dependencies

A **functional dependency** exists when the value of one column (or set of columns) uniquely determines the value of another column. In a properly normalized table, every non-key column should depend on the full primary key. If `column B` depends on `column A`, then knowing the value of `A` determines the value of `B`. For example, `employee_name` depends on `employee_id` because a given employee ID corresponds to exactly one employee name.

A dependency is **partial** when the dependent column relies on only a subset of a composite primary key. For example, in a table with the composite key `(author_id, book_id)`, if the column `book_title` depends only on `book_id` and not on `author_id`, that is a partial dependency.

## Example: Books and Authors

Consider a many-to-many relationship between books and authors, implemented with an intermediary table. A poorly designed intermediary table might look like this:

**Before 2NF:**

| author_id | book_id | author_position | isbn | book_title |
|---|---|---|---|---|
| 22 | 17 | 1 | 978-0-13-110362-7 | The C Programming Language |
| 22 | 38 | 2 | 978-0-201-53082-4 | Structure and Interpretation |
| 45 | 17 | 2 | 978-0-13-110362-7 | The C Programming Language |

The composite primary key is `(author_id, book_id)`. Now examine the dependencies:

- `author_position` depends on both `author_id` and `book_id` (an author's position varies by book). This is a correct full dependency.
- `isbn` depends only on `book_id`. The ISBN is a property of the book, not of the author-book combination. This is a partial dependency.
- `book_title` depends only on `book_id`. The title is a property of the book. This is also a partial dependency.

The partial dependencies on `book_id` mean that `isbn` and `book_title` are repeated for every author of the same book. If the book title needs to be corrected, every row for that book must be updated, creating an update anomaly.

**After 2NF:**

Remove the partially dependent columns to their own table:

| author_id | book_id | author_position |
|---|---|---|
| 22 | 17 | 1 |
| 22 | 38 | 2 |
| 45 | 17 | 2 |

| book_id | isbn | book_title |
|---|---|---|
| 17 | 978-0-13-110362-7 | The C Programming Language |
| 38 | 978-0-201-53082-4 | Structure and Interpretation |

The `book_author` intermediary table now contains only columns that depend on the full composite key `(author_id, book_id)`. The `isbn` and `book_title` columns have been moved to the `book` table, where they depend on `book_id` as a complete primary key.

## When 2NF Does Not Apply

If a table has a simple (single-column) primary key, it is automatically in 2NF because there is no "part" of the primary key for a column to partially depend on. A column either depends on the single primary key column or it does not. There is no intermediate case.

For example, a `users` table with `user_id` as the sole primary key column cannot violate 2NF. Every column in the table either depends on `user_id` or is misplaced in the table entirely. You can proceed directly to evaluating the table for 3NF.

## How to Identify Partial Dependencies

To check a table for 2NF compliance, follow these steps:

1. Identify the primary key (is it composite?)
2. For each non-key column, ask: does this column depend on the entire primary key, or only on a subset?
3. If any column depends on only a subset, move that column (along with the columns it depends on) to a separate table
4. Replace the moved columns with a foreign key reference if necessary

## Summary of 1NF to 2NF Transformation

| Step | Action |
|---|---|
| 1 | Confirm the table is in 1NF |
| 2 | Identify the composite primary key columns |
| 3 | For each non-key column, determine which subset of the key it depends on |
| 4 | Move partially dependent columns to a new table keyed by the subset they depend on |
| 5 | Retain a foreign key in the original table if needed |

Cross-reference: [[04 - 1NF First Normal Form]], [[06 - 3NF Third Normal Form]], [[01 - Introduction to Database Normalization]], [[07 - Designing Many-to-Many Relationships]]
