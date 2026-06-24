# Foreign Key

A foreign key is a column (or set of columns) in one table that references the primary key of another table. Foreign keys are the mechanism by which relational databases establish connections between tables, enabling the relational model to distribute data across multiple tables while preserving the logical relationships between entities. Without foreign keys, each table would be an isolated collection of data with no way to indicate which rows in one table correspond to rows in another. See [[01 - Introduction to Keys]] for foundational key concepts.

## How Foreign Keys Work

A foreign key column in a child table stores values that must match existing values in the primary key column of the parent table. This creates a referential link: each row in the child table points to a specific row in the parent table. The foreign key ensures that the relationship between the two rows is valid and enforceable at the database level.

Consider a college database with a `class` table and an `instructor` table. The `class` table contains a `class_id` as its primary key, along with an `instructor_id` column that references the `instructor_id` primary key in the `instructor` table. Every row in the `class` table must have an `instructor_id` value that exists in the `instructor` table, ensuring that no class is assigned to a nonexistent instructor.

```
class table
+----------+---------------+------------+----------+
| class_id | instructor_id | building_id| name     |
+----------+---------------+------------+----------+
| 7        | 63            | 16         | Biology  |
| 38       | 63            | 14         | Chemistry|
| 123      | 8             | 16         | Physics  |
+----------+---------------+------------+----------+

instructor table
+---------------+--------+
| instructor_id | name   |
+---------------+--------+
| 8             | Jake   |
| 63            | Caleb  |
+---------------+--------+

building table
+-------------+-----------+
| building_id | name      |
+-------------+-----------+
| 14          | Science A |
| 16          | Science B |
+-------------+-----------+
```

In this example, the `class` table has two foreign key columns: `instructor_id` references the `instructor` table, and `building_id` references the `building` table. Each value in these columns must correspond to a valid primary key value in the respective parent table.

## Foreign Keys and Referential Integrity

Foreign keys enforce referential integrity, which means the database guarantees that every foreign key value points to a valid primary key value in the referenced table. If you attempt to insert a row with a foreign key value that does not exist in the parent table, the database rejects the operation. Similarly, if you attempt to delete a parent row that is still referenced by child rows, the database will prevent the deletion (depending on the constraint configuration).

This automatic enforcement eliminates the need for application-level checks to ensure data consistency. The database itself becomes the gatekeeper, preventing orphaned references and maintaining the structural integrity of the data across all related tables.

## Multiple Foreign Keys Per Table

While a table can have only one primary key, it can contain multiple foreign key columns, each referencing a different parent table. In the `class` table example above, both `instructor_id` and `building_id` are foreign keys pointing to separate tables. This is a common pattern in database design: a single entity often has relationships with several other entities.

However, each individual foreign key column can only reference one parent table. A single column cannot serve as a foreign key to two different tables simultaneously. If you need a relationship where a row in one table can be associated with multiple rows in another table (a many-to-many relationship), you must introduce an intermediary table. See [[06 - Designing One-to-Many Relationships]] for details on how to structure these relationships.

## Primary Key vs. Foreign Key Summary

| Property | Primary Key | Foreign Key |
|---|---|---|
| Purpose | Uniquely identifies each row | References a primary key in another table |
| Uniqueness | Must be unique | Values can repeat (many children can reference one parent) |
| Null allowed | Never | Depends on relationship modality |
| Per table | Exactly one | Multiple allowed |
| Referential target | None (it is the target) | Points to a primary key |

## SQL Example: Creating Tables with Foreign Keys

```sql
CREATE TABLE instructor (
    instructor_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE building (
    building_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE class (
    class_id INT PRIMARY KEY,
    instructor_id INT,
    building_id INT,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id),
    FOREIGN KEY (building_id) REFERENCES building(building_id)
);
```

The `FOREIGN KEY` constraint in the `CREATE TABLE` statement tells the database that `instructor_id` in the `class` table must match a value in the `instructor_id` column of the `instructor` table, and likewise for `building_id`. This declarative approach lets the database engine handle integrity enforcement automatically.

Cross-reference: [[01 - Introduction to Keys]], [[06 - Designing One-to-Many Relationships]], [[07 - NOT NULL Foreign Key]], [[08 - Foreign Key Constraints]]
