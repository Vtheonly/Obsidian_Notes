# Outer Join Across 3 Tables

Outer joins can be extended across three or more tables by chaining join clauses, just as inner joins can. However, the interaction between outer join types and the sequential nature of multi-table joins introduces additional complexity. Each join in the chain operates on the result of the previous join, which means that the type and direction of each outer join affects which rows survive to the final result.

This note builds on the multi-table join concepts from [[43 - Inner Join on 3 Tables]] and the outer join fundamentals from [[45 - Introduction to Outer Joins]]. Understanding both of those topics is essential before tackling outer joins across three tables.

## The Chaining Principle

When you join three tables, the database processes the joins sequentially. The first join combines the first two tables into an intermediate result set. The second join then combines that intermediate result with the third table. The type of each join (inner, left outer, or right outer) determines how unmatched rows are handled at each stage.

This sequential processing means that rows eliminated by an early join cannot be recovered by a later join. If the first join is an inner join that excludes certain rows, those rows are gone regardless of what the second join does. Similarly, if the first join is a left outer join that preserves all rows from the left table, a subsequent inner join may then eliminate some of those rows if they do not match the third table.

## Example Schema: User, Comment, and Video

Consider a video-sharing platform with three tables:

```
user                    comment                    video
+---------+----------+  +------------+---------+----------+  +----------+-----------+
| user_id | username |  | comment_id | user_id | video_id |  | video_id | title     |
+---------+----------+  +------------+---------+----------+  +----------+-----------+
| 1       | Alice    |  | 1          | 1       | 1        |  | 1        | DB Design |
| 2       | Bob      |  | 2          | 2       | 2        |  | 2        | SQL Basics|
| 3       | Carol    |  | 3          | 1       | 2        |  | 3        | Joins     |
| 4       | Dave     |  +------------+---------+----------+  +----------+-----------+
+---------+----------+                                         |
                                                               No comments on video 3
                                    Dave (user 4) has no comments
```

The `comment` table has both `user_id` and `video_id` defined as `NOT NULL`. Every comment is guaranteed to have both a user and a video.

## Left Outer Join Followed by Right Outer Join

Consider a query that uses a left outer join between user and comment, then a right outer join between the intermediate result and video:

```sql
SELECT
    user.username,
    comment.comment_text,
    video.title
FROM user
LEFT OUTER JOIN comment
    ON user.user_id = comment.user_id
RIGHT OUTER JOIN video
    ON comment.video_id = video.video_id;
```

### Step 1: User LEFT OUTER JOIN Comment

The left outer join preserves all users. Every comment has a user (due to `NOT NULL`), so all comments are included as well.

```
Intermediate Result:
+---------+----------+------------+---------+----------+
| user_id | username | comment_id | user_id | video_id |
+---------+----------+------------+---------+----------+
| 1       | Alice    | 1          | 1       | 1        |
| 1       | Alice    | 3          | 1       | 2        |
| 2       | Bob      | 2          | 2       | 2        |
| 3       | Carol    | NULL       | NULL    | NULL     |
| 4       | Dave     | NULL       | NULL    | NULL     |
+---------+----------+------------+---------+----------+
```

Alice, Bob, Carol, and Dave are all present. Carol and Dave have no comments, so the comment columns are `NULL`.

### Step 2: Intermediate RIGHT OUTER JOIN Video

The right outer join preserves all videos. The intermediate result is matched to the video table on `comment.video_id = video.video_id`.

```
Final Result:
+----------+--------------+-----------+
| username | comment_text | title     |
+----------+--------------+-----------+
| Alice    | Great!       | DB Design |
| Alice    | Thanks!      | SQL Basics|
| Bob      | Nice         | SQL Basics|
| NULL     | NULL         | Joins     |
+----------+--------------+-----------+
```

Video 3 ("Joins") has no comments, so it appears with `NULL` in the user and comment columns. Carol and Dave, who were present in the intermediate result after step 1, are eliminated in step 2 because their `NULL` `video_id` values cannot match any row in the video table. The right outer join preserves videos, not users.

### Summary of This Join Pattern

| Entity | Included | Excluded | Reason |
|--------|----------|----------|--------|
| Videos | All | None | Right outer join preserves all videos |
| Comments | All | None | All comments have videos (NOT NULL) |
| Users | Only those with comments | Carol, Dave | Users without comments have no video_id to match |

## Alternative: Two Left Outer Joins

A different query uses left outer joins for both stages, placing the table you want to fully preserve on the left:

```sql
SELECT
    user.username,
    comment.comment_text,
    video.title
FROM video
LEFT OUTER JOIN comment
    ON video.video_id = comment.video_id
LEFT OUTER JOIN user
    ON comment.user_id = user.user_id;
```

### Step 1: Video LEFT OUTER JOIN Comment

All videos are preserved. Comments are matched where they exist.

```
Intermediate Result:
+----------+-----------+------------+---------+
| video_id | title     | comment_id | user_id |
+----------+-----------+------------+---------+
| 1        | DB Design | 1          | 1       |
| 2        | SQL Basics| 2          | 2       |
| 2        | SQL Basics| 3          | 1       |
| 3        | Joins     | NULL       | NULL    |
+----------+-----------+------------+---------+
```

### Step 2: Intermediate LEFT OUTER JOIN User

The left outer join preserves all rows from the intermediate result (which represents all videos). Users are matched where they exist.

```
Final Result:
+----------+--------------+-----------+
| username | comment_text | title     |
+----------+--------------+-----------+
| Alice    | Great!       | DB Design |
| Bob      | Nice         | SQL Basics|
| Alice    | Thanks!      | SQL Basics|
| NULL     | NULL         | Joins     |
+----------+--------------+-----------+
```

This produces the same final result as the previous query, but the logic flows more naturally: start with videos, attach comments, then attach users. Using consistent left outer joins makes the query easier to read and reason about.

## Handling NULLs Across Multiple Outer Joins

When chaining outer joins, `NULL` values from an early join can affect the behavior of later joins. A row with `NULL` in a foreign key column cannot match any row in the next table, which means it will either produce more `NULL` values (if the next join is a left or full outer join) or be eliminated entirely (if the next join is an inner or right outer join that does not preserve that side).

This cascading effect is why it is crucial to plan the order and type of your joins carefully. Always ask yourself: which table must be fully represented in the final result? Start with that table and use left outer joins to attach the others, preserving all rows from the starting table at each stage.

## General Strategy for Multi-Table Outer Joins

1. Identify the primary table whose rows must all appear in the result.
2. Place that table in the `FROM` clause.
3. Use `LEFT OUTER JOIN` for each subsequent table, attaching them in the order of the relationship chain.
4. Each left outer join preserves all rows from the accumulated result so far.
5. If you need to preserve rows from a table on the right side, either use a right outer join at that stage or restructure the query to make that table the starting point.

This strategy avoids the confusion of mixing left and right outer joins and produces queries that are easier to read, maintain, and debug.
