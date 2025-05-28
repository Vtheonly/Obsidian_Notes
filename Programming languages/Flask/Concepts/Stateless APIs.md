
## 📦 What Are Stateless APIs?

Now let's switch gears to your second question:

---

## 🔄 Stateless vs Stateful APIs

### 🧊 Stateless API = Each request is **independent**.

> The server does **not store any memory of previous requests.**  
> Every request contains **all the information** needed to complete it.

This is the design of **RESTful APIs**:

```http
GET /user/123
Authorization: Bearer <token>
```

Even if the user just made another request a second ago, this new request is **fresh and self-contained**.

---

### ✅ Benefits of Stateless APIs:

- Easy to scale horizontally (no server memory)
    
- Simpler to cache, load-balance, and debug
    
- Lower memory usage on server
    

---

### ❌ Drawbacks:

- Repetitive data sent in every request
    
- Can’t preserve temporary context between requests (unless you use sessions or client-side state)
    

---

## 🔁 Stateful APIs?

> Server **remembers** something between requests.

Examples:

- WebSocket connections
    
- Some older SOAP-based APIs
    
- Any custom API that uses server sessions instead of stateless tokens
    

---

## 🤝 So How Do Stateless APIs Handle Login?

With **tokens**, typically JWT (JSON Web Tokens):

- You log in once → server sends you a signed token
    
- You attach the token in **every future request**
    
- The server decodes the token and knows who you are
    

No memory is kept on the server.

---

## 🧠 TL;DR Summary

|Concept|Meaning|
|---|---|
|`session`|Temporary data store for a user across multiple HTTP requests (stateful)|
|Stateless API|An API where each request is isolated, carries all info it needs|
|Flask session|Encrypted cookie-based key-value storage per user|

---

Would you like a diagram showing the flow of **stateless vs stateful auth**, or how Flask sessions work with logins?