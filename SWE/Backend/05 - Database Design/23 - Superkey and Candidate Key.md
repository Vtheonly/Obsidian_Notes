# Superkey and Candidate Key

Before selecting a primary key for a table, you must first identify all possible keys by analyzing the table's columns. This analysis proceeds in two stages: first, you identify **superkeys**, which are any combinations of columns that guarantee uniqueness; then, you narrow those down to **candidate keys**, which are the minimal superkeys. This process ensures that you understand all the options available before making the final selection of a primary key.

## Superkey

A **superkey** is any combination of one or more columns that uniquely identifies every row in a table. The defining property of a superkey is that no two rows can have the same values for all columns in the superkey. The term "super" indicates that the key may contain more columns than necessary; it is a superset of uniqueness.

The most trivial superkey is the entire set of columns in the table. Since every row is unique (by definition, in a well-designed table), the combination of all columns always forms a superkey. However, this is rarely useful in practice because it includes redundant columns that do not contribute to uniqueness.

### Finding Superkeys: Step-by-Step Example

Consider a `users` table with the following columns:

| Column | Description |
|--------|-------------|
| username | User-chosen handle, must be unique |
| email | Email address, must be unique |
| password | Hashed password, may be shared |
| first_name | Given name, not unique |
| middle_name | Middle name or initial, may be null |
| last_name | Family name, not unique |
| birth_date | Date of birth, not unique |

To determine whether a set of columns is a superkey, ask: "Can two different rows ever have the same values for all columns in this set?" If the answer is no, the set is a superkey.

**{username}** is a superkey. No two users can have the same username, so username alone guarantees uniqueness.

**{email}** is a superkey. No two users can have the same email address, so email alone guarantees uniqueness.

**{username, email}** is a superkey. Since username is already unique, adding more columns cannot break uniqueness. However, this superkey is redundant because username alone suffices.

**{username, password, first_name, last_name}** is a superkey. Again, username alone makes the entire combination unique, but the additional columns are unnecessary.

**{first_name, last_name}** is NOT a superkey. Two different people can share the same first and last name.

**{first_name, middle_name, last_name, birth_date}** is likely a superkey in practice, since the probability of two people having the same full name and birth date is extremely low. However, it is not guaranteed to be unique in all cases (twins with the same name born on the same day), so it is a superkey only if the application's business rules enforce uniqueness on this combination.

## Candidate Key

A **candidate key** is a minimal superkey. It is a superkey from which no column can be removed without losing the uniqueness property. Every column in a candidate key is necessary; removing any column would allow duplicate rows. The term "candidate" reflects the fact that each candidate key is a potential choice for the table's primary key.

To test whether a superkey is a candidate key, try removing each column one at a time. If the resulting set is still a superkey, the original set was not minimal and therefore not a candidate key. If removing any column breaks uniqueness, the set is minimal and is a candidate key.

### Finding Candidate Keys: Step-by-Step

Starting from the superkeys identified above:

**{username}**: Remove username, and you have an empty set, which is not a superkey. Therefore, {username} is minimal. It is a candidate key.

**{email}**: Remove email, and you have an empty set, which is not a superkey. Therefore, {email} is minimal. It is a candidate key.

**{username, email}**: Remove email, and {username} is still a superkey. Therefore, {username, email} is NOT minimal. It is a superkey but not a candidate key.

**{first_name, middle_name, last_name, birth_date}**: If the business rules enforce uniqueness on this combination, try removing each column. Remove birth_date, and the combination {first_name, middle_name, last_name} is no longer unique (different people can share the same full name). Remove middle_name, and {first_name, last_name, birth_date} might still allow duplicates. Remove last_name, and the combination breaks. Since every column is necessary for uniqueness, this would be a candidate key if the business rules guarantee its uniqueness.

So for this table, the candidate keys are:

1. {username}
2. {email}
3. Possibly {first_name, middle_name, last_name, birth_date} (if uniqueness is enforced)

## The Design Process

The process of key identification follows a clear sequence:

1. **Can every row be unique?** First, verify that it is possible for every row in the table to be unique. If the table's structure allows duplicate rows, you need to add a column (such as an auto-incrementing ID) to enforce uniqueness. If every row can be unique, you have at least one superkey.

2. **How many columns are needed?** Determine the minimal combinations of columns that guarantee uniqueness. These are your candidate keys.

3. **How many candidate keys exist?** List all candidate keys. A table can have one or many candidate keys. Each candidate key is a viable option for the primary key.

4. **Which candidate key should be the primary key?** Select one candidate key as the primary key based on practical considerations such as simplicity, stability, and performance. The remaining candidate keys become alternate keys.

## Practical Considerations

Superkeys are primarily a design-time concept. You do not typically define superkeys in the database schema because they are too broad to be useful for indexing or constraint enforcement. Instead, superkeys serve as a starting point for identifying candidate keys.

Candidate keys, on the other hand, have direct practical implications. Each candidate key represents a natural way to uniquely identify rows, and you should consider indexing them for query performance even if they are not chosen as the primary key. The candidate key you select as the primary key will be used for all foreign key references, so choose wisely.

## Summary Table

| Concept | Definition | Example | Minimal? |
|---------|-----------|---------|----------|
| Superkey | Any combination of columns that guarantees uniqueness | {username, email, password} | No (usually not) |
| Candidate key | A minimal superkey | {username} | Yes |

## See Also

- [[20 - Introduction to Keys]] - Overview of keys and their role in database design
- [[24 - Primary Key and Alternate Key]] - How to select a primary key from candidate keys
- [[25 - Surrogate Key and Natural Key]] - The trade-offs between surrogate and natural keys
