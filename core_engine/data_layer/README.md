# Data Layer: Zero-Docker Persistence, Section-Aware Retrieval & Degree Filtering

The `core_engine/data_layer` module provides high-speed semantic job retrieval, local database persistence, and educational degree filtering for **CareerPulse**. It eliminates external vector database containers by leveraging an embedded **SQLite** store (`jobs.db`) and a pre-computed **PyTorch Tensor Embeddings Matrix** (`dataset_embeddings_cache.pt`).

---

## 1. Technical Stack

- **Embedded Database:** SQLite3 (`jobs.db` via standard library `sqlite3`)
- **Local Vector Cache:** PyTorch Tensor Matrix Cache (`dataset_embeddings_cache.pt`, shape `(5000, 384)`)
- **Semantic Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`, 384-dimensional vectors with batch query encoding)
- **Data Modeling:** Pydantic (`JobDescriptionModel` with strict schema validation)
- **Dataset Ingestion:** `pandas` (Automated stratified sampling of 5,000 diverse job postings from the 1.6M row Kaggle dataset)
- **Error Policy:** Explicit exception propagation (`FileNotFoundError`, `RuntimeError`, `ValueError`)

---

## 2. Key Capabilities & Progress

- [x] **Zero-Docker Embedded Persistence**: Uses standard library `sqlite3` to store structured job descriptions (`jobs.db`), ensuring zero Docker or container dependencies.
- [x] **Sub-10ms Vector Matrix Search**: Pre-computes and caches 5,000 dataset embeddings into a `(5000, 384)` PyTorch tensor matrix (`dataset_embeddings_cache.pt`) executed via GPU/CPU matrix multiplication (`torch.matmul`).
- [x] **Batch SBERT Query Encoding**: Encodes headline and full text simultaneously in a single forward pass (`batch_size=2`) to minimize tensor overhead.
- [x] **Section-Aware Weighted Hybrid Retrieval**: Blends separate SBERT vectors for the target role headline ($V_{\text{headline}}$) and full resume body ($V_{\text{experience}}$):
  $$\text{Sim}_{\text{blended}} = 0.40 \times \text{Sim}(V_{\text{headline}}, V_{\text{job}}) + 0.60 \times \text{Sim}(V_{\text{experience}}, V_{\text{job}})$$
- [x] **Educational Degree Group Filtering (`DEGREE_GROUPS`)**: Enforces strict degree relevance (`B.Tech`, `B.Sc`, `MBA`, `MCA`, etc.) to prevent cross-discipline job mismatches.
- [x] **Strict Failure Policies**:
  - Unseeded database without dataset CSV raises `FileNotFoundError`.
  - Zero matching jobs under strict qualification filter raises `ValueError`.
- [x] **Stratified Sampling Pipeline**: Automatically samples 5,000 balanced job records across 150,000 rows from `job_descriptions.csv`.
- [x] **Centralized Service Singleton**: Exposes `data_layer_service` for seamless consumption across the backend.

---

## 3. Directory Structure

```text
core_engine/data_layer/
├── README.md       # Subsystem documentation (this file)
├── __init__.py     # Package marker
├── database.py     # SQLite connection manager, table schema creation, CRUD queries
├── schemas.py      # JobDescriptionModel Pydantic validation schema
└── service.py      # DataLayerService, section-aware hybrid ranking & degree filtering
```

---

## 4. Architectural Deep Dive

### 1. SQLite Database Management (`database.py`)
- **Table Schema (`jobs`)**:
  - `id` (TEXT PRIMARY KEY)
  - `title`, `company`, `location`, `country`
  - `description`, `skills` (JSON string list)
  - `experience`, `qualifications`, `salary_range`, `work_type`
- **Helper Functions**: `init_db()`, `save_jobs(jobs)`, `fetch_all_jobs()`, `fetch_job_by_id(job_id)`.

### 2. PyTorch Tensor Matrix Search (`service.py`)
- `_get_dataset_embeddings(jobs)`: Loads or computes the `(5000, 384)` PyTorch float32 tensor matrix.
- `search_jobs(query_text, limit, qualification, strict_qualification)`:
  1. Extracts headline and body vectors in a single batch call via `EmbeddingService`.
  2. Applies `DEGREE_GROUPS` filtering against job qualification metadata.
  3. Raises `ValueError` if 0 jobs match the candidate's degree.
  4. Computes section-aware cosine similarity in parallel using PyTorch matrix operations.
  5. Returns top $K$ ranked `JobDescriptionModel` instances.

### 3. Degree Group Mapping (`DEGREE_GROUPS`)
- **Engineering & Tech**: `b.tech`, `b.e`, `m.tech`, `bca`, `mca`, `engineering`, `computer science`
- **Science & Research**: `b.sc`, `m.sc`, `ph.d`, `phd`, `science`, `mathematics`, `physics`
- **Business & Commerce**: `b.com`, `mba`, `bba`, `m.com`, `business`, `finance`, `marketing`
- **General**: `bachelor`, `master`, `degree`, `diploma`, `graduate`

---

## 5. Data Lifecycle

1. **Auto-Seeding**: If `jobs.db` is empty on startup, `DataLayerService` automatically parses and samples records from `core_engine/datasets/raw/job_descriptions.csv` and saves them to `jobs.db`.
2. **Embedding Cache**: Pre-computes 384D SBERT embeddings saved to `core_engine/datasets/dataset_embeddings_cache.pt`.
3. **High-Speed Querying**: When matching a resume, the service filters eligible candidates and performs GPU/CPU tensor cosine similarity in $< 10\text{ms}$.
