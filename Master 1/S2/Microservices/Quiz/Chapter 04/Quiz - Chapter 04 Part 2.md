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
> [!question] Middleware processes are executed only in the request phase, not in the response phase.
>> [!success]- Answer
>> False

> [!question] The `str` path converter is the default converter if none is specified in a URL pattern.
>> [!success]- Answer
>> True

> [!question] A SlugField with `db_index=True` improves database lookup speeds for slug strings.
>> [!success]- Answer
>> True

> [!question] The `re_path()` function has medium-low readability compared to `path()`.
>> [!success]- Answer
>> True

> [!question] FBVs have high reusability compared to CBVs because they are simpler.
>> [!success]- Answer
>> False

> [!question] The `dispatch` method in a CBV uses `getattr` to find the handler for the given HTTP method.
>> [!success]- Answer
>> True

> [!question] Decorating the `dispatch` method in a CBV with `@method_decorator` only affects the GET method.
>> [!success]- Answer
>> False

> [!question] The `slug` converter can match hyphens and underscores in addition to alphanumeric characters.
>> [!success]- Answer
>> True

> [!question] Using hardcoded URL paths in views and templates is a best practice for Django projects.
>> [!success]- Answer
>> False

> [!question] The `render` function combines a template with a context dictionary and returns an HttpResponse.
>> [!success]- Answer
>> True

> [!question] In the HTTP request lifecycle, what happens if a middleware returns an HttpResponse directly?
> a) The request continues to the view
> b) Downstream processing stops and the response is sent back to the client
> c) The middleware stack is restarted
> d) The URL resolver is called anyway
>> [!success]- Answer
>> b) Downstream processing stops and the response is sent back to the client

> [!question] Which path converter matches zero or any positive integer?
> a) str
> b) int
> c) slug
> d) uuid
>> [!success]- Answer
>> b) int

> [!question] What does `reverse('clinical:patient-detail', args=[1])` generate?
> a) /clinical/patient/1/
> b) /patient/1/
> c) /clinical/1/patient-detail/
> d) /patient-detail/1/clinical/
>> [!success]- Answer
>> a) /clinical/patient/1/

> [!question] What is the main advantage of CBVs over FBVs?
> a) CBVs are always faster than FBVs
> b) CBVs support reusability through mixins and inheritance
> c) CBVs do not require URL registration
> d) CBVs automatically handle database migrations
>> [!success]- Answer
>> b) CBVs support reusability through mixins and inheritance

> [!question] Which HTTP status code does `HttpResponseNotAllowed` return?
> a) 200
> b) 400
> c) 405
> d) 500
>> [!success]- Answer
>> c) 405

> [!question] What is the purpose of the `name` parameter in URL patterns?
> a) It sets the database table name
> b) It allows reverse URL resolution
> c) It names the server process
> d) It defines the view function name
>> [!success]- Answer
>> b) It allows reverse URL resolution

> [!question] How does Django's `slugify` utility work in a model's `save` method?
> a) It generates a UUID from the title
> b) It creates a URL-friendly string from the title
> c) It encrypts the title for security
> d) It validates the title format
>> [!success]- Answer
>> b) It creates a URL-friendly string from the title

> [!question] Which regex syntax declares a named capturing group in Django routing?
> a) (name:pattern)
> b) (?P<name>pattern)
> c) {name:pattern}
> d) @name(pattern)
>> [!success]- Answer
>> b) (?P<name>pattern)

> [!question] What happens when a CBV's `as_view()` is called?
> a) It creates a new database table
> b) It returns a callable view function
> c) It renders the template immediately
> d) It registers the URL pattern
>> [!success]- Answer
>> b) It returns a callable view function

> [!question] Which of the following is an advantage of FBVs over CBVs?
> a) Better for complex CRUD operations
> b) Higher simplicity and straightforward code flow
> c) Mixin support for reuse
> d) Automatic HTTP method routing
>> [!success]- Answer
>> b) Higher simplicity and straightforward code flow

> [!question] Match the middleware phase with its processing action.
>> [!example] Group A
>> a) Request Phase Middleware
>> b) Response Phase Middleware
>> c) Short-Circuit Middleware
>
>> [!example] Group B
>> n) Returns HttpResponse before reaching the view
>> o) Processes security, session, and auth headers
>> p) Handles GZip compression and header adjustments
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the path converter with its matching rule.
>> [!example] Group A
>> a) str
>> b) path
>> c) slug
>
>> [!example] Group B
>> n) Matches complete paths including slashes
>> o) Matches any non-empty string except '/'
>> p) Matches alphanumeric text with hyphens and underscores
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the dynamic URL generation method with its location.
>> [!example] Group A
>> a) reverse() in Python
>> b) {% url %} in templates
>> c) redirect() shortcut
>
>> [!example] Group B
>> n) Combines reverse and HTTP redirect
>> o) Used inside Python view functions
>> p) Used inside Django HTML templates
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the FBV pattern element with its function.
>> [!example] Group A
>> a) request.method check
>> b) get_object_or_404()
>> c) return render()
>
>> [!example] Group B
>> n) Retrieves record or raises HTTP 404
>> o) Renders template with context data
>> p) Routes logic based on HTTP verb
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the CBV method with its handling logic.
>> [!example] Group A
>> a) get()
>> b) post()
>> c) dispatch()
>
>> [!example] Group B
>> n) Handles form submission and data creation
>> o) Retrieves and displays data
>> p) Routes to the correct method based on HTTP verb
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the @method_decorator placement with its coverage.
>> [!example] Group A
>> a) On class definition with name='dispatch'
>> b) On individual get() method
>> c) On class definition without name
>
>> [!example] Group B
>> n) Raises a configuration error
>> o) Covers all HTTP methods
>> p) Covers only GET requests
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the converter with the regex equivalent.
>> [!example] Group A
>> a) <int:id>
>> b) <slug:slug>
>> c) <uuid:id>
>
>> [!example] Group B
>> n) [a-zA-Z0-9_-]+
>> o) [0-9]+
>> p) [0-9a-f-]{36}
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Django routing pattern with its use case.
>> [!example] Group A
>> a) Static URL
>> b) Slug-based URL
>> c) Regex-validated URL
>
>> [!example] Group B
>> n) Requires [0-9]{4} year format
>> o) SEO-friendly blog article URL
>> p) About page at /about/
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the CBV comparison metric with its winner.
>> [!example] Group A
>> a) Simplicity
>> b) HTTP Verb Handling
>> c) Reusability
>
>> [!example] Group B
>> n) FBV - straightforward code flow
>> o) CBV - mixins and inheritance
>> p) CBV - dedicated get()/post() methods
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the URL pattern with its correct code syntax.
>> [!example] Group A
>> a) Basic int parameter
>> b) App namespace declaration
>> c) Regex URL pattern
>
>> [!example] Group B
>> n) app_name = 'clinical'
>> o) re_path(r'^archive/(?P<year>[0-9]{4})/$', view)
>> p) path('patient/<int:id>/', view)
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)