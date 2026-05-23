---
sources:
  - "[[11.1. Dynamic Service Discovery Patterns]]"
  - "[[11.2. HashiCorp Consul Architecture Overview]]"
  - "[[11.3. Consensus Protocol Raft and Server Quorums]]"
  - "[[11.4. Gossip Protocol Serf and Local WAN Network Topology]]"
  - "[[11.5. Consul Network Ports and Routing Configuration]]"
  - "[[11.6. Bootstrapping a Multi-Node Consul Cluster]]"
  - "[[11.7. Managing Peer Consensus and Client Nodes]]"
  - "[[11.8. Consul Agent Command Line Tools]]"
  - "[[11.9. Consul Service Registration JSON Schemas]]"
  - "[[11.10. Django Application Health Check Endpoints]]"
  - "[[11.11. Programmatic Consul Integration using Python-Consul]]"
---
> [!question] Service discovery eliminates the need for hardcoded IP addresses in microservice configurations.
>> [!success]- Answer
>> True

> [!question] A Consul server cluster requires an odd number of server nodes to maintain effective quorum.
>> [!success]- Answer
>> True

> [!question] The Raft protocol's Leader Election phase guarantees that committed entries are preserved even if some nodes fail.
>> [!success]- Answer
>> False

> [!question] The Serf protocol is used by Consul for cluster membership and failure detection.
>> [!success]- Answer
>> True

> [!question] Consul client nodes participate in the Raft consensus protocol.
>> [!success]- Answer
>> False

> [!question] The `consul kv get` command retrieves a value from Consul's key-value store.
>> [!success]- Answer
>> True

> [!question] DNS-based service discovery uses the `dig` command to query Consul for service addresses.
>> [!success]- Answer
>> True

> [!question] The `check` field in a Consul service registration defines health check configurations.
>> [!success]- Answer
>> True

> [!question] Python-Consul's `agent.service.register()` method registers a service with the local Consul agent.
>> [!success]- Answer
>> True

> [!question] When bootstrapping a Consul cluster, the `bootstrap_expect` flag specifies the expected number of server nodes.
>> [!success]- Answer
>> True

> [!question] What happens when a Raft leader node fails?
> a) The cluster stops operating
> b) A new leader is elected from the remaining server nodes
> c) A client node takes over as leader
> d) The cluster waits for the leader to recover
>> [!success]- Answer
>> b) A new leader is elected from the remaining server nodes

> [!question] Which Consul port is used for DNS-based service discovery?
> a) 8300
> b) 8400
> c) 8500
> d) 8600
>> [!success]- Answer
>> d) 8600

> [!question] What is the recommended number of server nodes for a production Consul cluster?
> a) 1 or 2
> b) 3 or 5
> c) 7 or 9
> d) Any even number
>> [!success]- Answer
>> b) 3 or 5

> [!question] What does the `interval` parameter in a Consul health check specify?
> a) How often the health check runs
> b) The timeout for the health check
> c) The deregistration delay
> d) The TTL duration
>> [!success]- Answer
>> a) How often the health check runs

> [!question] What does the `consul leave` command do?
> a) Removes a node from the cluster gracefully
> b) Stops the Consul agent
> c) Deletes a service registration
> d) Leaves a key-value pair
>> [!success]- Answer
>> a) Removes a node from the cluster gracefully

> [!question] How does Consul achieve high availability?
> a) By storing data on each client node
> b) By replicating data across server nodes using Raft
> c) By using a single master database
> d) By caching data in memory
>> [!success]- Answer
>> b) By replicating data across server nodes using Raft

> [!question] What is the purpose of the `deregister_critical_service_after` setting in a health check?
> a) It immediately removes the service when the check fails
> b) It automatically deregisters the service after a specified timeout in a critical state
> c) It prevents deregistration of services
> d) It delays the first health check
>> [!success]- Answer
>> b) It automatically deregisters the service after a specified timeout in a critical state

> [!question] Which Consul agent command-line option specifies the data center name?
> a) -datacenter
> b) -dc
> c) -data-center
> d) -region
>> [!success]- Answer
>> a) -datacenter

> [!question] What happens when a Consul client forwards a service discovery request?
> a) It queries its local cache
> b) It forwards the request to one of the Consul server nodes
> c) It queries the DNS server
> d) It broadcasts to all nodes
>> [!success]- Answer
>> b) It forwards the request to one of the Consul server nodes

> [!question] What is the purpose of the `connect` block in a Consul service registration?
> a) To enable database connectivity
> b) To enable Consul Connect for secure service-to-service communication with mTLS
> c) To connect to external APIs
> d) To establish a VPN connection
>> [!success]- Answer
>> b) To enable Consul Connect for secure service-to-service communication with mTLS

> [!question] Match the Consul concept with its real-world analogy.
>> [!example] Group A
>> a) Service Registry
>> b) Health Check
>> c) Key-Value Store
>
>> [!example] Group B
>> n) Configuration database
>> o) Dynamic phonebook
>> p) Heartbeat monitor
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Raft server state with its behavior.
>> [!example] Group A
>> a) Follower
>> b) Candidate
>> c) Leader
>
>> [!example] Group B
>> n) Sends periodic heartbeats to followers
>> o) Votes for candidates and receives logs
>> p) Requests votes and becomes leader if elected
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Consul network protocol with its transport.
>> [!example] Group A
>> a) Gossip (Serf)
>> b) RPC
>> c) HTTP/DNS
>
>> [!example] Group B
>> n) Service registration and discovery
>> o) Cluster membership and failure detection
>> p) Server-to-server consensus communication
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Consul agent mode with its data storage behavior.
>> [!example] Group A
>> a) Server Mode
>> b) Client Mode
>> c) Dev Mode
>
>> [!example] Group B
>> n) Forwards requests, no data stored
>> o) Stores cluster state and participates in Raft
>> p) Single-node mode for testing
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the service registration field with its JSON key.
>> [!example] Group A
>> a) Service ID
>> b) Service Name
>> c) Health Check
>
>> [!example] Group B
>> n) "name"
>> o) "id"
>> p) "check"
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the consul command with its category.
>> [!example] Group A
>> a) consul agent
>> b) consul members
>> c) consul join
>
>> [!example] Group B
>> n) Cluster membership command
>> o) Node management command
>> p) Cluster connectivity command
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the health check response with its meaning.
>> [!example] Group A
>> a) HTTP 200 OK
>> b) HTTP 429 Too Many Requests
>> c) HTTP 503 Service Unavailable
>
>> [!example] Group B
>> n) Service is passing health check
>> o) Service is in warning state
>> p) Service has failed health check
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the gossip protocol feature with its description.
>> [!example] Group A
>> a) Failure Detection
>> b) Event Propagation
>> c) Membership List
>
>> [!example] Group B
>> n) Detecting when a node goes offline
>> o) Keeping a current list of all cluster nodes
>> p) Disseminating information across the cluster
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the cluster size with its fault tolerance.
>> [!example] Group A
>> a) 3 server nodes
>> b) 5 server nodes
>> c) 1 server node
>
>> [!example] Group B
>> n) No fault tolerance
>> o) Tolerates 1 node failure
>> p) Tolerates 2 node failures
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Python-Consul method with its function.
>> [!example] Group A
>> a) consul.agent.service.register()
>> b) consul.agent.check.register()
>> c) consul.catalog.service()
>
>> [!example] Group B
>> n) Registers a health check
>> o) Registers a service with the agent
>> p) Queries for services by name
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)