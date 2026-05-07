### 1. What is a Constructor?

A Constructor is a **special method** used to initialize objects. It is called immediately when you use the `new` keyword.

**Key Characteristics:**

1.  **Name:** Must match the Class name exactly.
2.  **Return Type:** It has **no return type** (not even `void`).
3.  **Execution:** Runs only once per object creation.

---

### 2. Types of Constructors

#### **A. The Default Constructor**

If you do not write _any_ constructor in your class, Java provides a invisible "Default Constructor" that takes no arguments.

- It initializes numbers to `0`, booleans to `false`, and objects to `null`.

#### **B. Parameterized Constructor**

This allows you to force data input when creating an object. This prevents "half-baked" objects (e.g., a User without a name).

```java
public class User {
    String name;
    String membership;

    // Custom Constructor
    public User(String name, String membership) {
        this.name = name;
        this.membership = membership;
    }
}
```

**Usage:**

```java
// We are now FORCED to provide data to create a User
User u = new User("Caleb", "Gold");
```

> [!WARNING] **The Disappearing Default Constructor**
> The moment you write _any_ custom constructor (e.g., one that takes arguments), Java **removes** the automatic default constructor.
>
> If you still want to allow `new User()` (empty), you must manually type out the empty constructor: `public User() {}`.

---

### 3. The `this` Keyword

In the constructor example above, you see `this.name = name`.

- **The Problem (Shadowing):** The parameter `name` (passed in) has the exact same spelling as the class attribute `name`. Java prefers the "closest" variable (the parameter).
- **The Solution:** `this` represents the **current object**.
  - `this.name`: Refers to the attribute belonging to the object being created.
  - `name`: Refers to the parameter passed into the constructor.
