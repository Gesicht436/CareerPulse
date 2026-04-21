# CareerPulse: AI-Powered Career Optimization & Semantic Job Matching

**CareerPulse** is a "Private-by-Design" career intelligence platform that leverages local Large Language Models (LLMs) and Vector Databases to provide job seekers with deep, actionable insights into their professional alignment. Unlike traditional ATS systems that rely on rigid keyword matching, CareerPulse understands the **semantic context** of your experience, identifying hidden skill gaps and generating personalized learning roadmaps without your data ever leaving your machine.

---

## Core Value Proposition

In an era of data privacy concerns and automated recruitment bias, CareerPulse offers three foundational pillars:

1. **100% Data Sovereignty**: All AI inference—from vector embeddings to LLM reasoning—happens locally using **Quantized Transformers** (Qwen 2.5). Your resume is never uploaded to external cloud providers like OpenAI or Anthropic.
2. **Semantic-First Alignment**: By using **SBERT (Sentence-BERT)**, the engine recognizes professional equivalence (e.g., understanding that "Cloud Orchestration" is conceptually similar to "Kubernetes Management").
3. **Defensive Intelligence**: A dedicated security layer audits every resume for adversarial "Prompt Injection" and hidden "ATS Hacks," ensuring a clean and honest match.

---

## Unified Technical Stack

The project is architected as a high-performance **Modular Monolith**, split between a specialized AI backend and a modern, utility-first frontend.

### **Backend (Core Engine)**

- **API Framework**: FastAPI (Asynchronous Python 3.12)
- **Vector Intelligence**: Qdrant (High-performance HNSW indexing)
- **Embedding Model**: `all-MiniLM-L6-v2` (384-dimensional semantic vectors)
- **Local LLM**: Qwen 2.5 1.5B/7B (Quantized via `bitsandbytes` NF4)
- **Extraction & Security**: `pdfplumber`, `Tesseract-OCR`, `spaCy` (NER), `OpenCV`

### **Frontend (Web Interface)**

- **Styling**: Tailwind CSS v4 (Utility-first, optimized build pipeline)
- **Logic**: Vanilla ES6+ JavaScript (Zero-dependency, high-speed execution)
- **Architecture**: Static-site generation with dynamic API orchestration.

### **Automation & Ops**

- **Dependency Management**: `uv` (Fastest Python package manager)
- **Visualization**: `matplotlib`, `numpy` (Programmatic technical diagrams)
- **Documentation**: `pandoc` (Cross-format conversion)

---

## Current Project Status

| Milestone | Feature | Status |
| :--- | :--- | :--- |
| **Security** | Layout-aware PDF extraction & PII Redaction | [x] Completed |
| **Security** | OCR Fallback for scanned documents | [x] Completed |
| **Data Layer** | Qdrant Vector DB integration & Job Ingestion | [x] Completed |
| **Matching** | Semantic Scoring via SBERT (Cosine Similarity) | [x] Completed |
| **Intelligence** | Local LLM Integration (Qwen 2.5) with 4-bit quantization | [x] Completed |
| **Web UI** | Responsive Dashboard, Upload Hub, and Search Interface | [x] Completed |
| **Orchestration** | Unified End-to-End Analysis Pipeline (`/analyze`) | [x] Completed |
| **Extended Formats** | Native support for `.docx` and `.txt` ingestion | [ ] Pending |
| **Persistence** | Multi-user Auth & Historical Analysis Tracking | [ ] Pending |
| **Analytics** | Market Trend visualization using real-time job data | [ ] Pending |

---

## Project Structure

```text
CareerPulse/
├── core_engine/                # The Backend Central Nervous System
│   ├── data_layer/             # Qdrant persistence & Pydantic schemas
│   ├── resume_security/        # PDF extraction, Redaction, & Audit
│   ├── smart_match/            # SBERT Scoring & LLM Reasoning
│   ├── embedding_service.py    # Shared SBERT singleton
│   ├── llm_service.py          # Local Qwen 2.5 inference layer
│   └── main.py                 # FastAPI Gateway
├── web_interface/              # Modern Professional Frontend
│   ├── public/                 # HTML templates & static assets
│   │   ├── css/                # Tailwind v4 source & output
│   │   └── js/                 # Vanilla JS logic (api.js, analyzer.js)
│   └── package.json            # Node.js build scripts
├── scripts/                    # Automation & Data Pipelines
│   ├── ingest_qdrant.py        # Vector ETL pipeline
│   ├── setup_data.py           # Automated Kaggle data retrieval
│   └── generate_visuals.py     # Technical diagram generator
├── project_assets/             # Generated visuals & Mid-Sem reports
├── ARCHITECTURE.md             # Master system blueprint
└── README.md                   # You are here
```

---

## Getting Started

Follow these steps to set up the complete CareerPulse environment on your local machine.

### 1. System Prerequisites

Ensure you have the following system-level dependencies installed:

- **Python 3.12+** (We recommend the `uv` package manager).
- **Node.js 20+** (For frontend styling).
- **Tesseract-OCR**: Required for processing scanned PDFs.
- **Poppler**: Required for PDF rasterization.
- **Docker**: To run the Qdrant vector database.

```bash
winget install --id Nvidia.CUDA --version 13.0
winget install Docker.DockerDesktop
uv install python 3.12
winget install CoreyButler.NVMforWindows
nvm install latest
```

### 2. Backend Setup (Core Engine)

```bash
# 1. Configure environment variables
# Copy .env.example to .env and update your Kaggle credentials
cp .env.example .env

# 2. Install Python dependencies and sync environment
uv sync

# 3. Download the spaCy NLP model
uv run python -m spacy download en_core_web_sm
```

### 3. Data Acquisition & Database Initialization

Follow this specific sequence to prepare the local job database:

```bash
# 1. Download the 2025 job description dataset from Kaggle
uv run python scripts/setup_data.py

# 2. Build and start the Qdrant vector database container
docker-compose up --build -d

# 3. Embed and ingest the job data into the running Qdrant instance
uv run python scripts/ingest_qdrant.py
```

### 4. Frontend Setup (Web Interface)

```bash
cd web_interface
npm install
# Start the development server (CSS watch + Live Server)
npm run dev
```

### 5. Launch the Engine

In a new terminal window:

```bash
# Return to root
cd ..
# Launch the FastAPI server
uv run uvicorn core_engine.main:app --reload
```

Your application will be live at `http://localhost:3000`, communicating with the backend at `http://localhost:8000`.

---

## The Team

- **Mayank Anand**: Team Lead, Architecture, LLM Inference & UX Refinement.
- **Abhinav Anand (285)**: Frontend Core, API Orchestration & Dashboard Logic.
- **Harsh Anand**: UI/UX Structure & Tailwind Implementation.
- **Abhinav Anand (08)**: Data Engineering & Vector Persistence.
- **Ankit Anand**: Security Auditing & Performance Benchmarking.
