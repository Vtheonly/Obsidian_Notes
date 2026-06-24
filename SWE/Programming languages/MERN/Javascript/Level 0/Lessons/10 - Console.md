Some of the commonly used console methods include:

```javascript
console.log();
console.error();
console.table([]); // takes an array
```

The log method can be formatted inside the console using what's called a directive, specifically "%c".

The console is not just for JavaScript; it's also part of the Web API. It provides services and functionalities that you can use with the JavaScript language to accomplish various tasks.

Here's some additional information about console methods and formatting:

1. console.warn() - for warning messages
2. console.info() - for informational messages
3. console.debug() - for debugging messages
4. console.group() and console.groupEnd() - for grouping related log messages
5. console.time() and console.timeEnd() - for performance measurements

Regarding the %c directive for styling console output:

```javascript
console.log("%cStyled log", "color: blue; font-size: 20px;");
```

This will output "Styled log" in blue, 20px font size in the console.
