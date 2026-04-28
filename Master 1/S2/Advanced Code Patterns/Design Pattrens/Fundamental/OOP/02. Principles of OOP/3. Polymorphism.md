### 1. Definition and Etymology

Polymorphism comes from Greek: _Poly_ (Many) + _Morph_ (Forms).
In Java, it allows an object to take on many forms. A `Student` object is a `Student`. It is also a `User`. It is also an `Object`.

Polymorphism allows us to write flexible code. We can write code that handles the _general_ type (`User`), and it will automatically handle any new _specific_ types (`Student`, `Teacher`, `Admin`) we invent in the future without changing the original code.

---

### 2. Compile-Time Polymorphism (Method Overloading)

This happens when you write the code. The compiler figures out which method to use based on the **Method Signature**.

**Method Signature = Method Name + Parameter List (Types and Order).**

- Return type is **NOT** part of the signature. You cannot overload just by changing `void` to `int`.

**Example: The `add` Method**

- `add(int a, int b)`
- `add(double a, double b)`
- `add(String a, String b)`

**Why use it?**
It improves code readability. You don't need `addInts()`, `addDoubles()`, `addStrings()`. You just use `add()`, and the compiler routes it to the correct logic.

---

### 3. Run-Time Polymorphism (Method Overriding)

This is the "True" polymorphism in OOP. It happens when the program is actually running.

#### **A. The Mechanics**

1.  **Inheritance:** You must have a Parent and Child.
2.  **Override:** The Child must re-declare a method that exists in the Parent with the **exact same signature**.
3.  **Upcasting:** You reference the Child object using a Parent variable.

#### **B. The `@Override` Annotation**

Technically optional, but **mandatory for good code**.

- It tells the compiler: "I intend to replace a parent method."
- **Safety Check:** If you make a typo (e.g., `tostring()` instead of `toString()`), the compiler will scream at you. Without the annotation, Java would treat `tostring()` as a brand new method, and your polymorphism would silently fail.

#### **C. Dynamic Binding (The Magic)**

```java
User u = new Student();
u.login();
```

- **Compile Time:** The compiler looks at reference `u` (Type `User`). It checks: "Does `User` have a `login()` method?" Yes. It passes compilation.
- **Run Time:** The JVM looks at the **Heap Memory**. It sees that the actual object created is a `Student` object. It ignores the `User` version of `login()` and executes the `Student` version.

**Visualizing Dynamic Binding**

```mermaid
graph TD
    Reference[Variable 'u' (Type: User)] -->|Points to| HeapObject[Object (Type: Student)]

    HeapObject -->|Method Call| StudentLogin[Student.login()]
    HeapObject -.->|Overrides| UserLogin[User.login()]
```

---

### 4. Polymorphism in Collections (The Ultimate Use Case)

The most powerful application of polymorphism is grouping different objects together.

**Scenario:** A Payroll System.

- Classes: `FullTimeEmployee`, `PartTimeEmployee`, `Contractor`.
- All extend `Employee`.
- All override `calculatePay()`.

```java
// We create a list of the Parent Type
ArrayList<Employee> staff = new ArrayList<>();

staff.add(new FullTimeEmployee());
staff.add(new Contractor());

// We iterate using the Parent Type
for (Employee e : staff) {
    // POLYMORPHISM IN ACTION:
    // e.calculatePay() does something different for each person!
    // We don't need 'if' statements to check what kind of employee they are.
    e.calculatePay();
}
```

If we add a new class `Intern` next year, this loop **does not need to change**. This is the "Open-Closed Principle" (Open for extension, closed for modification).
