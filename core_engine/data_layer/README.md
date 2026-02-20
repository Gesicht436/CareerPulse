# Data Layer (`core_engine/data_layer/`)

Responsible for the persistence of both structured relational data and high-dimensional vector embeddings.

---

## 1. Technical Stack

- **Relational DB:** PostgreSQL (User profiles, history, job metadata).
- **Vector DB:** Qdrant (Resume/JD embeddings for semantic search).
- **ORM:** SQLAlchemy or Tortoise ORM.

---

## 2. Key Responsibilities

### **Mayank Anand**

- **Schema Design:** Creating robust migrations for relational user data.
- **Vector Indexing:** Optimizing Qdrant collections for fast semantic retrieval.
- **Data Integrity:** Ensuring consistency between the primary database and the vector store.
- **Backup & Recovery:** Implementing automated database snapshotting.

---

## 3. Key Feature Requirements

1. **Hybrid Search:** Capability to filter by structured metadata (e.g., location, date) while performing semantic vector search.
2. **Automated Migrations:** Using Alembic or similar tools to ensure database schema changes are tracked and reversible.
3. **Optimized Indexing:** Custom HNSW (Hierarchical Navigable Small World) configurations in Qdrant for high-accuracy matching.
4. **Transaction Safety:** Ensuring that resume metadata and its corresponding embeddings are updated atomically.
