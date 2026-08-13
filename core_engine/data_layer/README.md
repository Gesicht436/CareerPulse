# Data Layer: Semantic Persistence, Retrieval & Degree Filtering

## Technical Stack

- **Vector Database:** Qdrant (Distributed HNSW vector search engine)
- **Database Client:** `qdrant-client` (Python SDK)
- **Local Tensor Cache:** PyTorch Tensor Matrix Cache (`dataset_embeddings_cache.pt`, shape `(5000, 384)`)
- **Validation Layer:** `pydantic` (Strict type checking for job schemas)
- **Data Processing:** `pandas` (Dataset sampling across 1.6M row `job_descriptions.csv`)
- **Embeddings:** `sentence-transformers` (Generating 384-d vectors via SBERT with Section-Aware weighting)
- **Environment:** Docker (Qdrant instance) or PyTorch In-Memory Fallback

---

## Key Progress

- [x] **Collection Schema:** Defined vector parameters (Cosine distance, 384 dimensions).
- [x] **Section-Aware Vector Search:** Weighted hybrid similarity ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$).
- [x] **Educational Degree Filtering:** Degree group matching (`DEGREE_GROUPS`) restricting matches to candidate educational qualifications (`B.Tech`, `B.Sc`, `MBA`, etc.).
- [x] **Local Tensor Cache Matrix:** Pre-computes and caches 5,000 dataset embeddings to disk (`dataset_embeddings_cache.pt`) executing vector search in $< 10\text{ms}$.
- [x] **Stratified Dataset Sampling:** Samples 5,000 diverse real job postings across the 1.6M row Kaggle dataset.
- [x] **Job Data Modeling:** Created Pydantic `JobDescriptionModel` for validated retrieval.
- [x] **Payload & Degree Filtering:** Integrated payload filters for experience levels and degree categories.
- [x] **ETL Ingestion Pipeline:** Developed `scripts/ingest_qdrant.py` for batch dataset ingestion.
- [x] **Singleton Accessor:** Exposed a centralized `data_layer_service` for the engine.

---

## Architectural Deep Dive

### 1. Vector Database & Local Tensor Cache (`service.py`)

The `DataLayerService` handles semantic persistence and vector proximity retrieval.

- **Primary Source (Qdrant)**: Connects to local Qdrant collection `job_descriptions` via Cosine Similarity (`Distance.COSINE`).
- **Secondary Source (PyTorch Tensor Cache Matrix)**: When Qdrant is offline or unpopulated, `_get_dataset_embeddings` loads the pre-computed 384D tensor matrix (`dataset_embeddings_cache.pt`). It computes vector similarities using PyTorch matrix operations (`torch.matmul`) in $< 10\text{ms}$.
- **Section-Aware Hybrid Ranking**: Computes separate SBERT vectors for the candidate's target role headline ($V_{\text{headline}}$) and full resume body ($V_{\text{experience}}$). Blends vector similarities: $\text{Sim}_{\text{blended}} = 0.40 \times \text{Sim}(V_{\text{headline}}, V_{\text{job}}) + 0.60 \times \text{Sim}(V_{\text{experience}}, V_{\text{job}})$.

### 2. Educational Degree Filtering Engine (`DEGREE_GROUPS`)

The `search_jobs` method supports strict educational degree qualification filtering:

- **Degree Groups**: Groups degrees into standardized categories:
  - **Engineering & Tech**: `B.Tech`, `B.E.`, `M.Tech`, `BCA`, `MCA`, `Computer Science`
  - **Science & Research**: `B.Sc`, `M.Sc`, `Ph.D`, `Mathematics`
  - **Business & Commerce**: `B.Com`, `MBA`, `BBA`, `Finance`, `Marketing`
- **Strict Qualification Mode**: When `strict_qualification=True`, filters dataset postings to only include jobs matching the candidate's specific educational background.

---

## Data Lifecycle

1. **Sampling & Ingestion**: Job postings from `job_descriptions.csv` are sampled across 150,000 rows into 5,000 diverse job records.
2. **Indexing & Tensor Cache**: Pre-computes 384D SBERT embeddings saved to `dataset_embeddings_cache.pt` or ingested into Qdrant HNSW vector index.
3. **Querying & Filtering**: When `search_jobs` is called with a resume, it extracts degree qualification, filters dataset postings, and returns top 5 recommendations.
