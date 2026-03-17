# Troubleshooting & Setup Log - March 17, 2026

This document details the technical hurdles encountered during the project setup and the specific steps taken to resolve them.

---

## 1. PyTorch & Torchvision CUDA Recognition

### **The Problem**

When attempting to run the data ingestion script (`scripts/ingest_qdrant.py`), the following errors occurred:

- `RuntimeError: operator torchvision::nms does not exist`
- `ModuleNotFoundError: Could not import module 'PreTrainedModel'`

**Detailed Breakdown:**

- **Architecture Mismatch:** The default `uv` resolution installed the standard PyPI versions of `torch` and `torchvision`. On Windows, these default to CPU-only binaries (`+cpu`).
- **Missing GPU Kernels:** `torchvision::nms` (Non-Maximum Suppression) is a C++ operator. The CPU-only version of `torchvision` lacks the CUDA-compiled kernels required when `torch` attempts to initialize GPU-accelerated operations.
- **Dependency Confusion:** PyTorch maintains its own repository (index) for CUDA-enabled wheels. Standard installers often fail to prioritize this index over the primary PyPI index.

### **The Solution**

1. **Diagnostic Scripting:** Created `diagnose_torch.py` to inspect the internal state of the libraries.
    - *Finding:* `torch.__version__` returned `2.10.0+cpu`.
2. **Index Strategy Configuration:** Added the explicit PyTorch CUDA 13.0 index to `pyproject.toml` as a trusted source:

    ```toml
    [[tool.uv.index]]
    url = "https://download.pytorch.org/whl/cu130"
    ```

3. **Resolving Package Conflicts:**
    - **Python Versioning:** `uv` attempted to resolve dependencies for all possible Python versions (including 3.14). Since CUDA-specific wheels for experimental Python versions are often missing, this caused a resolution failure. We restricted the project to `requires-python = "==3.12.*"`.
    - **MarkupSafe Conflict:** A mismatch occurred where `uv` tried to pull `markupsafe==3.0.3` from the PyTorch index, but it lacked a wheel for Python 3.12. By using `--index-strategy unsafe-best-match`, we allowed `uv` to pick the best compatible version (`3.0.2`) from the primary PyPI index instead.
4. **Explicit Version Pinning:** To guarantee the GPU versions, we modified `dependencies` in `pyproject.toml` to use the `+cu130` suffix:

    ```toml
    dependencies = [
        "torch==2.10.0+cu130",
        "torchvision==0.25.0+cu130",
    ]
    ```

5. **Forced Synchronization:** Ran `uv sync` to rebuild the virtual environment.
6. **Verification:** The final check confirmed:
    - `Torch version: 2.10.0+cu130`
    - `CUDA available: True`
    - `Device: NVIDIA GeForce RTX 3060 Laptop GPU`

---

## 2. Kaggle CLI Authentication

### **Kaggle**

Running `uv run kaggle` resulted in an authentication failure. The CLI expects either a physical `kaggle.json` file in `~/.kaggle/` or specific environment variables.

**Detailed Breakdown:**

- The legacy method requires a JSON file, which is difficult to manage across different development environments.
- The newer "Kaggle API Token" (`KGAT_...`) is intended to be used as a single environment variable, but the CLI sometimes defaults to searching for the file first.

### - **The Solution**

1. **Environment Variable Injection:** Instead of creating a file, we used the `KAGGLE_API_TOKEN` variable.
2. **Dotenv Implementation:** Created a `.env` file to store the token securely within the project:

    ```bash
    KAGGLE_API_TOKEN="KGAT_c6854ce6ed2b1bcb8115a94f8734a1fd"
    ```

3. **CLI Context:** Verified that `uv run` automatically loads the `.env` file into the process environment, allowing the `kaggle` package to authenticate seamlessly without any local configuration files.

---

## 3. Qdrant Data Version Control

## - **Qdrant Data Ingestion**

The `qdrant_data/` directory was being tracked by Git.

**Detailed Breakdown:**

- **Binary Bloat:** Vector databases store data in large `.mmap` and `.dat` files. Committing these makes the Git repository extremely heavy and slow to clone.
- **State Pollution:** Database state is local to the machine. Committing it leads to "dirty" repository states and merge conflicts every time the ingestion script is run.

### **Remove unwanted material**

1. **Index Removal:** Used `git rm -r --cached qdrant_data/`. The `--cached` flag is critical as it removes the files from Git's tracking index while **preserving the actual files on the hard drive**.
2. **Ignore Rule:** Updated `.gitignore` to prevent re-entry:

    ```text
    # Data
    qdrant_data/
    ```

3. **Result:** The vector database now remains local, and the repository only tracks the *scripts* used to generate that data, keeping the codebase lean and reproducible.

---
**Status:** All core engine components are now functional with GPU acceleration and proper environment configuration.
