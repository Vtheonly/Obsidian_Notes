---
tags: [infrastructure, postgres, pgvector, vector-storage]
iteration: 3
created: 2026-08-07
aliases: [pgvector Deep Dive, PostgreSQL for AI, Vector Storage with pgvector]
---

# 02 — Vector Storage with pgvector

> [!info] TL;DR
> pgvector is a Postgres extension that adds a `vector` type and ANN indexing (HNSW, IVFFlat). For most AI applications — agent memory, RAG, semantic search — pgvector is the right default: it stores vectors alongside relational data, supports ACID transactions, and uses SQL for hybrid search. It scales comfortably to ~100M vectors per index, beyond which dedicated vector DBs become preferable.

## Why pgvector

The traditional split between relational data and vector data created friction:
- User profiles, document metadata, and audit logs live in Postgres.
- Embeddings for semantic search lived in a separate vector DB (Pinecone, Qdrant).
- Joining the two required application-level coordination, fragile sync, and dual-write consistency issues.

pgvector eliminates this split. Vectors live in the same Postgres tables as the rest of your data. You can:
- Join vectors with relational data in a single query.
- Use ACID transactions across both.
- Use Postgres's mature ecosystem (ORMs, backups, replication, monitoring).

For most production AI workloads, pgvector is the right default. It is not the fastest at extreme scale, but it is the simplest to operate and the most flexible.

## Setup

```sql
-- Install the extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table with a vector column
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL,  -- OpenAI text-embedding-3-small dimension
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

-- Create an HNSW index for fast ANN search
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Create a B-tree index for tenant filtering
CREATE INDEX ON documents (tenant_id, created_at);
```

The `vector_cosine_ops` operator class specifies cosine similarity. Other options: `vector_l2_ops` (Euclidean), `vector_ip_ops` (inner product).

## Queries

### Semantic Search
```sql
-- Find the 10 most similar documents to a query embedding
SELECT id, title, content, 1 - (embedding <=> $1) AS similarity
FROM documents
ORDER BY embedding <=> $1
LIMIT 10;
```

The `<=>` operator is cosine distance. `<->` is L2 distance. `<#>` is negative inner product.

### Hybrid Search (Vector + Metadata Filter)
```sql
-- Find similar documents, filtered by tenant and date
SELECT id, title, content, 1 - (embedding <=> $1) AS similarity
FROM documents
WHERE tenant_id = $2
  AND created_at > NOW() - INTERVAL '30 days'
ORDER BY embedding <=> $1
LIMIT 10;
```

Postgres's query planner combines the HNSW index (vector search) with the B-tree index (metadata filter) efficiently. This is one of pgvector's biggest advantages — hybrid search is just SQL.

### Hybrid Search (Vector + Full-Text)
```sql
-- Combine vector similarity with keyword search
WITH vector_results AS (
    SELECT id, 1 - (embedding <=> $1) AS vector_score
    FROM documents
    ORDER BY embedding <=> $1
    LIMIT 100
),
keyword_results AS (
    SELECT id, ts_rank_cd(search_vector, query) AS keyword_score
    FROM documents, plainto_tsquery('english', $2) query
    WHERE search_vector @@ query
    LIMIT 100
)
SELECT d.id, d.title, d.content,
       (vr.vector_score * 0.7 + COALESCE(kr.keyword_score, 0) * 0.3) AS combined_score
FROM documents d
LEFT JOIN vector_results vr ON d.id = vr.id
LEFT JOIN keyword_results kr ON d.id = kr.id
WHERE vr.id IS NOT NULL OR kr.id IS NOT NULL
ORDER BY combined_score DESC
LIMIT 10;
```

This is the "reciprocal rank fusion" or weighted-score approach to hybrid search. It combines semantic (vector) and lexical (full-text) signals for better recall than either alone.

## Indexing Choices

### HNSW (Recommended Default)
- Builds a graph where each node is a vector; edges connect similar vectors.
- Search traverses the graph greedily from a random entry point.
- Parameters:
  - `m` (default 16): graph connectivity. Higher = better recall, more memory.
  - `ef_construction` (default 64): build-time search depth. Higher = better recall, slower build.
- Query parameter: `ef_search` (set per query, default 40). Higher = better recall, slower query.

HNSW is the right choice for most workloads. It gives >95% recall at sub-millisecond latency for moderate-scale datasets.

### IVFFlat
- Partitions vectors into clusters; search scans only the closest clusters.
- Parameters:
  - `lists`: number of clusters. Rule of thumb: `sqrt(rows)`.
  - `probes`: clusters to scan per query. Higher = better recall, slower query.
- Faster to build than HNSW, but lower recall at the same latency.

Use IVFFlat only if HNSW build time or memory is prohibitive.

### When to Use No Index
For very small tables (<10K rows), a sequential scan with vector distance computation is faster than index traversal. Skip the index until you have enough data to justify it.

## Performance Considerations

### Index Build Time
HNSW builds are expensive. For 1M vectors of 1536 dimensions, expect:
- Build time: 5–30 minutes depending on hardware and parameters.
- Memory during build: 2–4 GB.

For large datasets, build the index on a replica or during a maintenance window.

### Memory Usage
HNSW indexes are in-memory. A 1536-dimension vector is 6 KB (float4). For 1M vectors:
- Raw vectors: 6 GB.
- HNSW graph overhead: ~30% on top, so ~8 GB.

Postgres's shared buffers must be large enough to hold the index for good performance. If the index spills to disk, latency explodes.

### Query Latency
Typical latency on commodity hardware (8 vCPU, 32 GB RAM):
- 10K vectors: <1 ms.
- 100K vectors: 1–5 ms.
- 1M vectors: 5–20 ms.
- 10M vectors: 20–100 ms (consider dedicated vector DB).

### Throughput
A single Postgres instance handles ~100–1000 queries per second on vector search, depending on index size and hardware. For higher throughput, use read replicas or a dedicated vector DB.

## Operational Patterns

### Embedding Pipeline
Store embeddings alongside the data they describe, but compute them asynchronously:

```python
# On insert, just store the text
INSERT INTO documents (title, content) VALUES (?, ?) RETURNING id;

# Async job computes and updates the embedding
async def embed_document(doc_id):
    doc = await get_document(doc_id)
    embedding = await openai.embeddings.create(input=doc.content, model="text-embedding-3-small")
    await db.execute("UPDATE documents SET embedding = $1 WHERE id = $2", embedding, doc_id)
```

This decouples insert latency from embedding cost. Use Celery, SQS, or a similar queue.

### Embedding Versioning
When you change embedding models, old embeddings are invalid (they live in a different vector space). Track the embedding version:

```sql
ALTER TABLE documents ADD COLUMN embedding_model TEXT;
ALTER TABLE documents ADD COLUMN embedding_version INT;

-- During migration, re-embed documents with the new model
UPDATE documents SET embedding = $1, embedding_version = 2 WHERE id = $2;
```

Filter by version in queries to avoid mixing old and new embeddings.

### Tenant Isolation
For multi-tenant SaaS, use Postgres row-level security:

```sql
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON documents
    USING (tenant_id = current_setting('app.tenant_id')::BIGINT);
```

Each request sets `app.tenant_id` at the start of the transaction. Postgres automatically filters all queries. This is stronger isolation than application-level filtering (which is bug-prone).

### Backup and Recovery
pgvector data is just Postgres data. Standard Postgres backup tools (`pg_dump`, `pg_basebackup`, WAL archiving, point-in-time recovery) work without modification. This is a significant advantage over dedicated vector DBs, which require their own backup tooling.

### Monitoring
- **Index size**: track growth; unexpected growth may indicate a write bug.
- **Query latency**: p50, p95, p99. Slow queries indicate index degradation or insufficient memory.
- **Cache hit ratio**: `pg_stat_user_indexes`. Low ratio suggests the index doesn't fit in memory.
- **Recall**: sample queries with known-good results; alert on recall drops.

## Common Pitfalls

### Wrong Distance Metric
Using cosine distance when you stored L2-normalized vectors (or vice versa). Pick one and be consistent. For most text embeddings, cosine distance is the right choice.

### No Tenant Filter
Searching all tenants' vectors when you only need one. Always filter by `tenant_id` in the WHERE clause — Postgres will use the B-tree index to prune before the HNSW search.

### Stale Embeddings
Changed embedding models without re-embedding. Old vectors don't match new queries. Track embedding version; re-embed during migration.

### Index Not in Memory
HNSW index spilled to disk due to small `shared_buffers`. Latency explodes. Size `shared_buffers` to fit the index, or use a dedicated vector DB.

### No Hybrid Search
Pure vector search misses exact matches (entity names, IDs, code identifiers). Always combine with full-text or keyword search.

### Wrong Dimensionality
Storing 768-dimensional vectors in a `VECTOR(1536)` column (or vice versa). The vector type enforces dimensionality at insert — make sure it matches your embedding model.

## When to Choose a Dedicated Vector DB

pgvector is the right default, but switch to a dedicated vector DB (Qdrant, Milvus, Pinecone) when:
- You have >100M vectors and HNSW memory becomes prohibitive.
- You need sub-millisecond latency at very high QPS (>10K).
- You need specialized indexes (DiskANN, PQ) that pgvector doesn't support.
- You need to scale vector search independently of your relational database.

For most applications, this threshold is far away. Start with pgvector; migrate only when you hit a real limit.

## See Also

- [[01 - Production AI Stack]]
- [[04 - Vector Memory Backends]]
- [[03 - Memory Operations]]
- [[01 - RAG Pipeline Overview]]
- [[02 - Chunking Hybrid Search Reranking]]
- [[20 - AI Infrastructure/MOC|20 AI Infrastructure MOC]]
