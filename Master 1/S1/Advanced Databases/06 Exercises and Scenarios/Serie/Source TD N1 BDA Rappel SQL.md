Here is the first batch of 5 exercises, focusing on **TD N° 1 BDA : Rappel SQL** (The Car Dealership Database).

**Context Schema:**
*   `FOURN (NF, NomF, Code, VilleF)`
*   `REVEND (NR, NomR, VilleR)`
*   `VOITURE (NV, NomV, Couleur, Prix)`
*   `FVR (NF, NV, NR, Qté)` - *Association Table (Supplier-Car-Dealer)*

---

### Exercise 1: Information on All Dealers

**Source:** TD N° 1 BDA : Rappel SQL - Question 1
**Question:** "Donnez tous les renseignements sur tous les revendeurs." (Give all details about all dealers.)

#### 1. Solution
```sql
SELECT * 
FROM REVEND;
```

#### 2. Reasoning
The request asks for "all details" (all columns) and "all dealers" (all rows) without any specific filtering condition. In SQL, the wildcard `*` selects every column defined in the table schema.

#### 3. Detailed Explanation
*   **`SELECT *`**: This tells the database engine to retrieve data from every column (`NR`, `NomR`, `VilleR`) available in the table. It is equivalent to writing `SELECT NR, NomR, VilleR`.
*   **`FROM REVEND`**: Specifies the target table.
*   **Note:** While `SELECT *` is convenient for ad-hoc queries, in production applications (like Java or PHP apps), it is often better to list specific columns explicitly. This prevents the application from breaking if a new column is added to the database later.

---

### Exercise 2: Dealers in London

**Source:** TD N° 1 BDA : Rappel SQL - Question 2
**Question:** "Donnez tous les renseignements sur les revendeurs habitant Londres." (Give all details about dealers living in London.)

#### 1. Solution
```sql
SELECT * 
FROM REVEND 
WHERE VilleR = 'LONDRES';
```

#### 2. Reasoning
We need to filter the rows based on a specific attribute value. The condition corresponds to the column `VilleR`. Since "LONDRES" is a string literal, it must be enclosed in single quotes.

#### 3. Detailed Explanation
*   **`WHERE` Clause**: This clause acts as a filter. The database engine scans the `REVEND` table and evaluates the condition `VilleR = 'LONDRES'` for each row.
*   **String Sensitivity**: In standard SQL, string comparisons can be case-sensitive depending on the collation of the database. If 'Londres' is stored as 'London' or 'LONDRES', the query must match exactly unless a function like `UPPER()` is used.
*   **Result**: Only the tuples (rows) where the city matches exactly are returned in the result set.

---

### Exercise 3: Suppliers for Dealer R1

**Source:** TD N° 1 BDA : Rappel SQL - Question 3
**Question:** "Quels sont les numéros des fournisseurs fournissant des voitures au revendeur R1 ?" (Which supplier numbers supply cars to dealer R1?)

#### 1. Solution
```sql
SELECT DISTINCT NF 
FROM FVR 
WHERE NR = 'R1';
```

#### 2. Reasoning
The relationship between suppliers and dealers is stored in the association table `FVR`. We do not need the names of the suppliers, only their numbers (`NF`), so we do not need to join with the `FOURN` table. A dealer might receive multiple deliveries from the same supplier, so `DISTINCT` is required to remove duplicates.

#### 3. Detailed Explanation
*   **Target Table**: `FVR` contains the links between `NF` (Supplier), `NV` (Car), and `NR` (Dealer).
*   **Condition**: `NR = 'R1'` filters entries specifically for dealer R1.
*   **`DISTINCT`**: If Supplier F1 supplied a car to R1 on Monday and another car on Tuesday, F1 appears twice in the `FVR` table for R1. The question asks "Which suppliers", implying a set of unique identifiers. `DISTINCT` ensures F1 is listed only once.

---

### Exercise 4: Suppliers of Car V1 to Dealer R1

**Source:** TD N° 1 BDA : Rappel SQL - Question 4
**Question:** "Quels sont les numéros des fournisseurs qui fournissent des voitures V1 au revendeur R1 ?" (Which supplier numbers supply car V1 to dealer R1?)

#### 1. Solution
```sql
SELECT DISTINCT NF 
FROM FVR 
WHERE NR = 'R1' 
  AND NV = 'V1';
```

#### 2. Reasoning
This is a refinement of the previous query. We now have two conditions that must be true simultaneously: the dealer must be 'R1' AND the car product must be 'V1'.

#### 3. Detailed Explanation
*   **`AND` Operator**: Logical operators combine conditions. Both `NR='R1'` and `NV='V1'` must be satisfied for a row to be selected.
*   **Index Usage**: In a real-world scenario, a composite index on `(NR, NV)` would make this query extremely fast because the database could jump directly to the relevant pointers without scanning the whole table.
*   **Data Integrity**: This query assumes 'V1' and 'R1' exist. If they don't, the result is simply an empty set (no error).

---

### Exercise 5: Names of Dealers Supplied by F1

**Source:** TD N° 1 BDA : Rappel SQL - Question 5
**Question:** "Quels sont les noms des revendeurs dont l’un des fournisseurs est F1 ?" (What are the names of the dealers where one of the suppliers is F1?)

#### 1. Solution
**Option A (Using Join):**
```sql
SELECT DISTINCT R.NomR 
FROM REVEND R
JOIN FVR L ON R.NR = L.NR
WHERE L.NF = 'F1';
```

**Option B (Using Subquery):**
```sql
SELECT NomR 
FROM REVEND 
WHERE NR IN (SELECT NR FROM FVR WHERE NF = 'F1');
```

#### 2. Reasoning
The information is split across two tables:
1.  `REVEND` contains the names (`NomR`).
2.  `FVR` contains the supply logic (`NF` -> `NR`).
We must link these tables using the common key `NR` (Dealer Number).

#### 3. Detailed Explanation
*   **Join Logic (Option A)**:
    *   We create a Cartesian product of `REVEND` and `FVR`.
    *   We filter to keep only rows where the Dealer Numbers match (`R.NR = L.NR`).
    *   We filter again to keep only rows where the supplier is 'F1'.
    *   `DISTINCT` is crucial here because if F1 made 10 deliveries to the same dealer, the join would produce the dealer's name 10 times.
*   **Subquery Logic (Option B)**:
    *   The inner query `(SELECT NR FROM FVR WHERE NF = 'F1')` builds a list of IDs (e.g., 'R1', 'R2').
    *   The outer query selects the names of dealers whose ID is inside that list.
    *   This approach is often more readable for "set membership" questions ("Is this dealer in the set of F1's clients?").





### Exercise 6: Dealers With No Deliveries

**Source:** TD N° 1 BDA : Rappel SQL - Question 6
**Question:** "Quels sont les noms des revendeurs pour lesquels aucune voiture n’est fournie ?" (What are the names of the dealers to whom no car is supplied?)

#### 1. Solution
```sql
SELECT NomR 
FROM REVEND 
WHERE NR NOT IN (SELECT DISTINCT NR FROM FVR);
```
*Alternative (Using NOT EXISTS):*
```sql
SELECT NomR 
FROM REVEND R
WHERE NOT EXISTS (SELECT 1 FROM FVR F WHERE F.NR = R.NR);
```

#### 2. Reasoning
We need to find dealers present in the `REVEND` table but *missing* from the `FVR` (supply) table. This is a classic "set difference" problem (A - B).

#### 3. Detailed Explanation
*   **`NOT IN` Logic**:
    *   The subquery `SELECT DISTINCT NR FROM FVR` generates the list of all "active" dealers (those who have received at least one car).
    *   The outer query selects dealers whose ID is NOT in that list.
*   **Potential Pitfall (NULLs)**: If the column `FVR.NR` allowed NULL values, `NOT IN` would fail (it would return an empty set because `val != NULL` is unknown). Since `NR` is part of a primary key in `REVEND`, it is implicitly not null, but `NOT EXISTS` is generally safer and often more performant in modern optimizers.
*   **`NOT EXISTS` Logic**: For every dealer in `REVEND`, the database checks the `FVR` table. If it finds *no* rows linking to that dealer, the condition is true.

---

### Exercise 7: Suppliers for Both R1 and R2

**Source:** TD N° 1 BDA : Rappel SQL - Question 7
**Question:** "Quels sont les numéros des fournisseurs qui fournissent chacun simultanément des voitures pour les revendeurs R1 et R2 ?" (Which supplier numbers supply cars to BOTH dealer R1 and dealer R2?)

#### 1. Solution
```sql
SELECT NF 
FROM FVR 
WHERE NR = 'R1'
INTERSECT
SELECT NF 
FROM FVR 
WHERE NR = 'R2';
```
*Alternative (SQL Standard - Self Join):*
```sql
SELECT DISTINCT T1.NF 
FROM FVR T1 
JOIN FVR T2 ON T1.NF = T2.NF 
WHERE T1.NR = 'R1' AND T2.NR = 'R2';
```

#### 2. Reasoning
This requires an intersection of two sets:
1.  Set A: Suppliers who supply R1.
2.  Set B: Suppliers who supply R2.
We need suppliers found in *both* A and B.

#### 3. Detailed Explanation
*   **`INTERSECT`**: This set operator explicitly returns values common to both result sets. It is clean and mathematically precise.
*   **Self-Join approach**:
    *   We look at the table `FVR` twice (aliased as T1 and T2).
    *   We join T1 and T2 on the Supplier Number (`NF`), meaning "we are talking about the same supplier".
    *   We apply the condition: In instance T1, the dealer is R1. In instance T2, the dealer is R2.
    *   This proves that supplier `NF` exists in both contexts.

---

### Exercise 8: Suppliers of Red Cars to R1

**Source:** TD N° 1 BDA : Rappel SQL - Question 8
**Question:** "Quels sont les numéros des fournisseurs qui fournissent au moins une voiture rouge au revendeur R1 ?" (Which supplier numbers supply at least one red car to dealer R1?)

#### 1. Solution
```sql
SELECT DISTINCT F.NF 
FROM FVR F
JOIN VOITURE V ON F.NV = V.NV
WHERE F.NR = 'R1' 
  AND V.Couleur = 'ROUGE';
```

#### 2. Reasoning
We need to link the supply chain (`FVR`) with product details (`VOITURE`). The filtering criteria apply to both tables: the dealer (`FVR.NR`) and the car attribute (`VOITURE.Couleur`).

#### 3. Detailed Explanation
*   **Join Operation**: `FVR` connects suppliers to cars (`NV`). `VOITURE` connects cars to colors. By joining `F.NV = V.NV`, we associate the color "Red" with the transaction.
*   **Composite Condition**: The `WHERE` clause acts as a double filter. We only care about rows where *both* the recipient is R1 *and* the object received is Red.
*   **Optimization**: The database optimizer will likely filter `NR='R1'` first (using an index on FVR) and then look up the car color, rather than checking all red cars first, as R1 transactions are likely fewer than total red cars in the database.

---

### Exercise 9: Cars Supplied to All London Dealers

**Source:** TD N° 1 BDA : Rappel SQL - Question 9
**Question:** "Donnez les numéros des voitures fournies pour tous les revendeurs de Londres ?" (Give the car numbers supplied to ALL dealers in London?)

#### 1. Solution
*(This is a classic Relational Division problem)*

```sql
SELECT V.NV
FROM VOITURE V
WHERE NOT EXISTS (
    -- Find a London dealer...
    SELECT R.NR 
    FROM REVEND R 
    WHERE R.VilleR = 'LONDRES'
    AND NOT EXISTS (
        -- ...to whom this car (V.NV) has NOT been supplied.
        SELECT 1 
        FROM FVR F 
        WHERE F.NR = R.NR 
          AND F.NV = V.NV
    )
);
```

#### 2. Reasoning
The query asks for cars where the set of "London Dealers supplied with this car" contains the set of "All London Dealers".
In SQL, we rephrase "All X are Y" as "There is no X that is NOT Y".
*Translation:* Find cars such that there does not exist a London dealer who has *not* received this car.

#### 3. Detailed Explanation
*   **Outer Query**: Iterates through every car `V.NV`.
*   **Middle Query**: Finds all dealers in London.
*   **Inner Query**: Checks if there is a supply record (`FVR`) linking the current car (`V.NV`) to the current London dealer (`R.NR`).
*   **Logic Flow**:
    1.  Pick a car.
    2.  Look for a "Counter-Example": A London dealer who *didn't* get this car.
    3.  If no counter-example is found (`NOT EXISTS` returns true), then the car was supplied to everyone.

---

### Exercise 10: Suppliers of Red Cars to Paris or London

**Source:** TD N° 1 BDA : Rappel SQL - Question 10
**Question:** "Quels sont les numéros des fournisseurs qui fournissent des voitures rouges pour des revendeurs situés à Paris et Londres ?" (Which supplier numbers supply red cars to dealers located in Paris AND London?)
*(Note: The French phrasing "Paris et Londres" implies the set of target cities is {Paris, London}, but usually in SQL contexts, we interpret this as supplying to a dealer in Paris OR a dealer in London, OR supplying to BOTH distinct locations. Given typical exam patterns, let's assume the question implies suppliers active in this **zone** (Union of cities). However, if it implies "Suppliers who have clients in Paris AND clients in London", that is an Intersection problem).*

**Interpretation A (Union - Most likely simple filter):** "Suppliers supplying red cars to dealers in Paris or London".
**Interpretation B (Intersection - Strict):** "Suppliers who supply at least one red car to Paris AND at least one red car to London".

#### 1. Solution (Interpretation A - Union/List)
```sql
SELECT DISTINCT F.NF 
FROM FVR F
JOIN REVEND R ON F.NR = R.NR
JOIN VOITURE V ON F.NV = V.NV
WHERE V.Couleur = 'ROUGE'
  AND R.VilleR IN ('PARIS', 'LONDRES');
```

#### 1. Solution (Interpretation B - Intersection)
```sql
SELECT NF FROM FVR F, REVEND R, VOITURE V 
WHERE F.NR=R.NR AND F.NV=V.NV AND V.Couleur='ROUGE' AND R.VilleR='PARIS'
INTERSECT
SELECT NF FROM FVR F, REVEND R, VOITURE V 
WHERE F.NR=R.NR AND F.NV=V.NV AND V.Couleur='ROUGE' AND R.VilleR='LONDRES';
```

#### 2. Reasoning
We need three tables: `FVR` (Link), `REVEND` (City), `VOITURE` (Color).
*   **Interpretation A**: Simply filters rows where City is Paris OR London.
*   **Interpretation B**: Ensures the supplier appears in the "Paris Red Car" dataset AND the "London Red Car" dataset.

#### 3. Detailed Explanation
*   **Triple Join**: We join `FVR` to `REVEND` to check the city, and to `VOITURE` to check the color.
*   **`IN` Operator**: `R.VilleR IN ('PARIS', 'LONDRES')` is shorthand for `R.VilleR = 'PARIS' OR R.VilleR = 'LONDRES'`.
*   This effectively finds any transaction matching the criteria. If a supplier sends a Red car to Paris, they are selected. If they send one to London, they are selected.





### Exercise 11: Cars from Local Suppliers

**Source:** TD N° 1 BDA : Rappel SQL - Question 11
**Question:** "Quels sont les numéros des voitures dont les fournisseurs habitent la ville où est situé le revendeur auquel ces voitures sont destinées ?" (Which car numbers are supplied by suppliers who live in the same city as the dealer receiving the car?)

#### 1. Solution
```sql
SELECT DISTINCT FVR.NV
FROM FVR
JOIN FOURN F ON FVR.NF = F.NF
JOIN REVEND R ON FVR.NR = R.NR
WHERE F.VilleF = R.VilleR;
```

#### 2. Reasoning
This query requires comparing attributes from two different entities (`FOURN` and `REVEND`) that are linked by a transaction (`FVR`). We need to check if `Supplier.City` equals `Dealer.City`.

#### 3. Detailed Explanation
*   **Data Path**:
    1.  Start with the transaction table `FVR`.
    2.  Join `FOURN` to get the supplier's city (`VilleF`).
    3.  Join `REVEND` to get the dealer's city (`VilleR`).
*   **Condition**: The `WHERE` clause `F.VilleF = R.VilleR` enforces the "local supply" constraint.
*   **`DISTINCT`**: A specific car model (e.g., 'V1') might be supplied locally in Paris (F1->R1) and non-locally in London (F4->R5). If it is supplied locally at least once, it appears in the result. `DISTINCT` prevents duplicate car numbers if multiple local transactions occur for the same car type.

---

### Exercise 12: Dealers with Non-Local Suppliers

**Source:** TD N° 1 BDA : Rappel SQL - Question 12
**Question:** "Donnez les numéros des revendeurs dont un fournisseur au moins n’habite pas la ville où est situé ce revendeur." (Give the numbers of dealers who have at least one supplier not living in the dealer's city.)

#### 1. Solution
```sql
SELECT DISTINCT FVR.NR
FROM FVR
JOIN FOURN F ON FVR.NF = F.NF
JOIN REVEND R ON FVR.NR = R.NR
WHERE F.VilleF <> R.VilleR;
```

#### 2. Reasoning
This is the inverse logic of the previous exercise, but focused on dealers (`NR`) instead of cars (`NV`). We look for the existence of *any* transaction where the cities do not match.

#### 3. Detailed Explanation
*   **Inequality Operator**: The symbol `<>` (or `!=` in some SQL dialects) checks for inequality.
*   **Logic**:
    *   If Dealer R1 is in Paris.
    *   Supplier F1 is in London.
    *   Transaction F1 -> R1 exists.
    *   Since 'Paris' <> 'London', R1 is selected.
*   **Note**: A dealer might have 10 local suppliers and 1 non-local supplier. They will still be selected because the question asks for "at least one".

---

### Exercise 13: Dealers with No Red Cars from London Suppliers

**Source:** TD N° 1 BDA : Rappel SQL - Question 13
**Question:** "Quels sont les numéros des revendeurs pour lesquels aucune voiture rouge n’est fournie par un fournisseur habitant Londres ?" (Which dealer numbers have NO red cars supplied by a supplier living in London?)

#### 1. Solution
```sql
SELECT NR 
FROM REVEND
EXCEPT -- (or MINUS in Oracle)
SELECT FVR.NR
FROM FVR
JOIN FOURN F ON FVR.NF = F.NF
JOIN VOITURE V ON FVR.NV = V.NV
WHERE F.VilleF = 'LONDRES' 
  AND V.Couleur = 'ROUGE';
```
*Alternative using `NOT IN`:*
```sql
SELECT NR 
FROM REVEND
WHERE NR NOT IN (
    SELECT FVR.NR
    FROM FVR
    JOIN FOURN F ON FVR.NF = F.NF
    JOIN VOITURE V ON FVR.NV = V.NV
    WHERE F.VilleF = 'LONDRES' 
      AND V.Couleur = 'ROUGE'
);
```

#### 2. Reasoning
This is a "exclusion" query.
1.  Identify the "Forbidden Set": Transactions involving a **Red Car** coming from a **London Supplier**.
2.  Subtract the dealers involved in that set from the list of all dealers.

#### 3. Detailed Explanation
*   **The Subquery (The "Bad" List)**:
    *   Joins `FVR`, `FOURN`, and `VOITURE`.
    *   Filters for `VilleF='LONDRES'` AND `Couleur='ROUGE'`.
    *   Returns the list of dealers who *did* receive such a car.
*   **The Outer Query**: `NOT IN` removes anyone found in the bad list. The remaining dealers either received red cars from non-London suppliers, or non-red cars from London, or nothing at all. All these cases satisfy the condition "No red car from London".

---

### Exercise 14: Suppliers Matching Paris Code but Not in Paris

**Source:** TD N° 1 BDA : Rappel SQL - Question 14
**Question:** "Quels sont les numéros des fournisseurs n’habitant pas Paris mais dont le code est égal à celui d’un fournisseur habitant Paris ?" (Which supplier numbers do not live in Paris but have a code equal to that of a supplier living in Paris?)

#### 1. Solution
```sql
SELECT F1.NF
FROM FOURN F1
WHERE F1.VilleF <> 'PARIS'
  AND F1.Code IN (
      SELECT F2.Code 
      FROM FOURN F2 
      WHERE F2.VilleF = 'PARIS'
  );
```

#### 2. Reasoning
We are comparing suppliers to other suppliers.
1.  Find the set of codes belonging to suppliers in Paris.
2.  Find suppliers *not* in Paris whose code belongs to that set.

#### 3. Detailed Explanation
*   **Subquery**: `SELECT Code FROM FOURN WHERE VilleF = 'PARIS'` extracts the target codes (e.g., 10, 20).
*   **Main Query**: Scans the `FOURN` table.
    *   Row 1: F4, London, Code 20.
    *   Check 1: Is City <> Paris? Yes (London).
    *   Check 2: Is Code (20) in the Paris-list? Yes.
    *   Result: Keep F4.

---

### Exercise 15: Cars Supplied to ALL London Dealers

**Source:** TD N° 1 BDA : Rappel SQL - Question 15
**Question:** "Donnez les numéros des voitures fournies chacune à tous les revendeurs de Londres." (Give the car numbers supplied to ALL dealers in London.)

#### 1. Solution
*(Another Relational Division problem)*

```sql
SELECT V.NV
FROM VOITURE V
WHERE NOT EXISTS (
    -- Find a dealer in London...
    SELECT R.NR
    FROM REVEND R
    WHERE R.VilleR = 'LONDRES'
    AND NOT EXISTS (
        -- ...who has NOT received this car.
        SELECT 1
        FROM FVR F
        WHERE F.NR = R.NR
          AND F.NV = V.NV
    )
);
```

#### 2. Reasoning
This is mathematically identical to Exercise 9, but the "subject" is different.
*   Exercise 9: Cars supplied to all London Dealers? (Wait, looking back at Ex 9, it was the same question. Let me double check the provided context).
*   *Correction*: Exercise 9 asked for "cars supplied *for* all dealers". Exercise 15 asks "cars supplied *to* all dealers". In French "pour" vs "à". In the context of this schema, they mean the exact same thing (Relational Division).
*   **Verification**: Let's look at the correction provided in the image for Question 15.
    *   Image snippet says: `select nv from fvr x where not exists (select * from revend where ville='LONDRES' and not exists (select * from fvr where nr=revend.nr and nv=x.nv));`
    *   This confirms it is indeed the exact same logic.

#### 3. Detailed Explanation
*   **Double Negation**: "Find cars where there is NO London dealer who does NOT have the car."
*   **Step 1**: `SELECT R.NR ... WHERE VilleR = 'LONDRES'` gets the list of target dealers (the denominator of the division).
*   **Step 2**: The inner `NOT EXISTS` checks the link.
*   **Step 3**: The outer `NOT EXISTS` confirms that the set of "missing links" is empty for that specific car.

---

### Exercises 16 & 17 (Bonus from the image)

Although you asked for batches of 5, the image provided (Screenshot 2/3 from TD1 correction) contains Questions 16 and 17. I will include them briefly here to complete the TD1 set before moving to TD2 in the next batch.

**Exercise 16:** "Dealers with identical stock to F1"
*   **Query**: Find dealers where their set of cars is exactly equal to the set of cars supplied by F1.
*   **Logic**: (Cars of R contains Cars of F1) AND (Cars of F1 contains Cars of R).

**Exercise 17:** "Dealers offering *only* cars available from F1"
*   **Query**: Find dealers where `NOT EXISTS` a car they sell that is `NOT IN` F1's catalog.
*   **Logic**: Set Inclusion (Cars of R $\subseteq$ Cars of F1).

*End of TD 1.*