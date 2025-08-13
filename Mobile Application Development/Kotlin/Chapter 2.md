Excellent. Let's build on the foundation of variables and null safety by exploring how to create logic and behavior. In this chapter, we'll cover functions and Kotlin's powerful control flow structures. You'll see how Kotlin makes code more expressive and readable compared to Java.

Here is your second lesson.

***

# Chapter 2: Functions and Conditionals

#tags: #kotlin #functions #conditionals #control-flow #expressions #java-comparison

This chapter covers the building blocks of application logic: **functions** (how to define behavior) and **conditional statements** (how to make decisions). Kotlin introduces significant improvements over Java, such as treating functions as first-class citizens and using control flow statements as *expressions* that can return values.

---

## I. Functions in Kotlin

Functions are declared using the `fun` keyword. They are fundamental to organizing and reusing code.

### A. Basic Function Declaration

The structure of a Kotlin function is concise and easy to read.

**Syntax:** `fun functionName(parameterName: Type): ReturnType { ... }`

```kotlin
// A simple function that takes two integers and returns their sum.
fun add(a: Int, b: Int): Int {
    return a + b
}

// Calling the function
val sum = add(5, 3) // sum is 8
```

*   **Java Comparison:** Notice there's no need for `public static` ceremony for a top-level function. The return type comes *after* the parameter list, separated by a colon (`:`).

### B. Single-Expression Functions

If a function consists of only a single expression, you can make it even more concise by using the `=` syntax. The `return` keyword and curly braces `{}` are removed. The compiler can also infer the return type.

```kotlin
// The 'add' function from before, written as a single-expression function.
// The return type 'Int' is inferred by the compiler, but it's good practice to keep it for clarity.
fun add(a: Int, b: Int) = a + b 
```

### C. Functions with No Return Value: `Unit`
In Java, you use `void` to indicate a function doesn't return anything. In Kotlin, the equivalent is the `Unit` type.

*   `Unit` is a real object type.
*   If a function doesn't specify a return type, it implicitly returns `Unit`.
*   You can (and almost always should) omit the `: Unit` for cleaner code.

```kotlin
// This function prints a message and returns nothing (Unit).
fun printMessage(message: String) { // ': Unit' is omitted
    println(message)
}

// This is the more verbose, but equivalent, declaration:
fun printMessageVerbose(message: String): Unit {
    println(message)
}
```

### D. Default Arguments and Named Parameters
This is a major improvement over Java, eliminating the need for most function overloading.

*   **Default Arguments:** You can specify a default value for a parameter. If a caller omits that argument, the default value is used.
*   **Named Parameters:** When calling a function, you can specify the names of the arguments. This makes the code highly readable and allows you to change the order of arguments, especially when some are being omitted.

```kotlin
fun showToast(message: String, duration: String = "Short", isImportant: Boolean = false) {
    println("Showing toast: '$message' (Duration: $duration, Important: $isImportant)")
}

// --- Calling the function ---

// 1. Using all arguments in order
showToast("Profile Saved", "Long", true)

// 2. Omitting arguments with default values
showToast("Login successful") // duration defaults to "Short", isImportant defaults to false

// 3. Using NAMED arguments to improve readability and skip parameters
showToast(message = "File Deleted", isImportant = true) // duration is skipped and defaults to "Short"

// 4. Using named arguments in a different order
showToast(isImportant = true, message = "Warning!") 
```
This single function replaces what would have required multiple overloaded methods in Java.

---

## II. `if` and `else` Control Flow

The `if` statement in Kotlin is more powerful than in Java because it can be used as an **expression** that returns a value.

### A. Traditional `if-else` Statement
The standard `if-else` block works exactly as it does in Java.

```kotlin
val score = 85
var grade: String

if (score >= 90) {
    grade = "A"
} else if (score >= 80) {
    grade = "B"
} else {
    grade = "C"
}
println("Your grade is $grade") // Prints "Your grade is B"
```

### B. `if` as an Expression
You can use `if-else` to directly assign a value to a variable. This replaces Java's ternary operator (`condition ? value_if_true : value_if_false`) with a more readable syntax.

*   When used as an expression, the `else` branch is **mandatory**.

```kotlin
val a = 10
val b = 20

// The result of the if-else block is assigned to 'max'
val max = if (a > b) {
    println("Choosing a")
    a // The last expression in a block is the return value
} else {
    println("Choosing b")
    b
}
println("The max value is $max") // Prints "The max value is 20"

// For simple cases, it's very clean:
val min = if (a < b) a else b // Replaces Java's 'int min = (a < b) ? a : b;'
```

---

## III. `when` Control Flow

Kotlin's `when` is the modern, flexible replacement for Java's `switch` statement.

### A. `when` as a `switch` Replacement
It's cleaner and safer than `switch`:
*   No `break` statements are needed. Execution automatically stops after a matching branch is found.
*   The `else` branch is the equivalent of `default`.

```kotlin
val dayOfWeek = 3

when (dayOfWeek) {
    1 -> println("Monday")
    2 -> println("Tuesday")
    3 -> println("Wednesday")
    4 -> println("Thursday")
    5 -> println("Friday")
    else -> println("Weekend day")
}
// Prints "Wednesday"
```

### B. `when` as an Expression
Like `if`, `when` can be used as an expression to return a value. The `else` branch is mandatory unless the compiler can prove all possible cases have been covered (e.g., with enums or sealed classes).

```kotlin
val dayOfWeek = 6
val dayType = when (dayOfWeek) {
    1, 2, 3, 4, 5 -> "Weekday" // Combine multiple cases with a comma
    6, 7 -> "Weekend"
    else -> "Invalid day"
}
println("Day type is: $dayType") // Prints "Day type is: Weekend"
```

### C. Advanced `when` Usage
`when` can do much more than just match constants.

```kotlin
fun describe(obj: Any): String = when (obj) {
    1 -> "One"
    "Hello" -> "A greeting"
    is Long -> "A Long number"       // Check the type of the object
    !is String -> "Not a string"     // Negated type check
    else -> "Unknown"
}

val score = 88
when (score) {
    in 90..100 -> println("Grade: A") // Check if a value is in a range
    in 80..89 -> println("Grade: B")  // Prints "Grade: B"
    else -> println("Grade: C or lower")
}
```

You can even use `when` without an argument, turning it into a more readable `if-else if-else` chain.

```kotlin
val text = "Start"
when {
    text.startsWith("S") -> println("Starts with S")
    text.endsWith("t") -> println("Ends with t")
    else -> println("Doesn't match")
}
```

---

## IV. Quick Reference: From Java to Kotlin

| Java Concept                                             | Kotlin Equivalent                                      | Example                                                     |
| :------------------------------------------------------- | :----------------------------------------------------- | :---------------------------------------------------------- |
| `public void myFunc() {}`                                | `fun myFunc() { ... }` or `fun myFunc(): Unit { ... }`   | `fun log(msg: String) = println(msg)`                       |
| `int add(int a, int b){ return a+b; }`                    | `fun add(a: Int, b: Int): Int = a + b`                   | `fun add(a: Int, b: Int) = a + b`                           |
| Function Overloading                                     | **Default and Named Arguments**                        | `fun toast(msg: String, len: Int = 0)`                      |
| Ternary Operator `(a > b) ? a : b`                       | **`if` as an expression**                              | `val max = if (a > b) a else b`                             |
| `switch (day) { case 1: ...; break; default: ...; }`      | **`when` expression**                                  | `when (day) { 1 -> ... else -> ... }`                       |

Next, we can explore **Loops and Ranges**, which will complete our tour of Kotlin's basic control flow structures. Let me know when you're ready