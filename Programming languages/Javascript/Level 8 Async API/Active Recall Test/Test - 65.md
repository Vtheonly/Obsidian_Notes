### JavaScript `URL` Object Quiz

Here are 15 quiz questions based on the `URL` object in JavaScript:

1. - [ ] **What is the purpose of the `URL` object in JavaScript?**
   - [ ] a) To fetch data from a server.
   - [ ] b) To parse, manipulate, and extract information from URLs.
   - [ ] c) To navigate between pages.
   - [ ] d) To store data in the local storage.

2. - [ ] **How do you create a `URL` object?**
   - [ ] a) `new URL("https://example.com")`
   - [ ] b) `URL("https://example.com")`
   - [ ] c) `create URL("https://example.com")`
   - [ ] d) `url("https://example.com")`

3. - [ ] **Which property of the `URL` object returns the protocol of the URL?**
   - [ ] a) `url.host`
   - [ ] b) `url.protocol`
   - [ ] c) `url.pathname`
   - [ ] d) `url.search`

4. - [ ] **What does the `url.host` property return?**
   - [ ] a) The domain name.
   - [ ] b) The entire URL.
   - [ ] c) The protocol and domain name.
   - [ ] d) The pathname and search parameters.

5. - [ ] **How do you change the pathname of a `URL` object?**
   - [ ] a) `url.setPathname("/new-path")`
   - [ ] b) `url.pathname = "/new-path"`
   - [ ] c) `url.changePath("/new-path")`
   - [ ] d) `url.path("/new-path")`

6. - [ ] **Which method is used to update a search parameter in a `URL` object?**
   - [ ] a) `url.updateParam()`
   - [ ] b) `url.setParam()`
   - [ ] c) `url.searchParams.set()`
   - [ ] d) `url.modifySearch()`

7. - [ ] **How do you get the current page URL in JavaScript?**
   - [ ] a) `document.currentURL`
   - [ ] b) `window.url`
   - [ ] c) `window.location.href`
   - [ ] d) `location.url`

8. - [ ] **What is the output of the following code?**
   ```javascript
   const url = new URL("https://example.com/path?query=JavaScript");
   console.log(url.search);
   ```
   - [ ] a) `"query=JavaScript"`
   - [ ] b) `"?query=JavaScript"`
   - [ ] c) `"https://example.com?query=JavaScript"`
   - [ ] d) `"query"`

9. - [ ] **How can you add a new query parameter to an existing `URL` object?**
   - [ ] a) `url.addQuery("key", "value")`
   - [ ] b) `url.searchParams.append("key", "value")`
   - [ ] c) `url.searchParams.add("key", "value")`
   - [ ] d) `url.appendParam("key", "value")`

10. - [ ] **Which method converts a `URL` object back to a string?**
    - [ ] a) `url.toText()`
    - [ ] b) `url.stringify()`
    - [ ] c) `url.toString()`
    - [ ] d) `url.convertToString()`

11. - [ ] **What is returned by `url.pathname` for the URL `https://example.com/page?query=1`?**
    - [ ] a) `"/page?query=1"`
    - [ ] b) `"https://example.com/page"`
    - [ ] c) `"/page"`
    - [ ] d) `"page"`

12. - [ ] **True or False: The `URLSearchParams` object can only be used with `URL` objects.**
    - [ ] a) True
    - [ ] b) False

13. - [ ] **What does the `url.hash` property return if the URL does not contain a fragment identifier?**
    - [ ] a) `"#"`
    - [ ] b) `null`
    - [ ] c) `""` (an empty string)
    - [ ] d) `undefined`

14. - [ ] **How do you remove a specific query parameter from a `URL` object?**
    - [ ] a) `url.removeQueryParam("key")`
    - [ ] b) `url.searchParams.delete("key")`
    - [ ] c) `url.query.remove("key")`
    - [ ] d) `url.search.delete("key")`

15. - [ ] **What does `window.location.href` represent in JavaScript?**
    - [ ] a) The URL of the current document.
    - [ ] b) The base URL of the document.
    - [ ] c) The host name of the current document.
    - [ ] d) The search parameters of the current document.

---

1. **What is the purpose of the `URL` object in JavaScript?**
   - **Answer:** b) To parse, manipulate, and extract information from URLs.

2. **How do you create a `URL` object?**
   - **Answer:** a) `new URL("https://example.com")`

3. **Which property of the `URL` object returns the protocol of the URL?**
   - **Answer:** b) `url.protocol`

4. **What does the `url.host` property return?**
   - **Answer:** a) The domain name.

5. **How do you change the pathname of a `URL` object?**
   - **Answer:** b) `url.pathname = "/new-path"`

6. **Which method is used to update a search parameter in a `URL` object?**
   - **Answer:** c) `url.searchParams.set()`

7. **How do you get the current page URL in JavaScript?**
   - **Answer:** c) `window.location.href`

8. **What is the output of the following code?**
   ```javascript
   const url = new URL("https://example.com/path?query=JavaScript");
   console.log(url.search);
   ```
   - **Answer:** b) `"?query=JavaScript"`

9. **How can you add a new query parameter to an existing `URL` object?**
   - **Answer:** b) `url.searchParams.append("key", "value")`

10. **Which method converts a `URL` object back to a string?**
    - **Answer:** c) `url.toString()`

11. **What is returned by `url.pathname` for the URL `https://example.com/page?query=1`?**
    - **Answer:** c) `"/page"`

12. **True or False: The `URLSearchParams` object can only be used with `URL` objects.**
    - **Answer:** b) False

13. **What does the `url.hash` property return if the URL does not contain a fragment identifier?**
    - **Answer:** c) `""` (an empty string)

14. **How do you remove a specific query parameter from a `URL` object?**
    - **Answer:** b) `url.searchParams.delete("key")`

15. **What does `window.location.href` represent in JavaScript?**
    - **Answer:** a) The URL of the current document.
