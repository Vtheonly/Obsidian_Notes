# Understanding XMLHttpRequest (XHR)

## What is XHR

XHR (XMLHttpRequest) is one of the oldest APIs used in JavaScript to communicate with a server asynchronously. It allows web pages to fetch or send data without reloading the page, enabling a smoother user experience. It was the foundation of **AJAX (Asynchronous JavaScript and XML)** before the modern `fetch()` API emerged. The name is somewhat historical; despite containing "XML," XHR can handle any text-based data format, with JSON being the most common in modern applications.

To understand XHR, imagine you are in a restaurant: you (the client) call a waiter (XHR) to place an order (request) to the kitchen (server). The waiter goes back and forth, bringing you updates about your order (response). You do not need to go to the kitchen yourself; the waiter handles it **asynchronously**. This is exactly how XHR works. It allows your webpage to communicate with a server **without refreshing**, which was revolutionary when it was first introduced and remains relevant in legacy codebases today.

---

## Making a Basic XHR Request (GET Request)

Here is how XHR makes a simple **GET request** to fetch data from a server:

```javascript
const xhr = new XMLHttpRequest(); // Create a new XHR object

xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1"); // Specify request type and URL

xhr.onload = () => { // Runs when the request is successful
    console.log("Response:", xhr.responseText); // Log the response data
};

xhr.send(); // Send the request
```

**Explanation:**

1. We create an `XMLHttpRequest` object.
2. We use `.open("GET", URL)` to tell it what kind of request we are making and to which URL.
3. The `.onload` function runs when the request is completed successfully.
4. `.send()` sends the request to the server.

**Output (Example):**

```json
{
  "userId": 1,
  "id": 1,
  "title": "Sample Post",
  "body": "This is an example post fetched using XHR."
}
```

This basic example retrieves data from an API and logs it in the console.

---

## Sending Data to a Server (POST Request)

When you need to **send** data instead of just fetching it, you use a `POST` request:

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

**Explanation:**

1. We set `POST` as the request type because we are sending data.
2. `setRequestHeader("Content-Type", "application/json")` tells the server we are sending **JSON data**.
3. We convert our JavaScript object into a JSON string using `JSON.stringify()`.
4. Finally, `.send(data)` sends the request with our JSON payload.

**Server Response Example:**

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

## Handling Errors and Status Codes

Sometimes things go wrong. The server might be down, or the request might be invalid. We need to handle errors properly.

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

**Explanation:**

1. `.status` contains the **HTTP status code** (e.g., `200` for success, `404` for not found).
2. We check if the status is between `200-299` (successful responses).
3. If there is an error, we log the `statusText` to explain the issue.
4. `.onerror` handles **network failures**, like when the internet is disconnected.

**Example Output (If Page Not Found):**

```
Error: 404 Not Found
```

This ensures we **gracefully handle failures** rather than breaking the app.

---

## Using XHR with Authentication and Progress Tracking

In real applications, you often need **authentication** (e.g., API keys, JWT tokens) and **progress tracking** for file uploads.

### Fetching Data with Authentication

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

**Explanation:**

1. **Authentication:** We add an `Authorization` header with a **JWT token** (used for secure API access).
2. **Tracking progress:**
    - `.onprogress(event)` logs how much data is **loaded** vs **total size**.
    - Useful for **large files** or **slow connections**.
3. The `onload` function ensures **only successful responses** are logged.

**Example Output:**

```
Loaded 5000 of 10000
Loaded 10000 of 10000
Authenticated response: { "data": "Secure content here" }
```

This is useful for **secure API calls** and tracking **large downloads/uploads**.

---

## XHR vs fetch() API

The `fetch()` API was introduced as a modern replacement for XHR, offering a cleaner syntax and a Promise-based interface. Understanding the differences between the two is important for working with both legacy and modern codebases.

### Syntax Comparison

**XHR approach:**

```javascript
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://api.example.com/data");
xhr.onload = () => {
    if (xhr.status >= 200 && xhr.status < 300) {
        console.log(JSON.parse(xhr.responseText));
    } else {
        console.error("Error:", xhr.status);
    }
};
xhr.onerror = () => console.error("Network error");
xhr.send();
```

**fetch() approach:**

```javascript
fetch("https://api.example.com/data")
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.error("Error:", error));
```

### Key Differences

| Feature | XHR | fetch() |
|---|---|---|
| **API style** | Event-based (`onload`, `onerror`, `onprogress`) | Promise-based (`.then()`, `.catch()`, `async/await`) |
| **Error handling** | Network errors trigger `onerror`; HTTP errors (4xx, 5xx) still trigger `onload` | Rejects the promise only on network errors; HTTP errors do not reject (must check `response.ok`) |
| **Progress tracking** | Built-in via `onprogress` event | No native progress events (requires `Response.body` streaming with `ReadableStream`) |
| **Request abort** | `xhr.abort()` | `AbortController` with `abort()` |
| **Timeout** | `xhr.timeout` property | No built-in timeout (use `AbortController` with `setTimeout`) |
| **Streaming** | Limited support via `responseType = "stream"` | Native streaming via `Response.body` (`ReadableStream`) |
| **CORS** | Requires `withCredentials` for cookies | Uses `credentials` option (`"include"`, `"same-origin"`, `"omit"`) |
| **Browser support** | All browsers including legacy IE | Modern browsers only (no IE support) |

### When to Use XHR

- **Legacy browser support:** Older Internet Explorer versions that do not support `fetch()`.
- **Tracking request progress:** When you need built-in progress events for file uploads or downloads without implementing custom streaming logic.
- **Fine-grained control over HTTP requests:** When you need to set specific headers at different stages of the request lifecycle or use XHR-specific features like `overrideMimeType()`.

### When to Use fetch()

- **Modern applications:** Any project targeting modern browsers where Promise-based code is preferred.
- **Cleaner, more readable code:** The Promise-based API integrates naturally with `async/await`, avoiding callback-heavy patterns.
- **Streaming responses:** When you need to process large responses incrementally using `ReadableStream`.
- **Service Workers:** The `fetch()` API is the standard way to intercept and modify requests in Service Workers.

---

## When to Use XHR vs WebSockets

XHR and WebSockets serve fundamentally different communication patterns. XHR uses the standard HTTP request-response model, where the client initiates every exchange and the server responds. This is appropriate for scenarios where the client needs data on demand, such as fetching user profiles, submitting forms, or loading paginated data. WebSockets provide a persistent, bidirectional connection where either side can send messages at any time, making them suitable for real-time features like live chat, notifications, and streaming data.

In many applications, both XHR (or `fetch()`) and WebSockets are used together: XHR for standard CRUD operations and authentication, and WebSockets for real-time updates. There is no need to choose exclusively between them; each excels at different communication patterns.

---

## Related Concepts

- [[HTTP and HTTPS]] - Every XHR request results in an HTTP request being sent to the server. The `xhr.open()` method specifies the HTTP method and URL, `xhr.setRequestHeader()` sets HTTP headers, and `xhr.status` reads the HTTP status code from the response. Understanding HTTP methods, headers, and status codes is essential for using XHR effectively.
- [[WebSockets]] - While XHR uses the HTTP request-response model, WebSockets provide a persistent, bidirectional alternative for real-time communication. XHR is appropriate for occasional data fetching, while WebSockets are preferred when the server needs to push data to the client without waiting for a request.
