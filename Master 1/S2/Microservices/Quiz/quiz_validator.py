#!/usr/bin/env python3
"""
Quiz Format Validator
--------------------
Validates that quiz markdown files follow the exact expected format:
- YAML frontmatter with sources
- Three question types: True/False, Multiple Choice, Matching
- Correct use of Obsidian callouts: [!question], [!success]- Answer, [!example]

Usage: python quiz_validator.py [file_path ...]
       If no file paths are given, validates all .md files recursively from the current directory.
"""

import re
import sys
import os

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def log_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")


def log_error(msg):
    print(f"{RED}✗ {msg}{RESET}")


def log_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")


def log_info(msg):
    print(f"{CYAN}INFO: {msg}{RESET}")


class QuizValidator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.content = None
        self.lines = None
        self.errors = []
        self.warnings = []
        self.stats = {"true_false": 0, "multiple_choice": 0, "matching": 0}
        self.current_question_type = None

    def validate(self):
        """Run all validation checks and return True if valid."""
        print(f"\n{'='*60}")
        print(f"Validating: {self.filename}")
        print(f"{'='*60}")

        if not self._read_file():
            return False

        self._validate_frontmatter()
        self._validate_question_structure()
        self._validate_question_counts()

        if not self.errors:
            log_success(f"All {sum(self.stats.values())} questions are valid!")
            log_info(f"   True/False: {self.stats['true_false']}")
            log_info(f"   Multiple Choice: {self.stats['multiple_choice']}")
            log_info(f"   Matching: {self.stats['matching']}")
            return True
        else:
            log_error(f"Found {len(self.errors)} error(s) in {self.filename}")
            for err in self.errors:
                log_error(f"  Line ~{err[0]}: {err[1]}")
            for warn in self.warnings:
                log_warning(f"  Line ~{warn[0]}: {warn[1]}")
            return False

    def _read_file(self):
        """Read the file content."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.content = f.read()
            self.lines = self.content.split("\n")
            return True
        except FileNotFoundError:
            log_error(f"File not found: {self.filepath}")
            return False
        except Exception as e:
            log_error(f"Error reading file: {e}")
            return False

    def _validate_frontmatter(self):
        """Validate YAML frontmatter opening and closing."""
        if not self.content.startswith("---\n"):
            self.errors.append((1, "File must start with YAML frontmatter (---)"))

        # Find closing --- of frontmatter
        frontmatter_end = self.content.find("\n---", 4)
        if frontmatter_end == -1:
            self.errors.append((1, "YAML frontmatter closing (---) not found"))
            return

        frontmatter = self.content[4:frontmatter_end]

        # Check for sources key
        if "sources:" not in frontmatter:
            self.errors.append((2, "Frontmatter must contain 'sources:' key"))

        # Check for at least one wiki-link
        wiki_links = re.findall(r"\[\[.*?\]\]", frontmatter)
        if not wiki_links:
            self.warnings.append(
                (2, "No wiki-links [[...]] found in sources in frontmatter")
            )

    def _validate_question_structure(self):
        """Validate each question block in the file."""
        # Remove frontmatter
        frontmatter_end = self.content.find("\n---", 4)
        body = self.content[frontmatter_end + 5 :]  # +5 for \n---\n

        # Split into question blocks by [!question]
        # But we need to be careful - [!question] can appear as > [!question] or >> [!question]
        question_blocks = re.split(r"\n(?=>\s*\[!question\])", body)

        for i, block in enumerate(question_blocks):
            block = block.strip()
            if not block:
                continue
            self._validate_single_question(block, i + 1)

    def _validate_single_question(self, block, question_num):
        """Validate a single question block."""
        lines = block.split("\n")

        # Determine question type
        is_true_false = self._is_true_false(block)
        is_multiple_choice = self._is_multiple_choice(block)
        is_matching = self._is_matching(block)

        types_found = sum([is_true_false, is_multiple_choice, is_matching])

        if types_found == 0:
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"Question block {question_num}: Could not determine question type")
            )
            return
        elif types_found > 1:
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"Question block {question_num}: Ambiguous question type (matches multiple patterns)")
            )
            return

        if is_true_false:
            self.stats["true_false"] += 1
            self._validate_true_false(block, question_num)
        elif is_multiple_choice:
            self.stats["multiple_choice"] += 1
            self._validate_multiple_choice(block, question_num)
        elif is_matching:
            self.stats["matching"] += 1
            self._validate_matching(block, question_num)

    def _is_true_false(self, block):
        """Check if block is a True/False question."""
        # T/F: Has a [!question] line with a statement, and answer is just True/False
        has_question = re.search(r">\s*\[!question\]", block)
        has_answer = re.search(r">>\s*\[!success\]-\s*Answer", block)
        answer_lines = re.findall(r">>\s*(True|False)", block)
        # Should not have options a) b) c) d) or [!example]
        has_options = re.search(r">\s+a\)", block)
        has_example = re.search(r"\[!example\]", block)

        if has_question and has_answer and answer_lines and not has_options and not has_example:
            # Verify answer is just True or False (not a letter)
            return True
        return False

    def _is_multiple_choice(self, block):
        """Check if block is a Multiple Choice question."""
        has_question = re.search(r">\s*\[!question\]", block)
        has_answer = re.search(r">>\s*\[!success\]-\s*Answer", block)
        # Has options like a) b) c) d)
        has_options = re.search(r">\s+[a-d]\)", block)
        # Answer should be a letter like a) text
        answer_letter = re.search(r">>\s+[a-d]\)", block)
        has_example = re.search(r"\[!example\]", block)

        if has_question and has_options and has_answer and not has_example:
            return True
        return False

    def _is_matching(self, block):
        """Check if block is a Matching question."""
        has_question = re.search(r">\s*\[!question\]", block)
        has_answer = re.search(r">>\s*\[!success\]-\s*Answer", block)
        has_example = re.search(r"\[!example\]", block)
        has_group_a = re.search(r"\[!example\]\s*Group A", block)
        has_group_b = re.search(r"\[!example\]\s*Group B", block)
        has_arrow = re.search(r">>\s+[a-z]\)\s*->\s*[a-z]\)", block)

        if has_question and has_example and has_answer and has_arrow:
            return True
        return False

    def _validate_true_false(self, block, question_num):
        """Validate True/False question structure."""
        # Check answer is exactly "True" or "False"
        answer_match = re.findall(r">>\s*(True|False)", block)
        if not answer_match:
            self.errors.append(
                (self._find_line_number(block.split("\n")[0]),
                 f"T/F Question {question_num}: Answer must be 'True' or 'False'")
            )
        elif len(answer_match) > 1:
            self.warnings.append(
                (self._find_line_number(block.split("\n")[0]),
                 f"T/F Question {question_num}: Multiple answer values found: {answer_match}")
            )

        # Check question callout format
        if not re.search(r">\s*\[!question\]", block):
            self.errors.append(
                (self._find_line_number(block.split("\n")[0]),
                 f"T/F Question {question_num}: Missing '[!question]' callout")
            )

        # Check answer callout format
        if not re.search(r">>\s*\[!success\]-\s*Answer", block):
            self.errors.append(
                (self._find_line_number(block.split("\n")[0]),
                 f"T/F Question {question_num}: Missing '[!success]- Answer' callout")
            )

    def _validate_multiple_choice(self, block, question_num):
        """Validate Multiple Choice question structure."""
        lines = block.split("\n")

        # Check question callout
        if not re.search(r">\s*\[!question\]", block):
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"MC Question {question_num}: Missing '[!question]' callout")
            )

        # Check answer callout
        if not re.search(r">>\s*\[!success\]-\s*Answer", block):
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"MC Question {question_num}: Missing '[!success]- Answer' callout")
            )

        # Check that options are present (a, b, c, d at minimum)
        options = re.findall(r">\s+([a-d])\)", block)
        if len(options) < 2:
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"MC Question {question_num}: Must have at least 2 options (a, b, ...). Found: {len(options)}")
            )

        # Check answer is one of the options
        answer_match = re.search(r">>\s+([a-d])\)", block)
        if answer_match:
            answer_letter = answer_match.group(1)
            if answer_letter not in options:
                self.errors.append(
                    (self._find_line_number(lines[0]),
                     f"MC Question {question_num}: Answer '{answer_letter})' is not one of the options {options}")
                )

    def _validate_matching(self, block, question_num):
        """Validate Matching question structure."""
        lines = block.split("\n")

        # Check question callout
        if not re.search(r">\s*\[!question\]", block):
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"Matching Question {question_num}: Missing '[!question]' callout")
            )

        # Check Group A and Group B
        if not re.search(r"\[!example\]\s*Group A", block):
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"Matching Question {question_num}: Missing '[!example] Group A'")
            )

        if not re.search(r"\[!example\]\s*Group B", block):
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"Matching Question {question_num}: Missing '[!example] Group B'")
            )

        # Check answer callout
        if not re.search(r">>\s*\[!success\]-\s*Answer", block):
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"Matching Question {question_num}: Missing '[!success]- Answer' callout")
            )

        # Check arrow notation in answers
        arrow_matches = re.findall(r">>\s+([a-z])\)\s*->\s*([a-z])\)", block)
        if not arrow_matches:
            self.errors.append(
                (self._find_line_number(lines[0]),
                 f"Matching Question {question_num}: No arrow mappings (e.g., 'a) -> p)') found in answer")
            )

    def _validate_question_counts(self):
        """Validate that we have the expected number of each type."""
        total = sum(self.stats.values())

        # Count actual question callouts
        actual_questions = len(re.findall(r">\s*\[!question\]", self.content))
        # But some might be inside matching groups, so let's be more precise
        # Count top-level [!question] callouts (at the start of a line, not indented with >>)
        top_level_questions = len(
            re.findall(r"^>\s*\[!question\]", self.content, re.MULTILINE)
        )

        if total != top_level_questions:
            self.warnings.append(
                (1,
                 f"Question count mismatch: {total} classified vs {top_level_questions} '[!question]' callouts found")
            )

    def _find_line_number(self, line_text):
        """Find the approximate line number of a text in the file."""
        for i, line in enumerate(self.lines, 1):
            if line_text.strip() in line:
                return i
        return 0


def find_markdown_files(paths):
    """Find all .md files from the given paths, or recursively from current dir."""
    md_files = []
    for path in paths:
        if os.path.isfile(path) and path.endswith(".md"):
            md_files.append(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    if f.endswith(".md"):
                        md_files.append(os.path.join(root, f))
    return md_files


def main():
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        # Default: look for .md files in subdirectories
        paths = ["."]

    md_files = find_markdown_files(paths)

    if not md_files:
        log_warning("No markdown files found to validate.")
        log_info("Usage: python quiz_validator.py <file1.md> [file2.md ...]")
        log_info("   or: python quiz_validator.py <directory>")
        sys.exit(0)

    results = []
    for f in md_files:
        validator = QuizValidator(f)
        is_valid = validator.validate()
        results.append((f, is_valid, validator.stats))

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    valid_count = sum(1 for r in results if r[1])
    total_questions = sum(
        sum(r[2].values()) for r in results
    )
    print(f"Files validated: {len(results)}")
    print(f"Files valid:     {valid_count}")
    print(f"Files invalid:   {len(results) - valid_count}")
    print(f"Total questions: {total_questions}")

    for f, is_valid, stats in results:
        status = f"{GREEN}VALID{RESET}" if is_valid else f"{RED}INVALID{RESET}"
        tf = stats["true_false"]
        mc = stats["multiple_choice"]
        mt = stats["matching"]
        print(f"  {status} - {os.path.basename(f)} (TF:{tf} MC:{mc} Match:{mt})")

    if valid_count == len(results):
        print(f"\n{GREEN}All files passed validation!{RESET}")
        return 0
    else:
        print(f"\n{RED}Some files have errors. Please fix them and re-run.{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())