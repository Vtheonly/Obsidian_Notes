### 2008 Exam

**Year:** 2008
**Type:** Exam
**Correction:** Yes

#### Exercise 1

**Statement:**
You will find below the relational schema regarding sales management in a set of stationery stores grouped under the same brand.

*   **SUPPLIERS** (SUP_NUM, SUP_NAME)
*   **CLIENTS** (CLT_NUM, CLT_LASTNAME, CLT_FIRSTNAME, CLT_COUNTRY, CLT_LOC)
*   **STORES** (STR_NUM, STR_LOC, STR_MGR)
*   **ARTICLES** (ART_NUM, ART_NAME, ART_WEIGHT, ART_COLOR, ART_BP, ART_SP, SUP_NUM)
    *   *Note: ART_BP = Buying Price, ART_SP = Selling Price*
*   **SALES** (CLT_NUM, STR_NUM, ART_NUM, SALE_DATE, SALE_QTY, SALE_AMOUNT)

**Work to be done:**

**I/ Data Definition Language:**
Give in SQL the commands to create the preceding tables, specifying the data type of each column as well as the integrity constraints ensuring the consistency of data in such a database.

**II/ Queries:**
Program the following queries in SQL:

1.  List of localities where clients live.
2.  Select all articles whose weight is greater than X grams in descending order of weight.
3.  Select all articles for which the selling price is greater than or equal to double the buying price.
4.  Select all articles from the supplier "Les stylos réunis" whose buying price is less than X €.
5.  Select the list of articles whose selling price is between X and Y euros.
6.  Select the list of articles with the color 'RED' or 'GREEN' or 'BLUE'.
7.  Select the list of sales (name of articles, stores, clients) for clients whose name starts with 'JA'.
8.  Select articles that have no color and display the supplier's name.
9.  Select the list of all articles whose buying price is higher than the price of article number 08.
10. Select the profit margin on products whose buying price is greater than X €, in increasing order of margin.
11. Count the number of different colors existing in the stock.
12. What is/are the product(s) on which the highest margin is realized?
13. Calculate per article the total discount granted compared to the catalog selling price (listed in the articles table), for the week from '05/01/2008' to '11/01/2008'.
14. Select the stores which, between '01/01/2008' and '31/01/2008', made more than two sales. Display the number of sales for each of these stores.
15. Select the names of store managers who sold at least one article number X last month.
16. Select the list of clients whose sum of purchases is greater than the average sum of purchases of all clients.
17. Display information about stores that did not sell article number X last month.
18. What are the clients who, living in one city, made purchases in a store in another city?
19. What are the clients who made all their purchases in the city where they live?
20. Select the number and name of articles that were sold by ALL stores.
21. Which is/are the store(s) that achieved the highest turnover last month?
22. Knowing that there are never more than two stores in the same city, display on the same line the concerned cities and their two stores.

*Indication for queries 20 and 21: use the notion of a view to record intermediate results.*

#### Correction

```sql
-- I/ Creation of tables
-- (Note: The correction document provided specific creation commands 
-- but they were mixed with text. Below is the standard structure implied.)

-- II/ Queries

-- R1: List of localities where clients live.
SELECT DISTINCT clt_loc FROM clients ORDER BY clt_loc;

-- R2: Select all articles whose weight is greater than X grams in descending order of weight.
SELECT art_num, art_name, art_weight FROM articles
WHERE art_weight > [weight] ORDER BY art_weight DESC;

-- R3: Select all articles for which the selling price is greater than or equal 
-- to double the buying price.
SELECT art_num, art_name, art_bp, art_sp FROM articles
WHERE art_sp >= (art_bp * 2);

-- R4: Select all articles from the supplier "Les stylos réunis" whose buying price is less than X.
SELECT art_num, art_name, art_bp FROM articles
WHERE art_sup =
    (SELECT sup_num FROM suppliers WHERE sup_name ="LES STYLOS REUNIS")
AND art_bp < [Buying Price];

-- R5: Select the list of articles whose selling price is between X and Y euros.
SELECT art_num, art_name, art_sp FROM articles
WHERE art_sp BETWEEN [Price min] AND [Price max];

-- R6: Select the list of articles with the color 'RED' or 'GREEN' or 'BLUE'.
SELECT art_num, art_name, art_color FROM articles
WHERE art_color IN ('red', 'green', 'blue');

-- R7: Select the list of sales (name of articles, stores, clients) for clients 
-- whose name starts with 'JA'.
SELECT clt_num, clt_name, str_num, str_loc, art_name, sale_date, sale_qty, sale_amount
FROM clients, stores, articles, sales
WHERE sale_clt = clt_num AND sale_art = art_num AND sale_str = str_num
AND clt_name LIKE [First letters of client] & "*"
ORDER BY clt_name, sale_date;

-- R8: Select articles that have no color and display the supplier's name.
SELECT art_num, art_name, sup_name FROM articles, suppliers
WHERE art_color = NULL AND art_sup = sup_num ORDER BY art_num;

-- R9: Select the list of all articles whose buying price is higher than the price of article number 08.
SELECT art_num, art_name, art_bp FROM articles
WHERE art_bp > (SELECT art_bp FROM articles WHERE art_num = [Article Reference]);
-- Or using Self Join:
SELECT X.art_num, X.art_name, X.art_bp, Y.art_num AS Reference, Y.art_name, Y.art_bp AS [Ref Price] 
FROM articles AS X, articles AS Y
WHERE X.art_bp > Y.art_bp AND Y.art_num = [Article Reference];

-- R10: Select the profit margin on products whose buying price is greater than X € 
-- in increasing order of margin.
SELECT art_num, art_name, art_bp, art_sp, art_sp - art_bp AS Margin FROM articles
WHERE art_bp > [Buying price greater than] ORDER BY 4 DESC;

-- R11: Count the number of different colors existing in the stock.
-- R11a:
SELECT DISTINCT art_color AS Colors FROM articles;
-- Main Query:
SELECT COUNT(*) AS NB_Colors FROM R11a WHERE Colors IS NOT NULL;

-- R12: What is/are the product(s) on which the highest margin is realized?
SELECT art_num, art_name, art_bp, art_sp, art_sp - art_bp AS Margin FROM articles
WHERE art_sp - art_bp = (SELECT MAX(art_sp-art_bp) FROM articles) ORDER BY 3;

-- R13: Calculate per article the total discount granted compared to the catalog selling price.
SELECT sale_art, art_name, SUM(Sale_Qty*Art_Sp - Sale_Amount) AS [Total Discount]
FROM Sales, Articles WHERE Art_Num = Sale_Art AND
Sale_date Between [Start] AND [End] GROUP BY sale_art, art_name;

-- R14: Select the stores which, between ... and ..., made more than two sales.
SELECT str_loc, count (*) AS [Num Sales], SUM(sale_amount) AS Turnover, 
AVG(sale_amount) AS Avg_Turnover FROM sales, stores
WHERE sale_date BETWEEN [Start] AND [Start] + 6 AND sale_str = str_num
GROUP BY str_loc HAVING COUNT (*) > [Number of sales];

-- R15: Select the names of store managers who sold at least one article number X last month.
-- Helper View OldSales:
-- SELECT * FROM sales WHERE MONTH(sale_date) = MONTH(DATE())-1;
SELECT str_mgr, str_loc FROM stores
WHERE str_num IN (SELECT sale_str FROM OldSales WHERE sale_art = [Article Num] );

-- R16: Select the list of clients whose sum of purchases is greater than 
-- the average sum of purchases of all clients.
-- R16a: 
SELECT clt_name, SUM(sale_amount) AS Total FROM sales, clients
WHERE sale_clt = clt_num GROUP BY clt_name
HAVING SUM(sale_amount) > (SELECT AVG(sale_amount) FROM sales) ORDER BY 2 DESC;
-- Averaging the totals:
SELECT clt_name, Total, FORMAT(AVG(sale_amount), '#####') AS Average
FROM R16a, sales GROUP BY clt_name, Total;

-- R17: Display information about stores that did not sell article number X last month.
SELECT str_loc AS Store, str_mgr AS Manager FROM stores
WHERE str_num NOT IN (SELECT sale_str FROM sales WHERE sale_art = [Article Num]);

-- R18: What are the clients who, living in one city, made purchases in a store in another city?
SELECT clt_name, clt_loc, str_loc, sale_date FROM clients, sales, stores
WHERE clt_num = sale_clt AND sale_str = str_num AND str_loc <> clt_loc
ORDER BY clt_name, sale_date;

-- R19: What are the clients who made all their purchases in the city where they live?
-- (Note: The logic here is identifying those who did NOT shop elsewhere)
SELECT clt_name, clt_loc, str_loc, sale_date FROM clients, sales, stores
WHERE clt_num = sale_clt AND sale_str = str_num AND str_loc = clt_loc AND clt_name NOT 
IN (SELECT clt_name FROM R18) ORDER BY clt_name, sale_date;

-- R20: Select the number and name of articles that were sold by ALL stores.
-- R18a: SELECT DISTINCT Sale_Art, Sale_Str FROM Sales;
SELECT Sale_Art, art_name FROM R18a, articles WHERE sale_art = art_num
GROUP BY Sale_Art, art_name HAVING COUNT(*) =
(SELECT COUNT(*) FROM Stores);

-- R21: Which is/are the store(s) that achieved the highest turnover last month?
-- R19a: SELECT sale_str, sum(sale_amount) AS Turnover FROM oldsales GROUP BY sale_str;
SELECT str_mgr, str_loc, Turnover FROM R19a, stores WHERE sale_str = str_num
AND Turnover = (SELECT MAX (Turnover) FROM R19a);

-- R22: Display on the same line the concerned cities and their two stores.
SELECT X.str_loc, X.str_mgr, Y.str_mgr FROM stores AS X, stores AS Y 
WHERE X.str_loc = Y.str_loc AND X.str_num < Y.str_num ORDER BY X.str_num;
```

---
