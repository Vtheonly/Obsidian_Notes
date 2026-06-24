# Naming Conventions

## Why Naming Conventions Matter

A naming convention is a consistent pattern used when naming database objects such as tables, columns, keys, and constraints. Naming conventions are not enforced by the database system itself, but they are a critical practice for maintaining clarity, consistency, and professionalism in database design. Without a naming convention, database schemas become difficult to read, understand, and maintain, especially as they grow in size and complexity or when multiple developers collaborate on the same project.

Consistent naming ensures that anyone reviewing the database schema can immediately understand the purpose and relationships of each object. When you encounter a column named `user_id`, you can reasonably infer that it references the `id` column in a `users` table. This predictability reduces the cognitive overhead required to work with the database and minimizes the risk of errors caused by misinterpreting object names. Naming conventions also facilitate communication between team members, as everyone uses the same vocabulary and structure when referring to database objects.

Different relational database management systems and organizations may adopt different naming conventions, and there is no single universally correct standard. The most important principle is to choose a convention and apply it consistently throughout the entire database. This section presents a widely used convention that works well with MySQL and other common RDBMS platforms.

## Lowercase for All User-Defined Names

All user-defined database object names, including table names and column names, should be written in lowercase. Using lowercase eliminates ambiguity and avoids problems related to case sensitivity, which varies across different RDBMS platforms. Some database systems are case-insensitive for identifiers, while others are case-sensitive, and mixing cases can lead to unexpected behavior when moving schemas between platforms.

For example, use `users` rather than `Users`, `USERS`, or `uSeRs`. Similarly, use `phone_number` rather than `PhoneNumber`, `PHONE_NUMBER`, or `phoneNumber`. The lowercase convention is simple, consistent, and compatible with every major RDBMS.

SQL keywords, by contrast, are typically written in uppercase to visually distinguish them from user-defined names. This convention makes SQL code more readable by creating a clear visual separation between language commands and database object names.

```
SELECT username, email FROM users WHERE id = 72;
```

In this example, the SQL keywords `SELECT`, `FROM`, and `WHERE` are in uppercase, while the user-defined names `username`, `email`, `users`, and `id` are in lowercase.

## Underscores Instead of Spaces

Spaces should never be used in table or column names. Spaces create problems in SQL queries because they require the name to be enclosed in quotes or brackets, which adds complexity and increases the risk of syntax errors. Instead of spaces, use underscores to separate words in a multi-word name.

| Bad Practice | Good Practice |
|-------------|--------------|
| `first name` | `first_name` |
| `phone number` | `phone_number` |
| `order date` | `order_date` |
| `zip code` | `zip_code` |

The underscore serves as a clean, universally supported word separator. It maintains readability without introducing the quoting complications that spaces require. Some developers use camelCase (`firstName`) or PascalCase (`FirstName`) as alternatives, but the underscore convention is the most widely adopted in the MySQL community and in relational database design generally.

## Table Naming Rules

Table names should be descriptive, concise, and written in lowercase with underscores separating words. A table name should clearly indicate the type of entity it represents. Use plural names for tables that represent collections of entities, as a table contains multiple rows, each representing one instance.

| Convention | Example |
|-----------|---------|
| Plural, lowercase, underscore-separated | `users`, `sales`, `order_items`, `product_categories` |

Avoid abbreviations unless they are universally understood. A table named `usr` is less clear than `users`, and `prod_cat` is less clear than `product_categories`. The goal is immediate comprehension; the few characters saved by abbreviating are not worth the loss of clarity.

Do not prefix table names with generic identifiers such as `tbl_` or `table_`. Such prefixes add noise without providing meaningful information. The fact that an object is a table is already evident from its context within the database schema.

## Column Naming Rules

Column names follow the same lowercase and underscore conventions as table names. Each column name should clearly describe the attribute it represents. Column names are typically singular because each column holds one value per row.

| Convention | Example |
|-----------|---------|
| Singular, lowercase, underscore-separated | `username`, `first_name`, `phone_number`, `email` |

Avoid generic or ambiguous column names such as `name`, `value`, `date`, or `description` when they appear in tables where context is unclear. Instead, use more specific names like `product_name`, `order_value`, `registration_date`, or `product_description`. Specific names prevent confusion when writing joins across multiple tables that might each have a `name` or `date` column.

## Foreign Key Naming Conventions

Foreign key columns should be named consistently with the primary key they reference, typically by combining the referenced table name (singular) with the referenced column name. This convention makes the relationship between tables immediately apparent from the column name alone.

If the `users` table has a primary key column named `id`, then a foreign key in the `sales` table that references this column should be named `user_id`. This naming pattern creates a clear, predictable link: when you see `user_id` in any table, you know it references the `id` column in the `users` table.

| Primary Key Table | Primary Key Column | Foreign Key Column (in another table) |
|---|---|---|
| `users` | `id` | `user_id` |
| `products` | `id` | `product_id` |
| `orders` | `id` | `order_id` |

This convention ensures that foreign key columns are named the same way across all tables that reference the same parent table, which makes joins and queries more intuitive to write and easier to review.

## Real-World vs. Database Names

When initially brainstorming what data to store, it is natural to use plain language with spaces and mixed capitalization. For example, you might write "user's address" or "phone number" on a whiteboard during a planning session. This is perfectly acceptable during the conceptual design phase. When you transition to the logical and physical design phases, convert these natural-language names into the database naming convention. "User's address" becomes `address` (or `street_address`, `city`, `state`, `zip_code` if decomposed), and "phone number" becomes `phone_number`.

## Summary of Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| SQL keywords | Uppercase | `SELECT`, `FROM`, `WHERE` |
| Table names | Lowercase, plural, underscore-separated | `users`, `order_items` |
| Column names | Lowercase, singular, underscore-separated | `username`, `first_name` |
| Foreign keys | Referenced table (singular) + underscore + referenced column | `user_id`, `product_id` |
| Word separator | Underscore, never spaces | `phone_number`, not `phone number` |

## Next Steps

With naming conventions established, the next step is to understand what database design itself entails and why it is a necessary process. See [[07 - What is Database Design]] for an explanation of the design process and its importance.
