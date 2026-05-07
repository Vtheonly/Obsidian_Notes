import os
import sys

"""
FILE RENAMING AND SORTING SCRIPT (Safe, Atomic, No Underscores Version)
----------------------------------------------------------------------
This script renames the files in the current directory based on a predefined 
hierarchical mapping, using spaces instead of underscores.
It uses a two-phase renaming strategy to avoid filename collisions and overwrites.
"""

# The exact path to operate on
TARGET_DIR = "."

# Mapping of current filenames (key) to new sorted filenames (value)
RENAME_MAP = {
    "0 - OOP basics.md": "001 OOP Basics.md",
    "1 - Object.md": "002 Object.md",
    "4 - New keyword.md": "003 New Keyword.md",
    "14 - Compile time vs Run time.md": "004 Compile Time vs Run Time.md",
    "1. Introduction to Objects and Classes.md": "005 Intro to Classes.md",
    "2 - Constructors and Destructors.md": "010 Constructors and Destructors.md",
    "2. Constructors and Initialization.md": "011 Constructors and Initialization.md",
    "3. Static Members.md": "012 Static Members.md",
    "5 - Static keyword.md": "013 Static Keyword.md",
    "6. Enums (Enumerations).md": "014 Enums.md",
    "3 - final keyword.md": "015 Final Keyword.md",
    "3. Advanced Keywords & Modifiers.md": "016 Advanced Keywords and Modifiers.md",
    "1. Encapsulation and Access Control.md": "020 Encapsulation and Access Control.md",
    "8 - Encapsulation.md": "021 Encapsulation.md",
    "7 - inheritance.md": "030 Inheritance.md",
    "2. Inheritance Hierarchy.md": "031 Inheritance Hierarchy.md",
    "6 - Upcasting and Downcasting.md": "032 Upcasting and Downcasting.md",
    "12 - super.md": "033 Super Keyword.md",
    "5. Multiple Inheritance & The Diamond Problem.md": "034 Multiple Inheritance and The Diamond Problem.md",
    "9 - Abstraction.md": "040 Abstraction.md",
    "4. Abstraction (Abstract Classes vs Interfaces).md": "041 Abstraction Details.md",
    "10 - Polymorphism.md": "042 Polymorphism Summary.md",
    "3. Polymorphism.md": "043 Polymorphism Types.md",
    "11 - Interfaces.md": "044 Interfaces.md",
    "1. The Big Picture and Hierarchy.md": "050 Collections Overview.md",
    "2. Arrays - The Native Container.md": "051 Arrays.md",
    "2. Java Collection Framework.md": "052 Collection Framework.md",
    "3. The Collection Interface.md": "053 Collection Interface.md",
    "4. The List Interface and Implementations.md": "054 List Interface.md",
    "5. The Set Interface.md": "055 Set Interface.md",
    "6. Queues and Deques.md": "056 Queues and Deques.md",
    "7. The Map Interface.md": "057 Map Interface.md",
    "8. Legacy Collections.md": "058 Legacy Collections.md",
    "1. The Object Lifecycle & The Cosmic Superclass.md": "060 Object Lifecycle.md",
    "13 - Copying Objects.md": "061 Copying Objects.md",
    "15 - Generics.md": "062 Generics.md",
    "4. Robustness: Exceptions & Varargs.md": "063 Exceptions and Varargs.md",
    "9. Best Practices - Coding to Interfaces.md": "070 Coding to Interfaces.md",
    "1. Project Walkthrough - Inventory System.md": "091 Project Inventory.md",
    "2. Project Walkthrough - ATM Machine.md": "092 Project ATM.md",
    "3. Project Walkthrough - Calculator (Interfaces).md": "093 Project Calculator.md"
}

def rename_files():
    print("Scanning and analyzing files...")
    
    # 1. Verify all expected old files exist
    missing_files = []
    for old_name in RENAME_MAP.keys():
        if not os.path.exists(os.path.join(TARGET_DIR, old_name)):
            missing_files.append(old_name)
    
    if missing_files:
        print("Error: The following files are missing and cannot be renamed:")
        for f in missing_files:
            print(f"  - {f}")
        print("Aborting to prevent partial renaming.")
        return

    # 2. Verify uniqueness of new names to prevent collisions
    new_names = list(RENAME_MAP.values())
    if len(new_names) != len(set(new_names)):
        print("Error: Duplicate filenames detected in the new mapping names.")
        return
        
    # 3. Check if any new names already exist (that are not part of the old names)
    existing_new_names = []
    for new_name in new_names:
        if os.path.exists(os.path.join(TARGET_DIR, new_name)) and new_name not in RENAME_MAP:
            existing_new_names.append(new_name)
            
    if existing_new_names:
        print("Error: The following target filenames already exist in the directory:")
        for f in existing_new_names:
            print(f"  - {f}")
        print("Aborting to prevent overwriting existing files.")
        return

    print("Pre-checks passed. Starting safe two-phase rename process...\n")

    # Phase 1: Rename all to temporary names to prevent intermediate collisions
    # (e.g. if A -> B, and B -> C, we don't want A to overwrite B)
    temp_suffix = ".temp_rename_12345"
    phase1_success = []
    
    try:
        for old_name in RENAME_MAP.keys():
            old_path = os.path.join(TARGET_DIR, old_name)
            temp_path = os.path.join(TARGET_DIR, old_name + temp_suffix)
            os.rename(old_path, temp_path)
            phase1_success.append((old_name, temp_path))
    except Exception as e:
        print(f"Error during Phase 1 (Temporary Rename): {e}")
        print("Rolling back changes...")
        # Rollback
        for old_name, temp_path in phase1_success:
            old_path = os.path.join(TARGET_DIR, old_name)
            os.rename(temp_path, old_path)
        print("Rollback complete. No files were changed.")
        return
        
    # Phase 2: Rename from temporary names to final names
    phase2_success = []
    try:
        for old_name, temp_path in phase1_success:
            new_name = RENAME_MAP[old_name]
            new_path = os.path.join(TARGET_DIR, new_name)
            os.rename(temp_path, new_path)
            phase2_success.append((old_name, new_name))
            print(f"Renamed: '{old_name}' -> '{new_name}'")
    except Exception as e:
        print(f"Error during Phase 2 (Final Rename): {e}")
        print("Warning: The system is in a partially renamed state.")
        # Attempting rollback of Phase 2
        for old_name, new_name in phase2_success:
            new_path = os.path.join(TARGET_DIR, new_name)
            temp_path = os.path.join(TARGET_DIR, old_name + temp_suffix)
            os.rename(new_path, temp_path)
        # Rollback Phase 1
        for old_name, temp_path in phase1_success:
            old_path = os.path.join(TARGET_DIR, old_name)
            os.rename(temp_path, old_path)
        print("Rollback complete. Restored original filenames.")
        return

    print(f"\nSuccessfully renamed {len(phase2_success)} files.")

if __name__ == "__main__":
    confirm = input("This script will safely rename and sort files in the current directory. Proceed? (y/n): ")
    if confirm.lower() == 'y':
        rename_files()
    else:
        print("Operation aborted.")
