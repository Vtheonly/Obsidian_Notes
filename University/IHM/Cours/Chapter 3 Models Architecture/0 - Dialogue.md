
### 1.1. What is Dialogue?

#### Definition 1
- Dialogue is the set of exchanges between a user and a machine.
- This includes interactions such as using a touch screen, a microphone, a scanner, etc.

#### Definition 2
- Dialogue is the set of interactions produced by a human on a computer.
- An interaction is an action that provokes a perceptible reaction.
- This includes actions such as mouse clicks, keystrokes, touch screen presses, etc.
- This is the most common definition in HCI (Human-Computer Interaction).

#### Definition 3
- Dialogue is the use of natural language to work on a computer.
- This restrictive definition applies only to the field of natural language research.
- The goal is to work with a machine through commands given in everyday language, with the computer responding in the same language.
- This can be done in several ways: written, oral, or both.

---

### Dialogue Controller

#### Definition
- The Dialogue Controller is the module (or set of modules) dedicated to managing dialogue.
- This module has two main roles: dialogue analysis and dialogue control.

---

#### a. Dialogue Analysis

- Three types of analysis are distinguished:
  1. **Lexical Analysis**: Manages I/O, display, interaction.
  2. **Syntactic Analysis**: Handles dialogue processing and sequencing.
  3. **Semantic Analysis**: Analyzes concepts manipulable by the application.
  
- Most application models associate each type of analysis with a module, sometimes grouping them into a single module.

---

#### b. Dialogue Control

- Control corresponds to the validity of triggering operations depending on the context (data, previous processes, etc.).
- Dialogue control also means managing the sequencing of operations following user interactions.
- In summary, the dialogue controller verifies the validity of interactions and manages the sequencing of resulting processes.

#### Examples

1. **Button State**:
   - A non-grayed button means it can be activated, while a grayed button means it cannot.
   - The interface is informed of the button's state based on data and previous operations managed by the controller.

2. **Operation Sequencing**:
   - Completing one operation allows for the execution of others, which should be reflected on the screen (e.g., making a menu, button, or input field accessible).
   - It is important for the controller to know the necessary sequences to achieve goals.