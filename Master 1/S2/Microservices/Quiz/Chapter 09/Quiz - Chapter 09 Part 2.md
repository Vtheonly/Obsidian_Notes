---
sources:
  - "[[09.1. JSON Web Token Architecture and Authentication Flow]]"
  - "[[09.2. SimpleJWT Installation and Project Configurations]]"
  - "[[09.3. SimpleJWT Token Validation Settings]]"
  - "[[09.4. SimpleJWT Root Routing Views and Endpoints]]"
  - "[[09.5. Programmatic Client Integrations with JWTs]]"
  - "[[09.6. Session-Based Persistent Storage of JWT Tokens]]"
  - "[[09.7. Dynamic Access Token Renewal Pipelines]]"
---
> [!question] In distributed microservice architectures, stateful session synchronization creates bottlenecks and single points of failure.
>> [!success]- Answer
>> True

> [!question] The Base64URL encoding used in JWT is a reversible formatting step, not encryption.
>> [!success]- Answer
>> True

> [!question] The `AUTH_HEADER_TYPES` setting in SIMPLE_JWT configures which token prefix is accepted in the Authorization header.
>> [!success]- Answer
>> True

> [!question] In a hybrid architecture, the frontend server can automatically attach stored JWT tokens to requests proxied to downstream microservices.
>> [!success]- Answer
>> True

> [!question] Access tokens can be easily revoked before they expire, so a short lifetime is not necessary.
>> [!success]- Answer
>> False

> [!question] If an attacker attempts to reuse a blacklisted refresh token, the server can detect the reuse and revoke all associated tokens.
>> [!success]- Answer
>> True

> [!question] The `JWTAuthentication` class should be set as the primary authentication mechanism for DRF when using SimpleJWT.
>> [!success]- Answer
>> True

> [!question] PEM-encoded public keys are needed for RS256 asymmetric signing verification.
>> [!success]- Answer
>> True

> [!question] You should never store sensitive data like passwords or credit card numbers inside a JWT payload.
>> [!success]- Answer
>> True

> [!question] The `TokenBlacklistView` requires the `token_blacklist` app to be migrated before use.
>> [!success]- Answer
>> True

> [!question] What claim type includes standard pre-defined claims like `iss`, `exp`, and `sub`?
> a) Registered Claims
> b) Public Claims
> c) Private Claims
> d) Signature Claims
>> [!success]- Answer
>> a) Registered Claims

> [!question] What is the purpose of `BLACKLIST_AFTER_ROTATION` in SimpleJWT?
> a) It immediately invalidates old refresh tokens when new ones are issued
> b) It blocks all token requests
> c) It blacklists the user account after failed attempts
> d) It clears the token database
>> [!success]- Answer
>> a) It immediately invalidates old refresh tokens when new ones are issued

> [!question] Which HTTP header is used to send a JWT token from the client?
> a) Authentication: Bearer <token>
> b) Authorization: Bearer <token>
> c) X-Auth-Token: <token>
> d) Token: <token>
>> [!success]- Answer
>> b) Authorization: Bearer <token>

> [!question] In the `AuthorizedAPIClient` pattern, what triggers the automatic token renewal?
> a) A timer in the client
> b) An HTTP 401 response from the API
> c) The token's expiration claim
> d) A server-sent event
>> [!success]- Answer
>> b) An HTTP 401 response from the API

> [!question] What is the recommended refresh token lifetime in SimpleJWT?
> a) 5-15 minutes
> b) 1 hour
> c) 7-30 days
> d) 1 year
>> [!success]- Answer
>> c) 7-30 days

> [!question] What does `USER_ID_CLAIM` in SIMPLE_JWT configuration specify?
> a) The user's email claim
> b) Which claim in the JWT payload contains the user identifier
> c) The claim that stores the user's password
> d) The claim that stores user permissions
>> [!success]- Answer
>> b) Which claim in the JWT payload contains the user identifier

> [!question] How does a server-side proxy pattern handle JWTs for microservices?
> a) The browser sends JWTs directly to each microservice
> b) The frontend stores JWTs in its session and attaches them to proxied requests
> c) The microservices share a session database
> d) JWTs are not used in proxy patterns
>> [!success]- Answer
>> b) The frontend stores JWTs in its session and attaches them to proxied requests

> [!question] What is the risk of using symmetric (HS256) signing in a microservices architecture?
> a) It is too slow
> b) Every service with the shared secret can sign valid tokens
> c) It requires a certificate authority
> d) It cannot be used with databases
>> [!success]- Answer
>> b) Every service with the shared secret can sign valid tokens

> [!question] What does the `exp` claim in a JWT specify?
> a) The token issuer
> b) The token expiration time
> c) The token subject
> d) The token audience
>> [!success]- Answer
>> b) The token expiration time

> [!question] What should the client do when an access token renewal fails because the refresh token has also expired?
> a) Keep trying the same refresh token
> b) Redirect the user to the login page for re-authentication
> c) Generate a new access token locally
> d) Wait for the server to send a new token
>> [!success]- Answer
>> b) Redirect the user to the login page for re-authentication

> [!question] Match the JWT algorithm with its key management.
>> [!example] Group A
>> a) HS256
>> b) RS256
>> c) None
>
>> [!example] Group B
>> n) No signing
>> o) Same secret for sign and verify
>> p) Private key signs, public key verifies
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the SIMPLE_JWT setting with its purpose.
>> [!example] Group A
>> a) ACCESS_TOKEN_LIFETIME
>> b) REFRESH_TOKEN_LIFETIME
>> c) AUTH_HEADER_TYPES
>
>> [!example] Group B
>> n) ('Bearer',)
>> o) timedelta(minutes=15)
>> p) timedelta(days=7)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the token lifecycle event with the correct action.
>> [!example] Group A
>> a) Token obtained
>> b) Token expired
>> c) Token blacklisted
>
>> [!example] Group B
>> n) POST /api/token/blacklist/
>> o) POST /api/token/ with credentials
>> p) POST /api/token/refresh/
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the client storage method with the token type typically stored.
>> [!example] Group A
>> a) Local Memory
>> b) HttpOnly Cookie
>> c) Server Session
>
>> [!example] Group B
>> n) Access Token in SPA
>> o) Refresh Token in hybrid architecture
>> p) Refresh Token in secure web env
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the auth flow component with its role.
>> [!example] Group A
>> a) authenticate()
>> b) TokenObtainPairView
>> c) JWTAuthentication
>
>> [!example] Group B
>> n) DRF auth class for JWT
>> o) SimpleJWT view for login
>> p) Built-in credential verification
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the security characteristic with its JWT component.
>> [!example] Group A
>> a) Integrity
>> b) Confidentiality
>> c) Authentication
>
>> [!example] Group B
>> n) Signature prevents tampering
>> o) Token proves sender's identity
>> p) Not provided by standard JWTs
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the migration step with its purpose.
>> [!example] Group A
>> a) python manage.py migrate
>> b) register token_blacklist
>> c) add JWTAuthentication
>
>> [!example] Group B
>> n) Creates outstandingtoken tables
>> o) Enables SimpleJWT in DRF settings
>> p) Enables token revocation support
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the token type with its claim in the payload.
>> [!example] Group A
>> a) Access Token
>> b) Refresh Token
>> c) Both
>
>> [!example] Group B
>> n) token_type: "access"
>> o) token_type: "refresh"
>> p) Contains exp and jti claims
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the client code pattern with its purpose.
>> [!example] Group A
>> a) requests.post(url, json=credentials)
>> b) headers = {"Authorization": f"Bearer {token}"}
>> c) if response.status_code == 401
>
>> [!example] Group B
>> n) Check for token expiration
>> o) Send credentials to login
>> p) Attach token to API request
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the SimpleJWT database table with its purpose.
>> [!example] Group A
>> a) outstandingtoken
>> b) blacklistedtoken
>> c) django_migrations
>
>> [!example] Group B
>> n) Tracks applied database migrations
>> o) Tracks revoked refresh tokens
>> p) Tracks all issued refresh tokens
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)