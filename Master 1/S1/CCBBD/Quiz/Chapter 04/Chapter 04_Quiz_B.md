---
sources:
  - "[[Chapter 4 - Architecture and Communication Patterns/4.1 What are Microservices.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.2 What are Message Queues and Event-driven Patterns.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.3 What is a Broker.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.4 Event-Driven Architecture (EDA).md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.5 The Publisher-Subscriber Model.md]]"
  - "[[Chapter 4 - Architecture and Communication Patterns/4.6 Why Node.js Fits Serverless So Well.md]]"
---

> [!question] Node.js is well-suited for serverless computing due to its event-driven nature.
>> [!success]- Answer
>> True

> [!question] Microservices always require a message broker to communicate.
>> [!success]- Answer
>> False

> [!question] Event-driven architectures are always synchronous by nature.
>> [!success]- Answer
>> False

> [!question] A broker can provide message persistence and delivery guarantees.
>> [!success]- Answer
>> True

> [!question] Tight coupling is a goal of microservices architecture.
>> [!success]- Answer
>> False

> [!question] Why does Node.js fit serverless well?
> a) It is compiled
> b) It uses an event-driven, non-blocking I/O model
> c) It requires a heavy runtime
> d) It only runs on Windows
>> [!success]- Answer
>> b) It uses an event-driven, non-blocking I/O model

> [!question] What decouples producers from consumers in a messaging system?
> a) Direct API calls
> b) The broker/message queue
> c) Shared memory
> d) Environment variables
>> [!success]- Answer
>> b) The broker/message queue

> [!question] Event-driven architectures are typically:
> a) Synchronous and blocking
> b) Asynchronous and non-blocking
> c) Sequential
> d) Batch-oriented
>> [!success]- Answer
>> b) Asynchronous and non-blocking

> [!question] Which pattern allows multiple services to react to the same event?
> a) Request-Response
> b) Publish-Subscribe
> c) Point-to-Point
> d) Polling
>> [!success]- Answer
>> b) Publish-Subscribe

> [!question] A key benefit of microservices is:
> a) Larger codebase per service
> b) Independent deployability and scalability
> c) Single point of failure
> d) Tight coupling
>> [!success]- Answer
>> b) Independent deployability and scalability

> [!question] Match the pattern with its messaging model.
>> [!example] Group A
>> a) Request-Reply
>> b) Fire-and-Forget
>> c) Competing Consumers
>> d) Dead Letter Channel
>
>> [!example] Group B
>> n) Synchronous request followed by response
>> o) Async message without expectation of reply
>> p) Multiple consumers compete for same messages
>> q) Storage for messages that cannot be processed
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the broker type with its specialty.
>> [!example] Group A
>> a) Apache Kafka
>> b) RabbitMQ
>> c) Amazon SQS
>> d) Redis Pub/Sub
>
>> [!example] Group B
>> n) Distributed streaming platform for event logs
>> o) Message broker supporting AMQP protocol
>> p) Fully managed message queuing service
>> q) In-memory publish-subscribe messaging
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the deployment characteristic with serverless.
>> [!example] Group A
>> a) Scaling
>> b) Billing
>> c) Management
>> d) Cold start
>
>> [!example] Group B
>> n) Automatic from zero to any scale
>> o) Pay per execution, not per resource
>> p) Provider manages infrastructure fully
>> q) Initial latency when invoking idle function
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the coupling type with its description.
>> [!example] Group A
>> a) Tight coupling
>> b) Loose coupling
>> c) Temporal coupling
>> d) Spatial coupling
>
>> [!example] Group B
>> n) Components heavily depend on each other
>> o) Components have minimal dependencies
>> p) Sender and receiver must be available simultaneously
>> q) Components must know each other's location
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the ESB concept with its function.
>> [!example] Group A
>> a) Service registry
>> b) Protocol transformation
>> c) Message routing
>> d) Orchestration
>
>> [!example] Group B
>> n) Directory of available services
>> o) Converting between different communication protocols
>> p) Directing messages based on content
>> q) Coordinating multiple service executions
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
