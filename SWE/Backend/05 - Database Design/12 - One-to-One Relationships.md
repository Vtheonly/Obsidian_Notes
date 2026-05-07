# One-to-One Relationships

## Definition of a One-to-One Relationship

A one-to-one relationship exists when a single instance of one entity is associated with exactly one instance of another entity, and each instance of the second entity is associated with exactly one instance of the first. In other words, both sides of the relationship have a cardinality of one. For every row in the first table, there is at most one corresponding row in the second table, and vice versa. This type of relationship is the least common of the three relationship types in database design, but it serves important purposes in specific scenarios.

The defining characteristic of a one-to-one relationship is mutual exclusivity on both sides. Neither entity can have multiple associations with the other entity. If either side can have more than one connection, the relationship is not one-to-one. This constraint makes one-to-one relationships easy to identify once you understand what to look for, but they can be subtle in practice because the distinction between one-to-one and one-to-many often depends on business rules rather than inherent properties of the data.

## Examples of One-to-One Relationships

### Person and Social Security Number

In the United States, a social security number (SSN) is a unique identifier assigned to each citizen. The relationship between a person and their SSN is one-to-one: each person has exactly one SSN, and each SSN is assigned to exactly one person. Although rare cases of duplicate SSN assignment have occurred due to administrative errors, the intended design is strictly one-to-one, and the database should reflect this intended relationship.

If you were modeling this in a database, you might have a `persons` table and a `social_security_numbers` table (or simply store the SSN as a column in the `persons` table, since the relationship is one-to-one). The key point is that neither a person can have multiple SSNs nor can an SSN belong to multiple persons, under the rules of the system.

### User and User Profile

In many web applications, a user account has exactly one profile, and each profile belongs to exactly one user account. The `users` table stores authentication data (username, password, email), while the `user_profiles` table stores biographical data (bio, avatar URL, location). The relationship is one-to-one because a user cannot have multiple profiles, and a profile cannot belong to multiple users. This separation is often done for performance reasons (keeping the authentication table small for fast logins) or for security reasons (restricting access to sensitive profile data independently from account data).

### Employee and Parking Space

In a company where each employee is assigned exactly one parking space and each parking space is assigned to exactly one employee, the relationship between employees and parking spaces is one-to-one. An employee cannot have multiple spaces, and a space cannot be shared by multiple employees (under the company's assignment rules).

## When to Use Separate Tables vs. Combined Tables

One of the most practical questions in database design is whether to model a one-to-one relationship using two separate tables or to combine the data into a single table. The answer depends on several factors, including performance, security, maintainability, and the logical independence of the two entities.

### Reasons to Use Separate Tables

**Performance optimization:** If one side of the relationship contains large or infrequently accessed data, separating it into its own table can improve query performance. For example, if the `user_profiles` table contains a large `bio` text column that is rarely needed, keeping it separate from the `users` table means that queries that only need authentication data do not have to scan past the bio data. This is especially important when the large column is a TEXT or BLOB type that can significantly increase row size.

**Security and access control:** Different parts of a one-to-one relationship may require different access permissions. Authentication data in a `users` table should be tightly restricted, while profile data in a `user_profiles` table might be more broadly accessible. Separating the data into different tables allows you to apply different security policies to each table, and to create views that expose only the appropriate data to each user role.

**Logical independence:** If the two entities have different lifecycles or are managed by different parts of the application, separating them into different tables reflects this independence. A user might create an account before completing their profile, meaning the `users` row exists before the `user_profiles` row. If all data were in a single table, the profile columns would be null until the user completes their profile, which is less clean than having a separate table that simply has no row yet.

**Extensibility:** If one side of the relationship is likely to grow in complexity over time (adding more columns or requiring its own relationships to other tables), starting with a separate table makes future modifications easier and less disruptive.

### Reasons to Combine Into a Single Table

**Simplicity:** If both sides of the relationship always exist together, always have the same lifecycle, and do not have significantly different access patterns, combining them into a single table reduces schema complexity and eliminates the need for a join when retrieving the data. Fewer tables mean fewer foreign keys, fewer joins, and simpler queries.

**Always-together access pattern:** If every query that retrieves data from one side also needs data from the other side, the overhead of maintaining two tables and joining them on every access is not justified. A single table is simpler and potentially faster.

### Design Decision Framework

| Factor | Separate Tables | Single Table |
|--------|----------------|-------------|
| Large columns on one side | Preferred | Avoid |
| Different access permissions | Preferred | Avoid |
| Different lifecycles | Preferred | Acceptable |
| Always accessed together | Acceptable | Preferred |
| Schema simplicity priority | Acceptable | Preferred |

## Table Design Examples

### Option 1: Separate Tables with Foreign Key

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY,
    bio TEXT,
    avatar_url VARCHAR(255),
    location VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

In this design, the `user_profiles` table has a `user_id` column that serves as both the primary key and a foreign key referencing the `users` table. Because `user_id` is the primary key of `user_profiles`, it is inherently unique, which enforces the one-to-one constraint: each user can have at most one profile row.

### Option 2: Combined Single Table

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100),
    email VARCHAR(100),
    bio TEXT,
    avatar_url VARCHAR(255),
    location VARCHAR(100)
);
```

In this design, all data is stored in a single `users` table. The profile columns (`bio`, `avatar_url`, `location`) are nullable, so they can be null until the user completes their profile. This approach is simpler but less flexible if you later need to apply different access controls or if the profile data becomes large.

## Relationship to Other Relationship Types

One-to-one relationships are the simplest of the three relationship types, but they share the same underlying principles as one-to-many and many-to-many relationships. All three types define how entities are connected and determine how foreign keys and junction tables should be structured in the database schema. Understanding one-to-one relationships provides the foundation for understanding the more complex relationship types.

For comparison with other relationship types, see [[11 - Relationships]]. For one-to-many relationships, see the subsequent section on one-to-many relationships. For many-to-many relationships, see the subsequent section on many-to-many relationships.
