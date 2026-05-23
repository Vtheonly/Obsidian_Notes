---
sources:
  - "[[06.1. REST Principles in DRF API Design]]"
  - "[[06.2. Installation and REST Configuration Core Settings]]"
  - "[[06.3. Base Serializers Manual Fields Mapping]]"
  - "[[06.4. ModelSerializer Automation Mappings]]"
  - "[[06.5. Dynamic Calculations via SerializerMethodField]]"
  - "[[06.6. Deserialization Validation and Database Write Operations]]"
---
> [!question] REST is an architectural style designed by Roy Fielding in his 2000 doctoral dissertation.
>> [!success]- Answer
>> True

> [!question] In a RESTful API, endpoints should represent actions (verbs) rather than resources (nouns).
>> [!success]- Answer
>> False

> [!question] The `BrowsableAPIRenderer` should be disabled in production environments for security reasons.
>> [!success]- Answer
>> True

> [!question] A DRF Serializer converts Python model instances into primitive Python data types for JSON serialization.
>> [!success]- Answer
>> True

> [!question] A `ModelSerializer` requires you to manually implement `create()` and `update()` methods.
>> [!success]- Answer
>> False

> [!question] The `SerializerMethodField` is a read-only field that adds calculated data not stored in the database.
>> [!success]- Answer
>> True

> [!question] Calling `serializer.is_valid(raise_exception=True)` automatically returns an HTTP 400 Bad Request if validation fails.
>> [!success]- Answer
>> True

> [!question] RESTful APIs should use JSON as the payload format due to its lightweight serialization and compatibility with JavaScript.
>> [!success]- Answer
>> True

> [!question] The `fields = '__all__'` option in ModelSerializer is recommended for production use.
>> [!success]- Answer
>> False

> [!question] Field-level validation in DRF serializers uses a method named `validate()`.
>> [!success]- Answer
>> False

> [!question] Which constraint of RESTful architectures states that the server does not store any client context or session state?
> a) Cacheability
> b) Layered System
> c) Statelessness
> d) Uniform Interface
>> [!success]- Answer
>> c) Statelessness

> [!question] What is the DRF ViewSet method equivalent of a SQL `INSERT` statement?
> a) list()
> b) retrieve()
> c) create()
> d) update()
>> [!success]- Answer
>> c) create()

> [!question] Which Python package provides JWT authentication for DRF?
> a) djangorestframework-jwt
> b) djangorestframework-simplejwt
> c) django-jwt-auth
> d) drf-jwt
>> [!success]- Answer
>> b) djangorestframework-simplejwt

> [!question] What is the primary purpose of the `source` parameter in a DRF Serializer field?
> a) It defines where the data comes from in the URL
> b) It maps the serializer field to a specific attribute on the model instance
> c) It specifies the database connection
> d) It defines the HTML source for file uploads
>> [!success]- Answer
>> b) It maps the serializer field to a specific attribute on the model instance

> [!question] What does the `read_only_fields` option in a ModelSerializer's Meta class do?
> a) It prevents the field from being displayed in GET responses
> b) It includes the field in GET responses but ignores it in write operations
> c) It makes the field required in all operations
> d) It deletes the field from the database
>> [!success]- Answer
>> b) It includes the field in GET responses but ignores it in write operations

> [!question] What performance issue can `SerializerMethodField` introduce if it queries related records in a list view?
> a) Memory leak
> b) The N+1 Query Problem
> c) Connection timeout
> d) Database deadlock
>> [!success]- Answer
>> b) The N+1 Query Problem

> [!question] In deserialization, what step happens after `serializer.is_valid()` returns True?
> a) The serializer returns an error response
> b) Data is stored in `serializer.validated_data`
> c) The data is automatically rendered as JSON
> d) The serializer is destroyed
>> [!success]- Answer
>> b) Data is stored in `serializer.validated_data`

> [!question] Which HTTP method is used to partially update a resource in a RESTful API?
> a) PUT
> b) POST
> c) PATCH
> d) UPDATE
>> [!success]- Answer
>> c) PATCH

> [!question] How does a client pass a JWT token to a secure API endpoint?
> a) In the request body as JSON
> b) In the Authorization header as "Bearer <token>"
> c) As a URL query parameter
> d) In a cookie named "token"
>> [!success]- Answer
>> b) In the Authorization header as "Bearer <token>"

> [!question] What is the SQL equivalent of `serializer.save()` in a create operation?
> a) SELECT
> b) UPDATE
> c) INSERT INTO
> d) DELETE FROM
>> [!success]- Answer
>> c) INSERT INTO

> [!question] Match the core REST constraint with its description.
>> [!example] Group A
>> a) Statelessness
>> b) Cacheability
>> c) Client-Server Decoupling
>
>> [!example] Group B
>> n) UI separated from data storage
>> o) No client context stored on server
>> p) Responses define cache status
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the HTTP method with its RESTful purpose.
>> [!example] Group A
>> a) POST
>> b) PUT
>> c) DELETE
>
>> [!example] Group B
>> n) Replace entire resource
>> o) Create a new resource
>> p) Remove a resource
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the DRF configuration with its purpose.
>> [!example] Group A
>> a) DEFAULT_AUTHENTICATION_CLASSES
>> b) DEFAULT_PERMISSION_CLASSES
>> c) DEFAULT_RENDERER_CLASSES
>
>> [!example] Group B
>> n) Determines what the request user can do
>> p) Processes output response formats
>> o) Determines who is sending the request
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the serializer type with its appropriate use case.
>> [!example] Group A
>> a) Serializer (base class)
>> b) ModelSerializer
>> c) SerializerMethodField
>
>> [!example] Group B
>> n) Complete control over field mapping and validation
>> o) Calculated read-only fields
>> p) Automatic field generation from a model
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the validation level with its DRF method.
>> [!example] Group A
>> a) Field-Level
>> b) Object-Level
>> c) Serializer-Level
>
>> [!example] Group B
>> n) validate()
>> o) validate_<field_name>()
>> p) is_valid()
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the ModelSerializer Meta option with its effect.
>> [!example] Group A
>> a) fields
>> b) read_only_fields
>> c) extra_kwargs
>
>> [!example] Group B
>> n) Customizes field parameters without explicit declaration
>> o) Specifies which model fields to include
>> p) Marks fields as ignored during write operations
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the DRF component with its direction.
>> [!example] Group A
>> a) Serialization
>> b) Deserialization
>> c) Validation
>
>> [!example] Group B
>> n) Converts incoming JSON to Python dicts
>> o) Converts model instances to Python primitives
>> p) Checks data integrity and rules
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the N+1 solution with its approach.
>> [!example] Group A
>> a) annotate
>> b) select_related
>> c) SerializerMethodField
>
>> [!example] Group B
>> n) Pre-calculates aggregated values in the DB query
>> o) Adds custom calculated read-only fields
>> p) Pre-fetches ForeignKey relationships
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the HTTP status code with its RESTful meaning.
>> [!example] Group A
>> a) 200 OK
>> b) 201 Created
>> c) 204 No Content
>
>> [!example] Group B
>> n) Successful DELETE operation
>> o) Successful GET request
>> p) Successful POST creation
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the REST concept with its implementation detail.
>> [!example] Group A
>> a) Resource Identification
>> b) Self-descriptive Messages
>> c) Layered System
>
>> [!example] Group B
>> n) Client cannot tell if talking to end server or intermediate layer
>> o) Each message includes Content-Type metadata
>> p) Resources identified by stable URLs
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)