---
tags: [concept, auth, security]
type: concept
status: complete
---

# Authentication vs Authorization

## The distinction

- **Authentication (AuthN)** — "Who are you?" Verifying identity.
- **Authorization (AuthZ)** — "What can you do?" Determining permissions.

You authenticate first, then authorize.

## Example

1. User logs in with username + password. (AuthN)
2. System verifies the password matches the hash. (AuthN)
3. System checks the user's role is "Admin". (AuthZ)
4. System allows access to the admin panel. (AuthZ)

## The project's confusion

The project conflates AuthN and AuthZ:
- `oracleConnector.login(username, hash)` — AuthN (verifies credentials).
- `oracleConnector.isAdmin(username, hash)` — AuthZ (checks role), but re-authenticates each time.

The role check happens once at login; thereafter, the user is "admin" based on which FXML was loaded. There's no per-request authorization — anyone who can launch `user_insertion.fxml` bypasses auth entirely.

## The fix

- AuthN: `AuthService.authenticate(username, password) → Optional<AuthenticatedUser>`.
- AuthZ: `AuthzService.check(session, Permission.ACCEPT_INTERN) → boolean` or throw.
- Per-action checks: every privileged service method verifies the current user has the required permission.

## Further reading

- OWASP Authentication Cheat Sheet.
- OWASP Authorization Cheat Sheet.
