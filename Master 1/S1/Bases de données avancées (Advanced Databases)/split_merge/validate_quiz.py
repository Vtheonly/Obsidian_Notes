#!/usr/bin/env python3
"""
Quiz File Validator
Validates generated quiz Markdown files for correct structure and syntax.
Checks: frontmatter, True/False, Multiple Choice, Matching blocks.
"""

import os
import re
import sys
import yaml

def validate_frontmatter(content, filepath):
    """Validate YAML frontmatter exists and has sources."""
    if not content.startswith('---'):
        return [f"{filepath}: Missing opening '---' for frontmatter"]
    end = content.find('---', 3)
    if end == -1:
        return [f"{filepath}: Missing closing '---' for frontmatter"]
    fm = content[3:end].strip()
    errors = []
    try:
        data = yaml.safe_load(fm)
        if not isinstance(data, dict):
            errors.append(f"{filepath}: Frontmatter must be a dictionary")
        elif 'sources' not in data:
            errors.append(f"{filepath}: Frontmatter missing 'sources' key")
        elif not isinstance(data['sources'], list):
            errors.append(f"{filepath}: 'sources' must be a list")
        elif len(data['sources']) == 0:
            errors.append(f"{filepath}: 'sources' list is empty")
    except yaml.YAMLError as e:
        errors.append(f"{filepath}: YAML frontmatter parse error: {e}")
    return errors


def validate_tf_question(lines, start_idx, filepath, line_offset):
    """Validate a True/False question block."""
    errors = []
    # First line should be > [!question] ...
    if not re.match(r'^> \[!question\]', lines[start_idx]):
        errors.append(f"{filepath}:{line_offset + start_idx + 1}: Expected '> [!question]' for T/F question")
    
    # Find the answer line
    answer_found = False
    for i in range(start_idx + 1, min(start_idx + 5, len(lines))):
        stripped = lines[i].strip()
        if stripped.startswith('>> [!success]- Answer'):
            answer_found = True
            # Check the next line has an answer
            if i + 1 < len(lines):
                ans_line = lines[i + 1].strip()
                if ans_line not in ['>> True', '>> False', '>> True (or similar)', '>> False (or similar)']:
                    if not re.match(r'^>> (True|False)$', ans_line):
                        errors.append(f"{filepath}:{line_offset + i + 2}: Answer must be '>> True' or '>> False', got '{ans_line}'")
            break
    
    if not answer_found:
        errors.append(f"{filepath}:{line_offset + start_idx + 1}: Missing '>> [!success]- Answer' block in T/F question")
    
    return errors


def validate_mcq_question(lines, start_idx, filepath, line_offset):
    """Validate a Multiple Choice question block."""
    errors = []
    if not re.match(r'^> \[!question\]', lines[start_idx]):
        errors.append(f"{filepath}:{line_offset + start_idx + 1}: Expected '> [!question]' for MCQ")
    
    # Check for options (a, b, c, d)
    options_found = 0
    option_lines = []
    for i in range(start_idx + 1, min(start_idx + 10, len(lines))):
        stripped = lines[i].strip()
        if re.match(r'^> [a-d]\)', stripped):
            options_found += 1
            option_lines.append(stripped)
        elif stripped.startswith('>> [!success]- Answer'):
            break
    
    if options_found < 2:
        errors.append(f"{filepath}:{line_offset + start_idx + 1}: MCQ has only {options_found} options (need at least 2)")
    
    # Check for answer
    answer_found = False
    for i in range(start_idx + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith('>> [!success]- Answer'):
            answer_found = True
            if i + 1 < len(lines):
                ans_line = lines[i + 1].strip()
                if not re.match(r'^>> [a-d]\)', ans_line):
                    errors.append(f"{filepath}:{line_offset + i + 2}: MCQ answer must be '>> a)' format, got '{ans_line}'")
            break
    
    if not answer_found:
        errors.append(f"{filepath}:{line_offset + start_idx + 1}: Missing '>> [!success]- Answer' block in MCQ")
    
    return errors


def validate_matching_question(lines, start_idx, filepath, line_offset):
    """Validate a Matching question block."""
    errors = []
    if not re.match(r'^> \[!question\]', lines[start_idx]):
        errors.append(f"{filepath}:{line_offset + start_idx + 1}: Expected '> [!question]' for Matching question")
    
    # Check for Group A
    group_a_found = False
    group_b_found = False
    answer_found = False
    
    for i in range(start_idx + 1, min(start_idx + 30, len(lines))):
        stripped = lines[i].strip()
        if stripped.startswith('>> [!example] Group A'):
            group_a_found = True
        elif stripped.startswith('>> [!example] Group B'):
            group_b_found = True
        elif stripped.startswith('>> [!success]- Answer'):
            answer_found = True
            # Validate answer format
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith('>> '):
                ans_line = lines[j].strip()
                if not re.match(r'^>> [a-z]+\)\s*->\s*[a-z]+\)$', ans_line):
                    errors.append(f"{filepath}:{line_offset + j + 1}: Matching answer must be '>> a) -> n)' format, got '{ans_line}'")
                j += 1
    
    if not group_a_found:
        errors.append(f"{filepath}:{line_offset + start_idx + 1}: Missing '>> [!example] Group A' in Matching question")
    if not group_b_found:
        errors.append(f"{filepath}:{line_offset + start_idx + 1}: Missing '>> [!example] Group B' in Matching question")
    if not answer_found:
        errors.append(f"{filepath}:{line_offset + start_idx + 1}: Missing '>> [!success]- Answer' block in Matching question")
    
    return errors


def validate_file(filepath):
    """Validate a single quiz file."""
    errors = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Check file is not empty
    if not content.strip():
        errors.append(f"{filepath}: File is empty")
        return errors
    
    # Validate frontmatter
    errors.extend(validate_frontmatter(content, filepath))
    
    # Remove frontmatter for question parsing
    fm_end = content.find('---', 3)
    if fm_end != -1:
        rest = content[fm_end + 3:].strip()
        question_lines = rest.split('\n')
    else:
        question_lines = lines
    
    # Count questions by type
    tf_count = 0
    mcq_count = 0
    matching_count = 0
    total_questions = 0
    
    i = 0
    while i < len(question_lines):
        stripped = question_lines[i].strip()
        
        if stripped.startswith('> [!question]'):
            total_questions += 1
            # Determine type by looking ahead
            next_lines = []
            for j in range(i + 1, min(i + 30, len(question_lines))):
                if question_lines[j].strip().startswith('> [!question]'):
                    break
                next_lines.append(question_lines[j].strip())
            
            next_text = ' '.join(next_lines)
            
            if '>> [!example] Group A' in next_text or '>> [!example] Group B' in next_text:
                matching_count += 1
                errs = validate_matching_question(question_lines, i, filepath, fm_end + 3 if fm_end != -1 else 0)
                errors.extend(errs)
            elif any(re.match(r'^> [a-d]\)', l) for l in next_lines):
                mcq_count += 1
                errs = validate_mcq_question(question_lines, i, filepath, fm_end + 3 if fm_end != -1 else 0)
                errors.extend(errs)
            else:
                tf_count += 1
                errs = validate_tf_question(question_lines, i, filepath, fm_end + 3 if fm_end != -1 else 0)
                errors.extend(errs)
        
        i += 1
    
    # Check question counts
    if total_questions != 30:
        errors.append(f"{filepath}: Has {total_questions} questions, expected 30")
    
    if tf_count != 10:
        errors.append(f"{filepath}: Has {tf_count} True/False questions, expected 10")
    if mcq_count != 10:
        errors.append(f"{filepath}: Has {mcq_count} Multiple Choice questions, expected 10")
    if matching_count != 10:
        errors.append(f"{filepath}: Has {matching_count} Matching questions, expected 10")
    
    return errors


def main():
    """Main validation entry point."""
    quiz_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Quiz')
    
    if not os.path.exists(quiz_dir):
        print(f"ERROR: Quiz directory not found: {quiz_dir}")
        sys.exit(1)
    
    all_errors = []
    validated_files = 0
    
    for root, dirs, files in os.walk(quiz_dir):
        for fname in sorted(files):
            if fname.endswith('.md'):
                filepath = os.path.join(root, fname)
                errors = validate_file(filepath)
                validated_files += 1
                if errors:
                    all_errors.extend(errors)
                    for err in errors:
                        print(f"  FAIL: {err}")
                else:
                    rel = os.path.relpath(filepath, quiz_dir)
                    print(f"  PASS: {rel}")
    
    print(f"\n{'='*60}")
    print(f"Validated {validated_files} file(s)")
    
    if all_errors:
        print(f"Found {len(all_errors)} error(s)")
        sys.exit(1)
    else:
        print("All files passed validation!")
        sys.exit(0)


if __name__ == '__main__':
    main()