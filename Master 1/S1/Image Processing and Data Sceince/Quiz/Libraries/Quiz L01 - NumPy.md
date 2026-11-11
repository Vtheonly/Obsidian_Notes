---
sources:
  - "[[01. NumPy Foundations - Memory Layout, ndarray Anatomy, and Array Instantiation]]"
  - "[[02. NumPy Array Manipulation - Slicing, Strides, Shapes, and Vectorized Indexing]]"
  - "[[04. NumPy Mathematical Engine - Vectorization, ufuncs, and Broadcasting Rules]]"
  - "[[05. NumPy Linear Algebra and Advanced Numerical Computation]]"
---
> [!question] The strides attribute of an ndarray specifies how many bytes must be jumped in memory to advance one step along each dimension.
>> [!success]- Answer
>> True

> [!question] A standard Python list is an array of pointers to scattered PyObject structures, so every element access incurs pointer indirection and object header overhead.
>> [!success]- Answer
>> True

> [!question] Calling `.astype(np.float32)` on an array converts the buffer in place, without allocating a new array.
>> [!success]- Answer
>> False

> [!question] Modifying an element of a slice view such as `a[0:2, 0:2]` also changes the corresponding element of the underlying original array.
>> [!success]- Answer
>> True

> [!question] Boolean mask indexing such as `a[a < 6]` returns a view that shares memory with the original array.
>> [!success]- Answer
>> False

> [!question] Compound boolean mask conditions must be combined with the Python keywords and and or rather than the bitwise operators.
>> [!success]- Answer
>> False

> [!question] When broadcasting two arrays, the shape tuples are aligned starting from the trailing (rightmost) dimensions, and a shape with fewer dimensions is padded with ones on the left.
>> [!success]- Answer
>> True

> [!question] With axis=0, a reduction such as `np.mean` collapses the columns by computing statistics across each row.
>> [!success]- Answer
>> False

> [!question] A universal function (ufunc) operates on ndarray objects element-by-element in compiled C code, eliminating Python interpreter overhead and enabling SIMD parallel execution.
>> [!success]- Answer
>> True

> [!question] `np.linalg.solve(A, b)` computes the solution by explicitly forming the inverse of A and multiplying it with b.
>> [!success]- Answer
>> False

> [!question] For a C-order (row-major) `float64` array of shape (3, 4), what does the `a.strides` attribute report?
> a) `(24, 8)`
> b) `(32, 8)`
> c) `(8, 32)`
> d) `(4, 3)`
>> [!success]- Answer
>> b) `(32, 8)`

> [!question] What is the result of `np.array([100], dtype=np.uint8) - np.array([150], dtype=np.uint8)`?
> a) `array([206], dtype=uint8)`
> b) `array([-50], dtype=uint8)`
> c) `array([0], dtype=uint8)`
> d) An `OverflowError` is raised
>> [!success]- Answer
>> a) `array([206], dtype=uint8)`

> [!question] You need exactly 5 evenly spaced values from 0.0 to 1.0, with both endpoints included. Which call produces them?
> a) `np.arange(0, 1, 5)`
> b) `np.linspace(0, 1, 4)`
> c) `np.linspace(0, 1, 5)`
> d) `np.arange(0, 1, 0.25)`
>> [!success]- Answer
>> c) `np.linspace(0, 1, 5)`

> [!question] What does the single-argument call `np.where(mask)` return for a 2D boolean array mask?
> a) A 1D array holding the values at the masked positions
> b) A tuple of coordinate arrays identifying the indices where the mask is True
> c) A boolean mask of the same shape as the input
> d) A scalar count of the True positions
>> [!success]- Answer
>> b) A tuple of coordinate arrays identifying the indices where the mask is True

> [!question] For a 2D array `a`, what does the slice `a[::2, :]` select?
> a) Every 2nd row starting from row 0, such as rows 0 and 2 of a 3-row array
> b) Every 2nd column within each row
> c) The first two rows only
> d) All rows in reversed order
>> [!success]- Answer
>> a) Every 2nd row starting from row 0, such as rows 0 and 2 of a 3-row array

> [!question] What does `np.clip(np.array([-10, 50, 260]), 0, 255)` return?
> a) `array([-10, 50, 260])`
> b) `array([0, 50, 260])`
> c) `array([255, 50, 0])`
> d) `array([0, 50, 255])`
>> [!success]- Answer
>> d) `array([0, 50, 255])`

> [!question] What is the difference between `np.maximum(a, b)` and `np.max(a)`?
> a) They are aliases for the same operation
> b) `np.maximum(a, b)` is a binary ufunc returning the element-wise maxima of two arrays, while `np.max(a)` reduces one array to a single value per axis
> c) `np.maximum(a, b)` reduces both arrays to one scalar, while `np.max(a)` compares two arrays element-wise
> d) `np.max(a)` only accepts 2D arrays, while `np.maximum(a, b)` accepts any shape
>> [!success]- Answer
>> b) `np.maximum(a, b)` is a binary ufunc returning the element-wise maxima of two arrays, while `np.max(a)` reduces one array to a single value per axis

> [!question] Adding a matrix of shape (4, 3) to a vector of shape (4,) fails. Why, and what does NumPy raise?
> a) The trailing dimensions 3 and 4 are neither equal nor 1, so NumPy raises `ValueError: operands could not be broadcast together`
> b) The leading dimensions 4 and 4 match, so NumPy broadcasts successfully and returns shape (4, 3)
> c) NumPy silently pads the vector with zeros into shape (4, 3) and completes the addition
> d) NumPy raises `TypeError: unsupported operand types` for the mismatched shapes
>> [!success]- Answer
>> a) The trailing dimensions 3 and 4 are neither equal nor 1, so NumPy raises `ValueError: operands could not be broadcast together`

> [!question] How do you compute the matrix product of two 2D arrays `A` and `B` in modern NumPy?
> a) `A * B`
> b) `np.multiply(A, B)`
> c) `A @ B` or `np.dot(A, B)`
> d) `np.hstack((A, B))`
>> [!success]- Answer
>> c) `A @ B` or `np.dot(A, B)`

> [!question] What does `np.linalg.det(A)` return for a square matrix `A`?
> a) The inverse matrix of `A`
> b) A vector of the eigenvalues of `A`
> c) A boolean indicating whether `A` is invertible
> d) A scalar: the determinant of `A`
>> [!success]- Answer
>> d) A scalar: the determinant of `A`

> [!question] Match the array creation routine with the result it produces.
>> [!example] Group A
>> a) `np.zeros`
>> b) `np.full`
>> c) `np.eye`
>> d) `np.empty`
>> e) `np.fromfunction`
>
>> [!example] Group B
>> n) An identity matrix with 1.0 along the diagonal, e.g. 3x3 when N is 3.
>> o) Raw allocated memory with no initialization; contents are whatever bytes were already in RAM.
>> p) Values computed from their grid coordinates, e.g. the product i times j at each position (i, j).
>> q) A shape-(2, 3) array where every element starts at 0.0.
>> r) A 2x2 array where every element equals a caller-supplied constant such as 7.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> r)
>> c) -> n)
>> d) -> o)
>> e) -> p)

> [!question] Match the NumPy data type with its defining property.
>> [!example] Group A
>> a) `np.uint8`
>> b) `np.int16`
>> c) `np.float32`
>> d) `np.float64`
>
>> [!example] Group B
>> n) One byte per element holding values from 0 to 255, the standard for grayscale pixels and binary masks.
>> o) Four bytes per element with about 7 decimals of precision, the usual choice for deep learning tensors.
>> p) Two bytes per element spanning about -32,768 to +32,767, used for medical DICOM Hounsfield units.
>> q) Eight bytes per element with about 16 decimals of precision, preferred for high-precision scientific statistics.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
>> d) -> q)

> [!question] Match each slicing expression, evaluated on the 3x4 array `a` with rows [1, 2, 3, 4], [5, 6, 7, 8], and [9, 10, 11, 12], with its result.
>> [!example] Group A
>> a) `a[:, 0]`
>> b) `a[1, 2]`
>> c) `a[0:2, 1:4]`
>> d) `a[:, ::-1]`
>
>> [!example] Group B
>> n) Each row with its column order reversed.
>> o) The values in column 0 across all rows, giving [1, 5, 9].
>> p) The submatrix covering rows 0 and 1 and columns 1 through 3.
>> q) The single scalar element at row 1, column 2, which is 7.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match the index-extraction function with what it returns.
>> [!example] Group A
>> a) `np.argmax(a)`
>> b) `np.argmax(a, axis=0)`
>> c) `np.unravel_index(flat_index, shape)`
>> d) `np.argsort(a)`
>
>> [!example] Group B
>> n) The conversion of a flattened 1D index into multi-dimensional coordinates.
>> o) For each column, the row index where that column's maximum sits.
>> p) The indices that would sort the array, usable for ranking values.
>> q) The index of the maximum value in the flattened array.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the reshaping or combination operation with its behavior.
>> [!example] Group A
>> a) `a.reshape(r, c)`
>> b) `a.ravel()`
>> c) `a.flatten()`
>> d) `np.hstack((a, b))`
>> e) `np.vstack((a, b))`
>
>> [!example] Group B
>> n) Flattens to 1D, always allocating an independent copy.
>> o) Presents the same data under a new shape as a view, allowed only when the total element count is unchanged.
>> p) Joins arrays side by side along axis 1, so they must share their row count.
>> q) Puts one array above the other along axis 0, adding rows and requiring a shared column count.
>> r) Flattens to 1D without copying data whenever possible.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> r)
>> c) -> n)
>> d) -> p)
>> e) -> q)

> [!question] Match the random sampling function with the distribution it draws from.
>> [!example] Group A
>> a) `np.random.randint`
>> b) `np.random.rand`
>> c) `np.random.randn`
>> d) `np.random.normal`
>> e) `np.random.uniform`
>
>> [!example] Group B
>> n) Continuous values over the fixed unit interval [0, 1).
>> o) Whole-number uniform draws over an interval such as [0, 101), e.g. 50 synthetic grades.
>> p) Gaussian draws parameterized by a chosen mean and sigma.
>> q) Standard normal draws, the building block for feature matrices and Monte Carlo runs.
>> r) Continuous values over a caller-chosen interval [lo, hi), used for parameter sweeps.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)
>> e) -> r)

> [!question] Match the `np.fft` routine with its role in spectral processing.
>> [!example] Group A
>> a) `np.fft.fft2`
>> b) `np.fft.ifft2`
>> c) `np.fft.fftshift`
>
>> [!example] Group B
>> n) Maps a spatial image to its 2D frequency representation.
>> o) Moves the zero-frequency DC term from the corner to the middle of the spectrum.
>> p) Maps the spectrum back to the spatial domain; taking `.real` discards residual imaginary rounding noise.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the `np.linalg` function with the operation it performs.
>> [!example] Group A
>> a) `np.linalg.inv`
>> b) `np.linalg.solve`
>> c) `np.linalg.eig`
>> d) `np.linalg.norm`
>> e) `np.linalg.matrix_rank`
>
>> [!example] Group B
>> n) Computes the unknown $x$ in the system $A x = b$ via LU decomposition.
>> o) Returns values $\lambda$ and vectors $v$ linked by $A v = \lambda v$.
>> p) Returns, for a non-singular matrix, the multiplicative counterpart satisfying $A A^{-1} = I$.
>> q) Computes the Euclidean magnitude as the square root of the sum of squared components.
>> r) Counts the linearly independent rows or columns of a matrix.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)
>> e) -> r)

> [!question] Match the ndarray attribute, reported for a `float64` array of shape (3, 4), with what it measures.
>> [!example] Group A
>> a) `a.ndim`
>> b) `a.shape`
>> c) `a.size`
>> d) `a.itemsize`
>> e) `a.nbytes`
>
>> [!example] Group B
>> n) The number of dimensions, which is 2 here.
>> o) The total bytes of the data buffer, which is 96 here.
>> p) The bytes occupied by one element, which is 8 here.
>> q) The total count of elements, which is 12 here.
>> r) The tuple of lengths along each dimension, which is (3, 4) here.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> r)
>> c) -> q)
>> d) -> p)
>> e) -> o)

> [!question] Match the data replication mechanism with its behavior.
>> [!example] Group A
>> a) `np.tile`
>> b) `np.repeat`
>> c) broadcasting
>> d) `a[None, :]`
>
>> [!example] Group B
>> n) Duplicates each element consecutively, interleaving values, as needed to build kernel columns.
>> o) Copies the entire block a specified number of times along each axis, physically allocating memory.
>> p) Gives a size-1 axis a memory stride of 0 so the data acts as if repeated, with no copying.
>> q) Indexing idiom that introduces a leading size-1 axis so a 1D vector can be combined with a 2D matrix.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)
