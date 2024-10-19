
**Human-Machine Interaction**

**Definition:**
"**Human-machine interactions** (**HMI**) define the means and tools implemented so that a **human** can **control** and **communicate** with a **machine**."

**Areas of Interest:**

The field is interested in:

1. The way **humans interact** with **computers** or with each other using computers, as well as,
2. The way to design systems that are:
    - **Ergonomic**
    - **Efficient**
    - **Easy to use**
    - Or more generally **adapted to their context of use**

**Ways of Human-Computer Communication**

1. **Punched Cards**
   - The earliest computers were fed **input** through **instructions coded** on **punched cards**
   - **Output data** was provided on **printers**
   - Example: **Programmable automata**

2. **WIMP**
   - A **pointing system** like the **mouse** allows using a computer with the **WIMP paradigm**
   - WIMP = **Window Icon Menu Pointer**
   - Relies on **graphical user interfaces** to present **information** to the **user**

3. **Voice Command & Gestures**
   - **Automatic speech** or **gesture recognition** allows sending **information** to a computer
   - **Speech synthesis** allows sending **audio signals** understandable by humans
   - **Data gloves** offer more direct interaction than the mouse

4. **Virtual Reality**
   - **Visors** try to **immerse** the human in a **virtual reality**
   - Or **augment reality**

5. **Touch Tables & Smartphones**
   - **Interactive tables** allow coupling direct **human manipulation** on a surface with **information feedback**

**More Ways:**

1. **Command line** (e.g. Unix, Linux)
2. **Query languages** and **question-answering** (e.g. dialog boxes)
3. **Selection forms**
4. **Natural language** (written, speech)
5. **3D interfaces**, gestural, augmented reality
6. **Direct navigation** (e.g. websites)
7. **Direct manipulation WYSIWYG** ("What You See Is What You Get") - Ben Shneiderman (1983)
    - Examples: Word, Paint

----

**Delays in System Development**

The delay in the development of many operational systems is attributable to a lack of knowledge about the actual use and user of the final system, leading to the delivery of an initial version poorly adapted to the user's needs or even the operational context. The adjustment work carried out afterwards results not only in unforeseen developments, a source of budget overruns, but also in difficult acceptance of the system linked to secondary adaptations.

**Definition of Human-Machine Interface**

In a computer system, the **Human-Machine Interface (HMI)** represents the part of the software that allows the **user** to **interact** with the computer program and for the program to **communicate results** to the user.

The challenge is to develop an interface that can be easily used by a given person to perform the task for which it was designed. This includes both:

1. Task performance
2. The satisfaction provided by using the object
3. The ease with which one learns to use it

A user-friendly software will allow the intended task to be performed quickly, without wasting time and with less stress.

**Interface and Learning**

Goal of the interface: facilitate learning the software i.e. bring the user's mental model closer to the conceptual model.

**Cognitive Factors:**
- Learning by doing (trial-and-error, guidance, online help)
- Theoretical learning (rigorous, complete, solid manual)  
- Learning by analogy (metaphors, examples)

**Personality Factors:**
- Introverts, extraverts (different exploration methods)
- Anxious (a lot of feedback)
- Impulsive (short messages, error recovery)

**Usability of HMIs**

Wikipedia: The degree to which a product can be used by identified users to achieve defined goals with effectiveness, efficiency and satisfaction in a specified context of use.

The usability criteria are:
- **Effectiveness**: The product allows its users to achieve the intended result
- **Efficiency**: Achieves the result with less effort or requires minimal time
- **Satisfaction**: Comfort and subjective evaluation of the interaction for the user

**Solution**: User-centered design

---
**Ergonomic Criteria**

1. **Consistency**: The same concept must always be used in a similar way in an identical context of use.

2. **Concision**: Limitation of the number of user interventions to avoid errors (e.g. typographical errors, default value, copy/paste, abbreviation, grayed-out option, selection, ctrl+z and ctrl+y, etc.).

3. **Feedback**: Any user action must provide rapid and relevant feedback to allow them to quickly analyze the new state of the application. The feedback must be immediate and informative: the psychological variables, the user's areas of interest, must find their counterpart in the physical variables of the image.

4. **Structured Activities**: The application must be decomposed according to a hierarchy of increasing levels of complexity. 

5. **Flexibility**: Any application must be easily customizable by users. A modifiable interface through explicit user intervention.

6. **Error Management**: The user must be guided towards a method allowing them to solve their problem.

**Major Milestones in HMI History**

1. **1945: Memex (Vannevar Bush)**
    - Envisioned Memex, an external memory instrument
        - An electromechanical system to store books, notes, archives, etc.
        - A system of keywords, cross-references and indexing mechanisms for quick information access
        - Ability to annotate stored documents and save a "trail" (a chain of links)

2. **1963: Sketchpad (Ivan Sutherland, MIT)** 
    - Sketchpad, a cutting-edge drawing tool
        - Oscilloscope, light pen and buttons
        - Direct designation of objects on screen
        - Feedback in the form of elastic lines  
        - Separation between screen and drawing coordinates
        - Zoom in and out (factor 2000!)
        - Hierarchical structure, recursive operations
        - Constraint management system
        - Icons to represent complex objects

3. **1962/64: NLS/Augment (Douglas Engelbart)**
    - Mouse
    - "High resolution" screen
    - Word processing
    - Hypertext and hypermedia
    - Email
    - Video conferencing 
    - Groupware...

4. **1969, 1970: Xerox PARC (Palo Alto, CA)**
    - Brought together diverse talents interested in photocopying but also office systems
        - Part of Engelbart's team from SRI
        - Alumni from Berkeley Timesharing System
        - Others like Alan Kay
    - Notable achievements:
        - Laser printer
        - Object-oriented programming
        - Personal computer
        - Ethernet
        - Automatic natural language processing

5. **1981: Xerox Star**
    - Key features:
        - Hardware design guided by software needs (task analysis, scenarios, 600-700 hours of video)
        - Naturally networked system  
        - Graphical interface based on desktop metaphor
        - Use of icons, windows and WYSIWYG concept
        - Document-centric system (user doesn't know applications)
        - Restricted set of generic commands accessible by specific keys

6. **1981: Xerox Star (Contd.)**
    - Microcoded CPU less powerful than 1 MIPS  
    - 385KB memory
    - Ethernet connection
    - Storage: 10-40MB hard drive, 8-inch floppy drive
    - Interaction: 17-inch B&W screen, 2-button mouse, special keyboard

7. **Commercial Failure but Influential**
    - Too new, powerful, different system
    - Poorly evaluated target market (e.g. no spreadsheet)
    - Too expensive ($16,500)
    - Closed architecture (no external app development)
    - Lack of will to move beyond photocopiers?
    - But influenced current systems

8. **1984: Apple Macintosh**
    - Menu bar, modal dialog boxes, visible apps inherited from Apple Lisa
    - Commercial success  
        - More mature ideas, market ready to accept them
        - Aggressive pricing ($2,500) for mass market
        - Toolbox to facilitate external development
        - Detailed style guides for app consistency
    - Three key apps:
        - **Finder**
        - **MacPaint**
        - **MacWrite**

10. **1985: X Window System (MIT)**
    - Aimed to connect UNIX machines provided by numerous sponsors (DEC, IBM, Motorola, etc.)
    - Client/server model
        - Separation of what/how facilitating portability
        - Transparent network usage allowing remote display
    - Separation of mechanisms and usage policy

11. **1985 to Present: Microsoft Windows**
    - Microsoft's graphical operating system and user interface

12. **1990: World Wide Web (CERN)** 
    - Network hypertext model
    - Became hypermedia and public with Mosaic (ancestor of Netscape, Mozilla, Firefox)
    - Paper was rejected by the prestigious "ACM Hypertext" conference!

13. **1995: Java (Sun Microsystems)**
    - Object-oriented programming language
    - Enabled rich internet applications and applets

14. **2007: Multi-Touch (Apple iPhone)**
    - Intuitive direct manipulation interface
    - Sparked touchscreen revolution across devices

15. **2010s: Voice Interfaces (Siri, Alexa, Google Assistant)**
    - Natural language voice control 
    - Hands-free interaction paradigm

16. **Present & Future: Augmented & Virtual Reality**
    - Immersive experiences blending digital and physical
    - New frontiers for human-computer interaction

