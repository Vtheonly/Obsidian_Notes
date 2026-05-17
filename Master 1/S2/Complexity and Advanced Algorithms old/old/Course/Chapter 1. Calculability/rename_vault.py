import os

FILE_MAPPING = {
    "1. Introduction and Notion of Algorithm.md": "00 Introduction and Notion of Algorithm.md",
    "1. Finite Automata and Regular Languages.md": "01 Finite Automata and Regular Languages.md",
    "2. Countability and Pushdown Automata.md": "02 Countability and Pushdown Automata.md",
    "2. The Turing Machine - Model and Architecture.md": "03 Turing Machine Model and Architecture.md",
    "3. Formal Definition and Execution of a TM.md": "04 Formal Definition and Execution of a TM.md",
    "3. Turing Machines Basics and Formal Definitions.md": "05 Turing Machines Basics and Formal Definitions.md",
    "4. Configurations and Terminology.md": "06 Configurations and Terminology.md",
    "4. Tracing Configurations and Execution.md": "07 Tracing Configurations and Execution.md",
    "5. Decidability and The Halting Problem.md": "08 Decidability and The Halting Problem.md",
    "5. Turing Machines as Transducers.md": "09 Turing Machines as Transducers.md",
    "6. Turing Machines as Language Recognizers.md": "10 Turing Machines as Language Recognizers.md",
    "6. Undecidable Problems (PCP and MMP).md": "11 Undecidable Problems (PCP and MMP).md",
    "7. Non-Deterministic Turing Machines.md": "12 Non-Deterministic Turing Machines.md",
    "8. Advanced Turing Machine Variants.md": "13 Advanced Turing Machine Variants.md",
}

def rename_files():
    # Check for collisions/missing keys
    files = [f for f in os.listdir('.') if f.endswith('.md')]
    missing = [f for f in files if f not in FILE_MAPPING and f != "README.md"]
    if missing:
        print(f"Warning: The following files are not in the mapping and will be skipped: {missing}")

    for current_name, target_name in FILE_MAPPING.items():
        if os.path.exists(current_name):
            print(f"Renaming: '{current_name}' -> '{target_name}'")
            os.rename(current_name, target_name)
        else:
            print(f"File not found, skipping: '{current_name}'")

if __name__ == "__main__":
    rename_files()
    print("Renaming complete.")
