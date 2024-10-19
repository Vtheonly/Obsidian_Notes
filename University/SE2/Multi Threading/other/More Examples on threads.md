Sure! Here are five examples, each focusing on a different important thread function:

### Example 1: Using `pthread_self()`

This example demonstrates how to use `pthread_self()` to get the thread ID of the calling thread.

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function(void* arg) {
    printf("Thread %ld: started\n", pthread_self());
    sleep(1);
    printf("Thread %ld: finished\n", pthread_self());
    return NULL;
}

int main() {
    pthread_t tid;
    printf("Main thread %ld: start\n", pthread_self());
    pthread_create(&tid, NULL, thread_function, NULL);
    printf("Main thread %ld: created thread %ld\n", pthread_self(), tid);
    sleep(2);
    printf("Main thread %ld: end\n", pthread_self());
    return 0;
}
```


Or :

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function(void* arg) {
    printf("Thread ID: %lu\n", pthread_self());
    return NULL;
}

int main() {
    pthread_t tid1, tid2;
    
    pthread_create(&tid1, NULL, thread_function, NULL);
    pthread_create(&tid2, NULL, thread_function, NULL);
    
    printf("Main thread ID: %lu\n", pthread_self());
    
    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);
    
    return 0;
}

```

This example demonstrates the use of `pthread_self()` to get the ID of the current thread. It creates two threads and prints their IDs along with the main thread's ID.


---


### Example 2: Using `pthread_exit()`

This example demonstrates how to use `pthread_exit()` to terminate a thread and optionally return a status.

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function(void* arg) {
    printf("Thread %ld: started\n", pthread_self());
    sleep(1);
    printf("Thread %ld: exiting\n", pthread_self());
    pthread_exit((void*) 42); // 
}

int main() {
    pthread_t tid;
    void* status;
    printf("Main thread %ld: start\n", pthread_self());
    pthread_create(&tid, NULL, thread_function, NULL);
    printf("Main thread %ld: created thread %ld\n", pthread_self(), tid);
    pthread_join(tid, &status);
    printf("Main thread %ld: thread %ld exited with status %ld\n", pthread_self(), tid, (long) status);
    printf("Main thread %ld: end\n", pthread_self());
    return 0;
}
```


Or :

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

void* thread_function(void* arg) {
    int* result = malloc(sizeof(int));
    *result = 42;
    printf("Thread %lu: Exiting with result %d\n", pthread_self(), *result);
    pthread_exit(result);
}

int main() {
    pthread_t tid;
    void* thread_result;
    
    pthread_create(&tid, NULL, thread_function, NULL);
    
    pthread_join(tid, &thread_result);
    
    printf("Main thread: Thread returned %d\n", *(int*)thread_result);
    free(thread_result);
    
    return 0;
}

```

This example shows how to use `pthread_exit()` to terminate a thread and return a value. The thread allocates memory for the result, sets its value, and exits with `pthread_exit()`. The main thread then retrieves this value using `pthread_join()`.



---
### Example 3: Using `pthread_cancel()`

This example demonstrates how to use `pthread_cancel()` to cancel a thread.

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function(void* arg) {
    printf("Thread %ld: started\n", pthread_self());
    while (1) {
        printf("Thread %ld: running\n", pthread_self());
        sleep(1);
    }
    return NULL;
}

int main() {
    pthread_t tid;
    printf("Main thread %ld: start\n", pthread_self());
    pthread_create(&tid, NULL, thread_function, NULL);
    printf("Main thread %ld: created thread %ld\n", pthread_self(), tid);
    sleep(3);
    printf("Main thread %ld: canceling thread %ld\n", pthread_self(), tid);
    pthread_cancel(tid);
    pthread_join(tid, NULL);
    printf("Main thread %ld: end\n", pthread_self());
    return 0;
}
```



Or :

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function(void* arg) {
    int i = 0;
    while (1) {
        printf("Thread %lu: Working... %d\n", pthread_self(), i++);
        sleep(1);
    }
    return NULL;
}

int main() {
    pthread_t tid;
    
    pthread_create(&tid, NULL, thread_function, NULL);
    
    sleep(5);  // Let the thread run for 5 seconds
    
    printf("Main thread: Cancelling thread %lu\n", tid);
    pthread_cancel(tid);
    
    pthread_join(tid, NULL);
    printf("Main thread: Thread cancelled and joined\n");
    
    return 0;
}

```

This example demonstrates the use of `pthread_cancel()` to terminate a thread. The main thread creates a worker thread that runs indefinitely, then cancels it after 5 seconds.

---


### Example 4: Using `pthread_join()`

This example demonstrates how to use `pthread_join()` to make the calling thread wait for another thread to terminate.

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function(void* arg) {
    printf("Thread %ld: started\n", pthread_self());
    sleep(2);
    printf("Thread %ld: finished\n", pthread_self());
    return NULL;
}

int main() {
    pthread_t tid;
    printf("Main thread %ld: start\n", pthread_self());
    pthread_create(&tid, NULL, thread_function, NULL);
    printf("Main thread %ld: created thread %ld\n", pthread_self(), tid);
    pthread_join(tid, NULL);
    printf("Main thread %ld: end\n", pthread_self());
    return 0;
}
```

Or :

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function(void* arg) {
    int seconds = *(int*)arg;
    printf("Thread %lu: Starting to sleep for %d seconds\n", pthread_self(), seconds);
    sleep(seconds);
    printf("Thread %lu: Finished sleeping\n", pthread_self());
    return arg;
}

int main() {
    pthread_t tid1, tid2;
    int sleep_time1 = 3, sleep_time2 = 5;
    void *ret1, *ret2;
    
    pthread_create(&tid1, NULL, thread_function, &sleep_time1);
    pthread_create(&tid2, NULL, thread_function, &sleep_time2);
    
    printf("Main thread: Waiting for threads to finish\n");
    
    pthread_join(tid1, &ret1);
    printf("Main thread: Thread %lu joined, slept for %d seconds\n", tid1, *(int*)ret1);
    
    pthread_join(tid2, &ret2);
    printf("Main thread: Thread %lu joined, slept for %d seconds\n", tid2, *(int*)ret2);
    
    return 0;
}

```

This example shows how to use `pthread_join()` to wait for threads to complete. It creates two threads that sleep for different durations and then waits for both to finish using `pthread_join()`.


---
### Example 5: Using `pthread_detach()`

This example demonstrates how to use `pthread_detach()` to mark a thread as detached, meaning its resources are automatically released upon termination.

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function(void* arg) {
    printf("Thread %ld: started\n", pthread_self());
    sleep(2);
    printf("Thread %ld: finished\n", pthread_self());
    return NULL;
}

int main() {
    pthread_t tid;
    printf("Main thread %ld: start\n", pthread_self());
    pthread_create(&tid, NULL, thread_function, NULL);
    printf("Main thread %ld: created thread %ld\n", pthread_self(), tid);
    pthread_detach(tid);
    sleep(3);
    printf("Main thread %ld: end\n", pthread_self());
    return 0;
}
```

Or :

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function(void* arg) {
    printf("Thread %lu: Starting\n", pthread_self());
    sleep(2);
    printf("Thread %lu: Finishing\n", pthread_self());
    return NULL;
}

int main() {
    pthread_t tid;
    
    pthread_create(&tid, NULL, thread_function, NULL);
    
    pthread_detach(tid);
    printf("Main thread: Detached thread %lu\n", tid);
    
    sleep(3);  // Sleep to allow the detached thread to complete
    printf("Main thread: Exiting\n");
    
    return 0;
}

```

This example demonstrates the use of `pthread_detach()` to create a detached thread. The main thread creates a new thread and immediately detaches it, allowing the thread to run independently. The main thread then sleeps briefly to allow the detached thread to complete before the program exits.


---



These examples showcase the usage of different pthread functions for managing threads in C. Each example focuses on a specific function and demonstrates its typical use case.