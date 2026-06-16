#!/usr/bin/env python3
"""Direct validation script using ObsidianQuizValidator."""
import sys
import os

# Add the split_merge directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'split_merge'))

from vault_manager.services.validator import ObsidianQuizValidator

validator = ObsidianQuizValidator()

quiz_dir = os.path.join(os.path.dirname(__file__))
files_to_check = []
for root, _, files in os.walk(quiz_dir):
    for f in files:
        if f.endswith(".md"):
            files_to_check.append(os.path.join(root, f))

files_to_check = sorted(files_to_check)
if not files_to_check:
    print("No markdown files found in Quiz/")
    sys.exit(1)

valid_count = 0
for f in files_to_check:
    report = validator.validate(f)
    if report.is_valid:
        print(f"  VALID: {os.path.relpath(f, quiz_dir)}")
        print(f"         Stats: {report.stats}")
        valid_count += 1
    else:
        print(f"  INVALID: {os.path.relpath(f, quiz_dir)}")
        for line, err in report.errors:
            print(f"           Line ~{line}: {err}")
        for line, warn in report.warnings:
            print(f"           Line ~{line}: WARN: {warn}")

total = len(files_to_check)
print(f"\n{'='*50}")
print(f"Total files: {total}")
print(f"Passed:      {valid_count}")
print(f"Failed:      {total - valid_count}")
print(f"{'='*50}")

sys.exit(0 if valid_count == total else 1)