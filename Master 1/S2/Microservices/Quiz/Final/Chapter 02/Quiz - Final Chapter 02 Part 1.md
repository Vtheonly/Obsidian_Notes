---
sources:
  - "[[Final/Chapter 2]]"
---
> [!question] In the Django request lifecycle, the urls.py file is the first point of contact after the browser sends an HTTP request.
>> [!success]- Answer
>> True

> [!question] REST APIs require the server to maintain session state between client requests.
>> [!success]- Answer
>> False

> [!question] Serialization in DRF converts JSON data into Python Django objects.
>> [!success]- Answer
>> False

> [!question] A ModelViewSet in DRF automatically generates CRUD actions with minimal boilerplate code.
>> [!success]- Answer
>> True

> [!question] The DefaultRouter in DRF generates an interactive API root index page.
>> [!success]- Answer
>> True

> [!question] Template block inheritance allows child templates to override specific sections of a parent template.
>> [!success]- Answer
>> True

> [!question] In a microservices architecture, each service must use the same programming language for consistency.
>> [!success]- Answer
>> False

> [!question] An API acts as a communication bridge allowing two different applications to exchange data.
>> [!success]- Answer
>> True

> [!question] The PUT method in REST APIs is used to partially update an existing resource.
>> [!success]- Answer
>> False

> [!question] The SimpleRouter in DRF does not generate a landing root view listing all active endpoints.
>> [!success]- Answer
>> True

> [!question] How many core constraints define a RESTful architecture?
> a) 4
> b) 5
> c) 6
> d) 7
>> [!success]- Answer
>> c) 6

> [!question] What is the primary purpose of the Template engine in Django's MVT pattern?
> a) To handle business logic
> b) To manage database queries
> c) To separate presentation from application logic
> d) To handle URL routing
>> [!success]- Answer
>> c) To separate presentation from application logic

> [!question] Which DRF serializer type provides absolute manual control over every mapped field?
> a) ModelSerializer
> b) HyperlinkedModelSerializer
> c) Serializer
> d) ListSerializer
>> [!success]- Answer
>> c) Serializer

> [!question] What is a key advantage of microservices architecture?
> a) Simpler testing across services
> b) Technology stack flexibility per service
> c) Single database for all services
> d) Reduced network complexity
>> [!success]- Answer
>> b) Technology stack flexibility per service

> [!question] Which HTTP method is used to create a new resource in REST?
> a) GET
> b) POST
> c) PUT
> d) DELETE
>> [!success]- Answer
>> b) POST

> [!question] What does the ViewSet action list() correspond to in HTTP terms?
> a) GET /resource/{id}/
> b) GET /resource/
> c) POST /resource/
> d) DELETE /resource/{id}/
>> [!success]- Answer
>> b) GET /resource/

> [!question] Which ViewSet class provides automatic full CRUD functionality?
> a) ViewSet
> b) GenericViewSet
> c) ModelViewSet
> d) ReadOnlyModelViewSet
>> [!success]- Answer
>> c) ModelViewSet

> [!question] What is deserialization in the context of DRF?
> a) Converting Python objects to JSON
> b) Converting JSON to Python objects with validation
> c) Deleting database records
> d) Creating database schemas
>> [!success]- Answer
>> b) Converting JSON to Python objects with validation

> [!question] Which REST constraint ensures that each request contains all context needed to process it?
> a) Client-Server
> b) Stateless
> c) Cacheable
> d) Layered System
>> [!success]- Answer
>> b) Stateless

> [!question] What does the include tag {% include 'nav.html' %} do in Django templates?
> a) Extends a parent template
> b) Pulls a reusable partial view into the page
> c) Defines a block placeholder
> d) Loads static files
>> [!success]- Answer
>> b) Pulls a reusable partial view into the page

> [!question] Match the REST HTTP method with its CRUD operation.
>> [!example] Group A
>> a) GET
>> b) POST
>> c) DELETE
>
>> [!example] Group B
>> n) Create a new resource
>> o) Read or retrieve a resource
>> p) Remove a resource
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the DRF component with its description.
>> [!example] Group A
>> a) Serializer
>> b) ModelSerializer
>> c) ViewSet
>
>> [!example] Group B
>> n) Groups CRUD actions into a single cohesive class
>> o) Automatically maps serializers to a Django model
>> p) Provides manual field-by-field control
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the Django lifecycle step with its description.
>> [!example] Group A
>> a) Request Reception
>> b) Routing
>> c) Rendering
>
>> [!example] Group B
>> n) urls.py selects the corresponding view
>> o) View formats data and mixes with HTML
>> p) Browser sends an HTTP request
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the REST constraint with its definition.
>> [!example] Group A
>> a) Client-Server
>> b) Stateless
>> c) Uniform Interface
>
>> [!example] Group B
>> n) Resources follow a standardized, predictable pattern
>> o) Separation of UI concerns from data storage
>> p) Each request contains all context needed
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the microservice characteristic with its description.
>> [!example] Group A
>> a) Autonomous
>> b) Decoupled Database
>> c) Standard Communications
>
>> [!example] Group B
>> n) Each service manages its own storage engine
>> o) Communication over lightweight pathways like HTTP
>> p) Independently deployable and maintained
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the ViewSet hierarchy level with its capability.
>> [!example] Group A
>> a) ViewSet
>> b) ModelViewSet
>> c) ReadOnlyModelViewSet
>
>> [!example] Group B
>> n) Read only list/retrieve actions
>> o) Automatic full CRUD
>> p) Manual action implementation
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the template concept with its description.
>> [!example] Group A
>> a) Block Inheritance
>> b) Partial Views
>> c) Separation of Concerns
>
>> [!example] Group B
>> n) Small reusable templates pulled into pages
>> o) Prevents mixing logic with UI markup
>> p) Child files fill specific placeholders from parent
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the DRF Router with its features.
>> [!example] Group A
>> a) SimpleRouter
>> b) DefaultRouter
>
>> [!example] Group B
>> n) Includes interactive API root index page
>> o) Generates standard CRUD routes only
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the CRUD action with its corresponding ViewSet method.
>> [!example] Group A
>> a) Retrieve
>> b) Update
>> c) Destroy
>
>> [!example] Group B
>> n) PUT /resource/{id}/
>> o) DELETE /resource/{id}/
>> p) GET /resource/{id}/
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the template file type with its role.
>> [!example] Group A
>> a) base.html
>> b) home.html (with extends)
>> c) nav.html
>
>> [!example] Group B
>> n) Inherits shared structure and fills specific blocks
>> o) Defines shared layout with block placeholders
>> p) Reusable partial pulled into other pages
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)