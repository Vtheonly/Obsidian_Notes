Below are **five simple, clear auto-join examples**.  
Each example includes a **mini table**, a **query**, and a **short explanation**.  
All are designed to be easy yet realistic, similar in spirit to your given example but different in scenario.

---

# Auto-Join Examples

A self-join is when a table is joined with itself under two different aliases.  
This allows comparing rows from the same table.

---

# 1. Find employees who have the same job title as employee #3

### Table: Employee

|empID|name|job|
|---|---|---|
|1|Sara|Engineer|
|2|Malik|Manager|
|3|Amina|Engineer|
|4|Yacine|Engineer|
|5|Rami|Manager|

### Query

```sql
SELECT E2.empID, E2.name
FROM   Employee E1, Employee E2
WHERE  E1.empID = 3
AND    E1.job = E2.job;
```

### Explanation

E1 locates the job of employee 3 (Engineer).  
E2 finds everyone else with the same job.

---

# 2. Find products that have the same price as product A12

### Table: Product

|code|label|price|
|---|---|---|
|A10|Keyboard|1500|
|A11|Mouse|800|
|A12|USB Hub|1500|
|A13|Webcam|3200|
|A14|Microphone|1500|

### Query

```sql
SELECT P2.code, P2.label
FROM   Product P1, Product P2
WHERE  P1.code = 'A12'
AND    P1.price = P2.price;
```

### Explanation

P1 isolates the price of A12.  
P2 finds all items with that same price.

---

# 3. Find students who are in the same department as student #22

### Table: Student

|id|name|department|
|---|---|---|
|20|Hadi|CS|
|21|Noor|Math|
|22|Samir|CS|
|23|Leila|Physics|
|24|Karim|CS|

### Query

```sql
SELECT S2.id, S2.name
FROM   Student S1, Student S2
WHERE  S1.id = 22
AND    S1.department = S2.department;
```

### Explanation

S1 locates Samir and his department.  
S2 searches for all students in the same department.

---

# 4. Find flights departing from the same city as flight F09

### Table: Flight

|code|departure|
|---|---|
|F01|Paris|
|F02|Rome|
|F09|Paris|
|F11|London|
|F12|Paris|

### Query

```sql
SELECT F2.code
FROM   Flight F1, Flight F2
WHERE  F1.code = 'F09'
AND    F1.departure = F2.departure;
```

### Explanation

F1 gives the departure of flight F09.  
F2 lists all flights with the same departure city.

---

# 5. Find books written in the same language as book #7

### Table: Book

|bookID|title|language|
|---|---|---|
|5|Dawn|Arabic|
|6|Rain|French|
|7|Echoes|Arabic|
|8|Stars|English|
|9|Roots|Arabic|

### Query

```sql
SELECT B2.bookID, B2.title
FROM   Book B1, Book B2
WHERE  B1.bookID = 7
AND    B1.language = B2.language;
```

### Explanation

B1 selects the language of book 7.  
B2 returns other books written in that language.

---

If you want, I can also give you **5 harder examples**, **graphical diagrams**, or turn these into **Obsidian-ready notes**.