What you want is much more specific than generic “primitive 3D reconstruction.” You are describing:

> **semantic + structural decomposition of architectural scenes into functional building components**

So instead of cubes/superquadrics, your primitives are:

- walls
    
- floors
    
- roofs
    
- windows
    
- ceilings
    

That places your idea in a fairly well-defined research intersection between **3D scene understanding, building parsing, and structured reconstruction**.

Here are the closest real research directions that actually match this.

---

# 1. Building parsing (most direct match to your goal)

This is the closest to what you described.

## 🏗️ Architectural scene parsing

These methods treat buildings like structured systems instead of raw geometry.

### Key idea:

> image → semantic parts → 3D structure

Typical labels:

- wall
    
- floor
    
- roof
    
- window
    
- door
    
- ceiling
    

This is exactly your target decomposition.

---

## Examples of research

### 1. “LayoutNet” / indoor layout estimation (very relevant)

- Predicts:
    
    - walls
        
    - floor
        
    - ceiling
        
- Usually for indoor scenes
    

👉 Important because:  
It explicitly separates structural components instead of meshes.

---

### 2. “ScanNet-based semantic reconstruction”

- Uses real-world scans
    
- Outputs:
    
    - semantic segmentation of surfaces
        
    - room structure
        

---

### 3. “Structured3D dataset + methods”

- Synthetic dataset of buildings and rooms
    
- Labels:
    
    - wall, floor, ceiling, window, door
        
- Used for:
    
    - structured reconstruction learning
        

👉 This is VERY aligned with your idea.

---

# 2. 3D semantic scene reconstruction (building-level understanding)

Instead of primitives, these models build:

> semantic 3D maps

---

## Example direction:

### Semantic NeRF / Semantic 3D Gaussian Splatting

- Adds semantic labels to geometry
    
- Each region has meaning:
    
    - wall region
        
    - window region
        
    - roof region
        

👉 Difference from classic NeRF:  
Not just shape — but structure meaning

---

# 3. Floorplan + building structure reconstruction (very important)

This is one of the strongest matches.

## 🏢 Floorplan reconstruction papers

They do exactly:

> image → structured architectural graph

Typical output:

- walls (as line segments or planes)
    
- rooms
    
- windows
    
- doors
    
- floors/ceilings
    

---

### Key research lines:

#### 1. FloorNet / DeepFloorplan-style models

- Predict:
    
    - wall layout
        
    - room structure
        
- Output is graph-like, not mesh
    

#### 2. Building reconstruction from single image / panorama

- Infer:
    
    - full building layout
        
    - structural boundaries
        

👉 This is very close to:  
your “Model B structured decomposition”

---

# 4. 3D building reconstruction from primitives (CAD-style buildings)

This is where your idea becomes very explicit.

## CAD + procedural building models

Instead of raw mesh:

- walls → planes
    
- windows → cutouts
    
- roofs → parametric surfaces
    

---

### Example directions:

#### 1. Procedural modeling of buildings

- Uses rules like:
    
    - repeat windows along wall
        
    - roof follows geometry constraints
        

#### 2. Neural CAD reconstruction

- Models buildings as:
    
    - parameter sets (width, height, openings)
        
    - structured components
        

---

# 5. Scene graph representation (important conceptual layer)

Instead of geometry-first:

> building = graph of components

Example:

- Building
    
    - Floor 1
        
        - Wall A
            
            - Window 1
                
            - Window 2
                
        - Wall B
            
    - Roof
        

---

This is called:

> **3D scene graphs**

Very relevant research:

- Neural Scene Graphs
    
- Semantic Scene Graph generation
    

---

# 6. Where your idea actually sits (clean mapping)

Your Model B = combination of:

### 1. Semantic segmentation

- wall / floor / roof / window
    

### 2. Structural graph learning

- relationships between parts
    

### 3. Parametric geometry

- planes instead of meshes
    

### 4. Optional refinement model (Model A style)

- converts structure → detailed mesh
    

---

# 7. The real research category name for your idea

If you want to search properly, use:

> **“semantic 3D building reconstruction”**  
> **“structural scene parsing for buildings”**  
> **“floorplan reconstruction from images”**  
> **“layout-aware 3D reconstruction”**  
> **“scene graph based 3D reconstruction”**

---

# 8. My opinion (important)

Your Model B idea is actually stronger than raw mesh generation for buildings.

Because buildings are:

- inherently structured
    
- modular
    
- rule-based
    

So forcing:

> walls + floors + roofs + windows

is closer to how architecture actually works than any neural mesh model.

In practice:

- Model A = visual realism
    
- Model B = architectural intelligence
    

And the best systems in robotics, simulation, and CAD will always need Model B-style representations.

---

If you want next step, I can design a **real architecture for Model B (encoder → wall detector → planar decomposition → window/roof segmentation → graph builder → mesh generator)** that could realistically be trained on datasets like Structured3D or ScanNet.


Here are **real, relevant research papers and paper directions** that match exactly your goal:

> image → structured building decomposition (walls, floors, roofs, windows, ceilings) → 3D reconstruction / BIM-like model

I grouped them so you can actually build a mental map.

---

# 1. Floorplan + building structure reconstruction (MOST IMPORTANT)

These are the closest to your Model B idea.

## 🏢 FloorNet: A Unified Framework for Floorplan Reconstruction from 3D Scans

FloorNet

- Inputs: RGB-D scans
    
- Outputs:
    
    - walls
        
    - room layout
        
    - floorplan structure
        
- Key idea: multi-branch network (2D + 3D + image fusion)
    

This is basically:

> first real deep learning system that explicitly reconstructs building structure instead of meshes

---

## 🧭 Scan2Plan: Efficient Floorplan Generation from 3D Scans

Scan2Plan  
([Emergent Mind](https://www.emergentmind.com/papers/2003.07356?utm_source=chatgpt.com "Scan2Plan: Efficient Floorplan Generation from 3D Scans of Indoor Scenes"))

- Clusters:
    
    - wall instances
        
    - room instances
        
- Then reconstructs:
    
    - polygon floorplans
        

Key idea:

> scene → walls + rooms → geometric layout graph

This is extremely close to your “Model B”.

---

## 🧱 FloorPP-Net: Scan-to-Floorplan reconstruction

FloorPP-Net

- Uses point clouds
    
- Predicts:
    
    - corners
        
    - edges
        
- Outputs structured floorplan (BIM-style)
    

Key idea:

> detect structural building components instead of raw geometry

---

## 🧠 RoomFormer (Transformer-based floorplan model)

RoomFormer

- Uses transformer queries
    
- Outputs:
    
    - room polygons
        
    - architectural elements (doors, windows)
        

Key idea:

> treat building reconstruction as set prediction problem

---

# 2. Semantic building reconstruction (walls / windows / roofs explicitly)

These go beyond floorplans into full building semantics.

---

## 🏙️ Scan2LoD3: Semantic 3D building reconstruction

Scan2LoD3

- Reconstructs:
    
    - facades
        
    - windows
        
    - openings
        
- Uses:
    
    - probabilistic reasoning + geometry priors
        

Key idea:

> full semantic building model (not just indoor layout)

---

## 🧱 Semantic extraction of permanent structures from point clouds

([MDPI](https://www.mdpi.com/1424-8220/20/23/6916?utm_source=chatgpt.com "Semantic Extraction of Permanent Structures for the Reconstruction of Building Interiors from Point Clouds"))

- Separates:
    
    - walls
        
    - structural elements
        
    - non-structural objects (furniture)
        

Key idea:

> isolate building “skeleton” from noisy scene data

---

# 3. Indoor layout estimation (walls + floor + ceiling)

These are very relevant for your “Model B constraints”.

---

## 📐 Recovering indoor 3D layout from a single image

([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0167865515002731?utm_source=chatgpt.com "Recovering an indoor 3D layout with top-down semantic segmentation from a single image - ScienceDirect"))

- Predicts:
    
    - walls
        
    - floor
        
    - ceiling (cuboid layout assumption)
        

Key idea:

> structured scene priors instead of free-form geometry

---

## 🧭 LayoutNet (indoor layout estimation)

- Predicts room structure:
    
    - walls
        
    - floor
        
    - ceiling
        
- Uses geometric constraints
    

Key idea:

> enforce Manhattan-world structure (orthogonal building assumption)

---

# 4. Structured 3D datasets (you NEED these for your idea)

These are not papers about models, but they are critical.

---

## 📦 Structured3D dataset

- Synthetic indoor buildings
    
- Fully labeled:
    
    - walls
        
    - floors
        
    - ceilings
        
    - windows
        
    - doors
        

Used by:

- RoomFormer
    
- Scan2Plan
    
- FloorNet
    

---

## 🏠 ScanNet dataset

([Princeton University](https://collaborate.princeton.edu/en/publications/scannet-richly-annotated-3d-reconstructions-of-indoor-scenes?utm_source=chatgpt.com "ScanNet: Richly-annotated 3D reconstructions of indoor scenes - Princeton University"))

- Real-world RGB-D scans
    
- Semantic labels for:
    
    - walls
        
    - floors
        
    - objects
        

Key idea:

> real-world foundation for indoor semantic reconstruction

---

# 5. Floorplan reconstruction from point clouds (BIM-style)

---

## 🧩 Scan2Floor / Scan-to-BIM papers

([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9967194/?utm_source=chatgpt.com "Reconstructing Floorplans from Point Clouds Using GAN - PMC"))

- Convert point clouds → structured building models
    
- Use:
    
    - geometry + semantic constraints
        
    - graph-based reconstruction
        

Key idea:

> structured CAD-like building reconstruction pipeline

---

# 6. The exact research direction you are describing

If we summarize your idea:

> Model B = semantic + geometric decomposition of buildings into structural primitives

The closest academic term is:

## 🧠 “Semantic 3D Scene Reconstruction”

or more specifically:

## 🏗️ “Scan-to-BIM / Floorplan Reconstruction / Structural Scene Parsing”

---

# 7. My honest evaluation of your idea

What you are thinking is not just valid — it matches a **major research transition**:

### Old paradigm:

- image → mesh / NeRF
    

### New paradigm (your idea):

- image → structured building representation
    
    - walls
        
    - floors
        
    - roofs
        
    - windows
        
    - graph structure
        

This is what modern systems are moving toward because:

- easier to edit
    
- more interpretable
    
- closer to CAD/BIM systems
    
- better for robotics and architecture tools
    

---

# If you want next step

I can map all these papers into a **single unified architecture design** for your Model B:

- encoder (image → features)
    
- wall/floor/roof segmentation head
    
- structural graph builder
    
- primitive-based 3D decoder
    
- optional mesh refinement model (Model A layer)
    

That would basically be a research-grade system blueprint.

