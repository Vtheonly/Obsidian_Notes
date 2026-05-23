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
> [!question] A monolithic architecture is considered excellent for early-stage startups due to its simplicity.
>> [!success]- Answer
>> True

> [!question] In a microservices architecture, services communicate by directly querying each other's databases using SQL.
>> [!success]- Answer
>> False

> [!question] The API Gateway sits between client applications and internal microservices as a single point of entry.
>> [!success]- Answer
>> True

> [!question] In a microservices architecture, you can have beautifully separated folders in a project and that alone defines it as a microservice.
>> [!success]- Answer
>> False

> [!question] A memory leak in a monolithic application's PDF generation feature has no impact on other features like login or checkout.
>> [!success]- Answer
>> False

> [!question] A Message Broker enables asynchronous communication where Service A drops a message and moves on without waiting for a response.
>> [!success]- Answer
>> True

> [!question] Rate limiting is a core responsibility of the API Gateway that protects backend services from DDoS attacks.
>> [!success]- Answer
>> True

> [!question] In a monolithic architecture, if the billing module needs to scale, you can scale only the billing module independently.
>> [!success]- Answer
>> False

> [!question] Observability in microservices includes centralized logging, monitoring, and distributed tracing to help debug complex issues.
>> [!success]- Answer
>> True

> [!question] Microservices architectures introduce severe technical complexity and should not be used unless the benefits outweigh the costs.
>> [!success]- Answer
>> True

> [!question] Which of the following is a standard component of a microservices ecosystem?
> a) Single shared database
> b) Message Broker / Event Bus
> c) Monolithic deployment pipeline
> d) Centralized monolithic UI
>> [!success]- Answer
>> b) Message Broker / Event Bus

> [!question] What happens to a monolithic application when a single line of code in the billing module is changed?
> a) Only the billing module needs to be redeployed
> b) The entire application must be rebuilt, retested, and redeployed
> c) The change is automatically hot-reloaded
> d) Only the database needs to be updated
>> [!success]- Answer
>> b) The entire application must be rebuilt, retested, and redeployed

> [!question] What does "Bounded Context" mean in microservices terminology?
> a) A service that spans multiple business domains
> b) A service limited to one specific business task
> c) A service bounded by database constraints
> d) A service limited by network bandwidth
>> [!success]- Answer
>> b) A service limited to one specific business task

> [!question] Which industry-standard tools can be used as API Gateways?
> a) MySQL and PostgreSQL
> b) Kong and Traefik
> c) Django and Flask
> d) Redis and Memcached
>> [!success]- Answer
>> b) Kong and Traefik

> [!question] What is the main challenge of distributed transactions in microservices?
> a) They are faster than ACID transactions
> b) They require the Saga pattern to handle network failures
> c) They do not require any rollback mechanisms
> d) They only work with relational databases
>> [!success]- Answer
>> b) They require the Saga pattern to handle network failures

> [!question] How does a stateless service achieve scalability through replication?
> a) By storing all session data in local memory
> b) By delegating state to an external database or cache
> c) By using sticky sessions on the load balancer
> d) By sharing memory between instances
>> [!success]- Answer
>> b) By delegating state to an external database or cache

> [!question] Which of the following is an observability tool used for distributed tracing?
> a) PostgreSQL
> b) Jaeger
> c) Django
> d) Nginx
>> [!success]- Answer
>> b) Jaeger

> [!question] What is the "polyglot" nature of microservices architecture?
> a) All services must use the same programming language
> b) Services can use different programming languages and databases
> c) Services communicate using multiple languages at once
> d) All services must use Python
>> [!success]- Answer
>> b) Services can use different programming languages and databases

> [!question] What is a primary risk of running a single instance of a microservice?
> a) It consumes too many resources
> b) It represents a single point of failure
> c) It is too fast to monitor
> d) It cannot connect to a database
>> [!success]- Answer
>> b) It represents a single point of failure

> [!question] How does the API Gateway help mobile applications when there are many microservices?
> a) By making the mobile app memorize all 50 IP addresses
> b) By aggregating responses from multiple services into a single response
> c) By caching all API responses locally on the phone
> d) By converting REST APIs to GraphQL
>> [!success]- Answer
>> b) By aggregating responses from multiple services into a single response

> [!question] Match the multi-platform challenge with its corresponding description.
>> [!example] Group A
>> a) Data Consistency
>> b) Independent Feature Deployment
>> c) High Availability
>
>> [!example] Group B
>> n) Releasing a mobile feature without forcing web updates or risking downtime
>> o) Ensuring actions on mobile are immediately reflected on the web dashboard
>> p) Guaranteeing the system stays online even if one feature crashes
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the monolithic component with its role in the structure.
>> [!example] Group A
>> a) User Interface
>> b) Business Logic
>> c) Data Access Layer
>
>> [!example] Group B
>> n) Tier responsible for database queries
>> o) Layer containing the core processing rules
>> p) The presentation and templating layer
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the microservice trait with its definition.
>> [!example] Group A
>> a) Extreme Autonomy
>> b) Asynchronous Design
>> c) Single Database Ownership
>
>> [!example] Group B
>> n) Services should not share a database schema
>> o) Services use message brokers instead of waiting for HTTP responses
>> p) Services can be deployed independently without affecting others
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the distributed system component with its real-world example.
>> [!example] Group A
>> a) Message Broker
>> b) Service Registry
>> c) Observability Stack
>
>> [!example] Group B
>> n) HashiCorp Consul
>> o) RabbitMQ or Apache Kafka
>> p) ELK Stack
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the API Gateway responsibility with its description.
>> [!example] Group A
>> a) Request Routing
>> b) Response Aggregation
>> c) Rate Limiting
>
>> [!example] Group B
>> n) Combining results from multiple services into one response
>> o) Limiting how many requests a single IP can make per second
>> p) Inspecting the URL and forwarding to the correct internal service
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the replication concept with its description.
>> [!example] Group A
>> a) Replication
>> b) Load Balancing
>> c) The Stateless Rule
>
>> [!example] Group B
>> n) State must be delegated to an external database or cache
>> o) Distributing requests evenly across service clones
>> p) Running multiple identical clones of a service simultaneously
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the microservice benefit with its corresponding operational cost.
>> [!example] Group A
>> a) Independent Deployments
>> b) Granular Scalability
>> c) Fault Isolation
>
>> [!example] Group B
>> n) Requires advanced DevOps and Kubernetes knowledge
>> o) Requires the Saga pattern for distributed transactions
>> p) Requires centralized logging and distributed tracing
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the framework with the programming language ecosystem.
>> [!example] Group A
>> a) FastAPI
>> b) Fiber
>> c) Express
>
>> [!example] Group B
>> n) Go
>> o) Python
>> p) TypeScript / JavaScript
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the system design goal with its description.
>> [!example] Group A
>> a) Vertical Scaling
>> b) Horizontal Scaling
>> c) Fault Tolerance
>
>> [!example] Group B
>> n) Adding more servers or instances to distribute load
>> o) Upgrading a single server with more CPU and RAM
>> p) Designing a system to continue operating even when components fail
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the microservices challenge with its solution.
>> [!example] Group A
>> a) Inconsistent data across services
>> b) Debugging across multiple services
>> c) Service discovery with changing IPs
>
>> [!example] Group B
>> n) Centralized logging and distributed tracing
>> o) Consul or similar Service Registry
>> p) Saga Pattern for distributed transactions
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)