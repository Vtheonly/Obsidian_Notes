---
sources:
  - "[[23. Scikit-Learn Primitives - Clustering, Dimensionality, and Metrics]]"
---
> [!question] Passing a 3D image tensor directly to `KMeans.fit()` works because scikit-learn infers the channel dimension automatically.
>> [!success]- Answer
>> False

> [!question] `uint8` pixel features can overflow during distance accumulation, so they should be cast to `np.float32` before fitting.
>> [!success]- Answer
>> True

> [!question] K-Means is initialization-dependent, so fixing `random_state` makes segmentation reproducible.
>> [!success]- Answer
>> True

> [!question] `StandardScaler` is unnecessary for K-Means because Euclidean distance is scale-invariant.
>> [!success]- Answer
>> False

> [!question] What does the reshape pattern `img.reshape((-1, 3))` produce for scikit-learn?
> a) A (rows, columns) label map
> b) An (n_samples, n_features) pixel feature matrix
> c) A (3, n_pixels) transposed channel list
> d) A flattened 1D intensity vector
>> [!success]- Answer
>> b) An (n_samples, n_features) pixel feature matrix

> [!question] What does `jaccard_score` measure?
> a) Intersection-over-Union between a predicted binary mask and a ground-truth reference
> b) Pixel-wise accuracy between two grayscale images
> c) The mean squared error of cluster centers
> d) The silhouette quality of a clustering
>> [!success]- Answer
>> a) Intersection-over-Union between a predicted binary mask and a ground-truth reference

> [!question] For a multi-class segmentation, how do you obtain per-class IoU scores with `jaccard_score`?
> a) Rescale the mask values to 255 first
> b) Pass `average=None` with the flattened label maps
> c) Pass `n_clusters=K` to the scorer
> d) Convert the labels to one-hot RGB channels
>> [!success]- Answer
>> b) Pass `average=None` with the flattened label maps

> [!question] Which objective does K-Means minimize?
> a) The total pairwise distance between all pixels
> b) The between-cluster variance divided by the total variance
> c) The within-cluster sum of squared distances to the cluster means
> d) The number of clusters with empty membership
>> [!success]- Answer
>> c) The within-cluster sum of squared distances to the cluster means

> [!question] Match each scikit-learn primitive with its purpose.
>> [!example] Group A
>> a) `KMeans`
>> b) `jaccard_score`
>> c) `StandardScaler`
>
>> [!example] Group B
>> n) Measures Intersection-over-Union between predicted and ground-truth binary masks.
>> o) Partitions pixel colors into K clusters for unsupervised segmentation.
>> p) Standardizes features to zero mean and unit variance for scale-sensitive estimators.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match each step of the pixel clustering pattern with its role.
>> [!example] Group A
>> a) `img.reshape((-1, 3))`
>> b) `fit_predict(pixel_features)`
>> c) `labels.reshape((100, 100))`
>
>> [!example] Group B
>> n) Returns the cluster label for every pixel sample at once.
>> o) Builds the sample-feature matrix that scikit-learn expects.
>> p) Restores the flat label vector to the original 2D image geometry.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match each pitfall with its consequence.
>> [!example] Group A
>> a) Passing a 3D image tensor directly to `fit`
>> b) Keeping pixel features in `uint8`
>> c) Leaving `random_state` unset
>
>> [!example] Group B
>> n) Overflows during distance accumulation in the clustering objective.
>> o) Raises an error because images must become sample-feature matrices first.
>> p) Makes results vary between runs because initialization is random.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match each quantity with its meaning.
>> [!example] Group A
>> a) $\arg\min_{C} \sum_{k=1}^{K} \sum_{x \in C_k} \| x - \mu_k \|^2$
>> b) $J(A, B) = \frac{|A \cap B|}{|A \cup B|}$
>> c) Zero mean and unit variance
>
>> [!example] Group B
>> n) The statistical target produced by feature standardization.
>> o) The within-cluster objective that K-Means minimizes.
>> p) The Intersection-over-Union definition used for segmentation evaluation.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
