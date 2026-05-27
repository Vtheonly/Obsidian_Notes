---
sources:
  - "[[Final/Chapter 4]]"
---
> [!question] Service Discovery solves the problem of microservices needing dynamic peer-to-peer communication with changing IP addresses.
>> [!success]- Answer
>> True

> [!question] In client-side discovery, the client sends requests through a load balancer that queries the registry.
>> [!success]- Answer
>> False

> [!question] The Control Plane in Consul manages cluster state, service registrations, and health status.
>> [!success]- Answer
>> True

> [!question] The Data Plane in Consul manages physical network traffic via sidecar proxies like Envoy.
>> [!success]- Answer
>> True

> [!question] A Consul Server node uses the Gossip protocol for consensus and leader election.
>> [!success]- Answer
>> False

> [!question] Standard Service Discovery in lab environments requires the Data Plane proxies for communication.
>> [!success]- Answer
>> False

> [!question] Consul Servers maintain the authoritative global state of the system including the Service Registry.
>> [!success]- Answer
>> True

> [!question] A Consul cluster requires an even number of servers to maintain a quorum.
>> [!success]- Answer
>> False

> [!question] Consul Clients are lightweight daemons that run on every host hosting microservices.
>> [!success]- Answer
>> True

> [!question] The Gossip protocol is used by all nodes in a Consul cluster for membership management.
>> [!success]- Answer
>> True

> [!question] What is the main problem that Service Discovery solves in microservices?
> a) Database replication
> b) Static IP configuration becoming impossible with dynamic scaling
> c) Code compilation errors
> d) UI rendering issues
>> [!success]- Answer
>> b) Static IP configuration becoming impossible with dynamic scaling

> [!question] Which protocol does Consul use for consensus and leader election?
> a) Gossip
> b) Raft
> c) HTTP
> d) DNS
>> [!success]- Answer
>> b) Raft

> [!question] How many Consul Servers are typically recommended for fault tolerance?
> a) 1 or 2
> b) 3 or 5
> c) 10 or more
> d) Any even number
>> [!success]- Answer
>> b) 3 or 5

> [!question] What port does Consul use for the HTTP API and Web UI?
> a) 8300
> b) 8301
> c) 8500
> d) 8600
>> [!success]- Answer
>> c) 8500

> [!question] What is the purpose of the Gossip protocol in a Consul cluster?
> a) Database replication
> b) Leader election and consensus
> c) Decentralized membership and failure detection
> d) HTTP request routing
>> [!success]- Answer
>> c) Decentralized membership and failure detection

> [!question] What does blocking UDP ports cause in a Consul cluster?
> a) Faster performance
> b) UDP probes failed or unreachable network errors
> c) Automatic port reassignment
> d) Enhanced security
>> [!success]- Answer
>> b) UDP probes failed or unreachable network errors

> [!question] Which port does Consul use for DNS service discovery?
> a) 8300
> b) 8500
> c) 8600
> d) 8302
>> [!success]- Answer
>> c) 8600

> [!question] What is the role of a Consul Client agent?
> a) To participate in Raft consensus
> b) To act as a local bridge between microservices and Consul Servers
> c) To replace the API Gateway
> d) To manage database schemas
>> [!success]- Answer
>> b) To act as a local bridge between microservices and Consul Servers

> [!question] Which port is used for server-to-server RPC traffic in Consul?
> a) 8300
> b) 8500
> c) 8600
> d) 8301
>> [!success]- Answer
>> a) 8300

> [!question] What happens if port 8300 conflicts on a Consul server?
> a) The server runs in degraded mode
> b) Failed to start RPC layer or socket address errors occur
> c) The server switches to HTTP automatically
> d) The server ignores the conflict
>> [!success]- Answer
>> b) Failed to start RPC layer or socket address errors occur

> [!question] Match the service discovery approach with its description.
>> [!example] Group A
>> a) Client-side Discovery
>> b) Server-side Discovery
>
>> [!example] Group B
>> n) Client queries registry to select an instance
>> o) Client sends requests through a load balancer
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)

> [!question] Match the Consul plane with its responsibility.
>> [!example] Group A
>> a) Control Plane
>> b) Data Plane
>
>> [!example] Group B
>> n) Manages network traffic via sidecar proxies
>> o) Manages cluster state and service registrations
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the Consul node type with its role.
>> [!example] Group A
>> a) Consul Server
>> b) Consul Client
>
>> [!example] Group B
>> n) Lightweight daemon running on every host
>> o) Maintains authoritative global state
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the Consul protocol with its purpose.
>> [!example] Group A
>> a) Raft Protocol
>> b) Gossip Protocol
>
>> [!example] Group B
>> n) Decentralized membership and failure detection
>> o) Leader election and consensus
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the Consul port with its service.
>> [!example] Group A
>> a) 8300
>> b) 8500
>> c) 8600
>
>> [!example] Group B
>> n) HTTP API and Web UI
>> o) DNS Service Discovery
>> p) Server RPC traffic
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Gossip type with its scope.
>> [!example] Group A
>> a) LAN Gossip
>> b) WAN Gossip
>
>> [!example] Group B
>> n) Between datacenters on ports 8302
>> o) Within a datacenter on ports 8301
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the Raft node role with its state.
>> [!example] Group A
>> a) Leader
>> b) Follower
>
>> [!example] Group B
>> n) Replicates data from the leader
>> o) Maintains authoritative global state
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the Consul Client task with its description.
>> [!example] Group A
>> a) Local health checks
>> b) Service registration forwarding
>> c) Gossip membership updates
>
>> [!example] Group B
>> n) Sends registration requests to server cluster
>> o) Monitors application instance health
>> p) Communicates membership changes
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the port range with its TCP/UDP designation.
>> [!example] Group A
>> a) 8301 TCP
>> b) 8301 UDP
>> c) 8302 UDP
>
>> [!example] Group B
>> n) LAN Gossip heartbeat
>> o) LAN Gossip communication
>> p) WAN Gossip
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the architectural diagram role with the Consul component.
>> [!example] Group A
>> a) The Brain
>> b) The Agent
>> c) The Proxy
>
>> [!example] Group B
>> n) Envoy sidecar in Data Plane
>> o) Consul Server maintaining state
>> p) Consul Client on every host
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)