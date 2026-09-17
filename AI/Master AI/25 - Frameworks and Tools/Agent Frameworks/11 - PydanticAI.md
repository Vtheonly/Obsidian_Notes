---
tags: [framework, pydantic-ai, agents, type-safe, validation]
iteration: 6
created: 2026-08-08
aliases: [PydanticAI, Pydantic AI, Type-Safe Agents]
---

# 11 — PydanticAI

> [!info] TL;DR
> PydanticAI is a type-safe agent framework from the team behind Pydantic. The core idea: leverage Python type hints to define agent inputs, outputs, tool schemas, and dependencies — and let Pydantic validate everything at runtime. Where LangChain and AutoGen lean on JSON schemas and stringly-typed prompts, PydanticAI leans on Python types. This produces agents that are statically analyzable, IDE-friendly, and resistant to the "model returned weird JSON" class of bugs. PydanticAI is best for **production single-agent systems** where reliability and type safety matter more than multi-agent orchestration.

## Overview

- **Developer**: Pydantic Team (Samuel Colvin et al., 2024).
- **Languages**: Python (Python 3.10+).
- **License**: MIT.
- **Status**: actively developed; production-focused. Stable API since 0.0.10+.

## Why PydanticAI Exists

Most agent frameworks have a type-safety problem. Tools are defined as dicts or JSON schemas; outputs are parsed from strings; dependencies are passed via context objects with no static guarantees. This produces three classes of bugs:

1. **Tool argument mismatch**: the LLM calls a tool with the wrong argument types; the framework crashes at runtime.
2. **Output schema drift**: the LLM returns valid JSON but missing a field; downstream code crashes when it accesses the missing field.
3. **Implicit dependencies**: agents reach into global state or environment variables; tests can't isolate behavior.

PydanticAI addresses all three by leaning on Python type hints and Pydantic validation. The framework was built by the Pydantic team — the same people who wrote the validation library used by FastAPI, LangChain, and most of the Python web ecosystem. They know type safety.

## Core Concepts

### Agents

An agent is parameterized by the **output type** it produces:

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ResearchSummary(BaseModel):
    topic: str
    key_findings: list[str]
    confidence: float

research_agent = Agent(
    model="openai:gpt-4o-mini",
    output_type=ResearchSummary,
    system_prompt="You are a research analyst. Return a structured summary.",
)
```

The `output_type` can be a Pydantic model, a Python primitive (`str`, `int`, `bool`), a list, or a union. PydanticAI uses the type to construct the tool schema the LLM sees (when using tool-mode) or to validate the response (when using response-mode).

### Running an Agent

```python
result = await research_agent.run("Summarize the latest Mamba-2 paper.")
print(result.output)  # ResearchSummary(topic=..., key_findings=[...], confidence=0.8)
```

`result.output` is a fully validated `ResearchSummary` instance. If the LLM's response doesn't validate, PydanticAI retries (up to a configurable limit) with the validation error in context — so the LLM can correct itself.

### Tools

Tools are defined as Python functions with type hints:

```python
from pydantic_ai import RunContext

@research_agent.tool
async def search_web(ctx: RunContext[None], query: str, max_results: int = 5) -> list[dict]:
    """Search the web and return results."""
    # ctx contains dependencies, usage tracking, etc.
    return await search_api(query, limit=max_results)
```

The function's docstring becomes the tool description. The type hints become the JSON schema. The function is called with the LLM-provided arguments, validated by Pydantic. If validation fails, the error is returned to the LLM as a tool message — no exception raised.

### Dependencies

PydanticAI's signature feature is **typed dependencies**. The `RunContext` parameter carries a typed dependency object:

```python
from dataclasses import dataclass

@dataclass
class ResearchDeps:
    api_key: str
    rate_limiter: RateLimiter
    cache: Cache

@research_agent.tool
async def search_web(ctx: RunContext[ResearchDeps], query: str) -> list[dict]:
    await ctx.deps.rate_limiter.acquire()
    cached = ctx.deps.cache.get(query)
    if cached:
        return cached
    results = await search_api(query, api_key=ctx.deps.api_key)
    ctx.deps.cache.set(query, results)
    return results

# Pass deps at run time
result = await research_agent.run("...", deps=ResearchDeps(api_key="...", rate_limiter=rl, cache=c))
```

This is fundamentally different from LangChain, where dependencies typically come from global configuration or environment variables. With typed deps:

- Tests pass mock dependencies explicitly.
- IDE autocompletion works on `ctx.deps`.
- Static type checkers verify tool bodies use dependencies correctly.

### Streaming

PydanticAI streams partial outputs as they arrive. For structured outputs, it streams the JSON tokens and attempts partial validation:

```python
async with research_agent.run_stream("Summarize...") as result:
    async for partial in result.stream():
        print(partial)  # partial ResearchSummary, validated up to what's available
```

This is useful for UIs that show progressive results.

### Multi-Agent Handoffs

PydanticAI supports agent handoffs via tool delegation:

```python
@research_agent.tool
async def delegate_to_writer(ctx: RunContext[ResearchDeps], draft: str) -> str:
    """Pass the research draft to the writer agent."""
    writer_result = await writer_agent.run(draft, deps=ctx.deps)
    return writer_result.output
```

This is lighter than AutoGen's group chat or LangGraph's subgraphs, but sufficient for sequential multi-agent pipelines.

### Programmatic Usage Tracking

Every `result` exposes a `usage` object tracking input/output tokens and tool calls. This is essential for cost monitoring in production:

```python
result = await research_agent.run("...")
print(result.usage())  # Usage(input_tokens=1234, output_tokens=567, tool_calls=3)
```

## Common Patterns

### Typed RAG

PydanticAI is well-suited to RAG where the retrieval step benefits from typed inputs:

```python
@rag_agent.tool
async def retrieve(ctx: RunContext[Deps], query: str, top_k: int = 5) -> list[Document]:
    """Retrieve relevant documents."""
    return await ctx.deps.vector_db.search(query, k=top_k)
```

The LLM gets a clean tool schema; the retrieval function gets typed arguments; downstream code can rely on the returned `Document` type.

### Validation Loops

Because outputs are validated, you can build "validate and retry" loops cheaply:

```python
for attempt in range(3):
    try:
        result = await agent.run(user_input)
        return result.output  # validated
    except ValidationError:
        continue
raise RuntimeError("Agent failed to produce valid output after 3 attempts")
```

PydanticAI itself does retry-with-error-feedback internally, so this outer loop is rarely needed — but it's available as a safety net.

### Testing with Mock Dependencies

Because dependencies are typed and injected at runtime, tests are clean:

```python
async def test_research_agent_uses_cache():
    mock_cache = MockCache(...)
    deps = ResearchDeps(api_key="test", rate_limiter=NoOpRateLimiter(), cache=mock_cache)
    result = await research_agent.run("test query", deps=deps)
    assert mock_cache.get_called_with == "test query"
```

No global state to reset; no environment variables to mock. This is PydanticAI's strongest production feature.

### Multi-Model Agents

The same agent can run on multiple models by parameterizing at call time:

```python
# Use a small model for cheap tasks
result_cheap = await research_agent.run("simple query", model="openai:gpt-4o-mini")
# Use a big model for hard tasks
result_good = await research_agent.run("complex query", model="anthropic:claude-3-5-sonnet")
```

This enables cost-quality routing: route easy queries to cheaper models, hard queries to expensive ones.

## Comparison to Alternatives

| Framework   | Type Safety                  | Multi-Agent           | Best For                              |
|-------------|------------------------------|-----------------------|---------------------------------------|
| PydanticAI  | First-class (Python types)   | Via handoffs          | Type-safe single-agent production     |
| LangGraph   | Optional (Pydantic state)    | First-class (subgraphs) | Production agents, HiTL, durable    |
| AutoGen     | JSON schemas                 | First-class (group chat) | Multi-agent research               |
| CrewAI      | Optional (output_pydantic)   | First-class (crews)   | Role-based teams, content             |
| LangChain   | JSON schemas                 | Via AgentExecutor     | Prototyping, broad integrations       |

PydanticAI's distinct strength is **static type safety**: IDE autocompletion, mypy/pyright checking, and runtime validation all the way down. The trade-off is less multi-agent machinery.

## Strengths

### Type Safety End-to-End

From tool arguments to dependencies to outputs, every type is checked. This eliminates the "model returned weird JSON" class of bugs that plague other frameworks. mypy/pyright can verify your agent code before runtime.

### Testability

Typed, injected dependencies make agents trivially testable. No global state, no environment variable mocking. Tests look like normal Python tests. This is rare and valuable.

### Pydantic Ecosystem Integration

PydanticAI integrates natively with FastAPI (use PydanticAI agents as FastAPI endpoints), SQLModel (typed database queries), and the broader Pydantic ecosystem. If your stack is already Pydantic-based, PydanticAI fits cleanly.

### Validation with Retry

Output validation with error-feedback retry is built-in. The LLM gets the validation error and can self-correct. This dramatically improves output reliability for structured tasks.

### Clean Async API

The framework is async-first without forcing async on users who don't need it. Sync wrappers (`agent.run_sync`) are available for scripts and notebooks.

## Weaknesses

### Single-Agent Focus

PydanticAI is designed for single-agent systems with optional handoffs. If you need true multi-agent orchestration (group chats, manager routing, debate), you'll find PydanticAI limiting. AutoGen or CrewAI is better.

### Smaller Ecosystem

PydanticAI is newer than LangChain. Fewer pre-built integrations, fewer community examples, fewer Stack Overflow answers. You'll write more code yourself.

### Less HiTL Support

PydanticAI doesn't have first-class `interrupt_before`-style HiTL. You can implement it by splitting runs, but it's not a framework primitive like in LangGraph.

### No Built-In Memory

PydanticAI doesn't ship a memory layer. You build your own using dependencies (e.g., a `Memory` object in your deps dataclass). This is flexible but more work than CrewAI's built-in long-term memory.

## Production Patterns

### Define Dependencies as Dataclasses

Use a `@dataclass` for your `Deps` type. It's mutable, fast to construct, and works cleanly with type checkers. Avoid Pydantic `BaseModel` for deps unless you need validation — it adds overhead.

### Use Output Models Aggressively

Always specify `output_type` as a Pydantic model. Don't accept raw strings from agents in production. Structured outputs catch prompt drift and make downstream code reliable.

### Pass API Clients via Deps

Don't reach into environment variables from tool bodies. Pass API clients (OpenAI, search, vector DB) via deps. This makes tests trivial and lets you swap implementations per environment.

### Track Usage

Always log `result.usage()`. Token costs are the #1 surprise in production agent systems. Aggregated usage data lets you alert on budget overruns.

### Compose with FastAPI

PydanticAI agents fit cleanly into FastAPI endpoints:

```python
@app.post("/research")
async def research_endpoint(query: str) -> ResearchSummary:
    result = await research_agent.run(query, deps=get_deps())
    return result.output
```

The output Pydantic model serves as both the agent's output type and the FastAPI response model. Single source of truth.

## When to Use PydanticAI

### Good Fit
- **Production single-agent systems** where reliability matters.
- **API-backed agents** (FastAPI integration is clean).
- **Teams that value type safety** and IDE support.
- **Tested agent systems** (typed deps make testing trivial).
- **Structured output tasks** (validation with retry is a major win).

### Poor Fit
- **Complex multi-agent orchestration**: use LangGraph or AutoGen.
- **Rapid prototyping**: LangChain has more pre-built integrations.
- **Heavy tool ecosystems**: LangChain's tool library is larger.
- **When you need HiTL pauses**: LangGraph is better.

## See Also

- [[09 - AutoGen]] — multi-agent alternative
- [[10 - CrewAI]] — role-based alternative
- [[03 - LangGraph]] — graph-based alternative with HiTL
- [[04 - Function Calling]] — how PydanticAI's tools work
- [[25 - Frameworks and Tools/MOC|25 Frameworks MOC]]
