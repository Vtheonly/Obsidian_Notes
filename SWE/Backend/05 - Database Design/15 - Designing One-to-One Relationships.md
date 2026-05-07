# Designing One-to-One Relationships

Designing one-to-one relationships in a relational database involves deciding whether the relationship should be stored as a simple column within a single table or split across two tables with a foreign key connection. The choice depends on whether the related data is a simple attribute of the entity or whether it has its own distinct attributes that warrant a separate table. Understanding when to combine and when to separate is a fundamental design skill.

## One-to-One as a Column

The most common and practical way to store a one-to-one relationship is as a column within the same table. When one attribute is exclusively associated with a single entity and has no additional attributes of its own, it makes sense to store it directly in the entity's table. This avoids the overhead of an additional table and foreign key while maintaining the one-to-one nature of the relationship.

For example, consider the relationship between a user account and a username. Each user has exactly one username, and each username belongs to exactly one user. The username is an attribute of the user, not a separate entity with its own properties. Storing it as a column is the natural and correct approach.

```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL
);
```

In this design, the `username` column is unique and not null, enforcing the one-to-one constraint. No two users can share the same username, and every user must have one. This is clean, efficient, and requires no additional tables.

## When to Split Across Tables

There are situations where a one-to-one relationship should be stored across two separate tables. The primary reason to split is when the related data has its own distinct attributes that are not dependent on the main entity. If the related data has additional columns that describe it rather than the parent entity, storing everything in one table violates the principle that a table should describe one entity.

Consider a credit card company database. A cardholder can have one credit card, and a credit card can be owned by one cardholder. This is a one-to-one relationship. If the only information stored about the card is the card number, it can remain as a column in the cardholder table. However, if you also need to store the card's issue date, maximum amount, late fee, and expiration date, these attributes describe the card, not the cardholder. Storing them all in one table creates a design that mixes two entities.

**Storing everything in one table (problematic):**

| holder_id | first_name | last_name | card_number | max_amount | issue_date | late_fee |
|-----------|------------|-----------|-------------|------------|------------|----------|
| 1         | Alice      | Smith     | 4111...     | 5000.00    | 2023-01-15 | 25.00    |

This table is now about two things: the cardholder and the card. The `max_amount`, `issue_date`, and `late_fee` columns are attributes of the card, not the cardholder. This violates the rule that a table should focus on one entity and a row should describe one entity.

**Splitting across two tables (correct):**

```sql
CREATE TABLE cardholders (
    holder_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE cards (
    card_id INT PRIMARY KEY,
    holder_id INT UNIQUE NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    max_amount DECIMAL(10,2),
    issue_date DATE,
    late_fee DECIMAL(5,2),
    FOREIGN KEY (holder_id) REFERENCES cardholders(holder_id)
);
```

The `UNIQUE` constraint on `holder_id` in the cards table enforces the one-to-one relationship: each cardholder can have at most one card. Without this constraint, the same holder_id could appear multiple times, turning it into a one-to-many relationship instead.

## Methods for Implementing One-to-One Across Tables

There are two primary methods for implementing a one-to-one relationship across two tables:

**Method 1: Unique foreign key on the dependent side.** Place the foreign key in one table and add a `UNIQUE` constraint to it. This is the most common approach. The table that holds the foreign key is the dependent or child table, and the `UNIQUE` constraint ensures that each parent record is referenced at most once.

**Method 2: Shared primary key.** The dependent table uses the same primary key value as the parent table. The primary key of the dependent table also serves as a foreign key referencing the parent. This approach guarantees the one-to-one relationship inherently because primary keys are unique by definition.

```sql
-- Method 2: Shared primary key
CREATE TABLE cardholders (
    holder_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE cards (
    holder_id INT PRIMARY KEY,
    card_number VARCHAR(20) NOT NULL,
    max_amount DECIMAL(10,2),
    issue_date DATE,
    FOREIGN KEY (holder_id) REFERENCES cardholders(holder_id)
);
```

In this design, the `cards` table uses `holder_id` as both its primary key and its foreign key. No two cards can share the same `holder_id`, and every card must reference an existing cardholder.

## Decision Framework

When deciding whether to store a one-to-one relationship in one table or two, consider the following:

- If the related data is a simple attribute with no additional properties, store it as a column in the same table.
- If the related data has its own attributes that describe it rather than the parent entity, split it into a separate table.
- If separating the data improves security (for example, storing sensitive information like salaries in a separate table with restricted access), use two tables.
- If the related data is optional and most rows would have NULL values, consider splitting to avoid sparse tables.

## See Also

- [[12 - One-to-One Relationships]] - Conceptual overview of one-to-one relationships
- [[16 - Designing One-to-Many Relationships]] - Design patterns for one-to-many relationships
- [[7 - Data Integrity]] - How constraints enforce data correctness
