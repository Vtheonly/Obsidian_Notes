
Local Storage is part of the Web Storage API in the Browser Object Model, allowing data to be stored persistently in the browser.

### Local Storage Methods

#### Setting Items:

There are multiple ways to set items in Local Storage:

```javascript
window.localStorage.setItem("color", "#F00");
window.localStorage.fontWeight = "bold";
window.localStorage["fontSize"] = "20px";
```

The `setItem` method, dot notation, and bracket notation can all be used to store key-value pairs.

#### Getting Items:

Similarly, there are multiple ways to retrieve items:

```javascript
console.log(window.localStorage.getItem("color"));
console.log(window.localStorage.color);
console.log(window.localStorage["color"]);
```

The `getItem` method, dot notation, and bracket notation can all be used to retrieve values.

#### Removing Items:

```javascript
window.localStorage.removeItem("color");
```

The `removeItem` method deletes a specific key-value pair from Local Storage.

#### Clearing All Items:

```javascript
localStorage.clear();
```

The `clear` method removes all key-value pairs from Local Storage.

#### Getting Keys:

```javascript
const key = localStorage.key(0);
```

The `key` method returns the name of the key at the specified index.

### Practical Usage:

Setting a color in the page based on Local Storage:

```javascript
document.body.style.backgroundColor = window.localStorage.getItem("color");
```

### Inspecting Local Storage:

```javascript
console.log(window.localStorage);
console.log(typeof window.localStorage);
```

This will output the contents of Local Storage and its type (which is "object").

### Important Information:

- No Expiration Time: Data in Local Storage persists indefinitely.
- HTTP and HTTPS: Local Storage is protocol-specific.
- Private Tab: In private/incognito mode, Local Storage behavior may differ.

Local Storage provides 5MB (5120KB) of storage space in most browsers.

