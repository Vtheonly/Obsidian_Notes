---
tags: [memory, vector-db, pgvector, pinecone, qdrant]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Vector Memory Backends, Vector Databases for Agents]
---

# 04 — Vector Memory Backends

> [!info] TL;DR
> Vector databases store embeddings for semantic search — the foundation of agent memory and RAG. The major options in 2024–2026 are **pgvector** (Postgres extension, simplest, integrated), **Pinecone** (managed SaaS, zero-ops), **Qdrant** (open-source, Rust-based, fast), **Weaviate** (open-source, GraphQL API), and **Milvus** (open-source, scales to billions). The right choice depends on scale, ops capacity, and integration needs.

## Why Vector Databases Exist

Semantic search requires comparing the meaning of text, not just keywords. This is done by embedding text into high-dimensional vectors (typically 768–3072 dimensions) and computing similarity (cosine similarity, dot product) between vectors. Vectors close in embedding space correspond to text with similar meaning.

The problem: storing and searching millions of vectors is not what relational databases are built for. Brute-force search (compute similarity to every vector) is O(N) — too slow at scale.

Vector databases use **approximate nearest neighbor (ANN)** algorithms to search in O(log N) or better. They index vectors using structures like HNSW (Hierarchical Navigable Small World), IVF (Inverted File), or PQ (Product Quantization) to trade a small amount of recall for massive speedup.

## The Major Options

### pgvector

Postgres extension that adds a `vector` type and vector indexing. You store embeddings alongside relational data in the same database.

**Strengths**:
- Integrated with Postgres — no separate database to operate.
- ACID transactions across relational and vector data.
- Mature ecosystem (any ORM that supports Postgres supports pgvector).
- Hybrid search: combine vector similarity with SQL filters (e.g., "find similar documents in tenant X created after date Y").
- Good enough performance for most use cases (millions of vectors).

**Weaknesses**:
- Not as fast as dedicated vector DBs at very large scale (100M+ vectors).
- Index rebuilds can be slow.
- Limited ANN algorithm choices (HNSW, IVFFlat).

**When to use**: most production agent memory systems, RAG with <10M vectors, any system already using Postgres.

### Pinecone

Managed SaaS vector database. You create an index, upload vectors, query by API. No infrastructure to operate.

**Strengths**:
- Zero ops — Pinecone handles scaling, replication, backups.
- Fast (low latency, high throughput).
- Serverless option (pay per query).
- Built-in metadata filtering.
- Mature, well-documented API.

**Weaknesses**:
- Closed source — vendor lock-in.
- Cost scales with usage; can be expensive at high query volumes.
- Data must leave your infrastructure (compliance concern for some industries).
- Limited control over indexing parameters.

**When to use**: teams without DBA capacity, prototypes that need to scale fast, workloads where the convenience justifies the cost.

### Qdrant

Open-source vector database written in Rust. Self-hosted or managed cloud.

**Strengths**:
- Fast (Rust, no GC pauses).
- Rich filtering (payload filtering with complex conditions).
- Supports sparse vectors (BM25-like) alongside dense — useful for hybrid search.
- Good documentation, active community.
- Self-hosted or managed.

**Weaknesses**:
- Newer than Pinecone; smaller ecosystem.
- Less mature tooling than pgvector's Postgres ecosystem.

**When to use**: teams that want open-source with strong performance, hybrid search needs, self-hosting requirements.

### Weaviate

Open-source vector database with GraphQL and REST APIs. Self-hosted or managed cloud.

**Strengths**:
- Built-in modules for common embedding models (OpenAI, Cohere, HuggingFace) — automatic embedding on insert.
- GraphQL API for complex queries.
- Hybrid search (keyword + vector) out of the box.
- Multi-tenancy support (each tenant gets isolated collections).
- Generative capabilities (built-in RAG patterns).

**Weaknesses**:
- More complex to operate than Qdrant.
- GraphQL API has a learning curve.
- Performance slightly behind Qdrant in benchmarks.

**When to use**: teams that want built-in embedding + RAG patterns, multi-tenant SaaS applications.

### Milvus

Open-source vector database designed for very large scale (billions of vectors). Self-hosted or managed cloud (Zilliz).

**Strengths**:
- Scales to billions of vectors.
- Multiple index types (HNSW, IVF, DiskANN, etc.).
- Distributed architecture (sharding, replication).
- Separation of storage and compute.

**Weaknesses**:
- Complex to operate (multiple components: proxy, query node, data node, etc.).
- Overkill for most use cases (if you have <100M vectors, Milvus is more than you need).
- Steeper learning curve.

**When to use**: very large-scale deployments (100M+ vectors), specialized vector search workloads.

## Comparison Table

| Database  | Open Source | Managed | Scale      | Hybrid Search | Multi-Tenant | Best For                          |
|-----------|-------------|---------|------------|---------------|--------------|-----------------------------------|
| pgvector  | Yes         | Many    | <100M      | Yes (SQL)     | Yes (RLS)    | Most production systems           |
| Pinecone  | No          | Yes     | Any        | Yes           | Yes          | Zero-ops teams                    |
| Qdrant    | Yes         | Yes     | <1B        | Yes (sparse)  | Yes          | Performance-focused, self-host    |
| Weaviate  | Yes         | Yes     | <1B        | Yes           | Yes          | Built-in RAG, multi-tenant SaaS   |
| Milvus    | Yes         | Zilliz  | Billions   | Yes           | Yes          | Very large scale                  |

## Indexing Algorithms

The choice of indexing algorithm affects speed, recall, and memory:

### HNSW (Hierarchical Navigable Small World)
Graph-based index. Builds a multi-layer graph where each node is a vector, and edges connect similar vectors. Search traverses the graph from a random entry point, greedily moving toward the query.

- **Speed**: very fast (sub-millisecond at moderate scale).
- **Recall**: high (>95% at typical parameters).
- **Memory**: high (the graph is in memory).
- **Build time**: slow (the graph is expensive to construct).

HNSW is the default in pgvector, Qdrant, Weaviate, and most modern vector DBs. It is the right choice for most use cases.

### IVF (Inverted File)
Partitions vectors into clusters. At search time, only the clusters closest to the query are scanned.

- **Speed**: fast.
- **Recall**: moderate (depends on how many clusters you scan).
- **Memory**: lower than HNSW.
- **Build time**: fast.

IVF is older than HNSW and mostly superseded, but still useful for very large datasets where HNSW's memory footprint is prohibitive.

### PQ (Product Quantization)
Compresses vectors by dividing them into sub-vectors and quantizing each. Reduces memory by 8–64× at the cost of some recall.

- **Speed**: very fast (compressed vectors are fast to scan).
- **Recall**: lower than HNSW/IVF.
- **Memory**: very low.

PQ is used for very large datasets where memory is the constraint. Often combined with IVF (IVF-PQ).

### DiskANN
Disk-based index. Stores vectors on disk, with a small in-memory graph for navigation. Enables searching datasets larger than RAM.

- **Speed**: slower than in-memory indexes (disk I/O).
- **Recall**: high.
- **Memory**: low (only the graph is in memory).

DiskANN is used for very large datasets that don't fit in RAM. Milvus supports it; other DBs are adding support.

## Hybrid Search

Pure vector search misses exact matches (e.g., entity names, IDs, code identifiers). Hybrid search combines:
- **Dense vector search**: semantic similarity.
- **Sparse vector / keyword search**: exact matches, BM25-style.

Most modern vector DBs support hybrid search:
- **pgvector**: combine with Postgres full-text search.
- **Qdrant**: native sparse vectors.
- **Weaviate**: built-in hybrid search.
- **Pinecone**: supported via sparse-dense hybrid.

For agent memory and RAG, hybrid search is typically better than pure vector search — it catches both semantic and lexical matches. See [[02 - Chunking Hybrid Search Reranking]].

## Multi-Tenancy

For SaaS applications, each tenant's data must be isolated:

- **Database per tenant**: strongest isolation, highest overhead.
- **Schema per tenant**: good isolation, moderate overhead (Postgres schema).
- **Collection per tenant**: vector DB native (Weaviate, Qdrant support this).
- **Row-level filtering**: weakest isolation, lowest overhead (pgvector with `WHERE tenant_id = ?`).

For most SaaS applications, row-level filtering with proper indexing (and ideally database-level row-level security) is sufficient. Stronger isolation is needed for regulated industries or when tenants genuinely cannot share infrastructure.

## Production Considerations

### Embedding Pipeline
Storing a vector requires embedding the text first. Decisions:
- **Embedding model**: OpenAI text-embedding-3-small/large, BGE, E5, GTE. The choice affects dimensionality, quality, and cost.
- **Embedding cost**: $0.02–$0.13 per 1M tokens (OpenAI). For large corpora, this adds up.
- **Embedding version**: if you change models, you must re-embed everything. Maintain a versioning scheme.
- **Async embedding**: embed in a background job (Celery, SQS) to avoid blocking writes.

### Index Maintenance
- **HNSW parameters**: `m` (graph connectivity) and `ef_construction` (build-time search depth) affect quality and build time. Tune for your dataset.
- **Index rebuilds**: as you add vectors, the index degrades. Periodic rebuilds maintain quality.
- **Vacuum**: deleted vectors leave gaps. Vacuum reclaims space.

### Replication and Backup
- **Replication**: most vector DBs support replication for high availability.
- **Backup**: snapshot the database regularly. For pgvector, this is just Postgres backup. For others, use the DB's snapshot mechanism.
- **Disaster recovery**: test restore procedures. A backup you haven't restored is not a backup.

### Monitoring
- **Query latency**: p50, p95, p99. Slow queries indicate index degradation.
- **Recall**: sample queries with known good results; check that the index returns them.
- **Index size**: track growth. Unexpected growth may indicate a write bug.
- **Throughput**: queries per second. Capacity planning.

## Common Pitfalls

### Wrong Embedding Model
Using an old or poor embedding model. The model determines the upper bound of search quality. Use a current, well-evaluated model (BGE-large, OpenAI text-embedding-3, etc.).

### No Hybrid Search
Pure vector search misses exact matches. Always combine with keyword search for production systems.

### No Metadata Filtering
Searching all vectors when you only need a subset. Always filter by tenant, time, tags. Without filtering, you search 100M vectors when you needed 10K.

### Stale Embeddings
Changing embedding models without re-embedding. Old vectors use the old embedding space; new queries use the new one — they don't match. Either re-embed everything or maintain parallel indexes during migration.

### No Recall Monitoring
Recall degrades silently as the index grows. Without monitoring, you discover it when users complain. Sample queries with known good results and alert on recall drops.

### Over-Indexing
Creating too many indexes (different embedding models, different parameters). Each index costs storage and write throughput. Pick one good index and use it.

## See Also

- [[01 - Memory Types]]
- [[02 - MemGPT and Letta]]
- [[03 - Memory Operations]]
- [[18 - Memory Systems/MOC|18 Memory MOC]]
- [[02 - Chunking Hybrid Search Reranking]] — search techniques
- [[01 - RAG Pipeline Overview]] — vector DBs in RAG
- [[09 - Foundation Models/Embedding Models/02 - Embedding Models for Retrieval|Embedding Models]]

## Modern Developments (2024–2026)

### Multi-Vector and Late-Interaction Indexes
The ColBERT pattern (see [[26 - Papers/Multimodal/40 - BLIP-2 2023]]-era multi-vector work) is now mainstream: each document is tokenized into N tokens, each token gets its own embedding, and retrieval uses **MaxSim** (sum of max similarities per query token) instead of a single dot product. Vespa, Weaviate, and a new wave of dedicated late-interaction stores (e.g., Colin, LightOn's successors) support this natively. Multi-vector indexes are 5–10x larger than single-vector but achieve 10–20% higher nDCG on retrieval benchmarks.

### Quantized Vector Indexes (PQ, SQ, Binary)
Production vector DBs now universally support:
- **Product Quantization (PQ)**: split a 1024-dim vector into 16 sub-vectors of 64 dims each; quantize each sub-vector to 8 bits via codebook. 16x compression with ~3% recall loss.
- **Scalar Quantization (SQ)**: convert fp32 → int8. 4x compression, ~1% recall loss.
- **Binary quantization**: convert to 1-bit per dim. 32x compression, ~5–10% recall loss. Combined with **re-scoring** (retrieve 10x candidates with binary, re-score top-K with full fp32), reaches 99% of full-precision recall at 1/30th the storage cost.

Qdrant's `BinaryQuantization` and pgvector's `bit` indexes (0.7+) made this mainstream for billion-scale deployments.

### Disk-Based ANN Indexes (DiskANN, SPANN)
For trillion-scale corpora that don't fit in RAM, **DiskANN** (Microsoft) and **SPANN** (Microsoft) keep the search graph on SSD and only load graph nodes on demand. Latency: 5–20ms (vs 1–5ms for in-memory HNSW), but at 1/100th the cost. Used by Bing, Apple, and major RAG platforms. The trade-off is acceptable for archival memory tiers where latency budgets are 50ms+.

### Hybrid Search Becomes the Default
Pure vector search is now considered an anti-pattern for production. The 2025 consensus is **hybrid search**: combine BM25 (lexical) + vector (semantic) with reciprocal rank fusion (RRF). Most vector DBs ship this natively (Weaviate 1.25+, Qdrant 1.8+, pgvector + tsvector). Open-source libraries like `mixedbread-ai/rerank` and `cohere-ai/rerank` add a cross-encoder reranking step that boosts precision another 5–10%.

### Serverless Vector DBs
Pinecone Serverless (2024) introduced a storage/compute separation for vector indexes — you pay for storage ($0.10/GB/month) and query compute (per-100k-queries) separately. This dropped costs 10–50x for sparse workloads. Weaviate, Qdrant Cloud, and Turbopuffer followed. For RAG systems with bursty traffic, serverless is now the default.

### Vector Indexes in Postgres (pgvector 0.7+)
pgvector added **HNSW** indexes (in addition to IVFFlat), **half-vec** (16-bit floats, 2x compression), and **binary quantization** with re-scoring. For applications already on Postgres, pgvector is now the recommended default — no need for a separate vector DB until you hit ~100M vectors or strict latency SLAs.

### Specialized Indexes for Embedding Model Migrations
The "embedding model upgrade" problem (you change embedders, all your old vectors are stale) is now solved by:
- **Multi-index serving**: keep the old index for a transition period; query both; merge results.
- **On-demand re-embedding**: lazily re-embed documents as they're accessed.
- **Adapter networks**: train a small neural net to map old embeddings → new embeddings, avoiding full re-embedding. Cohere, OpenAI, and Voyage AI all publish adapter recipes for their embedder upgrades.

## Comparison Table — Production Vector DBs (2026)

| System       | Index Type                | Hybrid Search | Multi-Vector | Serverless | Open Source | Best For                                       |
|--------------|---------------------------|---------------|--------------|------------|-------------|------------------------------------------------|
| pgvector     | HNSW, IVFFlat             | Via tsvector  | Limited      | Via cloud PG | Yes       | Apps already on Postgres; <100M vectors        |
| Pinecone     | Proprietary (graph + PQ)  | Yes           | Yes          | Yes        | No          | Managed serverless; enterprise; zero ops       |
| Qdrant       | HNSW + scalar/binary Q    | Yes           | Yes          | Via cloud  | Yes         | Self-hosted with rich filtering; cost-sensitive |
| Weaviate     | HNSW                      | Yes (BM25 + vector) | Yes     | Yes        | Yes         | Schema-first; module ecosystem (multi-modal)   |
| Milvus       | HNSW, IVF, DiskANN, SCANN | Yes           | Yes          | Via Zilliz | Yes         | Billion-scale; on-prem enterprise              |
| Vespa        | HNSW + tensor fields      | Yes           | Yes (late-int) | Via cloud | Yes       | Real-time + complex ranking + huge scale       |
| Chroma       | HNSW                      | Limited       | No           | Via cloud  | Yes         | Prototyping; small datasets                    |
| LanceDB      | IVF + PQ                  | Yes           | Yes          | Embedded   | Yes         | Embedded (no server); multimodal; lakehouse    |
| Turbopuffer  | Disk-based HNSW           | Yes           | Yes          | Yes        | No          | Cost-optimized serverless on S3                |

## Worked Example — Production Vector Memory with pgvector

```sql
-- Schema with HNSW index + hybrid search
CREATE TABLE memories (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL,
    tenant_id   UUID NOT NULL,
    content     TEXT NOT NULL,
    metadata    JSONB NOT NULL DEFAULT '{}',
    embedding   halfvec(1024) NOT NULL,  -- half-precision: 2x smaller than vector
    confidence  REAL NOT NULL DEFAULT 1.0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_accessed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    access_count INT NOT NULL DEFAULT 0,
    superseded_by UUID REFERENCES memories(id)
);

-- HNSW index for fast ANN search (half-vec + binary quantization)
CREATE INDEX ON memories USING hnsw (embedding halfvec_l2_ops)
    WITH (m = 16, ef_construction = 64);

-- GIN index for metadata filtering
CREATE INDEX ON memories USING gin (metadata);
CREATE INDEX ON memories USING btree (tenant_id, user_id, last_accessed_at DESC);

-- Full-text search index for BM25 (hybrid search)
ALTER TABLE memories ADD COLUMN tsv tsvector
    GENERATED ALWAYS AS (to_tsvector('english', content)) STORED;
CREATE INDEX ON memories USING gin (tsv);
```

```python
import asyncpg
import numpy as np

async def search_memories(
    pool, user_id: str, tenant_id: str, query: str,
    query_embedding: np.ndarray, limit: int = 10,
    metadata_filter: dict = None, time_filter_days: int = None,
) -> list[dict]:
    """Hybrid search: BM25 + vector, fused with reciprocal rank fusion."""
    async with pool.acquire() as conn:
        # Step 1: BM25 (lexical) search — top 50
        bm25_sql = """
            SELECT id, content, metadata, ts_rank(tsv, plainto_tsquery($1)) AS bm25_score
            FROM memories
            WHERE tenant_id = $2 AND user_id = $3
              AND tsv @@ plainto_tsquery($1)
              AND superseded_by IS NULL
            ORDER BY bm25_score DESC
            LIMIT 50
        """
        bm25_results = await conn.fetch(bm25_sql, query, tenant_id, user_id)

        # Step 2: Vector (semantic) search — top 50 with binary quantization + re-score
        vec_sql = """
            SELECT id, content, metadata,
                   embedding <=> $1::halfvec AS distance
            FROM memories
            WHERE tenant_id = $2 AND user_id = $3
              AND superseded_by IS NULL
              AND ($4::int IS NULL OR created_at > now() - ($4::int || ' days')::interval)
            ORDER BY embedding <=> $1::halfvec
            LIMIT 50
        """
        vec_results = await conn.fetch(
            vec_sql,
            asyncpg.Record(query_embedding.tolist()),
            tenant_id, user_id, time_filter_days,
        )

        # Step 3: Reciprocal Rank Fusion (RRF)
        rrf_k = 60  # standard constant
        scores = {}
        for rank, r in enumerate(bm25_results, start=1):
            scores[r['id']] = scores.get(r['id'], 0) + 1.0 / (rrf_k + rank)
        for rank, r in enumerate(vec_results, start=1):
            scores[r['id']] = scores.get(r['id'], 0) + 1.0 / (rrf_k + rank)

        # Step 4: Top-K by fused score
        top_ids = sorted(scores, key=scores.get, reverse=True)[:limit]
        results_by_id = {r['id']: r for r in [*bm25_results, *vec_results]}
        return [dict(results_by_id[i]) | {'fused_score': scores[i]} for i in top_ids]
```

Key production patterns visible in this example:
- **Half-precision embeddings** (`halfvec`) cut index size 2x with negligible recall loss.
- **Hybrid search via RRF** combines lexical and semantic signals without retraining.
- **Tenant isolation via WHERE clauses**; consider Row-Level Security for defense in depth.
- **Pre-filtering** by `superseded_by IS NULL` to avoid retrieving historical memories.
- **Asyncpg** for connection pooling and concurrent queries in production.

## Common Failure Modes — Diagnostic Table

| Symptom                                | Likely Cause                                  | Fix                                                          |
|----------------------------------------|-----------------------------------------------|--------------------------------------------------------------|
| Recall drops after embedder upgrade    | Old vectors in old space; new queries in new  | Multi-index serving + lazy re-embedding; or train adapter   |
| Search latency 10x higher than expected| HNSW ef_search too high; or no quantization   | Tune ef_search (start 64); enable PQ or binary quantization |
| Index build takes hours                | ef_construction too high; single-threaded     | Lower ef_construction (64→32); parallelize build            |
| OOM on bulk insert                     | Building HNSW on huge batch in RAM            | Stream inserts in batches of 10k; build index after         |
| Metadata filter ignored                | Filter applied post-retrieval, not pre-       | Use vector DB's pre-filter API (Qdrant `filter`, Weaviate `where`) |
| Empty results on exact entity match    | Pure vector search misses exact strings       | Use hybrid (BM25 + vector); add entity aliases              |
| Index size > 10x raw data              | No quantization; ef_construction too high     | Apply PQ (16x compression); tune HNSW m (16→8)              |
| Tenant A sees tenant B's memories      | Missing tenant_id in WHERE clause             | Use RLS policies; CI test for cross-tenant leaks            |
| Re-embedding the whole DB on upgrade   | No versioning on embedding model              | Track `embedder_version` column; query with right model     |
| Slow at 1B+ vectors                    | HNSW in-memory; can't fit                     | Migrate to DiskANN / SPANN; or shard by tenant               |

## Interview Questions

1. **Q: When would you choose pgvector over a dedicated vector DB like Pinecone?**
   A: Choose pgvector when (1) you're already on Postgres and want one fewer system to operate; (2) you need strong transactional consistency between relational data and vectors (e.g., memories with foreign keys to user records); (3) your corpus is <100M vectors and SLA is <50ms p99. Choose Pinecone (or Qdrant Cloud, Weaviate Cloud) when (1) you need managed serverless with zero ops; (2) you're at 1B+ vectors; (3) you need advanced features like multi-vector or late-interaction retrieval that pgvector lacks.

2. **Q: Explain HNSW vs IVF — when do you use each?**
   A: **HNSW** (Hierarchical Navigable Small World) builds a multi-layer graph; queries traverse from a sparse top layer down to a dense bottom layer. O(log n) query time, O(n log n) build time, high RAM usage (graph + vectors in memory). Best for <100M vectors with tight latency SLAs. **IVF** (Inverted File) clusters vectors into Voronoi cells via k-means; queries probe the nearest N cells. Lower RAM, lower build time, but lower recall at the same latency. Best for 100M–1B vectors or when memory is constrained. Many DBs (Milvus, pgvector) support both; use HNSW for hot tiers, IVF for warm tiers.

3. **Q: How does binary quantization with re-scoring work, and what's the trade-off?**
   A: Each fp32 component of the vector is replaced with 1 bit (sign of the component). The 1024-dim fp32 vector (4KB) becomes a 1024-bit binary vector (128B) — 32x smaller. Hamming distance on binary vectors is dramatically faster (XOR + popcount, SIMD-parallel). At query time, retrieve 10x the desired K using fast binary search, then **re-score** those candidates with full fp32 dot products. Result: 99% of full-precision recall at 30x lower storage and 5x lower latency. The trade-off is implementation complexity — you need to store both binary and full-precision vectors (or re-compute on demand).

4. **Q: How do you handle embedding model migrations in production?**
   A: Three approaches, in increasing order of complexity: (1) **Big-bang re-embedding** — take downtime, re-embed everything, swap indexes. Simple but disruptive; only works for small corpora. (2) **Dual-index serving** — keep the old index running, build a new index in parallel, query both with RRF, slowly migrate traffic to the new index. Zero downtime, 2x query cost during migration. (3) **Adapter network** — train a small MLP that maps old embeddings → new embeddings. Apply adapter at query time (transform new query to old space) or at index time (transform old vectors to new space). Cheapest, but requires training data (pairs of old+new embeddings on the same text).

5. **Q: What's reciprocal rank fusion (RRF) and why is it the standard for hybrid search?**
   A: RRF combines ranked result lists from multiple retrievers (e.g., BM25 + vector) using the formula `score(d) = sum over retrievers of 1 / (k + rank_retriever(d))` where `k ≈ 60`. RRF has three properties that make it the default: (1) it doesn't require score calibration across retrievers (BM25 scores and cosine similarities aren't comparable); (2) it's robust to outliers (a single retriever's high score can't dominate); (3) it's parameter-light (only `k` to tune). Most vector DBs ship RRF natively; it consistently beats single-retriever baselines by 5–15% on nDCG.

6. **Q: How would you design a multi-tenant vector memory system with strict isolation?**
   A: Four layers of isolation: (1) **Logical** — every row has `tenant_id`; all queries filter on it; CI tests for cross-tenant leakage. (2) **Schema** — separate schemas per tenant (Postgres) or separate collections (Qdrant) for high-value tenants. (3) **Physical** — separate databases/clusters for the largest tenants; shared cluster for small ones. (4) **Crypto** — encrypt memory at rest with per-tenant keys (envelope encryption via AWS KMS); keys never co-located with data. Combine with RLS policies (defense in depth), audit logging of every query, and quarterly penetration tests for cross-tenant access.

## Connection to Other Concepts

- [[18 - Memory Systems/Types/01 - Memory Types]] — what gets stored in vector memory.
- [[18 - Memory Systems/Architectures/02 - MemGPT and Letta]] — uses vector DBs as the archival memory backend.
- [[18 - Memory Systems/Operations/03 - Memory Operations]] — write/read/decay/forget map to vector DB CRUD.
- [[17 - RAG/Ingestion and Retrieval/02 - Chunking Hybrid Search Reranking]] — same hybrid search techniques.
- [[17 - RAG/MOC]] — RAG pipelines use vector DBs for retrieval.
- [[20 - AI Infrastructure/Storage/02 - Vector Storage with pgvector]] — pgvector deep dive.
- [[09 - Foundation Models/Embedding Models/02 - Embedding Models for Retrieval]] — embedding model selection drives index design.
- [[09 - Foundation Models/Embedding Models/06 - Embedding Model Training]] — embedding model upgrades trigger re-indexing.
- [[22 - Production AI/Security/05 - PII and Data Leakage]] — PII in memory must be encrypted and filtered.
- [[13 - Inference/Quantization/03 - Quantization]] — PQ/SQ/binary quantization share theory with model quantization.
- [[25 - Frameworks and Tools/MOC]] — most vector DBs are listed as frameworks.
