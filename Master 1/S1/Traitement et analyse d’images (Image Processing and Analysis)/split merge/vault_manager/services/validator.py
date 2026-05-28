"""
Document Validation Engine.
Performs semantic audits on files, ensuring they conform to Obsidian callout rules.
"""

import re
from typing import List, Dict, Any
from vault_manager.core.interfaces import IValidationStrategy
from vault_manager.core.models import ValidationReport
from vault_manager.utils.file_ops import read_file_safely


class ObsidianQuizValidator(IValidationStrategy):
    """Validates that Quiz files adhere to the strict YAML and callout structure."""

    def validate(self, filepath: str) -> ValidationReport:
        content = read_file_safely(filepath)
        lines = content.split('\n')
        report = ValidationReport(filepath=filepath, is_valid=True)
        report.stats = {"true_false": 0, "multiple_choice": 0, "matching": 0}

        # Validate Frontmatter
        if not content.startswith("---\n"):
            report.errors.append((1, "File must begin with a YAML frontmatter block (---)"))
        
        closing_yaml = content.find("\n---", 4)
        if closing_yaml == -1:
            report.errors.append((1, "YAML frontmatter closing block (---) is missing"))
            report.is_valid = False
            return report

        frontmatter = content[4:closing_yaml]
        if "sources:" not in frontmatter:
            report.errors.append((2, "YAML frontmatter is missing the mandatory 'sources:' metadata key"))
        
        if not re.search(r"\[\[.*?\]\]", frontmatter):
            report.warnings.append((2, "No valid internal wiki-links [[Link]] found in frontmatter sources"))

        # Split into Question Blocks
        body = content[closing_yaml + 5:]
        question_blocks = re.split(r"\n(?=>\s*\[!question\])", body)

        for idx, block in enumerate(question_blocks, 1):
            block = block.strip()
            if not block:
                continue

            first_line = block.split('\n')[0]
            approx_line_num = 1
            for i, line in enumerate(lines, 1):
                if first_line.strip() in line:
                    approx_line_num = i
                    break

            is_tf = bool(re.search(r">\s*\[!question\]", block) and 
                         re.search(r">>\s*\[!success\]-\s*Answer", block) and 
                         re.search(r">>\s*(True|False)", block) and 
                         not re.search(r">\s+a\)", block) and 
                         not re.search(r"\[!example\]", block))

            is_mc = bool(re.search(r">\s*\[!question\]", block) and 
                         re.search(r">>\s*\[!success\]-\s*Answer", block) and 
                         re.search(r">\s+[a-d]\)", block) and 
                         not re.search(r"\[!example\]", block))

            is_match = bool(re.search(r">\s*\[!question\]", block) and 
                            re.search(r"\[!example\]\s*Group A", block) and 
                            re.search(r"\[!example\]\s*Group B", block) and 
                            re.search(r">>\s*[a-z]\)\s*->\s*[a-z]\)", block))

            matches_found = sum([is_tf, is_mc, is_match])

            if matches_found == 0:
                report.errors.append((approx_line_num, f"Question Block {idx}: Unable to classify question type (must be TF, MC, or Matching)."))
                continue
            elif matches_found > 1:
                report.errors.append((approx_line_num, f"Question Block {idx}: Structural conflict. Matches multiple types."))
                continue

            if is_tf:
                report.stats["true_false"] += 1
                if not re.search(r">>\s*(True|False)", block):
                    report.errors.append((approx_line_num, f"TF Question {idx}: Answer must be explicitly 'True' or 'False'"))
            elif is_mc:
                report.stats["multiple_choice"] += 1
                options = re.findall(r">\s+([a-d])\)", block)
                ans = re.search(r">>\s+([a-d])\)", block)
                if len(options) < 2:
                    report.errors.append((approx_line_num, f"MC Question {idx}: Must supply at least two valid options (a), b), etc.)"))
                if ans and ans.group(1) not in options:
                    report.errors.append((approx_line_num, f"MC Question {idx}: Declared answer '{ans.group(1)}' is not in available options {options}"))
            elif is_match:
                report.stats["matching"] += 1
                if not re.search(r">>\s*\[!success\]-\s*Answer", block):
                    report.errors.append((approx_line_num, f"Matching Question {idx}: Missing [!success]- Answer callout"))

        if report.errors:
            report.is_valid = False

        return report