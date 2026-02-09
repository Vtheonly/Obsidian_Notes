### 1. Static: Class-Level vs. Object-Level

The `static` keyword changes the _scope_ and _memory allocation_ of a member.

| Feature        | Instance Member (No static)           | Static Member                      |
| :------------- | :------------------------------------ | :--------------------------------- |
| **Belongs To** | The specific Object (e.g., User A)    | The Class (User Class blueprint)   |
| **Memory**     | Allocation per object created         | Allocation happens once at startup |
| **Access**     | `object.variable`                     | `ClassName.variable`               |
| **Lifecycle**  | Dies when object is garbage collected | Lives until program terminates     |

**Why `main` is static:**
`public static void main(String[] args)` is the entry point. The Java Virtual Machine (JVM) calls this method _before_ any objects have been created. Since no objects exist yet, the method _must_ be static to be callable on the class itself.

**The "Static Trap":**
A static method **cannot** access instance variables (non-static fields).

- _Reasoning:_ A static method belongs to the class blueprint. If the blueprint tries to access `name`, it doesn't know _whose_ name (User A's? User B's?) it refers to.

### 2. Final: The Immutable Modifier

- **Final Variable:** The value cannot be changed once assigned. It is a constant.
  - _Interface variables_ are implicitly `public static final`.
- **Final Method:** Cannot be overridden by a subclass. This is used for security (preventing hackers from changing critical logic in a subclass).
- **Final Class:** Cannot be inherited from (e.g., the `String` class in Java is final).

### 3. Abstract vs. Interface (The Deep Dive)

Both provide abstraction, but the mechanics differ.

#### **Abstract Class**

- **The "Partial Blueprint":** Can have fully working methods _and_ abstract methods (methods with no body).
- **State:** Can hold member variables (state) like `int speed` or `String name`.
- **Constructor:** Can have a constructor (called via `super()`), even though you can't instantiate it directly.
- **Usage:** Use when classes share a core identity ("Is-A"). A `Weapon` _is an_ `Item`.

#### **Interface**

- **The "Contract":** Traditionally contains _only_ method signatures (Java 8+ allows `default` methods).
- **No State:** Cannot hold instance variables (only constants).
- **Multiple Inheritance:** A class can implement **multiple** interfaces. This solves the "Diamond Problem" (where a class doesn't know which parent's method to inherit). Since interfaces have no implementation, there is no conflict.
- **Usage:** Use to define capabilities ("Can-Do"). A `Bird` and an `Airplane` are unrelated, but both implement `Flyable`.

**Project 3 (Calculator) Strategy:**
The calculator uses an Interface `Operate` with a method `getResult()`.

- `Add implements Operate`
- `Multiply implements Operate`
- **Benefit:** The main calculator loop doesn't care if it's adding or dividing. It treats _everything_ as an `Operate` type. This is **decoupling**.
