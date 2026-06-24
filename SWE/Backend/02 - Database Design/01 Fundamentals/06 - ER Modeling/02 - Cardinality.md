# Cardinality

Cardinality describes the numerical relationship between rows in one table and rows in another table. It specifies how many rows in the child table can be associated with a single row in the parent table, and vice versa. Cardinality is a fundamental property of every relationship in an ER diagram, and correctly identifying it is essential for producing a database schema that accurately reflects the business rules of the domain. See [[01 - Introduction to ER Modeling]] for the basics of ER diagrams and [[03 - Modality]] for the related concept of mandatory vs. optional participation.

## The Three Cardinality Types

### One-to-One

In a one-to-one relationship, a single row in table A is associated with at most one row in table B, and vice versa. Each row on one side corresponds to exactly one row (or zero rows) on the other side. One-to-one relationships are relatively uncommon but arise when an entity is split across multiple tables for organizational or performance reasons.

Example: A `user` table and a `user_profile` table, where each user has exactly one profile and each profile belongs to exactly one user.

### One-to-Many

In a one-to-many relationship, a single row in table A can be associated with multiple rows in table B, but each row in table B is associated with exactly one row in table A. This is the most common relationship type in relational databases and is implemented by placing a foreign key in the "many" side table that references the primary key of the "one" side table.

Example: A `card_holder` can own many credit `cards`, but each card belongs to exactly one card holder.

### Many-to-Many

In a many-to-many relationship, multiple rows in table A can be associated with multiple rows in table B, and vice versa. Many-to-many relationships cannot be directly implemented in a relational database; they must be decomposed into two one-to-many relationships using an intermediary table. The logical relationship is many-to-many in the conceptual model, but the physical implementation uses three tables.

Example: Many `students` can enroll in many `classes`. This is implemented with an intermediary `enrollment` table containing `student_id` and `class_id` as foreign keys.

## Crow's Foot Notation

Crow's Foot notation is the most widely used method for representing cardinality in ER diagrams. It uses distinct line endings to indicate the cardinality on each side of the relationship:

| Notation | Symbol | Meaning |
|---|---|---|
| One (mandatory) | `||` | Exactly one |
| One (optional) | `|O` | Zero or one |
| Many (mandatory) | `|<` | One or more |
| Many (optional) | `O<` | Zero or more |

The "crow's foot" is the three-pronged symbol (`<`) that indicates the "many" side. A single vertical line (`|`) indicates "one." A circle (`O`) indicates "zero" (optional).

### One-to-Many Example

```
+-------------+              +-------------+
| card_holder | 1        M   | card        |
|             |--------<-----|             |
+-------------+              +-------------+
```

Reading from left to right: one card holder can have many cards. The `1` side has a single line, and the `M` (many) side has the crow's foot.

### Many-to-One Example

```
+-------------+              +-------------+
| card        | M        1   | card_holder |
|             |-----<--------|             |
+-------------+              +-------------+
```

Reading from left to right: many cards can belong to one card holder. This is the same relationship viewed from the opposite direction.

## Cardinality and Physical Implementation

When you translate cardinality from the ER diagram into actual table definitions, the implementation rules are straightforward:

- **One-to-many**: Place the foreign key in the "many" side table. The "one" side holds the primary key.
- **One-to-one**: Place the foreign key in either table (choose the one that makes more semantic sense), and add a `UNIQUE` constraint to the foreign key column to prevent multiple references.
- **Many-to-many**: Create an intermediary table with foreign keys referencing both parent tables. The combination of foreign keys typically forms the primary key of the intermediary table.

| Cardinality | Implementation | Foreign Key Placement |
|---|---|---|
| One-to-one | FK + UNIQUE in either table | Either side |
| One-to-many | FK in the "many" table | Many side |
| Many-to-many | Intermediary table with two FKs | New table |

## Cardinality is About Rows, Not Tables

It is important to remember that cardinality describes the relationship between individual rows, not between entire tables. When we say "one card holder has many cards," we mean that a specific row in the `card_holder` table can be referenced by multiple rows in the `card` table. The `card_holder` table itself may contain thousands of rows, each of which can be referenced by multiple card rows. Cardinality describes the maximum number of related rows per individual row, not the total row count in each table.

Cross-reference: [[01 - Introduction to ER Modeling]], [[03 - Modality]], [[03 - One-to-Many Relationships]], [[04 - Many-to-Many Relationships]]
