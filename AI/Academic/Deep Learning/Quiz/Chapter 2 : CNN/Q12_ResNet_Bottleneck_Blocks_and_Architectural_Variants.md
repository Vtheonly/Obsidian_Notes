---
sources:
  - "[[12. ResNet Bottleneck Blocks and Architectural Variants]]"
---
> [!question] ResNet comes in five standard variants where the number indicates the total count of weighted layers.
>> [!success]- Answer
>> True

> [!question] The Basic Block is used in ResNet-50, ResNet-101, and ResNet-152.
>> [!success]- Answer
>> False

> [!question] The Bottleneck Block contains three layers arranged in a 1×1 → 3×3 → 1×1 pattern.
>> [!success]- Answer
>> True

> [!question] The first 1×1 convolution in a Bottleneck Block expands the channel count.
>> [!success]- Answer
>> False

> [!question] The Basic Block is more computationally expensive than the Bottleneck Block for deep networks with high channel counts.
>> [!success]- Answer
>> True

> [!question] ResNet-18 uses the Bottleneck Block design.
>> [!success]- Answer
>> False

> [!question] The parameter count for a 3×3 convolution with 64 input and output channels is 36,864.
>> [!success]- Answer
>> True

> [!question] In a Basic Block, the skip connection directly adds the input to the output after the second batch normalization.
>> [!success]- Answer
>> True

> [!question] The "reduce-operate-expand" principle is unique to the Bottleneck Block and not used in other architectures.
>> [!success]- Answer
>> False

> [!question] A Basic Block operating on 512 channels would require over 4.7 million parameters.
>> [!success]- Answer
>> True

> [!question] Which ResNet variants use the Basic Block?
> a) ResNet-18 and ResNet-34
> b) ResNet-50 and ResNet-101
> c) ResNet-34 and ResNet-50
> d) ResNet-18 and ResNet-152
>> [!success]- Answer
>> a) ResNet-18 and ResNet-34

> [!question] What is the primary architectural difference between ResNet variants?
> a) The type of residual block used
> b) The stride value in convolutions
> c) The activation function
> d) The pooling method
>> [!success]- Answer
>> a) The type of residual block used

> [!question] In a Bottleneck Block, what is the purpose of the first 1×1 convolution?
> a) To expand the channel count
> b) To reduce the channel count
> c) To change the spatial dimensions
> d) To add non-linearity
>> [!success]- Answer
>> b) To reduce the channel count

> [!question] Why is the Bottleneck Block used in deeper ResNet variants?
> a) It reduces the number of parameters
> b) It decreases computational cost while maintaining output dimensionality
> c) It improves gradient flow
> d) It reduces memory usage
>> [!success]- Answer
>> b) It decreases computational cost while maintaining output dimensionality

> [!question] What is the parameter count for a Basic Block operating on 64-channel feature maps?
> a) 36,864
> b) 73,728
> c) 147,456
> d) 294,912
>> [!success]- Answer
>> b) 73,728

> [!question] What architectural principle is shared between the Bottleneck Block and the Inception module?
> a) Skip connections
> b) Batch normalization
> c) Reduce-operate-expand
> d) Depthwise separable convolutions
>> [!success]- Answer
>> c) Reduce-operate-expand

> [!question] In a Basic Block, what comes after each 3×3 convolution?
> a) Activation function only
> b) Batch normalization only
> c) Batch normalization followed by ReLU activation
> d) ReLU activation followed by batch normalization
>> [!success]- Answer
>> c) Batch normalization followed by ReLU activation

> [!question] Why are convolutional biases not counted in the parameter calculation when batch normalization is used?
> a) They are set to zero
> b) They are redundant due to batch normalization's learnable bias
> c) They are automatically disabled
> d) They are included in the batch normalization parameters
>> [!success]- Answer
>> b) They are redundant due to batch normalization's learnable bias

> [!question] What is the output dimensionality of a Bottleneck Block compared to its input?
> a) Reduced
> b) Expanded
> c) The same
> d) Depends on the stride
>> [!success]- Answer
>> c) The same

> [!question] Match the ResNet variant with its block type.
>> [!example] ResNet Variants
>> a) ResNet-18
>> b) ResNet-50
>> c) ResNet-152
>>
>> [!example] Block Types
>> n) Basic Block
>> o) Bottleneck Block
>> p) Hybrid Block
>> 
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> o)

> [!question] Match the components of a Basic Block with their descriptions.
>> [!example] Components
>> a) 3×3 Convolution
>> b) Batch Normalization
>> c) Skip Connection
>>
>> [!example] Descriptions
>> n) Adds the input directly to the output
>> o) Normalizes activations after convolution
>> p) Performs spatial feature extraction
>> 
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the layers in a Bottleneck Block with their functions.
>> [!example] Layers
>> a) First 1×1 Convolution
>> b) 3×3 Convolution
>> c) Second 1×1 Convolution
>>
>> [!example] Functions
>> n) Expands channel count back to original size
>> o) Performs spatial feature extraction on compressed representation
>> p) Reduces channel count (compression)
>> 
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the ResNet stages with their typical channel counts.
>> [!example] Stages
>> a) First stage
>> b) Middle stages
>> c) Final stage
>>
>> [!example] Channel Counts
>> n) 64 channels
>> o) 128-256 channels
>> p) 512 channels
>> 
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the architectural elements with their computational impact.
>> [!example] Elements
>> a) Two 3×3 convolutions in Basic Block
>> b) 1×1 → 3×3 → 1×1 sequence in Bottleneck
>> c) High channel counts (512+)
>>
>> [!example] Impact
>> n) High computational cost with large channel counts
>> o) Reduced computational cost through compression
>> p) Manageable cost with small channel counts
>> 
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the concepts with their definitions.
>> [!example] Concepts
>> a) Degradation Problem
>> b) Residual Learning
>> c) Projection Shortcut
>>
>> [!example] Definitions
>> n) Using a 1×1 convolution to match dimensions when skip connection changes them
>> o) Learning the difference between input and output rather than the desired output directly
>> p) Deep networks' performance decreasing with added layers
>> 
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the optimization techniques with their benefits in ResNet.
>> [!example] Techniques
>> a) Bottleneck Design
>> b) Batch Normalization
>> c) Skip Connections
>>
>> [!example] Benefits
>> n) Mitigates vanishing gradients
>> o) Normalizes layer inputs, stabilizing training
>> p) Reduces computational cost for deep networks
>> 
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the residual block components with their order of operation.
>> [!example] Components
>> a) Input
>> b) Convolutions with BN and ReLU
>> c) Addition and Final ReLU
>>
>> [!example] Order
>> n) First operation in block
>> o) Middle operation in block
>> p) Final operation in block
>> 
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the ResNet variants with their typical use cases.
>> [!example] Variants
>> a) ResNet-18/34
>> b) ResNet-50
>> c) ResNet-101/152
>>
>> [!example] Use Cases
>> n) Very deep networks requiring high capacity
>> o) Balanced performance and efficiency
>> p) Limited computational resources
>> 
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
