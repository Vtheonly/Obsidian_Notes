#!/usr/bin/env python3
"""
quiz_validator.py — Strict parser/validator for the interactive puzzle quiz format.

The quiz format (Obsidian callouts) is:

---
sources:
  - "[[Note Name]]"
---
> [!question] True/False statement.
>> [!success]- Answer
>> True

> [!question] Multiple choice question?
> a) option
> b) option
> c) option
> d) option
>> [!success]- Answer
>> a) option

> [!question] Match the item with its description.
>> [!example] Group A
>> a) item
>> b) item
>> c) item
>
>> [!example] Group B
>> n) description.
>> o) description.
>> p) description.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o())

Rules enforced:
  * YAML frontmatter with a non-empty `sources:` list of quoted wikilinks.
  * True/False answers are exactly `True` or `False`.
  * Multiple choice: exactly four options a)-d), one correct; the answer line
    repeats the letter AND the exact option text.
  * Matching: `Group A` items lettered consecutively from `a)`; `Group B`
    items lettered consecutively from `n)`; equal group sizes (3-6); answers
    form a bijective `x) -> y)` mapping.
  * Blocks separated by exactly one blank line; no blank lines inside a block.
  * No headers, mermaid, fenced code blocks, bold/italic markers, tabs,
    trailing whitespace, display LaTeX (`$$` or `\\begin{...}`).
  * Inline LaTeX only: every line has an even number of `$` characters.
  * `sources` wikilinks must resolve to real notes in the vault.
  * No duplicate question stems (within a file or across files).

Usage:
    python3 quiz_validator.py PATH [PATH ...]

Exit code 0 iff no errors (warnings do not fail the run).
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

FRONT_OPEN = "---"
SOURCES_KEY = "sources:"
SOURCE_RE = re.compile(r'^  - "\[\[(.+?)\]\]"$')
QUESTION_RE = re.compile(r"^> \[!question\] (.+)$")
ANSWER_RE = re.compile(r"^>> \[!success\]- Answer$")
ANSWER_LINE_RE = re.compile(r"^>> (.+)$")
GROUP_A_RE = re.compile(r"^>> \[!example\] Group A$")
GROUP_B_RE = re.compile(r"^>> \[!example\] Group B$")
SEP_LINE = ">"
MC_OPT_RE = re.compile(r"^> ([a-d])\) (.+)$")
MATCH_A_RE = re.compile(r"^>> ([a-z])\) (.+)$")
MATCH_ANS_RE = re.compile(r"^>> ([a-z])\) -> ([a-z])\)$")
QUESTION_LINE_RE = re.compile(r"^> \[!question\] ", re.M)

MIN_PAIRS, MAX_PAIRS = 3, 6
GROUP_B_START = "n"
NEAR_DUP_THRESHOLD = 0.90


class QuizError(Exception):
    pass


def letter_seq(start: str, n: int) -> list[str]:
    return [chr(ord(start) + i) for i in range(n)]


def lint_line(line: str, path: Path, lineno: int, errors: list, warnings: list) -> None:
    """Format-hygiene checks applied to every line of a quiz file."""
    where = f"{path.name}:{lineno}"
    if line != line.rstrip():
        errors.append(f"{where}: trailing whitespace")
    if "\t" in line:
        errors.append(f"{where}: tab character (use spaces)")
    if "$$" in line:
        errors.append(f"{where}: display LaTeX `$$` is forbidden — use inline $...$")
    if "\\begin{" in line:
        errors.append(f"{where}: LaTeX environment `\\begin{{...}}` is forbidden")
    if line.lstrip().startswith("#"):
        errors.append(f"{where}: markdown header — quiz files must contain only question blocks")
    if "```" in line or "~~~" in line:
        errors.append(f"{where}: fenced code block — use inline `code` instead")
    if "**" in line or "__" in line:
        errors.append(f"{where}: bold marker — keep quiz text plain (no `**` / `__`)")
    if line.count("$") % 2 != 0:
        errors.append(f"{where}: unbalanced inline LaTeX `$` (odd number of `$`)")


def parse_quiz_file(path: Path, vault_notes: set[str] | None) -> dict:
    """Parse one quiz file. Returns stats dict. Raises QuizError on the first
    fatal structural problem; non-fatal issues are collected in errors."""
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    if text.endswith("\n\n"):
        errors.append(f"{path.name}: trailing blank line(s) at end of file")
    if not text.endswith("\n"):
        errors.append(f"{path.name}: file must end with a newline")
    if text.startswith("\ufeff"):
        errors.append(f"{path.name}: BOM marker present")

    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]

    for i, line in enumerate(lines, 1):
        lint_line(line, path, i, errors, warnings)

    # ---------------- frontmatter ----------------
    if len(lines) < 4 or lines[0] != FRONT_OPEN:
        raise QuizError(f"{path.name}: expected frontmatter to open with '---'")
    if lines[1] != SOURCES_KEY:
        raise QuizError(f"{path.name}: line 2 must be exactly 'sources:'")
    idx = 2
    sources: list[str] = []
    while idx < len(lines) and lines[idx] != FRONT_OPEN:
        m = SOURCE_RE.match(lines[idx])
        if not m:
            raise QuizError(
                f"{path.name}:{idx + 1}: invalid source entry — expected "
                f'  - "[[Note Name]]"  (two-space indent, quoted wikilink)'
            )
        sources.append(m.group(1))
        idx += 1
    if not sources:
        raise QuizError(f"{path.name}: sources list is empty")
    if idx >= len(lines):
        raise QuizError(f"{path.name}: frontmatter not closed with '---'")
    idx += 1  # past closing '---'

    if vault_notes is not None:
        for src in sources:
            if src not in vault_notes:
                errors.append(
                    f"{path.name}: source '[[{src}]]' does not resolve to any note in the vault"
                )

    if idx < len(lines) and lines[idx] == "":
        errors.append(
            f"{path.name}:{idx + 1}: no blank line allowed between frontmatter and the first question"
        )

    # ---------------- question blocks ----------------
    body = lines[idx:]
    if not body:
        raise QuizError(f"{path.name}: no question blocks found")

    blocks: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] = []
    for offset, line in enumerate(body):
        lineno = idx + offset + 1
        if line == "":
            if current:
                blocks.append(current)
                current = []
            else:
                errors.append(f"{path.name}:{lineno}: consecutive blank lines between questions")
        else:
            current.append((lineno, line))
    if current:
        blocks.append(current)

    stats = {"tf": 0, "mc": 0, "match": 0, "sources": sources, "stems": []}

    for block in blocks:
        first_no, first_line = block[0]
        m = QUESTION_RE.match(first_line)
        if not m:
            errors.append(
                f"{path.name}:{first_no}: block must start with '> [!question] ...' "
                f"(found: {first_line[:60]!r})"
            )
            continue
        stem = m.group(1).strip()
        if not stem:
            errors.append(f"{path.name}:{first_no}: empty question text")
        stats["stems"].append(stem)

        rest = block[1:]
        is_match = any(GROUP_A_RE.match(l) for _, l in rest)
        is_mc = any(MC_OPT_RE.match(l) for _, l in rest)

        if is_match:
            stats["match"] += 1
            parse_match_block(path, block, errors)
        elif is_mc:
            stats["mc"] += 1
            parse_mc_block(path, block, errors)
        else:
            stats["tf"] += 1
            parse_tf_block(path, block, errors)

    return {
        "path": path,
        "errors": errors,
        "warnings": warnings,
        **stats,
    }


def parse_tf_block(path: Path, block: list[tuple[int, str]], errors: list[str]) -> None:
    if len(block) != 3:
        errors.append(
            f"{path.name}:{block[0][0]}: True/False block must have exactly 3 lines "
            f"(question, answer callout, answer) — found {len(block)}"
        )
        return
    (n2, l2), (n3, l3) = block[1], block[2]
    if not ANSWER_RE.match(l2):
        errors.append(f"{path.name}:{n2}: expected '>> [!success]- Answer'")
        return
    m = ANSWER_LINE_RE.match(l3)
    if not m or m.group(1) not in ("True", "False"):
        errors.append(
            f"{path.name}:{n3}: True/False answer must be exactly 'True' or 'False' "
            f"(no explanation text)"
        )


def parse_mc_block(path: Path, block: list[tuple[int, str]], errors: list[str]) -> None:
    options: dict[str, str] = {}
    answer_lineno = None
    answer_line = None
    for lineno, line in block[1:]:
        if ANSWER_RE.match(line):
            answer_lineno = lineno
            continue
        if answer_lineno is not None:
            answer_line = (lineno, line)
            break
        m = MC_OPT_RE.match(line)
        if m:
            options[m.group(1)] = m.group(2)
        elif line.startswith(">"):
            errors.append(
                f"{path.name}:{lineno}: malformed option line (expected e.g. '> a) text')"
            )
        else:
            errors.append(f"{path.name}:{lineno}: stray line inside MC block")

    if len(block) != 7:
        errors.append(
            f"{path.name}:{block[0][0]}: MC block must have exactly 7 lines "
            f"(question, a)-d), answer callout, answer) — found {len(block)}"
        )
    if sorted(options.keys()) != ["a", "b", "c", "d"]:
        errors.append(
            f"{path.name}:{block[0][0]}: MC options must be exactly a) b) c) d) in order "
            f"— found {sorted(options.keys()) or 'none'}"
        )
    if answer_lineno is None or answer_line is None:
        errors.append(f"{path.name}:{block[0][0]}: missing answer callout or answer line")
        return
    m = ANSWER_LINE_RE.match(answer_line[1])
    if not m:
        errors.append(f"{path.name}:{answer_line[0]}: answer line must start with '>> '")
        return
    ans = m.group(1).strip()
    am = re.match(r"^([a-d])\) (.+)$", ans)
    if not am:
        errors.append(
            f"{path.name}:{answer_line[0]}: MC answer must look like 'a) option text'"
        )
        return
    letter, text = am.group(1), am.group(2)
    if letter not in options:
        errors.append(
            f"{path.name}:{answer_line[0]}: answer letter '{letter})' is not an option"
        )
        return
    if options[letter] != text:
        errors.append(
            f"{path.name}:{answer_line[0]}: answer text must exactly repeat option "
            f"'{letter}) {options[letter]}' — found '{letter}) {text}'"
        )


def parse_match_block(path: Path, block: list[tuple[int, str]], errors: list[str]) -> None:
    phase = "stem"  # stem -> A -> B -> answers
    group_a: dict[str, str] = {}
    group_b: dict[str, str] = {}
    answers: list[tuple[str, str]] = []
    for lineno, line in block[1:]:
        if GROUP_A_RE.match(line):
            if phase != "stem":
                errors.append(f"{path.name}:{lineno}: 'Group A' header out of place")
            phase = "A"
            continue
        if GROUP_B_RE.match(line):
            if phase != "A-sep":
                errors.append(
                    f"{path.name}:{lineno}: 'Group B' header must be preceded by a '>' separator line"
                )
            phase = "B"
            continue
        if ANSWER_RE.match(line):
            if phase != "B-sep":
                errors.append(
                    f"{path.name}:{lineno}: answer callout must be preceded by a '>' separator line"
                )
            phase = "answers"
            continue
        if line == SEP_LINE:
            if phase in ("A", "B"):
                phase += "-sep"
            else:
                errors.append(f"{path.name}:{lineno}: stray '>' separator line")
            continue
        m = MATCH_A_RE.match(line)
        if phase == "A" and m:
            group_a[m.group(1)] = m.group(2)
            continue
        m = MATCH_A_RE.match(line)
        if phase == "B" and m:
            group_b[m.group(1)] = m.group(2)
            continue
        m = MATCH_ANS_RE.match(line)
        if phase == "answers" and m:
            answers.append((m.group(1), m.group(2)))
            continue
        errors.append(
            f"{path.name}:{lineno}: unexpected line in matching block: {line[:60]!r}"
        )

    na, nb = len(group_a), len(group_b)
    if na != nb:
        errors.append(
            f"{path.name}:{block[0][0]}: Group A has {na} items but Group B has {nb}"
        )
    if not (MIN_PAIRS <= na <= MAX_PAIRS):
        errors.append(
            f"{path.name}:{block[0][0]}: matching groups must have {MIN_PAIRS}-{MAX_PAIRS} "
            f"items — found {na}"
        )
    if sorted(group_a) != letter_seq("a", na):
        errors.append(
            f"{path.name}:{block[0][0]}: Group A letters must be consecutive from 'a' "
            f"— found {sorted(group_a)}"
        )
    if sorted(group_b) != letter_seq(GROUP_B_START, nb):
        errors.append(
            f"{path.name}:{block[0][0]}: Group B letters must be consecutive from "
            f"'{GROUP_B_START})' — found {sorted(group_b)}"
        )
    for label, group in (("A", group_a), ("B", group_b)):
        for k, v in group.items():
            if not v.strip():
                errors.append(f"{path.name}:{block[0][0]}: Group {label} item '{k})' is empty")

    if len(answers) != na:
        errors.append(
            f"{path.name}:{block[0][0]}: expected {na} answer mappings — found {len(answers)}"
        )
    src_letters = [a for a, _ in answers]
    dst_letters = [b for _, b in answers]
    if sorted(src_letters) != sorted(group_a.keys()):
        errors.append(
            f"{path.name}:{block[0][0]}: answer left-hand letters {sorted(src_letters)} "
            f"do not cover Group A exactly once"
        )
    if sorted(dst_letters) != sorted(set(dst_letters)):
        errors.append(f"{path.name}:{block[0][0]}: duplicate right-hand letter in answers")
    for a, b in answers:
        if b not in group_b:
            errors.append(
                f"{path.name}:{block[0][0]}: answer maps to '{b})' which is not a Group B item"
            )


# ---------------- cross-file checks ----------------

def normalize_stem(stem: str) -> str:
    stem = stem.lower()
    stem = re.sub(r"[$`]", "", stem)
    stem = re.sub(r"[^a-z0-9]+", " ", stem)
    return " ".join(stem.split())


def cross_file_checks(results: list[dict]) -> list[str]:
    messages: list[str] = []
    seen: dict[str, list[str]] = {}
    stems_list = [(stem, str(r["path"])) for r in results for stem in r["stems"]]

    for stem, where in stems_list:
        norm = normalize_stem(stem)
        if norm in seen:
            for other in seen[norm]:
                messages.append(
                    f"DUPLICATE question stem: '{stem[:70]}' in {where} == {other}"
                )
            seen[norm].append(where)
        else:
            seen[norm] = [where]

    # near-duplicate detection
    items = [(normalize_stem(s), s, w) for s, w in stems_list]
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            n1, s1, w1 = items[i]
            n2, s2, w2 = items[j]
            if n1 == n2:
                continue  # already reported as exact duplicate
            if not n1 or not n2:
                continue
            ratio = difflib.SequenceMatcher(None, n1, n2).ratio()
            if ratio >= NEAR_DUP_THRESHOLD:
                messages.append(
                    f"NEAR-DUPLICATE (similarity {ratio:.2f}): "
                    f"'{s1[:60]}' [{w1}] ~ '{s2[:60]}' [{w2}]"
                )
    return messages


# ---------------- vault / CLI ----------------

def find_vault_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return start


def index_vault_notes(vault: Path) -> set[str]:
    return {p.stem for p in vault.rglob("*.md")}


def collect_quiz_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_dir():
            for f in sorted(p.rglob("*.md")):
                text = f.read_text(encoding="utf-8", errors="replace")
                if QUESTION_LINE_RE.search(text):
                    files.append(f)
        elif p.is_file():
            files.append(p)
        else:
            print(f"warning: path not found: {p}", file=sys.stderr)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate interactive quiz markdown files")
    ap.add_argument("paths", nargs="+", type=Path, help="quiz files or directories")
    ap.add_argument("--vault", type=Path, default=None, help="vault root for source resolution")
    args = ap.parse_args()

    files = collect_quiz_files(args.paths)
    if not files:
        print("no quiz files found")
        return 1

    roots = {find_vault_root(f.parent if f.is_file() else f) for f in files}
    vault = args.vault or (roots.pop() if len(roots) == 1 else None)
    vault_notes = index_vault_notes(vault) if vault else None

    results: list[dict] = []
    fatal = 0
    for f in files:
        try:
            results.append(parse_quiz_file(f, vault_notes))
        except QuizError as e:
            print(f"[FATAL] {e}")
            fatal += 1

    any_error = fatal > 0
    print("=" * 78)
    for r in results:
        status = "OK  " if not r["errors"] else "FAIL"
        print(
            f"[{status}] {r['path']}  —  TF:{r['tf']}  MC:{r['mc']}  "
            f"Match:{r['match']}  sources:{len(r['sources'])}"
        )
        for e in r["errors"]:
            print(f"    ERROR  {e}")
            any_error = True
        for w in r["warnings"]:
            print(f"    warn   {w}")
    print("=" * 78)

    cross = cross_file_checks(results)
    for msg in cross:
        print(f"X-FILE  {msg}")
        if msg.startswith("DUPLICATE"):
            any_error = True

    total_tf = sum(r["tf"] for r in results)
    total_mc = sum(r["mc"] for r in results)
    total_match = sum(r["match"] for r in results)
    print(
        f"{len(results)} file(s), {len(results) - fatal} parsed — "
        f"total questions: {total_tf + total_mc + total_match} "
        f"(TF:{total_tf} MC:{total_mc} Match:{total_match})"
    )
    print("RESULT: " + ("FAILED — fix errors above" if any_error else "ALL VALID"))
    return 1 if any_error else 0


if __name__ == "__main__":
    sys.exit(main())
