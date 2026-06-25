
##  What Are Sessions in Flask?

###  In a web context:

A **session** is a way to **store data across multiple requests** from the same user.

HTTP is **stateless** by design:

> The server doesn’t remember anything between two requests.

###  So why do we need sessions?

Because you often want to **track the user**:

- Did they log in?
    
- What’s in their cart?
    
- What page were they on?
    

###  Flask `session` object:

Flask provides a special `session` object — basically a Python dictionary — to store user-specific data **on the server or via cookies**.

```python
from flask import session

# Set a session key
session['username'] = 'marshal'

# Access it later
print(session['username'])  # marshal
```

---

##  Is the session stored in memory or the browser?

By default, Flask uses **signed cookies** to store session data.  
That means:

- It's saved in the user's browser.
    
- It’s **encrypted and signed** so it can’t be tampered with.
    
- But it’s not private — only secure from modification.
    

###  You need a secret key:

```python
app.secret_key = 'some_super_secret_key'
```

You can also plug in **server-side session systems** (like Redis or a DB) if you want to store larger or private data.

---

##  Common Use-Cases of Flask Sessions:

|Use Case|Example|
|---|---|
|Authentication|Store `user_id` when a user logs in|
|Shopping Cart|Store items in cart during checkout flow|
|Preferences|Dark mode, language setting, etc.|
|Flash Messages|Store temporary feedback between redirects|

---

##  When do sessions expire?

- When the **browser closes** (default)
    
- Or you set a custom timeout
    
- Or manually `session.clear()` or `session.pop('key')`
    

---
