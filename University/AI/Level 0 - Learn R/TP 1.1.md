Okay, I understand. Here's the same information, formatted for direct copy-pasting without the Markdown code blocks. I've kept the structure and explanations, but removed the Markdown formatting that would render in a Markdown viewer. I have retained the R code blocks (using triple backticks) so that you can copy and paste the R code directly into your R console.

---

### A. Installing R

R is available for both Windows and Linux.  The installation process depends on your operating system.

1.  **Go to CRAN:** Visit the CRAN Mirrors page (https://cran.r-project.org/mirrors.html).
2.  **Choose a Mirror:** Select a mirror site geographically close to you.  This will speed up the download.  The example given is `http://ftp.igh.cnrs.fr/pub/CRAN/`.
3.  **Select Your OS:**  Click the link for your operating system (Windows or Linux).
4.  **Follow Instructions:**  The CRAN website will provide detailed instructions for your specific OS.
5.  **For Ubuntu Linux Specifically**:
    Precautions must be taken before installation, check https://cran.r-project.org/bin/linux/ubuntu/ for more details, otherwise open terminal and run:

```bash
sudo apt-get install r-base
```

This command uses the `apt-get` package manager to install the `r-base` package, which is the core R system.

### B. Installing R Packages

R packages extend the functionality of base R.  You'll often need to install packages for specific tasks.

To install a package, use the `install.packages()` function:

```R
install.packages("packageName", dependencies = TRUE)
```

*   `"packageName"`:  Replace this with the actual name of the package you want to install (e.g., "ggplot2", "dplyr").  The name *must* be in quotes.
*   `dependencies = TRUE`:  This is generally recommended. It tells R to also install any other packages that the package you're installing depends on.
    *   Example:

```R
install.packages("ggplot2", dependencies = TRUE) # Install ggplot2 and its dependencies.
install.packages("dplyr", dependencies = TRUE)
install.packages("readr", dependencies = TRUE)
```

### C. The R Console

The R console is an interactive environment where you can execute R code.

*   **Starting R:**
    *   **Windows:** Find and run `R.exe`.
    *   **Linux:** Open a terminal and type `R`, then press Enter.
* You will see the output in the console (see example in the document).
* **Basic Commands:**

```R
   demo(graphics) # View a graphics demonstration.
   q()  # Quit R.  It will ask if you want to save your workspace.
   # comments starts with # symbol
   CTRL+L # Clear the console
   rm(list=ls()) #clear the workspace
```

```R
# Example 1: Simple calculation
2 + 3

# Example 2:  Displaying a message
print("Hello, R!")

# Example 3: Quit
# q() # Uncomment this to actually quit R
```

### D. Variables in R

In R, every variable is an object.  R has five fundamental data types (atomic classes):

1.  **logical:** Boolean values (`TRUE` or `FALSE`).
2.  **integer:** Whole numbers (e.g., `42L`, `-10L`).  The `L` suffix forces an integer.
3.  **numeric:**  Real numbers (e.g., `3.14`, `-2.7`, `10`).  This includes both integers and decimals.
4.  **complex:** Complex numbers (e.g., `1 + 2i`).
5.  **character:** Text strings (e.g., `"hello"`, `'R is fun!'`).

**Variable Assignment:**

You can assign values to variables using either `<-` (preferred) or `=`.  You can also use `->` to assign in the opposite direction.  The variable name (identifier) is case-sensitive.

```R
# Examples using <-
x <- 10       # Assign the value 10 to the variable x
y <- "Hello"  # Assign the string "Hello" to y
z <- TRUE     # Assign the logical value TRUE to z

# Examples using =
a = 5
b = "World"
c = FALSE

#Examples using ->
25 -> k
"test" -> l
FALSE -> m

# Displaying the value of a variable
x
y
z
a
b
c
k
l
m
```

```R
# Example 1: Numeric, Integer, Logical
my_numeric <- 3.14159
my_integer <- 10L
my_logical <- TRUE

print(my_numeric)
print(my_integer)
print(my_logical)

# Example 2: Character and Complex
my_string <- "R Programming"
my_complex <- 2 + 3i

print(my_string)
print(my_complex)

# Example 3: Reassigning a variable
my_variable <- 5
print(my_variable)
my_variable <- "Now it's a string"
print(my_variable)
```
**Role of just writing the variable name:**
Writing the name of the variable in R and executing it is equivalent to using a display method (like the function print()).

### E. Data Input and Output

**Input with `scan()`**

The `scan()` function reads data from the keyboard (or a file).

```R
# Basic usage: reads numeric data until an empty line is entered
my_numbers <- scan()
#Enter your inputs one by one in the console, ex:
#1
#2
#3
#
print(my_numbers)
```

*   **Reading a specific number of values:** Use the `nmax` argument.

```R
# Read only one value
single_value <- scan(nmax = 1)
#1
print(single_value)

#Read three values
three_value <- scan(nmax=3)
#1
#2
#3
print(three_value)
```

*   **Reading non-numeric data:** Use the `what` argument.

```R
# Read a string
my_string <- scan(what = "character", nmax = 1)
# hello
print(my_string)
# Read a logical value
my_logical1 <- scan(what=TRUE, nmax=1)
#TRUE
print(my_logical1)
my_logical2 <- scan(what = logical(), nmax = 1)
#FALSE
print(my_logical2)
```
 * Use the str() to check the variable type:

```R
x <- scan(what = logical(), nmax = 4)
#TRUE
#FALSE
#FALSE
#TRUE
str(x)
```

**Output with `print()`**

The `print()` function displays values.  You can control the output format.

```R
x <- 12.3456789

print(x)                 # Default display
print(x, digits = 3)     # Show 3 significant digits
print(x, digits = 5)     # Show 5 significant digits
```

```R
# Example 1: Basic Input and Output
name <- scan(what = "character", nmax = 1) #read an input from console
#yourName
print(paste("Hello,", name, "!"))

# Example 2:  Controlling output digits
pi_approx <- 3.14159265359
print(pi_approx, digits = 4)
print(pi_approx, digits = 7)

# Example 3: Reading and displaying multiple values
numbers <- scan(nmax = 3)
#10
#20
#30
print(numbers)
print(sum(numbers)) # Calculate and print the sum

#Read variables from the 5 atomic classes
v_logical <- scan(what=logical(),nmax=1)
v_integer <- scan(what=integer(),nmax=1)
v_numeric <- scan(what=numeric(),nmax=1)
v_complex <- scan(what=complex(),nmax=1)
v_character <- scan(what=character(),nmax=1)
#Test inputs:
#TRUE
#2L
#1.2
#1+3i
#"test"

#print the result
print("The entered values are:")
print(v_logical)
print(v_integer)
print(v_numeric)
print(v_complex)
print(v_character)
#verify the type
print("Type of entered variables:")
str(v_logical)
str(v_integer)
str(v_numeric)
str(v_complex)
str(v_character)

# Example using external file:
#create the file essai.R
#write into it using text editor:
# # Read two values and print their sum
# a <- scan(nmax = 1)
# b <- scan(nmax = 1)
# sum_ab <- a + b
# print(paste("The sum of", a, "and", b, "is", sum_ab))
#save and close
#run this command in the console:
source("essai.R") # make sure the file is located in the same folder, or provide path
#1
#2
#getwd()
#setwd("new path")
```

### F. R Operators

R provides a range of operators for performing calculations and comparisons.

| Operator | Description            |
| :-------- | :--------------------- |
| `+`       | Addition               |
| `-`       | Subtraction            |
| `*`       | Multiplication         |
| `/`       | Division               |
| `%%`      | Modulo (remainder)     |
| `%/%`     | Integer Division       |
| `^`       | Exponentiation         |
| `:`       | Sequence               |
| `==`      | Equal to               |
| `!=`      | Not equal to           |
| `>`       | Greater than           |
| `>=`      | Greater than or equal to |
| `<`       | Less than              |
| `<=`      | Less than or equal to  |
| `&`       | Logical AND (element-wise)|
| `&&`      | Logical AND (single)   |
| `|`       | Logical OR (element-wise) |
| `||`      | Logical OR (single)    |
| `!`       | Logical NOT            |

**Operator Precedence (highest to lowest):**

1.  `^` (Exponentiation - right to left)
2.  `-` `+` (Unary minus and plus)
3.  `:` (Sequence)
4.  `%any%` (e.g. `%%`, `%/%`)
5.  `*`, `/`
6.  `+`,`-`
7.  `<`, `>`, `<=`, `>=`, `==`, `!=`
8.  `!`
9.  `&`, `&&`
10. `|`, `||`
11. `->`
12. `<-`
13. `=`

```R
# Example 1: Arithmetic Operators
print(10 + 5)
print(10 - 5)
print(10 * 5)
print(10 / 5)
print(10 %% 3)  # Modulo
print(10 %/% 3) # Integer division
print(2^4)     # Exponentiation

# Example 2: Comparison Operators
print(10 > 5)
print(10 < 5)
print(10 == 10)
print(10 != 5)

# Example 3: Logical Operators
print(TRUE & TRUE)
print(TRUE & FALSE)
print(TRUE | FALSE)
print(!TRUE)
print( (5>3) && (2<7))
#check if comparison operators are associable
print( 1<2<3) # left to right
print( 3>2>1)

# Create a file operator.R as the document example
# And run this code in console:
# source("operateur.R")
```
### G. Identifiers in R

Identifiers are the names you give to variables, functions, etc.  Here are the rules:

*   Can contain letters, numbers, periods (`.`), and underscores (`_`).
*   Cannot start with a number or an underscore.
*   Cannot start with a period followed by a number.
*   **Reserved words:**  You cannot use the following as identifiers:
    `if`, `else`, `repeat`, `while`, `function`, `for`, `in`, `next`, `break`, `TRUE`, `FALSE`, `NULL`, `Inf`, `NaN`, `NA` , ...etc.

```R
# Example 1: Valid Identifiers
my_variable <- 10
variable.1 <- "hello"
_another_variable <- TRUE  #This is not a good practice, but shows the case.

print(my_variable)
print(variable.1)

# Example 2: Invalid Identifiers (will produce errors)
# 1st_variable <- 5  # Cannot start with a number
# _variable <- 10 #cannot start with _
# .2variable<-2 # Cannot start with a period followed by a number

# Example 3: Reserved words
# if <- 5     # Error:  'if' is a reserved word
TRUE_value <- FALSE #Valid variable name, not using the keyword
print(TRUE_value)

True <- 1; True # shows that True isn't the keyword TRUE
e<- 10;e #valid
```
---
