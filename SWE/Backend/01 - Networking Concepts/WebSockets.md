# WebSockets

## What is WebSocket

WebSocket is a communication protocol that provides **full-duplex, bidirectional** communication between a client and a server over a single TCP connection. Unlike HTTP, which is **request-response** based, WebSocket allows for **real-time communication** without the need for repeated requests. This makes it ideal for applications where the server needs to push data to the client without waiting for a request, such as live chat systems, real-time dashboards, collaborative editing tools, stock market tickers, and multiplayer games.

WebSocket was standardized as RFC 6455 in 2011. It operates over the same ports as HTTP (port 80 for `ws://` and port 443 for `wss://`), which helps it work through firewalls and proxies that might block non-standard ports. The `wss://` scheme uses TLS encryption, providing the same security benefits as HTTPS for WebSocket connections.

---

## The WebSocket Handshake

Every WebSocket connection begins as a standard HTTP request. The client sends an HTTP GET request with an `Upgrade: websocket` header and a `Connection: Upgrade` header, requesting that the server switch protocols from HTTP to WebSocket. The request also includes a `Sec-WebSocket-Key` header containing a base64-encoded random value, and the `Sec-WebSocket-Version` header specifying the protocol version.

If the server supports WebSocket and accepts the connection, it responds with HTTP status **101 Switching Protocols**, along with an `Upgrade: websocket` header and a `Sec-WebSocket-Accept` header. The `Sec-WebSocket-Accept` value is computed by concatenating the client's key with a fixed GUID (`258EAFA5-E914-47DA-95CA-C5AB0DC85B11`) and hashing the result with SHA-1, then base64-encoding the hash. This proves that the server understood the WebSocket handshake and is not just a regular HTTP server returning a generic response.

Only after this successful HTTP upgrade exchange is the persistent, bidirectional WebSocket connection considered established. The server typically fires a `connection` event at this point, and both sides can begin sending and receiving messages at any time without waiting for the other side to request them.

---

## Basic WebSocket Example

Here is a simple WebSocket setup with a client and server.

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

The client connects to the server, sends a message, and the server echoes it back. This demonstrates the fundamental bidirectional communication model of WebSockets.

---

## Handling Multiple Clients

In most real-world applications, the server needs to handle multiple connected clients simultaneously. The following example shows how to broadcast a message from one client to all connected clients:

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

When one client sends a message, all connected clients receive it. This broadcast pattern is the foundation for chat rooms, live notifications, and other real-time features where multiple users need to see the same updates.

---

## Using WebSockets with JSON Data

For structured communication, WebSocket messages can carry JSON-encoded data. This allows the client and server to exchange complex, typed messages rather than plain strings.

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

Using JSON allows you to include message types, metadata, and structured payloads, making it easier to build complex real-time applications with clear message protocols.

---

## WebSocket with Authentication and Reconnection

Production WebSocket applications typically require authentication and resilient reconnection logic. Authentication is usually handled by sending a token (such as a JWT) as part of the initial connection URL or as the first message after the connection is established. Reconnection logic ensures that the client automatically reconnects if the connection drops.

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

This ensures the client **reconnects automatically** if disconnected. In production, you would also implement exponential backoff for reconnection attempts, handle authentication failures separately from connection drops, and manage message queues for messages sent while the connection is down.

---

## Understanding WebSocket Connections: What Counts?

When working with WebSockets, it is crucial to understand what actually establishes a connection versus what does not.

### What Counts as Establishing a Connection

- **Using a WebSocket Client to Initiate:** Explicitly creating a WebSocket object in client-side code (like `const ws = new WebSocket("ws://your-server-address")`) and successfully completing the handshake described above. The client must send the HTTP upgrade request and receive the 101 response.
- **Successful Handshake Completion:** The moment the client receives the `101 Switching Protocols` response from the server, confirming the protocol switch, the WebSocket connection is considered established. The server typically fires its `connection` event at this point.

### What Does NOT Count as Establishing a Connection

- **Typing a `ws://` URL into a Browser Address Bar:** Browsers do not handle raw `ws://` or `wss://` URLs directly like they do `http://`. Nothing will happen; you need client-side code (JavaScript) to initiate the connection.
- **Sending Standard HTTP Requests:** Using `fetch()`, `axios`, `curl` (without specific WebSocket flags), or similar tools to send regular HTTP GET/POST requests to the WebSocket endpoint will not establish a WebSocket connection. These lack the required `Upgrade` header and handshake mechanism.
- **Simple Network Pings (ICMP/TCP):** Standard network pings check network reachability but do not perform the WebSocket handshake.
- **WebSocket Ping/Pong Frames (Before Connection):** WebSockets have a built-in ping/pong mechanism using special frames to keep an already established connection alive or check its health. Sending these before a connection is fully established does not create one.

### After Connection

Once established, the connection remains open (persistent). Sending and receiving messages (`ws.send()`, `ws.onmessage`) uses this existing connection; it does not create new ones. The connection remains active until either side explicitly closes it or a network failure causes it to drop.

---

## Common Use Cases

WebSockets are particularly well-suited for applications that require real-time, bidirectional communication:

- **Live chat applications** where messages from any participant need to appear instantly for all other participants.
- **Real-time notifications** where the server pushes alerts to clients as events occur, without clients needing to poll for updates.
- **Stock market and financial dashboards** where price updates stream continuously and must be displayed with minimal latency.
- **Multiplayer games** where the game state must be synchronized across all players in real time.
- **Collaborative editing tools** where multiple users edit the same document simultaneously and see each other's changes instantly.
- **Live sports scores and IoT dashboards** where sensors or data feeds push updates to connected clients as data arrives.

---

## Related Concepts

- [[HTTP and HTTPS]] - Every WebSocket connection begins as an HTTP request with an `Upgrade: websocket` header. The server responds with HTTP status 101 before switching to the WebSocket protocol. Understanding HTTP is essential for understanding how WebSocket connections are established.
- [[XHR]] - While XHR uses HTTP request-response cycles for server communication, WebSockets provide a persistent, bidirectional alternative that is better suited for real-time applications. XHR is appropriate for occasional data fetching, while WebSockets are preferred when the server needs to push data to the client.
