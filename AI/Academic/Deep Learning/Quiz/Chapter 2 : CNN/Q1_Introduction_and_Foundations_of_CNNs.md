---
sources:
  - "[[1. Introduction and Foundations of CNNs]]"
---
> [!question] A neural network is a computational model loosely inspired by the way biological neurons in the human brain process information.
>> [!success]- Answer
>> True

> [!question] Without an activation function, a neural network could still learn complex non-linear patterns.
>> [!success]- Answer
>> False

> [!question] The bias in a neuron shifts the entire weighted sum up or down before the activation function is applied.
>> [!success]- Answer
>> True

> [!question] In a neural network, weights determine how much influence each input has on the neuron's output.
>> [!success]- Answer
>> True

> [!question] A single artificial neuron by itself can learn very complex functions without being organized into layers.
>> [!success]- Answer
>> False

> [!question] The ReLU activation function is defined as f(z) = max(0, z).
>> [!success]- Answer
>> True

> [!question] In a fully connected layer, every neuron is connected to every neuron in the previous layer.
>> [!success]- Answer
>> True

> [!question] The input layer of a neural network consists of neurons with learnable parameters.
>> [!success]- Answer
>> False

> [!question] Without non-linearity introduced by activation functions, a neural network would collapse into a single linear transformation regardless of its depth.
>> [!success]- Answer
>> True

> [!question] Hidden layers in a neural network are called "hidden" because their values are directly observed and not learned from data.
>> [!success]- Answer
>> False

> [!question] What is the fundamental building block of every neural network?
> a) Layer
> b) Activation function
> c) Artificial neuron
> d) Weight matrix
>> [!success]- Answer
>> c) Artificial neuron

> [!question] What is the primary purpose of the bias in an artificial neuron?
> a) To determine how much influence each input has
> b) To shift the entire weighted sum before activation
> c) To introduce non-linearity into the network
> d) To normalize the inputs
>> [!success]- Answer
>> b) To shift the entire weighted sum before activation

> [!question] What would happen if you used no activation function in a neural network?
> a) The network would become more powerful
> b) The network would collapse into a single linear transformation
> c) The network would only be able to classify binary problems
> d) The network would require more training data
>> [!success]- Answer
>> b) The network would collapse into a single linear transformation

> [!question] Which of the following is NOT a common type of layer in a neural network?
> a) Input layer
> b) Hidden layer
> c) Output layer
> d) Bias layer
>> [!success]- Answer
>> d) Bias layer

> [!question] In the equation y = f(w⊤x + b), what does the term w⊤x represent?
> a) The activation function
> b) The bias term
> c) The weighted sum of inputs
> d) The final output
>> [!success]- Answer
>> c) The weighted sum of inputs

> [!question] Which activation function is defined as f(z) = 1/(1+e^-z)?
> a) ReLU
> b) Sigmoid
> c) Tanh
> d) Softmax
>> [!success]- Answer
>> b) Sigmoid

> [!question] What is the role of the input layer in a neural network?
> a) It contains neurons with learnable parameters
> b) It processes the raw input data
> c) It makes the final decision or prediction
> d) It normalizes the data before processing
>> [!success]- Answer
>> b) It processes the raw input data

> [!question] Why are hidden layers called "hidden"?
> a) Because they use hidden activation functions
> b) Because their values are not directly observed
> c) Because they are not used during training
> d) Because they are located in the middle of the network
>> [!success]- Answer
>> b) Because their values are not directly observed

> [!question] What is the output of a ReLU activation function when the input is -0.5?
> a) -0.5
> b) 0
> c) 0.5
> d) 1
>> [!success]- Answer
>> b) 0

> [!question] Match the neural network components with their descriptions.
>> [!example] Group A
>> a) Weights
>> b) Bias
>> c) Activation function
>
>> [!example] Group B
>> n) Learnable parameter that determines influence of each input
>> o) Special number that shifts the weighted sum
>> p) Introduces non-linearity into the network
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the activation functions with their mathematical definitions.
>> [!example] Group A
>> a) ReLU
>> b) Sigmoid
>> c) Tanh
>
>> [!example] Group B
>> n) f(z) = max(0, z)
>> o) f(z) = 1/(1+e^-z)
>> p) f(z) = tanh(z)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the types of neural network layers with their characteristics.
>> [!example] Group A
>> a) Input layer
>> b) Hidden layer
>> c) Fully connected layer
>
>> [!example] Group B
>> n) Contains the raw input data
>> o) Internal representations that the network learns
>> p) Every neuron connected to every neuron in previous layer
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following terms with their roles in a neural network.
>> [!example] Group A
>> a) Function approximator
>> b) Linear transformation
>> c) Non-linearity
>
>> [!example] Group B
>> n) What neural networks essentially do
>> o) What a neuron computes without activation
>> p) What gives neural networks their expressive power
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following concepts with their explanations.
>> [!example] Group A
>> a) Excitation
>> b) Inhibition
>> c) Ignored input
>
>> [!example] Group B
>> n) When input has strong positive influence on neuron
>> o) When input has strong negative influence on neuron
>> p) When input has near zero influence on neuron
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following neural network properties with their descriptions.
>> [!example] Group A
>> a) Expressive power
>> b) Decision boundary
>> c) Internal representations
>
>> [!example] Group B
>> n) The ability of a network to learn complex patterns
>> o) The surface that separates different classes
>> p) Hidden layer values that the network learns
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following statements with their truth values in the context of neural networks.
>> [!example] Group A
>> a) Single neuron can learn complex functions
>> b) Without bias, neuron outputs 0 when all inputs are 0
>> c) Activation functions make neural networks linear
>
>> [!example] Group B
>> n) False
>> o) True
>> p) False
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following neural network components with their mathematical representations.
>> [!example] Group A
>> a) Weighted sum
>> b) Bias term
>> c) Activation output
>
>> [!example] Group B
>> n) ∑wi*xi
>> o) b
>> p) f(w⊤x + b)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following layer types with their positions in a typical neural network.
>> [!example] Group A
>> a) Input layer
>> b) Hidden layer
>> c) Output layer
>
>> [!example] Group B
>> n) First layer that receives raw data
>> o) Middle layers between input and output
>> p) Final layer that produces predictions
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following neural network concepts with their purposes.
>> [!example] Group A
>> a) Weights
>> b) Biases
>> c) Activation functions
>
>> [!example] Group B
>> n) Determine influence of each input
>> o) Shift the decision boundary
>> p) Enable learning of complex patterns
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
