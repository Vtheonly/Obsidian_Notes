---
sources:
  - "[[10. Activation Functions in Deep Learning]]"
---
> [!question] Activation functions introduce non-linearity, allowing neural networks to learn complex patterns.
>> [!success]- Answer
>> True

> [!question] Without activation functions, stacking layers would only produce a linear model.
>> [!success]- Answer
>> True

> [!question] The Sigmoid function is the best choice for hidden layers in deep networks.
>> [!success]- Answer
>> False

> [!question] The ReLU activation function has a gradient of 1 for all positive inputs.
>> [!success]- Answer
>> True

> [!question] The 'Dying ReLU' problem occurs when neurons get stuck outputting 0 permanently.
>> [!success]- Answer
>> True

> [!question] Leaky ReLU fixes the Dying ReLU problem by allowing a slight negative slope for negative inputs.
>> [!success]- Answer
>> True

> [!question] Softmax is used in hidden layers to increase model capacity.
>> [!success]- Answer
>> False

> [!question] GELU is heavily used in Transformer architectures like BERT and GPT.
>> [!success]- Answer
>> True

> [!question] Tanh is zero-centered, which is an advantage over Sigmoid for hidden layers.
>> [!success]- Answer
>> True

> [!question] PReLU has a fixed alpha parameter that cannot be learned during training.
>> [!success]- Answer
>> False

> [!question] Which activation function is the industry standard for hidden layers?
> a) Sigmoid
> b) Tanh
> c) ReLU
> d) Softmax
>> [!success]- Answer
>> c) ReLU

> [!question] What is the maximum derivative value of the Sigmoid function?
> a) 1.0
> b) 0.5
> c) 0.25
> d) 2.0
>> [!success]- Answer
>> c) 0.25

> [!question] What activation function should be used for the output layer in binary classification?
> a) ReLU
> b) Sigmoid
> c) Softmax
> d) Tanh
>> [!success]- Answer
>> b) Sigmoid

> [!question] What activation function should be used for the output layer in multi-class classification?
> a) Sigmoid
> b) ReLU
> c) Softmax
> d) Tanh
>> [!success]- Answer
>> c) Softmax

> [!question] What is the 'Dying ReLU' problem?
> a) ReLU outputs are always 1
> b) Neurons output 0 permanently because the gradient is 0 for all negative inputs
> c) ReLU is too slow
> d) ReLU produces negative values
>> [!success]- Answer
>> b) Neurons output 0 permanently because the gradient is 0 for all negative inputs

> [!question] What is the key difference between Leaky ReLU and PReLU?
> a) They have different formulas
> b) Leaky ReLU has a fixed alpha while PReLU learns alpha during training
> c) PReLU cannot be used in hidden layers
> d) Leaky ReLU has a larger range
>> [!success]- Answer
>> b) Leaky ReLU has a fixed alpha while PReLU learns alpha during training

> [!question] Which activation function is smooth and non-monotonic, dipping slightly below zero around x = -1.25?
> a) ReLU
> b) ELU
> c) Swish
> d) Tanh
>> [!success]- Answer
>> c) Swish

> [!question] What is the approximate range of the GELU function?
> a) (0, 1)
> b) (-1, 1)
> c) Approximately (-0.17, +inf)
> d) [0, +inf)
>> [!success]- Answer
>> c) Approximately (-0.17, +inf)

> [!question] Why was ReLU revolutionary for deep learning?
> a) It is the most complex activation function
> b) Its gradient is 1 for positive inputs, solving the vanishing gradient problem
> c) It produces only positive outputs
> d) It uses exponentials
>> [!success]- Answer
>> b) Its gradient is 1 for positive inputs, solving the vanishing gradient problem

> [!question] What activation should be used for the output layer in a regression task?
> a) Sigmoid
> b) Softmax
> c) ReLU
> d) Linear (no activation)
>> [!success]- Answer
>> d) Linear (no activation)

> [!question] Match the activation function with its output range.
>> [!example] Group A
>> a) Sigmoid
>> b) Tanh
>> c) ReLU
>> d) Softmax
>
>> [!example] Group B
>> n) [0, +inf)
>> o) (-1, 1)
>> p) (0, 1) for each output, all sum to 1
>> q) (0, 1)
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the activation function with its primary use.
>> [!example] Group A
>> a) Sigmoid
>> b) Softmax
>> c) ReLU
>> d) GELU
>
>> [!example] Group B
>> n) Hidden layers (industry standard)
>> o) Multi-class classification output layer
>> p) Transformer architectures (BERT, GPT)
>> q) Binary classification output layer
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the activation function with its key problem.
>> [!example] Group A
>> a) Sigmoid
>> b) ReLU
>> c) ELU
>
>> [!example] Group B
>> n) Dying ReLU — neurons stuck at 0
>> o) Slower computation due to exponential for negative inputs
>> p) Vanishing gradient and not zero-centered
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the activation function with its formula.
>> [!example] Group A
>> a) Sigmoid
>> b) ReLU
>> c) Swish
>> d) Leaky ReLU
>
>> [!example] Group B
>> n) max(alpha*x, x) with alpha=0.01
>> o) 1 / (1 + e^{-x})
>> p) x * sigmoid(x)
>> q) max(0, x)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match the activation function variant with its alpha parameter behavior.
>> [!example] Group A
>> a) Leaky ReLU
>> b) PReLU
>
>> [!example] Group B
>> n) Alpha is learned during training via backpropagation
>> o) Alpha is a fixed constant (typically 0.01)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the problem with the activation function that causes it.
>> [!example] Group A
>> a) Vanishing Gradient
>> b) Dying Neurons
>
>> [!example] Group B
>> n) ReLU (gradient is 0 for negative inputs)
>> o) Sigmoid (max derivative is 0.25)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the output layer task with the correct activation.
>> [!example] Group A
>> a) Binary Classification
>> b) Multi-class Classification
>> c) Regression
>
>> [!example] Group B
>> n) Softmax
>> o) Linear (no activation)
>> p) Sigmoid
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the activation function with its special property.
>> [!example] Group A
>> a) Swish
>> b) GELU
>> c) Softmax
>> d) ReLU
>
>> [!example] Group B
>> n) Amplifies differences — largest input gets disproportionate probability
>> o) Probabilistic interpretation using CDF of standard normal
>> p) Creates sparse activations (many zeros)
>> q) Self-gating: sigmoid acts as a gate controlling flow
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the ELU characteristic with its benefit.
>> [!example] Group A
>> a) Smooth negative portion
>> b) Mean activation closer to zero
>
>> [!example] Group B
>> n) Helps gradient-based optimization
>> o) Speeds up learning
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)

> [!question] Match the vanishing gradient scenario with the severity.
>> [!example] Group A
>> a) Sigmoid in 10-layer network
>> b) ReLU in 10-layer network
>
>> [!example] Group B
>> n) Gradient passes through unchanged for positive pathway
>> o) Gradient reduced to approximately 0.00000095 of original
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
