---
sources:
  - "[[26. Demystifying the Black Box - CNN Interpretability]]"
---
> [!question] Convolutional Neural Networks are often referred to as "black boxes" because we don't know why they make certain predictions.
>> [!success]- Answer
>> True

> [!question] High accuracy in a CNN model guarantees that it has learned meaningful patterns.
>> [!success]- Answer
>> False

> [!question] Grad-CAM was introduced in 2017 by Selvaraju et al.
>> [!success]- Answer
>> True

> [!question] The European Union's General Data Protection Regulation (GDPR) includes a "right to explanation" for automated system decisions.
>> [!success]- Answer
>> True

> [!question] In medical diagnosis, interpretability is not important as long as the model achieves high accuracy.
>> [!success]- Answer
>> False

> [!question] The last convolutional layer of a CNN has the highest spatial resolution and semantic richness.
>> [!success]- Answer
>> True

> [!question] Grad-CAM produces a heatmap highlighting regions of an input image that are important for a CNN's prediction of a particular class.
>> [!success]- Answer
>> True

> [!question] Autonomous driving systems do not require interpretability as long as they make correct decisions.
>> [!success]- Answer
>> False

> [!question] The EU AI Act passed in 2024 strengthens interpretability requirements for high-risk AI systems.
>> [!success]- Answer
>> True

> [!question] Earlier layers in a CNN capture high-level semantic features while later layers capture low-level features.
>> [!success]- Answer
>> False

> [!question] Which of the following is NOT a domain where interpretability is critical?
> a) Autonomous Driving
> b) Medical Diagnosis
> c) Image Classification
> d) Legal Compliance
>> [!success]- Answer
>> c) Image Classification

> [!question] What is the primary purpose of Grad-CAM?
> a) To increase the accuracy of CNNs
> b) To identify which spatial locations influence a CNN's prediction for a specific class
> c) To reduce the computational complexity of CNNs
> d) To generate new images
>> [!success]- Answer
>> b) To identify which spatial locations influence a CNN's prediction for a specific class

> [!question] Which layer in a CNN is considered the "sweet spot" for Grad-CAM?
> a) The first convolutional layer
> b) The last fully connected layer
> c) The last convolutional layer
> d) The pooling layer
>> [!success]- Answer
>> c) The last convolutional layer

> [!question] According to the text, what might a CNN trained for medical diagnosis learn to exploit?
> a) Clinically relevant features
> b) Hospital watermarks
> c) Patient names
> d) Image resolution
>> [!success]- Answer
>> b) Hospital watermarks

> [!question] What is the first step in the Grad-CAM process?
> a) Backprop gradient to last conv layer
> b) Get feature maps from last conv layer
> c) Forward pass to get predicted class
> d) Upsample and overlay on original image
>> [!success]- Answer
>> c) Forward pass to get predicted class

> [!question] Why is interpretability important for debugging and model improvement?
> a) It allows engineers to increase model accuracy
> b) It reveals data quality issues and architectural problems
> c) It reduces the training time
> d) It decreases model complexity
>> [!success]- Answer
>> b) It reveals data quality issues and architectural problems

> [!question] What does the FDA require for AI-based diagnostic tools?
> a) Maximum accuracy
> b) Evidence that decisions are based on clinically relevant features
> c) Minimum computational requirements
> d) Open-source implementation
>> [!success]- Answer
>> b) Evidence that decisions are based on clinically relevant features

> [!question] What does the "right to explanation" in GDPR allow individuals to do?
> a) Request deletion of their data
> b) Understand why an automated system made a decision about them
> c) Opt out of automated decision-making
> d) Access all their data
>> [!success]- Answer
>> b) Understand why an automated system made a decision about them

> [!question] What is the key insight behind Grad-CAM?
> a) Earlier layers capture both spatial and semantic information
> b) The last convolutional layer retains spatial information and has semantic richness
> c) Fully connected layers contain the most important features
> d) Pooling layers preserve spatial information
>> [!success]- Answer
>> b) The last convolutional layer retains spatial information and has semantic richness

> [!question] Match the following Grad-CAM steps with their descriptions.
>> [!example] Steps
>> a) Forward pass → Get predicted class c
>> b) Backprop gradient ∂yᶜ/∂Aᵏ to last conv layer
>> c) Weighted combination + ReLU → Lᶜ
>> d) Global avg pool gradients → weights αₖ
>> e) Upsample & overlay on original image
>> f) Target last conv layer → Get feature maps Aᵏ
>
>> [!example] Descriptions
>> n) Combine feature maps with gradient weights and apply ReLU
>> o) Calculate average of gradients across spatial dimensions to get importance weights
>> p) Identify the class the model is predicting
>> q) Compute gradients of the class score with respect to feature maps
>> r) Resize the heatmap to match original image size and overlay
>> s) Extract feature maps from the last convolutional layer
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)
>> e) -> r)
>> f) -> s)

> [!question] Match the following domains with their specific interpretability requirements.
>> [!example] Domains
>> a) Autonomous Driving
>> b) Medical Diagnosis
>> c) Legal Compliance
>> d) Debugging and Model Improvement
>
>> [!example] Requirements
>> n) Evidence that decisions are based on clinically relevant features
>> o) Verification that models attend to correct visual features
>> p) Understanding why an automated system made a decision
>> q) Revealing data quality issues and architectural problems
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)

> [!question] Match the following CNN layers with their primary characteristics.
>> [!example] Layers
>> a) Earlier layers
>> b) Later layers
>> c) Last convolutional layer
>
>> [!example] Characteristics
>> n) Capture high-level semantic features
>> o) Represent a sweet spot with both spatial and semantic information
>> p) Capture low-level features
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the following interpretability techniques with their purposes.
>> [!example] Techniques
>> a) Grad-CAM
>> b) Simple Activation Mapping
>> c) Gradient-based methods
>
>> [!example] Purposes
>> n) Shows where the model looks for a specific class
>> o) Shows general regions the model looks at
>> p) Uses gradient information to highlight important regions
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following model failure scenarios with their potential causes.
>> [!example] Scenarios
>> a) Model achieves high accuracy but fails in deployment
>> b) Model performs well on training data but poorly on validation data
>> c) Model makes consistent errors on specific image types
>
>> [!example] Causes
>> n) Overfitting to spurious features in training data
>> o) Learning irrelevant features that correlate with labels
>> p) Dataset bias or insufficient diversity
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the following regulatory frameworks with their requirements.
>> [!example] Frameworks
>> a) GDPR
>> b) EU AI Act
>> c) FDA regulations for AI
>
>> [!example] Requirements
>> n) "Right to explanation" for automated decisions
>> o) Strengthened requirements for high-risk AI systems
>> p) Evidence that AI-based tools make decisions based on clinically relevant features
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following components of Grad-CAM with their roles.
>> [!example] Components
>> a) Feature maps Aᵏ
>> b) Gradients ∂yᶜ/∂Aᵏ
>> c) Weights αₖ
>> d) ReLU on Lᶜ
>
>> [!example] Roles
>> n) Spatial information from last conv layer
>> o) Importance weights for each feature map
>> p) Gradient information showing influence on class prediction
>> q) Ensuring only positive contributions are highlighted
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
>> d) -> q)

> [!question] Match the following CNN interpretability applications with their benefits.
>> [!example] Applications
>> a) Medical diagnosis
>> b) Autonomous driving
>> c) Model debugging
>
>> [!example] Benefits
>> n) Building trust with doctors and patients
>> o) Verifying detection of correct visual features
>> p) Identifying data quality issues and architectural problems
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the following concepts with their definitions in the context of CNN interpretability.
>> [!example] Concepts
>> a) Class-discriminative
>> b) Coarse heatmap
>> c) Spatial resolution
>
>> [!example] Definitions
>> n) Ability to distinguish between different classes
>> o) Detailed spatial information about where features are located
>> p) Low-resolution visualization showing important regions
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the following model properties with their implications for interpretability.
>> [!example] Properties
>> a) High accuracy
>> b) Exploiting shortcuts
>> c) Learning meaningful patterns
>
>> [!example] Implications
>> n) Model makes predictions for the right reasons
>> o) Model may fail catastrophically in new environments
>> p) Does not guarantee meaningful learning
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
