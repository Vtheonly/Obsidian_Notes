---
tags: [concept, testing, testfx, javafx]
type: concept
status: complete
related:
  - [[27 - Testing/02 - JUnit 5]]
---

# TestFX

## What it is

**TestFX** is a JavaFX UI testing framework. Click buttons, type text, verify UI state.

## Dependency

```xml
<dependency>
    <groupId>org.testfx</groupId>
    <artifactId>testfx-junit5</artifactId>
    <version>4.0.17</version>
    <scope>test</scope>
</dependency>
```

## Usage

```java
class LoginViewTest extends ApplicationTest {
    @Override
    public void start(Stage stage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("/login.fxml"));
        stage.setScene(new Scene(root));
        stage.show();
    }

    @Test
    void shouldShowErrorOnInvalidCredentials() {
        clickOn("#username").write("admin");
        clickOn("#password").write("wrongpass");
        clickOn("#loginButton");

        verifyThat(".alert", NodeMatchers.isVisible());
        verifyThat(".alert", hasText("Invalid username or password"));
    }

    @Test
    void shouldNavigateToAdminViewOnValidLogin() {
        clickOn("#username").write("admin");
        clickOn("#password").write("correctpass");
        clickOn("#loginButton");

        verifyThat("#adminView", NodeMatchers.isVisible());
    }
}
```

## Headless mode (CI)

```java
@Configuration
public class HeadlessConfig {
    static {
        System.setProperty("testfx.robot", "glass");
        System.setProperty("testfx.headless", "true");
        System.setProperty("prism.order", "sw");
        System.setProperty("prism.text", "t2k");
    }
}
```

Or use `monocle` for full headless support.

## Why

- **Catches UI bugs** — broken bindings, missing handlers, layout issues.
- **Regression tests** — verify a refactor didn't break the UI.
- **Confidence** — green UI tests mean the user-visible behavior works.

## Trade-offs

- **Slow** — UI tests take seconds each.
- **Brittle** — UI changes break tests.
- **Limited** — can't test everything (e.g., drag-and-drop is tricky).

Keep UI tests few (5-10) and focused on critical paths.

## Project Connection

The project has zero UI tests. The fix: TestFX for:
- Login flow (success, failure, rate limiting).
- Search (enter query, verify results).
- Insert (fill form, submit, verify row appears).
- Accept/reject (click, verify status changes).

## Further reading

- TestFX documentation.
