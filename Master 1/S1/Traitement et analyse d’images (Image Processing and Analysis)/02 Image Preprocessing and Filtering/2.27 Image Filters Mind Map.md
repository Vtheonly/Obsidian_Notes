# Part 1: Linear Spatial Filters
*These filters use Math (Weighted Sums) to change pixels.*

## 1. The Mean Filter (Average)

### The Concept
**"The Smear."** It treats every pixel in the neighborhood equally. It adds them all up and divides by the count. It is like smearing wet ink with your thumb.

### Mini Mind Map
```mermaid
mindmap
  root((Mean Filter))
    Best For
      Reducing Random Gaussian Noise
      Simple Smoothing
    Sucks At
      Preserving Edges makes them blurry
      Removing Salt and Pepper Noise just smears it
    Side Effects
      Make the whole image look out of focus
```

### Logic Diagram
```mermaid
graph TD
    A[Start at Center Pixel] --> B[Identify Neighbor Pixels]
    B --> C[Sum all Neighbor Values]
    C --> D[Divide Sum by Total Count]
    D --> E[Replace Center Pixel with Average]
```

---

## 2. The Gaussian Filter

### The Concept
**"The Natural Blur."** It calculates an average, but it gives more importance to the pixels in the center and less importance to the pixels far away. It follows a "Bell Curve."

### Mini Mind Map
```mermaid
mindmap
  root((Gaussian Filter))
    Best For
      Natural Smoothing
      Pre processing before other steps
    Sucks At
      Removing heavy Salt and Pepper noise
      Keeping very fine texture details
    Side Effects
      Softens the image but looks more natural than Mean filter
```

### Logic Diagram
```mermaid
graph TD
    A[Start at Center Pixel] --> B[Apply Weight Mask Bell Curve]
    B --> C[Multiply Close Neighbors by High Weight]
    B --> D[Multiply Far Neighbors by Low Weight]
    C --> E[Sum all Weighted Values]
    D --> E
    E --> F[Replace Center Pixel with Weighted Sum]
```

---

## 3. The Laplacian Filter

### The Concept
**"The Edge Detector."** It calculates the difference between a pixel and its neighbors. If the area is flat, it outputs zero (black). If there is a change, it lights up.

### Mini Mind Map
```mermaid
mindmap
  root((Laplacian Filter))
    Best For
      Sharpening blurry images
      Detecting Edges and Outlines
    Sucks At
      Noisy Images it makes noise 10x worse
    Side Effects
      Removes all color and smooth areas leaving only skeletons
```

### Logic Diagram
```mermaid
graph TD
    A[Start at Center Pixel] --> B[Multiply Center by Positive Number]
    A --> C[Multiply Neighbors by Negative Numbers]
    B --> D[Sum the Results]
    C --> D
    D --> E{Is the Sum Zero?}
    E -- Yes --> F[Output Black No Edge]
    E -- No --> G[Output White Edge Detected]
```

---

# Part 2: Non-Linear Spatial Filters
*These filters use Logic (Sorting/Selection) to change pixels.*

## 4. The Median Filter

### The Concept
**"The Democracy."** It looks at a group of pixels, sorts them from lowest to highest, and picks the one exactly in the middle. It ignores extreme outliers (noise).

### Mini Mind Map
```mermaid
mindmap
  root((Median Filter))
    Best For
      Completely removing Salt and Pepper Noise
      Preserving hard edges
    Sucks At
      Smooth continuous gradients like a sky
    Side Effects
      Can make the image look patchy or like an oil painting
```

### Logic Diagram
```mermaid
graph TD
    A[Start at Center Pixel] --> B[Collect Neighbor Values into a List]
    B --> C[Sort List form Lowest to Highest]
    C --> D[Ignore High and Low Extremes]
    D --> E[Select the Value exactly in the Middle]
    E --> F[Replace Center Pixel with Middle Value]
```

---

## 5. The Nagao Filter

### The Concept
**"The Smart Smoother."** It looks around in 9 different directions to find the "calmest" (lowest variance) area nearby. It copies the average of *that* area, effectively refusing to blur across an edge.

### Mini Mind Map
```mermaid
mindmap
  root((Nagao Filter))
    Best For
      Smoothing flat areas
      Keeping edges razor sharp
    Sucks At
      Computation Speed it is very slow
    Side Effects
      Gives the image a cartoonish blocky appearance
```

### Logic Diagram
```mermaid
graph TD
    A[Start at Center Pixel] --> B[Split Neighborhood into 9 Sub Regions]
    B --> C[Calculate Variance Chaos of EACH Region]
    C --> D{Which Region has LOWEST Variance?}
    D --> E[Select the Winner Region]
    E --> F[Calculate Average of ONLY the Winner Region]
    F --> G[Replace Center Pixel with Winner Average]
```

---

# Part 3: Frequency Domain Filters
*These filters convert the image to a spectrum, delete frequencies, and convert it back.*

## 6. Low-Pass Filter (Passe-Bas)

### The Concept
**"The Blur Mask."** In the frequency domain, the center represents smooth shapes. This filter keeps the center (White Box) and deletes the edges (Black).

### Mini Mind Map
```mermaid
mindmap
  root((Low Pass Filter))
    Best For
      Heavy Noise Reduction
      Smoothing
    Sucks At
      Keeping any detail at all
    Side Effects
      The output is a blurry blob
```

### Logic Diagram
```mermaid
graph TD
    A[Input Image] --> B[FFT Transform]
    B --> C[Apply Mask: White Center / Black Edges]
    C --> D[Inverse FFT]
    D --> E[Result: Blurred Image]
```

---

## 7. High-Pass Filter (Passe-Haut)

### The Concept
**"The Ghost Mask."** In the frequency domain, the edges represent details. This filter keeps the edges (White) and deletes the center (Black Box).

### Mini Mind Map
```mermaid
mindmap
  root((High Pass Filter))
    Best For
      Extracting Contours
      Sharpening
    Sucks At
      Keeping colors or brightness
    Side Effects
      The output is mostly black with white outlines
```

### Logic Diagram
```mermaid
graph TD
    A[Input Image] --> B[FFT Transform]
    B --> C[Apply Mask: Black Center / White Edges]
    C --> D[Inverse FFT]
    D --> E[Result: Edges Only]
```

---

## 8. Band-Reject Filter (Coupe-Bande)

### The Concept
**"The Noise Killer."** Sometimes noise is a specific repeating pattern. This filter creates a "Black Frame" (Square Donut) mask to delete just that specific range of frequencies.

### Mini Mind Map
```mermaid
mindmap
  root((Band Reject Filter))
    Best For
      Removing Periodic/Repeating Noise
      Cleaning interference lines
    Sucks At
      Removing random dust/speckle noise
    Side Effects
      Minimal side effects if tuned correctly
```

### Logic Diagram
```mermaid
graph TD
    A[Input Image] --> B[FFT Transform]
    B --> C[Apply Mask: Black Frame / White Center / White Edge]
    C --> D[Inverse FFT]
    D --> E[Result: Clean Image]
```

---

# Part 4: The Giant Summary Diagram

This diagram visualizes the decision process for the **Frequency Domain Filters** based on the square masks seen in your slides.

```mermaid
graph TD
    %% NODES SETUP
    Input[Input Image]
    FFT[Compute FFT -> Spectrum]
    
    %% BRANCHES
    Input --> FFT
    FFT --> Path1(Case 1: Low-Pass)
    FFT --> Path2(Case 2: High-Pass)
    FFT --> Path3(Case 3: Band-Reject)

    %% PATH 1: LOW PASS
    subgraph LP [FILTER 1: LOW PASS / Passe-Bas]
    Path1 --> Mask1[Mask Shape: <br/>BLACK background <br/> WHITE Square in Center]
    Mask1 --> Action1[Action: <br/>Keep ONLY the Center]
    Action1 --> Result1[Result: <br/>Image is BLURRED]
    end

    %% PATH 2: HIGH PASS
    subgraph HP [FILTER 2: HIGH PASS / Passe-Haut]
    Path2 --> Mask2[Mask Shape: <br/>WHITE background <br/> BLACK Square in Center]
    Mask2 --> Action2[Action: <br/>DELETE the Center]
    Action2 --> Result2[Result: <br/>EDGES Only / Ghost Look]
    end

    %% PATH 3: BAND REJECT
    subgraph BR [FILTER 3: BAND REJECT / Coupe-Bande]
    Path3 --> Mask3[Mask Shape: <br/>A Black SQUARE FRAME <br/> Center is White, Edge is White]
    Mask3 --> Action3[Action: <br/>Delete specific Middle Frequencies]
    Action3 --> Result3[Result: <br/>Remove REPEATING NOISE]
    end

    %% FINAL OUTPUT
    Result1 --> Inverse1[Inverse FFT -> View Image]
    Result2 --> Inverse2[Inverse FFT -> View Image]
    Result3 --> Inverse3[Inverse FFT -> View Image]
    
    style LP fill:#222,stroke:#fff,stroke-width:2px,color:#fff
    style HP fill:#ddd,stroke:#333,stroke-width:2px,color:#000
    style BR fill:#444,stroke:#ff9900,stroke-width:2px,color:#fff
```