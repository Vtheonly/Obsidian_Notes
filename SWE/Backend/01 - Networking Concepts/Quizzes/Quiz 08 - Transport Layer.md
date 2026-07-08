---
title: "Quiz 08 — Transport Layer"
type: quiz
chapter: 08
sources:
  - "[[10 - Transport Layer/10.01 Transport Layer Functions]]"
  - "[[10 - Transport Layer/10.02 Ports & Sockets]]"
  - "[[10 - Transport Layer/10.03 Well-Known Ports Reference]]"
  - "[[10 - Transport Layer/10.04 Socket Programming Lifecycle]]"
  - "[[10 - Transport Layer/10.05 UDP]]"
  - "[[10 - Transport Layer/10.06 TCP]]"
  - "[[10 - Transport Layer/10.07 TCP Header Fields]]"
  - "[[10 - Transport Layer/10.08 TCP Connection Lifecycle]]"
  - "[[10 - Transport Layer/10.09 TCP Flow Control & Windowing]]"
  - "[[10 - Transport Layer/10.10 TCP Reliability & Congestion Control]]"
  - "[[10 - Transport Layer/10.11 TCP vs UDP Comparison]]"
tags: [quiz, transport, tcp, udp, ports]
---

#  Quiz 08 — Transport Layer

> [!abstract] Test Your Knowledge
> This quiz covers ports, sockets, the socket API, UDP, TCP (header, handshake, flow control, congestion control), and the TCP vs UDP choice.

---

## Part 1 — True / False

> [!question] Separate connection sockets allow a server to communicate with active clients while continuing to listen for new connections.
>> [!success]- Answer
>> **True.** `accept()` returns a new connection socket; the listening socket stays open.

> [!question] Trivial File Transfer Protocol (TFTP) uses UDP port 69.
>> [!success]- Answer
>> **True.**

> [!question] Port numbers are 16-bit unsigned integers, providing a range from 0 to 65535.
>> [!success]- Answer
>> **True.**

> [!question] UDP is better suited for real-time applications like VoIP than TCP.
>> [!success]- Answer
>> **True.** Latency matters more than reliability for VoIP.

> [!question] Domain Name System (DNS) queries typically run over UDP port 53.
>> [!success]- Answer
>> **True.** DNS uses UDP for queries; TCP for zone transfers and large responses.

> [!question] The TCP three-way handshake sequence is SYN → ACK → SYN-ACK.
>> [!success]- Answer
>> **False.** Correct order: SYN → SYN-ACK → ACK.

> [!question] The minimum value of the UDP header Length field is 8 bytes.
>> [!success]- Answer
>> **True.** (8-byte header + 0 payload = length 8.)

> [!question] Simple Network Management Protocol (SNMP) uses UDP port 161.
>> [!success]- Answer
>> **True.**

> [!question] A connection key 5-tuple includes: Protocol, Source IP, Source Port, Destination IP, and Destination Port.
>> [!success]- Answer
>> **True.**

> [!question] Well-known port numbers are assigned by IANA.
>> [!success]- Answer
>> **True.**

> [!question] Port 22 is associated with unencrypted Telnet administration.
>> [!success]- Answer
>> **False.** Port 22 = SSH. Telnet = port 23.

> [!question] Hypertext Transfer Protocol Secure (HTTPS) uses TCP port 443.
>> [!success]- Answer
>> **True.**

> [!question] UDP is a connectionless protocol because it sends packets immediately without establishing a session.
>> [!success]- Answer
>> **True.**

> [!question] Simple Mail Transfer Protocol (SMTP) uses TCP port 110.
>> [!success]- Answer
>> **False.** SMTP = 25. POP3 = 110.

> [!question] The 'accept()' system call blocks until a client connection request arrives, returning a new connection socket.
>> [!success]- Answer
>> **True.**

> [!question] Post Office Protocol Version 3 (POP3) uses TCP port 110.
>> [!success]- Answer
>> **True.**

> [!question] The UDP checksum is calculated over a pseudo-header that includes source and destination IP addresses.
>> [!success]- Answer
>> **True.**

> [!question] TCP flow control prevents a fast sender from overwhelming the network infrastructure.
>> [!success]- Answer
>> **False.** Flow control protects the **receiver**. Congestion control protects the **network**.

> [!question] The UDP header is fixed at 8 bytes in length.
>> [!success]- Answer
>> **True.**

> [!question] UDP checksum verification is mandatory in IPv4.
>> [!success]- Answer
>> **False.** Optional in IPv4; mandatory in IPv6.

> [!question] TCP uses a sliding window mechanism for flow control.
>> [!success]- Answer
>> **True.**

> [!question] Internet Message Access Protocol (IMAP) uses TCP port 143.
>> [!success]- Answer
>> **True.**

> [!question] TCP ensures ordered delivery of data by using sequence numbers in the header.
>> [!success]- Answer
>> **True.**

> [!question] Ephemeral ports are dynamically assigned by the OS to act as client source ports.
>> [!success]- Answer
>> **True.**

> [!question] Well-Known Ports range from 0 to 1024.
>> [!success]- Answer
>> **False.** 0–1023. (1024 is the start of Registered Ports.)

> [!question] BGP peer connections utilize UDP port 179.
>> [!success]- Answer
>> **False.** BGP uses **TCP** port 179.

> [!question] In TCP, data chunks are referred to as segments, while in UDP they are called datagrams.
>> [!success]- Answer
>> **True.**

> [!question] DHCP server listening port is UDP port 68.
>> [!success]- Answer
>> **False.** DHCP server = UDP 67; client = UDP 68.

> [!question] UDP congestion control dynamically slows down transmission speed when network packet loss is detected.
>> [!success]- Answer
>> **False.** UDP has no congestion control.

> [!question] The minimum header size of a TCP segment is 8 bytes.
>> [!success]- Answer
>> **False.** TCP minimum is 20 bytes. UDP is 8.

> [!question] On Unix-like systems, binding an application to a well-known port requires administrative privileges.
>> [!success]- Answer
>> **True.** Ports < 1024 require root or `CAP_NET_BIND_SERVICE`.

---

## Part 2 — Multiple Choice

> [!question] What port does SNMP use to listen for management requests?
> a) TCP port 110
> b) UDP port 162
> c) UDP port 161
> d) TCP port 25
>> [!success]- Answer
>> **c) UDP port 161** (162 is for SNMP traps)

> [!question] What port is mapped to unencrypted HTTP traffic?
> a) TCP port 23
> b) TCP port 80
> c) TCP port 443
> d) TCP port 21
>> [!success]- Answer
>> **b) TCP port 80**

> [!question] What layer of the OSI model sits directly above the network layer and resolves its best-effort deficiencies?
> a) Session Layer
> b) Application Layer
> c) Data Link Layer
> d) Transport Layer
>> [!success]- Answer
>> **d) Transport Layer**

> [!question] Which protocol is faster due to lack of connection establishment and flow control overhead?
> a) BGP
> b) TCP
> c) UDP
> d) SMTP
>> [!success]- Answer
>> **c) UDP**

> [!question] What port is mapped to HTTPS?
> a) TCP port 443
> b) TCP port 21
> c) TCP port 80
> d) TCP port 22
>> [!success]- Answer
>> **a) TCP port 443**

> [!question] Which port range represents the Well-Known Ports?
> a) 49152 to 65535
> b) 0 to 1023
> c) 1024 to 49151
> d) 0 to 255
>> [!success]- Answer
>> **b) 0 to 1023**

> [!question] Which application protocol is mapped to UDP port 69?
> a) TFTP
> b) SNMP
> c) DNS
> d) FTP
>> [!success]- Answer
>> **a) TFTP**

> [!question] What is the port range for Registered Ports?
> a) 1024 to 49151
> b) 0 to 1023
> c) 1000 to 2000
> d) 49152 to 65535
>> [!success]- Answer
>> **a) 1024 to 49151**

> [!question] Which port does a DHCP server listen on?
> a) UDP port 68
> b) UDP port 69
> c) UDP port 67
> d) TCP port 80
>> [!success]- Answer
>> **c) UDP port 67**

> [!question] What is process multiplexing?
> a) Splitting packets across multiple routes
> b) Directing concurrent traffic to correct applications using ports
> c) Load balancing traffic at switch level
> d) Translating local private IPs to public IPs
>> [!success]- Answer
>> **b) Directing concurrent traffic to correct applications using ports**

> [!question] What are data units at the Transport Layer called when using TCP?
> a) Datagrams
> b) Segments
> c) Packets
> d) Frames
>> [!success]- Answer
>> **b) Segments**

> [!question] What TCP port is used for Secure Shell (SSH) connections?
> a) 22
> b) 443
> c) 80
> d) 23
>> [!success]- Answer
>> **a) 22**

> [!question] Which protocol is best suited for DNS queries and DHCP packets due to low overhead?
> a) SSH
> b) BGP
> c) TCP
> d) UDP
>> [!success]- Answer
>> **d) UDP**

> [!question] What does the UDP checksum calculation include to verify that a packet was not misrouted?
> a) MAC Address Table
> b) OSI Session ID
> c) L2 Frame Trailer
> d) IP Pseudo-header
>> [!success]- Answer
>> **d) IP Pseudo-header**

> [!question] What does TCP congestion control adjust in response to network congestion?
> a) Congestion Window / Transmission Rate
> b) Destination Port Number
> c) Sequence Number offset
> d) Sliding Window Size
>> [!success]- Answer
>> **a) Congestion Window / Transmission Rate** (cwnd)

> [!question] What is the correct sequence of flags sent during the TCP three-way handshake?
> a) ACK → SYN → SYN-ACK
> b) SYN → ACK → SYN-ACK
> c) SYN → SYN → ACK
> d) SYN → SYN-ACK → ACK
>> [!success]- Answer
>> **d) SYN → SYN-ACK → ACK**

> [!question] Which field in the UDP header specifies the combined size of the header and payload?
> a) Length
> b) Checksum
> c) Source Port
> d) Destination Port
>> [!success]- Answer
>> **a) Length**

> [!question] Which port is used by Simple Mail Transfer Protocol (SMTP) for mail relay?
> a) 25
> b) 110
> c) 143
> d) 587
>> [!success]- Answer
>> **a) 25** (587 is submission with auth)

> [!question] What is the minimum possible value for the UDP Length field?
> a) 8
> b) 20
> c) 0
> d) 16
>> [!success]- Answer
>> **a) 8** (8-byte header + 0 payload)

> [!question] Which port is used by FTP for the control connection?
> a) TCP port 22
> b) TCP port 21
> c) TCP port 23
> d) TCP port 20
>> [!success]- Answer
>> **b) TCP port 21** (20 is the FTP data channel)

> [!question] What type of socket remains bound to the configured server port to receive incoming requests?
> a) Connection Socket
> b) Ephemeral Socket
> c) Socket Endpoint
> d) Listening Socket
>> [!success]- Answer
>> **d) Listening Socket**

> [!question] What is the minimum header size of a TCP segment?
> a) 20 bytes
> b) 8 bytes
> c) 16 bytes
> d) 32 bytes
>> [!success]- Answer
>> **a) 20 bytes**

> [!question] Which protocol is connection-oriented, guarantees delivery, and ensures ordered data reassembly?
> a) UDP
> b) IP
> c) ICMP
> d) TCP
>> [!success]- Answer
>> **d) TCP**

> [!question] Which socket programming call shifts a socket state to passive listening?
> a) accept()
> b) bind()
> c) listen()
> d) connect()
>> [!success]- Answer
>> **c) listen()**

> [!question] What is a primary characteristic of UDP?
> a) Connection-oriented, reliable session
> b) High header size overhead
> c) Connectionless, best-effort delivery
> d) Guaranteed ordered segment delivery
>> [!success]- Answer
>> **c) Connectionless, best-effort delivery**

> [!question] Which socket is created by the accept() call to handle data exchange with a specific client?
> a) Connection Socket
> b) Raw Socket
> c) Standard Socket
> d) Listening Socket
>> [!success]- Answer
>> **a) Connection Socket**

> [!question] Which port range represents Ephemeral or Dynamic Ports?
> a) 1024 to 49151
> b) 0 to 1023
> c) 49152 to 65535
> d) 30000 to 40000
>> [!success]- Answer
>> **c) 49152 to 65535**

> [!question] What TCP flag is used during the handshake to acknowledge receipt of a connection request?
> a) ACK
> b) SYN
> c) FIN
> d) RST
>> [!success]- Answer
>> **a) ACK**

> [!question] What is the size of a standard, fixed UDP header?
> a) 32 bytes
> b) 8 bytes
> c) 20 bytes
> d) 16 bytes
>> [!success]- Answer
>> **b) 8 bytes**

> [!question] Which tuple uniquely identifies an active network connection?
> a) 4-Tuple: Src IP, Dst IP, Src Port, Dst Port
> b) 5-Tuple: Protocol, Src IP, Src Port, Dst IP, Dst Port
> c) 3-Tuple: IP, Port, MAC
> d) MAC 2-Tuple
>> [!success]- Answer
>> **b) 5-Tuple: Protocol, Src IP, Src Port, Dst IP, Dst Port**

---

## Part 3 — Matching

> [!question] Match the socket API call with its purpose.
>> [!example] Group A
>> a) socket()
>> b) bind()
>> c) listen()
>> d) accept()
>
>> [!example] Group B
>> n) Block until a client connects; returns new connection FD
>> o) Create a socket file descriptor
>> p) Mark socket as passive (accept connections)
>> q) Assign socket to a local (IP, port)
>
>> [!success]- Answer
>> a) → o)
>> b) → q)
>> c) → p)
>> d) → n)

> [!question] Match the TCP header field with its purpose.
>> [!example] Group A
>> a) Sequence Number
>> b) Acknowledgment Number
>> c) Window Size
>> d) Checksum
>
>> [!example] Group B
>> n) Error detection over pseudo-header + header + payload
>> o) Position of first byte of payload in the byte stream
>> p) Receiver's advertised buffer space (flow control)
>> q) Next byte the sender expects to receive
>
>> [!success]- Answer
>> a) → o)
>> b) → q)
>> c) → p)
>> d) → n)

> [!question] Match the TCP control flag with its purpose.
>> [!example] Group A
>> a) SYN
>> b) ACK
>> c) FIN
>> d) RST
>
>> [!example] Group B
>> n) Reset the connection (abort)
>> o) Synchronize sequence numbers (start handshake)
>> p) Confirm receipt (used in handshake and ongoing)
>> q) Sender is done sending data (graceful close)
>
>> [!success]- Answer
>> a) → o)
>> b) → p)
>> c) → q)
>> d) → n)

> [!question] Match the protocol with its transport.
>> [!example] Group A
>> a) HTTP
>> b) DNS
>> c) BGP
>> d) DHCP
>
>> [!example] Group B
>> n) TCP port 80
>> o) UDP port 67/68
>> p) TCP port 179
>> q) UDP port 53 (typically; TCP for zone transfers)
>
>> [!success]- Answer
>> a) → n)
>> b) → q)
>> c) → p)
>> d) → o)

> [!question] Match the protocol with its well-known port.
>> [!example] Group A
>> a) SSH
>> b) HTTPS
>> c) SMTP
>> d) SNMP
>
>> [!example] Group B
>> n) UDP 161
>> o) TCP 22
>> p) TCP 25
>> q) TCP 443
>
>> [!success]- Answer
>> a) → o)
>> b) → q)
>> c) → p)
>> d) → n)

> [!question] Match the property with the protocol (TCP or UDP).
>> [!example] Group A
>> a) Connection-oriented (3-way handshake)
>> b) Connectionless, best-effort
>> c) Sliding window flow control
>> d) Multicast/broadcast supported
>
>> [!example] Group B
>> n) UDP
>> o) TCP
>> p) TCP
>> q) UDP
>
>> [!success]- Answer
>> a) → o)
>> b) → n)
>> c) → p)
>> d) → q)

> [!question] Match the congestion control phase with its behavior.
>> [!example] Group A
>> a) Slow Start
>> b) Congestion Avoidance
>> c) Fast Retransmit
>> d) Fast Recovery
>
>> [!example] Group B
>> n) On 3 duplicate ACKs, retransmit immediately
>> o) cwnd doubles every RTT (exponential)
>> p) After Fast Retransmit, halve cwnd and continue (instead of slow start)
>> q) After ssthresh, cwnd grows linearly (1 MSS per RTT)
>
>> [!success]- Answer
>> a) → o)
>> b) → q)
>> c) → n)
>> d) → p)

> [!question] Match the TCP state with its meaning.
>> [!example] Group A
>> a) LISTEN
>> b) SYN_SENT
>> c) ESTABLISHED
>> d) TIME_WAIT
>
>> [!example] Group B
>> n) Server is waiting for connections
>> o) Connection is open and data can flow
>> p) Active closer waiting 2×MSL before final close
>> q) Client has sent SYN, waiting for SYN-ACK
>
>> [!success]- Answer
>> a) → n)
>> b) → q)
>> c) → o)
>> d) → p)

> [!question] Match the IP pseudo-header field with its content.
>> [!example] Group A
>> a) Source IP address
>> b) Destination IP address
>> c) Protocol
>> d) UDP/TCP Length
>
>> [!example] Group B
>> n) 17 for UDP, 6 for TCP
>> o) 4 bytes
>> p) Total UDP/TCP length (header + payload)
>> q) 4 bytes
>
>> [!success]- Answer
>> a) → o)
>> b) → q)
>> c) → n)
>> d) → p)

> [!question] Match the term with its layer.
>> [!example] Group A
>> a) Port number
>> b) IP address
>> c) MAC address
>> d) Frame
>
>> [!example] Group B
>> n) Layer 2 (Data Link)
>> o) Layer 2 (Data Link) — physical identity
>> p) Layer 3 (Network) — logical identity
>> q) Layer 4 (Transport) — process identity
>
>> [!success]- Answer
>> a) → q)
>> b) → p)
>> c) → o)
>> d) → n)

---

##  Score Interpretation

- **0–25 (≤ 50%):** Re-read Chapter 10 carefully, especially the TCP handshake and flags.
- **26–40 (50–75%):** Decent. Review missed topics.
- **41–50 (75–95%):** Strong.
- **51+ (> 95%):** Excellent. You've mastered the transport layer.
