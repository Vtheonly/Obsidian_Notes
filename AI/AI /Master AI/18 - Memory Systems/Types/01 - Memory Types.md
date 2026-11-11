---
tags: [memory, types, working, episodic, semantic, procedural, cognitive-science]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Memory Types, Agent Memory, Working Memory, Episodic Memory, Semantic Memory, Procedural Memory]
---

# 01 - Memory Types (Working, Episodic, Semantic, Procedural)

> [!info] TL;DR
> Agents need different memory types: **working** (current context), **episodic** (past events), **semantic** (facts), **procedural** (skills). Borrowed from cognitive science. Each requires different storage and retrieval. This note covers the four types, their properties, memory operations (write, read, consolidate, forget), architectures, comparison of frameworks, production patterns, and a worked example.

## The Four Memory Types

The taxonomy comes from cognitive science (Tulving, 1972; Atkinson & Shiffrin, 1968). AI agent memory systems borrow this framework because it maps cleanly onto the different storage and retrieval needs of agents.

### Working Memory (Short-Term)

The current context — the prompt, recent conversation, current task state. Lives in the LLM's context window.

- **Storage**: the context window itself.
- **Capacity**: limited (4k–2M tokens depending on model).
- **Lifetime**: a single conversation / task.
- **Cost**: high (every token in context costs compute per forward pass).
- **Retrieval**: implicit — it's already in context.
- **Analogy**: human short-term memory; what you're actively thinking about right now.

Examples:
- The current user message.
- The last few turns of conversation.
- The current task description.
- Retrieved context (RAG results, retrieved memories).

Working memory is what the LLM "sees" when generating a response. Everything else must be retrieved into working memory to be used.

### Episodic Memory

A log of past events: "at time T, the user said X and I responded Y."

- **Storage**: vector database, time-series log.
- **Capacity**: unbounded (grows over time).
- **Lifetime**: long-term (persist across sessions).
- **Retrieval**: by temporal recency or by similarity to current context.
- **Analogy**: human episodic memory; your memory of specific events.

Example: "Last week, the user asked about their account balance. I retrieved the balance from the database and reported $1,234."

Episodic memory is essential for:
- **Personalization**: remembering what the user asked before.
- **Continuity**: resuming a conversation across sessions.
- **Learning from past interactions**: avoiding repeated mistakes.

Episodic memories are typically stored as (timestamp, summary, embedding, metadata). The summary is important — raw transcripts are too long to be useful; a 1-2 sentence summary captures the gist.

### Semantic Memory

Facts about the world: "the user's name is Alice," "Alice's company is Acme."

- **Storage**: knowledge graph, structured database, vector DB.
- **Capacity**: unbounded.
- **Lifetime**: long-term.
- **Retrieval**: by entity, by relation, by similarity.
- **Analogy**: human semantic memory; your knowledge of facts.

Example: "Alice works at Acme; Acme is in Boston; Alice's role is Senior Engineer."

Semantic memory is essential for:
- **User profile**: name, preferences, role, organization.
- **Domain knowledge**: facts about the user's domain.
- **Relationships**: connections between entities.

Semantic memories are often extracted from episodic memories via consolidation (see below). 100 episodic memories about Alice's interactions might consolidate into 5 semantic facts about Alice.

### Procedural Memory

Skills and procedures: "how to write Python," "how to use this API."

- **Storage**: prompts, code snippets, tool definitions.
- **Capacity**: typically small (curated).
- **Lifetime**: long-term; updated as the agent learns.
- **Retrieval**: by task type.
- **Analogy**: human procedural memory; your knowledge of how to do things (riding a bike, typing).

Example: "When the user asks for code, use this template. When the user asks for a summary, use this prompt structure."

Procedural memory is essential for:
- **System prompts**: the agent's core instructions.
- **Tool definitions**: what tools are available and how to use them.
- **Workflows**: step-by-step procedures for common tasks.
- **Few-shot examples**: examples of how to handle specific situations.

Procedural memory is often the most curated type — it's not auto-extracted from conversations but explicitly written by the developer or learned via fine-tuning.

### Comparison Table

| Type        | Storage         | Capacity | Lifetime    | Retrieval              | Cost |
|-------------|-----------------|----------|-------------|------------------------|------|
| Working     | Context window  | Limited  | Per-session | Implicit (in context)  | High |
| Episodic    | Vector DB, log  | Unbounded| Long-term   | Recency or similarity  | Med  |
| Semantic    | KG, DB, vector  | Unbounded| Long-term   | Entity, relation, sim  | Med  |
| Procedural  | Prompts, code   | Small    | Long-term   | Task type              | Low  |

## Long-Term vs Short-Term

A simpler two-way classification:
- **Short-term** = working memory (context window).
- **Long-term** = episodic + semantic + procedural.

Most agent frameworks (MemGPT, Letta, Mem0) focus on long-term memory management — how to store, retrieve, and update memories across sessions.

### The Memory Hierarchy

In human cognition (and AI agents), memory forms a hierarchy:

```
Sensory input (raw observations)
       ↓
Working memory (active processing, ~7 items for humans, ~K tokens for LLMs)
       ↓
Episodic memory (specific events, time-stamped)
       ↓
Semantic memory (consolidated facts, decontextualized)
       ↓
Procedural memory (skills, automated procedures)
```

Information flows downward through consolidation. Raw experiences become episodic memories, which consolidate into semantic facts, which (with practice) become procedural skills. This is how humans learn, and it's a useful model for agents.

## Memory Operations

Regardless of type, memory systems implement four core operations:

### Write (encode)

Convert an experience into a memory representation.

- **Episodic**: timestamp + summary + embedding. The summary is critical — raw transcripts are too verbose.
- **Semantic**: extract entities and relations. Use an LLM to extract ("Alice works at Acme" → entity: Alice, relation: works_at, entity: Acme).
- **Procedural**: extract the prompt/template/workflow. Often manual, sometimes learned.

```python
def write_episodic(event, agent_response, user_id):
    summary = llm.summarize(f"User: {event}\nAgent: {agent_response}")
    embedding = embedder.encode(summary)
    memory = {
        "user_id": user_id,
        "summary": summary,
        "embedding": embedding,
        "timestamp": time.time(),
        "raw_event": event,  # optional, for debugging
    }
    vector_db.add(memory)
```

### Read (retrieve)

Find relevant memories given the current context. Methods:

- **Recency**: most recent N memories. Fast, simple, good for "what did we just talk about?"
- **Similarity**: top-k by embedding cosine. Good for "what's relevant to the current query?"
- **Relevance**: BM25 + vector hybrid (like RAG). Better than either alone.
- **Graph traversal**: for semantic memory, traverse the knowledge graph from current entities.
- **Multi-step**: retrieve episodic, then use it to find related semantic memories.

```python
def retrieve(query, user_id, k=5):
    q_emb = embedder.encode(query)
    # Filter by user_id (multi-tenancy)
    # Hybrid: vector + BM25
    vector_results = vector_db.search(q_emb, filter={"user_id": user_id}, k=k*2)
    bm25_results = bm25_index.search(query, filter={"user_id": user_id}, k=k*2)
    # Merge with reciprocal rank fusion
    merged = reciprocal_rank_fusion(vector_results, bm25_results)
    return merged[:k]
```

### Consolidate

Periodically merge, summarize, or compress memories. Important for managing memory growth.

Example: 100 episodic memories about user preferences → consolidate into 5 semantic facts ("user prefers brief answers", "user works in finance", etc.).

Consolidation patterns:
- **Clustering**: group similar memories, summarize each cluster.
- **Entity extraction**: extract entities and relations, store in semantic memory.
- **Temporal summarization**: summarize memories by time period (daily, weekly).
- **Importance filtering**: keep important memories, archive unimportant ones.

```python
def consolidate(user_id):
    # Get all episodic memories for user
    memories = vector_db.list(filter={"user_id": user_id, "type": "episodic"})
    
    # Cluster by similarity
    clusters = cluster_memories(memories, threshold=0.7)
    
    # Summarize each cluster into a semantic fact
    for cluster in clusters:
        summary = llm.summarize_cluster(cluster)
        # Store as semantic memory
        semantic_memory = {
            "user_id": user_id,
            "type": "semantic",
            "content": summary,
            "source_memories": [m["id"] for m in cluster],
        }
        semantic_db.add(semantic_memory)
        
        # Optionally: archive or delete the source episodic memories
```

### Forget (decay)

Remove or downweight old / unused memories. Without decay, memory grows unbounded and retrieval quality degrades (the "noise" overwhelms the signal).

Methods:
- **Time-based**: memories older than N days → archive or delete. Good for ephemeral data.
- **Importance-based**: low-importance memories → delete. Importance can be LLM-judged or user-flagged.
- **Access-based**: memories never retrieved → delete. Frees space for actively-used memories.
- **Conflict-based**: if a newer memory contradicts an older one, update or delete the older. Essential for keeping semantic memory current.
- **Capacity-based**: when memory exceeds N entries, evict least-recently-used.

```python
def decay(user_id, max_age_days=90, max_memories=10000):
    # Delete memories older than max_age_days (unless flagged important)
    cutoff = time.time() - max_age_days * 86400
    vector_db.delete_where({
        "user_id": user_id,
        "timestamp": {"$lt": cutoff},
        "important": False,
    })
    
    # If still over limit, evict least-recently-accessed
    count = vector_db.count(filter={"user_id": user_id})
    if count > max_memories:
        to_evict = count - max_memories
        vector_db.delete_lru(user_id, to_evict)
```

## Memory Architectures

### MemGPT / Letta

Treats memory like an OS manages virtual memory:
- **Main context** (in-context): the current working set.
- **External context** (vector DB): archival memory.
- The agent can page memories in/out of context.

MemGPT gives the agent explicit "memory management" tools: `search_memory`, `page_in`, `page_out`. The agent decides when to retrieve and when to forget. This is more flexible than automatic retrieval but adds complexity.

See [[02 - MemGPT and Letta]] for details.

### Mem0

A memory layer for agents:
- Stores user-specific, session-specific, and global memories.
- Automatic extraction from conversations.
- Retrieval via vector search.

Mem0 focuses on simplicity: drop it into an existing agent, and it handles memory automatically. Less flexible than MemGPT but easier to use.

### LangGraph Long-Term Memory

LangGraph has built-in long-term memory stores, with namespace-based organization. Memory is keyed by (namespace, key) and can be any JSON-serializable value. retrieval is by exact key or by vector similarity.

Integration with LangGraph's checkpointing makes it natural for long-running agents that need to persist state across sessions.

### Vector DBs (generic)

For simple use cases, just use a vector DB directly. Embed memories, retrieve by similarity. No framework needed — just `embed → store → search`.

This works for episodic memory but doesn't handle semantic memory (no entity/relation structure) or procedural memory (no skill organization). For more sophisticated needs, use a framework.

### Knowledge Graphs (for semantic memory)

For semantic memory, a knowledge graph (Neo4j, GraphRAG) is often the right storage. Entities are nodes, relations are edges. Retrieval is graph traversal.

Example: query "What do we know about Alice?" → traverse from Alice node → find all connected entities and relations.

KGs are more structured than vector DBs but harder to build and maintain. Use them when relationships matter more than similarity.

## Worked Example: A Multi-Type Memory System

```python
import time
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Memory:
    id: str
    content: str
    type: str  # 'episodic', 'semantic', 'procedural'
    embedding: list[float]
    timestamp: float
    user_id: str
    importance: float = 0.5
    metadata: dict = field(default_factory=dict)

class AgentMemory:
    def __init__(self, embedder, vector_store, llm):
        self.embedder = embedder
        self.store = vector_store
        self.llm = llm  # for consolidation, extraction
    
    def write_episodic(self, user_id, event, response):
        """Record an interaction."""
        summary = self.llm.summarize(f"User: {event}\nAgent: {response}")
        embedding = self.embedder.encode(summary)
        memory = Memory(
            id=generate_id(),
            content=summary,
            type="episodic",
            embedding=embedding,
            timestamp=time.time(),
            user_id=user_id,
            importance=self._judge_importance(summary),
        )
        self.store.add(memory)
        return memory
    
    def write_semantic(self, user_id, fact, source_memory_ids=None):
        """Record a fact (typically from consolidation)."""
        embedding = self.embedder.encode(fact)
        memory = Memory(
            id=generate_id(),
            content=fact,
            type="semantic",
            embedding=embedding,
            timestamp=time.time(),
            user_id=user_id,
            importance=0.8,  # semantic memories are typically important
            metadata={"source_memories": source_memory_ids or []},
        )
        self.store.add(memory)
        return memory
    
    def write_procedural(self, task_type, prompt_template, tool_definitions):
        """Record a skill/procedure (typically manual)."""
        content = f"Task: {task_type}\nPrompt: {prompt_template}\nTools: {tool_definitions}"
        embedding = self.embedder.encode(content)
        memory = Memory(
            id=generate_id(),
            content=content,
            type="procedural",
            embedding=embedding,
            timestamp=time.time(),
            user_id="global",  # procedural memory is often global
            importance=1.0,
            metadata={"task_type": task_type},
        )
        self.store.add(memory)
        return memory
    
    def retrieve(self, query, user_id, k=5, memory_types=None):
        """Retrieve relevant memories."""
        q_emb = self.embedder.encode(query)
        filter = {"user_id": {"$in": [user_id, "global"]}}
        if memory_types:
            filter["type"] = {"$in": memory_types}
        results = self.store.search(q_emb, filter=filter, k=k)
        # Boost by recency and importance
        for r in results:
            r.score *= self._recency_boost(r.timestamp)
            r.score *= r.importance
        return sorted(results, key=lambda r: r.score, reverse=True)[:k]
    
    def consolidate(self, user_id):
        """Periodically consolidate episodic → semantic."""
        episodic = self.store.list(filter={"user_id": user_id, "type": "episodic"})
        clusters = self._cluster(episodic, threshold=0.75)
        for cluster in clusters:
            if len(cluster) < 3:
                continue  # don't consolidate tiny clusters
            fact = self.llm.extract_fact([m.content for m in cluster])
            source_ids = [m.id for m in cluster]
            self.write_semantic(user_id, fact, source_ids)
            # Mark source memories as consolidated (don't delete; keep for audit)
            for m in cluster:
                m.metadata["consolidated"] = True
                self.store.update(m)
    
    def decay(self, user_id, max_age_days=90):
        """Forget old, unimportant memories."""
        cutoff = time.time() - max_age_days * 86400
        self.store.delete_where({
            "user_id": user_id,
            "timestamp": {"$lt": cutoff},
            "importance": {"$lt": 0.7},
            "metadata.consolidated": False,  # keep unconsolidated for audit
        })
    
    def _judge_importance(self, content):
        """Use LLM to judge importance (0-1)."""
        return self.llm.judge_importance(content)
    
    def _recency_boost(self, timestamp):
        """More recent = higher boost."""
        age_days = (time.time() - timestamp) / 86400
        return max(0.5, 1.0 - age_days * 0.01)  # decay over 100 days
```

## Why This Matters for AI

- Memory is **the** differentiator between one-shot chat and persistent agents. Without memory, every conversation starts from scratch.
- For agents that operate over days/weeks (autonomous research, persistent assistants), memory is essential.
- The cognitive-science framework (working/episodic/semantic/procedural) gives a useful vocabulary for designing memory systems.
- Different memory types serve different purposes; conflating them produces poor systems.
- Memory is a key differentiator between LLM applications and true agents.

## Production Implications

- **Start simple**: a vector DB storing conversation summaries is enough for most use cases. Don't build a full MemGPT-style system on day one.
- **For multi-user systems**, namespace memories per user — never mix. This is a critical security and privacy concern.
- **Memory is private data** — apply PII redaction, access control, retention policies. Memories often contain personal information.
- **Memory retrieval is a latency cost** — for real-time chat, retrieve in parallel with other work. Cache common queries.
- **Memory can grow unbounded** — implement decay or you'll run out of storage. Set retention policies.
- **Consolidation is essential** — without it, episodic memory grows without producing semantic knowledge.
- **Memory quality matters more than quantity** — 100 well-curated memories beat 10,000 noisy ones.
- **Test memory retrieval** — build an eval set of (query, expected memory) pairs. Memory systems drift over time.
- **Audit memory access** — log who accessed what memory when. Important for compliance and debugging.
- **Backup memory** — memories are valuable data. Back up regularly.

## Common Pitfalls

- **Storing everything** — most events aren't worth remembering. Filter at write time. Use LLM-based importance judging.
- **No decay** — memory grows, retrieval quality degrades, costs grow. Implement decay from day one.
- **No consolidation** — episodic memory should become semantic memory over time; otherwise you have 1000s of similar memories.
- **Mixing users** — easy to leak data across users. Always namespace by user_id.
- **Forgetting to redact PII** — memories often contain personal data; redact before storing. Especially important for regulated industries.
- **Treating all memories equally** — episodic, semantic, and procedural have different lifecycles. Don't manage them with one strategy.
- **Storing raw transcripts** — too verbose. Always summarize before storing.
- **No evaluation** — without measuring retrieval quality, you can't tell if memory is helping or hurting. Build eval sets.
- **Forgetting memory in context management** — retrieved memories go into working memory (the context window). Budget for them.
- **Ignoring memory conflicts** — when a fact changes ("Alice moved to Acme"), update the semantic memory. Don't leave stale facts.
- **No user control** — users should be able to view, edit, and delete their memories. Required by GDPR and similar regulations.

## Comparison of Memory Frameworks

| Framework | Memory Types | Storage | Retrieval | Key Feature |
|-----------|-------------|---------|-----------|-------------|
| MemGPT/Letta | Working + episodic + archival | Vector DB | Agent-controlled | "OS-like" memory management |
| Mem0 | Episodic + semantic | Vector DB | Automatic | Drop-in simplicity |
| LangGraph | All types (generic) | Pluggable | Configurable | Integration with graph state |
| Zep | Episodic + semantic | Vector DB + KG | Hybrid | Time-aware retrieval |
| Custom | Any | Any | Any | Full control |

Choose based on your needs:
- **Simple chat memory**: Mem0 or a vector DB.
- **Complex agent with memory management**: MemGPT/Letta.
- **LangGraph-based agent**: LangGraph long-term memory.
- **Relationship-heavy**: Zep or a knowledge graph.

## Future Directions

- **Memory-augmented LMs**: architectures that natively support memory (Mamba, Titans).
- **Continual learning**: agents that learn from memory without forgetting.
- **Memory compression**: better summarization and consolidation techniques.
- **Cross-agent memory**: shared memory pools for multi-agent systems.
- **Privacy-preserving memory**: federated memory, differential privacy.
- **Memory evaluation benchmarks**: standardized tests for agent memory.

## Interview Questions

- **Q: What are the four types of memory in agent systems?**  
  A: Working (current context), episodic (past events), semantic (facts), procedural (skills). Borrowed from cognitive science.

- **Q: Why consolidate episodic memory into semantic memory?**  
  A: To reduce memory volume, extract general knowledge from specific events, and improve retrieval quality. 100 episodic memories about Alice's interactions consolidate into 5 semantic facts about Alice.

- **Q: How would you implement memory decay?**  
  A: Combine time-based (delete old), importance-based (delete unimportant), access-based (delete unretrieved), and conflict-based (delete superseded) strategies. Always keep important memories regardless of age.

- **Q: Why namespace memories by user?**  
  A: To prevent data leakage between users. Without namespacing, one user's query could retrieve another user's memories — a critical privacy and security bug.

- **Q: How does MemGPT differ from a simple vector DB?**  
  A: MemGPT gives the agent explicit memory management tools (search, page_in, page_out). The agent decides when to retrieve and forget. A simple vector DB does automatic retrieval. MemGPT is more flexible but more complex.

## Further Reading

- Packer et al. (2023), *MemGPT: Towards LLMs as Operating Systems*.
- Tulving (1972), *Episodic and Semantic Memory* (cognitive science origin).
- Atkinson & Shiffrin (1968), *Human Memory: A Proposed System*.
- LangGraph memory docs.
- Mem0 documentation.
- Zep documentation.

## See Also

- [[02 - MemGPT and Letta]] — detailed MemGPT architecture
- [[03 - Memory Operations]] — write, read, consolidate, forget in depth
- [[04 - Vector Memory Backends]] — vector DB options
- [[17 - RAG/MOC|17 RAG]] — memory and RAG overlap heavily
- [[18 - Memory Systems/MOC|Memory Systems MOC]]
- [[15 - AI Agents/MOC|15 AI Agents]]
- [[08 - Autonomous Agent Lifecycles]] — memory in long-running agents
