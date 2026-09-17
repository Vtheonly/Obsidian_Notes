---
tags: [infrastructure, gpu, compute, sizing, deployment]
iteration: 3
created: 2026-08-07
aliases: [GPU Infrastructure, GPU Sizing, GPU Deployment]
---

# 04 — GPU Infrastructure and Sizing

> [!info] TL;DR
> GPU is the dominant cost in AI infrastructure. Choosing the right GPU type, count, and deployment model (owned vs. rented vs. managed) determines your cost-per-token, latency, and capability ceiling. For inference: A10/H100 for production, L4 for development. For training: H100 for frontier, A100 for fine-tuning. For most teams, cloud GPUs with reserved capacity beat owned hardware until scale justifies ownership.

## The GPU Landscape (2024–2026)

### NVIDIA Datacenter GPUs

| GPU         | Hopper Gen | Ampere Gen | Memory       | Bandwidth | Best For                          |
|-------------|------------|------------|--------------|-----------|-----------------------------------|
| H100        | Yes        | -          | 80 GB HBM3   | 3.35 TB/s | Frontier training, large inference |
| H200        | Yes        | -          | 141 GB HBM3e | 4.8 TB/s  | Long-context inference, LLM training |
| B100/B200   | Blackwell  | -          | 192 GB HBM3e | 8 TB/s    | Next-gen training (2025+)          |
| A100 80GB   | -          | Yes        | 80 GB HBM2e  | 2.0 TB/s  | Fine-tuning, large-model inference |
| A100 40GB   | -          | Yes        | 40 GB HBM2e  | 1.5 TB/s  | Smaller models, development        |
| L40S        | Ada        | -          | 48 GB GDDR6  | 0.86 TB/s | Inference, video, graphics         |
| A10         | Ampere     | -          | 24 GB GDDR6  | 0.6 TB/s  | Small/medium inference             |
| L4          | Ada        | -          | 24 GB GDDR6  | 0.3 TB/s  | Development, small inference       |
| T4          | Turing     | -          | 16 GB GDDR6  | 0.32 TB/s | Legacy, low-cost inference         |

### AMD GPUs
- MI300X: 192 GB HBM3, competitive with H100 for inference. Software ecosystem (ROCm) is less mature than CUDA but improving.
- MI250: previous generation, used in some HPC environments.

### Other
- Google TPU v5e, v5p, v6: custom ASIC for matrix multiplication. Competitive for training and inference, but ties you to Google Cloud.
- Groq LPU: specialized for fast inference (very high tokens/sec for some models). Limited model support.
- Cerebras, SambaNova: specialized AI hardware, niche use cases.

For most teams, NVIDIA GPUs remain the default — the software ecosystem (CUDA, PyTorch, vLLM, TensorRT-LLM) is mature and well-supported.

## Sizing for Inference

### Memory Requirements
The GPU must hold:
1. **Model weights**: `params × bytes_per_param`. For a 7B model in fp16: 14 GB. In INT8: 7 GB. In INT4: 3.5 GB.
2. **KV cache**: `2 × num_layers × hidden_dim × seq_len × batch_size × bytes_per_param`. Grows with sequence length and batch size.
3. **Activations**: relatively small for inference.
4. **Overhead**: ~10% for CUDA context, framework overhead.

For a 7B model with 4k context, batch size 8, fp16:
- Weights: 14 GB.
- KV cache: ~4 GB.
- Total: ~18 GB. Fits on an A10 (24 GB).

For a 70B model with 32k context, batch size 8, fp16:
- Weights: 140 GB.
- KV cache: ~80 GB.
- Total: ~220 GB. Needs 4× A100 80GB or 3× H100 80GB with tensor parallelism.

### Throughput vs. Latency
- **Throughput-optimal**: large batch size, maximize GPU utilization. Cheapest per token but higher latency (batch must fill before processing).
- **Latency-optimal**: batch size 1, process immediately. Lowest latency but expensive per token (GPU underutilized).

For interactive chat, optimize for latency (batch 1-8). For offline batch processing, optimize for throughput (batch 32-256).

### Model Parallelism
When a model doesn't fit on one GPU:
- **Tensor parallelism (TP)**: split each layer's matrices across GPUs. Requires fast GPU-to-GPU interconnect (NVLink). Lowest latency, highest GPU coupling.
- **Pipeline parallelism (PP)**: split layers across GPUs, pipeline execution. Lower bandwidth requirement, higher latency.
- **Expert parallelism (EP)**: for MoE models, distribute experts across GPUs.
- **Data parallelism (DP)**: replicate the model across GPU groups, process different requests in parallel.

For inference, TP is most common. vLLM and TensorRT-LLM support TP seamlessly.

## Sizing for Training

### Memory Requirements
Training memory includes:
1. **Model weights**: same as inference.
2. **Gradients**: same size as weights.
3. **Optimizer state**: Adam needs 2× weights in fp32 (momentum + variance). Total: 4× weights in fp32 = 8× weights in bytes (for fp16 training).
4. **Activations**: large, depends on batch size and sequence length. Gradient checkpointing reduces this at compute cost.

For a 7B model with Adam, fp16 training, batch size 4, 4k context:
- Weights: 14 GB.
- Gradients: 14 GB.
- Optimizer: 56 GB.
- Activations: ~16 GB.
- Total: ~100 GB. Needs 2× A100 80GB.

This is why **LoRA/QLoRA** is so valuable — it freezes the base weights (no gradients, no optimizer state for them) and trains only small adapter matrices. A 65B model can be QLoRA-fine-tuned on a single 48GB GPU.

### Distributed Training Patterns
- **Data Parallel (DP)**: each GPU has a full copy, processes different batches. Gradients are all-reduced across GPUs.
- **ZeRO (DeepSpeed)**: shards optimizer state, gradients, and parameters across GPUs. Reduces memory per GPU.
- **FSDP (PyTorch)**: similar to ZeRO, native PyTorch.
- **3D Parallelism (TP + PP + DP)**: for very large models (100B+), combine all three. Complex to set up.

For fine-tuning, FSDP or ZeRO-3 is the standard. For pretraining frontier models, 3D parallelism with Megatron-LM or TorchTitan.

## Deployment Models

### Cloud On-Demand
- Pay per hour (or per second).
- Most expensive per hour but most flexible.
- Best for: development, bursty workloads, short-lived experiments.
- Providers: AWS (P4/P5 instances), GCP (A2/A3 instances), Azure (ND series), Lambda Labs, CoreWeave.

### Cloud Reserved / Spot
- **Reserved**: commit to 1–3 years, get 30–60% discount. Best for steady-state production.
- **Spot**: bid on spare capacity, 60–90% discount, can be reclaimed with 2-minute warning. Best for fault-tolerant batch workloads (training with checkpointing).

### Owned Hardware
- Buy GPUs outright. Capital expenditure, not operational.
- Amortized over 3–4 years, cheapest per hour at high utilization.
- Best for: steady-state production with predictable load, teams with datacenter capacity.
- Total cost of ownership includes power, cooling, networking, datacenter space, and operations staff.

### Managed Inference Services
- Provider runs the model, you call an API. Examples: OpenAI, Anthropic, Together, Anyscale, Replicate, Modal, Baseten.
- No GPU management; pay per token or per hour.
- Best for: teams without ML infrastructure expertise, low-volume workloads, prototypes.
- Limitation: less control over model, prompt, and deployment.

### Decision Framework
| Workload profile                       | Best deployment                |
|----------------------------------------|--------------------------------|
| Prototype, low volume                  | Managed API (OpenAI, Together) |
| Production, low-medium volume          | Cloud on-demand or reserved    |
| Production, high volume                | Cloud reserved or owned        |
| Training, occasional                   | Cloud spot with checkpointing  |
| Training, continuous                   | Owned or cloud reserved        |
| Latency-sensitive, low volume          | Cloud on-demand, single GPU    |
| Latency-sensitive, high volume         | Owned, multiple GPUs           |

## Cost Optimization

### Quantization
- INT8 (or FP8): 2× memory reduction, minimal quality loss. Supported by vLLM, TensorRT-LLM.
- INT4 (GPTQ, AWQ): 4× memory reduction, small quality loss. Best for cost-sensitive inference.
- QLoRA: 4-bit base + 16-bit adapter. Enables fine-tuning large models on small GPUs.

### Speculative Decoding
A small "draft" model proposes tokens; the large model verifies. When the draft is correct, you skip the large model's forward pass. 2–3× throughput on accept-heavy workloads. See [[05 - Speculative Decoding]].

### Caching
- **Prefix caching**: cache the KV state of common prefixes (system prompts, few-shot examples). Avoids recomputation.
- **Semantic caching**: cache responses for similar queries. Higher hit rate but risks returning wrong answers.

### Batching
- **Continuous batching** (vLLM): process requests of different lengths together, dynamic batching. 5–10× throughput vs. naive batching. See [[04 - vLLM and Continuous Batching]].

### Right-Sizing
- Match GPU size to model size. Don't run a 7B model on an H100 — use an A10 or L4.
- Match GPU count to throughput requirements. Don't use 4 GPUs if 2 suffice.
- Monitor utilization. If GPU utilization is <50%, you're over-provisioned.

## Operational Concerns

### GPU Drivers and CUDA
- Pin driver versions. Driver upgrades can break CUDA compatibility.
- Use Docker images with bundled CUDA to avoid host driver issues (NVIDIA Container Toolkit).

### Monitoring
- **GPU utilization**: target >70% for production. Low utilization = wasted spend.
- **Memory utilization**: track actual usage vs. allocation.
- **Temperature**: high temperatures throttle performance and reduce GPU lifespan.
- **Power draw**: for capacity planning.

Tools: `nvidia-smi`, DCGM exporter (Prometheus), Cloud provider metrics.

### Failure Handling
- GPUs fail. Plan for it.
- For inference: load balancer + health checks + multiple replicas.
- For training: checkpoint frequently; resume from last checkpoint on failure.
- For spot instances: checkpoint every N steps; use spot replacement controllers (k8s spot handler).

### Networking
- For multi-GPU inference: NVLink (within a node) >> InfiniBand (across nodes) >> Ethernet.
- For training: InfiniBand or NVLink required for 3D parallelism. Ethernet-only training is impractical at scale.

## Common Pitfalls

### Overprovisioning for Headroom
"We might need more capacity, so let's get 8 GPUs." Unused GPUs are pure waste. Start small, scale based on actual load.

### No Quantization
Running fp16 when INT8 would suffice. 2× cost for negligible quality difference. Always quantize for inference unless you have a specific reason not to.

### No Continuous Batching
Processing one request at a time. 5–10× more expensive than necessary. Use vLLM or a similar server.

### Synchronous Inference in Web Handlers
Calling the LLM synchronously in a FastAPI handler blocks the worker. Use async patterns or offload to a dedicated inference service.

### No Checkpointing for Training
Training for days without checkpointing. A failure at hour 47 loses everything. Checkpoint every N minutes.

### Wrong GPU Type for Workload
Using an H100 for a 1B model. Using a T4 for a 70B model. Match the GPU to the workload.

### Ignoring Spot for Batch
Batch workloads (training, evaluation, bulk inference) are perfect for spot instances. Paying on-demand for these is a 4–10× cost premium.

## See Also

- [[01 - Production AI Stack]]
- [[02 - Vector Storage with pgvector]]
- [[03 - Messaging with Kafka and Celery]]
- [[05 - Observability Stack]]
- [[04 - vLLM and Continuous Batching]]
- [[03 - Quantization]]
- [[05 - Speculative Decoding]]
- [[20 - AI Infrastructure/MOC|20 AI Infrastructure MOC]]
