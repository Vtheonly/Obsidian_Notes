### 1. The Concept of Abstraction

Abstraction is the process of stripping away complexity.

- **User's View:** I press a button, the engine starts.
- **Engineer's View:** Fuel injection, spark plugs, combustion.

In Java, Abstraction allows us to define **templates** for classes. We force child classes to follow a specific design without telling them _how_ to implement the details.

---

### 2. Abstract Classes

An `abstract class` is a class that is "half-complete."

#### **A. Rules of Abstract Classes**

1.  **Keyword:** `public abstract class Item`.
2.  **Instantiation:** You **cannot** say `new Item()`. It is an incomplete blueprint. You can only instantiate concrete subclasses (e.g., `new Weapon()`).
3.  **Constructors:** Even though you can't instantiate it, it **can** have a constructor. This constructor is called by the child class via `super()` to initialize the variables defined in the abstract class (like `name` or `id`).
4.  **Mixture of Methods:** It can contain:
    - **Concrete Methods:** Fully written methods (e.g., `getName()`) that children inherit as-is.
    - **Abstract Methods:** Methods with no body (e.g., `abstract void use();`).

#### **B. The Abstract Method**

`public abstract void attack();`

- It has no curly braces `{}`. It ends with a semicolon.
- **The Contract:** Any concrete class that extends this **MUST** override and write the code for `attack()`. If it doesn't, the compiler throws an error.

---

### 3. Interfaces

An `interface` is a pure abstraction (historically). It is a contract of capabilities.

#### **A. Rules of Interfaces**

1.  **Keyword:** `interface`.
2.  **Relationships:** Classes `implement` interfaces.
3.  **Variables:** All variables declared in an interface are implicitly `public static final` (Constants). You cannot have instance variables like `int x` in an interface.
4.  **Methods:** All methods are implicitly `public abstract`. (Java 8/9 added `default` and `static` methods, but conceptually, stick to the abstract idea for core OOP).

#### **B. Multiple Inheritance (The Solution)**

While a class can only extend **one** parent class, it can implement **unlimited** interfaces.
`public class Amphibian implements Swimmable, Walkable`

This solves the Diamond Problem. Since interfaces (usually) don't have implementation logic, there is no conflict if two interfaces define the same method name. The class simply implements the logic once.

---

### 4. Abstract Class vs. Interface: How to Choose?

This is a classic interview question and architectural decision.

| Feature          | Abstract Class                                 | Interface                           |
| :--------------- | :--------------------------------------------- | :---------------------------------- |
| **Relation**     | **"Is-A"** (Identity)                          | **"Can-Do"** (Capability)           |
| **State**        | Can hold state (variables like `name`, `age`). | Cannot hold state (only constants). |
| **Constructors** | Yes.                                           | No.                                 |
| **Inheritance**  | Single (Extends one).                          | Multiple (Implements many).         |
| **Speed**        | Slightly faster (direct binding).              | Slightly slower (search required).  |

**Scenario Guide:**

1.  **Use Abstract Class when:**
    - You have a clear hierarchy (e.g., `Animal` -> `Dog`).
    - You want to share code (variables and methods) across all children.
    - You need to control the initialization via constructors.

2.  **Use Interface when:**
    - You want to define a capability that applies to unrelated objects (e.g., `Serializable`, `Cloneable`, `Flyable`).
      - A `Bird` is an animal that can fly.
      - A `Airplane` is a vehicle that can fly.
      - They share no parent class, but they both implement `Flyable`.
    - You need to simulate multiple inheritance.
    - You want to decouple your system (Dependency Injection often relies on interfaces).
