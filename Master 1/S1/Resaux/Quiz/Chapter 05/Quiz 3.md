---
sources:
  - "[[05.00 Introduction]]"
  - "[[05.01 Route Entries & Administrative Distance]]"
  - "[[05.02 Static Routing Mechanics]]"
  - "[[05.03 Distance-Vector Routing (RIPv2)]]"
  - "[[05.04 RIP Route Table Update Logic]]"
  - "[[05.05 Link-State Routing (OSPF & Dijkstra's Algorithm)]]"
---

> [!question] When a router receives multiple paths to the same destination from different sources, it will install the path with the highest Administrative Distance.
>> [!success]- Answer
>> False

> [!question] Next-hop static routes require the router to resolve the next-hop IP address to an exit interface.
>> [!success]- Answer
>> True

> [!question] The destination subnet mask for a host route is 255.255.255.255 (/32).
>> [!success]- Answer
>> True

> [!question] OSPF routers exchange their entire routing tables with their neighbors every 30 seconds.
>> [!success]- Answer
>> False

> [!question] RIPv2 supports classless routing updates by including subnet mask information in its updates.
>> [!success]- Answer
>> True

> [!question] A RIP metric value of 16 indicates that the route is unreachable.
>> [!success]- Answer
>> True

> [!question] If a RIP update is received from the same neighbor that advertised it, the router replaces the route only if the metric is better.
>> [!success]- Answer
>> False

> [!question] Dijkstra's algorithm uses a candidate list named Tentative (T) for confirmed shortest paths.
>> [!success]- Answer
>> False

> [!question] The default Administrative Distance for a directly connected interface is 0.
>> [!success]- Answer
>> True

> [!question] Disabling automatic summarization is optional for classful routing protocols like RIPv1.
>> [!success]- Answer
>> False

> [!question] Which routing protocol has a default Administrative Distance of 120?
> a) Static Route
> b) Directly Connected
> c) RIP
> d) OSPF
>> [!success]- Answer
>> c) RIP

> [!question] What is the primary purpose of the passive-interface command?
> a) To ignore all incoming routing updates on an interface
> b) To prevent sending routing updates out of an interface
> c) To disable an interface from forwarding data traffic
> d) To set the interface's administrative distance to 255
>> [!success]- Answer
>> b) To prevent sending routing updates out of an interface

> [!question] Which of the following is a key difference between RIPv2 and OSPF?
> a) RIPv2 builds a complete topological database (LSDB)
> b) OSPF uses Dijkstra's algorithm while RIPv2 uses distance-vector updates
> c) OSPF has a default Administrative Distance of 120
> d) RIPv2 is classless while OSPF is classful
>> [!success]- Answer
>> b) OSPF uses Dijkstra's algorithm while RIPv2 uses distance-vector updates

> [!question] What command on Cisco IOS configures a directly attached static route to 192.168.2.0/24 via Serial 0/0/0?
> a) ip route 192.168.2.0 255.255.255.0 serial 0/0/0
> b) ip default-route 192.168.2.0 serial 0/0/0
> c) route static 192.168.2.0 255.255.255.0 serial 0/0/0
> d) ip route 192.168.2.0 255.255.255.0 10.10.10.2
>> [!success]- Answer
>> a) ip route 192.168.2.0 255.255.255.0 serial 0/0/0

> [!question] What is the first step when a RIP router processes a routing update from a neighbor?
> a) Increment the metric of all incoming route entries by 1
> b) Broadcast the update to all other neighbors
> c) Compare each entry to the current routing table
> d) Overwrite the entire routing table
>> [!success]- Answer
>> a) Increment the metric of all incoming route entries by 1

> [!question] In the Dijkstra walkthrough from Node F, which node has the lowest path cost from F?
> a) Node D
> b) Node C
> c) Node B
> d) Node E
>> [!success]- Answer
>> b) Node C

> [!question] What is the default Administrative Distance of a static route?
> a) 1
> b) 0
> c) 120
> d) 110
>> [!success]- Answer
>> a) 1

> [!question] If a router is using longest prefix matching, which route will it select to forward a packet destined to 172.16.128.5?
> a) 0.0.0.0/0
> b) 172.0.0.0/8
> c) 172.16.128.0/17
> d) 172.16.0.0/16
>> [!success]- Answer
>> c) 172.16.128.0/17

> [!question] In RIPv2 configuration, what does the command version 2 enforce?
> a) Upgrading OSPF compatibility
> b) Enforcing classful auto-summarization
> c) Enabling link-state database exchanges
> d) Classless routing and support for VLSM
>> [!success]- Answer
>> d) Classless routing and support for VLSM

> [!question] In Dijkstra's algorithm, when a node is moved from the Tentative list to the Permanent list, it means:
> a) Its shortest path has been confirmed
> b) Its cost is under evaluation
> c) Its neighbor list is empty
> d) The path is blocked
>> [!success]- Answer
>> a) Its shortest path has been confirmed

> [!question] Match the routing table symbol with its protocol representation.
>> [!example] Group A
>> a) S
>> b) O
>> c) R
>
>> [!example] Group B
>> n) RIP
>> o) Static Route
>> p) OSPF
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the IP prefix with its route type.
>> [!example] Group A
>> a) 0.0.0.0/0
>> b) 192.168.1.1/32
>> c) 10.0.0.0/8
>
>> [!example] Group B
>> n) Network Route
>> o) Default Route
>> p) Host Route
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the RIP route table update logic event with its description.
>> [!example] Group A
>> a) New Route
>> b) Better Metric
>> c) Worse Metric (Different Neighbor)
>
>> [!example] Group B
>> n) Discard the update
>> o) Install the route in the routing table
>> p) Replace the existing route
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the routing protocol with its characteristic metric.
>> [!example] Group A
>> a) RIPv2
>> b) OSPF
>> c) Static Route
>
>> [!example] Group B
>> n) Link Cost
>> o) Hop Count
>> p) No dynamic metric (value of 0 in [1/0])
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Dijkstra algorithm step from Node F with the tentative list state.
>> [!example] Group A
>> a) Initial state
>> b) After Step 2 (C permanent)
>> c) After Step 3 (E permanent)
>
>> [!example] Group B
>> n) T = {[D, 3, C], [B, 3, E]}
>> o) T = {[C, 1, C], [E, 2, E], [D, 4, D]}
>> p) T = {[E, 2, E], [D, 3, C]}
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Cisco configuration syntax with its command purpose.
>> [!example] Group A
>> a) ip route [net] [mask] [next_hop]
>> b) passive-interface [int]
>> c) no auto-summary
>
>> [!example] Group B
>> n) Disables classful automatic summarization
>> o) Suppresses outgoing routing updates
>> p) Configures next-hop static route
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the routing reliability term with its default metric/distance value.
>> [!example] Group A
>> a) Directly connected AD
>> b) OSPF AD
>> c) RIP AD
>
>> [!example] Group B
>> n) 120
>> o) 0
>> p) 110
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the route entry component with its meaning.
>> [!example] Group A
>> a) [1 / 0]
>> b) DP
>> c) NH
>
>> [!example] Group B
>> n) Destination Prefix
>> o) Next Hop
>> p) [Administrative Distance / Metric]
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Dijkstra algorithm Node F walkthrough shortest path to each node.
>> [!example] Group A
>> a) Node D
>> b) Node B
>> c) Node A
>
>> [!example] Group B
>> n) F -> E -> B -> A
>> o) F -> C -> D
>> p) F -> E -> B
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the RIP route update metric calculation from neighbor 145.108.1.9.
>> [!example] Group A
>> a) Incoming 199.245.180.0/24 (metric 3)
>> b) Incoming 34.0.0.0/8 (metric 2)
>> c) Incoming 141.12.0.0/16 (metric 4)
>
>> [!example] Group B
>> n) Becomes metric 5
>> o) Becomes metric 4
>> p) Becomes metric 3
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
