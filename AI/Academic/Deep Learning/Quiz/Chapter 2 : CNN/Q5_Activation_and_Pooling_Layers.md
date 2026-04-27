---
sources:
  - "[[5. Activation and Pooling Layers]]"
---
Source: [[5. Activation and Pooling Layers]]

> [!question] Without non-linear activation functions, a neural network with multiple layers can only represent linear transformations.
>> [!success]- Answer
>> True

> [!question] The composition of multiple linear layers in a neural network is equivalent to a single linear layer.
>> [!success]- Answer
>> True

> [!question] ReLU is differentiable at x = 0.
>> [!success]- Answer
>> False

> [!question] ReLU solves the vanishing gradient problem for all inputs.
>> [!success]- Answer
>> False

> [!question] In a neural network without non-linear activations, the network can learn the XOR function regardless of its depth.
>> [!success]- Answer
>> False

> [!question] The dying ReLU problem occurs when a neuron's weights are updated such that its pre-activation value is negative for all training examples.
>> [!success]- Answer
>> True

> [!question] Leaky ReLU introduces a hyperparameter α that must be chosen for negative inputs.
>> [!success]- Answer
>> True

> [!question] ReLU saturates for large positive inputs, causing the gradient to approach zero.
>> [!success]- Answer
>> False

> [!question] The computational cost of ReLU is higher than sigmoid due to the comparison operation.
>> [!success]- Answer
>> False

> [!question] PReLU generalizes Leaky ReLU by making the negative slope a learnable parameter.
>> [!success]- Answer
>> True

> [!question] What happens when you stack multiple linear layers in a neural network without any activation functions?
> a) The network becomes more expressive and can learn non-linear functions
> b) The network is equivalent to a single linear transformation
> c) The network cannot learn anything
> d) The network requires more training data to converge
>> [!success]- Answer
>> b) The network is equivalent to a single linear transformation

> [!question] Which of the following statements about ReLU is correct?
> a) ReLU is differentiable everywhere including at x = 0
> b) ReLU outputs zero for all positive inputs
> c) ReLU has a constant gradient of 1 for all positive inputs
> d) ReLU can cause the vanishing gradient problem for positive inputs
>> [!success]- Answer
>> c) ReLU has a constant gradient of 1 for all positive inputs

> [!question] What is the main advantage of using ReLU over sigmoid or tanh activation functions?
> a) ReLU has a smoother curve which helps in optimization
> b) ReLU is computationally more expensive but provides better gradients
> c) ReLU avoids the vanishing gradient problem for positive inputs
> d) ReLU can output negative values which helps in better feature representation
>> [!success]- Answer
>> c) ReLU avoids the vanishing gradient problem for positive inputs

> [!question] Which problem does Leaky ReLU specifically address compared to standard ReLU?
> a) The computational cost of the activation function
> b) The vanishing gradient problem for all inputs
> c) The dying ReLU problem
> d) The saturation problem for large inputs
>> [!success]- Answer
>> c) The dying ReLU problem

> [!question] What happens during the "dying ReLU" problem?
> a) The neuron outputs positive values for all inputs
> b) The neuron's gradient becomes too large causing instability
> c) The neuron outputs zero for all inputs and stops learning
> d) The neuron's weights become undefined
>> [!success]- Answer
>> c) The neuron outputs zero for all inputs and stops learning

> [!question] Which activation function would you expect to have the highest computational cost in a large neural network?
> a) ReLU
> b) Leaky ReLU
> c) Sigmoid
> d) PReLU
>> [!success]- Answer
>> c) Sigmoid

> [!question] How does ReLU contribute to sparsity in neural networks?
> a) By setting all negative values to zero
> b) By setting all positive values to zero
> c) By normalizing all inputs to a standard range
> d) By randomly dropping neurons during training
>> [!success]- Answer
>> a) By setting all negative values to zero

> [!question] Which of the following is NOT a benefit of using ReLU activation functions?
> a) It helps with the vanishing gradient problem
> b) It is computationally efficient
> c) It prevents neurons from dying during training
> d) It maintains strong gradient signals for positive inputs
>> [!success]- Answer
>> c) It prevents neurons from dying during training

> [!question] What is the derivative of ReLU for x > 0?
> a) 0
> b) 1
> c) x
> d) e^x
>> [!success]- Answer
>> b) 1

> [!question] Match the activation function with its key characteristic.
>> [!example] Group A
>> a) ReLU
>> b) Leaky ReLU
>> c) Sigmoid
>
>> [!example] Group B
>> n) Has a small positive slope for negative inputs
>> o) Outputs values between 0 and 1
>> p) Has a constant gradient of 1 for positive inputs
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the neural network concept with its description.
>> [!example] Group A
>> a) Vanishing gradient problem
>> b) Dying ReLU
>> c) Linear transformation collapse
>
>> [!example] Group B
>> n) Occurs when gradients become extremely small in early layers
>> o) Multiple linear layers equivalent to a single linear layer
>> p) Neuron outputs zero for all inputs and stops learning
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the pooling operation with its effect on feature maps.
>> [!example] Group A
>> a) Max pooling
>> b) Average pooling
>> c) Global pooling
>
>> [!example] Group B
>> n) Reduces each feature map to a single value
>> o) Takes the maximum value in each region
>> p) Takes the average value in each region
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the ReLU variant with its mathematical definition.
>> [!example] Group A
>> a) Standard ReLU
>> b) Leaky ReLU
>> c) PReLU
>
>> [!example] Group B
>> n) f(x) = max(0, x)
>> o) f(x) = x if x > 0, αx if x ≤ 0 (α is learnable)
>> p) f(x) = x if x > 0, αx if x ≤ 0 (α is fixed)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the problem with its solution in deep learning.
>> [!example] Group A
>> a) Vanishing gradients
>> b) Dying neurons
>> c) Linear separability limitation
>
>> [!example] Group B
>> n) Non-linear activation functions
>> o) Leaky ReLU variants
>> p) Network depth with proper initialization
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the property with its corresponding activation function.
>> [!example] Group A
>> a) Saturation for large inputs
>> b) Zero-centered outputs
>> c) Piecewise linear
>
>> [!example] Group B
>> n) ReLU
>> o) Sigmoid
>> p) Tanh
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the computational aspect with its description in neural networks.
>> [!example] Group A
>> a) Forward pass computation
>> b) Backward pass computation
>> c) Parameter updates
>
>> [!example] Group B
>> n) Involves gradient calculation and chain rule
>> o) Involves matrix multiplication and activation functions
>> p) Involves weight adjustments based on gradients
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the neural network component with its primary function.
>> [!example] Group A
>> a) Activation functions
>> b) Pooling layers
>> c) Fully connected layers
>
>> [!example] Group B
>> n) Reduces spatial dimensions while preserving important features
>> o) Introduces non-linearity to the network
>> p) Learns global patterns and combines features
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the optimization challenge with its characteristic behavior.
>> [!example] Group A
>> a) Exploding gradients
>> b) Vanishing gradients
>> c) Dead neurons
>
>> [!example] Group B
>> n) Gradients become too large causing unstable updates
>> o) Gradients become extremely small halting learning
>> p) Neurons consistently output zero regardless of input
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
