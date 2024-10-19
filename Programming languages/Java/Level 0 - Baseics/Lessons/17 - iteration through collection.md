### Iterating Through Collections in Java

In Java, collections represent groups of objects. Common collection types include arrays, lists, and various classes implementing the `List`, `Set`, or `Map` interfaces. Iterating through these collections is a fundamental task in programming.

#### 1. **Iterating Through an Array**

Arrays in Java are fixed in size and hold elements of a single data type. You can iterate through an array using a `for` loop or an enhanced `for-each` loop.

- **Using a `for` Loop:**

```java
int[] numbers = {1, 2, 3, 4, 5};

for (int i = 0; i < numbers.length; i++) {
    System.out.println("Element at index " + i + ": " + numbers[i]);
}
```

- **Using a `for-each` Loop:**

```java
for (int num : numbers) {
    System.out.println("Number: " + num);
}
```

#### 2. **Iterating Through a List**

The `List` interface is part of the Java Collections Framework and allows for dynamic resizing and element manipulation. `ArrayList` is one of the most commonly used classes that implement `List`.

- **Using a `for` Loop:**

```java
List<String> fruits = new ArrayList<>();
fruits.add("Apple");
fruits.add("Banana");
fruits.add("Cherry");

for (int i = 0; i < fruits.size(); i++) {
    System.out.println("Fruit at index " + i + ": " + fruits.get(i));
}
```

- **Using a `for-each` Loop:**

```java
for (String fruit : fruits) {
    System.out.println("Fruit: " + fruit);
}
```

- **Using an Iterator:**

```java
Iterator<String> iterator = fruits.iterator();
while (iterator.hasNext()) {
    System.out.println("Fruit: " + iterator.next());
}
```

- **Using a Lambda Expression (Java 8+):**

```java
fruits.forEach(fruit -> System.out.println("Fruit: " + fruit));
```

#### 3. **Iterating Through a Set**

A `Set` is a collection that does not allow duplicate elements. The most commonly used `Set` implementations are `HashSet`, `LinkedHashSet`, and `TreeSet`.

- **Using a `for-each` Loop:**

```java
Set<Integer> uniqueNumbers = new HashSet<>();
uniqueNumbers.add(10);
uniqueNumbers.add(20);
uniqueNumbers.add(30);

for (int number : uniqueNumbers) {
    System.out.println("Unique number: " + number);
}
```

- **Using an Iterator:**

```java
Iterator<Integer> setIterator = uniqueNumbers.iterator();
while (setIterator.hasNext()) {
    System.out.println("Unique number: " + setIterator.next());
}
```

#### 4. **Iterating Through a Map**

A `Map` is a collection of key-value pairs. `HashMap` is a widely used implementation of `Map`.

- **Using a `for-each` Loop for `entrySet`:**

```java
Map<String, Integer> ageMap = new HashMap<>();
ageMap.put("Alice", 30);
ageMap.put("Bob", 25);
ageMap.put("Charlie", 35);

for (Map.Entry<String, Integer> entry : ageMap.entrySet()) {
    System.out.println(entry.getKey() + " is " + entry.getValue() + " years old.");
}
```

- **Using a `for-each` Loop for `keySet`:**

```java
for (String key : ageMap.keySet()) {
    System.out.println(key + " is " + ageMap.get(key) + " years old.");
}
```

- **Using a Lambda Expression (Java 8+):**

```java
ageMap.forEach((key, value) -> System.out.println(key + " is " + value + " years old."));
```

#### 5. **Iterating Through a Queue**

A `Queue` is a collection used to hold elements prior to processing. It follows FIFO (First-In-First-Out) order.

- **Using a `for-each` Loop:**

```java
Queue<String> queue = new LinkedList<>();
queue.add("First");
queue.add("Second");
queue.add("Third");

for (String item : queue) {
    System.out.println("Queue item: " + item);
}
```

- **Using an Iterator:**

```java
Iterator<String> queueIterator = queue.iterator();
while (queueIterator.hasNext()) {
    System.out.println("Queue item: " + queueIterator.next());
}
```

### Summary

- Arrays can be iterated using a simple `for` loop or a `for-each` loop.
- Lists, Sets, and Queues can be iterated using `for` loops, `for-each` loops, iterators, or lambda expressions.
- Maps require iteration over keys, values, or entries, commonly using `for-each` loops or lambda expressions.

Iterating through collections efficiently is crucial for manipulating and processing data in Java.