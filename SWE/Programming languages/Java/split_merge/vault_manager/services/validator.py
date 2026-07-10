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

def _determine_question_type(block: str) -> str | None:
    # 1. Check for success answer callout
    answer_match = re.search(r">>\s*\[!success\]-\s*Answer\s*\r?\n\s*(>>.*)", block)
    if answer_match:
        answer_line = answer_match.group(1).strip()
        # Clean the prefix '>>'
        if answer_line.startswith(">>"):
            answer_content = answer_line[2:].strip()
            if answer_content in ["True", "False"]:
                return "true_false"
            elif re.match(r"^[a-d]\)", answer_content) and "->" not in answer_content:
                return "multiple_choice"
            elif "->" in answer_content:
                return "matching"

    # 2. Fallback to classifiers based on content
    if _RE_EXAMPLE_BLOCK.search(block):
        return "matching"
    if _RE_MC_OPTION.search(block):
        return "multiple_choice"
    if _RE_QUESTION_OPENER.search(block):
        return "true_false"
        
    return None


def _is_true_false(block: str) -> bool:
    return _determine_question_type(block) == "true_false"


def _is_multiple_choice(block: str) -> bool:
    return _determine_question_type(block) == "multiple_choice"


def _is_matching(block: str) -> bool:
    return _determine_question_type(block) == "matching"


# ---------------------------------------------------------------------------
# Per-type detail checkers. Each appends to ``report.errors`` if a typed
# question has structural problems beyond mere classification.
# ---------------------------------------------------------------------------

def _check_true_false(block: str, idx: int, line: int, report: ValidationReport) -> None:
    if not _RE_ANSWER_CALLOUT.search(block):
        report.errors.append((
            line,
            f"TF Question {idx}: Missing [!success]- Answer callout",
        ))
    if not _RE_TF_ANSWER.search(block):
        report.errors.append((
            line,
            f"TF Question {idx}: Answer must be explicitly 'True' or 'False'",
        ))


def _check_multiple_choice(block: str, idx: int, line: int, report: ValidationReport) -> None:
    if not _RE_ANSWER_CALLOUT.search(block):
        report.errors.append((
            line,
            f"MC Question {idx}: Missing [!success]- Answer callout",
        ))
        
    # Extract options: lines starting with a single '>' followed by an option letter 'a)' to 'd)'
    options = []
    block_lines = block.split("\n")
    for raw_line in block_lines:
        stripped = raw_line.strip()
        if stripped.startswith(">") and not stripped.startswith(">>"):
            m = re.match(r"^>\s+([a-d])\)", stripped)
            if m:
                options.append(m.group(1))

    # Extract answer option
    answer_match = re.search(r">>\s+([a-d])\)", block)
    
    if len(options) < 2:
        report.errors.append((
            line,
            f"MC Question {idx}: Must supply at least two valid options (a), b), etc.)",
        ))
    if not answer_match:
        report.errors.append((
            line,
            f"MC Question {idx}: Missing or invalid declared answer (must be a), b), etc. in the success callout)",
        ))
    elif answer_match.group(1) not in options:
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
    if not _RE_EXAMPLE_GROUP_A.search(block):
        report.errors.append((
            line,
            f"Matching Question {idx}: Missing [!example] Group A callout",
        ))
    if not _RE_EXAMPLE_GROUP_B.search(block):
        report.errors.append((
            line,
            f"Matching Question {idx}: Missing [!example] Group B callout",
        ))

    # Divider checks:
    block_lines = block.split("\n")
    group_b_line_idx = -1
    answer_line_idx = -1
    for i, raw_line in enumerate(block_lines):
        line_stripped = raw_line.strip()
        if "Group B" in raw_line:
            group_b_line_idx = i
        elif "[!success]- Answer" in raw_line:
            answer_line_idx = i
        if line_stripped == ">>":
            report.errors.append((
                line + i,
                f"Matching Question {idx}: Divider line must be exactly '>', not '>>'",
            ))
        elif raw_line == "> ":
            report.errors.append((
                line + i,
                f"Matching Question {idx}: Divider line must be exactly '>', with no trailing space",
            ))

    if group_b_line_idx != -1:
        prev_idx = group_b_line_idx - 1
        if prev_idx >= 0:
            prev_line = block_lines[prev_idx]
            if prev_line != ">":
                report.errors.append((
                    line + prev_idx,
                    f"Matching Question {idx}: Divider line before Group B must be exactly '>', got '{prev_line}'",
                ))
    if answer_line_idx != -1:
        prev_idx = answer_line_idx - 1
        if prev_idx >= 0:
            prev_line = block_lines[prev_idx]
            if prev_line != ">":
                report.errors.append((
                    line + prev_idx,
                    f"Matching Question {idx}: Divider line before Answer must be exactly '>', got '{prev_line}'",
                ))

    # Items checks
    group_a_lines = []
    group_b_lines = []
    in_group_a = False
    in_group_b = False
    
    for raw_line in block_lines:
        if "Group A" in raw_line:
            in_group_a = True
            in_group_b = False
            continue
        elif "Group B" in raw_line:
            in_group_a = False
            in_group_b = True
            continue
        elif "[!success]- Answer" in raw_line:
            in_group_a = False
            in_group_b = False
            continue
            
        if in_group_a:
            m = re.match(r">>\s*([a-z])\)", raw_line.strip())
            if m:
                group_a_lines.append(m.group(1))
        elif in_group_b:
            m = re.match(r">>\s*([a-z])\)", raw_line.strip())
            if m:
                group_b_lines.append(m.group(1))

    # Mappings checks
    mappings = re.findall(r">>\s*([a-z])\)\s*->\s*([a-z])\)", block)
    
    if not group_a_lines:
        report.errors.append((
            line,
            f"Matching Question {idx}: Group A has no items",
        ))
    if not group_b_lines:
        report.errors.append((
            line,
            f"Matching Question {idx}: Group B has no items",
        ))
        
    if len(group_a_lines) != len(group_b_lines):
        report.errors.append((
            line,
            f"Matching Question {idx}: Group A count ({len(group_a_lines)}) "
            f"must match Group B count ({len(group_b_lines)})",
        ))
        
    # Group B letters must start at 'n' and be consecutive
    expected_b = [chr(ord('n') + i) for i in range(len(group_a_lines))]
    if group_b_lines != expected_b and group_a_lines:
        report.errors.append((
            line,
            f"Matching Question {idx}: Group B letters must start at 'n)' and be consecutive: {expected_b}",
        ))
        
    # Map checks
    mapped_a = [m[0] for m in mappings]
    mapped_b = [m[1] for m in mappings]
    for letter in group_a_lines:
        if letter not in mapped_a:
            report.errors.append((
                line,
                f"Matching Question {idx}: Group A letter '{letter})' is not mapped in the answer",
            ))
    for letter in group_b_lines:
        if letter not in mapped_b:
            report.errors.append((
                line,
                f"Matching Question {idx}: Group B letter '{letter})' is not mapped in the answer",
            ))
            
    # Check for duplicate mappings
    seen_a = set()
    seen_b = set()
    for a_let, b_let in mappings:
        if a_let in seen_a:
            report.errors.append((
                line,
                f"Matching Question {idx}: Group A letter '{a_let})' is mapped more than once",
            ))
        if b_let in seen_b:
            report.errors.append((
                line,
                f"Matching Question {idx}: Group B letter '{b_let})' is mapped more than once",
            ))
        seen_a.add(a_let)
        seen_b.add(b_let)

    # Check for invalid mapping letters not present in Group A or B
    for a_let, b_let in mappings:
        if a_let not in group_a_lines:
            report.errors.append((
                line,
                f"Matching Question {idx}: Answer maps from '{a_let})' which is not in Group A",
            ))
        if b_let not in group_b_lines:
            report.errors.append((
                line,
                f"Matching Question {idx}: Answer maps to '{b_let})' which is not in Group B",
            ))


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

class ObsidianQuizValidator(IValidationStrategy):
    """Validate that quiz files adhere to the strict YAML + callout structure."""

    def validate(self, filepath: str) -> ValidationReport:
        content = read_file_safely(filepath).replace("\r\n", "\n")
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

        # Check that every non-empty line inside the block starts with '>'
        block_lines = block.split("\n")
        for i, raw_line in enumerate(block_lines):
            line_stripped = raw_line.strip()
            if line_stripped and not line_stripped.startswith(">"):
                report.errors.append((
                    approx_line + i,
                    f"Question Block {idx}: Every line inside a callout must start with '>', got '{raw_line}'",
                ))

        q_type = _determine_question_type(block)

        if not q_type:
            report.errors.append((
                approx_line,
                f"Question Block {idx}: Unable to classify question type "
                f"(must be TF, MC, or Matching).",
            ))
            return

        if q_type == "true_false":
            report.stats["true_false"] += 1
            _check_true_false(block, idx, approx_line, report)
        elif q_type == "multiple_choice":
            report.stats["multiple_choice"] += 1
            _check_multiple_choice(block, idx, approx_line, report)
        elif q_type == "matching":
            report.stats["matching"] += 1
            _check_matching(block, idx, approx_line, report)
