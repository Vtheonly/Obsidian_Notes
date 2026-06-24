---
sources:
  - "[[08.00 Introduction]]"
  - "[[08.01 Transport Layer Role & Service Delivery Models]]"
  - "[[08.02 Logical Ports & Socket Programming Architecture]]"
  - "[[08.03 User Datagram Protocol (UDP) Architecture]]"
---

> [!question] The minimum header size of a TCP segment is 8 bytes.
>> [!success]- Answer
>> False

> [!question] In socket programming, the 'bind()' system call assigns a socket to a local IP address and port number.
>> [!success]- Answer
>> True

> [!question] A socket endpoint is uniquely defined as a combination of an IP address and a MAC address.
>> [!success]- Answer
>> False

> [!question] File Transfer Protocol (FTP) uses port 21 for control connection and port 20 for data connection.
>> [!success]- Answer
>> True

> [!question] TCP is a connection-oriented protocol that requires a three-way handshake before data transmission.
>> [!success]- Answer
>> True

> [!question] UDP tracks packet delivery and automatically requests retransmission of lost datagrams.
>> [!success]- Answer
>> False

> [!question] The Transport Layer provides logical communication between host systems, while the Network Layer provides logical communication between application processes.
>> [!success]- Answer
>> False

> [!question] On Unix-like systems, binding an application to a well-known port requires administrative privileges.
>> [!success]- Answer
>> True

> [!question] The UDP header Length field specifies the length of the UDP header only.
>> [!success]- Answer
>> False

> [!question] The 'listen()' system call is executed by a TCP client to initiate connection establishment.
>> [!success]- Answer
>> False

> [!question] What TCP flag is used during the handshake to acknowledge receipt of a connection request?
> a) ACK
> b) SYN
> c) FIN
> d) RST
>> [!success]- Answer
>> a) ACK

> [!question] What port does Internet Message Access Protocol (IMAP) utilize?
> a) TCP port 143
> b) TCP port 110
> c) TCP port 25
> d) TCP port 22
>> [!success]- Answer
>> a) TCP port 143

> [!question] What call blocks on a server until a TCP connection request is received?
> a) accept()
> b) connect()
> c) listen()
> d) bind()
>> [!success]- Answer
>> a) accept()

> [!question] Which TCP mechanism is used to prevent a sender from overwhelming the receiver's buffer?
> a) Segment reassembly
> b) Three-way handshake
> c) Slow Start / Congestion Avoidance
> d) Sliding Window / Flow Control
>> [!success]- Answer
>> d) Sliding Window / Flow Control

> [!question] Which system call is used by a server to bind a socket to a local IP and port?
> a) listen()
> b) bind()
> c) accept()
> d) socket()
>> [!success]- Answer
>> b) bind()

> [!question] What port and protocol does DNS utilize for standard name resolution queries?
> a) Port 67 UDP
> b) Port 53 TCP
> c) Port 80 TCP
> d) Port 53 UDP
>> [!success]- Answer
>> d) Port 53 UDP

> [!question] How is a socket endpoint defined?
> a) A MAC address and a Port number
> b) A Protocol and a Port number
> c) An IP address and a Port number
> d) An IP address and a MAC address
>> [!success]- Answer
>> c) An IP address and a Port number

> [!question] Which system call is used by a TCP client to initiate connection establishment?
> a) bind()
> b) listen()
> c) accept()
> d) connect()
>> [!success]- Answer
>> d) connect()

> [!question] What is the size of a standard, fixed UDP header?
> a) 32 bytes
> b) 8 bytes
> c) 20 bytes
> d) 16 bytes
>> [!success]- Answer
>> b) 8 bytes

> [!question] Which tuple uniquely identifies an active network connection?
> a) 4-Tuple: Src IP, Dst IP, Src Port, Dst Port
> b) 5-Tuple: Protocol, Src IP, Src Port, Dst IP, Dst Port
> c) 3-Tuple: IP, Port, MAC
> d) MAC 2-Tuple
>> [!success]- Answer
>> b) 5-Tuple: Protocol, Src IP, Src Port, Dst IP, Dst Port

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 5-Tuple
>> b) SMTP
>> c) Network Layer
>
>> [!example] Group B
>> n) Provides best-effort logical communication between host systems.
>> o) Protocol, Src IP, Src Port, Dst IP, Dst Port connection key.
>> p) Simple Mail Transfer Protocol mail relay on TCP port 25.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) accept()
>> b) Socket Endpoint
>> c) connect()
>
>> [!example] Group B
>> n) System call executed by TCP client to initiate connection.
>> o) System call blocking until a client connection arrives.
>> p) Unique identifier defined as <IP Address : Port Number>.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) UDP Length Field
>> b) SNMP
>> c) 5-Tuple
>
>> [!example] Group B
>> n) 16-bit field specifying total datagram size (min 8).
>> o) Protocol, Src IP, Src Port, Dst IP, Dst Port connection key.
>> p) Simple Network Management Protocol on UDP port 161.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Root Privilege
>> b) listen()
>> c) 5-Tuple
>
>> [!example] Group B
>> n) Protocol, Src IP, Src Port, Dst IP, Dst Port connection key.
>> o) Required on Unix systems to bind to ports below 1024.
>> p) System call shifting socket state to passive listening.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Network Layer
>> b) Dynamic / Ephemeral Ports
>> c) Flow Control
>
>> [!example] Group B
>> n) Temporary client source ports (49152 to 65535).
>> o) Prevents a fast sender from overwhelming a slow receiver.
>> p) Provides best-effort logical communication between host systems.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Telnet
>> b) IP Pseudo-header
>> c) IMAP
>
>> [!example] Group B
>> n) Internet Message Access Protocol on TCP port 143.
>> o) Contains Src/Dst IPs used in UDP checksum validation.
>> p) Unencrypted remote admin on TCP port 23.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Sliding Window
>> b) bind()
>> c) Dynamic / Ephemeral Ports
>
>> [!example] Group B
>> n) Dynamic window adjustment mechanism used by TCP for flow control.
>> o) System call assigning socket to local IP and port.
>> p) Temporary client source ports (49152 to 65535).
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Datagram
>> b) Network Layer
>> c) bind()
>
>> [!example] Group B
>> n) Provides best-effort logical communication between host systems.
>> o) System call assigning socket to local IP and port.
>> p) Transport Layer data unit when using UDP.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Process Multiplexing
>> b) UDP Length Field
>> c) FTP Data
>
>> [!example] Group B
>> n) Directing network traffic to correct application using ports.
>> o) File Transfer Protocol connection on TCP port 20.
>> p) 16-bit field specifying total datagram size (min 8).
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 5-Tuple
>> b) Listening Socket
>> c) POP3
>
>> [!example] Group B
>> n) Persistent server socket waiting for client connections.
>> o) Protocol, Src IP, Src Port, Dst IP, Dst Port connection key.
>> p) Post Office Protocol Version 3 on TCP port 110.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
