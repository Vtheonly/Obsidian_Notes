
# What an INNER JOIN really is

An INNER JOIN returns **only the rows where both tables match** according to the join condition.

The key rule is simple:

If no match exists on the ON condition, the row is _removed_.

```sql
A INNER JOIN B
```

means:

- Take row from A
    
- Find matching rows in B
    
- Keep only the ones that match
    

If there is no match, the row disappears.

---

# What the order of tables means in INNER JOIN

Most students think order matters.  
In INNER JOIN, **order does NOT matter logically**.

This:

```sql
SELECT *
FROM A
INNER JOIN B ON A.id = B.id;
```

is logically the same as:

```sql
SELECT *
FROM B
INNER JOIN A ON A.id = B.id;
```

Both produce the same rows.

Only exceptions where order _may_ matter:

- Query readability and mental organization
    
- When the DB optimizer chooses a different query plan for performance (internal, invisible to you)
    

But logically, **the result set is identical**.

---

# 10 INNER JOIN Examples

These examples progress from extremely simple to moderately advanced.

---

# 1. Match students to their department

### Student

|sid|name|depID|
|---|---|---|
|1|Sara|10|
|2|Amin|20|
|3|Leila|99|

### Department

|depID|depName|
|---|---|
|10|CS|
|20|Math|

### Query

```sql
SELECT S.name, D.depName
FROM Student S
INNER JOIN Department D
        ON S.depID = D.depID;
```

### Result

Leila disappears because depID 99 does not exist.

---

# 2. Match orders to customers

### Query

```sql
SELECT C.name, O.orderID
FROM Customer C
INNER JOIN Orders O
        ON C.id = O.customerID;
```

Only customers who made orders appear.

---

# 3. Products and their categories

```sql
SELECT P.label, C.categoryName
FROM Product P
INNER JOIN Category C
        ON P.categoryID = C.id;
```

A product with no category disappears.

---

# 4. Flights and their airports

```sql
SELECT F.flightCode, A.city
FROM Flight F
INNER JOIN Airport A
        ON F.airportID = A.airportID;
```

Only flights with a registered airport appear.

---

# 5. Employees and their managers (self join)

```sql
SELECT E.name AS employee,
       M.name AS manager
FROM Employee E
INNER JOIN Employee M
        ON E.managerID = M.empID;
```

Employees without managers vanish.

---

# 6. Books and authors

```sql
SELECT B.title, A.name
FROM Book B
INNER JOIN Author A
        ON B.authorID = A.authorID;
```

Books with a missing author do not show up.

---

# 7. Exams and enrolled students

```sql
SELECT St.name, Ex.subject
FROM Student St
INNER JOIN Exam Ex
        ON St.sid = Ex.sid;
```

Only students who took an exam appear.

---

# 8. Cities and their mayors

```sql
SELECT City.name, Mayor.name
FROM City
INNER JOIN Mayor
        ON City.id = Mayor.cityID;
```

If a city doesn’t have a mayor, it is excluded.

---

# 9. Posts and the users who wrote them

```sql
SELECT U.username, P.title
FROM UserAccount U
INNER JOIN Post P
        ON U.userID = P.userID;
```

Posts with missing users or orphan rows disappear.

---

# 10. Multi-table inner join (three tables)

Students → take exams → inside a classroom.

```sql
SELECT S.name, E.score, C.room
FROM Student S
INNER JOIN Exam E
        ON S.sid = E.sid
INNER JOIN Classroom C
        ON E.classroomID = C.cid;
```

A student appears only if:

- They have an exam record
    
- That exam has a valid classroom
    

Missing any connection removes the row.

---

# Final Summary

**INNER JOIN:**

- Keeps only matching rows from both tables
    
- Drops anything without a match
    
- Order of tables does _not_ change the logical results
    
- Used when you want strictly consistent relationships
    
- Self-join is a special case of inner join
    

If you want, I can also produce:

- A full Obsidian note combining INNER + OUTER + SELF joins
    
- A mega table showing the difference between INNER vs LEFT vs RIGHT vs FULL
    
- 10 practice exam-style problems with solutions