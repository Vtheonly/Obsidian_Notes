# NOT NULL Foreign Key

The `NOT NULL` constraint on a foreign key column determines whether the relationship between a child row and its parent is mandatory or optional. This distinction has significant implications for data integrity and business logic, because it controls whether a row can exist in the child table without referencing any row in the parent table. Understanding when to apply `NOT NULL` to a foreign key is essential for accurately modeling real-world requirements in your database schema. See [[06 - Foreign Key]] for the foundational concept of foreign keys.

## Mandatory vs. Optional Relationships

When a foreign key column is declared `NOT NULL`, every row in the child table must have a value that references a valid primary key in the parent table. This makes the relationship mandatory: no row can exist in the child table without being linked to a parent. When a foreign key column is nullable (the default), rows in the child table can exist without referencing any parent row, making the relationship optional.

The choice between mandatory and optional relationships depends entirely on the business rules governing the data. A foreign key should be `NOT NULL` only when the relationship it represents is truly required by the domain logic, not as a default assumption.

## When to Use NOT NULL on a Foreign Key

Use `NOT NULL` on a foreign key when the child entity cannot meaningfully exist without its parent. For example, consider a credit card database where every card must have a card holder. If the `card` table has a `holder_id` foreign key referencing the `card_holder` table, and the business rule states that only actively owned cards are stored, then `holder_id` should be `NOT NULL`.

```sql
CREATE TABLE card_holder (
    holder_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE card (
    card_id INT PRIMARY KEY,
    holder_id INT NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    FOREIGN KEY (holder_id) REFERENCES card_holder(holder_id)
);
```

With `NOT NULL` on `holder_id`, the database will reject any attempt to insert a card without specifying who holds it. This enforces the business rule at the database level and prevents orphaned or incomplete records from entering the system.

## When NOT to Use NOT NULL on a Foreign Key

Omit `NOT NULL` on a foreign key when the relationship is genuinely optional. For example, in a college database, a class may be created before an instructor has been assigned to it. Early in the semester, the registrar might need to add courses to the system without knowing which instructor will teach them. If `instructor_id` in the `class` table is `NOT NULL`, the database would prevent inserting a class without an instructor, which contradicts the operational workflow.

```sql
CREATE TABLE class (
    class_id INT PRIMARY KEY,
    instructor_id INT,          -- nullable: class may not have an instructor yet
    building_id INT NOT NULL,   -- mandatory: class must be assigned a building
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id),
    FOREIGN KEY (building_id) REFERENCES building(building_id)
);
```

In this design, `instructor_id` allows `NULL` values, so a class can exist in the table before an instructor is assigned. When an instructor is later assigned, the `instructor_id` can be updated from `NULL` to a valid reference. Meanwhile, `building_id` is `NOT NULL` because every class must have a physical location.

## Primary Keys vs. Foreign Keys and NOT NULL

An important distinction exists between primary keys and foreign keys regarding nullability. Primary keys are inherently `NOT NULL` -- this is a fundamental requirement of the relational model. A primary key must uniquely identify every row, and a null value cannot serve that purpose. Foreign keys, on the other hand, can legitimately be null when the relationship they represent is optional. This is one of the key differences between primary and foreign key behavior.

Additionally, while primary key values should never change, foreign key values can change when the relationship itself changes. For instance, if a user changes which car they own, the `car_id` foreign key in the `user` table would be updated to reference a different row in the `car` table. This is a valid operation because the reference changed, not the primary key of the car itself.

## Data Type Compatibility

The foreign key column and the primary key it references must share the same data type and related characteristics (such as character set or collation). The only characteristic that can differ between the two is `NOT NULL`. The parent column is always `NOT NULL` (because it is a primary key), but the child column may be either `NOT NULL` or nullable depending on whether the relationship is mandatory or optional.

| Property | Parent (Primary Key) | Child (Foreign Key) |
|---|---|---|
| Data type | Must match | Must match |
| NOT NULL | Always | Depends on relationship |
| Unique | Always | Not required |

Cross-reference: [[06 - Foreign Key]], [[08 - Foreign Key Constraints]], [[03 - Modality]]
