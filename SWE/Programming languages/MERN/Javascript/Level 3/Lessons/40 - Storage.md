


Session Storage is part of the Web Storage API in the Browser Object Model, providing temporary storage that lasts for the duration of a browser session.

#### setItem:

```javascript
sessionStorage.setItem("username", "John");
```

The `setItem` method stores a key-value pair in Session Storage.

#### getItem:

```javascript
const username = sessionStorage.getItem("username");
console.log(username); // "John"
```

The `getItem` method retrieves the value associated with a given key.

#### removeItem:

```javascript
sessionStorage.removeItem("username");
```

The `removeItem` method deletes a specific key-value pair from Session Storage.

#### clear:

```javascript
sessionStorage.clear();
```

The `clear` method removes all key-value pairs from Session Storage.

#### key:

```javascript
const firstKey = sessionStorage.key(0);
console.log(firstKey); // Returns the name of the first key in Session Storage
```

The `key` method returns the name of the key at the specified index.

### Info:

- New Tab = New Session:
  Opening a new tab creates a new, separate session storage.

- Duplicate Tab = Copy Session:
  Duplicating a tab copies the session storage from the original tab.

- New Tab With Same URL = New Session:
  Opening a new tab with the same URL still creates a new, separate session storage.

Additional Information:
- Session Storage is cleared when the tab or window is closed.
- It's limited to about 5MB of data in most browsers.
- Data in Session Storage is only accessible from the same origin (protocol, domain, and port).
