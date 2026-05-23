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
> [!question] The `AbstractBaseUser` provides password hashing, password reset helpers, and login tracking.
>> [!success]- Answer
>> True

> [!question] The `REQUIRED_FIELDS` list should include the `USERNAME_FIELD` and `password` fields.
>> [!success]- Answer
>> False

> [!question] A custom `BaseUserManager` must define both `create_user()` and `create_superuser()` methods.
>> [!success]- Answer
>> True

> [!question] The `AUTH_USER_MODEL` setting uses the format `<app_name>.<model_class_name>`.
>> [!success]- Answer
>> True

> [!question] The `synchronize_system_roles` function should be called manually after every deployment.
>> [!success]- Answer
>> False

> [!question] The `dispatch()` method can be overridden to evaluate permissions before executing the view handler.
>> [!success]- Answer
>> True

> [!question] DRF evaluates permission classes in the order they are listed, blocking immediately if any returns False.
>> [!success]- Answer
>> True

> [!question] The `AbstractUser` class inherits all standard fields from the default User model including username, first name, and last name.
>> [!success]- Answer
>> True

> [!question] The `get_queryset()` method in a custom manager uses `self._db` to specify which database to use for saving.
>> [!success]- Answer
>> True

> [!question] The `create_superuser()` method sets default values like `is_staff=True` and `is_superuser=True`.
>> [!success]- Answer
>> True

> [!question] Which fields are automatically set by `create_superuser()` when they are not provided?
> a) is_active, is_staff, is_superuser
> b) username, email, password
> c) date_joined, last_login, email
> d) first_name, last_name, role
>> [!success]- Answer
>> a) is_active, is_staff, is_superuser

> [!question] What validation error should be raised if `email` is missing in `create_user()`?
> a) TypeError
> b) ValueError("The Email field must be specified.")
> c) ValidationError
> d) PermissionDenied
>> [!success]- Answer
>> b) ValueError("The Email field must be specified.")

> [!question] What is the first step when configuring a custom user model for a new project?
> a) Run migrations
> b) Create the custom user model class
> c) Set AUTH_USER_MODEL in settings.py
> d) Create a superuser
>> [!success]- Answer
>> c) Set AUTH_USER_MODEL in settings.py

> [!question] What does `extra_fields.setdefault('is_staff', True)` do in `create_superuser()`?
> a) It sets is_staff to True only if it hasn't been set already
> b) It overwrites is_staff regardless of existing value
> c) It throws an error if is_staff is False
> d) It removes the is_staff field
>> [!success]- Answer
>> a) It sets is_staff to True only if it hasn't been set already

> [!question] What happens if `is_staff` is not True when creating a superuser?
> a) The superuser is created anyway
> b) A ValueError is raised
> c) is_staff is automatically set to True
> d) The user is created as a regular user
>> [!success]- Answer
>> b) A ValueError is raised

> [!question] In the role-based sync pattern, what does the dictionary `role_permissions` map?
> a) User IDs to permissions
> b) Role names to lists of permission codenames
> c) Groups to users
> d) Models to content types
>> [!success]- Answer
>> b) Role names to lists of permission codenames

> [!question] Which method in a CBV is overridden to return different permissions per HTTP method?
> a) get_queryset()
> b) get_permission_required()
> c) dispatch()
> d) has_permission()
>> [!success]- Answer
>> b) get_permission_required()

> [!question] In a custom DRF BasePermission, what does `request.method in permissions.SAFE_METHODS` check?
> a) If the request method is POST, PUT, or DELETE
> b) If the request method is GET, HEAD, or OPTIONS
> c) If the request is secure (HTTPS)
> d) If the request contains sensitive data
>> [!success]- Answer
>> b) If the request method is GET, HEAD, or OPTIONS

> [!question] What does `self.has_permission()` return in a CBV's dispatch method?
> a) The permission required for the view
> b) Whether the user has the required permissions
> c) The user's role
> d) The list of permissions
>> [!success]- Answer
>> b) Whether the user has the required permissions

> [!question] What is the correct format for the `AUTH_USER_MODEL` setting?
> a) clinical.Compte
> b) clinical.models.Compte
> c) Compte (clinical)
> d) clinical.CompteModel
>> [!success]- Answer
>> a) clinical.Compte

> [!question] Match the authentication base class with its inheritance.
>> [!example] Group A
>> a) AbstractBaseUser
>> b) AbstractUser
>> c) PermissionsMixin
>
>> [!example] Group B
>> n) Adds group and permission functionality
>> o) Password hashing and login tracking only
>> p) Standard User fields plus custom extensions
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the custom model configuration step with its timing.
>> [!example] Group A
>> a) Set AUTH_USER_MODEL
>> b) Create custom model class
>> c) Run migrations
>
>> [!example] Group B
>> n) Before migrations
>> o) After AUTH_USER_MODEL is set
>> p) After creating model class
>
>> [!success]- Answer
>> a) -> n)
>> b) -> n)
>> c) -> p)

> [!question] Match the manager validation with its condition.
>> [!example] Group A
>> a) email must exist
>> b) is_staff must be True for superuser
>> c) is_superuser must be True
>
>> [!example] Group B
>> n) Raises ValueError in create_user
>> o) Raises ValueError in create_superuser
>> p) Validates permissions level in create_superuser
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the DRF BasePermission method with its argument.
>> [!example] Group A
>> a) has_permission(self, request, view)
>> b) has_object_permission(self, request, view, obj)
>> c) SAFE_METHODS
>
>> [!example] Group B
>> n) (GET, HEAD, OPTIONS)
>> o) Checks permission using request and view
>> p) Checks permission using the target record
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the permission role with its allowed operations.
>> [!example] Group A
>> a) ADMIN
>> b) EDITOR
>> c) VIEWER
>
>> [!example] Group B
>> n) add, change, view permissions
>> o) view permission only
>> p) add, change, delete, view permissions
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the method-level permission with its HTTP method restriction.
>> [!example] Group A
>> a) GET requires view permission
>> b) POST requires add permission
>> c) DELETE requires delete permission
>
>> [!example] Group B
>> n) ('clinical.delete_patient',)
>> o) ('clinical.add_patient',)
>> p) ('clinical.view_patient',)
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the DRF permission attribute with its ViewSet usage.
>> [!example] Group A
>> a) permission_classes
>> b) IsEditorOrAdminOnly
>> c) IsPatientOwnerOrStaff
>
>> [!example] Group B
>> n) Custom permission class for object-level check
>> o) [IsEditorOrAdminOnly, IsPatientOwnerOrStaff]
>> p) Custom permission class for write access control
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the sync component with its code implementation.
>> [!example] Group A
>> a) post_migrate.connect()
>> b) ContentType.objects.get_for_model()
>> c) get_or_create(name=role)
>
>> [!example] Group B
>> n) Retrieves content type for Permission lookup
>> o) Connects sync to migration signal
>> p) Creates group if it doesn't exist
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the permission check scenario with its appropriate method.
>> [!example] Group A
>> a) Allow all authenticated users read access
>> b) Restrict write to editors only
>> c) Allow only record owner access
>
>> [!example] Group B
>> n) has_object_permission for specific records
>> o) has_permission checking SAFE_METHODS
>> p) has_permission checking user role
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the BaseUserManager helper with its function.
>> [!example] Group A
>> a) self.model()
>> b) user.set_password()
>> c) user.save(using=self._db)
>
>> [!example] Group B
>> n) Saves to the correct database
>> o) Instantiates the custom user model
>> p) Hashes the password string
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)