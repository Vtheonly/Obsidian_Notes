---
sources:
  - "[[3. The Convolution Operation Deep Dive]]"
---
> [!question] Filters and kernels are always the same size as the input they are applied to.
>> [!success]- Answer
>> False

> [!question] A filter applied to an RGB image with 3 color channels would have dimensions 3×3×3.
>> [!success]- Answer
>> True

> [!question] In signal processing, the terms "filter" and "kernel" have exactly the same meaning.
>> [!success]- Answer
>> False

> [!question] Feature maps are also called activation maps.
>> [!success]- Answer
>> True

> [!question] The values in a filter are typically hand-crafted and fixed during training.
>> [!success]- Answer
>> False

> [!question] Convolution in CNNs can be understood as a sliding dot product operation.
>> [!success]- Answer
>> True

> [!question] When applying multiple filters to the same input, each filter produces a separate feature map.
>> [!success]- Answer
>> True

> [!question] Feature maps highlight where specific patterns appear in the input, with high values indicating strong detection of the pattern.
>> [!success]- Answer
>> True

> [!question] In some frameworks, "kernel" refers to the 2D weight matrix while "filter" refers to the full 3D weight tensor.
>> [!success]- Answer
>> True

> [!question] The size of the output feature map is always the same as the input size.
>> [!success]- Answer
>> False

> [!question] What is the primary purpose of a filter in a convolutional neural network?
> a) To reduce the dimensionality of the input
> b) To extract specific types of features from the input
> c) To normalize the input values
> d) To activate neurons in the next layer
>> [!success]- Answer
>> b) To extract specific types of features from the input

> [!question] What dimensions would a filter have for an RGB image input?
> a) 3×3
> b) 5×5
> c) 3×3×3
> d) 5×5×3
>> [!success]- Answer
>> c) 3×3×3

> [!question] What does a feature map represent in a CNN?
> a) The input to the next layer
> b) The weights learned during training
> c) A 2D array showing the strength of a filter's response at each spatial location
> d) The activation values of all neurons in the network
>> [!success]- Answer
>> c) A 2D array showing the strength of a filter's response at each spatial location

> [!question] What happens when multiple filters are applied to the same input?
> a) They are averaged together
> b) Only the strongest filter's output is kept
> c) Each filter produces a separate feature map
> d) They are concatenated into a single large matrix
>> [!success]- Answer
>> c) Each filter produces a separate feature map

> [!question] How can feature maps be interpreted visually?
> a) As heat maps highlighting where specific patterns appear
> b) As color representations of the input
> c) As probability distributions
> d) As error maps
>> [!success]- Answer
>> a) As heat maps highlighting where specific patterns appear

> [!question] What is the convolution operation best described as?
> a) A sliding average
> b) A sliding dot product
> c) A matrix multiplication
> d) A max operation
>> [!success]- Answer
>> b) A sliding dot product

> [!question] In the context of CNNs, what determines what pattern a filter detects?
> a) The size of the filter
> b) The stride value
> c) The values in the filter
> d) The padding size
>> [!success]- Answer
>> c) The values in the filter

> [!question] What is the output when multiple filters are applied to an input and stacked along the channel dimension?
> a) A 2D array
> b) A 3D output tensor
> c) A 1D vector
> d) A scalar value
>> [!success]- Answer
>> b) A 3D output tensor

> [!question] What is typically the shape of a filter in CNNs?
> a) Always 3×3
> b) Always square (e.g., 3×3, 5×5, 7×7)
> c) Always rectangular
> d) The same as the input shape
>> [!success]- Answer
>> b) Always square (e.g., 3×3, 5×5, 7×7)

> [!question] What happens to filter values during training in a CNN?
> a) They remain fixed as hand-crafted values
> b) They are learned from the data
> c) They are randomly initialized and never updated
> d) They are normalized to a standard range
>> [!success]- Answer
>> b) They are learned from the data

> [!question] Match the terms with their definitions.
>> [!example] Group A
>> a) Filter
>> b) Kernel
>> c) Feature Map
>>
>> [!example] Group B
>> n) A small matrix of learnable weights used to extract features
>> o) The output produced by applying a single filter to the entire input
>> p) Sometimes used interchangeably with "filter" to refer to the weight matrix
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the components with their roles in convolution.
>> [!example] Group A
>> a) Filter values
>> b) Feature map
>> c) Stride
>>
>> [!example] Group B
>> n) Determines what pattern the filter detects
>> o) Shows where a specific feature is present in the input
>> p) Controls how much the filter moves each step
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the characteristics with their descriptions.
>> [!example] Group A
>> a) Vertical edge detection filter
>> b) RGB image input
>> c) Multiple filters applied to same input
>>
>> [!example] Group B
>> n) Produces high values at vertical transitions
>> o) Has 3 channels (red, green, blue)
>> p) Results in multiple feature maps
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the mathematical operations with their effects.
>> [!example] Group A
>> a) Dot product
>> b) Element-wise multiplication
>> c) Summation
>>
>> [!example] Group B
>> n) Combines all products to produce a single output value
>> o) Multiplies corresponding elements of filter and input patch
>> p) Measures similarity between filter and input patch
>>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the interpretations with their visual representations.
>> [!example] Group A
>> a) High values in feature map
>> b) Low values in feature map
>> c) Zero values in feature map
>>
>> [!example] Group B
>> n) Strong detection of pattern at that location
>> o) No significant pattern detected
>> p) Weak or no detection of pattern
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the filter components with their purposes.
>> [!example] Group A
>> a) Filter size
>> b) Filter depth
>> c) Filter values
>>
>> [!example] Group B
>> n) Matches the number of channels in the input
>> o) Determines the spatial extent of the pattern detection
>> p) Determines what specific pattern is detected
>>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the framework conventions with their terminology.
>> [!example] Group A
>> a) Some frameworks
>> b) Most practitioners
>> c) Signal processing
>>
>> [!example] Group B
>> n) Use "filter" and "kernel" interchangeably
>> o) Distinguish between kernel (2D) and filter (3D)
>> p) Have slightly different connotations for filter and kernel
>>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the convolution parameters with their functions.
>> [!example] Group A
>> a) Stride
>> b) Padding
>> c) Number of filters
>>
>> [!example] Group B
>> n) Controls how much the filter moves each step
>> o) Adds extra pixels around the input
>> p) Determines how many different features are extracted
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the input types with their filter dimensions.
>> [!example] Group A
>> a) Grayscale image
>> b) RGB image
>> c) Volume data (e.g., medical scan)
>>
>> [!example] Group B
>> n) 3×3×3
>> o) 3×3×1
>> p) 3×3×D (where D is the depth of the input)
>>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the learning concepts with their descriptions.
>> [!example] Group A
>> a) Hand-crafted features
>> b) Learned features in CNN
>> c) Feature visualization
>>
>> [!example] Group B
>> n) Network discovers useful patterns from data
>> o) Understanding what patterns each filter detects
>> p) Predefined patterns designed by experts
>>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
