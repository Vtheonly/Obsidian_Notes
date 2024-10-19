### Human-Computer Interface (HCI) Ergonomics

#### I. Window Appearance

1. **Display Density**
   - High density leads to high error rates and access times.
   - Distributing information across multiple windows can hinder users' overall perception of the application.

2. **Layout of Elements in Windows**
   - Group data into categories and define their sequence based on:
     1) Frequency of use
     2) Order of use in the current task
     3) Importance in context (mandatory, optional inputs).
   - Place the most important data groups at the top of the window according to the preferred criterion.
   - Vertically align input and/or display fields with their labels.

3. **Presentation of Lists and Tables**
   - Provide a title for lists and tables.
   - Respect standard alignments: labels on the left, numerical data on the right.
   - Organize elements in a table/list based on user work habits.

4. **Textual Elements**
   - Use vocabulary from users' domain of activity.
   - Use explicit and unambiguous terms, preferring affirmative forms.
   - Indicate the units of measurement used.
   - Avoid abbreviations except those widely adopted.
   - Use consistent labels for each field, list, table, column, or group of data.

5. **Graphical Elements**
   - **Typography**:
     - Use font sizes between 8 and 16 points.
     - Avoid italics and limit to three different fonts.
     - Use different fonts to differentiate elements.
   - **Color**:
     - Avoid incongruous color associations.
     - Prefer shades of gray or dark blue for window backgrounds.
     - Follow conventional color association rules.
   - **Icons**:
     - Icons should represent the action or concept they signify.
     - Prefer using a label in addition to the icon.
   - **Tab Usage**:
     - Used to avoid sequences of dialog boxes or buttons.
     - Limit to one row of tabs to facilitate manipulation.
     - Center tab labels on a single line.
     - Place buttons outside tabs if they are linked (dependent).

These principles aim to improve readability, understanding, and efficiency of user interfaces.

---
### II. Navigation Principles

#### 2. Intra-application Navigation

A. Two Types of Conversation
   - **Free Conversation**: Users have significant freedom in navigating within the application. Used for flexible applications like stock management.
   - **Guided Conversation**: Application controls the interface. Used in contexts prioritizing productivity or requiring strict adherence to procedures, such as online exams.

B. Number of Windows
   - Balancing the number of windows and displayed information density is crucial.
   - Find a compromise between presenting all necessary information and maintaining window readability.
   - Ideally, limit the application's depth to three levels to prevent user confusion and manipulation difficulties.

### III. Input Principles

#### 1. Keyboard Input

A. Input Fields
   - **Default Values**: Initialize input fields with default values whenever possible, corresponding to the user's most likely choice or their previous input.
   - **Mandatory vs. Optional Input**: Differentiate mandatory fields from optional ones, preferably by bold labels, symbols, or color highlighting.
   - **Validation**: Avoid data creation, update, or deletion without explicit user validation (confirmation message).

B. Input Feedback
   - **System Feedback**: Each keystroke should immediately trigger feedback, such as displaying the character or indicating prohibited characters.
   - **Error Handling**: Format or character type errors should be detected during input. Functional errors should be signaled only after data validation.

#### 2. Limited Options Selection

A. Exclusive Options: Radio Buttons
   - Use radio buttons for exclusive choices.
   - Provide at least two options unless the choice is insignificant, and always include a default value.

B. Non-exclusive Options: Checkboxes
   - Avoid checkboxes for critical functional choices like saving.
   - Group checkboxes and provide immediate visual feedback for selected items.

#### 3. Selection from a List

- Users should be able to deselect an item as easily as they select it.
- Highlight selected items immediately without triggering actions.
- Use lists to display elements, with the option for single or multiple selections.
- Display items logically or based on user frequency of use.

---

### IV. Menu Actions or Command Button Actions

#### 1. General Recommendations

A. Action Labels
   - Use easily understandable labels (and/or icons) to represent actions.
   - Choose unambiguous vocabulary familiar to the user.
   - Prefer infinitive verbs for labels (e.g., "Validate", "Save").
   - Capitalize the initial letter of the verb.
   - Avoid overly long labels.
   - Maintain consistency in action labels across the application (e.g., use "Validate" consistently instead of using synonyms like "OK" or "Apply").
   - If an action requires an additional dialog step, follow the label with ellipses ("Confirm…").

B. Keyboard Shortcuts
   - Triggering an action via keyboard shortcut should not change its functioning mode.
   - If an action is inaccessible for any reason, the shortcut should produce a beep.
   - Standardize keyboard shortcuts for common actions like Copy (Ctrl + C), Paste (Ctrl + V), etc.

C. Forbidden or Unavailable Actions
   - Grey out options for context-dependent actions.
   - If an option is never accessible, do not display it or display it in grey.
   - Provide an auditory warning when a user attempts an unavailable action.

D. Backward Navigation
   - Users should be able to revert to the previous state after accidental actions or long processing actions.
   - Inform users of the consequences of potentially data-destructive actions and require explicit confirmation.

E. Default Actions
   - Default command buttons typically have a dark border and a dashed-line label.
   - When a window is minimized, its default actions should not be triggered.
   - Using the "Enter" key should activate the default action of the window or the action associated with the cursor position.
   - Avoid redundant command buttons if the action is already accessible via the menu.

#### 2. Menus

A. Menu Bar
   - Offer at least two menus (excluding the system menu) but no more than ten in the menu bar.
   - Assign keyboard shortcuts to all menus.
   - Menu bar menus should not contain direct actions; they should provide access to dropdown menus.
   - Use a single word for each menu label if possible.

B. Menu Options
   - Menu option labels can consist of multiple words but no more than four.
   - Add ellipses to the end of menu options if they require additional information to complete execution.
   - Dropdown menus should have at least two options but no more than ten per menu.

#### 3. Command Buttons

A. Button Presentation
   - If activating a command button opens a dialog window, add "..." to the end of its label.
   - Avoid whimsical dimensions for command buttons; represent them with rectangles.
   - Group buttons of similar functional nature and differentiate them from others.
   - Place window-wide command buttons at the bottom or vertically to the right of the client area.

B. Button Behavior
   - Propose a default command button, usually the one most likely to be chosen in the dialog context.
   - Use standard keyboard shortcuts for command buttons (e.g., Enter for default, Esc for cancel).
   - Common command buttons include Save, Cancel, OK, Apply, Close, Help, etc.
---

### V. System Actions

#### 1. Messages

A. General Recommendations
   - Messages should include:
     - A title bar indicating the message's origin.
     - An icon for visual identification of the message type.
     - Message text explaining the situation or posing a question.
     - Specific command buttons tailored to the message type.
   - Use unambiguous words familiar to the user.
   - Avoid formulating questions with only "yes" or "no" answers; prefer action verbs for responses.

B. Information or Warning Messages
   - Usage: These messages inform the user of the outcome of an action that poses no risk to the user, such as potential data destruction.
   - Operation: Only provide the user with the option to click on "OK".
   - This message box may be covered by another window.

C. Warning Messages
   - Usage: Warn in advance of an action that may be dangerous, allowing the user to proceed or cancel.
   - Operation: Offer the user a choice between two options (the message may be in the form of a question): 
     - Continue the task and take the risk.
     - Cancel the current action.
   - Note: If necessary, pair the display of the message box with a sound signal.

D. Confirmation Messages
   - Usage: Mandatory for irreversible operations; always a question.
   - Operation: Only give the user the option to click "Yes" or "No" (or their equivalents).
   - This message box cannot be covered by another window; the user must respond to continue their task.

E. Immediate/Blocking Stop Messages
   - Usage: To signal to the user that an action cannot be performed.
   - Use this type of message whenever the user attempts an unattainable action in the current context.
   - Operation: Only give the user the option to click "OK".

#### 2. Cursor/Pointer

- Change the cursor shape for wait times exceeding 1 second.
- Change the cursor shape to an hourglass when an action is initiated and no other action can be launched.
- Limit cursor shape modification to the active window directly related to the current task. Outside this window, the cursor should return to its normal shape.

#### 3. Response Times

A. Generalities
   - Response time indications:
     - 0.1 second: Beyond this delay, the user may feel the system is not responding instantly to their action.
     - 1 second: Beyond this delay, the user may feel they no longer control the system.
     - 10 seconds: Beyond this delay, the user loses attentiveness to the ongoing interaction. In this case, the system should display a visual feedback (progress indicator).

B. Progress Indicator
   - Visually inform the user of elapsed time using a progress indicator, especially for waits exceeding 6 seconds.
   - Inform the user of the reason for the system's response time (users will accept waiting more easily if they know why they are waiting).

#### 4. Sound Signal

- Avoid excessive use of sound signals.
- Offer the option to disable sound signals.
- If used, the signal should have the same meaning throughout the application and should be coupled with visual information.
- Sound signals can be used for:
  - Attempted forbidden or impossible actions by the user.
  - Associated with the display of a warning or action message window.
  - At the end of waiting for the completion of a long-duration task, represented by a progress indicator.

#### 5. Information Confidentiality

- Allow users to choose their password to aid in remembering it.
- Allow users to change their password whenever they want, in case they fear their password has been compromised.
- Do not display the password entered by the user (e.g., display * to indicate the number of characters entered).
- Limit the number of consecutive access attempts.
- After a period of inactivity, freeze the screen and require a new password entry. The duration of inactivity is determined by an analysis of the system's usage context.