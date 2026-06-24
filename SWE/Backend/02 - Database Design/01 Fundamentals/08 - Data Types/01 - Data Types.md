# Data Types

Every column in a database table must be assigned a specific data type at the time of creation. The data type defines what kind of values can be stored in that column, how they are stored internally, and what operations can be performed on them. Choosing the correct data type for each column is a fundamental design decision that affects storage efficiency, query performance, and data integrity. Without proper data type assignment, the database cannot enforce constraints or optimize storage and retrieval effectively.

Data types are generally organized into three primary categories: **numeric**, **string**, and **date/time**. While the exact names and specifications of these types vary between database management systems (MySQL, PostgreSQL, SQL Server, Oracle), the conceptual categories remain consistent across all platforms. Understanding these categories and their subcategories is essential before designing any schema.

## Numeric Data Types

Numeric data types store numbers and support mathematical operations. Unlike strings that happen to contain digits, numeric types are stored in formats that allow arithmetic computation directly within the database engine. The choice between numeric subtypes depends on the required precision, the range of values, and whether fractional components are needed.

### Integer Types

Integer types store whole numbers without any fractional component. They are the most commonly used numeric types for primary keys, counts, and identifiers. Different integer subtypes provide different ranges of values and storage sizes:

| Type | Storage | Signed Range | Unsigned Range |
|------|---------|-------------|----------------|
| TINYINT | 1 byte | -128 to 127 | 0 to 255 |
| SMALLINT | 2 bytes | -32,768 to 32,767 | 0 to 65,535 |
| INT | 4 bytes | -2,147,483,648 to 2,147,483,647 | 0 to 4,294,967,295 |
| BIGINT | 8 bytes | -9.2 x 10^18 to 9.2 x 10^18 | 0 to 1.8 x 10^19 |

When a column is declared as `UNSIGNED`, it cannot store negative values, which effectively doubles the maximum positive value. For example, an `INT UNSIGNED` can store values from 0 to 4,294,967,295 instead of the signed range of -2,147,483,648 to 2,147,483,647. This distinction is important when designing columns that logically cannot be negative, such as ages or quantities.

```sql
CREATE TABLE products (
    product_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    quantity_in_stock SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (product_id)
);
```

### Decimal and Fixed-Point Types

The `DECIMAL` (or `NUMERIC`) type stores exact numeric values using a base-10 representation. It is the correct choice for financial calculations and any data where precision must be exact, such as currency amounts. When you declare `DECIMAL(p, s)`, the `p` specifies the total number of significant digits (precision) and `s` specifies the number of digits after the decimal point (scale).

```sql
CREATE TABLE invoices (
    invoice_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    tax_rate DECIMAL(5, 4) NOT NULL,
    PRIMARY KEY (invoice_id)
);
```

In this example, `DECIMAL(10, 2)` can store values up to 99,999,999.99, and `DECIMAL(5, 4)` can store values like 0.0875 (a tax rate). Because `DECIMAL` operates in base 10, it can represent values like 0.1 exactly, unlike floating-point types.

### Floating-Point Types

Floating-point types (`FLOAT` and `DOUBLE`) store approximate numeric values using a binary representation. They are suitable for scientific computations where slight rounding errors are acceptable but are not appropriate for financial data. The binary representation cannot exactly store certain decimal fractions. For instance, the decimal value 0.1 cannot be represented precisely in binary floating-point, leading to small but cumulative rounding errors.

```sql
CREATE TABLE sensor_readings (
    reading_id INT NOT NULL,
    temperature FLOAT NOT NULL,
    pressure DOUBLE,
    PRIMARY KEY (reading_id)
);
```

Use `FLOAT` for approximately 7 decimal digits of precision and `DOUBLE` for approximately 15 decimal digits. Always prefer `DECIMAL` over `FLOAT` or `DOUBLE` when exact precision is required.

## String Data Types

String data types store sequences of characters. They are used for names, addresses, descriptions, and any textual data. The choice between string subtypes depends on whether the data has a fixed or variable length and how much data needs to be stored.

### CHAR and VARCHAR

`CHAR(n)` stores fixed-length strings. Every value occupies exactly `n` characters of storage, padded with trailing spaces if the input is shorter than `n`. This makes `CHAR` appropriate for data that always has the same length, such as two-letter country codes, postal codes of uniform length, or MD5 hashes.

`VARCHAR(n)` stores variable-length strings up to a maximum of `n` characters. Unlike `CHAR`, it only uses as much storage as the actual data requires (plus a small overhead byte or two). This makes `VARCHAR` the standard choice for most textual data where lengths vary, such as names, email addresses, and descriptions.

```sql
CREATE TABLE customers (
    customer_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    country_code CHAR(2) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (customer_id)
);
```

### TEXT Types

The `TEXT` type is designed for large blocks of text data, such as comments, articles, or messages. Unlike `VARCHAR`, which has a relatively low maximum length in some database systems, `TEXT` can store much larger amounts of data. However, `TEXT` columns often cannot be used in certain index types or have default values in some systems, so `VARCHAR` should be preferred when the data is bounded.

```sql
CREATE TABLE blog_posts (
    post_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    PRIMARY KEY (post_id)
);
```

## Date and Time Data Types

Date and time types store temporal information. They are essential for tracking when events occur, when records are created, and when data changes. Understanding the differences between the subtypes is critical for choosing the right one for each use case.

| Type | Description | Example Format |
|------|-------------|----------------|
| DATE | Calendar date only | '2024-02-22' |
| TIME | Time of day only | '14:30:22' |
| DATETIME | Combined date and time | '2024-02-22 14:30:22' |
| TIMESTAMP | Date, time, and time zone awareness | '2024-02-22 14:30:22 UTC' |

### DATE

The `DATE` type stores only a calendar date (year, month, day) with no time component. It is appropriate for birth dates, holidays, and any scenario where the time of day is irrelevant.

### TIME

The `TIME` type stores a time of day (hours, minutes, seconds) without any date component. It can also represent elapsed time intervals. Use it for daily schedules, operating hours, or duration measurements.

### DATETIME

The `DATETIME` type stores both a date and a time together. It is suitable for recording appointments, event start times, and log entries where both the date and time are significant. The stored value is not time-zone aware; it represents whatever was inserted without conversion.

### TIMESTAMP

The `TIMESTAMP` type stores a date and time value that is typically converted to and stored as UTC, then converted back to the session time zone when retrieved. It is commonly used for tracking row creation or modification times. Many database systems support an `ON UPDATE CURRENT_TIMESTAMP` clause that automatically updates the column whenever the row is modified.

```sql
CREATE TABLE transactions (
    transaction_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    account_id INT UNSIGNED NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id)
);
```

## Boolean and Binary Types

### Boolean

Most database systems provide a `BOOLEAN` type (or `BOOL`), which is typically implemented as a synonym for `TINYINT(1)`. It stores logical true or false values. In SQL, true is represented as 1 and false as 0. Some systems support the literal keywords `TRUE` and `FALSE` for readability.

```sql
CREATE TABLE user_accounts (
    user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (user_id)
);
```

### Binary Types

Binary data types store raw byte sequences rather than character strings. `BLOB` (Binary Large Object) is used for storing images, files, or other binary data. `VARBINARY` is the binary equivalent of `VARCHAR`. These types do not undergo character set encoding or collation processing, which makes them suitable for encrypted data, compressed data, or media files.

```sql
CREATE TABLE documents (
    document_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    file_name VARCHAR(255) NOT NULL,
    file_data BLOB,
    PRIMARY KEY (document_id)
);
```

## Choosing the Right Data Type

Selecting the appropriate data type for each column involves balancing storage efficiency, query performance, and data integrity. The following guidelines should inform your decisions:

- Use the smallest type that can accommodate all expected values. An `INT` wastes storage if a `SMALLINT` suffices.
- Use `DECIMAL` for financial data and any values requiring exact precision. Never use `FLOAT` or `DOUBLE` for money.
- Use `VARCHAR` for variable-length text and `CHAR` for fixed-length text.
- Use `TIMESTAMP` for automatic tracking of row creation and modification times.
- Use `UNSIGNED` integer types when negative values are logically impossible.

Proper data type selection also supports [[08 - Data Integrity]] by preventing invalid data from being inserted into columns. For example, a `DATE` column will reject a value like '2024-02-30', and an `INT` column will reject alphabetic characters.

## Data Type Comparison Table

| Category | Type | Use Case | Precision |
|----------|------|----------|-----------|
| Numeric | INT | Whole numbers, IDs | Exact |
| Numeric | BIGINT | Very large whole numbers | Exact |
| Numeric | DECIMAL | Currency, financial data | Exact (base 10) |
| Numeric | FLOAT | Scientific measurements | Approximate (base 2) |
| Numeric | DOUBLE | High-precision scientific | Approximate (base 2) |
| String | CHAR | Fixed-length codes | N/A |
| String | VARCHAR | Names, addresses | N/A |
| String | TEXT | Articles, comments | N/A |
| Date/Time | DATE | Birth dates, holidays | Day-level |
| Date/Time | TIME | Schedules, durations | Second-level |
| Date/Time | DATETIME | Appointments, events | Second-level |
| Date/Time | TIMESTAMP | Auto-tracked modifications | Second-level |
| Boolean | BOOLEAN | True/false flags | N/A |
| Binary | BLOB | Images, files | N/A |
