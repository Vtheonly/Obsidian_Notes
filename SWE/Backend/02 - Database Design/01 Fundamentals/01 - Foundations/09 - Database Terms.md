# Database Terms

## Overview

This glossary defines the essential terms used in database design. Many of these terms have synonyms that are used interchangeably in different contexts, and understanding these equivalences is critical for avoiding confusion. The terms are organized into two categories: data-related terms and design-related terms.

## Data-Related Terms

### Data

Data refers to any information that can be recorded, stored, and processed within a database. Data encompasses numbers, text strings, dates, boolean values, and any other factual information that an application needs to persist. Data can represent customer records, transaction logs, user profiles, product catalogs, weather measurements, or virtually any other measurable or recordable fact. In the context of a database, data is the raw material that the system organizes, protects, and makes accessible through queries.

### Database

A database is an organized collection of structured data that is stored and accessed electronically. Unlike an unorganized collection of files, a database provides a systematic way to store, retrieve, update, and manage data through a database management system. Databases enforce structure, constraints, and relationships that ensure data integrity and support efficient querying.

### RDBMS

A Relational Database Management System (RDBMS) is software that manages relational databases. It provides the tools to create, query, update, and administer databases organized according to the relational model. An RDBMS handles data storage, retrieval, security, and integrity enforcement. Examples include MySQL, PostgreSQL, Oracle Database, and Microsoft SQL Server. See [[04 - RDBMS]] for a detailed explanation.

### Null

Null represents the absence of a value in a database field. When a column for a particular row contains no data, that field is said to be null. Null is not the same as zero, an empty string, or a blank space; it specifically means that no value has been entered or that the value is unknown. Null values are common in optional fields. For example, a `fax_number` column in a `users` table might be null for users who do not have a fax number. Null values require special handling in queries because comparisons with null (such as `= NULL`) do not behave as expected; the correct syntax is `IS NULL` or `IS NOT NULL`.

### Anomaly

An anomaly is an error or inconsistency in data that results from poor database design. Anomalies typically fall into three categories: update anomalies, insertion anomalies, and deletion anomalies. An update anomaly occurs when updating one instance of redundant data leaves other instances unchanged, creating contradictory information. An insertion anomaly occurs when certain data cannot be added without first adding unrelated data. A deletion anomaly occurs when deleting one piece of data inadvertently causes the loss of other unrelated information. Anomalies are prevented through proper database design and normalization. See [[07 - What is Database Design]] for examples.

### Integrity

Integrity refers to the accuracy, consistency, and reliability of data in a database. Data integrity is maintained through constraints, relationships, and design principles that prevent anomalies and ensure that data remains correct over time. The three main types of integrity are entity integrity, referential integrity, and domain integrity. See [[08 - Data Integrity]] for a comprehensive discussion.

## Design-Related Terms

### Entity

An entity is anything about which data is stored in a database. Entities represent the real-world objects, concepts, or events that the database is designed to track. Examples include users, orders, products, comments, transactions, employees, and courses. An entity type refers to the category of entity (such as "user"), while a specific entity refers to an individual instance (such as the user with ID 72). In a table, the entity type corresponds to the table itself, and each row represents a specific entity.

### Attribute

An attribute is a specific piece of information stored about an entity. Attributes describe the characteristics or properties of an entity. For a user entity, attributes might include username, password, email, and phone number. An attribute type refers to the category (such as "username"), while a specific attribute value is the actual data stored for a particular entity (such as "caleb_curry"). In a table, attribute types correspond to columns, and attribute values correspond to the data in individual cells.

### Relation

A relation is the mathematical term for a table in a relational database. The term comes from set theory and refers to a structured set of data organized into rows and columns. In everyday database work, the terms "relation" and "table" are used interchangeably, though "relation" carries the formal mathematical connotation of the relational model. The word "relational" in "relational database" derives from this concept of relations, not from the concept of relationships between tables.

### Tuple

A tuple is the formal mathematical term for a row in a relation (table). A tuple represents a single entity instance, containing a value for each attribute in the relation. For example, the tuple `(72, 'caleb_curry', 'pi123', 'coolguy@hotmail.com')` represents one specific user in a `users` table with columns for id, username, password, and email. The terms "tuple," "row," and "record" are synonymous.

### Table

A table is the physical representation of a relation in a relational database. It consists of rows and columns, where each column defines an attribute and each row represents a specific entity. Tables are the primary structural element in a relational database, and all data is stored within tables. A well-designed database contains multiple related tables, each focused on a single entity type.

### Row

A row is a horizontal collection of values in a table, representing a single entity instance. Each row contains one value for every column defined in the table, and together these values describe one specific entity. Synonyms for row include tuple and record.

### Column

A column is a vertical structure in a table that defines a specific attribute. Every row in the table has a value (or null) for each column. Columns have names and data types that determine what kind of data they can store. Synonyms for column include attribute and field.

### Field

A field is another term for a column in a table. It can also refer to the intersection of a row and a column, which holds a single value. The term "field" is more commonly used in file-based data processing contexts, while "column" is the standard term in relational database terminology.

### Value

A value is the actual data stored in a specific cell of a table, at the intersection of a row and a column. Values are the concrete instances of attributes for specific entities. For example, if the `username` column contains "caleb_curry" for a particular row, then "caleb_curry" is the value. Values must conform to the data type and constraints defined for their column.

### Entry

An entry is an informal term for a row in a table, referring to the act of entering data into the database. When you insert a new row, you create a new entry. The term emphasizes the process of data insertion rather than the structural concept of a row.

### Schema

A schema is a blueprint or structural definition of a database. It describes the tables, columns, data types, relationships, constraints, and other structural elements that define how data is organized. Schemas exist at three levels: conceptual (high-level relationships), logical (detailed table structure), and physical (implementation-specific details). See [[07 - What is Database Design]] for a detailed explanation of schema levels.

### Normalization

Normalization is the process of organizing a database schema to reduce redundancy and eliminate anomalies. It involves applying a series of rules, called normal forms, that progressively refine the structure of the database. The most commonly discussed normal forms are First Normal Form (1NF), Second Normal Form (2NF), and Third Normal Form (3NF). Normalization ensures that each piece of data is stored in exactly one place and that the database structure supports data integrity. This topic is covered in detail in later sections.

### Naming Conventions

Naming conventions are standardized patterns used for naming database objects such as tables, columns, and constraints. Consistent naming improves readability, reduces errors, and makes the database schema easier to understand and maintain. Common conventions include using lowercase for all names, underscores instead of spaces, and consistent foreign key naming patterns. See [[06 - Naming Conventions]] for detailed guidelines.

### Keys

Keys are columns or combinations of columns used to uniquely identify rows and establish relationships between tables. The primary key uniquely identifies each row within its own table. Foreign keys reference the primary key of another table to create relationships. Keys are fundamental to enforcing entity integrity and referential integrity. There are several types of keys, including primary keys, foreign keys, candidate keys, alternate keys, surrogate keys, and natural keys, each serving a specific purpose in database design.

## Synonym Reference

Many database terms have multiple names that are used interchangeably. The following table maps equivalent terms:

| Concept | Synonym 1 | Synonym 2 | Synonym 3 |
|---------|-----------|-----------|-----------|
| Table | Relation | File | -- |
| Row | Tuple | Record | Entry |
| Column | Attribute | Field | -- |

## Next Steps

For additional terminology related to SQL and application architecture, see [[10 - More Database Terms]].
