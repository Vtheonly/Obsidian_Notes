
![[P - 1.png]]

### Central Unit (CPU)
- **Composition**: The central unit is composed of the microprocessor (CPU).
- **Functioning**:
  - Interprets and executes instructions from programs.
  - Reads from and saves results to memory.
  - Communicates with input/output (I/O) units.
- **Characteristics**:
  - **Clock Frequency**: Measured in MHz (megahertz) or GHz (gigahertz), determining the speed of instruction execution.
  - **Instructions Per Second**: Indicates the number of instructions that the CPU can execute in a second.
  - **Data Size**: Specifies the size of the data the CPU can process, often measured in bits (e.g., 32-bit, 64-bit).

### Main Memory
This memory holds the instructions of the currently running program(s) and the associated data.

- **ROM (Read-Only Memory)**: Memory that can only be read and not written to. It stores data permanently.
- **RAM (Random Access Memory)**: Temporary memory that stores data while the system is powered on. The contents are lost when the power is turned off.

### Input/Output Interfaces
- These interfaces allow communication between the microprocessor and peripheral devices, such as the keyboard, monitor, and sensors.
- **Communication Protocols**:
  - **Serial**: Sends information bit by bit, one after the other.
  - **Parallel**: Sends bits of data simultaneously (in parallel).
  
### Explanation of Components in the Diagram:

1. **ROM (Read-Only Memory)**: Stores firmware or permanent software that the system needs to operate.
2. **RAM (Random Access Memory)**: Holds data for active programs, providing quick access to the CPU.
3. **DMA (Direct Memory Access)**: A controller that allows peripherals to access memory without involving the CPU, enhancing data transfer efficiency.
4. **Interrupt Handler**: A system that handles the signals (interrupts) sent by hardware or software indicating that a task requires immediate attention.
5. **CoP (Coprocessor)**: Assists the CPU in performing specific tasks more efficiently (e.g., mathematical calculations).
6. **CPU (Central Processing Unit)**: The primary component responsible for interpreting and executing instructions.
7. **Cache**: A smaller, faster type of volatile memory that stores copies of frequently accessed data for quicker CPU access.
8. **MMU (Memory Management Unit)**: Translates logical addresses into physical addresses in the memory, handling memory protection and virtual memory.
9. **Hardware Accelerator**: Specialized hardware designed to perform certain tasks faster than the CPU (e.g., graphics processing).
10. **Graphic Board**: Manages the rendering of images and video output to the screen.
11. **UART (Universal Asynchronous Receiver-Transmitter)**: Handles asynchronous serial communication with peripherals such as a mouse or modem.
12. **PIO (Parallel Input/Output)**: Manages parallel communication with devices like printers.
13. **USB (Universal Serial Bus)**: Allows connection and data transfer with devices such as scanners.
14. **Buses**: Communication pathways that transfer data between different components in the system.
15. **Bridges**: Components that connect two buses, allowing communication between different parts of the system.

---

This overview connects the components in the diagram to their respective functions, illustrating how a computer system is organized to handle instructions, process data, and communicate with external devices.