### Registres (Registers)
[[Test - 4 - Registers]]
The term "register" refers to the fastest and most immediately accessible memory type in a computer system, used primarily for temporary data storage during processing. Registers are crucial for the operation of the CPU (Central Processing Unit), holding both the instructions and the operands required for computations, as well as the results.

#### Key Characteristics:
- **Type**: Registers are usually built with **SRAM** (Static Random-Access Memory), which does not require refreshing, making it faster than DRAM (Dynamic RAM).
- **Construction**: Registers are constructed using flip-flops, typically made with a set of 4 transistors (2 NOR gates).
- **Integration**: They are integrated directly into the CPU and sometimes in other components for direct access.
- **Storage**: Registers store either instructions or data related to those instructions, such as operands and computation results.
- **Number**: There are typically fewer than 40 registers in a modern CPU, given their role and high cost.
- **Speed**: Registers are incredibly fast, operating at the clock speed of the CPU itself, ensuring low latency for critical operations.

### Types of Access

Registers, like other memory components, have specific ways they handle data access:

- **Sequential Access**: Typically not used for registers. This type of access requires traversing each piece of data in sequence to retrieve the desired information, common in magnetic tapes.
  
- **Direct Access**: Registers allow direct access, meaning each register has a unique address, and any specific register can be accessed instantly without needing to search through other data. This is common in the **central memory** of computers.

- **Associative Access**: Registers also support **associative access**, meaning data can be retrieved by matching the content rather than using explicit addresses. This type of access is commonly associated with **cache memory**, where a key identifies the needed data.

### Bank of Registers (Banc de Registres)


![[P - 2.png| Bank of Registers]]

A **bank of registers** refers to a group of registers used together for more efficient data handling. This bank is structured in a way that allows multiple simultaneous reads and writes, which can accelerate processing by the CPU.

#### Structure:
- **N Registers, K Bits**: A register bank consists of **N registers**, each storing **K bits** of data. For instance, a 3-bit register bank might include several individual registers, each able to store a 3-bit word.
- **Writing Port**: A single writing port enables data to be stored in a chosen register.
- **Two Reading Ports**: The bank has two reading ports, allowing the contents of two registers to be read simultaneously. This feature speeds up operations that require multiple operands.

#### Example:
- **N Registers, 3 Bits**: If the register bank has **N registers**, each holding **3 bits** of data, the system might involve:
  - One **writing port** for inputting data.
  - Two **reading ports** for retrieving the contents of two registers at the same time, typically used in operations involving two operands, such as additions in arithmetic logic units (ALUs).

### Usage of Register Banks in Computing

The role of register banks is critical in speeding up data access and arithmetic operations:

- **Reading Mechanism**: A **multiplexer** selects which register to read based on the address input, and the data is output to a **data line** for use in further operations.
  
- **Writing Mechanism**: A **decoder** determines which register to write to, and the data is written to the selected register based on the decoded address.

### Arithmetic Operations Using Registers

In arithmetic operations, the **ALU** (Arithmetic Logic Unit) takes data from two registers (for example, A and B) and performs the necessary computation (like addition: A + B). The result is stored back in the register bank or sent directly to other CPU components for further processing.

---
