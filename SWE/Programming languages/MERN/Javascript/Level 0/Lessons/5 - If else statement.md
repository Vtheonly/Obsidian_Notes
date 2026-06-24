[[16 - switch syntax]]

If you're looking for the syntax of an "else if" statement in JavaScript, here it is:

```javascript
if (condition1) {
  // Code to be executed if condition1 is true
} else if (condition2) {
  // Code to be executed if condition1 is false and condition2 is true
} else {
  // Code to be executed if both condition1 and condition2 are false
}
```

Here's an example:

```javascript
let grade = 75;

if (grade >= 90) {
  console.log('A');
} else if (grade >= 80) {
  console.log('B');
} else if (grade >= 70) {
  console.log('C');
} else {
  console.log('D');
}
```

In this example, depending on the value of `grade`, it will print the corresponding letter grade. The `else if` statements allow you to check multiple conditions in sequence. If one condition is true, the corresponding block of code will be executed, and the rest of the conditions will be skipped. If none of the conditions are true, the code inside the `else` block will be executed.