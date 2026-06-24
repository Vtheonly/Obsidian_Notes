# Data Integrity

## What is Data Integrity

Data integrity refers to the accuracy, consistency, and reliability of data stored in a database. A database with integrity contains data that is correct, up to date, and free from contradictions. When data integrity is compromised, the database may contain duplicate records, outdated information, broken relationships between tables, or values that violate business rules. These problems are collectively known as anomalies, and preventing them is one of the primary goals of database design.

Data integrity is not a single property but a combination of several distinct types, each addressing a different aspect of data correctness. The three main types are entity integrity, referential integrity, and domain integrity. Together, they form a comprehensive framework for ensuring that the data in a database remains trustworthy and usable over time. Understanding each type is essential for designing databases that resist errors and maintain their quality as data is inserted, updated, and deleted.

## Entity Integrity

Entity integrity ensures that each row in a table represents a unique, distinct entity and that no two rows are identical. This is typically enforced through a primary key, which is a column or combination of columns whose value uniquely identifies each row. The primary key must be unique and must not contain null values, guaranteeing that every row can be individually referenced and distinguished from all other rows.

Without entity integrity, a table may contain duplicate or ambiguous rows, making it impossible to determine whether two identical rows represent the same entity or two different entities that happen to share the same attributes. Consider a `users` table that stores only `name` and `phone_number` without a primary key. If two people named Caleb live in the same household and share the same phone number, the table would contain two identical rows with no way to distinguish them. Adding an `id` column as a primary key resolves this ambiguity by assigning a unique identifier to each person.

| id | name | phone_number |
|----|------|-------------|
| 6 | Caleb | 800-555-0100 |
| 7 | Caleb | 800-555-0100 |

With the `id` column, it is clear that these are two separate entities despite sharing the same name and phone number. Entity integrity also ensures that each table in the database appears only once; there should not be two separate `users` tables storing the same type of data. All user information belongs in a single, consolidated `users` table.

## Referential Integrity

Referential integrity ensures that relationships between tables remain valid and consistent. When one table references a row in another table through a foreign key, the referenced row must actually exist. If the relationship is broken, the database contains a reference to data that is no longer present, which leads to orphaned records and inconsistent query results.

Consider a `comments` table that includes a `user_id` column referencing the `id` column in the `users` table. Every comment must be associated with a user who posted it. If a user with `id = 7` is deleted from the `users` table, but the corresponding rows in the `comments` table still reference `user_id = 7`, the database now contains comments attributed to a nonexistent user. This breaks referential integrity.

Foreign key constraints are the mechanism by which referential integrity is enforced at the database level. A foreign key constraint can be configured with different actions when the referenced row is deleted or updated. The most common options are:

- **CASCADE**: When a parent row is deleted, all referencing child rows are automatically deleted as well. If user 7 is deleted, all comments by user 7 are also deleted.
- **RESTRICT / NO ACTION**: Prevents the deletion of a parent row if child rows still reference it. User 7 cannot be deleted until all associated comments are removed first.
- **SET NULL**: When a parent row is deleted, the foreign key column in the child rows is set to null. The comments remain, but their `user_id` becomes null.

The choice of which action to use depends on the business requirements. For a social media platform, cascading deletions might be appropriate so that deleting a user also removes their comments. For a financial system, restricting deletions might be necessary to preserve an audit trail.

## Domain Integrity

Domain integrity ensures that every value stored in a column conforms to a defined set of acceptable values, known as the domain. The domain specifies the data type, length, format, range, and any additional constraints that values in that column must satisfy. Domain integrity prevents invalid, out-of-range, or incorrectly formatted data from being stored in the database.

For example, a `phone_number` column should contain a 10-digit numeric value, not a text string like "call me." A `birth_date` column should contain a valid calendar date, not a string like "sometime in the 90s." An `age` column should contain a positive integer, not a negative number or a decimal. Each of these constraints defines the domain of acceptable values for the column.

Domain integrity is enforced through data types and constraints. A data type such as `INTEGER` ensures that only whole numbers are stored. A `VARCHAR(20)` ensures that text values do not exceed 20 characters. Additional constraints such as `CHECK`, `NOT NULL`, and `UNIQUE` further refine the domain. For instance, a `CHECK` constraint can enforce that an `age` column only accepts values between 0 and 150, or that a `status` column only accepts the values 'active', 'inactive', or 'pending'.

| Column | Data Type | Domain Constraint |
|--------|-----------|-----------------|
| phone_number | VARCHAR(15) | Must be numeric, 10 digits |
| email | VARCHAR(100) | Must contain '@' character |
| age | INTEGER | Must be between 0 and 150 |
| status | VARCHAR(20) | Must be 'active', 'inactive', or 'pending' |

## How Foreign Key Constraints Enforce Integrity

Foreign key constraints are the primary mechanism for enforcing referential integrity in a relational database. A foreign key is a column (or set of columns) in one table that references the primary key of another table. The foreign key establishes a link between the two tables and ensures that the relationship remains valid.

When a foreign key constraint is defined, the RDBMS automatically checks that any value inserted into the foreign key column matches an existing value in the referenced primary key column. If you attempt to insert a comment with `user_id = 999` and there is no user with `id = 999`, the RDBMS rejects the insertion. This prevents orphaned records from ever entering the database.

Similarly, foreign key constraints govern what happens when a referenced row is deleted or updated. The constraint actions (CASCADE, RESTRICT, SET NULL) determine whether dependent rows are deleted, whether the operation is blocked, or whether the foreign key value is set to null. These options give database designers fine-grained control over how relationships are maintained when data changes.

## Data Types and Constraints

Data types and constraints work together to enforce both domain integrity and entity integrity. Every column in a table must have a defined data type, which specifies the kind of data it can hold. Common data types include:

- **INTEGER**: Whole numbers
- **VARCHAR(n)**: Variable-length text up to `n` characters
- **DATE**: Calendar dates
- **BOOLEAN**: True or false values
- **DECIMAL(p, s)**: Precise decimal numbers with `p` total digits and `s` decimal places

Constraints add additional rules on top of data types. The most important constraints are:

- **PRIMARY KEY**: Ensures uniqueness and non-null values for the column(s)
- **NOT NULL**: Prevents null values from being stored in the column
- **UNIQUE**: Ensures all values in the column are distinct
- **CHECK**: Validates that values meet a specified condition
- **FOREIGN KEY**: Ensures referential integrity with another table

By combining appropriate data types with well-chosen constraints, you can build a database that rejects invalid data at the point of entry, long before it causes problems in downstream reports or applications.

## Summary of Integrity Types

| Integrity Type | Concern | Enforcement Mechanism |
|---------------|---------|----------------------|
| Entity | Unique, identifiable rows | Primary key |
| Referential | Valid relationships between tables | Foreign key constraints |
| Domain | Acceptable values per column | Data types, CHECK, NOT NULL, UNIQUE |

## Next Steps

Understanding data integrity provides the foundation for the terminology used throughout database design. See [[09 - Database Terms]] and [[10 - More Database Terms]] for comprehensive glossaries of the essential vocabulary.
