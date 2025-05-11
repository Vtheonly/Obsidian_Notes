Okay, let's clarify the `[1]` in R output.

You are correct that the output shows results from three separate commands or expressions.

The `[1]` in R's console output indicates the **index of the first element being displayed on that specific line**.

Here's the breakdown:

1.  **R is Vector-Based:** Fundamentally, R treats almost everything as a vector (or a more complex structure built upon vectors). Even a single number like `42` is considered a numeric vector of length one.
2.  **Indexing:** When R prints a vector (or the result of an expression, which is often a vector), it prefixes each line of output with the index of the *first* element shown on that line, enclosed in square brackets `[]`.
3.  **Single Value Output:** When the result is just a single value (a vector of length 1), like `42`, `8`, or `18`, the first (and only) element is at index `1`. Therefore, the output is prefixed with `[1]`.
    *   `[1] 42` means: "Starting at index 1, the value is 42."
    *   `[1] 8` means: "Starting at index 1, the value is 8."
    *   `[1] 18` means: "Starting at index 1, the value is 18."
4.  **Longer Vector Output:** You see the utility of this more clearly when R prints a longer vector that needs to wrap onto multiple lines:

    ```R
    > x <- 1:50 # Create a vector from 1 to 50
    > x
     [1]  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
    [21] 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
    [41] 41 42 43 44 45 46 47 48 49 50
    ```
    *   The first line starts with `[1]` because it displays elements starting from index 1.
    *   The second line starts with `[21]` because the first element shown on *that line* is the 21st element of the vector `x`.
    *   The third line starts with `[41]` for the same reason.

**In summary:** The `[1]` is simply R telling you that the output line starts with the element at index 1 of the resulting vector. It's part of R's default way of displaying output and *not* part of the actual data value itself. In your example, it confirms that each of the three outputs likely started with a single value (a vector of length 1).