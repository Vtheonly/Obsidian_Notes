# Designing One-to-Many Relationships

Designing a one-to-many relationship in a relational database requires placing a foreign key on the "many" side that references the primary key on the "one" side. This is a straightforward but critical rule: the foreign key always goes in the child table, never in the parent table. Understanding why this rule exists and how to apply it correctly is essential for building schemas that avoid data anomalies and wasted space.

## Foreign Key Placement

The fundamental design rule for one-to-many relationships is that the foreign key is placed on the "many" side of the relationship. This is not an arbitrary convention but a logical necessity. The "one" side has a single record that can be referenced by many other records. A single column in the parent table can only hold one value, so it cannot store references to multiple children. The "many" side, however, can easily hold a single reference back to its one parent.

Consider a user who posts multiple reviews on a shopping website. The user is on the "one" side, and the reviews are on the "many" side. Placing the foreign key in the reviews table (pointing back to the user) allows each review to identify its author. Multiple reviews can share the same user_id, correctly representing that one user wrote many reviews.

**Incorrect approach (foreign key on the wrong side):**

```
users
+---------+----------+-----------+-----------+
| user_id | username | review_id | review_id2|
+---------+----------+-----------+-----------+
```

This fails because you would need an unbounded number of review_id columns to accommodate users who write many reviews. Users with few reviews would have many NULL columns, wasting space.

**Correct approach (foreign key on the many side):**

```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE reviews (
    review_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    review_title VARCHAR(200) NOT NULL,
    review_content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

In this design, each review has a `user_id` column that points back to the user who wrote it. A user can have many reviews, each with its own row in the reviews table pointing to the same `user_id`.

## Parent and Child Tables

In a one-to-many relationship, the table on the "one" side is the **parent table** and the table on the "many" side is the **child table**. The child always contains the foreign key that references the parent's primary key. This parent-child terminology reflects the dependency: a child record cannot exist without its parent. A review without a user makes no sense, just as a comment without an author has no context.

The parent table is independent; it does not need to know about its children. The child table, however, must always point back to its parent. You can identify the parent of any child record by following the foreign key, but you cannot easily find all children of a given parent without querying the child table. This is analogous to seeing a baby and knowing it must have parents, versus seeing an adult and not knowing whether they have children.

## Example: User and Reviews

```
users
+---------+----------+----------------+
| user_id | username | email          |
+---------+----------+----------------+
| 62      | alice    | alice@a.com    |
| 63      | bob      | bob@b.com      |
+---------+----------+----------------+

reviews
+-----------+---------+-------------------+-------------------------+
| review_id | user_id | review_title      | review_content          |
+-----------+---------+-------------------+-------------------------+
| 6         | 62      | Awesome product   | This is really great... |
| 7         | 62      | Great value       | Worth every penny...    |
| 8         | 63      | Decent            | It does the job...      |
+-----------+---------+-------------------+-------------------------+
```

User 62 (alice) has two reviews, while user 63 (bob) has one. Each review points back to exactly one user through the `user_id` foreign key. This structure is efficient, normalized, and free of redundant data.

## Example: Credit Card Company

Consider a credit card company where one user can have many cards, but each card belongs to exactly one user. This is a one-to-many relationship:

```sql
CREATE TABLE cardholders (
    holder_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE cards (
    card_id INT PRIMARY KEY,
    holder_id INT NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    issue_date DATE,
    max_amount DECIMAL(10,2),
    FOREIGN KEY (holder_id) REFERENCES cardholders(holder_id)
);
```

The `holder_id` foreign key in the cards table links each card to its owner. A single cardholder can have multiple cards, each represented by a separate row with the same `holder_id` value. Without the foreign key, there would be no way to determine which cards belong to which cardholders.

## Key Design Rules

- Always place the foreign key on the "many" side of the relationship.
- The "one" side is the parent table; the "many" side is the child table.
- The child always references the parent, never the other way around.
- Multiple child rows can reference the same parent row.
- Each child row references exactly one parent row.
- Without a foreign key, there is no connection between the two tables.

## See Also

- [[13 - One-to-Many Relationships]] - Conceptual overview of one-to-many relationships
- [[17 - Parent Tables and Child Tables]] - Detailed explanation of parent-child relationships
- [[14 - Many-to-Many Relationships]] - Contrast with the many-to-many pattern
