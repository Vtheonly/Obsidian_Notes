# Primary Key and Alternate Key

After identifying all candidate keys for a table, the next step is to select one candidate key as the **primary key** and designate the remaining candidate keys as **alternate keys**. This selection has significant implications for how the table is indexed, how relationships are established, and how the database performs. Understanding the criteria for choosing a primary key and the role of alternate keys is essential for making informed design decisions.

## Selecting a Primary Key

A primary key is the candidate key that is chosen to serve as the main unique identifier for a table. It is the key that foreign keys in other tables will reference, and it receives a unique index from the database automatically. Selecting the right primary key from the available candidate keys requires evaluating each candidate against the three fundamental rules of keys: uniqueness, immutability, and non-nullability.

### Evaluation Criteria

Consider a `users` table with the following candidate keys:

1. **{username}** - A user-chosen handle, required at registration, must be unique
2. **{email}** - An email address, required at registration, must be unique
3. **{first_name, middle_name, last_name, birth_date, address}** - A combination of personal details

**Uniqueness**: All three candidate keys can be made unique through database constraints. Username and email are easy to enforce. The personal details combination is practically unique but theoretically possible to duplicate.

**Immutability (never changing)**: Username is typically stable; users rarely change their username. Email is somewhat stable but users do change their email addresses over time. Personal details can change frequently: people change their names (marriage, legal changes), move to new addresses, and in rare cases even adjust their recorded birth dates. The personal details combination is the least stable.

**Non-nullability (never null)**: Username and email are both required at account creation and can be enforced as NOT NULL. Personal details present problems: some people do not have middle names, and addresses can be temporarily unknown. This candidate key may contain null values, violating the rule.

Based on this analysis, **username** is the strongest candidate for the primary key. It is unique, rarely changes, and is always required. Email is a reasonable alternative but is more likely to change. The personal details combination is a poor choice due to mutability and nullability concerns.

```sql
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);
```

In this design, `username` is the primary key. It will be used for all foreign key references from other tables (comments, orders, messages, etc.). The `email` column has a UNIQUE constraint to enforce its uniqueness but is not the primary key.

## What Are Alternate Keys?

An alternate key is any candidate key that was not selected as the primary key. Alternate keys are still unique identifiers for the table, but they are not used for foreign key references from other tables. Their primary practical role is as indexed columns that improve query performance when searching by those attributes.

In the example above, `email` is an alternate key. It uniquely identifies each row, but it was not chosen as the primary key. However, many applications need to look up users by email (for example, during login or password reset), so indexing the email column is important.

## Indexing Alternate Keys

Although alternate keys are not used for foreign key references, they should often be indexed for performance. If your application frequently searches for users by email, the database needs an efficient way to locate rows by email value. Without an index, the database must perform a full table scan every time a user logs in with their email address.

```sql
-- Most databases create an index automatically when you add a UNIQUE constraint
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,  -- Automatically indexed
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);
```

The `UNIQUE` constraint on `email` automatically creates a unique index in most relational database management systems. This means queries like the following will be efficient:

```sql
SELECT * FROM users WHERE email = 'alice@example.com';
```

If the email column did not have a UNIQUE constraint or an explicit index, this query would require scanning every row in the table.

## Considerations for Choosing a Primary Key

When deciding which candidate key to designate as the primary key, consider the following practical factors:

**Simplicity.** A single-column key is preferable to a multi-column key. Single-column keys are easier to reference as foreign keys, easier to index, and easier to use in queries. A composite primary key made of five columns requires every foreign key reference in every child table to also include five columns, which is cumbersome and error-prone.

**Stability.** The primary key should rarely or never change. Changing a primary key value requires updating every foreign key reference across the entire database, which is expensive and risky. Keys derived from personal information (names, addresses, phone numbers) are prone to change and are generally poor primary keys.

**Size.** Smaller keys are more efficient for indexing and joining. An integer key (4 bytes) is more efficient than a string key like an email address (potentially 50+ bytes). When the primary key is referenced by millions of foreign keys across many tables, the size difference compounds significantly.

**Meaningfulness.** Some designers prefer keys with real-world meaning (natural keys), while others prefer meaningless generated keys (surrogate keys). Natural keys are intuitive but may change. Surrogate keys are stable but carry no information. This trade-off is explored in detail in [[04 - Surrogate Key and Natural Key]].

## Primary Key vs. Alternate Key Summary

| Property | Primary Key | Alternate Key |
|----------|-----------|---------------|
| Uniqueness | Enforced | Enforced |
| Number per table | Exactly one | Zero or more |
| Used for foreign key references | Yes | No |
| Automatically indexed | Yes | Usually (if UNIQUE constraint exists) |
| Selection | Chosen from candidate keys | Remaining candidate keys |
| Can be null | Never | Depends on constraint |

## See Also

- [[02 - Superkey and Candidate Key]] - How to identify superkeys and candidate keys
- [[04 - Surrogate Key and Natural Key]] - Trade-offs between surrogate and natural primary keys
- [[11 - Primary Key Index]] - How primary key indexes work
