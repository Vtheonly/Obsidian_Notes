
Comments are used to provide explanations or notes in code. They are ignored by the compiler and do not affect the program. C supports two types of comments: `/* */` for block comments and `//` for single-line comments.

#### Section 2.1: Commenting with the Preprocessor

To "comment out" large code sections, use preprocessor directives:

```c
#if 0  // Start the comment block
/* Multi-line code */
int foo() {
  /* Example comments */
  if (someTest) {
    return 1;
  }
  return 0;
}
#endif  // End the comment block
```

This is useful when the code contains nested `/* */` comments.

#### Section 2.2: `/* */` Delimited Comments

Block comments start with `/*` and end with `*/`. They can span multiple lines:

```c
/* This is a single-line comment */

/* 
 * This is a 
 * multi-line comment 
 */
```

Comments can be on their own line, at the end of a line, or within code lines. However, they **cannot** be nested, as the first `*/` encountered ends the comment.

#### Section 2.3: `//` Delimited Comments (C99 and Later)

C99 introduced `//` for single-line comments that run to the end of the line:

```c
// Single-line comment
if (x && y) { // End-of-line comment
}
```

Multiple single-line comments can be stacked to create a block of comments, but they cannot be nested within a line of code.

#### Section 2.4: Pitfalls Due to Trigraphs

C99 supports trigraphs, which can cause unintended behavior. For example:

```c
int x = 20; // Why did I do this??/
```

Here, `??/` is a trigraph for `\`, causing the compiler to treat the next line as a continuation, potentially leading to errors.

### Summary

- Use `/* */` for block comments but avoid nesting.
- Use `//` for single-line comments (C99 and later).
- Be cautious of trigraphs that may alter the intended comment behavior.