---
tags: [moc, memory, agent-memory, vector-db]
iteration: 3
created: 2026-08-07
---

# 18 — Memory Systems MOC

> [!info] Agent memory systems give LLMs persistent context across turns and conversations. Iteration 3 expanded this chapter with notes on MemGPT/Letta, memory operations (write, read, consolidate, decay, forget), and vector memory backends.

## Reading Order

| #   | Note                                              | Sub-domain      | Purpose                                            |
|-----|---------------------------------------------------|-----------------|----------------------------------------------------|
| 01  | [[01 - Memory Types]]                             | Types           | Working, episodic, semantic, procedural.           |
| 02  | [[02 - MemGPT and Letta]]                         | Architectures   | OS-inspired memory hierarchy for agents.           |
| 03  | [[03 - Memory Operations]]                        | Operations      | Write, read, consolidate, decay, forget.           |
| 04  | [[04 - Vector Memory Backends]]                   | Vector Memory   | pgvector, Pinecone, Qdrant, Weaviate, Milvus.      |

## Sub-Domains

- [[18 - Memory Systems/Types/01 - Memory Types|Types]] — note 01
- [[18 - Memory Systems/Architectures/02 - MemGPT and Letta|Architectures]] — note 02
- [[18 - Memory Systems/Operations/03 - Memory Operations|Operations]] — note 03
- [[18 - Memory Systems/Vector Memory/04 - Vector Memory Backends|Vector Memory]] — note 04

## Why This Matters for AI

- Without persistent memory, every conversation starts from scratch — agents cannot learn user preferences, recall past interactions, or maintain state.
- The OS-inspired memory hierarchy (MemGPT) is the most influential long-term-memory architecture for agents.
- Memory operations (consolidation, decay, forgetting) are as important as storage — without them, memory grows unboundedly and quality degrades.
- Vector databases are the storage layer; the choice of DB affects scale, ops cost, and search quality.

## Production Implications

- **Start with pgvector**: integrated, simple, sufficient for most use cases.
- **Implement decay and consolidation from day one**: retrofitting is painful.
- **Multi-tenant isolation is mandatory**: never let tenant A's memories leak to tenant B.
- **Memory is an active system, not a passive store**: budget engineering effort for the operations layer, not just storage.

## See Also

- [[15 - AI Agents/MOC|15 AI Agents]]
- [[17 - RAG/MOC|17 RAG]] — retrieval is the read operation of memory
- [[19 - MCP/MOC|19 MCP]] — agents use MCP to access memory servers
- [[25 - Frameworks and Tools/MOC|25 Frameworks]]
