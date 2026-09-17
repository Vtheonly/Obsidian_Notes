---
tags: [case-study, code-walkthrough, javafx, controller]
type: case-study
status: complete
---

# updateInternController and updateUserController

## updateInternController.java (81 lines)

```java
public class updateInternController implements Initializable {
    final String CURRENT_UPDATE_PARAM = insertionInternController.sendConstraint();
    Map<String, String> parameters = toolkit.parseText(CURRENT_UPDATE_PARAM);

    @FXML private TextField fullName;
    // ... other fields
    @FXML private ChoiceBox<String> internshipTypeChoiceBox;
    @FXML private DatePicker startDatePicker;  // injected but never read

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        fullName.setText(parameters.get("Name"));
        // ... set other fields
        // BUG: re-purposes internshipTypeChoiceBox for IS_ACCEPTED
        internshipTypeChoiceBox.setItems(FXCollections.observableArrayList(
            "Pending", "Accepted", "Rejected"
        ));
        internshipTypeChoiceBox.setValue(parameters.get("IS_ACCEPTED"));
    }
}
```

### What's wrong
1. **Field initialization depends on static state set by another controller** — `CURRENT_UPDATE_PARAM` is read at field-init time, before `initialize()` runs. Works only because the parent controller set `labelText` before opening this window.
2. **`internshipTypeChoiceBox` is reused for `IS_ACCEPTED`** — confusing; "internship type" means 1/2/3 months elsewhere.
3. **`startDatePicker` is `@FXML`-injected but never read** — dead injection.
4. **No `Integer.parseInt` exception handling** for age, theme_id, etc.
5. **No validation** — any input accepted.
6. **`updateIntern` builds `newUpdateParams` (SET) and `idNamePrimaryKey` (WHERE: intern_id + name)** — defensive double-condition, but means you can't rename an intern (the WHERE clause wouldn't match the new name).

### Fix
Pass the typed `Intern` object via a setter:
```java
public void setIntern(Intern intern) {
    this.intern = intern;
    populateFields();
}
```
No static state, no string parsing, no field-init dependencies.

## updateUserController.java (105 lines)

```java
public class updateUserController implements Initializable {
    final String CURRENT_UPDATE_PARAM = insertionUserController.sendConstraint();
    Map<String, String> params = parseText(CURRENT_UPDATE_PARAM);

    @FXML private TextField password;  // BUG: should be PasswordField

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        // ...
        password.setText(params.get("password_hash"));  // displays the hash!
    }

    public void updateWorker() {
        paramsMap.put("password_hash", password.getText());  // user can edit the hash directly
        oracleConnector.updateWorkerUser(paramsNext, paramsMap);
    }
}
```

### What's wrong
1. **Password hash displayed in the password field** — `password.setText(params.get("password_hash"))`. The user sees the hash, can edit it, can submit an arbitrary string as the new hash. Bypasses hashing entirely.
2. **`TextField` instead of `PasswordField`** — even if the hash weren't displayed, the field shows plaintext.
3. **No old-password verification** — admin can change any user's password without proving they know the current one.
4. **No "new password" + "confirm password" fields** — no strength check, no confirmation.
5. **Confusing variable naming** — `paramsMap` (SET values) and `paramsNext` (WHERE: user_id + full_name). Reversed from intuition.

### Fix
- Replace `TextField` with `PasswordField` that starts empty.
- Add separate "New Password" and "Confirm New Password" fields.
- If "New Password" is non-empty, hash it with Argon2id and update.
- If empty, leave the existing hash untouched.
- Require old password verification for non-admin users.
- Add a password strength meter.
- **Never display any password or hash in the UI.**

See [[16 - Authentication and Authorization/07 - Password Reset Flows]].
