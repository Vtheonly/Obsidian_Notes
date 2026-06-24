# Inner Join on 3 Tables Example

This note provides a practical walkthrough of a three-table inner join using a concrete example with sample data. While [[43 - Inner Join on 3 Tables]] covered the conceptual framework and syntax, this note focuses on applying those concepts to a realistic scenario and tracing the data through each stage of the join to understand exactly which rows are included and which are excluded.

## The Scenario: Video Sharing Platform

Consider a video-sharing website where users can post comments on videos. The database has three tables: `user`, `comment`, and `video`. The `comment` table serves as the junction between users and videos. Each comment is posted by exactly one user on exactly one video. A user can post many comments, and a video can receive many comments, but the user and video tables have no direct relationship with each other.

## Table Structure and Sample Data

### User Table

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

### Video Table

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

### Comment Table

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

## Key Design Decisions

The `comment` table has both `user_id` and `video_id` defined as `NOT NULL`. This is a deliberate design choice reflecting the business rule that every comment must be associated with a user who posted it and a video it was posted on. A comment without a user or without a video makes no logical sense in this context.

The `comment_id` is a surrogate primary key. An alternative design could use the combination of `user_id` and `video_id` as a compound key, but that would be inappropriate here because a single user can post multiple comments on the same video. The surrogate key avoids this limitation.

## The Three-Table Inner Join Query

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

## Tracing the Join Step by Step

### Step 1: Join user and comment

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

### Step 2: Join the intermediate result with video

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

## Summary of Exclusions

| Entity | Included | Excluded | Reason |
|--------|----------|----------|--------|
| Users | 5 of 6 | BestSpeller (ID 6) | No comments posted |
| Comments | 6 of 6 | None | All comments have users (NOT NULL) |
| Videos | 6 of 8 | Database Design 8 (ID 8) | No comments received |

The inner join ensures that only complete chains of relationships are included in the result. Any entity that is not connected through the full chain is excluded.

## Adding Filters and Ordering

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

## Transition to Outer Joins

If the application needs to show all users, even those who have never commented, or all videos, even those with zero comments, an inner join cannot accomplish this. In those cases, an outer join is required. See [[45 - Introduction to Outer Joins]] for the outer join alternatives that preserve unmatched rows, and [[48 - Outer Join Across 3 Tables]] for extending outer joins across multiple tables.
