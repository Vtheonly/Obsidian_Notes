# Inner Join on 3 Tables

Inner joins can be extended beyond two tables by chaining additional `INNER JOIN` clauses in a single query. This capability is essential because real-world databases rarely store all related data in just two tables. A typical query might need to pull information from three, four, or even more tables to assemble a complete view of the data. The principles that govern a two-table inner join apply to each additional join, but the cumulative effect on the result set requires careful analysis.

When you join three tables, the database evaluates the join conditions pairwise. The first join combines the first two tables and produces an intermediate result set. The second join then combines that intermediate result with the third table using another join condition. Because each inner join excludes unmatched rows, every additional table you join has the potential to further reduce the size of the result set.

## Chaining JOIN Clauses

The syntax for joining three tables follows naturally from the two-table pattern. After the first `INNER JOIN` and its `ON` clause, you add a second `INNER JOIN` with its own `ON` clause. Each `ON` clause specifies how the newly joined table relates to the tables already in the query.

```sql
SELECT
    table_a.column_name,
    table_b.column_name,
    table_c.column_name
FROM table_a
INNER JOIN table_b
    ON table_a.key = table_b.foreign_key
INNER JOIN table_c
    ON table_b.key = table_c.foreign_key;
```

The order in which you list the joins typically mirrors the chain of relationships between the tables. The first table connects to the second, the second connects to the third, and so on. The database optimizer may rearrange the join order for performance, but the logical order should reflect the structure of your data.

## How Relationships Work Across Multiple Tables

In a three-table join, the relationships between the tables do not need to form a closed loop. The first and third tables may have no direct relationship with each other; they are connected indirectly through the middle table. This is a common pattern when the middle table serves as a bridge or junction between two entities.

### Example A: Banking — Customer / Card / Card Type

Consider a banking database with three tables: `customer`, `card`, and `card_type`. The `customer` table stores personal information. The `card` table stores credit card details with a `customer_id` foreign key referencing the customer table and a `card_type_id` foreign key referencing the card type table. The `card_type` table is a lookup table that stores the type of card (Visa, Mastercard, etc.) along with any type-specific information such as standard interest rates.

```
customer                  card                    card_type
+-------------+------+   +--------+--------+-----+   +-------------+-----------+-------+
| customer_id | name |   | card_id|cust_id |ct_id|   | card_type_id| name      | rate  |
+-------------+------+   +--------+--------+-----+   +-------------+-----------+-------+
| 1           | Caleb|   | 101    | 1      | 2   |   | 1           | Visa      | 0.15  |
| 2           | Jimmy|   | 102    | 1      | 1   |   | 2           | Mastercard| 0.18  |
| 3           | Sarah|   | 103    | 2      | 2   |   | 3           | Amex      | 0.20  |
+-------------+------+   +--------+--------+-----+   +-------------+-----------+-------+
```

The `card` table is the middle table that connects customers to card types. A three-table inner join combines data from all three:

```sql
SELECT
    customer.first_name,
    customer.last_name,
    card.card_id,
    card_type.name AS card_type_name,
    card_type.rate
FROM customer
INNER JOIN card
    ON customer.customer_id = card.customer_id
INNER JOIN card_type
    ON card.card_type_id = card_type.card_type_id;
```

This query returns customer names alongside their card details and the card type name and interest rate. Without the join to `card_type`, the `card_type_id` in the card table would be an opaque number.

## The Lookup Table Pattern

The `card_type` table in the example above is a lookup table, as discussed in [[10 - Lookup Table]]. Lookup tables are a common reason for three-table joins. They eliminate repeating data by storing each unique value once and referencing it by an ID. If the card type name or rate changes (for example, if "Mastercard" is renamed), you update a single row in the lookup table rather than every row in the card table.

Without the lookup table, the card table might contain a `card_type` column with values like "Visa" repeated many times. This would violate the principles of normalization (specifically, it would create a transitive dependency between `card_type` and the card type's interest rate, violating third normal form). The lookup table resolves this by separating the card type attributes into their own table.

## Cumulative Filtering Effect

Each inner join in a multi-table query acts as a filter. The first join between `customer` and `card` excludes customers without cards and cards without customers. The second join between `card` and `card_type` further excludes cards without a card type and card types without any cards. The final result contains only rows where a complete chain of matches exists across all three tables.

This cumulative filtering means that adding more tables to an inner join generally produces a smaller result set, not a larger one. Each additional join condition removes rows that cannot be matched on both sides. This is an important consideration when designing queries: if you notice rows disappearing that you expected to see, it may be because an inner join is filtering them out.

## NOT NULL Considerations in Multi-Table Joins

The effect of the cumulative filter depends on whether the foreign key columns are defined as `NOT NULL`. If `card.customer_id` is `NOT NULL`, then every card has a customer, and the first inner join will not exclude any cards from the card table. If `card.card_type_id` is `NOT NULL`, then every card has a card type, and the second inner join will not exclude any cards either.

However, the reverse direction still applies. Even if every card has a customer, the inner join will still exclude customers who have no cards. And even if every card has a card type, the inner join will still exclude card types that have no associated cards (for example, a newly added card type that has not yet been issued to any customer).

Understanding which rows are excluded at each stage of a multi-table join is crucial for predicting and interpreting the query results. If you need to preserve rows that would otherwise be excluded, consider using outer joins as described in [[05 - Outer Joins Explained]].

## Example B: Practical Walkthrough — Video Sharing Platform

Consider a video-sharing website where users can post comments on videos. The database has three tables: `user`, `comment`, and `video`. The `comment` table serves as the junction between users and videos. Each comment is posted by exactly one user on exactly one video. A user can post many comments, and a video can receive many comments, but the user and video tables have no direct relationship with each other.

### Table Structure and Sample Data

**User Table**

```
+---------+----------------------+------------------+
| user_id | username             | email            |
+---------+----------------------+------------------+
| 1       | AllSkyPizza          | allsky@email.com |
| 2       | ha12                 | ha12@email.com   |
| 3       | PabloIsAwesome       | pablo@email.com  |
| 4       | MilkAndCookies       | milk@email.com   |
| 5       | YellowSwag           | yellow@email.com |
| 6       | BestSpeller          | best@email.com   |
+---------+----------------------+------------------+
```

**Video Table**

```
+----------+-------------------------+-----------------------------------+
| video_id | title                   | description                       |
+----------+-------------------------+-----------------------------------+
| 1        | Database Design 1       | Introduction to database design   |
| 2        | Database Design 2       | Relational databases explained    |
| 3        | Database Design 3       | RDBMS overview                    |
| 4        | Database Design 4       | Introduction to SQL               |
| 5        | Database Design 5       | Naming conventions                |
| 6        | Database Design 6       | What is database design           |
| 7        | Database Design 7       | Data integrity                    |
| 8        | Database Design 8       | Database terms                    |
+----------+-------------------------+-----------------------------------+
```

**Comment Table**

```
+------------+---------+----------+-----------------------+
| comment_id | user_id | video_id | comment               |
+------------+---------+----------+-----------------------+
| 1          | 1       | 3        | Great explanation!    |
| 2          | 2       | 5        | Very helpful          |
| 3          | 3       | 1        | Love this series      |
| 4          | 1       | 7        | Data integrity rules  |
| 5          | 4       | 2        | Nice video            |
| 6          | 5       | 4        | Learned a lot         |
+------------+---------+----------+-----------------------+
```

Notice that user ID 6 (BestSpeller) has no comments and video ID 8 (Database Design 8) has no comments. These two rows will be affected by the inner join behavior.

### Key Design Decisions

The `comment` table has both `user_id` and `video_id` defined as `NOT NULL`. This is a deliberate design choice reflecting the business rule that every comment must be associated with a user who posted it and a video it was posted on. A comment without a user or without a video makes no logical sense in this context.

The `comment_id` is a surrogate primary key. An alternative design could use the combination of `user_id` and `video_id` as a compound key, but that would be inappropriate here because a single user can post multiple comments on the same video. The surrogate key avoids this limitation.

### The Three-Table Inner Join Query

```sql
SELECT
    user.username,
    video.title,
    comment.comment
FROM user
INNER JOIN comment
    ON user.user_id = comment.user_id
INNER JOIN video
    ON comment.video_id = video.video_id;
```

### Tracing the Join Step by Step

**Step 1: Join user and comment**

The first inner join matches rows from the `user` table and the `comment` table where `user.user_id = comment.user_id`.

```
Intermediate Result (User JOIN Comment):
+---------+----------------------+------------+----------+---------------------+
| user_id | username             | comment_id | video_id | comment             |
+---------+----------------------+------------+----------+---------------------+
| 1       | AllSkyPizza          | 1          | 3        | Great explanation!  |
| 2       | ha12                 | 2          | 5        | Very helpful        |
| 3       | PabloIsAwesome       | 3          | 1        | Love this series    |
| 1       | AllSkyPizza          | 4          | 7        | Data integrity rules|
| 4       | MilkAndCookies       | 5          | 2        | Nice video          |
| 5       | YellowSwag           | 6          | 4        | Learned a lot       |
+---------+----------------------+------------+----------+---------------------+
```

User ID 6 (BestSpeller) is excluded because there is no matching `user_id` in the comment table. Since `user_id` is `NOT NULL` in the comment table, there are no orphan comments, so no comments are excluded at this stage. All six comments survive the first join.

**Step 2: Join the intermediate result with video**

The second inner join matches rows from the intermediate result and the `video` table where `comment.video_id = video.video_id`.

```
Final Result:
+----------------------+-------------------------+---------------------+
| username             | title                   | comment             |
+----------------------+-------------------------+---------------------+
| AllSkyPizza          | Database Design 3       | Great explanation!  |
| ha12                 | Database Design 5       | Very helpful        |
| PabloIsAwesome       | Database Design 1       | Love this series    |
| AllSkyPizza          | Database Design 7       | Data integrity rules|
| MilkAndCookies       | Database Design 2       | Nice video          |
| YellowSwag           | Database Design 4       | Learned a lot       |
+----------------------+-------------------------+---------------------+
```

Video ID 8 (Database Design 8) is excluded because it has no comments, meaning there is no `video_id = 8` in the comment table to match against. Since `video_id` is `NOT NULL` in the comment table, there are no comments without an associated video, so no comments are lost at this stage either.

### Summary of Exclusions

| Entity | Included | Excluded | Reason |
|--------|----------|----------|--------|
| Users | 5 of 6 | BestSpeller (ID 6) | No comments posted |
| Comments | 6 of 6 | None | All comments have users (NOT NULL) |
| Videos | 6 of 8 | Database Design 8 (ID 8) | No comments received |

The inner join ensures that only complete chains of relationships are included in the result. Any entity that is not connected through the full chain is excluded.

### Adding Filters and Ordering

You can refine the query with `WHERE` and `ORDER BY` clauses to focus on specific subsets of the joined data:

```sql
SELECT
    user.username,
    video.title,
    comment.comment
FROM user
INNER JOIN comment
    ON user.user_id = comment.user_id
INNER JOIN video
    ON comment.video_id = video.video_id
WHERE video.title LIKE '%Database Design%'
ORDER BY user.username, video.title;
```

This variation filters for videos whose titles contain "Database Design" (which includes all videos in this example) and sorts the results by username and then by video title.

## Full SQL Example (Banking)

```sql
-- Create the tables
CREATE TABLE customer (
    customer_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_id)
);

CREATE TABLE card_type (
    card_type_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    rate DECIMAL(5, 4) NOT NULL,
    PRIMARY KEY (card_type_id)
);

CREATE TABLE card (
    card_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    customer_id INT UNSIGNED NOT NULL,
    card_type_id INT UNSIGNED NOT NULL,
    max_amount DECIMAL(10, 2) NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL DEFAULT 0,
    PRIMARY KEY (card_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (card_type_id) REFERENCES card_type(card_type_id)
);

-- Three-table inner join
SELECT
    customer.first_name,
    customer.last_name,
    card_type.name AS card_type_name,
    card.max_amount,
    card.amount_paid
FROM customer
INNER JOIN card
    ON customer.customer_id = card.customer_id
INNER JOIN card_type
    ON card.card_type_id = card_type.card_type_id
ORDER BY customer.last_name, customer.first_name;
```

This complete example creates the three tables, establishes the foreign key relationships, and demonstrates the three-table inner join. The result shows each customer's name along with their card type and financial details, providing a user-friendly view that spans all three normalized tables.

## Transition to Outer Joins

If the application needs to show all users, even those who have never commented, or all videos, even those with zero comments, an inner join cannot accomplish this. In those cases, an outer join is required. See [[05 - Outer Joins Explained]] for the outer join alternatives that preserve unmatched rows, and [[06 - Outer Join Across 3 Tables]] for extending outer joins across multiple tables.

## See Also

- [[03 - Inner Join]] — Foundational inner join concepts
- [[10 - Lookup Table]] — The lookup table pattern used in three-table joins
- [[05 - Outer Joins Explained]] — Preserving unmatched rows
- [[06 - Outer Join Across 3 Tables]] — Outer joins across multiple tables
