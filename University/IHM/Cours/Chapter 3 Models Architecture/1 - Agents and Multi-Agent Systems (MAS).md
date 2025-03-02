### Agents and Multi-Agent Systems (MAS)

- **Agent**: 
  - An entity that acts autonomously to achieve its designated goals.
  - Can communicate with other agents.
  - Endowed with capabilities similar to living beings.
  - An agent can be a process, a server, a robot, a human, etc.

#### Properties of an Agent
- **Reactiveness**:
  - Ability to perceive the environment and respond in real-time to changes.
- **Sociability**:
  - Capacity to interact with other agents or users.
- **Proactivity**:
  - Capacity to take initiative and goal-oriented behavior.
- **Autonomy**:
  - Capacity to act without direct human intervention.

---

#### Multi-Agent Systems (MAS)
- A distributed system composed of:
  - A set of distributed agents,
  - Situated in a certain environment,
  - Interacting according to certain organizations.
- MAS allows solving complex problems by exploiting the collective intelligence of its constituent agents.

#### The Agent Model
- The Seeheim model has the major drawback of being a centralized system.
- The multi-agent model is a distributed system based on the principle of stimuli-response, with communications between agents established via events.
- An agent consists of:
  - Receivers that receive events from other agents, possibly accompanied by filters to be sensitive to certain types of events.
  - Emitters that transmit typed events to the system, not to a particular agent.
  - Memories to record detected events and to remember the agent's state.
  - A processor that processes events.

---

- An event is detected and captured by all agents whose active receptors at that moment are capable of intercepting it.
- This event is added to the queue of each agent that detected it.
- When its turn comes, the event processing causes a change in the agent's state, which can then emit new events.
- This operating mode allows working in multi-threaded dialogue by associating each thread with a specific agent, enabling a system supporting parallelism with distributed control rather than centralized control in a single component.

#### Implementation in Object-Oriented Languages
- The characteristics of multi-agent systems allow for good implementation in object-oriented languages.
- Each agent type corresponds to a class, with attributes representing the agents' memories, event processing operations stored as methods, and event communication replaced by message sending.
- The instantiation and inheritance capabilities of object-oriented languages enable dynamically creating agents, thus having an evolutionary system, as well as specializing agents compared to other agents.
- This similarity between object-oriented languages and multi-agent systems arises from the modularity and cooperation properties of object-oriented languages. An object is considered as an autonomous entity, just like an agent. Moreover, message communication (or event communication for agents) allows entities to communicate with each other.
- The concept of an agent has been used in several models, such as MVC and PAC.