# 1NF - First Normal Form

First Normal Form (1NF) is the foundational step in database normalization. A table is in 1NF if and only if every column contains atomic (indivisible) values and there are no repeating groups. Atomicity means that each cell in the table holds a single value that cannot be meaningfully broken down further within the context of that column. Repeating groups occur when multiple values are stored in a single column or when the same type of data is spread across multiple columns with repeated structure. See [[35 - Introduction to Database Normalization]] for the overview of all normal forms and [[10 - Atomic Values]] for the definition of atomicity.

## The Rules of 1NF

A table satisfies 1NF when:

1. Every column contains only atomic values (single, indivisible values)
2. Each row is unique (typically ensured by a primary key)
3. No repeating groups or arrays exist within a column
4. All entries in a column are of the same data type

## Violation Pattern 1: Multi-Part Values in a Single Column

When a column stores a value that actually contains multiple distinct pieces of information, the table violates 1NF. The most common example is an address column that combines street, city, state, and postal code into a single text field.

**Before 1NF:**

| user_id | first_name | last_name | email | address |
|---|---|---|---|---|
| 5 | Caleb | Curry | caleb@example.com | 123 Main St, Springfield, IL 62701 |

The `address` column is not atomic because it combines street, city, state, and postal code into a single value. If you need to query by state or sort by postal code, you cannot do so efficiently because those components are buried within a larger string.

**After 1NF:**

| user_id | first_name | last_name | email | street_address | city | state | postal_code |
|---|---|---|---|---|---|---|---|
| 5 | Caleb | Curry | caleb@example.com | 123 Main St | Springfield | IL | 62701 |

Each component of the address now occupies its own column, making every value atomic. Queries on city, state, or postal code are now straightforward.

## Violation Pattern 2: Multiple Values in a Single Column

When a column stores more than one value in a single cell (often separated by commas or other delimiters), the table violates 1NF. This pattern is common when a user can provide multiple email addresses or phone numbers.

**Before 1NF:**

| user_id | first_name | last_name | email |
|---|---|---|---|
| 5 | Caleb | Curry | caleb@example.com, caleb@work.com |

The `email` column contains two email addresses in one cell. This makes it impossible to enforce uniqueness on individual email addresses, difficult to query for a specific email, and error-prone when updating one of the values.

**After 1NF:**

Create a separate `email` table with a foreign key referencing the `user` table:

| user_id | first_name | last_name |
|---|---|---|
| 5 | Caleb | Curry |

| email_id | email | user_id |
|---|---|---|
| 6008 | caleb@example.com | 5 |
| 6009 | caleb@work.com | 5 |

Each email address now occupies its own row in the `email` table. The `user_id` foreign key links each email back to its owner. The `email_id` serves as the primary key of the email table, ensuring each row is unique. The repeating `user_id` value of 5 in the email table is acceptable because `user_id` is a foreign key in this table, not the primary key.

## Violation Pattern 3: Repeating Rows (Duplicate Data)

When the same entity appears in multiple rows because of a multi-valued attribute, the table violates 1NF. This creates update anomalies: if the user's name changes, every duplicate row must be updated, and missing any one of them leads to inconsistent data.

**Before 1NF:**

| user_id | first_name | last_name | email |
|---|---|---|---|
| 5 | Caleb | Curry | caleb@example.com |
| 5 | Caleb | Curry | caleb@work.com |

The same user appears twice with identical `user_id`, `first_name`, and `last_name` values. If the user changes their last name, both rows must be updated. If only one is updated, the data becomes inconsistent.

**After 1NF:**

The same solution as Pattern 2: separate the multi-valued attribute into its own table. The `user` table contains one row per user, and the `email` table contains one row per email address, linked by the `user_id` foreign key.

## Why 1NF Matters

1NF ensures that the data can be queried, updated, and constrained reliably. Non-atomic values make it difficult or impossible to write precise queries, enforce uniqueness constraints, or perform updates without risking inconsistency. By ensuring every column holds a single, indivisible value, 1NF provides the structural foundation upon which the higher normal forms build.

Without 1NF, you cannot meaningfully apply 2NF or 3NF, because those forms rely on the assumption that each column stores exactly one value that depends on the primary key in a well-defined way.

## Quick 1NF Checklist

- Does any column contain comma-separated or delimited lists? If yes, split into a separate table.
- Does any column contain a composite value (like a full address) that could be broken into components? If yes, split into individual columns.
- Does any entity appear in multiple rows due to a multi-valued attribute? If yes, extract the multi-valued attribute into its own table.
- Is every value in every column the smallest meaningful unit for that column? If not, decompose further.

Cross-reference: [[35 - Introduction to Database Normalization]], [[37 - 2NF Second Normal Form]], [[10 - Atomic Values]]
