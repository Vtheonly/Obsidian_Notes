---
sources:
  - "[[07.1. ViewSets Concepts and Action Mappings]]"
  - "[[07.2. ViewSets Structural Class Hierarchy]]"
  - "[[07.3. ModelViewSet and CRUD Automation Engine]]"
  - "[[07.4. ViewSets Hook Methods and Runtime Overrides]]"
  - "[[07.5. Custom Actions and Routes using action]]"
  - "[[07.6. DRF Routing Automations SimpleRouter]]"
  - "[[07.7. DRF Routing Automations DefaultRouter]]"
---
> [!question] A ViewSet combines all CRUD operations for a resource into a single class.
>> [!success]- Answer
>> True

> [!question] The `ViewSet` class inherits from `GenericAPIView` and provides standard database query helpers.
>> [!success]- Answer
>> False

> [!question] A `ModelViewSet` with just a queryset and serializer_class generates all CRUD endpoints automatically.
>> [!success]- Answer
>> True

> [!question] The `get_queryset()` hook method allows you to filter results dynamically based on the requesting user.
>> [!success]- Answer
>> True

> [!question] Custom actions in a ViewSet are defined using the `@custom_action` decorator.
>> [!success]- Answer
>> False

> [!question] A `SimpleRouter` automatically generates URL patterns for your ViewSets based on standard conventions.
>> [!success]- Answer
>> True

> [!question] The `DefaultRouter` generates an interactive API Root View at the root URL path.
>> [!success]- Answer
>> True

> [!question] A ViewSet maps incoming HTTP requests to actions like `list()`, `create()`, and `retrieve()`.
>> [!success]- Answer
>> True

> [!question] The `ReadOnlyModelViewSet` inherits from `CreateModelMixin` and `DestroyModelMixin`.
>> [!success]- Answer
>> False

> [!question] Custom actions require you to define both `detail` and `methods` parameters in the `@action` decorator.
>> [!success]- Answer
>> True

> [!question] Which HTTP method maps to the `list` action in a ViewSet?
> a) POST
> b) GET
> c) PUT
> d) DELETE
>> [!success]- Answer
>> b) GET

> [!question] Which ViewSet class provides complete CRUD operations without needing to write action methods?
> a) ViewSet
> b) GenericViewSet
> c) ModelViewSet
> d) ReadOnlyModelViewSet
>> [!success]- Answer
>> c) ModelViewSet

> [!question] What is the purpose of the `basename` parameter when registering a ViewSet with a Router?
> a) It sets the database table name
> b) It names the auto-generated URL patterns
> c) It defines the serializer class
> d) It sets the HTTP method
>> [!success]- Answer
>> b) It names the auto-generated URL patterns

> [!question] When using `@action(detail=True, methods=['POST'])`, what URL pattern is generated?
> a) /patients/action_name/
> b) /patients/{pk}/action_name/
> c) /action_name/patients/
> d) /patients/action_name/{pk}/
>> [!success]- Answer
>> b) /patients/{pk}/action_name/

> [!question] What happens if you don't define a `queryset` attribute or override `get_queryset()` in a ModelViewSet?
> a) It returns an empty list
> b) Django raises a configuration error
> c) It defaults to all objects
> d) It queries the admin interface
>> [!success]- Answer
>> b) Django raises a configuration error

> [!question] What does the `perform_create()` hook method allow you to do?
> a) Filter the queryset
> b) Automatically assign metadata before saving
> c) Change the serializer class
> d) Define custom URL patterns
>> [!success]- Answer
>> b) Automatically assign metadata before saving

> [!question] Which router includes format suffix patterns like `/api/patients.json`?
> a) SimpleRouter
> b) DefaultRouter
> c) BaseRouter
> d) FormatRouter
>> [!success]- Answer
>> b) DefaultRouter

> [!question] How do you combine multiple app routers in the project's main urls.py?
> a) Using router.merge()
> b) Using path() with include()
> c) Using router.combine()
> d) Using register()
>> [!success]- Answer
>> b) Using path() with include()

> [!question] What does `self.action` in a ViewSet's hook methods refer to?
> a) The HTTP method being used
> b) The current action name (list, create, retrieve, etc.)
> c) The URL path being accessed
> d) The serializer class being used
>> [!success]- Answer
>> b) The current action name (list, create, retrieve, etc.)

> [!question] What is the default HTTP method for a custom action if you don't specify `methods`?
> a) POST
> b) GET
> c) PUT
> d) DELETE
>> [!success]- Answer
>> b) GET

> [!question] Match the ViewSet action with its HTTP method.
>> [!example] Group A
>> a) list
>> b) create
>> c) destroy
>
>> [!example] Group B
>> n) DELETE
>> o) GET
>> p) POST
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the ViewSet class with its inheritance.
>> [!example] Group A
>> a) ViewSet
>> b) GenericViewSet
>> c) ModelViewSet
>
>> [!example] Group B
>> n) Inherits from APIView only
>> o) Inherits from GenericAPIView and all CRUD mixins
>> p) Inherits from GenericAPIView with query helpers
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the hook method with its purpose.
>> [!example] Group A
>> a) get_queryset()
>> b) get_serializer_class()
>> c) perform_create()
>
>> [!example] Group B
>> n) Uses different serializers for different actions
>> o) Filters results dynamically for the current user
>> p) Automatically assigns metadata on save
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the action parameter with its description.
>> [!example] Group A
>> a) detail=False
>> b) detail=True
>> c) methods=['POST']
>
>> [!example] Group B
>> n) Custom action acts on a single record
>> o) Custom action acts on the entire collection
>> p) Restricts the action to POST requests only
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the router with its feature.
>> [!example] Group A
>> a) SimpleRouter
>> b) DefaultRouter
>> c) Both routers
>
>> [!example] Group B
>> n) Generates standard list and detail URLs
>> o) Includes API Root View and format suffixes
>> p) Available in DRF for ViewSet routing
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the ModelViewSet component with its generated action.
>> [!example] Group A
>> a) queryset = Patient.objects.all()
>> b) serializer_class
>> c) permission_classes
>
>> [!example] Group B
>> n) Defines validation and formatting rules
>> o) Defines the base database query
>> p) Restricts access to the API
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the ViewSet concept with its benefit.
>> [!example] Group A
>> a) Single class for all operations
>> b) Router integration
>> c) Hook method overrides
>
>> [!example] Group B
>> n) Automatic URL pattern generation
>> o) Less code duplication across views
>> p) Dynamic customization of behaviors
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the action type with its generated URL.
>> [!example] Group A
>> a) Standard list action
>> b) Collection custom action
>> c) Detail custom action
>
>> [!example] Group B
>> n) /patients/active_records/
>> o) /patients/5/verify_insurance/
>> p) /patients/
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the router registration parameter with its purpose.
>> [!example] Group A
>> a) prefix
>> b) viewset
>> c) basename
>
>> [!example] Group B
>> n) The ViewSet class to register
>> o) URL prefix for all generated patterns
>> p) Name used for URL pattern reversal
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the CRUD mixin with its ViewSet action.
>> [!example] Group A
>> a) ListModelMixin
>> b) CreateModelMixin
>> c) DestroyModelMixin
>
>> [!example] Group B
>> n) destroy()
>> o) list()
>> p) create()
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)