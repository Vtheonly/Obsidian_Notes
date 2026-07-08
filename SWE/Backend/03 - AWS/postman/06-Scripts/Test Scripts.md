---
tags: [postman, scripts, tests]
---

# Test Scripts

> [!summary] TL;DR
> **Test scripts** run in JavaScript *after* the response arrives. Use them to assert status, headers, body content, response time — and to chain requests by saving variables.

## Where They Run

```mermaid
flowchart LR
    Send[Send request] --> Resp[Receive response]
    Resp --> ReqTest[Request Tests]
    ReqTest --> FldTest[Folder Tests]
    FldTest --> CollTest[Collection Tests]
```

## The `pm.response` Object (Cheat Sheet)

| API                                  | Purpose                                |
| ------------------------------------ | -------------------------------------- |
| `pm.response.code`                   | HTTP status code (number).             |
| `pm.response.status`                 | Status text.                            |
| `pm.response.responseTime`           | Time in ms.                             |
| `pm.response.headers.get('X')`       | Response header by name.               |
| `pm.response.text()`                 | Raw response body as string.           |
| `pm.response.json()`                 | Parsed JSON body.                       |
| `pm.response.to.have.status(200)`    | Chained assertion.                     |
| `pm.expect(value).to...`             | Chai-style assertion.                  |

## The `pm.test()` Function

```javascript
pm.test('Status is 200', () => {
  pm.response.to.have.status(200);
});
```

- First arg: test name (shown in results).
- Second arg: function that throws on failure.

## Common Assertions

### Status code

```javascript
pm.test('Returns 200', () => {
  pm.response.to.have.status(200);
});
```

### Status code (any of several)

```javascript
pm.test('Returns 2xx', () => {
  pm.expect(pm.response.code).to.be.oneOf([200, 201, 204]);
});
```

### Response time

```javascript
pm.test('Responds within 500ms', () => {
  pm.expect(pm.response.responseTime).to.below(500);
});
```

### Header exists

```javascript
pm.test('Has content-type', () => {
  pm.response.to.have.header('Content-Type');
});
```

### Body contains string

```javascript
pm.test('Body contains "Lovelace"', () => {
  pm.expect(pm.response.text()).to.include('Lovelace');
});
```

### JSON body — exact value

```javascript
pm.test('User name is Ada', () => {
  const j = pm.response.json();
  pm.expect(j.name).to.eql('Ada');
});
```

### JSON body — schema

```javascript
pm.test('Matches schema', () => {
  const schema = {
    type: 'object',
    required: ['id', 'email'],
    properties: {
      id: { type: 'number' },
      email: { type: 'string', format: 'email' }
    }
  };
  pm.response.to.have.jsonSchema(schema);
});
```

### Array length

```javascript
pm.test('Returns 10 users', () => {
  const arr = pm.response.json();
  pm.expect(arr).to.be.an('array').of.length(10);
});
```

### Chained assertions (one test, multiple checks)

```javascript
pm.test('Valid user object', () => {
  const j = pm.response.json();
  pm.expect(j).to.have.property('id');
  pm.expect(j.id).to.be.a('number');
  pm.expect(j.email).to.match(/^[^@]+@[^@]+\.[^@]+$/);
});
```

## Saving Data for the Next Request

```javascript
// In Tests of "Create user":
const j = pm.response.json();
pm.environment.set('userId', j.id);
pm.environment.set('userEmail', j.email);
```

Then the next request uses `{{userId}}` in the URL.

## Reading Request Data

```javascript
const reqMethod = pm.request.method;
const reqUrl = pm.request.url.toString();
console.log(`Sent ${reqMethod} ${reqUrl}`);
```

## Built-in Snippets

Next to the Tests editor there's a list of snippets you can click to insert:
- "Status code: Code is 200"
- "Response body: JSON value check"
- "Response headers: Content-Type header check"
- "Response time is less than 200 ms"
- "Status code: Successful POST request"

## Common Patterns

### Test that an array has *at least one* matching item

```javascript
pm.test('At least one admin', () => {
  const arr = pm.response.json();
  pm.expect(arr.some(u => u.role === 'admin')).to.be.true;
});
```

### Test pagination

```javascript
pm.test('Pagination metadata valid', () => {
  const j = pm.response.json();
  pm.expect(j.page).to.eql(1);
  pm.expect(j.per_page).to.eql(20);
  pm.expect(j.items).to.be.an('array').with.lengthOf.at.most(20);
});
```

## Common Mistakes

-  Calling `pm.response.json()` on a non-JSON body (throws).
-  Forgetting to wrap assertions in `pm.test(...)` (no name in results).
-  Testing too many things in one `pm.test` (hard to debug).
-  Using `console.log` instead of an assertion — won't show as a fail.

## Related Notes
- [[Pre-request Scripts]] · [[Assertions and Automated API Testing]] · [[Collection Runner]] · [[NewmanCLI]]
