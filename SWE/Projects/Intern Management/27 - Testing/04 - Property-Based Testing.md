---
tags: [concept, testing, property-based]
type: concept
status: complete
related:
  - [[27 - Testing/02 - JUnit 5]]
---

# Property-Based Testing

## What it is

Instead of writing tests with specific inputs, you write **properties** that should hold for all inputs. The framework generates random inputs and tries to falsify the property.

## Example (jqwik)

```java
import net.jqwik.api.*;

class EmailPropertyTest {
    @Property
    void everyValidEmailHasAtSign(@ForAll("validEmails") String email) {
        assertTrue(email.contains("@"));
    }

    @Provide
    Arbitrary<String> validEmails() {
        return Arbitraries.strings().alpha().ofMinLength(3).map(s -> s + "@" + s + ".com");
    }
}
```

jqwik generates 1000 random valid emails and checks each has `@`.

## When to use

- **Algorithms** — "sorting returns a list where each element ≤ the next."
- **Parsers** — "parsing a serialized object and re-serializing gives the same string."
- **Invariants** — "the sum of a transfer equals the difference in balances."

## Vs example-based

- Example-based: `assertEquals(4, add(2, 2))`.
- Property-based: `for all a, b: add(a, b) == add(b, a)`.

Property-based tests catch edge cases you didn't think of.

## Project Connection

Useful for testing `toolkit.parseText` / `formatString` round-trip: "for any Map, `parse(format(map))` equals `map`."

## Further reading

- jqwik documentation.
- *Property-Based Testing with PropEr, Erlang, and Elixir* (Kidissov).
