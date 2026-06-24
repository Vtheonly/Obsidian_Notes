`req.query.name` is how you access **query parameters** in Express.js. Query parameters are part of the URL and provide additional information to the server in the form of key-value pairs.

Let’s break it down in detail:

---

### **What Are Query Parameters?**

- Query parameters are appended to the URL after a `?`.
- They are written as **key-value pairs**, separated by `&` for multiple parameters.

For example:

```
http://localhost:3000/greet?name=Mersel
```

In this URL:

- `greet` is the route.
- `name` is a query parameter key.
- `Mersel` is the value of the query parameter `name`.

---

### **How Does `req.query.name` Work?**

- `req.query` is an object in Express.js that contains all the query parameters from the URL.
- If you access `req.query.name`, you are retrieving the value of the `name` parameter from the query string.

---

### **Example Code**

```javascript
const express = require('express');
const app = express();
const port = 3000;

// Route with query parameters
app.get('/greet', (req, res) => {
  const name = req.query.name || 'Guest'; // Get the 'name' query parameter, default to 'Guest' if it's not provided
  res.send(`Hello, ${name}!`);
});

app.listen(port, () => {
  console.log(`App running at http://localhost:${port}`);
});
```

---

### **Testing the Code**

#### **Scenario 1: Passing the `name` Query Parameter**

Run the server and visit the URL:

```
http://localhost:3000/greet?name=Mersel
```

Here:

- `req.query.name` will contain `"Mersel"`.
- Response:
    
    ```
    Hello, Mersel!
    ```
    

---

#### **Scenario 2: Missing the `name` Query Parameter**

Visit the URL without the `name` parameter:

```
http://localhost:3000/greet
```

Here:

- `req.query.name` is `undefined` because the `name` parameter isn’t provided.
- The code defaults to `"Guest"` using the `||` operator:
    
    ```javascript
    const name = req.query.name || 'Guest';
    ```
    
- Response:
    
    ```
    Hello, Guest!
    ```
    

---

### **Key Points**

1. **`req.query`**:
    
    - It's an object that holds all query parameters from the URL.
    - For `http://localhost:3000/greet?name=Mersel&age=20`, `req.query` will look like:
        
        ```javascript
        {
          name: 'Mersel',
          age: '20'
        }
        ```
        
2. **Accessing Query Parameters**:
    
    - Use `req.query.<key>` to access a specific query parameter, e.g., `req.query.name` or `req.query.age`.
3. **Default Values**:
    
    - Use the `||` operator to provide a default value if the query parameter is missing:
        
        ```javascript
        const name = req.query.name || 'Guest';
        ```
        

---

### **When to Use Query Parameters**

Query parameters are typically used for:

- Filtering or searching:
    
    ```
    /search?keyword=nodejs
    ```
    
- Pagination:
    
    ```
    /users?page=2&limit=10
    ```
    
- Sorting:
    
    ```
    /products?sort=price&order=asc
    ```
    

---

Let me know if you’d like to explore query parameters further, like how to validate or handle multiple query parameters effectively!