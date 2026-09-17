# Medical-NLP-Reconstructed

A reconstructed, mathematically rigorous, engineering-grade Obsidian vault covering every layer of a hybrid **Connectionist + Symbolic + Supervised** pipeline for rare-disease diagnosis from free-text clinical notes.

This vault is a **complete reconstruction** of the original `Medical-NLP` repository, built by treating a comprehensive critical audit as a hard specification. Every chapter has been reorganised, expanded, or rewritten so that the 37 deficiencies documented in the audit no longer exist.

---

## What Changed vs. the Original Vault

### Structural Changes

1. **The `OLD/` directory is removed.** The original vault contained 6 duplicate chapters under an outdated numbering scheme; these are gone.
2. **Chapter numbering is consistent.** The original had stale H1 headers (e.g., `03.4` opened with `# 2.2.`); all notes now have consistent numbering.
3. **The copy-paste break in 3.4 is fixed.** The original `03.4. BioBERT Fine-tuning Logic.md` cut off mid-sentence and restarted with a duplicate H1; the reconstructed note flows continuously.
4. **The HMER/OCR paragraph in the conclusion is removed.** The original `10.5. Project Conclusion.md` contained a paragraph copied from an unrelated OCR project; the reconstructed conclusion focuses exclusively on clinical NLP.
5. **Two new notes are added**: `02.2. Positional Encodings` (the original vault completely omitted positional encodings) and `03.6. UMLS and Concept Unique Identifiers` (the original mentioned UMLS but never defined it).

### Content Changes

Every mathematical and engineering gap identified in the audit is filled. Highlights:

- **Full QKV projection matrices** ($W^Q, W^K, W^V, W^O$) with dimensions and parameter counts — [[02.1. Self-Attention and the QKV Math]].
- **The $\sqrt{d_k}$ scaling derivation** — [[02.1. Self-Attention and the QKV Math]] §3.
- **Anisotropy and BERT-Whitening** — [[03.3. The 0.9 Similarity Trap and Anisotropy]].
- **SapBERT's Multi-Similarity Loss formula** — [[03.2. ClinicalBERT, PubMedBERT, and SapBERT]] §4.1.
- **Curse of Dimensionality proof** — [[04.3. Length Invariance and the Curse of Dimensionality]] §2.
- **Non-negative activation bound** on cosine similarity — [[04.2. Rigorous Cosine Similarity Derivation]] §3.
- **FAISS index families** (Flat, IVF-Flat, IVF-PQ, HNSW) with latency/recall table — [[05.2. Top-K Candidate Retrieval]].
- **Full LLM Cleaner system prompt + Pydantic schema** — [[05.1. LLM Clinical Cleaner Logic]].
- **KV-Caching** for decoder LLMs — [[06.1. LLM Architecture vs BERT]] §4.
- **Pydantic + Outlines + Instructor** for structured generation — [[06.4. Robust JSON Parsing and Schema Validation]].
- **Temperature-scaled softmax formula** — [[06.3. Deterministic AI (Temperature and Top-P)]] §2.
- **Micro-F1 vs. Macro-F1** and **strict vs. loose NER matching** — [[06.5. NER Evaluation Metrics]].
- **DAGs, multiple inheritance, transitive closures** — [[07.1. Taxonomy, Hierarchy, and DAGs in Medicine]].
- **Ontology versioning, deprecation, `owl:sameAs`** — [[07.2. HPO, Orphanet, MONDO, and UMLS ID Logic]].
- **SPECIALIST Lexicon** and **WSD** — [[07.3. Semantic Normalization]].
- **RDF-star / Reification** for edge metadata — [[08.1. RDF SPO Model, Turtle Syntax, and Reification]].
- **Corrected complexity claims** for NetworkX (the original falsely claimed $O(1)$) — [[08.2. Graph Theory, MultiDiGraphs, and Complexity]].
- **Resnik, Lin, Jiang-Conrath, Overlap Coefficient** (replacing flat Jaccard) — [[08.3. Beyond Jaccard — Asymmetric and Hierarchical Similarity]].
- **Hub-node IDF weighting** and path-constrained random walks — [[08.4. Multi-hop Traversal, Hub Nodes, and Explainability]].
- **GNN vs. symbolic KG comparison** — [[08.5. Hybrid Architectures — KG vs GNN]].
- **LTR taxonomy** (pointwise, pairwise, listwise) — [[09.1. Learning-to-Rank — Pointwise, Pairwise, Listwise]].
- **Group-aware split** to prevent data leakage — [[09.2. Pairwise Dataset Construction]] §3.
- **Full PyTorch `NeuralRanker(nn.Module)` implementation** — [[09.3. Neural Ranking Network Architecture]] §4.
- **BCE loss formula** — [[09.3. Neural Ranking Network Architecture]] §5.
- **Global cosine features** in the ranker input — [[09.3. Neural Ranking Network Architecture]] §3.
- **Bradley-Terry model** for non-transitive tournament cycles — [[09.4. Global Tournament Re-ranking]] §3.
- **Full Mann-Whitney U formula** with ties adjustment and $z$-score — [[10.1. Statistical Significance — Mann-Whitney U-Test]].
- **NDCG formula and code** — [[10.2. Ranking Metrics — MRR, Top-K, and NDCG]] §3–§4.
- **Bootstrap confidence intervals** — [[10.3. Visualizing Results with Statistical Rigor]] §2.
- **Random seed configuration** across all libraries — [[10.4. Reproducible Notebook Flow]] §2.
- **Patient-stratified three-way validation split** — [[10.4. Reproducible Notebook Flow]] §3.

For the complete issue-to-resolution mapping, see [[A1. Issue Traceability Matrix]].

---

## Vault Structure

```
Medical-NLP-Reconstructed/
├── 0. Master Index.md
├── 01. Foundations of Medical NLP/
│   ├── 01.1. The Medical Text Problem.md
│   ├── 01.2. The Evolution of NLP Vectors.md
│   └── 01.3. The Mission — Bridging the Semantic Gap.md
├── 02. The Transformer Engine and Tokenization/
│   ├── 02.1. Self-Attention and the QKV Math.md
│   ├── 02.2. Positional Encodings.md          [NEW]
│   └── 02.3. Tokenization and WordPiece Logic.md
├── 02b. BERT vs GPT — Encoder Versatility Across Domains/    [NEW CHAPTER]
│   ├── 02b.1. The Encoder-Decoder Split — BERT vs GPT Architectures.md
│   ├── 02b.2. Why BERT Is More Versatile — The Bidirectional Advantage.md
│   ├── 02b.3. The BERT Family Tree — Variants Across Domains.md
│   └── 02b.4. What Makes BERT Special — The Pre-train + Fine-tune Paradigm.md
├── 03. Multi-Embedding Strategy (Domain Adaptation)/
│   ├── 03.1. Why General AI Fails in Medicine.md
│   ├── 03.2. ClinicalBERT, PubMedBERT, and SapBERT.md
│   ├── 03.3. The 0.9 Similarity Trap and Anisotropy.md
│   ├── 03.4. BioBERT Fine-tuning Logic.md
│   ├── 03.5. BioBERT Specialization (Cased vs. Uncased).md
│   └── 03.6. UMLS and Concept Unique Identifiers.md    [NEW]
├── 04. Mathematics of Vector Similarity/
│   ├── 04.1. 768-D Geometry and Manifolds.md
│   ├── 04.2. Rigorous Cosine Similarity Derivation.md
│   └── 04.3. Length Invariance and the Curse of Dimensionality.md
├── 05. Phase 1 — Retrieval and Clinical Standardization/
│   ├── 05.1. LLM Clinical Cleaner Logic.md
│   └── 05.2. Top-K Candidate Retrieval.md
├── 06. Clinical Entity Extraction with LLMs/
│   ├── 06.1. LLM Architecture vs BERT.md
│   ├── 06.2. Medical Prompt Engineering.md
│   ├── 06.3. Deterministic AI (Temperature and Top-P).md
│   ├── 06.4. Robust JSON Parsing and Schema Validation.md
│   └── 06.5. NER Evaluation Metrics.md
├── 07. Medical Ontologies/
│   ├── 07.1. Taxonomy, Hierarchy, and DAGs in Medicine.md
│   ├── 07.2. HPO, Orphanet, MONDO, and UMLS ID Logic.md
│   └── 07.3. Semantic Normalization.md
├── 08. Unified Knowledge Graphs/
│   ├── 08.1. RDF SPO Model, Turtle Syntax, and Reification.md
│   ├── 08.2. Graph Theory, MultiDiGraphs, and Complexity.md
│   ├── 08.3. Beyond Jaccard — Asymmetric and Hierarchical Similarity.md
│   ├── 08.4. Multi-hop Traversal, Hub Nodes, and Explainability.md
│   └── 08.5. Hybrid Architectures — KG vs GNN.md
├── 09. Phase 2 — Neural Pairwise Ranking/
│   ├── 09.1. Learning-to-Rank — Pointwise, Pairwise, Listwise.md
│   ├── 09.2. Pairwise Dataset Construction.md
│   ├── 09.3. Neural Ranking Network Architecture.md
│   └── 09.4. Global Tournament Re-ranking.md
├── 10. Statistical Validation and Reporting/
│   ├── 10.1. Statistical Significance — Mann-Whitney U-Test.md
│   ├── 10.2. Ranking Metrics — MRR, Top-K, and NDCG.md
│   ├── 10.3. Visualizing Results with Statistical Rigor.md
│   ├── 10.4. Reproducible Notebook Flow.md
│   └── 10.5. Project Conclusion — The Triple-Threat Architecture.md
└── _meta/
    ├── A1. Issue Traceability Matrix.md
    └── A2. Glossary.md
```

**Total: 40 notes** across 11 chapters + 2 appendices (including the new Chapter 02b on BERT vs GPT versatility).

---

## How to Read the Vault

1. **Start with the [[0. Master Index]]** for the full chapter map.
2. **Read Chapter 1 first** — it establishes the failure modes that every later chapter addresses.
3. **Read in chapter order** — each chapter builds on the previous one. The chapters form a clean learning progression: foundations → transformer math → embeddings → vector geometry → retrieval → entity extraction → ontologies → knowledge graphs → ranking → validation.
4. **Follow cross-references** — every note has a "Cross-References" section at the bottom linking to related notes. Use these to navigate non-linearly once you have the overall picture.
5. **Use the [[A2. Glossary]]** for term definitions.
6. **Use the [[A1. Issue Traceability Matrix]]** to verify that a specific audit issue has been resolved.

---

## Opening in Obsidian

This vault is Obsidian-compatible. To open it:

1. Open Obsidian.
2. Click "Open folder as vault."
3. Select the `Medical-NLP-Reconstructed` folder.
4. The wiki-links (`[[Note Title]]`) will resolve automatically.

The vault uses **wiki-style links** (not Markdown links) so that links survive file moves. Obsidian resolves them by note title.

---

## Source

- **Original vault**: https://github.com/Vtheonly/Medical-NLP
- **Reconstruction specification**: The critical audit report provided alongside the original vault.

---

## License

Same as the original repository.
