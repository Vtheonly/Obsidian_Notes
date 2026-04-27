---
sources:
  - "[[6. Advanced Pooling Mechanisms and Global Average Pooling]]"
---
> [!question] Pooling layers are among the most philosophically important components in convolutional neural networks.
>> [!success]- Answer
>> True

> [!question] Max pooling selects the single most activated neuron in each pooling region.
>> [!success]- Answer
>> True

> [!question] Average pooling preserves the sharpest features while discarding surrounding context.
>> [!success]- Answer
>> False

> [!question] The number of channels remains unchanged after a pooling operation.
>> [!success]- Answer
>> True

> [!question] During backpropagation for max pooling, the gradient flows only through the position of the maximum value.
>> [!success]- Answer
>> True

> [!question] Max pooling produces a wider dynamic range compared to average pooling.
>> [!success]- Answer
>> True

> [!question] Average pooling computes a smoothed summary of each region.
>> [!success]- Answer
>> True

> [!question] Max pooling is equivalent to a logical OR-like operation.
>> [!success]- Answer
>> True

> [!question] The choice of pooling mechanism does not influence a network's parameter efficiency.
>> [!success]- Answer
>> False

> [!question] Pooling layers are only used for downsampling in CNNs.
>> [!success]- Answer
>> False

> [!question] What is the primary function of pooling layers in CNNs?
> a) Increasing the number of channels
> b) Spatial aggregation
> c) Adding non-linearity
> d) Reducing computational complexity
>> [!success]- Answer
>> b) Spatial aggregation

> [!question] Given a 4×4 feature map and a 2×2 max pooling kernel with stride 2, what is the resulting output size?
> a) 2×2
> b) 4×4
> c) 3×3
> d) 2×4
>> [!success]- Answer
>> a) 2×2

> [!question] In the provided max pooling example, what value appears in the bottom-right position of the output?
> a) 4
> b) 8
> c) 7
> d) 5
>> [!success]- Answer
>> b) 8

> [!question] How does backpropagation work for average pooling?
> a) Gradient flows only through the maximum value
> b) Gradient is distributed equally to all positions
> c) No gradient is propagated
> d) Gradient is multiplied by the average value
>> [!success]- Answer
>> b) Gradient is distributed equally to all positions

> [!question] What is the key difference between max pooling and average pooling in terms of information preservation?
> a) Max pooling retains overall activation while average pooling preserves sharp features
> b) Max pooling preserves sharp features while average pooling retains overall activation
> c) Both preserve the same type of information
> d) Neither preserves any information
>> [!success]- Answer
>> b) Max pooling preserves sharp features while average pooling retains overall activation

> [!question] What does max pooling amplify?
> a) The weakest activations
> b) The average activation
> c) The strongest activations
> d) The background noise
>> [!success]- Answer
>> c) The strongest activations

> [!question] How does average pooling affect the dynamic range compared to max pooling?
> a) It increases the dynamic range
> b) It decreases the dynamic range
> c) It maintains the same dynamic range
> d) It eliminates the dynamic range
>> [!success]- Answer
>> b) It decreases the dynamic range

> [!question] What does the provided text suggest about max pooling for classification tasks?
> a) The spatial extent of features is more important than their presence
> b) The mere presence of a feature is often more important than its spatial extent
> c) Both spatial extent and presence are equally important
> d) Neither spatial extent nor presence matters in classification
>> [!success]- Answer
>> b) The mere presence of a feature is often more important than its spatial extent

> [!question] Match the pooling mechanisms with their characteristics.
>> [!example] Pooling Mechanisms
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Average Pooling
>
>> [!example] Characteristics
>> n) Preserves the sharpest features
>> o) Computes a smoothed summary of each region
>> p) Reduces each feature map to a single number
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the pooling operations with their gradient propagation methods.
>> [!example] Pooling Operations
>> a) Max Pooling
>> b) Average Pooling
>> c) Strided Convolution
>
>> [!example] Gradient Propagation
>> n) Flows only through the maximum value position
>> o) Distributed equally to all positions in the window
>> p) Propagated through all positions in the kernel
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the pooling types with their effects on feature maps.
>> [!example] Pooling Types
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Average Pooling
>
>> [!example] Effects
>> n) Amplifies the strongest activations
>> o) Dampens activations toward the mean
>> p) Completely removes spatial information
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the pooling mechanisms with their computational properties.
>> [!example] Pooling Mechanisms
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Average Pooling
>
>> [!example] Properties
>> n) Parameter-free operation
>> o) Reduces spatial dimensions while preserving channel count
>> p) Reduces each channel to a single value
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the pooling operations with their use cases.
>> [!example] Pooling Operations
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Average Pooling
>
>> [!example] Use Cases
>> n) Tasks where feature presence is more important than location
>> o) Tasks requiring smooth feature representations
>> p) Final layers before classification in modern CNNs
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the pooling mechanisms with their mathematical operations.
>> [!example] Pooling Mechanisms
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Average Pooling
>
>> [!example] Operations
>> n) Takes the maximum value in each pooling window
>> o) Computes the arithmetic mean of all values in the feature map
>> p) Computes the mean of all values in each pooling window
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the pooling types with their sensitivity to spatial transformations.
>> [!example] Pooling Types
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Average Pooling
>
>> [!example] Sensitivity
>> n) More sensitive to small translations
>> o) Less sensitive to small translations
>> p) Most invariant to spatial transformations
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the pooling operations with their effects on dynamic range.
>> [!example] Pooling Operations
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Average Pooling
>
>> [!example] Effects
>> n) Wider dynamic range
>> o) Narrower dynamic range
>> p) Single value per channel
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the pooling mechanisms with their philosophical interpretations.
>> [!example] Pooling Mechanisms
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Average Pooling
>
>> [!example] Interpretations
>> n) "Is there any evidence of this feature in this region?"
>> o) "How much of this feature exists on average in this region?"
>> p) "What is the overall activation of this feature?"
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the pooling types with their historical development.
>> [!example] Pooling Types
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Average Pooling
>
>> [!example] Development
>> n) Early CNN component
>> o) Also early but less commonly used initially
>> p) Later development that changed modern CNN design
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
