---
sources:
  - "[[01 - Database Concepts, Relational Model & SQL Overview]]"
  - "[[02 - Relational Algebra & Formal Foundations]]"
  - "[[03 - Keys, Data Types & Static Constraints (PostgreSQL)]]"
---
> [!question] Suppose a table stores `'123 Epic Lane, Legit, CA 73821'` inside one `address` cell. Why does writing a SQL query to find everyone living in `'CA'` become messy and unreliable?
> a) SQL refuses to search inside any column that contains numbers and letters together.
> b) Multiple separate pieces of information are crammed into one cell, so SQL cannot filter cleanly by state alone.
> c) Storing commas inside text automatically turns the cell into a list of numbers.
> d) SQL cannot run `WHERE` filters on columns longer than 20 characters.
>> [!success]- Answer
>> b) Multiple separate pieces of information are crammed into one cell, so SQL cannot filter cleanly by state alone.

> [!question] Storing a comma-separated list like `'The Matrix, Inception, Interstellar'` inside a single `favorite_movies` cell makes it easy for SQL to prevent duplicate movies and delete just one movie cleanly.
>> [!success]- Answer
>> False

> [!question] If your queries always read and compare a calendar date as one complete value, storing `'2026-11-12'` in a single `DATE` column is better than splitting it into separate `year`, `month`, and `day` columns.
>> [!success]- Answer
>> True

> [!question] Match each data storage situation to the best table design choice.
>> [!example] Group A
>> a) Storing `'Caleb Daniel Curry'` in one `full_name` cell when you need to sort by last name
>> b) Storing `'The Matrix, Inception'` in a single `favorite_movies` cell
>> c) Storing `'2026-11-12'` when queries always use the complete date together
>
>> [!example] Group B
>> n) Extract the items into a separate child table so each movie gets its own row.
>> o) Keep it in a single `DATE` column to avoid unnecessary over-splitting.
>> p) Split it into separate `first_name`, `middle_name`, and `last_name` columns.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] A team upgrades a database table by splitting `full_name` into `first_name` and `last_name` columns, which would break older application queries still asking for `full_name`. How does SQL keep the old queries working without storing duplicate name data?
> a) By disabling all constraints on the table so SQL ignores missing column names.
> b) By storing a second hidden table that copies every row automatically on read.
> c) By creating a `VIEW` (a saved virtual query) that combines `first_name` and `last_name` into `full_name` on the fly.
> d) By inserting `full_name` back into every row separated by commas.
>> [!success]- Answer
>> c) By creating a `VIEW` (a saved virtual query) that combines `first_name` and `last_name` into `full_name` on the fly.

> [!question] A standard SQL `VIEW` stores a separate physical copy of the query's result rows on disk alongside the base table.
>> [!success]- Answer
>> False

> [!question] In SQL, inserting a new student row (`INSERT`) modifies the table's structural blueprint, whereas adding a new column (`ALTER TABLE`) only manipulates row data.
>> [!success]- Answer
>> False

> [!question] During a bank transfer, SQL subtracts $100 from Account A, and the server crashes right before adding $100 to Account B. When both steps are wrapped inside a transaction, what should the database do?
> a) Undo (`ROLLBACK`) the subtraction from Account A so either both updates succeed or neither takes effect.
> b) Keep Account A reduced by $100 and wait for the user to manually re-enter the transfer.
> c) Automatically guess Account B's final balance without recording the error.
> d) Drop the accounts table to prevent other users from seeing partial data.
>> [!success]- Answer
>> a) Undo (`ROLLBACK`) the subtraction from Account A so either both updates succeed or neither takes effect.

> [!question] Match each group of SQL commands to the database job it performs.
>> [!example] Group A
>> a) `CREATE`, `ALTER`, `DROP` (DDL)
>> b) `SELECT` (DQL)
>> c) `GRANT`, `REVOKE` (DCL)
>
>> [!example] Group B
>> n) Controls which database users have permission to view or modify objects.
>> o) Defines, alters, or removes the structural blueprint of tables and rules.
>> p) Retrieves, filters, and analyzes stored rows without altering the data.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match each SQL action to what it actually cancels, revokes, or removes.
>> [!example] Group A
>> a) `ROLLBACK`
>> b) `REVOKE`
>> c) `DELETE`
>
>> [!example] Group B
>> n) Cancels unfinished changes inside an active transaction.
>> o) Removes specific rows from inside a table.
>> p) Takes away a user's access privilege on a table or view.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Database design progresses through three layers: mapping business ideas, choosing exact tables and columns, and configuring server-specific features like B-tree indexes, partitioning, and backups. Which layer handles those PostgreSQL indexes and backups?
> a) Conceptual schema
> b) Logical schema
> c) Relational view layer
> d) Physical schema
>> [!success]- Answer
>> d) Physical schema

> [!question] Relational databases guard data accuracy with three core integrity pillars. Match each pillar to the real-world bug it stops.
>> [!example] Group A
>> a) Entity Integrity
>> b) Referential Integrity
>> c) Domain Integrity
>
>> [!example] Group B
>> n) Stops a child row from pointing to a parent ID that does not exist.
>> o) Rejects invalid entries like `'abc'` in a numeric column or negative values when forbidden.
>> p) Ensures two people who share the exact same name still have unique, non-null row identifiers.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] If five teachers all belong to department `1`, running `SELECT department_id FROM teacher;` in SQL keeps all five `1`s in the result instead of collapsing them to one row.
>> [!success]- Answer
>> True

> [!question] Formal relational theory treats every table as a mathematical set with no duplicate rows, whereas SQL allows duplicate values in query output by default. Which SQL query removes duplicate `department_id` values so each appears only once?
> a) `SELECT department_id FROM teacher;`
> b) `SELECT DISTINCT department_id FROM teacher;`
> c) `SELECT UNIQUE_ROWS department_id FROM teacher;`
> d) `SELECT SET(department_id) FROM teacher;`
>> [!success]- Answer
>> b) `SELECT DISTINCT department_id FROM teacher;`

> [!question] In SQL, the rows returned by a `SELECT` query have no guaranteed order unless an `ORDER BY` clause is explicitly included.
>> [!success]- Answer
>> True

> [!question] Suppose Query 1 returns `{10, 20}` and Query 2 returns `{20, 30}`. If you combine them using `UNION` instead of `UNION ALL`, how many rows does SQL return?
> a) 4 rows (`10, 20, 20, 30`) because `UNION` keeps every row from both queries.
> b) 1 row (`20`) because `UNION` keeps only rows found in both queries.
> c) 3 rows (`10, 20, 30`) because `UNION` removes duplicates while `UNION ALL` keeps them.
> d) 2 rows (`10, 30`) because `UNION` deletes any matching values.
>> [!success]- Answer
>> c) 3 rows (`10, 20, 30`) because `UNION` removes duplicates while `UNION ALL` keeps them.

> [!question] A student runs `SELECT first_name, salary FROM teacher UNION SELECT department_name FROM department;` and PostgreSQL rejects it immediately. Why?
> a) The two queries return different numbers of columns, violating union compatibility.
> b) `UNION` can only combine columns from the exact same table.
> c) `UNION` only works on numeric columns and never on text columns.
> d) `UNION` requires both tables to contain the same total number of rows.
>> [!success]- Answer
>> a) The two queries return different numbers of columns, violating union compatibility.

> [!question] Given Query A returning `{1, 2, 3}` and Query B returning `{3, 4}`, match each SQL set operator (written as `A <operator> B`) to its exact result.
>> [!example] Group A
>> a) `UNION`
>> b) `INTERSECT`
>> c) `EXCEPT`
>
>> [!example] Group B
>> n) `{1, 2}`
>> o) `{1, 2, 3, 4}`
>> p) `{3}`
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] In SQL `LIKE` pattern matching, `_` matches exactly one single character while `%` matches zero or more characters. Which name matches `WHERE name LIKE 'T_____'` (a `'T'` followed by five underscores)?
> a) `'Tom'`
> b) `'Thomas'`
> c) `'Tariq'`
> d) `'Timothy'`
>> [!success]- Answer
>> b) `'Thomas'`

> [!question] Match each SQL text pattern filter to what it actually matches.
>> [!example] Group A
>> a) `WHERE name LIKE '_a%'`
>> b) `WHERE name LIKE 'T%'`
>> c) `WHERE name ILIKE 'ahmed'` (PostgreSQL)
>
>> [!example] Group B
>> n) Matches `'Ahmed'`, `'AHMED'`, or `'ahmed'` by ignoring uppercase vs. lowercase.
>> o) Matches any name starting with `'T'` of any length, including `'T'` alone.
>> p) Matches any name whose second letter is `'a'`, regardless of total length.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] In SQL, storing `NULL` in a `salary` column is treated the exact same way as storing `0`, and storing `NULL` in a text column is identical to storing an empty string `''`.
>> [!success]- Answer
>> False

> [!question] A student wants to list every pupil with a missing `class_id` (`NULL`) and runs `SELECT * FROM student WHERE class_id = NULL;`. Even though such students exist, the query returns zero rows. Why?
> a) Because `=` only works on text columns and not on integer columns.
> b) Because comparing `NULL` with `=` automatically deletes matching rows from the result.
> c) Because PostgreSQL converts `= NULL` into `= 0` behind the scenes.
> d) Because `NULL` represents an unknown value, so nothing ever equals `NULL` with `=`; you must use `IS NULL`.
>> [!success]- Answer
>> d) Because `NULL` represents an unknown value, so nothing ever equals `NULL` with `=`; you must use `IS NULL`.

> [!question] Because binary floating-point types like `REAL` cannot represent decimals such as `0.1` without small rounding errors, `NUMERIC(p, s)` (or `DECIMAL(p, s)`) should be used for salaries and currency.
>> [!success]- Answer
>> True

> [!question] Match each PostgreSQL column data type to the exam-safe reason for choosing it.
>> [!example] Group A
>> a) `NUMERIC(10, 2)`
>> b) `SMALLINT`
>> c) `CHAR(2)`
>
>> [!example] Group B
>> n) Compact 2-byte whole number (`-32,768` to `32,767`), suited for small values like `age`.
>> o) Fixed-length 2-character code (space-padded if shorter), suited for country codes like `'DZ'`.
>> p) Exact base-10 decimal, mandatory for salaries and currency to prevent rounding bugs.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] A table defines `age SMALLINT`, which holds whole numbers from `-32,768` to `32,767`. What happens in PostgreSQL if someone tries to insert `40000` into `age`?
> a) PostgreSQL automatically widens the column to `INTEGER` during the insert.
> b) PostgreSQL silently caps the stored value at `32,767`.
> c) PostgreSQL rejects the insert with an out-of-range error because `40000` exceeds `32,767`.
> d) PostgreSQL replaces `40000` with `NULL` and inserts the row anyway.
>> [!success]- Answer
>> c) PostgreSQL rejects the insert with an out-of-range error because `40000` exceeds `32,767`.

> [!question] If an `email` column has a `UNIQUE` constraint without `NOT NULL`, PostgreSQL allows two different rows in the same table to both store `NULL` in that column.
>> [!success]- Answer
>> True

> [!question] If a column is declared as `salary NUMERIC(10, 2) CHECK (salary >= 0)` without `NOT NULL`, attempting to insert a row with `salary = NULL` will be rejected by the `CHECK` constraint.
>> [!success]- Answer
>> False

> [!question] In SQL's three-valued logic (`TRUE`, `FALSE`, `UNKNOWN`), a `CHECK` constraint rejects a row ONLY when its condition is `FALSE`. Match each case involving `salary = NULL` to its exact result.
>> [!example] Group A
>> a) Evaluating `NULL >= 0`
>> b) Evaluating `NULL IS NULL`
>> c) Inserting `salary = NULL` into `CHECK (salary >= 0)`
>
>> [!example] Group B
>> n) Succeeds and accepts the row, because `UNKNOWN` is not `FALSE`.
>> o) Evaluates to `UNKNOWN`.
>> p) Evaluates to `TRUE`.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Suppose a column is defined as `salary NUMERIC(10, 2) DEFAULT 30000`. Match each `INSERT` situation to what PostgreSQL actually does.
>> [!example] Group A
>> a) Omitting `salary` completely from the `INSERT` column list
>> b) Explicitly passing `NULL` for `salary` when `NOT NULL` is not present
>> c) Explicitly passing `NULL` for `salary` when `NOT NULL` is also enforced
>
>> [!example] Group B
>> n) Rejects the `INSERT`, because `NOT NULL` forbids storing `NULL`.
>> o) Stores `NULL`, because an explicit `NULL` overrides `DEFAULT`.
>> p) Stores `30000` by falling back to the `DEFAULT` value.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Exams often compare PostgreSQL syntax against MySQL or standard SQL. Match each PostgreSQL feature to what it represents.
>> [!example] Group A
>> a) `GENERATED ALWAYS AS IDENTITY`
>> b) `BYTEA`
>> c) `::NUMERIC`
>
>> [!example] Group B
>> n) Explicit type conversion (cast) syntax in PostgreSQL.
>> o) Raw binary data type for files/images in PostgreSQL (instead of MySQL's `BLOB`).
>> p) Auto-incrementing identifier syntax in PostgreSQL (instead of MySQL's `AUTO_INCREMENT`).
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)