### PAC (Présentation Abstraction Contrôle) Model

#### Overview
- PAC is a multi-agent model where each agent is responsible for a specific aspect of the application's functionality, composed of three components: presentation, abstraction, and control.

#### Components
- **Presentation**: Represents the user's perception of the agent.
  - Corresponds to the external representation of the agent.
  - Defines the perceivable behavior of the agent and interaction with the user.
- **Abstraction**: Represents the concepts and functions of the agent.
  - Defines the semantic functionalities of the agent.
  - Represents the expertise of the agent and manages the data to be represented.
- **Control**: Maintains coherence between Presentation and Abstraction.
  - Establishes a link between these two parts while arbitrating conflicts, synchronizations, refreshes, etc.
  - Acts as a translator since the three components exchange information that may have different formats.
  - Manages the correspondence between Abstraction and Presentation (consistency of representations with internal data, conversion of user actions into operations of the functional core) and handles relationships with other PAC agents in the hierarchy.

#### Object Structure
- A simple interactive PAC object consists of an image defining the behavior visible to the user (Presentation) of the functions it uses (Abstraction) and a module to manage the connection between these two modules (Control).

#### Application Structure
- An application based on the PAC model consists of a set of hierarchically and recursively structured PAC agents.
- PAC agents can be decomposed into a set of PAC agents.
- In the figure, the top object in the hierarchy corresponds to the three main parts of the application, with sub-levels being intermediate objects and leaves being the most elementary directly manipulable objects.
- A parent object inherits Presentations from its children, not vice versa.

#### Example: Air Traffic Control System
- A classic example of a PAC architecture is an air traffic control system.
- A PAC agent takes inputs from a radar system on the location of an incoming 747 and uses the Presentation component to paint a spot on the screen.
- Another agent independently takes information on a departing DC-10 and also paints this spot on the screen.
- Another agent takes meteorological data and paints clouds, while another follows the incoming enemy bomber and paints a red spot. 

#### Conclusion
- PAC provides a structured approach to application design by separating presentation, abstraction, and control components.
- It allows for hierarchical and recursive organization of agents, facilitating complex system design and management.
