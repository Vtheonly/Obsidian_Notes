---
tags: [concept, auth, session, security]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/04 - JWT (JSON Web Tokens)]]
---

# Session Management

## What it is

After authentication, the server creates a **session** — a server-side record of the authenticated user. The client gets a **session ID** (in a cookie or token) to identify the session on subsequent requests.

## Why

- Don't re-authenticate on every request (slow, annoying).
- Track the user's identity, role, login time, etc.
- Allow logout (invalidate the session).

## Server-side sessions

```
1. Client sends username + password.
2. Server authenticates, creates session #12345 with user data.
3. Server sends session ID (e.g., in a cookie: SESSIONID=abc123).
4. Client sends cookie on every request.
5. Server looks up session #12345, knows the user.
6. On logout, server invalidates session #12345.
```

## Session security

- **Session ID must be unguessable** — use `SecureRandom`, 128+ bits.
- **Session ID in a cookie** — `HttpOnly` (no JS access), `Secure` (HTTPS only), `SameSite=Strict` (CSRF protection).
- **Session timeout** — invalidate after 30 minutes of inactivity.
- **Regenerate on login** — prevent session fixation (attacker sets the session ID before login).
- **Invalidate on logout** — server-side, not just client-side.

## Project Connection

The project has **no session**. Login opens a new `Stage` with the role-specific FXML. The role is checked once and never re-validated. Anyone with read access to the JAR can launch any FXML directly via `FXMLLoader` and bypass authentication entirely.

The fix: introduce a `Session` object and `SessionManager`:
```java
public class Session {
    private final User user;
    private final Instant loginTime;
    private final Instant expiresAt;
    // ...
}

public class SessionManager {
    private Session current;
    public void startSession(User user) { ... }
    public Optional<Session> getCurrent() { ... }
    public void invalidate() { ... }
}
```

Every service method that performs a privileged operation checks the session:
```java
public void acceptIntern(long internId) {
    Session session = sessionManager.getCurrent().orElseThrow(() -> new NotAuthenticatedException());
    authz.require(session, Permission.ACCEPT_INTERN);
    // ...
}
```

## Further reading

- OWASP Session Management Cheat Sheet.
