import os

RENAME_MAP = {
    "1. Static vs Dynamic Views.md": "101 Static vs Dynamic Views.md",
    "2. Anatomy of a Class.md": "102 Anatomy of a Class.md",
    "1. The Fundamentals of UML Attributes Explicit vs Implicit.md": "103 UML Attributes Explicit vs Implicit.md",
    "3. Visibility and Encapsulation.md": "104 Visibility and Encapsulation.md",
    "4. Advanced Attribute and Method Properties.md": "105 Advanced Attribute and Method Properties.md",
    "5. Parameter Directions and Enumerations.md": "106 Parameter Directions and Enumerations.md",
    "2. UML Associations Navigability Roles and Multiplicity.md": "107 UML Associations Navigability Roles and Multiplicity.md",
    "3. Association Class.md": "108 Association Class.md",
    "4. Inheritance and Aggregation and Composition.md": "109 Inheritance Aggregation and Composition.md",
}

def rename_files():
    new_names = list(RENAME_MAP.values())
    if len(new_names) != len(set(new_names)):
        print("Error: Duplicate filenames detected in the mapping.")
        return

    count = 0
    target_dir = "./Chapter 1.2: Class Diagram Fundamentals"
    
    if not os.path.exists(target_dir):
        print(f"Error: Directory {target_dir} not found.")
        return

    for filename in os.listdir(target_dir):
        if filename in RENAME_MAP:
            old_path = os.path.join(target_dir, filename)
            new_path = os.path.join(target_dir, RENAME_MAP[filename])
            
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
