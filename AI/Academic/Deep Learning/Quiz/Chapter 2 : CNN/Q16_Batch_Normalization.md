---
sources:
  - "[[16. Batch Normalization]]"
---
> [!question] Batch Normalization was introduced by Sergey Ioffe and Christian Szegedy in 2015.
>> [!success]- Answer
>> True

> [!question] Internal Covariate Shift refers to the shifting distribution of activations between layers during training.
>> [!success]- Answer
>> True

> [!question] Batch Normalization completely eliminates the need for careful weight initialization.
>> [!success]- Answer
>> False

> [!question] The dying ReLU problem occurs when activations are pushed into the negative regime where ReLU outputs zero.
>> [!success]- Answer
>> True

> [!question] According to the original BN paper, the primary benefit of Batch Normalization is reducing Internal Covariate Shift.
>> [!success]- Answer
>> True

> [!question] Before Batch Normalization, practitioners could use large learning rates without causing divergence.
>> [!success]- Answer
>> False

> [!question] Batch Normalization is embedded in virtually every successful CNN architecture from ResNet to EfficientNet.
>> [!success]- Answer
>> True

> [!question] Internal Covariate Shift makes the optimization landscape effectively stationary from the perspective of each individual layer.
>> [!success]- Answer
>> False

> [!question] The "How Does Batch Normalization Help Optimization?" paper suggested that BN's benefits may not primarily come from reducing ICS.
>> [!success]- Answer
>> True

> [!question] When using sigmoid activation functions, input drift into the saturated regime causes gradients to become vanishingly small.
>> [!success]- Answer
>> True

> [!question] What problem does Batch Normalization primarily address?
> a) Vanishing gradients
> b) Internal Covariate Shift
> c) Overfitting
> d) Computational complexity
>> [!success]- Answer
>> b) Internal Covariate Shift

> [!question] What happens to layer k+1 when the weights of layer k are updated?
> a) Its input distribution remains the same
> b) Its input distribution changes
> c) It becomes permanently deactivated
> d) It requires no further adaptation
>> [!success]- Answer
>> b) Its input distribution changes

> [!question] What is a consequence of Internal Covariate Shift on training speed?
> a) Training becomes significantly faster
> b) Learning rates can be increased without issues
> c) Training is dramatically slowed down
> d) No effect on training speed
>> [!success]- Answer
>> c) Training is dramatically slowed down

> [!question] What problem can occur with sigmoid activation functions due to distribution shifts?
> a) Exploding gradients
> b) Vanishing gradients
> c) Dead neurons
> d) Overfitting
>> [!success]- Answer
>> b) Vanishing gradients

> [!question] What was required before Batch Normalization when training deep networks?
> a) Larger learning rates
> b) Careful initialization, tiny learning rates, and long convergence times
> c) No special initialization techniques
> d) Fewer layers in the network
>> [!success]- Answer
>> b) Careful initialization, tiny learning rates, and long convergence times

> [!question] What is the mini-batch size denoted as in the formal description of Internal Covariate Shift?
> a) k
> b) n
> c) m
> d) θ
>> [!success]- Answer
>> c) m

> [!question] What does the distribution of activations x depend on?
> a) Only the parameters of the current layer
> b) Only the input data
> c) All parameters of the preceding layers
> d) The learning rate
>> [!success]- Answer
>> c) All parameters of the preceding layers

> [!question] What happens when ReLU activations are pushed into the negative regime?
> a) They output values greater than 1
> b) They output zero, causing the "dying ReLU" problem
> c) They become linear
> d) They explode
>> [!success]- Answer
>> b) They output zero, causing the "dying ReLU" problem

> [!question] What makes the optimization landscape effectively non-stationary from the perspective of each individual layer?
> a) Fixed input distributions
> b) Constant learning rates
> c) Internal Covariate Shift
> d) Batch Normalization
>> [!success]- Answer
>> c) Internal Covariate Shift

> [!question] Match the following terms with their descriptions.
>> [!example] Group A
>> a) Batch Normalization
>> b) Internal Covariate Shift
>> c) Dying ReLU
>
>> [!example] Group B
>> n) Technique to normalize layer inputs
>> o) Shifting distribution of activations between layers
>> p) ReLU outputs zero when inputs are negative
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following concepts with their effects.
>> [!example] Group A
>> a) Saturated sigmoid
>> b) Small learning rates
>> c) Poor initialization
>
>> [!example] Group B
>> n) Vanishing gradients
>> o) Slow convergence
>> p) Training never recovers
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following architectural elements with their relationships.
>> [!example] Group A
>> a) Layer k
>> b) Layer k+1
>> c) Output
>
>> [!example] Group B
>> n) Receives inputs from layer k
>> o) Outputs serve as inputs to layer k+1
>> p) Final result of the network
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the following optimization challenges with their solutions.
>> [!example] Group A
>> a) Internal Covariate Shift
>> b) Vanishing gradients
>> c) Dying ReLU
>
>> [!example] Group B
>> n) Batch Normalization
>> o) Avoiding saturated regime
>> p) Careful initialization
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following researchers with their contributions.
>> [!example] Group A
>> a) Ioffe and Szegedy
>> b) Santurkar et al.
>> c) Xavier and He
>
>> [!example] Group B
>> n) Introduced Batch Normalization
>> o) Questioned the primary benefit of BN
>> p) Developed initialization techniques
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following network components with their roles in Internal Covariate Shift.
>> [!example] Group A
>> a) θj
>> b) x
>> c) Θ
>
>> [!example] Group B
>> n) Parameters of layer j
>> o) Activations of a layer
>> p) All parameters of preceding layers
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following training difficulties with their causes.
>> [!example] Group A
>> a) Slow convergence
>> b) Optimization instability
>> c) Need for small learning rates
>
>> [!example] Group B
>> n) Non-stationary optimization landscape
>> o) Perpetual re-adaptation to new distributions
>> p) Prevents destructive updates
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the following activation functions with their issues related to distribution shifts.
>> [!example] Group A
>> a) Sigmoid
>> b) ReLU
>> c) Tanh
>
>> [!example] Group B
>> n) Saturates for large positive/negative values
>> o) Outputs zero for negative inputs
>> p) Saturates for extreme values
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following network layers with their experiences during training.
>> [!example] Group A
>> a) Earlier layers
>> b) Later layers
>> c) Middle layers
>
>> [!example] Group B
>> n) Experience more distribution shifts
>> o) Experience fewer distribution shifts
>> p) Experience moderate distribution shifts
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following historical developments with their impacts on deep learning.
>> [!example] Group A
>> a) Pre-Batch Normalization era
>> b) Post-Batch Normalization era
>> c) Santurkar et al. findings
>
>> [!example] Group B
>> n) Required careful initialization and small learning rates
>> o) Enabled faster training and more layers
>> p) Challenged original explanation of BN benefits
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
