---
sources:
  - "[[10. Inception Architecture Deep Dive]]"
---
> [!question] A single filter size is optimal for capturing all types of visual information in an image.
>> [!success]- Answer
>> False

> [!question] Inception architecture was introduced in 2014 by Szegedy et al.
>> [!success]- Answer
>> True

> [!question] The naive Inception module processes input through multiple parallel branches with different filter sizes.
>> [!success]- Answer
>> True

> [!question] A 7×7 filter is ideal for capturing fine-grained textures in images.
>> [!success]- Answer
>> False

> [!question] The Inception module concatenates results from different branches along the channel dimension.
>> [!success]- Answer
>> True

> [!question] Deeper layers in a CNN accumulate increasingly large receptive fields.
>> [!success]- Answer
>> True

> [!question] The 1×1 convolution branch in Inception is primarily used for capturing global context.
>> [!success]- Answer
>> False

> [!question] The naive Inception module includes branches with 1×1, 3×3, and 5×5 convolutions.
>> [!success]- Answer
>> True

> [!question] Pooling layers in CNNs increase spatial resolution.
>> [!success]- Answer
>> False

> [!question] The choice of filter size in a convolutional layer commits the entire layer to looking at input through a single spatial window.
>> [!success]- Answer
>> True

> [!question] What is the fundamental tension that Inception architecture addresses?
> a) Computational efficiency
> b) Memory usage
> c) Committing to a single filter size
> d) Network depth
>> [!success]- Answer
>> c) Committing to a single filter size

> [!question] Which filter size is ideal for capturing fine-grained textures in images?
> a) 7×7
> b) 5×5
> c) 3×3
> d) 1×1
>> [!success]- Answer
>> d) 1×1

> [!question] What is the primary purpose of the 1×1 convolution branch in Inception?
> a) Capturing global context
> b) Reducing computational cost
> c) Capturing pixel-level patterns
> d) Increasing spatial resolution
>> [!success]- Answer
>> c) Capturing pixel-level patterns

> [!question] What happens to the results of different branches in the naive Inception module?
> a) They are averaged
> b) They are concatenated along the channel dimension
> c) They are max-pooled
> d) They are element-wise multiplied
>> [!success]- Answer
>> b) They are concatenated along the channel dimension

> [!question] Which of the following is NOT a benefit of multi-scale processing in Inception?
> a) Capturing information at different spatial scales
> b) Reducing network parameters
> c) Avoiding the need to choose a single filter size
> d) Preserving all information from different scales
>> [!success]- Answer
>> b) Reducing network parameters

> [!question] What is the role of the 3×3 convolution branch in Inception?
> a) Capturing global context
> b) Capturing local spatial structures
> c) Reducing channel dimensions
> d) Increasing spatial resolution
>> [!success]- Answer
>> b) Capturing local spatial structures

> [!question] What is the core insight of the Inception architecture?
> a) Using only 1×1 convolutions
> b) Multi-scale parallel processing within a single layer
> c) Increasing network depth
> d) Using only large filter sizes
>> [!success]- Answer
>> b) Multi-scale parallel processing within a single layer

> [!question] What does concatenation in the Inception module preserve?
> a) Spatial resolution
> b) All information from different scales
> c) Computational efficiency
> d) Network depth
>> [!success]- Answer
>> b) All information from different scales

> [!question] What is the primary limitation addressed by the Inception architecture?
> a) Overfitting
> b) The need to commit to a single filter size
> c) Vanishing gradients
> d) Computational complexity
>> [!success]- Answer
>> b) The need to commit to a single filter size

> [!question] Match the filter sizes to their primary use cases in CNNs.
>> [!example] Filter Sizes
>> a) 1×1
>> b) 3×3
>> c) 5×5
>
>> [!example] Use Cases
>> n) Capturing fine-grained textures
>> o) Capturing local object parts
>> p) Capturing global context
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the branches of the naive Inception module to their descriptions.
>> [!example] Branches
>> a) 1×1 Convolution
>> b) 3×3 Convolution
>> c) 5×5 Convolution
>
>> [!example] Descriptions
>> n) Captures pixel-level patterns without spatial context
>> o) Captures local spatial structures and medium-scale patterns
>> p) Captures larger spatial context and relationships
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the types of visual information to their appropriate filter sizes.
>> [!example] Information Types
>> a) Textures
>> b) Object parts
>> c) Global context
>
>> [!example] Filter Sizes
>> n) 1×1 or 3×3
>> o) 3×3 or 5×5
>> p) 5×5 or larger
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the components of CNNs to their functions.
>> [!example] Components
>> a) Convolutional layers
>> b) Pooling layers
>> c) Fully connected layers
>
>> [!example] Functions
>> n) Reducing spatial dimensions
>> o) Extracting features through filters
>> p) Final classification based on extracted features
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the concepts related to Inception architecture to their definitions.
>> [!example] Concepts
>> a) Multi-scale processing
>> b) Concatenation
>> c) Receptive field
>
>> [!example] Definitions
>> n) The area of input that affects a particular feature
>> o) Combining outputs from different branches
>> p) Processing data through multiple filter sizes simultaneously
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the filter operations to their effects on feature maps.
>> [!example] Operations
>> a) 1×1 convolution
>> b) 3×3 convolution with stride 2
>> c) 3×3 max pooling
>
>> [!example] Effects
>> n) Reduces spatial dimensions by half
>> o) Changes channel dimensions without spatial context
>> p) Captures local features while reducing spatial dimensions
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the network design considerations to their implications.
>> [!example] Considerations
>> a) Filter size selection
>> b) Network depth
>> c) Channel dimensions
>
>> [!example] Implications
>> n) Affects computational cost and memory usage
>> o) Determines what spatial scales can be captured
>> p) Influences receptive field size and feature hierarchy
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Inception module components to their roles in the architecture.
>> [!example] Components
>> a) Parallel branches
>> b) Concatenation
>> c) Subsequent layers
>
>> [!example] Roles
>> n) Aggregates multi-scale results
>> o) Processes input through different filter sizes
>> p) Learns to weight different-scale features
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the CNN concepts to their descriptions.
>> [!example] Concepts
>> a) Receptive field
>> b) Stride
>> c) Padding
>
>> [!example] Descriptions
>> n) Controls how much the filter moves each step
>> o) Adds border values to maintain spatial dimensions
>> p) The region of input that contributes to a feature
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the visual scales to their characteristics in CNN feature extraction.
>> [!example] Scales
>> a) Fine-grained
>> b) Medium
>> c) Coarse
>
>> [!example] Characteristics
>> n) Requires large receptive fields
>> o) Requires small to medium receptive fields
>> p) Requires very small receptive fields
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
