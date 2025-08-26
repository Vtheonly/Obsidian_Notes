---
title: "Working with std::thread"
---

The `std::thread` class, found in the `<thread>` header, is the primary way to create and manage threads in C++. A `std::thread` object represents a single thread of execution.

### Creating a `std::thread`

You create a `std::thread` by constructing it with a **callable** object (a function, function object, or lambda) that the thread will execute.

```cpp
#include <iostream>
#include <thread>

void hello() {
    std::cout << "Hello from a function." << std::endl;
}

class Greeter {
public:
    void operator()() const {
        std::cout << "Hello from a function object." << std::endl;
    }
};

int main() {
    // 1. Create a thread from a free function
    std::thread t1(hello);

    // 2. Create a thread from a function object (functor)
    Greeter greeter;
    std::thread t2(greeter);

    // 3. Create a thread from a lambda expression (most common)
    std::thread t3([]() {
        std::cout << "Hello from a lambda." << std::endl;
    });

    // Wait for all threads to complete
    t1.join();
    t2.join();
    t3.join();

    return 0;
}
```

### Passing Arguments to a Thread's Function

You can pass arguments to the callable object by providing them as additional arguments to the `std::thread` constructor.

```cpp
#include <iostream>
#include <thread>
#include <string>

void print_message(const std::string& message, int count) {
    for (int i = 0; i < count; ++i) {
        std::cout << message << std::endl;
    }
}

int main() {
    std::string msg = "Hello with arguments";
    // The arguments are copied into the thread's internal storage
    std::thread t(print_message, msg, 3);
    t.join();
    return 0;
}
```

**Important Note on Arguments**: The arguments are **copied** by default. If you want to pass an argument by reference, you must wrap it in `std::ref` or `std::cref` from the `<functional>` header.

```cpp
#include <functional> // For std::ref

void modify_string(std::string& s) {
    s = "modified";
}

int main() {
    std::string my_str = "original";
    // Pass by reference using std::ref
    std::thread t(modify_string, std::ref(my_str));
    t.join();
    std::cout << my_str << std::endl; // Output: modified
    return 0;
}
```

### Joining and Detaching Threads

A `std::thread` object must be either **joined** or **detached** before it is destroyed.

1.  **`join()`**: This blocks the calling thread until the thread represented by the `std::thread` object has finished its execution. This is the most common way to manage a thread's lifetime, as it ensures all work is complete before proceeding.

    ```cpp
    std::thread t(my_task);
    // ... do other work ...
    t.join(); // Wait for my_task to finish
    // ... continue, knowing the task is done ...
    ```

2.  **`detach()`**: This separates the thread of execution from the `std::thread` object. The thread becomes a "daemon" thread that runs in the background. You can no longer communicate with it, and you don't know when it will finish. This is less common and should be used with care, as it can easily lead to bugs if the detached thread outlives the resources it depends on.

    ```cpp
    std::thread t(background_task);
    t.detach(); // The thread will run independently
    // The main thread continues immediately
    ```

If a `std::thread` object is destroyed without being joined or detached, `std::terminate` is called, and your program will crash. This is a safety feature to prevent you from accidentally forgetting to manage a thread's lifetime.

### Other Useful `std::thread` Functions

-   **`get_id()`**: Returns a unique `std::thread::id` for the thread.
-   **`joinable()`**: Returns `true` if the thread can be joined or detached.
-   **`std::this_thread::sleep_for()`**: Pauses the *current* thread for a specified duration.
-   **`std::this_thread::get_id()`**: Gets the ID of the *current* thread.

```cpp
#include <iostream>
#include <thread>
#include <chrono>

void worker() {
    std::cout << "Worker thread ID: " << std::this_thread::get_id() << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(1));
}

int main() {
    std::thread t(worker);
    std::cout << "Main thread ID: " << std::this_thread::get_id() << std::endl;
    t.join();
    return 0;
}
```
