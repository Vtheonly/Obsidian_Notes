# Review and Key Points

This section consolidates all the key types and key-related concepts covered in the preceding lessons into a single reference. Understanding the relationships between these concepts is essential for making informed design decisions when building a relational database schema. Rather than treating each key type in isolation, this review emphasizes how they relate to each other and which ones matter most in practice.

## Key Types by Function

### Superkey

A superkey is any set of columns (one or more) that guarantees uniqueness for every row in a table. A superkey may contain more columns than necessary to enforce uniqueness. For example, in a `users` table, the combination of `(user_id, username, email)` is a superkey because no two rows can share all three values simultaneously. However, this superkey includes redundant columns -- `user_id` alone would suffice. Identifying superkeys is a theoretical exercise that helps narrow down the search for the most efficient key.

### Candidate Key

A candidate key is a minimal superkey: it uses the fewest possible columns to guarantee uniqueness. Any superkey from which you cannot remove a column without losing uniqueness is a candidate key. A table can have multiple candidate keys. For example, both `user_id` and `username` might each be candidate keys in a `users` table, because each one independently guarantees uniqueness.

### Primary Key

The primary key is the candidate key you select as the main identifier for the table. Each table has exactly one primary key, which the database uses as the default clustering mechanism and the target for foreign key references. The primary key must be unique and not null for every row.

### Alternate Key

An alternate key is any candidate key that was not chosen as the primary key. Alternate keys still enforce uniqueness (typically via a `UNIQUE` constraint) and can be used for efficient lookups, but they are not used as the primary reference target for foreign keys from other tables.

## Key Types by Composition

### Surrogate Key vs. Natural Key

| Property | Surrogate Key | Natural Key |
|---|---|---|
| Source | Artificially generated | Derived from existing data |
| Meaning | No real-world meaning | Carries business meaning |
| Stability | Never changes | May change if business rules change |
| Typical form | Single integer column | One or more business columns |
| Example | `user_id = 7462` | `username = 'jsmith'` |

See [[04 - Surrogate Key and Natural Key]] for the full comparison.

### Simple Key vs. Composite Key vs. Compound Key

| Key Type | Columns | Each Column a Key? | Example |
|---|---|---|---|
| Simple | 1 | N/A | `user_id` |
| Composite | 2+ | At least one is not a key | `(user_id, video_id, timestamp)` |
| Compound | 2+ | All are keys | `(student_id, class_id)` |

See [[09 - Simple, Composite, and Compound Key]] for detailed definitions.

## Foreign Keys and Constraints

A foreign key references a primary key in another (or the same) table, establishing a relationship between the two. Foreign keys can be nullable (optional relationship) or `NOT NULL` (mandatory relationship). Foreign key constraints (`ON DELETE` and `ON UPDATE`) define what happens to child rows when the parent is modified.

| Constraint | Effect on Child Rows |
|---|---|
| `RESTRICT` / `NO ACTION` | Reject the parent operation if children exist |
| `CASCADE` | Apply the same operation to children |
| `SET NULL` | Set the foreign key to `NULL` in children |
| `SET DEFAULT` | Set the foreign key to its default value |

See [[06 - Foreign Key]], [[07 - NOT NULL Foreign Key]], and [[08 - Foreign Key Constraints]] for full details.

## Priority of Key Concepts

Not all key concepts carry equal practical weight. The two most important key types for day-to-day database design are the **primary key** and the **foreign key**. Every table must have a primary key, and most tables will have at least one foreign key. Superkeys and candidate keys are useful during the analysis phase but rarely appear in implementation. Alternate keys are important for enforcing additional uniqueness constraints beyond the primary key.

The design-level classifications (surrogate vs. natural, simple vs. composite vs. compound) are not declared in SQL but inform your schema decisions. The most impactful choice you make is whether to use surrogate or natural keys consistently across your database. Once that decision is made, the structure of individual keys (simple or multi-column) follows naturally from the data model and the relationships you need to represent.

## Complete Key Type Summary

| Key Type | Category | Defined in SQL? | Purpose |
|---|---|---|---|
| Superkey | Functional | No | Theoretical: any unique column set |
| Candidate key | Functional | No | Minimal unique column set |
| Primary key | Functional | Yes (`PRIMARY KEY`) | Main row identifier |
| Alternate key | Functional | Yes (`UNIQUE`) | Additional uniqueness enforcement |
| Foreign key | Functional | Yes (`FOREIGN KEY`) | Cross-table reference |
| Surrogate key | Design | No | Artificial, meaningless identifier |
| Natural key | Design | No | Business-meaningful identifier |
| Simple key | Composition | No | Single-column key |
| Composite key | Composition | No | Multi-column key (at least one non-key column) |
| Compound key | Composition | No | Multi-column key (all columns are keys) |

Cross-reference: [[01 - Introduction to Keys]], [[02 - Superkey and Candidate Key]], [[03 - Primary Key and Alternate Key]], [[04 - Surrogate Key and Natural Key]], [[06 - Foreign Key]], [[07 - NOT NULL Foreign Key]], [[08 - Foreign Key Constraints]], [[09 - Simple, Composite, and Compound Key]]
