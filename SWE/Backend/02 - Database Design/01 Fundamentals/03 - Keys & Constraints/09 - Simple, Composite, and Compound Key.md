# Simple Key, Composite Key, Compound Key

Keys can be categorized by how many columns they span. A simple key consists of a single column, while composite and compound keys span multiple columns. These categories are design-level classifications -- they describe the structure of your key choice but are not keywords you must declare in SQL. Understanding these distinctions helps you evaluate trade-offs between simplicity and enforceable uniqueness when designing your tables. See [[01 - Introduction to Keys]] for the broader introduction to key concepts.

## Simple Key

A simple key is a key that consists of exactly one column. The column alone is sufficient to guarantee uniqueness for every row in the table. Simple keys are straightforward to implement, easy to index, and perform well in join operations because the database only needs to compare a single value.

Surrogate keys are always simple keys because they are typically a single auto-incremented integer column (e.g., `user_id`, `order_id`). Natural keys can also be simple if a single column naturally provides uniqueness, such as a `username` or an `isbn` column.

```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,        -- simple surrogate key
    username VARCHAR(50) UNIQUE NOT NULL  -- simple natural key candidate
);
```

In this example, both `user_id` and `username` are simple keys. `user_id` is the primary key (a simple surrogate key), and `username` is an alternate key (a simple natural key).

## Composite Key

A composite key is a key that consists of two or more columns, where at least one of the columns is not a key by itself. The combination of all columns in the composite key must be unique, but individual columns within the key may contain duplicate values. Composite keys commonly appear with natural keys, because a single column may not be sufficient to guarantee uniqueness.

For example, in an intermediary table for video comments, neither `user_id` nor `video_id` alone guarantees uniqueness (a user can comment on the same video more than once). Adding a `timestamp` column creates a composite key where the combination of `user_id`, `video_id`, and `timestamp` is unique, even though `timestamp` alone is not a key.

```sql
CREATE TABLE video_comments (
    user_id INT NOT NULL,
    video_id INT NOT NULL,
    comment_time TIMESTAMP NOT NULL,
    content TEXT NOT NULL,
    PRIMARY KEY (user_id, video_id, comment_time),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (video_id) REFERENCES videos(video_id)
);
```

In this table, `user_id` and `video_id` are each foreign keys (and therefore keys in their own right), but `comment_time` is not a key column. The presence of at least one non-key column makes this a composite key rather than a compound key.

## Compound Key

A compound key is a key that consists of two or more columns, where every column in the key is itself a key (typically a foreign key) in its own right. The most common example is the primary key of an intermediary table in a many-to-many relationship, where each column is a foreign key referencing a different parent table.

For example, in a college enrollment system, the `student_classes` intermediary table might use the combination of `student_id` and `class_id` as its primary key. Both columns are foreign keys referencing other tables, and both are keys individually. The combination must be unique (a student cannot be enrolled in the same class twice), but each column can repeat independently.

```sql
CREATE TABLE student_classes (
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    PRIMARY KEY (student_id, class_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);
```

In this table, both `student_id` and `class_id` are keys (foreign keys). Their combination forms the primary key. Every column in the primary key is itself a key, making this a compound key.

## Composite vs. Compound: The Distinction

The difference between composite and compound keys is subtle and not universally agreed upon. Some practitioners and database systems use the terms interchangeably to mean any multi-column key. When the distinction is made, the rule is:

- **Composite key**: at least one column in the key is not a key by itself
- **Compound key**: every column in the key is itself a key

| Key Type | Columns | Each Column a Key? | Example |
|---|---|---|---|
| Simple | 1 | N/A (single column) | `user_id` |
| Composite | 2+ | At least one is not | `user_id + video_id + timestamp` |
| Compound | 2+ | Yes, all are keys | `student_id + class_id` |

This distinction is a design concept, not a SQL keyword. You do not declare a key as "composite" or "compound" in your schema. The classification exists to help you reason about the structure and meaning of your key choices.

## Adding a Surrogate Key to an Intermediary Table

Some database frameworks and ORMs require a simple (single-column) primary key on every table. In such cases, you can add a surrogate key to an intermediary table while preserving the compound key as a unique constraint:

```sql
CREATE TABLE student_classes (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    UNIQUE (student_id, class_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);
```

Here, `enrollment_id` serves as the simple surrogate primary key, while the `UNIQUE` constraint on `(student_id, class_id)` preserves the business rule that each student-class combination must be unique.

Cross-reference: [[01 - Introduction to Keys]], [[04 - Surrogate Key and Natural Key]], [[07 - Designing Many-to-Many Relationships]]
