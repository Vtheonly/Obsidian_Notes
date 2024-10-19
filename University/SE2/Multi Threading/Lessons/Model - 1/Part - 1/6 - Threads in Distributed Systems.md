### Threads in Distributed Systems

Threads are widely used in distributed systems, such as in servers where threads remain blocked while waiting for a request to be processed. An alternative approach can be considered, where a new thread is created only when a request arrives. This is called a **pop-up thread**. Since this is a new thread, it doesn't have any history (registers, stack, etc.) to restore, and the threads are created very quickly. The latency between the arrival of the message and the start of processing is very short.

![[Pasted image 20241016224807.png]]

### Planning for Pop-up Threads

To implement pop-up threads, planning is required to determine where the new thread will be created (user/kernel space). It is faster and easier to create the thread in the kernel, as it can easily access the kernel tables and I/O devices. However, this solution, while fast, can be risky because a bug in a kernel thread can cause far more problems than one in a user thread.

---
