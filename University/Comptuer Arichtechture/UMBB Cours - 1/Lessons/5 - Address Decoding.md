### Address Decoding
As the number of peripherals connected to the microprocessor increases, a method to manage access to each device becomes necessary. This is where address decoding comes into play:

[[Test - 5 - Address Decoding]]
- **Device Address Assignment**: Each peripheral is assigned a specific address range in the system's memory.
- **Conflict Avoidance**: To avoid conflicts, only one device can be selected at a time to communicate with the microprocessor.
- **Address Decoder**: This component directs data to the correct peripheral by decoding the addresses sent over the data bus, ensuring that each device gets the correct instructions or data.