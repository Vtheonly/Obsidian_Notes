"""
Quiz Markup callouts validation suite.
Enforces the structural formatting rules of the Quiz files,
validating YAML frontmatter elements, markdown callouts, and questions.
"""

import os
import re
from typing import List, Optional
from vault_manager.core.interfaces import ContentValidator
from vault_manager.core.models import QuizValidationResult, QuizQuestionStats
from vault_manager.logging import logger


class ObsidianQuizValidator(ContentValidator):
    """
    Validates structural consistency and Obsidian callouts syntax 
    across target quiz documents.
    """

    def validate(self, filepath: str) -> bool:
        """Validates a single quiz file against formatting rules, logging any issues found."""
        result = self.analyze_quiz(filepath)
        
        if result.is_valid:
            logger.success(f"Quiz file is valid: {os.path.basename(filepath)}")
            logger.info(f"    - True/False: {result.stats.true_false}")
            logger.info(f"    - Multiple Choice: {result.stats.multiple_choice}")
            logger.info(f"    - Matching: {result.stats.matching}")
            return True
        
        logger.error(f"Validation failed for: {os.path.basename(filepath)}")
        for line_num, err_msg in result.errors:
            logger.error(f"  Line ~{line_num}: {err_msg}")
        for line_num, warn_msg in result.warnings:
            logger.warning(f"  Line ~{line_num}: {warn_msg}")
        return False

    def analyze_quiz(self, filepath: str) -> QuizValidationResult:
        """Runs validation checks on a quiz file and returns detailed results."""
        result = QuizValidationResult(filepath=filepath, is_valid=True)
        
        if not os.path.exists(filepath):
            result.is_valid = False
            result.errors.append((0, f"File not found on system path: {filepath}"))
            return result

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result.is_valid = False
            result.errors.append((0, f"Failed file I/O operations: {e}"))
            return result

        lines = content.split('\n')

        # 1. Validate YAML Metadata block
        if not content.startswith("---\n"):
            result.errors.append((1, "File must start with YAML metadata (---)"))
            result.is_valid = False

        closing_yaml = content.find("\n---", 4)
        if closing_yaml == -1:
            result.errors.append((1, "Closing YAML metadata element (---) not found"))
            result.is_valid = False
            return result

        frontmatter = content[4:closing_yaml]
        if "sources:" not in frontmatter:
            result.errors.append((2, "Metadata is missing the required 'sources' key"))
            result.is_valid = False

        if not re.findall(r"\[\[.*?\]\]", frontmatter):
            result.warnings.append((2, "No wiki-links [[...]] found inside metadata sources block"))

        # 2. Extract and validate question block content
        body = content[closing_yaml + 5:]
        # Split blocks by start of [!question] lines
        question_blocks = re.split(r"\n(?=>\s*\[!question\])", body)

        for idx, block in enumerate(question_blocks):
            block = block.strip()
            if not block:
                continue
            self._validate_question_block(block, idx + 1, lines, result)

        # 3. Final structural assertions
        total_classified = result.stats.total()
        top_level_callouts = len(re.findall(r"^>\s*\[!question\]", content, re.MULTILINE))

        if total_classified != top_level_callouts:
            result.warnings.append((
                1, f"Mismatch: Identified {total_classified} questions, but found {top_level_callouts} raw question callouts."
            ))

        if result.errors:
            result.is_valid = False

        return result

    def _validate_question_block(self, block: str, num: int, file_lines: List[str], result: QuizValidationResult) -> None:
        """Parses and validates a single question block."""
        first_line = block.split('\n')[0]
        approx_line = self._find_approximate_line(first_line, file_lines)

        is_tf = self._is_true_false(block)
        is_mc = self._is_multiple_choice(block)
        is_match = self._is_matching(block)

        types_matched = sum([is_tf, is_mc, is_match])

        if types_matched == 0:
            result.errors.append((approx_line, f"Question block {num}: Could not classify question type."))
            return
        elif types_matched > 1:
            result.errors.append((approx_line, f"Question block {num}: Matches multiple question patterns."))
            return

        if is_tf:
            result.stats.true_false += 1
            self._validate_true_false_format(block, num, approx_line, result)
        elif is_mc:
            result.stats.multiple_choice += 1
            self._validate_mc_format(block, num, approx_line, result, file_lines)
        elif is_match:
            result.stats.matching += 1
            self._validate_matching_format(block, num, approx_line, result)

    @staticmethod
    def _is_true_false(block: str) -> bool:
        """Returns True if the block matches a True/False question format."""
        has_q = re.search(r">\s*\[!question\]", block)
        has_ans_callout = re.search(r">>\s*\[!success\]-\s*Answer", block)
        has_ans = re.search(r">>\s*(True|False)", block)
        has_opt = re.search(r">\s+a\)", block)
        has_ex = re.search(r"\[!example\]", block)
        return bool(has_q and has_ans_callout and has_ans and not has_opt and not has_ex)

    @staticmethod
    def _is_multiple_choice(block: str) -> bool:
        """Returns True if the block matches a Multiple Choice question format."""
        has_q = re.search(r">\s*\[!question\]", block)
        has_ans_callout = re.search(r">>\s*\[!success\]-\s*Answer", block)
        has_opt = re.search(r">\s+[a-d]\)", block)
        return bool(has_q and has_opt and has_ans_callout and not re.search(r"\[!example\]", block))

    @staticmethod
    def _is_matching(block: str) -> bool:
        """Returns True if the block matches a Matching question format."""
        has_q = re.search(r">\s*\[!question\]", block)
        has_ans_callout = re.search(r">>\s*\[!success\]-\s*Answer", block)
        has_ex = re.search(r"\[!example\]", block)
        has_arrow = re.search(r">>\s+[a-z]\)\s*->\s*[a-z]\)", block)
        return bool(has_q and has_ex and has_ans_callout and has_arrow)

    @staticmethod
    def _validate_true_false_format(block: str, num: int, line_no: int, result: QuizValidationResult) -> None:
        """Validates formatting for True/False questions."""
        answers = re.findall(r">>\s*(True|False)", block)
        if not answers:
            result.errors.append((line_no, f"T/F Question {num}: Must have a 'True' or 'False' answer value."))
        elif len(answers) > 1:
            result.warnings.append((line_no, f"T/F Question {num}: Found multiple answer definitions: {answers}"))

        if not re.search(r">\s*\[!question\]", block):
            result.errors.append((line_no, f"T/F Question {num}: Missing parent '[!question]' callout block."))
        if not re.search(r">>\s*\[!success\]-\s*Answer", block):
            result.errors.append((line_no, f"T/F Question {num}: Missing nested '[!success]- Answer' block."))

    @staticmethod
    def _validate_mc_format(block: str, num: int, line_no: int, result: QuizValidationResult, file_lines: List[str]) -> None:
        """Validates formatting for Multiple Choice questions."""
        if not re.search(r">\s*\[!question\]", block):
            result.errors.append((line_no, f"MC Question {num}: Missing parent '[!question]' callout block."))
        if not re.search(r">>\s*\[!success\]-\s*Answer", block):
            result.errors.append((line_no, f"MC Question {num}: Missing nested '[!success]- Answer' block."))

        options = re.findall(r">\s+([a-d])\)", block)
        if len(options) < 2:
            result.errors.append((line_no, f"MC Question {num}: Expected at least 2 options. Found options: {options}"))

        ans_match = re.search(r">>\s+([a-d])\)", block)
        if ans_match:
            ans_letter = ans_match.group(1)
            if ans_letter not in options:
                result.errors.append((line_no, f"MC Question {num}: Declared answer '{ans_letter})' is not in available choices {options}."))

    @staticmethod
    def _validate_matching_format(block: str, num: int, line_no: int, result: QuizValidationResult) -> None:
        """Validates formatting for Matching questions."""
        if not re.search(r">\s*\[!question\]", block):
            result.errors.append((line_no, f"Matching Question {num}: Missing parent '[!question]' callout block."))
        if not re.search(r"\[!example\]\s*Group A", block):
            result.errors.append((line_no, f"Matching Question {num}: Missing '[!example] Group A' label."))
        if not re.search(r"\[!example\]\s*Group B", block):
            result.errors.append((line_no, f"Matching Question {num}: Missing '[!example] Group B' label."))
        if not re.search(r">>\s*\[!success\]-\s*Answer", block):
            result.errors.append((line_no, f"Matching Question {num}: Missing nested '[!success]- Answer' block."))

        mappings = re.findall(r">>\s+([a-z])\)\s*->\s*([a-z])\)", block)
        if not mappings:
            result.errors.append((line_no, f"Matching Question {num}: Answer is missing target mappings (e.g. 'a) -> x)')."))

    @staticmethod
    def _find_approximate_line(matched_text: str, file_lines: List[str]) -> int:
        """Locates the line number of a text pattern in the file."""
        for i, line in enumerate(file_lines, 1):
            if matched_text.strip() in line:
                return i
        return 1