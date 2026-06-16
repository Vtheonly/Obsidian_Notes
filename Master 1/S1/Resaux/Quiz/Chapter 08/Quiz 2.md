---
sources:
  - "[[08.00 Introduction]]"
  - "[[08.01 Transport Layer Role & Service Delivery Models]]"
  - "[[08.02 Logical Ports & Socket Programming Architecture]]"
  - "[[08.03 User Datagram Protocol (UDP) Architecture]]"
---

> [!question] Port 22 is associated with unencrypted Telnet administration.
>> [!success]- Answer
>> False

> [!question] Hypertext Transfer Protocol Secure (HTTPS) uses TCP port 443.
>> [!success]- Answer
>> True

> [!question] UDP is a connectionless protocol because it sends packets immediately without establishing a session.
>> [!success]- Answer
>> True

> [!question] Simple Mail Transfer Protocol (SMTP) uses TCP port 110.
>> [!success]- Answer
>> False

> [!question] The 'accept()' system call blocks until a client connection request arrives, returning a new connection socket.
>> [!success]- Answer
>> True

> [!question] Post Office Protocol Version 3 (POP3) uses TCP port 110.
>> [!success]- Answer
>> True

> [!question] The UDP checksum is calculated over a pseudo-header that includes source and destination IP addresses.
>> [!success]- Answer
>> True

> [!question] TCP flow control prevents a fast sender from overwhelming the network infrastructure.
>> [!success]- Answer
>> False

> [!question] The UDP header is fixed at 8 bytes in length.
>> [!success]- Answer
>> True

> [!question] UDP checksum verification is mandatory in IPv4.
>> [!success]- Answer
>> False

> [!question] What are data units at the Transport Layer called when using TCP?
> a) Datagrams
> b) Segments
> c) Packets
> d) Frames
>> [!success]- Answer
>> b) Segments

> [!question] What TCP port is used for Secure Shell (SSH) connections?
> a) 22
> b) 443
> c) 80
> d) 23
>> [!success]- Answer
>> a) 22

> [!question] Which protocol is best suited for DNS queries and DHCP packets due to low overhead?
> a) SSH
> b) BGP
> c) TCP
> d) UDP
>> [!success]- Answer
>> d) UDP

> [!question] What does the UDP checksum calculation include to verify that a packet was not misrouted?
> a) MAC Address Table
> b) OSI Session ID
> c) L2 Frame Trailer
> d) IP Pseudo-header
>> [!success]- Answer
>> d) IP Pseudo-header

> [!question] What does TCP congestion control adjust in response to network congestion?
> a) Congestion Window / Transmission Rate
> b) Destination Port Number
> c) Sequence Number offset
> d) Sliding Window Size
>> [!success]- Answer
>> a) Congestion Window / Transmission Rate

> [!question] What is the correct sequence of flags sent during the TCP three-way handshake?
> a) ACK -> SYN -> SYN-ACK
> b) SYN -> ACK -> SYN-ACK
> c) SYN -> SYN -> ACK
> d) SYN -> SYN-ACK -> ACK
>> [!success]- Answer
>> d) SYN -> SYN-ACK -> ACK

> [!question] Which field in the UDP header specifies the combined size of the header and payload?
> a) Length
> b) Checksum
> c) Source Port
> d) Destination Port
>> [!success]- Answer
>> a) Length

> [!question] Which port is used by Simple Mail Transfer Protocol (SMTP) for mail relay?
> a) 25
> b) 110
> c) 143
> d) 587
>> [!success]- Answer
>> a) 25

> [!question] What is the minimum possible value for the UDP Length field?
> a) 8
> b) 20
> c) 0
> d) 16
>> [!success]- Answer
>> a) 8

> [!question] Which port is used by FTP for the control connection?
> a) TCP port 22
> b) TCP port 21
> c) TCP port 23
> d) TCP port 20
>> [!success]- Answer
>> b) TCP port 21

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 5-Tuple
>> b) TCP Port 179
>> c) Sliding Window
>
>> [!example] Group B
>> n) BGP peer session transport port.
>> o) Dynamic window adjustment mechanism used by TCP for flow control.
>> p) Protocol, Src IP, Src Port, Dst IP, Dst Port connection key.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Sliding Window
>> b) TCP Header Size
>> c) listen()
>
>> [!example] Group B
>> n) Minimum size of 20 bytes.
>> o) Dynamic window adjustment mechanism used by TCP for flow control.
>> p) System call shifting socket state to passive listening.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TFTP
>> b) TCP Port 179
>> c) 5-Tuple
>
>> [!example] Group B
>> n) Trivial File Transfer Protocol on UDP port 69.
>> o) Protocol, Src IP, Src Port, Dst IP, Dst Port connection key.
>> p) BGP peer session transport port.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TCP Header Size
>> b) DHCP Client
>> c) Datagram
>
>> [!example] Group B
>> n) Minimum size of 20 bytes.
>> o) Transport Layer data unit when using UDP.
>> p) Bootstrap protocol client listening on UDP port 68.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Three-Way Handshake
>> b) 5-Tuple
>> c) IP Pseudo-header
>
>> [!example] Group B
>> n) SYN -> SYN-ACK -> ACK sequence to establish a session.
>> o) Protocol, Src IP, Src Port, Dst IP, Dst Port connection key.
>> p) Contains Src/Dst IPs used in UDP checksum validation.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) IMAP
>> b) Listening Socket
>> c) UDP Length Field
>
>> [!example] Group B
>> n) 16-bit field specifying total datagram size (min 8).
>> o) Persistent server socket waiting for client connections.
>> p) Internet Message Access Protocol on TCP port 143.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) DHCP Client
>> b) Process Multiplexing
>> c) Network Layer
>
>> [!example] Group B
>> n) Bootstrap protocol client listening on UDP port 68.
>> o) Directing network traffic to correct application using ports.
>> p) Provides best-effort logical communication between host systems.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Network Layer
>> b) IP Pseudo-header
>> c) DHCP Server
>
>> [!example] Group B
>> n) Contains Src/Dst IPs used in UDP checksum validation.
>> o) Provides best-effort logical communication between host systems.
>> p) Bootstrap protocol server listening on UDP port 67.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) HTTPS
>> b) DHCP Server
>> c) Congestion Control
>
>> [!example] Group B
>> n) Prevents network infrastructure from becoming overwhelmed.
>> o) Bootstrap protocol server listening on UDP port 67.
>> p) Encrypted Web protocol on TCP port 443.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) SMTP
>> b) Congestion Control
>> c) POP3
>
>> [!example] Group B
>> n) Simple Mail Transfer Protocol mail relay on TCP port 25.
>> o) Post Office Protocol Version 3 on TCP port 110.
>> p) Prevents network infrastructure from becoming overwhelmed.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
