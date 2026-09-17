---
tags: [framework, llamaindex, rag, data-framework]
iteration: 4
created: 2026-08-08
aliases: [LlamaIndex, GPT Index]
---

# 05 — LlamaIndex

> [!info] TL;DR
> LlamaIndex is a data framework for LLM applications, focused on connecting custom data sources to LLMs. Its strengths are document ingestion (diverse loaders), indexing (multiple index types for different retrieval patterns), and structured querying (query engines that combine retrieval with LLM reasoning). LlamaIndex is the standard choice for RAG-centric applications where data connection is the primary challenge.

## Overview

- **Developer**: LlamaIndex Inc. (Jerry Liu, 2022).
- **Language**: Python, TypeScript.
- **License**: MIT.
- **Status**: actively developed; focused on enterprise RAG.

## Core Focus: Data Connection

While LangChain tries to be a general LLM framework, LlamaIndex focuses specifically on the **data problem**: how do you connect LLMs to your data? This includes:
- Loading data from diverse sources (file systems, databases, APIs, SaaS tools).
- Structuring data for efficient retrieval (indexes).
- Querying data in ways that leverage LLM reasoning.

This focus makes LlamaIndex the strongest framework for RAG applications, especially enterprise RAG with complex data sources.

## Core Abstractions

### Documents and Nodes
- **Document**: a container for a piece of text + metadata (source, author, date, etc.).
- **Node**: a chunk of a document, the unit of retrieval. Nodes have parent-document relationships.

```python
from llama_index.core import Document, SimpleNodeParser

doc = Document(text="Long document text...", metadata={"source": "report.pdf"})
parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
nodes = parser.get_nodes_from_documents([doc])
```

### Indexes
Indexes are data structures that enable efficient retrieval. LlamaIndex supports several:

- **VectorStoreIndex**: embeddings for semantic search. The default for most RAG.
- **SummaryIndex** (formerly ListIndex): stores nodes in a sequence; good for summarization.
- **TreeIndex**: hierarchical tree of summaries; good for long documents.
- **KeywordTableIndex**: keyword extraction + lookup; good for entity-centric search.
- **KnowledgeGraphIndex**: entities + relationships; good for multi-hop reasoning.

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex(nodes)
```

### Query Engines
Query engines combine retrieval with LLM reasoning:

```python
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("What is the revenue trend?")
print(response.response)
```

The query engine:
1. Embeds the query.
2. Retrieves top-K nodes from the index.
3. Constructs a prompt with the query + retrieved context.
4. Calls the LLM to generate an answer.

### Chat Engines
Chat engines maintain conversation history:

```python
chat_engine = index.as_chat_engine()
response = chat_engine.chat("Tell me about the company")
followup = chat_engine.chat("What about their competitors?")
```

### Retrievers
Retrievers are customizable retrieval logic:

```python
from llama_index.core.retrievers import VectorIndexRetriever

retriever = VectorIndexRetriever(index, similarity_top_k=10)
nodes = retriever.retrieve("query")
```

You can compose retrievers (union, intersection, routing) for complex retrieval strategies.

### Response Synthesizers
Control how the LLM synthesizes a response from retrieved nodes:
- **Compact**: stuff all nodes into one prompt.
- **Tree summarize**: recursively summarize chunks.
- **Refine**: generate an initial answer, then refine with each subsequent chunk.

### Data Loaders
LlamaIndex has 200+ data loaders (LlamaHub) for diverse sources:
- File types: PDF, DOCX, HTML, Markdown, code files.
- Databases: Postgres, MongoDB, Snowflake, BigQuery.
- SaaS: Notion, Slack, GitHub, Google Drive, Jira.
- Web: URL crawling, sitemap parsing, RSS feeds.

```python
from llama_index.readers.file import PDFReader
from llama_index.readers.github import GithubRepositoryReader

# Load from PDF
pdf_docs = PDFReader().load_data("report.pdf")

# Load from GitHub
github_docs = GithubRepositoryReader(owner="owner", repo="repo").load_data()
```

## Advanced Features

### LlamaParse
LlamaIndex's commercial document parsing service. Handles complex PDFs (tables, figures, multi-column layouts) better than open-source alternatives. Produces Markdown that's LLM-friendly.

### LlamaCloud
Managed indexing and retrieval service. Handles document ingestion, indexing, and retrieval without infrastructure management. Targeted at enterprise RAG.

### Workflows
LlamaIndex's workflow system (similar to LangGraph) for multi-step RAG pipelines:
- Conditional retrieval (try vector search, fall back to keyword).
- Multi-hop retrieval (retrieve, reason, retrieve again).
- Agentic RAG (LLM decides when to retrieve and what to query).

### Agents
LlamaIndex has its own agent abstractions, though they're less mature than LangGraph's:
- `ReActAgent`: standard ReAct loop.
- `FunctionAgent`: function-calling-based agent.
- `WorkflowAgent`: agent built on the workflow system.

### Structured Output
LlamaIndex supports structured output extraction:
```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

query_engine = index.as_query_engine(output_cls=Person)
result = query_engine.query("Extract the person from the document")
print(result.name)  # "Alice"
```

## Strengths

### Data Connection Breadth
LlamaIndex's 200+ loaders cover virtually any data source. If you need to ingest data from an unusual source, LlamaIndex likely has a loader. This is its biggest advantage over LangChain.

### Index Variety
Multiple index types let you choose the right structure for your data:
- Vector for semantic search.
- Tree for long-document summarization.
- Graph for multi-hop reasoning.
- Keyword for exact-match retrieval.

Most other frameworks only support vector indexes.

### RAG-Centric Design
Every abstraction is designed with RAG in mind. The query engine, retriever, synthesizer separation maps cleanly to the RAG pipeline, making it easy to customize each stage.

### LlamaParse for Complex Documents
For enterprise RAG with complex PDFs (tables, figures, multi-column), LlamaParse is significantly better than open-source alternatives. It's a commercial add-on but worth it for production RAG.

### Cleaner Abstractions Than LangChain
LlamaIndex's abstractions (Document, Node, Index, QueryEngine) are more cohesive and less leaky than LangChain's. The framework feels more focused.

## Weaknesses

### Narrower Scope Than LangChain
LlamaIndex is RAG-focused. If you need general agent capabilities, complex tool orchestration, or non-RAG patterns, LangChain/LangGraph is more capable.

### Smaller Community Than LangChain
LlamaIndex has a smaller community and fewer third-party integrations. For niche use cases, you may need to build your own integrations.

### Commercial Components
LlamaParse and LlamaCloud are commercial. For open-source-only projects, you may need alternatives (Unstructured.io, self-hosted parsing).

### Less Mature Agent Support
LlamaIndex's agent abstractions are less mature than LangGraph's. For complex agents, LangGraph is the better choice.

## When to Use LlamaIndex

### Good Fit
- **RAG applications**: the primary use case. LlamaIndex is the strongest RAG framework.
- **Complex data ingestion**: diverse data sources, complex document formats.
- **Enterprise RAG**: with LlamaParse and LlamaCloud for production deployments.
- **Multi-index applications**: when you need different index types for different query patterns.

### Poor Fit
- **Agent-heavy applications**: use LangGraph.
- **Simple chatbots**: direct API calls are simpler.
- **Non-RAG LLM applications**: LlamaIndex's RAG focus is overkill.

## Comparison to Alternatives

| Framework   | Focus                    | Strengths                          | Weaknesses                       |
|-------------|--------------------------|------------------------------------|----------------------------------|
| LlamaIndex  | RAG + data connection    | Loaders, index variety, LlamaParse | Narrower scope, smaller community|
| LangChain   | General LLM framework    | Breadth, integrations, community   | Heavy abstractions, breaking chgs|
| DSPy        | Prompt optimization      | Systematic optimization            | Learning curve, compilation cost |
| Haystack    | Production NLP/RAG       | Clean design, production-focused   | Smaller community                |

LlamaIndex and Haystack are the closest competitors (both RAG-focused). LlamaIndex has broader data loader support; Haystack has a cleaner production architecture.

## Production Patterns

### Use LlamaParse for Complex PDFs
For enterprise RAG with complex documents (tables, multi-column, figures), LlamaParse is worth the cost. Open-source alternatives (PyPDF, pdfplumber) struggle with these formats.

### Combine Index Types
For complex applications, use multiple indexes:
- Vector index for semantic search.
- Keyword index for entity lookup.
- Tree index for document summarization.

Route queries to the appropriate index based on query type.

### Customize Retrievers
The default vector retriever is a starting point. For production, customize:
- Hybrid retrieval (vector + keyword).
- Reranking (cross-encoder after retrieval).
- Parent-document retrieval (retrieve chunks, return parent documents).
- Multi-hop retrieval (iterative retrieval for complex questions).

### Use the Workflow System for Complex Pipelines
For multi-step RAG (query rewriting, multi-hop, agentic), use LlamaIndex's workflow system rather than nesting query engines. It's more maintainable.

### Monitor Retrieval Quality
Track retrieval metrics (recall, precision) separately from generation metrics. A great LLM with poor retrieval produces hallucinated answers.

## See Also

- [[02 - LangChain]]
- [[03 - LangGraph]]
- [[04 - DSPy]]
- [[01 - Framework Selection Guide]]
- [[01 - RAG Pipeline Overview]]
- [[02 - Chunking Hybrid Search Reranking]]
- [[25 - Frameworks and Tools/MOC|25 Frameworks MOC]]
