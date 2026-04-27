---
sources:
  - "[[21. Model Evaluation Metrics Beyond Accuracy]]"
---
> [!question] Accuracy is a reliable metric for all types of datasets.
>> [!success]- Answer
>> False

> [!question] A model that always predicts the majority class will always have high accuracy.
>> [!success]- Answer
>> True

> [!question] In a balanced dataset, accuracy is an appropriate evaluation metric.
>> [!success]- Answer
>> True

> [!question] False negatives are generally more dangerous than false positives in medical diagnosis.
>> [!success]- Answer
>> True

> [!question] A confusion matrix can only be used for binary classification problems.
>> [!success]- Answer
>> False

> [!question] In a dataset with 990 healthy patients and 10 diseased patients, a model that always predicts "healthy" will have 99% accuracy.
>> [!success]- Answer
>> True

> [!question] True Positives represent instances where the model incorrectly identifies a negative case as positive.
>> [!success]- Answer
>> False

> [!question] Precision and recall are derived from the confusion matrix.
>> [!success]- Answer
>> True

> [!question] High accuracy on an imbalanced dataset guarantees good model performance.
>> [!success]- Answer
>> False

> [!question] False positives in medical screening lead to unnecessary treatment and wasted resources.
>> [!success]- Answer
>> True

> [!question] What is the primary limitation of accuracy as an evaluation metric?
> a) It's computationally expensive
> b) It doesn't account for class imbalance
> c) It only works for linear models
> d) It requires large datasets
>> [!success]- Answer
>> b) It doesn't account for class imbalance

> [!question] In a medical diagnosis scenario with a rare disease, which type of error is typically more dangerous?
> a) False positive
> b) False negative
> c) Both are equally dangerous
> d) Neither is particularly dangerous
>> [!success]- Answer
>> b) False negative

> [!question] A model has 100 true positives, 50 false positives, 20 false negatives, and 830 true negatives. What is the accuracy?
> a) 89%
> b) 93%
> c) 95%
> d) 97%
>> [!success]- Answer
>> b) 93%

> [!question] What does a precision metric measure?
> a) The proportion of actual positives that are correctly identified
> b) The proportion of predicted positives that are actual positives
> c) The balance between precision and recall
> d) The overall model performance
>> [!success]- Answer
>> b) The proportion of predicted positives that are actual positives

> [!question] In the confusion matrix, what does a True Negative represent?
> a) The model incorrectly predicts negative when the actual is positive
> b) The model correctly predicts negative when the actual is negative
> c) The model incorrectly predicts positive when the actual is negative
> d) The model correctly predicts positive when the actual is positive
>> [!success]- Answer
>> b) The model correctly predicts negative when the actual is negative

> [!question] If a model has high recall but low precision, what does this indicate?
> a) The model makes many false alarms but catches most actual positives
> b) The model has balanced performance between precision and recall
> c) The model misses many actual positives but has few false alarms
> d) The model performs poorly on all metrics
>> [!success]- Answer
>> a) The model makes many false alarms but catches most actual positives

> [!question] Which scenario would make accuracy a particularly misleading metric?
> a) A balanced dataset with equal representation of all classes
> b) A dataset with severe class imbalance
> c) A dataset with only one class
> d) A small dataset
>> [!success]- Answer
>> b) A dataset with severe class imbalance

> [!question] What is the F1 score?
> a) The harmonic mean of precision and recall
> b) The arithmetic mean of precision and recall
> c) The minimum of precision and recall
> d) The maximum of precision and recall
>> [!success]- Answer
>> a) The harmonic mean of precision and recall

> [!question] In fraud detection, which type of error is typically more costly?
> a) False positive (legitimate transaction flagged as fraud)
> b) False negative (fraudulent transaction missed)
> c) Both errors are equally costly
> d) Neither error is particularly costly
>> [!success]- Answer
>> b) False negative (fraudulent transaction missed)

> [!question] What is specificity?
> a) The proportion of actual negatives that are correctly identified
> b) The proportion of actual positives that are correctly identified
> c) The balance between precision and recall
> d) The overall model performance
>> [!success]- Answer
>> a) The proportion of actual negatives that are correctly identified

> [!question] Match the confusion matrix components with their definitions.
>> [!example] Group A
>> a) True Positive
>> b) False Negative
>> c) False Positive
>
>> [!example] Group B
>> n) Model predicts positive when actual is negative
>> o) Model predicts positive when actual is positive
>> p) Model predicts negative when actual is positive
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the evaluation metrics with their formulas.
>> [!example] Group A
>> a) Precision
>> b) Recall
>> c) F1 Score
>
>> [!example] Group B
>> n) TP / (TP + FP)
>> o) 2 × (Precision × Recall) / (Precision + Recall)
>> p) TP / (TP + FN)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the scenarios with their appropriate evaluation metrics.
>> [!example] Group A
>> a) Medical diagnosis of a deadly disease
>> b) Spam email detection
>> c) Credit card fraud detection
>
>> [!example] Group B
>> n) High recall (minimize false negatives)
>> o) High precision (minimize false positives)
>> p) Balanced precision and recall
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the types of errors with their consequences in medical diagnosis.
>> [!example] Group A
>> a) False Positive
>> b) False Negative
>> c) True Negative
>
>> [!example] Group B
>> n) Patient receives unnecessary treatment
>> o) Patient's condition goes untreated
>> p) No unnecessary treatment or alarm
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the metrics with what they primarily measure.
>> [!example] Group A
>> a) Accuracy
>> b) Specificity
>> c) F1 Score
>
>> [!example] Group B
>> n) Overall correctness of predictions
>> o) Ability to correctly identify negative cases
>> p) Balance between precision and recall
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the evaluation scenarios with their appropriate metrics.
>> [!example] Group A
>> a) Imbalanced dataset with important minority class
>> b) Balanced dataset with equal importance for all classes
>> c) When both false positives and false negatives are equally costly
>
>> [!example] Group B
>> n) Precision and recall
>> o) Accuracy
>> p) F1 Score
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the metric types with their sensitivity to class imbalance.
>> [!example] Group A
>> a) Accuracy
>> b) Precision and Recall
>> c) F1 Score
>
>> [!example] Group B
>> n) Highly sensitive to class imbalance
>> o) Moderately sensitive to class imbalance
>> p) Less sensitive to class imbalance
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the evaluation metrics with their focus areas.
>> [!example] Group A
>> a) True Positive Rate
>> b) False Positive Rate
>> c) True Negative Rate
>
>> [!example] Group B
>> n) Proportion of actual negatives incorrectly classified
>> o) Proportion of actual positives correctly classified
>> p) Proportion of actual negatives correctly classified
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the model evaluation scenarios with their appropriate metrics.
>> [!example] Group A
>> a) When false positives are very costly
>> b) When false negatives are very costly
>> c) When both types of errors have similar costs
>
>> [!example] Group B
>> n) High precision
>> o) High recall
>> p) Balanced precision and recall
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the evaluation metrics with their mathematical properties.
>> [!example] Group A
>> a) Precision
>> b) Recall
>> c) F1 Score
>
>> [!example] Group B
>> n) Can be misleading with imbalanced data
>> o) Focuses on minimizing false positives
>> p) Harmonic mean of precision and recall
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the classification problems with their appropriate evaluation metrics.
>> [!example] Group A
>> a) Rare disease detection
>> b) Spam filtering
>> c) Sentiment analysis
>
>> [!example] Group B
>> n) High recall (minimize false negatives)
>> o) High precision (minimize false positives)
>> p) Balanced metrics (F1 score)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
