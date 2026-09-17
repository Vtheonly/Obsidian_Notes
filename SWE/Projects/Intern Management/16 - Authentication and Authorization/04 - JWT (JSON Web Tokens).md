---
tags: [concept, auth, jwt, tokens]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/10 - Session Management]]
---

# JWT (JSON Web Tokens)

## What it is

A **JWT** is a compact, self-contained token for stateless authentication. The token contains the user's identity and claims, signed by the server.

## Structure

```
<header>.<payload>.<signature>
```

- **Header** — algorithm (HS256, RS256) and token type (JWT).
- **Payload** — claims (user ID, role, expiry).
- **Signature** — HMAC of header + payload, using a secret key.

All three are Base64URL-encoded and joined with dots.

## Example

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE2OTAwMDAwMDB9.signature
```

Decoded payload:
```json
{
  "sub": "123",
  "role": "admin",
  "exp": 1690000000
}
```

## Stateless vs stateful

- **Stateful (server session)**: server stores session data; client has an ID. Server lookup per request.
- **Stateless (JWT)**: server signs the token; client stores everything. No server lookup.

## When to use JWT

- **REST APIs** — no server-side session needed.
- **Microservices** — services can verify the token independently (shared secret or public key).
- **Mobile apps** — no cookies needed.
- **Short-lived tokens** — access tokens expire in 15 min; refresh tokens in 7 days.

## When NOT to use JWT

- **Server-side web apps** — sessions are simpler and more secure (can be invalidated instantly).
- **Long-lived sessions** — JWT can't be easily revoked before expiry.
- **Sensitive data** — JWT payload is Base64, not encrypted (anyone can read it). Use JWE for encrypted tokens.

## Security considerations

- **Signing algorithm** — use RS256 (asymmetric) or HS256 (symmetric). Avoid `none`.
- **Expiry** — short (15 min for access tokens). Use refresh tokens for longer sessions.
- **Revocation** — JWT can't be revoked before expiry. Maintain a blacklist (defeats statelessness) or use short expiries.
- **Storage** — store in `HttpOnly` cookies (web) or secure storage (mobile/desktop). Not in `localStorage` (XSS-vulnerable).

## Project Connection

For a desktop app, JWT is overkill. A server-side session (in-memory) is sufficient. JWT would be useful if the app evolves to a REST API + multiple clients.

## Further reading

- JWT.io — interactive debugger.
- RFC 7519 (JWT).
