---
tags: [framework, ollama, llama-cpp, local-inference, edge]
iteration: 4
created: 2026-08-08
aliases: [Ollama, llama.cpp, Local LLM Serving]
---

# 08 — Ollama and llama.cpp

> [!info] TL;DR
> Ollama and llama.cpp are the standard tools for running LLMs locally — on laptops, desktops, and edge devices. llama.cpp (Georgi Gerganov, 2023) is a C/C++ implementation that runs LLM inference on CPU (with optional GPU acceleration) with minimal dependencies. Ollama wraps llama.cpp with a user-friendly CLI and API, making local LLM running as easy as `ollama run llama3.1`. Together, they enabled the local-LLM ecosystem — privacy-preserving AI, offline applications, and edge deployment.

## llama.cpp

### Overview
- **Developer**: Georgi Gerganov (2023).
- **Language**: C/C++.
- **License**: MIT.
- **Status**: actively developed; the foundation of local LLM inference.

### Why llama.cpp Exists
In early 2023, LLaMA was released but required PyTorch + GPU to run. Gerganov reimplemented the inference in C/C++, with:
- No dependencies (just a C compiler).
- CPU inference (no GPU required).
- Quantized inference (INT4, INT8) for memory efficiency.
- Cross-platform (Linux, macOS, Windows, including Apple Silicon).

This made it possible to run LLMs on consumer hardware — laptops, MacBooks, even Raspberry Pi. The local-LLM ecosystem grew from this capability.

### Key Features

**GGUF format**: llama.cpp introduced the GGUF (GPT-Generated Unified Format) file format for storing quantized models. GGUF supports multiple quantization levels (INT2 through INT16) and metadata (tokenizer, chat template, model architecture). GGUF replaced the older GGML format.

**CPU inference**: llama.cpp's primary innovation. Uses optimized SIMD (AVX2, AVX-512, ARM NEON, Apple Silicon Accelerate) for fast CPU inference. A 7B model in INT4 runs at 10–30 tokens/second on a modern laptop CPU.

**GPU acceleration**: optional CUDA (NVIDIA), Metal (Apple Silicon), ROCm (AMD), and Vulkan support. When a GPU is available, llama.cpp uses it; when not, it falls back to CPU.

**Apple Silicon optimization**: llama.cpp is particularly well-optimized for Apple's M-series chips, leveraging unified memory and the Neural Engine. M-series Macs can run 70B models with reasonable performance.

**Model support**: llama.cpp supports most major LLM architectures (Llama, Mistral, Qwen, DeepSeek, Gemma, Phi, and many more). New architectures are added quickly after release.

**Server mode**: llama.cpp includes an OpenAI-compatible server (`llama-server`), so it can be used as a drop-in replacement for OpenAI in applications.

**Embeddings**: llama.cpp can compute embeddings, not just generate text. Useful for local RAG.

### Usage
```bash
# Build from source
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# Download a model (GGUF format)
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf

# Run inference
./main -m llama-2-7b-chat.Q4_K_M.gguf -p "What is the capital of France?" -n 100

# Run as a server
./server -m llama-2-7b-chat.Q4_K_M.gguf --port 8080
```

### Quantization Levels
llama.cpp supports multiple quantization levels, balancing quality and memory:

| Quantization | Bits/Weight | Memory (7B model) | Quality Loss |
|--------------|-------------|-------------------|--------------|
| FP16         | 16          | 14 GB             | none         |
| Q8_0         | 8           | 7 GB              | minimal      |
| Q5_K_M       | 5           | 4.8 GB            | small        |
| Q4_K_M       | 4           | 4.1 GB            | small        |
| Q3_K_M       | 3           | 3.3 GB            | moderate     |
| Q2_K         | 2           | 2.7 GB            | significant  |

Q4_K_M is the most popular — it balances quality and memory, allowing a 7B model to run in 4GB of RAM.

## Ollama

### Overview
- **Developer**: Ollama Inc. (2023).
- **Language**: Go (wrapper) + llama.cpp (inference).
- **License**: MIT.
- **Status**: actively developed; the standard for user-friendly local LLM running.

### Why Ollama Exists
llama.cpp is powerful but requires technical knowledge: building from source, downloading GGUF files, managing command-line flags. Ollama wraps this with a user-friendly CLI and API:
- `ollama run llama3.1` — download and run a model.
- `ollama serve` — start an OpenAI-compatible API server.
- Automatic model management (download, update, remove).
- Pre-configured models with appropriate prompts and parameters.

### Usage
```bash
# Install (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Run a model (downloads automatically if needed)
ollama run llama3.1
>>> What is the capital of France?

# List installed models
ollama list

# Serve as an API
ollama serve  # runs on port 11434
```

### API
Ollama provides an HTTP API:
```bash
curl http://localhost:11434/api/generate -d '{
    "model": "llama3.1",
    "prompt": "What is the capital of France?"
}'
```

And an OpenAI-compatible endpoint:
```bash
curl http://localhost:11434/v1/chat/completions -d '{
    "model": "llama3.1",
    "messages": [{"role": "user", "content": "Hello"}]
}'
```

### Modelfiles
Ollama uses "Modelfiles" (similar to Dockerfiles) to define custom models:
```dockerfile
FROM llama3.1

# Set parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9

# Set system prompt
SYSTEM """
You are a helpful coding assistant. Always provide complete, runnable code.
"""

# Add files (for fine-tuned models)
ADAPTER ./my-lora.gguf
```

Build with `ollama create my-model -f Modelfile`.

### Model Library
Ollama maintains a library of pre-configured models at ollama.com/library:
- `llama3.1` (Meta's Llama 3.1)
- `mistral` (Mistral 7B)
- `qwen2.5` (Alibaba's Qwen 2.5)
- `deepseek-r1` (DeepSeek's reasoning model)
- `codellama` (Meta's Code Llama)
- `nomic-embed-text` (embedding model)
- Many more

Models are automatically quantized to appropriate levels (typically Q4_K_M).

## Comparison: llama.cpp vs. Ollama

| Aspect          | llama.cpp                    | Ollama                           |
|-----------------|------------------------------|----------------------------------|
| Target user     | Developers, researchers      | General users, developers        |
| Installation    | Build from source            | One-command install              |
| Model management| Manual (download GGUF)       | Automatic (pull from library)    |
| API             | OpenAI-compatible server     | Custom + OpenAI-compatible       |
| Customization   | Full (all llama.cpp options) | Limited (via Modelfile)          |
| Performance     | Slightly faster (no wrapper) | Same (uses llama.cpp underneath) |
| Use case        | Maximum control, research    | Easy local LLM running           |

**Choose llama.cpp if**: you need maximum control, are doing research, or want to use cutting-edge features before they're in Ollama.

**Choose Ollama if**: you want to run LLMs locally with minimal setup, are building an application that needs local LLM serving, or are not a C/C++ developer.

## Use Cases

### Privacy-Preserving AI
For applications with sensitive data (medical, legal, financial), local inference keeps data on-device. No data is sent to cloud providers, simplifying compliance with GDPR, HIPAA, etc.

### Offline Applications
Applications that need to work without internet: field tools, military applications, disaster response, remote locations. Local LLMs enable AI assistance without connectivity.

### Development and Testing
Developers use Ollama/llama.cpp to test applications locally before deploying to cloud GPUs. Same model, same API, just local — enables fast iteration without API costs.

### Edge Deployment
Running LLMs on edge devices (industrial controllers, vehicles, IoT) where cloud connectivity is unreliable or latency-sensitive. llama.cpp's CPU inference and quantization make this feasible.

### Cost-Sensitive Applications
For low-volume applications, local inference is cheaper than cloud APIs. A one-time hardware purchase replaces ongoing API costs.

### Personal AI Assistants
Local LLMs enable personal AI assistants that don't send user data to cloud providers. Privacy-conscious users prefer this.

## Performance Considerations

### CPU vs. GPU
- **CPU only**: slower but works everywhere. 7B model: 10–30 tokens/sec on modern CPU.
- **GPU accelerated**: much faster. 7B model: 50–100+ tokens/sec on consumer GPU.
- **Apple Silicon**: excellent performance via Metal. M2 Max runs 70B models at reasonable speed.

### Quantization Trade-offs
- **Q8_0**: minimal quality loss, 2× memory reduction. Use when you have enough memory.
- **Q4_K_M**: small quality loss, 4× memory reduction. The default for most use cases.
- **Q2_K**: significant quality loss, 8× memory reduction. Only for extreme memory constraints.

### Memory Requirements
| Model Size | Q4_K_M Memory | Q8_0 Memory | FP16 Memory |
|------------|---------------|-------------|-------------|
| 7B         | 4 GB          | 7 GB        | 14 GB       |
| 13B        | 8 GB          | 13 GB       | 26 GB       |
| 70B        | 40 GB         | 70 GB       | 140 GB      |

Apple Silicon Macs with unified memory can run larger models than discrete-GPU systems with the same nominal memory, because they don't need to copy data between CPU and GPU.

## Strengths

### Privacy
Local inference keeps data on-device. No data leaves the user's machine. Essential for sensitive applications.

### Cost
After the one-time hardware purchase, inference is free. No per-token API costs.

### Latency
No network round-trip. First-token latency is just the model's prefill time, often <1 second.

### Offline Capability
Works without internet. Essential for field tools and unreliable connectivity scenarios.

### Open Source
Both llama.cpp and Ollama are open source. No vendor lock-in, full transparency, community-driven development.

## Weaknesses

### Performance Gap
Local hardware is slower than datacenter GPUs. A 70B model on a consumer GPU is much slower than on an H100. For high-throughput applications, cloud is better.

### Model Size Limits
Consumer hardware limits model size. A 405B model (Llama 3.1 405B) cannot run on consumer hardware — you need datacenter GPUs.

### No Training
llama.cpp and Ollama are inference-only. For training or fine-tuning, use other tools.

### Limited Multi-GPU
Multi-GPU support exists but is less mature than vLLM's tensor parallelism. For multi-GPU production serving, vLLM is better.

### Configuration Complexity (llama.cpp)
llama.cpp has many command-line flags. Tuning for optimal performance requires understanding them. Ollama abstracts this but limits control.

## Production Patterns

### Use Ollama for Development, vLLM for Production
A common pattern: develop with Ollama locally (same model, same API), deploy with vLLM on cloud GPUs for production. The OpenAI-compatible API makes this seamless.

### Quantize for the Target Hardware
Choose quantization based on available memory:
- 16GB RAM: Q4_K_M for 7B models.
- 32GB RAM: Q5_K_M for 13B, Q4_K_M for 13–33B.
- 64GB+ RAM: Q8_0 or FP16 for 7–13B, Q4_K_M for 33–70B.

### Use Apple Silicon for Personal Use
M-series Macs (especially M2/M3 Max with 64GB+ unified memory) are excellent for local LLM running. Better performance per dollar than discrete-GPU systems for single-user use.

### Bundle Models with Applications
For edge deployment, bundle the model (GGUF file) with the application. Avoid runtime downloads — they may fail or be slow.

### Use the OpenAI-Compatible API
Both llama.cpp and Ollama provide OpenAI-compatible APIs. Write your application against this API, so you can switch between local and cloud providers without code changes.

## See Also

- [[07 - vLLM]]
- [[03 - Quantization]]
- [[04 - GPU Infrastructure and Sizing]]
- [[01 - Framework Selection Guide]]
- [[25 - Frameworks and Tools/MOC|25 Frameworks MOC]]
