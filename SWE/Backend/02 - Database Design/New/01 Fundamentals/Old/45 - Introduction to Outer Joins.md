# Introduction to Outer Joins

Outer joins extend the behavior of inner joins by preserving rows from one or both tables even when no matching row exists in the other table. While an inner join returns only the intersection of two tables (rows that match on the join condition), an outer join guarantees that at least one side of the relationship is fully represented in the result. When a row has no match on the other side, the columns from the unmatched table are filled with `NULL` values.

Understanding outer joins is essential for queries where excluding unmatched rows would produce an incomplete or misleading result. For example, if you want a list of all customers and their credit cards, including customers who have not yet been issued a card, an inner join would silently drop those customers from the result. A left outer join preserves them.

## How Outer Joins Differ from Inner Joins

The key difference between inner and outer joins is how they handle unmatched rows. In an inner join, if a row in the left table has no corresponding row in the right table (based on the join condition), that row is simply absent from the result. In an outer join, the row is included, and the columns from the table where no match was found are populated with `NULL`.

```
INNER JOIN:          LEFT OUTER JOIN:     RIGHT OUTER JOIN:    FULL OUTER JOIN:
+-------------+      +-------------+      +-------------+      +-------------+
| Matched Only|      | All Left +  |      | All Right + |      | All Left +  |
|             |      | Matched R   |      | Matched L   |      | All Right   |
|  A AND B    |      | NULL for    |      | NULL for    |      | NULL where  |
|  present    |      | missing R   |      | missing L   |      | no match    |
+-------------+      +-------------+      +-------------+      +-------------+
```

This distinction has significant practical implications. If you use an inner join when you should have used an outer join, you may lose data without realizing it. If you use an outer join when an inner join would suffice, you may introduce `NULL` values that complicate downstream processing.

## Types of Outer Joins

### Left Outer Join (LEFT JOIN)

A `LEFT OUTER JOIN` returns all rows from the left table (the table listed in the `FROM` clause). For each left row that has a match in the right table, the columns from the right table are included. For each left row that has no match, the right table columns are `NULL`. This is the most commonly used outer join type.

```sql
SELECT customer.first_name, customer.last_name, card.card_id, card.max_amount
FROM customer
LEFT OUTER JOIN card
    ON customer.customer_id = card.customer_id;
```

In this query, every customer appears in the result. Customers with cards show the card details. Customers without cards show `NULL` in the card columns.

### Right Outer Join (RIGHT JOIN)

A `RIGHT OUTER JOIN` returns all rows from the right table (the table listed after the `JOIN` keyword). Unmatched rows from the left table are filled with `NULL`. This is functionally equivalent to a left outer join with the table order reversed. See [[46 - Right Outer Join]] for a detailed discussion.

```sql
SELECT customer.first_name, customer.last_name, card.card_id
FROM customer
RIGHT OUTER JOIN card
    ON customer.customer_id = card.customer_id;
```

This query returns every card. Cards with an associated customer show the customer details. Cards without a customer (perhaps unissued or deactivated cards) show `NULL` in the customer columns.

### Full Outer Join (FULL JOIN)

A `FULL OUTER JOIN` returns all rows from both tables. Where matches exist, the columns from both tables are combined. Where a row in either table has no match, the missing side is filled with `NULL`. This join type is not supported by MySQL but is available in PostgreSQL and SQL Server.

```sql
SELECT customer.first_name, card.card_id
FROM customer
FULL OUTER JOIN card
    ON customer.customer_id = card.customer_id;
```

This query returns every customer and every card. Matched pairs are combined. Unmatched customers have `NULL` card columns, and unmatched cards have `NULL` customer columns.

## NULL Values in Outer Join Results

The presence of `NULL` values in outer join results is the primary difference from inner join results. These `NULL` values represent missing relationships and can be used intentionally in queries. For example, to find all customers who do not have a card, you can use a left outer join and filter for `NULL` in the right table's key column:

```sql
SELECT customer.first_name, customer.last_name
FROM customer
LEFT OUTER JOIN card
    ON customer.customer_id = card.customer_id
WHERE card.card_id IS NULL;
```

This pattern of using an outer join combined with an `IS NULL` filter is a common technique for finding orphaned or missing records. It works because `NULL` in the right table's key column indicates that no matching row was found in the join.

## When to Use Each Join Type

Choosing the correct join type depends on the question you are asking of the data. The following table summarizes the decision criteria:

| Question | Join Type | Rationale |
|----------|-----------|-----------|
| Show only matched pairs | INNER JOIN | Unmatched rows are irrelevant |
| Show all from left, plus matches | LEFT OUTER JOIN | Preserve every row in the left table |
| Show all from right, plus matches | RIGHT OUTER JOIN | Preserve every row in the right table |
| Show everything from both sides | FULL OUTER JOIN | Preserve all rows from both tables |
| Find rows with no match | LEFT/RIGHT JOIN + IS NULL | Identify orphaned or missing records |

## Comparison Table of All Join Types

| Join Type | Left Table Rows | Right Table Rows | NULLs Produced |
|-----------|----------------|-----------------|----------------|
| INNER JOIN | Only matched | Only matched | None |
| LEFT OUTER JOIN | All | Only matched | In right columns for unmatched left rows |
| RIGHT OUTER JOIN | Only matched | All | In left columns for unmatched right rows |
| FULL OUTER JOIN | All | All | In either side for unmatched rows |

## Outer Joins Across Multiple Tables

Just as inner joins can be chained across three or more tables (see [[43 - Inner Join on 3 Tables]]), outer joins can also be extended. The interaction between outer join types and the order of joins in a multi-table query produces different results, which is covered in detail in [[48 - Outer Join Across 3 Tables]]. The key principle remains: each join condition determines how rows are matched, and the outer join type determines what happens to unmatched rows at that stage.

The concepts introduced here build on the join fundamentals from [[41 - Introduction to Joins]] and the inner join specifics from [[42 - Inner Join]]. The following notes will explore the outer join variants in greater depth, starting with [[46 - Right Outer Join]].
