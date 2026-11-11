---
tags: [rag, agentic-rag, graphrag, self-rag, advanced]
iteration: 2
created: 2026-08-07
aliases: [Agentic RAG, GraphRAG, Self-RAG, Corrective RAG]
---

# 03 - Advanced RAG Patterns (Agentic, GraphRAG, Self-RAG)

> [!info] TL;DR
> Beyond basic RAG: **Agentic RAG** uses an LLM agent to decide when and what to retrieve. **GraphRAG** uses a knowledge graph for multi-hop retrieval. **Self-RAG / Corrective RAG** lets the model self-assess and re-retrieve. Higher quality, higher cost, more complexity.

## Agentic RAG

Standard RAG: retrieve once, generate. Agentic RAG: an agent decides when to retrieve, what query to use, and whether to retrieve again.

### The pattern
```
User question
   ↓
[Agent reasons: do I need to search?]
   ↓ yes
[Agent formulates search query]
   ↓
[Retrieve]
   ↓
[Agent observes results: enough info?]
   ↓ no
[Agent reformulates query, searches again]
   ↓ yes
[Agent generates answer with citations]
```

### When agentic RAG helps
- Complex questions requiring multi-hop retrieval.
- Questions where the initial query needs reformulation.
- Questions that need synthesis across multiple sources.

### When it doesn't
- Simple lookups (just do basic RAG).
- Latency-sensitive applications (each retrieve-observe cycle adds seconds).

### Implementation
Use ReAct pattern (see [[15 - AI Agents/Reasoning/03 - ReAct Pattern|ReAct]]) with retrieval as a tool. LangGraph and LlamaIndex both have agentic RAG templates.

## GraphRAG (Microsoft, 2024)

Build a **knowledge graph** from documents, then use graph traversal for retrieval.

### The pipeline
1. **Extract entities and relationships** from each document (LLM-based).
2. **Build a graph**: nodes = entities, edges = relationships.
3. **Cluster entities** into communities (e.g., Leiden algorithm).
4. **Generate community summaries** (LLM-based).
5. **Query**:
   - For specific entity queries: traverse the graph from the entity.
   - For broad queries: read community summaries.

### When GraphRAG helps
- Multi-hop questions about entities and relationships.
- "Who are the key players in X and how do they connect?"
- Questions where the answer requires synthesizing across many documents.

### When it doesn't
- Simple factual lookups (basic RAG is fine).
- Document collections without clear entity structure.
- Cost-sensitive applications (GraphRAG construction is expensive).

## Self-RAG (Asai et al. 2023)

Train the model to **self-assess** whether retrieval is needed and whether retrieved context is relevant.

### Reflection tokens
The model emits special "reflection" tokens:
- `Retrieve`: should I retrieve? (yes/no)
- `ISREL`: is the retrieved doc relevant? (yes/no)
- `ISSUP`: is the answer supported by the docs? (yes/no)
- `ISUSE`: is the answer useful? (rating)

### Training
Self-RAF fine-tunes the model on trajectories that include these reflection tokens, with rewards for correct retrieval and grounded answers.

### Inference
The model self-decides when to retrieve and self-evaluates its answers. If unsupported, it can re-retrieve and try again.

## Corrective RAG (CRAG, Yan et al. 2024)

A simpler alternative to Self-RAG:

1. Retrieve documents.
2. **Confidence assessment**: a small model scores whether the retrieved docs are relevant.
3. If high confidence: use the docs (with retrieval refinement).
4. If low confidence: **fall back to web search**.
5. Generate answer with the (corrected) context.

CRAG doesn't require fine-tuning — it's a prompting + workflow pattern.

## Worked Example (Agentic RAG with LangGraph)

```python
from langgraph.graph import StateGraph, END

class State(TypedDict):
    question: str
    retrieved: List[str]
    answer: str
    needs_more: bool

def decide_retrieve(state):
    # LLM decides if retrieval is needed
    decision = llm.generate(f"Does this question need retrieval? {state['question']}")
    if "yes" in decision.lower():
        return "retrieve"
    return "generate"

def retrieve(state):
    query = llm.generate(f"Formulate a search query for: {state['question']}")
    docs = vector_db.search(query, k=5)
    return {"retrieved": docs}

def assess(state):
    # LLM assesses if retrieved docs are sufficient
    assessment = llm.generate(f"Are these docs sufficient? {state['retrieved']}")
    return {"needs_more": "no" in assessment.lower()}

def generate(state):
    answer = llm.generate(f"Context: {state['retrieved']}\nQ: {state['question']}")
    return {"answer": answer}

graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("assess", assess)
graph.add_node("generate", generate)
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "assess")
graph.add_conditional_edges("assess", lambda s: "retrieve" if s["needs_more"] else "generate")
graph.add_edge("generate", END)
app = graph.compile()
```

## Why This Matters for AI

- These patterns represent the **frontier of RAG** in 2026. Most production RAG is still basic, but advanced patterns are increasingly adopted for high-value use cases.
- **Agentic RAG** is the bridge between RAG and full agents — many "agents" are essentially agentic RAG with tools.
- **GraphRAG** is Microsoft's bet on knowledge-graph-augmented retrieval; useful for enterprise knowledge management.
- **Self-RAG / CRAG** address the "stuck with bad retrieval" failure mode of basic RAG.

## Production Implications

- **Start with basic RAG + reranking**. Add agentic patterns only when you've exhausted simpler approaches.
- **Agentic RAG** is expensive (multiple LLM calls per query). Use for high-value queries, not high-volume.
- **GraphRAG** requires significant upfront investment (graph construction) but pays off for entity-heavy domains.
- **Self-RAG / CRAG** improve reliability at moderate cost. CRAG is the easier starting point (no fine-tuning).
- **Latency**: advanced patterns add 5–30s per query. Not suitable for real-time chat.

## Common Pitfalls

- **Jumping to advanced patterns too early** — basic RAG with good chunking + hybrid search + reranking is hard to beat.
- **No evaluation** — without measuring retrieval quality, you can't tell if agentic patterns help.
- **Cost overruns** — agentic patterns can 10x token costs. Budget per query.
- **Infinite loops** — agentic RAG can loop forever on bad queries. Always set max iterations.

## Further Reading

- Asai et al. (2023), *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*.
- Yan et al. (2024), *Corrective Retrieval Augmented Generation*.
- Edge et al. (2024), *From Local to Global: A GraphRAG Approach to Query-Focused Summarization* (Microsoft GraphRAG).

## See Also

- [[01 - RAG Pipeline Overview]]
- [[02 - Chunking Hybrid Search Reranking|Chunking, Hybrid Search, Reranking]]
- [[15 - AI Agents/Reasoning/03 - ReAct Pattern|ReAct Pattern]]
- [[15 - AI Agents/Patterns/05 - Reflection|Reflection]]
- [[17 - RAG/MOC|RAG MOC]]
