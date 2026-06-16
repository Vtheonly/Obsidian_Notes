import os

"""
OBSIDIAN KEYWORD AND TAG INJECTOR
---------------------------------
This script adds Obsidian YAML frontmatter (Properties) to the top of every file.
It includes 'tags' (for searching) and 'aliases' (for linking).
It also adds a 'Related Links' block at the bottom.
"""

TARGET_DIR = "."

# Mapping of Target Files to their Keywords
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
    "031 Inheritance Hierarchy": ["hierarchy", "parent", "child"],
    "032 Upcasting and Downcasting": ["upcasting", "downcasting", "type casting"],
    "033 Super Keyword": ["super keyword"],
    "034 Multiple Inheritance and The Diamond Problem": ["multiple inheritance", "diamond problem"],
    "040 Abstraction": ["abstraction"],
    "041 Abstraction Details": ["abstract class", "abstract method"],
    "042 Polymorphism Summary": ["polymorphism", "dynamic polymorphism", "static polymorphism"],
    "043 Polymorphism Types": ["overloading", "overriding", "binding"],
    "044 Interfaces": ["interface", "interfaces", "implements"],
    "050 Collections Overview": ["collections", "data structures"],
    "051 Arrays": ["array", "arrays"],
    "052 Collection Framework": ["collection framework", "java collections"],
    "053 Collection Interface": ["collection interface", "iterable"],
    "054 List Interface": ["list interface", "arraylist", "linkedlist"],
    "055 Set Interface": ["set interface", "hashset", "treeset"],
    "056 Queues and Deques": ["queue", "deque", "fifo", "lifo"],
    "057 Map Interface": ["map interface", "hashmap", "treemap"],
    "058 Legacy Collections": ["vector", "hashtable", "stack"],
    "060 Object Lifecycle": ["lifecycle", "garbage collection"],
    "061 Copying Objects": ["copying objects", "deep copy", "shallow copy"],
    "062 Generics": ["generics", "type erasure"],
    "063 Exceptions and Varargs": ["exception", "exceptions", "varargs"],
    "070 Coding to Interfaces": ["best practices", "design principles"],
    "091 Project Inventory": ["inventory system", "project"],
    "092 Project ATM": ["atm machine", "project"],
    "093 Project Calculator": ["calculator", "project"]
}

def inject_keywords():
    print("Injecting keywords into all files...")
    count = 0
    
    for filename in os.listdir(TARGET_DIR):
        if not filename.endswith(".md") or filename == "000 Master Index.md":
            continue
            
        current_name = filename.replace(".md", "")
        keywords = KEYWORD_MAPPING.get(current_name, [])
        
        if not keywords:
            continue
            
        filepath = os.path.join(TARGET_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Prevent double injection
        if content.startswith("---"):
            print(f"Skipped {filename} (already has frontmatter)")
            continue
            
        # 1. Create YAML Frontmatter (Properties)
        # Convert keywords to valid Obsidian tags (no spaces)
        tags = [k.replace(" ", "-").replace("(", "").replace(")", "").lower() for k in keywords]
        
        # Format lists for YAML
        tags_str = ", ".join(tags)
        aliases_str = ", ".join(keywords)
        
        yaml_frontmatter = f"---\ntags: [{tags_str}]\naliases: [{aliases_str}]\nkeywords: [{aliases_str}]\n---\n"
        
        # 2. Append a "Keywords" footer section
        footer = f"\n\n---\n**Keywords:** {', '.join(['#' + t for t in tags])}\n"
        
        # Write back to file
        new_content = yaml_frontmatter + content + footer
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        count += 1
        print(f"Injected keywords to: {filename}")
        
    print(f"\nSuccessfully injected keywords into {count} files.")

if __name__ == "__main__":
    inject_keywords()
