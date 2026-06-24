# Introduction to Entity Relationship Modeling

Entity Relationship (ER) modeling is a standardized method for visually representing the structure of a database before it is implemented in code. An ER diagram captures the tables (entities), their columns (attributes), and the connections between them (relationships) in a format that both technical and non-technical stakeholders can understand. ER modeling serves as the blueprint for your database, allowing you to validate the design with others before writing a single line of SQL. See [[01 - Relationships Overview]] for the foundational concepts of database relationships.

## What ER Diagrams Represent

An ER diagram defines the Data Definition Language (DDL) structure of your database: the tables, columns, data types, constraints, primary keys, foreign keys, and indexes. It does not include the data itself (no sample rows or values). The purpose is to capture the schema -- the rules and structure that govern how data is organized -- rather than the actual data content.

When you draw an ER diagram for a `users` table, you list the columns such as `user_id`, `username`, `password`, and `email`, along with their data types and constraints. You do not fill in specific values like "Caleb Curry" or "password123" because those are data values, not structural definitions.

## Terminology

Several terms refer to the same general concept, and you will encounter them interchangeably in database literature and tools:

- **ER Model** (Entity-Relationship Model): the abstract conceptual design
- **ERD** (Entity-Relationship Diagram): the visual representation of that model
- **EER** (Enhanced Entity-Relationship): an extended version that adds support for specialization, generalization, and categorization
- **Database design diagram**: a more casual term for the same visual output

The distinction between "relation" and "relationship" is important. A **relation** is a table (a set of tuples with the same attributes). A **relationship** is a connection between two tables. ER diagrams model relationships, not relations.

## Drawing Entities (Tables)

In an ER diagram, each table is represented as a rectangle. The table name is written at the top of the rectangle or in a separate header section. The columns are listed vertically within the rectangle, one per line. You may also include data types and constraints such as `NOT NULL`, though these are often omitted during early design phases and added when finalizing the schema.

```
+---------------------+
| users               |
+---------------------+
| user_id    INT  PK  |
| username   VARCHAR  |
| password   VARCHAR  |
| email      VARCHAR  |
+---------------------+
```

In this text-based representation, `PK` denotes the primary key column. When using a graphical ER design tool, primary keys are typically underlined or marked with a key icon. Foreign key columns may be labeled `FK` or connected to their referenced table with a line.

## Drawing Relationships

Relationships between tables are represented by lines connecting the rectangles. The style of the line conveys the type and cardinality of the relationship. Different notation systems exist (Chen notation, Crow's Foot notation, UML), but the most common for practical database design is Crow's Foot notation, which uses distinct end markers to indicate cardinality:

- A single vertical line (`|`) represents "one"
- A three-pronged shape (crow's foot) represents "many"
- A circle (`O`) represents "zero" (optional)
- A vertical line through a circle represents "one or zero" (optional one)

```
+-----------+          +-----------+
| users     | 1    M   | comments  |
|           |----<-----|           |
+-----------+          +-----------+
```

In this diagram, one user can have many comments (a one-to-many relationship). The crow's foot on the `comments` side indicates the "many" end.

## Tools for ER Modeling

Several software tools support ER diagram creation, many of which include forward engineering capabilities that generate SQL `CREATE TABLE` statements directly from the diagram:

- **MySQL Workbench**: supports EER diagrams with forward and reverse engineering for MySQL databases
- **Vertabelo**: a web-based tool that supports multiple database engines
- **Lucidchart**: a general-purpose diagramming tool with ER templates
- **draw.io / diagrams.net**: a free diagramming tool with ER shape libraries

Forward engineering is particularly powerful because it allows you to design visually and then produce the corresponding DDL code automatically, reducing the chance of manual transcription errors.

## From Design to Implementation

The typical workflow for using ER diagrams in database development follows three phases:

1. **Conceptual design**: Identify the entities, their attributes, and the relationships between them. Focus on the business requirements without worrying about implementation details like data types or indexes.
2. **Logical design**: Refine the conceptual model by adding data types, primary keys, foreign keys, and constraints. Apply normalization rules to eliminate redundancy and dependency problems.
3. **Physical design**: Generate the actual SQL DDL statements from the logical model and deploy them to the database server. Consider performance factors such as indexing, partitioning, and storage engines.

ER diagrams are most valuable during the first two phases, where they serve as a communication tool and a validation mechanism. Once the design is finalized, the physical implementation follows directly from the logical model.

Cross-reference: [[01 - Relationships Overview]], [[02 - Cardinality]], [[03 - Modality]], [[01 - Introduction to Database Normalization]]
