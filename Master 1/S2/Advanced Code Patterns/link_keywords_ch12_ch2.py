import os
import re

KEYWORD_MAPPING = {
    # Chapter 1.2
    "101 Static vs Dynamic Views": ["static view", "dynamic view", "class diagram", "object diagram"],
    "102 Anatomy of a Class": ["class anatomy", "class diagram", "attributes", "operations"],
    "103 UML Attributes Explicit vs Implicit": ["uml attributes", "explicit attribute", "implicit attribute"],
    "104 Visibility and Encapsulation": ["visibility", "encapsulation", "public", "private", "protected", "uml visibility"],
    "105 Advanced Attribute and Method Properties": ["advanced attributes", "method properties", "derived attribute"],
    "106 Parameter Directions and Enumerations": ["parameter direction", "in", "out", "inout", "enumerations", "enum"],
    "107 UML Associations Navigability Roles and Multiplicity": ["uml associations", "navigability", "roles", "multiplicity"],
    "108 Association Class": ["association class", "link class"],
    "109 Inheritance Aggregation and Composition": ["inheritance", "aggregation", "composition", "whole-part"],

    # Chapter 2.1
    "201 Intro to Class Relationships and Dependencies": ["class relationships", "dependencies", "dependency"],
    "202 Associations Roles and Navigability": ["associations", "roles", "navigability"],
    "203 Multiplicity and Cardinality in Depth": ["multiplicity", "cardinality"],
    "204 Advanced Associations Reflexive and Nary": ["reflexive association", "n-ary association", "n-ary"],
    "205 Association Constraints XOR Subset Total": ["association constraints", "xor constraint", "subset constraint", "total constraint"],
    "206 Association Classes and Qualification": ["association class", "qualification"],
    "207 Masterclass on Qualified Associations": ["qualified association", "dictionary", "map"],

    # Chapter 2.2
    "301 Aggregation vs Composition": ["aggregation", "composition", "whole part"],
    "302 Inheritance and Generalization": ["inheritance", "generalization", "is-a"],
    "303 Advanced Inheritance Constraints": ["inheritance constraints", "disjoint", "overlapping", "complete", "incomplete"],
    "304 Abstract Classes Interfaces and Realization": ["abstract class", "interface", "realization"],
    "404 From Class Diagrams to Object Diagrams": ["class diagram", "object diagram", "dob"],

    # Chapter 2.3
    "305 Generic and Parametrized Classes": ["generic class", "parametrized class", "template"],
    "306 Recursive Composition Pattern Trap": ["recursive composition", "composite pattern"],
    "401 Constructors Destructors and Method Stereotypes": ["constructor", "destructor", "method stereotype", "stereotype"],
    "402 Advanced OCL Constraints": ["ocl constraints", "addonly", "frozen", "unique"],
    
    # Chapter 2.4 / Exams
    "403 Slide Annotations and Leftover Rules": ["slide annotations", "leftover rules"],
    "501 Theoretical Exam Questions": ["exam questions", "theory"],
    "502 TD Identification Exercise": ["td", "identification exercise"],
    "503 TD Deep Dive Arithmetic Expression Trap": ["td", "arithmetic expression"],
    "504 TD Deep Dive File System and Shortcuts": ["td", "file system", "shortcuts"],
    "505 TD Deep Dive Reading Complex Diagrams": ["td", "complex diagrams"],
}

def auto_link_files():
    print("Auto-linking keywords across all mapped files...")
    # Regex to split by code blocks, inline code, and existing links
    # so we don't accidentally link inside them.
    # We also add YAML frontmatter to the ignore pattern
    ignore_pattern = re.compile(r'(---.*?---|```.*?```|`.*?`|\[\[.*?\]\]|\[.*?\]\(.*?\))', re.DOTALL)
    
    linked_count = 0
    
    for root, dirs, files in os.walk("."):
        for filename in files:
            if not filename.endswith(".md") or filename == "000 Master Index.md":
                continue
                
            current_name = filename.replace(".md", "")
            # Only process if it's one of our mapped files to avoid touching Chapter 1.1 again needlessly
            if current_name not in KEYWORD_MAPPING:
                continue
                
            filepath = os.path.join(root, filename)
            
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
                        # Handle potential spaces carefully
                        # We sort keywords by length descending so longer keywords are matched first? (We can skip that since loop takes care of one match per file)
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
    auto_link_files()
