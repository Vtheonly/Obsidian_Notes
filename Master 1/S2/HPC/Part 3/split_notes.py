import os

file_path = "/home/mersel/Documents/Learn/Obsidian Notes/Shared/Master 1/S2/HPC/Part 3/Untitled.md"
output_dir = "/home/mersel/Documents/Learn/Obsidian Notes/Shared/Master 1/S2/HPC/Part 3"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('\n# Chapter ')

count = 0
for part in parts[1:]: # Skip the first part (vault structure)
    lines = part.split('\n', 1)
    chapter_title = lines[0].strip()
    
    chapter_content = ""
    if len(lines) > 1:
        chapter_content = lines[1].strip()
    
    # Strip trailing *** or --- if present at the very end
    while chapter_content.endswith('*') or chapter_content.endswith('-'):
        chapter_content = chapter_content[:-1].strip()
    
    filename = f"Chapter {chapter_title}.md"
    file_content = f"# Chapter {chapter_title}\n\n{chapter_content}\n"
    
    out_path = os.path.join(output_dir, filename)
    with open(out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(file_content)
    print(f"Created: {filename}")
    count += 1

print(f"Total files created: {count}")
