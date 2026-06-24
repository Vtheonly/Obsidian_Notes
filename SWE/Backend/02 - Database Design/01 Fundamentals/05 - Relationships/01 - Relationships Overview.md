# Relationships

## What Are Relationships in Databases

In database design, a relationship is a logical connection between two or more entities. Rather than storing all data in a single massive table, the relational model distributes data across multiple tables, each representing a distinct entity type. Relationships define how these separate tables are linked, enabling the database to reassemble related information through queries and joins. Without relationships, data stored in separate tables would be isolated and meaningless; relationships provide the structure that makes the distributed data coherent and useful.

The concept of relationships is fundamental to the relational model, though it is distinct from the term "relational" itself. The word "relational" in "relational database" comes from the mathematical concept of a relation (a table), not from the concept of relationships between tables. However, relationships between tables are a core feature of relational databases, and understanding them is essential for effective database design.

Relationships arise naturally from the way entities in the real world are connected. A student enrolls in classes, a customer places orders, an employee belongs to a department, and a user posts comments. Each of these connections represents a relationship that must be captured in the database structure. Identifying and properly modeling these relationships is one of the most important tasks in the database design process.

## Entities and Their Connections

Before defining relationships, it is necessary to identify the entities that will participate in them. An entity, as defined in [[09 - Database Terms]], is anything about which data is stored. In a typical database, there are multiple entity types, each represented by its own table. For example, a university database might include entities for students, professors, classes, and majors. Each entity has its own set of attributes that describe it.

Entities do not exist in isolation. They are connected to one another through meaningful associations that reflect the real-world interactions between them. A student takes classes, a professor teaches classes, and classes belong to a major. These connections are the relationships that the database must model. When designing a database, you must identify not only the entities and their attributes, but also the relationships between entities and the rules that govern those relationships.

The attributes of an entity describe what the entity is, while the relationships describe how the entity is connected to other entities. Both are necessary for a complete database design. A `students` table with columns for name, address, and major is informative, but it does not capture the fact that a student enrolls in specific classes or that classes are taught by specific professors. These connections require explicit relationship definitions.

## The Three Types of Relationships

Relationships between entities are classified into three types based on how many instances of one entity can be associated with how many instances of another entity. These three types are one-to-one, one-to-many, and many-to-many. Each type has different implications for how the relationship should be implemented in the database schema.

### One-to-One (1:1)

In a one-to-one relationship, a single instance of one entity is associated with exactly one instance of another entity, and vice versa. Each entity on either side of the relationship is limited to a single connection. For example, a person has exactly one social security number, and a social security number is assigned to exactly one person. One-to-one relationships are the least common type in practice, but they are important in specific design scenarios such as splitting a table for performance or security reasons. See [[02 - One-to-One Relationships]] for a detailed explanation.

### One-to-Many (1:N)

In a one-to-many relationship, a single instance of one entity can be associated with multiple instances of another entity, but each instance of the second entity is associated with only one instance of the first. For example, a user can place many orders, but each order belongs to exactly one user. This is the most common type of relationship in database design. The entity on the "one" side is called the parent, and the entity on the "many" side is called the child. The relationship is implemented by placing a foreign key in the child table that references the primary key of the parent table.

### Many-to-Many (M:N)

In a many-to-many relationship, multiple instances of one entity can be associated with multiple instances of another entity. For example, a student can enroll in many classes, and a class can have many students. Many-to-many relationships cannot be directly implemented in a relational database; they require an intermediate table (called a junction table or associative table) that breaks the relationship into two one-to-many relationships. The junction table contains foreign keys referencing both of the original tables.

## How Relationships Determine Table Structure

The type of relationship between two entities directly determines how the relationship is implemented in the database schema. Choosing the wrong relationship type leads to an incorrect schema that either restricts valid data or permits invalid data.

For one-to-many relationships, the standard implementation is to add a foreign key column to the table on the "many" side. If a user can have many orders, the `orders` table includes a `user_id` column that references the `id` column in the `users` table. Each order points to exactly one user, while a user can be pointed to by many orders.

For one-to-one relationships, a foreign key is placed in one of the two tables, with a `UNIQUE` constraint to ensure that each value appears at most once. Alternatively, the two entities can be combined into a single table if they always appear together and have the same lifecycle.

For many-to-many relationships, a junction table is created with two foreign key columns, one referencing each of the original tables. Each row in the junction table represents one association between the two entities. A `student_classes` table, for example, might have columns `student_id` and `class_id`, with each row indicating that a particular student is enrolled in a particular class.

## Practical Example: A University Database

Consider a university with the following entities and relationships:

- **Student to Major**: A student has one major (one-to-many from major to student)
- **Student to Class**: A student enrolls in many classes, and a class has many students (many-to-many)
- **Professor to Class**: A professor teaches many classes, but each class is taught by one professor (one-to-many from professor to class)
- **Professor to Department**: A professor belongs to one department, and a department has many professors (one-to-many from department to professor)

These relationships define the connections between the tables and determine where foreign keys should be placed. The `students` table would have a `major_id` foreign key. The `classes` table would have a `professor_id` foreign key. The `professors` table would have a `department_id` foreign key. The many-to-many relationship between students and classes would require a `student_classes` junction table with `student_id` and `class_id` foreign keys.

## Next Steps

The following sections explore each relationship type in detail, starting with one-to-one relationships. See [[02 - One-to-One Relationships]] for the first in-depth examination.
