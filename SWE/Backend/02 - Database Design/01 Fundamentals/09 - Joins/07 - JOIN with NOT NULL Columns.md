# JOIN with NOT NULL Columns

The interaction between `NOT NULL` column constraints and join behavior is a subtle but important topic in SQL. When a foreign key column is defined as `NOT NULL`, it guarantees that every row in the child table has a reference to an existing row in the parent table. This guarantee has direct consequences for the results of inner joins and outer joins, and understanding these consequences prevents confusion when query results do not match expectations.

This note builds on the concepts from [[07 - NOT NULL Foreign Key]] and [[03 - Inner Join]], focusing specifically on how the `NOT NULL` constraint changes the practical behavior of different join types.

## The NOT NULL Guarantee

When a foreign key column is declared as `NOT NULL`, the database enforces the rule that every row must have a value in that column. In the context of a relationship between two tables, this means that every row in the child table is guaranteed to have an associated parent row. For example, if the `comment` table has a `user_id` column defined as `NOT NULL`, then every comment must be associated with a user. There can be no orphan comments floating without an author.

This guarantee simplifies join behavior because it eliminates the possibility of unmatched rows on the child side. However, the parent side is not constrained in the same way. A user is not required to have any comments, so users without comments still exist and can be excluded or included depending on the join type used.

## Example Schema: User and Comment

```sql
CREATE TABLE user (
    user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE comment (
    comment_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id INT UNSIGNED NOT NULL,
    comment_text TEXT NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
```

In this schema, `comment.user_id` is `NOT NULL`. Every comment has a user. But a user can have zero comments.

## Inner Join with NOT NULL Foreign Key

An inner join between `user` and `comment` on `user_id` returns only users who have comments. Because every comment has a user (enforced by `NOT NULL`), no comments are ever excluded by the inner join. However, users who have never posted a comment are excluded because their `user_id` does not appear in the comment table.

```sql
SELECT user.username, comment.comment_text
FROM user
INNER JOIN comment
    ON user.user_id = comment.user_id;
```

Result analysis:
- All comments are included (every comment has a user_id, so every comment matches a user).
- Only some users are included (users without comments have no matching row in the comment table).

## Left Outer Join with Comments on the Left

If you place the comment table on the left side of a left outer join, all comments are preserved. Since every comment already has a user (due to `NOT NULL`), this produces the same result as the inner join:

```sql
SELECT user.username, comment.comment_text
FROM comment
LEFT OUTER JOIN user
    ON comment.user_id = user.user_id;
```

Result analysis:
- All comments are included (the left outer join preserves all left-table rows).
- The user columns are never `NULL` because every comment has a user.

This query and the inner join above return identical results. The left outer join is not wrong, but it is unnecessary in this case because the `NOT NULL` constraint already guarantees that no comment will ever lack a matching user.

## Left Outer Join with Users on the Left

If you place the user table on the left side of a left outer join, all users are preserved, including those who have never posted a comment:

```sql
SELECT user.username, comment.comment_text
FROM user
LEFT OUTER JOIN comment
    ON user.user_id = comment.user_id;
```

Result analysis:
- All users are included (the left outer join preserves all left-table rows).
- Users without comments show `NULL` in the `comment_text` column.
- All comments are included (every comment matches a user).

This is the only query of the three that produces a different result. It includes users who have never commented, which neither the inner join nor the comment-left outer join does.

## Comparison Table

| Join Type | Users Included | Comments Included | NULLs in Result |
|-----------|---------------|-------------------|-----------------|
| INNER JOIN | Only users with comments | All (NOT NULL guarantees this) | None |
| LEFT JOIN (comment left) | Only users with comments | All | None (same as inner join) |
| LEFT JOIN (user left) | All users | All | In comment columns for users without comments |

The critical insight is that when the foreign key is `NOT NULL`, the inner join and the left outer join with the child table on the left produce identical results. The `NOT NULL` constraint makes the outer join redundant in that direction because there are no unmatched child rows to preserve.

## Practical Implications

When planning your joins, you should consider the nullability of your foreign key columns. If a foreign key is `NOT NULL`, you can safely use an inner join without worrying about losing child-table rows. If a foreign key is nullable, an inner join will exclude rows where the foreign key is `NULL`, and you may need an outer join to preserve them.

A practical approach is to design your joins as if all foreign keys were nullable, choosing the join type based on the logical requirements of the query. This strategy works correctly regardless of whether the column is actually `NOT NULL` or not. If the column happens to be `NOT NULL`, the outer join simply degrades gracefully to produce the same result as an inner join, with no `NULL` values appearing in the output.

However, when you need to optimize query performance or understand why a query returns certain results, knowing the `NOT NULL` status of your foreign keys is invaluable. An inner join on a `NOT NULL` foreign key will never lose child rows, which can save you from adding unnecessary outer joins and their associated `NULL`-handling logic.

## Nullable Foreign Key Example

For contrast, consider what happens when the foreign key is nullable:

```sql
CREATE TABLE card (
    card_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    customer_id INT UNSIGNED,
    max_amount DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (card_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
```

Here, `card.customer_id` allows `NULL`, meaning a card can exist without a customer. An inner join between `customer` and `card` would exclude these unassigned cards, while a left outer join (with card on the left) or a right outer join (with card on the right) would preserve them. The nullable foreign key creates the possibility of unmatched rows, making the choice of join type consequential in a way that `NOT NULL` foreign keys do not.

## Summary

The `NOT NULL` constraint on a foreign key column guarantees that every row in the child table references a parent row. This guarantee means that inner joins and outer joins in the "child-to-parent" direction produce identical results. The join type only matters in the "parent-to-child" direction, where the parent may have no associated child rows. Understanding this interaction allows you to choose the simplest join type that correctly expresses your query logic, avoiding unnecessary outer joins while ensuring no data is inadvertently lost.
