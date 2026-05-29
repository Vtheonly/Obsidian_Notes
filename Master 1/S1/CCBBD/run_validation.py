#!/usr/bin/env python3
"""Quick validation script that imports the ObsidianQuizValidator directly."""
import sys
import os
sys.path.insert(0, "split_merge")
from vault_manager.services.validator import ObsidianQuizValidator

quiz_dir = "Quiz"
validator = ObsidianQuizValidator()
all_passed = 0
all_failed = 0

for root, dirs, files in os.walk(quiz_dir):
    for f in sorted(files):
        if f.endswith(".md"):
            path = os.path.join(root, f)
            report = validator.validate(path)
            if report.is_valid:
                print(f"  PASS: {path} -> {report.stats}")
                all_passed += 1
            else:
                print(f"  FAIL: {path}")
                for line, err in report.errors:
                    print(f"        Line ~{line}: {err}")
                all_failed += 1

print(f"\nTotal: {all_passed + all_failed} | Passed: {all_passed} | Failed: {all_failed}")
sys.exit(0 if all_failed == 0 else 1)