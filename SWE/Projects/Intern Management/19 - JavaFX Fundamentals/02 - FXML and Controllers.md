---
tags: [concept, javafx, fxml, controllers]
type: concept
status: complete
related:
  - [[20 - JavaFX Layout and CSS/00 - MOC - JavaFX Layout]]
---

# FXML and Controllers

## What it is

**FXML** is an XML-based markup for defining JavaFX UIs. It separates the view (FXML) from the controller (Java).

## Example

```xml
<!-- login.fxml -->
<VBox xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1"
      fx:controller="com.example.LoginController">
    <TextField fx:id="username" promptText="Username"/>
    <PasswordField fx:id="password" promptText="Password"/>
    <Button text="Login" onAction="#onLoginClick"/>
</VBox>
```

```java
public class LoginController {
    @FXML private TextField username;
    @FXML private PasswordField password;

    @FXML
    public void onLoginClick() {
        String user = username.getText();
        String pass = password.getText();
        // ...
    }
}
```

## `fx:controller`

The controller class. FXMLLoader instantiates it via no-arg constructor, then injects `@FXML`-annotated fields.

## `fx:id`

Links an FXML element to a `@FXML` field in the controller:
```xml
<TextField fx:id="username"/>
```
```java
@FXML private TextField username;
```

## `onAction`

Links an event to a controller method:
```xml
<Button onAction="#onLoginClick"/>
```
```java
@FXML public void onLoginClick() { ... }
```

## Controller lifecycle

```java
public class MyController implements Initializable {
    @FXML private TextField field;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        // runs after @FXML injection, before the view is shown
        field.setText("default");
    }
}
```

`initialize()` is called by FXMLLoader after injecting all `@FXML` fields.

## `fx:include`

```xml
<VBox>
    <fx:include source="header.fxml"/>
    <fx:include source="content.fxml"/>
</VBox>
```

Composes reusable components. Each include has its own controller.

## Controller factory (for DI)

```java
FXMLLoader loader = new FXMLLoader(url);
loader.setControllerFactory(type -> {
    // Use DI container to create the controller
    return applicationContext.getBean(type);
});
Parent root = loader.load();
```

Enables dependency injection into controllers.

## Project Connection

The project uses FXML correctly in structure, but:
- No `fx:include` (no composition).
- No `controllerFactory` (no DI).
- Lowercase class names in `fx:controller`.
- Controllers do everything (Smart UI anti-pattern).

The fix:
- Extract reusable components (`StatusView`, `ValidatedTextField`) as FXML includes.
- Use `controllerFactory` for DI.
- Move business logic to services; controllers only handle UI.

## Further reading

- JavaFX FXML documentation.
