AJAX (Asynchronous JavaScript and XML) allows you to send HTTP requests from a web page to a server and process the response without reloading the page. This is commonly done using the `XMLHttpRequest` object or the more modern `fetch` API. Below is a basic example of how to make an HTTP request using both methods.



```javascript
function makeRequest() {
  var xhr = new XMLHttpRequest();  // Creates a new XMLHttpRequest object
  xhr.open('GET', 'https://api.example.com/data', true);  // Initializes a request
  xhr.onreadystatechange = function () {  // Sets up a function to handle the state changes
    if (xhr.readyState == 4 && xhr.status == 200) {  // Checks if the request is complete and successful
      console.log(xhr.responseText);  // Logs the response text to the console
    }
  };
  xhr.send();  // Sends the request
}
```

### Breakdown of the code:

1. **Creating the XMLHttpRequest Object:**
   ```javascript
   var xhr = new XMLHttpRequest();
   ```
   This line creates a new instance of the `XMLHttpRequest` object, which is used to interact with servers via HTTP.

2. **Opening the Connection:**
   ```javascript
   xhr.open('GET', 'https://api.example.com/data', true);
   ```
   - `xhr.open` initializes a new request.
   - The first argument `'GET'` specifies the HTTP method to use. In this case, it's a GET request, which means we're requesting data from the server.
   - The second argument `'https://api.example.com/data'` is the URL to which the request is sent.
   - The third argument `true` indicates that the request should be asynchronous, meaning it will not block the execution of the script while waiting for the server's response.

3. **Handling the Response:**
   ```javascript
   xhr.onreadystatechange = function () {
     if (xhr.readyState == 4 && xhr.status == 200) {
       console.log(xhr.responseText);
     }
   };
   ```
   - `xhr.onreadystatechange` is an event handler that is triggered whenever the `readyState` property of the `XMLHttpRequest` object changes.
   - `xhr.readyState` represents the state of the request. The value `4` means the request is complete.
   - `xhr.status` represents the HTTP status code of the response. The value `200` means the request was successful.
   - If both conditions are met, the response text (data received from the server) is logged to the console.

4. **Sending the Request:**
   ```javascript
   xhr.send();
   ```
   - This method sends the request to the server.


### Explanation

1. **Using `XMLHttpRequest`**:
   - Create a new `XMLHttpRequest` object.
   - Open a connection to the server with the `open` method (`GET` method in this example).
   - Define a function to handle the `onreadystatechange` event, checking if the request is complete (`readyState == 4`) and successful (`status == 200`).
   - Send the request with the `send` method.

2. **Using `fetch`**:
   - Call `fetch` with the URL of the resource you want to request.
   - Use the `then` method to handle the response. Check if the response is OK with `response.ok`.
   - Convert the response to JSON with `response.json()`.
   - Use another `then` method to handle the JSON data.
   - Catch any errors with the `catch` method.

### Advantages of `fetch`

- **Promise-based**: Makes it easier to handle asynchronous operations.
- **Cleaner Syntax**: More readable and concise.
- **Better Error Handling**: `fetch` treats HTTP errors as failed promises, making it easier to handle errors.

### Example in an HTML file

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AJAX Example</title>
</head>
<body>
  <button onclick="makeRequest()">Fetch Data</button>
  <script>
    function makeRequest() {
      fetch('https://api.example.com/data')
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
          return response.json();
        })
        .then(data => console.log(data))
        .catch(error => console.error('There was a problem with your fetch operation:', error));
    }
  </script>
</body>
</html>
```

In this example, clicking the button will trigger the `makeRequest` function, which sends a request to the specified URL and logs the response data to the console.

