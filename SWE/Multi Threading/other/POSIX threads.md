### POSIX and What It Is

**POSIX (Portable Operating System Interface)** is a family of standards specified by the IEEE Computer Society for maintaining compatibility between operating systems. POSIX defines the application programming interface (API), along with command line shells and utility interfaces, for software compatible with variants of Unix and other operating systems.

### Key Points about POSIX:
- **Standardization**: POSIX aims to standardize the interface between applications and the operating system, making it easier to port software between different Unix-like systems.
- **Components**: It includes standards for system calls, library functions, command-line utilities, and more.
- **Wide Adoption**: Many operating systems, including Linux, macOS, and various Unix variants, comply with POSIX standards to some degree.
- **Enhanced Portability**: By adhering to POSIX standards, developers can write code that is more portable across different platforms.

### POSIX Threads (pthreads)

POSIX threads, often referred to as pthreads, are a set of C library functions that provide a standardized way to create and manage threads in a program. These functions are defined in the `pthread.h` header file.

## Thread Management in C

To use threads in C, you need to use the POSIX threads (pthreads) library. This involves including the `pthread.h` library and using specific functions to create and manage threads. Here's a summary of the main functions used in managing threads:

### Main Functions for Thread Management

1. **Creating a Thread**:
   ```c
   int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine)(void *), void *arg);
   ```
   - **Parameters**:
     - `thread`: Pointer to a `pthread_t` variable where the thread ID will be stored.
     - `attr`: Pointer to a `pthread_attr_t` structure that specifies thread attributes.
     - `start_routine`: Function that the thread will execute.
     - `arg`: Argument to be passed to the `start_routine` function.

2. **Joining a Thread**:
   ```c
   int pthread_join(pthread_t thread, void **retval);
   ```
   - **Parameters**:
     - `thread`: The thread ID of the thread to join.
     - `retval`: Pointer to a location where the exit status of the thread will be stored.

3. **Detaching a Thread**:
   ```c
   int pthread_detach(pthread_t thread);
   ```
   - **Parameters**:
     - `thread`: The thread ID of the thread to detach.

4. **Exiting a Thread**:
   ```c
   void pthread_exit(void *retval);
   ```
   - **Parameters**:
     - `retval`: The exit status of the thread.

5. **Initializing a Mutex**:
   ```c
   int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
   ```
   - **Parameters**:
     - `mutex`: Pointer to a `pthread_mutex_t` variable.
     - `attr`: Pointer to a `pthread_mutexattr_t` structure that specifies mutex attributes.

6. **Locking a Mutex**:
   ```c
   int pthread_mutex_lock(pthread_mutex_t *mutex);
   ```
   - **Parameters**:
     - `mutex`: Pointer to a `pthread_mutex_t` variable.

7. **Unlocking a Mutex**:
   ```c
   int pthread_mutex_unlock(pthread_mutex_t *mutex);
   ```
   - **Parameters**:
     - `mutex`: Pointer to a `pthread_mutex_t` variable.

### Example Code

Here's a simple example of creating and managing threads using pthreads:

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

void *print_message(void *ptr) {
    char *message;
    message = (char *) ptr;
    printf("%s\n", message);
    pthread_exit(NULL);
}

int main() {
    pthread_t thread1, thread2;
    char *message1 = "Thread 1";
    char *message2 = "Thread 2";
    int iret1, iret2;

    iret1 = pthread_create(&thread1, NULL, print_message, (void *) message1);
    iret2 = pthread_create(&thread2, NULL, print_message, (void *) message2);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("Thread 1 returns: %d\n", iret1);
    printf("Thread 2 returns: %d\n", iret2);

    exit(0);
}
```

This example demonstrates creating two threads, each printing a message, and then joining them back to the main thread.