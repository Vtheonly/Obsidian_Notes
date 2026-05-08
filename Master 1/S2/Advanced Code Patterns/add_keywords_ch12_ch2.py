import os

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

def inject_keywords():
    print("Injecting keywords into all mapped files...")
    count = 0
    
    for root, dirs, files in os.walk("."):
        for filename in files:
            if not filename.endswith(".md"):
                continue
                
            current_name = filename.replace(".md", "")
            keywords = KEYWORD_MAPPING.get(current_name, [])
            
            if not keywords:
                continue
                
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Prevent double injection
            if content.startswith("---"):
                print(f"Skipped {filename} (already has frontmatter)")
                continue
                
            # Convert keywords to valid Obsidian tags (no spaces)
            tags = [k.replace(" ", "-").replace("(", "").replace(")", "").lower() for k in keywords]
            
            # Format lists for YAML
            tags_str = ", ".join(tags)
            aliases_str = ", ".join(keywords)
            
            yaml_frontmatter = f"---\ntags: [{tags_str}]\naliases: [{aliases_str}]\nkeywords: [{aliases_str}]\n---\n"
            
            # Append a "Keywords" footer section
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
