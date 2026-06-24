## 2.4. Session State Management with Cookies and Local Storage

HTTP is a stateless protocol; by default, every request is treated as completely independent of any prior request. To maintain sessions (e.g., keeping a user logged in), web applications must store state across requests.

---

### 1. Cookies vs. Web Storage (Local & Session)

Web browsers provide different client-side storage mechanisms, each designed for specific use cases:

| Feature | HTTP Cookies | Local Storage | Session Storage |
| :--- | :--- | :--- | :--- |
| **Capacity** | ~4 KB | ~5 - 10 MB | ~5 MB |
| **Sent with HTTP Requests?**|  Yes (automatically by browser) |  No |  No |
| **Expiration** | Set manually via cookie header | Persistent until cleared | Cleared when browser tab closes |
| **Access Methods** | Server HTTP headers / JavaScript | Client-side JavaScript only | Client-side JavaScript only |
| **Security Risk** | CSRF, XSS | XSS (very vulnerable) | XSS (very vulnerable) |

---

### 2. Cookie Security Attributes

Because cookies are automatically attached to matching outgoing domain requests, they are a primary target for security attacks. Modern applications secure cookies using specific flag attributes:

```
Set-Cookie: session_id=abc123xyz; Secure; HttpOnly; SameSite=Strict
```

#### `HttpOnly`
Prevents client-side scripts (JavaScript) from accessing the cookie via `document.cookie`. This is a vital mitigation against **Cross-Site Scripting (XSS)** attacks, ensuring that malicious scripts injected into the webpage cannot steal sensitive session tokens.

#### `Secure`
Instructs the browser to only transmit the cookie over encrypted **HTTPS** connections. This prevents attackers from sniffing session identifiers out of unencrypted Wi-Fi packets (Man-in-the-Middle attacks).

#### `SameSite`
Controls whether cookies are sent along with requests initiated by third-party websites. It is the primary defense against **Cross-Site Request Forgery (CSRF)**:
* **`SameSite=Strict`:** The cookie is only sent if the site listed in the browser's address bar matches the cookie's host domain.
* **`SameSite=Lax`:** The browser sends the cookie only on "safe" cross-site navigations (specifically top-level GET requests, such as clicking a normal link to navigate to the site).
* **`SameSite=None`:** Cookies are sent with all cross-site requests (requires the `Secure` flag to be set).

---

###  Common Student Pitfalls & Pro-Tips
* **Missing Cookie Domains:** When setting or mocking cookies in automation scripts, pay close attention to the **domain** and **path** attributes. If your script sets a cookie for `example.com` but attempts to make an automated request to `api.example.com`, the browser/cookie-jar will not attach the cookie unless the domain attribute was configured to allow subdomains (e.g., `.example.com`).

---
