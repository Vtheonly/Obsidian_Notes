

In operating systems, processes not only compete for resources but can also cooperate to achieve common tasks. This cooperation requires interprocess communication (IPC). To enable such communication, synchronization tools are used to coordinate processes.

There are two main methods of IPC:

1. **Shared Memory:** Processes communicate by sharing a variable through a common memory zone (shared memory segments). The synchronization responsibility falls on the user.
2. **Message Passing:** The operating system manages the exchange of messages through message queues using the primitives `send(message)` and `receive(message)`.

#### 1. Communication through Shared Variables

In shared memory communication, each process can read or write to the shared zone. Multiple processes might access the zone concurrently, so synchronization tools are necessary to prevent conflicts.

##### 1.1 Producer-Consumer Model

In the producer-consumer model, producer processes generate information that is consumed by consumer processes. The concurrent execution of producers and consumers relies on a set of intermediate buffers filled by producers and emptied by consumers. Both producers and consumers compete to perform their tasks.

Examples:
1. The keyboard process produces characters that are consumed by the screen display process.
2. The printer driver produces lines of characters that are consumed by the printer.
3. A compiler produces lines of code consumed by the assembler.

There are two variations of the producer-consumer problem:
- **Unbounded Buffer:** If the buffer is unbounded, only the consumer must wait when the buffer is empty.
- **Bounded Buffer:** If the buffer is bounded, both the producer must wait when the buffer is full, and the consumer waits when the buffer is empty.

###### Case: Bounded Buffer of Size n
In this scenario, communication happens through a buffer with `n` slots. The objects or items are consumed in the order they were produced (FIFO – First In, First Out).

Two primitives are used:
1. `Deposit(item)` – Adds an item to the buffer.
2. `Retrieve(item)` – Removes an item from the buffer.

Synchronization conditions:
- The producer can only deposit if there is at least one empty slot.
- The consumer can only retrieve if there is at least one filled slot.
- Each item should only be retrieved once.
- Mutual exclusion (E.M.) must be enforced at the buffer slots level to prevent concurrent access.

###### a. Single Producer – Single Consumer

The buffer synchronization can be handled using semaphores:
- `nbplein := 0`: Semaphore that blocks the consumer when the buffer is empty.
- `nbvide := n`: Semaphore that counts the number of empty slots.

**Producer Process:**
```pseudocode
Repeat
  P(nbvide); 
  Deposit(item); 
  V(nbplein); 
Until false
```

**Consumer Process:**
```pseudocode
Repeat
  P(nbplein); 
  Retrieve(item); 
  V(nbvide); 
Until false
```

The producer and consumer never operate on the same buffer slot at the same time. The buffer is managed circularly using two pointers:
- `t`: Points to the first filled slot (consumer’s pointer).
- `q`: Points to the first empty slot (producer’s pointer).

###### b. Multiple Producers – Multiple Consumers

In this case, access to the buffer must be ensured through mutual exclusion within each process family. Both `Deposit(item)` and `Retrieve(item)` operations must be performed under mutual exclusion.

Additional semaphores are introduced:
- `mutex_p` and `mutex_c`: Both initialized to 1, they ensure that producers and consumers access the buffer in mutual exclusion.

**Producer Process:**
```pseudocode
Repeat
  P(nbvide); 
  P(mutex_p); 
  Deposit(item); 
  V(mutex_p); 
  V(nbplein); 
Until false
```

**Consumer Process:**
```pseudocode
Repeat
  P(nbplein); 
  P(mutex_c); 
  Retrieve(item); 
  V(mutex_c); 
  V(nbvide); 
Until false
```

The buffer operations `Deposit(item)` and `Retrieve(item)` are performed circularly:
- **Deposit:** `T[q] := item; q := (q + 1) mod n;`
- **Retrieve:** `item := T[t]; t := (t + 1) mod n;`

##### 1.2 Reader-Writer Model

This model is a specific case where the shared object is accessible by two types of operations: reads and writes. The object can be a file, database record, or even an entire file system. Common use cases include:
- **Bank account management:** Where account records are both read and updated.
- **Airline reservation systems:** Where booking records are accessed and modified.

In this model, two scenarios can arise:
###### a. No Explicit Priority

In the no-priority scenario, both readers and writers share access to a resource, such as a file or database. The file is considered a critical resource for writers, meaning when a writer is active, neither other writers nor readers can access the file.

**Semaphores:**
- `mutex`: Ensures exclusive access to the shared reader counter.
- `w`: Controls access to the critical resource (e.g., the file).

**Reader Process:**
```pseudocode
Repeat
  P(mutex); 
  nl := nl + 1; 
  If nl == 1 Then P(w); EndIf 
  V(mutex); 
  <reading>; 
  P(mutex); 
  nl := nl - 1; 
  If nl == 0 Then V(w); EndIf 
  V(mutex); 
Until false
```

**Writer Process:**
```pseudocode
Repeat
  P(w); 
  <writing>; 
  V(w); 
Until false
```

##### Comments:
1. The file is a critical resource for writers. When a writer is writing, no other process can access it.
2. Multiple readers can read simultaneously.
3. Only the first reader checks if a writer is active. If they succeed, subsequent readers access directly.

###### b. Reader Priority

In the reader-priority scenario, the system is biased toward granting readers access over writers. This is done by introducing an additional semaphore `mutex2` to prevent writers from waiting indefinitely while readers continue to access the resource.

**Reader Process:**
```pseudocode
Repeat
  P(mutex); 
  nl := nl + 1; 
  If nl == 1 Then P(w); EndIf 
  V(mutex); 
  <reading>; 
  P(mutex); 
  nl := nl - 1; 
  If nl == 0 Then V(w); EndIf 
  V(mutex); 
Until false
```

**Writer Process:**
```pseudocode
Repeat
  P(mutex2); 
  P(w); 
  <writing>; 
  V(w); 
  V(mutex2); 
Until false
```

In this case, `mutex2` ensures that writers don't get stuck waiting, giving preference to the readers.

---

By combining these classical synchronization models, we can manage resource access, process coordination, and ensure both efficiency and correctness in multi-process environments.