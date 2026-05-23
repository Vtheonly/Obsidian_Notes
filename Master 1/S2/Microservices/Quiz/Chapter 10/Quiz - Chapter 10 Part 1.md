---
sources:
  - "[[10.1. Modifying Base Identities The AbstractBaseUser Class]]"
  - "[[10.2. Custom User Models with AbstractBaseUser]]"
  - "[[10.3. BaseUserManager Custom Implementation]]"
  - "[[10.4. Project Integration for Custom User Models]]"
  - "[[10.5. Automated Application Group Syncing]]"
  - "[[10.6. Method-Level Custom View Permissions]]"
  - "[[10.7. DRF Custom BasePermission Implementation]]"
---
> [!question] The `AbstractUser` class provides only bare-minimum authentication requirements without standard fields.
>> [!success]- Answer
>> False

> [!question] The `PermissionsMixin` adds support for Django's built-in group and permission structures.
>> [!success]- Answer
>> True

> [!question] The `REQUIRED_FIELDS` attribute lists fields that the `createsuperuser` command will prompt for.
>> [!success]- Answer
>> True

> [!question] Changing `AUTH_USER_MODEL` mid-project is safe and does not affect relational integrity.
>> [!success]- Answer
>> False

> [!question] The `post_migrate` signal can be used to automate group and permission synchronization.
>> [!success]- Answer
>> True

> [!question] The `get_permission_required()` method allows dynamic permission requirements based on the HTTP method.
>> [!success]- Answer
>> True

> [!question] The `has_permission()` method in DRF's BasePermission runs after view execution.
>> [!success]- Answer
>> False

> [!question] Custom user models should be defined BEFORE running initial database migrations.
>> [!success]- Answer
>> True

> [!question] The `normalize_email()` method in BaseUserManager makes email domains lowercase.
>> [!success]- Answer
>> True

> [!question] The `create_user()` method must be defined manually when using AbstractBaseUser.
>> [!success]- Answer
>> True

> [!question] Which class should you inherit from if you want complete control over the user schema with email-based login?
> a) AbstractUser
> b) AbstractBaseUser
> c) User
> d) BaseUserManager
>> [!success]- Answer
>> b) AbstractBaseUser

> [!question] What does the `USERNAME_FIELD` attribute specify in a custom user model?
> a) The password field
> b) The field used as the login credential
> c) The user's display name
> d) The email field for notifications
>> [!success]- Answer
>> b) The field used as the login credential

> [!question] Why is a custom BaseUserManager needed for email-based user models?
> a) To handle database connections
> b) Because the default manager expects a username field
> c) To manage URL routing
> d) To create database indexes
>> [!success]- Answer
>> b) Because the default manager expects a username field

> [!question] Where should `AUTH_USER_MODEL` be configured in a Django project?
> a) In urls.py
> b) In models.py
> c) In settings.py
> d) In apps.py
>> [!success]- Answer
>> c) In settings.py

> [!question] Which signal is used to trigger automated group synchronization after migrations?
> a) pre_save
> b) post_migrate
> c) pre_migrate
> d) post_save
>> [!success]- Answer
>> b) post_migrate

> [!question] What does the `has_object_permission()` method check in a custom DRF permission class?
> a) The user's authentication status
> b) Permissions at the specific database record level
> c) The view's HTTP method
> d) The request's IP address
>> [!success]- Answer
>> b) Permissions at the specific database record level

> [!question] Which BaseUserManager method is used to create a superuser?
> a) create_user()
> b) create_superuser()
> c) create_admin()
> d) create_staff()
>> [!success]- Answer
>> b) create_superuser()

> [!question] What happens if `AUTH_USER_MODEL` is not set before the first migration?
> a) Django uses the default User model
> b) An error is raised
> c) The migration fails silently
> d) Django guesses the model
>> [!success]- Answer
>> a) Django uses the default User model

> [!question] Where should the automated group sync function be connected in the app lifecycle?
> a) In the models.py file
> b) In the views.py file
> c) In the apps.py ready() method
> d) In the urls.py file
>> [!success]- Answer
>> c) In the apps.py ready() method

> [!question] In a custom DRF permission class, which method checks permissions at the request level before the view is executed?
> a) has_object_permission()
> b) has_permission()
> c) check_permissions()
> d) validate_permissions()
>> [!success]- Answer
>> b) has_permission()

> [!question] Match the user model class with its appropriate use case.
>> [!example] Group A
>> a) AbstractUser
>> b) AbstractBaseUser
>> c) PermissionsMixin
>
>> [!example] Group B
>> n) Complete control over user schema
>> o) Standard fields plus a few custom fields
>> p) Adds group and permission support
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the custom user model attribute with its purpose.
>> [!example] Group A
>> a) USERNAME_FIELD
>> b) REQUIRED_FIELDS
>> c) objects
>
>> [!example] Group B
>> n) Custom BaseUserManager instance
>> o) Fields prompted by createsuperuser
>> p) Login credential field identifier
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the BaseUserManager method with its action.
>> [!example] Group A
>> a) create_user()
>> b) normalize_email()
>> c) set_password()
>
>> [!example] Group B
>> n) Lowercases email domain
>> o) Hashes password securely
>> p) Creates and saves a user
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the RBAC sync concept with its implementation step.
>> [!example] Group A
>> a) Role definition
>> b) Permission assignment
>> c) Group creation
>
>> [!example] Group B
>> n) Group.objects.get_or_create(name=role)
>> o) Dictionary mapping roles to permissions
>> p) group.permissions.add(permission)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the permission method with its scope in DRF.
>> [!example] Group A
>> a) has_permission()
>> b) has_object_permission()
>> c) SAFE_METHODS
>
>> [!example] Group B
>> n) GET, HEAD, OPTIONS
>> o) Request-level check before view runs
>> p) Object-level check on specific record
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the method-level permission component with its role.
>> [!example] Group A
>> a) get_permission_required()
>> b) dispatch()
>> c) has_permission()
>
>> [!example] Group B
>> n) Evaluates permissions before view handler
>> o) Returns different perms per HTTP method
>> p) Inherited from PermissionRequiredMixin
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the permission class attribute with its behavior.
>> [!example] Group A
>> a) raise_exception
>> b) permission_classes
>> c) SAFE_METHODS
>
>> [!example] Group B
>> n) List of permission classes in ViewSet
>> o) Returns HTTP 403 instead of redirect
>> p) Read-only HTTP methods tuple
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the sync event with its trigger.
>> [!example] Group A
>> a) post_migrate signal
>> b) AppConfig.ready()
>> c) Group.get_or_create()
>
>> [!example] Group B
>> n) Creates group if it doesn't exist
>> o) Connects sync function to signal
>> p) Fired after migrations complete
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the custom user model field with its example.
>> [!example] Group A
>> a) Custom identity field
>> b) Role-based field
>> c) Operational flags
>
>> [!example] Group B
>> n) role = CharField(choices=ROLE_CHOICES)
>> o) email = EmailField(unique=True)
>> p) is_active = BooleanField(default=True)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the superuser creation validation with its check.
>> [!example] Group A
>> a) is_staff must be True
>> b) is_superuser must be True
>> c) role must be ADMIN
>
>> [!example] Group B
>> n) Validates superuser permissions level
>> o) Validates admin panel access
>> p) Validates admin role assignment
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)