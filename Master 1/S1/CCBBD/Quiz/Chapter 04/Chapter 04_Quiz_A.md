---
sources:
  - "[[Chapter 4 - Architecture and Communication Patterns/4.1 What are Microservices.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.2 What are Message Queues and Event-driven Patterns.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.3 What is a Broker.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.4 Event-Driven Architecture (EDA).md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.5 The Publisher-Subscriber Model.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.6 Why Node.js Fits Serverless So Well.md]]"
---

> [!question] Microservices architecture splits an application into small, independent services.
>> [!success]- Answer
>> True

> [!question] Message queues enable asynchronous communication between services.
>> [!success]- Answer
>> True

> [!question] A broker is a component that routes messages between producers and consumers.
>> [!success]- Answer
>> True

> [!question] Event-Driven Architecture (EDA) relies on the production and consumption of events.
>> [!success]- Answer
>> True

> [!question] In the Publisher-Subscriber model, publishers send messages directly to specific subscribers.
>> [!success]- Answer
>> False

> [!question] Microservices architecture is characterized by:
> a) Single monolithic deployment
> b) Small independent services communicating via APIs
> c) All code in one repository
> d) Shared database for all services
>> [!success]- Answer
>> b) Small independent services communicating via APIs

> [!question] A message queue provides:
> a) Direct synchronous communication
> b) Asynchronous decoupling of services
> c) Permanent data storage
> d) CPU scheduling
>> [!success]- Answer
>> b) Asynchronous decoupling of services

> [!question] In Event-Driven Architecture, events are:
> a) Error messages only
> b) Significant changes in state
> c) Database backups
> d) Network pings
>> [!success]- Answer
>> b) Significant changes in state

> [!question] A broker in messaging systems typically:
> a) Routes messages between producers and consumers
> b) Replaces the database
> c) Manages physical servers
> d) Compiles application code
>> [!success]- Answer
>> a) Routes messages between producers and consumers

> [!question] In the Publisher-Subscriber model:
> a) Publishers send to specific subscribers
> b) Publishers send messages without knowing subscribers
> c) Subscribers send messages to publishers
> d) Messages are always deleted after reading
>> [!success]- Answer
>> b) Publishers send messages without knowing subscribers

> [!question] Match the architecture style with its description.
>> [!example] Group A
>> a) Monolithic
>> b) Microservices
>> c) Event-Driven
>> d) Layered
>
>> [!example] Group B
>> n) Single unified codebase for entire application
>> o) Small independent services communicating via APIs
>> p) Components react to events asynchronously
>> q) Organized in tiers with specific responsibilities
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the messaging concept with its role.
>> [!example] Group A
>> a) Producer
>> b) Consumer
>> c) Broker
>> d) Queue
>
>> [!example] Group B
>> n) Creates and sends messages
>> o) Receives and processes messages
>> p) Routes messages between producers and consumers
>> q) Temporary storage for pending messages
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the communication pattern with its behavior.
>> [!example] Group A
>> a) Synchronous
>> b) Asynchronous
>> c) Publish-Subscribe
>> d) Point-to-Point
>
>> [!example] Group B
>> n) Sender blocks until response is received
>> o) Sender continues without waiting for response
>> p) One-to-many message distribution
>> q) One-to-one message delivery
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the EDA component with its function.
>> [!example] Group A
>> a) Event
>> b) Event source
>> c) Event handler
>> d) Event bus
>
>> [!example] Group B
>> n) A significant change in state
>> o) Component that generates events
>> p) Component that processes events
>> q) Channel that transports events
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the microservice benefit with its description.
>> [!example] Group A
>> a) Scalability
>> b) Resilience
>> c) Autonomy
>> d) Technology diversity
>
>> [!example] Group B
>> n) Each service can be scaled independently
>> o) Failure in one service does not cascade
>> p) Teams can develop and deploy independently
>> q) Different tech stacks can be used per service
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
