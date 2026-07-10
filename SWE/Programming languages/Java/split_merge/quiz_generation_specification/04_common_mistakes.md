# Common AI Mistakes — Annotated Catalogue

> This document enumerates the most frequent mistakes AI models make when
> generating quiz files in this format. Each mistake is shown with an example
> of the wrong output, an explanation of why it breaks the parser, and the
> correct alternative.
>
> The catalogue is derived from the structure of the existing corpus (18 quiz
> files across 9 chapters) and from the validator's classification rules in
> `vault_manager/services/validator.py`. Mistakes are grouped by category.

---

## Category A — Callout Syntax Errors

### A1. Missing `-` in the answer callout

**Wrong:**
```markdown
> [!question] The sky is blue.
>> [!success] Answer
>> True
```

**Why it breaks:** The parser's regex for the answer callout is
`>>\s*\[!success\]-\s*Answer`. Without the `-`, the regex fails to match and
the question is unclassifiable.

**Correct:**
```markdown
> [!question] The sky is blue.
>> [!success]- Answer
>> True
```

### A2. Answer on the same line as the callout title

**Wrong:**
```markdown
> [!question] The sky is blue.
>> [!success]- Answer: True
```

**Why it breaks:** The parser expects the answer on the line *after* the
callout title, prefixed with `>> `. Putting it on the same line means there is
no `>> True` or `>> False` line, so the TF regex fails.

**Correct:**
```markdown
> [!question] The sky is blue.
>> [!success]- Answer
>> True
```

### A3. Using `[!success]` with a different title

**Wrong variants:**
* `>> [!success]- Answers`
* `>> [!success]- Correct Answer`
* `>> [!success]- Answer:`
* `>> [!success] Answer`
* `>> [!answer] True`

**Why it breaks:** The parser matches the literal string
`[!success]- Answer`. Any variation fails the match.

**Correct:** `>> [!success]- Answer` (exact string).

### A4. Wrong callout type for the question opener

**Wrong:**
```markdown
> [!quiz] The sky is blue.
> [!note] The sky is blue.
> [!q] The sky is blue.
```

**Why it breaks:** The parser only recognises `[!question]`.

**Correct:** `> [!question] <text>`.

---

## Category B — Quote Depth Errors (`>` vs `>>`)

### B1. Using `>` instead of `>>` for the answer callout

**Wrong:**
```markdown
> [!question] The sky is blue.
> [!success]- Answer
> True
```

**Why it breaks:** The answer callout must be nested inside the question
blockquote (depth 2). At depth 1, the parser sees it as a separate top-level
callout, so the question has no answer callout and is unclassifiable.

**Correct:**
```markdown
> [!question] The sky is blue.
>> [!success]- Answer
>> True
```

### B2. Using `>>` instead of `>` for MC options

**Wrong:**
```markdown
> [!question] What color is the sky?
>> a) Blue
>> b) Green
```

**Why it breaks:** The MC classifier looks for options at depth 1
(regex `>\s+[a-d]\)`). At depth 2 they are invisible to the MC classifier,
so the question may be misclassified as TF (no options) or Matching (depth-2
items look like matching items).

**Correct:**
```markdown
> [!question] What color is the sky?
> a) Blue
> b) Green
```

### B3. Using `>>` for the matching divider line

**Wrong:**
```markdown
> [!question] Match the items.
>> [!example] Group A
>> a) item
>> b) item
>>
>> [!example] Group B
```

**Why it breaks:** The divider line is what tells the parser that Group A has
ended. A `>>` line is treated as continuation of Group A, so the parser never
sees a clear boundary and may merge the two groups.

**Correct:** The divider line is **bare `>`** (depth 1, no trailing space):
```markdown
> [!question] Match the items.
>> [!example] Group A
>> a) item
>> b) item
>
>> [!example] Group B
```

### B4. Trailing space on the matching divider line

**Wrong:** (the line is `> ` with a trailing space, invisible in most editors)
```
>
```
…where the line actually contains `> ` (greater-than + space).

**Why it breaks:** Some plugin versions treat `> ` (with trailing space) as
continuation of the previous blockquote content rather than a structural
divider. The validator's strict mode flags this.

**Correct:** The line must be exactly `>` followed by a newline — no space.

---

## Category C — Option & Letter Errors

### C1. Uppercase option letters

**Wrong:**
```markdown
> A) Blue
> B) Green
```

**Why it breaks:** The MC regex is `>\s+[a-d]\)` — lowercase only. Uppercase
options are invisible to the classifier.

**Correct:** Lowercase `a)`, `b)`, `c)`, `d)`.

### C2. Period instead of close-paren

**Wrong:**
```markdown
> a. Blue
> b. Green
```

**Why it breaks:** Same regex — `a)` is required, `a.` does not match.

**Correct:** `a) Blue`.

### C3. No space after `)`

**Wrong:**
```markdown
> a)Blue
```

**Why it breaks:** The regex expects `>\s+[a-d]\)\s+` — a space after `)`.

**Correct:** `> a) Blue`.

### C4. Group B starting at `a)` instead of `n)`

**Wrong:**
```markdown
>> [!example] Group B
>> a) First B item
>> b) Second B item
```

**Why it breaks:** The matching classifier looks for Group B items using the
range `n-z`. If Group B starts at `a)`, those items are classified as
additional Group A items, leading to a structural conflict.

**Correct:** Group B starts at `n)`:
```markdown
>> [!example] Group B
>> n) First B item
>> o) Second B item
```

### C5. Missing `)` after the Group B letter in the answer

**Wrong:**
```markdown
>> a) -> n
>> b) -> o
```

**Why it breaks:** The answer regex is `>>\s*[a-z]\)\s*->\s*[a-z]\)`. Both
letters must be followed by `)`.

**Correct:** `>> a) -> n)`.

---

## Category D — Arrow Errors in Matching

### D1. Using `=>` instead of `->`

**Wrong:** `>> a) => n)`

**Correct:** `>> a) -> n)`.

### D2. Using the Unicode arrow `→`

**Wrong:** `>> a) → n)`

**Correct:** `>> a) -> n)`.

### D3. No spaces around the arrow

**Wrong:** `>> a)->n)`

**Why it breaks:** The regex expects `\s*->\s*` — actually the regex is
lenient on inner whitespace, but the corpus convention and the validator's
strict mode expect one space on each side. Always use `a) -> n)`.

**Correct:** `>> a) -> n)`.

### D4. Using `-->` (double hyphen)

**Wrong:** `>> a) --> n)`

**Correct:** `>> a) -> n)`.

---

## Category E — Structural Errors

### E1. Blank line inside a question block

**Wrong:**
```markdown
> [!question] What color is the sky?
> a) Blue

> b) Green
>> [!success]- Answer
>> a) Blue
```

**Why it breaks:** A blank line terminates the blockquote. The parser then
sees two separate callouts and tries to classify each one. The second callout
(`> b) Green`) has no `[!question]` opener and is unclassifiable.

**Correct:** No blank lines inside a question:
```markdown
> [!question] What color is the sky?
> a) Blue
> b) Green
>> [!success]- Answer
>> a) Blue
```

### E2. Headings inside the body

**Wrong:**
```markdown
## True / False

> [!question] ...
```

**Why it breaks:** The body must be a flat list of callouts. Headings break
the flat structure and may confuse the parser's question-block splitter.

**Correct:** No headings. Just callouts separated by one blank line.

### E3. Numbering the questions

**Wrong:**
```markdown
1. > [!question] ...
2. > [!question] ...
```

**Why it breaks:** The `1.` prefix breaks the blockquote. The parser sees a
Markdown ordered list, not a callout.

**Correct:** No numbering. The questions are an unordered list of callouts.

### E4. Wrapping the file in a code fence

**Wrong:**
````markdown
```markdown
---
sources:
  - "[[Note.md]]"
---
...
```
````

**Why it breaks:** The frontmatter opener `---` is then inside a code block,
so the YAML parser does not see it as a frontmatter delimiter.

**Correct:** No outer code fence. The file starts directly with `---`.

### E5. Horizontal rule between questions

**Wrong:**
```markdown
> [!question] Q1
>> [!success]- Answer
>> True

---

> [!question] Q2
```

**Why it breaks:** `---` inside the body is ambiguous (it can be parsed as a
frontmatter delimiter or as a horizontal rule) and breaks the flat callout
structure.

**Correct:** Use a single blank line to separate questions. No `---`.

### E6. Multiple `[!success]` blocks in one question

**Wrong:**
```markdown
> [!question] ...
>> [!success]- Answer
>> a) Blue
>> [!success]- Explanation
>> Because of Rayleigh scattering.
```

**Why it breaks:** The format supports exactly one answer callout per
question. Extra callouts may shift the parser's classification.

**Correct:** One answer callout per question. No explanations.

---

## Category F — Frontmatter Errors

### F1. Missing `sources:` key

**Wrong:**
```yaml
---
title: Chapter 1 Quiz
---
```

**Why it breaks:** The validator explicitly checks for the `sources:` string
in the frontmatter. Without it, the file is flagged as invalid.

**Correct:** Always include `sources:`.

### F2. Wikilink not double-quoted

**Wrong:**
```yaml
---
sources:
  - [[Note.md]]
---
```

**Why it breaks:** YAML may parse `[[Note.md]]` as a flow-style nested
sequence, not as a string. The validator's regex `\[\[.*?\]\]` will still
match, but downstream YAML consumers may fail.

**Correct:** Wrap each entry in double quotes:
```yaml
  - "[[Note.md]]"
```

### F3. Wrong list indentation

**Wrong:**
```yaml
---
sources:
- "[[Note.md]]"
---
```

**Why it breaks:** While this is valid YAML (block sequences can be indented
at the same level as the parent key), the corpus convention is two-space
indentation. Some strict YAML consumers may also treat this differently. Use
the convention to be safe.

**Correct:** Two-space indentation:
```yaml
---
sources:
  - "[[Note.md]]"
---
```

### F4. Frontmatter not on line 1

**Wrong:**
```markdown

---
sources:
  - "[[Note.md]]"
---
```

(a blank line at the top of the file)

**Why it breaks:** The validator checks `content.startswith("---\n")`. A
leading blank line means the file does not start with `---\n`.

**Correct:** Line 1 is exactly `---`.

---

## Category G — Content & Encoding Errors

### G1. Emoji anywhere in the file

**Wrong:** `> [!question] 🌤️ The sky is blue.`

**Why it breaks:** The validator does not directly reject emoji, but the
separate emoji-purge pipeline will strip them, which can shift line content
and break callout classification. More fundamentally, emoji are not part of
the format.

**Correct:** No emoji.

### G2. Tabs for indentation

**Wrong:** A frontmatter or option line indented with a tab character.

**Why it breaks:** Tabs are not consistently handled by YAML parsers or by
the regex classifier. Use spaces.

**Correct:** Spaces only.

### G3. Trailing whitespace on any line

**Wrong:** A line ending with spaces (invisible in most editors).

**Why it breaks:** Trailing whitespace can shift the regex match for the
matching divider line (`>` vs `> `) and other strict patterns.

**Correct:** No trailing whitespace on any line.

### G4. CRLF line endings

**Wrong:** File saved with Windows `\r\n` line endings.

**Why it breaks:** The validator's `content.startswith("---\n")` check fails
if the line ending is `\r\n` (because `---\r\n` != `---\n`). Other regexes
may also behave unexpectedly.

**Correct:** Unix `\n` line endings.

### G5. No trailing newline at end of file

**Wrong:** The last line of the file has no terminating `\n`.

**Why it breaks:** Some text processing tools (and the parser's last-block
detection) expect a final newline. While the validator tolerates this, the
convention is to always end the file with a newline.

**Correct:** End the file with a single `\n` after the last answer line.

### G6. Multiple trailing blank lines

**Wrong:** Several blank lines at the end of the file.

**Why it breaks:** May cause the parser to attempt classifying an empty
"question block" at the end, producing spurious errors.

**Correct:** Exactly one `\n` after the last answer line. No extra blank
lines.

---

## Category H — Workflow Errors

### H1. Generating only one file when two were requested

The workflow asks for two files per chapter (`_Quiz_A.md` and `_Quiz_B.md`).
Some AI models generate only one. Both must be produced.

### H2. Inventing the chapter folder name

The folder name should be `Chapter XX` (with a space, zero-padded two-digit
number). Variants like `Chapter1`, `chapter 01`, `Chapter 1` break the
convention.

### H3. Generating fewer than 30 questions

Each file should have 30 questions (10 TF, 10 MC, 10 Matching). Generating
fewer is a content shortfall, not a format error, but it violates the
workflow contract.

### H4. Confirming instead of generating

The original prompt said "Do not generate content yet. Confirm understanding
first." Many AI models took this literally and replied with a confirmation
instead of producing files. The rewritten prompt removes this instruction and
tells the model to emit files directly when asked.

---

## Frequency Summary

Based on the structure of the validator and the corpus, the most common
mistakes in rough order of frequency are:

1. **B3 / B4** — `>>` divider or trailing space on divider (matching).
2. **A1** — missing `-` in `[!success]- Answer`.
3. **C4** — Group B starting at `a)` instead of `n)`.
4. **D1 / D2** — wrong arrow (`=>` or `→`).
5. **C1 / C2** — uppercase letters or period instead of `)`.
6. **E1** — blank line inside a question block.
7. **E2 / E3** — headings or numbering inside the body.
8. **A2** — answer on the same line as the callout title.
9. **F1** — missing `sources:` key.
10. **E4** — wrapping the file in a code fence.

Avoiding these ten mistakes eliminates the vast majority of parser failures.
