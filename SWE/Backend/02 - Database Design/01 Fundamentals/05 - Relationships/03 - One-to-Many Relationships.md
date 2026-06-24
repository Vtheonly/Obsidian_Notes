# One-to-Many Relationships

A one-to-many relationship is one of the three fundamental relationship types in database design. In this relationship, a single record in one entity can be associated with multiple records in another entity, but each record on the "many" side belongs to exactly one record on the "one" side. This is the most common relationship pattern you will encounter in relational database design, and understanding it thoroughly is essential for building well-structured schemas.

## Definition

In a one-to-many relationship (often written as 1:N or 1:many), one instance of Entity A can relate to many instances of Entity B, while each instance of Entity B relates back to exactly one instance of Entity A. The directionality matters: the "one" side is the parent, and the "many" side is the child. This asymmetry distinguishes it from both one-to-one and many-to-many relationships, where the relationship is symmetric in both directions.

The key constraint is that the "many" side is exclusive to the "one" side. A given child record cannot be shared across multiple parent records. If sharing were allowed, the relationship would no longer be one-to-many and would instead be many-to-many. Recognizing this exclusivity is critical when analyzing real-world requirements and translating them into database schemas.

## Examples

### User and Comments

Consider a website where users can post comments. A single user can write many comments over time, but each individual comment is authored by exactly one user. The comment belongs exclusively to that user. No comment is co-authored by multiple users in this model, and no comment exists without an author. This is a classic one-to-many relationship where User is on the "one" side and Comment is on the "many" side.

```
users
+---------+----------+-----------+
| user_id | username | email     |
+---------+----------+-----------+
| 1       | alice    | a@a.com   |
| 2       | bob      | b@b.com   |
+---------+----------+-----------+

comments
+------------+---------+-------------------+
| comment_id | user_id | content           |
+------------+---------+-------------------+
| 101        | 1       | Great post!       |
| 102        | 1       | I agree entirely. |
| 103        | 2       | Nice work.        |
+------------+---------+-------------------+
```

Notice how user_id `1` (alice) appears twice in the comments table, because she posted two comments. Each comment, however, points back to exactly one user.

### Department and Employees

Another common example is a company where each department has many employees, but each employee belongs to exactly one department. The department is on the "one" side, and the employees are on the "many" side. If an employee could belong to multiple departments simultaneously, the relationship would need to be modeled differently as a many-to-many relationship.

```
departments
+-------------+------------------+
| dept_id     | dept_name        |
+-------------+------------------+
| 10          | Engineering      |
| 20          | Marketing        |
+-------------+------------------+

employees
+------------+---------+----------+
| emp_id     | dept_id | name     |
+------------+---------+----------+
| 1001       | 10      | Alice    |
| 1002       | 10      | Bob      |
| 1003       | 20      | Carol    |
+------------+---------+----------+
```

## Implementation with Foreign Keys

One-to-many relationships are implemented in relational databases by placing a **foreign key** on the "many" side of the relationship. The foreign key in the child table references the primary key of the parent table. This is a fundamental rule: the foreign key always goes on the "many" side. Placing it on the "one" side would not work because a single column can only hold one value, and you would need to store multiple references there.

```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE comments (
    comment_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

The `user_id` column in the comments table is the foreign key. It ensures that every comment is associated with a valid user. The database enforces this constraint through referential integrity: you cannot insert a comment with a `user_id` that does not exist in the users table, and you cannot delete a user who still has comments (depending on the constraint configuration).

## Key Principles

- The foreign key is always placed on the "many" side of the relationship, never on the "one" side.
- Each record on the "many" side references exactly one record on the "one" side.
- A single record on the "one" side can be referenced by many records on the "many" side.
- The "one" side is the parent table; the "many" side is the child table.
- This is the most frequently occurring relationship type in relational databases.

## See Also

- [[01 - Relationships Overview]] - Overview of all relationship types
- [[06 - Designing One-to-Many Relationships]] - How to design and implement one-to-many relationships in practice
- [[04 - Many-to-Many Relationships]] - Contrast with the many-to-many pattern
