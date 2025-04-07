### **Stage 1: What is WebSocket? (Easy)**

WebSocket is a communication protocol that provides **full-duplex, bidirectional** communication between a client and a server over a single TCP connection. Unlike HTTP, which is **request-response** based, WebSocket allows for **real-time communication** without the need for repeated requests.

---

### **Stage 2: Basic WebSocket Example**

Here’s a simple WebSocket setup:

**Client-side (JavaScript in Browser):**

```javascript
const socket = new WebSocket("ws://localhost:3000");

socket.onopen = () => {
    console.log("Connected to server");
    socket.send("Hello, Server!");
};

socket.onmessage = (event) => {
    console.log("Message from server:", event.data);
};

socket.onclose = () => {
    console.log("Disconnected from server");
};
```

**Server-side (Node.js using WebSocket library):**

```javascript
const WebSocket = require("ws");
const server = new WebSocket.Server({ port: 3000 });

server.on("connection", (ws) => {
    console.log("Client connected");
    ws.send("Welcome to WebSocket server!");

    ws.on("message", (message) => {
        console.log("Received:", message);
        ws.send("Server Echo: " + message);
    });

    ws.on("close", () => {
        console.log("Client disconnected");
    });
});
```

Here, the client connects to the server, sends a message, and the server echoes it back.

---

### **Stage 3: Handling Multiple Clients**

To support multiple clients efficiently:

```javascript
const WebSocket = require("ws");
const server = new WebSocket.Server({ port: 3000 });

server.on("connection", (ws) => {
    console.log("New client connected");

    ws.on("message", (message) => {
        console.log("Received:", message);
        // Broadcast to all connected clients
        server.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(`Broadcast: ${message}`);
            }
        });
    });
});
```

Now, when one client sends a message, all connected clients receive it.

---

### **Stage 4: Using WebSockets with JSON Data**

To send structured data:

**Client:**

```javascript
const socket = new WebSocket("ws://localhost:3000");

socket.onopen = () => {
    const data = { type: "chat", message: "Hello, everyone!" };
    socket.send(JSON.stringify(data));
};

socket.onmessage = (event) => {
    const receivedData = JSON.parse(event.data);
    console.log("Received:", receivedData);
};
```

**Server:**

```javascript
server.on("connection", (ws) => {
    ws.on("message", (message) => {
        const data = JSON.parse(message);
        console.log("Received:", data);

        // Broadcast JSON data
        server.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({ type: "response", message: "Got your message!" }));
            }
        });
    });
});
```

Now, the communication is structured and supports JSON-based messaging.

---

### **Stage 5: WebSocket with Authentication and Reconnection**

For secure WebSockets:

- Use authentication (JWT, API key).
    
- Handle reconnections.
    

**Example with Reconnection:**

```javascript
let socket;

function connect() {
    socket = new WebSocket("ws://localhost:3000");

    socket.onopen = () => {
        console.log("Connected!");
        socket.send(JSON.stringify({ authToken: "your_token_here" }));
    };

    socket.onmessage = (event) => {
        console.log("Message:", event.data);
    };

    socket.onclose = () => {
        console.log("Disconnected, reconnecting in 3 seconds...");
        setTimeout(connect, 3000);
    };
}

connect();
```

This ensures the client **reconnects automatically** if disconnected.

---

### **Final Thoughts**

WebSockets are great for:

- **Live chats**
    
- **Real-time notifications**
    
- **Stock market updates**
    
- **Multiplayer games**
    

By mastering WebSockets, you can build **fast and interactive** web applications! 🚀