---
sources:
  - "[[04.1. HTTP Request-Response Lifecycle in Django]]"
  - "[[04.2. Routing URL Pattern Matching and Dynamic Parameters]]"
  - "[[04.3. Routing Slugs and Complex Path Converters]]"
  - "[[04.4. Routing Regular Expression Matchers]]"
  - "[[04.5. Function-Based Views FBVs]]"
  - "[[04.6. Class-Based Views CBVs]]"
  - "[[04.7. The CBV Dispatcher and Method Decorators]]"
---
> [!question] The WSGI/ASGI web server receives the client request and wraps it in a Django HttpRequest object.
>> [!success]- Answer
>> True

> [!question] A middleware can short-circuit the HTTP lifecycle by returning an HttpResponse before the request reaches the view.
>> [!success]- Answer
>> True

> [!question] The `path()` function uses regular expressions to match URL patterns.
>> [!success]- Answer
>> False

> [!question] A SlugField is used to create human-readable SEO-friendly URL representations of model data.
>> [!success]- Answer
>> True

> [!question] The `re_path()` function has higher readability than the `path()` function.
>> [!success]- Answer
>> False

> [!question] Function-Based Views (FBVs) route different HTTP methods using conditional if statements checking `request.method`.
>> [!success]- Answer
>> True

> [!question] Class-Based Views (CBVs) route HTTP requests to dedicated methods like `get()`, `post()`, and `put()`.
>> [!success]- Answer
>> True

> [!question] The `dispatch` method in a CBV inspects the HTTP request method and routes to the matching class method.
>> [!success]- Answer
>> True

> [!question] Applying `@method_decorator` directly to a class definition without specifying the `name` parameter works without errors.
>> [!success]- Answer
>> False

> [!question] The `path` converter matches any non-empty string including path separators like slashes.
>> [!success]- Answer
>> True

> [!question] What is the correct order of the HTTP request lifecycle in Django?
> a) Client → URL Conf → View → Middleware → DB → Client
> b) Client → WSGI/ASGI → Middleware → URL Conf → View → DB → View → Middleware → Client
> c) Client → View → Middleware → URL Conf → DB → Client
> d) Client → DB → View → URL Conf → Middleware → Client
>> [!success]- Answer
>> b) Client → WSGI/ASGI → Middleware → URL Conf → View → DB → View → Middleware → Client

> [!question] Which converter matches a formatted UUID in a URL pattern?
> a) str
> b) int
> c) slug
> d) uuid
>> [!success]- Answer
>> d) uuid

> [!question] What is the purpose of `app_name` in Django URL configuration?
> a) It sets the application's database name
> b) It creates a namespace to avoid route name collisions across apps
> c) It defines the app's Python package name
> d) It generates the URL for the admin interface
>> [!success]- Answer
>> b) It creates a namespace to avoid route name collisions across apps

> [!question] How do you register a Class-Based View in `urls.py`?
> a) path('url/', views.MyCBV, name='name')
> b) path('url/', views.MyCBV.as_view(), name='name')
> c) path('url/', views.MyCBV.dispatch, name='name')
> d) path('url/', MyCBV(), name='name')
>> [!success]- Answer
>> b) path('url/', views.MyCBV.as_view(), name='name')

> [!question] Which decorator restricts the HTTP methods a Function-Based View will accept?
> a) @login_required
> b) @require_http_methods
> c) @permission_required
> d) @csrf_exempt
>> [!success]- Answer
>> b) @require_http_methods

> [!question] What does the `dispatch` method return if the HTTP method is not supported by the CBV?
> a) HTTP 404 Not Found
> b) HTTP 405 Method Not Allowed
> c) HTTP 500 Internal Server Error
> d) HTTP 400 Bad Request
>> [!success]- Answer
>> b) HTTP 405 Method Not Allowed

> [!question] Which utility is used to apply decorators to Class-Based Views?
> a) @class_decorator
> b) @view_decorator
> c) @method_decorator
> d) @decorator_class
>> [!success]- Answer
>> c) @method_decorator

> [!question] What does the `slugify` function do in Django?
> a) Converts a string into a URL-friendly slug
> b) Creates a UUID from a string
> c) Validates email addresses
> d) Encrypts sensitive data
>> [!success]- Answer
>> a) Converts a string into a URL-friendly slug

> [!question] Which routing function is used for regular expression pattern matching?
> a) path()
> b) include()
> c) re_path()
> d) url()
>> [!success]- Answer
>> c) re_path()

> [!question] What happens if a Function-Based View doesn't return an HttpResponse?
> a) It returns a default empty response
> b) Django raises a ValueError
> c) The view is retried automatically
> d) Django returns a 404 response
>> [!success]- Answer
>> b) Django raises a ValueError

> [!question] Match the lifecycle step with its description.
>> [!example] Group A
>> a) WSGI/ASGI Entrypoint
>> b) URL Routing
>> c) View Controller Execution
>
>> [!example] Group B
>> n) Parses URL and extracts variables
>> o) Wraps request in HttpRequest object
>> p) Runs business logic and queries models
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the path converter with the data it matches.
>> [!example] Group A
>> a) int
>> b) slug
>> c) uuid
>
>> [!example] Group B
>> n) Alphanumeric, hyphens, and underscores
>> o) Zero or positive integer
>> p) Formatted unique identifier
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the routing concept with its example URL.
>> [!example] Group A
>> a) Static Route
>> b) Dynamic Integer Parameter
>> c) Slug Parameter
>
>> [!example] Group B
>> n) /contact/
>> o) /blog/introduction-to-django/
>> p) /patient/42/
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the reverse resolution method with its code context.
>> [!example] Group A
>> a) Python view reverse
>> b) Template URL generation
>> c) Redirect using reverse
>
>> [!example] Group B
>> n) {% url 'clinical:patient-detail' patient_id=5 %}
>> o) reverse('clinical:patient-detail', args=[patient_id])
>> p) redirect(reverse('clinical:patient-detail', args=[id]))
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the routing function with its characteristic.
>> [!example] Group A
>> a) path()
>> b) re_path()
>> c) include()
>
>> [!example] Group B
>> n) Uses named regex groups for pattern matching
>> o) Delegates routing to another URL configuration
>> p) High readability with basic type checks
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the FBV component with its purpose.
>> [!example] Group A
>> a) get_object_or_404
>> b) HttpResponseNotAllowed
>> c) render
>
>> [!example] Group B
>> n) Returns HTTP 405 for unsupported methods
>> o) Returns a record or raises HTTP 404
>> p) Combines template with context into HttpResponse
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the CBV pattern with its behavior.
>> [!example] Group A
>> a) dispatch()
>> b) as_view()
>> c) get()
>
>> [!example] Group B
>> n) Converts a class into a callable view function
>> o) Handles GET request method specifically
>> p) Routes request to the correct method
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the decorator approach with the CBV method it affects.
>> [!example] Group A
>> a) @method_decorator(login_required, name='dispatch')
>> b) @method_decorator(login_required) on get()
>> c) @method_decorator on class without name
>
>> [!example] Group B
>> n) Covers all HTTP methods in the view
>> o) Raises a configuration error
>> p) Covers only the GET method
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the URL component with its regex pattern requirement.
>> [!example] Group A
>> a) 4-digit year
>> b) File directory path
>> c) UUID format
>
>> [!example] Group B
>> n) <path:filepath>
>> o) <uuid:id>
>> p) [0-9]{4}
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the CBV advantage with its description.
>> [!example] Group A
>> a) Object-Oriented Principles
>> b) HTTP Method Routing
>> c) Mixin Extensibility
>
>> [!example] Group B
>> n) Dedicated get() and post() methods instead of conditionals
>> o) Inheriting and extending behavior using mixins
>> p) Using class inheritance for code reuse
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)