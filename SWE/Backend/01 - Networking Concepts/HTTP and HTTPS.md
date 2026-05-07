# HTTP and HTTPS

## What is HTTP

HTTP (HyperText Transfer Protocol) is the foundational communication protocol of the World Wide Web. It defines how messages are formatted and transmitted between clients (typically web browsers) and servers (web servers hosting content). HTTP operates on a strict request-response model: the client sends a request to the server, and the server returns a response. This cycle repeats for every resource the client needs, whether that resource is an HTML page, an image, a stylesheet, or an API payload.

HTTP is inherently stateless, meaning that each request-response pair is independent and the server does not retain any memory of previous interactions by default. Every request must contain all the information the server needs to understand and process it. This statelessness simplifies server design and improves reliability, because the server does not need to manage session state across requests. However, it also means that mechanisms like cookies, session tokens, and hidden form fields must be used to simulate stateful interactions when they are needed, such as maintaining a user's logged-in session across multiple page loads.

### HTTP Methods

HTTP defines a set of request methods that indicate the desired action to be performed on a given resource. The most commonly used methods are GET, POST, PUT, DELETE, and PATCH. Each method has a specific semantic meaning that both clients and servers are expected to honor.

- **GET** retrieves a representation of the specified resource. GET requests should only retrieve data and should not modify server state. They are considered safe and idempotent, meaning that making the same GET request multiple times produces the same result without side effects on the server.
- **POST** submits data to be processed by the target resource. POST requests typically create new resources or trigger server-side processing. Unlike GET, POST is neither safe nor idempotent, because each request may create a new resource or cause a different side effect.
- **PUT** replaces the entire target resource with the supplied payload. PUT is idempotent, because sending the same PUT request multiple times results in the same resource state on the server. It is commonly used for full resource updates.
- **DELETE** removes the specified resource from the server. Like PUT, DELETE is idempotent because deleting a resource that has already been deleted results in the same end state (the resource is gone).
- **PATCH** applies partial modifications to a resource. Unlike PUT, which replaces the entire resource, PATCH only updates the fields specified in the request payload. PATCH is not guaranteed to be idempotent, depending on how the server implements the patch logic.

### HTTP Status Codes

HTTP status codes are three-digit numbers returned by the server in its response to indicate the outcome of the client's request. They are grouped into five categories based on their first digit.

- **1xx Informational:** These codes indicate that the request was received and the server is continuing the process. For example, `100 Continue` tells the client that the server has received the initial part of the request and the client should continue sending the rest.
- **2xx Success:** These codes indicate that the request was successfully received, understood, and accepted. The most common is `200 OK`, which means the request succeeded. Other examples include `201 Created` (a new resource was successfully created) and `204 No Content` (the request succeeded but there is no content to return).
- **3xx Redirection:** These codes indicate that further action is needed by the client to complete the request, typically by following a redirect to a different URL. For example, `301 Moved Permanently` indicates that the resource has been permanently moved to a new URL, while `302 Found` indicates a temporary redirect. The `304 Not Modified` code is used in caching scenarios to indicate that the cached version of the resource is still valid.
- **4xx Client Error:** These codes indicate that the client made an error in its request. The most well-known is `404 Not Found`, meaning the requested resource does not exist on the server. Other examples include `400 Bad Request` (malformed request syntax), `401 Unauthorized` (authentication required), `403 Forbidden` (authenticated but not authorized), and `429 Too Many Requests` (rate limiting).
- **5xx Server Error:** These codes indicate that the server failed to fulfill a valid request. Common examples include `500 Internal Server Error` (a generic server-side failure), `502 Bad Gateway` (the server acting as a gateway received an invalid response from an upstream server), `503 Service Unavailable` (the server is temporarily unable to handle the request, often due to overload or maintenance), and `504 Gateway Timeout` (the upstream server did not respond in time).

### HTTP Headers

HTTP headers are key-value pairs sent in both requests and responses that provide essential metadata about the message. They control caching behavior, specify content formats, handle authentication, manage CORS policies, and much more.

- **Content-Type** specifies the media type of the resource or the data being sent. For example, `application/json` indicates JSON data, `text/html` indicates an HTML document, and `multipart/form-data` is used for file uploads.
- **Authorization** carries credentials that the client uses to authenticate itself to the server. The most common format is `Bearer <token>`, where the token is typically a JWT (JSON Web Token) issued by an authentication service.
- **Cache-Control** directs caching mechanisms on how to handle the response. Values like `no-cache`, `no-store`, `max-age=3600`, and `public` or `private` control whether and for how long responses can be cached by browsers and intermediate proxies.
- **CORS Headers** control cross-origin resource sharing, which determines whether a web page running at one origin is allowed to make requests to a different origin. The key headers include `Access-Control-Allow-Origin` (specifies which origins are permitted), `Access-Control-Allow-Methods` (lists allowed HTTP methods), `Access-Control-Allow-Headers` (lists allowed request headers), and `Access-Control-Allow-Credentials` (indicates whether cookies and authentication headers can be included in cross-origin requests).

Other important request headers include `Accept` (what content types the client can handle), `User-Agent` (identifies the client software), `Cookie` (sends previously stored cookies to the server), and `Referer` (indicates the URL of the page that linked to the current request). Important response headers include `Set-Cookie` (instructs the browser to store a cookie), `Location` (used with redirects to specify the new URL), and `X-Request-ID` (used for tracing requests across distributed systems).

---

## What is HTTPS

HTTPS (HyperText Transfer Protocol Secure) is the encrypted version of HTTP. It combines standard HTTP with TLS (Transport Layer Security) encryption to protect the data transmitted between client and server from eavesdropping, tampering, and forgery. When a user visits an HTTPS URL, the browser establishes a secure TLS connection before sending any HTTP data, ensuring that all subsequent communication is encrypted and cannot be read or modified by intermediaries.

### The TLS Handshake

The TLS handshake is the process by which the client and server negotiate encryption parameters and establish a shared secret before any application data is exchanged. In TLS 1.2, the handshake typically proceeds as follows: the client sends a ClientHello message containing supported TLS versions, cipher suites, and a random number; the server responds with a ServerHello message selecting the TLS version and cipher suite, along with its digital certificate and a random number; the client verifies the server's certificate against trusted certificate authorities; the client and server perform a key exchange (often using RSA or Diffie-Hellman) to derive a shared pre-master secret; both sides independently compute the master secret and session keys; and finally, both sides exchange Finished messages to confirm the handshake is complete. TLS 1.3 streamlined this process significantly by reducing the number of round trips required and removing support for older, less secure cryptographic algorithms.

### Certificate Authorities

Certificate Authorities (CAs) are trusted third-party organizations that issue digital certificates binding a public key to a specific domain or organization. When a browser connects to an HTTPS site, it checks whether the server's certificate was issued by a CA that the browser trusts. Major CAs include Let's Encrypt, DigiCert, GlobalSign, and Sectigo. Browsers and operating systems ship with a pre-installed set of root CA certificates, forming a chain of trust. If a server presents a certificate that chains back to one of these trusted roots, the browser accepts the connection as authentic.

### Why HTTPS Matters

HTTPS is critical for modern web security. Without encryption, any data sent over HTTP can be intercepted and read by anyone with access to the network path between client and server. This includes passwords, credit card numbers, personal information, and session tokens. HTTPS prevents eavesdropping through encryption, prevents tampering through message integrity checks, and provides authentication through certificate validation, ensuring that users are connecting to the legitimate server and not an impostor. Modern web features such as HTTP/2, service workers, geolocation, and many JavaScript APIs are only available over HTTPS, making it a practical necessity as well as a security requirement.

---

## HTTP/1.1 vs HTTP/2 vs HTTP/3

The HTTP protocol has evolved significantly over the years to address performance limitations and adapt to changing network conditions. Each major version introduces improvements in how requests and responses are transmitted.

### HTTP/1.1

HTTP/1.1, formalized in RFC 7230-7235, was the dominant version of HTTP for over two decades. It introduced persistent connections (keep-alive) so that multiple requests could be sent over a single TCP connection, reducing the overhead of establishing new connections for each resource. It also added chunked transfer encoding, the Host header (enabling virtual hosting), and pipelining. However, pipelining was rarely used in practice because of head-of-line blocking at the application layer, where a slow response blocks all subsequent responses on the same connection. Browsers typically opened six parallel TCP connections per origin to work around this limitation, which introduced its own overhead and connection management costs.

### HTTP/2

HTTP/2, published in 2015, addressed the limitations of HTTP/1.1 by introducing multiplexing, header compression, and server push. Multiplexing allows multiple requests and responses to be interleaved on a single TCP connection using binary frames and streams, eliminating the need for multiple parallel connections and reducing head-of-line blocking at the HTTP layer. Header compression using HPACK reduces the overhead of repetitive headers across requests. Server push allows the server to proactively send resources that it knows the client will need, though this feature has seen mixed adoption. Despite these improvements, HTTP/2 still operates over TCP, so head-of-line blocking can occur at the transport layer if a TCP packet is lost, stalling all streams on that connection until the packet is retransmitted.

### HTTP/3

HTTP/3, standardized in 2022, replaces TCP with QUIC (Quick UDP Internet Connections) as the underlying transport protocol. QUIC runs over UDP and implements its own reliability, congestion control, and encryption mechanisms. Because QUIC streams are independent at the transport level, a lost packet only blocks the specific stream it belongs to, not all streams on the connection. This eliminates the TCP-level head-of-line blocking that affected HTTP/2. QUIC also integrates TLS 1.3 directly into the handshake, reducing connection establishment latency and enabling 0-RTT (zero round-trip time) connection resumption for returning clients. Additionally, QUIC supports connection migration, allowing a connection to survive changes in the client's IP address (such as switching from Wi-Fi to cellular), which is not possible with TCP.

---

## Relationship to Other Networking Concepts

HTTP is deeply intertwined with many other networking concepts covered in this vault. [[WebSockets]] begin as an HTTP request with an `Upgrade: websocket` header, and the server responds with HTTP status `101 Switching Protocols` before the connection is promoted to a full-duplex WebSocket connection. This means that every WebSocket connection starts its life as an HTTP connection, and understanding HTTP is essential for understanding how WebSockets are established.

[[XHR]] (XMLHttpRequest) is a browser API that uses HTTP to send asynchronous requests from JavaScript. Every `xhr.open()` and `xhr.send()` call results in an HTTP request being sent to the server, and the response is processed using standard HTTP status codes and headers. The modern `fetch()` API serves the same purpose but with a cleaner, Promise-based interface.

[[SNI Injector Explained]] relies on the TLS handshake that underpins HTTPS connections. By manipulating the SNI (Server Name Indication) field in the TLS ClientHello message, SNI injectors can make SSH traffic appear as legitimate HTTPS traffic to network filters. This technique depends entirely on the structure of the HTTPS handshake and the way intermediate network devices inspect SNI fields to make filtering decisions.

[[SSL and TLS]] provides the encryption layer that transforms HTTP into HTTPS. Without TLS, there would be no HTTPS, and all web traffic would be transmitted in plaintext. The TLS handshake, certificate validation, and key exchange mechanisms are all essential components that make secure web communication possible.

---

## Key Takeaways

HTTP is the foundational protocol of the web, operating on a stateless request-response model with well-defined methods, status codes, and headers. HTTPS adds a critical layer of security through TLS encryption, protecting data in transit from interception and tampering. The protocol has evolved from HTTP/1.1 through HTTP/2 to HTTP/3, each version addressing performance bottlenecks and improving the efficiency of data transfer. Understanding HTTP and HTTPS is essential for working with virtually any web technology, from building web applications to diagnosing network issues to understanding advanced techniques like SNI injection.
