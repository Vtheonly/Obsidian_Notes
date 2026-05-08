import os
import re

"""
OBSIDIAN AUTO-LINKER AND INDEX GENERATOR
----------------------------------------
This script does two things:
1. Creates a "000 Master Index.md" with all files and their keywords.
2. Scans all your markdown files and automatically turns keywords 
   into Obsidian wiki-links (e.g., turning "encapsulation" into [[021 Encapsulation|encapsulation]]).
   It safely ignores text inside code blocks and existing links.
"""

TARGET_DIR = "."

# Mapping of Target Files to the Keywords that should link to them
# The script will look for these words in your text and create links.
KEYWORD_MAPPING = {
    "001 OOP Basics": ["OOP", "Object-Oriented Programming"],
    "002 Object": ["object", "objects", "instance"],
    "003 New Keyword": ["new keyword", "new operator"],
    "004 Compile Time vs Run Time": ["compile time", "run time", "runtime"],
    "005 Intro to Classes": ["class", "classes", "blueprint"],
    "010 Constructors and Destructors": ["constructor", "destructor"],
    "012 Static Members": ["static member", "static method", "static variable"],
    "013 Static Keyword": ["static keyword"],
    "014 Enums": ["enum", "enumerations", "enumeration"],
    "015 Final Keyword": ["final keyword"],
    "020 Encapsulation and Access Control": ["encapsulation", "access control", "access modifier", "private", "public", "protected"],
    "030 Inheritance": ["inheritance", "extends", "subclass", "superclass"],
    "032 Upcasting and Downcasting": ["upcasting", "downcasting", "type casting"],
    "033 Super Keyword": ["super keyword"],
    "034 Multiple Inheritance and The Diamond Problem": ["multiple inheritance", "diamond problem"],
    "040 Abstraction": ["abstraction"],
    "041 Abstraction Details": ["abstract class", "abstract method"],
    "042 Polymorphism Summary": ["polymorphism", "dynamic polymorphism", "static polymorphism"],
    "044 Interfaces": ["interface", "interfaces", "implements"],
    "050 Collections Overview": ["collections", "data structures"],
    "051 Arrays": ["array", "arrays"],
    "052 Collection Framework": ["collection framework", "java collections"],
    "054 List Interface": ["list interface", "arraylist", "linkedlist"],
    "055 Set Interface": ["set interface", "hashset", "treeset"],
    "056 Queues and Deques": ["queue", "deque", "fifo", "lifo"],
    "057 Map Interface": ["map interface", "hashmap", "treemap"],
    "061 Copying Objects": ["copying objects", "deep copy", "shallow copy"],
    "062 Generics": ["generics", "type erasure"],
    "063 Exceptions and Varargs": ["exception", "exceptions", "varargs"]
}

def generate_master_index():
    index_path = os.path.join(TARGET_DIR, "000 Master Index.md")
    print("Generating Master Index...")
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# 📚 Master Index: Advanced Code Patterns\n\n")
        f.write("This file acts as a Map of Content, linking to all topics and their main keywords.\n\n")
        
        for target, keywords in KEYWORD_MAPPING.items():
            # Check if file exists to link it properly
            if os.path.exists(os.path.join(TARGET_DIR, target + ".md")):
                f.write(f"- **[[{target}]]**\n")
                f.write(f"  - *Keywords*: {', '.join(keywords)}\n")
                
    print(f"Created: {index_path}\n")

def auto_link_files():
    print("Auto-linking keywords across all files...")
    # Regex to split by code blocks, inline code, and existing links
    # so we don't accidentally link inside them.
    ignore_pattern = re.compile(r'(```.*?```|`.*?`|\[\[.*?\]\]|\[.*?\]\(.*?\))', re.DOTALL)
    
    linked_count = 0
    
    for filename in os.listdir(TARGET_DIR):
        if not filename.endswith(".md") or filename == "000 Master Index.md":
            continue
            
        filepath = os.path.join(TARGET_DIR, filename)
        current_name = filename.replace(".md", "")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tokens = ignore_pattern.split(content)
        modified = False
        
        # Keep track of what we linked in this file so we only link a keyword once per file 
        # to avoid link spam
        linked_in_this_file = set()
        
        for target_file, keywords in KEYWORD_MAPPING.items():
            # Don't link a file to itself
            if target_file == current_name:
                continue
                
            for keyword in keywords:
                if target_file in linked_in_this_file:
                    break # Already linked to this target in this file
                    
                # Search only in normal text (even indices)
                for i in range(0, len(tokens), 2):
                    text = tokens[i]
                    
                    # Regex to find the keyword with word boundaries, case insensitive
                    pattern = re.compile(r'\b(' + re.escape(keyword) + r')\b', re.IGNORECASE)
                    
                    if pattern.search(text):
                        # Replace only the first occurrence to avoid link spam
                        tokens[i] = pattern.sub(r'[[' + target_file + r'|\1]]', text, count=1)
                        modified = True
                        linked_in_this_file.add(target_file)
                        break # Move to next keyword/target once linked

        if modified:
            new_content = ''.join(tokens)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            linked_count += 1
            print(f"Added links to: {filename}")
            
    print(f"\nSuccessfully auto-linked keywords in {linked_count} files.")

if __name__ == "__main__":
    generate_master_index()
    
    confirm = input("Do you want to automatically scan all files and convert keywords into internal [[links]]? (y/n): ")
    if confirm.lower() == 'y':
        auto_link_files()
    else:
        print("Auto-linking skipped.")
