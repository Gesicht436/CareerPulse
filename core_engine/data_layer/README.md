# Data Layer: Zero-Docker Persistence, Section-Aware Retrieval & 1.61M Vector Matrix

The `core_engine/data_layer` module provides high-speed semantic job retrieval, local database persistence, and educational degree filtering for **CareerPulse**. It eliminates external vector database containers by leveraging an embedded **SQLite** store (`jobs.db`, 1.78 GB) and an in-memory **PyTorch Float16 Tensor Embeddings Matrix** (`embeddings/dataset_embeddings_full.pt`, shape `(1615940, 384)`, ~1.24 GB).

---

## 1. Technical Stack

- **Embedded Database:** SQLite3 (`jobs.db` via standard library `sqlite3` in WAL mode with B-Tree indexes)
- **Local Vector Matrix:** PyTorch FP16 Tensor Matrix (`embeddings/dataset_embeddings_full.pt`, shape `(1615940, 384)`) + Degree Bitmask Tensor (`embeddings/dataset_meta_full.pt`, shape `(1615940,)`)
- **Semantic Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`, 384-dimensional vectors with batch query encoding)
- **Data Modeling:** Pydantic (`JobDescriptionModel`, `CompanyProfileModel` with strict schema validation)
- **Dataset Scale:** Direct in-memory operations across **1,615,940 jobs** (1.61M records)
- **Error Policy:** Explicit exception propagation (`FileNotFoundError`, `RuntimeError`, `ValueError`) with zero mock fallbacks

---

## 2. Key Capabilities & Architecture

- [x] **Zero-Docker Embedded Persistence**: Uses standard library `sqlite3` (`jobs.db`) to store 1.61M structured job descriptions with WAL mode and indexed primary keys.
- [x] **Sub-250ms Vector Matrix Search across 1.61M Rows**: Evaluates cosine similarities across all 1.61M vectors simultaneously using GPU/CPU matrix multiplication (`torch.matmul`) without allocating Python objects for non-winning rows.
- [x] **Batch SBERT Query Encoding**: Encodes headline and full resume text simultaneously in a single forward pass (`batch_size=2`) to minimize tensor overhead.
- [x] **Section-Aware Weighted Hybrid Retrieval**: Blends separate SBERT vectors for the target role headline ($V_{\text{headline}}$) and full resume body ($V_{\text{experience}}$):
  $$\text{Sim}_{\text{blended}} = 0.40 \times \text{Sim}(V_{\text{headline}}, V_{\text{job}}) + 0.60 \times \text{Sim}(V_{\text{experience}}, V_{\text{job}})$$
- [x] **Pre-Tagged Degree Bitmask Filtering (`DEGREE_GROUPS` & `DEGREE_CODE_MAP`)**: Enforces strict degree relevance (`Engineering: 1`, `Business: 2`, `Arts: 3`, `Research: 4`) using GPU tensor masking in $< 1\text{ms}$.
- [x] **Indexed Batch SQLite Retrieval**: Uses `fetch_jobs_by_ids([id1, id2, id3, id4, id5])` to fetch only the 5 winning records from SQLite in $< 2\text{ms}$.
- [x] **Strict Failure Policies**:
  - Missing vector matrix or SQLite database raises explicit `FileNotFoundError`.
  - Zero matching jobs under strict qualification filter raises `ValueError`.
- [x] **Centralized Service Singleton**: Exposes `data_layer_service` for seamless consumption across the backend.

---

## 3. Directory Structure

```text
core_engine/data_layer/
├── README.md       # Subsystem documentation (this file)
├── __init__.py     # Package marker
├── database.py     # SQLite connection manager, 18-column table schema, WAL mode, CRUD & batch queries
├── schemas.py      # JobDescriptionModel & CompanyProfileModel Pydantic schemas
└── service.py      # DataLayerService, 1.61M vector ranking & degree bitmask filtering
```

---

## 4. Architectural Deep Dive

### 1. SQLite Database Management (`database.py`)
- **Table Schema (`jobs`)**:
  - `id` (TEXT PRIMARY KEY)
  - `title`, `role`, `company`, `location`, `country`, `work_type`
  - `experience` (INTEGER: normalized years)
  - `qualifications`, `salary_range`
  - `skills` (JSON string list)
  - `responsibilities`, `description`
  - `job_portal`, `preference`, `contact_person`, `contact`
  - `company_profile` (JSON string: Sector, Industry, Website, CEO, etc.)
- **Performance Features**:
  - `PRAGMA journal_mode = WAL` & `PRAGMA synchronous = NORMAL`.
  - B-Tree indexes on `qualifications` and `role`.
- **Key Functions**:
  - `init_db()`: Initializes database and runs automatic column migrations.
  - `save_jobs(jobs)`: Parameterized batch insert.
  - `fetch_jobs_by_ids(job_ids)`: High-speed indexed batch retrieval.
  - `fetch_job_by_id(job_id)` & `fetch_all_jobs()`.

### 2. PyTorch Tensor Matrix Search (`service.py`)
- `_ensure_dataset_loaded()`: Loads the `(1615940, 384)` PyTorch Float16 tensor matrix into memory along with `job_ids` and `degree_codes` bitmask tensor.
- `search_jobs(query_text, limit, qualification, strict_qualification)`:
  1. Generates 384D query embeddings for headline ($V_{\text{head}}$) and full resume text ($V_{\text{full}}$).
  2. Applies `DEGREE_CODE_MAP` bitmasking on GPU tensor if `strict_qualification=True`.
  3. Executes parallel matrix multiplication:
     $$\text{Blended Score} = 0.40 \times (\mathbf{M} \cdot V_{\text{head}}) + 0.60 \times (\mathbf{M} \cdot V_{\text{full}})$$
  4. Runs `torch.topk(..., k=5)` to extract top 5 winning job IDs in $\sim 1.5\text{ms}$.
  5. Calls `fetch_jobs_by_ids(winning_ids)` to retrieve full structured records from SQLite.

### 3. Degree Group Mapping (`DEGREE_GROUPS` & `DEGREE_CODE_MAP`)
- **1: Engineering & Tech**: `b.tech`, `m.tech`, `bca`, `mca`, `b.e`, `computer science`, `engineering`
- **2: Business & Commerce**: `mba`, `bba`, `b.com`, `m.com`, `business`, `finance`, `marketing`, `management`
- **3: Arts & Humanities**: `ba`, `bachelor of arts`, `arts`, `humanities`
- **4: Research & Doctorate**: `phd`, `ph.d`, `doctorate`, `research`

---

## 5. Performance Benchmarks (1.61M Scale)

| Metric | Measured Benchmark Performance |
| :--- | :--- |
| **Total Jobs Indexed** | **1,615,940 jobs** |
| **Vector Matrix Dimensions** | `(1615940, 384)` Float16 (~1.24 GB) |
| **RAM / VRAM Footprint** | **~1.24 GB** (Zero Python object overhead) |
| **Warm Vector Search Latency** | **204.92 ms** (Sub-second response across 1.61M jobs) |
| **Filtered Candidates Scanned** | 645,761 Engineering jobs scanned in $< 100\text{ms}$ |
| **Top-5 Record SQLite Fetch** | **$< 2\text{ ms}$** via primary key index |
| **Docker / Vector DB Containers** | **0 (Zero Docker Dependencies)** |
