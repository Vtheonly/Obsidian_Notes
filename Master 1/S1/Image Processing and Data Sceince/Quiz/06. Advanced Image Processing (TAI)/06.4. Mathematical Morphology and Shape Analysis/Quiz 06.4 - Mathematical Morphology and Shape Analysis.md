---
sources:
  - "[[06.4.1. Set-Theoretic Foundations, Binary Grids, and Structuring Elements]]"
  - "[[06.4.2. Compound Operators (Opening, Closing, Gradient, and Zhang-Suen Thinning)]]"
---
> [!question] The structuring element is the morphological counterpart of the convolution kernel: a small binary matrix that defines the shape and neighborhood of the probe.
>> [!success]- Answer
>> True

> [!question] Binary erosion expands foreground objects by growing their boundaries outward.
>> [!success]- Answer
>> False

> [!question] For a grayscale image, erosion replaces each pixel with the local maximum of the intensities in the neighborhood defined by the structuring element.
>> [!success]- Answer
>> False

> [!question] In the set-theoretic definition of dilation, the reflected structuring element translated by $z$ must be completely contained within the foreground set $A$.
>> [!success]- Answer
>> False

> [!question] Morphological opening is idempotent: applying it a second time with the same structuring element produces no further change.
>> [!success]- Answer
>> True

> [!question] Zhang-Suen thinning reduces a binary object to a one-pixel-wide skeleton while preserving the original topology and connectivity of the object.
>> [!success]- Answer
>> True

> [!question] Which set-theoretic condition defines the erosion $A \ominus B$ of a foreground set $A$ by a structuring element $B$?
> a) The reflected structuring element translated by $z$ overlaps $A$ in at least one pixel.
> b) The structuring element translated by $z$ fits completely inside $A$.
> c) The structuring element translated by $z$ is disjoint from $A$.
> d) The structuring element translated by $z$ contains the entire set $A$.
>> [!success]- Answer
>> b) The structuring element translated by $z$ fits completely inside $A$.

> [!question] In the Zhang-Suen thinning algorithm, what does the quantity $A(P_1)$ count?
> a) The number of non-zero neighbors surrounding $P_1$.
> b) The number of connected components in the object containing $P_1$.
> c) The number of $0 \to 1$ transitions in the ordered sequence $P_2, P_3, P_4, P_5, P_6, P_7, P_8, P_9, P_2$.
> d) The number of thinning sub-iterations applied so far.
>> [!success]- Answer
>> c) The number of $0 \to 1$ transitions in the ordered sequence $P_2, P_3, P_4, P_5, P_6, P_7, P_8, P_9, P_2$.

> [!question] Which expression defines the morphological gradient of a set $A$ with structuring element $B$?
> a) $(A \oplus B) - (A \ominus B)$
> b) $(A \oplus B) + (A \ominus B)$
> c) $(A \circ B) - (A \bullet B)$
> d) $A - (A \ominus B)$
>> [!success]- Answer
>> a) $(A \oplus B) - (A \ominus B)$

> [!question] In the matrix representation of a structuring element, what does the bracketed cell indicate?
> a) A don't-care position that is excluded from probing.
> b) The maximum intensity allowed within the probe.
> c) The pixel scheduled for deletion during thinning.
> d) The origin (0,0) of the element, which marks the pivot point of the probe.
>> [!success]- Answer
>> d) The origin (0,0) of the element, which marks the pivot point of the probe.

> [!question] What does grayscale dilation with structuring element $B$ compute at each pixel of an image $f$?
> a) The local minimum over the neighborhood defined by $B$.
> b) The local maximum over the neighborhood defined by $B$.
> c) The arithmetic mean over the neighborhood defined by $B$.
> d) The median of the sorted values over the neighborhood defined by $B$.
>> [!success]- Answer
>> b) The local maximum over the neighborhood defined by $B$.

> [!question] In the Zhang-Suen deletion conditions, the constraint $2 \le B(P_1) \le 6$ applies to which quantity?
> a) The number of $0 \to 1$ transitions in the neighbor sequence.
> b) The number of completed thinning iterations.
> c) The number of non-zero neighbors among the eight pixels surrounding $P_1$.
> d) The number of structuring elements applied to $P_1$.
>> [!success]- Answer
>> c) The number of non-zero neighbors among the eight pixels surrounding $P_1$.

> [!question] Match the structuring element shape with its probing behavior.
>> [!example] Group A
>> a) Box or square
>> b) Cross
>> c) Disk
>
>> [!example] Group B
>> n) Provides isotropic, rotationally symmetric probing.
>> o) Probes connectivity equally in all 8 directions.
>> p) Probes only the 4-connected horizontal and vertical directions.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the compound operator with the sequence of basic operations that constructs it.
>> [!example] Group A
>> a) Opening
>> b) Closing
>> c) Zhang-Suen thinning
>
>> [!example] Group B
>> n) A dilation followed by an erosion using the same structuring element.
>> o) An erosion followed by a dilation using the same structuring element.
>> p) Parallel passes that alternate two sub-iterations of boundary-pixel deletion.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the morphological operation with its geometric analogy or characterization.
>> [!example] Group A
>> a) Opening
>> b) Closing
>> c) Morphological gradient
>
>> [!example] Group B
>> n) A non-linear boundary extraction method, contrasted with differential operators such as Sobel and Laplacian.
>> o) Rolling a ball along the outside of the object so that gaps narrower than the ball are filled.
>> p) Rolling a ball inside the object so that protrusions narrower than the ball are eliminated.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the morphological operation with its primary effect on the foreground.
>> [!example] Group A
>> a) Erosion
>> b) Dilation
>> c) Opening
>> d) Closing
>
>> [!example] Group B
>> n) Eliminates small isolated bright specks (salt noise) and severs thin bridges between adjacent structures.
>> o) Expands foreground boundaries, filling small holes and gaps (pepper noise) and merging nearby structures.
>> p) Removes small outer protrusions and separates lightly touching objects while restoring surviving structures to their original size.
>> q) Fills interior holes and bridges small breaks in contours while restoring the original outer dimensions.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match each pixel label of the Zhang-Suen neighborhood with its position or role.
>> [!example] Group A
>> a) $P_1$
>> b) $P_2$
>> c) $P_4$
>> d) $P_6$
>> e) $P_8$
>
>> [!example] Group B
>> n) The neighbor directly to the right of the central pixel.
>> o) The foreground boundary pixel examined for possible deletion.
>> p) The neighbor directly to the left of the central pixel.
>> q) The neighbor directly above the central pixel.
>> r) The neighbor directly below the central pixel.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> r)
>> e) -> p)

> [!question] Match each aspect of the Zhang-Suen algorithm with its specification.
>> [!example] Group A
>> a) Sub-iteration 1
>> b) Sub-iteration 2
>> c) Deletion rule
>> d) Stopping rule
>
>> [!example] Group B
>> n) Requires $P_2 \cdot P_4 \cdot P_8 = 0$ and $P_2 \cdot P_6 \cdot P_8 = 0$.
>> o) Passes are repeated until no further boundary pixels can be removed.
>> p) Requires $P_2 \cdot P_4 \cdot P_6 = 0$ and $P_4 \cdot P_6 \cdot P_8 = 0$.
>> q) A boundary pixel is removed only when all four requirements hold at the same time.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)
