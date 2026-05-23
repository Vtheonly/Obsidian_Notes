---
sources:
  - "[[08.1. Authentication vs Authorization Core Concepts]]"
  - "[[08.2. Django Contrib Auth Module and Built-In User Model]]"
  - "[[08.3. Credentials Verification and Session Integration]]"
  - "[[08.4. Session Engine Architecture and Cookie Lifetiming]]"
  - "[[08.5. Permissions and Group Management in Django Core]]"
  - "[[08.6. Authentication Status Helpers in View Controllers]]"
---
> [!question] Authentication answers the question "What are you allowed to do?" while Authorization answers "Who are you?"
>> [!success]- Answer
>> False

> [!question] Django automatically hashes passwords using PBKDF2 with a SHA256 hash signature and a cryptographic salt.
>> [!success]- Answer
>> True

> [!question] The `login()` function generates a session on the server and returns a session cookie to the browser.
>> [!success]- Answer
>> True

> [!question] Setting `SESSION_COOKIE_HTTPONLY = True` prevents client-side JavaScript from accessing session cookies.
>> [!success]- Answer
>> True

> [!question] Django automatically creates three standard permissions for every model: add, change, and delete.
>> [!success]- Answer
>> False

> [!question] The `request.user.is_authenticated` property returns True when a user is logged in.
>> [!success]- Answer
>> True

> [!question] When protecting a Class-Based View with mixins, you should list the mixins after the base View class.
>> [!success]- Answer
>> False

> [!question] The `PermissionDenied` exception returns an HTTP 403 Forbidden response.
>> [!success]- Answer
>> True

> [!question] Django's `logout()` function destroys session data on the server and deletes the cookie from the browser.
>> [!success]- Answer
>> True

> [!question] The `USERNAME_FIELD` in a custom user model defines the field used as the login credential.
>> [!success]- Answer
>> True

> [!question] Which HTTP status code indicates an authentication failure in DRF?
> a) 401 Unauthorized
> b) 403 Forbidden
> c) 400 Bad Request
> d) 404 Not Found
>> [!success]- Answer
>> a) 401 Unauthorized

> [!question] Which HTTP status code indicates an authorization failure in DRF?
> a) 401 Unauthorized
> b) 403 Forbidden
> c) 405 Method Not Allowed
> d) 500 Internal Server Error
>> [!success]- Answer
>> b) 403 Forbidden

> [!question] Which method should you use to create a new user with a hashed password?
> a) User.objects.create()
> b) User.objects.create_user()
> c) User.save()
> d) User.objects.create_superuser()
>> [!success]- Answer
>> b) User.objects.create_user()

> [!question] What does the `authenticate()` function return if the credentials are invalid?
> a) False
> b) None
> c) An empty User object
> d) HTTP 401 error
>> [!success]- Answer
>> b) None

> [!question] What is the default value of `SESSION_COOKIE_AGE` in seconds?
> a) 3600 (1 hour)
> b) 86400 (1 day)
> c) 1209600 (2 weeks)
> d) 2592000 (30 days)
>> [!success]- Answer
>> c) 1209600 (2 weeks)

> [!question] How do you check if a user has a specific permission in a Django template?
> a) {% if user.has_perm 'clinical.change_patient' %}
> b) {% if perms.clinical.change_patient %}
> c) {% if user.permissions.clinical.change_patient %}
> d) {% if has_perm clinical.change_patient %}
>> [!success]- Answer
>> b) {% if perms.clinical.change_patient %}

> [!question] Which method is used to verify a user's password and create a session in a single flow?
> a) authenticate() then login()
> b) login() then authenticate()
> c) login() only
> d) authenticate() only
>> [!success]- Answer
>> a) authenticate() then login()

> [!question] What is the correct inheritance order for protecting a CBV with mixins?
> a) class MyView(View, LoginRequiredMixin)
> b) class MyView(LoginRequiredMixin, View)
> c) class MyView(LoginRequiredMixin, PermissionRequiredMixin, View)
> d) Both b and c are correct, but mixins must come before View
>> [!success]- Answer
>> d) Both b and c are correct, but mixins must come before View

> [!question] What does `raise_exception=True` do in a PermissionRequiredMixin?
> a) It logs the error silently
> b) It returns an HTTP 403 Forbidden response
> c) It redirects to the login page
> d) It sends an email alert
>> [!success]- Answer
>> b) It returns an HTTP 403 Forbidden response

> [!question] Which method safely clears the current session dictionary and regenerates a new session key?
> a) request.session.clear()
> b) request.session.flush()
> c) request.session.delete()
> d) request.session.reset()
>> [!success]- Answer
>> b) request.session.flush()

> [!question] Match the security concept with its HTTP status code.
>> [!example] Group A
>> a) Authentication Failure
>> b) Authorization Failure
>> c) Successful Login
>
>> [!example] Group B
>> n) 200 OK
>> o) 403 Forbidden
>> p) 401 Unauthorized
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the Django auth function with its purpose.
>> [!example] Group A
>> a) authenticate()
>> b) login()
>> c) logout()
>
>> [!example] Group B
>> n) Creates a session and returns a cookie
>> o) Verifies username and password
>> p) Destroys session data and deletes cookie
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the User model field with its purpose.
>> [!example] Group A
>> a) is_active
>> b) is_staff
>> c) is_superuser
>
>> [!example] Group B
>> n) Grants all permissions automatically
>> o) Grants admin panel access
>> p) Active status flag for account
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the session setting with its description.
>> [!example] Group A
>> a) SESSION_ENGINE
>> b) SESSION_COOKIE_AGE
>> c) SESSION_EXPIRE_AT_BROWSER_CLOSE
>
>> [!example] Group B
>> n) Session storage backend
>> o) Session validity duration in seconds
>> p) Expire session when browser closes
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the permission concept with its example.
>> [!example] Group A
>> a) Permission codename
>> b) Group
>> c) ContentType
>
>> [!example] Group B
>> n) change_patient
>> o) Maps model to its permissions
>> p) Clinical Editors
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the auth helper with its type.
>> [!example] Group A
>> a) @login_required
>> b) LoginRequiredMixin
>> c) @permission_required
>
>> [!example] Group B
>> n) FBV decorator for permissions
>> o) FBV decorator for login check
>> p) CBV mixin for login check
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the permission check with its context.
>> [!example] Group A
>> a) request.user.has_perm()
>> b) perms.clinical.change_patient
>> c) @permission_required()
>
>> [!example] Group B
>> n) Template permission check
>> o) Python view permission check
>> p) FBV decorator permission check
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the session cookie flag with its security benefit.
>> [!example] Group A
>> a) SESSION_COOKIE_HTTPONLY
>> b) SESSION_COOKIE_SECURE
>> c) SESSION_EXPIRE_AT_BROWSER_CLOSE
>
>> [!example] Group B
>> n) Prevents XSS cookie theft
>> o) Forces HTTPS-only transmission
>> p) Limits session lifetime
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the User status helper with its meaning.
>> [!example] Group A
>> a) is_authenticated
>> b) is_anonymous
>> c) is_active
>
>> [!example] Group B
>> n) Account is enabled and not deactivated
>> o) User is currently logged in
>> p) User is browsing without login
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the auth component with its action.
>> [!example] Group A
>> a) create_user()
>> b) set_password()
>> c) normalize_email()
>
>> [!example] Group B
>> n) Hashes password securely before saving
>> o) Creates user with hashed password
>> p) Lowercases email domain
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)