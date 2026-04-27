---
sources:
  - "[[5. Gradient Descent Optimization]]"
---
> [!question] Gradient Descent is an iterative optimization algorithm used to minimize a differentiable function.
>> [!success]- Answer
>> True

> [!question] The gradient points in the direction of the steepest descent.
>> [!success]- Answer
>> False

> [!question] If the learning rate is too small, gradient descent will converge very slowly.
>> [!success]- Answer
>> True

> [!question] If the learning rate is too large, gradient descent may overshoot and diverge.
>> [!success]- Answer
>> True

> [!question] A convex function has multiple local minima.
>> [!success]- Answer
>> False

> [!question] Neural network loss functions are typically convex.
>> [!success]- Answer
>> False

> [!question] A saddle point is a point that is a minimum in some directions but a maximum in others.
>> [!success]- Answer
>> True

> [!question] Batch Gradient Descent computes the gradient using the entire dataset for each update.
>> [!success]- Answer
>> True

> [!question] Stochastic Gradient Descent (SGD) uses all training data for each weight update.
>> [!success]- Answer
>> False

> [!question] Mini-Batch Gradient Descent is the industry standard for training deep learning models.
>> [!success]- Answer
>> True

> [!question] What does the learning rate (alpha) control in gradient descent?
> a) The number of features
> b) The size of the step taken in the opposite direction of the gradient
> c) The number of layers
> d) The batch size
>> [!success]- Answer
>> b) The size of the step taken in the opposite direction of the gradient

> [!question] What is the update rule for gradient descent?
> a) x = x + alpha * gradient
> b) x = x - alpha * gradient
> c) x = alpha * gradient
> d) x = x / gradient
>> [!success]- Answer
>> b) x = x - alpha * gradient

> [!question] Why cannot we solve deep learning optimization analytically?
> a) The functions are too simple
> b) There are millions of non-linear parameters making analytical solutions impossible
> c) Computers cannot do math
> d) The loss is always zero
>> [!success]- Answer
>> b) There are millions of non-linear parameters making analytical solutions impossible

> [!question] What is a convex function?
> a) A function with multiple local minima
> b) A function with a single global minimum shaped like a bowl
> c) A function that is always flat
> d) A function that has no minimum
>> [!success]- Answer
>> b) A function with a single global minimum shaped like a bowl

> [!question] What happens when gradient descent gets stuck in a local minimum on a non-convex landscape?
> a) It always finds the global minimum anyway
> b) It converges prematurely to a suboptimal solution
> c) It automatically switches to a convex function
> d) It crashes
>> [!success]- Answer
>> b) It converges prematurely to a suboptimal solution

> [!question] Which variant of gradient descent uses a single random data point per update?
> a) Batch GD
> b) Mini-Batch GD
> c) Stochastic GD
> d) Full GD
>> [!success]- Answer
>> c) Stochastic GD

> [!question] Why are saddle points more common than true local minima in high-dimensional spaces?
> a) Because all dimensions have the same minimum
> b) Because a local minimum in one dimension is rarely a local minimum in all other dimensions
> c) Because saddle points do not exist
> d) Because neural networks are always convex
>> [!success]- Answer
>> b) Because a local minimum in one dimension is rarely a local minimum in all other dimensions

> [!question] What is a key benefit of mini-batch noise?
> a) It makes training slower
> b) It can help escape shallow local minima or saddle points
> c) It increases the learning rate
> d) It removes the need for a loss function
>> [!success]- Answer
>> b) It can help escape shallow local minima or saddle points

> [!question] Which adaptive optimizer automatically adjusts the learning rate per parameter?
> a) Only vanilla SGD
> b) Adam, RMSProp, or Adagrad
> c) Batch GD
> d) No optimizer does this
>> [!success]- Answer
>> b) Adam, RMSProp, or Adagrad

> [!question] What is the stopping criterion for gradient descent?
> a) When the gradient is zero or very close to zero
> b) When the learning rate reaches 1
> c) When all weights are zero
> d) When the dataset is empty
>> [!success]- Answer
>> a) When the gradient is zero or very close to zero

> [!question] Match the GD variant with the amount of data used per update.
>> [!example] Group A
>> a) Batch GD
>> b) Stochastic GD
>> c) Mini-Batch GD
>
>> [!example] Group B
>> n) A small group (e.g., 32-512 samples)
>> o) The entire dataset
>> p) A single random sample
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the GD variant with its stability.
>> [!example] Group A
>> a) Batch GD
>> b) Stochastic GD
>> c) Mini-Batch GD
>
>> [!example] Group B
>> n) Very stable, smooth path
>> o) Noisy/chaotic, seismograph-like
>> p) Stable enough, slight noise
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the learning rate scenario with the behavior.
>> [!example] Group A
>> a) Learning rate too small
>> b) Learning rate too large
>
>> [!example] Group B
>> n) Overshoots, bounces, may diverge
>> o) Tiny steps, very slow convergence
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the function type with its landscape shape.
>> [!example] Group A
>> a) Convex function
>> b) Non-convex function
>
>> [!example] Group B
>> n) Single bowl, one global minimum
>> o) Multiple valleys, local and global minima
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)

> [!question] Match the concept with its definition.
>> [!example] Group A
>> a) Gradient
>> b) Learning Rate
>> c) Saddle Point
>
>> [!example] Group B
>> n) Step size hyperparameter
>> o) Minimum in some directions, maximum in others
>> p) Direction of steepest ascent
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the mini-batch benefit with its description.
>> [!example] Group A
>> a) Escape from local minima
>> b) RAM management
>> c) Faster convergence
>
>> [!example] Group B
>> n) Stochastic noise shakes the algorithm out of shallow valleys
>> o) Updates weights many times per epoch instead of once
>> p) Fits in GPU VRAM — cannot load millions of images at once
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the GD variant with its memory usage.
>> [!example] Group A
>> a) Batch GD
>> b) SGD
>> c) Mini-Batch GD
>
>> [!example] Group B
>> n) Low
>> o) Medium
>> p) Very High
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the term with the formula component.
>> [!example] Group A
>> a) x_t
>> b) alpha
>> c) nabla f(x_t)
>
>> [!example] Group B
>> n) The gradient (slope) at the current point
>> o) Current parameter value
>> p) Learning rate (step size)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the solution to the learning rate problem.
>> [!example] Group A
>> a) Learning Rate Schedulers
>> b) Adaptive Optimizers
>
>> [!example] Group B
>> n) Automatically adjust learning rate per parameter (Adam, RMSProp)
>> o) Start high then gradually reduce the rate
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the convexity property with the implication for GD.
>> [!example] Group A
>> a) Convex landscape
>> b) Non-convex landscape
>
>> [!example] Group B
>> n) GD may get stuck in local minima
>> o) GD guaranteed to find the global minimum
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
