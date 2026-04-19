## 8.3 Cloud Integration and Persistence

### The Problem: Ephemeral Cloud Sessions

Kaggle and Google Colab sessions are ephemeral compute environments. They provide powerful GPUs (T4, P100, A100) for free or at low cost, but with hard session time limits:
- Kaggle: 12 hours maximum per session on GPU.
- Colab Free: 3-6 hours (quota-dependent).
- Colab Pro: 12-24 hours.

Training TAMER from scratch to full convergence takes 60-120 hours of GPU time. No single cloud session can complete this. The training must be interrupted and resumed across many sessions.

The naive approach: save a checkpoint at the end of the session. But if the session crashes unexpectedly (OOM, network error, session timeout without clean shutdown), the checkpoint may not be saved. Weeks of training time can be lost to a single unexpected crash.

---

### The TAMER Persistence Architecture

TAMER uses a multi-layered persistence strategy designed to be fault-tolerant, cloud-agnostic, and automatically resumable.

#### Layer 1: Local Checkpointing (Every N Steps)

The training loop saves a local checkpoint every $N$ gradient steps (configurable, default 500 steps):

```python
def save_checkpoint(model, optimizer, scaler, scheduler,
                    epoch, step, loss, path):
    checkpoint = {
        'epoch': epoch,
        'step': step,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'scaler_state_dict': scaler.state_dict(),
        'scheduler_state_dict': scheduler.state_dict(),
        'loss': loss,
        'config': model.config,
    }
    # Atomic write: write to temp file then rename
    # This prevents a corrupt checkpoint if the session dies mid-write
    temp_path = path + '.tmp'
    torch.save(checkpoint, temp_path)
    os.rename(temp_path, path)
```

The atomic write pattern (write to `.tmp` then rename) is critical. If the session dies in the middle of writing a checkpoint file, the `.tmp` file is incomplete and corrupt. The rename operation is atomic at the OS level: the old checkpoint is not replaced until the new one is fully written. Therefore, you always have at least one valid checkpoint, even after an unexpected crash.

#### Layer 2: Background Upload to Hugging Face Hub

Local Kaggle session files are lost when the session ends. TAMER runs a background daemon thread that periodically uploads checkpoints to the Hugging Face Hub (a free model repository with large storage limits):

```python
import threading
from huggingface_hub import HfApi

class BackgroundCheckpointUploader:
    def __init__(self, repo_id, upload_interval_steps=500):
        self.api = HfApi()
        self.repo_id = repo_id
        self.upload_interval = upload_interval_steps
        self.queue = []
        self.thread = threading.Thread(
            target=self._upload_loop,
            daemon=True  # Dies when main process dies
        )
        self.thread.start()
    
    def schedule_upload(self, checkpoint_path, step):
        self.queue.append((checkpoint_path, step))
    
    def _upload_loop(self):
        while True:
            if self.queue:
                path, step = self.queue.pop(0)
                try:
                    self.api.upload_file(
                        path_or_fileobj=path,
                        path_in_repo=f"checkpoints/step_{step}.pt",
                        repo_id=self.repo_id,
                    )
                except Exception as e:
                    # Never crash the uploader. Log and retry next cycle.
                    print(f"Upload failed: {e}. Will retry.")
                    self.queue.insert(0, (path, step))
            time.sleep(30)  # Check every 30 seconds
```

**Why a daemon thread?**
The `daemon=True` flag means the thread automatically terminates when the main training process terminates. You do not need to explicitly join or kill it. This prevents the training script from hanging after training completes, waiting for the upload thread to finish.

**Why not the main thread?**
The Hugging Face Hub upload involves network I/O, which is slow and unpredictable. If the upload is on the main thread, the GPU sits idle during every upload (potentially minutes). The background thread allows the GPU to continue training while the upload happens in parallel on the CPU.

#### Layer 3: Automatic Resume (`_auto_resume`)

When a new session starts, the `_auto_resume` function automatically pulls the latest checkpoint from the Hugging Face Hub and restores all training state:

```python
def auto_resume(model, optimizer, scaler, scheduler, repo_id):
    api = HfApi()
    
    # List all checkpoints sorted by step number
    files = api.list_repo_files(repo_id)
    checkpoints = [f for f in files if f.startswith('checkpoints/step_')]
    
    if not checkpoints:
        print("No remote checkpoint found. Starting from scratch.")
        return 0, 0  # epoch=0, step=0
    
    # Find the checkpoint with the highest step number
    latest = max(checkpoints, key=lambda f: int(f.split('_')[-1].split('.')[0]))
    
    # Download to local disk
    local_path = api.hf_hub_download(repo_id=repo_id, filename=latest)
    
    # Load and restore all state
    checkpoint = torch.load(local_path, map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    scaler.load_state_dict(checkpoint['scaler_state_dict'])
    scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
    
    epoch = checkpoint['epoch']
    step = checkpoint['step']
    
    print(f"Resumed from epoch {epoch}, step {step}")
    return epoch, step
```

The combination of all three layers means:
- **Within a session:** Local checkpoints every 500 steps guarantee at most 500 steps of lost work on unexpected crash.
- **Across sessions:** Hugging Face Hub persistence guarantees that training state survives session termination.
- **On restart:** Auto-resume restores exactly where training left off, including optimizer momentum, learning rate schedule position, and gradient scaler state.

> **Critical reminder:** When resuming from a checkpoint, you must also restore the **curriculum sampler state**. If you resume at epoch 35 (which should be in Phase 3 of the curriculum) but the sampler re-initializes to Phase 1, the model trains on easy data that it mastered long ago. This wastes GPU time and may cause slight regression on complex formulas. The checkpoint should save `current_epoch` and the sampler should call `set_epoch(current_epoch)` on resume.

---

### Kaggle-Specific Considerations

#### Read-Only Input Directories

Kaggle separates datasets into `/kaggle/input/` (read-only, persistent across sessions) and `/kaggle/working/` (writable, wiped at session end).

This creates a trap: if your preprocessing code generates a cache manifest and tries to write it back to `/kaggle/input/dataset/manifest.json`, it throws `PermissionError: [Errno 13] Permission denied`. If this error is not caught, the entire preprocessing script crashes. If it is naively caught and ignored, the manifest is never saved, and the dataset re-preprocesses on every session restart.

TAMER handles this with a two-tier manifest storage strategy:
1. Always attempt to write the manifest to the source directory.
2. If that raises `OSError` (permission denied), silently fall back to writing the manifest to `/kaggle/working/tamer_cache/manifest.json`.
3. On startup, check both locations for a valid manifest.

```python
def save_manifest(manifest, primary_path, fallback_path):
    try:
        os.makedirs(os.path.dirname(primary_path), exist_ok=True)
        with open(primary_path, 'w') as f:
            json.dump(manifest, f)
        return primary_path
    except OSError:
        os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
        with open(fallback_path, 'w') as f:
            json.dump(manifest, f)
        return fallback_path
```

#### Session Memory Management During Long Training

Over 12 hours of continuous training in a single Kaggle session, Python's memory can gradually accumulate unreleased references. Common sources:
- Matplotlib figures created for loss plotting but never closed (`plt.close()` never called).
- Validation outputs accumulated in a list for BLEU computation that is never cleared between validation runs.
- PyTorch tensors moved to CPU for logging but still in memory because the logging list holds a reference.

TAMER's training loop performs explicit memory auditing every 50 epochs:

```python
import gc

def periodic_memory_cleanup(step, interval=50):
    if step % interval == 0:
        gc.collect()           # Force Python GC
        torch.cuda.empty_cache()  # Release PyTorch CUDA memory cache
```

`torch.cuda.empty_cache()` does not free memory that is actively in use. It only releases memory that PyTorch has already freed internally but is holding in a cache for fast reallocation. Calling it periodically keeps the CUDA memory fragmentation low over long training runs.

> **Important reminder:** `torch.cuda.empty_cache()` does NOT solve OOM errors caused by actual memory leaks (references still held). If you are getting OOM during training, `empty_cache()` will not help. You must find and remove the reference that is keeping the tensor alive. The most common culprits are: appending tensors to a list for accumulation without calling `.detach()` first, creating large intermediate tensors inside evaluation loops without `torch.no_grad()`, and storing the full model output for logging when only the loss scalar is needed.

---

*End of TAMER Math OCR - Deep Learning Theory & Architecture Vault*