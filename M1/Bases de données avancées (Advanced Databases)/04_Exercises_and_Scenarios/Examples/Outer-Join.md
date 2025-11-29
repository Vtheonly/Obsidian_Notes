Below is a clean, direct explanation of **Outer Join**, followed by **one very simple example** and **one slightly smarter example**.  
Style stays technical, descriptive, and clear.

---

# Outer Join

An outer join returns **all rows from one table**, even if there is **no matching row** in the other table.

There are three types:

1. **Left Outer Join**  
    Returns all rows from the left table and the matching rows from the right table.  
    If no match exists, the right side becomes NULL.
    
2. **Right Outer Join**  
    Returns all rows from the right table and matching rows from the left table.
    
3. **Full Outer Join**  
    Returns all rows from both tables.  
    Matches where possible; otherwise the opposite side becomes NULL.
    

Relational algebra uses the symbol ⟕ for left-join, ⟖ for right-join, and ⟗ for full-join.

---

# Dumb and extremely simple example

### Goal

Show customers even if they never made an order.

### Table: Customer

|id|name|
|---|---|
|1|Sara|
|2|Adam|
|3|Lina|

### Table: Order

|orderID|customerID|total|
|---|---|---|
|10|1|2000|
|11|1|3500|
|12|3|500|

### Query

```sql
SELECT C.id, C.name, O.total
FROM   Customer C
LEFT OUTER JOIN Order O
       ON C.id = O.customerID;
```

### Result

|id|name|total|
|---|---|---|
|1|Sara|2000|
|1|Sara|3500|
|2|Adam|NULL|
|3|Lina|500|

### What happened

Adam has no orders, but he still appears because a **left outer join** keeps all rows from Customer.

---

# Slightly smarter example

### Goal

Find all employees and show the project they are assigned to.  
Employees without projects must still appear.

### Table: Employee

|empID|name|
|---|---|
|1|Amina|
|2|Yacine|
|3|Rami|
|4|Selma|

### Table: ProjectAssignment

|projectID|empID|role|
|---|---|---|
|P01|1|Developer|
|P02|3|Tester|

### Query

```sql
SELECT E.empID, E.name, P.projectID, P.role
FROM   Employee E
LEFT OUTER JOIN ProjectAssignment P
       ON E.empID = P.empID;
```

### Result

|empID|name|projectID|role|
|---|---|---|---|
|1|Amina|P01|Developer|
|2|Yacine|NULL|NULL|
|3|Rami|P02|Tester|
|4|Selma|NULL|NULL|

### Explanation

The join keeps all employees, even those who are not assigned to a project.  
This is the typical real-world use of outer join: **listing everything on one side**, with optional details from the other.

Here are **five more outer-join examples**, each with **two small tables**, **the query**, and **a clear explanation**.  
The difficulty increases slightly as you go down.

---

# 1. Show all departments, even empty ones

### Department

|depID|name|
|---|---|
|10|HR|
|20|Finance|
|30|Marketing|

### Employee

|empID|name|depID|
|---|---|---|
|1|Sara|10|
|2|Malik|10|
|3|Hana|20|

### Query

```sql
SELECT D.depID, D.name, E.empID, E.name
FROM   Department D
LEFT OUTER JOIN Employee E
       ON D.depID = E.depID;
```

### Explanation

Marketing has no employees, but still appears with NULL values.

---

# 2. List all courses and show which student is enrolled

### Course

|cid|title|
|---|---|
|1|Math|
|2|CS|
|3|Physics|

### Enrollment

|cid|student|
|---|---|
|1|Karim|
|3|Nabil|

### Query

```sql
SELECT C.cid, C.title, E.student
FROM   Course C
LEFT OUTER JOIN Enrollment E
       ON C.cid = E.cid;
```

### Explanation

Course 2 (CS) has no students, but still appears.

---

# 3. Show all payments and match them with receipts

Useful when payments might not have a receipt yet.

### Payment

|pid|amount|
|---|---|
|1|1000|
|2|2000|
|3|500|

### Receipt

|rid|pid|date|
|---|---|---|
|10|1|2024-01-02|

### Query

```sql
SELECT P.pid, P.amount, R.date
FROM   Payment P
LEFT OUTER JOIN Receipt R
       ON P.pid = R.pid;
```

### Explanation

Payments 2 and 3 appear with NULL receipts.

---

# 4. Show all teachers and their assigned classrooms

Some teachers have no classroom.

### Teacher

|tid|name|
|---|---|
|1|Idris|
|2|Leila|
|3|Younes|

### Classroom

|room|teacherID|
|---|---|
|A101|1|

### Query

```sql
SELECT T.tid, T.name, C.room
FROM   Teacher T
LEFT OUTER JOIN Classroom C
       ON T.tid = C.teacherID;
```

### Explanation

Leila and Younes appear with NULL rooms.

---

# 5. List all items and their discount if applicable

A practical case when only a few products have discounts.

### Item

|itemID|label|price|
|---|---|---|
|1|Monitor|50000|
|2|Keyboard|3000|
|3|Headphones|8000|

### Discount

|itemID|percent|
|---|---|
|1|20|

### Query

```sql
SELECT I.itemID, I.label, I.price, D.percent
FROM   Item I
LEFT OUTER JOIN Discount D
       ON I.itemID = D.itemID;
```

### Explanation

Only the Monitor has a discount.  
Keyboard and Headphones appear with NULL discount values.

---

If you want, I can add:

- Right join versions of the same examples
    
- Three full outer join examples
    
- Exercises similar to your exam
    
- A full Obsidian note combining auto join + outer join with diagrams and practice questions