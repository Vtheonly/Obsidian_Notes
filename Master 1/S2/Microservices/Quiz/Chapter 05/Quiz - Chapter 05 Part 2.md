---
sources:
  - "[[05.1. Django Template Language Syntax]]"
  - "[[05.2. Layout Inheritance and Block Architecture]]"
  - "[[05.3. Static Assets Management and Configurations]]"
  - "[[05.4. HTML5 Standard Core Layout Integration]]"
  - "[[05.5. Standard Django Form Class Validation]]"
  - "[[05.6. Django ModelForms and Automatic Synchronization]]"
  - "[[05.7. Form Presentation Rendering Styles]]"
  - "[[05.8. Form Lifecycles inside Controller Views]]"
---
> [!question] The `{% for %}` tag in DTL supports a `{% empty %}` block that executes if the list is empty.
>> [!success]- Answer
>> True

> [!question] Django's automatic HTML escaping prevents Cross-Site Scripting (XSS) attacks by rendering script tags as literal text.
>> [!success]- Answer
>> True

> [!question] The `{% include %}` tag is used for layout inheritance between parent and child templates.
>> [!success]- Answer
>> False

> [!question] The `STATIC_URL` configuration defines the absolute system folder path for production static files.
>> [!success]- Answer
>> False

> [!question] A Django `Form` class inherits from `django.forms.Form` and manages validation and error handling.
>> [!success]- Answer
>> True

> [!question] A `ModelForm` requires you to write custom `create()` and `update()` methods for saving data.
>> [!success]- Answer
>> False

> [!question] The `form.as_ul` rendering style requires a parent `<ul>` container to produce valid HTML.
>> [!success]- Answer
>> True

> [!question] In a CBV form lifecycle, the POST method should instantiate an empty form and render it.
>> [!success]- Answer
>> False

> [!question] The `forloop.counter` variable in DTL loops outputs the current iteration count starting from 0.
>> [!success]- Answer
>> False

> [!question] The `ValidationError` is raised in form validation when data fails the validation rules.
>> [!success]- Answer
>> True

> [!question] What does the `{% empty %}` tag do inside a `{% for %}` loop in DTL?
> a) It clears the loop variables
> b) It executes if the loop iterable is empty or None
> c) It skips the first iteration
> d) It ends the loop early
>> [!success]- Answer
>> b) It executes if the loop iterable is empty or None

> [!question] Which configuration in settings.py defines where Django looks for raw static assets during development?
> a) STATIC_URL
> b) STATIC_ROOT
> c) STATICFILES_DIRS
> d) STATICFILES_FINDERS
>> [!success]- Answer
>> c) STATICFILES_DIRS

> [!question] In Django forms, what is `clean_<fieldname>()` used for?
> a) To validate rules spanning multiple fields
> b) To validate a single specific field
> c) To clean all form data at once
> d) To reset the form to its initial state
>> [!success]- Answer
>> b) To validate a single specific field

> [!question] What must you do after creating a Django app to make its templates and static files discoverable?
> a) Run collectstatic
> b) Register the app in INSTALLED_APPS
> c) Create a templates folder
> d) Add the app to urls.py
>> [!success]- Answer
>> b) Register the app in INSTALLED_APPS

> [!question] Which of the following is NOT a DTL filter?
> a) |upper
> b) |default
> c) |if
> d) |truncatechars
>> [!success]- Answer
>> c) |if

> [!question] What is the `forloop.first` variable used for in a DTL for loop?
> a) It outputs the index of the first item
> b) It returns True on the first iteration
> c) It returns the first item in the list
> d) It stops the loop after the first iteration
>> [!success]- Answer
>> b) It returns True on the first iteration

> [!question] Which production server is recommended for serving static files?
> a) Gunicorn
> b) Nginx
> c) uWSGI
> d) Django runserver
>> [!success]- Answer
>> b) Nginx

> [!question] In the PRG pattern, what happens when form validation fails in the POST handler?
> a) The user is redirected to an error page
> b) The form is re-rendered with validation error messages
> c) The form data is discarded silently
> d) A 500 error is returned
>> [!success]- Answer
>> b) The form is re-rendered with validation error messages

> [!question] What does the `widgets` attribute in a ModelForm's Meta class control?
> a) The database column type
> b) The HTML rendering of form fields
> c) The validation logic
> d) The URL patterns
>> [!success]- Answer
>> b) The HTML rendering of form fields

> [!question] How does `form.non_field_errors` differ from `field.errors`?
> a) They are the same thing
> b) non_field_errors contains errors from the clean() method
> c) non_field_errors contains all field errors combined
> d) non_field_errors is only for ModelForms
>> [!success]- Answer
>> b) non_field_errors contains errors from the clean() method

> [!question] Match the DTL template tag with its control flow purpose.
>> [!example] Group A
>> a) {% if %}
>> b) {% for %}
>> c) {% empty %}
>
>> [!example] Group B
>> n) Iterates over a list or queryset
>> o) Handles conditional branching logic
>> p) Provides fallback content for empty lists
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the template inheritance strategy with its use case.
>> [!example] Group A
>> a) extends
>> b) include
>> c) block
>
>> [!example] Group B
>> n) Embedding reusable HTML fragments
>> o) Defining a region child templates can override
>> p) Inheriting the full parent page layout
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Django Form component with its role.
>> [!example] Group A
>> a) fields
>> b) widgets
>> c) labels
>
>> [!example] Group B
>> n) Customizes CSS classes or HTML attributes
>> o) Defines which model attributes to include
>> p) Customizes the display text for field names
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the form rendering approach with its best use case.
>> [!example] Group A
>> a) form.as_p
>> b) Manual field looping
>> c) form.as_table
>
>> [!example] Group B
>> n) Rapid prototyping with basic HTML
>> o) Custom CSS frameworks like Tailwind
>> p) Table-based form layouts
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the validation method with its scope.
>> [!example] Group A
>> a) clean_<fieldname>()
>> b) clean()
>> c) is_valid()
>
>> [!example] Group B
>> n) Triggers all validation and returns boolean
>> o) Validates a single field independently
>> p) Validates rules spanning multiple fields
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the ModelForm concept with its purpose.
>> [!example] Group A
>> a) model = Patient
>> b) fields = '__all__'
>> c) read_only_fields
>
>> [!example] Group B
>> n) Marks fields as excluded from write operations
>> o) Includes all model fields (risky in production)
>> p) Associates the form with a specific database model
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the form view phase with its action.
>> [!example] Group A
>> a) GET request
>> b) POST with valid data
>> c) POST fails validation
>
>> [!example] Group B
>> n) Redirect to success URL
>> o) Render blank form
>> p) Render form with errors
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the static file command with its effect.
>> [!example] Group A
>> a) collectstatic
>> b) {% load static %}
>> c) {% static 'css/style.css' %}
>
>> [!example] Group B
>> n) Generates the URL path to a static asset
>> o) Loads the static template tag library
>> p) Copies files from dev directories to STATIC_ROOT
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the security feature with its DTL mechanism.
>> [!example] Group A
>> a) XSS Prevention
>> b) CSRF Protection
>> c) Safe content rendering
>
>> [!example] Group B
>> n) {% csrf_token %} in forms
>> o) |safe filter for trusted HTML
>> p) Automatic HTML escaping of {{ variables }}
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the form lifecycle trap with its solution.
>> [!example] Group A
>> a) Failing to bind data
>> b) Double submission
>> c) Missing cleaned_data
>
>> [!example] Group B
>> n) Use PRG pattern with redirect
>> o) Pass request.POST to form constructor
>> p) Call is_valid() before accessing cleaned_data
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)