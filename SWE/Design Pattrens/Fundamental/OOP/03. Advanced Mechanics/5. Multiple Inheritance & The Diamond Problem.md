### 1. The Restriction

Java does **not** allow a class to extend two classes (`class Child extends Mother, Father` is ILLEGAL).

**The Reasoning (The Diamond Problem):**
Imagine this scenario:

1.  Class `Animal` has a method `eat()`.
2.  Class `Tiger` extends `Animal` and overrides `eat()`.
3.  Class `Lion` extends `Animal` and overrides `eat()`.
4.  Class `Liger` extends **both** `Tiger` and `Lion`.
5.  You call `liger.eat()`. **Which version runs?** The Tiger's or the Lion's?

This ambiguity causes compiler errors in C++. Java avoids it entirely by banning multiple class inheritance.

### 2. The Interface Solution

Java allows a class to implement multiple Interfaces.
`class Liger implements TigerBehavior, LionBehavior`.

- **Why this works:** Interfaces (traditionally) do not have method bodies. They only say "I must have an `eat()` method."
- The `Liger` class is forced to provide **its own** implementation of `eat()`. There is no ambiguity because the parent interfaces didn't provide conflicting code—only conflicting requirements, which the child resolves by writing the code itself.
