# Introduction to Keys

Keys are one of the most fundamental concepts in relational database design. A key is a column or combination of columns that uniquely identifies each row in a table. Without keys, there would be no way to distinguish between rows, no mechanism for establishing relationships between tables, and no foundation for maintaining data integrity. Understanding keys is essential for designing databases that are correct, efficient, and maintainable.

## What Is a Key?

A key is a column or set of columns whose values uniquely identify every row in a table. No two rows in a table can have the same key value. This uniqueness constraint is what allows the database to locate, reference, and connect specific records. When you look up a user by their username, query an order by its order number, or join a comment to its author, you are relying on keys to make those associations precise and reliable.

Consider a user account table with columns for username, first name, last name, password, and email. Without a key, two users could potentially have the same first name and last name (like two people named "Caleb Curry"), making it impossible to determine whether they are the same person or different people. A key eliminates this ambiguity by guaranteeing that each row can be uniquely identified.

## Why Keys Matter

Keys serve several critical functions in a relational database:

**Uniqueness**: Keys ensure that no two rows in a table are identical. This prevents duplicate records and the confusion they cause. Without uniqueness, the database cannot reliably determine which row a query should return or update.

**Relationships**: Keys are the mechanism by which tables are connected. A foreign key in one table references a primary key in another table, establishing a relationship between the two. Without keys, there would be no way to link a comment to its author, an order to its customer, or an enrollment to its student.

**Data integrity**: Keys enforce constraints that protect the correctness of data. A primary key constraint prevents duplicate rows. A foreign key constraint prevents orphaned records that reference non-existent parents. These constraints are the backbone of referential integrity in a relational database.

**Performance**: Keys are indexed by the database, which dramatically speeds up queries that search for specific rows. Instead of scanning every row in a table (a full table scan), the database can use the key's index to locate the desired row directly.

## Three Rules of Keys

Every key in a relational database must satisfy three fundamental rules:

**1. Always unique.** No two rows in a table can have the same key value. This is the defining characteristic of a key. If a column allows duplicates (like first name or password), it cannot serve as a key on its own.

**2. Never changing.** The value of a key should never be updated after it is assigned. Keys are used to establish relationships between tables, and changing a key value requires updating every foreign key reference across the entire database. This is computationally expensive and error-prone. If a key needs to change, the integrity of all relationships that depend on it is at risk.

**3. Never null.** A key must always have a value. A row without a key is an orphan with no identity. If a row cannot be uniquely identified, it cannot be reliably referenced, updated, or deleted. Null keys break the uniqueness constraint because null values are not considered equal to each other, making it impossible to enforce uniqueness.

## Types of Keys

The concept of a key encompasses several specific categories, each with a distinct role in database design:

- **Superkey**: Any combination of columns that uniquely identifies every row in a table. A superkey may include more columns than necessary. The entire set of columns in a table is always a superkey, but it is usually not the most practical one.
- **Candidate key**: A minimal superkey. It is the smallest combination of columns that still guarantees uniqueness. Removing any column from a candidate key would make it non-unique. A table can have multiple candidate keys.
- **Primary key**: The candidate key that is chosen to be the main identifier for the table. There is exactly one primary key per table.
- **Alternate key**: Any candidate key that was not chosen as the primary key. Alternate keys can be indexed for performance but are not used for foreign key references.
- **Foreign key**: A column in one table that references the primary key of another table. Foreign keys establish relationships between tables.
- **Natural key**: A key that is derived from existing data in the table, such as a username or email address. It has real-world meaning.
- **Surrogate key**: An artificial key with no real-world meaning, typically an auto-incrementing integer. It is generated solely for the purpose of serving as a primary key.

These categories are not mutually exclusive. A primary key can be natural or surrogate. A foreign key references a primary key, which itself may be a candidate key, a superkey, or a surrogate key. Understanding the hierarchy and relationships between these key types is essential for advanced database design.

## Keys and Relationships

Keys are the connective tissue of a relational database. Every relationship between tables is established through keys. The primary key in the parent table is referenced by the foreign key in the child table, creating a link that the database can traverse to join related data. Without keys, tables would be isolated islands of data with no way to connect or cross-reference information.

When you design a database, you define keys first and then build relationships around them. The choice of which column or columns to use as the primary key affects every foreign key reference in the entire schema. Changing a primary key after the database is populated is extremely difficult and risky, which is why key selection is one of the most important early design decisions.

## See Also

- [[11 - Primary Key Index]] - How primary key indexes work to speed up queries
- [[02 - Superkey and Candidate Key]] - Detailed explanation of superkeys and candidate keys
- [[03 - Primary Key and Alternate Key]] - How to choose a primary key from candidate keys
- [[04 - Surrogate Key and Natural Key]] - The trade-offs between surrogate and natural keys
