---
tags: [case-study, code-walkthrough, javafx, controller]
type: case-study
status: complete
---

# insertionInternController.java (376 lines)

## What it does

Secretary view. Tabs: Manage, Email, Report.
- Manage tab: nested TabPane with Insert/Search sub-tabs. Insert form → `oracleConnector.insertIntern`. Search form → `oracleConnector.searchIntern` → builds TitledPane per result.
- Email tab: TextField + HTMLEditor + Button **with no `onAction`** (dead UI).
- Report tab: HTMLEditor + Button → `makePDF()` using OpenPDF's deprecated `HTMLWorker`.

## `static String labelText`

```java
public static String labelText;
public static String sendConstraint() { return labelText; }
```

Cross-controller data passing. When the user clicks "Update" on a search result, `labelText` is set to the formatted record string, then `update_intern.fxml` is loaded in a new Stage. `updateInternController.initialize()` calls `insertionInternController.sendConstraint()` to read it back.

### What's wrong
1. **Race condition** — two clicks in quick succession: click 1 sets labelText to intern A, click 2 overwrites it to intern B, click 1's window reads intern B. The user edits what they think is intern A but is actually intern B.
2. **Global mutable state** — untestable, no encapsulation, no ownership.
3. **String serialization** — the intern is serialized via `Map.toString()` then parsed back via `toolkit.parseText`. Any value containing `:` or `, ` breaks the parser.

### Fix
Pass typed data via the controller instance:
```java
FXMLLoader loader = new FXMLLoader(...);
Parent root = loader.load();
UpdateInternController ctrl = loader.getController();
ctrl.setIntern(selectedIntern);
stage.show();
```
No static state. See [[05 - Software Architecture/04 - Dependency Injection]].

## `addToPool` — TitledPane + UI tree walking

```java
Label innerLabel = new Label(intern.toString());
// ... build AnchorPane, HBox(Update,Delete,Print), VBox, TitledPane
DeleteButton.setOnAction(event -> {
    labelText = ((Label) ((AnchorPane) ((VBox) ((HBox) DeleteButton.getParent()).getParent()).getChildren().get(0)).getChildren().get(0)).getText();
    // ... parse labelText, call deleteIntern
});
```

### What's wrong
1. **Five chained casts through the scene graph** — `DeleteButton → HBox → VBox → child 0 → AnchorPane → child 0 → Label`. If anyone adds a wrapper, reorders children, or replaces HBox with BorderPane, this throws `ClassCastException` at runtime.
2. **`intern.toString()` used as serialization format** — couples the database to the UI layout.
3. **No virtualization** — VBox instantiates one TitledPane per result. 1,000 interns = 1,000 heavy graphical nodes. Memory explosion + scroll lag.
4. **`PrintButton.setOnAction` commented out TODO** — dead button.
5. **Inline CSS per status** — `"-fx-text-fill: green/red/orange"` hardcoded per case.

### Fix
- Replace TitledPane-in-VBox with `TableView<Intern>` (virtualized).
- Hold the typed `Intern` on the button's `userData`: `deleteButton.setUserData(intern)`.
- Use CSS classes for status colors: `.badge-accepted`, `.badge-pending`, `.badge-rejected`.

See [[22 - JavaFX Advanced Controls/08 - TableView]] and [[22 - JavaFX Advanced Controls/10 - Virtualization (how it works)]].

## `insertInternController` — the `value == ""` bug

```java
for (String key : internData.keySet()) {
    String value = String.valueOf(internData.get(key));
    if (value == "" || value.isEmpty()) {  // BUG: value == "" is reference equality
        JOptionPane.showMessageDialog(null, "Fill all the inputs fields");
        return;
    }
}
```

### What's wrong
1. **`value == ""`** is reference equality — always false for runtime-constructed strings. The code "works" only because `value.isEmpty()` catches the empty case.
2. **`String.valueOf(internData.get(key))`** — redundant; `get()` already returns `Object`, but `String.valueOf` on a String is wasteful.
3. **`JOptionPane` mixed into JavaFX**.
4. **No field-level validation** — no email format check, no phone format check, no name length cap. Generic "fill everything" message is useless when 9 of 10 fields are filled.

### Fix
Use inline form validation: `TextField` with a `focusedProperty` listener that validates on blur. Add `.error` CSS class for red border. Show a `Label` below the field with the error message. Disable the submit button until all fields are valid. See [[23 - JavaFX UX and Polish/06 - Inline Form Validation]].

## `makePDF` — deprecated HTMLWorker

```java
Document document = new Document();
PdfWriter.getInstance(document, new FileOutputStream("document_now.pdf"));
document.open();
HTMLWorker.parse(new StringReader(PDF_INPUT.getHtmlText()));
document.close();
```

### What's wrong
1. **`HTMLWorker` is deprecated** (since 2010, removed in iText 7.x). Does not support modern CSS.
2. **`document_now.pdf` written to CWD** — unpredictable location. From IntelliJ, it's the project root. From `java -jar`, it's wherever the user ran the command. From a Windows Start Menu shortcut, it's `C:\Windows\System32` — no write permission.
3. **No `FileChooser`** — user can't pick the save location.
4. **No exception handling** for `IOException` — silent failure.
5. **The committed `document_now.pdf`** in the repo is the result of one developer running this once and accidentally committing the output.

### Fix
Replace with OpenHTMLtoPDF. Use `FileChooser.showSaveDialog()`. Default to `System.getProperty("user.home") + "/Documents/"`. See [[31 - Enterprise Java/07 - OpenHTMLtoPDF]].

## N+1 in `searchIntern`

```java
List<Map<String, Object>> results = oracleConnector.searchIntern(filters);
for (Map<String, Object> intern : results) {
    String themeName = oracleConnector.getNameById(
        Integer.parseInt((String) intern.get("theme_id")),
        "theme", "theme_id", "theme_name"
    );
    addToPool(...);
}
```

100 interns = 101 queries. See [[11 - DB Performance and Indexing/18 - N+1 Query Problem]].

### Fix
```sql
SELECT i.intern_id, i.name, i.email, t.theme_name
FROM interns i
LEFT JOIN themes t ON i.theme_id = t.theme_id
WHERE i.name LIKE ?
```
One query, one round-trip.
