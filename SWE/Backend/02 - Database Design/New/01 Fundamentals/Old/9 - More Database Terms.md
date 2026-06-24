# More Database Terms

## Overview

This glossary continues the vocabulary established in [[8 - Database Terms]], covering terms related to SQL, application architecture, and data presentation. Understanding these terms is essential for working with databases in real-world application contexts, where the database interacts with frontend interfaces, server-side code, and multiple user roles.

## SQL-Related Terms

### SQL

SQL stands for Structured Query Language. It is the standard programming language used to communicate with relational database management systems. SQL enables users to define database structures (through Data Definition Language), manipulate data within those structures (through Data Manipulation Language), and control access permissions. SQL is a declarative language: you specify what results you want, and the RDBMS determines how to produce them. Although SQL syntax varies slightly between RDBMS platforms, the core commands and concepts are consistent across all of them. See [[4 - Introduction to SQL]] for a detailed explanation.

### DDL: Data Definition Language

Data Definition Language (DDL) is the subset of SQL used to define and manage the structure of database objects. DDL commands create, alter, and remove tables, indexes, views, and other structural elements. The key DDL commands are `CREATE` (to define new objects), `ALTER` (to modify existing objects), and `DROP` (to remove objects entirely). DDL operates on the schema, not on the data within the schema. For example, `CREATE TABLE users (...)` defines a new table structure, but does not populate it with any data.

### DML: Data Manipulation Language

Data Manipulation Language (DML) is the subset of SQL used to work with the data stored within database structures. DML commands insert new rows, update existing values, delete rows, and retrieve data. The key DML commands are `INSERT` (to add new rows), `UPDATE` (to modify existing values), `DELETE` (to remove rows), and `SELECT` (to retrieve data). DML operates on the contents of tables, not on their structure. For example, `INSERT INTO users (...) VALUES (...)` adds data to an existing table without changing the table's definition.

### Keywords

SQL keywords are reserved words that have predefined meanings in the SQL language. Words such as `SELECT`, `FROM`, `WHERE`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `TABLE`, and `JOIN` are keywords that the RDBMS interprets as commands or clauses. Because these words are reserved, they should not be used as names for user-defined database objects such as tables or columns. Using a keyword as an identifier can cause syntax errors, confusion, or unexpected behavior. A common convention is to write SQL keywords in uppercase to visually distinguish them from user-defined names.

## Application Architecture Terms

### Front-End

The front-end is the part of an application that the user directly interacts with. In a web application, the front-end consists of the HTML, CSS, and JavaScript that render the user interface in a browser. The front-end is designed to be intuitive and user-friendly, presenting data in a readable format and accepting user input through forms, buttons, and other interface elements. Users of the front-end do not need to know SQL, understand database structure, or have direct access to the database server.

The front-end communicates with the database indirectly through the back-end. When a user submits a registration form, the front-end sends the data to the back-end, which validates it and stores it in the database. When a user views their profile, the front-end requests the data from the back-end, which retrieves it from the database and returns it in a presentable format. This separation ensures that users never interact with the database directly, which is both a usability and a security measure.

### Back-End

The back-end is the part of an application that runs behind the scenes, handling data processing, business logic, and database communication. The back-end includes the server, the server-side programming language (such as PHP, Python, or Node.js), and the database itself. When the front-end sends a request, the back-end processes it, interacts with the database as needed, and returns the result to the front-end.

The back-end is responsible for translating user actions into database operations. It validates input, enforces business rules, constructs SQL queries, manages database connections, and handles errors. The back-end also implements security measures such as input sanitization to prevent SQL injection attacks, access control to ensure users can only modify their own data, and error handling that presents generic messages to users rather than exposing internal database details.

### Client

A client is any device or application that requests data or services from a server. In a typical web application, the client is the user's web browser running on their computer or mobile device. The client sends requests to the server, receives responses, and presents the data to the user through the front-end interface. Multiple clients can connect to the same server simultaneously, each making independent requests.

The client does not have direct access to the database. Instead, it communicates with the server, which acts as an intermediary. This architecture centralizes data management on the server while distributing the presentation layer across many client devices. The client-server model is the foundation of most modern web applications and network services.

### Server

A server is a computer or software system that provides data or services to clients. In the context of a database application, the server hosts the database and the server-side application code. It receives requests from clients, processes them, interacts with the database, and returns the results. The server is responsible for data storage, query execution, security enforcement, and concurrent access management.

The server-side is where the database and the business logic reside. When a client requests data, the server determines whether the request is authorized, constructs the appropriate query, executes it against the database, and returns the result. This centralized architecture ensures that data integrity is maintained, security policies are consistently enforced, and all clients access the same authoritative data source.

## Data Presentation Terms

### View

A view is a virtual table that presents a customized subset or transformation of the data stored in the underlying base tables. Views do not store data themselves; they are saved queries that the RDBMS executes on demand. When you query a view, the RDBMS retrieves the current data from the base tables and presents it according to the view definition.

Views serve several important purposes. They provide data security by restricting what columns and rows are visible to different users. They simplify complex queries by encapsulating joins and filters into a reusable object. They provide a consistent interface to the data, even when the underlying table structure changes. For example, if a `users` table is restructured to split a `full_name` column into `first_name` and `last_name`, a view can concatenate these columns back into `full_name`, preserving compatibility with existing applications.

Views can also implement row-level security. A regular user accessing a website might interact with a view that returns only their own record, while an administrator accesses a view that includes all records. This fine-grained access control is a powerful security mechanism that prevents users from seeing or modifying data they are not authorized to access.

### Join

A join is a SQL operation that combines rows from two or more tables based on a related column between them. Joins are essential in relational databases because data is intentionally distributed across multiple tables. When you need information that spans multiple tables, a join brings that data together into a single result set.

The most common type of join is the inner join, which returns only the rows that have matching values in both tables. For example, if a `comments` table contains a `user_id` column that references the `id` column in a `users` table, an inner join can combine the comment text with the user's name:

```sql
SELECT users.username, comments.text
FROM comments
JOIN users ON comments.user_id = users.id;
```

This query returns a result set where each row contains a username and the text of a comment posted by that user. The join connects the two tables through the shared `id`/`user_id` values. Joins can be further classified into inner joins, left outer joins, right outer joins, and full outer joins, each including different subsets of rows based on whether matches exist.

Using numeric IDs for joins rather than names is important because names are not unique. Multiple users might share the same name, but each user has a unique ID. The foreign key relationship ensures that each comment is correctly attributed to exactly one user, regardless of name collisions.

## Synonym Reference

Building on the table from [[8 - Database Terms]], additional synonyms include:

| Concept | Synonym 1 | Synonym 2 |
|---------|-----------|-----------|
| View | Virtual table | Saved query |
| Front-end | Client-side | User interface |
| Back-end | Server-side | Application logic |

## Next Steps

With the essential terminology established, the next topic explores the concept of atomic values, which is a foundational principle of database normalization. See [[10 - Atomic Values]] for a detailed explanation.
