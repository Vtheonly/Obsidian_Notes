### 1. The `Object` Class

In Java, inheritance is not optional. Every single class you create implicitly extends a specific class called `java.lang.Object`. If you write `class User {}`, the compiler treats it as `class User extends Object {}`.

**Implications:**
Because everything "is-a" Object, every class inherits a specific set of methods that define how objects behave in memory. The two most critical methods you must often take control of are `toString()` and `equals()`.

---

### 2. String Representation: `toString()`

#### **The Default Behavior**

When you print an object (e.g., `System.out.println(myUser);`), Java automatically calls `myUser.toString()`.

- **Default Implementation:** defined in the `Object` class.
- **Output:** `ClassName@HexadecimalHash` (e.g., `User@15db9742`).
  - This is the **memory address** hash. It is useful for the computer, but useless for a human debugger.

#### **Overriding for Clarity**

To make logs readable, you must apply **Polymorphism (Overriding)**. By defining your own `toString`, you intercept the call.

```java
@Override
public String toString() {
    // We construct a meaningful string state of the object
    return "User[Name: " + this.name + ", Membership: " + this.membership + "]";
}
```

> [!TIP] **Polymorphism in Action**
> In the Inventory Project (File 1), the `Inventory` class loops through a list of `Item` objects. Even though the list is typed as `Item`, when `System.out.println(item)` is called:
>
> - If the object is a `Weapon`, Java runs `Weapon.toString()`.
> - If the object is a `Fruit`, Java runs `Fruit.toString()`.
> - This decision happens at **Runtime** (Runtime Polymorphism).

---

### 3. Object Equality: `==` vs `.equals()`

This is one of the most common sources of bugs for beginners.

#### **The `==` Operator (Reference Comparison)**

- **Primitive Types (`int`, `char`):** Compares the actual value (e.g., is 5 equal to 5?).
- **Reference Types (Objects):** Compares the **memory address**.
  - It asks: "Are these two variables pointing to the exact same physical location in RAM?"

#### **The `.equals()` Method (Logical Comparison)**

- **Default Behavior:** In the `Object` class, `.equals()` just calls `==`. It checks memory addresses.
- **Desired Behavior:** We usually want to check **content equality**. "Do these two users have the same ID and Name?"

To achieve this, we override `.equals()`.

**Mermaid Diagram: Reference vs. Content Equality**

```mermaid
graph TD
    subgraph Memory
        Loc1[Address: 0x001<br>User: Caleb]
        Loc2[Address: 0x002<br>User: Caleb]
    end

    VarA(User A) --> Loc1
    VarB(User B) --> Loc2
    VarC(User C) --> Loc1

    check1{A == B?}
    check2{A == C?}
    check3{A.equals(B)?}

    check1 -- False --> Res1[Different Addresses]
    check2 -- True --> Res2[Same Address]
    check3 -- True --> Res3[Same Data Content]

    style Res3 fill:#bbf,stroke:#333,stroke-width:2px
```

#### **The HashCode Contract**

> [!CRITICAL] **The Rule of HashMaps**
> If you override `equals()`, you **must** override `hashCode()`.
>
> - **Reason:** Collections like `HashMap` and `HashSet` use the hash code to organize storage buckets.
> - **The Contract:** If `A.equals(B)` is true, then `A.hashCode()` **must** equal `B.hashCode()`. If you break this, your objects will get lost inside HashMaps.
