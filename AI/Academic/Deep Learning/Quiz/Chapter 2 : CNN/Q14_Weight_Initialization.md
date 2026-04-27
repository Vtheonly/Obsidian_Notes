---
sources:
  - "[[14. Weight Initialization]]"
---
Source: [[14. Weight Initialization]]

> [!question] Proper weight initialization is crucial in deep neural networks because the optimization landscape is non-convex.
>> [!success]- Answer
>> True

> [!question] Setting all weights to zero allows the network to break symmetry and learn different features in each neuron.
>> [!success]- Answer
>> False

> [!question] The symmetry problem in neural networks occurs when all neurons in a layer produce identical outputs and receive identical gradient updates.
>> [!success]- Answer
>> True

> [!question] Initializing all weights to a large constant value can help prevent vanishing gradients in deep networks.
>> [!success]- Answer
>> False

> [!question] In a properly initialized network, different neurons should start with different weight values to break symmetry.
>> [!success]- Answer
>> True

> [!question] All-zero initialization allows each neuron in a layer to learn different features by receiving different gradient updates.
>> [!success]- Answer
>> False

> [!question] The symmetry problem can be solved by using random initialization with different values for each weight.
>> [!success]- Answer
>> True

> [!question] A large constant weight initialization will lead to exponentially growing activations and gradients as they propagate through layers.
>> [!success]- Answer
>> True

> [!question] Well-initialized networks tend to find sharper, more specific minima that generalize better than poorly initialized networks.
>> [!success]- Answer
>> False

> [!question] The initialization point in a neural network determines which region of the loss landscape the optimization process will explore.
>> [!success]- Answer
>> True

> [!question] What is the main problem with initializing all weights to zero in a neural network?
> a) It causes vanishing gradients
> b) It leads to the symmetry problem
> c) It makes the loss function non-convex
> d) It prevents the use of ReLU activation functions
>> [!success]- Answer
>> b) It leads to the symmetry problem

> [!question] Which of the following is a consequence of initializing all weights to large constant values?
> a) Vanishing gradients
> b) Exploding activations and gradients
> c) Increased model capacity
> d) Faster convergence to global minimum
>> [!success]- Answer
>> b) Exploding activations and gradients

> [!question] Why is weight initialization particularly important in deep neural networks?
> a) Because deep networks have more parameters
> b) Because the optimization landscape becomes exponentially more complex with depth
> c) Because deep networks always use ReLU activation functions
> d) Because deep networks require more computational resources
>> [!success]- Answer
>> b) Because the optimization landscape becomes exponentially more complex with depth

> [!question] Which of the following statements about the non-convex nature of neural network loss landscapes is true?
> a) Local minima are guaranteed to be global minima
> b) The number of saddle points decreases with network depth
> c) Initialization determines which region of the landscape is explored
> d) Gradient descent will always converge to the global minimum
>> [!success]- Answer
>> c) Initialization determines which region of the landscape is explored

> [!question] What happens when all neurons in a layer produce identical outputs due to poor initialization?
> a) The network's capacity increases
> b) The layer becomes functionally equivalent to having a single neuron
> c) The training becomes more stable
> d) The gradients become more informative
>> [!success]- Answer
>> b) The layer becomes functionally equivalent to having a single neuron

> [!question] Which initialization problem leads to the loss becoming NaN during training?
> a) Vanishing gradients
> b) Exploding gradients
> c) Symmetry problem
> d) Poor learning rate
>> [!success]- Answer
>> b) Exploding gradients

> [!question] Why is random initialization necessary for breaking symmetry in neural networks?
> a) Random values ensure numerical stability
> b) Different initial values allow neurons to receive different gradient updates
> c) Random initialization reduces computational cost
> d) Random values guarantee convergence to global minimum
>> [!success]- Answer
>> b) Different initial values allow neurons to receive different gradient updates

> [!question] What is a key difference between the effects of zero initialization versus large constant initialization?
> a) Zero initialization causes exploding gradients while large constants cause vanishing gradients
> b) Zero initialization breaks symmetry while large constants maintain it
> c) Zero initialization leads to symmetric neurons while large constants lead to exponential growth
> d) Zero initialization speeds up convergence while large constants slow it down
>> [!success]- Answer
>> c) Zero initialization leads to symmetric neurons while large constants lead to exponential growth

> [!question] Which of the following best describes why initialization affects final model performance?
> a) Different initializations lead to different local minima with varying generalization properties
> b) Initialization determines the learning rate schedule
> c) Proper initialization reduces the number of parameters needed
> d) Initialization only affects convergence speed, not final performance
>> [!success]- Answer
>> a) Different initializations lead to different local minima with varying generalization properties

> [!question] Match the initialization problem with its description.
>> [!example] Group A
>> a) All-zero initialization
>> b) All-large-constant initialization
>> c) Random initialization with improper scaling
>> d) Identical initialization across layers
>
>> [!example] Group B
>> n) Causes neurons to behave identically and prevents learning diverse features
>> o) Leads to exponentially growing activations and gradients
>> p) Results in vanishing gradients in deep networks
>> q) Breaks symmetry but may still cause training instability
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the optimization challenge with its characteristic in deep neural networks.
>> [!example] Group A
>> a) Non-convex loss landscape
>> b) High-dimensional parameter space
>> c) Multiple local minima
>> d) Saddle points
>
>> [!example] Group B
>> n) Regions where gradient is zero but not a minimum
>> o) Exponentially more complex as network depth increases
>> p) Regions where gradient descent may get stuck
>> q) Estimated to have roughly 2^N saddle points for N parameters
>
>> [!success]- Answer
>> a) -> o)
>> b) -> o)
>> c) -> p)
>> d) -> n)

> [!question] Match the initialization strategy with its primary effect on network training.
>> [!example] Group A
>> a) Zero initialization
>> b) Large constant initialization
>> c) Small random initialization
>> d) Xavier/Glorot initialization
>
>> [!example] Group B
>> n) Prevents symmetry but causes gradient explosion
>> o) Maintains neuron diversity but may cause vanishing gradients
>> p) Breaks symmetry but leads to degenerate learning
>> q) Aims to keep activations and gradients in stable ranges
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match the consequence of poor initialization with its impact on training.
>> [!example] Group A
>> a) Symmetry problem
>> b) Exploding gradients
>> c) Vanishing gradients
>> d) Oscillating loss
>
>> [!example] Group B
>> n) Prevents learning from progressing due to near-zero updates
>> o) Causes wild parameter updates without convergence
>> p) Makes all neurons learn identical features
>> q) Results in unstable training with loss spikes
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match the analogy with its corresponding concept in neural network training.
>> [!example] Group A
>> a) Parachute landing point
>> b) Mountain range exploration
>> c) Slope beneath feet
>> d) Walking downhill
>
>> [!example] Group B
>> n) Gradient descent steps
>> o) Weight initialization
>> p) Loss landscape
>> q) Direction of steepest descent
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the initialization strategy with the appropriate scenario for its use.
>> [!example] Group A
>> a) All-zero initialization
>> b) Large constant initialization
>> c) Small random values
>> d) Layer-specific initialization
>
>> [!example] Group B
>> n) Never recommended due to symmetry problem
>> o) Used for specific normalization techniques like batch norm
>> p) Necessary for breaking symmetry in hidden layers
>> q) Applied to prevent layer-specific gradient problems
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the property with its effect on network training dynamics.
>> [!example] Group A
>> a) Well-initialized network
>> b) Poorly-initialized network
>> c) Properly scaled gradients
>> d) Exploding gradients
>
>> [!example] Group B
>> n) Finds wider, more generalizable minima
>> o) May converge to sharp, poorly generalizing minima
>> p) Allows steady progress in gradient descent
>> q) Causes erratic weight updates and instability
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the mathematical concept with its role in weight initialization.
>> [!example] Group A
>> a) Mean
>> b) Variance
>> c) Normal distribution
>> d) Uniform distribution
>
>> [!example] Group B
>> n) Used to ensure weights are centered around zero
>> o) Controls the spread of initial weight values
>> p) Common choice for random weight generation
>> q) Alternative to normal distribution for initialization
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
