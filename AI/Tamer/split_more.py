import os

base_dir = "/home/mersel/Documents/Learn/Obsidian Notes/Shared/AI/Tamer/"
source_path = os.path.join(base_dir, "More.md")

with open(source_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def write_lines(folder, filename, start_line, end_line):
    """Extract lines [start_line, end_line] (1-indexed, inclusive)."""
    section = ''.join(lines[start_line - 1:end_line]).rstrip() + '\n'
    out_dir = os.path.join(base_dir, folder)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(section)
    print(f"  Created: {folder}/{filename}  (lines {start_line}-{end_line})")

print("=== ITERATION 1 (lines 1-134) ===")

# Intro text
write_lines("Meta", "AI_Transition_3.md", 1, 1)

# Outline
write_lines("Outlines", "Outline_Part4.md", 5, 19)

# Chapter 2, Sections 9 & 10 (Encoder Architecture + GPS Mechanics)
write_lines("Chapter 2 - Computer Vision", "Part_4.md", 23, 58)

# Chapter 3, Sections 5 & 6 (Decoder Architecture + Dimensional Rationale)
write_lines("Chapter 3 - Sequence Modeling", "Part_3.md", 62, 88)

# Chapter 7, Sections 2 & 3 (TAMER v2.4 deviations + Parameter Breakdown)
write_lines("Chapter 7 - Context and SOTA", "Part_2.md", 91, 133)

print("\n=== ITERATION 2 (lines 137-237, first occurrence — duplicate at 238-347 skipped) ===")

# Intro text
write_lines("Meta", "AI_Transition_4.md", 137, 137)

# Outline
write_lines("Outlines", "Outline_Part5.md", 141, 149)

# Chapter 2, Section 11 (SwinV2 Advantage)
write_lines("Chapter 2 - Computer Vision", "Part_5.md", 154, 174)

# Chapter 3, Section 7 (Layer-by-Layer Anatomy of Decoder Block)
write_lines("Chapter 3 - Sequence Modeling", "Part_4.md", 178, 225)

# Chapter 3, Section 8 (Tensor Journey) 
# Lines 227-237 from first copy + lines 340-343 for "Why dimensions" block (only in duplicate, but belongs here)
section_8_first = ''.join(lines[227-1:237])
section_8_dims  = '\n' + ''.join(lines[340-1:343])
combined = (section_8_first + section_8_dims).rstrip() + '\n'
out_path = os.path.join(base_dir, "Chapter 3 - Sequence Modeling", "Part_5.md")
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(combined)
print(f"  Created: Chapter 3 - Sequence Modeling/Part_5.md  (lines 227-237 + 340-343)")

print("\nDone! All sections from More.md extracted. Duplicates excluded.")
