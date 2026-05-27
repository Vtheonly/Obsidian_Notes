---
sources:
  - "[[Final/Chapter 4]]"
---
> [!question] The consul --version command verifies that the Consul binary is correctly installed.
>> [!success]- Answer
>> True

> [!question] The -server flag in Consul CLI indicates the agent runs in server mode to join consensus.
>> [!success]- Answer
>> True

> [!question] The -bootstrap-expect=1 flag allows a single server to self-elect as Leader.
>> [!success]- Answer
>> True

> [!question] The consul agent -dev command launches a single node in-memory agent for local testing.
>> [!success]- Answer
>> True

> [!question] The -data-dir flag specifies the directory where Consul stores its cluster state.
>> [!success]- Answer
>> True

> [!question] The -retry-join flag tells a Consul agent to register with a specific leader address.
>> [!success]- Answer
>> True

> [!question] The -http-port flag in Consul allows running multiple agents on the same machine.
>> [!success]- Answer
>> True

> [!question] The consul members command lists all cluster nodes with their status and type.
>> [!success]- Answer
>> True

> [!question] The consul operator raft list-peers command shows the Raft consensus peers.
>> [!success]- Answer
>> True

> [!question] The -node flag is optional when starting a Consul agent.
>> [!success]- Answer
>> False

> [!question] Which cURL method is used to register a service in Consul via HTTP API?
> a) GET
> b) POST
> c) PUT
> d) DELETE
>> [!success]- Answer
>> c) PUT

> [!question] What does the curl http://localhost:8500/v1/catalog/services command return?
> a) A list of registered nodes
> b) A list of registered catalog services
> c) The health status of a service
> d) The Raft peer list
>> [!success]- Answer
>> b) A list of registered catalog services

> [!question] Which URL endpoint retrieves details of a specific service in Consul?
> a) /v1/health/service/{name}
> b) /v1/catalog/service/{name}
> c) /v1/agent/service/{name}
> d) /v1/status/service/{name}
>> [!success]- Answer
>> b) /v1/catalog/service/{name}

> [!question] What is the purpose of the ?passing parameter in the health check endpoint?
> a) Returns only services that are passing health checks
> b) Skips health checks entirely
> c) Filters services by their name
> d) Returns only failing services
>> [!success]- Answer
>> a) Returns only services that are passing health checks

> [!question] Which cURL command deregisters a service from Consul?
> a) curl --request DELETE /v1/agent/service/deregister/{id}
> b) curl --request PUT /v1/agent/service/deregister/{id}
> c) curl --request PUT /v1/catalog/service/deregister/{id}
> d) curl --request DELETE /v1/catalog/service/deregister/{id}
>> [!success]- Answer
>> a) curl --request PUT /v1/agent/service/deregister/{id}

> [!question] What HTTP status code should a Django health check endpoint return for a healthy service?
> a) 200
> b) 201
> c) 204
> d) 301
>> [!success]- Answer
>> a) 200

> [!question] Which Python library simplifies Consul service registration and discovery?
> a) requests
> b) consul
> c) http
> d) json
>> [!success]- Answer
>> b) consul

> [!question] What does the _ (underscore) variable represent when calling c.catalog.service(name)?
> a) The service metadata
> b) The index value from Consul
> c) The error message
> d) The service ID
>> [!success]- Answer
>> b) The index value from Consul

> [!question] What is returned by the c.catalog.service(name) function in python-consul?
> a) A dictionary
> b) A tuple (index, [list_of_services])
> c) A list of IP addresses
> d) A JSON string
>> [!success]- Answer
>> b) A tuple (index, [list_of_services])

> [!question] What exception should be caught when no healthy instances of a service are found?
> a) ValueError
> b) IndexError
> c) KeyError
> d) TypeError
>> [!success]- Answer
>> b) IndexError

> [!question] Match the Consul CLI flag with its purpose.
>> [!example] Group A
>> a) -server
>> b) -bootstrap-expect=1
>> c) -retry-join
>
>> [!example] Group B
>> n) Register to a leader address
>> o) Self-elect as Leader in a single-node cluster
>> p) Run agent in server mode for consensus
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the Consul CLI command with its output.
>> [!example] Group A
>> a) consul members
>> b) consul operator raft list-peers
>> c) consul agent -dev
>
>> [!example] Group B
>> n) Launches single node in-memory agent at localhost:8500
>> o) Lists all cluster nodes with status and type
>> p) Shows Raft consensus peers with their states
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the cURL endpoint with its purpose.
>> [!example] Group A
>> a) PUT /v1/agent/service/register
>> b) GET /v1/catalog/services
>> c) GET /v1/health/service/{name}?passing
>
>> [!example] Group B
>> n) Lists all registered catalog services
>> o) Registers a new service with health check
>> p) Retrieves healthy instances of a service
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the service registration JSON field with its purpose.
>> [!example] Group A
>> a) ID
>> b) Name
>> c) Check
>
>> [!example] Group B
>> n) The health check configuration
>> o) Unique identifier for the service instance
>> p) Logical service name for discovery
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the health check JSON field with its purpose.
>> [!example] Group A
>> a) HTTP
>> b) Interval
>
>> [!example] Group B
>> n) How often to perform the health check
>> o) The URL endpoint to check for service health
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the Consul command with its node type.
>> [!example] Group A
>> a) consul agent -server
>> b) consul agent (no -server)
>> c) consul agent -dev
>
>> [!example] Group B
>> n) Client agent for development
>> o) Server agent for production
>> p) Client agent without consensus
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the server startup scenario with its required flags.
>> [!example] Group A
>> a) Single server on one machine
>> b) Follower on same machine
>> c) Client agent
>
>> [!example] Group B
>> n) Must override ports to avoid conflicts
>> o) Needs -bootstrap-expect=1
>> p) Omits -server flag
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the port override flag with the standard port it replaces.
>> [!example] Group A
>> a) -server-port=8305
>> b) -http-port=8501
>> c) -dns-port=8601
>
>> [!example] Group B
>> n) Replaces default 8600
>> o) Replaces default 8300
>> p) Replaces default 8500
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Django Consul integration component with its code.
>> [!example] Group A
>> a) Health check view
>> b) Service registration
>> c) Service discovery
>
>> [!example] Group B
>> n) c.agent.service.register(**service_definition)
>> o) return JsonResponse({"status": "ok"}, status=200)
>> p) c.catalog.service(name) returns instance details
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the consul agent -dev characteristic with its behavior.
>> [!example] Group A
>> a) Single node
>> b) In-memory storage
>> c) Web UI exposed
>
>> [!example] Group B
>> n) Data is not persisted to disk
