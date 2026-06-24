# Lookup Table

A lookup table (also called a reference table or dimension table) is a small, dedicated table that stores a fixed set of valid values for a particular attribute. Instead of repeating the same descriptive text across thousands of rows in a main table, the main table stores a foreign key that references the lookup table. This pattern improves data consistency, reduces storage waste, and makes the database easier to maintain.

## What Is a Lookup Table?

A lookup table contains a predefined list of options or categories. Each option is stored once with a unique identifier (typically a primary key), and other tables reference this identifier rather than duplicating the descriptive text. The lookup table is the "one" side of a one-to-many relationship, and the main table that references it is the "many" side.

The primary purpose of a lookup table is to centralize the storage of values that have a fixed or limited number of options. Rather than allowing free-text entry that might contain typos, inconsistencies, or invalid values, the lookup table constrains the possible values to a known, controlled set. This is a form of data integrity enforcement.

## When to Use Lookup Tables

Lookup tables are appropriate whenever an attribute has a limited, known set of valid values. Common scenarios include:

- **Membership levels**: Bronze, Silver, Gold, Platinum
- **Status codes**: Active, Inactive, Pending, Suspended
- **Categories**: Product categories, issue categories, request types
- **Geographic data**: States, provinces, countries
- **Enum-like values**: Priority levels (Low, Medium, High), user roles (Admin, Editor, Viewer)

Any time you find yourself repeating the same string values across many rows in a table, and those values come from a fixed set of options, a lookup table is likely the right design choice.

## Example: Membership Status

Consider a membership database where each member has a membership tier. Without a lookup table, the membership tier is stored directly in the members table:

**Without a lookup table (problematic):**

```
members
+-----------+--------+-----------+---------+
| member_id | name   | tier      | price   |
+-----------+--------+-----------+---------+
| 1         | Caleb  | Gold      | 60.00   |
| 2         | Jimmy  | Gold      | 60.00   |
| 3         | Jake   | Silver    | 30.00   |
| 4         | Sally  | Gold      | 60.00   |
| 5         | Sammy  | Platinum  | 100.00  |
+-----------+--------+-----------+---------+
```

In this design, "Gold" and "60.00" are repeated for every Gold member. If the price of Gold changes from $60 to $75, you must update every single Gold member's row. If someone types "gold" instead of "Gold" or "Gld" instead of "Gold", you now have inconsistent data that queries may miss.

**With a lookup table (correct):**

```sql
CREATE TABLE membership_tiers (
    tier_id INT PRIMARY KEY,
    tier_name VARCHAR(50) NOT NULL,
    monthly_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE members (
    member_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    tier_id INT NOT NULL,
    FOREIGN KEY (tier_id) REFERENCES membership_tiers(tier_id)
);
```

```
membership_tiers
+---------+-----------+---------------+
| tier_id | tier_name | monthly_price |
+---------+-----------+---------------+
| 1       | Bronze    | 10.00         |
| 2       | Silver    | 30.00         |
| 3       | Gold      | 60.00         |
| 4       | Platinum  | 100.00        |
+---------+-----------+---------------+

members
+-----------+------------+-----------+---------+
| member_id | first_name | last_name | tier_id |
+-----------+------------+-----------+---------+
| 1         | Caleb      | Smith     | 3       |
| 2         | Jimmy      | Jones     | 3       |
| 3         | Jake       | Brown     | 2       |
| 4         | Sally      | Davis     | 3       |
| 5         | Sammy      | Wilson    | 4       |
+-----------+------------+-----------+---------+
```

Now the tier information is stored once in the `membership_tiers` table. Changing the price of Gold from $60 to $75 requires updating a single row. The `tier_id` foreign key in the members table ensures that only valid tiers can be assigned, preventing typos and invalid entries.

## Benefits of Lookup Tables

**Data consistency.** By constraining values to a fixed set, lookup tables prevent typos, abbreviations, and other inconsistencies. "Gold", "gold", "GOLD", and "Gld" are all different strings, but a lookup table forces everyone to use the same identifier.

**Reduced maintenance.** When a value needs to change (renaming "Gold" to "Epic", updating the price of a tier), you update a single row in the lookup table instead of thousands of rows in the main table. The foreign key references remain valid because the primary key (the ID) does not change.

**Data integrity.** Foreign key constraints ensure that only valid values can be entered. You cannot assign a member to a tier that does not exist in the lookup table. You can also configure constraints to prevent deletion of a tier that is still in use.

**Added complexity.** Lookup tables allow you to store additional attributes about each option. In the membership example, you can add columns for price, duration, perks, and any other tier-specific information. These attributes would be impractical to store in the members table because they would be repeated for every member with the same tier.

**Storage efficiency.** Storing a small integer foreign key (like tier_id = 3) instead of a string (like "Platinum") saves space, especially when the value is repeated across thousands or millions of rows. The descriptive text is stored once in the lookup table.

## Foreign Key Constraints and Lookup Tables

The foreign key relationship between the main table and the lookup table is what enforces data integrity. The database guarantees that every `tier_id` in the members table corresponds to a valid row in the membership_tiers table. You can configure the foreign key constraint to:

- **Reject invalid inserts**: Prevent inserting a member with a tier_id that does not exist in the lookup table.
- **Restrict deletions**: Prevent deleting a tier that is still referenced by members.
- **Cascade updates**: If a tier's primary key changes (which should be rare), automatically update all foreign key references.
- **Set null on delete**: If a tier is deleted, set the tier_id in referencing members to NULL (if allowed).

```sql
CREATE TABLE members (
    member_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    tier_id INT,
    FOREIGN KEY (tier_id) REFERENCES membership_tiers(tier_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

## See Also

- [[08 - Data Integrity]] - How constraints protect the correctness of data
- [[01 - Introduction to Keys]] - The role of keys in establishing relationships
- [[06 - Designing One-to-Many Relationships]] - The relationship pattern used by lookup tables
