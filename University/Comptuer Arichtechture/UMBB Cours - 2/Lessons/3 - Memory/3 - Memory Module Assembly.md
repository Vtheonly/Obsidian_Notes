### Memory Module Assembly
Due to **technological integration limits**, individual memory chips have restricted sizes. To overcome these limitations and achieve larger memory sizes, **multiple memory chips (memory modules)** are grouped together. This assembly approach allows two primary enhancements:
- **Increase in word size**: Combining multiple memory modules to create wider memory words.
- **Increase in the number of words**: Combining memory modules to increase the total number of words in the memory.
[[Test - 3 - Memory Module Assembly]] 
#### Increasing Word Size
When you want to increase the **size of each word** stored in memory, you can assemble multiple memory modules side by side. For instance:
- If you have two memory modules, each with **2ᴷ words** of **N bits**, you can combine them into a block of **2ᴷ words**, each having **2 * N bits**.
  
  This effectively **doubles the word size** while maintaining the same number of words.

#### Increasing the Number of Words
To increase the **total number of words** in memory, you can stack additional memory modules. For example:
- If you have **4 memory modules**, each with **2ᴷ words** of **N bits**, you can combine them into a block of **4 * 2ᴷ words**, each still consisting of **N bits**.
  
  This multiplies the **total number of words** by the number of modules without changing the word size.

#### Addressing the Expanded Memory
When memory blocks are assembled, the system requires additional address bits to handle the larger memory space. For example, in the case of four memory modules, you would need an extra **2 bits** to address the additional memory blocks. If the original memory address used **K bits**, the new memory block would need **K + 2 bits** for addressing.

---

In summary, **assembling memory modules** allows you to either:
1. **Increase word size** (by combining memory in parallel), or
2. **Increase the number of words** (by adding more modules in series). 

Each method requires handling the memory's addressing scheme to accommodate the expanded memory space.