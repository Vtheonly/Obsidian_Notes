#!/usr/bin/env python3
"""Compact quiz generator - writes JSON data then generates markdown files."""
import os, json, subprocess

def main():
    # Step 1: Generate the JSON data file
    subprocess.run(["python3", "split_merge/build_quiz_json.py"], check=True)
    
    # Step 2: Generate markdown from JSON
    subprocess.run(["python3", "split_merge/json_to_md.py"], check=True)

if __name__ == "__main__":
    main()