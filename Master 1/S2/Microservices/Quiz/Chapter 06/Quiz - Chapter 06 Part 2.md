---
sources:
  - "[[06.1. REST Principles in DRF API Design]]"
  - "[[06.2. Installation and REST Configuration Core Settings]]"
  - "[[06.3. Base Serializers Manual Fields Mapping]]"
  - "[[06.4. ModelSerializer Automation Mappings]]"
  - "[[06.5. Dynamic Calculations via SerializerMethodField]]"
  - "[[06.6. Deserialization Validation and Database Write Operations]]"
---
> [!question] The REST constraint of Uniform Interface has four sub-constraints including Resource Identification and Self-descriptive Messages.
>> [!success]- Answer
>> True

> [!question] DRF's `SessionAuthentication` can be used alongside `JWTAuthentication` in the same project.
>> [!success]- Answer
>> True

> [!question] Django Forms and DRF Serializers serve the same primary purpose of generating HTML markup.
>> [!success]- Answer
>> False

> [!question] The `exclude` option in a ModelSerializer's Meta class includes all fields except the specified ones.
>> [!success]- Answer
>> True

> [!question] Pre-fetching related data using `annotate` or `prefetch_related` in the view prevents the N+1 Query Problem.
>> [!success]- Answer
>> True

> [!question] In deserialization field-level validation, you should raise a standard Python `ValueError` to indicate invalid data.
>> [!success]- Answer
>> False

> [!question] The `PAGE_SIZE` setting in DRF's REST_FRAMEWORK dictionary controls global pagination behavior.
>> [!success]- Answer
>> True

> [!question] DRF's `FormParser` is one of the default parser classes for processing incoming formats.
>> [!success]- Answer
>> True

> [!question] The `source='nom'` parameter in a serializer field maps the output field name to the model attribute name.
>> [!success]- Answer
>> True

> [!question] Standard JWTs are encrypted, ensuring that the payload data cannot be read by anyone who intercepts the token.
>> [!success]- Answer
>> False

> [!question] Which HTTP method is used for full replacement of a resource in a RESTful API?
> a) POST
> b) PUT
> c) PATCH
> d) MERGE
>> [!success]- Answer
>> b) PUT

> [!question] What is the primary output format of a Django Form compared to a DRF Serializer?
> a) JSON for both
> b) HTML markup for Forms, primitive Python types for Serializers
> c) XML for Forms, JSON for Serializers
> d) YAML for Forms, XML for Serializers
>> [!success]- Answer
>> b) HTML markup for Forms, primitive Python types for Serializers

> [!question] Which DRF parser handler processes incoming JSON payloads?
> a) JSONParser
> b) FormParser
> c) MultiPartParser
> d) FileUploadParser
>> [!success]- Answer
>> a) JSONParser

> [!question] How does `get_<field_name>()` work in a SerializerMethodField?
> a) It retrieves the field value from the database directly
> b) It receives the model instance being serialized as the `obj` parameter
> c) It receives the raw request data as a parameter
> d) It automatically caches the calculated value
>> [!success]- Answer
>> b) It receives the model instance being serialized as the `obj` parameter

> [!question] What does `extra_kwargs` in a ModelSerializer Meta class allow you to do?
> a) Add extra fields not in the model
> b) Override field parameters on auto-generated serializer fields
> c) Create additional database columns
> d) Define custom URL patterns
>> [!success]- Answer
>> b) Override field parameters on auto-generated serializer fields

> [!question] What is the recommended approach to fix the N+1 Query Problem in a SerializerMethodField?
> a) Use caching in the serializer method
> b) Pre-calculate data using annotate() in the view's queryset
> c) Remove the SerializerMethodField
> d) Use a slower database connection
>> [!success]- Answer
>> b) Pre-calculate data using annotate() in the view's queryset

> [!question] In deserialization, what does the `serializer.save()` method call internally?
> a) Either create() or update() depending on whether an instance exists
> b) Always calls create()
> c) Always calls update()
> d) Calls validate() first
>> [!success]- Answer
>> a) Either create() or update() depending on whether an instance exists

> [!question] Which DRF feature provides a user-friendly web interface for testing API endpoints during development?
> a) JSONRenderer
> b) BrowsableAPIRenderer
> c) AdminRenderer
> d) TemplateHTMLRenderer
>> [!success]- Answer
>> b) BrowsableAPIRenderer

> [!question] What is the main difference between DRF Serializers and Django Forms regarding relationship handling?
> a) Serializers cannot handle relationships
> b) Serializers support nested relational serialization
> c) Forms are better at relationship handling
> d) Both handle relationships identically
>> [!success]- Answer
>> b) Serializers support nested relational serialization

> [!question] What should you never store in a JWT payload?
> a) User ID
> b) User role
> c) Sensitive data like passwords or credit card numbers
> d) Token expiration time
>> [!success]- Answer
>> c) Sensitive data like passwords or credit card numbers

> [!question] Match the REST constraint with its purpose.
>> [!example] Group A
>> a) Code on Demand
>> b) Uniform Interface
>> c) Layered System
>
>> [!example] Group B
>> n) Standardized interaction with resources
>> o) Intermediate layers like load balancers
>> p) Optional executable code transfer
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the DRF configuration component with its example.
>> [!example] Group A
>> a) DEFAULT_AUTHENTICATION_CLASSES
>> b) DEFAULT_PAGINATION_CLASS
>> c) DEFAULT_PARSER_CLASSES
>
>> [!example] Group B
>> n) PageNumberPagination
>> o) SessionAuthentication
>> p) JSONParser
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the DRF feature comparison with Django Forms.
>> [!example] Group A
>> a) Primary Output
>> b) Validation Engine
>> c) Relationship Handling
>
>> [!example] Group B
>> n) Nested relational serialization
>> o) HTML markup for Forms
>> p) Parses raw JSON for Serializers
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the serializer concept with its direction.
>> [!example] Group A
>> a) Serialization
>> b) Deserialization
>> c) Validation
>
>> [!example] Group B
>> n) Model instance to Python primitives
>> o) Checking data integrity rules
>> p) JSON payload to validated Python dict
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the validation method with its DRF serializer technique.
>> [!example] Group A
>> a) validate_age(self, value)
>> b) validate(self, data)
>> c) is_valid(raise_exception=True)
>
>> [!example] Group B
>> n) Returns HTTP 400 on validation failure
>> o) Validates a single field
>> p) Validates rules across multiple fields
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the DRF serializer role with its method.
>> [!example] Group A
>> a) create()
>> b) update()
>> c) save()
>
>> [!example] Group B
>> n) Writes new records to the database
>> o) Dispatches to create or update
>> p) Modifies existing records
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the DRF setting with its security implication.
>> [!example] Group A
>> a) BrowsableAPIRenderer in production
>> b) JSONRenderer only
>> c) DEBUG=False
>
>> [!example] Group B
>> n) Standard production configuration
>> o) Disables debug error pages
>> p) Exposes API structure to browsers
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the REST concept with its HTTP mapping.
>> [!example] Group A
>> a) Create
>> b) Read
>> c) Delete
>
>> [!example] Group B
>> n) DELETE method
>> o) GET method
>> p) POST method
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the field type with its validation purpose.
>> [!example] Group A
>> a) IntegerField
>> b) EmailField
>> c) CharField
>
>> [!example] Group B
>> n) Validates integer input
>> o) Validates email format
>> p) Validates string length
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the production configuration with its action.
>> [!example] Group A
>> a) Disable BrowsableAPIRenderer
>> b) Set PAGE_SIZE
>> c) Use JWTAuthentication
>
>> [!example] Group B
>> n) Controls paginated response size
>> o) Stateless API authentication
>> p) Prevents API structure exposure
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)