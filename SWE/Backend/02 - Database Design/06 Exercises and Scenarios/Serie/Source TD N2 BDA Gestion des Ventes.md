Here is the complete processing for the source **TD N°2 BDA : SQL (Dates)**.

Based on the provided context, this TD appears to be identical to the "Correction examen du 06 Février 2008" provided in the documents. I will use that correction as the authoritative reference.

---

# Source: TD N°2 BDA - Gestion des Ventes (Papeterie)

**Context Schema:**
*   `FOURNISS (FRS_NUM, FRS_NOM)`
*   `CLIENTS (CLT_NUM, CLT_NOM, CLT_PNOM, CLT_PAYS, CLT_LOC)`
*   `MAGASINS (MAG_NUM, MAG_LOC, MAG_GER)`
*   `ARTICLES (ART_NUM, ART_NOM, ART_POIDS, ART_COUL, ART_PA, ART_PV, FRS_NUM)`
*   `VENTES (CLT_NUM, MAG_NUM, ART_NUM, VNT_DATE, VNT_QTE, VNT_MONTANT)`

---

## Part I: Data Definition Language (DDL)

**Exercise:** Create tables with integrity constraints.

### 1. Solution
```sql
CREATE TABLE FOURNISS ( 
    FRS_NUM Number(6) PRIMARY KEY, 
    FRS_NOM Varchar(30) NOT NULL
);

CREATE TABLE CLIENTS ( 
    CLT_NUM Number(6) PRIMARY KEY, 
    CLT_NOM Varchar(30), 
    CLT_PNOM Varchar(30) NOT NULL, 
    CLT_PAYS Varchar(30), 
    CLT_LOC Varchar(50) 
); 

CREATE TABLE MAGASINS ( 
    MAG_NUM Number(6) PRIMARY KEY, 
    MAG_LOC Varchar(50) NOT NULL, 
    MAG_GER Varchar(30) 
);

CREATE TABLE ARTICLES ( 
    ART_NUM Number(6) PRIMARY KEY, 
    ART_NOM Varchar(30), 
    ART_POIDS Number(6) NOT NULL,
    ART_COUL Varchar(15), 
    ART_PA Number(8,2), 
    ART_PV Number(8,2), 
    FRS_NUM Number(6) REFERENCES FOURNISS(FRS_NUM) 
);

CREATE TABLE VENTES ( 
    CLT_NUM Number(6) REFERENCES CLIENTS(CLT_NUM), 
    MAG_NUM Number(6) REFERENCES MAGASINS(MAG_NUM), 
    ART_NUM Number(6) REFERENCES ARTICLES(ART_NUM), 
    VNT_DATE Date,
    VNT_QTE Number(6) NOT NULL,
    VNT_MONTANT Number(8,2) NOT NULL,
    PRIMARY KEY (CLT_NUM, MAG_NUM, ART_NUM, VNT_DATE) 
);
```

### 2. Reasoning
*   **Primary Keys**: Every table needs a unique identifier. For `VENTES`, since a client can buy the same article in the same shop on different dates, the primary key is composite: `(CLT, MAG, ART, DATE)`.
*   **Foreign Keys**: `ARTICLES` links to `FOURNISS`. `VENTES` links to `CLIENTS`, `MAGASINS`, and `ARTICLES`.
*   **Constraints**: `NOT NULL` is applied to essential fields like names, quantities, and prices.

### 3. Detailed Explanation
*   **`REFERENCES table(col)`**: This enforces **Referential Integrity**. You cannot sell an article that doesn't exist in the `ARTICLES` table.
*   **`Number(8,2)`**: This defines a number with 8 digits total, 2 of which are decimal (e.g., 123456.78), ideal for prices.
*   **Composite Key in VENTES**: If we didn't include `VNT_DATE` in the primary key, a client could only buy a specific item from a specific shop *once* in their entire life. Including the date allows repeat purchases.

---

## Part II: Data Manipulation Language (DML)

### Exercise 1: Client Localities
**Question:** Liste des localités où habitent les clients.

#### 1. Solution
```sql
SELECT DISTINCT CLT_LOC 
FROM CLIENTS 
ORDER BY CLT_LOC;
```
#### 2. Reasoning
We need the `CLT_LOC` column. Since multiple clients live in the same city, `DISTINCT` removes duplicates.
#### 3. Detailed Explanation
The `ORDER BY` clause sorts the cities alphabetically, making the list easier to read.

---

### Exercise 2: Heavy Articles
**Question:** Sélectionnez tous les articles dont le poids est supérieur à X grammes par ordre décroissant de poids.

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM, ART_POIDS 
FROM ARTICLES
WHERE ART_POIDS > X 
ORDER BY ART_POIDS DESC;
```
#### 2. Reasoning
Filter rows using `WHERE` with a numeric comparison (`>`). Sort results using `ORDER BY ... DESC`.
#### 3. Detailed Explanation
`DESC` stands for Descending (largest to smallest). This puts the heaviest items at the top of the list.

---

### Exercise 3: High Margin Articles
**Question:** Sélectionnez tous les articles pour lesquels le prix de vente est supérieur ou égal au double du prix d'achat.

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM, ART_PA, ART_PV 
FROM ARTICLES
WHERE ART_PV >= (ART_PA * 2);
```
#### 2. Reasoning
We can use arithmetic expressions inside the `WHERE` clause.
#### 3. Detailed Explanation
The database engine calculates `ART_PA * 2` for every row and compares it to `ART_PV`. Only rows satisfying the condition are returned.

---

### Exercise 4: Specific Supplier and Price
**Question:** Sélectionnez tous les articles du fournisseur "Les stylos réunis" dont le prix d'achat est inférieur à X €.

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM, ART_PA 
FROM ARTICLES
WHERE FRS_NUM = (SELECT FRS_NUM FROM FOURNISS WHERE FRS_NOM = 'Les stylos réunis') 
  AND ART_PA < X;
```
#### 2. Reasoning
We only know the supplier's *name*, but the `ARTICLES` table only contains the supplier's *number*. We use a subquery to find the ID first.
#### 3. Detailed Explanation
Alternatively, a `JOIN` could be used: `FROM ARTICLES A JOIN FOURNISS F ON A.FRS_NUM = F.FRS_NUM`. The subquery method is often preferred when we only need columns from the main table (`ARTICLES`).

---

### Exercise 5: Price Range
**Question:** Sélectionnez la liste des articles dont le prix de vente est compris entre X et Y euros.

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM, ART_PV 
FROM ARTICLES
WHERE ART_PV BETWEEN X AND Y;
```
#### 2. Reasoning
The `BETWEEN` operator is the standard way to check ranges (inclusive of endpoints).
#### 3. Detailed Explanation
This is equivalent to `WHERE ART_PV >= X AND ART_PV <= Y`.

---

### Exercise 6: Specific Colors
**Question:** Sélectionnez la liste des articles de couleur 'ROUGE' ou 'VERT' ou 'BLEU'.

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM, ART_COUL 
FROM ARTICLES
WHERE ART_COUL IN ('ROUGE', 'VERT', 'BLEU');
```
#### 2. Reasoning
The `IN` operator checks if a value exists within a specific list.
#### 3. Detailed Explanation
Using `IN` is more readable and often more efficient than writing `ART_COUL = 'ROUGE' OR ART_COUL = 'VERT' ...`.

---

### Exercise 7: Sales for Clients 'JA...'
**Question:** Liste des ventes (articles, magasins, clients) des clients dont le nom commence par 'JA'.

#### 1. Solution
```sql
SELECT C.CLT_NOM, M.MAG_LOC, A.ART_NOM, V.VNT_DATE, V.VNT_QTE
FROM CLIENTS C, MAGASINS M, ARTICLES A, VENTES V
WHERE V.CLT_NUM = C.CLT_NUM 
  AND V.ART_NUM = A.ART_NUM 
  AND V.MAG_NUM = M.MAG_NUM 
  AND C.CLT_NOM LIKE 'JA%';
```
#### 2. Reasoning
This requires joining 4 tables. `VENTES` is the hub. We use `LIKE 'JA%'` for pattern matching.
#### 3. Detailed Explanation
The `%` wildcard matches any sequence of characters. 'JA%' matches 'JANIS', 'JACKSON', 'JAY', etc.

---

### Exercise 8: Colorless Articles
**Question:** Sélectionnez les articles qui n'ont pas de couleur.

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM 
FROM ARTICLES 
WHERE ART_COUL IS NULL;
```
#### 2. Reasoning
In SQL, you cannot say `= NULL`. You must use `IS NULL`.
#### 3. Detailed Explanation
`NULL` represents the absence of data (unknown). Comparing `Unknown = Unknown` yields Unknown (False), so the query would fail without `IS`.

---

### Exercise 9: Expensive Articles
**Question:** Articles dont le prix d'achat est supérieur au prix de l'article numéro 08.

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM, ART_PA 
FROM ARTICLES
WHERE ART_PA > (SELECT ART_PA FROM ARTICLES WHERE ART_NUM = 8);
```
#### 2. Reasoning
We need a reference value (Price of article 8). A subquery retrieves this single value, which is then compared against all rows.
#### 3. Detailed Explanation
The subquery runs first, finding e.g., 50.00. The main query then becomes `WHERE ART_PA > 50.00`.

---

### Exercise 10: Profit Margin
**Question:** Marge bénéficiaire sur les produits dont le prix d'achat > X, ordre croissant de la marge.

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM, (ART_PV - ART_PA) AS Marge 
FROM ARTICLES
WHERE ART_PA > X 
ORDER BY Marge ASC;
```
#### 2. Reasoning
We calculate a derived column `(ART_PV - ART_PA)` and alias it `Marge`.
#### 3. Detailed Explanation
Calculated columns can be used in `ORDER BY` clauses. `ASC` (Ascending) puts the smallest margins first.

---

### Exercise 11: Count Colors
**Question:** Comptez le nombre de couleurs différentes existant dans le stock.

#### 1. Solution
```sql
SELECT COUNT(DISTINCT ART_COUL) AS NB_Couleurs 
FROM ARTICLES 
WHERE ART_COUL IS NOT NULL;
```
#### 2. Reasoning
`COUNT(*)` counts rows. `COUNT(col)` counts non-null values. `COUNT(DISTINCT col)` counts unique non-null values.
#### 3. Detailed Explanation
If we have 5 red pens and 3 blue pens, `COUNT(*)` is 8, but `COUNT(DISTINCT)` is 2 (Red, Blue).

---

### Exercise 12: Best Margin Product
**Question:** Quels sont le ou les produits sur lesquels on réalise la marge la plus élevée ?

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM
FROM ARTICLES
WHERE (ART_PV - ART_PA) = (SELECT MAX(ART_PV - ART_PA) FROM ARTICLES);
```
#### 2. Reasoning
We cannot put `MAX()` directly in a `WHERE` clause. We must calculate the Max Margin in a subquery first.
#### 3. Detailed Explanation
The subquery finds the single highest margin value (e.g., 100). The outer query finds *all* articles that happen to have that specific margin.

---

### Exercise 13: Total Discounts
**Question:** Calculez la remise totale accordée par rapport au prix catalogue pour une semaine donnée.

#### 1. Solution
```sql
SELECT V.ART_NUM, A.ART_NOM, SUM((V.VNT_QTE * A.ART_PV) - V.VNT_MONTANT) AS Remise_Totale
FROM VENTES V, ARTICLES A
WHERE V.ART_NUM = A.ART_NUM 
  AND V.VNT_DATE BETWEEN '05/01/2008' AND '11/01/2008'
GROUP BY V.ART_NUM, A.ART_NOM;
```
#### 2. Reasoning
*Theoretical Price* = Qty * Catalog Price (`ART_PV`).
*Actual Price* = `VNT_MONTANT` (assuming this column stores the total paid).
*Difference* = Discount.
#### 3. Detailed Explanation
We group by article to see the total discount given per product over that specific week.

---

### Exercise 14: High Volume Shops
**Question:** Magasins ayant réalisé plus de deux ventes sur une période.

#### 1. Solution
```sql
SELECT M.MAG_NUM, M.MAG_LOC, COUNT(*) AS Nbre_Ventes
FROM VENTES V, MAGASINS M
WHERE V.MAG_NUM = M.MAG_NUM 
  AND V.VNT_DATE BETWEEN '01/01/2008' AND '31/01/2008'
GROUP BY M.MAG_NUM, M.MAG_LOC
HAVING COUNT(*) > 2;
```
#### 2. Reasoning
Filtering *groups* (aggregates) requires `HAVING`, not `WHERE`.
#### 3. Detailed Explanation
1. `WHERE` filters individual sales (by date).
2. `GROUP BY` aggregates them by shop.
3. `HAVING` keeps only shops with count > 2.

---

### Exercise 15: Active Managers Last Month
**Question:** Nom des gérants ayant vendu l'article X le mois dernier.

#### 1. Solution
```sql
SELECT DISTINCT M.MAG_GER
FROM MAGASINS M, VENTES V
WHERE M.MAG_NUM = V.MAG_NUM
  AND V.ART_NUM = X
  AND TO_CHAR(V.VNT_DATE, 'MM/YYYY') = TO_CHAR(ADD_MONTHS(SYSDATE, -1), 'MM/YYYY');
```
#### 2. Reasoning
We need to match the month of the sale to "Today minus 1 month".
#### 3. Detailed Explanation
*   `SYSDATE`: Current server date (Oracle).
*   `ADD_MONTHS(..., -1)`: Go back one month.
*   `TO_CHAR(..., 'MM')`: Extract just the month part to compare.

---

### Exercise 16: Big Spender Clients
**Question:** Clients dont la somme des achats est supérieure à la moyenne.

#### 1. Solution
*Step 1: Create View for Total per Client*
```sql
CREATE VIEW V_TOTAL_CLIENT AS
SELECT CLT_NUM, SUM(VNT_MONTANT) AS Total_Achat
FROM VENTES
GROUP BY CLT_NUM;
```
*Step 2: Query the View*
```sql
SELECT CLT_NUM, Total_Achat
FROM V_TOTAL_CLIENT
WHERE Total_Achat > (SELECT AVG(Total_Achat) FROM V_TOTAL_CLIENT);
```
#### 2. Reasoning
It is impossible to nest aggregates like `AVG(SUM(...))` in standard SQL directly in one clause without subqueries or views.
#### 3. Detailed Explanation
The view calculates how much each client spent. The subquery calculates the average of those totals. The main query filters clients above that average.

---

### Exercise 17: Shops Missing Product X
**Question:** Magasins n'ayant pas vendu l'article X le mois dernier.

#### 1. Solution
```sql
SELECT MAG_LOC 
FROM MAGASINS
WHERE MAG_NUM NOT IN (
    SELECT MAG_NUM 
    FROM VENTES 
    WHERE ART_NUM = X 
      AND TO_CHAR(VNT_DATE, 'MM') = TO_CHAR(ADD_MONTHS(SYSDATE, -1), 'MM')
);
```
#### 2. Reasoning
Set Difference: All Shops - Shops that *did* sell X.
#### 3. Detailed Explanation
The subquery finds the "Active sellers of X". `NOT IN` excludes them, leaving shops that either sold nothing or sold other things, but not X.

---

### Exercise 18: Cross-City Shopping
**Question:** Clients achetant dans une autre ville.

#### 1. Solution
```sql
SELECT DISTINCT C.CLT_NOM
FROM CLIENTS C, VENTES V, MAGASINS M
WHERE C.CLT_NUM = V.CLT_NUM 
  AND V.MAG_NUM = M.MAG_NUM
  AND C.CLT_LOC <> M.MAG_LOC;
```
#### 2. Reasoning
Join Client -> Sale -> Shop. Compare Client City (`CLT_LOC`) with Shop City (`MAG_LOC`).
#### 3. Detailed Explanation
`<>` means "Not Equal". We look for mismatches between residence and shop location.

---

### Exercise 19: Strictly Local Shoppers
**Question:** Clients achetant *uniquement* dans leur ville.

#### 1. Solution
```sql
SELECT CLT_NOM 
FROM CLIENTS C
WHERE NOT EXISTS (
    SELECT 1 
    FROM VENTES V, MAGASINS M
    WHERE V.CLT_NUM = C.CLT_NUM 
      AND V.MAG_NUM = M.MAG_NUM
      AND C.CLT_LOC <> M.MAG_LOC
);
```
#### 2. Reasoning
"Only in their city" = "There does not exist a purchase outside their city".
#### 3. Detailed Explanation
We reuse the logic from Ex 18 but negate it using `NOT EXISTS`.

---

### Exercise 20: Articles sold in ALL shops
**Question:** Articles vendus par TOUS les magasins.

#### 1. Solution
```sql
SELECT ART_NUM, ART_NOM 
FROM ARTICLES A
WHERE NOT EXISTS (
    SELECT M.MAG_NUM 
    FROM MAGASINS M
    WHERE NOT EXISTS (
        SELECT 1 
        FROM VENTES V 
        WHERE V.ART_NUM = A.ART_NUM 
          AND V.MAG_NUM = M.MAG_NUM
    )
);
```
*Alternative (Aggregation):*
```sql
SELECT ART_NUM 
FROM VENTES 
GROUP BY ART_NUM 
HAVING COUNT(DISTINCT MAG_NUM) = (SELECT COUNT(*) FROM MAGASINS);
```
#### 2. Reasoning
This is **Relational Division**.
#### 3. Detailed Explanation
Logic: Find an article where the count of distinct shops selling it equals the total count of shops available.

---

### Exercise 21: Best Turnover Shop
**Question:** Magasins avec le meilleur chiffre d'affaires le mois dernier.

#### 1. Solution
```sql
CREATE VIEW V_CA_MAG AS
SELECT MAG_NUM, SUM(VNT_MONTANT) AS CA
FROM VENTES
WHERE TO_CHAR(VNT_DATE, 'MM') = TO_CHAR(ADD_MONTHS(SYSDATE, -1), 'MM')
GROUP BY MAG_NUM;

SELECT MAG_NUM, CA 
FROM V_CA_MAG
WHERE CA = (SELECT MAX(CA) FROM V_CA_MAG);
```
#### 2. Reasoning
Similar to Ex 16 (Max of Sums).
#### 3. Detailed Explanation
We aggregate sales by shop for the period, then select the shop(s) matching the maximum aggregated value.

---

### Exercise 22: Cities with exactly 2 shops
**Question:** Villes concernées et leurs deux magasins (sachant qu'il n'y a jamais plus de 2).

#### 1. Solution
```sql
SELECT M1.MAG_LOC AS Ville, M1.MAG_GER, M2.MAG_GER
FROM MAGASINS M1, MAGASINS M2
WHERE M1.MAG_LOC = M2.MAG_LOC
  AND M1.MAG_NUM < M2.MAG_NUM;
```
#### 2. Reasoning
Self-join on the City column.
#### 3. Detailed Explanation
`M1.MAG_NUM < M2.MAG_NUM` ensures we don't pair a shop with itself (A, A) and we don't list the pair twice (A, B) and (B, A). We only get the unique pair (A, B) per city.