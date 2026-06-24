In JavaScript, the `URL` object provides methods and properties to work with URLs. It allows you to easily parse, manipulate, and extract information from URLs. Here's a basic overview of how to use the `URL` object:

### Creating a URL Object:

You can create a `URL` object by passing a URL string to its constructor:

```javascript
const urlString = "https://www.example.com/path?name=John&age=30";
const url = new URL(urlString);
```

### Accessing Components of the URL:

Once you have a `URL` object, you can access various components of the URL, such as protocol, host, pathname, search parameters, etc.

```javascript
console.log("Protocol:", url.protocol); // "https:"
console.log("Host:", url.host); // "www.example.com"
console.log("Pathname:", url.pathname); // "/path"
console.log("Search:", url.search); // "?name=John&age=30"
console.log("Hash:", url.hash); // ""
```

### Modifying Components:

You can also modify components of the URL and convert the `URL` object back to a string:

```javascript
url.pathname = "/new-path";
url.searchParams.set("name", "Jane");
console.log(url.toString()); // "https://www.example.com/new-path?name=Jane&age=30"
```

### Extracting the Current URL of the Website:

If you want to get the URL of the current page (the page where the JavaScript is running), you can use the `window.location` object:

```javascript
const currentUrl = window.location.href;
console.log("Current URL:", currentUrl);
```

### Example: Extracting Query Parameters:

Let's say you have a URL like `https://www.example.com/search?query=JavaScript&page=1` and you want to extract the query parameters:

```javascript
const urlString = "https://www.example.com/search?query=JavaScript&page=1";
const url = new URL(urlString);

const queryParams = new URLSearchParams(url.search);
const query = queryParams.get("query");
const page = queryParams.get("page");

console.log("Query:", query); // "JavaScript"
console.log("Page:", page); // "1"
```

In this example, the `URLSearchParams` object is used to easily work with the query parameters.

Using the `URL` object provides a convenient and standardized way to work with URLs in JavaScript. It's particularly useful when dealing with complex URLs and extracting or modifying their components.