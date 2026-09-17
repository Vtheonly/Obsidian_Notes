---
tags: [nlp, tokenization, wordpiece]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [WordPiece]
---

# WordPiece

> [!info] TL;DR
> WordPiece is BPE's cousin: instead of merging the most frequent pair, it merges the pair that **maximizes the likelihood of the training corpus**. Used by BERT, DistilBERT, Electra. Largely superseded by BPE for modern LLMs but still important for the BERT ecosystem.

## The Algorithm

WordPiece is identical to BPE in structure but differs in the merge criterion:

1. **Initialize** the vocabulary with all single characters.
2. **Represent each word** as a sequence of characters, with prefix markers (WordPiece uses `##` for non-initial subwords, e.g., `play` → `p ##l ##a ##y`).
3. **Score each candidate pair** by likelihood gain: $\frac{f(AB)}{f(A) \cdot f(B)}$.
4. **Merge** the highest-scoring pair. Add it to the vocabulary.
5. **Repeat** until the vocabulary reaches the target size.

The scoring function $\frac{f(AB)}{f(A) f(B)}$ is a likelihood ratio — it prefers pairs whose joint frequency is much higher than expected under independence.

## Worked Example

Corpus: `play playing played plays`

After character init:
```
p l a y
p l a y ##i ##n ##g
p l a y ##e ##d
p l a y ##s
```

Candidate pairs (with frequencies):
- `p l`: 4 / (4 × 4) = 0.25
- `l a`: 4 / (4 × 4) = 0.25
- `a y`: 4 / (4 × 4) = 0.25
- `y ##i`: 1 / (4 × 1) = 0.25
- `y ##e`: 1 / (4 × 1) = 0.25
- `y ##s`: 1 / (4 × 1) = 0.25

Top pair (by frequency tiebreak): `p l`. Merge → `pl`.

Continue: `pl a` (4 / 4×4 = 0.25), `a y` (4 / 4×4 = 0.25), merge → `pla`. Eventually `play` becomes a single token.

For "playing", `play ##ing` would be the eventual split — `##ing` itself becomes a token via repeated merges.

## Differences from BPE

| Aspect                | BPE                         | WordPiece                              |
|-----------------------|-----------------------------|----------------------------------------|
| Merge criterion       | Most frequent pair          | Pair with highest likelihood ratio     |
| Subword marker        | `</w>` (end-of-word)        | `##` (continuation prefix)             |
| Implementation        | Tiktoken, HF tokenizers     | HuggingFace tokenizers                 |
| Used by               | GPT-2/3/4, Llama, Mistral   | BERT, DistilBERT, Electra              |
| Handling whitespace   | Whitespace attached to next token | Whitespace splits words (pre-tokenized by spaces) |

## The `##` Convention

WordPiece uses `##` to mark subwords that **do not start a word**. This lets the model know whether a subword is at the start of a word (no `##`) or a continuation (with `##`). For example:

- `playing` → `play` + `##ing`
- `##ing` is a different token from `ing` (which would mean "ing" at the start of a word, like in "ingot").

This is different from BPE, where whitespace handling is in the pre-tokenization step (with ` ?` regex) rather than in the token representation.

## Worked Implementation Sketch

```python
# WordPiece scoring (simplified)
def score_pair(pair, pair_freq, a_freq, b_freq):
    return pair_freq / (a_freq * b_freq)

# Train loop similar to BPE but pick the highest-scoring pair
# rather than the most frequent pair.
```

In practice, you use HuggingFace `tokenizers.WordPiece` or `BertTokenizer`.

## Decoding

To decode WordPiece tokens back to text:
1. Concatenate all tokens.
2. Remove `##` prefixes (the next token attaches directly to the previous one).
3. Insert spaces between tokens that don't start with `##`.

```python
def decode_wordpiece(tokens):
    text = ""
    for tok in tokens:
        if tok.startswith("##"):
            text += tok[2:]
        else:
            if text:
                text += " "
            text += tok
    return text
```

## Why This Matters for AI

- WordPiece is **historically important** — it powered BERT, which kicked off the Transformer era for NLP.
- BERT-based models are still widely used in production for classification, NER, and embedding (via sentence-transformers).
- If you work with BERT-family models, you need to understand WordPiece.
- For modern decoder LLMs (Llama, Mistral, Qwen, GPT-4), BPE is the default — WordPiece is rare.

## Production Implications

- **Use `BertTokenizer` or `AutoTokenizer`** for BERT-family models. The vocabulary is fixed per model — never retrain.
- **`[UNK]` tokens are possible** with WordPiece (unlike byte-level BPE). If you encounter `[UNK]` in production, your input contains characters not in the vocabulary — rare but possible with unusual scripts.
- **Lowercasing** — original BERT's WordPiece was trained on lowercased text (`bert-base-uncased`). If you pass mixed-case text, results degrade. Use `bert-base-cased` if you need case sensitivity.

## Common Pitfalls

- **Passing mixed-case to uncased BERT** — silently produces wrong embeddings. Always check the model name (`-uncased` vs `-cased`).
- **Forgetting `[CLS]` and `[SEP]`** — BERT expects `[CLS] text [SEP]`. Most HuggingFace tokenizers add these automatically when called with `tokenizer(text)`, but raw encode/decode may not.
- **Confusing WordPiece with BPE** — they look similar but produce different vocabularies for the same corpus. Don't mix them.

## Further Reading

- Schuster & Nakajima (2012), *Japanese and Korean Voice Search* — original WordPiece.
- Wu et al. (2016), *Google's Neural Machine Translation System* — WordPiece for NMT.
- Devlin et al. (2019), *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*.

## WordPiece vs. BPE: Mathematical Comparison

The key difference is the merge criterion:

| Aspect              | BPE                          | WordPiece                          |
|---------------------|------------------------------|------------------------------------|
| Merge criterion     | Most frequent pair           | Highest likelihood ratio $\frac{f(AB)}{f(A) f(B)}$ |
| Optimizes           | Frequency of pairs           | Likelihood of corpus under tokenization |
| Theoretical basis   | Greedy frequency             | Maximum likelihood                 |
| Tends to merge      | Common pairs (even if expected) | Surprising pairs (more frequent than expected) |

### Why likelihood ratio differs from frequency
Consider two pairs:
- Pair "th": frequency 1000. "t" frequency 5000, "h" frequency 4000. Likelihood ratio = 1000 / (5000 × 4000) = 5e-5.
- Pair "qu": frequency 500. "q" frequency 600, "u" frequency 3000. Likelihood ratio = 500 / (600 × 3000) = 2.8e-4.

"qu" has lower frequency but higher likelihood ratio — because "q" is almost always followed by "u", making the pair more "surprising" (more frequent than independence would predict). WordPiece prefers "qu"; BPE prefers "th".

### Practical consequence
WordPiece tends to create tokens that capture **linguistic regularities** (q→u, tion, ing), while BPE tends to create tokens for **common sequences** (th, er, an). For English, the difference is small. For languages with rich morphology (German, Turkish), WordPiece may produce more linguistically meaningful subwords.

## The `##` Convention (Detailed)

WordPiece marks continuation subwords with `##`:
- `playing` → `play` + `##ing`
- `ingot` → `in` + `##got` (or `ingot` if it's in the vocabulary)
- `in` (start of word) is a different token from `##in` (continuation)

### Why this matters
1. **Position information**: the model knows whether a subword starts a word or continues one. This is positional information that BPE (which uses whitespace pre-tokenization) handles differently.
2. **Vocabulary efficiency**: `##ing` and `ing` are separate tokens, each learned from its context. The model learns that `##ing` is a suffix (verb conjugation, noun formation), while `ing` is a word-starter (e.g., "ingot", "ingredient").
3. **Decoding**: remove `##` and concatenate; insert space before non-`##` tokens. Unambiguous.

### Comparison with BPE whitespace handling
BPE uses a different convention: prepend a special marker (usually `Ġ` or `</w>`) to mark word boundaries. For example, " playing" becomes `Ġplay` + `ing` (the space is attached to the first subword). This achieves similar position information but with a different convention.

## WordPiece in the Modern LLM Ecosystem

### Models using WordPiece
- **BERT** (2018): 30K WordPiece vocab, uncased and cased variants.
- **DistilBERT**: same vocab as BERT.
- **Electra**: same vocab as BERT.
- **ALBERT**: same vocab as BERT.
- **MobileBERT**: same vocab as BERT.

### Models NOT using WordPiece
- **GPT-2/3/4, Llama, Mistral, Qwen**: BPE (byte-level).
- **T5**: SentencePiece (similar to BPE but with different conventions).
- **Gemini, Claude**: not publicly disclosed, likely BPE-based.

The BERT ecosystem (encoder-only models for classification/embedding) stuck with WordPiece. The decoder LLM ecosystem adopted BPE. This split reflects historical path dependence more than technical superiority.

### Why BPE won for LLMs
1. **Byte-level BPE** (GPT-2) can encode any text without `[UNK]` tokens — important for multilingual LLMs.
2. **BPE is simpler** to implement and understand.
3. **The GPT-2/Llama ecosystem** dominated the open-source LLM space, making BPE the de facto standard.
4. **WordPiece's advantages** (likelihood ratio, `##` convention) are minor for large-scale LLMs.

## Worked Example: WordPiece Tokenization in Practice

```python
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Basic tokenization
tokens = tokenizer.tokenize("Playing played plays player")
print(tokens)
# ['play', '##ing', 'play', '##ed', 'play', '##s', 'play', '##er']

# The `##` marks continuation subwords
# Notice: 'play' is the same token in all 4 words (shared root)

# Convert to IDs
ids = tokenizer.encode("Playing played plays player")
print(ids)
# [101, 2383, 2652, 2383, 2102, 2383, 2361, 2383, 2486, 102]
# 101 = [CLS], 102 = [SEP], 2383 = 'play', 2652 = '##ing', etc.

# Decode back
print(tokenizer.decode(ids))
# '[CLS] playing played plays player [SEP]'

# Handling unknown characters (rare with WordPiece)
tokens = tokenizer.tokenize("汉字 Chinese characters")
print(tokens)
# ['汉', '字', 'chinese', 'character', '##s']
# Chinese characters become individual tokens (not in vocab)
# Note: 'chinese' is a single token (lowercased)
```

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `[UNK]` tokens in output | Character not in WordPiece vocab | Use cased model; switch to byte-level BPE; expand vocab |
| Mixed-case text gives wrong results | Using uncased model on cased text | Use `bert-base-cased`; or lowercase input |
| Missing `[CLS]`/`[SEP]` | Manual encode/decode | Use `tokenizer(text)` which adds special tokens automatically |
| Different tokenization across model versions | Vocab mismatch | Pin model version; re-embed if vocab changes |
| WordPiece on non-English text | Vocab designed for English | Use multilingual BERT (`bert-base-multilingual`); or retrain vocab |

## Connection to Other Concepts

- [[05 - NLP Fundamentals/Tokenization/01 - Tokenization Overview|Tokenization Overview]] — the broader context.
- [[05 - NLP Fundamentals/Tokenization/02 - BPE|BPE]] — the dominant alternative.
- [[05 - NLP Fundamentals/Tokenization/04 - SentencePiece|SentencePiece]] — Google's multilingual tokenizer.
- [[05 - NLP Fundamentals/Embeddings/06 - Contextual Embeddings ELMo to BERT|Contextual Embeddings]] — BERT uses WordPiece.
- [[07 - Transformers/Encoder Models/07 - BERT|BERT]] — the model that popularized WordPiece.
- [[08 - LLMs/Architecture/01 - Decoder-Only Architecture|Decoder-Only Architecture]] — why LLMs use BPE instead.
- [[05 - NLP Fundamentals/Language Modeling/08 - Perplexity|Perplexity]] — tokenization affects PPL.

## Interview Questions

1. **Q: What's the difference between BPE and WordPiece merge criteria?**
   A: BPE merges the most frequent pair. WordPiece merges the pair with highest likelihood ratio $\frac{f(AB)}{f(A) f(B)}$. BPE optimizes for pair frequency; WordPiece optimizes for corpus likelihood. WordPiece prefers "surprising" pairs (more frequent than independence would predict), which tend to be linguistically meaningful (qu, tion, ing). BPE prefers common pairs (th, er, an), regardless of whether they're surprising.

2. **Q: Why does WordPiece use the `##` convention?**
   A: To mark continuation subwords: `playing` → `play` + `##ing`. This gives the model positional information (whether a subword starts a word or continues one). `##ing` (suffix) and `ing` (word-starter) are different tokens, each learned from its context. BPE achieves similar with a different convention (Ġ prefix for word-initial).

3. **Q: Why did BPE replace WordPiece for modern LLMs?**
   A: Four reasons. (1) Byte-level BPE (GPT-2) handles any text without `[UNK]` — important for multilingual. (2) BPE is simpler to implement. (3) The GPT-2/Llama ecosystem dominated open-source LLMs, making BPE the de facto standard. (4) WordPiece's advantages (likelihood ratio, `##`) are minor at scale. WordPiece remains in the BERT ecosystem (classification, embeddings).

4. **Q: When would you encounter `[UNK]` with WordPiece?**
   A: When the input contains characters not in the WordPiece vocabulary. Original BERT's vocab is English-focused — Chinese, Arabic, or rare Unicode characters may produce `[UNK]`. Byte-level BPE (GPT-2+) never produces `[UNK]` because all 256 bytes are in the base vocabulary. For non-English text with BERT, use `bert-base-multilingual` (110 languages) or switch to a BPE-based model.

5. **Q: How does WordPiece handle the word "unhappiness"?**
   A: WordPiece would tokenize it based on its vocabulary. Likely: `un` + `##happi` + `##ness` (if these subwords are in vocab) or `un` + `##happiness` (if "happiness" is a token) or character-by-character (if none of the subwords are in vocab). The exact tokenization depends on the vocabulary, which is learned from the training corpus. The `##` marks continuation: `un` starts the word, `##happi` and `##ness` continue it.

6. **Q: Why does uncased BERT produce wrong results on mixed-case input?**
   A: Uncased BERT was trained on lowercased text, so its vocabulary and embeddings are for lowercase tokens. If you pass "Apple" (the company), it's lowercased to "apple" (the fruit) — the model can't distinguish. Use `bert-base-cased` for tasks where case matters (NER, where "Apple" the company vs "apple" the fruit is important). Always check the model name (`-uncased` vs `-cased`) before using BERT.

## See Also

- [[Tokenization Overview]]
- [[BPE]]
- [[SentencePiece]]
- [[05 - NLP Fundamentals/MOC|NLP Fundamentals MOC]]