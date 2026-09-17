---
tags: [concept, auth, password-reset, security]
type: concept
status: complete
related:
  - [[31 - Enterprise Java/03 - Jakarta Mail]]
---

# Password Reset Flows

## The secure pattern

1. User clicks "Forgot password?" and enters their email.
2. Server generates a one-time token (UUID, 128+ bits).
3. Server stores the token with an expiry (e.g., 1 hour) and the user ID.
4. Server emails a link: `https://app.com/reset?token=abc123`.
5. User clicks the link.
6. Server verifies the token (exists, not expired, not used).
7. User enters a new password.
8. Server hashes the new password, updates the DB, invalidates the token.
9. Server emails the user a "password changed" notification.

## Security considerations

- **Token must be unguessable** — `SecureRandom`, 128+ bits.
- **Token must expire** — 1 hour is typical. Shorter is safer.
- **Token must be one-time** — invalidate after use.
- **Token must be tied to the user** — can't use Alice's token to reset Bob's password.
- **Email the user on change** — alerts them if they didn't initiate it.
- **Don't reveal if the email exists** — "If this email is registered, you'll receive a reset link." Prevents user enumeration.
- **Re-authenticate on password change** — require the old password for non-admin users.
- **Invalidate all sessions** — after a password change, log out everywhere.

## The project's vulnerability

The project has no password reset flow. `updateUserController` lets an admin change any user's password (displayed in plaintext, no old-password verification). An admin can set any password for any user.

## The fix

Implement a password reset flow:
1. "Forgot password?" link on the login screen.
2. Email-based token (stored in a `password_reset_tokens` table).
3. Jakarta Mail to send the email.
4. New password page with strength validation.
5. Old password required for non-admin self-service changes.

## Further reading

- OWASP Forgot Password Cheat Sheet.
