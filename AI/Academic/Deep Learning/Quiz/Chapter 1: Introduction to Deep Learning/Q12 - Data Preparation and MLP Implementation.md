---
sources:
  - "[[12. Data Preparation and MLP Implementation]]"
---
> [!question] Missing values must be imputed or dropped before training an MLP.
>> [!success]- Answer
>> True

> [!question] Categorical variables should be converted using One-Hot Encoding.
>> [!success]- Answer
>> True

> [!question] Data scaling is optional for neural networks — it rarely affects convergence.
>> [!success]- Answer
>> False

> [!question] Z-score Standardization is typically paired with ReLU activation.
>> [!success]- Answer
>> True

> [!question] Min-Max Scaling is typically paired with Sigmoid/Tanh activations.
>> [!success]- Answer
>> True

> [!question] You should train and test on the same data to maximize accuracy.
>> [!success]- Answer
>> False

> [!question] The Validation set is used to tune hyperparameters and trigger Early Stopping.
>> [!success]- Answer
>> True

> [!question] L2 Regularization pushes many weights exactly to zero, creating a sparse model.
>> [!success]- Answer
>> False

> [!question] L1 Regularization creates sparse models by pushing weights exactly to zero.
>> [!success]- Answer
>> True

> [!question] He initialization is designed for ReLU and its variants.
>> [!success]- Answer
>> True

> [!question] What must you do with categorical variables before feeding them to an MLP?
> a) Leave them as text
> b) Use One-Hot Encoding to convert them to numerical form
> c) Delete them
> d) Replace with zeros
>> [!success]- Answer
>> b) Use One-Hot Encoding to convert them to numerical form

> [!question] Which data split is used for tuning hyperparameters and Early Stopping?
> a) Training set
> b) Test set
> c) Validation set
> d) The entire dataset
>> [!success]- Answer
>> c) Validation set

> [!question] What is the recommended data split ratio?
> a) 50% train, 50% test
> b) 70% train, 15% validation, 15% test
> c) 90% train, 10% test
> d) 100% train, 0% test
>> [!success]- Answer
>> b) 70% train, 15% validation, 15% test

> [!question] What is the formula for Z-score Standardization?
> a) (x - x_min) / (x_max - x_min)
> b) (x - mu) / sigma
> c) x * sigma
> d) x / mu
>> [!success]- Answer
>> b) (x - mu) / sigma

> [!question] Why should you never initialize all weights to zero?
> a) It is too slow
> b) Every neuron computes the same output and receives the same gradient — symmetry breaking failure
> c) The loss becomes zero
> d) It only works for small networks
>> [!success]- Answer
>> b) Every neuron computes the same output and receives the same gradient — symmetry breaking failure

> [!question] Which weight initialization should be used with ReLU?
> a) Xavier (Glorot)
> b) He initialization
> c) Zero initialization
> d) Uniform [-1, 1]
>> [!success]- Answer
>> b) He initialization

> [!question] What does Dropout do during training?
> a) Adds more neurons
> b) Randomly deactivates a percentage of neurons to prevent over-reliance on specific features
> c) Increases the learning rate
> d) Removes the bias terms
>> [!success]- Answer
>> b) Randomly deactivates a percentage of neurons to prevent over-reliance on specific features

> [!question] What is data leakage?
> a) Training data being lost
> b) Fitting the scaler on the entire dataset including test data, giving the model hints about unseen data
> c) Using too much training data
> d) Having duplicate samples
>> [!success]- Answer
>> b) Fitting the scaler on the entire dataset including test data, giving the model hints about unseen data

> [!question] What does Early Stopping do?
> a) Stops training when the GPU overheats
> b) Monitors validation loss and stops training when it starts rising while training loss drops
> c) Stops after 1 epoch
> d) Prevents the model from learning
>> [!success]- Answer
>> b) Monitors validation loss and stops training when it starts rising while training loss drops

> [!question] What is the most important hyperparameter to tune first?
> a) Activation function
> b) Batch size
> c) Learning rate
> d) Dropout rate
>> [!success]- Answer
>> c) Learning rate

> [!question] Match the scaling method with the activation it pairs with.
>> [!example] Group A
>> a) Z-score Standardization
>> b) Min-Max Scaling
>
>> [!example] Group B
>> n) Sigmoid / Tanh
>> o) ReLU
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the dataset split with its purpose.
>> [!example] Group A
>> a) Training set (70%)
>> b) Validation set (15%)
>> c) Test set (15%)
>
>> [!example] Group B
>> n) Final evaluation on completely unseen data
>> o) Learn the weights
>> p) Tune hyperparameters and trigger Early Stopping
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the regularization type with its effect.
>> [!example] Group A
>> a) L2 (Ridge)
>> b) L1 (Lasso)
>> c) Dropout
>
>> [!example] Group B
>> n) Pushes many weights exactly to zero (sparse model)
>> o) Randomly deactivates neurons during training
>> p) Forces weights to be small but rarely zero
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the weight initialization with the activation it is designed for.
>> [!example] Group A
>> a) Xavier (Glorot)
>> b) He
>
>> [!example] Group B
>> n) ReLU and its variants
>> o) Sigmoid / Tanh
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the overfitting signal with the diagnosis.
>> [!example] Group A
>> a) Training Loss low, Validation Loss high
>> b) Both Training and Validation Loss high
>> c) Both Training and Validation Loss low and close
>
>> [!example] Group B
>> n) Well-fit model
>> o) Underfitting
>> p) Overfitting
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the hyperparameter with its search priority (1 = most important).
>> [!example] Group A
>> a) Learning rate
>> b) Batch size
>> c) Number of layers/neurons
>> d) Regularization strength
>
>> [!example] Group B
>> n) 2
>> o) 4
>> p) 1 (most important)
>> q) 3
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the anti-overfitting technique with how it works.
>> [!example] Group A
>> a) L2 Regularization
>> b) Dropout
>> c) Early Stopping
>
>> [!example] Group B
>> n) Randomly turns off neurons so no single neuron dominates
>> o) Stops training when validation loss starts rising
>> p) Adds squared weight penalty to loss function
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the scaling vulnerability with the method.
>> [!example] Group A
>> a) Min-Max Scaling
>> b) Z-score Standardization
>
>> [!example] Group B
>> n) A single extreme outlier compresses all values into a tiny range
>> o) Handles outliers better — does not bound data to a fixed range
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)

> [!question] Match the weight initialization formula with the method.
>> [!example] Group A
>> a) W ~ N(0, sqrt(2/n_in))
>> b) W ~ N(0, sqrt(1/n_in))
>
>> [!example] Group B
>> n) He initialization
>> o) Xavier initialization
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)

> [!question] Match the implementation principle with its description.
>> [!example] Group A
>> a) Start Simple
>> b) Change One Hyperparameter at a Time
>> c) Track Metrics
>
>> [!example] Group B
>> n) Plot Training Loss and Validation Loss together to diagnose problems
>> o) Begin with 1 hidden layer and add complexity only if needed
>> p) Change one setting, evaluate, keep or revert, then move to next
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
