# Keys, Data Types & Static Constraints (PostgreSQL)

Keys establish row identity and cross-table relationships, while data types and static constraints enforce domain and referential integrity declaratively at schema creation (`CREATE TABLE` / `ALTER TABLE`).

---

## 1. Taxonomy of Relational Keys

Every key in a relational table must obey **Three Fundamental Rules**:

1. **Always unique:** No two rows may share the same key value.
2. **Never changing (immutable):** Updating a primary key requires cascading changes across every referencing foreign key in the database—expensive and error-prone.
3. **Never null:** A null key leaves a row unidentifiable and breaks uniqueness checks (because `NULL`s are not equal to each other).

### Functional Hierarchy (Selection Pipeline)

1. **Superkey:** Any combination of 1+ columns that uniquely identifies every row (may include redundant columns; the entire column set of a valid table is always a superkey).
2. **Candidate Key:** A **minimal superkey**—removing any column destroys guaranteed uniqueness. A table may have several candidate keys.
3. **Primary Key (`PRIMARY KEY`):** The single candidate key selected as the official row identifier and target for foreign keys. Enforces `UNIQUE` + `NOT NULL` and automatically creates a unique B-tree index. Exactly **one** per table.
4. **Alternate Key:** Any candidate key _not_ chosen as the primary key. Should be given a `UNIQUE` constraint (creating a unique index for fast lookups, e.g., logging in by `email`).
5. **Foreign Key (`FOREIGN KEY`):** Column(s) in a child table referencing the primary key of a parent table. Unlike primary keys, foreign key values can repeat (many children per parent), can change when reassignment occurs, and can be `NULL` if optional.

#### Worked Superkey $\to$ Candidate Key $\to$ Primary Key Selection

Consider `users(username, email, password, first_name, middle_name, last_name, birth_date, address)`:

- **Superkeys:** `{username}` (unique), `{email}` (unique), `{username, email}` (redundant—not minimal!), `{username, password, first_name, last_name}` (redundant). `{first_name, last_name}` is **not** a superkey (duplicates exist).
- **Candidate Keys:** `{username}`, `{email}` (minimal!). `{first_name, middle_name, last_name, birth_date, address}` is risky (middle name can be NULL; address/name can change; twins could collide).
- **Primary Key Choice:** Choose `username` (stable, required, single-column) as `PRIMARY KEY`, and declare `email VARCHAR(100) UNIQUE NOT NULL` as an indexed **alternate key**.

### Design Choice: Natural Key vs. Surrogate Key

| Property               | Natural Key                                                                                                                                                                                                                                                                                            | Surrogate Key                                                                                                        |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Source**             | Existing business data (`username`, `email`, `ISBN`, `VIN`)                                                                                                                                                                                                                                            | Artificially generated (`user_id`, `GENERATED ALWAYS AS IDENTITY`, `UUID`)                                           |
| **Meaning**            | Carries real-world meaning (fewer joins needed to interpret IDs)                                                                                                                                                                                                                                       | Meaningless identifier                                                                                               |
| **Stability**          | Volatile if business rules/user details change (cascading FK updates!)                                                                                                                                                                                                                                 | Immutable (ID `42` never changes)                                                                                    |
| **Simplicity & Speed** | Often larger strings or multi-column composites                                                                                                                                                                                                                                                        | Single 4/8-byte integer; compact B-tree & fast joins (UUIDs avoid distributed conflicts & enumeration leaks in URLs) |
| **Consistency Rule**   | Pick **one** strategy consistently across the whole database. **Important caveat:** The moment a "surrogate" ID (e.g., printed Student Card ID) is given real-world meaning externally, it inherits natural-key change risks! Best practice: use surrogate PKs + `UNIQUE` constraints on natural keys. |

### Structural Composition: Simple, Composite & Compound Keys

This classification describes structure (not SQL keywords):

- **Simple Key:** 1 column (e.g., `user_id` or `username`).
- **Composite Key:** 2+ columns where **at least one** column is not a key by itself (e.g., `video_comments(user_id, video_id, comment_time)`—a user can comment multiple times on the same video, and `comment_time` is not a key alone).
- **Compound Key:** 2+ columns where **every** column is itself a key (usually an FK), such as `student_classes(student_id, class_id)` or `teacher_class(teacher_id, class_id)`.
  _(If an ORM requires a single-column PK on a junction table, add a surrogate `enrollment_id` PK and keep `UNIQUE(student_id, class_id)`.)_

### `NOT NULL` Foreign Keys & Lookup Tables

- **`NOT NULL` Foreign Key (Mandatory vs. Optional):** Apply `NOT NULL` only when business logic requires every child row to have a parent (e.g., `card.holder_id NOT NULL` when only owned cards are stored; **omit `NOT NULL`** on `class.instructor_id` or `student.class_id` when a class can be created before an instructor is assigned, or a student like Farah Ines is not yet enrolled in a class). Data types of parent PK and child FK must match; only nullability may differ.
- **Lookup (Reference) Tables:** Centralize fixed sets of options (e.g., `membership_tiers(tier_id, tier_name, monthly_price)` referenced by `members.tier_id`) rather than repeating `'Gold'` and `60.00` in every member row. Prevents typos (`'Gld'`, `'gold'`), simplifies price updates to 1 row, saves space, and eliminates 3NF transitive dependencies.

---

## 2. SQL Data Types (PostgreSQL Curriculum Standard)

Every column requires a data type for **domain integrity** (Ch 1 Slide 8 & TP 1/TP 2):

| Data Type                         | Storage / Description                                          | Example         | Usage in Course                                                                                         |
| :-------------------------------- | :------------------------------------------------------------- | :-------------- | :------------------------------------------------------------------------------------------------------ |
| `INTEGER` (`INT`)                 | 4-byte signed whole number ($\pm 2.14 \times 10^9$)            | `25, 100, -5`   | Primary/foreign keys, `student.age` (TP 1)                                                              |
| `SMALLINT`                        | 2-byte signed small integer ($-32{,}768$ to $32{,}767$)        | `10, 500`       | Small integers (`student.age`, Ch 1 Slide 6 & TP 1 Part P.4)                                            |
| `BIGINT`                          | 8-byte large integer                                           | `9000000000`    | High-volume identifiers                                                                                 |
| `VARCHAR(n)`                      | Variable-length character string (max $n$)                     | `'Ahmed'`       | Names, emails (`VARCHAR(50)`, `VARCHAR(100)`)                                                           |
| `CHAR(n)`                         | Fixed-length character string (space-padded to $n$)            | `'M'`, `'DZ'`   | Fixed-length codes (country codes, hashes)                                                              |
| `TEXT`                            | Variable-length unbounded text                                 | `'Dir -> Dean'` | Long articles, recursive path strings (`::TEXT`, TP 3)                                                  |
| `NUMERIC(p, s)` / `DECIMAL(p, s)` | Exact base-10 decimal ($p$ precision, $s$ scale)               | `75000.50`      | **Mandatory for salaries & currency** (`NUMERIC(10,2)`)—represents `0.1` without binary rounding error! |
| `REAL`                            | 4-byte single-precision floating point ($\approx 7$ digits)    | `12.45`         | Approximate scientific calculations (never money!)                                                      |
| `DOUBLE PRECISION`                | 8-byte double-precision floating point ($\approx 15$ digits)   | `1234.56789`    | Higher-precision approximate scientific math                                                            |
| `BOOLEAN`                         | True/False logic                                               | `TRUE`, `FALSE` | Procedural flags (`v_done BOOLEAN`)                                                                     |
| `DATE` / `TIME` / `TIMESTAMP`     | Calendar date / time / date+time (UTC-aware via `TIMESTAMPTZ`) | `'2026-11-12'`  | Audit logs (`DEFAULT CURRENT_TIMESTAMP`)                                                                |
| `BLOB` / `BYTEA`                  | Raw binary bytes (files, images)                               | —               | Media/binary objects (`BYTEA` in PostgreSQL, `BLOB` in MySQL)                                           |
| `NULL`                            | Absence of a value / unknown                                   | `NULL`          | Missing salary (`109`), missing `class_id` (`8`)                                                        |

_(Dialect note: MySQL adds `TINYINT` (1 byte), `UNSIGNED` integer modifiers that double the positive range e.g. `INT UNSIGNED` $0 \dots 4.29\times 10^9$, `AUTO_INCREMENT`, `DATETIME`, and `ON UPDATE CURRENT_TIMESTAMP`; PostgreSQL uses `GENERATED ALWAYS AS IDENTITY` or `SERIAL` instead of `AUTO_INCREMENT` and explicit `::TYPE` casts.)_

---

## 3. Static Integrity Constraints & Foreign Key Actions

| Constraint     | Role                | PostgreSQL & SQL Behavior                                                                                                                                                                                           |
| :------------- | :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `PRIMARY KEY`  | Entity uniqueness   | Implicitly `NOT NULL` + `UNIQUE` + unique B-tree index.                                                                                                                                                             |
| `NOT NULL`     | Mandatory attribute | Rejects `NULL` values (`department_name VARCHAR(50) NOT NULL`).                                                                                                                                                     |
| `UNIQUE`       | Prevents duplicates | Allows multiple `NULL`s unless combined with `NOT NULL`.                                                                                                                                                            |
| `CHECK (cond)` | Domain condition    | Rejects rows ONLY when `cond` is **`FALSE`**. Because `NULL >= 0` evaluates to **`UNKNOWN`** in Three-Valued Logic, `NULL` **passes** `CHECK` unless `NOT NULL` is also specified (critical for **TD 2 Ex 16\***!). |
| `DEFAULT val`  | Fallback value      | Used when `INSERT` omits the column (`salary NUMERIC(10,2) DEFAULT 30000`). Explicitly inserting `NULL` overrides `DEFAULT`.                                                                                        |
| `FOREIGN KEY`  | Referential link    | Value must exist in parent PK or be `NULL` (if nullable).                                                                                                                                                           |

### Foreign Key Referential Actions (`ON DELETE` / `ON UPDATE`) — TP 1 Part H

When a parent row is deleted or its PK is updated, the child table follows the declared referential action:

| Action                      | Effect on Child Rows                                            | Course Rationale (`university` DB, TP 1 Part H)                                                                                                                                                                                                                                                            |
| :-------------------------- | :-------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`ON DELETE CASCADE`**     | Child rows are automatically deleted                            | Used on `class.department_id` and `teacher_class` (`teacher_id`, `class_id`): if a class or teacher is deleted, junction rows lose meaning; furthermore, `teacher_class` columns are part of the `PRIMARY KEY`, so `SET NULL` is **impossible** (TP 1 H.8).                                                |
| **`ON DELETE SET NULL`**    | Child FK becomes `NULL`; child survives                         | Used on `teacher.department_id` and `student.class_id`: deleting a department (`DELETE FROM department WHERE department_id = 3`) must **not** erase teachers—they stay in `teacher` with `department_id = NULL` so they can be reassigned later. **Forbidden if the FK column is `NOT NULL`!** (TP 1 H.6). |
| **`ON DELETE RESTRICT`**    | Deletion refused immediately if child rows exist                | Protects parents with dependents; forces manual cleanup first.                                                                                                                                                                                                                                             |
| **`ON DELETE NO ACTION`**   | Default action; refuses if child rows still exist at check time | Same practical effect as `RESTRICT` for standard non-deferred FKs.                                                                                                                                                                                                                                         |
| **`ON UPDATE CASCADE`**     | Child FK automatically updates to new parent PK                 | `UPDATE department SET department_id = 100 WHERE department_id = 1;` updates all teachers & classes from `1` to `100` automatically, preventing orphan rows (TP 1 H.2 & H.7).                                                                                                                              |
| **`ON UPDATE SET NULL`**    | Child FK set to `NULL` when parent PK changes                   | Rare; disconnects children on parent renumbering.                                                                                                                                                                                                                                                          |
| **`ON UPDATE RESTRICT`**    | Parent PK update refused if child rows exist                    | Prevents renumbering `department_id = 1` while teachers/classes reference it (TP 1 H.5).                                                                                                                                                                                                                   |
| **`ON DELETE SET DEFAULT`** | Sets child FK to column `DEFAULT` value                         | Supported in SQL standard / PostgreSQL (provided default value exists in parent); MySQL treats as `RESTRICT`.                                                                                                                                                                                              |

---

## 4. Modifying Constraints with `ALTER TABLE` (TP 1 Part F)

**PostgreSQL does not support direct modification of an existing constraint.** To change a constraint, you must **drop the old constraint** and **add the new one** (for composite FKs, actions apply to the key tuple as a single unit):

```sql
-- 1. Add a named CHECK constraint
ALTER TABLE teacher ADD CONSTRAINT chk_teacher_salary CHECK (salary IS NULL OR salary > 0);

-- 2. Modify by dropping then re-adding
ALTER TABLE teacher DROP CONSTRAINT chk_teacher_salary;
ALTER TABLE teacher ADD CONSTRAINT chk_teacher_salary CHECK (salary IS NULL OR salary >= 30000);

-- 3. Drop completely
ALTER TABLE teacher DROP CONSTRAINT chk_teacher_salary;
```

_(Note: When adding a constraint to a populated table, PostgreSQL scans existing rows under an exclusive lock; if any existing row violates the new rule, `ALTER TABLE` fails and rolls back.)_
