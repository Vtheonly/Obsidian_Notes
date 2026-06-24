# RDBMS

## What is an RDBMS

A Relational Database Management System (RDBMS) is the software application that manages relational databases. It provides the tools and interfaces needed to create, maintain, query, and secure relational databases. While the database itself is the collection of structured data, the RDBMS is the system that sits between the raw data and the users or applications that need to interact with it. Without an RDBMS, data stored on disk would be an unorganized collection of bits with no practical way to retrieve or manipulate it in a structured manner.

The RDBMS takes data stored on physical storage media and presents it in organized, human-readable tables. Data on a hard drive may be scattered across different physical locations, but the RDBMS abstracts this complexity and presents a clean, tabular view of the data. This abstraction is what allows users and applications to interact with data using high-level commands rather than dealing with low-level file operations.

## DBMS vs. RDBMS

A Database Management System (DBMS) is a broader category of software that manages any type of database, whether relational, hierarchical, network-based, or another model. An RDBMS is a specific subtype of DBMS that is designed to work exclusively with relational databases. The distinction matters because not all database systems follow the relational model, and the features offered by an RDBMS are specifically tailored to the table-and-relationship structure that defines relational data.

In practice, most modern database systems you encounter in business and web development will be RDBMSes. The relational model dominates the industry because of its mathematical rigor, its support for complex queries, and its robust integrity mechanisms. When people refer to a database system in a professional context, they are almost always referring to an RDBMS.

## Queries

One of the primary functions of an RDBMS is to execute queries. A query is a request for data or an action performed on data, typically expressed in SQL. Queries allow you to search for specific records, filter data based on conditions, aggregate information, and perform calculations across large datasets. The RDBMS processes the query, retrieves the relevant data from storage, and returns the results in a structured format.

For example, consider a database with millions of user records. Finding every user who has not logged in for over a year would be impractical to do manually. An RDBMS allows you to write a query such as `SELECT * FROM users WHERE last_login < '2025-01-01'` and receive the results instantly. This capability to search, filter, and manipulate data at scale is what makes an RDBMS essential for any data-driven application.

## Views

A view is a virtual table that presents a subset or transformation of the data stored in the underlying tables. Views do not store data themselves; instead, they provide a customized presentation of the existing data. The RDBMS supports a view mechanism that allows different users to see different slices of the same data without modifying the underlying table structure.

Consider a `users` table with columns for `id`, `username`, `password`, `email`, `street_address`, `city`, and `state`. A database administrator might need access to all columns, while a marketing analyst only needs `username` and `email`, and a regular user of a website should only see their own `username` and `email`. Views allow each of these stakeholders to access precisely the data they need and nothing more.

Views serve as a security mechanism because they restrict what data is visible to different users. A website user accessing their profile page might interact with a view that returns only their own record, while an internal employee might access a view that includes all users but excludes sensitive fields like passwords. This fine-grained access control is a critical feature of any RDBMS.

## Transactions

A transaction is a unit of work that is executed as a single, indivisible operation. Transactions follow the ACID properties: Atomicity, Consistency, Isolation, and Durability. The key principle is that a transaction either completes entirely or does not happen at all. If any step within a transaction fails, the entire transaction is rolled back and the database returns to its previous state.

A classic example is transferring money between bank accounts. The transaction involves two steps: deducting money from one account and adding it to another. If the system crashes after the deduction but before the addition, the money would simply disappear. Transactions prevent this by ensuring that both steps succeed or neither does. If the power goes out mid-transaction, the RDBMS rolls back the partial changes and the database remains consistent.

This capability is essential for any application where data accuracy is critical, including financial systems, inventory management, and reservation systems. Without transaction support, partial updates could leave the database in an inconsistent state that is difficult or impossible to repair.

## Examples of RDBMS

Several widely used RDBMS platforms exist, each with its own strengths and ecosystem. The core principles of relational database design apply across all of them, which is why this course focuses on general concepts rather than platform-specific features.

**MySQL** is one of the most popular open-source RDBMS platforms, widely used in web applications. It is known for its ease of use, strong community support, and compatibility with popular programming languages and frameworks.

**PostgreSQL** is another open-source RDBMS, distinguished by its advanced feature set, extensibility, and strict adherence to SQL standards. It supports complex data types, full-text search, and geospatial data, making it a preferred choice for applications that require sophisticated querying capabilities.

**Oracle Database** is a commercial RDBMS known for its scalability, reliability, and comprehensive feature set. It is widely used in large enterprise environments where performance, security, and support are critical requirements.

**Microsoft SQL Server** is a commercial RDBMS that integrates tightly with the Microsoft ecosystem. It is commonly used in corporate environments that rely on Windows-based infrastructure and Microsoft development tools.

Despite their differences, all of these systems implement the same fundamental relational model. The SQL syntax varies slightly between platforms, but the concepts of tables, rows, columns, keys, constraints, and relationships remain consistent.

## Consistency and the Front End

An RDBMS also provides consistency between the backend data layer and the frontend application layer. When the structure of the database changes, the frontend does not necessarily need to change with it. For example, if a database administrator decides to split a `full_name` column into `first_name` and `last_name` columns, a view can be created that presents the data in the original format, keeping the frontend unchanged. This decoupling allows the backend to evolve independently of the frontend, reducing the risk of breaking changes.

Server-side scripting languages such as PHP, Python, or Node.js further insulate the frontend from the database layer. If an error occurs on the database side, the server-side code can present a generic error message to the user rather than exposing internal details about the database structure. This is both a usability concern and a security measure, as revealing database structure information could aid attackers in exploiting the system.

## Next Steps

With an understanding of what an RDBMS does, the next step is to learn about the language used to communicate with it. SQL is the standard language for defining database structures and manipulating the data within them. See [[05 - Introduction to SQL]] for a detailed introduction.
