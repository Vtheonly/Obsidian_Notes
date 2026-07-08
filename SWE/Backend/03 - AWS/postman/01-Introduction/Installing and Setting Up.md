---
tags: [postman, setup]
---

# Installing and Setting Up Postman

> [!summary] TL;DR
> Install the Postman desktop app, sign in, create a workspace, and you're ready to send requests in under 5 minutes.

## Step 1 — Download

Go to <https://www.postman.com/downloads/> and pick your OS:

- **Windows** — `.exe` installer.
- **macOS** — `.dmg` (Apple Silicon or Intel).
- **Linux** — `.tar.gz`, Snap, or Flatpak.

> [!tip] Web vs Desktop
> Postman has a web version, but the desktop app is recommended — full scripting, faster, better with local APIs.

## Step 2 — Sign Up / Sign In

1. Open the app.
2. Click **Sign Up** (or **Sign In** if you already have an account).
3. Use email, Google, or GitHub.

Signing in syncs your collections, environments, and history across machines.

## Step 3 — Create a Workspace

A **workspace** is a container for your collections, environments, mocks, etc.

1. Click the workspace dropdown (top-left) → **Create Workspace**.
2. Pick:
   - **Personal** — only you.
   - **Team** — shared with teammates.
   - **Private** (paid) — restricted team workspace.
3. Name it (e.g. "Learning APIs").

## Step 4 — Tour the UI

```mermaid
flowchart TB
    Header[Header bar: workspace switcher, search, invite, settings]
    Sidebar[Sidebar: Collections / APIs / Environments / History / Mocks / Monitors]
    Builder[Builder: method dropdown, URL bar, tabs (Params/Headers/Body/Tests/etc.)]
    Response[Response pane: status code, time, size, body, headers, cookies]
```

## Step 5 — Send Your First Request

1. Click **+** to open a new tab.
2. Method: **GET**.
3. URL: `https://httpbin.org/get`.
4. Click **Send**.

You should see a `200 OK` with a JSON body.

## Step 6 — Recommended First Settings

Open **Settings** (gear icon):

- **General**:
  - **Trim keys and values in request parameters** → ON.
  - **Always ask before closing unsaved tabs** → ON.
- **Themes** → pick whatever you like.
- **Proxy** → leave off unless you need it.
- **SSL certificate verification** → ON (turn off only for self-signed certs in dev).

## Optional: Install Postman CLI / Newman

For CI/CD you'll want **Newman**, the CLI runner:

```bash
npm install -g newman
newman --version
```

See [[NewmanCLI]].

## Optional: Proxy & CA Cert

If your company intercepts HTTPS:

- **Settings → Certificates → Add Certificate**.
- Add the corporate root CA as a CA cert (or per-host client cert).

## Related Notes
- [[Introduction to Postman]] · [[APIs and HTTP]] · [[Creating and Sending Requests]]
