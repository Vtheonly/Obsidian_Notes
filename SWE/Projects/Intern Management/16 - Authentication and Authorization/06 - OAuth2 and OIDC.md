---
tags: [concept, auth, oauth2, oidc]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/04 - JWT (JSON Web Tokens)]]
---

# OAuth2 and OIDC

## OAuth2

**OAuth2** (RFC 6749) is a framework for **delegated authorization** — letting a third-party app access your data in another service, without giving it your password.

Example: "Log in with Google." A third-party app gets a token that lets it read your Google profile, but it never sees your Google password.

## Flows (grant types)

| Flow | Use case |
|---|---|
| Authorization Code | Web apps (with a backend) |
| Authorization Code + PKCE | Mobile/SPAs |
| Client Credentials | Server-to-server |
| Resource Owner Password | Legacy (deprecated) |
| Implicit | Legacy (deprecated) |
| Refresh Token | Renew expired access tokens |

## OIDC (OpenID Connect)

**OIDC** is an identity layer on top of OAuth2. While OAuth2 is about authorization (what can the app do), OIDC is about authentication (who is the user).

OIDC adds an **ID Token** (a JWT) that contains the user's identity.

## Tokens

- **Access Token** — sent to the API; proves the app can access the user's data.
- **Refresh Token** — long-lived; used to get new access tokens.
- **ID Token** (OIDC) — JWT with the user's identity.

## Project Connection

For a desktop app, OAuth2/OIDC is overkill. But if the app evolves to a SaaS with "Log in with Google/Microsoft/GitHub," OIDC is the way.

## Further reading

- RFC 6749 (OAuth2).
- OIDC specification (openid.net).
