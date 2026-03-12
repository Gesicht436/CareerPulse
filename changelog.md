# Changelog - CareerPulse Core Engine (Smart Match Foundation)

This document records the updates, technical decisions, and implementations made to the **CareerPulse** project to establish the Smart Match Engine.

---

## [2026-03-12] - Smart Match Engine Initialization

### 1. Project Infrastructure & Package Setup

- **Changes:** Created `core_engine/main.py`, `core_engine/__init__.py`, and `core_engine/smart_match/__init__.py`.
- **How:** Used standard Python package initialization and FastAPI boilerplating.
- **Why:**
  - Established the **Core Engine** as the central API gateway.
  - `__init__.py` files ensure the directory structure is recognized as a modular Python package, allowing for clean imports across the project.
- **Result:** A functioning FastAPI application reachable at `http://localhost:8000`.

### 2. Dependency Modernization

- **Changes:** Updated `pyproject.toml` with `sentence-transformers`, `qdrant-client`, `httpx`, and `pytest-asyncio`.
- **How:** Executed via `uv add` to ensure deterministic dependency resolution and locking.
- **Why:**
  - **`sentence-transformers`**: Essential for moving beyond "keyword matching" to true "semantic matching" using high-dimensional vector embeddings.
  - **`qdrant-client`**: Prepares the system for the RAG (Retrieval-Augmented Generation) pipeline by providing the interface for the Vector Database.
  - **`httpx` & `pytest-asyncio`**: Required for testing asynchronous FastAPI endpoints and services.
- **Result:** A production-ready environment capable of running advanced NLP models.

### 3. Smart Match Module Implementation

- **Changes:** Implemented `schemas.py`, `router.py`, and `service.py` within `core_engine/smart_match/`.
- **How:**
  - **Schemas:** Utilized `Pydantic v2` for strict type validation of inputs (Resume + JD text) and outputs (Scores + Justifications).
  - **Router:** Created a modular `APIRouter` to isolate matching logic from other engine components (like security or data).
  - **Service:** Implemented the `SmartMatchService` using the `all-MiniLM-L6-v2` model.
- **Why:**
  - **Semantic Similarity:** By encoding text into vectors and calculating **Cosine Similarity**, the engine can understand that "Python Expert" and "Software Engineer with 5 years of Python experience" are nearly identical, even if the words differ.
  - **Singleton Pattern:** Initialized the service as a singleton to ensure the NLP model is loaded into memory only once, significantly reducing API latency for subsequent requests.
- **Result:** A functional REST endpoint (`POST /api/v1/smart-match/match`) that returns a semantic match score between 0-100%.

### 4. Quality Assurance & Validation

- **Changes:** Created `quality_assurance/test_smart_match.py`.
- **How:** Developed an asynchronous test suite using `pytest` to simulate real-world API interactions.
- **Why:**
  - **Empirical Verification:** Proved the "Smart" part of the engine by testing two edge cases:
    - **Positive Case:** A developer resume vs. a developer JD (Resulted in **~89.8%** match).
    - **Negative Case:** A professional chef resume vs. a developer JD (Resulted in **~22.1%** match).
- This confirms the engine correctly differentiates between diverse career paths without relying on exact word overlaps.
- **Result:** A verified, stable core for the matching engine.

### 5. Technical Adjustments (Python 3.14 Compatibility)

- **Changes:** Removed `spaCy` from the initial matching service and refactored to use `sentence-transformers` exclusively.
- **How:** Modified `service.py` to remove `spacy.load()` calls.
- **Why:** `spaCy` currently has a compatibility issue with Python 3.14's Pydantic V1 bridge. To maintain the "Logic First" philosophy, the transition to `sentence-transformers` was accelerated as it provides superior semantic accuracy for the RAG pipeline while avoiding the version conflict.
- **Result:** A stable, error-free runtime on the latest Python version.

---

**Current Status:** The "Semantic Matching" foundation is complete. The system is ready for **RAG integration** (retrieving real JDs from Qdrant) and **Local LLM integration** (generating explainable reports).
