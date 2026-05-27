"""
Atomic Sequential File Renaming Engine.
Applies safe, transaction-controlled structural file renames 
to prevent filename collisions.
"""

from typing import Dict
from vault_manager.core.interfaces import FileProcessor
from vault_manager.utils.file_ops import atomic_two_phase_rename
from vault_manager.logging import logger


class VaultFileRenamer(FileProcessor):
    """
    Handles sequential renaming mappings using transactional, two-phase steps.
    """

    # --- Pre-defined OOP Renaming Mapping ---
    OOP_JAVA_MAPPING: Dict[str, str] = {
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

    # --- Pre-defined Theory of Computation Renaming Mapping ---
    AUTOMATA_MAPPING: Dict[str, str] = {
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
        "8. Advanced Turing Machine Variants.md": "13 Advanced Turing Machine Variants.md"
    }

    def execute(self, mapping_type: str, target_dir: str = ".") -> None:
        """
        Executes file renaming based on the specified mapping.
        
        Args:
            mapping_type: Either 'oop' or 'automata'.
            target_dir: Directory where the target files are located.
        """
        if mapping_type.lower() == "oop":
            mapping = self.OOP_JAVA_MAPPING
            label = "Java OOP Basics"
        elif mapping_type.lower() == "automata":
            mapping = self.AUTOMATA_MAPPING
            label = "Theory of Automata / Computation"
        else:
            raise ValueError(f"Unknown renaming mapping type: '{mapping_type}'")

        logger.info(f"Initializing sequential renames for {label} in '{target_dir}'...")
        atomic_two_phase_rename(target_dir=target_dir, name_mapping=mapping)
        logger.success(f"Renaming completed for {label}.")