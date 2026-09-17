---
tags: [concept, security, cors, csrf]
type: concept
status: complete
---

# CORS and CSRF

> These are web-specific. Included for completeness; the project is a desktop app.

## CORS (Cross-Origin Resource Sharing)

A browser security mechanism. By default, JavaScript on `site-a.com` can't make requests to `site-b.com`'s API. CORS lets `site-b.com` explicitly allow `site-a.com`.

Without CORS, any web page could read your bank's API (if you're logged in).

## CSRF (Cross-Site Request Forgery)

An attacker tricks a logged-in user's browser into making a request to a site where the user is authenticated.

Example: you're logged into your bank. You visit `evil.com`, which has `<img src="bank.com/transfer?to=attacker&amount=1000">`. The browser sends the request with your cookies. The bank transfers money.

### Prevention
- **CSRF tokens** — a random token in each form; verified on submit.
- **SameSite cookies** — `SameSite=Strict` prevents the cookie from being sent on cross-site requests.
- **Custom headers** — APIs using `Authorization: Bearer` (not cookies) are immune.

## Project Connection

Not applicable (desktop app). If the app evolves to a web app, these matter.

## Further reading

- OWASP CSRF Prevention Cheat Sheet.
- MDN — CORS.
