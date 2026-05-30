#!/usr/bin/env python3
"""Validate all quiz markdown files for correct structure and syntax."""
import os, re, sys, glob

def validate_file(filepath):
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split("\n")
    
    # Check YAML frontmatter
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter opening ---")
    if lines.count("---") < 2:
        errors.append("Missing YAML frontmatter closing ---")
    if "sources:" not in content.split("---")[1] if len(content.split("---")) > 1 else True:
        errors.append("Missing sources in YAML frontmatter")
    
    # Count question types
    tf_count = 0
    mcq_count = 0
    match_count = 0
    
    # Find all question blocks
    in_question = False
    question_type = None
    
    for i, line in enumerate(lines):
        # Check for question start
        if line.startswith("> [!question] "):
            in_question = True
            question_type = None
            continue
        
        if in_question:
            # Check if this is a T/F answer
            if line.startswith(">> [!success]- Answer"):
                continue
            if line.startswith(">> True") or line.startswith(">> False"):
                if question_type is None:
                    tf_count += 1
                    question_type = "tf"
                continue
            
            # Check if MCQ options start
            if re.match(r"^> [a-d]\) ", line):
                if question_type is None:
                    question_type = "mcq"
                continue
            
            # Check if matching starts
            if line.startswith(">> [!example] Group A"):
                if question_type is None:
                    question_type = "matching"
                continue
            
            # Check matching items
            if re.match(r"^>> [a-d]\) ", line):
                continue
            if line.startswith(">\n>> [!example] Group B"):
                continue
            if re.match(r"^>> [n-q]\) ", line):
                continue
            
            # Check matching answers
            if line.startswith(">> [a-d]) -> ["):
                continue
            if re.match(r"^>> [a-d]\) -> [", line):
                continue
            
            # If we reach here, question ended
            if question_type == "tf":
                tf_count += 1
            elif question_type == "mcq":
                mcq_count += 1
            elif question_type == "matching":
                match_count += 1
            else:
                # Check what type this question was
                pass
            
            in_question = False
            question_type = None
    
    # Final count check
    total = tf_count + mcq_count + match_count
    if total != 30:
        errors.append(f"Total questions: {total} (expected 30)")
    if tf_count != 10:
        errors.append(f"True/False questions: {tf_count} (expected 10)")
    if mcq_count != 10:
        errors.append(f"MCQ questions: {mcq_count} (expected 10)")
    if match_count != 10:
        errors.append(f"Matching questions: {match_count} (expected 10)")
    
    # Check structure
    if not re.search(r"^> \[!question\] ", content, re.MULTILINE):
        errors.append("No question blocks found")
    
    # Check answers exist
    if ">> [!success]- Answer" not in content:
        errors.append("No answer blocks found")
    
    # Check MCQ format
    mcq_questions = re.findall(r"> \[!question\] (.*?)\n> [a-d]\)", content)
    
    # Check matching format
    match_groups = content.count("[!example] Group A")
    match_groups_b = content.count("[!example] Group B")
    if match_groups != match_groups_b:
        errors.append(f"Mismatched Group A ({match_groups}) and Group B ({match_groups_b})")
    
    return errors, {"tf": tf_count, "mcq": mcq_count, "match": match_count, "total": total}

def main():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Quiz")
    files = sorted(glob.glob(os.path.join(base, "Chapter *", "*_Quiz_*.md")))
    
    print(f"Validating {len(files)} quiz files...\n")
    
    all_valid = True
    total_questions = 0
    
    for f in files:
        rel = os.path.relpath(f, base)
        errors, counts = validate_file(f)
        
        if errors:
            all_valid = False
            print(f"FAIL: {rel}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"OK: {rel} ({counts['total']} questions: {counts['tf']} TF, {counts['mcq']} MCQ, {counts['match']} Matching)")
            total_questions += counts['total']
    
    print(f"\n{'='*50}")
    if all_valid:
        print(f"ALL {len(files)} files PASSED validation")
        print(f"Total questions: {total_questions}")
    else:
        print(f"SOME files FAILED - see above for details")
        sys.exit(1)

if __name__ == "__main__":
    main()