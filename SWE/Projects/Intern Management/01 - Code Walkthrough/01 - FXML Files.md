---
tags: [case-study, code-walkthrough, fxml, javafx]
type: case-study
status: complete
---

# FXML Files

## Overview

6 FXML files, 908 lines total. Every one uses:
- `AnchorPane` root with `layoutX`/`layoutY` absolute coordinates.
- Inline `style="-fx-..."` properties.
- Misspelled button text.
- No `<fx:include>` (no composition).
- `style.css` referenced in some but the file is empty.

## login_page.fxml (45 lines)

```xml
<AnchorPane fx:id="loginP" xmlns="http://javafx.com/javafx/21">
    <GridPane>
        <AnchorPane GridPane.columnIndex="0" style="-fx-background-color: #F8981C;">
            <ImageView><image><Image url="@sonatrach-logo.png"/></image></ImageView>
        </AnchorPane>
        <TextField fx:id="username" layoutX="..." layoutY="..."/>
        <PasswordField fx:id="password" layoutX="..." layoutY="..."/>
        <Button text="Login" onAction="#onLoginClick" layoutX="..." layoutY="..."/>
    </GridPane>
</AnchorPane>
```

### What's wrong
1. **Absolute positioning** via `layoutX`/`layoutY` — not responsive, breaks on 4K / 13" / accessibility zoom.
2. **Inline `-fx-background-color: #F8981C`** (Sonatrach orange) — should be a CSS class.
3. **Hardcoded English** — no `ResourceBundle`, no `%key` references. No i18n.
4. **`mnemonicParsing` not set** — no Alt+key shortcuts.
5. **No `accessibleText`** — screen readers can't identify the fields.
6. **`setResizable(true)` on the Stage but content is fixed-size** — resizing shows empty orange space.

## intern_insertion.fxml (269 lines)

```xml
<AnchorPane>
    <TabPane tabClosingPolicy="UNAVAILABLE">
        <Tab fx:id="manageTab" text="Manage">
            <TabPane>  <!-- nested TabPane! -->
                <Tab text="Insert">
                    <BorderPane>
                        <ScrollPane><GridPane>
                            <effect><Glow/></effect>  <!-- bizarre -->
                            <!-- form fields -->
                        </GridPane></ScrollPane>
                    </BorderPane>
                </Tab>
                <Tab text="Search">
                    <SplitPane>
                        <!-- form -->
                        <VBox fx:id="ResultPool"/>  <!-- TitledPane-in-VBox goes here -->
                    </SplitPane>
                </Tab>
            </TabPane>
        </Tab>
        <Tab fx:id="emailTab" text="Email">
            <TextField/>
            <HTMLEditor/>
            <Button text="Send"/>  <!-- no onAction! -->
        </Tab>
        <Tab fx:id="reportTab" text="Report">
            <HTMLEditor fx:id="PDF_INPUT"/>
            <Button text="Serach" onAction="#makePDF"/>  <!-- misspelled -->
        </Tab>
    </TabPane>
</AnchorPane>
```

### What's wrong
1. **Nested TabPane** — tabs inside tabs. Confusing UX.
2. **`<effect><Glow/></effect>` on a GridPane** — decorative glow on a form. Reduces contrast (accessibility issue), looks unprofessional.
3. **`GridPane.columnSpan="2147483647"`** (Integer.MAX_VALUE) — used to span all columns. Should use `REMAINING` or a sensible value.
4. **`RowConstraints maxHeight="1.7976931348623157E308"`** (Double.MAX_VALUE) — to grow to fill. Use `vgrow="ALWAYS"`.
5. **Email tab Button has no `onAction`** — dead UI. Clicking "Send" does nothing.
6. **"Serach"** misspelling (should be "Search").
7. **`VBox fx:id="ResultPool"`** — the TitledPane-in-VBox anti-pattern lives here.

## user_insertion.fxml (293 lines)

TabPane with tabs: `Manage_User`, `Manage_theme`, `Manage_Departement ` (trailing space, misspelled), `Statitics` (misspelled). Three SplitPanes for CRUD forms, each with `Glow` effect. Two `PieChart`s. Misspellings throughout: `Describtion`, `Loaction`, `Paasword`, `Reciver`.

## decision_Intern.fxml (88 lines)

`SplitPane` root. Left `BorderPane` with `ButtonBar` (`Accepte All`, `Refuse All`, `Search` — all misspelled) and `GridPane` form. `startDatePicker` declared in FXML but never `@FXML`-injected in `chiefDecisionController` — silent dead UI element.

## update_intern.fxml (100 lines) and update_worker_user.fxml (113 lines)

Both `BorderPane` root with `ScrollPane` → `GridPane` form, `ButtonBar` with Update (`defaultButton="true"`) and Cancel (`cancelButton="true"`, **no `onAction`**). The Cancel button does nothing when clicked.

## style.css

**Empty file** (0 bytes). All styling is inline. See [[20 - JavaFX Layout and CSS/03 - CSS in JavaFX]].

## The fix

- Replace `AnchorPane` with `BorderPane` (top header, left sidebar, center content).
- Replace `GridPane` with `GridPane` (good for forms) but use `ColumnConstraints` with `percentWidth`, not absolute coordinates.
- Move all inline styles to `style.css` with design tokens (CSS variables).
- Use `<fx:include>` to compose reusable components.
- Add `mnemonicParsing="true"` and `text="_Login"` for Alt+L.
- Add `accessibleText` to every interactive control.
- Move all strings to `messages.properties` for i18n.
- Remove `<Glow/>` from form GridPanes.
- Remove dead tabs and buttons.
- Fix all misspellings.

See [[20 - JavaFX Layout and CSS/00 - MOC - JavaFX Layout]] and [[23 - JavaFX UX and Polish/00 - MOC - JavaFX UX]].
