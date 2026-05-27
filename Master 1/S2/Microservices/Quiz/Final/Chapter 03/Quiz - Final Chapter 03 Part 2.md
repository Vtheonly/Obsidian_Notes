---
sources:
  - "[[Final/Chapter 3]]"
---
> [!question] The AUTH_USER_MODEL setting in settings.py points Django to the custom user model.
>> [!success]- Answer
>> True

> [!question] A custom user model in Django must subclass only the AbstractBaseUser class.
>> [!success]- Answer
>> False

> [!question] The ready() method in apps.py is used to dynamically create user groups on startup.
>> [!success]- Answer
>> True

> [!question] Custom permissions in Django are defined inside the model's inner Meta class.
>> [!success]- Answer
>> True

> [!question] The SESSION_COOKIE_AGE setting defines how long a session lasts in seconds.
>> [!success]- Answer
>> True

> [!question] The PermissionRequiredMixin is used in Function-Based Views to check permissions.
>> [!success]- Answer
>> False

> [!question] The IsAuthenticated permission class in DRF checks if a user is logged in.
>> [!success]- Answer
>> True

> [!question] A custom permission class in DRF must override the has_permission() method.
>> [!success]- Answer
>> True

> [!question] The @permission_required decorator raises a 500 error when permission is denied by default.
>> [!success]- Answer
>> False

> [!question] Access tokens should be stored in the client-side session when using server-side rendering.
>> [!success]- Answer
>> True

> [!question] Which command creates a superuser after a custom user model migration?
> a) python manage.py createsuperuser
> b) python manage.py createsuperuser --email admin@example.com
> c) python manage.py createadmin
> d) python manage.py makemigrations --superuser
>> [!success]- Answer
>> a) python manage.py createsuperuser

> [!question] What does the get_or_create() method do in Django ORM?
> a) Creates a record if it does not exist, or retrieves it
> b) Gets a record and deletes it
> c) Creates a record and immediately deletes it
> d) Gets all records and creates a backup
>> [!success]- Answer
>> a) Creates a record if it does not exist, or retrieves it

> [!question] What is the purpose of the raise_exception parameter in @permission_required?
> a) To return a 404 error when permission is denied
> b) To raise an exception and return a 403 Forbidden response
> c) To log the permission check
> d) To automatically grant the permission
>> [!success]- Answer
>> b) To raise an exception and return a 403 Forbidden response

> [!question] What is the correct way to assign a permission to a group programmatically?
> a) group.user_permissions.add(permission)
> b) group.permissions.add(permission)
> c) group.add_permission(permission)
> d) permission.assign_to(group)
>> [!success]- Answer
>> b) group.permissions.add(permission)

> [!question] Which view mixin is used for class-based permission checking in Django?
> a) LoginRequiredMixin
> b) PermissionRequiredMixin
> c) UserPassesTestMixin
> d) AccessMixin
>> [!success]- Answer
>> b) PermissionRequiredMixin

> [!question] What does the SAFE_METHODS constant contain in DRF permissions?
> a) POST, PUT, PATCH
> b) GET, HEAD, OPTIONS
> c) GET, POST, PUT
> d) DELETE, UPDATE, PATCH
>> [!success]- Answer
>> b) GET, HEAD, OPTIONS

> [!question] Which database engine stores Django sessions when using SESSION_ENGINE = 'db'?
> a) Redis
> b) Database
> c) File
> d) Cache
>> [!success]- Answer
>> b) Database

> [!question] What is the correct import for creating a custom permission class in DRF?
> a) from django.contrib.auth import permissions
> b) from rest_framework import permissions
> c) from django.conf import permissions
> d) from myapp import permissions
>> [!success]- Answer
>> b) from rest_framework import permissions

> [!question] What does the normalize_email() method do in a custom user manager?
> a) Converts email to lowercase
> b) Validates email format
> c) Checks if email exists in database
> d) Sends a verification email
>> [!success]- Answer
>> a) Converts email to lowercase

> [!question] Which field is used to link the custom user manager to the model in Django?
> a) manager = CompteManager()
> b) objects = CompteManager()
> c) users = CompteManager()
> d) admin = CompteManager()
>> [!success]- Answer
>> b) objects = CompteManager()

> [!question] Match the permission check method with the correct code.
>> [!example] Group A
>> a) @permission_required
>> b) PermissionRequiredMixin
>> c) has_perm in template
>
>> [!example] Group B
>> n) {% if user.has_perm 'myapp.can_publish' %}
>> o) permission_required = 'myapp.can_publish'
>> p) @permission_required('myapp.can_publish')
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the custom user model attribute with its purpose.
>> [!example] Group A
>> a) USERNAME_FIELD
>> b) REQUIRED_FIELDS
>> c) is_staff
>
>> [!example] Group B
>> n) List of fields prompted when creating a superuser
>> o) Specifies the unique login identifier
>> p) Indicates if the user can access the admin site
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the migration command with its action.
>> [!example] Group A
>> a) makemigrations
>> b) migrate
>> c) createsuperuser
>
>> [!example] Group B
>> n) Applies migration files to the database
>> o) Scans models and creates migration files
>> p) Creates an admin user in the database
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the permission assignment scope with the code.
>> [!example] Group A
>> a) Assign to user
>> b) Assign to group
>> c) Define in Meta class
>
>> [!example] Group B
>> n) class Meta: permissions = []
>> o) user.user_permissions.add(permission)
>> p) group.permissions.add(permission)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the DRF permission class with its behavior.
>> [!example] Group A
>> a) IsAuthenticated
>> b) IsAdminUser
>> c) AllowAny
>
>> [!example] Group B
>> n) Grants access to any user without authentication
>> o) Requires the user to be logged in
>> p) Requires the user to have staff status
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the HTTP method with the required permission in the custom permission class.
>> [!example] Group A
>> a) GET, HEAD, OPTIONS
>> b) POST
>> c) PUT, PATCH
>
>> [!example] Group B
>> n) Requires add permission
>> o) Requires view permission
>> p) Requires change permission
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the JWT configuration with its purpose.
>> [!example] Group A
>> a) DEFAULT_AUTHENTICATION_CLASSES
>> b) permission_classes
>> c) SIMPLE_JWT settings
>
>> [!example] Group B
>> n) Configures token lifetimes and rotation
>> o) Sets JWT as the default authentication backend
>> p) Defines which permission checks apply to a view
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the exception handling with the correct response status.
>> [!example] Group A
>> a) OperationalError
>> b) DoesNotExist
>> c) ValidationError
>
>> [!example] Group B
>> n) 404 Not Found
>> o) 400 Bad Request
>> p) Database not initialized error
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the token storage method with the code.
>> [!example] Group A
>> a) Store access token
>> b) Attach token to header
>> c) Refresh access token
>
>> [!example] Group B
>> n) request.session['access_token'] = token
>> o) requests.get(url, headers=headers)
>> p) requests.post('/api/token/refresh/', data={'refresh': refresh})
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the group naming with the role it represents.
>> [!example] Group A
>> a) ADMIN
>> b) EDITOR
>> c) VIEWER
>
>> [!example] Group B
>> n) Can create and modify content
>> o) Full system access
>> p) Read-only access
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)