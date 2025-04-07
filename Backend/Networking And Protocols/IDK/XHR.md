# **Understanding XMLHttpRequest (XHR) in 5 Stages (Easy to Hard)**

XHR (XMLHttpRequest) is one of the oldest APIs used in JavaScript to communicate with a server asynchronously. It allows web pages to fetch or send data without reloading the page, enabling a smoother user experience. It was the foundation of **AJAX (Asynchronous JavaScript and XML)** before the modern `fetch()` API emerged.

---

## **Stage 1: What is XHR? (Easy)**

Imagine you're in a restaurant:

- You (the client) call a waiter (XHR) to place an order (request) to the kitchen (server).
    
- The waiter goes back and forth, bringing you updates about your order (response).
    
- You don't need to go to the kitchen yourself; the waiter handles it **asynchronously**.
    

This is exactly how XHR works! It allows your webpage to communicate with a server **without refreshing**.

---

## **Stage 2: Making a Basic XHR Request (GET Request)**

Now, let's see how XHR makes a simple **GET request** to fetch data from a server:

```javascript
const xhr = new XMLHttpRequest(); // Create a new XHR object

xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1"); // Specify request type and URL

xhr.onload = () => { // Runs when the request is successful
    console.log("Response:", xhr.responseText); // Log the response data
};

xhr.send(); // Send the request
```

### **Explanation**:

1. We create an `XMLHttpRequest` object.
    
2. We use `.open("GET", URL)` to tell it what kind of request we're making and to which URL.
    
3. The `.onload` function runs when the request is completed successfully.
    
4. `.send()` sends the request to the server.
    

#### **Output (Example)**

```json
{
  "userId": 1,
  "id": 1,
  "title": "Sample Post",
  "body": "This is an example post fetched using XHR."
}
```

This basic example retrieves data from a fake API and logs it in the console.

---

## **Stage 3: Sending Data to a Server (POST Request)**

What if we want to **send** data instead of just fetching it? We use a `POST` request:

```javascript
const xhr = new XMLHttpRequest();
xhr.open("POST", "https://jsonplaceholder.typicode.com/posts"); // Sending data

xhr.setRequestHeader("Content-Type", "application/json"); // Telling the server we are sending JSON

xhr.onload = () => {
    console.log("Response:", xhr.responseText);
};

const data = JSON.stringify({ title: "New Post", body: "This is a test.", userId: 1 }); // Convert JS object to JSON
xhr.send(data); // Send the JSON data
```

### **Explanation**:

1. We set `POST` as the request type because we're sending data.
    
2. `setRequestHeader("Content-Type", "application/json")` tells the server we're sending **JSON data**.
    
3. We convert our JavaScript object into a JSON string using `JSON.stringify()`.
    
4. Finally, `.send(data)` sends the request with our JSON payload.
    

#### **Server Response Example:**

```json
{
  "title": "New Post",
  "body": "This is a test.",
  "userId": 1,
  "id": 101
}
```

Now the data is **stored on the server** (at least in a real application).

---

## **Stage 4: Handling Errors and Status Codes**

Sometimes, things **go wrong**. Maybe the server is down, or the request is invalid. We need to handle errors properly.

```javascript
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1000"); // A non-existent post

xhr.onload = () => {
    if (xhr.status >= 200 && xhr.status < 300) {
        console.log("Success:", xhr.responseText);
    } else {
        console.error("Error:", xhr.status, xhr.statusText);
    }
};

xhr.onerror = () => {
    console.error("Network error occurred");
};

xhr.send();
```

### **Explanation**:

1. `.status` contains the **HTTP status code** (e.g., `200` for success, `404` for not found).
    
2. We check if the status is between `200-299` (successful responses).
    
3. If there's an error, we log the `statusText` to explain the issue.
    
4. `.onerror` handles **network failures**, like when the internet is disconnected.
    

#### **Example Output (If Page Not Found)**:

```
Error: 404 Not Found
```

This ensures we **gracefully handle failures** rather than breaking the app.

---

## **Stage 5: Using XHR with Authentication & Progress Tracking**

In real applications, you often need:

- **Authentication** (e.g., API keys, JWT tokens).
    
- **Progress tracking** for file uploads.
    

### **Example: Fetching Data with Authentication**

```javascript
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://example.com/protected-data");

xhr.setRequestHeader("Authorization", "Bearer your_jwt_token"); // Adding authentication token

xhr.onprogress = (event) => {
    console.log(`Loaded ${event.loaded} of ${event.total}`);
};

xhr.onload = () => {
    if (xhr.status === 200) {
        console.log("Authenticated response:", xhr.responseText);
    } else {
        console.error("Access denied:", xhr.status);
    }
};

xhr.send();
```

### **Explanation**:

1. **Authentication**: We add an `Authorization` header with a **JWT token** (used for secure API access).
    
2. **Tracking progress**:
    
    - `.onprogress(event)` logs how much data is **loaded** vs **total size**.
        
    - Useful for **large files** or **slow connections**.
        
3. The `onload` function ensures **only successful responses** are logged.
    

#### **Example Output**:

```
Loaded 5000 of 10000
Loaded 10000 of 10000
Authenticated response: { "data": "Secure content here" }
```

This is useful for **secure API calls** and tracking **large downloads/uploads**.

---

## **Final Thoughts: When to Use XHR?**

**✅ XHR is useful for:**

- **Legacy browser support** (Older IE versions).
    
- **Tracking request progress** (e.g., file uploads).
    
- **Fine-grained control over HTTP requests**.
    

**❌ But it's outdated for:**

- Simple API calls → Use `fetch()` instead.
    
- WebSockets → For real-time applications.
    

XHR is a **powerful but old** tool. While it still has its use cases, most modern applications now use `fetch()` or WebSockets for better performance and readability. 🚀