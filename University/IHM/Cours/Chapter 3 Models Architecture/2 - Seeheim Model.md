
### Software Architecture

- A software architecture describes symbolically and schematically the various elements of one or more computer systems, their interrelationships, and interactions.
- Fundamental principle: separation between interface and functional core (set of services specific to an application).
- Different models:
  - Fundamental model
  - Seeheim model
  - Model-View-Controller (MVC)
  - Presentation-Abstraction-Control (PAC)
  - And others.

### Fundamental Architecture

- **Functional Core**:
  - It must provide a minimum of services within the framework of an interface:
    - **Notification**: Ability for an external module to be notified when the state of the semantic core changes (data and processing).
    - **Error Prevention**: Ability to determine if a function call is valid in a certain context (not with exceptions, functions for testing).
    - **Cancellation**: Ability to revert to previous states of the semantic core, avoiding simulation at the interface level (e.g., undoing a database transaction, history).

---

### Seeheim Model

- The Seeheim model is the first model to highlight the dialogue controller by separating an application into three modules.
- Historical Role: Software model allowing the replacement of text interfaces with graphical interfaces without changing the functional core.
- The purpose of this model is to distinguish dialogue management from application semantics.
- It consists of three modules grafted onto the application core. Each of these modules is distinct and has well-defined roles.

#### Presentation:
- Responsible for purely lexical management of the application (i.e., manages I/O, display, interaction).
- Its role is to:
  - Manage the presentation and display of manipulated entities, meeting criteria of ergonomics and usability.
  - Manage physical input/output events, translating information between the format of the external real world and the internal computing world.
  - Therefore, presentation handles the external representation of the application.

#### Application Interface:
- A layer connecting the functions and data of the functional core to the data and actions of the interface.
- Its role is to:
  - Connect the functional core and the dialogue control module by calling application procedures.
  - Convert information from the dialogue controller into manipulable concepts by the application.

#### Dialogue Controller:
- Acts as the mediator between the user and the application, i.e., between the presentation and the application interface.
- Its role is to:
  - Control exchanges at the syntactic level (dialogue processing and sequencing) and manage dialogue dynamics.
  - Coordinate between display (presentation) and processing progress.

- Implementing this model presents difficulties as the roles of the modules are not sufficiently explicit.
- It does not perfectly match object-oriented and event-driven programming models, which advocate for control distribution among manipulated objects.
- Therefore, this model has given rise to several models and "improved" versions (e.g., "Modified Seeheim", "Extended Seeheim").
