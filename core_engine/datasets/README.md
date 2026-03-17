# Data Layer (`core_engine/data_layer/`)

Responsible for the persistence of both structured relational data and high-dimensional vector embeddings.

---

## 1. Technical Stack

- **Relational DB:** PostgreSQL (User profiles, history, job metadata).
- **Vector DB:** Qdrant (Resume/JD embeddings for semantic search).
- **ORM:** SQLAlchemy or Tortoise ORM.

---

## 2. Infrastructure & Ingestion

### **Vector Database (Qdrant)**

We use Qdrant for storing and searching job description embeddings. It runs as a containerized service.

```bash
# Start Qdrant
docker-compose up -d qdrant
```

### **Data Ingestion Pipeline**

1. **Fetch Raw Data:** Ensure `KAGGLE_API_TOKEN` is in `.env`, then run `uv run python scripts/setup_data.py`.
2. **Ingest to Qdrant:** Processes the raw CSV, generates embeddings, and uploads to the `job_descriptions` collection.

```bash
# Run from project root
uv run python scripts/ingest_qdrant.py
```

---

## 3. Key Progress

- [ ] **Qdrant Integration:** Automated collection creation and vector search.
- [ ] **Unified Query API:** Implementation of `query_points` for semantic retrieval.
- [ ] **Batch Ingestion:** Optimized script for bulk uploading job metadata.

---

## 3. Key Feature Requirements

1. **Hybrid Search:** Capability to filter by structured metadata (e.g., location, date) while performing semantic vector search.
2. **Automated Migrations:** Using Alembic or similar tools to ensure database schema changes are tracked and reversible.
3. **Optimized Indexing:** Custom HNSW (Hierarchical Navigable Small World) configurations in Qdrant for high-accuracy matching.
4. **Transaction Safety:** Ensuring that resume metadata and its corresponding embeddings are updated atomically.

## 4. Setup

## 5. Roadmap
