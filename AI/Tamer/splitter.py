import os

source_file = "TAMER.md"
base_dir = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(base_dir, source_file)

with open(source_path, 'r', encoding='utf-8') as f:
    content = f.read()

current_position = 0

def extract_section(folder, filename, start_flag, end_flag):
    global current_position
    
    start_idx = content.find(start_flag, current_position)
    if start_idx == -1:
        print(f"ERROR: start_flag not found for {folder}/{filename}:\n{repr(start_flag)}")
        return
    
    end_idx = content.find(end_flag, start_idx)
    if end_idx == -1:
        print(f"ERROR: end_flag not found for {folder}/{filename}:\n{repr(end_flag)}")
        return
    
    end_len = len(end_flag)
    section = content[start_idx:end_idx + end_len]
    
    out_dir = os.path.join(base_dir, folder)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(section)
    print(f"Created: {folder}/{filename}")
    
    current_position = end_idx + end_len

# Extract parts
extract_section("Outlines", "Outline_Part1.md", 
    start_flag="```text\nCourse {\n    Chapter 1", 
    end_flag="OCR Evaluation Metrics\n}\n```")

extract_section("Chapter 1 - Deep Learning", "Part_1.md", 
    start_flag="# Chapter 1: Deep Learning", 
    end_flag="making gradient flow significantly more stable.")

extract_section("Chapter 2 - Computer Vision", "Part_1.md", 
    start_flag="# Chapter 2: Computer Vision", 
    end_flag="have a stable, fixed reference point.")

extract_section("Chapter 3 - Sequence Modeling", "Part_1.md", 
    start_flag="# Chapter 3: Sequence Modeling", 
    end_flag="attention strictly to the ink strokes.")

extract_section("Chapter 4 - Text Processing", "Part_1.md", 
    start_flag="# Chapter 4: Text Processing", 
    end_flag="Out of vocabulary (rare, since you tokenize at the character level).")

extract_section("Chapter 5 - Advanced Training Strategies", "Part_1.md", 
    start_flag="# Chapter 5: Advanced Training", 
    end_flag="datasets (like CROHME) to fine-tune its performance.")

extract_section("Chapter 6 - Inference and Evaluation", "Part_1.md", 
    start_flag="# Chapter 6: Inference", 
    end_flag="SER: 1/5 = 20%]\n```")

extract_section("Meta", "AI_Transition_1.md", 
    start_flag="Here is the next iteration", 
    end_flag="State-of-the-Art (SOTA) context.")

extract_section("Outlines", "Outline_Part2.md", 
    start_flag="```text\nCourse {\n    Chapter 2", 
    end_flag="Benchmarks in Mathematical OCR\n}\n```")

extract_section("Chapter 2 - Computer Vision", "Part_2.md", 
    start_flag="# Chapter 2: Computer Vision", 
    end_flag="Out[GPU Tensor & real_w, real_h]\n```")

extract_section("Chapter 3 - Sequence Modeling", "Part_2.md", 
    start_flag="# Chapter 3: Sequence Modeling", 
    end_flag="vanishing gradient problem in deep decoders.")

extract_section("Chapter 5 - Advanced Training Strategies", "Part_2.md", 
    start_flag="# Chapter 5: Advanced Training", 
    end_flag="oscillating smoothly without internal conflict.")

extract_section("Chapter 6 - Inference and Evaluation", "Part_2.md", 
    start_flag="# Chapter 6: Inference", 
    end_flag="human could fix with a single keystroke.")

extract_section("Chapter 7 - Context and SOTA", "Part_1.md", 
    start_flag="# Chapter 7: Context and State-of-the-Art", 
    end_flag="fraction of the computational complexity required by massive multimodal models like Nougat.")

extract_section("Meta", "AI_Transition_2.md", 
    start_flag="Here is the next expansion", 
    end_flag="NFS bottlenecks, and OOM diagnostics).")

extract_section("Outlines", "Outline_Part3.md", 
    start_flag="```text\nCourse {\n    Chapter 2", 
    end_flag="Memory Exhaustion\n}\n```")

extract_section("Chapter 2 - Computer Vision", "Part_3.md", 
    start_flag="# Chapter 2: Computer Vision", 
    end_flag="Rot[90 Deg Rotation: + becomes x]\n```")

extract_section("Chapter 4 - Text Processing", "Part_2.md", 
    start_flag="# Chapter 4: Text Processing", 
    end_flag="Heavily nested, nightmare equations.")

extract_section("Chapter 5 - Advanced Training Strategies", "Part_3.md", 
    start_flag="# Chapter 5: Advanced Training", 
    end_flag="direction of the learning step remains exactly the same, but the magnitude is safely capped.")

extract_section("Chapter 8 - Data Engineering", "Part_1.md", 
    start_flag="# Chapter 8: Data Engineering", 
    end_flag="never empty.")

extract_section("Chapter 9 - System Reliability", "Part_1.md", 
    start_flag="# Chapter 9: System Reliability", 
    end_flag="just below the crash limit.")

print("Done.")
