---
sources:
  - "[[Final/Chapter 1]]"
---
> [!question] A monolithic architecture consists of a single, unified software unit.
>> [!success]- Answer
>> True

> [!question] In a microservices architecture, all services share a single database to ensure data consistency.
>> [!success]- Answer
>> False

> [!question] The API Gateway acts as a single entry point for client requests in a microservices architecture.
>> [!success]- Answer
>> True

> [!question] Django uses the MVC pattern exactly as traditionally defined without any modifications.
>> [!success]- Answer
>> False

> [!question] The ORM translates Python class attributes to database table columns automatically.
>> [!success]- Answer
>> True

> [!question] In a monolithic architecture, scaling requires duplicating the entire application even if only one module needs more resources.
>> [!success]- Answer
>> True

> [!question] Service Discovery in microservices allows services to find each other using hardcoded IP addresses.
>> [!success]- Answer
>> False

> [!question] The manage.py file is the CLI entry point for Django administration tasks.
>> [!success]- Answer
>> True

> [!question] Microservices architecture always has higher deployment speed than monolithic architecture.
>> [!success]- Answer
>> False

> [!question] The models.py file in a Django app handles data structures and business logic.
>> [!success]- Answer
>> True

> [!question] What is the primary characteristic of tight coupling in a monolithic architecture?
> a) Services can be deployed independently
> b) Components are highly interdependent
> c) Each module has its own database
> d) Scaling is granular and efficient
>> [!success]- Answer
>> b) Components are highly interdependent

> [!question] Which component acts as a centralized directory for service instance locations in microservices?
> a) API Gateway
> b) Message Broker
> c) Service Registry
> d) Load Balancer
>> [!success]- Answer
>> c) Service Registry

> [!question] In Django's MVT pattern, what does the View component correspond to in the traditional MVC pattern?
> a) Model
> b) View
> c) Controller
> d) Template
>> [!success]- Answer
>> c) Controller

> [!question] Which of the following is a limitation of the ORM pattern?
> a) Complete SQL syntax abstraction
> b) SGBD Portability
> c) Performance overhead on complex queries
> d) Automatic relationship table management
>> [!success]- Answer
>> c) Performance overhead on complex queries

> [!question] What is the purpose of the wsgi.py file in a Django project?
> a) To define URL path routing
> b) To serve as the WSGI entry point for production deployment
> c) To manage database migrations
> d) To render HTML templates
>> [!success]- Answer
>> b) To serve as the WSGI entry point for production deployment

> [!question] Which Consul operation resolves healthy target instances for a microservice?
> a) Register
> b) Query
> c) Secure
> d) Bootstrap
>> [!success]- Answer
>> b) Query

> [!question] What does polyglot refer to in a microservices architecture?
> a) Using a single programming language for all services
> b) All services communicate using the same protocol
> c) Choosing the best tech stack per service independently
> d) Services share the same database management system
>> [!success]- Answer
>> c) Choosing the best tech stack per service independently

> [!question] Which file in a Django application configures models for the Admin Panel?
> a) views.py
> b) models.py
> c) admin.py
> d) apps.py
>> [!success]- Answer
>> c) admin.py

> [!question] What is the primary function of a Message Broker in microservices?
> a) To route HTTP requests to the correct service
> b) To manage asynchronous inter-service communication
> c) To store service registration data
> d) To aggregate monitoring metrics
>> [!success]- Answer
>> b) To manage asynchronous inter-service communication

> [!question] Which of the following is NOT a component of the Django MVT pattern?
> a) Model
> b) View
> c) Controller
> d) Template
>> [!success]- Answer
>> c) Controller

> [!question] Match the architecture type with its scalability characteristic.
>> [!example] Group A
>> a) Monolithic Architecture
>> b) Microservices Architecture
>
>> [!example] Group B
>> n) All-or-nothing scaling
>> o) Granular, per-service scaling
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)

> [!question] Match the microservice component with its role.
>> [!example] Group A
>> a) API Gateway
>> b) Service Registry
>> c) Message Broker
>
>> [!example] Group B
>> n) Dynamic inventory tracking of service locations
>> o) Single entry point handling routing and authentication
>> p) Manages asynchronous inter-service communication
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Django MVT component with its MVC equivalent.
>> [!example] Group A
>> a) Django Model
>> b) Django View
>> c) Django Template
>
>> [!example] Group B
>> n) The Controller
>> o) The Model
>> p) The View
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the ORM concept with its database equivalent.
>> [!example] Group A
>> a) Python Model Class
>> b) Class Attribute
>> c) Object Instance
>
>> [!example] Group B
>> n) Database Table
>> o) Table Column
>> p) Table Row
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the Django project file with its purpose.
>> [!example] Group A
>> a) settings.py
>> b) urls.py
>> c) manage.py
>
>> [!example] Group B
>> n) Main URL path routing tree registry
>> o) CLI entrypoint for administration tasks
>> p) Centralized global configurations
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Django app file with its responsibility.
>> [!example] Group A
>> a) admin.py
>> b) models.py
>> c) views.py
>
>> [!example] Group B
>> n) View controllers handling incoming requests
>> o) Object-Relational database schema declarations
>> p) Exposes models to Django Admin Panel
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the architectural dimension with its characteristic.
>> [!example] Group A
>> a) Monolithic Resilience
>> b) Microservices Resilience
>
>> [!example] Group B
>> n) Low - A single crash can bring down the system
>> o) High - Fault isolation localizes failures
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)

> [!question] Match the Consul operation with its description.
>> [!example] Group A
>> a) Register
>> b) Query
>> c) Secure
>
>> [!example] Group B
>> n) Resolves healthy target instances
>> o) Adds service instance details to the directory
>> p) Protects communications using mTLS and ACLs
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Django directory entry with its description.
>> [!example] Group A
>> a) __init__.py
>> b) migrations/
>> c) tests.py
>
>> [!example] Group B
>> n) Identifies directory as a Python package
>> o) Auto-generated database structural changes history
>> p) Code Unit testing scripts repository
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the microservice advantage with its description.
>> [!example] Group A
>> a) Independent Deployment
>> b) Technology Evolution
>> c) High Availability
>
>> [!example] Group B
>> n) Services can be deployed without impacting others
>> o) Different technologies can be used per service
>> p) Fault isolation prevents single crash from taking down everything
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)