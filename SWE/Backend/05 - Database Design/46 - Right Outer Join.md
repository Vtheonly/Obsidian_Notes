# Right Outer Join

A `RIGHT OUTER JOIN` (commonly written as `RIGHT JOIN`) returns all rows from the right table and only the matching rows from the left table. When a row in the right table has no corresponding match in the left table, the columns from the left table are populated with `NULL` values in the result. This join type is the mirror image of the `LEFT OUTER JOIN` discussed in [[45 - Introduction to Outer Joins]].

While the right outer join is fully supported by SQL and has legitimate use cases, it is less commonly used in practice than the left outer join. Understanding how it works is important for reading and maintaining existing queries, even if you tend to prefer left joins in your own code.

## Right Outer Join Syntax

The syntax for a right outer join follows the same pattern as other join types. The right table is the one listed after the `RIGHT JOIN` keyword, and it is this table whose rows are fully preserved in the result.

```sql
SELECT left_table.column_name, right_table.column_name
FROM left_table
RIGHT OUTER JOIN right_table
    ON left_table.foreign_key = right_table.primary_key;
```

The `OUTER` keyword is optional. Writing `RIGHT JOIN` is equivalent to `RIGHT OUTER JOIN`.

## How the Right Outer Join Works

Consider a bank database with a `customer` table and a `card` table. The card table has a `customer_id` foreign key that references the customer table, but this column is not necessarily `NOT NULL` -- a card could exist without being assigned to a customer (for example, an unactivated card or a placeholder card in the system).

```
Customer Table                    Card Table
+-------------+-----------+       +--------+-------------+-----------+
| customer_id | name      |       | card_id| customer_id | max_amount|
+-------------+-----------+       +--------+-------------+-----------+
| 1           | Caleb     |       | 101    | 1           | 5000      |
| 2           | Jimmy     |       | 102    | 1           | 3000      |
| 3           | Sarah     |       | 103    | 2           | 10000     |
+-------------+-----------+       | 104    | NULL        | 8000      |
                                  +--------+-------------+-----------+
```

A right outer join with `customer` on the left and `card` on the right:

```sql
SELECT customer.name, card.card_id, card.max_amount
FROM customer
RIGHT OUTER JOIN card
    ON customer.customer_id = card.customer_id;
```

Result:

```
+-----------+--------+-----------+
| name      | card_id| max_amount|
+-----------+--------+-----------+
| Caleb     | 101    | 5000      |
| Caleb     | 102    | 3000      |
| Jimmy     | 103    | 10000     |
| NULL      | 104    | 8000      |
+-----------+--------+-----------+
```

Card 104 has no associated customer, so the `name` column from the customer table is `NULL`. All four cards appear in the result because the right table (card) is fully preserved. Sarah does not appear because she has no cards and the left table (customer) is not fully preserved in a right join.

## Right Join vs. Flipped Left Join

In practice, a right outer join can always be rewritten as a left outer join by swapping the order of the tables. The two queries below produce identical results:

```sql
-- Right outer join
SELECT customer.name, card.card_id, card.max_amount
FROM customer
RIGHT OUTER JOIN card
    ON customer.customer_id = card.customer_id;

-- Equivalent left outer join (tables swapped)
SELECT customer.name, card.card_id, card.max_amount
FROM card
LEFT OUTER JOIN customer
    ON card.customer_id = customer.customer_id;
```

Both queries return all cards with their associated customer information. The only difference is the order in which the tables appear in the `FROM` and `JOIN` clauses. Because of this equivalence, many developers and teams adopt a convention of using only left outer joins for consistency. When every join in a codebase uses the same direction, it is easier to read and reason about the queries.

## When to Use a Right Outer Join

Despite the common convention of preferring left joins, there are situations where a right outer join is the natural choice:

- **Building on an existing query**: If you have a complex query that already references several tables and you need to add a new table on the "left" side while preserving all rows from an existing table, using a right join avoids restructuring the entire query.
- **Reading direction**: Some developers find it more intuitive to list the preserved table after the `JOIN` keyword, especially when the query logic reads more naturally from right to left in the business context.
- **Legacy code**: Existing codebases may use right joins extensively, and understanding them is necessary for maintenance even if you would not write them that way yourself.

## The NOT NULL Effect

If the foreign key column in the right table is defined as `NOT NULL`, then every row in the right table is guaranteed to have a match in the left table. In this case, the right outer join produces the same result as an inner join because there are no unmatched rows in the right table to preserve. This is an important observation: when foreign key columns are `NOT NULL`, the distinction between inner and outer joins may be functionally irrelevant for that side of the relationship.

For example, if `card.customer_id` is `NOT NULL`, then every card has a customer, and a right outer join between customer and card returns exactly the same rows as an inner join. The `NULL` placeholders never appear because every right-table row finds a match. See [[47 - JOIN with NOT NULL Columns]] for a deeper exploration of this interaction.

## Practical Example

```sql
-- Find all cards that have no associated customer
SELECT card.card_id, card.max_amount
FROM customer
RIGHT OUTER JOIN card
    ON customer.customer_id = card.customer_id
WHERE customer.customer_id IS NULL;
```

This query uses the right outer join combined with an `IS NULL` filter to identify orphaned cards. The right join ensures that all cards are included, and the `WHERE` clause filters for the rows where no customer was found. This is the same "find orphans" pattern discussed in [[45 - Introduction to Outer Joins]], but applied from the right side.

## Summary

The right outer join is a legitimate SQL tool that preserves all rows from the right table. While it can always be rewritten as a left outer join by swapping table order, understanding the right join syntax is essential for reading existing SQL and for situations where the right join is the more natural expression of the query logic. The choice between left and right outer joins should be guided by consistency and clarity within your codebase.
