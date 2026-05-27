---
sources:
  - "[[Final/Chapter 2]]"
---
> [!question] The Django path converter int captures a floating point number from the URL.
>> [!success]- Answer
>> False

> [!question] Class-Based Views in Django automatically route GET requests to the get() method via the dispatch() method.
>> [!success]- Answer
>> True

> [!question] The {% csrf_token %} tag is optional in Django forms.
>> [!success]- Answer
>> False

> [!question] A ModelForm in Django is automatically linked to a specific model class.
>> [!success]- Answer
>> True

> [!question] The @action decorator in DRF allows attaching custom HTTP endpoints to ViewSets.
>> [!success]- Answer
>> True

> [!question] The collectstatic command in Django collects static files from all apps into a single directory.
>> [!success]- Answer
>> True

> [!question] A partial update in DRF is performed using the PUT HTTP method with partial=True.
>> [!success]- Answer
>> False

> [!question] The form.as_p method renders form fields inside paragraph tags.
>> [!success]- Answer
>> True

> [!question] The re_path function in Django allows using regular expressions for URL matching.
>> [!success]- Answer
>> True

> [!question] A custom serializer method field in DRF must follow the naming pattern get_fieldname.
>> [!success]- Answer
>> True

> [!question] Which Django path converter captures a full relative path containing slashes?
> a) int
> b) slug
> c) path
> d) str
>> [!success]- Answer
>> c) path

> [!question] What is the key parameter used in DRF to indicate a partial update in a serializer?
> a) update=True
> b) partial=True
> c) patch=True
> d) modify=True
>> [!success]- Answer
>> b) partial=True

> [!question] Which method must be overridden in a ModelViewSet to customize queryset filtering?
> a) get_serializer_class()
> b) get_queryset()
> c) perform_create()
> d) perform_update()
>> [!success]- Answer
>> b) get_queryset()

> [!question] What does the form.is_valid() method do in Django?
> a) Saves the form data to the database
> b) Validates the submitted form data
> c) Renders the form as HTML
> d) Checks if the user is authenticated
>> [!success]- Answer
>> b) Validates the submitted form data

> [!question] Which HTTP method triggers the create() action in a DRF ViewSet?
> a) GET
> b) POST
> c) PUT
> d) DELETE
>> [!success]- Answer
>> b) POST

> [!question] What does the @action(detail=False) decorator create in a ViewSet?
> a) A custom endpoint on a single resource
> b) A custom endpoint on the entire collection
> c) A new model serializer
> d) A new route in urls.py
>> [!success]- Answer
>> b) A custom endpoint on the entire collection

> [!question] Which of the following is a valid Django template conditional tag?
> a) {{ if condition }}
> b) {% if condition %}
> c) <if condition>
> d) $(if condition)
>> [!success]- Answer
>> b) {% if condition %}

> [!question] What does the Meta class fields = '__all__' do in a ModelSerializer?
> a) Excludes all fields from serialization
> b) Includes all model fields in the serializer
> c) Validates all form fields
> d) Creates all database tables
>> [!success]- Answer
>> b) Includes all model fields in the serializer

> [!question] What is the purpose of the STATIC_ROOT setting in Django?
> a) Defines the URL prefix for static files in development
> b) Defines the absolute path for production static file deployment
> c) Lists directories for static file search in development
> d) Configures the template engine for static files
>> [!success]- Answer
>> b) Defines the absolute path for production static file deployment

> [!question] In a DRF custom action with @action(detail=True, methods=['post']), which URL pattern is generated?
> a) POST /resource/action/
> b) POST /resource/{id}/action/
> c) POST /action/resource/
> d) POST /action/resource/{id}/
>> [!success]- Answer
>> b) POST /resource/{id}/action/

> [!question] Match the URL path converter with the data it captures.
>> [!example] Group A
>> a) int
>> b) slug
>> c) path
>
>> [!example] Group B
>> n) Alphanumeric string with dashes/underscores
>> o) Full relative path containing slashes
>> p) Integer number
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Django view type with its code pattern.
>> [!example] Group A
>> a) Function-Based View
>> b) Class-Based View
>> c) View with dispatch()
>
>> [!example] Group B
>> n) def ma_vue(request)
>> o) class DashboardView(View) with get() and post()
>> p) Intercepts requests before method dispatching
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the form rendering style with its HTML output.
>> [!example] Group A
>> a) form.as_p
>> b) form.as_table
>> c) form.as_ul
>
>> [!example] Group B
>> n) Fields in table format rows
>> o) Fields inside block paragraphs
>> p) Fields as list markup items
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the SerializerMethodField with its required pattern.
>> [!example] Group A
>> a) Field declaration
>> b) Method name
>> c) Method return value
>
>> [!example] Group B
>> n) The calculated data to include in serialization
>> o) nom_complet = serializers.SerializerMethodField()
>> p) def get_nom_complet(self, obj)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the ModelViewSet override method with its purpose.
>> [!example] Group A
>> a) get_serializer_class()
>> b) perform_create()
>> c) perform_update()
>
>> [!example] Group B
>> n) Injects custom fields when creating a record
>> o) Selects different serializers per action
>> p) Triggers actions after updating a record
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the @action detail parameter with its scope.
>> [!example] Group A
>> a) detail=True
>> b) detail=False
>
>> [!example] Group B
>> n) Applies to the entire collection
>> o) Applies to a single resource
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the DRF ViewSet method with its HTTP verb and URL.
>> [!example] Group A
>> a) list
>> b) create
>> c) retrieve
>
>> [!example] Group B
>> n) POST /resource/
>> o) GET /resource/{id}/
>> p) GET /resource/
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Python requests call with its HTTP action.
>> [!example] Group A
>> a) requests.get()
>> b) requests.post()
>> c) requests.put()
>
>> [!example] Group B
>> n) Send JSON data to create a resource
>> o) Read data from a URL
>> p) Update an existing resource
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the configuration setting with its purpose.
>> [!example] Group A
>> a) TEMPLATES DIRS
>> b) STATICFILES_DIRS
>> c) STATIC_ROOT
>
>> [!example] Group B
>> n) Dev path for static file directories
>> o) Production deployment path for static files
>> p) Tells Django where HTML template files live
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Router registration parameter with its role.
>> [!example] Group A
>> a) router.register(r'auteurs', AuteurViewSet)
>> b) basename parameter
>> c) prefix parameter
>
>> [!example] Group B
>> n) Required if ViewSet lacks a queryset attribute
>> o) The URL path prefix for the viewset
>> p) The ViewSet class to register
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)