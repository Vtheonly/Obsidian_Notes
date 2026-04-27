---
sources:
  - "[[4. The Mathematics of Receptive Fields and 1x1 Convolutions]]"
---
> [!question] The receptive field of a neuron in a CNN is the region of the input image that influences the output of that neuron.
>> [!success]- Answer
>> True

> [!question] A neuron with a small receptive field captures coarse-grained, global patterns.
>> [!success]- Answer
>> False

> [!question] A neuron in the first convolutional layer with 3×3 filters has a receptive field of exactly 3×3.
>> [!success]- Answer
>> True

> [!question] The receptive field size decreases as we go deeper into the network.
>> [!success]- Answer
>> False

> [!question] Early layers in a CNN detect objects and scenes due to their large receptive fields.
>> [!success]- Answer
>> False

> [!question] The jump (effective stride) at layer L is computed as j_L = j_{L-1} × S_L.
>> [!success]- Answer
>> True

> [!question] The receptive field size R_L at layer L is computed as R_L = R_{L-1} + (K_L - 1) × j_{L-1}.
>> [!success]- Answer
>> True

> [!question] The base case for jump calculation is j_0 = 1.
>> [!success]- Answer
>> True

> [!question] The receptive field size in the second convolutional layer with 3×3 filters is 3×3, same as the first layer.
>> [!success]- Answer
>> False

> [!question] The Window Analogy compares the receptive field to a window through which a neuron looks at the input image.
>> [!success]- Answer
>> True

> [!question] What is the receptive field of a neuron in the first convolutional layer that uses 3×3 filters?
> a) 1×1
> b) 3×3
> c) 5×5
> d) 7×7
>> [!success]- Answer
>> b) 3×3

> [!question] If a neuron in the second convolutional layer (also using 3×3 filters) has a receptive field of 5×5, what is the receptive field size in terms of the original input?
> a) 3×3
> b) 5×5
> c) 7×7
> d) 9×9
>> [!success]- Answer
>> b) 5×5

> [!question] Which of the following statements about receptive fields is correct?
> a) Neurons in early layers have larger receptive fields than those in later layers
> b) Neurons in later layers have larger receptive fields than those in early layers
> c) All neurons in a CNN have the same receptive field size
> d) Receptive field size decreases with network depth
>> [!success]- Answer
>> b) Neurons in later layers have larger receptive fields than those in early layers

> [!question] What does the jump (effective stride) at layer L represent?
> a) The size of the kernel at layer L
> b) The distance in the original input image between two adjacent pixels in the feature map at layer L
> c) The number of layers in the network
> d) The padding size at layer L
>> [!success]- Answer
>> b) The distance in the original input image between two adjacent pixels in the feature map at layer L

> [!question] If the first layer has a stride of 1, what is the jump at layer 1?
> a) 0
> b) 1
> c) 2
> d) 3
>> [!success]- Answer
>> b) 1

> [!question] What is the base case for receptive field size calculation?
> a) R_0 = 0
> b) R_0 = 1
> c) R_0 = K_0
> d) R_0 = S_0
>> [!success]- Answer
>> b) R_0 = 1

> [!question] If layer 3 has a stride of 2, and the jump at layer 2 is 1, what is the jump at layer 3?
> a) 1
> b) 2
> c) 3
> d) 4
>> [!success]- Answer
>> b) 2

> [!question] What happens to the receptive field when we add a new convolutional layer with 3×3 filters and stride 1?
> a) It decreases by 2 pixels
> b) It increases by 2 pixels
> c) It remains the same
> d) It doubles in size
>> [!success]- Answer
>> b) It increases by 2 pixels

> [!question] Match the receptive field sizes with their corresponding layer descriptions in a typical CNN.
>> [!example] Receptive Field Sizes
>> a) 3×3
>> b) 5×5
>> c) 7×7
>> d) 15×15
>
>> [!example] Layer Descriptions
>> n) First convolutional layer with 3×3 filters
>> o) Second convolutional layer with 3×3 filters
>> p) Third convolutional layer with 3×3 filters and stride 2
>> q) Deep layer in a network with multiple 3×3 layers
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the mathematical formulas with their descriptions.
>> [!example] Formulas
>> a) j_L = j_{L-1} × S_L
>> b) R_L = R_{L-1} + (K_L - 1) × j_{L-1}
>> c) R_0 = 1
>> d) j_0 = 1
>
>> [!example] Descriptions
>> n) Base case for receptive field size calculation
>> o) Base case for jump calculation
>> p) Formula for computing jump at layer L
>> q) Formula for computing receptive field size at layer L
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the layer properties with their effects on receptive field.
>> [!example] Layer Properties
>> a) Larger kernel size
>> b) Larger stride
>> c) More layers
>> d) Smaller padding
>
>> [!example] Effects
>> n) Increases receptive field size
>> o) Increases effective stride (jump)
>> p) Decreases feature map resolution
>> q) Has minimal effect on receptive field size
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match the concepts with their intuitive explanations.
>> [!example] Concepts
>> a) Receptive field
>> b) Jump (effective stride)
>> c) Window analogy
>> d) Base case
>
>> [!example] Explanations
>> n) Distance between adjacent pixels in the original input image
>> o) A neuron's view of the input image as a window
>> p) The starting point of calculations (R_0 = 1, j_0 = 1)
>> q) Region of input that influences a neuron's output
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)

> [!question] Match the network layer characteristics with their receptive field calculations.
>> [!example] Layer Characteristics
>> a) First layer: 3×3 kernel, stride 1
>> b) Second layer: 3×3 kernel, stride 1
>> c) Third layer: 3×3 kernel, stride 2
>> d) Fourth layer: 3×3 kernel, stride 1
>
>> [!example] Receptive Field Calculations
>> n) R = 3, j = 1
>> o) R = 5, j = 1
>> p) R = 7, j = 2
>> q) R = 9, j = 2
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the statements about receptive fields with their correctness.
>> [!example] Statements
>> a) Neurons with small receptive fields capture fine-grained details
>> b) Receptive field size decreases with network depth
>> c) The jump represents the stride between adjacent pixels in the original input
>> d) Base case for jump is j_0 = 1
>
>> [!example] Correctness
>> n) True
>> o) False
>> p) True
>> q) False
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> n)
