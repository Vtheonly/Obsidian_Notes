---
sources:
  - "[[15. The Vanishing and Exploding Gradient Problems]]"
---
Source: [[15. The Vanishing and Exploding Gradient Problems]]

> [!question] The vanishing and exploding gradient problems arise from the same mathematical mechanism.
>> [!success]- Answer
>> True

> [!question] During backpropagation, the gradient of the loss with respect to weights in an early layer is computed as a sum of terms.
>> [!success]- Answer
>> False

> [!question] The derivative of the sigmoid function has a maximum value of 1.0.
>> [!success]- Answer
>> False

> [!question] In a deep network, if each term in the gradient product is less than one, the product grows exponentially toward infinity.
>> [!success]- Answer
>> False

> [!question] The gradient behavior in deep networks is determined by the interaction between the activation function and the weight magnitude.
>> [!success]- Answer
>> True

> [!question] If each term in the gradient product has magnitude α = 1.2, after 50 layers the gradient will be smaller than its original value.
>> [!success]- Answer
>> False

> [!question] The vanishing gradient problem is only a theoretical concern and doesn't affect practical deep network training.
>> [!success]- Answer
>> False

> [!question] The hyperbolic tangent (tanh) activation function has a maximum derivative of 1.0.
>> [!success]- Answer
>> True

> [!question] In the telephone game analogy, each layer in a neural network corresponds to a person who passes the gradient message.
>> [!success]- Answer
>> True

> [!question] The fundamental equation for gradient computation in a scalar network is ∂ℒ/∂a^(l) = ∂ℒ/∂a^(L) × ∑(k=l+1 to L) f'(z^(k)) × w^(k).
>> [!success]- Answer
>> False

> [!question] What is the primary mechanism that causes both vanishing and exploding gradient problems?
> a) Division by zero during backpropagation
> b) Product of many terms during gradient computation
> c) Non-convexity of the loss function
> d) Insufficient computational resources
>> [!success]- Answer
>> b) Product of many terms during gradient computation

> [!question] What is the maximum value of the derivative of the sigmoid function?
> a) 0.5
> b) 1.0
> c) 0.25
> d) 0.75
>> [!success]- Answer
>> c) 0.25

> [!question] In a 10-layer network using sigmoid activations, what is the gradient after passing through all layers in the best case scenario (each neuron at x=0)?
> a) 0.25
> b) 1/4^10 ≈ 9.5×10^-7
> c) 0.1^10 = 10^-10
> d) 1.0
>> [!success]- Answer
>> b) 1/4^10 ≈ 9.5×10^-7

> [!question] What happens when the gradient passes through a saturated sigmoid activation?
> a) It gets multiplied by a value greater than 1
> b) It gets multiplied by a value close to 0
> c) It remains unchanged
> d) It gets divided by 2
>> [!success]- Answer
>> b) It gets multiplied by a value close to 0

> [!question] What is the consequence of having α = 0.5 in the gradient product after 50 layers?
> a) The gradient becomes extremely large
> b) The gradient becomes approximately 10^-15
> c) The gradient becomes exactly zero
> d) The gradient becomes unstable
>> [!success]- Answer
>> b) The gradient becomes approximately 10^-15

> [!question] What is the primary difference between the vanishing and exploding gradient problems?
> a) Vanishing affects only recurrent networks, while exploding affects only CNNs
> b) Vanishing occurs when each term in the product is less than 1, exploding when each term is greater than 1
> c) Vanishing occurs in shallow networks, exploding in deep networks
> d) Vanishing affects only early layers, exploding affects only late layers
>> [!success]- Answer
>> b) Vanishing occurs when each term in the product is less than 1, exploding when each term is greater than 1

> [!question] Why is the telephone game used as an analogy for gradient flow in deep networks?
> a) Because both involve passing messages through multiple people/layers
> b) Because both result in perfect information preservation
> c) Because both require specialized equipment
> d) Because both are only theoretical constructs
>> [!success]- Answer
>> a) Because both involve passing messages through multiple people/layers

> [!question] What is the relationship between the vanishing gradient problem and weight initialization?
> a) Proper initialization can mitigate the vanishing gradient problem
> b) Proper initialization causes the vanishing gradient problem
> c) The vanishing gradient problem is completely independent of weight initialization
> d) Weight initialization only affects exploding gradients
>> [!success]- Answer
>> a) Proper initialization can mitigate the vanishing gradient problem

> [!question] What is the mathematical form of the gradient of the loss with respect to activations at layer l in a deep feedforward network?
> a) ∂ℒ/∂a^(l) = ∂ℒ/∂a^(L) × ∑(k=l+1 to L) ∂a^(k)/∂a^(k-1)
> b) ∂ℒ/∂a^(l) = ∂ℒ/∂a^(L) × ∏(k=l+1 to L) ∂a^(k)/∂a^(k-1)
> c) ∂ℒ/∂a^(l) = ∂ℒ/∂a^(L) + ∑(k=l+1 to L) ∂a^(k)/∂a^(k-1)
> d) ∂ℒ/∂a^(l) = ∂ℒ/∂a^(L) - ∏(k=l+1 to L) ∂a^(k)/∂a^(k-1)
>> [!success]- Answer
>> b) ∂ℒ/∂a^(l) = ∂ℒ/∂a^(L) × ∏(k=l+1 to L) ∂a^(k)/∂a^(k-1)

> [!question] Match the gradient behavior with its corresponding condition.
>> [!example] Group A
>> a) Vanishing gradient
>> b) Exploding gradient
>> c) Stable gradient
>>
>> [!example] Group B
>> n) |f'(z^(k)) × w^(k)| < 1 for most layers
>> o) |f'(z^(k)) × w^(k)| > 1 for most layers
>> p) |f'(z^(k)) × w^(k)| ≈ 1 for most layers
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the activation function with its derivative property.
>> [!example] Group A
>> a) Sigmoid
>> b) Tanh
>> c) ReLU
>>
>> [!example] Group B
>> n) Maximum derivative of 0.25
>> o) Zero-centered with maximum derivative of 1.0
>> p) Derivative of 1 for positive inputs, 0 for negative inputs
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the gradient magnitude α with its effect after many layers.
>> [!example] Group A
>> a) α = 0.9
>> b) α = 1.1
>> c) α = 1.5
>>
>> [!example] Group B
>> n) Gradient grows exponentially
>> o) Gradient shrinks exponentially but slowly
>> p) Gradient grows very rapidly
>>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the layer position with its gradient behavior in a deep network.
>> [!example] Group A
>> a) Early layers
>> b) Middle layers
>> c) Late layers
>>
>> [!example] Group B
>> n) Receive almost no gradient signal in vanishing gradient scenarios
>> o) Have gradient magnitudes closest to the original gradient
>> p) Experience gradient magnitudes that are intermediate between early and late layers
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the gradient problem with its corresponding consequence.
>> [!example] Group A
>> a) Vanishing gradient
>> b) Exploding gradient
>>
>> [!example] Group B
>> n) Early layers receive no learning signal
>> o) Training becomes unstable with large weight updates
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)

> [!question] Match the network characteristic with its effect on gradient flow.
>> [!example] Group A
>> a) Deep network
>> b) Network with sigmoid activations
>> c) Network with proper initialization
>>
>> [!example] Group B
>> n) Exaggerates both vanishing and exploding gradient problems
>> o) Particularly susceptible to vanishing gradients
>> p) Helps maintain stable gradient magnitudes
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the gradient product term with its effect on overall gradient magnitude.
>> [!example] Group A
>> a) f'(z^(k)) × w^(k) = 0.8
>> b) f'(z^(k)) × w^(k) = 1.2
>> c) f'(z^(k)) × w^(k) = 1.0
>>
>> [!example] Group B
>> n) Contributes to vanishing gradient
>> o) Contributes to exploding gradient
>> p) Maintains gradient magnitude
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the saturation behavior with its corresponding activation function.
>> [!example] Group A
>> a) Positive saturation
>> b) Negative saturation
>> c) No saturation
>>
>> [!example] Group B
>> n) Sigmoid with large positive input
>> o) Sigmoid with large negative input
>> p) ReLU with positive input
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the gradient magnitude with its impact on training.
>> [!example] Group A
>> a) Extremely small gradient (e.g., 10^-15)
>> b) Extremely large gradient (e.g., 10^15)
>> c) Moderate gradient (e.g., 10^-1)
>>
>> [!example] Group B
>> n) Results in numerical instability and potential overflow
>> o) Results in negligible weight updates
>> p) Results in reasonable weight updates
>>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the network component with its role in addressing gradient problems.
>> [!example] Group A
>> a) ReLU activation
>> b) Batch normalization
>> c) Residual connections
>>
>> [!example] Group B
>> n) Prevents saturation by allowing a linear path
>> o) Reduces internal covariate shift, helping maintain gradient magnitudes
>> p) Avoids negative derivatives, reducing vanishing gradient risk
>>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
