---
tags: [framework, langchain, llm-framework, abstractions]
iteration: 8
created: 2026-08-08
last_updated: 2026-08-08
aliases: [LangChain, LangChain Framework]
---

# 02 — LangChain

> [!info] TL;DR
> LangChain was the first widely-adopted LLM application framework, providing abstractions for prompts, chains, agents, tools, memory, and retrieval. Its "LCEL" (LangChain Expression Language) lets you compose components via a pipe syntax. LangChain's breadth (it tries to do everything) made it the default starting point for LLM apps in 2022–2023, but its heavy abstractions and frequent breaking changes have pushed many production teams toward lighter alternatives or direct API usage.

## Overview

- **Developer**: LangChain Inc. (Harrison Chase, 2022).
- **Language**: Python, JavaScript/TypeScript.
- **License**: MIT.
- **Status**: actively developed; the framework has evolved significantly (LangChain → LCEL → LangGraph for agents).

## Core Abstractions

LangChain provides a layered set of abstractions:

### Prompts
`PromptTemplate` and `ChatPromptTemplate` format strings with variables:
```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Summarize this: {text}"),
])
```

### Models
Wrappers for LLM providers (OpenAI, Anthropic, local models):
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
```

### Output Parsers
Parse LLM output into structured data:
```python
from langchain.output_parsers import PydanticOutputParser
parser = PydanticOutputParser(pydantic_object=MySchema)
```

### Chains (LCEL)
The LangChain Expression Language composes components via pipe syntax:
```python
chain = prompt | llm | parser
result = chain.invoke({"text": "long text..."})
```

LCEL is the modern way to compose LangChain components. It replaces the older `LLMChain` class and provides streaming, batching, and async support automatically.

### Agents
LangChain's agent abstraction wraps an LLM with tools:
```python
from langchain.agents import create_tool_calling_agent

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
result = agent_executor.invoke({"input": "What's the weather?"})
```

For modern agent development, LangChain recommends **LangGraph** (see [[03 - LangGraph]]) — a more controlled graph-based approach that supersedes the older agent abstractions.

### Memory
Conversation memory:
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
```

### Retrievers
Wrappers for vector stores and retrieval:
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()
```

## Strengths

### Breadth of Integrations
LangChain integrates with virtually every LLM provider, vector store, document loader, and tool. If a new service appears, LangChain likely has an integration within weeks. This makes it excellent for prototyping — you can swap components without rewriting code.

### LCEL Composition
The pipe syntax (`prompt | llm | parser`) is intuitive and provides streaming, batching, and async for free. This is a genuine productivity boost for simple chains.

### Documentation and Community
LangChain has extensive documentation, tutorials, and a large community. Most LLM application patterns have a LangChain example, making it easy to learn from existing code.

### LangSmith Integration
LangChain's observability platform (LangSmith) provides tracing, evaluation, and prompt management. It's one of the better LLM observability tools, though it works best with LangChain applications.

## Weaknesses

### Heavy Abstractions
LangChain wraps every concept in multiple layers of abstraction. A simple "call the LLM" can require understanding `Runnable`, `RunnableSerializable`, `BaseChatModel`, and provider-specific classes. For simple use cases, this is overkill.

### Frequent Breaking Changes
LangChain's API changed significantly between versions. Code written for LangChain 0.0.200 may not work with 0.1.0. This is frustrating for production teams that need stability.

### Magic Behavior
Some abstractions (especially the older `AgentExecutor`) have surprising default behaviors. The agent might loop forever, call tools in unexpected orders, or fail silently. Debugging requires understanding LangChain's internal state machine.

### Performance Overhead
The abstraction layers add overhead. For high-throughput applications, calling the OpenAI API directly is faster than going through LangChain's wrappers.

### Lock-In
Once your application is deeply integrated with LangChain, migrating to direct API calls or a different framework is painful. The abstractions don't map cleanly to other frameworks.

## When to Use LangChain

### Good Fit
- **Prototyping**: LangChain's breadth makes it excellent for trying ideas quickly.
- **Educational**: learning LLM application patterns.
- **Integration-heavy**: when you need to connect many components (LLM + vector store + document loader + tools).
- **LangSmith users**: if you want LangSmith observability, LangChain is the natural fit.

### Poor Fit
- **Simple API calls**: if you just need to call OpenAI's API, LangChain adds complexity without value.
- **High-throughput production**: the abstraction overhead matters.
- **Long-term stable codebase**: frequent breaking changes are a liability.
- **Agent applications**: use LangGraph instead — it's more controlled and is the recommended approach.

## Production Patterns

### Use LCEL, Not Legacy Chains
The legacy `LLMChain`, `SequentialChain`, etc. are deprecated. Use LCEL's pipe syntax for all composition. It's more powerful, more readable, and gets streaming/async for free.

### Avoid `AgentExecutor`
The legacy agent executor is being phased out. For agents, use LangGraph, which provides:
- Explicit state management.
- Better control over the agent loop.
- Built-in support for human-in-the-loop.
- Persistent state across runs.

### Pin Dependencies
LangChain's breaking changes mean you should pin exact versions in production. Test thoroughly before upgrading.

### Use LangSmith for Observability
If you're using LangChain, LangSmith is the natural observability tool. It provides traces, eval, and prompt management that integrate seamlessly.

### Consider Direct API Calls for Simple Cases
If a chain is just `prompt | llm | parser`, consider implementing it directly with the provider's SDK. You get more control, less overhead, and no framework dependency.

## Comparison to Alternatives

| Framework   | Strengths                          | Weaknesses                       | Best For                          |
|-------------|------------------------------------|----------------------------------|-----------------------------------|
| LangChain   | Breadth, integrations, community   | Heavy, breaking changes          | Prototyping, integration-heavy    |
| LlamaIndex  | RAG-focused, cleaner abstractions  | Narrower scope                   | RAG applications                  |
| DSPy        | Prompt optimization, declarative   | Steeper learning curve           | Prompt engineering at scale       |
| Direct SDK  | Simple, fast, no lock-in           | You build abstractions yourself  | Simple applications, production   |

## The LangChain Ecosystem

LangChain Inc. has expanded into multiple products:
- **LangChain**: the core framework.
- **LangGraph**: graph-based agent orchestration (the recommended approach for agents).
- **LangSmith**: observability and eval platform (commercial).
- **LangServe**: deploy LangChain applications as APIs.
- **LangChain Hub**: shared prompts and components.

The ecosystem is comprehensive but can be overwhelming. For new projects, the recommended path is: LangGraph for agents, LCEL for simple chains, LangSmith for observability.

## LCEL (LangChain Expression Language) in Detail

LCEL is the modern way to compose LangChain components. Any LCEL chain:
- Supports streaming (token-by-token output) for free.
- Supports async (`ainvoke`, `astream`) for free.
- Supports batching (`batch`) for free.
- Has built-in retry and fallback mechanisms.
- Integrates with LangSmith for tracing.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel

class Summary(BaseModel):
    title: str
    summary: str
    key_points: list[str]

# LCEL chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the following text. {format_instructions}"),
    ("user", "{text}"),
])
parser = PydanticOutputParser(pydantic_object=Summary)
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

chain = prompt | llm | parser

# Synchronous
result = chain.invoke({
    "text": "long text...",
    "format_instructions": parser.get_format_instructions(),
})

# Streaming tokens (not the parsed output)
for chunk in (prompt | llm | StrOutputParser()).stream({"text": "...", "format_instructions": "..."}):
    print(chunk, end="", flush=True)

# Async
result = await chain.ainvoke({"text": "...", "format_instructions": "..."})

# Batching
results = chain.batch([{"text": t, "format_instructions": "..."} for t in texts])

# With fallback
from langchain_core.runnables import RunnableWithFallbacks
robust_chain = chain.with_fallbacks([simple_chain])
```

The pipe syntax (`|`) is implemented via Python's `__or__` operator. Each component is a `Runnable` with `invoke`, `stream`, `ainvoke`, `astream`, `batch` methods. The composition handles data flow and error propagation automatically.

## Common LangChain Patterns (Production)

### Pattern 1: Simple Chain (Use LCEL)
```python
chain = prompt | llm | parser
```
Best for: stateless request-response. Don't use the legacy `LLMChain` class.

### Pattern 2: RAG with LCEL
```python
from langchain_community.vectorstores import pgvector
from langchain_openai import OpenAIEmbeddings

vectorstore = pgvector.PGVector(connection_string=..., embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

rag_prompt = ChatPromptTemplate.from_template("""Answer based on:
{context}

Question: {question}""")

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)
```

### Pattern 3: Agents (Use LangGraph, NOT legacy AgentExecutor)
```python
# DON'T: from langchain.agents import AgentExecutor
# DO: use LangGraph
```

See [[03 - LangGraph]] for the modern agent pattern.

### Pattern 4: Streaming with Sources
```python
def format_with_sources(docs, answer):
    return {"answer": answer, "sources": [{"content": d.page_content, "metadata": d.metadata} for d in docs]}

chain = (
    RunnableParallel({"docs": retriever, "question": RunnablePassthrough()})
    | {"docs": lambda x: x["docs"], "answer": (lambda x: x["question"]) | rag_prompt | llm | StrOutputParser()}
    | (lambda x: format_with_sources(x["docs"], x["answer"]))
)
```

## Migration Guide: Legacy to Modern

| Legacy (avoid)        | Modern (use)            | Notes                              |
|-----------------------|-------------------------|------------------------------------|
| `LLMChain`            | `prompt | llm` (LCEL)   | LCEL has streaming, async, batch   |
| `SequentialChain`     | LCEL with `|`           | Compose via pipe                   |
| `AgentExecutor`       | LangGraph               | Better state, control, observability |
| `ConversationBufferMemory` | LangGraph state   | Graph state is more flexible        |
| `RetrievalQA`         | LCEL RAG chain          | LCEL is more customizable          |
| `load_qa_chain`       | LCEL with stuff/map_reduce | LCEL handles all QA patterns    |

If you're starting a new LangChain project, use only LCEL + LangGraph. Avoid all legacy classes.

## Common Pitfalls (Production)

1. **Mixing legacy and LCEL**: the legacy classes don't compose with LCEL cleanly. Pick one (LCEL) and stick with it.
2. **Not pinning versions**: LangChain's API changes between minor versions. Pin to `langchain==0.3.x` and test before upgrading.
3. **Using `AgentExecutor` for production agents**: it's deprecated and has unpredictable behavior. Use LangGraph.
4. **Trusting the model to format output**: use Pydantic parsers + retry logic. Models will return malformed JSON occasionally.
5. **Not using LangSmith**: if you're using LangChain, LangSmith is the natural observability tool. Without it, debugging LCEL chains is much harder.
6. **Over-abstraction**: if a chain is just `prompt | llm`, consider direct SDK calls. LangChain adds overhead for simple use cases.
7. **Not handling rate limits**: LCEL has built-in retry, but you need to configure it. Use `chain.with_retry()` for production.

## Performance Considerations

LangChain adds overhead compared to direct SDK calls:
- **Latency**: 5-20ms per chain component (negligible for LLM-bound workloads, noticeable for high-QPS).
- **Memory**: each Runnable has metadata, schema, and serialization overhead.
- **CPU**: input/output parsing and validation.

For high-throughput production (>1000 QPS), consider:
- Direct SDK calls for simple chains.
- Custom async wrappers for complex logic.
- LangChain only for prototyping or integration-heavy code.

For most applications (1-100 QPS), the overhead is negligible compared to LLM latency.

## Comparison with Modern Alternatives (2026)

| Framework   | Philosophy                              | Best For                              | Lock-in Risk |
|-------------|-----------------------------------------|---------------------------------------|--------------|
| LangChain   | Wrap everything in abstractions         | Prototyping, integration-heavy        | High         |
| LangGraph   | Graph-based orchestration               | Agents, multi-step workflows          | Medium       |
| LlamaIndex  | RAG-focused, cleaner abstractions       | RAG applications                      | Medium       |
| DSPy        | Declarative prompt optimization         | Prompt engineering at scale           | Low (PyTorch-like) |
| PydanticAI  | Type-safe, minimal abstractions         | Production agents, type safety        | Low          |
| Direct SDK  | No framework                            | Simple applications, maximum control  | None         |

The 2024-2026 trend is away from LangChain toward either LangGraph (for agents) or direct SDK + PydanticAI (for simple applications). LangChain remains useful for prototyping and integration-heavy applications.

## Connection to Other Concepts

- [[25 - Frameworks and Tools/Agent Frameworks/03 - LangGraph|LangGraph]] — the recommended agent framework from LangChain Inc.
- [[25 - Frameworks and Tools/LLM Frameworks/05 - LlamaIndex|LlamaIndex]] — RAG-focused alternative.
- [[25 - Frameworks and Tools/LLM Frameworks/04 - DSPy|DSPy]] — declarative prompt optimization.
- [[25 - Frameworks and Tools/Agent Frameworks/11 - PydanticAI|PydanticAI]] — type-safe modern alternative.
- [[25 - Frameworks and Tools/Agent Frameworks/01 - Framework Selection Guide|Framework Selection Guide]] — when to use which.
- [[21 - LLMOps and MLOps/MOC|LLMOps]] — operational concerns.
- [[15 - AI Agents/MOC|AI Agents]] — agent patterns.

## Interview Questions

1. **Q: What is LCEL, and why is it preferred over legacy LangChain chains?**
   A: LCEL (LangChain Expression Language) composes components via pipe syntax (`prompt | llm | parser`). Preferred because it provides streaming, async, batching, retry, and LangSmith tracing for free — without writing extra code. Legacy chains (`LLMChain`, `SequentialChain`) are deprecated, don't support these features natively, and have less consistent behavior.

2. **Q: When would you NOT use LangChain?**
   A: Four cases: (1) simple API calls — direct SDK is faster and simpler, (2) high-throughput production — LangChain's overhead matters at >1000 QPS, (3) long-term stable codebase — LangChain's frequent breaking changes are a liability, (4) agent applications — use LangGraph instead, which is the recommended modern approach.

3. **Q: How does LangChain compare to LangGraph?**
   A: LangChain is the umbrella framework for LLM applications (prompts, chains, retrievers, legacy agents). LangGraph is a separate library (from the same company) for graph-based agent orchestration — explicit state, cycles, durable execution. LangGraph is the recommended approach for agents; LangChain (with LCEL) is for simpler chains. They're complementary, not competing.

4. **Q: What are the main criticisms of LangChain?**
   A: Four: (1) heavy abstractions — multiple layers wrap simple operations, (2) frequent breaking changes between minor versions, (3) "magic" behavior in legacy `AgentExecutor` (loops, unexpected tool calls), (4) lock-in — once deeply integrated, migration is painful. These criticisms pushed many teams toward direct SDK calls or lighter frameworks (PydanticAI, LlamaIndex).

5. **Q: How would you migrate a legacy LangChain app to modern LCEL?**
   A: Step-by-step: (1) identify all `LLMChain`, `SequentialChain`, `AgentExecutor` usages, (2) replace `LLMChain` with `prompt | llm`, (3) replace `SequentialChain` with LCEL pipes, (4) replace `AgentExecutor` with LangGraph, (5) replace `ConversationBufferMemory` with LangGraph state, (6) replace `RetrievalQA` with LCEL RAG chains, (7) test thoroughly — behavior may differ slightly, (8) pin versions and add CI evals to catch regressions.

6. **Q: How does LangSmith integrate with LangChain?**
   A: LangSmith traces every LCEL chain invocation automatically (via environment variable `LANGCHAIN_TRACING_V2=true`). Each trace shows the chain's inputs, outputs, intermediate steps, token counts, latency, and errors. This makes debugging LCEL chains much easier than going without LangSmith. LangSmith also provides eval sets, prompt management, and A/B testing — useful for production LangChain apps.

## See Also

- [[03 - LangGraph]]
- [[04 - DSPy]]
- [[05 - LlamaIndex]]
- [[01 - Framework Selection Guide]]
- [[25 - Frameworks and Tools/MOC|25 Frameworks MOC]]