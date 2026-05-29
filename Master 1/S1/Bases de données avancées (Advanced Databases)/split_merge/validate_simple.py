#!/usr/bin/env python3
"""Simple validation of quiz files - counts questions by type."""

import os
import re
import sys

quiz_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Quiz')

all_pass = True
file_count = 0

for root, dirs, files in os.walk(quiz_dir):
    for fname in sorted(files):
        if not fname.endswith('.md'):
            continue
        
        fp = os.path.join(root, fname)
        with open(fp) as f:
            content = f.read()
        
        lines = content.strip().split('\n')
        file_count += 1
        
        tf = mcq = match = total = 0
        i = 0
        while i < len(lines):
            if lines[i].strip().startswith('> [!question]'):
                total += 1
                next_text = ''
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('> [!question]'):
                    next_text += lines[j].strip() + ' '
                    j += 1
                
                if '>> [!example] Group A' in next_text:
                    match += 1
                elif re.search(r'> [a-d]\)', next_text):
                    mcq += 1
                else:
                    tf += 1
            i += 1
        
        rel = os.path.relpath(fp, quiz_dir)
        status = 'PASS' if (total == 30 and tf == 10 and mcq == 10 and match == 10) else 'FAIL'
        if status == 'FAIL':
            all_pass = False
            reasons = []
            if total != 30: reasons.append(f'{total}q (expected 30)')
            if tf != 10: reasons.append(f'{tf}TF (expected 10)')
            if mcq != 10: reasons.append(f'{mcq}MCQ (expected 10)')
            if match != 10: reasons.append(f'{match}Match (expected 10)')
            print(f'  FAIL: {rel} - {", ".join(reasons)}')
        else:
            print(f'  PASS: {rel}')

print(f'\nValidated {file_count} file(s)')
if all_pass:
    print('ALL FILES PASSED VALIDATION!')
else:
    print('Some files have errors.')
    sys.exit(1)