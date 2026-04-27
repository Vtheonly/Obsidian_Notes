---
sources:
  - "[[17. Dropout and Regularization]]"
---
> [!source] Source: [[17. Dropout and Regularization]]

> [!question] Overfitting occurs when a model performs well on training data but poorly on validation data.
>> [!success]- Answer
>> True

> [!question] Dropout was introduced by Geoffrey Hinton and his team in 2014.
>> [!success]- Answer
>> True

> [!question] The primary purpose of regularization is to increase model complexity.
>> [!success]- Answer
>> False

> [!question] Inverted dropout ensures that the expected value of each neuron's output remains the same during training.
>> [!success]- Answer
>> True

> [!question] A training accuracy of 99% and validation accuracy of 75% indicates a healthy model that generalizes well.
>> [!success]- Answer
>> False

> [!question] Dropout prevents co-adaptation by forcing neurons to learn features that are individually useful.
>> [!success]- Answer
>> True

> [!question] Early stopping is a regularization technique that involves stopping training when validation loss starts increasing.
>> [!success]- Answer
>> True

> [!question] The dropout rate p determines the probability that a neuron will be kept rather than dropped.
>> [!success]- Answer
>> False

> [!question] At test time, dropout is applied with the same random mask as during training.
>> [!success]- Answer
>> False

> [!question] Ensemble averaging is a benefit of dropout because it trains multiple models simultaneously.
>> [!success]- Answer
>> False

> [!question] What is the primary indicator that a model is overfitting?
> a) High training accuracy but low validation accuracy
> b) Low training accuracy but high validation accuracy
> c) Both training and validation accuracy are low
> d) Both training and validation accuracy are high but decreasing
>> [!success]- Answer
>> a) High training accuracy but low validation accuracy

> [!question] What happens to the outputs of neurons that are not dropped during training with dropout?
> a) They remain unchanged
> b) They are scaled up by a factor of 1/(1-p)
> c) They are scaled down by a factor of (1-p)
> d) They are replaced with zeros
>> [!success]- Answer
>> b) They are scaled up by a factor of 1/(1-p)

> [!question] Which of the following is NOT a primary cause of overfitting?
> a) Too many parameters relative to training data
> b) Too little training data
> c) Too many epochs
> d) Too few layers in the network
>> [!success]- Answer
>> d) Too few layers in the network

> [!question] What is the mathematical operation performed by dropout on a neuron's activation h_i with probability p?
> a) Set h_i to zero
> b) Set h_i to h_i/(1-p)
> c) Set h_i to r_i * h_i where r_i is Bernoulli(1-p)
> d) Set h_i to r_i * h_i/(1-p) where r_i is Bernoulli(1-p)
>> [!success]- Answer
>> d) Set h_i to r_i * h_i/(1-p) where r_i is Bernoulli(1-p)

> [!question] How does dropout help prevent co-adaptation of neurons?
> a) By forcing all neurons to learn the same features
> b) By randomly dropping neurons and preventing dependencies
> c) By scaling down all neuron outputs
> d) By increasing the number of neurons in each layer
>> [!success]- Answer
>> b) By randomly dropping neurons and preventing dependencies

> [!question] What is the effect of dropout at test time?
> a) The same dropout mask is applied as during training
> b) No dropout is applied, and all neurons are used
> c) A different, fixed dropout mask is applied
> d) Dropout is applied with a higher rate than during training
>> [!success]- Answer
>> b) No dropout is applied, and all neurons are used

> [!question] Which of the following statements about dropout's ensemble effect is true?
> a) It trains 2^n independent models where n is the number of neurons
> b) It approximates an ensemble average of sub-networks during training
> c) It requires training multiple models separately and then averaging their outputs
> d) It only works for convolutional neural networks, not fully connected networks
>> [!success]- Answer
>> b) It approximates an ensemble average of sub-networks during training

> [!question] What is the "death by capacity" problem?
> a) When a model has too few parameters to learn the data
> b) When a model has too many parameters and can memorize the training data
> c) When a model's capacity is perfectly matched to the data complexity
> d) When a model's capacity decreases during training
>> [!success]- Answer
>> b) When a model has too many parameters and can memorize the training data

> [!question] What is the "divergence point" in the context of overfitting?
> a) The point where training and validation accuracy are equal
> b) The point where training accuracy reaches 100%
> c) The point where validation loss starts increasing while training loss continues decreasing
> d) The point where the model's capacity becomes too high
>> [!success]- Answer
>> c) The point where validation loss starts increasing while training loss continues decreasing

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Dropout
>> b) Overfitting
>> c) Inverted dropout
>> d) Co-adaptation
>
>> [!example] Group B
>> n) Scaling neuron outputs to preserve expected value
>> o) Neurons developing interdependencies where specific neurons only produce useful outputs when others are active
>> p) Randomly setting a fraction of neurons to zero during training
>> q) Model memorizing training data without generalizing to unseen data
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the regularization technique with its primary mechanism.
>> [!example] Group A
>> a) Dropout
>> b) Early stopping
>> c) L2 regularization
>> d) Data augmentation
>
>> [!example] Group B
>> n) Penalizing large weights to encourage simpler models
>> o) Stopping training when validation performance degrades
>> p) Randomly dropping neurons to create sub-networks
>> q) Creating modified versions of training data
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match the cause of overfitting with its description.
>> [!example] Group A
>> a) Too many parameters
>> b) Too little data
>> c) Too many epochs
>> d) High learning rate
>
>> [!example] Group B
>> n) Model memorizes noise rather than learning general patterns
>> o) Model has too many degrees of freedom relative to data
>> p) Insufficient examples to learn true data distribution
>> q) Training for too long causes fitting of training noise
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the mathematical concept with its correct formulation in dropout.
>> [!example] Group A
>> a) Dropout mask
>> b) Dropout output
>> c) Expected value preservation
>> d) Dropout rate
>
>> [!example] Group B
>> n) r_i ~ Bernoulli(1-p)
>> o) E[tilde{h}_i] = h_i
>> p) p determines probability of dropping a neuron
>> q) tilde{h}_i = r_i * h_i / (1-p)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> q)
>> c) -> o)
>> d) -> p)

> [!question] Match the dropout benefit with its explanation.
>> [!example] Group A
>> a) Prevents co-adaptation
>> b) Ensemble effect
>> c) Adds noise for robustness
>> d) Reduces model capacity
>
>> [!example] Group B
>> n) Forces neurons to learn individually useful features
>> o) Approximates averaging of multiple models
>> p) Makes network more resistant to input variations
>> q) Decreases number of parameters in the network
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the statement about overfitting with its correct implication.
>> [!example] Group A
>> a) Training accuracy >> Validation accuracy
>> b) Model performs well on training but poorly on test
>> c) Small gap between training and validation performance
>> d) Large gap between training and validation performance
>
>> [!example] Group B
>> n) Indicates good generalization
>> o) Suggests severe overfitting
>> p) Diagnostic signal of overfitting
>> q) May indicate underfitting
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> o)

> [!question] Match the regularization technique with its typical use case.
>> [!example] Group A
>> a) Dropout
>> b) Early stopping
>> c) L1 regularization
>> d) Batch normalization
>
>> [!example] Group B
>> n) Effective for large networks with many parameters
>> o) Useful when training time is limited
>> p) Particularly effective for sparse feature selection
>> q) Helps stabilize training but not primarily a regularization technique
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the dropout scenario with its correct description.
>> [!example] Group A
>> a) Training with dropout
>> b) Test/inference with dropout
>> c) Training without dropout
>> d) Dropout rate p = 0.5
>
>> [!example] Group B
>> n) All neurons used with no scaling
>> o) Random subset of neurons used with scaling
>> p) All neurons used with full weights
>> q) Maximum regularization effect
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)
