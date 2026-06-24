# Introduction to SQL

## What is SQL

SQL stands for Structured Query Language. It is the standard programming language used to communicate with relational database management systems. SQL serves as the intermediary between human instructions and database operations, allowing users to define database structures, insert and modify data, retrieve information, and control access permissions. The language is designed to be readable and close to natural language, making it more accessible than many other programming languages.

It is important to understand that SQL is not specific to any single RDBMS. It is a general standard recognized by all major relational database systems, including MySQL, PostgreSQL, Oracle Database, and SQL Server. While each platform may have minor variations in syntax or proprietary extensions, the core SQL commands and concepts remain consistent across all of them. Learning standard SQL provides a foundation that transfers to any RDBMS you encounter.

SQL is a declarative language, which means you specify what you want the database to do rather than how to do it. When you write a SQL query, you describe the result you want, and the RDBMS determines the most efficient way to retrieve or modify the data. This is fundamentally different from procedural programming languages, where you specify each step the computer must execute.

## DDL: Data Definition Language

Data Definition Language (DDL) is the subset of SQL used to define and manage the structure of the database. DDL commands create, modify, and remove database objects such as tables, indexes, and views. They do not manipulate the data within those structures; instead, they define the schema that the data conforms to. DDL is concerned with the blueprint of the database, specifying what tables exist, what columns they contain, what data types those columns accept, and what constraints govern them.

The primary DDL commands are `CREATE`, `ALTER`, and `DROP`. The `CREATE` statement defines new database objects. The `ALTER` statement modifies the structure of existing objects. The `DROP` statement removes objects entirely from the database. These commands give you full control over the structural definition of your database.

### CREATE

The `CREATE` statement is used to create new database objects, most commonly tables. When you create a table, you define its name, its columns, the data type for each column, and any constraints that apply.

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100),
    email VARCHAR(100)
);
```

This statement creates a `users` table with four columns. The `id` column is defined as an integer and designated as the primary key, which means it must be unique for every row and cannot be null. The other columns are defined as variable-length character strings with maximum lengths specified.

### ALTER

The `ALTER` statement modifies the structure of an existing table. You can use it to add new columns, remove existing columns, or change the data type of a column.

```sql
ALTER TABLE users ADD phone_number VARCHAR(15);
```

This statement adds a new column called `phone_number` to the `users` table. The existing data in the table is not affected; the new column simply receives null values for all existing rows.

### DROP

The `DROP` statement removes a database object entirely. When you drop a table, all data within that table is permanently deleted along with the table structure.

```sql
DROP TABLE users;
```

This statement deletes the entire `users` table and all of its data. Use `DROP` with extreme caution, as the operation is irreversible in most RDBMS platforms.

## DML: Data Manipulation Language

Data Manipulation Language (DML) is the subset of SQL used to work with the data within the database structures defined by DDL. DML commands insert new data, update existing data, delete data, and retrieve data from tables. While DDL defines the containers, DML fills and manages the contents of those containers.

The primary DML commands are `SELECT`, `INSERT`, `UPDATE`, and `DELETE`. These four commands cover the basic CRUD operations (Create, Read, Update, Delete) that form the backbone of most database interactions.

### SELECT

The `SELECT` statement retrieves data from one or more tables. It is the most commonly used SQL command and supports extensive filtering, sorting, and aggregation options.

```sql
SELECT username, email FROM users;
```

This statement returns the `username` and `email` columns for every row in the `users` table. The `SELECT` statement can also include `WHERE` clauses for filtering, `ORDER BY` clauses for sorting, and `JOIN` clauses for combining data from multiple tables.

```sql
SELECT username, email FROM users WHERE id = 72;
```

This variation returns only the row where the `id` equals 72, demonstrating how `SELECT` can be used to retrieve specific records.

### INSERT

The `INSERT` statement adds new rows to a table. You specify the table, the columns you are providing values for, and the values themselves.

```sql
INSERT INTO users (id, username, password, email)
VALUES (72, 'caleb_curry', 'pi123', 'coolguy@hotmail.com');
```

This statement inserts a new row into the `users` table with the specified values. The column names and values must match in number and order.

### UPDATE

The `UPDATE` statement modifies existing data in a table. You specify which table to update, which columns to change, and the new values. A `WHERE` clause determines which rows are affected.

```sql
UPDATE users SET password = 'newpassword456' WHERE id = 72;
```

This statement changes the `password` value for the row where `id` equals 72. Without a `WHERE` clause, `UPDATE` would modify every row in the table, which is almost never the intended behavior.

### DELETE

The `DELETE` statement removes rows from a table. Like `UPDATE`, it uses a `WHERE` clause to determine which rows to remove.

```sql
DELETE FROM users WHERE id = 72;
```

This statement deletes the row where `id` equals 72. Without a `WHERE` clause, `DELETE` removes every row in the table.

## SQL Keywords

SQL keywords are reserved words that the RDBMS recognizes as commands or clauses. Words like `SELECT`, `INSERT`, `CREATE`, `WHERE`, `FROM`, and `TABLE` are keywords with predefined meanings in the SQL language. Because these words are reserved, you should avoid using them as names for tables, columns, or other database objects. Naming a column `select` or `table` can cause syntax errors or unexpected behavior.

A common convention is to write SQL keywords in uppercase letters (e.g., `SELECT`, `INSERT`) and user-defined names in lowercase (e.g., `users`, `phone_number`). This convention makes SQL code easier to read by visually distinguishing between language commands and database object names.

## Joins

A join is a SQL operation that combines data from two or more tables based on a related column between them. Joins are essential in relational databases because data is intentionally distributed across multiple tables to reduce redundancy and maintain integrity. When you need information that spans multiple tables, a join brings that data together in a single result set.

For example, if a `sales` table contains a `user_id` column that references the `id` column in a `users` table, you can join these tables to produce a result that includes both the sale details and the user's name:

```sql
SELECT users.name, sales.item
FROM sales
JOIN users ON sales.user_id = users.id;
```

This query returns a result set showing the name of each user alongside the items they purchased. Joins can be further classified into inner joins, outer joins, and cross joins, each with different rules about which rows are included in the result.

## Summary of SQL Categories

| Category | Purpose | Key Commands |
|----------|---------|-------------|
| DDL | Define database structure | CREATE, ALTER, DROP |
| DML | Manipulate data within structures | SELECT, INSERT, UPDATE, DELETE |

## Next Steps

With an understanding of how SQL is used to define and manipulate database structures, the next topic addresses how to name database objects consistently and clearly. See [[5 - Naming Conventions]] for best practices.
