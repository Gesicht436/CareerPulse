# Local Datasets & Tensor Embeddings Cache

The `core_engine/datasets` directory stores local job description databases, raw Kaggle dataset archives, and pre-computed PyTorch vector embedding matrices for **CareerPulse**.

---

## 1. Directory Structure

```text
core_engine/datasets/
├── README.md                       # Subsystem documentation (this file)
├── jobs.db                         # Embedded SQLite database storing structured job records
├── dataset_embeddings_cache.pt     # Pre-computed 5,000 x 384 PyTorch tensor embeddings matrix
└── raw/
    └── job_descriptions.csv        # 1.6M row raw Kaggle job descriptions dataset
```

---

## 2. Component Specifications

### 1. `jobs.db` (Embedded SQLite Database)
- Standard library `sqlite3` database table `jobs` containing parsed and structured job postings:
  - `id` (TEXT PRIMARY KEY)
  - `title`, `company`, `location`, `country`
  - `description`, `skills` (JSON serialized string)
  - `experience`, `qualifications`, `salary_range`, `work_type`
- Eliminates external database containers while delivering $< 5\text{ms}$ record lookups.

### 2. `dataset_embeddings_cache.pt` (Pre-Computed PyTorch Tensor Matrix)
- Serialized PyTorch tensor dictionary containing:
  - `embeddings`: Tensor of shape `torch.Size([5000, 384])` containing normalized SBERT (`all-MiniLM-L6-v2`) vectors for the 5,000 sampled job descriptions.
  - `job_ids`: List of corresponding unique job identifiers.
- Enables sub-10ms semantic cosine similarity matrix multiplication on GPU (`torch.matmul`) or CPU fallback.

### 3. `raw/job_descriptions.csv` (Raw Dataset)
- Acquired via `scripts/setup_data.py` from Kaggle (`adityarajsrv/job-descriptions-2025-tech-and-non-tech-roles`).
- Contains ~1.6 million real-world tech and non-tech job descriptions across global tech hubs.
