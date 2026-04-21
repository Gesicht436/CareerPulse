# CareerPulse Core Engine: High-Performance Resume Intelligence

## 1. Technical Stack

- **Framework:** FastAPI (High-performance API layer)
- **Python:** 3.12 (managed via `uv` for reproducible builds)
- **Parsing:** `pdfplumber`, `pytesseract`, `pdf2image` (Hybrid extraction)
- **Vector Database:** Qdrant (Semantic persistence)
- **AI/NLP:**
  - `spaCy` (PII detection & Named Entity Recognition)
  - `sentence-transformers` (SBERT for vector embeddings)
  - `transformers` (Local LLM inference via Qwen 2.5)
  - `bitsandbytes` (4-bit quantization for GPU efficiency)
- **Middleware:** CORSMiddleware for secure frontend-to-backend communication.

---

## 2. Key Progress

- [x] **Project Architecture:** Modular monolith structure with decoupled service layers.
- [x] **Service Orchestration:** Singleton pattern for high-VRAM AI model instances.
- [x] **Security Guardrails:** Integrated PII redaction and prompt injection defense.
- [x] **RAG Implementation:** Retrieval-Augmented Generation using Qdrant vector search.
- [x] **Local AI Inference:** Full support for 4-bit quantized local LLM execution.
- [x] **OCR Pipeline:** Automated fallback to Tesseract for scanned PDF documents.
- [x] **Unified API:** Single `/analyze` endpoint for end-to-end resume intelligence.
- [ ] **Extended Format Support:** Native ingestion of `.docx` and `.txt` files.
- [ ] **User Persistence:** Multi-user session management and analysis history.
- [ ] **Horizontal Scaling:** Support for distributed worker nodes via Celery/Redis.
The **Core Engine** is the central nervous system of CareerPulse, a next-generation career optimization platform. Built with **FastAPI**, **Transformers**, and **Qdrant**, the engine is designed to bridge the gap between candidate qualifications and complex job market requirements. It leverages state-of-the-art Natural Language Processing (NLP) to provide a private, secure, and highly accurate job-matching experience that runs entirely on local infrastructure.

## Architectural Philosophy

The Core Engine follows a **Modular Monolith** architecture. While it is deployed as a single FastAPI application, the internal logic is strictly decoupled into independent domains:

1. **Ingestion Layer**: Handles raw data conversion (PDF to structured text).
2. **Security Layer**: Ensures data privacy and system integrity.
3. **Persistence Layer**: Manages vector-based semantic search.
4. **Inference Layer**: Orchestrates local AI models (Embeddings & LLMs).
5. **API Layer**: Exposes the unified `/analyze` and matching endpoints.

This modularity ensures that the engine is **Hardware-Agile**. It can run on a high-end NVIDIA GPU for maximum throughput or fall back to an optimized CPU-only mode for lightweight deployments.

---

## The Unified Analysis Pipeline

When a user uploads a resume, the engine triggers a complex, non-linear pipeline to ensure the best possible match result.

### 1. Secure Extraction

The `resume_security` module receives the file. It first attempts a layout-preserved extraction using `pdfplumber`. If the document appears to be a scanned image, it triggers an **OCR Fallback** using Tesseract. Simultaneously, it scans the document for "Hidden Text" (White-on-White characters), which is a common trick used to manipulate ATS scores.

### 2. Privacy Redaction

The raw text is never sent to the LLM directly. Instead, a **Named Entity Recognition (NER)** model (spaCy) identifies sensitive data like candidate names, personal phone numbers, and private emails. These are replaced with semantic tokens (e.g., `[PERSON]`). This ensures that the career advice generated is completely unbiased and privacy-compliant.

### 3. Semantic Search & Candidate Ranking

The redacted text is converted into a 384-dimensional vector embedding. The engine performs a **Vector Similarity Search** against the Qdrant database, which contains thousands of indexed job descriptions. This stage returns the top-K jobs that are "conceptually similar" to the candidate's profile, even if they don't share exact keywords.

### 4. LLM-Powered Qualitative Analysis

For each top-ranked job, the engine invokes the **Local LLM** (Qwen 2.5). The LLM is provided with the candidate's experience and the job's requirements. It generates a structured report including a justification for the match, a skill gap analysis, and a personalized 4-week career roadmap to help the candidate become the perfect fit.

---

## Service Deep Dives

### `embedding_service.py` (The Mathematical Foundation)

This service is a shared singleton that manages the `SentenceTransformer` model.

- **Model**: `all-MiniLM-L6-v2`. Chosen for its perfect balance between speed and semantic accuracy.
- **Device Placement**: Automatically detects CUDA. If a GPU is present, it moves the model to VRAM, enabling near-instant vector generation.
- **Caching**: The model is loaded once into memory on startup, ensuring zero latency for subsequent requests.

### `llm_service.py` (The Intelligence Layer)

This service manages the lifecycle of the local Large Language Model.

- **Model Selection**: Supports `Qwen/Qwen2.5-1.5B-Instruct` for speed or the `7B` variant for higher reasoning quality.
- **Quantization**: Implements **4-bit quantization** via `bitsandbytes` (NF4). This allows the 7B model to run on consumer-grade GPUs with as little as 6GB of VRAM without significant loss in reasoning capability.
- **Prompt Engineering**: Uses a sophisticated system prompt that enforces **Strict JSON Output**. This eliminates the "hallucination" issues common with LLMs, ensuring the frontend always receives valid data for the dashboard.

### `main.py` (The Gateway)

The entry point of the engine. It handles:

- **FastAPI Lifecycle**: Initializes the database and warms up the AI models on startup.
- **CORS Configuration**: Securely manages cross-origin requests from the web dashboard.
- **Unified Endpoint**: The `/api/v1/analyze` endpoint coordinates the entire workflow across all sub-services in a single, atomic operation.

---

## How to Run the Core Engine

### 1. Prerequisites

Ensure you have the following installed on your system:

- **Python 3.10+**: We recommend using a virtual environment (`venv` or `uv`).
- **Tesseract-OCR**: Install via your OS package manager (`apt install tesseract-ocr` on Linux or `brew install tesseract` on Mac).
- **Poppler**: Required for PDF image conversion.
- **Qdrant**: The easiest way is via Docker: `docker run -p 6333:6333 qdrant/qdrant`.

### 2. Installation

Using `uv` (recommended for speed and reproducibility):

```bash
# 1. Configure environment variables
# Copy .env.example to .env and update your Kaggle credentials
cp .env.example .env

# 2. Install Python dependencies and sync environment
uv sync

# 3. Download the spaCy NLP model
uv run python -m spacy download en_core_web_sm
```

### 3. Database Initialization & Data Ingestion

Follow this sequence to set up the semantic search foundation:

```bash
# 1. Acquire the job description dataset from Kaggle
uv run python scripts/setup_data.py

# 2. Build and start the Qdrant containerized environment
docker-compose up --build -d

# 3. Process, embed, and ingest job data into Qdrant
uv run python scripts/ingest_qdrant.py
```

### 4. Launching the Engine

Start the FastAPI server using Uvicorn with 'uv run':

```bash
uv run uvicorn core_engine.main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the interactive Swagger documentation at `http://localhost:8000/docs`.

---

## Performance & Hardware Optimization

The Core Engine is designed to scale with your hardware:

- **Minimal (CPU-only)**: Requires 8GB RAM. Uses `all-MiniLM-L6-v2` and the `1.5B` LLM. Ideal for local testing and basic analysis.
- **Recommended (GPU)**: NVIDIA GPU with 6GB+ VRAM (RTX 3060 or better). Enables 4-bit quantization and significantly faster matching speeds.
- **Production (Enterprise)**: Dual GPU setup or high-VRAM A100/H100 instances. Supports full-precision `7B` or `14B` models for ultra-high accuracy.

## Security & Privacy Standards

- **Local Inference**: No data is ever sent to OpenAI, Anthropic, or any third-party cloud provider. Your resume stays on your machine.
- **Input Sanitization**: Every file upload is validated for type, size, and content.
- **PII Scrubbing**: Automatic redaction of sensitive identifiers before LLM processing.
- **Audit Logs**: The engine generates detailed security reports for every processed file, identifying potential risks like prompt injection or hidden text.

## Roadmap

- [ ] Support for `.docx` and `.txt` file formats.
- [ ] Multilingual support for global job markets.
- [ ] Integration with LinkedIn API for automated profile ingestion.
- [ ] Real-time job market trend analysis.
