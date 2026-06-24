## Introduction
- Window Object Is The Browser Window
- Window Contains The Document Object
- All Global Variables, Objects, And Functions
  - Test Document And Console

## What Can We Do With Window Object?
- Open Window
- Close Window
- Move Window
- Resize Window
- Print Document
- Run Code After a Period Of Time Once Or More
- Fully Control The URL
- Save Data Inside Browser To Use Later

---

# Browser Object Model (BOM) in JavaScript

The Browser Object Model (BOM) provides JavaScript with the ability to interact with the browser window and its components. It's not part of the official JavaScript specification but is supported by most modern web browsers.

## Key Components of BOM

### 1. window Object

The `window` object is the top-level object in the BOM hierarchy, representing the browser window.

```javascript
console.log(window.innerWidth); // Width of the browser window
console.log(window.innerHeight); // Height of the browser window
```

### 2. navigator Object

Provides information about the browser itself.

```javascript
console.log(navigator.userAgent); // Information about the browser
console.log(navigator.language); // Preferred language of the user
```

### 3. screen Object

Offers information about the user's screen.

```javascript
console.log(screen.width); // Width of the user's screen
console.log(screen.height); // Height of the user's screen
```

### 4. history Object

Allows manipulation of the browser's history.

```javascript
history.back(); // Go back one page
history.forward(); // Go forward one page
history.go(-2); // Go back two pages
```

### 5. location Object

Provides information about the current URL and allows navigation.

```javascript
console.log(location.href); // Current URL
location.href = "https://example.com"; // Navigate to a new URL
```

## Working with BOM

### Opening a New Window

```javascript
const newWindow = window.open("https://example.com", "ExampleWindow", "width=500,height=400");
```

### Setting Timeouts and Intervals

```javascript
// Execute after 2 seconds
setTimeout(() => {
    console.log("Delayed message");
}, 2000);

// Execute every 1 second
const intervalId = setInterval(() => {
    console.log("Repeated message");
}, 1000);

// Stop the interval after 5 seconds
setTimeout(() => {
    clearInterval(intervalId);
}, 5000);
```

The BOM provides powerful tools for interacting with the browser environment, enabling developers to create more dynamic and interactive web applications.
