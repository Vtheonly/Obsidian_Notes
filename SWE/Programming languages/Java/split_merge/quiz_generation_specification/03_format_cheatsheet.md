# Quiz Format Cheatsheet

> One-page quick reference. For the full rules see `01_quiz_format_specification.md`.

## File Skeleton

```
---
sources:
  - "[[Folder/Note.md]]"
  - "[[Folder/Other Note.md]]"
---

<question 1>

<question 2>

...

<question N>
```

## Two Quote Depths — memorise

| Depth | Syntax | Used for |
|-------|--------|----------|
| 1 | `> ` (one `>`, one space) | `[!question]` opener, MC options |
| 2 | `>> ` (two `>`, one space) | `[!success]- Answer`, answer body, `[!example]` groups, matching items |
| bare | `>` (one `>`, no trailing space) | Divider line inside matching questions only |

## Type 1 — True / False

```
> [!question] <statement>
>> [!success]- Answer
>> True
```
* Answer is exactly `True` or `False` (capitalised, no period).

## Type 2 — Multiple Choice

```
> [!question] <question>
> a) opt A
> b) opt B
> c) opt C
> d) opt D
>> [!success]- Answer
>> b) opt B
```
* Lowercase letters `a)`-`d)`. Close-paren, not period.
* Exactly one correct answer.
* Answer at depth 2, repeats the option text verbatim.

## Type 3 — Matching

```
> [!question] <match instruction>
>> [!example] Group A
>> a) item a
>> b) item b
>> c) item c
>> d) item d
>
>> [!example] Group B
>> n) item n
>> o) item o
>> p) item p
>> q) item q
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
```
* Group A: `a)`-`d)`. Group B: `n)`-`q)` (starts at `n`, not `a`).
* Divider line is **`>` alone** — no trailing space, no `>>`.
* Arrow is **`->`** with one space on each side. Not `=>`, not `→`.
* `)` after the Group B letter in each mapping is mandatory.

## Top 10 Mistakes to Avoid

1. Missing `-` in `[!success]- Answer`.
2. Using `>>` for the matching divider line (should be bare `>`).
3. Trailing space on the matching divider line (`> ` instead of `>`).
4. Group B starting at `a)` instead of `n)`.
5. Using `=>` or `→` instead of `->`.
6. Uppercase option letters (`A)` instead of `a)`).
7. Using `a.` instead of `a)`.
8. Answer on same line as callout title (`[!success]- Answer: True`).
9. Blank line inside a question block.
10. Adding headings, numbering, or explanations.

## Mandatory Fields

* Frontmatter `---` opener on line 1.
* `sources:` key with at least one `"[[...]]"` entry (2-space indent).
* Frontmatter `---` closer.
* One blank line after frontmatter.
* `> [!question] ` opener for every question.
* `>> [!success]- Answer` callout in every question.
* Type-specific answer body.

## Forbidden Everywhere

* Headings (`#`, `##`, …).
* Question numbers (`1.`, `Q1.`, …).
* Horizontal rules (`---`) inside the body.
* Code fences (` ``` `) inside the body.
* Tables, images, HTML.
* Emoji.
* Tabs (use spaces).
* Trailing whitespace on any line.
* Explanations or rationale under answers.
