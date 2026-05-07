import os

base_dir = "/home/mersel/Documents/Learn/Obsidian Notes/Shared/AI/Tamer/"

# Files to ensure writing to
files = [
    ("Meta/AI_Transition_2.md", """Here is the next expansion of your Obsidian vault. This iteration focuses strictly on the new material found in the codebase that has not been covered yet: the data engineering pipeline, the algorithmic complexity scoring, the micro-mechanics of gradient accumulation, and the critical systems-level programming required to survive the Kaggle environment (atomic writes, NFS bottlenecks, and OOM diagnostics)."""),
    
    ("Outlines/Outline_Part3.md", """```text
Course {
    Chapter 2: Computer Vision and The Encoder
        - 8. Albumentations and Math Safe Augmentations

    Chapter 4: Text Processing and Tokenization
        - 3. Algorithmic Complexity Scoring for Math Equations

    Chapter 5: Advanced Training Strategies and Loss Functions
        - 10. Gradient Accumulation and Gradient Clipping Mechanics

    Chapter 8: Data Engineering and Distributed Systems
        - 1. Robust Dataset Acquisition and Streaming
        - 2. Bypassing the Kaggle NFS Bottleneck with O(1) Indexing
        - 3. Eliminating Dataloader Bottlenecks

    Chapter 9: System Reliability and Checkpointing
        - 1. Atomic Checkpoint Writes and POSIX Constraints
        - 2. The Hardware Flight Recorder and Shared Memory Exhaustion
}
```"""),

    ("Chapter 2 - Computer Vision/Part_3.md", """# Chapter 2: Computer Vision and The Encoder

## 8. Albumentations and Math Safe Augmentations

**The Danger of Standard Augmentation:**
In standard computer vision (like identifying dogs vs. cats), flipping an image horizontally or rotating it 90 degrees is perfectly safe—a dog upside down is still a dog. 
In Mathematical OCR, the spatial orientation defines the semantic meaning. 
*   If you flip a `p` horizontally, it becomes a `q`. 
*   If you rotate a `+` by 45 degrees, it becomes a `\times`.
*   If you flip a `\leq` vertically, it becomes `\geq`.

**Math-Safe Pipeline:**
In `augmentation.py`, the training transformations are strictly bounded to prevent the destruction of mathematical logic:
1.  **ShiftScaleRotate (Subtle Geometry):** Rotation is strictly capped at ±3 degrees. Translation (shifting) is capped at ±2%, and scaling at ±5%. This simulates a slightly crooked scan or uneven handwriting without breaking the structural integrity of the equation.
2.  **Gaussian and Median Blur:** Randomly applied to simulate out-of-focus camera shots or low-DPI flatbed scans.
3.  **GaussNoise:** Simulates the digital sensor noise common in low-light smartphone photos of homework.
4.  **CoarseDropout (The Ink-Eraser):** As previously mentioned, we drop out small rectangular chunks. By setting `max_holes=4` and capping the height/width of the holes, we simulate faded ink, chalk gaps on a blackboard, or dry erase marker skipping.

```mermaid
graph TD
    Input[Raw Image] --> Safe[Math-Safe Operations]
    Safe --> Blur[Blur: Simulates low-res scan]
    Safe --> Noise[Noise: Simulates bad sensor]
    Safe --> Drop[Dropout: Simulates faded ink]
    Safe --> Affine[Affine: Max 3 degree tilt]
    
    Input --> Unsafe[Banned Operations]
    Unsafe --> Flip[Horizontal Flip: d becomes b]
    Unsafe --> Rot[90 Deg Rotation: + becomes x]
```"""),

    ("Chapter 4 - Text Processing/Part_2.md", """# Chapter 4: Text Processing and Tokenization

## 3. Algorithmic Complexity Scoring for Math Equations

We previously established that the trainer uses Curriculum Learning (Simple $\\rightarrow$ Medium $\\rightarrow$ Complex). But how does the system objectively know if a mathematical equation is "simple" or "complex" before it even looks at the image?

In `latex_normalizer.py`, you wrote a highly specific heuristic scoring algorithm: `get_complexity(latex)`.

**1. Immediate Complex Triggers:**
If the LaTeX string contains elements that break standard 1D left-to-right reading, it bypasses the scoring and is instantly flagged as `complex`. These include matrices (`\\begin{matrix}`), multiline alignments (`\\begin{aligned}`), row separators (`\\\\`), and column separators (`&`).

**2. The Point System:**
If there are no immediate triggers, the algorithm calculates a float score:
*   **Length Penalty:** `+1 point` for every 25 characters. Long sequences stress the Transformer's attention matrix.
*   **Spatial Shifts (Up/Down):** `+1 point` for every superscript (`^`) or subscript (`_`). These require the model to learn localized vertical relationships.
*   **Heavy Vertical Structures:** `+2 points` for symbols that drastically alter the 2D bounding box of the equation, such as `\\frac`, `\\sqrt`, `\\int`, `\\sum`, `\\prod`.
*   **Grouping Depth:** `+0.5 points` for every opening brace `{`. Deeply nested braces (e.g., `\\frac{1}{x^{2}}`) require the decoder to track long-range bracket-matching syntax.

**3. Classification Thresholds:**
*   **Score < 4.0 (`simple`):** Basic algebra, e.g., $x^2 + y = 3$. Used in Epochs 1-10.
*   **Score 4.0 to 12.0 (`medium`):** Standard college math with multiple fractions or integrals.
*   **Score > 12.0 (`complex`):** Heavily nested, nightmare equations."""),

    ("Chapter 5 - Advanced Training Strategies/Part_3.md", """# Chapter 5: Advanced Training Strategies and Loss Functions

## 10. Gradient Accumulation and Gradient Clipping Mechanics

**The VRAM Wall:**
To achieve a stable gradient that accurately represents the dataset distribution, you need a large batch size. However, passing a batch of 192 high-resolution (384x1280) images through an 88-million parameter SwinV2 encoder and a 10-layer decoder requires far more than the 96GB of VRAM available on an RTX 6000 Ada.

**The Solution: Gradient Accumulation**
In `engine.py`, you implemented a `train_step` with `accumulation_steps = 6`, running a physical batch size of 36.
1.  **Forward Pass 1:** Pass 36 images. Compute the loss.
2.  **Divide the Loss:** `loss = loss / 6`. This is mathematically critical. Without division, the gradients would sum up and act like a learning rate multiplier of 6x, blowing up the training.
3.  **Backward Pass 1:** Compute gradients and *accumulate* (add) them into the `.grad` attributes of the weights.
4.  **Repeat 6 times.**
5.  **Optimizer Step:** Only after 6 iterations (effectively $36 \\times 6 = 216$ images) do you call `optimizer.step()` to update the weights, followed by `optimizer.zero_grad()` to clear the cache.

**Gradient Clipping (`max_grad_norm = 1.0`):**
In deep networks (especially Transformers), the error surface can have steep "cliffs". If a batch contains highly unusual images, the computed gradient might be massive. If the optimizer takes a massive step, it destroys the model weights (a NaN explosion). 
Before taking a step, `torch.nn.utils.clip_grad_norm_` calculates the global L2 norm of all gradients. If the norm exceeds `1.0`, it scales the entire gradient vector down. The direction of the learning step remains exactly the same, but the magnitude is safely capped."""),

    ("Chapter 8 - Data Engineering/Part_1.md", """# Chapter 8: Data Engineering and Distributed Systems

## 1. Robust Dataset Acquisition and Streaming

Training requires hundreds of gigabytes of data. Pulling this into a cloud kernel is highly prone to failure. `advanced_downloader.py` handles this with resilience:

*   **HTTP Range Headers (Resuming):** When downloading massive ZIP files from Zenodo, network sockets often drop. The downloader checks if a partial file exists on disk, reads its size in bytes, and sends an HTTP header `Range: bytes=X-` to the server. The server resumes the download from the exact byte where it failed.
*   **Chunked Streaming:** The `requests` session uses `iter_content(chunk_size=1MB)`. Instead of loading a 10GB dataset into system RAM (which would immediately crash the kernel), it streams the bytes directly from the network socket to the physical disk in 1MB chunks.
*   **Exponential Backoff:** If the Kaggle API or HuggingFace hub throws a 502 Bad Gateway or 429 Too Many Requests, the downloader does not crash. It waits 2 seconds, then 4, then 8, attempting up to 5 retries.

## 2. Bypassing the Kaggle NFS Bottleneck with O(1) Indexing

**The Silent Killer: NFS Ping Storms**
In Kaggle and Colab, the `/kaggle/input/` directory is not a physical hard drive; it is a Network File System (NFS) mounted over the cloud. 
In a naive implementation, checking `os.path.exists('image_001.png')` requires sending a network request to the NFS server and waiting for a response. If a dataset has 300,000 images, calling `os.path.exists()` during the JSONL parsing phase creates 300,000 network requests. This "ping storm" causes the OS to freeze, and the kernel will timeout before training even begins.

**The O(1) Hash Map Solution:**
In `offline_utils.py`, you implemented an ingenious bypass:
1.  **Single Traversal:** `os.walk()` traverses the directory tree exactly *once*. It collects every single file.
2.  **The Index:** It builds a global Python dictionary (`_FILENAME_INDEX`) mapping `basename -> [List of Absolute Paths]`.
3.  **O(1) Resolution:** When parsing the JSONL file, the program extracts the base image name and performs a dictionary lookup: `candidates = _FILENAME_INDEX[basename]`. This happens entirely in CPU RAM (0 milliseconds) with zero NFS traffic.
4.  **Collision Handling:** If two datasets both have a file named `1.png`, the dictionary returns two paths. The resolver checks the parent directory strings to disambiguate which path belongs to `crohme` vs `im2latex`.

```mermaid
sequenceDiagram
    participant Parser
    participant HashIndex in RAM
    participant Kaggle NFS

    Note over HashIndex, Kaggle NFS: Init: os.walk() called exactly ONCE
    HashIndex->>Kaggle NFS: Fetch all file paths
    Kaggle NFS-->>HashIndex: Return 300k paths (1 network call)
    
    Note over Parser, HashIndex: Parsing Phase
    Parser->>HashIndex: Lookup "math_123.png"
    HashIndex-->>Parser: Return "/kaggle/input/.../math_123.png"
    Note over Parser, HashIndex: ZERO network requests made during parsing
```

## 3. Eliminating Dataloader Bottlenecks

A 96GB GPU can process math equations faster than the CPU can read the images from disk. If the GPU reaches 0% utilization while waiting for the next batch, your training time doubles. Your `DataLoader` configuration uses three advanced OS-level optimizations:

1.  **`pin_memory=True`:** Normally, data loaded by the CPU is placed in "pageable" memory (which the OS can swap to the hard drive). Transferring pageable memory to the GPU is slow. Pinning the memory locks the tensors into physical RAM, allowing the GPU to use direct memory access (DMA) via the PCIe bus to pull the tensors instantly without CPU intervention.
2.  **`persistent_workers=True`:** Spawning a new Python multi-processing worker takes time. If workers are destroyed at the end of every epoch and recreated, you lose minutes of training time. Persistent workers stay alive across epoch boundaries.
3.  **`prefetch_factor=2`:** While the GPU is training on Batch 1, the CPU workers are already loading, preprocessing, and holding Batch 2 and Batch 3 in RAM, ensuring the GPU's queue is never empty."""),

    ("Chapter 9 - System Reliability/Part_1.md", """# Chapter 9: System Reliability and Checkpointing

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
The flight recorder specifically monitors `/dev/shm`. PyTorch Dataloaders use shared memory to pass the augmented image tensors from the CPU worker processes to the main GPU thread. Docker containers (which Kaggle uses) often have a hard limit on `/dev/shm` size (e.g., 8GB). If `prefetch_factor` is too high, the workers fill the shared memory, the OS triggers an Out-Of-Memory kill signal (SIGKILL), and the Python script dies instantly without warning. Monitoring `/dev/shm` allows you to scientifically tune the `num_workers` and `prefetch_factor` to stay just below the crash limit.""")
]

for filename, content in files:
    full_path = os.path.join(base_dir, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Files successfully generated/overwritten with the provided text.")
