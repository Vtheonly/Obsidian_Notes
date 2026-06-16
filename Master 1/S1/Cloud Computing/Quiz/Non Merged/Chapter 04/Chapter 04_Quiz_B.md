---
sources:
  - "[[Chapter 4 - Architecture and Communication Patterns/4.1 What are Microservices.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.2 What are Message Queues and Event-driven Patterns.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.3 What is a Broker.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.4 Event-Driven Architecture (EDA).md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.5 The Publisher-Subscriber Model.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.6 Why Node.js Fits Serverless So Well.md]]"
---

> [!question] In event-driven architecture services communicate by producing and consuming events.
>> [!success]- Answer
>> True

> [!question] A message queue stores messages permanently until manually deleted.
>> [!success]- Answer
>> False

> [!question] Pub/Sub requires publishers to know exactly which subscribers exist.
>> [!success]- Answer
>> False

> [!question] The broker in Pub/Sub routes messages to the correct subscribers.
>> [!success]- Answer
>> True

> [!question] Microservices always have lower operational complexity than monoliths.
>> [!success]- Answer
>> False

> [!question] Asynchronous communication eliminates temporal coupling between services.
>> [!success]- Answer
>> True

> [!question] In a monolithic architecture all features are intertwined in a single deployable unit.
>> [!success]- Answer
>> True

> [!question] Node.js is poorly suited for serverless because it is single-threaded.
>> [!success]- Answer
>> False

> [!question] An event in EDA represents a significant change in state.
>> [!success]- Answer
>> True

> [!question] Containerization is the only way to deploy microservices.
>> [!success]- Answer
>> False

> [!question] What is a key disadvantage of synchronous communication?
> a) It is always slower than async
> b) It creates temporal coupling and can cause cascading failures
> c) It requires message brokers
> d) It cannot use HTTP
>> [!success]- Answer
>> b) It creates temporal coupling and can cause cascading failures

> [!question] In Pub/Sub what is a topic?
> a) A database table
> b) A named category for published messages
> c) A network protocol
> d) A type of server
>> [!success]- Answer
>> b) A named category for published messages

> [!question] Which best describes Event-Driven Architecture?
> a) A programming paradigm based on loops
> b) An architecture where components react to events as they occur
> c) A database design pattern
> d) A network topology
>> [!success]- Answer
>> b) An architecture where components react to events as they occur

> [!question] What is the role of the broker in a message queue?
> a) Store and forward messages between producer and consumer
> b) Execute application code
> c) Manage user authentication
> d) Provide DNS resolution
>> [!success]- Answer
>> a) Store and forward messages between producer and consumer

> [!question] Which scenario is NOT suitable for serverless computing?
> a) Short-lived event-driven functions
> b) Long-running stateful processes
> c) Image processing on demand
> d) Webhook handlers
>> [!success]- Answer
>> b) Long-running stateful processes

> [!question] What does Conway Law suggest about microservice architecture?
> a) Services should be organized around business capabilities
> b) All services must use the same database
> c) Monoliths are always better
> d) Teams should be centralized
>> [!success]- Answer
>> a) Services should be organized around business capabilities

> [!question] What is the purpose of an API gateway?
> a) Encrypt all service communications
> b) Single entry point that routes requests to appropriate services
> c) Replace the need for service discovery
> d) Store all microservice data
>> [!success]- Answer
>> b) Single entry point that routes requests to appropriate services

> [!question] Which pattern helps manage distributed transactions?
> a) Singleton pattern
> b) Saga pattern
> c) Factory pattern
> d) Observer pattern
>> [!success]- Answer
>> b) Saga pattern

> [!question] What is distributed tracing used for?
> a) Finding physical location of servers
> b) Tracking a requests path across multiple services
> c) Monitoring CPU usage
> d) Managing IP addresses
>> [!success]- Answer
>> b) Tracking a requests path across multiple services

> [!question] Which is a message queue system?
> a) MySQL
> b) Redis
> c) RabbitMQ
> d) Nginx
>> [!success]- Answer
>> c) RabbitMQ

> [!question] Match the communication style with its example.
>> [!example] Group A
>> a) Synchronous
>> b) Asynchronous
>> c) Event-driven
>> d) Request-reply
>
>> [!example] Group B
>> n) HTTP REST API call waiting for response
>> o) Publishing a message and continuing
>> p) Reacting to state changes in the system
>> q) gRPC call with response expected
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the communication tool with its protocol.
>> [!example] Group A
>> a) REST
>> b) gRPC
>> c) RabbitMQ
>> d) Kafka
>
>> [!example] Group B
>> n) HTTP/HTTPS
>> o) HTTP/2 with Protobuf
>> p) AMQP (Advanced Message Queuing Protocol)
>> q) Custom binary protocol over TCP
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the EDA term with its analogy.
>> [!example] Group A
>> a) Event
>> b) Producer
>> c) Consumer
>> d) Channel
>
>> [!example] Group B
>> n) A newspaper published
>> o) The news agency writing the story
>> p) A person reading the newspaper
>> q) The newspaper delivery system
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Node.js feature with serverless benefit.
>> [!example] Group A
>> a) Event loop
>> b) Non-blocking I/O
>> c) Single-threaded model
>> d) NPM ecosystem
>
>> [!example] Group B
>> n) Efficiently handles multiple concurrent requests
>> o) No thread blocking during I/O operations
>> p) Lightweight execution per function invocation
>> q) Rich library support for cloud integrations
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the integration pattern with resilience.
>> [!example] Group A
>> a) Circuit breaker
>> b) Retry with backoff
>> c) Dead letter queue
>> d) Bulkhead
>
>> [!example] Group B
>> n) Prevents repeated calls to failing services
>> o) Automatically retries with exponential delay
>> p) Stores messages that cannot be processed
>> q) Isolates failures to prevent system-wide impact
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the queue model with delivery behavior.
>> [!example] Group A
>> a) Point-to-point queue
>> b) Pub/Sub topic
>> c) Priority queue
>> d) Delayed queue
>
>> [!example] Group B
>> n) One consumer processes each message
>> o) All subscribers receive each message
>> p) Messages processed by priority level
>> q) Messages available after a delay
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the architectural style with structure.
>> [!example] Group A
>> a) Monolith
>> b) Microservices
>> c) Service-oriented
>> d) Event-driven
>
>> [!example] Group B
>> n) Single codebase deployed as one unit
>> o) Collection of small independent services
>> p) Modular services with enterprise service bus
>> q) Reactive components triggered by events
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the scaling strategy with relevance.
>> [!example] Group A
>> a) Horizontal scaling
>> b) Vertical scaling
>> c) Auto-scaling
>> d) Blue-green deployment
>
>> [!example] Group B
>> n) Adding more instances of a service
>> o) Increasing resources to an existing instance
>> p) Automatic adjustment based on metrics
>> q) Zero-downtime deployment with two environments
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the microservice challenge with context.
>> [!example] Group A
>> a) Network latency
>> b) Data duplication
>> c) Log aggregation
>> d) Versioning
>
>> [!example] Group B
>> n) Overhead from inter-service network calls
>> o) Each service may own duplicate data
>> p) Centralized logging from multiple services
>> q) Managing multiple API versions simultaneously
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the scaling scenario with the approach.
>> [!example] Group A
>> a) Flash sale on e-commerce site
>> b) Scheduled batch processing
>> c) Real-time analytics
>> d) Legacy app modernization
>
>> [!example] Group B
>> n) Horizontal auto-scaling of web tier
>> o) Vertical scaling of compute nodes
>> p) Stream processing with Kafka and Spark
>> q) Container-based microservice decomposition
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
