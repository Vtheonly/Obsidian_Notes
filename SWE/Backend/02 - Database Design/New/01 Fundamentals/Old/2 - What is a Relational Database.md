# What is a Relational Database

## The Relational Model

A relational database is a type of database that stores and organizes data into tables that are related to one another through defined connections. The term "relational" derives from the mathematical concept of a relation, which in database theory refers to a set of data organized into a table structure. This model was introduced by Edgar F. Codd in 1970 and has since become the dominant paradigm for structured data storage. The relational model provides a rigorous, mathematically grounded framework for ensuring data consistency, reducing redundancy, and enabling flexible data retrieval.

In a relational database, data is not stored in a single monolithic structure. Instead, it is divided into separate tables, each representing a distinct entity type. These tables are then connected through relationships, typically using keys that reference one table from another. This separation allows each table to focus on a single subject, which reduces duplication and makes the overall data structure more maintainable. When changes are needed, they can be made in one place without cascading errors across the entire dataset.

## Entities and Attributes

Two fundamental concepts underpin the relational model: entities and attributes. An entity is anything about which data is stored. In a business context, entities might include customers, orders, products, employees, or transactions. Each entity represents a distinct category of information that the database needs to track. Entities are not limited to people or tangible objects; they can represent abstract concepts such as accounts, sessions, or memberships.

Attributes are the specific pieces of information stored about an entity. If the entity is a user, the attributes might include the user's name, username, password, email address, phone number, and date of registration. Each attribute captures a single, atomic piece of information about the entity. The combination of all attributes for a given entity instance forms a complete record of that entity within the database.

The distinction between entity types and specific entities is important. An entity type is the category or class, such as "user" or "order." A specific entity is an individual instance, such as a particular user named Caleb or a specific order with ID 1052. In table terms, the entity type corresponds to the table itself, while specific entities correspond to individual rows within that table.

## Tables, Rows, and Columns

The relational model represents data using tables, which are the physical manifestation of relations. A table consists of columns and rows, each serving a distinct purpose in the organization of data.

Columns represent the attributes of the entity type. Each column has a name and a data type that defines what kind of values it can hold. For example, a `users` table might have columns named `id`, `username`, `password`, and `email`. The column names serve as labels that describe the attribute, and the data type ensures that only appropriate values are stored in that column.

Rows, also known as tuples or records, represent individual entity instances. Each row contains a value for every column in the table, describing a single specific entity. For instance, one row in the `users` table might contain the values `72`, `caleb_curry`, `pi123`, and `coolguy@hotmail.com`, representing one particular user. Every row in the table should describe a distinct entity, and no two rows should be identical in all their column values.

The intersection of a row and a column is called a cell or field, and it holds a single value. This structure is similar to a spreadsheet at a glance, but the relational model adds constraints, relationships, and integrity rules that spreadsheets lack.

| id | username | password | email |
|----|----------|----------|-------|
| 72 | caleb_curry | pi123 | coolguy@hotmail.com |
| 73 | billy_joe | pizza | bjoe@example.com |

## The Mathematical Origin of Relations

The concept of a relation in database theory has its origins in set theory and mathematics. In mathematical terms, a relation is formed by combining elements from two or more sets. For example, given the set `{2, 4}` and the set `{6, 8}`, a Cartesian product produces all possible combinations: `{(2,6), (2,8), (4,6), (4,8)}`. Each pairing represents a relation between elements of the two sets.

In the database context, this concept is applied not to numbers but to attributes of real-world entities. Instead of combining sets of numbers, the relational model combines attribute types (the columns) with attribute values (the data in rows) to form meaningful records. The connection between attribute types and their values for a specific entity constitutes a relation, which is physically stored as a row in a table. This mathematical foundation gives the relational model its precision and predictability, enabling the powerful query capabilities that relational databases are known for.

## How Relationships Work Between Tables

One of the defining features of a relational database is that data is distributed across multiple tables, and these tables are connected through relationships. Rather than storing all information in a single massive table, the relational model separates data by entity type. A `users` table stores information about users, a `sales` table stores information about sales, and a `comments` table stores information about comments.

Relationships between tables are established using keys. A primary key uniquely identifies each row in a table, while a foreign key in another table references that primary key to create a link. For example, if every sale must be associated with a user, the `sales` table would include a `user_id` column that references the `id` column in the `users` table. This foreign key relationship ensures that every sale points to a valid, existing user.

These relationships are what make the relational model so powerful. They allow data to be stored without redundancy (each user's information appears only once, in the `users` table) while still enabling complex queries that combine data from multiple tables (finding all sales made by a specific user, for example). The relationships enforce referential integrity, ensuring that connections between tables remain valid and consistent even as data is inserted, updated, or deleted.

## Key Terminology Summary

| Concept | Table Equivalent | Also Known As |
|---------|-----------------|---------------|
| Entity type | Table | Relation, File |
| Specific entity | Row | Tuple, Record |
| Attribute | Column | Field |
| Attribute value | Cell value | Value |

## Next Steps

Understanding how relational databases organize data into tables with relationships sets the stage for learning about the software systems that manage these databases. See [[3 - RDBMS]] for an explanation of Relational Database Management Systems and the capabilities they provide.
