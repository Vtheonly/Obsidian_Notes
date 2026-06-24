---
sources:
  - "[[05.00 Introduction]]"
  - "[[05.01 Route Entries & Administrative Distance]]"
  - "[[05.02 Static Routing Mechanics]]"
  - "[[05.03 Distance-Vector Routing (RIPv2)]]"
  - "[[05.04 RIP Route Table Update Logic]]"
  - "[[05.05 Link-State Routing (OSPF & Dijkstra's Algorithm)]]"
---

> [!question] Routers use Administrative Distance to compare paths to the same destination learned from the same routing protocol.
>> [!success]- Answer
>> False

> [!question] Directly connected interfaces must have an IP address configured and be in an up/up state to have an Administrative Distance of 0.
>> [!success]- Answer
>> True

> [!question] Directly attached static routes require recursive lookup of the next-hop IP address.
>> [!success]- Answer
>> False

> [!question] RIPv2 broadcasts routing updates to 255.255.255.255.
>> [!success]- Answer
>> False

> [!question] Disabling automatic summarization under OSPF configuration is required to support VLSM.
>> [!success]- Answer
>> False

> [!question] The metric of a RIP route is incremented before it is evaluated against the router's current routing table.
>> [!success]- Answer
>> True

> [!question] If a RIP router receives a worse metric update for an existing route from a different neighbor, it overwrites the route.
>> [!success]- Answer
>> False

> [!question] Dijkstra's algorithm constructs a Shortest Path Tree (SPT) with the calculating node as the root.
>> [!success]- Answer
>> True

> [!question] In the Node F Dijkstra walkthrough, the shortest path to Node D is directly from F (F -> D) with cost 4.
>> [!success]- Answer
>> False

> [!question] A static route next-hop configured with an exit interface is referred to as a directly attached route.
>> [!success]- Answer
>> True

> [!question] Which routing source has the highest trustworthiness (lowest AD)?
> a) OSPF
> b) Directly Connected
> c) Static Route
> d) RIP
>> [!success]- Answer
>> b) Directly Connected

> [!question] What is the default Administrative Distance value for a static route?
> a) 1
> b) 110
> c) 120
> d) 0
>> [!success]- Answer
>> a) 1

> [!question] What is the destination IP address in the default route configuration ip route 0.0.0.0 0.0.0.0 10.10.10.2?
> a) 0.0.0.0
> b) 255.255.0.0
> c) 10.10.10.2
> d) 255.255.255.255
>> [!success]- Answer
>> a) 0.0.0.0

> [!question] How often does a RIP router send periodic routing updates?
> a) Every 10 seconds
> b) Every 60 seconds
> c) Only when a link state changes
> d) Every 30 seconds
>> [!success]- Answer
>> d) Every 30 seconds

> [!question] Which command is used to enable version 2 of RIP?
> a) ip rip version 2
> b) version 2
> c) rip version 2
> d) router rip version 2
>> [!success]- Answer
>> b) version 2

> [!question] What is the first thing a RIP router does to incoming route entries when it receives an update?
> a) Discards the route
> b) Compares the metrics
> c) Overwrites the next hop
> d) Increments the metric by 1
>> [!success]- Answer
>> d) Increments the metric by 1

> [!question] In the Node F Dijkstra walkthrough, what is the cost of the shortest path to Node B?
> a) 3
> b) 2
> c) 1
> d) 4
>> [!success]- Answer
>> a) 3

> [!question] If a router has two matches in its routing table for a packet's destination IP (172.16.130.1), namely 172.16.128.0/17 and 172.16.0.0/16, which one does it select?
> a) 172.16.128.0/17 (longest prefix)
> b) It load balances between both
> c) 172.16.0.0/16 (shortest prefix)
> d) It discards the packet
>> [!success]- Answer
>> a) 172.16.128.0/17 (longest prefix)

> [!question] In RIPv2 configuration, what does associating a network using network 10.0.0.0 do?
> a) Allows RIP to run on and advertise interfaces matching classful network 10.0.0.0
> b) Enables OSPF database synchronization for network 10.0.0.0
> c) Statically maps 10.0.0.0/8 to exit interfaces
> d) Configures a loopback interface on classful block 10.0.0.0
>> [!success]- Answer
>> a) Allows RIP to run on and advertise interfaces matching classful network 10.0.0.0

> [!question] What list is used in Dijkstra's algorithm to store unconfirmed paths under evaluation?
> a) Permanent list (P)
> b) Shortest path tree
> c) Tentative list (T)
> d) Path list
>> [!success]- Answer
>> c) Tentative list (T)

> [!question] Match the default Administrative Distance with its route source.
>> [!example] Group A
>> a) Directly Connected
>> b) Static Route
>> c) OSPF
>
>> [!example] Group B
>> n) 110
>> o) 0
>> p) 1
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the routing lookup term with its description.
>> [!example] Group A
>> a) Prefix Length
>> b) Next Hop
>> c) Administrative Distance
>
>> [!example] Group B
>> n) IP address of the next router to send packets to
>> o) Value representing trustworthiness of a source
>> p) The number of bits in the subnet mask
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the static route type with its configuration description.
>> [!example] Group A
>> a) Directly Attached Route
>> b) Next-hop Route
>> c) Default Route
>
>> [!example] Group B
>> n) Uses next-hop router interface IP address
>> o) Matches all destination networks
>> p) Uses local exit interface of routing device
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the RIP operational characteristic with its parameter or value.
>> [!example] Group A
>> a) Multicast address
>> b) Metric
>> c) Update interval
>
>> [!example] Group B
>> n) Hop count
>> o) 30 seconds
>> p) 224.0.0.9
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the RIP route update logic rule with its description.
>> [!example] Group A
>> a) Better Metric
>> b) Worse Metric (Different Neighbor)
>> c) Same Next Hop
>
>> [!example] Group B
>> n) Always overwrite existing route with the new metric
>> o) Replace the route with the lower metric
>> p) Discard the update
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Dijkstra algorithm walkthrough step from Node F with its permanent list (P) state.
>> [!example] Group A
>> a) Step 1
>> b) Step 2
>> c) Step 3
>
>> [!example] Group B
>> n) P = {[F, 0, -], [C, 1, C], [E, 2, E]}
>> o) P = {[F, 0, -], [C, 1, C]}
>> p) P = {[F, 0, -]}
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the Dijkstra node path from F to its path cost.
>> [!example] Group A
>> a) Path to Node D
>> b) Path to Node B
>> c) Path to Node A
>
>> [!example] Group B
>> n) Cost 4
>> o) Cost 3
>> p) Cost 3
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the routing concept with its fundamental definition.
>> [!example] Group A
>> a) Distance-Vector
>> b) Link-State
>> c) Routing Table
>
>> [!example] Group B
>> n) Database containing routes used for forwarding decisions
>> o) Algorithm sharing full topology map to compute shortest paths
>> p) Protocol passing copies of routing tables to neighbors
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the RIP route update metric changes.
>> [!example] Group A
>> a) Metric 15 after step 1
>> b) Metric 14 after step 1
>> c) Metric 13 after step 1
>
>> [!example] Group B
>> n) Metric 15
>> o) Metric 16 (unreachable)
>> p) Metric 14
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Cisco IOS RIP config command with its syntax format.
>> [!example] Group A
>> a) Enabling the routing process
>> b) Specifying RIP version
>> c) Associating classful network
>
>> [!example] Group B
>> n) version 2
>> o) network 192.168.1.0
>> p) router rip
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
