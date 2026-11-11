---
tags: [nlp, tokenization, bpe]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [BPE, Byte-Pair Encoding]
---

# BPE (Byte-Pair Encoding)

> [!info] TL;DR
> BPE builds a subword vocabulary by repeatedly merging the most frequent adjacent symbol pair. Used by GPT-2/3/4, Llama, Mistral, and most modern LLMs (via `tiktoken` or HuggingFace tokenizers).

## The Algorithm

BPE on text works as follows:

1. **Initialize** the vocabulary with all single characters.
2. **Represent each word** as a sequence of characters, with an end-of-word marker (e.g., `low</w>`).
3. **Count** all adjacent symbol pairs across the corpus.
4. **Merge** the most frequent pair into a new symbol. Add it to the vocabulary.
5. **Repeat** steps 3–4 until the vocabulary reaches the target size.

The result is a **ranked list of merges**. To tokenize new text, apply the merges in rank order.

## Worked Example

Corpus: `low low low low low lower newer newest newest`

After character-level init:
```
l o w </w>
l o w e r
n e w e r
n e w e s t </w>
```

Pair counts (first round): `lo` appears 7 times, `ow` appears 7 times, `ne` 3 times, etc. Top pair: `lo` and `ow` tie. Pick `lo` (or whichever rule says).

Merge `l o` → `lo`:
```
lo w </w>
lo w e r
...
```

After many rounds, `low</w>` becomes a single token; `est</w>` becomes a single token. Now the word `lowest</w>` tokenizes as `low est</w>` — two subwords, both common.

## Byte-Level BPE

The classic BPE above operates on Unicode characters. **Byte-level BPE** (used by GPT-2 onwards) operates on **UTF-8 bytes** instead. This has two huge advantages:

1. **No `[UNK]` tokens ever** — any Unicode string is representable, because every byte is in the base vocabulary.
2. **Vocabulary is bounded** — the base vocabulary is 256 bytes; merges grow it to the target size.

The base vocabulary is 256 bytes. Each merge adds 1 token. With 50k merges, the vocabulary is 50,257 tokens (GPT-2's size).

## Pre-tokenization

BPE alone would let merges cross word boundaries, producing weird tokens. **Pre-tokenization** splits text into chunks first, then BPE-encodes each chunk independently.

GPT-2's pre-tokenization regex (used by `tiktoken`):

```
's|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

This matches: contractions, optional-space-then-letters, optional-space-then-digits, optional-space-then-punctuation, trailing whitespace, leading whitespace.

The key design: **whitespace is attached to the following token** (with ` ?`), so the model can distinguish `the` (mid-sentence) from ` the` (preceded by space). This is why encoding `the cat` and `thecat` produces different tokens.

## Encoding New Text

To tokenize new text with a trained BPE:

1. Pre-tokenize into chunks.
2. For each chunk, get its byte sequence.
3. Repeatedly apply the highest-ranked applicable merge until no more merges apply.
4. Output the resulting token IDs.

The merges are applied **in rank order** — the first merge in the learned list is applied first, then the second, and so on. This guarantees deterministic output.

## Implementation

```python
# A minimal BPE implementation
import re
from collections import Counter

def get_pairs(word):
    return list(zip(word[:-1], word[1:]))

def train_bpe(corpus, vocab_size):
    # Pre-tokenize
    words = re.findall(r'\S+|\s+', corpus)
    word_freqs = Counter(words)
    
    # Initialize: each word is a list of chars + end-of-word marker
    splits = {w: list(w) + ['</w>'] for w in word_freqs}
    
    vocab = set(c for w in splits.values() for c in w)
    merges = []
    
    while len(vocab) < vocab_size:
        pair_counts = Counter()
        for w, freq in word_freqs.items():
            for pair in get_pairs(splits[w]):
                pair_counts[pair] += freq
        if not pair_counts:
            break
        best = pair_counts.most_common(1)[0][0]
        merges.append(best)
        new_token = best[0] + best[1]
        vocab.add(new_token)
        # Apply merge in all words
        for w in splits:
            splits[w] = merge_word(splits[w], best, new_token)
    return vocab, merges
```

In production, use `tiktoken` (OpenAI) or HuggingFace `tokenizers` — they are 100–1000x faster (Rust implementation) and handle edge cases.

## Why This Matters for AI

- BPE is **the** dominant tokenizer for modern LLMs. If you use GPT-4, Llama, Mistral, or Qwen, you're using BPE.
- The merges encode information about the training corpus — they're optimized for that language distribution. Multilingual coverage depends entirely on the corpus the tokenizer was trained on.
- **Tokenizer leakage** — the choice of merges affects what the model "sees". A tokenizer that splits numbers into individual digits (e.g., `123` → `1 2 3`) makes arithmetic harder than one that keeps multi-digit numbers together.

## Production Implications

- **Use the official tokenizer.** Always load via `tiktoken.get_encoding("cl100k_base")` or `AutoTokenizer.from_pretrained(model_id)`. Never re-train a BPE for a model that's already pretrained.
- **Pin the tokenizer version** in your model registry. GPT-3 used `r50k_base`; GPT-3.5/4 use `cl100k_base`; GPT-4o uses `o200k_base`. The encodings are not interchangeable.
- **Token counting** — `len(encoding)` gives the exact billable count. For approximate counting without loading the tokenizer, use a rough estimate: ~4 characters per token for English, ~2 characters for Chinese, ~3-4 for code.
- **Caching** — encode prompts once and cache the IDs if you reuse prompts. Decoding is cheap; encoding is moderately expensive.

## Common Pitfalls

- **Forgetting pre-tokenization** — applying BPE directly to character sequences causes merges across word boundaries, producing terrible tokens.
- **Mixing tokenizer versions** — a model trained with `cl100k_base` will produce nonsense with `r50k_base`.
- **Adding tokens without resizing** — if you add a special token during fine-tuning, you must `model.resize_token_embeddings(len(tokenizer))`.
- **Decoding mid-token** — bytes might be partial UTF-8. Use `errors="replace"` or accumulate until a complete codepoint.

## Variants and Successors

- **Byte-level BPE** — used by GPT-2/3/4.
- **Qwen tokenizer** — adds specific merges for Chinese, code, math.
- **SentencePiece BPE** — same algorithm, but treats whitespace as a normal character (lossless).
- **tiktoken** — OpenAI's high-performance BPE library (Rust + Python bindings).

## Further Reading

- Sennrich, Haddow, Birch (2016), *Neural Machine Translation of Rare Words with Subword Units*.
- Radford et al. (2019), *Language Models are Unsupervised Multitask Learners* (GPT-2) — introduced byte-level BPE.
- `tiktoken` repo: https://github.com/openai/tiktoken

## See Also

- [[Tokenization Overview]]
- [[WordPiece]]
- [[SentencePiece]]
- [[05 - NLP Fundamentals/MOC|NLP Fundamentals MOC]]

## BPE Training Time Complexity

Training BPE on a corpus of $W$ words with average length $L$ to vocab size $V$:

- **Initial pair counting**: $O(W \cdot L)$ — count all adjacent pairs.
- **Each merge iteration**: re-count pairs (naive $O(W \cdot L)$, but can be done incrementally in $O(W)$ with a pair-to-words index).
- **Total iterations**: $V - V_0$ where $V_0$ is the initial vocab (256 for byte-level).
- **Total**: $O((V - V_0) \cdot W)$ — quadratic in vocab size.

For a 1B-word corpus and 50K vocab: ~50K × 1B = 5 × 10^13 operations. Takes hours on a single machine. Production BPE trainers (HuggingFace `tokenizers`, Tiktoken) use Rust + parallelism to make this tractable.

## Encoding New Text — Complexity and Optimizations

Encoding a text of length $N$ characters to tokens:

- **Naive**: for each merge in rank order, scan the text and apply. $O(V \cdot N)$ — too slow.
- **Optimized** (Tiktoken): build a merge index, apply only the relevant merges. $O(N \log V)$ with binary search, or $O(N)$ with a hash table.

Tiktoken (Rust) can encode ~1M tokens/sec on a single CPU core — fast enough that tokenization is never the bottleneck in production.

## Why Byte-Level BPE Won

Character-level BPE operates on Unicode codepoints. The problem: the base vocabulary is up to 1.1M codepoints (full Unicode), which is huge and includes many rare characters.

Byte-level BPE (introduced by GPT-2) operates on UTF-8 bytes. Benefits:

1. **Base vocabulary is always 256** — the 256 possible byte values. Bounded and small.
2. **No `[UNK]` ever** — any Unicode string is representable, because every byte is in the base vocab.
3. **Multilingual by default** — bytes are language-agnostic; the merges learned from the corpus determine language coverage.
4. **Backward compatible with ASCII** — the first 128 bytes are ASCII, so English text tokenizes naturally.

The cost: non-ASCII characters take more bytes (and thus more tokens) than they would with a Unicode-aware tokenizer. This is the "non-English tax" — but the simplicity and boundedness of byte-level BPE outweigh this cost for most use cases.

## Pre-tokenization Regex Patterns Compared

| Tokenizer      | Pre-tokenization regex                                                              | Notes                                          |
|----------------|-------------------------------------------------------------------------------------|------------------------------------------------|
| GPT-2          | `'s\|'t\|'re\|'ve\|'m\|'ll\|'d\| ?\p{L}+\| ?\p{N}+\| ?[^\s\p{L}\p{N}]+\|\s+` | Contractions, words, numbers, punctuation     |
| GPT-3.5/4      | Same as GPT-2                                                                       | `cl100k_base`                                  |
| GPT-4o         | Refined for better multilingual and code                                            | `o200k_base`                                   |
| Llama 3        | Similar to GPT-4, with code-specific patterns                                       | Better for code than Llama 2                   |
| Qwen 2/2.5     | Custom regex with Chinese / code patterns                                            | Strong multilingual                            |

The regex determines what counts as a "chunk" for BPE. Bad regex causes merges across word boundaries, producing terrible tokens. The pattern `'?\p{L}+` (optional apostrophe + letters) ensures words stay together while contractions like "don't" become a single chunk.

## Worked Example: BPE Encoding Step by Step

```python
import tiktoken

# Use GPT-4's encoding
enc = tiktoken.get_encoding("cl100k_base")

text = "Hello, world! 123"
tokens = enc.encode(text)
print(f"Text: {text!r}")
print(f"Tokens: {tokens}")
print(f"Decoded tokens: {[enc.decode([t]) for t in tokens]}")

# Example output:
# Text: 'Hello, world! 123'
# Tokens: [9906, 11, 1917, 0, 4513]
# Decoded tokens: ['Hello', ',', ' world', '!', ' 123']

# Note: spaces are attached to the following token (' world', ' 123')
# This is by design — distinguishes 'the' (mid-sentence) from ' the' (after space)

# Compare different texts
for text in ['the cat', 'thecat', 'The Cat', 'THE CAT']:
    tokens = enc.encode(text)
    print(f"{text!r:20} -> {tokens} -> {[enc.decode([t]) for t in tokens]}")
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Garbage output | Wrong tokenizer version | Pin the encoding in your model registry |
| Encoding is slow | Using Python loop instead of batch API | Use `tiktoken.encode_batch` or HuggingFace batch encoding |
| Decoding crashes on partial UTF-8 | BPE merge spans a multi-byte codepoint | Use `errors='replace'`; or accumulate bytes until a complete codepoint |
| Numbers split into single digits | Old tokenizer (GPT-2) without number-aware merges | Use Llama 3 or GPT-4o tokenizer with number-aware merges |
| Cost is higher than expected | Counting characters, not tokens | Use `len(enc.encode(text))` for cost estimation |

## Connection to Other Concepts

- [[05 - NLP Fundamentals/Tokenization/01 - Tokenization Overview|Tokenization Overview]] — the broader context.
- [[05 - NLP Fundamentals/Tokenization/03 - WordPiece|WordPiece]] — BERT's variant.
- [[05 - NLP Fundamentals/Tokenization/04 - SentencePiece|SentencePiece]] — the library that implements BPE and Unigram.
- [[08 - LLMs/MOC|LLMs MOC]] — where BPE is used.
- [[12 - Fine-Tuning/Instruction Tuning/03 - Instruction Tuning and Chat Templates|Instruction Tuning and Chat Templates]] — special tokens added to BPE.
- [[13 - Inference/Decoding/07 - Constrained Decoding and CFG|Constrained Decoding and CFG]] — token-level constraints during decoding.
- [[17 - RAG/Ingestion and Retrieval/02 - Chunking Hybrid Search Reranking|Chunking Hybrid Search Reranking]] — BPE-aware chunking.
- [[21 - LLMOps and MLOps/Cost/06 - Cost Optimization|Cost Optimization]] — BPE token count drives cost.
- [[26 - Papers/LLMs/15 - GPT-2 2019|GPT-2 2019]] — introduced byte-level BPE.

## Interview Questions

1. **Q: Why does byte-level BPE use a base vocabulary of 256?**
   A: UTF-8 encodes every Unicode codepoint as a sequence of 1-4 bytes. There are exactly 256 possible byte values (0x00 to 0xFF). By operating on bytes instead of codepoints, BPE has a bounded base vocabulary of 256, regardless of how many Unicode characters exist. This means any Unicode string is representable — every byte is in the vocab, so there's never an `[UNK]` token. The cost: non-ASCII characters take more bytes (and thus more tokens), which is the "non-English tax". But the simplicity and boundedness outweigh this cost.

2. **Q: Explain pre-tokenization and why it matters.**
   A: Pre-tokenization splits text into chunks (words, numbers, punctuation) before BPE is applied. Without it, BPE would let merges cross word boundaries, producing terrible tokens like "hecat" (merging "he" + "cat"). The GPT-2 regex `'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+` matches contractions, optional-space-then-letters, optional-space-then-digits, optional-space-then-punctuation, and whitespace. The key design: whitespace is attached to the following token (`' the'` vs `'the'`), so the model can distinguish mid-sentence from after-space. Each chunk is then BPE-encoded independently.

3. **Q: How is BPE encoding optimized for speed?**
   A: Naive encoding applies merges in rank order, scanning the text each time — $O(V \cdot N)$, too slow. Tiktoken (Rust) builds a merge index and applies only the relevant merges. With binary search: $O(N \log V)$. With a hash table: $O(N)$. Tiktoken can encode ~1M tokens/sec on a single CPU core, making tokenization never the bottleneck in production. HuggingFace's `tokenizers` library (also Rust) achieves similar speeds.

4. **Q: What's the difference between GPT-2's `r50k_base` and GPT-4o's `o200k_base`?**
   A: `r50k_base` (GPT-2/3): 50,257 tokens, byte-level BPE trained on English-heavy web text. Poor multilingual coverage — Chinese text takes 2-3× more tokens than English. `o200k_base` (GPT-4o): 200,019 tokens, BPE trained with more multilingual data and code. Better non-English coverage (Chinese tax reduced from 3× to ~1.5×). Better code coverage (multi-character operators like `==`, `!=` are single tokens). The encodings are NOT interchangeable — a model trained with one will produce garbage with another.

5. **Q: Why does the order of BPE merges matter?**
   A: BPE applies merges in the order they were learned (rank order). The first merge is the most frequent pair in the training corpus; the last is the least frequent. Applying in rank order ensures that common subwords are formed first, and rare merges only apply if no common merge is possible. This produces deterministic, reproducible tokenization. If you applied merges in a different order, you'd get different tokens — the rank order is part of the tokenizer's "DNA".

6. **Q: How would you train a custom BPE tokenizer for a new domain (e.g., medical text)?**
   A: (1) Collect a representative corpus (at least 1GB of medical text). (2) Choose vocab size (32K-128K, depending on multilingual needs). (3) Choose pre-tokenization regex (medical text has abbreviations like "mg", "IV" that should stay together). (4) Train byte-level BPE with HuggingFace `tokenizers` or Tiktoken's trainer. (5) Add special tokens (`[PATIENT]`, `[DIAGNOSIS]`, etc.) for your task. (6) Validate: encode a sample and check that medical terms are single tokens. (7) If you'll fine-tune a pretrained model, you must resize its embedding matrix to match the new vocab size — this is invasive, so consider whether a custom tokenizer is worth it.

## See Also

- [[Tokenization Overview]]
- [[WordPiece]]
- [[SentencePiece]]
- [[05 - NLP Fundamentals/MOC|NLP Fundamentals MOC]]
