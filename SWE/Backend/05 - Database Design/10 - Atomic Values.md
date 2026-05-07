# Atomic Values

## What Are Atomic Values

An atomic value is a value that represents one and only one thing. In database design, every value stored in a table cell should be atomic, meaning it cannot be meaningfully broken down into smaller components without losing its identity as a single unit of information. The concept of atomicity derives from the idea of an atom as the smallest indivisible unit: just as an atom was once considered the smallest possible piece of matter, an atomic value is the smallest meaningful piece of data that should be stored in a single field.

The principle of atomic values is a foundational requirement of First Normal Form (1NF), the most basic level of database normalization. A table that violates atomicity stores composite or multi-valued data in individual cells, which makes it difficult to query, update, and maintain the data consistently. By ensuring that every value in every cell is atomic, the database structure supports clean, predictable queries and prevents a wide range of data anomalies.

It is important to understand that atomicity is contextual, not absolute. A value is atomic if it is treated as a single unit within the context of the database. A phone number, for example, consists of an area code, an exchange, and a line number, but if the application always treats the phone number as a single unit, storing it in one column is appropriate. Atomicity is about how the data is used, not about whether it can theoretically be decomposed further.

## Why Atomic Values Matter

Atomic values matter because they directly affect the ability to query, update, and maintain data accurately and efficiently. When non-atomic values are stored in a single cell, the database cannot easily search for, sort by, or filter on the individual components of that value. This limitation leads to complex, error-prone query logic and increases the risk of data inconsistencies.

Consider a column that stores a person's full name as a single value, such as "Caleb Daniel Curry." If you need to find all users with the last name "Curry," you must search within the string, which is slower and less reliable than searching a dedicated `last_name` column. If you need to sort users by last name, the database cannot do so accurately because the last name is buried within a larger string. If a user changes their last name, you must perform string manipulation to update only part of the value, which is fragile and prone to errors.

Atomic values also prevent multi-valued attributes, where a single cell contains multiple distinct values. A column named `favorite_movies` that contains "The Matrix, Inception, Interstellar" is not atomic because it holds three separate values in one cell. Querying for users who like "Inception" requires string parsing, and adding or removing a movie requires complex update logic. The correct approach is to restructure the data so that each movie preference is stored as a separate row in a related table.

## Examples of Non-Atomic Values

### Names

Storing a person's full name in a single column is a common violation of atomicity. A full name typically consists of a first name, a middle name, and a last name. These are distinct pieces of information that may need to be queried or displayed independently. A greeting might use only the first name, a legal document might require the full name, and a directory listing might show "last name, first name" format.

**Before (non-atomic):**

| id | full_name |
|----|-----------|
| 1 | Caleb Daniel Curry |
| 2 | Mary Jane Watson |

**After (atomic):**

| id | first_name | middle_name | last_name |
|----|-----------|-------------|-----------|
| 1 | Caleb | Daniel | Curry |
| 2 | Mary | Jane | Watson |

### Addresses

An address is a composite value that consists of multiple distinct components: street address, city, state, and zip code. Storing the entire address in a single column prevents you from querying by city, filtering by state, or sorting by zip code. Decomposing the address into separate columns enables all of these operations.

**Before (non-atomic):**

| id | address |
|----|---------|
| 1 | 123 Epic Lane, Legit, CA 73821 |

**After (atomic):**

| id | street_address | city | state | zip_code |
|----|---------------|------|-------|----------|
| 1 | 123 Epic Lane | Legit | CA | 73821 |

With the atomic structure, you can easily query for all users in California (`WHERE state = 'CA'`) or all users in a specific city, operations that would require complex string parsing with the non-atomic version.

### Phone Numbers

Phone numbers present an interesting case for atomicity. A phone number consists of an area code, an exchange, and a line number. However, phone numbers are almost always treated as a single unit in applications: they are displayed, stored, and searched as complete numbers. For this reason, storing a phone number in a single column is generally acceptable, even though it can theoretically be decomposed.

If the application has a specific need to query by area code (for example, to identify all users in a particular region), then decomposing the phone number into `area_code` and `local_number` columns would be appropriate. The decision depends on how the data will be used, not on whether decomposition is theoretically possible.

### Multi-Valued Attributes

Storing multiple values in a single cell is a clear violation of atomicity. Common examples include comma-separated lists of tags, categories, phone numbers, or email addresses in a single column. This approach makes it impossible to query for individual values efficiently and creates problems when inserting, updating, or deleting individual items from the list.

**Before (non-atomic):**

| id | username | favorite_movies |
|----|----------|----------------|
| 1 | caleb_curry | The Matrix, Inception, Interstellar |
| 2 | billy_joe | Titanic, Avatar |

**After (atomic):**

`users` table:

| id | username |
|----|----------|
| 1 | caleb_curry |
| 2 | billy_joe |

`favorite_movies` table:

| user_id | movie |
|---------|-------|
| 1 | The Matrix |
| 1 | Inception |
| 1 | Interstellar |
| 2 | Titanic |
| 2 | Avatar |

In the atomic structure, each favorite movie is stored as a separate row in a related table. This allows you to query for all users who like "Inception" with a simple `WHERE movie = 'Inception'`, add new movies without string manipulation, and remove movies without parsing the entire list.

## How to Decompose Non-Atomic Values

The process of decomposing non-atomic values involves identifying the individual components of a composite value and creating separate columns (or separate tables) for each component. The decomposition should continue until each column contains values that are treated as single units by the application. The key question to ask is: "Will I ever need to query, sort, filter, or display this component independently?" If the answer is yes, the component should be stored in its own column.

For simple decompositions, such as splitting a full name into first, middle, and last name, the components are stored as separate columns in the same table. For multi-valued attributes, such as a list of favorite movies, the values are moved to a separate table with a foreign key relationship back to the original entity. This pattern of decomposition is fundamental to database normalization and is explored in greater depth in the context of normal forms.

## Avoiding Over-Decomposition

While atomicity is important, it is equally important not to decompose values beyond the point of usefulness. Breaking a word into individual letters, for example, would satisfy a strict interpretation of atomicity but would make the data practically unusable. A word like "subscribe" is a single unit of meaning and should be stored as one value, not as separate letters. Similarly, a date value like "2025-01-15" can theoretically be split into year, month, and day, but if the application always treats dates as complete units, storing them in a single `DATE` column is the correct approach.

The principle is to decompose only to the level that the application requires. If you will never need to query users by the second letter of their first name, do not create a column for it. If you will never need to filter orders by the month alone, do not split the order date into separate year, month, and day columns. Atomicity serves the practical needs of the application; it is not an end in itself.

## Next Steps

Atomic values are a prerequisite for understanding relationships between entities, which is the next major topic in database design. See [[11 - Relationships]] for an introduction to how entities connect to one another.
