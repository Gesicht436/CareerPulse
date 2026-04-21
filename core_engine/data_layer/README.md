# Data Layer: Semantic Persistence & Retrieval

## Technical Stack

- **Vector Database:** Qdrant (Distributed vector search engine)
- **Database Client:** `qdrant-client` (Python SDK)
- **Validation Layer:** `pydantic` (Strict type checking for job schemas)
- **Data Processing:** `pandas` (ETL for raw job description datasets)
- **Embeddings:** `sentence-transformers` (Generating 384-d vectors via SBERT)
- **Environment:** Docker (Qdrant instance management)

---

## Key Progress

- [x] **Collection Schema:** Defined optimized vector parameters (Cosine distance, 384 dimensions).
- [x] **Connection Management:** Implemented idempotent initialization and connection pooling.
- [x] **Job Data Modeling:** Created Pydantic `JobDescriptionModel` for validated retrieval.
- [x] **Semantic Search:** Built the core search service using vector proximity queries.
- [x] **Metadata Filtering:** Integrated payload filters for experience levels and categories.
- [x] **ETL Pipeline:** Developed `ingest_qdrant.py` for batch CSV dataset ingestion.
- [x] **Singleton Accessor:** Exposed a centralized `data_layer_service` for the engine.
- [ ] **Hybrid Retrieval:** Integration of full-text keyword search with vector similarity.
- [ ] **Real-time Indexing:** API endpoint for instant job posting and embedding updates.
- [ ] **Data Versioning:** Multi-collection support for A/B testing different embedding models.

The **Data Layer** serves as the foundation for CareerPulse's job-matching capabilities. Unlike traditional recruitment platforms that rely on brittle keyword matching (SQL `LIKE` queries or Elasticsearch term frequencies), this module implements a **Vector-First Retrieval System** powered by **Qdrant**. This allows the engine to understand that a resume mentioning "Deep Learning" is highly relevant to a job description asking for "Neural Networks," even if the exact strings do not match.

## Architectural Deep Dive

### 1. The Vector Database: Qdrant (`database.py`)

The `database.py` module acts as the low-level connector to the Qdrant instance. It is designed to be self-healing and idempotent.

- **Client Initialization**: It initializes a `QdrantClient` using environment variables (`QDRANT_HOST`, `QDRANT_PORT`). In a production environment, this could easily point to a Qdrant Cloud cluster or a distributed Docker setup.
- **Collection Management**: The `init_qdrant()` function is critical. It doesn't just check for a connection; it inspects the existing collections. If the `job_descriptions` collection is missing, it creates it with specific **VectorParams**.
- **Distance Metrics**: We utilize **Cosine Similarity** (`Distance.COSINE`). In the context of high-dimensional embeddings, Cosine similarity is superior to Euclidean distance because it measures the *angle* between vectors rather than their magnitude. This is essential for resumes and job descriptions which may vary significantly in length but share the same semantic direction.
- **Vector Dimensions**: The `VECTOR_SIZE` is strictly locked to **384**. This matches the output layer of our `all-MiniLM-L6-v2` transformer model. If the model is upgraded to a larger variant (like `all-mpnet-base-v2`), this constant must be updated to 768.

### 2. Data Modeling: Pydantic Schemas (`schemas.py`)

The `schemas.py` file defines the contract between the database and the rest of the application.

- **`JobDescriptionModel`**: This model captures more than just the raw text. It includes structured fields like `skills` (a `List[str]`) and `location`. By using Pydantic, we ensure that every piece of data retrieved from the database is validated. If a document in Qdrant is missing a mandatory field like `title`, the service layer will raise a validation error before the bad data can reach the LLM or the frontend.

### 3. Retrieval Service: Semantic Search (`service.py`)

The `DataLayerService` is where the high-level search logic resides.

- **Embedding Integration**: The `search_jobs` method takes a raw string (which could be a short search query or a 10-page resume) and passes it to the `embedding_service`. This transforms the text into a 384-dimensional floating-point array.
- **The Query Mechanism**: Instead of traditional filters, we use `qdrant.query_points`. This method performs a "Nearest Neighbor" search. It scans the `job_descriptions` collection for vectors that are mathematically closest to the query vector.
- **Payload Filtering**: Despite being a vector DB, Qdrant allows for "Filtering Search." In `service.py`, we implement a dynamic filter for `experience_level`. If a user specifies "Senior," the engine restricts the vector search to only those points where the metadata (payload) matches "Senior," ensuring we don't suggest internship roles to veteran engineers.
- **Mapping Logic**: The raw results from Qdrant (`ScoredPoint` objects) are unstructured. The service manually maps these results back into `JobDescriptionModel`. This decoupling ensures that even if we change our database provider (e.g., to Milvus or Weaviate), the internal API for the rest of the engine remains unchanged.

## Data Lifecycle

1. **Ingestion**: Job descriptions are processed by the `scripts/ingest_qdrant.py` utility. Each description is embedded and stored with its metadata (title, company, skills) in the Qdrant payload.
2. **Indexing**: Qdrant builds an HNSW (Hierarchical Navigable Small World) index, allowing for sub-millisecond retrieval even across millions of job postings.
3. **Querying**: When `search_jobs` is called, the vector representation of the resume acts as the "search needle," and the HNSW index quickly identifies the most relevant "haystack" items.

## Performance Considerations

By using a singleton `data_layer_service`, we maintain a persistent connection pool to Qdrant. This avoids the overhead of handshaking for every search request, which is vital for the responsiveness of the `SmartMatch` module.
