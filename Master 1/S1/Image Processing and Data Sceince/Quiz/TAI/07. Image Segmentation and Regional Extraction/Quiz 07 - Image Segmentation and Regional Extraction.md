---
sources:
  - "[[07.1. Formal Segmentation Axioms and Homogeneity Predicates]]"
  - "[[07.2. Global Optimal Statistical Thresholding (Otsu's Method Derivation)]]"
  - "[[07.3. Local Adaptive Thresholding (Niblack and Dynamic Range Sauvola)]]"
  - "[[07.4. Complex Document Segmentation (Gaceb's Multi-Scale Mixed Binarization)]]"
  - "[[07.5. Morphological Watershed Segmentation and Topological Distance Transforms]]"
  - "[[07.6. Connected Component Analysis (Two-Pass CCL and Equivalence Trees)]]"
  - "[[07.7. Geometric Region Descriptors (AABB, OBB, Centroids, and Central Moments)]]"
  - "[[07.8. Segmentation Evaluation Benchmarks (Dice DSC, Jaccard IoU, Hausdorff Distance)]]"
---
> [!question] During the first pass of two-pass connected component labeling, when exactly one already-scanned neighbor of a foreground pixel carries a label, the pixel must receive a brand-new provisional label.
>> [!success]- Answer
>> False

> [!question] Under the standard binarization rule, a pixel whose intensity is exactly equal to the threshold $T$ is assigned to the foreground class.
>> [!success]- Answer
>> True

> [!question] Because the total variance $\sigma_T^2$ is constant for a given image, minimizing the within-class variance $\sigma_W^2(t)$ is mathematically equivalent to maximizing the between-class variance $\sigma_B^2(t)$.
>> [!success]- Answer
>> True

> [!question] Otsu's method locates the optimal threshold by iteratively refining an initial guess until convergence, rather than by exhaustively evaluating a criterion over all candidate gray levels.
>> [!success]- Answer
>> False

> [!question] In Niblack's method, flat background regions where the local standard deviation is nearly zero make the threshold collapse toward the local mean, so faint background noise is often misclassified as foreground text.
>> [!success]- Answer
>> True

> [!question] Sauvola's method uses the same negative tuning values as Niblack's method, typically $k = -0.2$, for binarizing dark text on a light background.
>> [!success]- Answer
>> False

> [!question] In Gaceb's multi-scale mixed binarization, the global Fisher discriminant classification of blocks is performed before any local adaptive thresholding is applied.
>> [!success]- Answer
>> True

> [!question] Applying the watershed transform directly to a raw image gradient frequently produces severe over-segmentation, dividing the image into thousands of tiny, meaningless fragments.
>> [!success]- Answer
>> True

> [!question] In the first scan of the classical two-pass labeling algorithm, each foreground pixel is labeled by consulting the pixels below it and to its right.
>> [!success]- Answer
>> False

> [!question] Although the Dice coefficient and the Jaccard index quantify region overlap, they also fully capture how closely a segmented boundary follows the ground-truth contour.
>> [!success]- Answer
>> False

> [!question] In the formal segmentation axioms, the uniform property predicate P that every region must satisfy typically expresses which requirement?
> a) The region shares no pixel with any other region.
> b) The pixels of the region match in intensity, color, or texture.
> c) The region is a single connected set of pixels on the grid.
> d) The union of the regions covers the entire image domain.
>> [!success]- Answer
>> b) The pixels of the region match in intensity, color, or texture.

> [!question] With $L$ discrete gray levels and a candidate threshold $t$, how does Otsu's method define its two pixel classes?
> a) Background $C_1$ takes intensities in $[t+1, L-1]$ and foreground $C_2$ takes $[0, t]$.
> b) Background $C_1$ takes intensities in $[0, t-1]$ and foreground $C_2$ takes $[t, L-1]$.
> c) Background $C_1$ takes intensities in $[0, t]$ and foreground $C_2$ takes $[t+1, L-1]$.
> d) Background $C_1$ takes intensities in $[0, L/2]$ and foreground $C_2$ takes $[L/2 + 1, L-1]$.
>> [!success]- Answer
>> c) Background $C_1$ takes intensities in $[0, t]$ and foreground $C_2$ takes $[t+1, L-1]$.

> [!question] Which expression is a closed form of the between-class variance $\sigma_B^2(t)$ in Otsu's method?
> a) $\omega_1(t)\omega_2(t)(\mu_1(t) - \mu_2(t))^2$
> b) $\omega_1(t)\sigma_1^2(t) + \omega_2(t)\sigma_2^2(t)$
> c) $\omega_1(t)\mu_1(t) + \omega_2(t)\mu_2(t)$
> d) $(\mu_1(t) - \mu_2(t))^2$
>> [!success]- Answer
>> a) $\omega_1(t)\omega_2(t)(\mu_1(t) - \mu_2(t))^2$

> [!question] Global thresholding methods such as Otsu's typically break down, requiring local adaptive thresholding, when the image has which property?
> a) A strongly bimodal histogram with two sharp peaks.
> b) More than two distinct object classes.
> c) Very high spatial resolution.
> d) Non-uniform lighting, shadows, or intensity gradients across the scene.
>> [!success]- Answer
>> d) Non-uniform lighting, shadows, or intensity gradients across the scene.

> [!question] Which formula gives the threshold that Niblack's method computes inside each $W \times W$ sliding window?
> a) $T(x, y) = m(x, y) - k \cdot s(x, y)$
> b) $T(x, y) = m(x, y) + k \cdot s(x, y)$
> c) $T(x, y) = m(x, y) \cdot [1 + k \cdot (\frac{s(x, y)}{R} - 1)]$
> d) $T(x, y) = m(x, y) + k \cdot R$
>> [!success]- Answer
>> b) $T(x, y) = m(x, y) + k \cdot s(x, y)$

> [!question] In the marker-controlled watershed pipeline, what value does the distance transform assign to each foreground pixel?
> a) Its Euclidean distance to the nearest background pixel.
> b) The gradient magnitude at that pixel.
> c) Its Euclidean distance to the nearest sure foreground marker.
> d) Its Euclidean distance to the image center.
>> [!success]- Answer
>> a) Its Euclidean distance to the nearest background pixel.

> [!question] How is the centroid $(\bar{x}, \bar{y})$ of a labeled region computed from its raw moments?
> a) $\bar{x} = m_{01}/m_{00}$ and $\bar{y} = m_{10}/m_{00}$
> b) $\bar{x} = \mu_{10}/\mu_{00}$ and $\bar{y} = \mu_{01}/\mu_{00}$
> c) $\bar{x} = m_{10}/m_{00}$ and $\bar{y} = m_{01}/m_{00}$
> d) $\bar{x} = m_{10}/m_{01}$ and $\bar{y} = m_{01}/m_{10}$
>> [!success]- Answer
>> c) $\bar{x} = m_{10}/m_{00}$ and $\bar{y} = m_{01}/m_{00}$

> [!question] The orientation angle $\theta$ of a region's principal axis of inertia is computed from which quantities?
> a) The width and height of the axis-aligned bounding box.
> b) The raw moments $m_{10}$ and $m_{01}$.
> c) The area $m_{00}$ and the centroid coordinates.
> d) The second-order central moments, via $\theta = \frac{1}{2}\arctan(\frac{2\mu_{11}}{\mu_{20} - \mu_{02}})$.
>> [!success]- Answer
>> d) The second-order central moments, via $\theta = \frac{1}{2}\arctan(\frac{2\mu_{11}}{\mu_{20} - \mu_{02}})$.

> [!question] A segmentation obtains a Jaccard index of $0.5$ against the ground truth; using the relationship between the two overlap metrics, what is its Dice coefficient?
> a) $0.5$
> b) $\frac{2}{3}$
> c) $0.75$
> d) $1$
>> [!success]- Answer
>> b) $\frac{2}{3}$

> [!question] Dice, Jaccard, and the Hausdorff distance are called supervised evaluation metrics; what does this mean?
> a) They compare the algorithm's output against an annotated ground-truth reference.
> b) They measure intrinsic region properties such as homogeneity without needing any reference.
> c) They require a human expert to visually approve every segmentation result.
> d) They compare the output only against results from other unsupervised algorithms.
>> [!success]- Answer
>> a) They compare the algorithm's output against an annotated ground-truth reference.

> [!question] Match each statistical quantity in Otsu's derivation with its meaning.
>> [!example] Group A
>> a) $\omega_1(t)$
>> b) $\omega_2(t)$
>> c) $\mu_1(t)$
>> d) $\sigma_W^2(t)$
>> e) $\sigma_B^2(t)$
>
>> [!example] Group B
>> n) The variance component that reflects how far apart the two class means sit, and the quantity the method maximizes.
>> o) The cumulative probability mass of the background class, summing $p_i$ over intensities up to $t$.
>> p) A probability-weighted average of the variances inside each of the two classes.
>> q) The average intensity of the background pixels, computed from the histogram levels up to $t$.
>> r) The class weight of the foreground, obtained as one minus the background weight.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> r)
>> c) -> q)
>> d) -> p)
>> e) -> n)

> [!question] Match each behavior or parameter of local adaptive thresholding with its description.
>> [!example] Group A
>> a) Niblack tuning constant
>> b) Sauvola dynamic range
>> c) Sauvola in flat backgrounds
>> d) Sauvola at text strokes
>> e) Sauvola's design goal
>
>> [!example] Group B
>> n) Introduced in 2000 to cure the noise amplification that earlier windowed methods suffered in uniform regions.
>> o) Typically negative, around $-0.1$ or $-0.2$, when segmenting dark text on a light page.
>> p) The local standard deviation approaches its ceiling, so the threshold stays close to the mean and character edges remain crisp.
>> q) Fixed at $128$ for standard 8-bit images.
>> r) The threshold falls to roughly $m(x, y) \cdot (1 - k)$, far below the mean, so faint fluctuations are not detected as foreground.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> r)
>> d) -> p)
>> e) -> n)

> [!question] Match each stage of Gaceb's mixed binarization pipeline with its role.
>> [!example] Group A
>> a) Spatial block decomposition
>> b) Fisher discriminant analysis
>> c) Cumulative gradient operator
>> d) Sauvola refinement pass
>
>> [!example] Group B
>> n) Runs the windowed adaptive threshold only within active text regions, preserving fine character detail while the background stays clean.
>> o) Splits the page into rectangular patches of varying sizes so differently illuminated areas are isolated.
>> p) Classifies each patch as pure background or mixed content; background patches go straight to a fast global cut.
>> q) Finds potential character strokes inside mixed patches containing degraded or faded text.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match each topographic watershed concept with its description.
>> [!example] Group A
>> a) Topographic relief
>> b) Catchment basin
>> c) Watershed line
>> d) Local minima
>
>> [!example] Group B
>> n) A dam erected where water arriving from two different directions would meet, forming the final segmentation boundary.
>> o) The points where holes are pierced so that water can rise and fill the surface.
>> p) Interprets pixel intensity as altitude, turning the grayscale image into a 3D landscape.
>> q) The depression that gradually fills as water rises around one of the pierced holes.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match each element of the marker-controlled watershed pipeline with its purpose.
>> [!example] Group A
>> a) Sure foreground markers
>> b) Sure background markers
>> c) Unknown region
>> d) Marker-controlled flooding
>
>> [!example] Group B
>> n) Pixels guaranteed to lie outside any object, obtained by dilating the binary mask.
>> o) Object centers isolated by thresholding the distance map.
>> p) Runs the transform on the image gradient, with water entering only at the verified locations, which prevents excessive fragmentation.
>> q) The boundary zone between the two verified sets, found by subtracting one from the other, where object edges lie.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match each step of the two-pass connected component labeling algorithm with its behavior.
>> [!example] Group A
>> a) First pass
>> b) Case A
>> c) Case C
>> d) Union-Find table
>> e) Second pass
>
>> [!example] Group B
>> n) All already-scanned neighbors are background, so the pixel receives a brand-new label.
>> o) A disjoint-set structure that remembers which provisional labels are equivalent.
>> p) A raster scan, row by row from top to bottom and left to right, handing out provisional labels.
>> q) Several neighbors hold different labels, so the smallest one is assigned and the conflict is recorded for later merging.
>> r) A final sweep that replaces every provisional label with the root label of its equivalence class.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)
>> e) -> r)

> [!question] Match each geometric region descriptor with its definition.
>> [!example] Group A
>> a) Axis-aligned bounding box
>> b) Raw moment $m_{00}$
>> c) Centroid
>> d) Central moments
>> e) Oriented bounding box
>
>> [!example] Group B
>> n) Statistics measured about the center of mass, unaffected by where the object sits in the image.
>> o) The smallest enclosing rectangle with sides parallel to the image rows and columns.
>> p) A rotated minimum-area rectangle aligned with the principal axis of inertia, tighter for elongated objects.
>> q) Counts every pixel of the object, giving its total area.
>> r) The center of mass of the object's pixel distribution.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> r)
>> d) -> n)
>> e) -> p)

> [!question] Match each axis-aligned bounding box measurement with its formula.
>> [!example] Group A
>> a) Width
>> b) Height
>> c) Aspect ratio
>> d) Extent
>
>> [!example] Group B
>> n) The quotient of the horizontal span divided by the vertical span.
>> o) The span in the x direction, computed as $x_{max} - x_{min} + 1$.
>> p) The fraction of the enclosing rectangle that is actually covered by object pixels.
>> q) The span in the y direction, computed as $y_{max} - y_{min} + 1$.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match each segmentation evaluation metric with its definition.
>> [!example] Group A
>> a) Dice coefficient
>> b) Jaccard index
>> c) Hausdorff distance
>> d) Intra-region variance
>> e) Zeboudj contrast
>
>> [!example] Group B
>> n) Relative region overlap computed as $2|A \cap B| / (|A| + |B|)$, ranging from 0 to 1.
>> o) The maximum separation between the two boundary sets, highly sensitive to outliers and localized errors.
>> p) An area-weighted sum of the squared intensity deviations within each segment, where lower values mean more homogeneous regions.
>> q) Intersection over union, computed as $|A \cap B| / |A \cup B|$.
>> r) Scores how distinct neighboring regions are relative to their internal homogeneity, with higher scores indicating better separation.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> q)
>> c) -> o)
>> d) -> p)
>> e) -> r)

> [!question] Match each formal segmentation axiom with its requirement.
>> [!example] Group A
>> a) Completeness
>> b) Disjointness
>> c) Homogeneity
>> d) Separability
>> e) Connectivity
>
>> [!example] Group B
>> n) Every pixel of the image domain belongs to some region, since the union of all regions reconstructs the whole image.
>> o) Two adjacent regions cannot be merged, because their combined pixels violate the uniformity requirement.
>> p) No pixel can belong to two regions at once: pairwise intersections are empty.
>> q) All pixels inside a region satisfy one uniform property predicate.
>> r) Every region forms one spatially contiguous piece on the discrete pixel grid.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> q)
>> d) -> o)
>> e) -> r)
