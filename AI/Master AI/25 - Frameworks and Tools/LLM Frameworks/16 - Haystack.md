---
tags: [framework, haystack, rag, deepset, pipelines, search]
iteration: 10
created: 2026-08-08
aliases: [Haystack, deepset Haystack, Haystack 2.x]
---

# 16 — Haystack

> [!info] TL;DR
> Haystack is deepset's open-source framework for building production **search and RAG** systems. Its distinctive feature is a **pipeline-as-DAG** architecture: every system is a directed acyclic graph of typed components, validated at construction time. Compared to LangChain (which favors stringly-typed chains) and LlamaIndex (which favors higher-level abstractions), Haystack is the most **type-safe and pipeline-centric** of the major RAG frameworks. Best for **production search systems** where you need strict schemas, reproducible pipelines, and integration with Elasticsearch / OpenSearch / vector databases.

## Overview

- **Developer**: deepset (German NLP company; originally Malte Pietsch and team, 2019).
- **Languages**: Python.
- **License**: Apache 2.0.
- **Status**: Haystack 2.x is the current major version (released 2023, stable since). Haystack 1.x is in maintenance only — do not start new projects on 1.x.

## Why Haystack Exists

deepset builds enterprise search systems (deepset Cloud, deepset Studio). Their pain points, starting in 2019, were:

1. **Reproducibility** — search pipelines involve many components (retrievers, readers, rerankers, generators). Without a strict pipeline abstraction, every refactor breaks downstream behavior.
2. **Type safety** — components pass data through a chain. If a retriever returns a `list[Document]` and the next component expects a `list[str]`, the error should be caught at pipeline construction, not at runtime.
3. **Search-engine integration** — deepset's stack is Elasticsearch / OpenSearch / vector DBs. They need first-class connectors and consistent APIs across them.

Haystack was built to solve these. The 2.x rewrite (2023) doubled down on the pipeline-as-DAG model with Pydantic-validated components and an explicit component protocol (`@component` decorator, `run()` method).

## Core Concepts

### Components

A component is a typed, reusable unit with declared inputs and outputs:

```python
from haystack import component, Document
from typing import List

@component
class KeywordExtractor:
    @component.output_types(keywords=List[str])
    def run(self, documents: List[Document], top_k: int = 5) -> dict:
        # Extract top-k keywords from each document.
        return {"keywords": [extract(doc.text) for doc in documents[:top_k]]}
```

The `@component.output_types` decorator declares the output schema. Haystack validates connections at pipeline-build time: if you connect this component's output to one expecting `List[Document]`, you get an immediate error.

### Pipelines

A pipeline is a DAG of components. Components are added and connected by name:

```python
from haystack import Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.embedders import OpenAITextEmbedder, OpenAIDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore

# Indexing pipeline
indexing = Pipeline()
indexing.add_component("embedder", OpenAIDocumentEmbedder())
indexing.add_component("writer", DocumentWriter(document_store=InMemoryDocumentStore()))
indexing.connect("embedder.documents", "writer.documents")

# Query pipeline
query = Pipeline()
query.add_component("embedder", OpenAITextEmbedder())
query.add_component("retriever", InMemoryBM25Retriever(document_store=store, top_k=10))
query.add_component("generator", OpenAIGenerator())
query.connect("embedder.embedding", "retriever.query_embedding")
query.connect("retriever.documents", "generator.documents")
```

Pipelines are serializable to YAML — you can version them in Git, diff them in code review, and ship the same YAML from dev to prod. This is a major production advantage over LangChain, where the pipeline structure is implicit in the Python code.

### Document Stores

Haystack has first-class support for:

- **InMemoryDocumentStore** — for prototyping and tests.
- **ElasticsearchDocumentStore** — production search.
- **OpenSearchDocumentStore** — production search (open-source Elasticsearch fork).
- **WeaviateDocumentStore**, **QdrantDocumentStore**, **PineconeDocumentStore** — vector DBs.
- **pgvectorDocumentStore** — Postgres with pgvector.

All expose the same `write_documents()`, `search()`, `delete()` interface, so swapping stores is a one-line change.

### Retrievers and Readers

Haystack inherits the **retriever-reader** distinction from its QA roots:

- **Retriever**: given a query, return a list of relevant Documents. BM25, embedding, hybrid.
- **Reader**: given a query + Documents, extract or generate an answer. Extractive readers (BERT-style span extraction) and generative readers (LLM) are both supported.

Modern Haystack pipelines often use a retriever + generative reader (i.e., RAG), but the retriever-reader abstraction is preserved for backwards compatibility and for cases where extractive QA is preferred (faster, no LLM cost, more controllable).

## Worked Example: Hybrid RAG Pipeline

```python
from haystack import Pipeline, Document
from haystack.components.embedders import OpenAITextEmbedder, OpenAIDocumentEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever, InMemoryBM25Retriever
from haystack.components.joiners import DocumentJoiner
from haystack.components.rankers import TransformersSimilarityRanker
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.document_stores.in_memory import InMemoryDocumentStore

# Build a hybrid retrieval + RAG pipeline
store = InMemoryDocumentStore(embedding_dim=1536, bm25_algorithm="BM25Plus")

# Indexing
index = Pipeline()
index.add_component("doc_embedder", OpenAIDocumentEmbedder(model="text-embedding-3-small"))
index.add_component("writer", DocumentWriter(document_store=store))
index.connect("doc_embedder.documents", "writer.documents")

# Query: hybrid retrieval + reranking + RAG generation
prompt_template = """
Given these documents, answer the question.

Documents:
{% for doc in documents %}
  - {{ doc.content }}
{% endfor %}

Question: {{ question }}
Answer:
"""

query = Pipeline()
query.add_component("query_embedder", OpenAITextEmbedder(model="text-embedding-3-small"))
query.add_component("vec_retriever", InMemoryEmbeddingRetriever(document_store=store, top_k=20))
query.add_component("bm25_retriever", InMemoryBM25Retriever(document_store=store, top_k=20))
query.add_component("joiner", DocumentJoiner(join_mode="reciprocal_rank_fusion"))
query.add_component("ranker", TransformersSimilarityRanker(model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_k=5))
query.add_component("prompt_builder", PromptBuilder(template=prompt_template))
query.add_component("generator", OpenAIGenerator(model="gpt-4o-mini"))

query.connect("query_embedder.embedding", "vec_retriever.query_embedding")
query.connect("bm25_retriever.documents", "joiner.documents")
query.connect("vec_retriever.documents", "joiner.documents")
query.connect("joiner.documents", "ranker.documents")
query.connect("ranker.documents", "prompt_builder.documents")
query.connect("prompt_builder.prompt", "generator.prompt")

# Run
result = query.run({
    "bm25_retriever": {"query": "What is Mamba-2?"},
    "query_embedder": {"text": "What is Mamba-2?"},
    "prompt_builder": {"question": "What is Mamba-2?"}
})
print(result["generator"]["replies"][0])
```

Note the explicit connection of inputs and outputs — every component's input must come from another component's output or from the `run()` arguments. This explicitness is what makes Haystack pipelines inspectable and versionable.

## Comparison with Other Frameworks

| Aspect               | Haystack                    | LangChain                  | LlamaIndex                |
|----------------------|-----------------------------|----------------------------|---------------------------|
| Core abstraction     | DAG pipeline of components  | Chains / LCEL              | Indexes + query engines   |
| Type safety          | Strong (Pydantic-validated) | Weak (stringly-typed)      | Moderate (Pydantic in v0.10+) |
| Pipeline serialization | YAML serializable         | Implicit (in code)         | Partial                   |
| Search engine focus  | First-class (ES, OS, vector DBs) | Limited                | Limited                   |
| RAG quality          | Strong (hybrid, reranking built-in) | Moderate            | Strong                    |
| Agent support        | Basic (Tool component)      | Strong (LangGraph)         | Moderate (sub-question query engine) |
| Best for             | Production search + RAG     | General LLM apps           | RAG-focused data apps     |
| Production maturity  | GA (deepset Cloud)          | GA (LangChain Inc.)        | GA                        |

## When to Choose Haystack

- **Production search systems** — the pipeline-as-DAG model with type checking catches integration bugs at construction time.
- **Elasticsearch / OpenSearch shops** — Haystack's connectors are first-class and well-tested.
- **Hybrid retrieval** — built-in BM25 + vector + reciprocal rank fusion + cross-encoder reranking, no glue code.
- **Reproducibility requirements** — YAML-serialized pipelines can be versioned, diffed, and audited.
- **Regulated industries** — the explicit pipeline structure makes compliance audits easier ("show me exactly what the system does for this query").

## When NOT to Choose Haystack

- **Complex agents** — Haystack's agent support is basic; use LangGraph or PydanticAI for serious agent work.
- **Rapid prototyping** — the type-safety overhead slows you down in early exploration; LangChain or direct OpenAI SDK is faster.
- **Novel research patterns** — Haystack's component model assumes well-defined inputs/outputs; novel patterns (e.g., dynamic tool composition) don't fit cleanly.
- **Non-search LLM apps** — if you're not doing retrieval, Haystack's pipeline model is overkill.

## Production Patterns

### Pipeline versioning

Serialize every pipeline to YAML and store in Git alongside model configs. When you deploy, the YAML + model version is the deployment artifact. This makes rollbacks trivial (revert the YAML) and gives you audit history ("what did the pipeline look like when this bug was reported?").

### Component testing

Each component can be tested in isolation by calling its `run()` method with mock inputs. This is much easier than testing a LangChain chain, where you have to construct the entire chain to test one step.

### Hybrid retrieval default

For most production RAG systems, start with BM25 + vector retrieval with RRF fusion, then add a cross-encoder reranker. This beats pure-vector or pure-BM25 retrieval by 5–15% on most benchmarks. Haystack makes this a 5-line pipeline; in LangChain it's significantly more code.

### Streaming and async

Haystack 2.x supports async components and streaming outputs. For latency-sensitive deployments, use streaming generators so the user sees the first tokens within ~200ms instead of waiting for the full answer.

## Common Pitfalls

- **Using Haystack 1.x** — 1.x is maintenance-only. The 2.x API is incompatible; do not start new projects on 1.x. Migration guides exist but are non-trivial.
- **Forgetting to connect every component input** — Haystack raises a clear error at `Pipeline()` construction if any input is unconnected. Pay attention to these errors — they catch real bugs.
- **Mixing pipeline and ad-hoc code** — if you bypass the pipeline (e.g., call a retriever directly outside a pipeline), you lose serialization, telemetry, and async benefits. Keep everything in pipelines.
- **Wrong document store for the workload** — InMemoryDocumentStore is for tests only; production needs Elasticsearch/OpenSearch/Qdrant/pgvector. Choose based on your scale: <1M docs → pgvector or Qdrant; 1M–100M → Qdrant or Weaviate; >100M → Elasticsearch or OpenSearch with dedicated hardware.
- **Not using a reranker** — pure vector retrieval leaves 5–15% quality on the table. Add a cross-encoder reranker (`TransformersSimilarityRanker`) on top-20 retrieved docs to get top-5 for generation.

## Further Reading

- deepset, *Haystack Documentation* — https://haystack.deepset.ai/
- deepset, *Haystack GitHub* — https://github.com/deepset-ai/haystack
- deepset, *Haystack 2.0 Migration Guide* — for teams on 1.x.
- Pietsch et al., various deepset blog posts on hybrid retrieval and RAG evaluation.

## Connection to Other Concepts

- [[25 - Frameworks and Tools/Agent Frameworks/01 - Framework Selection Guide|Framework Selection Guide]] — when Haystack is the right choice.
- [[25 - Frameworks and Tools/LLM Frameworks/02 - LangChain|LangChain]] — the more general alternative.
- [[25 - Frameworks and Tools/LLM Frameworks/05 - LlamaIndex|LlamaIndex]] — the RAG-focused alternative.
- [[17 - RAG/Ingestion and Retrieval/02 - Chunking Hybrid Search Reranking|Chunking Hybrid Search Reranking]] — Haystack's hybrid retrieval implements this pattern.
- [[17 - RAG/Ingestion and Retrieval/01 - RAG Pipeline Overview|RAG Pipeline Overview]] — Haystack is a concrete implementation of this pipeline.
- [[18 - Memory Systems/Vector Memory/04 - Vector Memory Backends|Vector Memory Backends]] — Haystack's document stores are these backends.
- [[27 - Projects/Mini-Projects/02 - Build a Mini RAG Pipeline|Build a Mini RAG Pipeline]] — the from-scratch version of what Haystack provides.

## Interview Questions

1. **Q: What distinguishes Haystack from LangChain and LlamaIndex?**
   A: Haystack's distinctive feature is the **pipeline-as-DAG** architecture with Pydantic-validated components. Every system is a directed acyclic graph of typed components, and connections are validated at pipeline construction time. LangChain favors stringly-typed chains; LlamaIndex favors higher-level abstractions. Haystack is the most type-safe and pipeline-centric of the three, making it best for production search systems where reproducibility and strict schemas matter.

2. **Q: Explain the retriever-reader distinction in Haystack.**
   A: A retriever takes a query and returns a list of relevant Documents (BM25, embedding, hybrid). A reader takes a query + Documents and produces an answer. Extractive readers (BERT-style span extraction) identify the exact answer span in a document; generative readers (LLM) generate a free-form answer conditioned on the documents. Modern Haystack pipelines typically use retriever + generative reader (i.e., RAG), but the retriever-reader abstraction is preserved for backwards compatibility and for cases where extractive QA is preferred (faster, no LLM cost, more controllable).

3. **Q: Why would you serialize a Haystack pipeline to YAML?**
   A: Three reasons. (1) **Versioning** — the YAML becomes the deployment artifact, stored in Git alongside model configs. Rollbacks are trivial (revert the YAML). (2) **Auditability** — you can answer "what did the pipeline look like when this bug was reported?" by checking out the YAML at that commit. (3) **Reproducibility** — the same YAML ships from dev to staging to prod, eliminating "works on my machine" issues. This is a major production advantage over LangChain, where the pipeline structure is implicit in the Python code.

4. **Q: Describe the hybrid retrieval pattern in Haystack and why you'd use it.**
   A: Run BM25 and vector retrieval in parallel, each returning top-K (e.g., 20) documents. Combine via reciprocal rank fusion (RRF) — a rank-based scoring that doesn't require score calibration. Then run a cross-encoder reranker on the fused top-20 to get top-5 for generation. This beats pure-vector or pure-BM25 by 5–15% on most benchmarks because BM25 catches keyword matches (names, IDs, rare terms) that embeddings miss, while embeddings catch semantic matches that BM25 misses. Haystack makes this a 5-line pipeline; in LangChain it's significantly more code.

5. **Q: When would you NOT use Haystack?**
   A: Four cases. (1) Complex agents — Haystack's agent support is basic; use LangGraph or PydanticAI. (2) Rapid prototyping — the type-safety overhead slows you down in early exploration; LangChain or direct OpenAI SDK is faster. (3) Novel research patterns — Haystack's component model assumes well-defined inputs/outputs; novel patterns like dynamic tool composition don't fit cleanly. (4) Non-search LLM apps — if you're not doing retrieval, Haystack's pipeline model is overkill.

6. **Q: How do you choose a document store in Haystack?**
   A: By scale and existing infrastructure. InMemoryDocumentStore is for tests only. For production: <1M docs → pgvector (if you already use Postgres) or Qdrant (standalone, fast). 1M–100M docs → Qdrant or Weaviate. >100M docs → Elasticsearch or OpenSearch with dedicated hardware. All expose the same `write_documents()`, `search()`, `delete()` interface, so swapping stores is a one-line change — start with the one matching your existing stack.

## See Also

- [[25 - Frameworks and Tools/MOC|Frameworks and Tools MOC]]
- [[25 - Frameworks and Tools/Agent Frameworks/01 - Framework Selection Guide|Framework Selection Guide]]
- [[25 - Frameworks and Tools/LLM Frameworks/02 - LangChain|LangChain]]
- [[25 - Frameworks and Tools/LLM Frameworks/05 - LlamaIndex|LlamaIndex]]
- [[17 - RAG/Ingestion and Retrieval/01 - RAG Pipeline Overview|RAG Pipeline Overview]]
- [[17 - RAG/Ingestion and Retrieval/02 - Chunking Hybrid Search Reranking|Chunking Hybrid Search Reranking]]
- [[18 - Memory Systems/Vector Memory/04 - Vector Memory Backends|Vector Memory Backends]]
- [[27 - Projects/Mini-Projects/02 - Build a Mini RAG Pipeline|Build a Mini RAG Pipeline]]
