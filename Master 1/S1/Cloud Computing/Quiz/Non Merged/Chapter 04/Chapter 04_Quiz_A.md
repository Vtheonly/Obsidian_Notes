---
sources:
  - "[[Chapter 4 - Architecture and Communication Patterns/4.1 What are Microservices.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.2 What are Message Queues and Event-driven Patterns.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.3 What is a Broker.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.4 Event-Driven Architecture (EDA).md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.5 The Publisher-Subscriber Model.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.6 Why Node.js Fits Serverless So Well.md]]"
---

> [!question] Microservices are an architectural approach where applications are divided into small independent services.
>> [!success]- Answer
>> True

> [!question] In a monolithic application each feature is deployed independently.
>> [!success]- Answer
>> False

> [!question] Microservices communicate with each other through shared databases.
>> [!success]- Answer
>> False

> [!question] Message queues enable asynchronous communication between services.
>> [!success]- Answer
>> True

> [!question] The Publisher-Subscriber model decouples message senders from receivers.
>> [!success]- Answer
>> True

> [!question] A broker is not required in a pub/sub messaging system.
>> [!success]- Answer
>> False

> [!question] Event-Driven Architecture relies on producing and consuming events.
>> [!success]- Answer
>> True

> [!question] Node.js fits serverless well because of its synchronous I/O model.
>> [!success]- Answer
>> False

> [!question] Microservices must all use the same programming language.
>> [!success]- Answer
>> False

> [!question] gRPC is an example of synchronous communication between microservices.
>> [!success]- Answer
>> True

> [!question] What is the main characteristic of a microservice architecture?
> a) Single large codebase
> b) Small independent services each with a specific function
> c) Shared database across all components
> d) One deployment unit
>> [!success]- Answer
>> b) Small independent services each with a specific function

> [!question] Which communication pattern is asynchronous?
> a) REST API call
> b) gRPC call
> c) Message queue
> d) HTTP request
>> [!success]- Answer
>> c) Message queue

> [!question] In the Pub/Sub model what is the role of a broker?
> a) Store application data
> b) Route messages from publishers to subscribers
> c) Compile application code
> d) Manage user authentication
>> [!success]- Answer
>> b) Route messages from publishers to subscribers

> [!question] What is the primary advantage of event-driven architecture?
> a) Simpler code
> b) Loosely coupled and scalable services
> c) Eliminates need for databases
> d) Requires only one server
>> [!success]- Answer
>> b) Loosely coupled and scalable services

> [!question] Which is a disadvantage of microservices?
> a) Independent deployment
> b) Complex networking and monitoring
> c) Technology flexibility
> d) Better fault tolerance
>> [!success]- Answer
>> b) Complex networking and monitoring

> [!question] What is a message queue?
> a) A database for storing messages
> b) Middleware that lets services send and receive messages asynchronously
> c) A network protocol
> d) A type of virtual machine
>> [!success]- Answer
>> b) Middleware that lets services send and receive messages asynchronously

> [!question] Which statement about synchronous communication is true?
> a) It decouples services completely
> b) The caller waits for a response before continuing
> c) It uses message queues
> d) It is always more reliable
>> [!success]- Answer
>> b) The caller waits for a response before continuing

> [!question] What does the Publisher-Subscriber model enable?
> a) Direct point-to-point communication
> b) One-to-many message distribution without sender knowing receivers
> c) Synchronous request-response
> d) Shared memory access
>> [!success]- Answer
>> b) One-to-many message distribution without sender knowing receivers

> [!question] Why does Node.js fit well with serverless computing?
> a) It is a compiled language
> b) Its event-driven non-blocking I/O handles short-lived functions efficiently
> c) It requires heavy runtime environments
> d) It supports only synchronous operations
>> [!success]- Answer
>> b) Its event-driven non-blocking I/O handles short-lived functions efficiently

> [!question] What is the key difference between monoliths and microservices?
> a) Monoliths are faster
> b) Microservices can be deployed scaled and developed independently
> c) Monoliths use more resources
> d) Microservices always use Docker
>> [!success]- Answer
>> b) Microservices can be deployed scaled and developed independently

> [!question] Match the microservice characteristic with its benefit.
>> [!example] Group A
>> a) Independent deployment
>> b) Technology diversity
>> c) Fault isolation
>> d) Independent scaling
>
>> [!example] Group B
>> n) Deploy one service without affecting others
>> o) Choose best language for each service job
>> p) A crash in one service does not bring down others
>> q) Scale only the services that need it
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the communication pattern with its description.
>> [!example] Group A
>> a) REST API
>> b) Message queue
>> c) gRPC
>> d) Pub/Sub
>
>> [!example] Group B
>> n) Synchronous HTTP-based API calls
>> o) Asynchronous buffered message passing
>> p) High-performance RPC framework
>> q) Topic-based publish/subscribe messaging
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Pub/Sub role with its function.
>> [!example] Group A
>> a) Publisher
>> b) Subscriber
>> c) Broker
>> d) Topic
>
>> [!example] Group B
>> n) Sends messages to a topic
>> o) Receives messages from subscribed topics
>> p) Routes messages from publishers to subscribers
>> q) Named channel categorizing messages
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the EDA component with its purpose.
>> [!example] Group A
>> a) Event
>> b) Event producer
>> c) Event consumer
>> d) Event channel
>
>> [!example] Group B
>> n) A significant change in state
>> o) Generates and emits events
>> p) Processes events when they occur
>> q) Transports events from producer to consumer
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the cloud option with microservice suitability.
>> [!example] Group A
>> a) Containers (Docker)
>> b) Kubernetes
>> c) Serverless functions
>> d) Virtual machines
>
>> [!example] Group B
>> n) Packages each service with its dependencies
>> o) Orchestrates scaling and networking of services
>> p) Ideal for small event-driven services
>> q) Provides full OS isolation for each service
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the message queue feature with its benefit.
>> [!example] Group A
>> a) Buffering
>> b) Decoupling
>> c) Load leveling
>> d) Guaranteed delivery
>
>> [!example] Group B
>> n) Absorbs traffic spikes between producer and consumer
>> o) Removes direct dependency between services
>> p) Smooths variable processing rates
>> q) Ensures messages are not lost
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the design pattern with its role.
>> [!example] Group A
>> a) Saga pattern
>> b) Circuit breaker
>> c) Event sourcing
>> d) CQRS
>
>> [!example] Group B
>> n) Managing distributed transactions across services
>> o) Prevents cascading failures in service calls
>> p) Stores state changes as a sequence of events
>> q) Separates read and write operations
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the challenge with its solution.
>> [!example] Group A
>> a) Service discovery
>> b) Distributed tracing
>> c) Data consistency
>> d) API gateway
>
>> [!example] Group B
>> n) Service registry for locating service instances
>> o) Request tracking across multiple services
>> p) Eventual consistency and saga patterns
>> q) Single entry point for all microservice requests
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the communication tool with its use.
>> [!example] Group A
>> a) Apache Kafka
>> b) RabbitMQ
>> c) NATS
>> d) Redis Pub/Sub
>
>> [!example] Group B
>> n) Distributed event streaming platform
>> o) Message broker with advanced routing
>> p) High-performance lightweight messaging
>> q) In-memory publish/subscribe messaging
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the microservice deployment concern with its tool.
>> [!example] Group A
>> a) Service registry
>> b) Configuration management
>> c) API documentation
>> d) Health monitoring
>
>> [!example] Group B
>> n) Consul or Eureka
>> o) Consul KV or Kubernetes ConfigMaps
>> p) Swagger/OpenAPI
>> q) Prometheus and Grafana
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
