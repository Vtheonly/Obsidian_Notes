---
sources:
  - "[[08.00 Introduction]]"
  - "[[08.01 Transport Layer Role & Service Delivery Models]]"
  - "[[08.02 Logical Ports & Socket Programming Architecture]]"
  - "[[08.03 User Datagram Protocol (UDP) Architecture]]"
---

> [!question] TCP uses a sliding window mechanism for flow control.
>> [!success]- Answer
>> True

> [!question] Internet Message Access Protocol (IMAP) uses TCP port 143.
>> [!success]- Answer
>> True

> [!question] TCP ensures ordered delivery of data by using sequence numbers in the header.
>> [!success]- Answer
>> True

> [!question] Ephemeral ports are dynamically assigned by the OS to act as client source ports.
>> [!success]- Answer
>> True

> [!question] Well-Known Ports range from 0 to 1024.
>> [!success]- Answer
>> False

> [!question] BGP peer connections utilize UDP port 179.
>> [!success]- Answer
>> False

> [!question] In TCP, data chunks are referred to as segments, while in UDP they are called datagrams.
>> [!success]- Answer
>> True

> [!question] DHCP server listening port is UDP port 68.
>> [!success]- Answer
>> False

> [!question] UDP congestion control dynamically slows down transmission speed when network packet loss is detected.
>> [!success]- Answer
>> False

> [!question] A server maintains multiple listening sockets on a single port to handle concurrent clients.
>> [!success]- Answer
>> False

> [!question] What type of socket remains bound to the configured server port to receive incoming requests?
> a) Connection Socket
> b) Ephemeral Socket
> c) Socket Endpoint
> d) Listening Socket
>> [!success]- Answer
>> d) Listening Socket

> [!question] What is the minimum header size of a TCP segment?
> a) 20 bytes
> b) 8 bytes
> c) 16 bytes
> d) 32 bytes
>> [!success]- Answer
>> a) 20 bytes

> [!question] Which protocol is connection-oriented, guarantees delivery, and ensures ordered data reassembly?
> a) UDP
> b) IP
> c) ICMP
> d) TCP
>> [!success]- Answer
>> d) TCP

> [!question] Which socket programming call shifts a socket state to passive listening?
> a) accept()
> b) bind()
> c) listen()
> d) connect()
>> [!success]- Answer
>> c) listen()

> [!question] Under Unix-like systems, which user privilege is needed to bind a socket to a port below 1024?
> a) Standard User privilege
> b) Nobody user group
> c) Root / Administrative privilege
> d) Guest privilege
>> [!success]- Answer
>> c) Root / Administrative privilege

> [!question] What port is used by Post Office Protocol Version 3 (POP3)?
> a) TCP port 25
> b) TCP port 80
> c) TCP port 143
> d) TCP port 110
>> [!success]- Answer
>> d) TCP port 110

> [!question] Which port does a DHCP client use?
> a) UDP port 67
> b) UDP port 53
> c) TCP port 443
> d) UDP port 68
>> [!success]- Answer
>> d) UDP port 68

> [!question] What is a primary characteristic of UDP?
> a) Connection-oriented, reliable session
> b) High header size overhead
> c) Connectionless, best-effort delivery
> d) Guaranteed ordered segment delivery
>> [!success]- Answer
>> c) Connectionless, best-effort delivery

> [!question] Which socket is created by the accept() call to handle data exchange with a specific client?
> a) Connection Socket
> b) Raw Socket
> c) Standard Socket
> d) Listening Socket
>> [!success]- Answer
>> a) Connection Socket

> [!question] Which port range represents Ephemeral or Dynamic Ports?
> a) 1024 to 49151
> b) 0 to 1023
> c) 49152 to 65535
> d) 30000 to 40000
>> [!success]- Answer
>> c) 49152 to 65535

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) DHCP Client
>> b) DHCP Server
>> c) Sliding Window
>
>> [!example] Group B
>> n) Bootstrap protocol server listening on UDP port 67.
>> o) Bootstrap protocol client listening on UDP port 68.
>> p) Dynamic window adjustment mechanism used by TCP for flow control.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) SNMP
>> b) Segment
>> c) Well-Known Ports
>
>> [!example] Group B
>> n) Simple Network Management Protocol on UDP port 161.
>> o) Reserved system ports ranging from 0 to 1023.
>> p) Transport Layer data unit when using TCP.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Well-Known Ports
>> b) bind()
>> c) IP Pseudo-header
>
>> [!example] Group B
>> n) System call assigning socket to local IP and port.
>> o) Reserved system ports ranging from 0 to 1023.
>> p) Contains Src/Dst IPs used in UDP checksum validation.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Datagram
>> b) DHCP Server
>> c) Segment
>
>> [!example] Group B
>> n) Transport Layer data unit when using UDP.
>> o) Transport Layer data unit when using TCP.
>> p) Bootstrap protocol server listening on UDP port 67.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) bind()
>> b) UDP Header Size
>> c) Telnet
>
>> [!example] Group B
>> n) Fixed size of 8 bytes.
>> o) System call assigning socket to local IP and port.
>> p) Unencrypted remote admin on TCP port 23.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TFTP
>> b) FTP Control
>> c) Network Layer
>
>> [!example] Group B
>> n) File Transfer Protocol connection on TCP port 21.
>> o) Provides best-effort logical communication between host systems.
>> p) Trivial File Transfer Protocol on UDP port 69.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Three-Way Handshake
>> b) IP Pseudo-header
>> c) FTP Control
>
>> [!example] Group B
>> n) SYN -> SYN-ACK -> ACK sequence to establish a session.
>> o) File Transfer Protocol connection on TCP port 21.
>> p) Contains Src/Dst IPs used in UDP checksum validation.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TCP Header Size
>> b) connect()
>> c) Ordered Delivery
>
>> [!example] Group B
>> n) System call executed by TCP client to initiate connection.
>> o) TCP feature using sequence numbers to reassemble data.
>> p) Minimum size of 20 bytes.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) connect()
>> b) DHCP Server
>> c) UDP Header Size
>
>> [!example] Group B
>> n) Fixed size of 8 bytes.
>> o) Bootstrap protocol server listening on UDP port 67.
>> p) System call executed by TCP client to initiate connection.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) connect()
>> b) DHCP Client
>> c) Socket Endpoint
>
>> [!example] Group B
>> n) Unique identifier defined as <IP Address : Port Number>.
>> o) Bootstrap protocol client listening on UDP port 68.
>> p) System call executed by TCP client to initiate connection.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
