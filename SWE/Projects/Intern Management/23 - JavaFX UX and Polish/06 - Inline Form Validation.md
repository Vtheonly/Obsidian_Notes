---
tags: [concept, ux, validation, forms]
type: concept
status: complete
---

# Inline Form Validation

## What it is

Validate each field as the user types or on blur, showing the error next to the field (not in a popup).

## Implementation

```java
@FXML private TextField emailField;
@FXML private Label emailError;

@Override
public void initialize(URL url, ResourceBundle rb) {
    emailField.focusedProperty().addListener((obs, wasFocused, isNowFocused) -> {
        if (!isNowFocused) {  // on blur
            validateEmail();
        }
    });
}

private void validateEmail() {
    String email = emailField.getText();
    if (email.isEmpty()) {
        setError(emailField, emailError, "Email is required");
    } else if (!email.matches("^[^@]+@[^@]+\.[^@]+$")) {
        setError(emailField, emailError, "Invalid email format");
    } else {
        clearError(emailField, emailError);
    }
}

private void setError(TextField field, Label errorLabel, String message) {
    field.getStyleClass().add("error");
    errorLabel.setText(message);
    errorLabel.setVisible(true);
}

private void clearError(TextField field, Label errorLabel) {
    field.getStyleClass().remove("error");
    errorLabel.setVisible(false);
}
```

CSS:
```css
.text-input.error { -fx-border-color: -color-danger; }
.label-error { -fx-text-fill: -color-danger; -fx-font-size: 11; }
```

## Disable submit until valid

```java
submitButton.disableProperty().bind(
    emailField.textProperty().isEmpty()
        .or(nameField.textProperty().isEmpty())
        .or(ageField.textProperty().isEmpty())
);
```

## Why this matters

- **Instant feedback** — the user sees the error immediately, not after clicking Submit.
- **Specific** — "Email is required" vs. "Fill all the inputs fields."
- **Recoverable** — the user knows what to fix.
- **Professional** — modern apps validate inline; popups feel dated.

## Project Connection

The project's validation:
```java
if (value == "" || value.isEmpty()) {
    JOptionPane.showMessageDialog(null, "Fill all the inputs fields");
    return;
}
```

Generic message, popup dialog, no field-level feedback. The fix: inline validation with red borders and error labels.

## Further reading

- Nielsen Norman Group — Inline Validation.
