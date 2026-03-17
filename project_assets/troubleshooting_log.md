# Technical Troubleshooting & Setup Reference

This log serves as a permanent reference for project environment configuration, dependency resolution, and hardware optimization. I will use this as a guide for future projects involving local LLMs and GPU acceleration.

---

## 1. PyTorch & Torchvision failing to recognize NVIDIA GPU

### **PyTorch default installation lacks CUDA kernels**

When I ran my ingestion scripts, I received `RuntimeError: operator torchvision::nms does not exist` and `ModuleNotFoundError: Could not import module 'PreTrainedModel'`.

- **The Cause:** Standard package managers often install the CPU-only version of PyTorch on Windows (`+cpu`). This version lacks the C++ CUDA kernels required for GPU-accelerated operations like Non-Maximum Suppression (NMS).
- **The Complexity:** PyTorch maintains a separate wheel index for CUDA. If you don't explicitly point your installer there, it defaults to the lighter, non-GPU version.

### **Configured explicit CUDA 13.0 index and restricted Python version**

1. **Index Strategy:** I added the official PyTorch CUDA index to my `pyproject.toml` to ensure the library looks there first:

    ```toml
    [[tool.uv.index]]
    url = "https://download.pytorch.org/whl/cu130"
    ```

2. **Version Pinning:** I manually forced the CUDA-specific versions in `dependencies` using the `+cu130` suffix:

    ```toml
    "torch==2.10.0+cu130",
    "torchvision==0.25.0+cu130"
    ```

3. **Handling Dependency Conflicts:** `uv` initially failed because it tried to resolve packages for Python 3.14 (which lacks stable CUDA wheels). I fixed this by restricting the project to `requires-python = "==3.12.*"`.
4. **Index Trust:** I used the `--index-strategy unsafe-best-match` flag. This was critical because some secondary packages (like `markupsafe`) were missing on the PyTorch index; this flag allowed `uv` to grab the model weights from the PyTorch index while pulling standard libraries from PyPI.

---

## 2. Kaggle CLI Authentication failure

### **Missing kaggle.json file in user home directory**

The Kaggle CLI by default looks for a JSON file in `C:\Users\Name\.kaggle\kaggle.json`. This makes the project less portable and harder to set up on new machines.

### **Implemented Environment-based Authentication**

1. **Token Retrieval:** I generated a "Kaggle API Token" from the website settings.
2. **Dotenv Persistence:** Instead of creating a file in my system folders, I added the token to a local `.env` file:

    ```bash
    KAGGLE_API_TOKEN="KGAT_c6854ce6ed2b1bcb8115a94f8734a1fd"
    ```

3. **uv Integration:** I verified that `uv run` automatically injects `.env` variables into the process. This is the "cleanest" way to handle secrets without polluting the global system state.

---

## 3. Qdrant local database files appearing in Git

### **Binary database files polluting the repository**

My `qdrant_data/` directory, which stores the vector embeddings, was being tracked by Git. These are massive binary files that slow down cloning and cause merge conflicts every time the database is updated.

### **Untracked data and enforced .gitignore rules**

1. **Safe Removal:** I used `git rm -r --cached qdrant_data/`. This is a critical command: the `--cached` flag tells Git to stop tracking the files but **does not delete them from my hard drive**.
2. **Permanent Exclusion:** I added `qdrant_data/` to my `.gitignore` to prevent any future ingestion runs from accidentally re-adding binary state to the repo.

---

## 4. ModuleNotFoundError for internal packages

### **Incorrect relative import paths in service layer**

The application crashed with `ModuleNotFoundError: No module named 'core_engine.data_layer.database'`.

- **The Cause:** My folder structure was `core_engine/datasets/`, but my code was trying to import from `core_engine.data_layer`. This happens when refactoring code without updating all import statements.

### **Realigned imports to match actual project structure**

I performed a surgical update on `core_engine/datasets/service.py` to point to the correct internal modules. I learned that whenever this error appears, I should immediately verify the directory names vs. the dots in my import statements.

---

## 5. ValueError: Using device_map="auto" requires 'accelerate'

### **Missing weight orchestration library for GPU loading**

When I tried to load a model directly onto the GPU, the `transformers` library threw an error stating that `accelerate` was required.

- **The Cause:** Even on a single-GPU setup, `device_map="auto"` uses the `accelerate` library to handle the "hooks" that map model weights between your RAM and VRAM.

### **Installed accelerate with CUDA-compatible index strategy**

I added `accelerate` using the same `unsafe-best-match` strategy used for PyTorch. This ensured that the library installed without triggering version conflicts with `numpy`.

---

## 6. Inference Latency & VRAM Constraints (7B vs 1.5B)

### **7B Model too slow and VRAM-heavy for real-time analysis**

I tried running **Qwen 2.5 7B** with 4-bit quantization (NF4).

- **The Problem:** It consumed ~5.0GB of my 6GB VRAM. Because my Windows OS and Chrome use ~1.4GB, the model couldn't fit entirely on the GPU without "swapping" to system RAM.
- **Technical Fail:** I tried to use `llm_int8_enable_fp32_cpu_offload=True` to fix this, but learned that **NF4 (4-bit) does not support CPU offloading** in the `transformers` library. It must be 100% in VRAM or it fails.

### **Prioritized speed by reverting to 1.5B model and enabling GPU Embeddings**

1. **The Switch:** I moved back to **Qwen 2.5 1.5B**. Because it's small, it doesn't need quantization, making it natively faster.
2. **Parallel GPU Usage:** The 1.5B model only uses ~3.5GB of VRAM. This gave me enough "headroom" to move my **EmbeddingService** (`all-MiniLM-L6-v2`) to **CUDA** as well.
3. **The Result:** I achieved "Zero Latency." The search happens on the GPU, and the advice generation starts immediately after, providing a seamless user experience.

---
**Current System Status:** Optimized for NVIDIA RTX 3060 (6GB). All AI services (Search + LLM) are running on CUDA with high efficiency.
