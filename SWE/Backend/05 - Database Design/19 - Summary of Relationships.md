# Summary of Relationships

Relational databases support three fundamental types of relationships between entities: one-to-one, one-to-many, and many-to-many. Each type has a distinct implementation strategy, and choosing the correct relationship type depends on the specific requirements of the application. This summary provides a consolidated reference for all three relationship types, their design patterns, and when to use each one.

## Relationship Types Overview

### One-to-One (1:1)

In a one-to-one relationship, a single record in Entity A is associated with exactly one record in Entity B, and vice versa. This is the simplest relationship type and is often stored as a column within a single table rather than across two tables. When the related data has its own distinct attributes, it can be split into a separate table with a unique foreign key or shared primary key enforcing the one-to-one constraint.

One-to-one relationships are the least common in practice. They typically arise when an entity has a subset of attributes that are optional, sensitive, or conceptually distinct. Examples include a user and their profile details, a person and their passport, or a cardholder and their single credit card.

### One-to-Many (1:N)

In a one-to-many relationship, a single record in Entity A can be associated with multiple records in Entity B, but each record in Entity B belongs to exactly one record in Entity A. This is the most common relationship type in relational databases. It is implemented by placing a foreign key on the "many" side that references the primary key on the "one" side.

Examples include a user and their comments, a department and its employees, an order and its line items, and a customer and their purchases. The "one" side is the parent table, and the "many" side is the child table containing the foreign key.

### Many-to-Many (M:N)

In a many-to-many relationship, multiple records in Entity A can be associated with multiple records in Entity B, and vice versa. This relationship cannot be directly stored in a relational database. It must be decomposed into two one-to-many relationships using a junction table that contains foreign keys referencing both parent tables.

Examples include students and classes, products and orders, doctors and patients, and tags and articles. The junction table serves as the child of both parent tables, and its composite primary key ensures that each association is unique.

## Comparison Table

| Property | One-to-One | One-to-Many | Many-to-Many |
|----------|-----------|-------------|--------------|
| Tables required | 1 (or 2) | 2 | 3 |
| Foreign key placement | Unique FK or shared PK | On the "many" side | In the junction table |
| Parent-child structure | Symmetric or none | Parent = "one", Child = "many" | Both entities are parents; junction is child |
| Junction table needed | No | No | Yes |
| Common occurrence | Rare | Very common | Common |
| Example | User and username | User and comments | Students and classes |

## Implementation Patterns

### One-to-One Implementation

```sql
-- Option 1: Single table (most common)
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Option 2: Two tables with unique foreign key
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE user_profiles (
    profile_id INT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    bio TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Option 3: Shared primary key
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY,
    bio TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### One-to-Many Implementation

```sql
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    dept_id INT NOT NULL,
    emp_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
```

### Many-to-Many Implementation

```sql
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE classes (
    class_id INT PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL
);

CREATE TABLE enrollments (
    class_id INT NOT NULL,
    student_id INT NOT NULL,
    PRIMARY KEY (class_id, student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

## Choosing the Right Relationship

Determining the correct relationship type is not always automatic. The same two entities can have different relationship types depending on the application's business rules. Consider the relationship between a class and a professor:

- **One-to-one**: A professor teaches exactly one class, and each class is taught by exactly one professor. This might apply in a small training company where instructors are dedicated to a single course.
- **One-to-many**: A professor can teach many classes, but each class has only one professor. This is common in many universities where courses have a single instructor.
- **Many-to-many**: A professor can teach many classes, and each class can be taught by many professors (team-teaching, multiple sections). This is common in large universities with co-instructed courses.

The relationship type depends entirely on the business requirements of the specific application. There is no universal answer; you must analyze the rules and constraints of the domain you are modeling. Always ask: Can Entity A be associated with multiple instances of Entity B? Can Entity B be associated with multiple instances of Entity A? The answers determine the relationship type.

## Key Takeaways

- One-to-one relationships are usually stored as columns within a single table unless the related data has its own attributes.
- One-to-many relationships use two tables with the foreign key on the "many" side.
- Many-to-many relationships require a junction table to decompose them into two one-to-many relationships.
- The same pair of entities can have different relationship types depending on the application context.
- The parent-child distinction determines foreign key placement: the child always holds the foreign key.

## See Also

- [[12 - One-to-One Relationships]] - Conceptual overview of one-to-one relationships
- [[13 - One-to-Many Relationships]] - Conceptual overview of one-to-many relationships
- [[14 - Many-to-Many Relationships]] - Conceptual overview of many-to-many relationships
- [[15 - Designing One-to-One Relationships]] - Design patterns for one-to-one
- [[16 - Designing One-to-Many Relationships]] - Design patterns for one-to-many
- [[18 - Designing Many-to-Many Relationships]] - Design patterns for many-to-many
