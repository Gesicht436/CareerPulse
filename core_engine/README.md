# Core Engine (`core_engine/`)

The **Core Engine** is the high-performance FastAPI backend of CareerPulse. It orchestrates security audits, semantic matching, and vector-based analysis.

---

## 1. Technical Stack

- **Framework:** FastAPI
- **Python:** 3.12 (managed via `uv`)
- **Parsing:** `pdfplumber` (PDF extraction)
- **AI/NLP:**
  - `spaCy` (PII detection with `en_core_web_sm`)
  - `sentence-transformers` (Vector embeddings on CUDA)
  - `accelerate` (Optimized model loading)
  - `bitsandbytes` (Quantization support)
- **Middleware:** CORSMiddleware enabled for frontend integration.

---

## 2. Key Progress

- [x] **Project Setup:** FastAPI initialized with modular routing.
- [x] **GPU Acceleration:** Fully configured for CUDA 13.0 on NVIDIA RTX 3060.
- [x] **Resume Security:** Implementation of `SecurityService` for adversarial defense.
- [x] **Data Layer (RAG):** Full integration with Qdrant for semantic job search.
- [x] **Explainable AI:** Local LLM (`Qwen2.5-1.5B`) for real-time match feedback.
- [x] **Secure Upload:** Created `/api/v1/security/upload` endpoint with PDF parsing.
- [x] **Shared Services:** Singleton services for Embeddings and LLM inference.

---

## 3. Sub-Modules

- **[`resume_security/`](./resume_security/):** Handles PII detection, hidden text check, and prompt injection defense.
- **[`smart_match/`](./smart_match/):** (Next) RAG-based matching and skill-gap analysis.
- **[`data_layer/`](./data_layer/):** Vector database (Qdrant) and relational storage.

---

## 4. Development Setup

```bash
# Sync dependencies (from project root)
uv sync

# Run the API server with auto-reload from root directory
uv run uvicorn core_engine.main:app --reload
```

Interactive Swagger documentation is available at `http://localhost:8000/docs`.

---

## 5. Roadmap
