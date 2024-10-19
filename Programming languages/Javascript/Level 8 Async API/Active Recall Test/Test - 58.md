Here are 15 quiz questions based on AJAX, `XMLHttpRequest`, and `fetch`:

### AJAX, `XMLHttpRequest`, and `Fetch` Quiz

1. **What does AJAX stand for?**
   - [ ] Asynchronous JavaScript and XML
   - [ ] Asynchronous JSON and XML
   - [ ] Advanced JavaScript and XML
   - [ ] Asynchronous JavaScript and XHTML

2. **What is the purpose of AJAX in web development?**
   - [ ] To reload the entire page after sending a request
   - [ ] To send HTTP requests to a server and process the response without reloading the page
   - [ ] To create server-side scripts
   - [ ] To handle user authentication

3. **Which method is used to send an HTTP request in an `XMLHttpRequest` object?**
   - [ ] `getRequest`
   - [ ] `sendRequest`
   - [ ] `open`
   - [ ] `send`

4. **What does the third argument in the `xhr.open` method specify?**
   - [ ] The HTTP method
   - [ ] The URL
   - [ ] Whether the request should be synchronous or asynchronous
   - [ ] The headers for the request

5. **What value of `xhr.readyState` indicates that the request is complete?**
   - [ ] 1
   - [ ] 2
   - [ ] 3
   - [ ] 4

6. **Which HTTP status code indicates that the request was successful?**
   - [ ] 200
   - [ ] 400
   - [ ] 404
   - [ ] 500

7. **In an `XMLHttpRequest`, where is the server's response stored?**
   - [ ] `xhr.responseURL`
   - [ ] `xhr.responseText`
   - [ ] `xhr.responseData`
   - [ ] `xhr.responseCode`

8. **What type of object does the `fetch` function return?**
   - [ ] `XMLHttpRequest`
   - [ ] `Promise`
   - [ ] `Response`
   - [ ] `Error`

9. **Which method is used to handle the response in a `fetch` operation?**
   - [ ] `then`
   - [ ] `catch`
   - [ ] `send`
   - [ ] `onreadystatechange`

10. **What does `fetch` use to handle errors that occur during the request?**
    - [ ] `onerror`
    - [ ] `try...catch`
    - [ ] `catch`
    - [ ] `finally`

11. **Which method is used to convert the response to JSON in a `fetch` operation?**
    - [ ] `response.json()`
    - [ ] `response.text()`
    - [ ] `response.convert()`
    - [ ] `response.parse()`

12. **What is one advantage of using `fetch` over `XMLHttpRequest`?**
    - [ ] It is synchronous by default
    - [ ] It is promise-based and provides a cleaner syntax
    - [ ] It doesn't require a URL
    - [ ] It automatically parses the response to JSON

13. **How do you handle a failed `fetch` request in the promise chain?**
    - [ ] By checking `xhr.status`
    - [ ] By using the `catch` method
    - [ ] By using `try...catch`
    - [ ] By using `finally`

14. **Which of the following is a correct way to handle a non-OK HTTP response in a `fetch` request?**
    - [ ] `if (!response.ok) { throw new Error('Network response was not ok'); }`
    - [ ] `if (!response.status) { throw new Error('Failed response'); }`
    - [ ] `if (response.error) { console.log('Error occurred'); }`
    - [ ] `if (response.ok === false) { alert('Request failed'); }`

15. **What event handler is triggered when the `readyState` of an `XMLHttpRequest` changes?**
    - [ ] `onload`
    - [ ] `onerror`
    - [ ] `onreadystatechange`
    - [ ] `onresponse`

---

**Answers:**
1. Asynchronous JavaScript and XML
2. To send HTTP requests to a server and process the response without reloading the page
3. `send`
4. Whether the request should be synchronous or asynchronous
5. 4
6. 200
7. `xhr.responseText`
8. `Promise`
9. `then`
10. `catch`
11. `response.json()`
12. It is promise-based and provides a cleaner syntax
13. By using the `catch` method
14. `if (!response.ok) { throw new Error('Network response was not ok'); }`
15. `onreadystatechange`