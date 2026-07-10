"""
Quiz file validation service.

``ObsidianQuizValidator`` audits a Markdown quiz file against the strict
YAML + Obsidian-callout format expected by the vault's quiz plugin.

A file is valid iff:
  1. It begins with a YAML frontmatter block delimited by ``---`` lines.
  2. The frontmatter contains a ``sources:`` key.
  3. The body is a non-empty list of question callouts.
  4. Each question callout can be classified as EXACTLY ONE of:
        * True/False
        * Multiple Choice
        * Matching
  5. Each Multiple-Choice question has at least two ``a)``-style options
     and an answer letter that exists among them.
  6. Each Matching question has ``[!example] Group A`` and ``Group B``
     plus a complete set of ``a) -> n)`` mappings.

The validator returns a :class:`ValidationReport` with ``is_valid``,
``errors``, ``warnings``, and per-type ``stats``.
"""

from __future__ import annotations

import re
from typing import List

from vault_manager.core.interfaces import IValidationStrategy
from vault_manager.core.models import ValidationReport
from vault_manager.utils.file_ops import read_file_safely


# ---------------------------------------------------------------------------
# Regexes — preserved EXACTLY from the original. Do not modify.
# ---------------------------------------------------------------------------
# These regexes are the de-facto format spec. The golden tests in
# tests/test_validator.py pin their behaviour byte-for-byte; any change
# here will break equivalence.

_RE_QUESTION_OPENER = re.compile(r">\s*\[!question\]")
_RE_ANSWER_CALLOUT = re.compile(r">>\s*\[!success\]-\s*Answer")
_RE_TF_ANSWER = re.compile(r">>\s*(True|False)")
_RE_MC_OPTION = re.compile(r">\s+[a-d]\)")
_RE_EXAMPLE_BLOCK = re.compile(r"\[!example\]")
_RE_EXAMPLE_GROUP_A = re.compile(r"\[!example\]\s*Group A")
_RE_EXAMPLE_GROUP_B = re.compile(r"\[!example\]\s*Group B")
_RE_MATCHING_ANSWER = re.compile(r">>\s*[a-z]\)\s*->\s*[a-z]\)")
_RE_FRONTMATTER_OPENER = "---\n"
_RE_WIKILINK = re.compile(r"\[\[.*?\]\]")

# Splitter used to carve the body into individual question blocks.
_RE_QUESTION_BLOCK_BOUNDARY = re.compile(r"\n(?=>\s*\[!question\])")


# ---------------------------------------------------------------------------
# Per-type classifiers. Each returns True iff the block matches that type's
# signature. A block matching more than one type is flagged as a structural
# conflict by the caller.
# ---------------------------------------------------------------------------

def _is_true_false(block: str) -> bool:
    return bool(
        _RE_QUESTION_OPENER.search(block)
        and _RE_ANSWER_CALLOUT.search(block)
        and _RE_TF_ANSWER.search(block)
        and not _RE_MC_OPTION.search(block)
        and not _RE_EXAMPLE_BLOCK.search(block)
    )


def _is_multiple_choice(block: str) -> bool:
    return bool(
        _RE_QUESTION_OPENER.search(block)
        and _RE_ANSWER_CALLOUT.search(block)
        and _RE_MC_OPTION.search(block)
        and not _RE_EXAMPLE_BLOCK.search(block)
    )


def _is_matching(block: str) -> bool:
    return bool(
        _RE_QUESTION_OPENER.search(block)
        and _RE_EXAMPLE_GROUP_A.search(block)
        and _RE_EXAMPLE_GROUP_B.search(block)
        and _RE_MATCHING_ANSWER.search(block)
    )


# ---------------------------------------------------------------------------
# Per-type detail checkers. Each appends to ``report.errors`` if a typed
# question has structural problems beyond mere classification.
# ---------------------------------------------------------------------------

def _check_true_false(block: str, idx: int, line: int, report: ValidationReport) -> None:
    if not _RE_TF_ANSWER.search(block):
        report.errors.append((
            line,
            f"TF Question {idx}: Answer must be explicitly 'True' or 'False'",
        ))


def _check_multiple_choice(block: str, idx: int, line: int, report: ValidationReport) -> None:
    options = re.findall(r">\s+([a-d])\)", block)
    answer_match = re.search(r">>\s+([a-d])\)", block)
    if len(options) < 2:
        report.errors.append((
            line,
            f"MC Question {idx}: Must supply at least two valid options (a), b), etc.)",
        ))
    if answer_match and answer_match.group(1) not in options:
        report.errors.append((
            line,
            f"MC Question {idx}: Declared answer '{answer_match.group(1)}' "
            f"is not in available options {options}",
        ))


def _check_matching(block: str, idx: int, line: int, report: ValidationReport) -> None:
    if not _RE_ANSWER_CALLOUT.search(block):
        report.errors.append((
            line,
            f"Matching Question {idx}: Missing [!success]- Answer callout",
        ))


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

class ObsidianQuizValidator(IValidationStrategy):
    """Validate that quiz files adhere to the strict YAML + callout structure."""

    def validate(self, filepath: str) -> ValidationReport:
        content = read_file_safely(filepath)
        lines = content.split("\n")
        report = ValidationReport(filepath=filepath, is_valid=True)
        report.stats = {
            "true_false": 0,
            "multiple_choice": 0,
            "matching": 0,
        }

        # Frontmatter opener check.
        if not content.startswith(_RE_FRONTMATTER_OPENER):
            report.errors.append((
                1,
                "File must begin with a YAML frontmatter block (---)",
            ))

        # Frontmatter closer check + early return (matches original).
        closing_yaml = content.find("\n---", 4)
        if closing_yaml == -1:
            report.errors.append((
                1,
                "YAML frontmatter closing block (---) is missing",
            ))
            report.is_valid = False
            return report

        # Frontmatter body checks.
        frontmatter = content[4:closing_yaml]
        if "sources:" not in frontmatter:
            report.errors.append((
                2,
                "YAML frontmatter is missing the mandatory 'sources:' metadata key",
            ))
        if not _RE_WIKILINK.search(frontmatter):
            report.warnings.append((
                2,
                "No valid internal wiki-links [[Link]] found in frontmatter sources",
            ))

        # Body: split into question blocks and validate each.
        body = content[closing_yaml + 5:]
        question_blocks = _RE_QUESTION_BLOCK_BOUNDARY.split(body)
        for idx, block in enumerate(question_blocks, 1):
            self._validate_question_block(idx, block, lines, report)

        if report.errors:
            report.is_valid = False
        return report

    # ------------------------------------------------------------------
    # Per-question classification + detail checks
    # ------------------------------------------------------------------

    @staticmethod
    def _approx_line_number(block: str, lines: List[str]) -> int:
        """Find the line number of the first line of ``block`` in ``lines``.

        Matches the original's heuristic: take the block's first line, scan
        ``lines`` from the top, return the index of the first line that
        contains that text. Defaults to 1 if not found.
        """
        first_line = block.split("\n")[0]
        for i, line in enumerate(lines, 1):
            if first_line.strip() in line:
                return i
        return 1

    def _validate_question_block(
        self,
        idx: int,
        block: str,
        lines: List[str],
        report: ValidationReport,
    ) -> None:
        block = block.strip()
        if not block:
            return

        approx_line = self._approx_line_number(block, lines)

        is_tf = _is_true_false(block)
        is_mc = _is_multiple_choice(block)
        is_match = _is_matching(block)
        matches_found = sum([is_tf, is_mc, is_match])

        if matches_found == 0:
            report.errors.append((
                approx_line,
                f"Question Block {idx}: Unable to classify question type "
                f"(must be TF, MC, or Matching).",
            ))
            return
        if matches_found > 1:
            report.errors.append((
                approx_line,
                f"Question Block {idx}: Structural conflict. "
                f"Matches multiple types.",
            ))
            return

        if is_tf:
            report.stats["true_false"] += 1
            _check_true_false(block, idx, approx_line, report)
        elif is_mc:
            report.stats["multiple_choice"] += 1
            _check_multiple_choice(block, idx, approx_line, report)
        elif is_match:
            report.stats["matching"] += 1
            _check_matching(block, idx, approx_line, report)
