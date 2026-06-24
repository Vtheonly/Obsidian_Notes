---
title: "Asynchronous Tasks with Futures and Promises"
---

While `std::thread` is great for running tasks, it can be cumbersome to get a return value from a function running on a new thread. You would typically have to pass a pointer or reference to a shared variable and protect it with a mutex.

Modern C++ provides a much cleaner, higher-level abstraction for this: **asynchronous tasks** using `std::async`, `std::future`, and `std::promise` from the `<future>` header.

### The Problem: Getting a Return Value from a Thread

```cpp
// Old, cumbersome way
#include <thread>
#include <mutex>

void calculate(int* result) {
    // ... perform long calculation ...
    *result = 42;
}

int main() {
    int my_result = 0;
    std::thread t(calculate, &my_result);
    t.join();
    // my_result is now 42
    return 0;
}
```
This is verbose and requires manual synchronization if the data is more complex.

### `std::async` and `std::future`: The Easy Way

`std::async` is a function that runs a task asynchronously (potentially in a new thread). It returns a `std::future`, which is an object that will eventually hold the result of the task.

-   **`std::async`**: Runs a callable object asynchronously.
-   **`std::future<T>`**: Represents a future result of type `T`. It acts as a handle to the asynchronous operation's result.

```cpp
#include <iostream>
#include <future>
#include <chrono>

int long_calculation() {
    std::this_thread::sleep_for(std::chrono::seconds(2));
    return 42;
}

int main() {
    std::cout << "Starting calculation..." << std::endl;

    // Launch the calculation asynchronously
    std::future<int> my_future = std::async(std::launch::async, long_calculation);

    // ... do other work in the main thread ...
    std::cout << "Main thread is doing other work." << std::endl;

    // To get the result, call .get() on the future
    // This will block until the future is ready (i.e., the calculation is complete)
    int result = my_future.get();

    std::cout << "Calculation finished. Result is: " << result << std::endl;

    return 0;
}
```

**Key Points:**
-   `std::async` is often much better than creating a `std::thread` manually, as the C++ runtime can manage the threads more efficiently in a thread pool.
-   `my_future.get()` can only be called **once**. After you get the value, the future is no longer valid.

### `std::promise` and `std::future`: The Manual Way

Sometimes you need more control over when the result is set. A `std::promise` is an object that can store a value to be retrieved by a `std::future` object later.

This pattern separates the **producer** of the value (which uses the `std::promise`) from the **consumer** of the value (which uses the `std::future`).

-   **`std::promise<T>`**: The "producer" side. You create a promise, get its future, and then at some point, you fulfill the promise with a value using `.set_value()`.
-   **`std::future<T>`**: The "consumer" side. It is connected to the promise and will receive the value when it is set.

```cpp
#include <iostream>
#include <future>
#include <thread>

void producer_task(std::promise<int> my_promise) {
    std::cout << "Producer is calculating..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(2));

    // Fulfill the promise with the result
    my_promise.set_value(101);
}

int main() {
    // 1. Create a promise
    std::promise<int> my_promise;

    // 2. Get the future from the promise
    std::future<int> my_future = my_promise.get_future();

    // 3. Start a thread, moving the promise into it
    std::thread t(producer_task, std::move(my_promise));

    // ... do other work ...
    std::cout << "Main thread is waiting for the result." << std::endl;

    // 4. Get the result from the future
    int result = my_future.get();

    std::cout << "Producer finished. Result is: " << result << std::endl;

    t.join();
    return 0;
}
```

**Handling Exceptions**: You can also set an exception in a promise using `.set_exception()`. When the consumer calls `.get()` on the future, the exception will be re-thrown.

### Conclusion

-   Use **`std::async`** as the default, high-level tool for running one-off asynchronous tasks that return a value.
-   Use **`std::promise` and `std::future`** when you need more fine-grained control to decouple the producer and consumer of a result across different threads.

These tools provide a much safer and more expressive way to handle asynchronous computation than manual synchronization with threads and mutexes.
