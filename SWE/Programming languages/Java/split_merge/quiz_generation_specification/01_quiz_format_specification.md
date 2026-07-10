# Quiz File Format — Definitive Specification

> **Status:** Authoritative reference. Any AI model generating quiz files MUST
> comply with every rule in this document. The Obsidian plugin that parses these
> files is strict: a single missing space, a wrong bracket, or an extra blank
> line is enough to break parsing for the entire file.
>
> **Audience:** AI models / chatbots that generate quiz Markdown, and humans who
> review or hand-edit the output.
>
> **Scope:** A single quiz file (one `.md` file). A typical quiz contains 30
> questions distributed across three types (10 True/False, 10 Multiple Choice,
> 10 Matching), but the format itself places no hard limit on counts.

---

## Table of Contents

1. [File-Level Anatomy](#1-file-level-anatomy)
2. [YAML Frontmatter](#2-yaml-frontmatter)
3. [Body Structure](#3-body-structure)
4. [Obsidian Callout Refresher](#4-obsidian-callout-refresher)
5. [Question Type 1 — True / False](#5-question-type-1--true--false)
6. [Question Type 2 — Multiple Choice](#6-question-type-2--multiple-choice)
7. [Question Type 3 — Matching](#7-question-type-3--matching)
8. [Cross-Cutting Rules](#8-cross-cutting-rules)
9. [Mandatory vs Optional Fields](#9-mandatory-vs-optional-fields)
10. [Edge Cases & Assumptions](#10-edge-cases--assumptions)
11. [Character & Encoding Rules](#11-character--encoding-rules)
12. [Validation Criteria](#12-validation-criteria)
13. [Reference: Full Minimal Example](#13-reference-full-minimal-example)

---

## 1. File-Level Anatomy

A quiz file is a plain UTF-8 Markdown document with exactly two top-level
sections, in this order:

```
┌────────────────────────────────────────────────┐
│  YAML FRONTMATTER                              │   ← metadata block
│  (delimited by lines containing exactly "---") │
├────────────────────────────────────────────────┤
│  (exactly one blank line)                      │
├────────────────────────────────────────────────┤
│  BODY                                          │   ← question callouts
│  (sequence of Obsidian callout blocks)         │
└────────────────────────────────────────────────┘
```

There is no title, no table of contents, no headings, no prose between
questions. The body is a flat list of callout blocks separated by exactly one
blank line.

**File extension:** `.md` (mandatory).
**Encoding:** UTF-8, no BOM.
**Line endings:** `\n` (Unix). Do not use `\r\n`.
**Trailing newline:** The file MUST end with a single `\n` after the last
non-empty line. No trailing blank lines.

---

## 2. YAML Frontmatter

### 2.1 Structure

The file MUST begin on line 1 with a YAML frontmatter block:

```markdown
---
sources:
  - "[[Chapter 1 - Introduction to Cloud Computing/1.1 Cloud Computing Definition and Foundations.md]]"
  - "[[Chapter 1 - Introduction to Cloud Computing/1.2 Historical Evolution of Computing Paradigms.md]]"
---
```

### 2.2 Rules

| Rule ID | Rule |
|---------|------|
| FM-1 | Line 1 of the file MUST be exactly `---` (three hyphens, nothing else). |
| FM-2 | The frontmatter MUST contain a top-level `sources:` key. |
| FM-3 | `sources:` MUST be a YAML list. Each entry is a string. |
| FM-4 | Each source entry MUST be an Obsidian wikilink of the form `[[...]]`, wrapped in double quotes inside the YAML string. |
| FM-5 | The closing `---` MUST be on its own line. |
| FM-6 | Between the opening `---` and `sources:` there MUST be no other keys, comments, or blank lines. |
| FM-7 | Indentation for list items under `sources:` is exactly **two spaces** followed by `- `. |
| FM-8 | The frontmatter MUST NOT contain tabs. |
| FM-9 | No key other than `sources:` is consumed by the parser. Extra keys are tolerated but discouraged. |

### 2.3 Field: `sources`

* **Type:** list of strings.
* **Mandatory:** yes. A quiz file without `sources:` is invalid.
* **Each entry** must be a double-quoted YAML string whose value is an Obsidian
  wikilink `[[Target Note Name.md]]` or `[[Folder/Note Name.md]]`.
* **Path style:** forward slashes `/` separate folder levels. The `.md`
  extension at the end is conventional but not enforced by the parser; keep it
  for consistency with the existing corpus.
* **Minimum count:** the parser emits a *warning* (not an error) if no
  `[[...]]` wikilink is detected in the frontmatter. In practice, every quiz
  should list at least one source note.

### 2.4 Example — Correct Frontmatter

```yaml
---
sources:
  - "[[Chapter 6 - Virtual and Networked Storage/6.1 Storage Foundations and Access Models.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.2 Networked Storage Architectures - DAS NAS SAN.md]]"
---
```

### 2.5 Example — Invalid Frontmatter (each one fails)

```yaml
# BAD: line 1 is not exactly "---"
sources:
  - "[[Note.md]]"
---
```

```yaml
---
# BAD: missing 'sources:' key
title: My Quiz
---
```

```yaml
---
sources:
- "[[Note.md]]"      # BAD: list item not indented by two spaces
---
```

```yaml
---
sources:
  - [[Note.md]]       # BAD: wikilink not wrapped in double quotes
---
```

---

## 3. Body Structure

### 3.1 Layout

After the closing `---` of the frontmatter there MUST be **exactly one blank
line**, then the body begins. The body is a sequence of one or more Obsidian
callout blocks. Every callout block represents exactly one question.

Two consecutive question blocks are separated by exactly one blank line:

```
> [!question] ...question 1 content...
>> [!success]- Answer
>> ...

                                              ← exactly one blank line
> [!question] ...question 2 content...
>> [!success]- Answer
>> ...
```

### 3.2 Body Rules

| Rule ID | Rule |
|---------|------|
| BD-1 | The body MUST contain at least one question block. |
| BD-2 | Question blocks MUST be separated by exactly one blank line. |
| BD-3 | There MUST be no Markdown headings (`#`, `##`, etc.) anywhere in the body. |
| BD-4 | There MUST be no thematic section dividers like `---` between questions. |
| BD-5 | There MUST be no prose, commentary, or "Section 1: True/False" labels. |
| BD-6 | Questions may appear in any order; the format does not require grouping by type. |
| BD-7 | The body MUST NOT be wrapped in a Markdown code fence. |
| BD-8 | No trailing blank lines at the end of the file beyond the single terminating `\n`. |

---

## 4. Obsidian Callout Refresher

The whole format hinges on Obsidian's callout syntax. A callout is a blockquote
whose first line starts with `> [!TYPE]`. Subsequent `>`-prefixed lines belong
to the same callout until a non-`>` line (or a blank line) ends it.

This format uses three callout types:

| Callout type | Purpose | Prefix |
|--------------|---------|--------|
| `[!question]` | Wraps the question itself. | `> ` (one `>` then one space) |
| `[!success]- Answer` | Wraps the answer. The `-` makes it collapsible. | `>> ` (two `>` then one space) |
| `[!example]` | Wraps a group inside a matching question. | `>> ` (two `>` then one space) |

### 4.1 The two prefix levels — CRITICAL

The format uses **two distinct quote depths**:

* **Depth 1 — `> `** (single greater-than, single space): used for the
  `[!question]` opener and for multiple-choice option lines.
* **Depth 2 — `>> `** (two greater-thans, single space): used for the
  `[!success]- Answer` callout, the answer body, `[!example]` group blocks,
  and matching item lines.

Mixing these depths breaks the parser. When in doubt, remember:
**the answer block is *nested inside* the question block**, so it gets one
extra `>`.

### 4.2 The foldable marker `-`

`[!success]- Answer` contains a hyphen `-` immediately after the type and
before the space that precedes the title. This is Obsidian's "default-collapsed"
syntax. Without the `-`, the callout renders expanded and the plugin cannot
locate the answer. **The `-` is mandatory.**

### 4.3 The literal title `Answer`

After `[!success]-` comes a single space and then the literal word `Answer`
(capitalized exactly like that). The parser matches the literal string
`[!success]- Answer`. Variants like `[!success]-Answers`,
`[!success]- Answer:`, or `[!success]- Correct Answer` are NOT recognised.

---

## 5. Question Type 1 — True / False

### 5.1 Anatomy

```
> [!question] <statement>
>> [!success]- Answer
>> True
```

Or, with the false answer:

```
> [!question] <statement>
>> [!success]- Answer
>> False
```

### 5.2 Rules

| Rule ID | Rule |
|---------|------|
| TF-1 | Line 1: `> [!question] ` followed by exactly one space and then the statement text on the same line. |
| TF-2 | Line 2: `>> [!success]- Answer` (exact string, no trailing colon, no extra text). |
| TF-3 | Line 3: `>> True` or `>> False` — capitalised exactly, no period, no extra text. |
| TF-4 | The statement text MUST NOT contain a newline; the entire question lives on one line. |
| TF-5 | There MUST be no options (`a)`, `b)`, ...) and no `[!example]` blocks. Presence of either re-classifies the question as a different type and breaks TF classification. |
| TF-6 | The answer MUST be `True` or `False` (no `T`/`F`, no `Yes`/`No`, no `TRUE`/`FALSE`). |

### 5.3 Example

```markdown
> [!question] The XML declaration is optional and is not required for a valid XML document.
>> [!success]- Answer
>> False
```

### 5.4 Common Mistakes

* Forgetting the `-` and writing `>> [!success] Answer`.
* Writing the answer on the same line as the callout title:
  `>> [!success]- Answer: False` — invalid.
* Lowercase answer: `>> false` — invalid; the parser expects `True` or `False`.
* Adding options: this stops being a True/False question.

---

## 6. Question Type 2 — Multiple Choice

### 6.1 Anatomy

```
> [!question] <question text>
> a) <option a>
> b) <option b>
> c) <option c>
> d) <option d>
>> [!success]- Answer
>> <letter>) <full option text repeated>
```

### 6.2 Rules

| Rule ID | Rule |
|---------|------|
| MC-1 | Line 1: `> [!question] ` + space + question text on the same line. |
| MC-2 | The next lines are the options, each at depth 1: `> a) text`, `> b) text`, etc. |
| MC-3 | Option letters MUST be lowercase: `a)`, `b)`, `c)`, `d)`. Uppercase `A)` is invalid. |
| MC-4 | Each option letter MUST be immediately followed by `)` (close-paren) and then one space. No `.` after the parenthesis. No `a.` or `a)`. |
| MC-5 | There MUST be at least two options. Four is the conventional count; the parser accepts any count ≥ 2 within the range `a`–`d` (so practically 2, 3, or 4 options). |
| MC-6 | After the last option line, the next line is `>> [!success]- Answer`. |
| MC-7 | The answer line is `>> ` followed by the chosen option letter, `)`, a space, and the full text of that option. |
| MC-8 | The answer letter MUST be one of the option letters actually present above. |
| MC-9 | There MUST be exactly one correct answer. Multi-answer questions are not supported by this format. |
| MC-10 | The answer text should match the option text verbatim. The parser primarily checks the letter; matching the text is conventional. |
| MC-11 | There MUST be NO `[!example]` blocks. Presence of `[!example]` re-classifies the question as Matching. |
| MC-12 | There MUST be no blank lines between the question line, the option lines, and the answer callout. The whole question is a single contiguous blockquote. |

### 6.3 Example

```markdown
> [!question] Which attribute in the XML declaration specifies the character encoding used?
> a) encoding
> b) version
> c) standalone
> d) charset
>> [!success]- Answer
>> a) encoding
```

### 6.4 Common Mistakes

* Adding a blank line between the options and the answer callout — this
  terminates the blockquote and breaks parsing.
* Using uppercase letters: `> A) encoding` — invalid.
* Using a period: `> a. encoding` — invalid; must be `a)`.
* Writing only the letter in the answer: `>> a)` without the option text —
  tolerated by the parser but inconsistent with the corpus; always repeat the
  full option text.
* Listing multiple correct answers — the format is single-answer only.
* Forgetting the `)`: `>> a encoding` — invalid.

---

## 7. Question Type 3 — Matching

### 7.1 Anatomy

A matching question has **two item groups** (Group A and Group B) and an answer
block that maps each Group A item to a Group B item.

```
> [!question] <match instruction>
>> [!example] Group A
>> a) <item a>
>> b) <item b>
>> c) <item c>
>> d) <item d>
>
>> [!example] Group B
>> n) <item n>
>> o) <item o>
>> p) <item p>
>> q) <item q>
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
```

### 7.2 The divider line — CRITICAL

Between Group A and Group B, and between Group B and the Answer, there is a
line containing exactly `>` (one greater-than, no trailing space, no other
text). This is the divider that separates nested callouts inside the outer
question blockquote. **Forgetting this divider, or using `>>` instead of `>`,
breaks the parser.**

### 7.3 Letter conventions

* **Group A** uses lowercase letters starting at `a)`: `a)`, `b)`, `c)`, `d)`, …
* **Group B** uses lowercase letters starting at `n)`: `n)`, `o)`, `p)`, `q)`, …
  This continuation past `m` is intentional: it makes the two groups visually
  and lexically distinct, so the parser can tell which side of a mapping each
  letter belongs to.
* Both groups MUST have the same number of items. The conventional count is 4
  per group (so 4 mappings in the answer), but any count ≥ 2 works as long as
  both groups match.
* Group B's letters continue alphabetically from `n` regardless of Group A's
  size. So if Group A has 4 items, Group B is `n, o, p, q`. If Group A has 5
  items, Group B is `n, o, p, q, r`.

### 7.4 Answer format

Each mapping line is:

```
>> <group-a-letter>) -> <group-b-letter>)
```

* `>>` prefix (depth 2).
* A Group A letter, immediately followed by `)`.
* A single space.
* The literal arrow `->` (hyphen + greater-than, no spaces inside).
* A single space.
* A Group B letter, immediately followed by `)`.

So the full pattern is: `>> a) -> n)`.

Acceptable variants the parser tolerates: none. Use exactly `->` with one
space on each side. Do NOT use `=>`, `→`, `-->`, `>>`, or any other arrow.

### 7.5 Rules

| Rule ID | Rule |
|---------|------|
| MT-1 | Line 1: `> [!question] ` + space + match instruction. |
| MT-2 | Line 2: `>> [!example] Group A` (literal title `Group A`). |
| MT-3 | Subsequent lines: `>> a) item`, `>> b) item`, … |
| MT-4 | After Group A's last item: exactly one line containing `>` (depth-1 divider). |
| MT-5 | Next line: `>> [!example] Group B` (literal title `Group B`). |
| MT-6 | Subsequent lines: `>> n) item`, `>> o) item`, … |
| MT-7 | After Group B's last item: exactly one line containing `>`. |
| MT-8 | Next line: `>> [!success]- Answer`. |
| MT-9 | Mapping lines: `>> <A-letter>) -> <B-letter>)` for each pair, in Group A order. |
| MT-10 | Every Group A letter MUST appear exactly once on the left of `->`. |
| MT-11 | Every Group B letter MUST appear exactly once on the right of `->`. |
| MT-12 | No `[!example]` titles other than `Group A` and `Group B`. |
| MT-13 | No options at depth 1 (`> a) ...`). If depth-1 option lines are present, the question is misclassified. |

### 7.6 Example

```markdown
> [!question] Match the XML declaration attribute with its description.
>> [!example] Group A
>> a) encoding
>> b) version
>> c) standalone
>
>> [!example] Group B
>> n) Specifies the XML version being used.
>> o) Indicates whether the document relies on external markup declarations.
>> p) Specifies the character encoding used.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
```

Note that the mappings need not be alphabetical: in the example above, `a`
maps to `p` (not `n`), which is correct because `encoding` corresponds to
"Specifies the character encoding used."

### 7.7 Common Mistakes

* Using `>>` instead of `>` for the divider line.
* Adding a space after `>` on the divider line (`> ` instead of `>`).
* Using `=>` or `→` instead of `->`.
* Putting a space inside the arrow: `> ->` or `- >`.
* Forgetting the `)` after the Group B letter in the answer:
  `>> a) -> n` (missing close-paren) — invalid.
* Starting Group B at `a)` instead of `n)`.
* Using a different number of items in Group A vs Group B.
* Adding extra `[!example]` groups (Group C, etc.) — unsupported.

---

## 8. Cross-Cutting Rules

These rules apply to every question type.

| Rule ID | Rule |
|---------|------|
| CC-1 | Every question MUST start with `> [!question] ` (single `>`, single space, literal type, single space). |
| CC-2 | Every question MUST contain exactly one `>> [!success]- Answer` callout. |
| CC-3 | The answer callout MUST be the last callout inside the question block. |
| CC-4 | A question MUST be classifiable as exactly one type (TF, MC, or Matching). Questions that match multiple type signatures are flagged as a structural conflict. |
| CC-5 | No empty lines inside a question block (between the `[!question]` opener and the answer body). The only allowed "divider" lines are the single `>` lines inside matching questions. |
| CC-6 | No Markdown formatting that breaks the blockquote: no indented code blocks, no fenced code blocks, no tables, no images. Inline formatting (`**bold**`, `*italic*`, `` `code` ``) inside the text is acceptable but discouraged inside option items. |
| CC-7 | No HTML tags. |
| CC-8 | No emoji. The emoji purge pipeline will strip them, but their presence indicates a formatting mistake. |
| CC-9 | Question and option text MUST be on a single line. No soft wraps, no manual line breaks. |
| CC-10 | Trim trailing whitespace from every line. |
| CC-11 | The file MUST NOT contain tab characters anywhere. Use spaces. |

---

## 9. Mandatory vs Optional Fields

### 9.1 Mandatory

| Field | Location | Format |
|-------|----------|--------|
| Frontmatter opening `---` | Line 1 | Literal |
| `sources:` key | Frontmatter | YAML key |
| At least one `[[...]]` wikilink | Under `sources:` | Double-quoted YAML string |
| Frontmatter closing `---` | After sources | Literal |
| `> [!question] <text>` | Each question | Single line |
| `>> [!success]- Answer` | Each question | Literal |
| Answer body | Each question | Type-specific |
| Options `a) b) c) d)` | MC questions | Depth-1 lines |
| `[!example] Group A` and `Group B` | Matching questions | Depth-2 lines |
| `>` divider lines | Matching questions | Depth-1, no trailing space |

### 9.2 Optional

| Field | Default | Notes |
|-------|---------|-------|
| Number of sources | — | One or more; no upper limit. |
| Number of questions per file | — | Convention is 30 (10/10/10); parser accepts any count ≥ 1. |
| Number of options per MC question | 4 | Minimum 2, maximum 4 (letters `a`–`d`). |
| Number of items per matching group | 4 | Minimum 2; both groups must match. |
| Other frontmatter keys (`title`, `tags`, …) | none | Tolerated but ignored by the parser. |

### 9.3 Forbidden

| Field | Why |
|-------|-----|
| Markdown headings (`#`, `##`, …) | Not part of the format; breaks the flat callout list. |
| Horizontal rules (`---`) inside the body | Conflicts with frontmatter delimiter semantics. |
| Code fences (` ``` `) in the body | Breaks the blockquote. |
| Tables, images, HTML | Breaks the blockquote. |
| Comments (`<!-- -->`) | Not stripped; may confuse the parser. |
| Section labels like `## True/False` | Not part of the format. |
| Question numbers (`1.`, `2.`, …) | Not part of the format. |

---

## 10. Edge Cases & Assumptions

### 10.1 Whitespace

* **Tabs are forbidden.** A single tab character anywhere in the file is a
  formatting violation. Always use spaces.
* **Trailing whitespace on a line is forbidden.** Many editors strip this
  automatically; when generating, ensure no line ends with spaces.
* **The blank line between two questions** must be truly empty (zero
  characters). Not a line with two spaces, not a line with `>`.
* **The `>` divider line in matching questions** must be exactly `>` with no
  trailing space and no leading space. (It is at column 0.)

### 10.2 Text content inside questions

* **Special characters in question text** (`:`, `-`, `(`, `)`, `?`, `!`, `/`,
  etc.) are allowed as long as they don't break the blockquote. Avoid leading
  the question text with `>`, `[!`, or `#` because the parser may misinterpret
  them.
* **Quotes inside question text:** use straight quotes `"` or `'`. Curly
  quotes are tolerated but discouraged.
* **Numbers, units, percentages, dates:** write them inline in plain text.
  Avoid surrounding them with backticks (`` ` ``) inside option items, since
  some plugin versions mishandle inline code inside callouts.
* **Ampersands and angle brackets** (`&`, `<`, `>`): these are valid Markdown
  characters. Avoid them at the start of a line (where they may be
  misinterpreted) but they are fine mid-line.

### 10.3 Length

* **Question text length:** no hard limit. Keep questions under ~300 characters
  for readability.
* **Option / item text length:** no hard limit. Keep under ~150 characters.
* **File length:** no hard limit. A 30-question file is typically 200–400
  lines.

### 10.4 Order of question types

The format does not require grouping by type. The existing corpus groups them
(TF block first, then MC, then Matching) for human readability. The parser
detects type from structural cues, not from position. When generating, follow
the convention of grouping by type for consistency with the corpus.

### 10.5 Multiple files per chapter

The original prompt mentions "2 quiz files per chapter." This is a
*workflow-level* instruction, not a format rule. Each file is independent and
must individually conform to this specification. The two files in a chapter
typically share the same `sources:` list and cover overlapping but not
identical content.

### 10.6 The `sources:` list

* The same source may appear in multiple files.
* Sources are not required to be sorted alphabetically, but the corpus
  convention is to list them in the order they appear in the chapter.
* The path inside `[[...]]` is relative to the Obsidian vault root, not to the
  quiz file. Forward slashes separate folders.

### 10.7 What the parser does NOT check

The parser checks structure only. It does NOT check:

* Factual correctness of answers.
* Whether the answer letter actually matches the correct option text.
* Whether matching mappings are factually correct.
* Whether the question text is meaningful or well-phrased.
* Whether the same question appears twice.
* Whether sources actually exist in the vault.

These are content-quality concerns, handled by human review.

---

## 11. Character & Encoding Rules

| Concern | Rule |
|---------|------|
| File encoding | UTF-8, no BOM. |
| Line endings | `\n` (Unix). |
| Tabs | Forbidden everywhere. |
| Non-breaking spaces | Forbidden; use regular spaces. |
| Zero-width characters | Forbidden. |
| Emoji | Forbidden (the purge pipeline removes them, but their presence indicates a mistake). |
| Curly quotes / smart punctuation | Discouraged; use straight ASCII quotes. |
| Em-dashes and en-dashes | Discouraged inside option items; use `-` or `:`. |
| Arrow characters (`→`, `⇒`) | Forbidden in matching answers; use `->`. |
| Trailing whitespace | Forbidden on any line. |

---

## 12. Validation Criteria

A file is **valid** if and only if all of the following hold:

1. The file starts with `---\n` (frontmatter opener).
2. The frontmatter contains a `sources:` key.
3. The frontmatter contains at least one `[[...]]` wikilink (warning if
   missing, but does not by itself invalidate the file).
4. The frontmatter is properly closed by a line containing exactly `---`.
5. The body is non-empty.
6. Every question block in the body can be classified as exactly one of:
   True/False, Multiple Choice, or Matching.
7. Every question block contains a `>> [!success]- Answer` callout.
8. Every Multiple Choice question has at least two options and an answer letter
   that exists among the options.
9. Every Matching question has both `Group A` and `Group B`, with divider
   lines, and a complete one-to-one mapping.
10. No structural conflicts (a question matching multiple type signatures).

A file is **invalid** if any of the above fail. The validator returns a list
of `(line_number, message)` errors and a stats dictionary
`{"true_false": N, "multiple_choice": N, "matching": N}`.

---

## 13. Reference: Full Minimal Example

A complete, minimal, parser-valid quiz file with one question of each type:

```markdown
---
sources:
  - "[[Sample/Note.md]]"
---

> [!question] The sky is blue on a clear day.
>> [!success]- Answer
>> True

> [!question] What color is the sky on a clear day?
> a) Green
> b) Blue
> c) Red
> d) Yellow
>> [!success]- Answer
>> b) Blue

> [!question] Match the color with its typical sky condition.
>> [!example] Group A
>> a) Blue
>> b) Gray
>> c) Orange
>> d) Black
>
>> [!example] Group B
>> n) Clear daytime sky
>> o) Overcast sky
>> p) Sunset or sunrise
>> q) Night sky
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
```

This file passes every rule in this specification and is the canonical
reference for AI models generating new quiz files.
