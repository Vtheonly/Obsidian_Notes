# Parent Tables and Child Tables

In relational database design, every relationship between tables involves a parent table and a child table. Understanding which table is the parent and which is the child is not merely a labeling exercise; it determines where foreign keys are placed, how referential integrity works, and whether certain records can exist independently. This distinction is foundational to correct schema design and affects every aspect of how tables relate to one another.

## Defining Parent and Child Tables

The **parent table** is the table that is referenced by another table. It contains the primary key that serves as the target of a foreign key reference. The **child table** is the table that contains the foreign key pointing back to the parent. The child depends on the parent for its context and identity within the relationship. Without the parent, the child's foreign key reference would be meaningless.

This relationship mirrors the real-world concept of parent and child. A child inherits characteristics from a parent and depends on the parent for existence. In a database, the child inherits the value of the parent's primary key as its foreign key. If the parent's primary key is 86, the child's foreign key is also 86, establishing the link between them. The child always knows who its parent is, but the parent does not inherently know about all of its children.

## Foreign Key Placement

The most important practical implication of the parent-child distinction is the placement of the foreign key. The foreign key always goes in the child table, never in the parent table. This is because the child is the dependent entity that needs to reference its parent. The parent is the independent entity that does not need to know about its children directly.

```
parent_table (users)          child_table (comments)
+---------+----------+       +------------+---------+----------+
| user_id | username |       | comment_id | user_id | content  |
+---------+----------+       +------------+---------+----------+
| 1       | alice    |<------| 101        | 1       | Hello    |
| 2       | bob      |       | 102        | 1       | World    |
+---------+----------+       | 103        | 2       | Hi       |
                             +------------+---------+----------+
```

The `user_id` column in the comments table is the foreign key. Each comment points back to exactly one user. Multiple comments can point to the same user, but each comment has only one parent. This directional reference from child to parent is the structural backbone of one-to-many relationships.

## Weak Entities and Identifying Relationships

A **weak entity** is a child entity that cannot exist without its parent. Its very identity depends on the parent. For example, an order line item cannot exist without an order. If you delete the order, all of its line items become meaningless and should also be deleted. This is called an **identifying relationship** because the parent's primary key is part of the child's primary key.

In contrast, a **strong entity** can exist independently. A department can exist even if it currently has no employees. The department does not depend on employees for its existence. When a child is a strong entity, the relationship is **non-identifying**: the parent's primary key becomes a foreign key in the child but is not part of the child's primary key.

**Identifying relationship example (weak entity):**

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL
);

CREATE TABLE order_items (
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

The `order_items` table uses `order_id` as part of its composite primary key. Without the order, the line item has no identity. This is an identifying relationship.

**Non-identifying relationship example (strong entity):**

```sql
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    dept_id INT,
    emp_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
```

The `employees` table has its own independent primary key (`emp_id`). The `dept_id` is a foreign key but not part of the primary key. An employee can exist (temporarily) without being assigned to a department, making this a non-identifying relationship.

## How Parent-Child Determines Foreign Key Placement

When analyzing a relationship between two entities, ask yourself which entity depends on the other. The dependent entity is the child, and the independent entity is the parent. The foreign key goes in the child table, pointing back to the parent.

Consider the relationship between a user and an order. An order cannot exist without a user who placed it. The order depends on the user. Therefore, the user is the parent and the order is the child. The foreign key (user_id) goes in the orders table.

Consider the relationship between a comment and a video. A comment cannot exist without a video to comment on. The comment depends on the video. Therefore, the video is the parent and the comment is the child. The foreign key (video_id) goes in the comments table.

This dependency analysis works consistently: whichever entity would be meaningless without the other is the child, and it receives the foreign key.

## Directional Awareness

An important property of parent-child relationships is that they are directional. Given a child record, you can always determine its parent by following the foreign key. Given a parent record, however, you cannot directly determine its children without querying the child table. This asymmetry has practical implications for query design and application logic.

When you see a comment on a website, you can immediately identify who posted it because the comment stores the author's identity. But when you view a user profile, you typically need a separate query or feed to display all of their comments. The child points to the parent, not the other way around.

## See Also

- [[06 - Designing One-to-Many Relationships]] - Practical design patterns using parent-child relationships
- [[03 - One-to-Many Relationships]] - The relationship type most commonly associated with parent-child structures
- [[01 - Introduction to Keys]] - Understanding primary keys and foreign keys in depth
