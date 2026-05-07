# Chapter 9: System Reliability and Checkpointing

## 1. Atomic Checkpoint Writes and POSIX Constraints

**The Corruption Race Condition:**
Standard PyTorch uses `torch.save()`, which serializes the model to disk using multiple internal `write()` calls. If a background process (like a HuggingFace upload thread) attempts to read the file before `torch.save()` has finished, it reads a truncated, corrupted file. If the Kaggle kernel times out mid-write, your checkpoint is permanently destroyed.

**The Atomic POSIX Solution:**
In `checkpoint.py`, you implemented a system guaranteed by the POSIX operating system standard to never corrupt:
1.  **Write to Temp:** `torch.save()` writes the entire 1GB model to `epoch_15.pt.tmp`.
2.  **Kernel Flush:** You explicitly open the `.tmp` file and call `os.fsync()`. This forces the operating system to flush all dirty write-back buffers from RAM into the physical storage hardware.
3.  **Atomic Rename:** You call `os.replace(tmp_path, final_path)`. At the OS file-system level, a rename is an atomic pointer swap. Any process reading the file will either see the complete old file or the complete new file. A partial read is mathematically impossible.

## 2. The Hardware Flight Recorder and Shared Memory Exhaustion

Kaggle kernels often die with a silent "Kernel Restarting" message, providing no Python traceback. To diagnose this, you built a background daemon thread (`hardware_flight_recorder`).

**What it does:**
Every 1.0 seconds, the thread writes the exact state of system RAM, GPU VRAM, and Docker Shared Memory to a CSV file. It bypasses Python's internal file buffering by using `os.fsync()`, ensuring the last line is written to disk even if the machine hard-crashes a millisecond later.

**The `/dev/shm` (Shared Memory) Trap:**
The flight recorder specifically monitors `/dev/shm`. PyTorch Dataloaders use shared memory to pass the augmented image tensors from the CPU worker processes to the main GPU thread. Docker containers (which Kaggle uses) often have a hard limit on `/dev/shm` size (e.g., 8GB). If `prefetch_factor` is too high, the workers fill the shared memory, the OS triggers an Out-Of-Memory kill signal (SIGKILL), and the Python script dies instantly without warning. Monitoring `/dev/shm` allows you to scientifically tune the `num_workers` and `prefetch_factor` to stay just below the crash limit.