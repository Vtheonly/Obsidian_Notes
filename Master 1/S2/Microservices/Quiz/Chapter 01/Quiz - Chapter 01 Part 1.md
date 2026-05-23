---
sources:
  - "[[01.1. Multi-Platform Systems Challenges]]"
  - "[[01.2. Monolithic Architecture Limitations]]"
  - "[[01.3. Microservices Core Characteristics]]"
  - "[[01.4. Distributed Systems Component Overview]]"
  - "[[01.5. API Gateway Pattern and Responsibilities]]"
  - "[[01.6. Service Layer and Microservice Replication]]"
  - "[[01.7. Microservices Architectural Trade-offs and Operational Costs]]"
---
> [!question] Modern information systems are typically confined to a single interface such as a desktop browser.
>> [!success]- Answer
>> False

> [!question] In a monolithic architecture, if the inventory module is under heavy load, you can scale just that module independently.
>> [!success]- Answer
>> False

> [!question] A microservice must be completely independent of other services, including owning its own database.
>> [!success]- Answer
>> True

> [!question] The API Gateway validates authentication tokens once at the edge and rejects invalid requests before they reach the internal network.
>> [!success]- Answer
>> True

> [!question] In a microservices architecture, services should share a common database schema to ensure data consistency.
>> [!success]- Answer
>> False

> [!question] The "blast radius" in a monolithic architecture means a bug in one feature can crash the entire application process.
>> [!success]- Answer
>> True

> [!question] Stateless services cannot be effectively replicated for scalability because they lose data between requests.
>> [!success]- Answer
>> False

> [!question] Distributed tracing tools like Jaeger attach a unique Trace-ID to requests to track their journey across multiple microservices.
>> [!success]- Answer
>> True

> [!question] Microservices architectures are always the best choice for any project regardless of its size or complexity.
>> [!success]- Answer
>> False

> [!question] In a monolithic architecture, technological lock-in means you can easily adopt new programming languages for specific modules without a major rewrite.
>> [!success]- Answer
>> False

> [!question] Which of the following is NOT one of the key challenges when designing multi-platform systems?
> a) Data consistency
> b) Scalability
> c) File compression
> d) High availability and resilience
>> [!success]- Answer
>> c) File compression

> [!question] What does "monolithic" mean in the context of software architecture?
> a) Composed of many independent modules
> b) Composed all in one piece
> c) Distributed across multiple servers
> d) Using a microkernel design pattern
>> [!success]- Answer
>> b) Composed all in one piece

> [!question] Which characteristic is essential for a component to qualify as a true microservice?
> a) Shared database with other services
> b) Single Responsibility (Bounded Context)
> c) Tight coupling with other services
> d) Single deployment package for all features
>> [!success]- Answer
>> b) Single Responsibility (Bounded Context)

> [!question] What is the primary purpose of a Service Registry in a microservices ecosystem?
> a) To store application logs from all services
> b) To act as a dynamic phonebook for service discovery
> c) To render user interface templates
> d) To manage database schema migrations
>> [!success]- Answer
>> b) To act as a dynamic phonebook for service discovery

> [!question] Which of the following is a core responsibility of an API Gateway?
> a) Database management and schema design
> b) Code compilation and build automation
> c) Response aggregation (Backend for Frontend)
> d) File storage and media processing
>> [!success]- Answer
>> c) Response aggregation (Backend for Frontend)

> [!question] For replication to work seamlessly in a microservice layer, the service must be:
> a) Stateful
> b) Stateless
> c) Single-threaded
> d) Monolithic
>> [!success]- Answer
>> b) Stateless

> [!question] Which pattern is used to handle rollbacks over network calls in distributed transactions?
> a) Observer Pattern
> b) Saga Pattern
> c) Singleton Pattern
> d) Factory Pattern
>> [!success]- Answer
>> b) Saga Pattern

> [!question] What does the API Gateway do when it receives a request with an invalid JWT token?
> a) Forwards the request to the microservice for validation
> b) Rejects the request before it reaches the internal network
> c) Stores the token in a database for later analysis
> d) Redirects the request to a login page
>> [!success]- Answer
>> b) Rejects the request before it reaches the internal network

> [!question] Which of the following is NOT a benefit of microservices architecture?
> a) Granular scalability
> b) Independent deployments
> c) Simplified distributed testing
> d) Fault isolation
>> [!success]- Answer
>> c) Simplified distributed testing

> [!question] In a monolithic architecture, how does the application handle scaling when one module experiences heavy traffic?
> a) Each module scales independently
> b) The entire monolith must be duplicated across servers
> c) Only the database is scaled
> d) Scaling is not possible in a monolith
>> [!success]- Answer
>> b) The entire monolith must be duplicated across servers

> [!question] Match the modern platform type with its corresponding example.
>> [!example] Group A
>> a) Web Applications
>> b) Mobile Applications
>> c) Third-Party Integrations
>
>> [!example] Group B
>> n) iOS and Android apps
>> o) B2B APIs and IoT devices
>> p) React and Angular frameworks
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the monolithic limitation with its correct description.
>> [!example] Group A
>> a) All or Nothing Deployment
>> b) Blast Radius
>> c) Technological Lock-in
>
>> [!example] Group B
>> n) A bug in one feature crashes the entire process
>> o) Every module must use the same programming language
>> p) Changing one line requires rebuilding the entire application
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the microservice characteristic with its corresponding description.
>> [!example] Group A
>> a) Single Responsibility
>> b) Independent Data
>> c) Independent Deployment
>
>> [!example] Group B
>> n) Deploy a new version without restarting other services
>> o) Each service owns its own database
>> p) Executes one specific business task
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the ecosystem component with its primary role.
>> [!example] Group A
>> a) API Gateway
>> b) Message Broker
>> c) Service Registry
>
>> [!example] Group B
>> n) Acts as a dynamic phonebook for service discovery
>> o) Acts as the single point of entry for client requests
>> p) Enables asynchronous communication between services
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the API Gateway responsibility with its corresponding action.
>> [!example] Group A
>> a) Request Routing
>> b) Authentication
>> c) Rate Limiting
>
>> [!example] Group B
>> n) Validates JWT tokens at the edge of the network
>> o) Protects backend services from DDoS attacks
>> p) Forwards requests to the correct internal service
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the popular framework with its programming language.
>> [!example] Group A
>> a) Django
>> b) Spring Boot
>> c) NestJS
>
>> [!example] Group B
>> n) Java / Kotlin
>> o) Python
>> p) TypeScript
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the microservice benefit with its description.
>> [!example] Group A
>> a) Granular Scalability
>> b) Fault Isolation
>> c) Technological Freedom
>
>> [!example] Group B
>> n) Teams can choose the best language for their specific problem
>> o) Scale only the parts of the system under heavy load
>> p) A crash in one service does not affect other services
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the operational cost with its implication.
>> [!example] Group A
>> a) Distributed Testing
>> b) Distributed Transactions
>> c) Mandatory Observability
>
>> [!example] Group B
>> n) Need the Saga pattern to handle rollbacks
>> o) Need to mock network calls for integration tests
>> p) Need centralized logging and distributed tracing
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the service type with its characteristic.
>> [!example] Group A
>> a) Stateless Service
>> b) Stateful Service
>> c) Message Broker
>
>> [!example] Group B
>> n) Maintains continuous state for data persistence
>> o) Stores no local data between incoming requests
>> p) Facilitates asynchronous service communication
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the architectural challenge with its microservices solution.
>> [!example] Group A
>> a) Dynamic IP addresses
>> b) Network request tracing
>> c) Single point of failure
>
>> [!example] Group B
>> n) Service Registry for dynamic discovery
>> o) Service replication for high availability
>> p) Distributed tracing with unique Trace-IDs
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)