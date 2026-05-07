# Chapter 5: Advanced Training Strategies and Loss Functions

## 10. Gradient Accumulation and Gradient Clipping Mechanics

**The VRAM Wall:**
To achieve a stable gradient that accurately represents the dataset distribution, you need a large batch size. However, passing a batch of 192 high-resolution (384x1280) images through an 88-million parameter SwinV2 encoder and a 10-layer decoder requires far more than the 96GB of VRAM available on an RTX 6000 Ada.

**The Solution: Gradient Accumulation**
In `engine.py`, you implemented a `train_step` with `accumulation_steps = 6`, running a physical batch size of 36.
1.  **Forward Pass 1:** Pass 36 images. Compute the loss.
2.  **Divide the Loss:** `loss = loss / 6`. This is mathematically critical. Without division, the gradients would sum up and act like a learning rate multiplier of 6x, blowing up the training.
3.  **Backward Pass 1:** Compute gradients and *accumulate* (add) them into the `.grad` attributes of the weights.
4.  **Repeat 6 times.**
5.  **Optimizer Step:** Only after 6 iterations (effectively $36 \times 6 = 216$ images) do you call `optimizer.step()` to update the weights, followed by `optimizer.zero_grad()` to clear the cache.

**Gradient Clipping (`max_grad_norm = 1.0`):**
In deep networks (especially Transformers), the error surface can have steep "cliffs". If a batch contains highly unusual images, the computed gradient might be massive. If the optimizer takes a massive step, it destroys the model weights (a NaN explosion). 
Before taking a step, `torch.nn.utils.clip_grad_norm_` calculates the global L2 norm of all gradients. If the norm exceeds `1.0`, it scales the entire gradient vector down. The direction of the learning step remains exactly the same, but the magnitude is safely capped.