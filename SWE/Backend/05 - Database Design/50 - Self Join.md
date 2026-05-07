# Self Join

A self join is a join in which a table is joined with itself. Rather than combining two different tables, a self join treats a single table as if it were two separate tables by assigning each instance a different alias. The database uses the aliases to distinguish between the two "copies" of the same table, allowing you to compare rows within the same table or follow relationships that exist between rows of a single table.

Self joins are not a distinct join type in SQL syntax. You use the standard `INNER JOIN`, `LEFT JOIN`, or other join keywords, but both sides of the join refer to the same underlying table. The key requirement is that you must use [[49 - Alias|aliases]] to give each instance of the table a unique name.

## When to Use a Self Join

Self joins are used when rows within a single table have relationships to other rows in the same table. The most common scenarios include:

- **Hierarchical data**: An employee table where each employee has a `manager_id` that references another employee's `employee_id`. A self join can pair each employee with their manager's details.
- **Referral systems**: A user table where each user has a `referred_by` column that references another user's `user_id`. A self join can show each user alongside the person who referred them.
- **Adjacency lists**: Any tree or graph structure stored in a single table where rows reference other rows in the same table.
- **Comparing rows**: Finding pairs of rows in the same table that share a characteristic, such as employees in the same department or products with the same price.

## Self Join Syntax

The syntax for a self join follows the standard join pattern, with the critical addition of table aliases to distinguish the two instances of the same table:

```sql
SELECT
    a.column_name,
    b.column_name
FROM table_name AS a
JOIN table_name AS b
    ON a.foreign_key = b.primary_key;
```

The aliases `a` and `b` are arbitrary but should be chosen to reflect the logical role of each instance. For example, in an employee-manager self join, you might use `e` for employee and `m` for manager.

## Complete Example: Employee-Manager Hierarchy

Consider an `employee` table where each employee has a `manager_id` that references the `employee_id` of their manager. The CEO has a `manager_id` of `NULL` because they report to nobody.

### Table Structure

```sql
CREATE TABLE employee (
    employee_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    manager_id INT UNSIGNED,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (manager_id) REFERENCES employee(employee_id)
);
```

Notice that `manager_id` is a foreign key that references the same `employee` table. This is a perfectly valid and common pattern. The `manager_id` column is nullable because the top-level employee (the CEO or founder) has no manager.

### Sample Data

```
+-------------+------------+-----------+----------------------+------------+
| employee_id | first_name | last_name | email                | manager_id |
+-------------+------------+-----------+----------------------+------------+
| 1           | Diana      | Prince    | diana@company.com    | NULL       |
| 2           | Bruce      | Wayne     | bruce@company.com    | 1          |
| 3           | Clark      | Kent      | clark@company.com    | 1          |
| 4           | Barry      | Allen     | barry@company.com    | 2          |
| 5           | Hal        | Jordan    | hal@company.com      | 2          |
| 6           | Arthur     | Curry     | arthur@company.com   | 3          |
+-------------+------------+-----------+----------------------+------------+
```

The hierarchy is:
- Diana (CEO) manages Bruce and Clark
- Bruce manages Barry and Hal
- Clark manages Arthur

### Self Join Query

To list each employee alongside their manager's name, you join the `employee` table to itself. The first instance (alias `e`) represents the employee, and the second instance (alias `m`) represents the manager.

```sql
SELECT
    e.first_name AS "Employee First Name",
    e.last_name AS "Employee Last Name",
    e.email AS "Employee Email",
    m.first_name AS "Manager First Name",
    m.last_name AS "Manager Last Name",
    m.email AS "Manager Email"
FROM employee AS e
LEFT OUTER JOIN employee AS m
    ON e.manager_id = m.employee_id;
```

### Expected Output

```
+---------------------+--------------------+----------------------+-------------------+------------------+-------------------+
| Employee First Name | Employee Last Name | Employee Email       | Manager First Name| Manager Last Name| Manager Email     |
+---------------------+--------------------+----------------------+-------------------+------------------+-------------------+
| Diana               | Prince             | diana@company.com    | NULL              | NULL             | NULL              |
| Bruce               | Wayne              | bruce@company.com    | Diana             | Prince           | diana@company.com |
| Clark               | Kent               | clark@company.com    | Diana             | Prince           | diana@company.com |
| Barry               | Allen              | barry@company.com    | Bruce             | Wayne            | bruce@company.com |
| Hal                 | Jordan             | hal@company.com      | Bruce             | Wayne            | bruce@company.com |
| Arthur              | Curry              | arthur@company.com   | Clark             | Kent             | clark@company.com |
+---------------------+--------------------+----------------------+-------------------+------------------+-------------------+
```

Diana has `NULL` values for the manager columns because her `manager_id` is `NULL`. The `LEFT OUTER JOIN` ensures that Diana is still included in the result. If you used an `INNER JOIN` instead, Diana would be excluded because there is no row in the `m` instance that matches `e.manager_id = m.employee_id` when `e.manager_id` is `NULL`.

## Why a Left Outer Join Is Usually Appropriate

In a self join on a hierarchical structure, the top-level node (the one with a `NULL` reference) will be excluded by an inner join. If you want to include all rows in the result, including those at the top of the hierarchy, use a `LEFT OUTER JOIN`. If you only want rows where the relationship exists (for example, only employees who have a manager), an `INNER JOIN` suffices.

```sql
-- Inner join: excludes employees with no manager
SELECT
    e.first_name,
    e.last_name,
    m.first_name AS manager_first_name
FROM employee AS e
INNER JOIN employee AS m
    ON e.manager_id = m.employee_id;

-- Left outer join: includes all employees
SELECT
    e.first_name,
    e.last_name,
    m.first_name AS manager_first_name
FROM employee AS e
LEFT OUTER JOIN employee AS m
    ON e.manager_id = m.employee_id;
```

## Self Join for Referral Systems

Another common use case is a referral system where each user has a `referred_by` column referencing another user's `user_id`:

```sql
CREATE TABLE user (
    user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    referred_by INT UNSIGNED,
    PRIMARY KEY (user_id),
    FOREIGN KEY (referred_by) REFERENCES user(user_id)
);

-- Self join to show each user and who referred them
SELECT
    u1.first_name AS "User First Name",
    u1.last_name AS "User Last Name",
    u1.email AS "User Email",
    u2.email AS "Referred By Email"
FROM user AS u1
LEFT OUTER JOIN user AS u2
    ON u1.referred_by = u2.user_id;
```

In this query, `u1` represents the user being referred and `u2` represents the referrer. The `LEFT OUTER JOIN` ensures that users who were not referred by anyone (the original users who signed up without a referral) are still included in the result.

## Self Join for Row Comparison

Self joins can also be used to compare rows within the same table. For example, to find all pairs of employees who work in the same department:

```sql
SELECT
    e1.first_name AS employee_1,
    e2.first_name AS employee_2,
    e1.department_id
FROM employee AS e1
INNER JOIN employee AS e2
    ON e1.department_id = e2.department_id
    AND e1.employee_id < e2.employee_id;
```

The condition `e1.employee_id < e2.employee_id` prevents duplicate pairs (A-B and B-A) and prevents matching an employee with themselves. This pattern is useful for finding duplicates, similarities, or relationships between rows in the same dataset.

## Summary

A self join is a powerful technique for working with hierarchical data, referral chains, and intra-table comparisons within a single table. It requires table aliases to distinguish between the two instances of the same table, as described in [[49 - Alias]]. The join condition in a self join typically matches a foreign key column in one instance with the primary key column in the other instance, establishing the relationship between rows. Choosing between `INNER JOIN` and `LEFT OUTER JOIN` depends on whether you want to include rows at the top of the hierarchy (those with `NULL` references). Self joins integrate seamlessly with the join concepts covered in [[42 - Inner Join]] and the aliasing techniques discussed in [[49 - Alias]].
