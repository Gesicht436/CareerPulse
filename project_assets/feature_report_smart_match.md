# feat(core): implement semantic matching engine & automated data pipeline

This update establishes the architectural foundation for the **Smart Match Engine** and streamlines the local development environment. By moving from legacy keyword-based matching to **vector-space semantic similarity**, we have realized the core value proposition of CareerPulse.

## Core Features

- **Semantic Match Engine:** A modular FastAPI service that calculates the "meaning distance" between Resumes and JDs using the `all-MiniLM-L6-v2` transformer model.
- **Automated Data Ingestion:** A new script-based pipeline (`setup_data.py`) to fetch and unzip Kaggle datasets directly into the `data_layer`, including automated `.env` credential handling via `python-dotenv`.
- **Robust Schema Design:** Pydantic v2 models for strict request/response validation and clear API contracts for the frontend team.

## Technical Implementation

- **Sentence-Transformers Integration:** Leveraged dense vector embeddings (384-dimensional) to understand context rather than just words.
- **Singleton Service Pattern:** Optimized the `SmartMatchService` to load the AI model into memory once, ensuring subsequent API requests are near-instantaneous (<100ms).
- **Dependency Modernization:** Transitioned the project to `uv` for lightning-fast package management and implemented a modular package structure across the `core_engine`.

## Verification & QA

- **Automated Testing:** Implemented an asynchronous test suite in `quality_assurance/` that confirms the engine correctly differentiates between diverse career paths (e.g., verifying a ~90% match for similar tech roles vs. a ~22% match for unrelated roles).
- **Interactive Documentation:** Verified the endpoint functionality via the FastAPI Swagger UI at `/docs`.

---
**This update moves the project from "Static Structure" to a "Functional AI Prototype."**
