import os
import re

base_dir = "/home/mersel/Documents/Learn/Obsidian Notes/Shared/Master 1/S2/Complexity and Advanced Algorithms/Series/serise 2"
s2_path = os.path.join(base_dir, "s2.md")

with open(s2_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r"### `(.*?)`\s*```markdown\n(.*?)```", re.DOTALL)
matches = pattern.findall(content)

if not matches:
    print("No files found to split!")

for rel_path, file_content in matches:
    safe_rel_path = rel_path.replace(":", " -")
    
    full_path = os.path.join(base_dir, safe_rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(file_content.strip() + "\n")
    print(f"Created: {safe_rel_path}")

print("Splitting completed successfully.")
