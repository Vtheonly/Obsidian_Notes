
# 🔄 `apply()` vs `sapply()` vs `mapply()` in R

## 📌 Overview

These are all part of R’s *"apply family"*, built to replace `for` loops with cleaner, more efficient **vectorized** operations.

| Function   | Use Case                            | Input Type            | Output Type                | Applies Over         |
|------------|-------------------------------------|------------------------|-----------------------------|----------------------|
| `apply()`  | Row/column-wise operations          | Matrix/array           | Vector / Matrix / List      | Rows or Columns      |
| `sapply()` | Simplified `lapply()`               | List or vector         | Simplified vector/matrix    | Each element         |
| `mapply()` | Vectorized multivariate function    | Multiple vectors/lists | Simplified list/vector      | Multiple inputs in parallel |

---

## 🔧 Syntax and Examples

### 🔸 `apply(X, MARGIN, FUN, ...)`

Use it when working with matrices or arrays.

```r
mat <- matrix(1:9, nrow=3)
apply(mat, 1, sum)  # Sum of each row → [6, 15, 24]
apply(mat, 2, mean) # Mean of each column → [4, 5, 6]
````

> ⚠️ `apply()` coerces data frames to matrices — be cautious with mixed types.

---

### 🔸 `sapply(X, FUN, ..., simplify = TRUE)`

Applies `FUN` over a list or vector and **tries to simplify** the result (to vector, matrix, or array).

```r
lst <- list(a = 1:3, b = 4:6)
sapply(lst, sum)  # Returns a named numeric vector: a = 6, b = 15
```

> ✅ Cleaner output than `lapply()`, but simplification can sometimes break consistency.

---

### 🔸 `mapply(FUN, ..., MoreArgs = NULL)`

Applies a function to **multiple arguments in parallel** — useful for element-wise mapping across several inputs.

```r
mapply(rep, 1:4, 4:1)
# Output: list(1 1 1 1, 2 2 2, 3 3, 4)
```

> 📍 Think of `mapply()` as `Map()` + `sapply()`

---

## ⚔️ Key Differences

|Feature|`apply()`|`sapply()`|`mapply()`|
|---|---|---|---|
|Row/Col matrix ops|✅ Yes|❌ No|❌ No|
|Element-wise apply|❌ No|✅ Yes|✅ Yes (multi-args)|
|Input structures|matrix/array|list/vector|multiple vectors/lists|
|Simplification|Depends on FUN|Yes (default)|Yes (default)|
|Parallel args|❌ No|❌ No|✅ Yes|
|Loop Replacement|over matrix dims|over list elements|over zipped input sets|

---

## 🧠 When to Use What

|Use Case|Use...|
|---|---|
|Summing each row or column of a matrix|`apply()`|
|Applying a function to each list element cleanly|`sapply()`|
|Running a function with multiple parallel args|`mapply()`|

---

## 🧨 Common Pitfalls

- `apply()` turns a data frame into a matrix: this **can corrupt column types**
    
- `sapply()` simplifies the result: great for clean code, **bad for consistency** in pipelines
    
- `mapply()` has overhead: use only when **parallel** argument processing is needed
    

---

## ✅ Summary Cheatsheet

```r
apply(matrix, 1 or 2, func)        # for rows or columns
sapply(list_or_vector, func)      # like lapply(), but simplified
mapply(func, vec1, vec2, ...)     # vectorized mapping over multiple inputs
```

---

```

Would you like a visual graph for your vault or a usage flowchart?
```