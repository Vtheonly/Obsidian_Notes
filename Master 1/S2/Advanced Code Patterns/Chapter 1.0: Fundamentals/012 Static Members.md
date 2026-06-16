---
tags: [static-member, static-method, static-variable]
aliases: [static member, static method, static variable]
keywords: [static member, static method, static variable]
---
### 1. Instance vs. Static

- **Instance (Non-static):** Belongs to the specific [[002 Object|object]]. Every object has its own copy.
  - _Example:_ `name`. Caleb has a name, Sally has a different name.
- **Static:** Belongs to the **[[005 Intro to Classes|Class]]** itself. There is only one copy shared by _all_ objects.

### 2. Static Variables

Useful for shared data or constants.

```java
public class User {
    String name; // Instance variable
    static List<User> admins = new ArrayList<>(); // Static variable
}
```

- **Accessing:** You access it via the Class name, not the object variable.
  - Correct: `User.admins.add(u);`
  - Incorrect (but technically works): `u.admins.add(u);` (This is confusing).

### 3. Static Methods

A method that can run without creating an object.

- **Example:** `public static void printAdmins()`
- **Constraint:** A static method **cannot** access instance variables (like `name`) directly, because it doesn't know _which_ user's name you are talking about. It can only access static variables.

> [!NOTE] **Main Method**
> `public static void main` is static because the Java Virtual Machine (JVM) needs to run it to start the program _before_ any objects exist.


---
**Keywords:** #static-member, #static-method, #static-variable
