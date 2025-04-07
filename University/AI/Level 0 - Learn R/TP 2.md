Okay, here's the breakdown of TP N° 2, formatted for easy copy-pasting without extra Markdown rendering, keeping the R code within triple backticks for direct execution.

### A. Structures alternatives (Conditional Statements)

L'instruction alternative (if-else statements) in R is very similar to C.  The basic structure is:

```R
x <- -5
if (x > 0) {
  print("Non-negative number")
} else {
  print("Negative number")
}
```

*   **Key Point about Statement Termination:** R uses semicolons (`;`) and newlines to separate statements.  A semicolon *always* ends a statement.  A newline ends a statement *if the statement is syntactically complete*.

*   **Error Example (and why it happens):**

    ```R
    x <- -5
    if (x > 0) {print("Non-negative number")} else {print("Negative number")}
    ```
    Running `source("essai2.R")` with the above code will produce an error: `unexpected 'else'`.
    **Reason:** The `if` statement is considered *complete* on the first line because of the closing curly brace `}`.  R doesn't expect an `else` to follow a completed `if`. The correct ways to structure this are:
    1.  Put the `else` on the same line as the closing brace of the `if`:
        ```r
        if (x > 0) {print("Non-negative number")} else {print("Negative number")}
        ```
    2.  Put the opening curly brace `{` on the same level, and the closing curly brace `}` in another line.
        ```r
         if (x>0)
         {
           print("Non-negative number")
         }
         else
         {
           print("Negative number")
         }
        ```

*   **Observation Exercise:**  Type the following into the R console and press Enter *after the closing brace*:
    ```R
    if (x > 0) {
    ```
    **What you'll notice:** R will show a `+` prompt, indicating that it's waiting for the rest of the statement.  It hasn't executed the `if` yet because it's not syntactically complete (it needs a closing brace and potentially an `else` block).

### B. Appels de fonctions R (Function Calls)

Function calls in R consist of the function name followed by arguments in parentheses, separated by commas.  Arguments often have names, which can be specified.

*   **Example: `writeLines()`**
    The `writeLines()` function writes text to a file (overwriting it if it exists). It takes two main arguments: the text to write (`text`) and the file connection (`con`, often a filename).

    ```R
    # Writing "146.6" to a file named "popRate.txt"
    writeLines("146.6", "popRate.txt")

    # Equivalent call using named arguments:
    writeLines(text = "146.6", con = "popRate.txt")

    # Named arguments can be in any order:
    writeLines(con = "popRate.txt", text = "146.6")

    # If 'con' is omitted, it defaults to the console (standard output):
    writeLines("146.6")  # This will print "146.6" to the console
    ```

*  **Example 2: Verify seq behavior**
    *   Execute these two commands:
        ```R
        seq(from=1, by=5, to=20)
        seq(1, 5, 20)
        ```
        The output will be different.

    *   Use `?seq` to view the help page for `seq`.

        *   **Explanation of the difference:** The `seq` function has arguments in the order `from`, `to`, `by`, and others.  When you call `seq(1, 5, 20)`, you are providing values for `from`, `to`, and `by` *in that order*.  When you call `seq(from=1, by=5, to=20)`, you are explicitly naming the arguments, so the order doesn't matter, and the `to` parameter is correctly put.

### C. Vecteurs (Vectors)

Vectors are fundamental data structures in R.  Here are common ways to create them:

| Function          | Example                                     | Result            |
| :---------------- | :------------------------------------------ | :---------------- |
| `c(a, b, ...)`     | `c(1, 5, 9, 1)` or `c(c(1,5),c(9,1))`          | `1, 5, 9, 1`      |
| `a:b`             | `1:5`                                       | `1, 2, 3, 4, 5`   |
| `seq(from, to, by)` | `seq(from = 0, to = 6, by = 2)`            | `0, 2, 4, 6`      |
| `rep(x, times, each)` | `rep(c(7, 3), times = 2, each = 2)`    | `7, 7, 3, 3, 7, 7, 3, 3` |

*   **Determine the commands:**
    *   To get `-7 -4 -1 2 5 8 11 14 17 20 23`:  `seq(-7, 23, by = 3)`
    *   To get `1 3 5 7 9 11 13 15 17 19 21`: `seq(1,21,2)`
    *   To get `3 3 5 5 7 7 9 9 3 3 5 5 7 7 9 9 3 3 5 5 7 7 9 9`: `rep(c(3,5,7,9),times=3,each=2)`
*   **Accessing Vector Elements:**
    *   Access elements using square brackets and indices (starting from 1).
        ```R
        a <- seq(2, 15, 3)
        a[4]  # Access the 4th element
        ```
    * Accessing a sequence of elements by another vector.

        ```R
        a <- seq(2, 25, 3)
        a[3:6]
        a[c(2, 2, 1, 1)]
        a[seq(2,10,3)]
        ```
* **ifelse**
    * The ifelse() is a useful function for the element-wise conditional modification of a vector.
    ```r
    a = c(5,7,2,9)
    ifelse(a %% 2 == 0,"even","odd")
    ```
    * Create a script R that, if the input is a vector of integers, returns the corresponding vector of absolute values:
     ```r
     #create the file
     #Write into it the following code:
     #Read the vector
     vect <- scan()
     #apply the transformation
     vect_abs <- ifelse(vect<0, -vect,vect)
     #print the result
     print(vect_abs)
     #save the script
     # Run source("script_name.R")
     # Give a test input
    ```

### D. Matrices

Matrices are two-dimensional data structures. Create them using the `matrix()` function.

```R
x <- c(2, 4, 3, 1, 5, 7)
A <- matrix(
  x,          # The data elements
  nrow = 2,   # Number of rows
  ncol = 3,   # Number of columns
  byrow = TRUE  # Fill matrix by rows (FALSE fills by columns)
)
print(A)
```

*   **Accessing Matrix Elements:**
    *   `A[i, j]`: Access the element at row `i` and column `j`.
        ```R
        A[2, 3]  # Access the element in the 2nd row, 3rd column
        ```
    *   `A[i, ]`: Extract the entire `i`-th row.
        ```R
        A[2, ]  # Extract the 2nd row
        ```
    *   `A[, j]`: Extract the entire `j`-th column.
        ```R
        A[, 3]  # Extract the 3rd column
        ```
    *   `A[, c(1, 3)]`: Extract a submatrix (columns 1 and 3 in this case).

### D. Structures répétitives (Loops)

R has three main loop structures:

*   **`for` loop:**
    ```R
    for (variable in sequence) {
      # instructions
    }
    ```

*   **`while` loop:**
    ```R
    while (condition) {
      # instructions
    }
    ```

*   **`repeat` loop:**
    ```R
    repeat {
      # instructions
      if (condition) {
        break
      }
    }
    ```

*   **Script 1 (and variations with `while` and `repeat`):**

    ```R
    # Original for loop script
    mat <- matrix(data = seq(10, 21, by = 1), nrow = 6, ncol = 2)
    for (i in 1:nrow(mat)) {
      for (j in 1:ncol(mat)) {
        cat(c("L'element a ligne ", i, " et la colonne ", j, " est ", mat[i, j]))
        cat("\n")
      }
    }

    # Equivalent while loop
    mat <- matrix(data = seq(10, 21, by = 1), nrow = 6, ncol = 2)
    i <- 1
    while (i <= nrow(mat)) {
      j <- 1
      while (j <= ncol(mat)) {
        cat(c("L'element a ligne ", i, " et la colonne ", j, " est ", mat[i, j]))
        cat("\n")
        j <- j + 1
      }
      i <- i + 1
    }
    # Equivalent repeat loop
    mat <- matrix(data = seq(10, 21, by = 1), nrow = 6, ncol = 2)
    i <- 1
    repeat {
      if (i > nrow(mat)) {
        break
      }
      j <- 1
      repeat {
        if (j > ncol(mat)) {
          break
        }
        cat(c("L'element a ligne ", i, " et la colonne ", j, " est ", mat[i, j]))
        cat("\n")
        j <- j + 1
      }
      i <- i + 1
    }
    ```

*   **Script 2:**

    ```R
    mat <- matrix(data = seq(1, 12, by = 1), nrow = 6, ncol = 2)

    vMoyLin <- rep(0, nrow(mat))
    for (i in 1:nrow(mat)) {
      for (j in 1:ncol(mat)) {
        vMoyLin[i] <- vMoyLin[i] + mat[i, j]
      }
      vMoyLin[i] <- vMoyLin[i] / ncol(mat)
    }

    vMoyCol <- rep(0, ncol(mat))
    for (j in 1:ncol(mat)) {
      for (i in 1:nrow(mat)) {
        vMoyCol[j] <- vMoyCol[j] + mat[i, j]
      }
      vMoyCol[j] <- vMoyCol[j] / nrow(mat)
    }

    print(mat)
    print(vMoyLin)
    print(vMoyCol)
    ```

*   **Script 3:**

    ```R
    mat <- matrix(data = seq(1, 12, by = 1), nrow = 6, ncol = 2)

    for (i in 1:nrow(mat)) {
      vMoyLin[i] <- mean(mat[i, ])
    }

    for (j in 1:ncol(mat)) {
      vMoyCol[j] <- mean(mat[, j])
    }
    print(mat)
    print(vMoyLin)
    print(vMoyCol)
    ```

### D. Manipulations vectorielles avec apply() (Vectorized Operations with `apply()`)

R provides functions like `apply()` for vectorized operations, which are often more concise and efficient than loops.

*   `apply(X, MARGIN, FUN)`
    *   `X`: The matrix.
    *   `MARGIN`:  `1` for rows, `2` for columns.
    *   `FUN`: The function to apply.

```R
mat <- matrix(data = seq(1, 12, by = 1), nrow = 6, ncol = 2)

vMoyLin <- apply(mat, 1, mean)  # Calculate row means
vMoyCol <- apply(mat, 2, mean)  # Calculate column means

print(mat)
print(vMoyLin)
print(vMoyCol)
```

This provides a complete, copy-paste-friendly version of the second R tutorial, ready for use in your notes or R environment.
