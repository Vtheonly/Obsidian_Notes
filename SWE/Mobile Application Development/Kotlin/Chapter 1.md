Excellent! This is a fantastic way to learn. By building a structured knowledge base from the start, you'll have a powerful reference for the future. I'll act as your Kotlin tutor and present each lesson in the requested Obsidian note format.

Let's begin with the absolute fundamentals. For a Java developer, the most immediate changes are how you declare variables and how the language fundamentally handles `null`.

Here is your first lesson.

***

# Chapter 1: Variables, Data Types, and Null Safety

#tags: #kotlin #fundamentals #variables #data-types #null-safety #java-comparison

Welcome to Kotlin! As a Java developer, you'll find many similarities, but Kotlin introduces powerful features that make code safer and more concise. This first chapter covers the most foundational concepts: declaring variables, understanding basic data types, and mastering Kotlin's famous **null safety** system.

---

## I. Variable Declaration: `val` vs. `var`

In Java, you declare a variable with its type first (e.g., `String name = "Java";`). Kotlin simplifies this with two keywords: `val` and `var`.

### A. `val` — The Immutable Variable
*   `val` stands for *value*. It creates a **read-only** or *immutable* variable.
*   Once a value is assigned to a `val`, it **cannot be changed**.
*   This is the direct equivalent of using the `final` keyword in Java.
*   **Best Practice:** You should *always* prefer `val` over `var` unless you have a specific reason to change the variable later. This promotes immutability, which makes your code safer and easier to reason about.

```kotlin
// Declaring a 'val'
val name: String = "Kotlin" 

// You cannot reassign a 'val'
// name = "Java" // This will cause a COMPILE ERROR: "Val cannot be reassigned"

val pi = 3.14 // Type is inferred as Double
val question = "The Ultimate Question" // Type is inferred as String
```

### B. `var` — The Mutable Variable
*   `var` stands for *variable*. It creates a **mutable** variable.
*   You can change the value of a `var` at any time, as long as the new value is of the same type.
*   This is like a standard, non-final variable declaration in Java.

```kotlin
// Declaring a 'var'
var score: Int = 0
println(score) // Prints 0

// You can reassign a 'var'
score = 100
println(score) // Prints 100

// But you cannot change its type
// score = "one hundred" // COMPILE ERROR: Type mismatch
```

---

## II. Basic Data Types

A key difference from Java is that **in Kotlin, everything is an object**. There are no primitive types like `int`, `double`, or `boolean`. Instead, you use classes like `Int`, `Double`, and `Boolean`. The compiler handles optimizing this down to primitives behind the scenes for performance.

| Type      | Description                               | Size (bits) | Java Equivalent          |
| :-------- | :---------------------------------------- | :---------- | :----------------------- |
| `Int`     | A 32-bit signed integer.                  | 32          | `int`, `Integer`         |
| `Long`    | A 64-bit signed integer.                  | 64          | `long`, `Long`           |
| `Double`  | A 64-bit double-precision floating point. | 64          | `double`, `Double`       |
| `Float`   | A 32-bit single-precision floating point. | 32          | `float`, `Float`         |
| `Boolean` | Represents `true` or `false`.           | ~           | `boolean`, `Boolean`     |
| `Char`    | A single character (enclosed in `' '`).   | 16          | `char`, `Character`      |
| `String`  | A sequence of characters.                 | ~           | `String` (immutable)     |

---

## III. Type Inference

Kotlin's compiler is smart. In most cases, you don't need to explicitly declare the type of a variable. The compiler can *infer* it from the assigned value. This makes the code cleaner and more concise.

```kotlin
// Explicit type declaration
val explicitInt: Int = 10
val explicitString: String = "Hello"

// Inferred type (preferred when the type is obvious)
val inferredInt = 10           // Compiler knows this is an Int
val inferredString = "Hello"   // Compiler knows this is a String
val inferredDouble = 10.5      // Compiler knows this is a Double
```
*You only need to declare the type explicitly when the compiler can't infer it, or for clarity in more complex situations.*

---

## IV. The Core of Kotlin: Null Safety

Java's biggest weakness is the `NullPointerException` (NPE), often called the "billion-dollar mistake." Kotlin solves this at the compiler level by building nullability directly into its type system.

### A. Non-Nullable Types (The Default)
By default, variables in Kotlin **cannot hold `null` values**. This is a massive safety feature.

```kotlin
var name: String = "Alice"
// name = null // COMPILE ERROR!

// The compiler prevents you from assigning null, eliminating NPEs at the source.
```

### B. Nullable Types (The Question Mark `?`)
To allow a variable to hold `null`, you must explicitly declare it as *nullable* by appending a question mark `?` to the type.

```kotlin
var middleName: String? = "B." // This variable CAN hold a String or null
println(middleName) // Prints "B."

middleName = null // This is now perfectly legal
println(middleName) // Prints "null"
```

### C. Working with Nullable Types
The compiler forces you to handle the possibility of `null` before you can use a nullable variable. This prevents NPEs at runtime.

#### 1. The Safe Call Operator: `?.`
This is the most common and elegant way to handle nulls. It executes the action only if the value is *not* null; otherwise, it returns `null` and does nothing.

```kotlin
val nullableName: String? = null

// In Java, this would crash if nullableName is null:
// int length = nullableName.length(); // Throws NullPointerException

// In Kotlin, use the safe call operator:
val length = nullableName?.length // If nullableName is null, 'length' becomes null. No crash.
println(length) // Prints "null"

val realName: String? = "Bob"
val realLength = realName?.length // If realName is "Bob", 'realLength' becomes 3.
println(realLength) // Prints "3"
```

#### 2. The Elvis Operator: `?:`
This operator is often used together with the safe call. It provides a default value to use if the expression on its left side results in `null`. *(If the value is not null, it looks like Elvis Presley's hair `?:`)*

```kotlin
val name: String? = null

// If name?.length is null, use the value -1 instead.
val length = name?.length ?: -1 

println(length) // Prints "-1"
```

#### 3. The "Not-Null Assertion" Operator: `!!`
This is the "I know what I'm doing" operator. It forcibly converts a nullable type to its non-nullable version. **If the value is actually `null` at runtime, it will throw a `KotlinNullPointerException`**.

***Warning:*** *Avoid using the `!!` operator where possible. It defeats the purpose of Kotlin's null safety system. Use it only when you are 100% certain that a value will not be null.*

```kotlin
val name: String? = "Carol"
val length = name!!.length // This is okay because name is not null.

val nullName: String? = null
// val badLength = nullName!!.length // This WILL CRASH with a KotlinNullPointerException
```

#### 4. Smart Casts
The Kotlin compiler is smart enough to know when you've performed a null check. Inside the scope of that check, it will automatically treat the nullable variable as a non-nullable one.

```kotlin
fun printNameLength(name: String?) {
    if (name != null) {
        // Inside this 'if' block, the compiler SMART CASTS 'name' to a non-nullable String.
        // You don't need ?. or !!
        println("Name length is ${name.length}") 
    } else {
        println("Name is null.")
    }
}
```

---

## V. String Templates

Kotlin makes string formatting much cleaner than Java's concatenation. You can embed variables and expressions directly into a string using the `$` symbol.

```kotlin
val name = "World"
val score = 42

// Simple variable template
println("Hello, $name!") // Prints "Hello, World!"

// Expression template with curly braces {}
println("Your score is ${score * 2}") // Prints "Your score is 84"
println("First letter of your name is ${name[0]}") // Prints "First letter of your name is W"
```

---

## VI. Quick Reference: From Java to Kotlin

| Java Concept                        | Kotlin Equivalent                                                              | Example                                             |
| :---------------------------------- | :----------------------------------------------------------------------------- | :-------------------------------------------------- |
| `final String name = "A";`          | **`val`** (Immutable)                                                          | `val name = "A"`                                    |
| `String name = "B";`                | **`var`** (Mutable)                                                            | `var name = "B"`                                    |
| `int x = 10;`                       | Object Type (`Int`) with Type Inference                                        | `val x = 10`                                        |
| `String str = null;`                | Must be explicitly marked as **nullable (`?`)**                                | `val str: String? = null`                           |
| `if (str != null) { str.length() }` | **Safe Call (`?.`)** or **Smart Cast**                                         | `str?.length` or `if (str != null) { str.length }` |
| `str != null ? str : "default"`     | **Elvis Operator (`?:`)**                                                      | `str ?: "default"`                                  |
| `"Name: " + name`                   | **String Template (`$`)**                                                      | `"Name: $name"`                                     |

Ready for the next chapter? We can dive into **Functions and Conditionals** next, which also have some nice improvements over Java.