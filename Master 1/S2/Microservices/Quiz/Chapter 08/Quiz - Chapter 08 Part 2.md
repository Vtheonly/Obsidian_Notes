---
sources:
  - "[[08.1. Authentication vs Authorization Core Concepts]]"
  - "[[08.2. Django Contrib Auth Module and Built-In User Model]]"
  - "[[08.3. Credentials Verification and Session Integration]]"
  - "[[08.4. Session Engine Architecture and Cookie Lifetiming]]"
  - "[[08.5. Permissions and Group Management in Django Core]]"
  - "[[08.6. Authentication Status Helpers in View Controllers]]"
---
> [!question] HTTP is a stateless protocol, meaning each request is treated as completely independent.
>> [!success]- Answer
>> True

> [!question] The `sessionid` cookie is encrypted, making it impossible for the client to read or modify its contents.
>> [!success]- Answer
>> False

> [!question] Django automatically creates four standard permissions for every model: add, change, delete, and view.
>> [!success]- Answer
>> True

> [!question] The `redirect_field_name` attribute in LoginRequiredMixin specifies the URL parameter name for the redirect path.
>> [!success]- Answer
>> True

> [!question] Using `User.objects.create(username="john", password="my_password")` correctly hashes the password before saving.
>> [!success]- Answer
>> False

> [!question] Authorization always happens before authentication in the security flow.
>> [!success]- Answer
>> False

> [!question] Permissions in Django use the format `<app_label>.<codename>_<model_name>`.
>> [!success]- Answer
>> True

> [!question] Session-based login uses a two-step process of credential verification followed by session integration.
>> [!success]- Answer
>> True

> [!question] Default `User` model's `email` field is unique by default.
>> [!success]- Answer
>> False

> [!question] The `@login_required` decorator can take a `login_url` parameter to specify the login page URL.
>> [!success]- Answer
>> True

> [!question] What is the difference between authentication and authorization?
> a) They are the same concept
> b) Authentication verifies identity; authorization verifies permissions
> c) Authorization verifies identity; authentication verifies permissions
> d) Both happen simultaneously
>> [!success]- Answer
>> b) Authentication verifies identity; authorization verifies permissions

> [!question] What happens when a user with `is_active=False` tries to log in?
> a) They are logged in normally
> b) The login succeeds but they see a warning
> c) The login should be rejected by checking is_active after authenticate()
> d) The account is automatically deleted
>> [!success]- Answer
>> c) The login should be rejected by checking is_active after authenticate()

> [!question] How does a session work in Django?
> a) The server stores user data in a cookie on the browser
> b) Django creates a session in its backend and returns a signed sessionid cookie
> c) Sessions are not supported in Django
> d) The client stores all session data
>> [!success]- Answer
>> b) Django creates a session in its backend and returns a signed sessionid cookie

> [!question] What is the purpose of the `ContentType` model in Django's permission system?
> a) It stores the actual permission data
> b) It maps each model to its associated permissions
> c) It defines user roles
> d) It stores group membership
>> [!success]- Answer
>> b) It maps each model to its associated permissions

> [!question] Which view decorator should you use to protect a Function-Based View that requires a user to be logged in?
> a) @user_passes_test
> b) @login_required
> c) @permission_required
> d) @staff_member_required
>> [!success]- Answer
>> b) @login_required

> [!question] What happens when `request.session.flush()` is called?
> a) Only the session cookie is deleted
> b) The session dictionary is cleared and a new session key is generated
> c) The user is logged out
> d) The database session table is truncated
>> [!success]- Answer
>> b) The session dictionary is cleared and a new session key is generated

> [!question] How do you assign a user to a permission group programmatically?
> a) user.set_group(editors_group)
> b) user.groups.add(editors_group)
> c) Group.objects.add_user(user)
> d) user.add_group('Clinical Editors')
>> [!success]- Answer
>> b) user.groups.add(editors_group)

> [!question] What is the correct way to create a group and assign permissions?
> a) Create the group, then assign permissions using group.permissions.add()
> b) Create permissions first, then create the group
> c) Groups and permissions are created automatically
> d) You can only use the admin panel
>> [!success]- Answer
>> a) Create the group, then assign permissions using group.permissions.add()

> [!question] For REST APIs, what should you set `raise_exception` to in PermissionRequiredMixin?
> a) False
> b) True
> c) It doesn't matter
> d) raise_exception is not supported
>> [!success]- Answer
>> b) True

> [!question] In a CBV, what happens if mixins are listed in the wrong inheritance order?
> a) The view works normally
> b) The mixin security checks may be bypassed
> c) Django raises a syntax error
> d) The mixins are automatically reordered
>> [!success]- Answer
>> b) The mixin security checks may be bypassed

> [!question] Match the security flow step with its description.
>> [!example] Group A
>> a) Authentication
>> b) Authorization
>> c) Session Creation
>
>> [!example] Group B
>> n) Checking if user can edit a record
>> o) Creating a session and returning a cookie
>> p) Verifying username and password
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the password concept with its correct implementation.
>> [!example] Group A
>> a) Plain text storage
>> b) Hashed storage
>> c) create_user() method
>
>> [!example] Group B
>> n) PBKDF2 with SHA256
>> o) Correct user creation approach
>> p) Critical security vulnerability
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the User field with its data type.
>> [!example] Group A
>> a) username
>> b) password
>> c) is_superuser
>
>> [!example] Group B
>> n) BooleanField
>> o) CharField
>> p) Hashed string stored in CharField
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the session security setting with its effect.
>> [!example] Group A
>> a) SESSION_COOKIE_HTTPONLY
>> b) SESSION_COOKIE_SECURE
>> c) SESSION_COOKIE_SAMESITE
>
>> [!example] Group B
>> n) Prevents CSRF-based session attacks
>> o) Prevents XSS cookie theft
>> p) Forces HTTPS-only transmission
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the permission type with its description.
>> [!example] Group A
>> a) add_patient
>> b) change_patient
>> c) view_patient
>
>> [!example] Group B
>> n) Permission to modify records
>> o) Permission to read records
>> p) Permission to create records
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the authentication helper with its CBV equivalent.
>> [!example] Group A
>> a) @login_required
>> b) @permission_required
>> c) @user_passes_test
>
>> [!example] Group B
>> n) UserPassesTestMixin
>> o) LoginRequiredMixin
>> p) PermissionRequiredMixin
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the auth action with its method.
>> [!example] Group A
>> a) Login
>> b) Logout
>> c) Verify credentials
>
>> [!example] Group B
>> n) authenticate()
>> o) login() + session creation
>> p) logout() + session flush
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the user status with the HTTP response implication.
>> [!example] Group A
>> a) Inactive user login
>> b) Anonymous user
>> c) Authenticated user
>
>> [!example] Group B
>> n) request.user.is_authenticated = False
>> o) Should return HTTP 403 after authenticate()
>> p) request.user.is_authenticated = True
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the RBAC component with its role.
>> [!example] Group A
>> a) Permission
>> b) Group
>> c) User
>
>> [!example] Group B
>> n) Assigned to Groups which are assigned to Users
>> o) Receives permissions through group membership
>> p) Collection of permissions representing a role
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the authentication flow step with its code.
>> [!example] Group A
>> a) Password hashing
>> b) Credential verification
>> c) Session creation
>
>> [!example] Group B
>> n) User.objects.create_user()
>> o) login(request, user)
>> p) authenticate(request, username, password)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)