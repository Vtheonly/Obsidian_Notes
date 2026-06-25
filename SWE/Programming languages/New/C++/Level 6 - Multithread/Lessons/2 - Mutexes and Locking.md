---
title: "Mutexes and Locking for Data Protection"
---

When multiple threads access and modify the same shared data, you can get a **race condition**—a bug where the final state of the data depends on the unpredictable order in which threads are scheduled by the OS. This leads to corrupted data and incorrect results.

To prevent race conditions, you must ensure **mutual exclusion**: only one thread can access the shared data at a time. The primary tool for this in C++ is the **mutex**.

### `std::mutex`

A `std::mutex` (from the `<mutex>` header) is a synchronization primitive that can be used to protect shared data. A mutex has two states: locked and unlocked.

-   **`lock()`**: A thread calls `lock()` to acquire the mutex. If the mutex is already locked by another thread, this call will **block** until the mutex is released.
-   **`unlock()`**: When the thread is finished with the shared data, it calls `unlock()` to release the mutex, allowing another waiting thread to acquire it.

**Example with a Race Condition:**

```cpp
#include <iostream>
#include <thread>
#include <vector>

int counter = 0;

void increment() {
    for (int i = 0; i < 100000; ++i) {
        counter++; // This is not atomic! It's a read-modify-write operation.
    }
}

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 10; ++i) {
        threads.push_back(std::thread(increment));
    }

    for (auto& t : threads) {
        t.join();
    }

    // The final value should be 1,000,000, but it will likely be less.
    std::cout << "Final counter value: " << counter << std::endl;
    return 0;
}
```

**Fixing it with `std::mutex`:**

```cpp
#include <iostream>
#include <thread>
#include <vector>
#include <mutex>

int counter = 0;
std::mutex mtx; // Create a mutex

void increment_safe() {
    for (int i = 0; i < 100000; ++i) {
        mtx.lock();   // Lock the mutex before accessing shared data
        counter++;
        mtx.unlock(); // Unlock the mutex after accessing shared data
    }
}

// ... (main function is the same, just calls increment_safe) ...
```

### The Problem with Manual Locking

Manually calling `lock()` and `unlock()` is dangerous. If an exception is thrown after `lock()` but before `unlock()`, the mutex will remain locked forever, causing a **deadlock** as other threads wait indefinitely.

### The RAII Solution: `std::lock_guard` and `std::scoped_lock`

To solve this, C++ provides RAII-style lock guards. These are objects that acquire a mutex in their constructor and release it in their destructor. This guarantees the mutex is always unlocked when the guard goes out of scope, even if an exception is thrown.

#### `std::lock_guard`

This is the simplest lock guard. It locks the mutex in its constructor and unlocks it in its destructor.

```cpp
#include <mutex>

std::mutex mtx;

void increment_with_lock_guard() {
    for (int i = 0; i < 100000; ++i) {
        std::lock_guard<std::mutex> lock(mtx); // Lock is acquired here
        counter++;
    } // 'lock' goes out of scope here, destructor is called, mutex is unlocked
}
```
This code is exception-safe and much cleaner. **You should always prefer lock guards over manual `lock()`/`unlock()` calls.**

#### `std::scoped_lock` (C++17)

`std::scoped_lock` is a more modern and flexible guard. It can lock multiple mutexes at once using a deadlock-avoidance algorithm, which is essential for more complex synchronization scenarios.

```cpp
std::mutex m1, m2;

void lock_multiple() {
    // Acquires locks on m1 and m2 in a deadlock-safe way
    std::scoped_lock lock(m1, m2);
    // ... access data protected by m1 and m2 ...
} // Both mutexes are unlocked here
```

### Conclusion

-   To prevent race conditions, protect shared data with a `std::mutex`.
-   **Never** use manual `lock()` and `unlock()` calls.
-   **Always** use an RAII lock guard like `std::lock_guard` (for a single mutex) or `std::scoped_lock` (for one or more mutexes) to ensure mutexes are managed safely and automatically.
