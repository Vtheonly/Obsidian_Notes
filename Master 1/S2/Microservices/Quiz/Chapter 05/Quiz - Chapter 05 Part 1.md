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
> [!question] Django variables in templates use `{{ variable }}` syntax to output values from the context dictionary.
>> [!success]- Answer
>> True

> [!question] The `{% extends %}` tag should appear anywhere in the child template file.
>> [!success]- Answer
>> False

> [!question] The `collectstatic` command copies all static files into the directory defined by STATIC_ROOT.
>> [!success]- Answer
>> True

> [!question] HTML5 semantic elements include `<header>`, `<nav>`, `<main>`, and `<footer>`.
>> [!success]- Answer
>> True

> [!question] The `cleaned_data` attribute is available on a form instance before calling `is_valid()`.
>> [!success]- Answer
>> False

> [!question] A `ModelForm` automatically generates HTML form fields based on the model's fields and validates them.
>> [!success]- Answer
>> True

> [!question] The `form.as_p` rendering style wraps form fields in `<table>` elements.
>> [!success]- Answer
>> False

> [!question] The Post-Redirect-Get (PRG) pattern prevents duplicate form submissions when the user refreshes the page.
>> [!success]- Answer
>> True

> [!question] The `safe` filter in Django templates should be used on all user-submitted input to preserve formatting.
>> [!success]- Answer
>> False

> [!question] A child template overrides parent blocks using the `{% block %}` tag with the same name.
>> [!success]- Answer
>> True

> [!question] Which DTL syntax is used for control flow logic like loops and conditions?
> a) {{ variable }}
> b) {% tag %}
> c) {{ var|filter }}
> d) {# comment #}
>> [!success]- Answer
>> b) {% tag %}

> [!question] What is the purpose of the `{% extends %}` tag in Django templates?
> a) To include a reusable HTML fragment
> b) To declare inheritance from a parent template
> c) To extend the URL configuration
> d) To add CSS class extensions
>> [!success]- Answer
>> b) To declare inheritance from a parent template

> [!question] Which command collects all static files into a single directory for production deployment?
> a) python manage.py staticfiles
> b) python manage.py collectstatic
> c) python manage.py buildstatic
> d) python manage.py deploystatic
>> [!success]- Answer
>> b) python manage.py collectstatic

> [!question] What is the correct setting for serving static files in production using a dedicated server?
> a) STATIC_URL
> b) STATIC_ROOT
> c) STATICFILES_DIRS
> d) STATIC_SERVE
>> [!success]- Answer
>> b) STATIC_ROOT

> [!question] In Django forms, what is `clean()` used for?
> a) To validate a single field independently
> b) To validate rules that span multiple fields
> c) To sanitize HTML input
> d) To clear the form data
>> [!success]- Answer
>> b) To validate rules that span multiple fields

> [!question] What does calling `form.save(commit=False)` do in a ModelForm?
> a) It validates the form without saving
> b) It creates a model instance in memory without writing to the database
> c) It cancels the save operation
> d) It saves only the first field
>> [!success]- Answer
>> b) It creates a model instance in memory without writing to the database

> [!question] Which attribute provides sanitized input data after calling `is_valid()`?
> a) form.data
> b) form.cleaned_data
> c) form.valid_data
> d) form.sanitized_data
>> [!success]- Answer
>> b) form.cleaned_data

> [!question] What is the purpose of the `{% csrf_token %}` tag in Django forms?
> a) To validate form field lengths
> b) To enforce Cross-Site Request Forgery protection
> c) To generate session tokens
> d) To encrypt form submissions
>> [!success]- Answer
>> b) To enforce Cross-Site Request Forgery protection

> [!question] In the PRG pattern, what should a successful POST request return?
> a) A render() of the success page
> b) An HTTP 302 redirect
> c) A JsonResponse
> d) An HTTP 200 with the form page
>> [!success]- Answer
>> b) An HTTP 302 redirect

> [!question] Which method must you call if your ModelForm has many-to-many fields and you used `commit=False`?
> a) form.save()
> b) form.save_m2m()
> c) form.save_m2m_fields()
> d) form.commit_m2m()
>> [!success]- Answer
>> b) form.save_m2m()

> [!question] Match the DTL syntax type with its purpose.
>> [!example] Group A
>> a) {{ variable }}
>> b) {% tag %}
>> c) {{ var|filter }}
>
>> [!example] Group B
>> n) Modifies how variables are displayed
>> o) Outputs values from the context dictionary
>> p) Handles control flow logic
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the template inheritance component with its role.
>> [!example] Group A
>> a) {% extends %}
>> b) {% block %}
>> c) {% include %}
>
>> [!example] Group B
>> n) Embeds reusable HTML fragments
>> o) Marks modifiable regions in parent templates
>> p) Inherits from a parent template layout
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the static file configuration with its purpose.
>> [!example] Group A
>> a) STATIC_URL
>> b) STATICFILES_DIRS
>> c) STATIC_ROOT
>
>> [!example] Group B
>> n) Local directories for raw assets during development
>> o) Public URL path for browser access
>> p) Production folder path for collected files
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the HTML5 semantic element with its usage.
>> [!example] Group A
>> a) <header>
>> b) <nav>
>> c) <main>
>
>> [!example] Group B
>> n) Primary navigation links
>> o) Core dynamic content body
>> p) Site branding and identity
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the form validation concept with its description.
>> [!example] Group A
>> a) Field-Level Validation
>> b) Form-Level Validation
>> c) cleaned_data
>
>> [!example] Group B
>> n) Sanitized data available after is_valid()
>> o) clean() method for cross-field rules
>> p) clean_<fieldname>() for single field rules
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the ModelForm component with its role.
>> [!example] Group A
>> a) class Meta
>> b) fields list
>> c) save(commit=False)
>
>> [!example] Group B
>> n) Prevents DB write for additional modifications
>> o) Specifies which model fields to include
>> p) Nested configuration class inside ModelForm
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the form rendering style with its HTML element.
>> [!example] Group A
>> a) form.as_p
>> b) form.as_table
>> c) form.as_ul
>
>> [!example] Group B
>> n) <li> elements
>> o) <tr> elements
>> p) <p> elements
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the PRG lifecycle step with its action.
>> [!example] Group A
>> a) GET request
>> b) POST with invalid data
>> c) POST with valid data
>
>> [!example] Group B
>> n) HTTP 302 redirect to success page
>> o) Re-render form with error messages
>> p) Render empty form for user input
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the DTL filter with its effect.
>> [!example] Group A
>> a) |upper
>> b) |truncatechars:50
>> c) |default:"text"
>
>> [!example] Group B
>> n) Limits characters displayed
>> o) Converts text to uppercase
>> p) Provides fallback value if empty
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the form security concept with its protection.
>> [!example] Group A
>> a) Auto HTML Escaping
>> b) CSRF Token
>> c) safe filter
>
>> [!example] Group B
>> n) Renders raw HTML (use with caution)
>> o) Prevents Cross-Site Scripting (XSS)
>> p) Prevents Cross-Site Request Forgery
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)