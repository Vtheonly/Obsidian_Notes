---
sources:
  - "[[Apprentissage Profond]]"
---

### True or False Questions

> [!question] In classic Machine Learning, feature extraction is done automatically by the machine, whereas in Deep Learning, humans must define features manually.
>> [!success]- Answer
>> False

> [!question] Deep Learning generally outperforms classic Machine Learning when working with very large volumes of data ("Big Data").
>> [!success]- Answer
>> True

> [!question] Standard Gradient Descent (GD) uses only a single, randomly chosen data point at each training iteration to calculate parameters.
>> [!success]- Answer
>> False

> [!question] Stochastic Gradient Descent (SGD) is faster than standard GD but produces a noisier/more unstable convergence trajectory.
>> [!success]- Answer
>> True

> [!question] Mini-batch Gradient Descent is widely used for training deep neural networks because it balances computational speed and trajectory stability.
>> [!success]- Answer
>> True

> [!question] A convex function typically contains multiple local minima, making optimization with Gradient Descent highly difficult.
>> [!success]- Answer
>> False

> [!question] If the learning rate ($\alpha$) is set too high during Gradient Descent, the algorithm may oscillate and fail to converge.
>> [!success]- Answer
>> True

> [!question] The Mean Absolute Error (MAE) loss function is more sensitive to outliers than the Mean Squared Error (MSE) loss function.
>> [!success]- Answer
>> False

> [!question] Binary Cross-Entropy (BCE) loss is specifically designed for multi-class classification tasks.
>> [!success]- Answer
>> False

> [!question] Huber Loss functions as a hybrid between MSE and MAE, shifting its mathematical behavior based on a defined threshold.
>> [!success]- Answer
>> True

> [!question] In simple linear regression, the parameter $\theta_0$ corresponds to the slope of the line, while $\theta_1$ corresponds to the y-intercept.
>> [!success]- Answer
>> False

> [!question] In multiple linear regression, failing to scale features can significantly slow down the convergence of Gradient Descent.
>> [!success]- Answer
>> True

> [!question] Using Mean Squared Error (MSE) directly as the cost function for logistic regression results in a non-convex optimization landscape.
>> [!success]- Answer
>> True

> [!question] The sigmoid function maps input values to an output range of [-1, 1].
>> [!success]- Answer
>> False

> [!question] The decision boundary in logistic regression is always strictly linear and cannot represent complex geometric shapes.
>> [!success]- Answer
>> False

> [!question] A single-layer Perceptron can successfully classify data that is not linearly separable.
>> [!success]- Answer
>> False

> [!question] The aggregation step in a Perceptron is calculated as $z = \sum w_j x_j + b$.
>> [!success]- Answer
>> True

> [!question] The Hyperbolic Tangent (Tanh) activation function is centered on zero, with values ranging between -1 and 1.
>> [!success]- Answer
>> True

> [!question] Softmax activation is typically applied in hidden layers of a neural network to facilitate gradient flow.
>> [!success]- Answer
>> False

> [!question] The rectified linear unit (ReLU) activation function helps mitigate the vanishing gradient problem in deep networks.
>> [!success]- Answer
>> True

> [!question] Leaky ReLU avoids the "dead neuron" problem by allowing a small, non-zero gradient when the input is negative.
>> [!success]- Answer
>> True

> [!question] The Parametric ReLU (PReLU) activation function uses a fixed, unlearnable slope ($\alpha = 0.01$) for negative inputs.
>> [!success]- Answer
>> False

> [!question] Swish is an auto-gated activation function discovered by Google that can outperform ReLU in very deep networks.
>> [!success]- Answer
>> True

> [!question] GELU (Gaussian Error Linear Unit) is heavily used in Transformer architectures like BERT and GPT.
>> [!success]- Answer
>> True

> [!question] Without non-linear activation functions, a multi-layer neural network collapses into a simple linear combination of operations.
>> [!success]- Answer
>> True

> [!question] In the backward pass of a Multi-Layer Perceptron (MLP), we compute the predictions of the network layer by layer.
>> [!success]- Answer
>> False

> [!question] Neurons in the input layer of an MLP perform linear transformations and apply activation functions.
>> [!success]- Answer
>> False

> [!question] Early Stopping is a regularization technique used to prevent overfitting by halting training when validation performance begins to degrade.
>> [!success]- Answer
>> True

> [!question] One-Hot Encoding is used to convert continuous numerical features into binary categories.
>> [!success]- Answer
>> False

> [!question] Dropout is a regularization technique that randomly deactivates a fraction of neurons during training to prevent co-adaptation.
>> [!success]- Answer
>> True

---

### Multiple Choice Questions

> [!question] Which of the following is a primary characteristic of Deep Learning compared to classical Machine Learning?
> a) It requires manual feature engineering.
> b) It performs poorly on complex unstructured data.
> c) It automatically learns complex representations from raw data.
> d) It runs highly efficiently on CPU without requiring GPU.
>> [!success]- Answer
>> c) It automatically learns complex representations from raw data.

> [!question] Who is credited with inventing the Perceptron in the late 1950s?
> a) Frank Rosenblatt
> b) Yann LeCun
> c) Geoffrey Hinton
> d) Yoshua Bengio
>> [!success]- Answer
>> a) Frank Rosenblatt

> [!question] Which model architecture won the ImageNet competition in 2012, triggering the deep learning boom?
> a) Transformer
> b) AlexNet
> c) GPT-3
> d) AlphaGo
>> [!success]- Answer
>> b) AlexNet

> [!question] What major AI milestone occurred in 2016 involving a victory over humans?
> a) The victory of AlexNet in ImageNet
> b) The release of ChatGPT
> c) The victory of AlphaGo in the game of Go
> d) The invention of GANs
>> [!success]- Answer
>> c) The victory of AlphaGo in the game of Go

> [!question] Which framework is noted in the slides as being highly flexible and favored for research?
> a) TensorFlow
> b) JAX
> c) Caffe
> d) PyTorch
>> [!success]- Answer
>> d) PyTorch

> [!question] In the optimization of a differentiable and convex function $f(x)$, what does a local minimum represent?
> a) A point where $f'(x) > 0$
> b) The global minimum of the function
> c) A point of maximum loss
> d) A point where the function is non-differentiable
>> [!success]- Answer
>> b) The global minimum of the function

> [!question] In Gradient Descent, what does the parameter $\alpha$ (or $\eta$) represent?
> a) The loss value
> b) The model bias
> c) The learning rate
> d) The number of layers
>> [!success]- Answer
>> c) The learning rate

> [!question] What is a major disadvantage of using a fixed, extremely small learning rate?
> a) The algorithm will oscillate wildly and never converge.
> b) The algorithm will converge very slowly.
> c) It will immediately get stuck in local maxima.
> d) It leads to massive memory consumption.
>> [!success]- Answer
>> b) The algorithm will converge very slowly.

> [!question] Which Gradient Descent variant uses a subset (e.g., 32 to 512) of the training dataset at each step?
> a) Batch Gradient Descent
> b) Stochastic Gradient Descent (SGD)
> c) Mini-batch Gradient Descent
> d) Analytical Gradient Descent
>> [!success]- Answer
>> c) Mini-batch Gradient Descent

> [!question] Which loss function is defined as Hinge Loss, commonly used in SVMs and some neural networks?
> a) $\sum \max(0, 1 - y_i \cdot \hat{y}_i)$
> b) $\frac{1}{n}\sum(y_i - \hat{y}_i)^2$
> c) $-\frac{1}{n}\sum y_i \log(\hat{y}_i)$
> d) $\frac{1}{n}\sum|y_i - \hat{y}_i|$
>> [!success]- Answer
>> a) $\sum \max(0, 1 - y_i \cdot \hat{y}_i)$

> [!question] Which cost function should be used for a multi-class classification problem?
> a) Mean Squared Error (MSE)
> b) Binary Cross-Entropy (BCE)
> c) Categorical Cross-Entropy (CCE)
> d) Huber Loss
>> [!success]- Answer
>> c) Categorical Cross-Entropy (CCE)

> [!question] In the linear regression hypothesis $h(x) = \theta_0 + \theta_1 x$, what does $\theta_0$ represent in Machine Learning terminology?
> a) Weight
> b) Bias
> c) Input feature
> d) Cost
>> [!success]- Answer
>> b) Bias

> [!question] What is the derivative of the cost function $J(\theta_0, \theta_1)$ with respect to $\theta_0$ in simple linear regression?
> a) $\frac{1}{m} \sum (h_{\theta}(x_i) - y_i)$
> b) $\frac{1}{m} \sum (h_{\theta}(x_i) - y_i) \cdot x_i$
> c) $\frac{1}{2m} \sum (h_{\theta}(x_i) - y_i)^2$
> d) $\sum (y_i - h_{\theta}(x_i))$
>> [!success]- Answer
>> a) $\frac{1}{m} \sum (h_{\theta}(x_i) - y_i)$

> [!question] In vectorizing multiple linear regression, what represents the hypothesis function?
> a) $h(x) = \theta + x$
> b) $h(x) = \theta^T x$
> c) $h(x) = \theta \cdot \text{sigmoid}(x)$
> d) $h(x) = \theta / x$
>> [!success]- Answer
>> b) $h(x) = \theta^T x$

> [!question] Which feature scaling method normalizes data such that $x_{ij} \in [0, 1]$?
> a) Z-score Standardisation
> b) Min-Max Scaling
> c) Mean Normalisation
> d) Absolute Scaling
>> [!success]- Answer
>> b) Min-Max Scaling

> [!question] Which of the following is the mathematical formula of the Sigmoid function?
> a) $g(z) = \max(0, z)$
> b) $g(z) = \frac{1}{1 + e^{-z}}$
> c) $g(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$
> d) $g(z) = z$
>> [!success]- Answer
>> b) $g(z) = \frac{1}{1 + e^{-z}}$

> [!question] What occurs when we evaluate the cost of a prediction where the true label is $y = 1$ and the predicted probability $h(x)$ approaches $0$ in Logistic Regression?
> a) The cost approaches 0.
> b) The cost is halved.
> c) The cost approaches $+\infty$.
> d) The cost remains negative.
>> [!success]- Answer
>> c) The cost approaches $+\infty$.

> [!question] In Gradient Descent updates for linear regression, why must parameters $\theta_j$ be updated simultaneously?
> a) To avoid using partially updated parameters in the calculation of other gradients.
> b) To decrease the learning rate automatically.
> c) To allow the use of CPUs instead of GPUs.
> d) To convert a non-convex function into a convex one.
>> [!success]- Answer
>> a) To avoid using partially updated parameters in the calculation of other gradients.

> [!question] What is the output range of the Tanh activation function?
> a) $[0, 1]$
> b) $[-1, 1]$
> c) $[0, +\infty]$
> d) $[-\infty, +\infty]$
>> [!success]- Answer
>> b) $[-1, 1]$

> [!question] Which activation function is defined as $f(x) = \max(0, x)$?
> a) Sigmoid
> b) Tanh
> c) ReLU
> d) Leaky ReLU
>> [!success]- Answer
>> c) ReLU

> [!question] What distinguishing feature does Parametric ReLU (PReLU) have?
> a) It has a constant slope of 0.01 for negative inputs.
> b) It sets all negative inputs to zero.
> c) The slope for negative inputs is a parameter learned during training.
> d) It is defined as a Gaussian distribution.
>> [!success]- Answer
>> c) The slope for negative inputs is a parameter learned during training.

> [!question] Which activation function is recommended in the slides for use in the output layer of a multi-class classification problem?
> a) Sigmoid
> b) ReLU
> c) Softmax
> d) Linear
>> [!success]- Answer
>> c) Softmax

> [!question] What is the fundamental role of activation functions in deep neural networks?
> a) To reduce the number of parameters.
> b) To introduce non-linearity so the network can learn complex patterns.
> c) To perform dimensionality reduction.
> d) To initialize weights to zero.
>> [!success]- Answer
>> b) To introduce non-linearity so the network can learn complex patterns.

> [!question] In the Perceptron mathematical framework, what is the output of the aggregation stage ($z$)?
> a) The activation values of the hidden layers.
> b) $z(W) = W^T X + b$
> c) The cross-entropy error.
> d) The final predicted class.
>> [!success]- Answer
>> b) $z(W) = W^T X + b$

> [!question] During MLP data preparation, what does Standardisation (Z-score) do to the data?
> a) Scales values strictly between 0 and 1.
> b) Centers the data around 0 with a variance of 1.
> c) Converts categorical variables into binary vectors.
> d) Removes all empty entries.
>> [!success]- Answer
>> b) Centers the data around 0 with a variance of 1.

> [!question] Which of the following is NOT an architectural layer of a Multi-Layer Perceptron (MLP)?
> a) Input layer
> b) Recurrent layer
> c) Hidden layer(s)
> d) Output layer
>> [!success]- Answer
>> b) Recurrent layer

> [!question] What is the purpose of the validation dataset in MLP training?
> a) To train the model weights and biases directly.
> b) To tune hyperparameters and prevent overfitting.
> c) To perform the final evaluation on entirely unseen data.
> d) To clean categorical values.
>> [!success]- Answer
>> b) To tune hyperparameters and prevent overfitting.

> [!question] Which weight initialization techniques are specifically highlighted in the slides as suitable for deep neural networks?
> a) Random Zero initialization
> b) Constant value initialization
> c) Xavier or He initialization
> d) Gradient descent initialization
>> [!success]- Answer
>> c) Xavier or He initialization

> [!question] What does the term "Backpropagation" refer to in neural network training?
> a) Passing inputs forward to calculate predictions.
> b) Computing the gradients of the loss function to update the model weights.
> c) Generating synthetic training data.
> d) Pruning inactive neurons from the network.
>> [!success]- Answer
>> b) Computing the gradients of the loss function to update the model weights.

> [!question] Which of the following is an adaptive optimizer mentioned in the slides that automatically adjusts the learning rate?
> a) Stochastic Gradient Descent (SGD)
> b) Batch Gradient Descent
> c) Adam
> d) Analytical Descent
>> [!success]- Answer
>> c) Adam

---

### Matching Questions

> [!question] Match the AI sub-field with its definition.
>> [!example] Group A
>> a) Intelligence Artificielle (IA)
>> b) Machine Learning (ML)
>> c) Deep Learning (DL)
>
>> [!example] Group B
>> n) Sub-field of ML based on multi-layered artificial neural networks.
>> o) Broad field aimed at simulating human intelligence.
>> p) Sub-field of IA focused on algorithms that learn from data.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Deep Learning pioneer with their specific achievement.
>> [!example] Group A
>> a) Geoffrey Hinton
>> b) Yann LeCun
>> c) Ian Goodfellow
>
>> [!example] Group B
>> n) Invented Generative Adversarial Networks (GANs) in 2014.
>> o) Main developer of backpropagation and deep networks.
>> p) Invented Convolutional Neural Networks (CNNs) for image recognition.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Gradient Descent variant with its main characteristic.
>> [!example] Group A
>> a) Batch Gradient Descent
>> b) Stochastic Gradient Descent (SGD)
>> c) Mini-batch Gradient Descent
>
>> [!example] Group B
>> n) Uses a single random data point per iteration; fast but unstable.
>> o) Uses the entire dataset at each iteration; stable but very slow.
>> p) Uses small random subsets of data; standard for Deep Learning.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the cost function with its typical regression behavior.
>> [!example] Group A
>> a) Mean Squared Error (MSE)
>> b) Mean Absolute Error (MAE)
>> c) Huber Loss
>
>> [!example] Group B
>> n) Less sensitive to outliers; computes absolute differences.
>> o) Hybrid loss that behaves like MSE near zero and MAE elsewhere.
>> p) Computes the average of squared differences; highly penalizes large errors.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the classic activation function with its output range.
>> [!example] Group A
>> a) Sigmoid
>> b) Tanh (Hyperbolic Tangent)
>> c) Softmax
>
>> [!example] Group B
>> n) Outputs probabilities summing to 1; used for multi-class classification.
>> o) Maps inputs to an output range between 0 and 1; used for binary classification.
>> p) Zero-centered activation function with values between -1 and 1.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the ReLU variant with its mathematical definition.
>> [!example] Group A
>> a) Leaky ReLU
>> b) Parametric ReLU (PReLU)
>> c) ELU (Exponential Linear Unit)
>
>> [!example] Group B
>> n) Slope for negative inputs is a parameter learned during training.
>> o) Uses a small fixed slope (e.g., 0.01) for negative inputs.
>> p) Uses an exponential curve for negative values to bring mean activations closer to zero.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the machine learning model with its task definition.
>> [!example] Group A
>> a) Simple Linear Regression
>> b) Logistic Regression
>> c) Multiple Linear Regression
>
>> [!example] Group B
>> n) Supervised classification technique using a sigmoid function.
>> o) Predicts a continuous output using a single independent variable.
>> p) Predicts a continuous output using multiple independent variables.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the MLP architectural layer with its functional role.
>> [!example] Group A
>> a) Input Layer
>> b) Hidden Layers
>> c) Output Layer
>
>> [!example] Group B
>> n) Computes final predictions; size depends on task type.
>> o) Passes raw features directly to the next layer without calculation.
>> p) Intermediary layers that perform feature transformations using weights and activations.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the regularization method with its operation.
>> [!example] Group A
>> a) Dropout
>> b) Early Stopping
>> c) L1/L2 Regularization
>
>> [!example] Group B
>> n) Adds a penalty term directly to the loss function to limit weight magnitudes.
>> o) Randomly deactivates a percentage of neurons during training.
>> p) Halts training when the loss on the validation dataset begins to rise.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the data scaling technique with its definition.
>> [!example] Group A
>> a) Min-Max Scaling
>> b) Z-score Standardisation
>> c) One-Hot Encoding
>
>> [!example] Group B
>> n) Converts categorical features into numerical binary vectors.
>> o) Scales values strictly between a fixed range, typically [0, 1].
>> p) Shifts data to have a mean of 0 and a standard deviation of 1.
>
>> [success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

---
sources:
  - "[[Apprentissage Profond]]"
---

### True or False Questions

> [!question] Standardisation (Z-score) is recommended for hidden layers when using Sigmoid or Tanh activation functions, while Min-Max normalization is typically preferred for ReLU.
>> [!success]- Answer
>> False

> [!question] In PyTorch, LibTorch represents the C++ API, while Python is the primary interface used for writing standard commands.
>> [!success]- Answer
>> True

> [!question] The analytical solution for minimizing the function $f(x) = x^2 - x + 1$ is $x^* = 0.5$.
>> [!success]- Answer
>> True

> [!question] An analytical solution to optimization is always possible and preferred, even when the number of parameters is extremely large.
>> [!success]- Answer
>> False

> [!question] The parameter space of a deep learning model is typically one-dimensional, allowing easy visualization of the loss landscape.
>> [!success]- Answer
>> False

> [!question] In Gradient Descent, a derivative of the cost function is used to determine both the step direction and magnitude.
>> [!success]- Answer
>> True

> [!question] Large batch sizes introduce more stochastic noise into gradient calculations than small batch sizes.
>> [!success]- Answer
>> False

> [!question] Small batch sizes generally offer better generalization but can lead to more unstable calculations during training.
>> [!success]- Answer
>> True

> [!question] Computing the gradient over millions of data points simultaneously can easily exceed standard hardware RAM capacity.
>> [!success]- Answer
>> True

> [!question] Adaptive optimizers like Adam completely eliminate the need to tune the initial learning rate.
>> [!success]- Answer
>> False

> [!question] In simple linear regression, the cost function $J(\theta_0, \theta_1)$ is represented as a 3D parabolic surface when using MSE.
>> [!success]- Answer
>> True

> [!question] In the gradient descent update for multiple linear regression, parameters are updated as $\theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta)$.
>> [!success]- Answer
>> True

> [!question] The vector of features $x$ in vectorized multiple linear regression starts with $x_0 = 1$ to account for the bias term $\theta_0$.
>> [!success]- Answer
>> True

> [!question] If two features have extremely different scales (e.g., [0, 1] vs [0, 1000000]), Gradient Descent will converge along a highly efficient, straight-line path.
>> [!success]- Answer
>> False

> [!question] Logistic regression is a regression technique used to predict continuous outputs such as house prices.
>> [!success]- Answer
>> False

> [!question] The sigmoid function output $g(z)$ is exactly 0.5 when the input $z$ is exactly 0.
>> [!success]- Answer
>> True

> [!question] If $z$ approaches negative infinity ($z \to -\infty$), the sigmoid output $g(z)$ approaches 1.
>> [!success]- Answer
>> False

> [!question] In logistic regression, we predict class $y=1$ if the hypothesis output $h(x) \geq 0.5$.
>> [!success]- Answer
>> True

> [!question] The cost function of logistic regression is derived using the logarithm because the sigmoid activation is non-linear and would otherwise lead to a non-convex MSE cost.
>> [!success]- Answer
>> True

> [!question] In the gradient update equation for logistic regression, the mathematical form of the derivative is identical to that of linear regression, despite the different hypothesis functions.
>> [!success]- Answer
>> True

> [!question] A biological neuron transmits signals through dendrites, processes them in the soma, and forwards the output via the axon.
>> [!success]- Answer
>> True

> [!question] In a Perceptron, the aggregation function is non-linear while the activation function is linear.
>> [!success]- Answer
>> False

> [!question] Softmax scales a vector of $K$ real numbers into a probability distribution where all values are between 0 and 1, and their sum equals 1.
>> [!success]- Answer
>> True

> [!question] In the standard Swish activation function formula $f(x) = x \cdot \sigma(x)$, the term $\sigma(x)$ represents the sigmoid function.
>> [!success]- Answer
>> True

> [!question] The non-linearity introduced by activation functions allows a neural network to model complex, curved decision boundaries.
>> [!success]- Answer
>> True

> [!question] In the vectorization of Perceptron equations, the matrix $X$ has dimensions $n \times (m+1)$, where $n$ is the number of samples and $m$ is the number of features.
>> [!success]- Answer
>> True

> [!question] In the backpropagation equations, $\nabla \mathcal{L}$ represents the Jacobian matrix of the cost function.
>> [!success]- Answer
>> True

> [!question] A Multi-Layer Perceptron (MLP) is a feedforward neural network (propagation avant).
>> [!success]- Answer
>> True

> [!question] In a fully connected MLP, every neuron in a hidden layer is connected to every neuron in the subsequent layer.
>> [!success]- Answer
>> True

> [!question] Data augmentation, such as rotating or zooming images, is primarily used to reduce training time.
>> [!success]- Answer
>> False

---

### Multiple Choice Questions

> [!question] Which of the following is a key advantage of using GPU over CPU for Deep Learning?
> a) GPUs handle sequential tasks much faster than CPUs.
> b) GPUs have superior parallel processing capabilities suited for massive matrix multiplication.
> c) GPUs completely eliminate the risk of overfitting during training.
> d) GPUs do not require memory management during computation.
>> [!success]- Answer
>> b) GPUs have superior parallel processing capabilities suited for massive matrix multiplication.

> [!question] Yann LeCun, Geoffrey Hinton, and Yoshua Bengio were jointly awarded which prestigious prize in 2018?
> a) The Nobel Prize in Physics
> b) The Fields Medal
> c) The Turing Award
> d) The Kyoto Prize
>> [!success]- Answer
>> c) The Turing Award

> [!question] What is the primary role of Scale AI, founded by Alexandr Wang in 2016?
> a) Designing next-generation GPU microchips.
> b) Annotating and managing data to help train AI models.
> c) Developing the PyTorch framework.
> d) Manufacturing autonomous electric vehicles.
>> [!success]- Answer
>> b) Annotating and managing data to help train AI models.

> [!question] Why was there a period of retreat for neural networks (ANN) prior to 2006?
> a) Because computers were too expensive to purchase.
> b) Because they were temporarily banned in academic research.
> c) Because researchers preferred simpler statistical methods like SVM, Decision Trees, and Random Forests.
> d) Because backpropagation had not been invented yet.
>> [!success]- Answer
>> c) Because researchers preferred simpler statistical methods like SVM, Decision Trees, and Random Forests.

> [!question] What was the core challenge of the ImageNet LSVRC competition?
> a) Translating text documents across 1000 different languages.
> b) Automatically classifying 1 million annotated images into 1000 classes.
> c) Beating the world champion in chess.
> d) Generating realistic human faces from text descriptions.
>> [!success]- Answer
>> b) Automatically classifying 1 million annotated images into 1000 classes.

> [!question] Which application is mentioned under the "Security" domain of Deep Learning?
> a) Automated check depositing.
> b) Identifying risky situations such as crowd stampedes or fights via surveillance cameras.
> c) Sorting food products on assembly lines.
> d) Generating personalized marketing banners.
>> [!success]- Answer
>> b) Identifying risky situations such as crowd stampedes or fights via surveillance cameras.

> [!question] In financial institutions, how is Deep Learning utilized for processing checks?
> a) It automatically registers checks using visual text recognition of handwritten characters.
> b) It physically moves checks between banks.
> c) It calculates the interest rate on loans based on check deposits.
> d) It limits the maximum amount a customer can write on a check.
>> [!success]- Answer
>> a) It automatically registers checks using visual text recognition of handwritten characters.

> [!question] Which mathematical equation represents the analytical solution $f'(x) = 0$ for the convex function $f(x) = x^2 - x + 1$?
> a) $2x - 1 = 0$
> b) $x^2 - x = 0$
> c) $2x + 1 = 0$
> d) $x - 1 = 0$
>> [!success]- Answer
>> a) $2x - 1 = 0$

> [!question] In Gradient Descent, the gradient vector points in which direction?
> a) Towards the global minimum.
> b) Along the path of steepest ascent of the function.
> c) Parallel to the horizontal axis.
> d) Directly perpendicular to the parameter space.
>> [!success]- Answer
>> b) Along the path of steepest ascent of the function.

> [!question] If the loss function is convex, what is the ideal outcome of Gradient Descent optimization?
> a) Oscillating infinitely around the starting point.
> b) Gradually converging to the global minimum.
> c) Reaching the global maximum.
> d) Diverging to infinity.
>> [!success]- Answer
>> b) Gradually converging to the global minimum.

> [!question] What is the main drawback of standard (Batch) Gradient Descent on very large datasets?
> a) It is highly unstable and noisy.
> b) It only updates parameters after evaluating the entire dataset, making it extremely slow.
> c) It requires zero memory.
> d) It can only optimize single-parameter functions.
>> [!success]- Answer
>> b) It only updates parameters after evaluating the entire dataset, making it extremely slow.

> [!question] Why does Mini-batch Gradient Descent help the model "jump" out of shallow local minima?
> a) Because it uses an analytical solver.
> b) Because the noise introduced by calculating gradients on small subsets (stochastic noise) creates small oscillations.
> c) Because it sets the learning rate to zero.
> d) Because it increases the dimension of the parameter space.
>> [!success]- Answer
>> b) Because the noise introduced by calculating gradients on small subsets (stochastic noise) creates small oscillations.

> [!question] What is the default batch size range suggested in the slides for optimal speed and stability?
> a) 1 to 10
> b) 32 to 512
> c) 1000 to 5000
> d) 10000 to 100000
>> [!success]- Answer
>> b) 32 to 512

> [!question] Which loss function is highly suitable for multi-class classification and utilizes logarithms?
> a) Mean Absolute Error (MAE)
> b) Binary Cross-Entropy (BCE)
> c) Categorical Cross-Entropy (CCE)
> d) Huber Loss
>> [!success]- Answer
>> c) Categorical Cross-Entropy (CCE)

> [!question] How does the negative sign in the Binary Cross-Entropy formula affect the loss?
> a) It ensures the loss value is always negative.
> b) It transforms the negative logarithm of a probability into a positive, highly penalized cost.
> c) It cancels out the learning rate.
> d) It divides the gradients by the number of features.
>> [!success]- Answer
>> b) It transforms the negative logarithm of a probability into a positive, highly penalized cost.

> [!question] What type of variable is predicted by a Linear Regression model?
> a) Binary labels (0 or 1)
> b) Multi-class labels (0, 1, 2, or 3)
> c) Continuous numerical values
> d) Categorical text strings
>> [!success]- Answer
>> c) Continuous numerical values

> [!question] What does the term "Endogenous variable" ($Y$) refer to in a linear regression model?
> a) The independent variable determined outside the model.
> b) The dependent variable to be explained.
> c) The error term added to the features.
> d) The learning rate parameter.
>> [!success]- Answer
>> b) The dependent variable to be explained.

> [!question] In the cost function $J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=1}^m (h(x_i) - y_i)^2$, what does the term $m$ represent?
> a) The number of input features.
> b) The number of training samples.
> c) The index of the current feature.
> d) The maximum weight value.
>> [!success]- Answer
>> b) The number of training samples.

> [!question] Which mathematical formula represents Min-Max scaling of a feature $x_{ij}$?
> a) $\frac{x_{ij} - \text{Moy}_j}{\sigma_j}$
> b) $\frac{x_{ij} - \text{Min}_j}{\text{Max}_j - \text{Min}_j}$
> c) $x_{ij} \cdot \sigma_j$
> d) $\max(0, x_{ij})$
>> [!success]- Answer
>> b) $\frac{x_{ij} - \text{Min}_j}{\text{Max}_j - \text{Min}_j}$

> [!question] When we perform Z-score normalization, what does $\sigma_j$ in the denominator represent?
> a) The mean value of the feature.
> b) The standard deviation of the feature.
> c) The maximum value of the feature.
> d) The variance of the model's predictions.
>> [!success]- Answer
>> b) The standard deviation of the feature.

> [!question] If we have a classification task with outcomes $y \in \{0, 1, 2, 3\}$, what category of classification is this?
> a) Binary classification
> b) Regression classification
> c) Multi-class classification
> d) Non-linear regression
>> [!success]- Answer
>> c) Multi-class classification

> [!question] In logistic regression, what is the predicted probability $h(x)$ if the linear term $\theta^T x$ is exactly 0?
> a) 0.0
> b) 0.5
> c) 1.0
> d) -1.0
>> [!success]- Answer
>> b) 0.5

> [!question] What happens if we try to use a non-convex cost function for training a neural network with Gradient Descent?
> a) The algorithm is guaranteed to find the global minimum instantly.
> b) The algorithm may easily get trapped in local minima and fail to find the global optimum.
> c) The gradients will always become zero at the first step.
> d) The weights will grow exponentially to infinity.
>> [!success]- Answer
>> b) The algorithm may easily get trapped in local minima and fail to find the global optimum.

> [!question] In the Perceptron model, what is the role of the activation function?
> a) To calculate the sum of inputs multiplied by weights.
> b) To convert the aggregated scalar value into a target prediction or decision.
> c) To perform backpropagation of error.
> d) To scale the input values.
>> [!success]- Answer
>> b) To convert the aggregated scalar value into a target prediction or decision.

> [!question] Which of the following activation functions is recommended for hidden layers in a standard neural network?
> a) Sigmoid
> b) Softmax
> c) ReLU or Leaky ReLU
> d) Linear
>> [!success]- Answer
>> c) ReLU or Leaky ReLU

> [!question] What does "GELU" stand for in deep learning terminology?
> a) Gated Exponential Linear Unit
> b) Gaussian Error Linear Unit
> c) Gradient Enhanced Linear Unit
> d) Generalized Elastic Linear Unit
>> [!success]- Answer
>> b) Gaussian Error Linear Unit

> [!question] In backpropagation, which mathematical rule is used to compute the gradients of the loss function across multiple nested layers?
> a) L'Hôpital's Rule
> b) The Chain Rule (Règle de la chaîne)
> c) The Product Rule
> d) Euler's Formula
>> [!success]- Answer
>> b) The Chain Rule (Règle de la chaîne)

> [!question] In the vectorization of equations, if the input matrix $X$ has size $n \times (m+1)$ and the weight vector $W$ has size $(m+1) \times 1$, what is the size of the product $Z = X \cdot W$?
> a) $n \times (m+1)$
> b) $n \times 1$
> c) $(m+1) \times 1$
> d) $1 \times n$
>> [!success]- Answer
>> b) $n \times 1$

> [!question] In the MLP architecture, what is the primary role of the "bias neuron" (neurone de biais)?
> a) To multiply inputs by zero.
> b) To add a constant value that shifts the activation function to better fit the data.
> c) To compute the derivatives of the hidden layers.
> d) To select the batch size.
>> [!success]- Answer
>> b) To add a constant value that shifts the activation function to better fit the data.

> [!question] What is the difference between standard L1 and L2 regularization?
> a) L1 penalizes the sum of squared weights, while L2 penalizes the sum of absolute weights.
> b) L1 penalizes the sum of absolute weights, while L2 penalizes the sum of squared weights.
> c) L1 completely deletes half of the layers, while L2 doubles the learning rate.
> d) L1 is used for classification, while L2 is used for regression.
>> [!success]- Answer
>> b) L1 penalizes the sum of absolute weights, while L2 penalizes the sum of squared weights.

---

### Matching Questions

> [!question] Match the AI sub-field with its corresponding core concept.
>> [!example] Group A
>> a) Artificial Intelligence
>> b) Machine Learning
>> c) Deep Learning
>
>> [!example] Group B
>> n) Multi-layered neural network architectures.
>> o) Algorithmic learning from structured/unstructured data.
>> p) Simulation of human cognitive functions.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the researcher with their historical milestone.
>> [!example] Group A
>> a) Frank Rosenblatt
>> b) Yann LeCun
>> c) Ian Goodfellow
>
>> [!example] Group B
>> n) Development of Generative Adversarial Networks (GANs).
>> o) Invention of the Perceptron.
>> p) Pioneer of Convolutional Neural Networks (CNNs).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the ImageNet 2012 concept with its description.
>> [!example] Group A
>> a) ILSVRC
>> b) AlexNet
>> c) ImageNet
>
>> [!example] Group B
>> n) Database of millions of labeled images.
>> o) The large-scale visual recognition challenge.
>> p) The deep network that won the 2012 challenge.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the framework with its creator.
>> [!example] Group A
>> a) PyTorch
>> b) TensorFlow
>> c) JAX
>
>> [!example] Group B
>> n) Google (primarily for high-performance numerical computing).
>> o) Facebook (Meta).
>> p) Google Brain (widely used in production).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the optimization term with its definition.
>> [!example] Group A
>> a) Parameter space
>> b) Cost function
>> c) Analytical solution
>
>> [!example] Group B
>> n) Exact mathematical calculation to find the optimal point directly.
>> o) Multi-dimensional set of all possible parameter combinations.
>> p) Metric used to evaluate the error of a model.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the learning rate scenario with its consequence.
>> [!example] Group A
>> a) Balanced learning rate
>> b) Too high learning rate
>> c) Too low learning rate
>
>> [!example] Group B
>> n) Slow but steady convergence toward the minimum.
>> o) Fast and stable convergence.
>> p) Oscillations and potential divergence from the minimum.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the batch size category with its key characteristic.
>> [!example] Group A
>> a) Single instance (SGD)
>> b) Mini-batch
>> c) Full Batch (Classic GD)
>
>> [!example] Group B
>> n) Optimal trade-off between speed and hardware memory efficiency.
>> o) Highly noisy updates but extremely low memory footprint.
>> p) Stable updates but highly computationally expensive on large datasets.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the cost function abbreviation with its full mathematical name.
>> [!example] Group A
>> a) MSE
>> b) MAE
>> c) CCE
>
>> [!example] Group B
>> n) Categorical Cross-Entropy.
>> o) Mean Squared Error.
>> p) Mean Absolute Error.
>
>> [success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the cost function with its typical task category.
>> [!example] Group A
>> a) Mean Squared Error
>> b) Binary Cross-Entropy
>> c) Categorical Cross-Entropy
>
>> [!example] Group B
>> n) Multi-class classification.
>> o) Continuous value regression.
>> p) Binary classification.
>
>> [success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the advanced loss function with its descriptive feature.
>> [!example] Group A
>> a) Huber Loss
>> b) Hinge Loss
>> c) Log Loss
>
>> [!example] Group B
>> n) Used to force a clear separation boundary between classes.
>> o) Combines quadratic and absolute error terms based on a threshold.
>> p) Standard probabilistic cost function for classification.
>
>> [success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the variables in a linear regression model with their role.
>> [!example] Group A
>> a) Endogenous variable (Y)
>> b) Exogenous variable (X)
>> c) Parameters ($\theta$)
>
>> [!example] Group B
>> n) Values to be learned that define the line's height and slope.
>> o) Independent variable determined outside the model.
>> p) Dependent variable that is being predicted.
>
>> [success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the linear regression formula element with its definition.
>> [!example] Group A
>> a) $h(x) = \theta_0 + \theta_1 x$
>> b) $\theta_0$
>> c) $\theta_1$
>
>> [!example] Group B
>> n) Slope (weight of the input).
>> o) The linear hypothesis model.
>> p) Y-intercept (bias of the model).
>
>> [success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the feature scaling approach with its corresponding range.
>> [!example] Group A
>> a) Min-Max Scaling
>> b) Z-score Standardisation
>> c) Mean Normalisation
>
>> [!example] Group B
>> n) Centered on 0 with variance equal to 1.
>> o) Scaled strictly between 0 and 1.
>> p) Scaled between negative and positive standard deviations.
>
>> [success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the classification type with its potential output set.
>> [!example] Group A
>> a) Binary Classification
>> b) Multi-class Classification
>> c) Regression Task
>
>> [!example] Group B
>> n) Continuous real-valued output.
>> o) Discrete set such as {0, 1}.
>> p) Discrete set such as {0, 1, 2, 3}.
>
>> [success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the input boundary of the Sigmoid function with its output limit.
>> [!example] Group A
>> a) Input $z \to +\infty$
>> b) Input $z \to -\infty$
>> c) Input $z = 0$
>
>> [!example] Group B
>> n) Output approaches 0.
>> o) Output is exactly 0.5.
>> p) Output approaches 1.
>
>> [success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the logistic regression component with its representation.
>> [!example] Group A
>> a) $h(x) \geq 0.5$
>> b) $h(x) < 0.5$
>> c) $h(x) = g(\theta^T x)$
>
>> [!example] Group B
>> n) Predicting the class outcome $y = 0$.
>> o) The mathematical hypothesis function.
>> p) Predicting the class outcome $y = 1$.
>
>> [success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the cost function property with the corresponding model.
>> [!example] Group A
>> a) Convex cost landscape with MSE
>> b) Non-convex cost landscape with MSE
>> c) Convex cost landscape with Log Loss
>
>> [!example] Group B
>> n) Logistic Regression.
>> o) Linear Regression.
>> p) Multi-layered architectures using sigmoid functions.
>
>> [success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the biological neuron component with its artificial counterpart.
>> [!example] Group A
>> a) Dendrite
>> b) Soma
>> c) Axon
>
>> [!example] Group B
>> n) Input connection (with weight).
>> o) Aggregation/Activation calculation.
>> p) Output signal of the node.
>
>> [success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the Perceptron pipeline step with its description.
>> [!example] Group A
>> a) Aggregation Step
>> b) Activation Step
>> c) Weight parameter
>
>> [!example] Group B
>> n) Scales the input feature to determine its relative influence.
>> o) Applies a non-linear threshold function to the aggregated sum.
>> p) Computes the weighted sum of inputs plus bias.
>
>> [success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the activation function with its primary drawback.
>> [!example] Group A
>> a) Sigmoid
>> b) Standard ReLU
>> c) Linear Activation
>
>> [!example] Group B
>> n) Suffers from the "dead neuron" issue if inputs are negative.
>> o) Limits the model to solving only simple, linearly separable tasks.
>> p) Suffers from vanishing gradients in deep networks.
>
>> [success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the activation function formula with its name.
>> [!example] Group A
>> a) $\max(0, x)$
>> b) $\max(\alpha x, x)$
>> c) $x \cdot \text{sigmoid}(x)$
>
>> [!example] Group B
>> n) Swish.
>> o) Standard ReLU.
>> p) Leaky ReLU.
>
>> [success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the activation function with its primary developer.
>> [!example] Group A
>> a) Swish
>> b) GELU
>> c) Sigmoid
>
>> [!example] Group B
>> n) Google (based on reinforcement learning search).
>> o) Classical mathematics (logistic curve).
>> p) Dan Hendrycks (probabilistic error approximation).
>
>> [success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the architectural layer with its recommended activation function.
>> [!example] Group A
>> a) Hidden layers (Standard MLP)
>> b) Binary Classification Output
>> c) Multi-class Classification Output
>
>> [!example] Group B
>> n) Sigmoid.
>> o) ReLU or Leaky ReLU.
>> p) Softmax.
>
>> [success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the vectorized Perceptron element with its dimension.
>> [!example] Group A
>> a) Weight matrix (W)
>> b) Input matrix (X)
>> c) Output vector (Y)
>
>> [!example] Group B
>> n) $(m+1) \times 1$.
>> o) $n \times (m+1)$.
>> p) $n \times 1$.
>
>> [success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the Multi-Layer Perceptron (MLP) component with its description.
>> [!example] Group A
>> a) Input Layer
>> b) Hidden Layer
>> c) Output Layer
>
>> [!example] Group B
>> n) Represents the predicted output classes or values.
>> o) Intermediary representation of features (unseen by user).
>> p) Directly reads raw input features.
>
>> [success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the MLP Forward Pass step with its correct order.
>> [!example] Group A
>> a) Step 1
>> b) Step 2
>> c) Step 3
>
>> [!example] Group B
>> n) Compute activation values for each layer sequentially.
>> o) Accept raw feature inputs.
>> p) Calculate predictions at the final output layer.
>
>> [success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the MLP Backward Pass step with its correct order.
>> [!example] Group A
>> a) Step 1
>> b) Step 2
>> c) Step 3
>
>> [!example] Group B
>> n) Use optimization algorithm (SGD) to adjust weights.
>> o) Compute prediction error using the loss function.
>> p) Calculate gradients sequentially from output to input.
>
>> [success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the data preprocessing task with its main objective.
>> [!example] Group A
>> a) Imputation
>> b) One-Hot Encoding
>> c) Feature Scaling
>
>> [!example] Group B
>> n) Convert categories into numeric values.
>> o) Handle missing values in the dataset.
>> p) Ensure all numeric features share a similar scale.
>
>> [success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the prevention method with its regularization category.
>> [!example] Group A
>> a) Dropout
>> b) Early Stopping
>> c) L2 regularization
>
>> [!example] Group B
>> n) Halting training based on validation metrics.
>> o) Randomly dropping nodes during the training phase.
>> p) Penalizing the square of parameter magnitudes.
>
>> [success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the dataset split with its primary operational purpose.
>> [!example] Group A
>> a) Training Set
>> b) Validation Set
>> c) Test Set
>
>> [!example] Group B
>> n) Tune hyperparameters and check for early signs of overfitting.
>> o) Provide final, unbiased evaluation of the fully trained model.
>> p) Learn model weights and biases directly from data.
>
>> [success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)