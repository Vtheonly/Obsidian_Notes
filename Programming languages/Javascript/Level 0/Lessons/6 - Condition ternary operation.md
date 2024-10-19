[[13 - if else statement]]

The syntax for the ternary operator, also known as the conditional operator, in JavaScript is as follows:

```javascript
condition ? expression_if_true : expression_if_false;
```

Here's a simple example:

```javascript
let age = 20;
let status = (age >= 18) ? 'Adult' : 'Minor';

console.log(status); // Output: 'Adult'
```

In this example, the condition `(age >= 18)` is evaluated. If it's true, the value `'Adult'` is assigned to the variable `status`; otherwise, the value `'Minor'` is assigned. The entire expression `(age >= 18) ? 'Adult' : 'Minor'` itself returns a value, which is then stored in the `status` variable.

It's a concise way to express a simple if-else statement in a single line.


However, if you still want to express multiple conditions in a more compact way, you can nest ternary operators. Here's an example:

```javascript
let age = 20;
let status =
  age >= 18
    ? 'Adult'
    : age >= 13
    ? 'Teen'
    : 'Child';

console.log(status); // Output: 'Adult'
```

In this example, the nested ternary operators check for different age ranges. However, as the conditions become more complex, readability decreases, and it's generally better to use a traditional if-else-if-else statement for clarity.
