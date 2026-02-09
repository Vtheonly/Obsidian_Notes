
# Master Class: Database Views (Vues)

**Course Context:** Bases de Données Avancées (Master 1)
**Sources:** *Chapitre 2 (Contrôle de données), TD N°2 (Ventes), TD N°3 (Missions)*

---

## Part 1: Theoretical Foundations

### 1.1 What is a View?
Based on **Source 10 (Chapitre 2 - Slide 4)**, a view is a **Virtual Table**.
*   **Storage:** Unlike a standard table, a view **does not store data physically** (with the exception of Materialized Views, which are not covered here).
*   **Definition:** It is stored in the Data Dictionary essentially as a saved `SELECT` query.
*   **Behavior:** When you query a view, the SGBD effectively runs the underlying query in real-time.

### 1.2 Why use Views?
The course highlights three main objectives:
1.  **Security (Confidentiality):** Restrict access to specific rows (e.g., only employees in Algiers) or specific columns (e.g., hide salaries).
2.  **Simplification:** Hide complex joins or calculations. The user queries a simple view instead of writing a 20-line SQL statement.
3.  **Data Independence:** If the structure of the base tables changes, you can modify the view definition so the user application doesn't break.

### 1.3 Syntax
```sql
CREATE VIEW <nom_vue> [(alias_col1, alias_col2...)]
AS <Requête_SQL_SELECT>
[WITH CHECK OPTION];
```

> [!WARNING] Restrictions on Creation
> According to **Source 10**, the sub-query defining the view generally cannot contain an `ORDER BY` clause (sorting is done when *querying* the view, not creating it).

---

## Part 2: Views for Security (Access Control)

This is the most critical aspect covered in **Chapitre 2**. A view allows you to give a user a "window" into the data without giving them the keys to the whole house.

### 2.1 Column-Level Security (Vertical Filtering)
**Scenario:** You want User U1 to see Employee Names, but **not** their salaries.

**Solution:**
```sql
CREATE VIEW V_Public_Emp AS
SELECT Name, Function, Email -- Salary is omitted
FROM Employees;

GRANT SELECT ON V_Public_Emp TO U1;
```
*Result:* If U1 tries `SELECT * FROM Employees`, access is denied. If U1 does `SELECT * FROM V_Public_Emp`, they see the allowed data.

### 2.2 Row-Level Security (Horizontal Filtering)
**Source 10 (Example 10 & 14)** demonstrates filtering specific rows.

**Scenario:** Restrict access to the table `CLIENT` to only show clients living in 'ALGER'.
```sql
CREATE VIEW CLIENTS_ALGER AS
SELECT * 
FROM CLIENT 
WHERE Adresse = 'ALGER';
```

**Advanced Scenario (Context-Aware Views):**
**Source 10 (Example 14)** shows how to restrict data based on the environment (e.g., terminal ID or Time).
```sql
-- View that only shows data if accessed from Terminal 'T100'
CREATE VIEW V_Secure AS
SELECT * FROM T 
WHERE userenv('TERMINAL') = 'T100';
```

---

## Part 3: The "WITH CHECK OPTION" Clause

This is a subtle but crucial concept mentioned in **Source 10 (Slide 4)**.

### The Problem
If you create a view `CLIENTS_ALGER` (defined by `WHERE City='Alger'`), a user might theoretically try to insert a client living in 'ORAN' through that view.
*   Without `CHECK OPTION`: The insert succeeds, but the row immediately disappears from the view (because it doesn't match the filter).
*   This is confusing and potentially dangerous.

### The Solution
```sql
CREATE VIEW CLIENTS_ALGER AS
SELECT * FROM CLIENT WHERE Adresse = 'ALGER'
WITH CHECK OPTION;
```
*   **Effect:** The SGBD checks every `INSERT` or `UPDATE` made through the view.
*   **Result:** If you try to insert `Adresse = 'ORAN'`, the database throws an error and rejects the operation. It enforces the view's integrity.

---

## Part 4: Solved Exercises (Deep Dive)

Here we apply the concepts to the specific scenarios found in your TDs.

### Exercise 1: Complex Access Control Matrix
**Source:** Chapitre 2 (Example 12)

**Scenario:**
*   Table `T1(a1, a2, a3, a4, a5)`
*   Table `T2(b1, b2, b3)`

**Q1. Restrict User U1 to columns a1, a2 of T1 where condition 'COND' is true.**
```sql
-- 1. Create the Window
CREATE VIEW V1 AS 
SELECT a1, a2 
FROM T1 
WHERE COND; -- e.g., a1 > 100

-- 2. Give the Key
GRANT SELECT ON V1 TO U1;
```

**Q2. Restrict User U2 to columns a4, a5 of T1 (No condition).**
```sql
CREATE VIEW V2 AS 
SELECT a4, a5 
FROM T1;

GRANT SELECT ON V2 TO U2;
```

**Q3. Complex Chain: User U3 needs a join between V2 and T2.**
*   *Requirement:* U3 needs columns `a4, a5` (from V2) and `b1, b2` (from T2), joined where `a4 = b1`.
*   *Reasoning:* You can build a view on top of another view.
```sql
CREATE VIEW V3 AS
SELECT V2.a4, V2.a5, T2.b1, T2.b2
FROM V2, T2
WHERE V2.a4 = T2.b1;

GRANT SELECT ON V3 TO U3;
```
> [!TIP] Diagram of Dependency
> User U3 -> Query V3 -> (Queries V2 + Queries T2) -> (Queries T1).

---

### Exercise 2: Simplification & Aggregation
**Source:** TD N°3 (Missions) - Corrections

In this TD, views are used to solve SQL problems that are impossible or very hard to do in a single nested query (specifically regarding Aggregates).

**Q11. Who is the "Chef de Service" who has traveled the most kilometers?**
*   *The Difficulty:* We need to calculate the sum of kilometers for *each* chef (`SUM`), and then find the *maximum* of those sums (`MAX`). SQL standard forbids `MAX(SUM(km))`.
*   *The View Solution:* Break it into steps.

**Step 1: Create a View to calculate totals per Chef.**
```sql
CREATE VIEW R11 AS 
SELECT 
    chef.SRV_Libelle, 
    chef.EMP_Num, 
    chef.EMP_Nom, 
    SUM(m.MIS_KlmRetour - m.MIS_KlmDepart) AS NbKil
FROM chef, MISSION m
WHERE chef.EMP_Num = m.EMP_Num
GROUP BY chef.SRV_Libelle, chef.EMP_Num, chef.EMP_Nom;
```
*Note:* The view `chef` was created in a previous question to isolate managers.

**Step 2: Query the View.**
```sql
SELECT * 
FROM R11 
WHERE NbKil = (SELECT MAX(NbKil) FROM R11);
```
*   **Reasoning:** The view acts as a temporary storage of the "Sum" results. We can then easily find the "Max" from that storage.

---

### Exercise 3: Views for Intermediate Sets (Relational Division)
**Source:** TD N°2 (Ventes/Papeterie) - Questions 20 & 21

**Q20. Select articles sold by ALL shops.**
This is a classic "Relational Division" problem. Writing this in one block is messy. Views make it clean.

**Step 1: Create a View of distinct (Article, Shop) pairs.**
```sql
CREATE VIEW V20 AS
SELECT DISTINCT art_num, mag_num 
FROM VENTES;
```

**Step 2: Count shops per article vs Total shops.**
```sql
SELECT V.art_num, A.art_nom
FROM V20 V, ARTICLES A
WHERE V.art_num = A.art_num
GROUP BY V.art_num, A.art_nom
HAVING COUNT(*) = (SELECT COUNT(*) FROM MAGASINS);
```
*   **Reasoning:** If an article is found in the `V20` view associated with 5 different shops, and the total number of shops in the database is 5, then that article was sold by all shops.

**Q21. Shops with the highest turnover (Chiffre d'affaire) last month.**
Similar to the "Chef" example in TD3, we need to compare a Sum against a Max of Sums.

**Step 1: View for Turnover per Store.**
```sql
CREATE VIEW V21 AS
SELECT mag_num, SUM(vnt_montant) AS Chiffre_Affaire
FROM VENTES
WHERE to_char(vnt_date, 'MM') = to_char(add_months(sysdate, -1), 'MM') -- Last Month logic
GROUP BY mag_num;
```

**Step 2: Select the Max.**
```sql
SELECT mag_loc, mag_ger, Chiffre_Affaire
FROM V21 V, MAGASINS M
WHERE V.mag_num = M.mag_num
AND Chiffre_Affaire = (SELECT MAX(Chiffre_Affaire) FROM V21);
```

---

## Part 5: Managing Views (DDL)

### 5.1 Modification
Standard SQL doesn't have an easy "ALTER VIEW" to change the definition logic (in older versions). You usually use:
```sql
CREATE OR REPLACE VIEW nom_vue AS ...
```
This overwrites the old definition with the new one without dropping permissions.

### 5.2 Dropping
```sql
DROP VIEW nom_vue;
```
*   **Impact:** This deletes the definition from the dictionary. It does **not** delete the data in the underlying tables.

### 5.3 Updates through Views (LMD)
Can you `INSERT` into a view?
**Source 10 (Slide 4)** provides specific rules:
1.  **YES**, if the view is simple (1 table, no functions).
2.  **NO**, if the view contains:
    *   `GROUP BY`
    *   Aggregate Functions (`SUM`, `AVG`, etc.)
    *   `DISTINCT`
    *   Joins (often restricted, or only one side of the join is updatable).

**Reasoning:** If a view shows `SUM(Salary)`, and you try to change that sum to 5000, the database doesn't know which specific employee rows to update to achieve that total. Therefore, it is ambiguous and forbidden.

---

## Summary Checklist for Exams

1.  **Syntax:** `CREATE VIEW x AS SELECT ...`
2.  **Security:** Used with `GRANT` to limit access.
3.  **Aggregates:** Used to solve "Max of Sums" problems (create view for Sum, query view for Max).
4.  **Integrity:** `WITH CHECK OPTION` prevents inserting data that disappears from the view.
5.  **Limitations:** Cannot update views with `GROUP BY` or Aggregates.
