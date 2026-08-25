# CareerPulse Scripts: Automation & Data Pipelines

The `scripts/` directory contains automated dataset acquisition, data preprocessing, high-throughput vector ingestion, interactive inspection, artifact distribution, and technical visualization tools for **CareerPulse**.

---

## 1. Script Directory Overview

| Script | Purpose | Key Dependencies | Speed / Output |
| :--- | :--- | :--- | :--- |
| `setup_data.py` | Automated dataset acquisition from Kaggle | `kaggle`, `python-dotenv` | Downloads 1.62 GB Kaggle dataset |
| `preprocess_dataset.py` | Cleans raw dataset, drops 5 unnecessary columns & normalizes experience | `pandas`, `re` | Processed 1.61M rows in ~40s |
| `inspect_dataset.py` | Interactive terminal dataset explorer, search, and distribution stats | `pandas`, `json` | Instant CLI queries |
| `ingest_full_dataset.py` | High-throughput PyTorch CUDA FP16 ingestion into SQLite & vector matrix | `torch`, `transformers`, `sqlite3` | ~4,630 texts/sec (~5.8 min for 1.61M rows) |
| `package_dataset.py` | Packages `jobs.db` and full vector matrices into a compressed distribution bundle | `zipfile`, `os` | Creates `careerpulse_1.6m_dataset_bundle.zip` |
| `download_precomputed_data.py` | One-click setup script to download precomputed artifacts for teammates | `urllib`, `zipfile` | Sets up full dataset in < 60s |
| `generate_visuals.py` | Generates architectural, RAG pipeline, and VRAM benchmark diagrams | `matplotlib`, `numpy` | High-res figures in `generated_visuals/` |

---

## 2. Script Details & Usage Guide

### 1. Data Acquisition: `setup_data.py`
Automates retrieval of the 1.6M Kaggle job descriptions dataset required to populate the local database:
- **Authentication**: Supports `KAGGLE_API_TOKEN`, `KAGGLE_USERNAME` + `KAGGLE_KEY`, or `~/.kaggle/kaggle.json`.
- **Target Dataset**: `ravindrasinghrana/job-description-dataset`.
- **Destination**: Downloads and extracts archive into `core_engine/datasets/raw/job_descriptions.csv`.

```bash
uv run python scripts/setup_data.py
```

---

### 2. Dataset Preprocessing: `preprocess_dataset.py`
Streams through the 1.61M raw dataset to optimize size and normalize data types:
- **Pruned Columns**: Drops `longitude`, `latitude`, `Job Posting Date`, `Company Size`, and `Benefits`.
- **Experience Normalization**: Converts textual experience ranges (e.g., `"5 to 15 Years"`) using the formula:
  $$\text{Normalized Experience} = \text{round}(\text{average}(\text{numbers in Experience}) \times 1.10)$$
- **Output**: Automatically creates `core_engine/datasets/processed/` and writes [`core_engine/datasets/processed/cleaned_job_descriptions.csv`](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/datasets/processed/cleaned_job_descriptions.csv) (1.39 GB, 18 columns, 1,615,940 rows).

```bash
uv run python scripts/preprocess_dataset.py
```

---

### 3. Interactive Dataset Explorer: `inspect_dataset.py`
Interactive CLI utility to explore cleaned records and verify column integrity:
- View structured records in formatted JSON.
- Search jobs by keyword (Role, Title, Skills).
- View qualifications, normalized experience, and work type distributions.

```bash
uv run python scripts/inspect_dataset.py
```

---

### 4. High-Throughput 1.61M Ingestion Engine: `ingest_full_dataset.py`
Streams all 1.61M jobs into SQLite and compiles the full PyTorch FP16 vector matrix:
- **PyTorch CUDA FP16**: Utilizes `half()`, `torch.inference_mode()`, and TensorFloat-32 (`TF32`).
- **Fast Tokenizer**: Vectorized batch encoding via `AutoTokenizer(use_fast=True)` in batches of 1,024.
- **Throughput**: Processes **~4,630 texts/second** (~5.8 minutes total execution time on an RTX 3060).
- **Outputs**:
  - `core_engine/datasets/jobs.db` (1.78 GB)
  - `core_engine/datasets/embeddings/dataset_embeddings_full.pt` (1.24 GB)
  - `core_engine/datasets/embeddings/dataset_meta_full.pt` (43 MB)
  - `core_engine/datasets/embeddings/cache_checkpoints/` (Intermediate chunk checkpoints)

```bash
uv run python scripts/ingest_full_dataset.py
```

---

### 5. Artifact Distribution: `package_dataset.py` & `download_precomputed_data.py`
Enables seamless "Compute Once, Distribute Everywhere" workflow for teammates:
- **`package_dataset.py`**: Bundles `jobs.db`, `embeddings/dataset_embeddings_full.pt`, and `embeddings/dataset_meta_full.pt` into a single compressed `.zip` for hosting on Hugging Face Hub or GitHub Releases.
- **`download_precomputed_data.py`**: Downloads and extracts the bundle on any teammate's machine in **< 60 seconds** without requiring GPU computation.

```bash
# Package pre-built database & vector matrix (Run once)
uv run python scripts/package_dataset.py

# Download on teammate machine (< 60s setup)
uv run python scripts/download_precomputed_data.py <OPTIONAL_URL>
```

---

### 6. Technical Visualizations: `generate_visuals.py`
Generates high-resolution architecture diagrams for documentation:
- **System Architecture**: High-level component flowchart.
- **Document Pipeline**: Multi-column spatial layout sorting and OCR pipeline.
- **RAG & Scoring Workflow**: SBERT vector cosine similarity and 50/50 ATS calibration.
- **Hardware Benchmarks**: VRAM footprint and query latency charts.

```bash
uv run python scripts/generate_visuals.py
```
