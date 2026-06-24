
Destructuring is a powerful feature in JavaScript that allows you to extract values from arrays or properties from objects into distinct variables.

### Array Destructuring:

#### Basic Array Destructuring:

```javascript
const [a, b, c] = [1, 2, 3];
console.log(a, b, c); // 1 2 3
```

#### Skipping Elements:

```javascript
const [a, , c] = [1, 2, 3];
console.log(a, c); // 1 3
```

#### Rest Pattern:

```javascript
const [a, ...rest] = [1, 2, 3, 4, 5];
console.log(a, rest); // 1 [2, 3, 4, 5]
```

#### Default Values:

```javascript
const [a, b, c = 3] = [1, 2];
console.log(a, b, c); // 1 2 3
```

#### Swapping Variables:

```javascript
let a = 1, b = 2;
[a, b] = [b, a];
console.log(a, b); // 2 1
```

### Object Destructuring:

#### Basic Object Destructuring:

```javascript
const { name, age } = { name: 'John', age: 30 };
console.log(name, age); // John 30
```

#### Renaming Variables:

```javascript
const { name: fullName, age } = { name: 'John', age: 30 };
console.log(fullName, age); // John 30
```

#### Default Values:

```javascript
const { name, age = 25 } = { name: 'John' };
console.log(name, age); // John 25
```

#### Nested Object Destructuring:

```javascript
const { address: { city } } = { address: { city: 'New York' } };
console.log(city); // New York
```

#### Rest Pattern in Objects:

```javascript
const { name, ...rest } = { name: 'John', age: 30, city: 'New York' };
console.log(name, rest); // John { age: 30, city: 'New York' }
```

### Mixed Destructuring:

```javascript
const { name, [0]: firstHobby } = { name: 'John', hobbies: ['reading', 'sports'] };
console.log(name, firstHobby); // John reading
```

### Function Parameter Destructuring:

#### Array Parameter Destructuring:

```javascript
function printCoords([x, y]) {
    console.log(`X: ${x}, Y: ${y}`);
}
printCoords([10, 20]); // X: 10, Y: 20
```

#### Object Parameter Destructuring:

```javascript
function printPerson({ name, age }) {
    console.log(`${name} is ${age} years old`);
}
printPerson({ name: 'John', age: 30 }); // John is 30 years old
```

### Destructuring with Computed Property Names:

```javascript
const key = 'name';
const { [key]: personName } = { name: 'John' };
console.log(personName); // John
```

### Destructuring Returned Arrays:

```javascript
function getCoords() {
    return [10, 20];
}
const [x, y] = getCoords();
console.log(x, y); // 10 20
```

### Destructuring Returned Objects:

```javascript
function getPerson() {
    return { name: 'John', age: 30 };
}
const { name, age } = getPerson();
console.log(name, age); // John 30
```

### Destructuring in Loops:

```javascript
const people = [{ name: 'John' }, { name: 'Jane' }];
for (const { name } of people) {
    console.log(name);
}
// John
// Jane
```

These examples cover a wide range of destruct