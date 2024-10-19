
### Sequential Circuit Examples
[[Test - 2 - Clock Sync]]
Sequential circuits are a class of digital logic circuits that not only depend on the current inputs but also on the history of those inputs. They maintain a "memory" of previous states, and can be categorized based on their operation mode: **asynchronous** and **synchronous**. Below are two examples of such circuits:

---

### **Asynchronous Sequential Circuit Example: D Flip-Flop (Bascule D)**

In an **asynchronous** system, outputs can change immediately when inputs change, without waiting for a clock signal. Here's how a **D flip-flop** (or D latch) works asynchronously.

#### Components:
- **D** = Data input
- **W** = Write signal
- **Q** = Output

#### Functionality:
- When **W = 1**, the output **Q** is updated with the value of **D**, and this value is **stored (memorized)**. The flip-flop writes the data from the input to the output immediately.
- When **W = 0**, the flip-flop remains in the **same state**, meaning the output **Q** keeps its last value. No change occurs, and the last written data is held.

#### Example Use Case:
An asynchronous D flip-flop might be used in a simple memory storage element, where data is written immediately when triggered (W = 1), and stays stable when not triggered (W = 0).

---

### **Synchronous Sequential Circuit Example: D Flip-Flop (Bascule D) with Clock**

In a **synchronous** system, the state of the circuit changes based on a **clock signal**. A clock signal synchronizes the timing of changes in the output. The D flip-flop also exists in a **synchronous** variant.

#### Components:
- **D** = Data input
- **H** = Clock signal (Horloge in French)
- **Q** = Output

#### Functionality:
- When the **clock signal (H)** triggers (usually at a rising or falling edge of the clock pulse), the output **Q** is updated with the value of **D**. This means that changes in **D** are only reflected in **Q** at specific times, determined by the clock.
- Between clock signals, the value of **Q** remains constant, no matter how the input **D** changes.

#### Example Use Case:
Synchronous D flip-flops are used in most digital systems, such as **registers** or **memory cells**, where data is updated only at specific intervals determined by a global clock, ensuring stable and predictable operation.

---

### **Comparison between Asynchronous and Synchronous D Flip-Flops**

| Feature                           | Asynchronous D Flip-Flop         | Synchronous D Flip-Flop            |
|------------------------------------|----------------------------------|------------------------------------|
| **Control Signal**                 | Write signal (**W**)             | Clock signal (**H**)               |
| **Data Update**                    | Immediate, when W = 1            | Only at clock pulse (H)            |
| **Output State (Q)**               | Can change any time inputs change | Changes only at clock intervals    |
| **Timing Control**                 | No global timing, reacts instantly | Tightly controlled by clock signal |
| **Typical Usage**                  | Simple memory/storage element    | Registers, memory cells, counters  |

---

In summary, the **asynchronous D flip-flop** responds instantly to changes when **W = 1**, while the **synchronous D flip-flop** waits for the clock signal to update its output, ensuring predictable and timed updates in digital circuits.