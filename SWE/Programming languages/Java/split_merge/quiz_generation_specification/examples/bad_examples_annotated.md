# Annotated Bad Examples

> Each block below shows a fragment of an invalid quiz file, the specific rule
> it violates (referencing `01_quiz_format_specification.md`), and the
> corrected version. Use this file as a negative training reference for AI
> models.
>
> The notation `← BAD:` marks the offending line.

---

## Bad Example 1 — Missing `-` in the answer callout (rule A1, spec CC-2)

```markdown
> [!question] The Earth revolves around the Sun.
>> [!success] Answer          ← BAD: missing "-" after "[!success]"
>> True
```

**Why it breaks:** The parser's regex `>>\s*\[!success\]-\s*Answer` requires
the literal `-`. Without it, the answer callout is not detected and the
question is unclassifiable.

**Correct:**
```markdown
> [!question] The Earth revolves around the Sun.
>> [!success]- Answer
>> True
```

---

## Bad Example 2 — Answer on the same line as the callout title (rule A2)

```markdown
> [!question] The Earth revolves around the Sun.
>> [!success]- Answer: True   ← BAD: answer must be on the next line
```

**Why it breaks:** The parser expects the answer text on the line *after* the
callout title, prefixed by `>> `. There is no `>> True` line, so the TF
classifier fails.

**Correct:**
```markdown
> [!question] The Earth revolves around the Sun.
>> [!success]- Answer
>> True
```

---

## Bad Example 3 — Wrong quote depth for the answer (rule B1)

```markdown
> [!question] The Earth revolves around the Sun.
> [!success]- Answer          ← BAD: depth 1 instead of depth 2
> True                        ← BAD: depth 1 instead of depth 2
```

**Why it breaks:** The answer callout must be nested inside the question
blockquote. At depth 1, it is a separate top-level callout and the question
has no answer callout.

**Correct:**
```markdown
> [!question] The Earth revolves around the Sun.
>> [!success]- Answer
>> True
```

---

## Bad Example 4 — Uppercase option letters (rule C1, spec MC-3)

```markdown
> [!question] Which planet is the Red Planet?
> A) Venus                    ← BAD: uppercase letter
> B) Mars                     ← BAD: uppercase letter
> C) Jupiter                  ← BAD: uppercase letter
> D) Saturn                   ← BAD: uppercase letter
>> [!success]- Answer
>> B) Mars                    ← BAD: uppercase letter
```

**Why it breaks:** The MC classifier regex `>\s+[a-d]\)` is lowercase-only.
Uppercase options are invisible to the classifier, so the question is
misclassified as True/False (no options detected).

**Correct:**
```markdown
> [!question] Which planet is the Red Planet?
> a) Venus
> b) Mars
> c) Jupiter
> d) Saturn
>> [!success]- Answer
>> b) Mars
```

---

## Bad Example 5 — Period instead of close-paren (rule C2, spec MC-4)

```markdown
> [!question] Which planet is the Red Planet?
> a. Venus                    ← BAD: period instead of ")"
> b. Mars
> c. Jupiter
> d. Saturn
>> [!success]- Answer
>> b. Mars
```

**Why it breaks:** The MC regex requires `a)`, not `a.`.

**Correct:**
```markdown
> [!question] Which planet is the Red Planet?
> a) Venus
> b) Mars
> c) Jupiter
> d) Saturn
>> [!success]- Answer
>> b) Mars
```

---

## Bad Example 6 — Group B starts at `a)` instead of `n)` (rule C4, spec MT-3 / MT-6)

```markdown
> [!question] Match the planet with its feature.
>> [!example] Group A
>> a) Mercury
>> b) Venus
>> c) Earth
>> d) Mars
>
>> [!example] Group B
>> a) Closest to the Sun      ← BAD: should be n)
>> b) Hottest surface         ← BAD: should be o)
>> c) Has liquid water        ← BAD: should be p)
>> d) Red Planet              ← BAD: should be q)
>
>> [!success]- Answer
>> a) -> a)                   ← BAD: ambiguous mapping
```

**Why it breaks:** The matching classifier looks for Group B items using the
range `n-z`. With Group B also at `a)`, those items are merged into Group A,
and the question fails to match the Matching signature.

**Correct:**
```markdown
> [!question] Match the planet with its feature.
>> [!example] Group A
>> a) Mercury
>> b) Venus
>> c) Earth
>> d) Mars
>
>> [!example] Group B
>> n) Closest to the Sun
>> o) Hottest surface
>> p) Has liquid water
>> q) Red Planet
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
```

---

## Bad Example 7 — Wrong arrow in matching answer (rule D1)

```markdown
>> [!success]- Answer
>> a) => n)                   ← BAD: "=>" instead of "->"
>> b) => o)
```

**Why it breaks:** The matching answer regex
`>>\s*[a-z]\)\s*->\s*[a-z]\)` requires the ASCII arrow `->`. `=>` does not
match.

**Correct:** `>> a) -> n)`.

---

## Bad Example 8 — Unicode arrow in matching answer (rule D2)

```markdown
>> [!success]- Answer
>> a) → n)                    ← BAD: Unicode arrow
```

**Why it breaks:** Same as Bad Example 7. Use ASCII `->`.

**Correct:** `>> a) -> n)`.

---

## Bad Example 9 — `>>` divider line in matching (rule B3, spec MT-4)

```markdown
> [!question] Match the items.
>> [!example] Group A
>> a) Mercury
>> b) Venus
>>                             ← BAD: divider must be ">", not ">>"
>> [!example] Group B
>> n) Closest to the Sun
>> o) Hottest surface
```

**Why it breaks:** The divider line tells the parser that Group A has ended.
A `>>` line is treated as continuation of Group A, so the parser merges the
two groups and the question fails the Matching signature.

**Correct:** The divider line is bare `>` (depth 1, no trailing space):
```markdown
> [!question] Match the items.
>> [!example] Group A
>> a) Mercury
>> b) Venus
>
>> [!example] Group B
>> n) Closest to the Sun
>> o) Hottest surface
```

---

## Bad Example 10 — Trailing space on the divider line (rule B4)

```markdown
> [!question] Match the items.
>> [!example] Group A
>> a) Mercury
>> b) Venus
>                              ← BAD: trailing space after ">" (invisible)
>> [!example] Group B
```

**Why it breaks:** Strict plugin versions treat `> ` (with trailing space) as
continuation of the previous blockquote, not as a structural divider.

**Correct:** The line is exactly `>` followed by a newline — no space.

---

## Bad Example 11 — Missing `)` after the Group B letter in the answer (rule C5)

```markdown
>> [!success]- Answer
>> a) -> n                    ← BAD: missing ")" after "n"
>> b) -> o
```

**Why it breaks:** The matching answer regex requires both letters to be
followed by `)`.

**Correct:** `>> a) -> n)`.

---

## Bad Example 12 — Blank line inside a question block (rule E1, spec CC-5)

```markdown
> [!question] Which planet is the Red Planet?
> a) Venus

> b) Mars                      ← BAD: blank line above broke the blockquote
> c) Jupiter
> d) Saturn
>> [!success]- Answer
>> b) Mars
```

**Why it breaks:** A blank line terminates the blockquote. The parser then
sees two separate callouts. The second callout (`> b) Mars`) has no
`[!question]` opener and is unclassifiable.

**Correct:** No blank lines inside a question:
```markdown
> [!question] Which planet is the Red Planet?
> a) Venus
> b) Mars
> c) Jupiter
> d) Saturn
>> [!success]- Answer
>> b) Mars
```

---

## Bad Example 13 — Heading inside the body (rule E2, spec BD-3)

```markdown
## True / False                 ← BAD: heading inside body

> [!question] The Earth revolves around the Sun.
>> [!success]- Answer
>> True
```

**Why it breaks:** The body must be a flat list of callouts. Headings break
the flat structure.

**Correct:** No headings. Just callouts separated by one blank line.

---

## Bad Example 14 — Numbering the questions (rule E3, spec BD-3)

```markdown
1. > [!question] The Earth revolves around the Sun.    ← BAD: numbered prefix
   >> [!success]- Answer
   >> True

2. > [!question] ...                                   ← BAD: numbered prefix
```

**Why it breaks:** The `1.` prefix breaks the blockquote. The parser sees a
Markdown ordered list, not a callout.

**Correct:** No numbering.

---

## Bad Example 15 — Horizontal rule between questions (rule E5, spec BD-4)

```markdown
> [!question] Q1
>> [!success]- Answer
>> True

---                              ← BAD: horizontal rule / ambiguous frontmatter delimiter

> [!question] Q2
```

**Why it breaks:** `---` inside the body is ambiguous and breaks the flat
callout structure.

**Correct:** Use a single blank line to separate questions.

---

## Bad Example 16 — Missing `sources:` key (rule F1, spec FM-2)

```markdown
---
title: Chapter 1 Quiz            ← BAD: no sources: key
---
```

**Why it breaks:** The validator explicitly checks for the `sources:` string
in the frontmatter.

**Correct:**
```markdown
---
sources:
  - "[[Sample/Note.md]]"
---
```

---

## Bad Example 17 — Wikilink not double-quoted (rule F2, spec FM-4)

```yaml
---
sources:
  - [[Note.md]]                  ← BAD: not double-quoted
---
```

**Why it breaks:** YAML may parse `[[Note.md]]` as a flow-style nested
sequence, not as a string.

**Correct:**
```yaml
---
sources:
  - "[[Note.md]]"
---
```

---

## Bad Example 18 — Frontmatter not on line 1 (rule F4, spec FM-1)

```markdown

---                              ← BAD: blank line at top of file
sources:
  - "[[Note.md]]"
---
```

**Why it breaks:** The validator checks `content.startswith("---\n")`. A
leading blank line means the file does not start with `---\n`.

**Correct:** Line 1 is exactly `---`.

---

## Bad Example 19 — Explanations under the answer (rule E6, spec CC-6)

```markdown
> [!question] Which planet is the Red Planet?
> a) Venus
> b) Mars
> c) Jupiter
> d) Saturn
>> [!success]- Answer
>> b) Mars
>> [!note] Explanation           ← BAD: extra callout
>> Mars appears red because of iron oxide on its surface.
```

**Why it breaks:** The format supports exactly one answer callout per
question. Extra callouts may shift the parser's classification.

**Correct:** One answer callout per question. No explanations.

---

## Bad Example 20 — Wrapping the file in a code fence (rule E4, spec BD-7)

````markdown
```markdown                       ← BAD: outer code fence
---
sources:
  - "[[Note.md]]"
---
...
```                               ← BAD: outer code fence
````

**Why it breaks:** The frontmatter opener `---` is then inside a code block,
so the YAML parser does not see it as a frontmatter delimiter.

**Correct:** No outer code fence. The file starts directly with `---`.

---

## Bad Example 21 — Emoji in question text (rule G1, spec CC-8)

```markdown
> [!question] 🌍 The Earth revolves around the Sun.   ← BAD: emoji
>> [!success]- Answer
>> True
```

**Why it breaks:** Emoji are not part of the format and may be stripped by
the purge pipeline, shifting line content.

**Correct:** No emoji.

---

## Bad Example 22 — Tabs for indentation (rule G2, spec FM-8)

```yaml
---
sources:
	- "[[Note.md]]"           ← BAD: tab indentation
---
```

**Why it breaks:** Tabs are not consistently handled by YAML parsers or by
the regex classifier.

**Correct:** Use spaces.

---

## Frequency Summary

The most common mistakes, in rough order of frequency observed in AI-generated
quiz files, are:

1. Bad Example 9 — `>>` divider line in matching.
2. Bad Example 10 — trailing space on the divider line.
3. Bad Example 1 — missing `-` in `[!success]- Answer`.
4. Bad Example 6 — Group B starting at `a)` instead of `n)`.
5. Bad Example 7 / 8 — wrong arrow (`=>` or `→`).
6. Bad Example 4 / 5 — uppercase letters or period instead of `)`.
7. Bad Example 12 — blank line inside a question block.
8. Bad Example 13 / 14 — headings or numbering inside the body.
9. Bad Example 2 — answer on the same line as the callout title.
10. Bad Example 16 — missing `sources:` key.

Avoiding these ten mistakes eliminates the vast majority of parser failures.
