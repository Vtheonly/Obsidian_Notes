Alright, let's move on. Now that you can define variables and create logic with functions and conditionals, the next step is learning how to perform repetitive tasks. This chapter covers loops and the powerful `range` expressions that make looping in Kotlin intuitive and safe.

Here is your third lesson.

***

# Chapter 3: Loops and Ranges

#tags: #kotlin #fundamentals #loops #ranges #control-flow #iteration #java-comparison

In programming, loops are essential for executing a block of code multiple times. While Kotlin has the familiar `while` loop, its `for` loop is a significant enhancement over Java's C-style `for` loop. It's designed to be safer and more expressive, working seamlessly with collections and special expressions called **ranges**.

---

## I. The `for` Loop

In Kotlin, the `for` loop iterates through anything that provides an *iterator*. This includes ranges, arrays, lists, maps, and other collections. It operates like Java's enhanced `for-each` loop, but it's the *only* kind of `for` loop in Kotlin.

**Syntax:** `for (item in collection) { ... }`

```kotlin
val fruits = listOf("Apple", "Banana", "Cherry") // listOf creates a read-only list

for (fruit in fruits) {
    println(fruit)
}
// Output:
// Apple
// Banana
// Cherry
```

You can't write a C-style `for (int i = 0; ...)` loop. Instead, you use ranges.

---

## II. Ranges: The Power Behind `for` Loops

Ranges are a core feature for creating sequences of values. They are the standard way to perform traditional indexed loops.

### A. The `..` Operator (Inclusive Range)

Creates a range from the start value to the end value, **including** the end value.

```kotlin
// This loop runs for i = 1, 2, 3, 4, and 5.
for (i in 1..5) {
    print("$i ") // Prints "1 2 3 4 5 "
}
```
*This is the direct Kotlin equivalent of Java's `for (int i = 1; i <= 5; i++)`.*

### B. The `until` Infix Function (Exclusive Range)

Creates a range up to, but **excluding**, the end value. This is extremely useful for iterating over collections by index, as indices are typically `0` to `size - 1`.

```kotlin
val numbers = arrayOf(10, 20, 30) // Creates an array

// The range will be 0, 1, 2. It does NOT include 3.
for (index in 0 until numbers.size) {
    println("Element at index $index is ${numbers[index]}")
}
// Output:
// Element at index 0 is 10
// Element at index 1 is 20
// Element at index 2 is 30
```
*This is the direct Kotlin equivalent of Java's `for (int i = 0; i < array.length; i++)`.*

### C. The `downTo` Infix Function (Reverse Order)

Creates a range that counts backward.

```kotlin
// This loop runs for i = 5, 4, 3, 2, and 1.
for (i in 5 downTo 1) {
    print("$i ") // Prints "5 4 3 2 1 "
}
```
*This is the direct Kotlin equivalent of Java's `for (int i = 5; i >= 1; i--)`.*

### D. The `step` Infix Function (Custom Increment)

Changes the increment of the iteration. It can be combined with `..`, `until`, and `downTo`.

```kotlin
// Prints odd numbers from 1 to 9
for (i in 1..10 step 2) {
    print("$i ") // Prints "1 3 5 7 9 "
}

println() // New line

// Counts down from 10 to 0 in steps of 3
for (i in 10 downTo 0 step 3) {
    print("$i ") // Prints "10 7 4 1 "
}
```

---

## III. Iterating Over Collections (Advanced)

The `for` loop offers more advanced ways to iterate over complex data structures.

### A. Iterating with Index using `.withIndex()`

If you need both the index and the value of an item in a collection, use the `.withIndex()` function. This returns a pair of `(index, value)` for each item, which can be destructured directly in the loop.

```kotlin
val permissions = listOf("Camera", "Location", "Storage")

for ((index, permission) in permissions.withIndex()) {
    println("Permission #${index + 1}: $permission")
}
// Output:
// Permission #1: Camera
// Permission #2: Location
// Permission #3: Storage
```

### B. Iterating Over a Map

You can easily iterate over the key-value pairs of a `Map`.

```kotlin
val userAges = mapOf("Alice" to 30, "Bob" to 25) // mapOf creates a read-only map

// Destructure the key and value directly
for ((name, age) in userAges) {
    println("$name is $age years old.")
}
// Output:
// Alice is 30 years old.
// Bob is 25 years old.
```

---

## IV. `while` and `do-while` Loops

These loops work **exactly the same as in Java**. Their syntax and behavior are identical. Use them when you don't know the number of iterations in advance.

### A. `while` Loop

The condition is checked *before* the loop body is executed.

```kotlin
var i = 0
while (i < 5) {
    print("$i ") // Prints "0 1 2 3 4 "
    i++
}
```

### B. `do-while` Loop

The loop body is executed *at least once*, and the condition is checked *after*.

```kotlin
var input: String
do {
    println("Please enter 'exit' to quit.")
    input = readLine() ?: "" // readLine() reads from console, Elvis operator handles null
} while (input != "exit")

println("Exiting program.")
```

---

## V. Loop Control: `break` and `continue`

These keywords also work exactly as they do in Java.

*   `continue`: Skips the rest of the current iteration and proceeds to the next one.
*   `break`: Terminates the loop entirely.

```kotlin
for (i in 1..10) {
    if (i % 2 == 0) {
        continue // Skip even numbers
    }
    if (i == 7) {
        break // Stop the loop when i is 7
    }
    print("$i ") // Prints "1 3 5 "
}
```

#### Labeled `break` and `continue`

For nested loops, Kotlin allows you to label a loop and then specify which loop to `break` from or `continue`. This is a cleaner alternative to `goto` or complex flag variables.

```kotlin
outerLoop@ for (i in 1..3) {
    for (j in 1..3) {
        if (i == 2 && j == 2) {
            break@outerLoop // Breaks the outer loop, not just the inner one
        }
        println("i = $i, j = $j")
    }
}
// Output:
// i = 1, j = 1
// i = 1, j = 2
// i = 1, j = 3
// i = 2, j = 1 
// (Loop terminates here)
```

---

## VI. Quick Reference: From Java to Kotlin

| Java For Loop                                | Kotlin Equivalent                                    | Description                            |
| :------------------------------------------- | :--------------------------------------------------- | :------------------------------------- |
| `for (int i = 0; i < 10; i++)`               | `for (i in 0 until 10)`                              | Loop from 0 to 9.                      |
| `for (int i = 1; i <= 10; i++)`              | `for (i in 1..10)`                                   | Loop from 1 to 10 (inclusive).         |
| `for (int i = 10; i >= 1; i--)`              | `for (i in 10 downTo 1)`                             | Loop from 10 down to 1.                |
| `for (int i = 0; i < 10; i += 2)`            | `for (i in 0 until 10 step 2)`                       | Loop with a step of 2.                 |
| `for (String item : list)`                   | `for (item in list)`                                 | For-each loop.                         |
| `while (condition) { ... }`                  | `while (condition) { ... }`                          | Identical `while` loop.                |

You've now covered the essentials of Kotlin's syntax and control flow! The next logical step is to dive into **Classes and Objects**, where you'll see how Kotlin streamlines object-oriented programming. Ready to proceed?