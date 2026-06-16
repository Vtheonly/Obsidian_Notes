---
sources:
  - "[[08.00 Introduction]]"
  - "[[08.01 Transport Layer Role & Service Delivery Models]]"
  - "[[08.02 Logical Ports & Socket Programming Architecture]]"
  - "[[08.03 User Datagram Protocol (UDP) Architecture]]"
---

> [!question] Separate connection sockets allow a server to communicate with active clients while continuing to listen for new connections.
>> [!success]- Answer
>> True

> [!question] Trivial File Transfer Protocol (TFTP) uses UDP port 69.
>> [!success]- Answer
>> True

> [!question] Port numbers are 16-bit unsigned integers, providing a range from 0 to 65535.
>> [!success]- Answer
>> True

> [!question] UDP is better suited for real-time applications like VoIP than TCP.
>> [!success]- Answer
>> True

> [!question] Domain Name System (DNS) queries typically run over UDP port 53.
>> [!success]- Answer
>> True

> [!question] The TCP three-way handshake sequence is SYN -> ACK -> SYN-ACK.
>> [!success]- Answer
>> False

> [!question] The minimum value of the UDP header Length field is 8 bytes.
>> [!success]- Answer
>> True

> [!question] Simple Network Management Protocol (SNMP) uses UDP port 161.
>> [!success]- Answer
>> True

> [!question] A connection key 5-tuple includes: Protocol, Source IP, Source Port, Destination IP, and Destination Port.
>> [!success]- Answer
>> True

> [!question] Well-known port numbers are assigned by IANA.
>> [!success]- Answer
>> True

> [!question] What port does SNMP use to listen for management requests?
> a) TCP port 110
> b) UDP port 162
> c) UDP port 161
> d) TCP port 25
>> [!success]- Answer
>> c) UDP port 161

> [!question] What port is mapped to unencrypted HTTP traffic?
> a) TCP port 23
> b) TCP port 80
> c) TCP port 443
> d) TCP port 21
>> [!success]- Answer
>> b) TCP port 80

> [!question] What layer of the OSI model sits directly above the network layer and resolves its best-effort deficiencies?
> a) Session Layer
> b) Application Layer
> c) Data Link Layer
> d) Transport Layer
>> [!success]- Answer
>> d) Transport Layer

> [!question] Which protocol is faster due to lack of connection establishment and flow control overhead?
> a) BGP
> b) TCP
> c) UDP
> d) SMTP
>> [!success]- Answer
>> c) UDP

> [!question] What port is mapped to HTTPS?
> a) TCP port 443
> b) TCP port 21
> c) TCP port 80
> d) TCP port 22
>> [!success]- Answer
>> a) TCP port 443

> [!question] Which port range represents the Well-Known Ports?
> a) 49152 to 65535
> b) 0 to 1023
> c) 1024 to 49151
> d) 0 to 255
>> [!success]- Answer
>> b) 0 to 1023

> [!question] Which application protocol is mapped to UDP port 69?
> a) TFTP
> b) SNMP
> c) DNS
> d) FTP
>> [!success]- Answer
>> a) TFTP

> [!question] What is the port range for Registered Ports?
> a) 1024 to 49151
> b) 0 to 1023
> c) 1000 to 2000
> d) 49152 to 65535
>> [!success]- Answer
>> a) 1024 to 49151

> [!question] Which port does a DHCP server listen on?
> a) UDP port 68
> b) UDP port 69
> c) UDP port 67
> d) TCP port 80
>> [!success]- Answer
>> c) UDP port 67

> [!question] What is process multiplexing?
> a) Splitting packets across multiple routes
> b) Directing concurrent traffic to correct applications using ports
> c) Load balancing traffic at switch level
> d) Translating local private IPs to public IPs
>> [!success]- Answer
>> b) Directing concurrent traffic to correct applications using ports

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TCP Header Size
>> b) accept()
>> c) Ordered Delivery
>
>> [!example] Group B
>> n) System call blocking until a client connection arrives.
>> o) TCP feature using sequence numbers to reassemble data.
>> p) Minimum size of 20 bytes.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) DNS Queries
>> b) bind()
>> c) Transport Layer
>
>> [!example] Group B
>> n) Provides logical communication between application processes.
>> o) System call assigning socket to local IP and port.
>> p) Domain Name System queries over UDP port 53.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Flow Control
>> b) UDP Header Size
>> c) DHCP Client
>
>> [!example] Group B
>> n) Prevents a fast sender from overwhelming a slow receiver.
>> o) Bootstrap protocol client listening on UDP port 68.
>> p) Fixed size of 8 bytes.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TFTP
>> b) Flow Control
>> c) listen()
>
>> [!example] Group B
>> n) Trivial File Transfer Protocol on UDP port 69.
>> o) Prevents a fast sender from overwhelming a slow receiver.
>> p) System call shifting socket state to passive listening.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) HTTPS
>> b) FTP Control
>> c) Process Multiplexing
>
>> [!example] Group B
>> n) Encrypted Web protocol on TCP port 443.
>> o) Directing network traffic to correct application using ports.
>> p) File Transfer Protocol connection on TCP port 21.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Transport Layer
>> b) SSH
>> c) UDP Length Field
>
>> [!example] Group B
>> n) Provides logical communication between application processes.
>> o) 16-bit field specifying total datagram size (min 8).
>> p) Secure Shell remote admin on TCP port 22.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 5-Tuple
>> b) TCP Port 179
>> c) UDP Length Field
>
>> [!example] Group B
>> n) 16-bit field specifying total datagram size (min 8).
>> o) Protocol, Src IP, Src Port, Dst IP, Dst Port connection key.
>> p) BGP peer session transport port.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 5-Tuple
>> b) POP3
>> c) FTP Control
>
>> [!example] Group B
>> n) Protocol, Src IP, Src Port, Dst IP, Dst Port connection key.
>> o) File Transfer Protocol connection on TCP port 21.
>> p) Post Office Protocol Version 3 on TCP port 110.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Segment
>> b) Listening Socket
>> c) bind()
>
>> [!example] Group B
>> n) System call assigning socket to local IP and port.
>> o) Transport Layer data unit when using TCP.
>> p) Persistent server socket waiting for client connections.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Root Privilege
>> b) TCP Header Size
>> c) Dynamic / Ephemeral Ports
>
>> [!example] Group B
>> n) Temporary client source ports (49152 to 65535).
>> o) Minimum size of 20 bytes.
>> p) Required on Unix systems to bind to ports below 1024.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
