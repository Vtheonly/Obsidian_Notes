---
tags: [frameworks, langgraph, autogen, pydanticai, crewai, vllm]
iteration: 2
created: 2026-08-07
aliases: [Framework Selection Guide]
---

# 01 - Framework Selection Guide

> [!info] TL;DR
> Choosing the right framework for your AI project: LangGraph for production agents, PydanticAI for type-safe Python, vLLM for serving, Ollama for local dev, pgvector for vector DB if you already have Postgres, Qdrant otherwise. This note guides the choices.

## Decision Tree

### What are you building?

**A chatbot / single-turn Q&A**
- Use direct OpenAI / Anthropic SDK or `litellm`.
- Don't need a framework.

**A RAG system**
- Use LlamaIndex (purpose-built for RAG) or LangChain.
- For simple cases, write the pipeline directly.

**An agent (single agent with tools)**
- PydanticAI (type-safe, clean API).
- LangGraph (more features, more complex).
- OpenAI Agents SDK (if OpenAI-only).

**A multi-agent system**
- LangGraph (production-grade, durable).
- AutoGen (group chat pattern).
- CrewAI (role-based, simpler).

**Serving an LLM in production**
- vLLM (default).
- TensorRT-LLM (NVIDIA-only, max perf).
- SGLang (newer, often faster for agentic workloads).

**Running LLMs locally**
- Ollama (easiest UX).
- llama.cpp (most flexible, lowest level).
- LM Studio (GUI).

**Vector database**
- pgvector (if you have Postgres; simplest ops).
- Qdrant (standalone, fast, Rust-based).
- Weaviate (feature-rich).
- Milvus (very large scale).
- Pinecone (managed, no ops).

**Embedding models**
- BGE (open-source default).
- OpenAI text-embedding-3 (managed, easy).
- Cohere / Voyage (managed, high quality).

## Framework Summaries

### LangChain / LangGraph
- **LangChain**: general LLM application framework. Many integrations; can be over-abstracted.
- **LangGraph**: graph-based agent framework. Production-grade, durable execution. **The recommended choice for serious agent work.**
- LangSmith: observability and eval (commercial).

### LlamaIndex
- RAG-focused framework. Better than LangChain for pure RAG.
- Strong data connectors (loaders for many file types).
- Less general-purpose than LangChain.

### OpenAI SDK / Agents SDK
- OpenAI's first-party Python SDK.
- Agents SDK (2024+): official agent framework, tight OpenAI integration.
- Useful if you're committed to OpenAI models.

### PydanticAI
- Type-safe agent framework. Strong Python type hints.
- Built by the Pydantic team.
- Clean API, less abstraction than LangChain.
- Good for production agents that need type safety.

### AutoGen (Microsoft)
- Multi-agent conversation framework.
- Group chat pattern (multiple agents talk to each other).
- AutoGen 0.4+ (2025) is a major rewrite with cleaner architecture.

### CrewAI
- Role-based multi-agent framework.
- Define agents with roles ("Researcher", "Writer"), assign tasks.
- Simpler than LangGraph; less flexible.
- Good for straightforward workflows.

### Semantic Kernel (Microsoft)
- Multi-language (Python, C#, Java).
- Strong in enterprise Microsoft-stack environments.
- Less popular in pure Python ecosystems.

### Haystack (deepset)
- Older framework, still maintained.
- Good for search and RAG.
- Less popular than LangChain/LlamaIndex.

### DSPy (Stanford)
- "Programming with prompts" — declarative prompt optimization.
- Compiles declarative programs into optimized prompts.
- Research-grade but production-curious.

## Serving Frameworks

### vLLM
- Default for production LLM serving.
- PagedAttention, continuous batching, prefix caching, spec decoding, LoRA serving.
- OpenAI-compatible API.

### TensorRT-LLM (NVIDIA)
- Highest performance on NVIDIA hardware.
- Compiles models to optimized kernels.
- Use only for NVIDIA-only deployments with strict perf requirements.

### TGI (HuggingFace)
- HuggingFace's serving engine.
- Good HF Hub integration.
- Less performant than vLLM.

### SGLang
- Newer; strong for agentic / structured workloads.
- RadixAttention for prefix caching.
- Often outperforms vLLM on specific workloads.

### Ollama
- Local LLM runtime. Best UX for single-user dev.
- GGUF format; CPU + GPU.
- Not for production serving.

### llama.cpp
- C++ LLM inference library. Lower-level than Ollama.
- Best for embedded / edge / custom integrations.
- GGUF format.

## Worked Example (PydanticAI agent)

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ResearchResult(BaseModel):
    summary: str
    sources: list[str]

research_agent = Agent(
    model='openai:gpt-4o',
    result_type=ResearchResult,
    system_prompt='You are a research assistant. Provide concise summaries with sources.',
)

@research_agent.tool
async def search(ctx, query: str) -> str:
    """Search the web."""
    return await web_search(query)

result = research_agent.run_sync('Research the history of attention in deep learning.')
print(result.data.summary)
print(result.data.sources)
```

## Why This Matters for AI

- Framework choice affects **development speed, production reliability, and team productivity**.
- The "best" framework depends on your use case, team skills, and existing stack.
- For most teams starting new agent work in 2026: **LangGraph for agents, vLLM for serving, pgvector for vectors** is a sensible default stack.

## Production Implications

- **Don't over-framework**. Many use cases are simpler without a framework — direct API calls work fine.
- **For production agents**: LangGraph is the safest bet. Durable, observable, well-supported.
- **For serving**: vLLM is the default. Move to TensorRT-LLM only if you've benchmarked and need more.
- **For local dev**: Ollama. So much easier than installing CUDA, PyTorch, etc.
- **Avoid vendor lock-in**: prefer open-source frameworks where possible. Use LiteLLM for LLM API abstraction.

## Common Pitfalls

- **Adopting a framework too early** — start with direct API calls; add a framework when you outgrow them.
- **Using LangChain for everything** — it's general-purpose but over-abstracted for simple cases.
- **Mixing frameworks** — pick one and commit. Mixing LangChain + LlamaIndex + custom code is a mess.
- **Ignoring observability** — whatever framework you pick, add tracing (LangSmith, Langfuse, Arize).

## See Also

- [[25 - Frameworks and Tools/MOC|Frameworks MOC]]
- [[15 - AI Agents/MOC|15 AI Agents]]
- [[13 - Inference/Serving/04 - vLLM and Continuous Batching|vLLM]]
- [[19 - MCP/MOC|19 MCP]]
