---
tags: [concept, security, validation]
type: concept
status: complete
related:
  - [[17 - Application Security/01 - Bean Validation (JSR-380)]]
---

# Input Validation

## The rule

> "Never trust user input." — OWASP

Validate **all** input from users, external APIs, file uploads, environment variables. Validation should happen at the boundary (controller, API endpoint).

## What to validate

- **Type** — is the age a number? Is the email a string?
- **Format** — does the email match `xxx@xxx.xxx`? Is the phone E.164?
- **Length** — is the name ≤ 100 chars?
- **Range** — is the age 16-100?
- **Required** — is the email provided?
- **Charset** — is the name valid Unicode (no control chars)?
- **Semantics** — does the department_id exist? Is the start_date in the future?

## Where to validate

### Client-side (UX only)
JavaFX form validation improves UX (instant feedback) but is bypassable. Never rely on it for security.

### Server-side (the real validation)
Validate in the service layer. Reject invalid input with a clear error.

### Database-side (last line of defense)
CHECK constraints, NOT NULL, FKs, UNIQUE. Even if the app is buggy, the DB enforces integrity.

## The project's validation

```java
if (value == "" || value.isEmpty()) {  // broken (==)
    JOptionPane.showMessageDialog(null, "Fill all the inputs fields");
    return;
}
int age = Integer.parseInt(insert_intern_Age.getText());  // no try/catch
```

- No email format validation.
- No phone format validation.
- No name length cap.
- `Integer.parseInt` can throw `NumberFormatException`.
- No semantic validation (does the theme exist?).

## The fix

Use Bean Validation (JSR-380) annotations on domain objects:
```java
public record CreateInternCommand(
    @NotBlank @Size(max = 100) String name,
    @NotNull @Min(16) @Max(100) Integer age,
    @NotBlank @Email @Size(max = 100) String email,
    @Size(max = 150) String university,
    @Pattern(regexp = "^\+?[0-9 ]{8,20}$") String phoneNumber,
    @NotNull Long themeId
) {}
```

A validator checks all constraints and returns a list of violations.

## Further reading

- OWASP Input Validation Cheat Sheet.
