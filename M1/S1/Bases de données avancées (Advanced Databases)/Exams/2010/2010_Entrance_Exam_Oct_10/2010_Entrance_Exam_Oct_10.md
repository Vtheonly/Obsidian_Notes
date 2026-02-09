Here are the next 3 exams (2010 Entrance Exam, 2010 Exam, and 2012 Control).

---

### 2010 Post-Graduation Entrance Exam

**Year:** 2010
**Type:** Entrance Exam (Concours d’entrée)
**Correction:** Yes

#### Exercise 3 (8 pts)

**Statement:**
*(Reconstructed from the provided correction document)*

Given the following relational schema regarding sales:
*   **SUPPLIERS** (frs_num, frs_name)
*   **CLIENTS** (clt_num, clt_name, clt_fname, clt_country, clt_loc)
*   **STORES** (mag_num, mag_loc, mag_ger)
*   **ARTICLES** (art_num, art_name, art_weight, art_color, art_bp, art_sp, frs_num)
*   **SALES** (clt_num, mag_num, art_num, vnt_date, vnt_qty, vnt_amount)

**I/ Commands to create tables:**
Write the SQL commands to create these tables respecting primary and foreign keys and not null constraints.

**II/ SQL Queries:**
1.  Select all articles from the supplier "Les stylos réunis" whose buying price is lower than X Dinars without using the join operation.
2.  List of sales (name of articles, stores, clients) for clients whose name starts with 'JA'.
3.  Products on which the highest margin is realized.
4.  Calculate per article the total discount granted compared to the catalog selling price (listed in the articles table), for the week from 05/01/2008 to 11/01/2008.
5.  Search for stores which, between '01/01/2008' and '31/01/2008', made more than two sales. Display the number of sales for each of these stores.
6.  Give the name of store managers who sold at least one article number X last month.
7.  Clients who, living in a city, made purchases in a store in another city.
8.  Clients who made all their purchases in the city where they live.
9.  Number and name of articles that were sold by ALL stores.
10. Knowing that there are never more than two stores in the same city, display on the same line the concerned cities and their two stores.

#### Correction

```sql
-- I/ Creation of tables
CREATE TABLE suppliers (
    frs_num Number(6) primary key,
    frs_name varchar(30) not null
);

CREATE TABLE clients (
    clt_num Number(6) primary key,
    clt_name varchar(30) not null,
    clt_fname varchar(30) not null,
    clt_country varchar(30),
    clt_loc varchar(50)
);

CREATE TABLE stores (
    mag_num Number(6) primary key,
    mag_loc varchar(50) not null,
    mag_ger varchar(30)
);

CREATE TABLE articles (
    art_num Number(6) primary key,
    art_name varchar(30) not null,
    art_weight Number(6),
    art_color varchar(15),
    art_bp Number(8,2), -- Buying Price
    art_sp Number(8,2), -- Selling Price
    frs_num Number(6) references suppliers(frs_num)
);

CREATE TABLE sales (
    clt_num Number(6) references clients(clt_num),
    mag_num Number(6) references stores(mag_num),
    art_num Number(6) references clients(clt_num), -- Note: likely error in source, should refer to articles
    vnt_date date,
    vnt_qty Number(6) not null,
    vnt_amount Number(8,2) not null,
    primary key (clt_num, mag_num, art_num, vnt_date)
);

-- II/ SQL Queries

-- 1. Articles from "Les stylos réunis" with buying price < X (No Join)
SELECT art_num, art_name, art_bp 
FROM articles 
WHERE art_frs = (select frs_num from suppliers where frs_name ="Les stylos réunis")
AND art_bp < X;

-- 2. Sales list for clients starting with 'JA'
SELECT clt_num, clt_name, mag_num, mag_loc, art_name, vnt_date, vnt_qty, vnt_amount
FROM clients c, stores m, articles a, sales v
WHERE v.clt_num = c.clt_num
AND v.art_num = a.art_num
AND v.mag_num = m.mag_num
AND c.clt_name LIKE "JA*" -- (or "JA%")
ORDER BY clt_name, vnt_date;

-- 3. Products with the highest margin
SELECT art_num, art_name, art_bp, art_sp, (art_sp - art_bp) AS Margin
FROM articles
WHERE art_sp - art_bp = (select max(art_sp - art_bp) from articles)
ORDER BY art_num, art_name;

-- 4. Total discount per article for the week of 05/01/2008
SELECT v.art_num, art_name, Sum((vnt_qty * art_sp) - vnt_amount) AS Total_Discount
FROM sales v, articles a
WHERE a.art_num = v.art_num
AND vnt_date Between '05/01/2008' AND '11/01/2008'
GROUP BY v.art_num, art_name;

-- 5. Stores with more than 2 sales in Jan 2008
SELECT mag_num, mag_loc, count(*) AS Sales_Count
FROM sales v, stores m
WHERE v.mag_num = m.mag_num
AND vnt_date between '01/01/2008' AND '31/01/2008'
GROUP BY mag_num, mag_loc
HAVING count(*) > 2;

-- 6. Managers who sold article X last month
SELECT mag_ger, mag_loc 
FROM stores 
WHERE mag_num IN (
    SELECT v.mag_num
    FROM sales v
    WHERE art_num = X
    AND to_char(vnt_date,'MM') = to_char(add_months(sysdate,-1),'MM') 
    -- Or: months_between(sysdate, vnt_date) = 1
);

-- 7. Clients shopping in a different city
SELECT c.clt_name, c.clt_loc, m.mag_loc, v.vnt_date
FROM clients c, sales v, stores m
WHERE c.clt_num = v.clt_num
AND v.mag_num = m.mag_num
AND m.mag_loc <> c.clt_loc
ORDER BY clt_name, vnt_date;

-- 8. Clients shopping only in their city
SELECT c.clt_name, c.clt_loc, m.mag_loc, v.vnt_date
FROM clients c, sales v, stores m
WHERE c.clt_num = v.clt_num
AND v.mag_num = m.mag_num
AND clt_name NOT IN (
    -- Subquery identifying those who shopped elsewhere (from Q7)
    SELECT c2.clt_name 
    FROM clients c2, sales v2, stores m2
    WHERE c2.clt_num = v2.clt_num 
    AND v2.mag_num = m2.mag_num 
    AND m2.mag_loc <> c2.clt_loc
)
ORDER BY c.clt_name, v.vnt_date;

-- 9. Articles sold by ALL stores
CREATE VIEW Req_9 AS
SELECT DISTINCT art_num, mag_num FROM sales;

SELECT r.Art_num, a.art_name 
FROM Req_9 r, articles a
WHERE r.art_num = a.art_num
GROUP BY r.Art_num, a.art_name
HAVING Count(*) = (Select Count(*) From Stores);

-- 10. Cities with two stores displayed on one line
SELECT X.mag_loc, X.mag_ger, Y.mag_ger
FROM stores AS X, stores AS Y
WHERE X.mag_loc = Y.mag_loc
AND X.mag_num < Y.mag_num
ORDER BY X.mag_num;
```

---
