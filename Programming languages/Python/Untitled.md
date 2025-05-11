---
sources:
  - "[[Python socket Module]]"
---
> [!question] The `socket` module in Python only supports communication via the TCP protocol.
>> [!success]- Answer
>> False

> [!question] `socket.AF_INET` is the constant used to specify the IPv4 address family when creating a socket.
>> [!success]- Answer
>> True

> [!question] `socket.SOCK_STREAM` indicates that a UDP socket should be created.
>> [!success]- Answer
>> False

> [!question] The `bind()` method is used by a TCP server to start listening for incoming connections.
>> [!success]- Answer
>> False

> [!question] The `listen()` method in a TCP server specifies the maximum number of connections that can be queued before refusing new ones.
>> [!success]- Answer
>> True

> [!question] The `connect()` method is typically called on the client-side socket to establish a TCP connection with a server.
>> [!success]- Answer
>> True

> [!question] UDP, often used with `socket.SOCK_DGRAM`, is a connection-oriented protocol ensuring guaranteed delivery.
>> [!success]- Answer
>> False

> [!question] The `recvfrom()` method is the standard way to receive data on a connected TCP socket.
>> [!success]- Answer
>> False

> [!question] Using threads is a common technique to allow a server to handle multiple client connections concurrently.
>> [!success]- Answer
>> True

> [!question] By default, Python sockets operate in non-blocking mode, meaning calls like `recv()` return immediately even if no data is available.
>> [!success]- Answer
>> False