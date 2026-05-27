---
sources:
  - "[[Final/Chapter 3]]"
---
> [!question] Authentication confirms who the user is, while authorization determines what they can do.
>> [!success]- Answer
>> True

> [!question] Django's default authentication system uses a stateless token-based approach.
>> [!success]- Answer
>> False

> [!question] Every Django model automatically generates add, change, delete, and view permissions.
>> [!success]- Answer
>> True

> [!question] Session-based authentication stores user data on the client side only.
>> [!success]- Answer
>> False

> [!question] JWT tokens are self-contained and contain signed payload data like user ID and expiration.
>> [!success]- Answer
>> True

> [!question] The standard Django User model uses email as the primary identifier by default.
>> [!success]- Answer
>> False

> [!question] Access tokens in JWT architecture are typically long-lived compared to refresh tokens.
>> [!success]- Answer
>> False

> [!question] A 401 Unauthorized status means the user failed authentication.
>> [!success]- Answer
>> True

> [!question] A 403 Forbidden status means the user failed authentication.
>> [!success]- Answer
>> False

> [!question] JWT authentication is suitable for microservices and Single Page Applications.
>> [!success]- Answer
>> True

> [!question] What is the primary purpose of authorization in system security?
> a) To verify the user's identity
> b) To determine what an authenticated user is allowed to do
> c) To encrypt user passwords
> d) To create user accounts
>> [!success]- Answer
>> b) To determine what an authenticated user is allowed to do

> [!question] Which of the following is NOT a default permission generated for Django models?
> a) add_modelname
> b) change_modelname
> c) publish_modelname
> d) view_modelname
>> [!success]- Answer
>> c) publish_modelname

> [!question] What is a key characteristic of JWT authentication?
> a) Requires server-side session storage
> b) Stateless and self-contained tokens
> c) Uses cookies for session tracking
> d) Only works with monolithic applications
>> [!success]- Answer
>> b) Stateless and self-contained tokens

> [!question] Why is a custom user model recommended over the default Django User model?
> a) It is faster to query
> b) It allows email as primary identifier and custom roles
> c) It requires less code to implement
> d) It automatically creates API endpoints
>> [!success]- Answer
>> b) It allows email as primary identifier and custom roles

> [!question] Which status code indicates a user is authenticated but lacks permission for an action?
> a) 200 OK
> b) 401 Unauthorized
> c) 403 Forbidden
> d) 404 Not Found
>> [!success]- Answer
>> c) 403 Forbidden

> [!question] What does the ROTATE_REFRESH_TOKENS setting in SimpleJWT do?
> a) Keeps refresh tokens valid forever
> b) Issues a new refresh token each time one is used
> c) Rotates access tokens every minute
> d) Disables refresh tokens completely
>> [!success]- Answer
>> b) Issues a new refresh token each time one is used

> [!question] What is the default lifetime of an access token in SimpleJWT?
> a) 5 minutes
> b) 15 minutes
> c) 1 hour
> d) 1 day
>> [!success]- Answer
>> b) 15 minutes

> [!question] Which method should a custom user manager implement to create superusers?
> a) create_user()
> b) create_superuser()
> c) create_admin()
> d) create_staff()
>> [!success]- Answer
>> b) create_superuser()

> [!question] What is the USERNAME_FIELD used for in a custom Django user model?
> a) To specify the field used for login
> b) To define the password field
> c) To set the database table name
> d) To configure the admin display name
>> [!success]- Answer
>> a) To specify the field used for login

> [!question] Which HTTP endpoint is used to refresh an expired JWT access token?
> a) /api/token/
> b) /api/token/refresh/
> c) /api/token/verify/
> d) /api/token/renew/
>> [!success]- Answer
>> b) /api/token/refresh/

> [!question] Match the security concept with its definition.
>> [!example] Group A
>> a) Authentication
>> b) Authorization
>
>> [!example] Group B
>> n) Determines what a user can do
>> o) Confirms who a user is
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the HTTP status code with its meaning.
>> [!example] Group A
>> a) 401 Unauthorized
>> b) 403 Forbidden
>
>> [!example] Group B
>> n) User lacks permission for the action
>> o) User failed identity verification
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the token type with its lifetime characteristic.
>> [!example] Group A
>> a) Access Token
>> b) Refresh Token
>
>> [!example] Group B
>> n) Long-lived (e.g., 7 days)
>> o) Short-lived (e.g., 15 minutes)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the authentication strategy with its characteristic.
>> [!example] Group A
>> a) Session-Based
>> b) JWT Token-Based
>
>> [!example] Group B
>> n) Stateless and self-contained tokens
>> o) Stateful with server-side session storage
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the default Django permission with its prefix.
>> [!example] Group A
>> a) add_modelname
>> b) change_modelname
>> c) delete_modelname
>
>> [!example] Group B
>> n) Permission to modify a record
>> o) Permission to create a new record
>> p) Permission to remove a record
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the custom user model class with its purpose.
>> [!example] Group A
>> a) AbstractBaseUser
>> b) BaseUserManager
>> c) PermissionsMixin
>
>> [!example] Group B
>> n) Provides permission-related fields and methods
>> o) Provides the core user model implementation
>> p) Provides methods to create users and superusers
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the SimpleJWT setting with its description.
>> [!example] Group A
>> a) ACCESS_TOKEN_LIFETIME
>> b) REFRESH_TOKEN_LIFETIME
>> c) BLACKLIST_AFTER_ROTATION
>
>> [!example] Group B
>> n) Invalidates old refresh tokens after rotation
>> o) Duration of the short-term access token
>> p) Duration of the long-term refresh token
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the authentication flow step with its action.
>> [!example] Group A
>> a) POST /api/token/
>> b) Bearer token in header
>> c) POST /api/token/refresh/
>
>> [!example] Group B
>> n) Request new access token using refresh token
>> o) Send credentials to obtain tokens
>> p) Attach access token to protected requests
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the user role with its typical permission level.
>> [!example] Group A
>> a) Admin
>> b) Editor
>> c) Viewer
>
>> [!example] Group B
>> n) Read-only access
>> o) Can create and modify content
>> p) Full system access including user management
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the permission check method with its level.
>> [!example] Group A
>> a) Template-Level
>> b) Function-Based View
>> c) Class-Based View
>
>> [!example] Group B
>> n) PermissionRequiredMixin
>> o) user.has_perm in HTML templates
>> p) @permission_required decorator
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)