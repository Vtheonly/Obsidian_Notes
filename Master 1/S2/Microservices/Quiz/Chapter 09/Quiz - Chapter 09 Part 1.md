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
> [!question] JWTs introduce Stateless Authentication, where user information is encoded into a signed token sent to the client.
>> [!success]- Answer
>> True

> [!question] Access tokens should have a long lifetime because they are stateless and cannot be easily revoked.
>> [!success]- Answer
>> False

> [!question] Standard JWTs are encrypted, ensuring the payload data cannot be read by anyone who intercepts the token.
>> [!success]- Answer
>> False

> [!question] The `TokenObtainPairView` endpoint accepts user credentials and returns an access token and a refresh token.
>> [!success]- Answer
>> True

> [!question] In a hybrid architecture, JWT tokens can be stored inside Django's secure session engine for server-side proxying.
>> [!success]- Answer
>> True

> [!question] Refresh Token Rotation creates a security pipeline where old refresh tokens are blacklisted when new ones are issued.
>> [!success]- Answer
>> True

> [!question] The `TokenBlacklistView` endpoint is used to revoke refresh tokens during logout.
>> [!success]- Answer
>> True

> [!question] Standard JWTs are signed using Base64URL encoding, which is a form of encryption.
>> [!success]- Answer
>> False

> [!question] JWTs are useful in microservices because each service can verify the token independently without a database lookup.
>> [!success]- Answer
>> True

> [!question] The `token_blacklist` app must be registered in INSTALLED_APPS to support token revocation during logout.
>> [!success]- Answer
>> True

> [!question] What are the three parts of a JWT separated by dots?
> a) header.body.signature
> b) header.payload.signature
> c) header.claims.signature
> d) metadata.payload.signature
>> [!success]- Answer
>> b) header.payload.signature

> [!question] What is the recommended lifetime for an access token in SimpleJWT?
> a) 5-15 minutes
> b) 1-2 hours
> c) 7-30 days
> d) 1 year
>> [!success]- Answer
>> a) 5-15 minutes

> [!question] Which SimpleJWT endpoint is used to exchange a refresh token for a new access token?
> a) /api/token/
> b) /api/token/refresh/
> c) /api/token/blacklist/
> d) /api/token/verify/
>> [!success]- Answer
>> b) /api/token/refresh/

> [!question] What does `ROTATE_REFRESH_TOKENS` do when set to True?
> a) It rotates the signing algorithm
> b) It issues a new refresh token when refreshing an access token
> c) It rotates the user's password
> d) It rotates the database connection
>> [!success]- Answer
>> b) It issues a new refresh token when refreshing an access token

> [!question] What is the most secure storage location for an access token in a Single-Page Application?
> a) localStorage
> b) Session cookie
> c) Local memory (JavaScript state)
> d) URL query parameter
>> [!success]- Answer
>> c) Local memory (JavaScript state)

> [!question] In a hybrid architecture, why are JWT tokens stored in the server session rather than exposed to the browser?
> a) It's faster
> b) The browser cannot handle JWTs
> c) It's more secure because tokens are not directly exposed to client-side code
> d) JWTs cannot be sent to browsers
>> [!success]- Answer
>> c) It's more secure because tokens are not directly exposed to client-side code

> [!question] How does a client detect that an access token has expired?
> a) The server sends a warning header
> b) The API returns HTTP 401 Unauthorized
> c) The client tracks time using Date headers
> d) The token changes color
>> [!success]- Answer
>> b) The API returns HTTP 401 Unauthorized

> [!question] Which algorithm uses a private-public key pair for JWT signing?
> a) HS256
> b) RS256
> c) MD5
> d) AES256
>> [!success]- Answer
>> b) RS256

> [!question] What does the `JTI_CLAIM` in the SIMPLE_JWT configuration refer to?
> a) The token issuer
> b) The token type
> c) A unique identifier for the JWT
> d) The audience claim
>> [!success]- Answer
>> c) A unique identifier for the JWT

> [!question] In the `AuthorizedAPIClient` pattern, what happens when the refresh token has also expired?
> a) The client retries automatically
> b) The client raises an exception requiring re-authentication
> c) The client generates a new access token without credentials
> d) The client waits for the token to refresh
>> [!success]- Answer
>> b) The client raises an exception requiring re-authentication

> [!question] Match the JWT component with its content.
>> [!example] Group A
>> a) Header
>> b) Payload
>> c) Signature
>
>> [!example] Group B
>> n) Contains claims about the user
>> o) Verifies token integrity
>> p) Contains algorithm and token type
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the SimpleJWT endpoint with its purpose.
>> [!example] Group A
>> a) TokenObtainPairView
>> b) TokenRefreshView
>> c) TokenBlacklistView
>
>> [!example] Group B
>> n) Revoke refresh token on logout
>> o) Exchange credentials for tokens
>> p) Renew an expired access token
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the token type with its characteristic.
>> [!example] Group A
>> a) Access Token
>> b) Refresh Token
>> c) Both tokens
>
>> [!example] Group B
>> n) Short lifetime, stateless, cannot be revoked
>> o) Returned by TokenObtainPairView
>> p) Longer lifetime, can be blacklisted
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the storage location with its security level.
>> [!example] Group A
>> a) Local Memory
>> b) HttpOnly Cookie
>> c) localStorage
>
>> [!example] Group B
>> n) Safe from XSS, vulnerable to CSRF
>> o) Cleared on refresh, safe from XSS and CSRF
>> p) Vulnerable to XSS attacks
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the rotation policy with its effect.
>> [!example] Group A
>> a) ROTATE_REFRESH_TOKENS
>> b) BLACKLIST_AFTER_ROTATION
>> c) UPDATE_LAST_LOGIN
>
>> [!example] Group B
>> n) Marks old tokens as revoked
>> o) Issues new refresh token on refresh
>> p) Records login timestamps
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the claim type with its description.
>> [!example] Group A
>> a) Registered Claims
>> b) Public Claims
>> c) Private Claims
>
>> [!example] Group B
>> n) Custom claims between agreeing parties
>> o) Standard pre-defined claims like exp and iss
>> p) Collision-resistant custom claims
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the signing algorithm with its security model.
>> [!example] Group A
>> a) HS256 (Symmetric)
>> b) RS256 (Asymmetric)
>> c) None
>
>> [!example] Group B
>> n) Public key verifies, private key signs
>> o) Same key signs and verifies
>> p) No signature verification
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the client-side action with its HTTP request pattern.
>> [!example] Group A
>> a) Login
>> b) Authorized request
>> c) Token renewal
>
>> [!example] Group B
>> n) POST /api/token/ with credentials
>> o) GET /api/data/ with Bearer token
>> p) POST /api/token/refresh/ with refresh token
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the proxy pattern step with its description.
>> [!example] Group A
>> a) Store JWT in session
>> b) Extract JWT from session
>> c) Proxy request with JWT
>
>> [!example] Group B
>> n) Retrieve token from request.session
>> o) Attach Bearer token to downstream request
>> p) Save tokens after successful remote login
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the token auto-renewal step with its position.
>> [!example] Group A
>> a) Detect 401 response
>> b) Call refresh endpoint
>> c) Retry original request
>
>> [!example] Group B
>> n) With new access token
>> o) Intercept the failed response
>> p) Submit current refresh token
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)