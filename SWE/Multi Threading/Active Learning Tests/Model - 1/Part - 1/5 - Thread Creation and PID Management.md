# Quiz on Thread Creation and PID Management in GNU/Linux

Please select the correct option for each question.

### Questions

1. What library must be linked to compile the `pthread-pid.c` program?
   - [ ] A) -lm
   - [ ] B) -lpthread
   - [ ] C) -lrt
   - [ ] D) -lX11

2. In the provided code, what does the `fonction()` function print?
   - [ ] A) Main thread PID
   - [ ] B) Child thread PID
   - [ ] C) Process name
   - [ ] D) Execution time

3. Which function is used to create a new thread in the `pthread-pid.c` example?
   - [ ] A) pthread_create
   - [ ] B) pthread_join
   - [ ] C) pthread_exit
   - [ ] D) pthread_start

4. What is the output of `printf("Main PID = %d\n", (int)getpid());` in `main()`?
   - [ ] A) The PID of the child thread
   - [ ] B) The PID of the main thread
   - [ ] C) The PID of the executing process
   - [ ] D) An error message

5. Which command is used to display the current processes and threads?
   - [ ] A) list
   - [ ] B) jobs
   - [ ] C) ps
   - [ ] D) show

6. Scheduler activations aim to provide what type of performance?
   - [ ] A) Improved disk performance
   - [ ] B) Enhanced network performance
   - [ ] C) Kernel thread performance
   - [ ] D) User application performance

7. What happens when a thread is blocked on a system call?
   - [ ] A) The process terminates.
   - [ ] B) Another ready thread should be executed.
   - [ ] C) The thread restarts from the beginning.
   - [ ] D) The kernel is notified to kill the thread.

8. What is a key mechanism used for notifying the execution system of a thread blockage?
   - [ ] A) Signal
   - [ ] B) Upcall
   - [ ] C) Callback
   - [ ] D) Interrupt

9. How does the kernel manage virtual processors for each process?
   - [ ] A) By assigning one to each thread statically
   - [ ] B) By allowing the process to request and return them
   - [ ] C) By limiting to a maximum of two processors
   - [ ] D) By using only one virtual processor

10. In case of a hardware interrupt, what happens if it concerns a different process?
    - [ ] A) The system crashes.
    - [ ] B) The thread is restored to its previous state.
    - [ ] C) The thread is terminated.
    - [ ] D) The kernel shuts down.

11. Which of the following statements is true regarding related interrupts?
    - [ ] A) The thread is immediately terminated.
    - [ ] B) The thread remains blocked while the system handles it.
    - [ ] C) The thread is restored to its previous state.
    - [ ] D) The system ignores the interrupt.

12. What is the purpose of the `while(1);` loop in both `fonction()` and `main()`?
    - [ ] A) To pause the program
    - [ ] B) To create an infinite execution
    - [ ] C) To handle interrupts
    - [ ] D) To wait for user input

13. When using `pthread_create()`, what is the third argument that specifies the function to run?
    - [ ] A) arg
    - [ ] B) function
    - [ ] C) thread_func
    - [ ] D) fonction

14. What is one potential downside of thread blockage in a multithreaded environment?
    - [ ] A) Increased CPU usage
    - [ ] B) Decreased responsiveness
    - [ ] C) Automatic termination of threads
    - [ ] D) Memory leaks

15. What is the primary benefit of using scheduler activations?
    - [ ] A) Reduced context switches between threads
    - [ ] B) Faster execution of user applications
    - [ ] C) Better memory management
    - [ ] D) Improved CPU speed

---

### Answers

1. B) -lpthread
2. B) Child thread PID
3. A) pthread_create
4. B) The PID of the main thread
5. C) ps
6. C) Kernel thread performance
7. B) Another ready thread should be executed.
8. B) Upcall
9. B) By allowing the process to request and return them
10. B) The thread is restored to its previous state.
11. B) The thread remains blocked while the system handles it.
12. B) To create an infinite execution
13. D) fonction
14. B) Decreased responsiveness
15. A) Reduced context switches between threads
