# What is Database Design

## The Purpose of Database Design

Database design is the process of structuring a database to eliminate data anomalies, minimize redundancy, and ensure data integrity. It involves planning how data will be organized, how tables will relate to one another, and what rules will govern the data before any actual database is created. Designing a database is analogous to creating architectural blueprints before constructing a building: the quality of the design determines the quality, maintainability, and reliability of the final product.

A poorly designed database suffers from a range of problems that compound over time. Redundant data wastes storage and creates opportunities for inconsistencies. Update anomalies occur when the same piece of information is stored in multiple places and an update to one instance is not propagated to the others. Deletion anomalies occur when removing one piece of data inadvertently causes the loss of other unrelated but important information. Insertion anomalies occur when certain data cannot be added to the database without first adding unrelated data. These problems are not merely theoretical; they cause real operational failures, incorrect reports, and degraded application performance.

Good database design prevents these problems by carefully structuring data so that each piece of information is stored in exactly one place, relationships between data elements are clearly defined and enforced, and the schema supports all required operations without introducing inconsistencies.

## Update Anomalies

An update anomaly is a data integrity problem that arises when redundant data is stored in multiple locations within a database. If the same information exists in more than one row or table, and an update is applied to only one instance, the database now contains conflicting versions of the same fact. This is one of the most common and damaging consequences of poor database design.

Consider a poorly designed `users` table that includes columns for `id`, `username`, `phone`, and `favorite_color`. If a user wants to store multiple favorite colors, the table might end up with two rows for the same user:

| id | username | phone | favorite_color |
|----|----------|-------|---------------|
| 7 | caleb_curry | 800-555-0100 | camo |
| 7 | caleb_curry | 800-555-0100 | green |

If this user changes their phone number, updating only one row creates a contradiction: the same user now appears to have two different phone numbers. The database contains conflicting information, and there is no reliable way to determine which version is correct. This is a direct result of storing redundant data (the username and phone number appear in both rows) in a structure that does not properly separate concerns.

The solution is to redesign the schema so that each fact is stored in exactly one place. A `users` table would store user details, and a separate `favorite_colors` table would store color preferences, linked by a foreign key. When the phone number changes, it is updated in one row of the `users` table, and no inconsistencies can arise.

## Data Integrity Through Good Design

Data integrity is the overarching goal of database design. A database with integrity contains data that is accurate, consistent, and reliable. Three specific types of integrity are particularly relevant to the design process.

Entity integrity ensures that each row in a table is uniquely identifiable, typically through a primary key. No two rows should represent the same entity, and no primary key value should be null.

Referential integrity ensures that relationships between tables remain valid. If a row in a `sales` table references a user through a `user_id` foreign key, that user must exist in the `users` table. If the user is deleted, the reference in the `sales` table must be handled appropriately, either by cascading the deletion or by preventing it.

Domain integrity ensures that every value in a column conforms to the expected data type and range. A `phone_number` column should contain numbers, not text. A `birth_date` column should contain valid dates, not arbitrary strings.

Good database design enforces these integrity principles through table structure, constraints, and relationships. When the design is sound, the database itself prevents most types of data errors rather than relying on application logic to catch them after the fact. See [[08 - Data Integrity]] for a more detailed exploration of these concepts.

## The Three Schemas: Conceptual, Logical, and Physical

Database design is commonly divided into three levels of abstraction, known as schemas. These schemas represent a progression from general, platform-independent thinking to specific, implementation-ready planning. Rather than rigidly distinct phases, it is helpful to think of them as points on a continuum, where ideas become progressively more concrete and constrained.

### Conceptual Schema

The conceptual schema represents the highest level of abstraction. At this stage, the focus is on understanding what entities exist, what attributes they have, and how they relate to one another. There is no consideration of technical limitations, specific RDBMS features, or implementation details. The conceptual schema captures the business requirements and the logical relationships between data elements in their purest form.

For example, at the conceptual level, you might determine that a user can place multiple orders, and each order belongs to exactly one user. This relationship is documented without worrying about data types, indexing strategies, or which RDBMS will be used. The conceptual schema answers the question: what data do we need to store, and how is it logically connected?

### Logical Schema

The logical schema adds detail to the conceptual design by specifying the actual table structure. This includes defining tables with their columns, data types, primary keys, foreign keys, and constraints. The logical schema is still independent of any specific RDBMS, but it is precise enough that it could be implemented on any relational platform.

At this stage, you define a `users` table with columns like `id` (integer, primary key), `username` (varchar), `email` (varchar), and a `sales` table with columns like `id` (integer, primary key), `user_id` (integer, foreign key referencing `users.id`), `item` (varchar), and `sale_date` (date). The logical schema bridges the gap between abstract relationships and concrete table definitions.

### Physical Schema

The physical schema is the most specific level of design. It involves decisions about which RDBMS to use, how to configure the server, how to handle indexing, what storage engine to select, and how to implement security. The physical schema also considers performance optimization, such as which columns to index, whether to partition large tables, and how to configure connection pooling.

Physical design decisions also include determining how users will access the database (through a web application, desktop software, or direct SQL access), what views and stored procedures to create, and what backup and recovery strategies to implement. At this level, the design becomes tied to a specific technology stack and deployment environment.

| Schema Level | Focus | Example Decision |
|-------------|-------|-----------------|
| Conceptual | Entities and relationships | A user places orders |
| Logical | Table structure and constraints | `users` table with `id`, `username`; `orders` table with `user_id` foreign key |
| Physical | Implementation details | Use PostgreSQL with B-tree indexes on `users.id` |

## The Design Process

Database design is not a linear process; it is iterative. You begin with broad conceptual thinking, refine it into a logical schema, and then adapt it for physical implementation. At each stage, you may discover issues that require revisiting earlier decisions. A relationship you assumed was one-to-many might turn out to be many-to-many after further analysis. A column you planned to store as a single value might need to be decomposed into multiple columns to satisfy atomic value requirements.

The key principles to follow throughout the process are: store each fact in exactly one place, ensure all relationships are properly defined and enforced, make every value atomic, and choose data types and constraints that enforce domain integrity. When these principles are applied consistently, the resulting database will be robust, maintainable, and free of the anomalies that plague poorly designed systems.

## Next Steps

Understanding the design process leads naturally to a deeper exploration of data integrity, which is the primary objective of good design. See [[08 - Data Integrity]] for a comprehensive discussion of entity, referential, and domain integrity.
