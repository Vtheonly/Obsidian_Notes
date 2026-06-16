---
sources:
  - "[[07.00 Introduction]]"
  - "[[07.01 IP Router Operations & Packet Processing]]"
  - "[[07.02 Longest Prefix Match (LPM) Algorithmic Routing]]"
  - "[[07.03 Static vs. Dynamic Routing Paradigms]]"
  - "[[07.04 Distance Vector Protocols & RIPv2]]"
  - "[[07.05 Link-State Routing & OSPF]]"
  - "[[07.06 Path Vector Routing & BGP]]"
---

> [!question] RIPv2 does not support Variable Length Subnet Masking (VLSM).
>> [!success]- Answer
>> False

> [!question] By default, OSPF assigns a cost of 1 to both Fast Ethernet and Gigabit Ethernet interfaces.
>> [!success]- Answer
>> True

> [!question] Static routing adapts automatically to link failures.
>> [!success]- Answer
>> False

> [!question] Split Horizon prevents routing loops by not advertising a route back out the interface it was learned from.
>> [!success]- Answer
>> True

> [!question] Poison Reverse immediately advertises a failed route with a hop count of 16.
>> [!success]- Answer
>> True

> [!question] RIPv1 broadcasts updates to 255.255.255.255, while RIPv2 multicasts updates to 224.0.0.9.
>> [!success]- Answer
>> True

> [!question] Fragmentation is performed by the router when DF=0 and the packet exceeds the MTU of the egress link.
>> [!success]- Answer
>> True

> [!question] BGP Update messages negotiate session parameters when a peer connection is initialized.
>> [!success]- Answer
>> False

> [!question] Hold-down timers lock a RIP route for 60 seconds and ignore worse metric updates.
>> [!success]- Answer
>> True

> [!question] The command to resolve the OSPF gigabit bottleneck is 'auto-cost reference-bandwidth 10000'.
>> [!success]- Answer
>> True

> [!question] What is BGP classified as?
> a) Path-Vector Routing Protocol
> b) Static Routing Protocol
> c) Distance-Vector Routing Protocol
> d) Link-State Routing Protocol
>> [!success]- Answer
>> a) Path-Vector Routing Protocol

> [!question] What does the router do if a packet exceeds the outbound MTU and the DF flag is set to 1?
> a) Fragments the packet anyway
> b) Buffers the packet
> c) Drops the packet and sends ICMP Type 3 Code 4
> d) Ignores the MTU limit
>> [!success]- Answer
>> c) Drops the packet and sends ICMP Type 3 Code 4

> [!question] What ICMP message is returned if a router cannot find a matching route or default route?
> a) ICMP Type 3 Code 0 (Network Unreachable)
> b) ICMP Type 8 (Echo Request)
> c) ICMP Type 11 (Time Exceeded)
> d) ICMP Type 3 Code 4 (Frag Needed)
>> [!success]- Answer
>> a) ICMP Type 3 Code 0 (Network Unreachable)

> [!question] What is the default Administrative Distance of a static route?
> a) 1
> b) 110
> c) 0
> d) 120
>> [!success]- Answer
>> a) 1

> [!question] Which command resolves the OSPF Gigabit bottleneck issue?
> a) auto-cost reference-bandwidth 10000
> b) ospf reference-bandwidth 1000
> c) ip ospf cost 1
> d) reference-bandwidth gigabit
>> [!success]- Answer
>> a) auto-cost reference-bandwidth 10000

> [!question] What role is assigned to an OSPF router that redistributes routes from external networks?
> a) Autonomous System Boundary Router (ASBR)
> b) Backbone Router (BR)
> c) Internal Router (IR)
> d) Area Boundary Router (ABR)
>> [!success]- Answer
>> a) Autonomous System Boundary Router (ASBR)

> [!question] How does BGP prevent routing loops across Autonomous Systems?
> a) Checking if its own ASN is in the AS_PATH attribute
> b) Hop Count limits
> c) Split Horizon
> d) Poison Reverse
>> [!success]- Answer
>> a) Checking if its own ASN is in the AS_PATH attribute

> [!question] What is the default OSPF cost assigned to a Gigabit Ethernet interface under the default reference bandwidth?
> a) 0
> b) 100
> c) 1
> d) 10
>> [!success]- Answer
>> c) 1

> [!question] What action does a router take if the incoming L2 frame fails the CRC/FCS check?
> a) Extracts the IP packet
> b) Floods the frame
> c) Requests retransmission
> d) Discards the frame immediately
>> [!success]- Answer
>> d) Discards the frame immediately

> [!question] Which BGP message type is sent to verify that a neighbor remains active when no updates are being sent?
> a) Update
> b) Open
> c) Keepalive
> d) Notification
>> [!success]- Answer
>> c) Keepalive

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TTL
>> b) OSPF Area 0
>> c) ICMP Type 3 Code 4
>
>> [!example] Group B
>> n) Time to Live field decremented by routers to prevent loops.
>> o) Message sent when packet exceeds MTU and DF flag is 1.
>> p) Backbone area to which all regular areas must connect.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Dijkstra Algorithm
>> b) Hello Packet
>> c) OSPF Cost
>
>> [!example] Group B
>> n) SPF calculation algorithm run locally by OSPF routers.
>> o) Metric calculated as Reference Bandwidth / Bandwidth.
>> p) Multicast packet used by OSPF for neighbor discovery.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) AD of 120
>> b) CRC / FCS
>> c) BGP Update
>
>> [!example] Group B
>> n) Message type advertising new routes or withdrawing inactive ones.
>> o) Administrative Distance of RIP protocol.
>> p) Trailer check used to detect incoming frame corruption.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Gigabit Bottleneck
>> b) ICMP Type 3 Code 0
>> c) OSPF Area 0
>
>> [!example] Group B
>> n) Backbone area to which all regular areas must connect.
>> o) Message sent when destination network is unreachable.
>> p) Fast Ethernet and Gigabit interfaces having same cost of 1.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) ICMP Type 3 Code 4
>> b) BGP Update
>> c) Dijkstra Algorithm
>
>> [!example] Group B
>> n) SPF calculation algorithm run locally by OSPF routers.
>> o) Message type advertising new routes or withdrawing inactive ones.
>> p) Message sent when packet exceeds MTU and DF flag is 1.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) DF Flag
>> b) auto-cost reference-bandwidth 10000
>> c) LSA
>
>> [!example] Group B
>> n) Don't Fragment flag that blocks packet splitting.
>> o) Cisco command to set reference bandwidth to 10 Gbps.
>> p) Link-State Advertisement containing interface state and cost.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Administrative Distance
>> b) DF Flag
>> c) ABR
>
>> [!example] Group B
>> n) Don't Fragment flag that blocks packet splitting.
>> o) Area Boundary Router connecting regular areas to Area 0.
>> p) Trustworthiness rating of a routing source (0-255).
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Bellman-Ford
>> b) Autonomous System
>> c) Reference Bandwidth
>
>> [!example] Group B
>> n) Default 100 Mbps value used for OSPF metric calculation.
>> o) Network under single admin with unified routing policy.
>> p) Algorithmic foundation of distance-vector routing.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) AD of 0
>> b) BGP Update
>> c) LSDB
>
>> [!example] Group B
>> n) Administrative Distance of directly connected interfaces.
>> o) Link-State Database containing the complete topological map.
>> p) Message type advertising new routes or withdrawing inactive ones.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) AD of 110
>> b) ASBR
>> c) ABR
>
>> [!example] Group B
>> n) Area Boundary Router connecting regular areas to Area 0.
>> o) Administrative Distance of OSPF protocol.
>> p) Autonomous System Boundary Router importing external routes.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
