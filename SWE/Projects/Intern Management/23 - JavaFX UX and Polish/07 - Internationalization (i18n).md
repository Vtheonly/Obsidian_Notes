---
tags: [concept, ux, i18n, l10n]
type: concept
status: complete
related:
  - [[03 - Java Foundations/09 - Modern Date and Time API (java.time)]]
---

# Internationalization (i18n)

## What it is

**i18n** (internationalization) is designing the app to support multiple languages. **l10n** (localization) is translating for a specific locale.

## Java i18n

### Resource bundles
`messages.properties` (default):
```
login.title=Login
login.username=Username
login.password=Password
login.button=Login
```

`messages_fr.properties` (French):
```
login.title=Connexion
login.username=Nom d'utilisateur
login.password=Mot de passe
login.button=Se connecter
```

`messages_ar.properties` (Arabic):
```
login.title=تسجيل الدخول
login.username=اسم المستخدم
login.password=كلمة المرور
login.button=دخول
```

### Loading
```java
Locale locale = Locale.getDefault();  // or user preference
ResourceBundle bundle = ResourceBundle.getBundle("messages", locale);
String loginText = bundle.getString("login.button");
```

### FXML
```xml
<Button text="%login.button"/>
```
`%key` tells FXMLLoader to look up the key in the resource bundle.

```java
FXMLLoader loader = new FXMLLoader(url, bundle);
```

### Number/date formatting
```java
NumberFormat nf = NumberFormat.getInstance(locale);
String formatted = nf.format(1234.56);  // "1,234.56" (US) or "1 234,56" (France)

DateTimeFormatter df = DateTimeFormatter.ofLocalizedDate(FormatStyle.MEDIUM).withLocale(locale);
String dateStr = LocalDate.now().format(df);
```

## RTL (Right-to-Left)

For Arabic, Hebrew:
```java
scene.getRoot().setNodeOrientation(NodeOrientation.RIGHT_TO_LEFT);
```

Or in FXML:
```xml
<VBox nodeOrientation="RIGHT_TO_LEFT">
```

## Project Connection

The project is for Sonatrach (Algeria) — French and Arabic are official languages. But every string is hardcoded English:
```xml
<Button text="Login"/>
<Label text="Username"/>
```

The fix:
1. Move every string to `messages.properties`.
2. Add `messages_fr.properties` and `messages_ar.properties`.
3. Use `%key` in FXML.
4. Set `nodeOrientation="RIGHT_TO_LEFT"` for Arabic.
5. Add a language selector in Settings.

## Further reading

- Java Internationalization tutorial.
- JavaFX i18n documentation.
