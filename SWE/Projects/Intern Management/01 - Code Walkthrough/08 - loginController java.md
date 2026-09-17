---
tags: [case-study, code-walkthrough, login, security]
type: case-study
status: complete
---

# loginController.java (72 lines)

## What it does

```java
@FXML
public void onLoginClick() {
    String user = username.getText();
    String pass = hashIt(password.getText());
    if (oracleConnector.login(user, pass)) {
        int roleId = oracleConnector.getUserAccessLevel(user, pass);
        if (oracleConnector.isAdmin(user, pass)) {
            // open user_insertion.fxml in a new Stage, close loginWindow
        } else if (oracleConnector.isChief(user, pass)) {
            // open decision_Intern.fxml
        } else {
            // secretary: open intern_insertion.fxml, call setAccessLevel(roleId)
        }
    } else {
        JOptionPane.showMessageDialog(null, "Invalid username or password.");
    }
}
```

## What's wrong

1. **`hashIt` called up to 4 times for the same password** — `login`, `getUserAccessLevel`, `isAdmin`, `isChief` each call `hashIt(password.getText())` internally. Should hash once, pass the hash.
2. **3–4 round-trips for one login** — should be 1 query: `SELECT user_id, password_hash, role_id FROM worker_user WHERE username = ?`.
3. **`JOptionPane` mixed into JavaFX** — `JOptionPane.showMessageDialog(null, "Invalid username or password.")` pops a Swing dialog from a JavaFX thread.
4. **No rate limiting / lockout** — an attacker can hammer login with thousands of guesses/sec.
5. **No constant-time comparison** — `oracleConnector.login` does `SELECT COUNT(*) WHERE username=? AND password_hash=?`. Sending the hash to the DB for comparison. The DB comparison is not constant-time (though it's harder to exploit than app-side comparison).
6. **No session** — opens a new Stage per role, closes the login window. No session token, no logout, no re-validation. Anyone with read access to the JAR can launch any FXML directly via `FXMLLoader` and bypass authentication entirely.
7. **Magic role IDs 4 and 5** — hardcoded in `oracleConnector.isAdmin`/`isChief`. If the DBA renumbers roles, the app breaks.
8. **`e.printStackTrace()`** in catch — not logging.
9. **Opens new `Stage` per view** — should be single-Stage scene swap. See [[20 - JavaFX Layout and CSS/07 - Single-Stage Navigation]].

## The fix

```java
public void onLoginClick() {
    String username = this.username.getText();
    char[] password = this.password.getText().toCharArray();
    try {
        Optional<AuthenticatedUser> user = authService.authenticate(username, password);
        if (user.isPresent()) {
            sessionManager.startSession(user.get());
            navigationController.showMainView(user.get().getRole());
        } else {
            showLoginError("Invalid username or password.");
            rateLimiter.recordFailedAttempt(username);
        }
    } catch (AccountLockedException e) {
        showLoginError("Account locked. Try again in " + e.getRetryAfter() + " seconds.");
    } finally {
        Arrays.fill(password, '\0');  // clear password from memory
    }
}
```

Where `authService.authenticate`:
1. Fetches the user by username only: `SELECT user_id, password_hash, salt, role_id, status FROM users WHERE username = ?`.
2. Verifies the password in-app with Argon2id's `verify()` (constant-time).
3. Returns `Optional<AuthenticatedUser>` — one round-trip, no enumeration oracle, no hash on the wire.

See [[16 - Authentication and Authorization/00 - MOC - Auth]].
