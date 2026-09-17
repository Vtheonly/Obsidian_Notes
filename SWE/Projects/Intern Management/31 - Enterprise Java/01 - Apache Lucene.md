---
tags: [concept, enterprise, search, lucene]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/08 - Oracle Text and Full-Text Search]]
---

# Apache Lucene

## What it is

**Apache Lucene** is a full-text search engine library (Java). Embed in your app for in-memory search.

## Why

- **Fast** — indexes text for O(1) lookup.
- **Fuzzy** — finds "Ali" when you search "alice" (stemming, fuzzy matching).
- **Relevance** — ranks results by relevance.
- **Embedded** — no external service (unlike Elasticsearch).

## Maven

```xml
<dependency>
    <groupId>org.apache.lucene</groupId>
    <artifactId>lucene-core</artifactId>
    <version>9.8.0</version>
</dependency>
```

## Usage

### Index
```java
Directory directory = FSDirectory.open(Path.of("lucene-index"));
IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
IndexWriter writer = new IndexWriter(directory, config);

Document doc = new Document();
doc.add(new TextField("name", intern.getName(), Field.Store.YES));
doc.add(new TextField("email", intern.getEmail(), Field.Store.YES));
doc.add(new StringField("id", intern.getId().toString(), Field.Store.YES));
writer.addDocument(doc);
writer.close();
```

### Search
```java
IndexReader reader = DirectoryReader.open(directory);
IndexSearcher searcher = new IndexSearcher(reader);

Query query = new QueryParser("name", new StandardAnalyzer()).parse("alice");
TopDocs results = searcher.search(query, 10);

for (ScoreDoc scoreDoc : results.scoreDocs) {
    Document doc = searcher.doc(scoreDoc.doc);
    long id = Long.parseLong(doc.get("id"));
    // ...
}
```

## When to use

- **In-app search** — search intern names, emails, descriptions.
- **Offline** — no network dependency.
- **Small-to-medium datasets** — up to ~1M documents.

For larger datasets or multi-instance, use **Elasticsearch** (built on Lucene, distributed).

## Project Connection

The project uses `LIKE '%name%'` for search — slow (full scan), no ranking, no fuzzy. For better search:
- Small dataset: `FilteredList` with in-memory filtering.
- Medium: Lucene index.
- Large: Elasticsearch.

For the intern app (likely < 100K interns), Lucene is sufficient.

## Further reading

- Lucene documentation.
