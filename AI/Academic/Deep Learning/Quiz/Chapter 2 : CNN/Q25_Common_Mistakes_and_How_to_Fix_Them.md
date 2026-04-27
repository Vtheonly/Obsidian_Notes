---
sources:
  - "[[25. Common Mistakes and How to Fix Them]]"
---
> [!question] Forgetting to call `optimizer.zero_grad()` before each backward pass in PyTorch will cause gradients to accumulate across iterations.
>> [!success]- Answer
>> True

> [!question] When evaluating a model in PyTorch, it's important to call `model.train()` to ensure consistent results.
>> [!success]- Answer
>> False

> [!question] The primary symptom of forgetting `optimizer.zero_grad()` is that training loss decreases steadily and consistently.
>> [!success]- Answer
>> False

> [!question] BatchNorm layers in evaluation mode use the running mean and variance accumulated during training.
>> [!success]- Answer
>> True

> [!question] Dropout layers remain active during evaluation in PyTorch by default.
>> [!success]- Answer
>> False

> [!question] When using gradient accumulation, you should call `optimizer.zero_grad()` every N batches rather than every batch.
>> [!success]- Answer
>> True

> [!question] The placement of `optimizer.zero_grad()` doesn't matter as long as it's called once per training iteration.
>> [!success]- Answer
>> True

> [!question] Forgetting `model.eval()` during evaluation typically causes validation accuracy to be higher than expected.
>> [!success]- Answer
>> False

> [!question] PyTorch automatically handles mode switching between training and evaluation for layers like Dropout and BatchNorm.
>> [!success]- Answer
>> False

> [!question] When using `torch.no_grad()`, you still need to call `model.eval()` to ensure proper behavior of certain layers.
>> [!success]- Answer
>> True

> [!question] What happens if you forget to call `optimizer.zero_grad()` before each backward pass?
> a) The gradients will be reset to zero, causing no updates
> b) Gradients from previous iterations accumulate, leading to incorrect updates
> c) The optimizer will automatically handle gradient accumulation
> d) PyTorch will raise an error
>> [!success]- Answer
>> b) Gradients from previous iterations accumulate, leading to incorrect updates

> [!question] Which of the following is NOT a symptom of forgetting `optimizer.zero_grad()`?
> a) Training loss decreases erratically
> b) Model becomes unstable after initial learning
> c) Loss suddenly spikes to very large values
> d) Training accuracy improves steadily
>> [!success]- Answer
>> d) Training accuracy improves steadily

> [!question] What is the purpose of calling `model.eval()` before evaluation?
> a) To enable dropout for regularization
> b) To use batch statistics instead of running statistics
> c) To disable dropout and use running statistics for BatchNorm
> d) To increase model capacity
>> [!success]- Answer
>> c) To disable dropout and use running statistics for BatchNorm

> [!question] Where should `optimizer.zero_grad()` typically be placed in a training loop?
> a) After `optimizer.step()`
> b) Before `loss.backward()`
> c) After `loss.backward()`
> d) It doesn't matter as long as it's called once per iteration
>> [!success]- Answer
>> b) Before `loss.backward()`

> [!question] What happens to BatchNorm layers during evaluation if you forget to call `model.eval()`?
> a) They use the running mean and variance
> b) They use the current batch's mean and variance
> c) They are disabled
> d) They raise an error
>> [!success]- Answer
>> b) They use the current batch's mean and variance

> [!question] Which of these scenarios would make the impact of forgetting `model.eval()` most severe?
> a) Evaluating with large batch sizes
> b) Evaluating with small batch sizes
> c) Evaluating a model without BatchNorm
> d) Evaluating with `torch.no_grad()`
>> [!success]- Answer
>> b) Evaluating with small batch sizes

> [!question] What is the effect of Dropout layers remaining active during evaluation?
> a) Predictions become deterministic and stronger
> b) Predictions become stochastic and potentially weaker
> c) The model trains faster
> d) No effect on predictions
>> [!success]- Answer
>> b) Predictions become stochastic and potentially weaker

> [!question] When would you intentionally use gradient accumulation in PyTorch?
> a) When you want to accumulate gradients across multiple mini-batches
> b) When you want to reset gradients more frequently
> c) When you want to disable gradient computation
> d) When you want to increase learning rate
>> [!success]- Answer
>> a) When you want to accumulate gradients across multiple mini-batches

> [!question] Which of the following is NOT a layer that behaves differently between training and evaluation modes in PyTorch?
> a) Dropout
> b) BatchNorm
> c) Linear
> d) InstanceNorm
>> [!success]- Answer
>> c) Linear

> [!question] Match the mistake with its correct fix.
>> [!example] Mistake
>> a) Forgetting optimizer.zero_grad()
>> b) Forgetting model.eval() during evaluation
>> c) Using training mode during validation
>>
>> [!example] Fix
>> n) Call optimizer.zero_grad() before backward pass
>> o) Call model.eval() before evaluation
>> p) Call model.eval() before evaluation
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the mistake with its primary symptom.
>> [!example] Mistake
>> a) Forgetting optimizer.zero_grad()
>> b) Forgetting model.eval() during evaluation
>> c) Using training mode during validation
>>
>> [!example] Symptom
>> n) Erratic training loss or sudden spikes
>> o) Lower than expected validation accuracy
>> p) Inconsistent validation metrics across runs
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the layer with its behavior in training mode.
>> [!example] Layer
>> a) Dropout
>> b) BatchNorm
>> c) InstanceNorm
>>
>> [!example] Behavior in Training Mode
>> n) Uses current batch's mean and variance
>> o) Randomly zeros neurons
>> p) Normalizes each channel separately
>>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the layer with its behavior in evaluation mode.
>> [!example] Layer
>> a) Dropout
>> b) BatchNorm
>> c) LayerNorm
>>
>> [!example] Behavior in Evaluation Mode
>> n) Uses running mean and variance
>> o) All neurons active, outputs scaled
>> p) Normalizes across all features
>>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the PyTorch function with its purpose.
>> [!example] Function
>> a) optimizer.zero_grad()
>> b) model.eval()
>> c) torch.no_grad()
>>
>> [!example] Purpose
>> n) Disables gradient computation
>> o) Switches model to evaluation mode
>> p) Clears gradients from previous iteration
>>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the mistake with its explanation.
>> [!example] Mistake
>> a) Forgetting optimizer.zero_grad()
>> b) Forgetting model.eval() during evaluation
>> c) Using training mode during validation
>>
>> [!example] Explanation
>> n) Gradients accumulate instead of being replaced
>> o) Dropout remains active, BatchNorm uses batch stats
>> p) Predictions become stochastic and unreliable
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the scenario with its recommended action.
>> [!example] Scenario
>> a) Standard training loop
>> b) Gradient accumulation with batch size 128, desired effective batch size 512
>> c) Model evaluation
>>
>> [!example] Action
>> n) Call optimizer.zero_grad() every batch
>> o) Call optimizer.zero_grad() every 4 batches
>> p) Call model.eval() and use torch.no_grad()
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the layer with its typical training mode behavior.
>> [!example] Layer
>> a) Dropout
>> b) BatchNorm
>> c) GroupNorm
>>
>> [!example] Training Mode Behavior
>> n) Normalizes within each group
>> o) Randomly drops neurons
>> p) Normalizes using current batch statistics
>>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the mistake with its impact on model performance.
>> [!example] Mistake
>> a) Forgetting optimizer.zero_grad()
>> b) Forgetting model.eval() during evaluation
>> c) Using training mode during validation
>>
>> [!example] Impact
>> n) Training becomes unstable or oscillates
>> o) Validation accuracy degraded by 1-5%
>> p) Inconsistent results across validation runs
>>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the PyTorch component with its default behavior.
>> [!example] Component
>> a) optimizer.step()
>> b) loss.backward()
>> c) model.train()
>>
>> [!example] Default Behavior
>> n) Switches layers to training mode
>> o) Accumulates gradients with existing ones
>> p) Updates model parameters using gradients
>>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
