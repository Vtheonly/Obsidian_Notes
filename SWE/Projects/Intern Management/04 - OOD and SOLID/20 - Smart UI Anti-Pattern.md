---
tags: [concept, anti-pattern, smart-ui]
type: concept
status: complete
related:
  - [[05 - Software Architecture/10 - Layered Architecture]]
  - [[05 - Software Architecture/15 - Separation of Concerns]]
---

# Smart UI Anti-Pattern

## What it is

A **Smart UI** (or Fat Client) is a user interface class that does everything: renders the UI, handles events, validates input, executes business logic, accesses the database, and shows error dialogs. There is no separation of concerns.

## The project's Smart UI

```java
public class insertionInternController implements Initializable {
    @FXML private VBox ResultPool;

    public void insertInternController() {  // event handler
        // 1. Read UI fields
        String name = insert_intern_Name.getText();
        String ageStr = insert_intern_Age.getText();
        // 2. Validate (badly)
        if (value == "" || value.isEmpty()) {
            JOptionPane.showMessageDialog(null, "Fill all the inputs fields");
            return;
        }
        // 3. Generate ID (race condition)
        int newId = oracleConnector.getMaxId("intern", "intern_id") + 1;
        // 4. Build the record as a Map
        HashMap<String, Object> internData = new HashMap<>();
        internData.put("intern_id", newId);
        // ...
        // 5. Insert into DB
        oracleConnector.insertIntern(internData);
        // 6. Show success dialog
        JOptionPane.showMessageDialog(null, "Intern inserted successfully");
    }

    public void searchIntern() {
        // 1. Read UI fields
        // 2. Build filters Map
        // 3. Query DB (N+1)
        // 4. For each result, build TitledPane with inline CSS
        // 5. Add to VBox
        // 6. Wire up Update/Delete buttons with UI tree walking
    }

    public void makePDF() {
        // 1. Read HTMLEditor content
        // 2. Use deprecated HTMLWorker to generate PDF
        // 3. Write to CWD
    }
}
```

The controller does: UI rendering, event handling, input validation, ID generation, data construction, DB access, dialog display, PDF generation. **Eight responsibilities in one class.**

## Why it's bad

- **Cannot reuse business logic** — if you want a REST API or CLI, you can't, because the logic is locked inside the JavaFX controller.
- **Cannot test** — to test the insert logic, you need to launch JavaFX, click the button, and check the DB.
- **Hard to maintain** — a schema change requires editing the controller.
- **Hard to extend** — adding a new UI (e.g., a web view) requires rewriting the logic.

## The fix: Layered Architecture

```
[ UI Layer (Controllers) ]        — only UI rendering and event handling
       ↓
[ Service Layer ]                 — business logic, validation, orchestration
       ↓
[ Repository Layer ]              — data access
       ↓
[ Database ]
```

- Controller calls `internService.create(internDto)`.
- `InternService.create()` validates, calls `internRepository.save()`, logs audit.
- `InternRepository.save()` executes SQL.
- Controller catches exceptions and shows JavaFX `Alert`.

No business logic in the controller. No SQL in the controller. No `JOptionPane` anywhere.

## Common pitfalls

- **"It's just a small app"** — Smart UI is fine for a 100-line script. It's a disaster for anything larger.
- **"I'll add layers later"** — later never comes. Add layers from the start.
- **Anemic controllers + anemic services** — just moving the Smart UI logic into a service that's also a God Class doesn't help.

## Project Connection

Every controller in the project is a Smart UI. The fix is to introduce a service layer and repository layer. See [[05 - Software Architecture/10 - Layered Architecture]].

## Further reading

- *Patterns of Enterprise Application Architecture* (Fowler), "Smart UI" anti-pattern.
