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
> [!question] A Service Registry acts as a dynamic phonebook for microservices to discover each other.
>> [!success]- Answer
>> True

> [!question] Consul uses the Raft consensus protocol to maintain consistency across server nodes.
>> [!success]- Answer
>> True

> [!question] The Raft protocol can tolerate a minority of nodes failing while still maintaining a functional cluster.
>> [!success]- Answer
>> True

> [!question] The Gossip protocol in Consul is used only for the LAN and not for the WAN.
>> [!success]- Answer
>> False

> [!question] Consul agents can run in either server mode or client mode.
>> [!success]- Answer
>> True

> [!question] The `consul agent` command is used to start a Consul agent on a node.
>> [!success]- Answer
>> True

> [!question] A health check endpoint in Django returns a simple status response indicating the application's health.
>> [!success]- Answer
>> True

> [!question] The `python-consul` library allows Django applications to interact with Consul programmatically.
>> [!success]- Answer
>> True

> [!question] In Raft consensus, Log Replication ensures that all server nodes execute the same commands in the same order.
>> [!success]- Answer
>> True

> [!question] A quorum in Raft requires more than half of the voting server nodes to agree on a leader.
>> [!success]- Answer
>> True

> [!question] What is the primary purpose of a Service Registry in microservices?
> a) To store application logs
> b) To act as a dynamic phonebook for service discovery
> c) To render UI templates
> d) To manage database connections
>> [!success]- Answer
>> b) To act as a dynamic phonebook for service discovery

> [!question] Which consensus protocol does HashiCorp Consul use?
> a) Paxos
> b) Raft
> c) Zab
> d) PBFT
>> [!success]- Answer
>> b) Raft

> [!question] What is the minimum number of nodes required to form a fault-tolerant Raft cluster?
> a) 1
> b) 2
> c) 3
> d) 5
>> [!success]- Answer
>> c) 3

> [!question] What does the Serf Gossip protocol handle in Consul?
> a) Database replication
> b) Cluster membership, failure detection, and event propagation
> c) HTTP request routing
> d) Service registration
>> [!success]- Answer
>> b) Cluster membership, failure detection, and event propagation

> [!question] Which Consul port is used for the HTTP API?
> a) 8300
> b) 8301
> c) 8500
> d) 8600
>> [!success]- Answer
>> c) 8500

> [!question] What is the purpose of the `consul members` command?
> a) To list all registered services
> b) To list all cluster members and their status
> c) To create a new service registration
> d) To check health check status
>> [!success]- Answer
>> b) To list all cluster members and their status

> [!question] What format is used for Consul service registration definitions?
> a) XML
> b) YAML
> c) JSON
> d) TOML
>> [!success]- Answer
>> c) JSON

> [!question] What should a Django health check endpoint return when the application is healthy?
> a) HTTP 500 with error message
> b) HTTP 200 with status OK
> c) HTTP 302 redirect
> d) HTTP 404 Not Found
>> [!success]- Answer
>> b) HTTP 200 with status OK

> [!question] What does the `consul kv put` command do?
> a) Puts a service into maintenance mode
> b) Writes a key-value pair to Consul's key-value store
> c) Registers a new client node
> d) Updates DNS records
>> [!success]- Answer
>> b) Writes a key-value pair to Consul's key-value store

> [!question] Which Python package allows programmatic integration with Consul?
> a) consul-py
> b) python-consul
> c) django-consul
> d) consul-client
>> [!success]- Answer
>> b) python-consul

> [!question] Match the Consul component with its role.
>> [!example] Group A
>> a) Server Node
>> b) Client Node
>> c) Agent
>
>> [!example] Group B
>> n) Runs on every node in the cluster
>> o) Participates in Raft consensus and stores data
>> p) Forwards requests to servers, does not store data
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Raft consensus phase with its purpose.
>> [!example] Group A
>> a) Leader Election
>> b) Log Replication
>> c) Safety
>
>> [!example] Group B
>> n) Ensures consistency across all servers
>> o) Selecting a new leader when current leader fails
>> p) Guarantees committed entries are preserved
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Consul protocol with its network scope.
>> [!example] Group A
>> a) LAN Gossip Protocol
>> b) WAN Gossip Protocol
>> c) Raft Protocol
>
>> [!example] Group B
>> n) Used for server node data consistency
>> o) Used for data center cluster membership
>> p) Used for cross-data center communication
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Consul port with its service.
>> [!example] Group A
>> a) 8300
>> b) 8301
>> c) 8500
>
>> [!example] Group B
>> n) LAN/WAN Gossip
>> o) Server RPC (consensus)
>> p) HTTP API
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Consul CLI command with its function.
>> [!example] Group A
>> a) consul agent
>> b) consul members
>> c) consul join
>
>> [!example] Group B
>> n) List all cluster members
>> o) Start a Consul agent
>> p) Join a node to an existing cluster
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the service registration field with its purpose.
>> [!example] Group A
>> a) name
>> b) address
>> c) port
>
>> [!example] Group B
>> n) Network port the service runs on
>> o) Hostname or IP of the service
>> p) Logical name identifying the service
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the health check type with its description.
>> [!example] Group A
>> a) Script check
>> b) HTTP check
>> c) TTL check
>
>> [!example] Group B
>> n) Runs a command on the agent node
>> o) Queries an HTTP endpoint periodically
>> p) Expects the service to report its status
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the Raft node state with its meaning.
>> [!example] Group A
>> a) Follower
>> b) Candidate
>> c) Leader
>
>> [!example] Group B
>> n) Manages log replication and client requests
>> o) Passively accepts log entries from leader
>> p) Requests votes to become leader
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the cluster operation with its purpose.
>> [!example] Group A
>> a) Bootstrapping
>> b) Joining
>> c) Leaving
>
>> [!example] Group B
>> n) Adding a node to an existing cluster
>> p) Gracefully removing a node from the cluster
>> o) Starting the initial cluster setup
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Consul integration with its Python code.
>> [!example] Group A
>> a) Consul(host='localhost', port=8500)
>> b) consul.agent.service.register()
>> c) consul.kv.put('key', 'value')
>
>> [!example] Group B
>> n) Writes to the key-value store
>> o) Registers a service with Consul
>> p) Initializes the Consul client connection
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)