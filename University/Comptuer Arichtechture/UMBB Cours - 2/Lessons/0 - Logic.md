### Combinational Logic and Sequential Logic

---
[[Test - 0 - Logic]]
#### 1. Combinational Logic

**Definition**:  
Combinational logic circuits are those in which the output is purely determined by the current input. The circuit does not have any memory or past state information—it only depends on the current combination of input signals. These circuits are stateless.

**Key Characteristics**:  
- Outputs depend solely on the present inputs.
- No feedback paths are involved.
- No memory elements, such as flip-flops or latches, are used.
- Can be represented with logic gates (AND, OR, NOT, etc.).
- Propagation time: Outputs change almost immediately after inputs change, but there is a small delay due to gate propagation.

**Examples of Combinational Logic Circuits**:
- **Multiplexer (MUX)**:  
   A multiplexer is a circuit that selects one input from multiple inputs and directs it to a single output, depending on control inputs. For example, an 8-to-1 multiplexer takes 8 inputs but only sends one of them to the output based on 3 control bits.  
   *Use case*: Data selection from different sources.
  
- **Decoder**:  
   A decoder is a circuit that activates exactly one output line out of many possible outputs based on the binary value provided at its input. A 3-to-8 decoder, for instance, has 3 input lines and 8 output lines, and it will activate only one of the output lines depending on the binary value of the inputs.  
   *Use case*: Address decoding in memory selection.

**Important Point**:  
For proper functioning, it is crucial to wait until the signals are stable to ensure accurate results, as there is always a small delay between input changes and output propagation.

---

#### 2. Sequential Logic

**Definition**:  
Unlike combinational logic, sequential logic circuits have memory and can store past states. The output depends not only on the current input but also on the history of inputs (i.e., the previous states).

**Key Characteristics**:  
- Outputs depend on both current inputs and past states.
- Includes feedback paths, where outputs are fed back to inputs.
- Utilizes memory elements like flip-flops and latches.
- Has a clock signal in synchronous circuits to synchronize changes. [[1 - Synchronous and Asynchronous| more ]]
**Examples of Sequential Logic Circuits**:
- **Flip-Flop**:  
   A basic building block of sequential logic, used to store a single bit of data. Flip-flops change their state on clock edges (rising or falling edge).
  
- **Counter**:  
   A circuit that goes through a predefined sequence of states based on a clock signal. It can count in binary (up or down) based on its design.

---

#### 3. Truth Table for Combinational Logic Circuits

Let’s look at two example truth tables: one for a simple **AND gate** (combinational logic) and one for a **Multiplexer (MUX)**.

##### AND Gate (Two inputs: A, B)

| A | B | Output (A AND B) |
|---|---|------------------|
| 0 | 0 | 0                |
| 0 | 1 | 0                |
| 1 | 0 | 0                |
| 1 | 1 | 1                |

In an AND gate, the output is only `1` if both inputs (A and B) are `1`, otherwise it is `0`.

##### 2-to-1 Multiplexer (MUX)

- **Inputs**:  
  S = Select line  
  I0, I1 = Input lines

| S | I0 | I1 | Output |
|---|----|----|--------|
| 0 | 0  | 0  | 0      |
| 0 | 1  | 0  | 1      |
| 1 | 0  | 0  | 0      |
| 1 | 0  | 1  | 1      |

In this case, when the select line `S` is `0`, the output follows `I0`. When `S` is `1`, the output follows `I1`.

---

### Conclusion

Combinational logic circuits play a vital role in digital systems, providing fast and simple responses based on input without memory, while sequential circuits add complexity by considering past inputs (history) and using memory elements. Both are foundational in building more complex systems like processors, memory units, and control circuits.

--- 

Let me know if you'd like me to expand on any specific section or add more circuits!