
# Web Application Attacks: SQL Injection (Slides 45-47)
[[Q9]]
This section details the SQL Injection (SQLi) vulnerability, a common and critical web application attack.

## SQL Injection Overview (Slide 45)

*   **Prevalence:** SQL Injection is arguably the **most widespread vulnerability** affecting web applications on the Internet.
*   **Target:** The vulnerability lies within the **web application's code**, specifically how it handles user input and constructs database queries, **not within the database system itself**. Databases execute the SQL they receive; the application is responsible for ensuring that SQL is safe.
*   **Definition:** SQL Injection is a technique used to **exploit the vulnerability of lacking input data validation**. It allows an attacker to send specially crafted input that manipulates the structure of SQL commands sent by the application to its backend database.
*   **Core Problem:** The fundamental issue is the **lack of clear distinction between the control plane (SQL instructions) and the data plane (user-provided data)** within the dynamically generated SQL query.
*   **Vulnerability Condition:** Without strict control and sanitization of the SQL syntax within user-provided input, the generated SQL query might interpret parts of this input **as SQL instructions instead of ordinary data**, leading to unauthorized database actions.

## The SQL Injection Mechanism (Slides 45-47)

### Normal Operation (Example based on Slide 46 login):

1.  A user enters their credentials (e.g., User-Id: `srinivas`, Password: `mypassword`) into a web form.
2.  The web application takes this input.
3.  The application constructs an SQL query to validate the credentials against the database, like:
    ```sql
    SELECT * FROM Users WHERE user_id = 'srinivas' AND password = 'mypassword';
    ```
4.  The database executes this query. If a matching record is found, the application logs the user in.

### Attack Scenario (Example based on Slide 46 bypass):

1.  An attacker enters malicious input into the web form fields. For example:
    *   User-Id: `' OR 1=1; /*`
    *   Password: `*/--` (or anything, as it might be commented out)
2.  The web application takes this malicious input.
3.  The application constructs the SQL query, naively incorporating the input:
    ```sql
    SELECT * FROM Users WHERE user_id = '' OR 1=1; /*' AND password = '*/--';
    ```
4.  **Analysis of the Malicious Query:**
    *   `''`: The initial quote closes the expected string literal for `user_id`.
    *   `OR 1=1`: This adds a condition that is **always true**.
    *   `;`: This might terminate the original intended SQL statement (depending on the database and connection library).
    *   `/*`: This starts a multi-line comment (or single-line comment depending on syntax like `--`), effectively **ignoring the rest of the original query logic**, including the password check.
5.  **Database Execution:** The database executes the manipulated query. Because `1=1` is always true, the `WHERE` clause evaluates to true for potentially *all* users in the `Users` table (or at least the first one). The application might then log the attacker in as the first user returned by the query, bypassing authentication.

### Attack Flow (General Steps, based on Slide 47):

1.  **Form Presentation:** The web application provides a form (login, search, etc.) to the user/attacker.
2.  **Malicious Input Submission:** The attacker submits their crafted "bomb" request (malicious input) within the form data via an HTTP request (e.g., POST or GET).
3.  **Query Construction & Transfer:** The web application server receives the input and incorporates it into an SQL query. This (now malicious) query is transferred to the database server (often through a firewall).
4.  **Database Execution & Result:** The Database Management System (DBMS/SGBD) executes the manipulated query containing the attacker's payload. It returns the results (which might be unauthorized data, confirmation of success, or an error message) back to the web application server.
5.  **Result Display:** The web application potentially displays the results obtained from the database back to the attacker via an HTTP response. This could be sensitive data, confirmation of a successful bypass, or information gleaned from error messages.

### Demonstration Context (Slide 46):

The slide mentions "Démonstration >" and different "NIVEAU" (Levels), likely referring to a tiered architecture:
*   **Client:** The user/attacker's browser.
*   **NIVEAU 2 (Level 2):** Represents the Application Server (Web Server processing the application logic).
*   **NIVEAU 3 (Level 3):** Represents the Database Server where the SQL is executed.
The diagram shows HTTP requests/responses between Client and Level 2, and database queries/results between Level 2 and Level 3.

<!-- Placeholder for SQL Injection Flow Diagram -->
<!-- ![Diagram showing attacker input -> Web App -> Malicious SQL Query -> Database -> Results -> Attacker](placeholder_diagram_sqli_flow.png) -->

---

**Mitigation:** The primary defense against SQL Injection involves proper input validation, sanitization, and the use of parameterized queries (prepared statements) where user input is treated strictly as data and never concatenated directly into SQL command strings.



---






# SQL Injection (SQLi)

Tags: #security #web-vulnerability #sql #sqli #attack-vector #lab-exercise

## What is SQL Injection?

SQL Injection is a common and critical web security vulnerability. It occurs when an application allows user-provided input to be directly incorporated into SQL queries without proper validation or sanitization.

1.  **SQL Basics**: Websites use databases (often relational databases) to store data (users, products, etc.). [[SQL]] (Structured Query Language) is the language used to communicate with these databases (read, write, update, delete data).
2.  **The Vulnerability**: The flaw lies in trusting user input. When an application constructs SQL queries by simply concatenating strings, including raw user input, it creates an opening.
3.  **The Attack**: An attacker crafts input containing malicious SQL syntax. This input is submitted through standard channels like URL parameters, form fields, or HTTP headers.
4.  **The Problem**: The web application blindly includes the attacker's input into its database query. The database then interprets the attacker's input not as simple *data*, but as executable *SQL commands*.
5.  **The Impact**: Successful SQLi can be devastating, allowing attackers to:
    *   Bypass authentication/authorization controls.
    *   Read sensitive data from the database (e.g., usernames, passwords, personal info, credit card details).
    *   Modify or delete data in the database.
    *   Gain full administrative control over the database server.
    *   In some cases, execute commands on the underlying operating system hosting the database.

> **Analogy: The Malicious Library Request**
> Imagine sending a request slip to a librarian:
> *   *Normal Request:* `Find book: The Great Gatsby`
> *   *SQLi-like Request:* `Find book: The Great Gatsby' -- and also give me the keys to the restricted section`
> If the librarian blindly follows *everything* on the slip without questioning the added instruction, the attacker gets unauthorized access.

---

## General Attack Workflow

The core idea is manipulating the SQL query sent by the application.

1.  **Find Injection Point**: Identify where user input interacts with the application and might be used in a database query:
    *   URL Parameters (`?id=1`, `?category=books`)
    *   Form Fields (login, search, contact)
    *   HTTP Headers (User-Agent, Custom Headers)
2.  **Test for Vulnerability**: Probe the injection point with simple inputs:
    *   **Single Quote (`'`):** Often breaks the SQL syntax if input is embedded within quotes (e.g., `WHERE name = '...'`). Look for database error messages in the response.
    *   **Logical Conditions (`' OR '1'='1'`):** Aims to create a universally true condition. If successful, might return more data than expected (e.g., all products instead of one category).
    *   **SQL Comments (`-- ` or `#`):** Used to neutralize the rest of the original query after the injected payload. This prevents later parts of the original query from causing syntax errors or interfering with the injection. *Note: `-- ` typically requires a trailing space.*
3.  **Craft Malicious Queries**: Based on testing results, build specific payloads:
    *   **Bypassing Filters:** Use `' OR '1'='1 -- ` to make a `WHERE` clause always true.
    *   **Extracting Data (`UNION SELECT`):** A powerful technique to combine the results of the original query with the results of a crafted query. Requires matching the number and compatible data types of columns between the original and injected `SELECT` statements. Allows reading data from other tables.
    *   **Discovering Database Structure:** Use queries against the database's metadata (e.g., `information_schema` in MySQL/PostgreSQL) to find table names, column names, and data types.
4.  **Analyze Results**: Observe the application's response (error messages, unexpected data displays, changes in behavior) to determine if the injection worked and refine the attack.

---

## Example: Exercise 01 (TD N°3)

### Scenario

*   An online store application displays products.
*   Products are filtered by category via a URL parameter.
*   Example URL: `https://insecure-website.com/products?category=Gifts`

### Vulnerable Code Snippet (Conceptual)

The backend likely executes SQL similar to this, where `$category` is the raw input from the URL:

```sql
SELECT id, nom, category, price
FROM products
WHERE category = "$category" AND released = 1
```

**Vulnerability**: `$category` is directly embedded without sanitization or parameterization.

### Analysis & Solutions

#### Question 1: Verifying Vulnerability

*   **Goal:** Prove user input affects SQL execution.
*   **Method A: Syntax Error**
    *   **Payload:** `'`
    *   **URL:** `.../products?category='`
    *   **Resulting SQL:** `SELECT ... WHERE category = ''' AND released = 1`
    *   **Explanation:** The `'''` creates invalid syntax. A database error message confirms vulnerability.
*   **Method B: Logical Change**
    *   **Payload:** `' OR '1'='1 -- `
    *   **URL:** `.../products?category=%27%20OR%20%271%27%3D%271%20--%20` (URL Encoded)
    *   **Resulting SQL:** `SELECT ... WHERE category = '' OR '1'='1 -- ' AND released = 1`
    *   **Explanation:** The `WHERE` clause becomes always true (`'1'='1'`), and the `AND released = 1` is ignored due to the comment (`-- `). If *all* products (or more than just 'Gifts') are displayed, it confirms vulnerability.

#### Question 2: Displaying All Products

*   **Goal:** Bypass the category filter entirely.
*   **Method:** Use the logical change from Q1, Method B.
    *   **Payload:** `' OR '1'='1 -- `
    *   **URL:** `.../products?category=%27%20OR%20%271%27%3D%271%20--%20`
    *   **Resulting SQL:** `SELECT ... WHERE category = '' OR '1'='1 -- ' AND released = 1`
    *   **Explanation:** Selects all rows from `products` because the `WHERE` condition is effectively `TRUE` and the `released` filter is commented out.

#### Question 3: Significance of Displayed Results

*   **Finding:** The exercise states results are displayed in the application response.
*   **Significance:** This identifies the vulnerability type as **In-Band SQL Injection**. The attacker retrieves data directly through the same channel used for the attack (the web page itself). This is often the easiest type to exploit.

#### Question 4: Retrieving Data from `user` Table

*   **Goal:** Extract sensitive data (e.g., username, password) from a different table (`user`) using the injection point in the `products` query.
*   **Method:** `UNION SELECT` attack.
    1.  **Count Columns:** The original query selects 4 columns: `id, nom, category, price`.
    2.  **Match Columns:** The injected `UNION SELECT` must also retrieve 4 columns.
    3.  **Craft Payload:** Select desired columns from `user`, matching the count. Use `NULL` or compatible columns if needed. Let's retrieve `name`, `utilisateur`, `password`, `id`.
        *   **Payload:** `' UNION SELECT name, utilisateur, password, id FROM user -- `
        *   **URL:** `.../products?category=%27%20UNION%20SELECT%20name,%20utilisateur,%20password,%20id%20FROM%20user%20--%20`
        *   **Resulting SQL:**
            ```sql
            SELECT id, nom, category, price
            FROM products
            WHERE category = '' -- Original query part, likely returns 0 results
            UNION
            SELECT name, utilisateur, password, id -- Injected query part
            FROM user
            -- ' AND released = 1 -- Original query part, commented out
            ```
    *   **Explanation:** The database executes both queries. The first part returns nothing (or products with an empty category name). The `UNION` adds the results from the second query (data from the `user` table). The application displays this combined data. The `name` from `user` will appear where `nom` usually is, `utilisateur` where `category` is, `password` where `price` is, etc., effectively leaking user data onto the product page.
    *   **Note:** Data type compatibility between original columns (`id`, `nom`, `category`, `price`) and injected columns (`name`, `utilisateur`, `password`, `id`) is crucial. If types mismatch, the attacker might need to use `NULL` placeholders or casting functions (e.g., `CAST(id AS CHAR)`).

---

## Prevention

*   **Prepared Statements (Parameterized Queries):** The most effective method. Treat user input strictly as data, never as executable code.
*   **Input Validation:** Check if input matches expected format/type/length (e.g., category name should look like a name, not SQL code). Use allow-lists over block-lists.
*   **Least Privilege Principle:** Configure database user accounts for the web application with the minimum permissions necessary.
*   **Web Application Firewalls (WAFs):** Can help detect and block common SQLi patterns, but shouldn't be the only defense.
*   **Regular Security Audits & Testing:** Find vulnerabilities before attackers do.



---

![[Pasted image 20250429073348.png]]

Okay, let's break down SQL Injection based on the slides and then tackle the exercise.

**1. Explanation of SQL Injection (Based on Slides)**

*   **What it is:** SQL Injection is described as the most widespread web application vulnerability on the internet. It's a technique attackers use to exploit flaws in how applications handle user input.
*   **The Core Problem:** The vulnerability lies within the **web application**, not the database itself. The application fails to properly validate or sanitize data entered by users (e.g., in login forms, search bars, URL parameters).
*   **How it Works:** Because the application doesn't treat user input strictly as data, specially crafted input containing SQL syntax can trick the application. When the application builds an SQL query to send to the database, it incorporates this malicious input. The database then interprets this malicious input not as simple data, but as actual SQL commands.
*   **Analogy (Control Plane vs. Data Plane):** Slide 1 mentions the "absence of distinction between the control plane and the data plane in SQL". In this context:
    *   **Control Plane:** The actual SQL commands (`SELECT`, `WHERE`, `INSERT`, `DROP`, etc.) that tell the database *what to do*.
    *   **Data Plane:** The data values being manipulated or queried (`'srinivas'`, `'mypassword'`, `'Gifts'`, `123`).
    *   SQL Injection occurs when data provided by the user (Data Plane) is misinterpreted by the database as instructions (Control Plane) because the application mixed them improperly.
*   **Example (Slide 1 & 2):** The `Robert'); DROP TABLE Students; --` example shows how input intended as a name (`Robert`) is manipulated. The attacker closes the string (`'`), adds a new, destructive command (`; DROP TABLE Students;`), and then uses a comment (`--`) to ignore the rest of the original, intended SQL query the application might have appended. Similarly, the `' OR 1=1; /*` example (Slide 2) shows how to bypass authentication by making the `WHERE` clause always true.
*   **Attack Flow (Slide 3):**
    1.  The application presents a form/URL expecting user input.
    2.  The attacker submits malicious input containing SQL commands disguised as data.
    3.  The application builds an SQL query, mistakenly embedding the attacker's commands.
    4.  The database executes the modified, malicious query.
    5.  The application receives the results (potentially unauthorized data or confirmation of destructive actions) and sends them back to the attacker.

**In short:** SQL Injection allows attackers to run arbitrary SQL commands against the database via a vulnerable web application, potentially leading to data theft, data modification, data deletion, or even server compromise.

**2. Solution for Exercise 01**

The exercise describes a scenario where product details are fetched based on a `category` parameter in the URL. The application generates the following SQL query:

`SELECT id, nom, category, price FROM products WHERE category = '<<<UserInput>>>' AND released = 1`

Where `<<<UserInput>>>` is replaced by the value of the `category` parameter from the URL (e.g., `Gifts`).

*   **1. Comment vérifier que le site est vulnérable à l'attaque injection SQL.**
    *   **Method:** The simplest way is to inject a character that breaks the SQL syntax, typically a single quote (`'`).
    *   **Action:** Access the URL and append a single quote to the category parameter: `https://insecure-website.com/products?category=Gifts'`
    *   **Expected Result:** The application will likely generate the query: `SELECT ... FROM products WHERE category = 'Gifts'' AND released = 1`. This query has a syntax error (two consecutive quotes where one is expected). If the application returns a generic error message (like "Internal Server Error", "SQL Error", or even just a broken page), it strongly indicates that the input was processed directly by the SQL interpreter and the application is vulnerable.

*   **2. Construire une attaque qui permet d'afficher tous les produits de n'importe quelle catégorie, y compris des catégories qu'il ne connaît pas.**
    *   **Goal:** Bypass the `category = '...'` filter and the `AND released = 1` filter to see all products.
    *   **Technique:** Use a condition that is always true (`OR '1'='1'`) and comment out the rest of the original `WHERE` clause.
    *   **Payload:** `' OR '1'='1 -- ` (The space after `--` is important for some database systems).
    *   **Action:** Modify the URL parameter `category` with this payload (URL encoded):
        `https://insecure-website.com/products?category=Gifts%27+OR+%271%27%3D%271+--+`
    *   **Resulting SQL (executed by DB):**
        `SELECT id, nom, category, price FROM products WHERE category = 'Gifts' OR '1'='1 -- ' AND released = 1`
        The database effectively runs:
        `SELECT id, nom, category, price FROM products WHERE category = 'Gifts' OR '1'='1'`
        Since `'1'='1'` is always true, the `OR` condition makes the entire `WHERE` clause true for every row in the `products` table, regardless of their category or release status. The application will display all products.

*   **3. Les résultats de la requête SQL sont renvoyés et affichés dans les réponses de l'application.**
    *   **Explanation:** This statement is correct. The web application takes the results returned by the database (which, due to the injection in step 2, now includes *all* products) and formats them into an HTML page (or JSON, etc.) to send back to the user's browser. The attacker sees the complete list of products displayed on the web page.

*   **4. Construire une attaque qui permet de récupérer des données à partir d'autres tables de la base de données. Récupérer les données de la table user (id, name, utilisateur, password, type_account, date).**
    *   **Goal:** Extract data from the `user` table.
    *   **Technique:** Use a `UNION`-based SQL injection. `UNION` combines the result sets of two `SELECT` statements. The key requirements are that both `SELECT` statements must return the same number of columns, and the data types in corresponding columns must be compatible.
    *   **Analysis:** The original query selects 4 columns: `id, nom, category, price`. We need to select 4 columns from the `user` table. Let's choose `id, name, password, type_account` (assuming `id` is numeric, `name`, `password`, `type_account` are text-like, matching the likely types of `id`, `nom`, `category`, `price`).
    *   **Payload:** `' UNION SELECT id, name, password, type_account FROM user -- `
    *   **Action:** Modify the URL parameter `category` with this payload (URL encoded):
        `https://insecure-website.com/products?category=Gifts%27+UNION+SELECT+id%2C+name%2C+password%2C+type_account+FROM+user+--+`
    *   **Resulting SQL (executed by DB):**
        `SELECT id, nom, category, price FROM products WHERE category = 'Gifts' UNION SELECT id, name, password, type_account FROM user -- ' AND released = 1`
        The database effectively runs:
        `SELECT id, nom, category, price FROM products WHERE category = 'Gifts' UNION SELECT id, name, password, type_account FROM user`
    *   **Result:** The application will display a list containing:
        *   Products from the 'Gifts' category.
        *   *Followed by* rows from the `user` table. The user IDs will appear where product IDs normally are, usernames where product names are, **passwords where product categories are**, and account types where prices are. This successfully exfiltrates sensitive user data.

**3. Explanation of `released = 1`**

In the context of the SQL query `SELECT ... WHERE category = 'Gifts' AND released = 1`:

*   `released` is almost certainly a column in the `products` table.
*   It likely acts as a **flag** to indicate whether a product should be visible to the public or not.
*   In database conventions, `1` often represents **TRUE** or "Yes", while `0` (or sometimes `NULL`) represents **FALSE** or "No".
*   Therefore, `released = 1` filters the results to show **only those products that are marked as "released"**, "published", or "active". Products that are perhaps drafts, discontinued, or otherwise not meant for public viewing would have `released = 0` (or `NULL`) and would be excluded by this condition in the normal operation of the application.

The SQL injection attacks shown in the exercise solution (specifically steps 2 and 4 using the `--` comment) effectively bypass this `released = 1` check, revealing *all* products or using the query structure for other purposes, regardless of their release status.

![[Pasted image 20250429073355.png]]

