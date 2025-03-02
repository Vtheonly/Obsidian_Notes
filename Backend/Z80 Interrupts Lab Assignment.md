Below is a complete and self-contained response to the EE424 Advanced ICs Pre-Lab Assignment query, addressing each part based on the provided information. The response uses markdown for clarity and focuses on the user's requirements without relying on external context beyond the query itself.

---

Pre-Lab Assignment Responses

1. Review Z80 Subroutine Programs

Z80 subroutine programs are blocks of code designed for reusability, similar to functions in high-level languages. They rely on key instructions:

- CALL address: Transfers control to the subroutine at the specified address, pushing the 16-bit return address (the next instruction after CALL) onto the stack. The stack pointer (SP) decreases by 2 bytes.
    
- RET: Pops the 16-bit return address from the stack into the program counter (PC), returning control to the caller. SP increases by 2 bytes.
    

The stack, managed by SP, operates in a last-in, first-out (LIFO) manner. Proper balancing of stack operations (e.g., PUSH and POP) is essential to prevent overflow or underflow, ensuring reliable subroutine execution.

---

1. Review Z80 Interrupts

Interrupts enable the Z80 to respond to events without continuous polling. The Z80 supports three interrupt modes:

- Mode 0: The interrupting device places an instruction (e.g., RST or CALL) on the data bus, which the Z80 executes. Commonly used with predefined restart vectors.
    
- Mode 1: Upon an interrupt, the Z80 jumps to address 0038H, ignoring the data bus. Ideal for simple, fixed ISR locations.
    
- Mode 2: The interrupting device provides an 8-bit vector. This vector (low byte) combines with the I register (high byte) to form a 16-bit address in a vector table, pointing to the ISR. Suitable for multiple interrupt sources.
    

Interrupts are enabled with the EI instruction and disabled with DI. The mode is selected using IM 0, IM 1, or IM 2. Hardware interrupts are triggered via the /INT pin, while software interrupts use instructions like RST.

---

1. Write a Subroutine to Read Keypad and Display [2200H] on LCD

Task: Write a subroutine that:

- Calls the read keypad subroutine at 03F1H, which waits for a key press and stores the key value in 3FFCH.
    
- Displays the content of memory location 2200H on the LCD.
    

Assumption: Since the LCD display method isn’t specified, assume writing to a memory-mapped address (e.g., 3FFDH) outputs to the LCD, a common approach in Z80 systems.

Code:

assembly

```text
READ_DISPLAY:
    CALL 03F1H       ; Call keypad subroutine (waits for key press, stores key in 3FFCH)
    LD HL, 2200H     ; Load address 2200H into HL
    LD A, (HL)       ; Load value at 2200H into A
    LD (3FFDH), A    ; Output value to LCD (assuming 3FFDH is LCD data register)
    RET              ; Return to caller
```

Explanation:

- CALL 03F1H: Waits for a key press, storing the key value in 3FFCH. The key value isn’t used here; it simply triggers the display action.
    
- LD HL, 2200H: Sets HL to point to 2200H.
    
- LD A, (HL): Loads the 8-bit value at 2200H into A.
    
- LD (3FFDH), A: Writes A to 3FFDH, assumed to be the LCD’s data register.
    
- RET: Returns control to the calling program.
    

In a real system, LCD display might require additional steps (e.g., initialization, command/data mode switching), but this meets the pre-lab’s simplified requirements.

---

1. Address of Instruction Executed After Subroutines

Determine the next instruction executed after:

a) Subroutine 1

assembly

```text
PUSH HL
LD HL, (3FF0)
EX (SP), HL
RET
```

Analysis:

1. CALL Sub1: Assume called from address X. The return address (X + 3, as CALL is 3 bytes) is pushed onto the stack.
    
2. PUSH HL: Pushes HL’s current value onto the stack (SP -= 2).
    
3. LD HL, (3FF0): Loads HL with the 16-bit value from 3FF0H (low byte) and 3FF1H (high byte).
    
4. EX (SP), HL: Swaps HL with the stack’s top two bytes (original HL). The stack’s top now holds the value from 3FF0H.
    
5. RET: Pops the stack’s top (the value from 3FF0H) into PC.
    

Result: Execution jumps to the address stored at 3FF0H (16-bit value [3FF1H][3FF0H], little-endian).

Answer: The address stored at 3FF0H.

b) Subroutine 2

assembly

```text
LD B, 00H
DJNZ FE
JP 00B4H
```

Analysis:

1. LD B, 00H: Sets B to 0.
    
2. DJNZ FE: Decrements B to 255 (FFH, as 0 - 1 = 255 in 8-bit). Since B ≠ 0, it jumps by offset FEh (-2, signed) relative to the next instruction’s address. DJNZ is 2 bytes, so the jump loops back to itself, repeating 255 times until B = 1, then B = 0, and proceeds to the next instruction.
    
3. JP 00B4H: Unconditionally jumps to 00B4H.
    

Note: As a subroutine, it should end with RET, but the provided code uses JP, redirecting control instead of returning.

Result: Execution jumps to 00B4H.

Answer: 00B4H.

---

1. Design the Circuit and Write the Code for Task 2

Assumption: Task 2 involves a hardware interrupt in Mode 1, based on the lab’s focus on interrupt modes and simplicity for initial tasks.

Circuit

- Components:
    
    - Push-button or interrupt source connected to the Z80’s /INT pin.
        
    - 10kΩ pull-up resistor from /INT to +5V to keep it high normally.
        
    - Button grounds /INT when pressed, triggering a low signal.
        
- Operation: A high-to-low transition on /INT triggers the interrupt (if enabled).
    

Code

assembly

```text
        ORG 0000H
        IM 1          ; Set interrupt mode 1
        EI            ; Enable interrupts
MAIN:   JP MAIN       ; Infinite loop to keep CPU active

        ORG 0038H     ; ISR address for Mode 1
ISR:
        PUSH AF       ; Save registers
        CALL READ_DISPLAY ; Display [2200H] on LCD
        POP AF        ; Restore registers
        EI            ; Re-enable interrupts
        RETI          ; Return from interrupt
```

Explanation:

- IM 1: Sets Mode 1, where interrupts jump to 0038H.
    
- EI: Enables interrupt handling.
    
- MAIN: Keeps the CPU running.
    
- ISR: At 0038H, saves AF, calls the subroutine from Q3 to display [2200H], restores AF, re-enables interrupts, and uses RETI to acknowledge the interrupt and return.
    

---

1. Design the Circuit and Write the Code for Task 3

Assumption: Task 3 uses Mode 2 for a more complex interrupt setup with a vector table.

Circuit

- Components:
    
    - Interrupt source (e.g., a peripheral) connected to /INT.
        
    - Pull-up resistor (10kΩ) to +5V on /INT.
        
    - Peripheral places an 8-bit vector (e.g., 00H) on the data bus during the interrupt acknowledge cycle.
        
- Operation: The vector combines with the I register to address the ISR.
    

Code

assembly

```text
        ORG 0000H
        LD A, 20H     ; Set I register to 20H
        LD I, A
        IM 2          ; Set interrupt mode 2
        EI            ; Enable interrupts
MAIN:   JP MAIN       ; Infinite loop

        ORG 2000H     ; Vector table at 2000H (I=20H, vector=00H)
        DW ISR_ADDR   ; ISR address in table

ISR_ADDR:
        PUSH AF       ; Save registers
        CALL READ_DISPLAY ; Display [2200H] on LCD
        POP AF
        EI            ; Re-enable interrupts
        RETI          ; Return from interrupt
```

Explanation:

- LD I, A: Sets I to 20H, defining the vector table’s high byte.
    
- IM 2: Sets Mode 2, using I and the device’s vector.
    
- EI: Enables interrupts.
    
- Vector Table: At 2000H (I=20H, vector=00H), stores the ISR address.
    
- ISR: Saves AF, calls the Q3 subroutine, restores AF, re-enables interrupts, and uses RETI.
    

---

Summary

- 3: Subroutine waits for a key press and displays [2200H] on the LCD (via 3FFDH).
    
- 4:
    
    - a) Address at 3FF0H.
        
    - b) 00B4H.
        
- 5: Mode 1 interrupt with a button circuit, ISR at 0038H.
    
- 6: Mode 2 interrupt with a vector table at 2000H.
    

This response fully addresses the pre-lab, using reasonable assumptions where details are unspecified. Adjust hardware addresses or LCD specifics based on your system.