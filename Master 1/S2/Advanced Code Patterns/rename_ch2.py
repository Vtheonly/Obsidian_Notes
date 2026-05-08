import os

RENAME_MAP = {
    # 200s: Relationships & Associations
    "1. Introduction to Class Relationships and Dependencies.md": "201 Intro to Class Relationships and Dependencies.md",
    "2. Associations, Roles, and Navigability.md": "202 Associations Roles and Navigability.md",
    "3. Multiplicity and Cardinality in Depth.md": "203 Multiplicity and Cardinality in Depth.md",
    "4. Advanced Associations (Reflexive and N-ary).md": "204 Advanced Associations Reflexive and Nary.md",
    "5. Association Constraints (XOR, Subset, Total).md": "205 Association Constraints XOR Subset Total.md",
    "6. Association Classes and Qualification.md": "206 Association Classes and Qualification.md",
    "3. Masterclass on Qualified Associations (Dictionaries Maps).md": "207 Masterclass on Qualified Associations.md",

    # 300s: Inheritance & Whole-Part
    "1. Aggregation vs Composition (The Whole-Part Relationships).md": "301 Aggregation vs Composition.md",
    "2. Inheritance and Generalization (Is-A Relationship).md": "302 Inheritance and Generalization.md",
    "3. Advanced Inheritance Constraints.md": "303 Advanced Inheritance Constraints.md",
    "4. Abstract Classes, Interfaces, and Realization.md": "304 Abstract Classes Interfaces and Realization.md",
    "1. Generic and Parametrized Classes (Templates).md": "305 Generic and Parametrized Classes.md",
    "5. Recursive Composition (The Composite Pattern Trap).md": "306 Recursive Composition Pattern Trap.md",

    # 400s: Advanced Rules & Object Diagrams
    "2. Constructors, Destructors, and Method Stereotypes.md": "401 Constructors Destructors and Method Stereotypes.md",
    "4. Advanced OCL Constraints (addOnly, frozen, unique).md": "402 Advanced OCL Constraints.md",
    "6. Slide Annotations & Leftover Rules.md": "403 Slide Annotations and Leftover Rules.md",
    "5. From Class Diagrams to Object Diagrams (DOB).md": "404 From Class Diagrams to Object Diagrams.md",

    # 500s: Exams & TDs
    "1. Theoretical Exam Questions (The Free Points Bank).md": "501 Theoretical Exam Questions.md",
    "2. The TD Identification Exercise (Rattrapage 2014-2015).md": "502 TD Identification Exercise.md",
    "3. TD Deep Dive - The Arithmetic Expression Trap.md": "503 TD Deep Dive Arithmetic Expression Trap.md",
    "4. TD Deep Dive - The File System and Shortcuts (TD 4 Ex 5).md": "504 TD Deep Dive File System and Shortcuts.md",
    "5. TD Deep Dive - Reading Complex Diagrams (TD 3 Ex 1).md": "505 TD Deep Dive Reading Complex Diagrams.md"
}

def rename_files():
    new_names = list(RENAME_MAP.values())
    if len(new_names) != len(set(new_names)):
        print("Error: Duplicate filenames detected in the mapping.")
        return

    count = 0
    for root, dirs, files in os.walk("."):
        if "Chapter 1" in root:
            continue
            
        for filename in files:
            if filename in RENAME_MAP:
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, RENAME_MAP[filename])
                
                if os.path.exists(new_path):
                    print(f"Skipping '{filename}': Target '{RENAME_MAP[filename]}' already exists.")
                    continue
                
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: '{filename}' -> '{RENAME_MAP[filename]}'")
                    count += 1
                except Exception as e:
                    print(f"Failed to rename '{filename}': {e}")
    
    print(f"\nSuccessfully renamed {count} files.")

if __name__ == "__main__":
    rename_files()
