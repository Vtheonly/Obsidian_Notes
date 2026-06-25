## Python `socket` Module

### **1. Overview**
The `socket` module in Python provides low-level networking interfaces, allowing programs to communicate over a network using **TCP, UDP, and raw sockets**.

---

### **2. Importing the Module**
```python
import socket
```

---

### **3. Creating a Socket**
#### **TCP Socket (SOCK_STREAM)**
```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
- `AF_INET` → IPv4 Address Family
- `SOCK_STREAM` → TCP (connection-oriented)

#### **UDP Socket (SOCK_DGRAM)**
```python
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```
- `SOCK_DGRAM` → UDP (connectionless)

---

### **4. Server Socket Example (TCP)**
```python
import socket

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 8080))  # Bind to localhost on port 8080
server_socket.listen(5)  # Allow 5 connections in queue
print("Server listening on port 8080...")

while True:
    client_socket, addr = server_socket.accept()  # Accept new connection
    print(f"Connection from {addr}")
    
    data = client_socket.recv(1024).decode("utf-8")
    print(f"Received: {data}")
    
    client_socket.send("Hello from server!".encode("utf-8"))  # Send response
    client_socket.close()
```

---

### **5. Client Socket Example (TCP)**
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 8080))  # Connect to server

client_socket.send("Hello Server!".encode("utf-8"))  # Send data
response = client_socket.recv(1024).decode("utf-8")  # Receive response

print("Server response:", response)
client_socket.close()
```

---

### **6. UDP Communication Example**
#### **UDP Server**
```python
import socket

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(("127.0.0.1", 8080))

print("UDP Server listening on port 8080...")
while True:
    data, addr = udp_server.recvfrom(1024)  # Receive data
    print(f"Received '{data.decode()} from {addr}")
    udp_server.sendto("Hello UDP Client!".encode(), addr)  # Send response
```

#### **UDP Client**
```python
import socket

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client.sendto("Hello UDP Server!".encode(), ("127.0.0.1", 8080))

response, _ = udp_client.recvfrom(1024)  # Receive response
print("Server response:", response.decode())
udp_client.close()
```

---

### **7. Common Methods**
| Method                     | Description                                    |
|----------------------------|------------------------------------------------|
| `bind(address)`            | Binds the socket to a specific IP/port        |
| `listen(backlog)`         | Listens for incoming connections (TCP only)   |
| `accept()`                 | Accepts an incoming connection (TCP)          |
| `connect(address)`         | Connects to a remote server (TCP)             |
| `send(data)`               | Sends data over a TCP connection              |
| `sendto(data, address)`    | Sends data over UDP                           |
| `recv(bufsize)`            | Receives data (TCP)                           |
| `recvfrom(bufsize)`        | Receives data (UDP)                           |
| `close()`                  | Closes the socket connection                  |

---

### **8. Handling Multiple Clients (Threaded Server)**
```python
import socket
import threading

def handle_client(client_socket):
    data = client_socket.recv(1024).decode("utf-8")
    print(f"Received: {data}")
    client_socket.send("Hello from server!".encode("utf-8"))
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 8080))
server_socket.listen(5)
print("Server listening on port 8080...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
```

---

### **9. Non-Blocking Sockets**
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(False)  # Set non-blocking mode
```
- **Blocking Mode** → `sock.recv(1024)` waits until data arrives.
- **Non-blocking Mode** → Returns immediately, even if no data is available.

---

### **10. Exception Handling**
```python
import socket

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("invalid.host", 8080))
except socket.error as e:
    print(f"Socket error: {e}")
```

---

### **11. Summary**
- `socket.AF_INET`: IPv4
- `socket.AF_INET6`: IPv6
- `socket.SOCK_STREAM`: TCP
- `socket.SOCK_DGRAM`: UDP
- Use `bind()` to assign an IP/port
- Use `listen()` and `accept()` for server-client TCP
- Use `sendto()` and `recvfrom()` for UDP
- Handle multiple clients using **threads**
- Use **exception handling** for errors

---

### **12. Useful Links**
- [Python socket documentation](https://docs.python.org/3/library/socket.html)
